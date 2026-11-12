#!/usr/bin/env python3
"""Merge map/verify/judge outputs into repo/data/<overlay>-{steps,displays}-mapping.json."""
import json,os,glob,sys
ROOT=__import__('os').environ.get('TG_COMPANION',__import__('os').path.expanduser('~/tg-companion'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import check
S=check.S; TG=check.TG
R=os.path.join(ROOT,'repo/data/')
P='192ca57362fa3ee737cd83205cb9ea99526c4553'
ML='56a005855ea17e0b0958f73ec801ae140b0a1679'
idx=check.byname
_lines={}
def flines(f):
    if f not in _lines: _lines[f]=open(TG+f).read().split('\n')
    return _lines[f]
def module_of(f):
    if f.startswith('.lake/packages/mathlib/'): f=f[len('.lake/packages/mathlib/'):]
    return f[:-5].replace('/','.')
def norm_end(e,nomatch):
    d=e['declaration']; f=e.get('file','')
    out={'declaration':d}
    if f.startswith('.lake/packages/mathlib'):
        v=check.mlidx()[d]; dl=v['lines']
        out.update(repo='mathlib',commit=ML,file=f[len('.lake/packages/mathlib/'):],module=module_of(f))
    else:
        v=idx[d]; f=v['file']; dl=v['lines']
        out.update(repo='lean',commit=P,file=f,module=module_of(f))
    if nomatch:
        out['lines']=dl or e.get('lines')
        return out
    a,b=e['lines']
    if dl:
        a2,b2=max(a,dl[0]),min(b,dl[1])
        if a2>b2: a2,b2=dl
        if [a2,b2]!=[a,b]: out['lines_clamped_from']=[a,b]
        a,b=a2,b2
    out['lines']=[a,b]
    out['snippet']='\n'.join(flines(e['file'] if e.get('file','').startswith('.lake') else f)[a-1:b])
    pc={'declaration':d,'lines':dl,'conclusion':e.get('conclusion','')}
    if e.get('notation'): pc['notation']=e['notation']
    out['proof_context']=pc
    return out
def final_record(r,verif,src):
    rel=r['relation']; nm=rel=='noMatch'
    o={'id':r['id'],'relation':rel,'class':check.CLASS[rel]}
    if r.get('note'): o['note']=r['note']
    if not nm and r.get('proof_kind'): o['proof_kind']=r['proof_kind']
    ends=r.get('ends') or []
    if nm and not ends:
        ends=[{'declaration':d} for d in (r.get('searched') or {}).get('declarations',[])]
    good=[]
    for e in ends:
        d=e.get('declaration','')
        if d not in idx:
            alt=[n for n in idx if n.endswith('.'+d)] or [n for n in idx if n.split('.')[-1]==d.split('.')[-1]]
            if len(alt)==1: e['declaration']=alt[0]; d=alt[0]
        if d in idx or (e.get('file','').startswith('.lake') and d in check.mlidx()):
            good.append(norm_end(e,nm))
        else: o.setdefault('dropped_ends',[]).append(d)
    o['ends']=good
    if nm or r.get('searched'):
        o['searched']=json.loads(json.dumps(r.get('searched')).replace('~/tg-companion/tg/','').replace('~/tg-companion/tg','[L]').replace('',''))
    e=ERRATA.get(r['id'])
    if e and e['status'] in ('confirmed-script','confirmed-lean'):
        ev=e.get('check') or e.get('lean')
        o['text_error']={'kind':e['kind'],'corrected':e.get('corrected'),'evidence':ev,
                         'confirmed_by':'two skeptics (opus), each confirming independently'}
        sent=f"Text {e['kind']}, confirmed by two skeptics and {'`'+e['check']+'`' if e.get('check') else 'the Lean ('+str(e['lean'])+')'}."
        o['note']=(o.get('note','').rstrip()+' '+sent).strip()
    fx=NOTEFIX.get(r['id'])
    if fx and fx[0] in o.get('note',''): o['note']=o['note'].replace(fx[0],fx[1]); o['note_edited']='unconfirmed text-error wording removed or evidence added by the session lead'
    o['verification']=verif
    return o
AUD={}
NOTEFIX=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'notefix.json')))
ERRATA={x['id']:x for x in json.load(open(S+'skeptic/errata-table.json'))} if os.path.exists(S+'skeptic/errata-table.json') else {}
for f in glob.glob(S+'audit/A*.json'):
    if f.endswith('.todo.json'): continue
    for j in json.load(open(f))['rulings']: AUD[j['id']]=(os.path.basename(f)[:-5],j)
def merge():
    out={}
    stats={'batches':0,'judged':0}
    finals={}
    for pk in sorted(glob.glob(S+'packets/*.json')):
        b=os.path.basename(pk)[:-5]; P_=json.load(open(pk))
        if not (os.path.exists(S+f'map/{b}.json') and os.path.exists(S+f'verify/{b}.json')): continue
        res,x=check.compare(b)
        if x is None: continue
        dis,samp=x; dis=dict(dis)
        jp=S+f'judge/{b}.json'
        jud={}
        if os.path.exists(jp):
            for j in json.load(open(jp))['rulings']: jud[j['id']]=j
        elif dis or samp: continue   # wait for judge
        m={r['id']:r for r in json.load(open(S+f'map/{b}.json'))['records']}
        v={r['id']:r for r in json.load(open(S+f'verify/{b}.json'))['records']}
        stats['batches']+=1
        for rec in P_['records']:
            i=rec['id']
            verif={'batch':b,'steps':['mapper (sonnet)','verifier (sonnet)']}
            if i in dis:
                j=jud.get(i)
                if not j: continue
                verif['steps'].append('judge (opus)'); verif['agreed']=False; verif['disagreement']=dis[i]
                verif['ruling']=j['ruling']; verif['reason']=j.get('reason')
                r=j['record']; r['id']=i
            else:
                verif['agreed']=True
                verif['same_relation']=m[i]['relation']==v[i]['relation']
                r=m[i]
                if i in jud:
                    j=jud[i]; verif['steps'].append('judge (opus): noMatch search re-run')
                    verif['ruling']=j['ruling']; verif['reason']=j.get('reason')
                    if j['ruling']=='overturned': r=j['record']; r['id']=i
            if i in AUD and r.get('relation')=='noMatch':
                a,j=AUD[i]
                verif['steps'].append('absence audit (opus)'); verif['audit']={'file':a,'ruling':j['ruling'],'reason':j.get('reason')}
                if j['ruling']=='overturned': r=j['record']; r['id']=i
            finals[i]=(P_['overlay'],P_['kind'],rec,final_record(r,verif,b))
    return finals,stats
SOV=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sample_overrides.json')))
def apply_sov(finals):
    for i,ov in SOV.items():
        if i not in finals: continue
        a,b,rec,f=finals[i]
        if 'ends_from' in ov:
            f['ends']=json.loads(json.dumps(finals[ov['ends_from']][3]['ends']))
            f['proof_kind']=finals[ov['ends_from']][3].get('proof_kind','direct')
            f.pop('searched',None)
        f['relation']=ov['relation']; f['class']=check.CLASS[ov['relation']]; f['note']=ov['note']
        f['verification']['steps'].append('session lead sample check (opus): relation changed')
if __name__=='__main__':
    finals,stats=merge()
    apply_sov(finals)
    carried=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'carried.json')))
    for ov in ['book','paper-2013']:
        steps=json.load(open(R+f'{ov}-steps.json'))['steps']; disp=json.load(open(R+f'{ov}-displays.json'))['displays']
        for kind,lst,key in (('steps',steps,'proof_item'),('displays',disp,'section')):
            recs=[]
            for x in lst:
                i=x['id']
                if ov!='book' and i in carried:
                    src=carried[i]
                    if src not in finals: continue
                    f=json.loads(json.dumps(finals[src][3])); f['id']=i
                    f['verification']={'carried_from':f'book {src}','reason':'LaTeX identical to the book record (whitespace ignored)','book_verification':finals[src][3]['verification']}
                elif i in finals: f=finals[i][3]
                else: continue
                f={'id':i, ('item' if kind=='steps' else 'section'):x[key], **{k:v for k,v in f.items() if k!='id'}}
                recs.append(f)
            doc={'overlay':ov,'kind':kind,'lean':{'uri':'https://github.com/calr3/ternary-goldbach','commit':P},
                 'mathlib':{'uri':'https://github.com/leanprover-community/mathlib4','commit':ML},
                 'method':'each record mapped by one agent and independently by a second; an opus judge ruled on class or declaration-set disagreements and re-ran one in five agreed noMatch searches; an opus absence audit re-checked every other agreed noMatch; paper records with LaTeX identical to a book record carry the book verdict; text-error claims enter a note only when two opus skeptics confirm them and a re-run check script (scripts/checks/steps/) or the Lean backs them. Every declaration was checked with #check at the pin. No person has reviewed these verdicts.',
                 'total':len(lst),'mapped':len(recs),'records':recs}
            json.dump(doc,open(R+f'{ov}-{kind}-mapping.json','w'),indent=1,ensure_ascii=False)
            print(ov,kind,len(recs),'/',len(lst))
    print(stats)

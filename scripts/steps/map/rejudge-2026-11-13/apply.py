"""Apply the S5 rulings to data/*-mapping.json: noMatch -> relatedMatch (opus judges), -> closeMatch (triage
accepted on review), chain summaries, one-end chains. Prints a log; writes scratch/s5/applied.json."""
import json,glob,os,sys,collections
H=os.path.expanduser('~/tg-companion/'); R=H+'repo/data/'; S=H+'scratch/s5/'
PIN=json.load(open(R+'pins.json'))['lean']['commit']
idx=json.load(open(H+'scratch/steps2/declindex.json'))
items={i['id']:i for i in json.load(open(R+'items.json'))['items']}
matches=json.load(open(R+'matches-paper-2013.json'))['items']
def keyd(o,item):
    if o=='paper-2013':
        b=(matches.get(item) or {}).get('book'); item=b if isinstance(b,str) else (b or {}).get('id') if isinstance(b,dict) else None
    return {l['decl'] for l in (items.get(item) or {}).get('lean',[])}
rul={(x['overlay'],x['id']):x for f in sorted(glob.glob(S+'judge/out/j*.json')) for x in json.load(open(f))}
CLOSE={'Lemma 4.2.1 step 10','Proposition 5.2.4 step 9','Lemma 5.2.1 step 3','Lemma 5.1.1 step 15','Lemma B.2.3 step 5',
       'Lemma B.1.1 step 1','6.2 display 18','14.1 display 5','6.2 display 1'}
tri={x['id']:x for f in ('tri1','tri2') for x in json.load(open(S+f'out/{f}.json')) if x['overlay']=='book'}
summ={(x['overlay'],x['id']):x['summary'] for f in glob.glob(S+'m4/c*.out.json') for x in json.load(open(f))}
extra_summ=json.load(open(S+'summaries-new.json')) if os.path.exists(S+'summaries-new.json') else {}
TODAY='2026-11-13'
log=collections.defaultdict(list); bad=[]
def mkend(e,item_keys):
    d=idx.get(e['declaration'])
    a,b=e['lines']
    if not d or d['file']!=e['file'] or not (d['lines'][0]<=a<=b<=d['lines'][1]):
        return None
    L=open(H+'tg/'+d['file'],encoding='utf-8').readlines()
    return {'declaration':e['declaration'],'repo':'lean','commit':PIN,'file':d['file'],'module':d['module'],'lines':[a,b],
            'snippet':''.join(L[a-1:b]).rstrip('\n'),
            'proof_context':{'declaration':e['declaration'],'lines':d['lines'],'conclusion':e['conclusion']}}
changed={}
for o in ['book','paper-2013']:
    for k in ['steps','displays']:
        p=R+f'{o}-{k}-mapping.json'; raw=open(p,encoding='utf-8').read(); doc=json.loads(raw)
        for x in doc['records']:
            key=(o,x['id']); v=x['verification']
            if 'carried_from' in v: continue
            if key in rul and x['relation']=='noMatch':
                j=rul[key]
                if j['verdict']=='relatedMatch':
                    item=x.get('item') or x.get('section'); kd=keyd(o,item)
                    ends=[mkend(e,kd) for e in j['ends']]
                    if not ends or None in ends:
                        bad.append((key,j['ends'])); continue
                    old_note=x.get('note','')
                    x['relation']='relatedMatch'; x['class']='Deviates'; x['ends']=ends; x['note']=j['note']
                    x.pop('searched',None); x.pop('note_edited',None)
                    if k=='steps':
                        if len(ends)>1:
                            x['proof_kind']='chain'
                            if o=='book' and x['id'] in extra_summ: x['summary']=extra_summ[x['id']]
                        else:
                            x['proof_kind']='direct' if ends[0]['declaration'] in kd else 'helper'
                    v.setdefault('steps',[]).append(f'judge (opus), {TODAY}: re-judged against relatedMatch, changed')
                    v['rejudged_2026_11_13']={'from':'noMatch','reason':j['reason'],'old_note':old_note}
                    changed[key]=x; log['noMatch->relatedMatch'].append(key)
                else:
                    v.setdefault('steps',[]).append(f'judge (opus), {TODAY}: re-judged against relatedMatch, noMatch kept')
                    v['rejudged_2026_11_13']={'from':'noMatch','kept':True,'reason':j['reason']}
                    log['noMatch kept'].append(key)
            elif o=='book' and x['id'] in CLOSE:
                t=tri[x['id']]; assert x['relation']==t['old'],(x['id'],x['relation'])
                v.setdefault('steps',[]).append(f'sweep (sonnet) and lead check (opus), {TODAY}: {t["old"]} -> closeMatch')
                v['rejudged_2026_11_13']={'from':x['relation'],'reason':t['reason'],'old_note':x.get('note','')}
                x['relation']='closeMatch'; x['class']='Faithful'; x['note']=t['note']
                changed[key]=x; log[t['old']+'->closeMatch'].append(key)
            if x.get('proof_kind')=='chain':
                if len(x['ends'])<2:
                    x['proof_kind']='direct' if x['ends'][0]['declaration'] in keyd(o,x.get('item')) else 'helper'; log['one-end chain'].append(key)
                elif key in summ: x['summary']=summ[key]
                elif x['id'] in extra_summ and o=='book': x['summary']=extra_summ[x['id']]
        # carried records follow their book record
        if o=='paper-2013':
            book={r['id']:r for kk in ['steps','displays'] for r in json.load(open(R+f'book-{kk}-mapping.json'))['records']}
            for x in doc['records']:
                v=x['verification']
                if 'carried_from' not in v: continue
                b=book[v['carried_from'].split(' ',1)[1]]
                for f in ('relation','class','ends','note','proof_kind','summary','searched','text_error'):
                    if f in b: x[f]=b[f]
                    else: x.pop(f,None)
                if b['verification'].get('rejudged_2026_11_13') or b.get('summary'):
                    v['book_verification']=b['verification']
                    if b['verification'].get('rejudged_2026_11_13') and not b['verification']['rejudged_2026_11_13'].get('kept'):
                        log['carried change'].append((o,x['id']))
        s=json.dumps(doc,ensure_ascii=False,indent=1)+('\n' if raw.endswith('\n') else '')
        if '--write' in sys.argv: open(p,'w',encoding='utf-8').write(s)
print({k:len(v) for k,v in log.items()}); print('bad',bad)
missing=[ (o,x['id']) for o in ['book','paper-2013'] for x in json.load(open(R+f'{o}-steps-mapping.json'))['records'] if x.get('proof_kind')=='chain' and not x.get('summary')] if '--write' in sys.argv else []
print('chains without summary after write',len(missing), missing[:10])
json.dump({k:[list(t) for t in v] for k,v in log.items()},open(S+'applied.json','w'),indent=1)

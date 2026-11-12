#!/usr/bin/env python3
"""check.py BATCH: validate map/verify outputs, compare, write judge packet if needed."""
import json,sys,os,hashlib
ROOT=__import__('os').environ.get('TG_COMPANION',__import__('os').path.expanduser('~/tg-companion'))
S=os.path.join(ROOT,'scratch/steps/')
TG=os.path.join(ROOT,'tg/')
H=os.path.dirname(os.path.abspath(__file__))
idx=json.load(open(os.path.join(H,'declindex.json')))
byname={}
for n,v in idx.items():
    byname[n.split('.0.',1)[1] if n.startswith('_private.') else n]=v
CLASS={'exactMatch':'1-to-1','closeMatch':'Faithful','broadMatch':'Faithful','hasPart':'Partial',
       'narrowMatch':'Deviates','relatedMatch':'Deviates','noMatch':'Absent'}
_ml=None
_mi=None
def mlidx():
    global _mi
    if _mi is None: _mi=json.load(open(os.path.join(H,'mathlib-index.json')))
    return _mi
def mathlib_has(n):
    global _ml
    if _ml is None: _ml=set(json.load(open(os.path.join(H,'mathlib-names.json'))))
    return n in _ml
def validate(out,pk):
    errs=[]
    ids=[r['id'] for r in pk['records']]
    got={r['id']:r for r in out.get('records',[])}
    for i in ids:
        if i not in got: errs.append(f'{i}: missing')
    for i,r in got.items():
        if i not in ids: errs.append(f'{i}: not in packet'); continue
        if r.get('relation') not in CLASS: errs.append(f"{i}: bad relation {r.get('relation')}")
        if r.get('relation')=='noMatch' and not r.get('searched'): errs.append(f'{i}: noMatch without searched')
        for e in r.get('ends',[]):
            d=e.get('declaration'); f=e.get('file','')
            if f.startswith('.lake/packages/mathlib'):
                v=mlidx().get(d)
            else:
                v=byname.get(d)
                if not v:
                    tail=d.split('.')[-1]
                    alt=[n for n in byname if n.split('.')[-1]==tail and n.endswith(d.split('.',1)[-1].split('.')[-1])]
                    if len(alt)==1: e['declaration']=d=alt[0]; v=byname[d]
            if not v: errs.append(f'{i}: decl not found {d}'); continue
            if v['file']!=f: errs.append(f"{i}: {d} file {f} != {v['file']}"); e['file']=v['file']
            if list(e.get('decl_lines',[]))!=v['lines']: e['decl_lines']=v['lines']
            L=e.get('lines')
            if not L or len(L)!=2 or not (v['lines'][0]<=L[0]<=L[1]<=v['lines'][1]):
                errs.append(f"{i}: {d} lines {L} outside {v['lines']}")
    return errs,got
def decls(r): return {e.get('declaration') for e in r.get('ends',[])}
def compare(batch):
    pk=json.load(open(S+f'packets/{batch}.json'))
    res={'batch':batch}
    outs={}
    for role in ('map','verify'):
        p=S+f'{role}/{batch}.json'
        if not os.path.exists(p): res[role]='absent'; continue
        try: o=json.load(open(p))
        except Exception as ex: res[role]=f'bad json {ex}'; continue
        errs,got=validate(o,pk); res[role+'_errors']=errs; outs[role]=got
    if len(outs)<2: return res,None
    m,v=outs['map'],outs['verify']; dis=[];agree=[];samp=[]
    for r in pk['records']:
        i=r['id']; a=m.get(i); b=v.get(i)
        if not a or not b: dis.append((i,'missing')); continue
        ca,cb=CLASS.get(a.get('relation')),CLASS.get(b.get('relation'))
        da,db=decls(a),decls(b)
        why=[]
        if ca!=cb: why.append(f'class {a.get("relation")} vs {b.get("relation")}')
        if ca!='Absent' and cb!='Absent' and not (da&db): why.append('disjoint declarations')
        if why: dis.append((i,'; '.join(why)))
        else:
            agree.append(i)
            if ca=='Absent' and int(hashlib.sha1(i.encode()).hexdigest(),16)%5==0: samp.append(i)
    res.update(n=len(pk['records']),disagree=dis,agree=len(agree),nomatch_sample=samp,
               same_decls=sum(1 for i in agree if decls(m[i])==decls(v[i])),
               same_relation=sum(1 for i in agree if m[i].get('relation')==v[i].get('relation')))
    return res,(dis,samp)
def _main():
    for b in sys.argv[1:]:
        res,_=compare(b)
        json.dump(res,open(S+f'judge/{b}.check.json','w'),indent=1)
        print(b, 'n',res.get('n'),'agree',res.get('agree'),'same_rel',res.get('same_relation'),'same_decls',res.get('same_decls'),
              'disagree',len(res.get('disagree',[])),'sample',len(res.get('nomatch_sample',[])),
              'errs',len(res.get('map_errors',[])),len(res.get('verify_errors',[])))

def todo(batch):
    res,x=compare(batch)
    if x is None: return None
    dis,samp=x
    pk=json.load(open(S+f'packets/{batch}.json'))
    m={r['id']:r for r in json.load(open(S+f'map/{batch}.json'))['records']}
    v={r['id']:r for r in json.load(open(S+f'verify/{batch}.json'))['records']}
    recs={r['id']:r for r in pk['records']}
    t={'batch':batch,'packet':S+f'packets/{batch}.json','disputed':[],'nomatch_sample':[]}
    for i,why in dis: t['disputed'].append({'id':i,'why':why,'text':recs[i],'mapper':m.get(i),'verifier':v.get(i)})
    for i in samp: t['nomatch_sample'].append({'id':i,'text':recs[i],'mapper':m.get(i),'verifier':v.get(i)})
    if t['disputed'] or t['nomatch_sample']:
        json.dump(t,open(S+f'judge/{batch}.todo.json','w'),indent=1,ensure_ascii=False)
    return t
if __name__=='__main__':
    _main()
    for b in sys.argv[1:]:
        t=todo(b)
        if t: print(b,'todo',len(t['disputed']),len(t['nomatch_sample']))

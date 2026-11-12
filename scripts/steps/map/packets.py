import json,re,math,os
ROOT=__import__('os').environ.get('TG_COMPANION',__import__('os').path.expanduser('~/tg-companion'))
R=os.path.join(ROOT,'repo/data/')
OUT=os.path.join(ROOT,'scratch/steps/packets/')
idx=json.load(open('declindex.json'))
items={x['id']:x for x in json.load(open(R+'items.json'))['items']}
pitems={x['id']:x for x in json.load(open(R+'items-paper-2013.json'))['items']}
matches=json.load(open(R+'matches-paper-2013.json'))['items']
def norm(x): return re.sub(r'\s+','',x)
def leanlist(it):
    out=[]
    for l in it.get('lean',[]):
        e={'decl':l['decl'],'relation':l.get('relation'),'note':l.get('note')}
        i=idx.get(l['decl'])
        if i: e['file']=i['file']; e['lines']=i['lines']
        else: e['module']=l.get('module'); e['line']=l.get('line')
        out.append(e)
    return out
def iteminfo(bid,full=True):
    it=items[bid]
    d={'id':bid,'status':it['status'],'statement':it.get('book_statement')}
    if full: d['note']=it.get('note'); d['lean']=leanlist(it)
    else: d['lean']=[l['decl'] for l in it.get('lean',[])]
    return d
def book_of(ov,iid):
    if ov=='book': return iid
    m=matches.get(iid); return m and m.get('book')
def rec(x):
    r={k:x[k] for k in ('id','kind','latex','file','line','end_line','printed_page') if k in x}
    return r
def inside(ov,x):
    its=items.values() if ov=='book' else pitems.values()
    for it in its:
        if ov=='book': f,a,b=it['tex']['file'],it['tex']['line'],it['tex']['end_line']
        else: f,a,b=it['chapter_file']+'.tex',it['line'],it['end_line']
        if f==x['file'] and a<=x['line']<=b and it['kind'] not in ('equation','eq'): return it['id']
def chunks(lst,maxn=25,cap=35):
    if len(lst)<=cap: return [lst]
    k=math.ceil(len(lst)/maxn); n=math.ceil(len(lst)/k)
    return [lst[i:i+n] for i in range(0,len(lst),n)]
batches=[]; carried={}
bsteps=json.load(open(R+'book-steps.json'))['steps']; bdisp=json.load(open(R+'book-displays.json'))['displays']
bylatex={}
for x in bsteps: bylatex.setdefault(('step',x['proof_item'],norm(x['latex'])),x['id'])
for x in bdisp+bsteps: bylatex.setdefault(('any',norm(x['latex'])),x['id'])
for ov in ['book','paper-2013']:
    steps=json.load(open(R+f'{ov}-steps.json'))['steps']; disp=json.load(open(R+f'{ov}-displays.json'))['displays']
    if ov!='book':
        keep=[]
        for x in steps:
            b=book_of(ov,x['proof_item']); k=('step',b,norm(x['latex']))
            if b and k in bylatex: carried[x['id']]=bylatex[k]
            else: keep.append(x)
        steps=keep; keep=[]
        for x in disp:
            k=('any',norm(x['latex']))
            if k in bylatex: carried[x['id']]=bylatex[k]
            else: keep.append(x)
        disp=keep
    # steps by proof
    groups=[]; 
    for x in steps:
        if groups and groups[-1][0]==x['proof_item']: groups[-1][1].append(x)
        else: groups.append((x['proof_item'],[x]))
    cur=[]
    def flush(kind='steps'):
        global cur
        if cur: batches.append((kind,ov,cur)); cur=[]
    for p,g in groups:
        if len(g)>35:
            flush()
            for c in chunks(g): batches.append(('steps',ov,c))
        else:
            if len(cur)+len(g)>30: flush()
            cur=cur+g
    flush()
    groups=[]
    for x in disp:
        if groups and groups[-1][0]==x['section']: groups[-1][1].append(x)
        else: groups.append((x['section'],[x]))
    cur=[]
    for s,g in groups:
        ch=s.split('.')[0]
        if len(g)>35:
            flush('displays')
            for c in chunks(g): batches.append(('displays',ov,c))
        else:
            if cur and len(cur)+len(g)>30: flush('displays')
            cur=cur+g
    flush('displays')
merged=[]
for b in batches:
    if merged and len(b[2])<5 and merged[-1][0]==b[0] and merged[-1][1]==b[1] and len(merged[-1][2])+len(b[2])<=32:
        merged[-1]=(b[0],b[1],merged[-1][2]+b[2])
    else: merged.append(b)
batches=merged
names=[]
for n,(kind,ov,lst) in enumerate(batches,1):
    name=f"{'B' if ov=='book' else 'P'}{n:03d}-{kind[0]}"
    pk={'batch':name,'overlay':ov,'kind':kind,'records':[rec(x) for x in lst]}
    src='~/tg-companion/prior-2026-11-06/book/src/' if ov=='book' else '~/tg-companion/prior-2026-11-06/papers2013/1312.7748v2/'
    pk['tex_source_dir']=src
    if kind=='steps':
        pk['proofs']=[]
        for p in dict.fromkeys(x['proof_item'] for x in lst):
            b=book_of(ov,p)
            info={'proof_item':p}
            if ov!='book':
                info['paper_item']=pitems.get(p); info['book_counterpart']=b; info['change_since_book']=matches.get(p,{}).get('change')
            if b: info.update({'book_item':iteminfo(b)})
            pk['proofs'].append(info)
    else:
        secs=list(dict.fromkeys(x['section'] for x in lst))
        for r,x in zip(pk['records'],lst):
            ii=inside(ov,x)
            if ii: r['inside_item']=ii
        if ov=='book':
            pk['section_items']=[iteminfo(i,full=False) for i,it in items.items() if it['section'] in secs]
            ins={r['inside_item'] for r in pk['records'] if 'inside_item' in r}
            pk['enclosing_items']=[iteminfo(i) for i in ins]
        else:
            sec_items=[i for i,it in pitems.items() if it['section'] in secs]
            pk['section_items']=[{'paper_item':i,'book_counterpart':book_of(ov,i),**({'book':iteminfo(book_of(ov,i),full=False)} if book_of(ov,i) in items else {})} for i in sec_items]
            ins={r['inside_item'] for r in pk['records'] if 'inside_item' in r}
            pk['enclosing_items']=[{'paper_item':i,'book_counterpart':book_of(ov,i),**({'book':iteminfo(book_of(ov,i))} if book_of(ov,i) in items else {})} for i in ins]
    json.dump(pk,open(OUT+name+'.json','w'),indent=1,ensure_ascii=False)
    names.append((name,len(lst),lst[0]['id'],lst[-1]['id']))
json.dump(carried,open('carried.json','w'),indent=1)
json.dump(names,open('batches.json','w'),indent=0)
print(len(batches),'batches; carried',len(carried))
for n in names: print(*n)

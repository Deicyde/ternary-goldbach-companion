import json,glob,os
ROOT=__import__('os').environ.get('TG_COMPANION',__import__('os').path.expanduser('~/tg-companion'))
S=os.path.join(ROOT,'scratch/steps/')
out={}
for role in ('map','verify'):
    for f in glob.glob(S+role+'/*.json'):
        if '.weak' in f: continue
        b=os.path.basename(f)[:-5]
        for r in json.load(open(f)).get('records',[]):
            c=r.get('text_error_claim')
            if c: out.setdefault(r['id'],{'batch':b,'claims':[]})['claims'].append({'by':role,'claim':c})
for f in glob.glob(S+'judge/*.json'):
    if f.endswith('.todo.json') or f.endswith('.check.json'): continue
    b=os.path.basename(f)[:-5]
    for j in json.load(open(f)).get('rulings',[]):
        c=(j.get('record') or {}).get('text_error_claim')
        if c: out.setdefault(j['id'],{'batch':b,'claims':[]})['claims'].append({'by':'judge','claim':c})
json.dump(out,open('claims.json','w'),indent=1,ensure_ascii=False)
print(len(out))
for i,v in out.items(): print(i,'|',v['claims'][0]['claim'][:110].replace('\n',' '))

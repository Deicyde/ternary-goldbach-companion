import json,glob,os,sys
ROOT=__import__('os').environ.get('TG_COMPANION',__import__('os').path.expanduser('~/tg-companion'))
root=os.path.join(ROOT,'tg')
idx={}
for f in glob.glob(root+'/.lake/build/lib/lean/**/*.ilean',recursive=True):
    d=json.load(open(f)); mod=d['module']
    src=mod.replace('.','/')+'.lean'
    for n,r in d['decls'].items():
        idx[n]={'module':mod,'file':src,'lines':[r[0]+1,r[2]+1],'sel':r[4]+1}
json.dump(idx,open('declindex.json','w'))
print(len(idx))
# mathlib names (existence only)
ml=set()
for f in glob.glob(root+'/.lake/packages/mathlib/.lake/build/lib/lean/**/*.ilean',recursive=True):
    try: ml.update(json.load(open(f))['decls'].keys())
    except Exception as e: pass
json.dump(sorted(ml),open('mathlib-names.json','w')); print(len(ml))

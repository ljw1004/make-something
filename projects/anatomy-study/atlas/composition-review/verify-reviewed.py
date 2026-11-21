"""Compare current frozen chapter inputs to versions actually accepted by fresh reviewers."""
from pathlib import Path
from PIL import Image
import json,hashlib,sys,re
R=Path(sys.argv[1]).resolve();parent=R.parent;cache={}
def art(path):
 if path not in cache:
  im=Image.open(path).convert('RGBA');cache[path]=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
 return cache[path]
def obj(o):return {k:o[k] for k in ['id','name','fitted']}|{'base':art(o['base']),'layers':[art(x) for x in o['layers']]}
def fingerprint(p):
 d=json.loads(p.read_text());content={'chapter':d['chapter'],'title':d['title'],'inventory':[obj(o)for o in d['inventory']], 'operations':[{k:o[k] for k in ['type','fates','rule']}|{k:obj(o[k]) for k in ['a','b','result']}for o in d['operations']]}
 return hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
rounds=sorted([p for p in parent.glob('round-*') if p.is_dir()],key=lambda p:(int(re.search(r'\d+',p.name)[0]),p.name))
retained_file=Path(__file__).with_name('outcomes.json')
retained=json.loads(retained_file.read_text()) if retained_file.exists() else {}
retained={x['chapter']:x for x in retained.get('chapters',[])} if isinstance(retained,dict) else {}
results=[]
for p in sorted(R.glob('*/packet.json')):
 n=int(p.parent.name);fp=fingerprint(p);matches=[]
 for rnd in rounds:
  q=rnd/p.parent.name;review=q/'review.json'
  if review.exists() and json.loads(review.read_text())['overall']=='accept' and fingerprint(q/'packet.json')==fp:matches.append(rnd.name)
 prior=retained.get(n,{})
 if not matches and prior.get('acceptedFingerprint')==fp and prior.get('latestReview',{}).get('verdict')=='accept':matches.append('retained:'+prior['latestReview']['round'])
 results.append({'chapter':n,'fingerprint':fp,'acceptedMatchingRounds':matches})
missing=[r['chapter']for r in results if not r['acceptedMatchingRounds']]
(R/'reviewed-version-check.json').write_text(json.dumps({'chapters':results,'needsFreshReview':missing},indent=2)+'\n')
print(json.dumps({'matched':len(results)-len(missing),'needsFreshReview':missing}))
if missing:sys.exit(1)

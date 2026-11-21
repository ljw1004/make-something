"""Retain concise first/latest decisions; raw reviewer answers stay disposable."""
from pathlib import Path
import json,re,sys
P=Path(__file__).resolve().parent;R=P.parents[3]/'runs/anatomy-composition-review'
rounds=sorted([p for p in R.glob('round-*') if p.is_dir()],key=lambda p:(int(re.search(r'\d+',p.name)[0]),p.name))
changes={
1:'Closed membrane enclosure and matched nucleus/component scale.',
2:'Registered organelles and membrane carrier; one readable ribosome represents more.',
3:'Reuses the single completed cell as the representative for prepared embryonic descendants.',
4:'Constructs bone-building cells with a differentiation cue; coherent matrix and arm-bone/muscle family.',
5:'One transmembrane pore joins the axon wall; coherent Schwann wraps preserve the same axon.',
6:'One posterior skull/column view with continuous cord, root exits and a real sensory/motor junction.',
7:'Eye layers and optic nerve share one coherent globe and receiving anatomy.',
8:'Continuous ear anatomy and supported cochlear sensory tissue; no detached magnification.',
9:'Three-dimensional canal planes and sensory structures spanning their receiving chambers.',
10:'Cells remain immersed in continuous plasma; white/red cell proportions corrected.',
11:'Continuous arterial–capillary–venous specimen; lining persists under added valves and later joins.',
12:'Natural heart portions, distinct pulmonary/body routes and coronary vessels on retained muscle.',
13:'One lung lobule with continuous airway-to-alveolar spaces; no airway loop.',
14:'Open anterior thorax, actual intercostal bands and a separately added diaphragm.',
15:'Mucus alone in its material supply; trapped particles and phagocytosed bacteria physically enclosed.',
16:'Blind-ended lymphatic branches join collectors and a real receiving venous lumen.',
17:'The responding lymph node remains the same supported organ; cellular response fits within it.',
18:'Existing material transformation accepted under the clarified representative-quantity rule.',
19:'Supported villus with continuous capillary loops and a local collecting vein.',
20:'Glycogen lies within cell boundaries; hormone samples use the same fluid blood.',
21:'Coherent colon walls and ileal join; fermentation preserves residual food and depicts real products.',
22:'Separate blood and urine pathways; continuous tubular and drainage connections.',
23:'Water mixes inside the capillary lumen through a registered fitting.',
24:'Irregular living dermis without premature vessel ghosts; nerve enters through the section boundary.',
25:'Natural torn tissue and interrupted vessel; adhered platelet plug and locally reinforced clot.',
26:'Fibrin persists through clearance; one-ended sprout connects at fitting; living repair remains.',
27:'Existing cell renewal and material recycling accepted; no count-only reconstruction demanded.',
28:'One proportioned whole-body family, explicit chest handoff and flush healed surface patch.'}
old_file=P/'outcomes.json';old=json.loads(old_file.read_text())if old_file.exists()else {}
prior={r['chapter']:r for r in old.get('chapters',[])}if isinstance(old,dict)else {}
rows=[];threads=[]
def order(name):return (int(re.search(r'\d+',name)[0]),name)
def concise(d,packet,rnd):
 return {'round':rnd,'sourceHash':packet['sourceHash'],'verdict':d['overall'],'criteria':{k:d[k]['verdict']for k in ['components','composition','standalone']},'findings':[{'severity':x['severity'],'objects':x['objects'],'problem':re.split(r'(?<=[.!?])\s+',x['problem'])[0]}for x in d['issues']]}
for n in range(1,29):
 reviews=[]
 for rnd in rounds:
  f=rnd/f'{n:02}'/'review.json'
  if not f.exists():continue
  d=json.loads(f.read_text());packet=json.loads(f.with_name('packet.json').read_text());reviews.append(concise(d,packet,rnd.name))
  for line in f.with_name('events.jsonl').read_text().splitlines():
   event=json.loads(line)
   if event.get('type')=='thread.started':threads.append(event['thread_id'])
 previous=prior.get(n,{})
 candidates=[*reviews,*[previous[k]for k in ['firstReview','latestReview']if previous.get(k)]]
 candidates.sort(key=lambda d:order(d['round']))
 names=sorted(set(previous.get('reviewRounds',[]))|{d['round']for d in reviews},key=order)
 row={'chapter':n,'reviewCount':len(names),'reviewRounds':names,'firstReview':candidates[0]if candidates else None,'latestReview':candidates[-1]if candidates else None,'adoptedRepair':changes[n]}
 if row['latestReview']==previous.get('latestReview') and previous.get('acceptedFingerprint'):row['acceptedFingerprint']=previous['acceptedFingerprint']
 rows.append(row)
verification=None
if len(sys.argv)>1:
 folder=Path(sys.argv[1]);verification=json.loads((folder/'reviewed-version-check.json').read_text())
 verification['sourceHash']=__import__('hashlib').sha256((folder/'source.md').read_bytes()).hexdigest()
 for row,check in zip(rows,verification['chapters']):
  assert row['chapter']==check['chapter'];row['acceptedFingerprint']=check['fingerprint']if check['acceptedMatchingRounds']else None
if len(threads)!=len(set(threads)):raise ValueError('A reviewer conversation was reused')
total=sum(r['reviewCount']for r in rows)
result={'reviewCount':total,'uniqueReviewerConversations':total,'chapters':rows,'finalVersionCheck':verification}
(P/'outcomes.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['# Independent composition review outcomes','','Every assignment and revision uses a new ephemeral reviewer conversation. These are informed visual reviews with recipes, not blind recognition tests or human learning evidence. The first round predated the explicit synecdoche allowance; count-only objections are superseded. Raw answers and packets are disposable; this is a concise outcome record, not a replayable transcript.','',f"Completed reviews: **{total}**, with **{total} distinct conversations**.",'','| Chapter | First | Latest | Adopted correction or retained decision |','|---|---|---|---|']
for row in rows:
 first=row['firstReview'];last=row['latestReview'];lines.append(f"| {row['chapter']} | {first['verdict']if first else 'pending'} | {last['verdict']if last else 'pending'} | {row['adoptedRepair']} |")
if verification:lines+=['',f"Final artwork/operation versions matched independent acceptances for **{28-len(verification['needsFreshReview'])}/28 chapters**. Manuscript SHA-256: `{verification['sourceHash']}`."]
lines+=['','[Version hashes, criteria and remaining findings](outcomes.json). Technical playback checks are recorded in the [atlas production record](../README.md).']
(P/'outcomes.md').write_text('\n'.join(lines)+'\n')

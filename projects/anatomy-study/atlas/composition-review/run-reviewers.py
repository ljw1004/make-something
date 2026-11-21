"""One fresh Codex exec conversation per chapter; no resume/fork or inherited history.
Detailed packets/results stay under ignored runs/. No model override is applied.
"""
import json,subprocess,sys,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
CLI=Path('/Users/ljw/.vscode/extensions/openai.chatgpt-26.1021.22027-darwin-arm64/bin/macos-aarch64/codex')
ROUND=Path(sys.argv[1]).resolve();numbers=[int(x) for x in sys.argv[2:]] or list(range(1,29))
GUIDE=Path(__file__).with_name('reviewer-instructions.md')
verdict={'type':'string','enum':['accept','revise','uncertain']}
criterion={'type':'object','properties':{'verdict':verdict,'reason':{'type':'string'}},'required':['verdict','reason'],'additionalProperties':False}
schema={'type':'object','properties':{'chapter':{'type':'integer'},'sequence_intuition':{'type':'string'},'components':criterion,'composition':criterion,'standalone':criterion,'operations':{'type':'array','items':{'type':'object','properties':{'number':{'type':'integer'},'verdict':verdict,'observation':{'type':'string'}},'required':['number','verdict','observation'],'additionalProperties':False}},'issues':{'type':'array','items':{'type':'object','properties':{'severity':{'type':'string','enum':['blocker','important','minor']},'objects':{'type':'array','items':{'type':'string'}},'problem':{'type':'string'},'suggested_fix':{'type':'string'}},'required':['severity','objects','problem','suggested_fix'],'additionalProperties':False}},'overall':verdict},'required':['chapter','sequence_intuition','components','composition','standalone','operations','issues','overall'],'additionalProperties':False}
(ROUND/'schema.json').write_text(json.dumps(schema))
def one(n):
 folder=ROUND/f'{n:02}'
 if (folder/'review.json').exists():raise ValueError(f'Chapter {n} already has a review in {ROUND.name}; choose a new frozen round')
 prompt=GUIDE.read_text()+f'\n\nYour sole packet is {folder}. Chapter {n}. First open inventory.jpg with an image-viewing tool, then recipes.md and all operation PNGs. Return JSON only in final.\n'
 (folder/'request.txt').write_text(prompt)
 attachments=[str(folder/'inventory.jpg'),*[str(p) for p in sorted(folder.glob('operation-*.png'))]]
 cmd=[str(CLI),'exec',*[a for image in attachments for a in ['--image',image]],'--ephemeral','--sandbox','read-only','-C',str(ROOT),'--json','--output-schema',str(ROUND/'schema.json'),'-o',str(folder/'review.json'),'-']
 with (folder/'events.jsonl').open('w') as out,(folder/'stderr.txt').open('w') as err:
  run=subprocess.run(cmd,input=prompt,text=True,stdout=out,stderr=err)
 if run.returncode: return {'chapter':n,'error':'CLI exit '+str(run.returncode)}
 try:
  review=json.loads((folder/'review.json').read_text());assert review['chapter']==n
  return {'chapter':n,'overall':review['overall'],'issues':len(review['issues'])}
 except Exception as e:return {'chapter':n,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(one,numbers):print(json.dumps(result),flush=True)

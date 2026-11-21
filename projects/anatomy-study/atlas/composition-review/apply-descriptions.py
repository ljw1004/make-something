"""Apply physical description replacements without changing identities or recipes."""
from pathlib import Path
import json,re,sys
P=Path(__file__).resolve().parents[2];story=P/'anatomy.md';s=story.read_text()
alias=json.loads((P/'atlas/identity-aliases.json').read_text());reverse={v:k for k,v in alias.items()}
for arg in sys.argv[1:]:
 data=json.loads(Path(arg).read_text());descriptions=data.get('descriptions',data)
 for key,desc in descriptions.items():
  if not key.startswith(('id:','name:')):
   if 'descriptions' in data:key='name:'+key
   else:continue
  key=reverse.get(key,key);ref='`'+key[3:]+'`' if key.startswith('id:') else key[5:]
  suffix=r'[^\n]*' if key.startswith('id:') else r'(?: \(compound\))?'
  pat=r'^- '+re.escape(ref)+suffix+r'\n(?:(?!^- |^\*\*|^## ).*\n)*'
  matches=list(re.finditer(pat,s,re.M));m=next((m for m in matches if 'icon:' in m[0]),None)
  if not m:raise ValueError('Missing illustrated declaration '+key)
  block=m[0]
  if re.search(r'\{[^}]*\}',block):block=re.sub(r'\{[^}]*\}','{'+desc+'}',block,count=1)
  else:
   lines=block.splitlines();j=1
   while j<len(lines) and lines[j].startswith('  - '):j+=1
   lines[j:j]=['  {'+desc+'}',''];block='\n'.join(lines)+'\n'
  s=s[:m.start()]+block+s[m.end():]
story.write_text(s)

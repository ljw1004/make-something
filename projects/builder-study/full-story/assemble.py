"""Assemble the revised family sources into one reviewable study manuscript."""
from pathlib import Path
import argparse
import json
import re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
FAMILIES=['pinball','dragon','periscope','kaleidoscope','gantry','carousel','claw','drum','rover','projector','carrier']
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--captions',help='Audited JSON picture descriptions; requires coverage of every primary item image');args=p.parse_args()
source=(HERE/'opening.md').read_text().rstrip()+'\n\n'+'\n\n'.join((HERE/(family+'.md')).read_text().strip() for family in FAMILIES)
source+='\n\n## `c-end` The End\nbackground: ![White instruction page](assets/backgrounds/white.svg)\n\n“Can I have a go?”\n'
# The canonical route picks up the incoming part. Both physical drag directions
# remain legal; this ordering keeps the main workpiece stable in browser replay.
source=re.sub(r'^- (`[^`]+`) \[transform\] \+ (`[^`]+`) \[consume\] ->',r'- \2 [consume] + \1 [transform] ->',source,flags=re.M)
source=source.replace('(size 248px, 248px)','(size 236px, 248px)')
if args.captions:
    captions=json.loads((ROOT/args.captions).read_text());used=set();missing=set()
    def describe_section(section):
        def describe_item(item):
            block=item.group(0)
            icon=re.search(r'^  - icon: !\[[^\n]*\]\(([^)]+\.webp)\)',block,re.M)
            if not icon:return block
            identity=Path(icon[1]).stem
            if identity not in captions:missing.add(identity);return block
            caption=captions[identity]
            if not caption.strip() or any(c in caption for c in '{}\n'):raise ValueError('Caption must be one nonempty plain paragraph: '+identity)
            used.add(identity)
            # Builder's generated picture paragraphs have one home in captions.json.
            block=re.sub(r'\n  \{[^{}\n]*\}\n','\n',block)
            metadata=list(re.finditer(r'^  - (?:icon:|from chapter )[^\n]*\n',block,re.M))
            at=metadata[-1].end()
            return block[:at]+'\n  {'+caption+'}\n'+block[at:]
        return section[1]+re.sub(r'^- `[^`]+`[^\n]*\n.*?(?=^- `|\Z)',describe_item,section[2],flags=re.M|re.S)
    source=re.sub(r'(^\*\*Items\*\*\n)(.*?)(?=^\*\*Combinations\*\*|^## |\Z)',describe_section,source,flags=re.M|re.S)
    if missing:raise ValueError('Missing picture descriptions: '+', '.join(sorted(missing)))
    print(f'{len(used)} distinct item pictures described')
source=source.replace('(assets/','(../../stories/builder/assets/').replace('(icon.png)','(../../stories/builder/icon.png)')
output=ROOT/args.output;output.write_text(source)
print(output.relative_to(ROOT))

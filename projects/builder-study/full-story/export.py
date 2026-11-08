"""Export rendered groups with tight stage crops and shared physical scales."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_art import export
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--masters',required=True);p.add_argument('--output',required=True);p.add_argument('--family',required=True);p.add_argument('--sizes',help='Optional group CSS-size override JSON')
args=p.parse_args();src,out=Path(args.masters),Path(args.output);out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((src/(args.family+'-manifest.json')).read_text());overrides=json.loads(Path(args.sizes).read_text()) if args.sizes else {};groups={};records=[]
if manifest.get('changedSources'):raise ValueError('Sources changed during rendering')
for row in manifest['images']:groups.setdefault(row['group'],[]).append(row)
for group,rows in groups.items():
    dimensions={row['css'] for row in rows};assert len(dimensions)==1,(group,dimensions)
    images={row['image']:Image.open(src/(row['image']+'.png')).convert('RGBA') for row in rows};boxes=[im.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox() for im in images.values()]
    assert all(boxes),(group,'empty icon')
    for im,box in zip(images.values(),boxes):assert box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height,(group,'clipped geometry',box)
    crop=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes));css=overrides.get(group,next(iter(dimensions)));ratio=css*4/max(crop[2]-crop[0],crop[3]-crop[1])
    for identity,im in images.items():
        record=export(im,ratio,out/(identity+'.webp'))
        records.append(dict(image=identity,group=group,css=css,scaleBounds=crop,**record))
(src/(args.family+'-export.json')).write_text(json.dumps(records,indent=2)+'\n')

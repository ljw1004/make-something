"""Export new folds through the selected flat/full-fold physical scale with tight current crops."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_art import export
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--masters',required=True)
parser.add_argument('--baseline-masters',required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
src,base,out=Path(args.masters),Path(args.baseline_masters),Path(args.output)
out.mkdir(parents=True,exist_ok=True)
reference=next(row for row in json.loads((base/'export-manifest.json').read_text()) if row['id']=='pw-paper')
crop=tuple(reference['scaleBounds'])
scale=reference['pixelsPerSourcePixel']
records=[]
for identity in ['pw-one-blade','pw-two-blades','pw-three-blades']:
    image=Image.open(src/(identity+'.png')).convert('RGBA')
    bounds=image.getchannel('A').point(lambda a:255 if a>=24 else 0).getbbox()
    assert bounds[0]>=crop[0] and bounds[1]>=crop[1] and bounds[2]<=crop[2] and bounds[3]<=crop[3],(identity,bounds,crop)
    record=export(image,scale,out/(identity+'.webp'))
    records.append(dict(id=identity,scaleBounds=crop,sameScaleAs='pw-paper,pw-loose-rotor,pw-folded-rotor',**record))
(src/'export-manifest.json').write_text(json.dumps(records,indent=2)+'\n')

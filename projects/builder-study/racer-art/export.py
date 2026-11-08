"""Apply the recovered production registration to only the two new states."""
from pathlib import Path
import argparse
import json
from PIL import Image

HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--masters',required=True);p.add_argument('--output',required=True)
args=p.parse_args();src,out=Path(args.masters),Path(args.output)
out.mkdir(parents=True,exist_ok=True)
settings=json.loads((HERE/'registration.json').read_text())
for identity in ('wr-front-bearing-chassis','wr-rear-bearing-chassis'):
    image=Image.open(src/(identity+'.png')).convert('RGBA')
    assert image.size==(960,960)
    image=image.crop(tuple(settings['crop']))
    image=image.resize(tuple(round(n*settings['factor']) for n in image.size),Image.Resampling.LANCZOS)
    assert list(image.size)==settings['size']
    image.save(out/('c02--'+identity+'.webp'),lossless=True,method=4)

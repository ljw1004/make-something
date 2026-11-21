"""Mechanical extraction of one continuous generated nervous-system family.
Run with: uv run --with pillow python projects/anatomy-study/atlas/composition-review/nervous/produce.py
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
SCALE=.85;mapping={}
def load(n):
 im=Image.open(ROOT/'sources'/f'{n}.png').convert('RGBA')
 # Discard only negligible alpha outside the painted tissue; preserve antialiasing.
 im.putalpha(im.getchannel('A').point(lambda a:0 if a<12 else a));return im

def mask(size,pts):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(pts,fill=255);return m

def part(im,m):
 o=im.copy();o.putalpha(ImageChops.multiply(o.getchannel('A'),m));return o

def output(key,im,slug):
 b=im.getchannel('A').getbbox();im=im.crop(b);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(im.width+12,im.height+12));out.alpha_composite(im,(6,6));out.save(OUT/f'{slug}.png');mapping[key]=f'atlas/composition-review/nervous/assets/{slug}.png'
whole=load('whole-posterior-v3');tissue=load('tissue-posterior-v3')
# Adopt the generated lower routing while retaining the accepted upper master.
# The old outer silhouette removes only generated background haze, not tissue.
lower=mask(whole.size,[(0,1060),(1024,1060),(1024,1536),(0,1536)]).filter(ImageFilter.GaussianBlur(5))
newwhole=load('lower-routes-whole-v4')
newwhole.putalpha(ImageChops.multiply(newwhole.getchannel('A'),whole.getchannel('A')))
whole=Image.composite(newwhole,whole,lower)
bones=load('bones-v4')
# Bone and soft-tissue junctions differ slightly: the occipital condyles extend
# below the brainstem cut. The cord keeps its exposed upper tip in every state.
headmask=mask(whole.size,[(0,0),(1024,0),(1024,350),(0,350)])
columnmask=ImageChops.invert(headmask)
brainmask=mask(whole.size,[(0,0),(1024,0),(1024,310),(0,310)])
cordmask=ImageChops.invert(brainmask)
# A whole generated preparation supplies natural cut rootlet ends, a continuous
# canal floor and a short exposed lateral bone boundary. There is no erasure.
receiver=load('receiver-v4')
nervepts=[(515,772),(540,777),(555,783),(585,785),(608,793),(635,808),(660,812),(730,805),(739,816),(735,833),(693,837),(660,838),(636,850),(608,858),(571,861),(543,854),(515,863)]
nerve=part(tissue,mask(tissue.size,nervepts))
# The completed whole retains generated bone occlusion. The separately edited
# loose specimen already has prepared endpoints and matching lower routes.
initial_tissue=load('prepared-tissue-v4')
sensorypts=[(500,740),(760,740),(760,885),(650,885),(640,833),(620,835),(590,834),(565,820),(540,815),(515,813)]
sensorymask=mask(tissue.size,sensorypts)
sensory=part(nerve,sensorymask);motor=part(nerve,ImageChops.invert(sensorymask))
protected_head=Image.alpha_composite(part(bones,headmask),part(tissue,brainmask))
protected_cord=part(receiver,columnmask)
upper_cord=mask(whole.size,[(0,310),(1024,310),(1024,350),(0,350)])
protected_cord=Image.alpha_composite(protected_cord,part(initial_tissue,upper_cord))
output('id:brain-model',part(tissue,brainmask),'brain')
output('id:school-skull',part(bones,headmask),'skull')
output('id:spinal-cord-model',part(initial_tissue,cordmask),'cord')
output('id:school-backbone',part(bones,columnmask),'backbone')
output('id:school-protected-brain',protected_head,'protected-brain')
output('id:school-protected-cord',protected_cord,'protected-cord')
output('id:central-nervous-system-model',receiver,'central-nervous-system')
output('id:sensory-routes',sensory,'sensory-root')
output('id:motor-routes',motor,'motor-root')
output('id:school-peripheral-nerves',nerve,'spinal-nerve')
output('id:nervous-system-model',whole,'nervous-system')
(ROOT/'map.json').write_text(json.dumps({'itemIcons':mapping,'slotIcons':{}},indent=2)+'\n')
print(f'Produced {len(mapping)} mapped nervous-system assets')

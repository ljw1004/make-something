"""Registered immune/airway states from selected generated tissue masters.
Run with uv run --with pillow python projects/anatomy/atlas/composition-review/immune/produce.py
"""
from PIL import Image,ImageDraw,ImageChops
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'assets';OUT.mkdir(exist_ok=True);mapping={}
def load(n):
 im=Image.open(ROOT/'sources'/f'{n}.png').convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:0 if a<12 else a));return im

def mask(size,pts):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(pts,fill=255);return m

def part(im,pts):
 o=im.copy();o.putalpha(ImageChops.multiply(o.getchannel('A'),mask(im.size,pts)));return o

def trim(im):return im.crop(im.getchannel('A').getbbox())
def scaled(im,s):return im.resize((max(1,round(im.width*s)),max(1,round(im.height*s))),Image.Resampling.LANCZOS)
def output(name,im,slug,scale=.65,registered=False):
 if not registered:im=trim(im)
 im=scaled(im,scale);out=Image.new('RGBA',(im.width+12,im.height+12));out.alpha_composite(im,(6,6));out.save(OUT/f'{slug}.png');mapping['name:'+name]=f'atlas/composition-review/immune/assets/{slug}.png'

# A bounded phagosome remains wholly separate from the kidney-shaped nucleus.
ph=load('phagocytes');clean=ph.crop((0,0,724,724));intact=ph.crop((724,0,1448,724));debris=ph.crop((1448,0,2172,724))
output('Lung white blood cells',clean,'lung-white-cells')
output('Lung white cells containing bacteria',intact,'lung-containing-bacteria')
output('Engulfing white blood cells',clean,'engulfing-white-cells')
output('White blood cells containing bacterial remains',debris,'white-cells-with-remains')
# Bacteria are extracted at exactly their intracellular source dimensions.
bacteria=load('bacteria-extracted')
output('Bacteria in a lung air sac',bacteria,'lung-bacteria')
output('Bacteria',bacteria,'bacteria')

# Rotate painted antibody proteins, with one binding ARM TIP anchored to the
# actual bacterial surface. The Fc stem points away; no unattached glyphs.
antibody=load('antibody').resize((24,31),Image.Resampling.LANCZOS)
# Tip coordinates in the normalized painted antibody; use the upper right arm.
anchor=(19,2)
def anchored_protein(angle):
 r=antibody.rotate(angle,expand=True,resample=Image.Resampling.BICUBIC)
 a=math.radians(angle);dx=anchor[0]-antibody.width/2;dy=anchor[1]-antibody.height/2
 pt=(r.width/2+math.cos(a)*dx+math.sin(a)*dy,r.height/2-math.sin(a)*dx+math.cos(a)*dy)
 return r,pt
pad=45;coated=Image.new('RGBA',(bacteria.width+pad*2,bacteria.height+pad*2));coated.alpha_composite(bacteria,(pad,pad))
contacts=[(82,7,180),(137,22,90),(88,50,0),(12,82,270),(52,145,0),(21,61,180),(156,80,90),(106,132,0),(138,54,180)]
for x,y,a in contacts:
 im,pt=anchored_protein(a);coated.alpha_composite(im,(round(pad+x-pt[0]),round(pad+y-pt[1])))
output('Antibody-coated bacteria',coated,'coated-bacteria')
loose=Image.new('RGBA',(130,75))
for x,y,a in [(8,8,0),(48,5,35),(90,8,-25),(25,40,10),(75,40,-10)]:
 im,_=anchored_protein(a);loose.alpha_composite(im,(x,y))
output('Matching antibodies',loose,'matching-antibodies')

# Coherent mucus follows the apical plane instead of crossing cell bodies.
airway=load('airway');bare=load('airway-bare')
mucuspts=[(76,297),(112,278),(201,265),(410,237),(606,213),(824,194),(1056,177),(1301,161),(1524,142),(1746,119),(1945,109),(2096,114),(2112,127),(2086,147),(1975,166),(1815,185),(1622,215),(1404,240),(1194,259),(974,275),(764,294),(534,312),(312,328),(144,332),(90,321)]
mucus=Image.new('RGBA',airway.size)
clean_sheet=trim(load('mucus-clean')).resize((2027,214),Image.Resampling.LANCZOS)
mucus.alpha_composite(clean_sheet,(81,119))
output('Airway lining with sweeping hairs',bare,'bare-airway',.45)
output('Mucus-covered airway lining',airway,'coated-airway',.45)
output('Airway mucus',mucus,'mucus',.45)
# A few representative dust grains and rods are embedded in the SAME gel plane.
dust=load('dust-sample');dustpieces=[trim(dust.crop(b)) for b in [(40,0,190,120),(193,60,270,117),(0,135,85,230)]]
rods=[trim(bacteria.crop(b)) for b in [(30,0,145,60),(0,55,74,155),(75,43,174,145)]]
particles=Image.new('RGBA',(430,160));trapped=mucus.copy()
for n,im in enumerate(dustpieces+rods):
 im=scaled(im,.32)
 particles.alpha_composite(im,(20+n*65,45+(n%2)*35))
 # Cap has a sloping coherent surface. Scatter samples along its top plane.
 x=260+n*275;y=273-n*20
 trapped.alpha_composite(im,(x,y))
 # A faint copy of existing gel over the particles conveys embedding, not paint.
 gel=mucus.crop((x,y,x+im.width,y+im.height));gel.putalpha(ImageChops.multiply(gel.getchannel('A'),im.getchannel('A')).point(lambda a:round(a*.22)));trapped.alpha_composite(gel,(x,y))
output('Inhaled particles and bacteria',particles,'inhaled-particles',.45)
output('Mucus with trapped particles',trapped,'trapped-mucus',.45)

# Whole organ states replace one fixed node in place; no cell overlay layer.
nodes=load('nodes');left=nodes.crop((0,0,971,809));right=nodes.crop((971,0,1942,809))
output('Living lymph node',left,'living-node',.8,registered=True)
output('Responding lymph node',right,'responding-node',.8,registered=True)
(ROOT/'map.json').write_text(json.dumps({'itemIcons':mapping,'slotIcons':{},'hotspots':{'17':{'name:Living lymph node':{'center':[780,1000]},'name:Responding lymph node':{'center':[780,1000]}}}},indent=2)+'\n')
print(f'Produced {len(mapping)} immune assets')

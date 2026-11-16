"""Extract matched anatomical constituents from selected generated paintings.

Only masks, crops, alpha composition and common-scale resizing happen here.
No anatomy is painted by this script. Run with Pillow and NumPy.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageChops, ImageFilter
import numpy as np
import json,re
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
M={'itemIcons':{},'slotIcons':{},'presentations':{}}
PREFIX='atlas/composition-review/circulation/assets/'
def read(n):
 im=Image.open(ROOT/'sources'/f'{n}.png').convert('RGBA')
 a=np.array(im);a[a[:,:,3]<20]=0
 return Image.fromarray(a)
def poly(im,points):
 m=Image.new('L',im.size);ImageDraw.Draw(m).polygon(points,fill=255)
 return m
def rect(im,box):
 m=Image.new('L',im.size);ImageDraw.Draw(m).rectangle(box,fill=255);return m
def part(im,m):
 p=im.copy();p.putalpha(ImageChops.multiply(im.getchannel('A'),m));return p
def minus(im,m):return part(im,ImageOps.invert(m))
def union(*m):
 r=m[0]
 for v in m[1:]:r=ImageChops.lighter(r,v)
 return r
def emit(n,im,scale=1,trim=True,key=None):
 if trim:
  b=im.getchannel('A').getbbox()
  if not b:raise ValueError(n+' is empty')
  im=ImageOps.expand(im.crop(b),8,fill=(0,0,0,0))
 if scale!=1:im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
 slug=re.sub('[^a-z0-9]+','-',n.lower()).strip('-');im.save(OUT/(slug+'.png'))
 path=PREFIX+slug+'.png'
 if key is not False:M['itemIcons'][key or 'name:'+n]=path
 return path
# Chapter11: one continuous painted tissue route, with parts left at that scale.
v=read('vascular-lined-valved');rawv=read('vascular-master');s=.53
artery=poly(v,[(0,275),(45,272),(210,245),(400,280),(495,320),(585,340),(585,400),(470,425),(200,440),(0,435)])
vein=poly(v,[(1560,363),(1665,350),(1780,312),(1990,304),(2135,290),(2172,315),(2172,423),(2100,448),(1900,459),(1740,440),(1640,412),(1560,403)])
valve=poly(v,[(1894,328),(1920,342),(1945,359),(2007,373),(1980,384),(1941,400),(1912,421),(1884,417),(1891,395),(1916,382),(1890,363)])
center=rect(v,(550,0,1630,v.height))
emit('Arterial wall',part(rawv,artery),s)
emit('Arterial vessels',part(read('vessels-lined').resize(v.size),artery),s)
emit('Venous wall',part(read('vein-unvalved').resize(v.size),vein),s)
emit('One-way valve flaps',part(v,valve),s)
emit('Venous return',part(v,vein),s)
emit('Capillary bed',part(v,center),s)
emit('Distribution and exchange bed',part(v,rect(v,(0,0,1630,v.height))),s)
emit('Capillaries and venous return',part(v,rect(v,(550,0,v.width,v.height))),s)
emit('Body blood-vessel network',v,s)
tissue=read('vascular-tissue').resize(v.size)
emit('Nearby body cells',part(tissue,center),s)
# Chapter16: actual lumen junction and blind-ended small lymphatic branches.
l=read('lymph-master');s=.72
low=rect(l,(0,600,770,1024));high=ImageOps.invert(low)
neck=poly(l,[(1060,0),(1536,0),(1536,410),(1260,410),(1260,277),(1220,243),(1206,220),(1248,207),(1268,180),(1240,164),(1217,180),(1200,191),(1130,140),(1060,60)])
emit('Tiny lymph vessels',part(read('lymph-only').resize(l.size),low),s)
emit('Larger lymph vessels',part(read('lymph-only').resize(l.size),high),s)
emit('Neck vein segment',part(l,neck),s)
emit('Tissue with lymph capillaries',part(l,low),s)
emit('Lymph return route',part(l,high),s)
emit('Lymph drainage network',l,s)
emit('Tissue beside blood capillaries',read('lymph-tissue'),s)
# Chapter14: shared coordinates from a unified completed thorax.
t=read('thorax-master');s=.84
organ=poly(t,[(550,0),(665,0),(665,110),(710,170),(760,192),(826,208),(901,260),(980,360),(1060,508),(1080,650),(1092,710),(1104,775),(1115,840),(1125,915),(1127,985),(1120,1040),(1104,1102),(1080,1060),(1010,1008),(920,978),(885,949),(770,952),(625,927),(555,914),(492,920),(445,945),(355,949),(255,980),(157,1040),(66,1098),(60,1000),(68,845),(100,667),(135,547),(190,414),(270,302),(347,235),(405,201),(462,196),(488,256),(490,338),(505,338),(511,114),(550,112)])
diaphragm=poly(t,[(66,1098),(157,1040),(255,980),(355,949),(445,945),(492,920),(555,914),(625,927),(770,952),(885,949),(920,978),(1010,1008),(1090,1065),(1161,1085),(1130,1256),(1010,1215),(880,1160),(722,1125),(625,1108),(500,1114),(380,1140),(250,1182),(110,1259)])
empty=read('thorax-anterior-spine').resize(t.size)
emit('Breathing apparatus',empty,s,False,key='id:art-breathing-apparatus')
org=part(t,organ);dia=part(t,diaphragm)
emit('Heart and lungs',org,s)
emit('Diaphragm',part(dia,rect(t,(110,0,1115,t.height))),s)
pdia=emit('Chest diaphragm layer',dia,s,False,False)
porg=emit('Chest organ layer',org,s,False,False)
M['slotIcons']['id:art-breathing-apparatus']={'name:Diaphragm':pdia,'name:Heart and lungs':porg}
emit('Complete chest',t,s,False,False)
emit('Rib cage',read('thorax-anterior-bones').resize(t.size),s)
emit('Whole lungs',read('whole-lungs').resize((1102,1100)),s,key='id:atlas-whole-lungs')
# Corrected isolated inputs retain natural material surfaces.
emit('Blood-facing lining cells',read('endothelial-sheet'),.5)
emit('Thin-walled veins',part(read('vessels-lined').resize(v.size),vein),.53)
emit('Tiny capillary tubes',part(read('vascular-tubes').resize(v.size),center),.53)
emit('Muscles between the ribs',read('intercostals-v2').resize(t.size),.84)
# Chapter12: one exterior master and its prepared tissue family.
import sys
sys.dont_write_bytecode = True
from cardiac_family import build
build(read,emit,M)
# Chapter13 remains one enlarged lobule throughout.
b=read('lobule-duct-v2');s=.72
aw=read('lobule-airways').resize(b.size)
stem=rect(b,(580,0,720,205))
emit('Terminal airway',part(aw,stem),s)
emit('Fine branching air tubes',minus(aw,stem),s)
emit('Lobular airways',aw,s)
emit('Tiny air sacs',read('lobule-sacs').resize(b.size),s)
emit('Lung capillaries',read('lobule-capillaries').resize(b.size),s)
emit('Elastic supporting tissue',read('lobule-elastic').resize(b.size),s)
emit('Lung lobule',b,s)
for name,source in [('Air sacs with blood vessels','lobule-vascular-sacs'),('Elastic air sacs','lobule-elastic-sacs'),('Elastic air sacs with blood vessels','lobule-exchange')]:
 stage=read(source).resize(b.size)
 window=poly(b,[(385,996),(420,982),(459,927),(485,875),(530,866),(561,811),(615,787),(697,788),(730,771),(769,783),(794,812),(864,803),(901,841),(920,867),(958,869),(987,897),(994,944),(999,994),(966,1034),(908,1058),(866,1086),(846,1124),(781,1130),(733,1157),(684,1160),(644,1155),(590,1161),(530,1148),(496,1117),(430,1090),(392,1053)])
 stage.alpha_composite(part(b,window))
 emit(name,stage,s)
(ROOT/'map.json').write_text(json.dumps(M,indent=2)+'\n')
print(f'Wrote {len(M["itemIcons"])} item assets')

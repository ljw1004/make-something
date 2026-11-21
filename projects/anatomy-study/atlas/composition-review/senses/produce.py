"""Extract generated sensory-organ families; no procedural painting.
Run: uv run --with pillow python projects/anatomy-study/atlas/composition-review/senses/produce.py
Coordinates below are source-pixel masks; all installed states use one master scale.
"""
from PIL import Image,ImageDraw,ImageChops,ImageFilter
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
MAP={};SCALE=.68

def load(name): return Image.open(ROOT/'sources'/f'{name}.png').convert('RGBA')
def mask(size,points):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(points,fill=255);return m

def region(im,points):
 o=im.copy();o.putalpha(ImageChops.multiply(im.getchannel('A'),mask(im.size,points)));return o

def cut(im,box): return im.crop(box)
def trim(im):
 b=im.getchannel('A').point(lambda x:255 if x>15 else 0).getbbox()
 return im.crop(b) if b else im

def output(name,im,slug,scale=SCALE):
 im=trim(im);im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
 # Consistent small safety margin, preserving the exact common physical scale.
 out=Image.new('RGBA',(im.width+12,im.height+12));out.alpha_composite(im,(6,6));out.save(OUT/f'{slug}.png')
 MAP['name:'+name]=f'atlas/composition-review/senses/assets/{slug}.png'
 return out

def replace(base,detail,points):
 return Image.composite(detail,base,mask(base.size,points).filter(ImageFilter.GaussianBlur(2)))
def pack(parts,gap=24):
 parts=[trim(x) for x in parts];out=Image.new('RGBA',(sum(x.width for x in parts)+gap*(len(parts)-1),max(x.height for x in parts)))
 x=0
 for im in parts:out.alpha_composite(im,(x,(out.height-im.height)//2));x+=im.width+gap
 return out

# EYE. Broad cup-shaped layers are real material surfaces, not arbitrary arcs.
eye=load('eye-master');parts=load('eye-parts')
cornea=trim(cut(parts,(170,0,530,445)));iris=trim(cut(parts,(610,0,930,445)));lens=trim(cut(parts,(1060,40,1270,410)))
photo=trim(cut(parts,(60,445,700,1024)));neural=trim(cut(parts,(700,440,1536,1024)))
output('Clear dome (cornea)',cornea,'cornea',SCALE*1.35)
output('Coloured muscle ring (iris)',iris,'iris',SCALE*1.28)
output('Clear lens',lens,'lens',SCALE*.86)
output('Light-sensitive cells',photo,'photoreceptors',SCALE*1.40)
output('Retinal nerve cells',neural,'retinal-cells',SCALE*1.30)
front_poly=[(0,0),(520,0),(485,210),(490,350),(550,445),(620,650),(602,765),(530,825),(440,1024),(0,1024)]
front=region(eye,front_poly)
posterior_poly=[(520,0),(1536,0),(1536,1024),(440,1024),(530,825),(602,765),(620,650),(550,445),(490,350),(485,210)]
posterior=region(eye,posterior_poly)
# Optical front: complete master, and same receiving front with lens omitted.
lens_poly=[(534,444),(569,453),(606,509),(626,591),(620,656),(594,710),(565,725),(536,700),(520,640),(516,550),(520,480)]
front_no_lens=front.copy();front_no_lens.putalpha(ImageChops.subtract(front.getchannel('A'),mask(front.size,lens_poly)))
output('Cornea and iris',front_no_lens,'cornea-iris')
output('Light-controlling eye front',front,'eye-front')
# Alternate order uses the same front silhouette, with clear cornea replacing iris.
focusing=front.copy();optical_poly=[(310,297),(382,305),(437,365),(479,470),(496,615),(482,745),(435,839),(381,868),(303,830),(232,749),(181,630),(165,513),(192,413),(250,337)]
cap=cornea.resize((335,580),Image.Resampling.LANCZOS);cap_layer=Image.new('RGBA',eye.size);cap_layer.alpha_composite(cap,(162,292))
focusing=replace(focusing,cap_layer,optical_poly)
output('Focusing eye front',focusing,'focusing-front')
output('Retina with optic nerve',posterior,'retina-nerve')
output('Eye with optic nerve',eye,'eye')

# EAR. The enclosing middle-ear tissue is supplied with the canal; the cochlear
# preparation includes the bounded oval-window receiving region.
ear=load('ear-master');empty=load('ear-empty')
window_poly=[(1061,512),(1097,509),(1119,532),(1118,591),(1097,616),(1063,608)]
empty=replace(empty,load('ear-window'),window_poly)
cochlea_poly=[(1076,0),(1536,0),(1536,822),(1200,822),(1130,773),(1095,710),(1050,677),(1061,629),(1057,600),(1055,554),(1066,491),(1070,439),(1057,369)]
outer_mask=ImageChops.invert(mask(ear.size,cochlea_poly))
def outer(im):
 o=im.copy();o.putalpha(ImageChops.multiply(o.getchannel('A'),outer_mask));return o
# Exact tympanic membrane and ossicles regions follow their physical contours.
drum_poly=[(748,477),(775,484),(797,509),(814,540),(829,570),(816,604),(807,642),(791,688),(770,697),(739,680),(716,646),(704,604),(706,554),(722,509)]
bones_poly=[(811,409),(826,390),(850,377),(875,378),(892,395),(891,412),(904,420),(936,428),(972,430),(999,432),(1009,443),(987,456),(978,478),(977,502),(990,533),(993,545),(1008,552),(1030,539),(1055,531),(1081,528),(1100,534),(1109,553),(1107,579),(1090,601),(1074,603),(1047,594),(1017,589),(995,581),(976,583),(965,572),(966,557),(957,537),(947,521),(941,494),(936,475),(910,467),(889,452),(878,447),(861,463),(849,492),(840,516),(847,542),(852,564),(846,582),(837,581),(828,553),(821,529),(812,506),(809,488),(815,468),(815,444),(808,430)]
drum=region(ear,drum_poly);bones=region(ear,bones_poly)
with_drum=replace(empty,ear,drum_poly)
conducting=replace(with_drum,ear,bones_poly)
# The sensory ribbon follows the partition as one continuous spiral strip.
ribbon_poly=[(1221,376),(1265,363),(1320,370),(1377,391),(1421,424),(1465,473),(1490,526),(1495,573),(1482,621),(1453,666),(1404,695),(1349,705),(1293,697),(1234,675),(1172,649),(1123,631),(1090,625),(1097,592),(1139,591),(1186,607),(1249,630),(1300,646),(1352,649),(1397,630),(1422,599),(1432,561),(1424,520),(1400,492),(1361,479),(1320,484),(1284,509),(1266,541),(1277,561),(1298,562),(1296,579),(1277,578),(1253,564),(1240,538),(1248,509),(1265,478),(1298,453),(1338,449),(1382,457),(1410,483),(1429,518),(1419,465),(1384,427),(1336,403),(1285,393),(1234,400)]
ribbon=region(ear,[(1110,586),(1142,591),(1180,607),(1220,621),(1255,633),(1246,655),(1206,642),(1160,625),(1120,618),(1095,617)])
output('Outer ears and canals',outer(empty),'outer-ear')
output('Eardrums',drum,'eardrum')
output('Outer ears with eardrums',outer(with_drum),'outer-eardrum')
output('Middle-ear bones',bones,'ear-bones')
output('Sound-conducting ears',outer(conducting),'conducting-ear')
output('Coiled inner-ear chambers and fluid',region(empty,cochlea_poly),'cochlea')
output('Hearing cells with tiny hairs',ribbon,'hair-cells')
output('Vibration-sensitive inner ears',region(replace(ear,empty,window_poly),cochlea_poly),'sensing-cochlea')
output('Ears',ear,'ear')

# BALANCE. All prepared sensory patches retain their installed dimensions,
# with separate orientations. Empty-state fills are generated, never painted.
balance=load('balance-v2-master');empty_b=load('balance-v2-empty');unweighted=load('balance-v2-unweighted')
turn_polys=[[(375,548),(389,518),(418,500),(450,502),(478,519),(485,557),(491,607),(504,649),(475,651),(443,641),(415,639),(384,620),(371,586)],[(945,462),(971,438),(1012,414),(1051,405),(1081,417),(1112,449),(1132,494),(1138,537),(1124,569),(1093,586),(1052,579),(1018,566),(984,582),(956,563),(938,536),(933,502)],[(449,802),(478,766),(521,745),(565,740),(607,757),(642,776),(672,798),(693,827),(698,863),(676,896),(642,914),(608,928),(566,940),(516,937),(478,921),(448,896),(427,869),(424,841)]]
tilt_polys=[[(789,783),(800,764),(829,749),(866,733),(900,738),(939,747),(977,768),(1009,793),(1019,816),(1001,836),(962,845),(914,840),(866,837),(824,823),(795,810)],[(842,1025),(854,1006),(873,988),(895,989),(915,1000),(927,1030),(929,1070),(926,1112),(915,1148),(901,1166),(879,1159),(863,1135),(849,1103),(843,1062)]]
turn_parts=[region(balance,p) for p in turn_polys]
weighted_parts=[region(balance,p) for p in tilt_polys]
plain_parts=[region(unweighted,p) for p in tilt_polys]
turn_state=empty_b.copy()
for p in turn_polys:turn_state=replace(turn_state,balance,p)
output('Fluid-filled loops',empty_b,'fluid-filled-loops')
output('Turning sensor cells',pack(turn_parts),'turning-sensor-cells')
output('Turn-sensing canals',turn_state,'turn-sensing-canals')
output('Tilt sensor cells',pack(plain_parts),'tilt-sensor-cells')
output('Weighted balance sensors',pack(weighted_parts),'weighted-balance-sensors')
output('Balance organs',balance,'balance-organs')
# Retained calcium-carbonate material sample: a representative visible sample,
# not a literal count of the fine granules in the macular jelly.
output('Tiny mineral weights',load('mineral-sample'),'tiny-mineral-weights')
(ROOT/'map.json').write_text(json.dumps({'itemIcons':MAP,'slotIcons':{}},indent=2)+'\n')
print(f'Produced {len(MAP)} item assets')

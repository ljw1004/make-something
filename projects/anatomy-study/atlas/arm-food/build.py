"""Mechanical extraction/registration of generated atlas artwork; no new painting.
Run: uv run --with pillow python projects/anatomy-study/atlas/arm-food/build.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json

ROOT=Path(__file__).parent
OUT=ROOT/'assets'
OUT.mkdir(exist_ok=True)
L=Image.Resampling.LANCZOS
mapping={'itemIcons':{},'slotIcons':{},'hotspots':{'4':{}},'placements':{}}

def load(name): return Image.open(ROOT/'sources'/f'{name}.png').convert('RGBA')
def trim(im):
    box=im.getchannel('A').point(lambda a:255 if a>30 else 0).getbbox()
    return im.crop(box) if box else im
def fit(im,maxsize):
    im=trim(im); im.thumbnail(maxsize,L); return im
def store(im,name,key=None):
    # Remove near-transparent generated matte residue while retaining soft edges.
    im=im.copy()
    im.putalpha(im.getchannel('A').point(lambda a:0 if a<20 else (255 if a>244 else a)))
    im.save(OUT/f'{name}.png')
    if key: mapping['itemIcons'][key]=f'atlas/arm-food/assets/{name}.png'
    return im
def part(im,box,maxsize,name,key=None): return store(fit(im.crop(box),maxsize),name,key)
def masked(im,points):
    mask=Image.new('L',im.size); ImageDraw.Draw(mask).polygon(points,fill=255)
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return out

# All stages retain the skeleton master's coordinates. Polygon masks only remove
# not-yet-built anatomy. Muscle layers use selected generated muscle pixels.
skeleton=load('arm-skeleton')
shoulder=masked(skeleton,[(0,0),(500,0),(500,105),(398,107),(336,112),(312,123),(298,143),(298,176),(311,197),(286,220),(270,203),(250,265),(245,420),(0,470)])
humerus=masked(skeleton,[(0,0),(1024,0),(1024,690),(445,690),(434,716),(404,725),(387,718),(374,727),(348,730),(324,725),(302,714),(0,714)])
ulna=masked(skeleton,[(310,724),(348,717),(382,729),(397,766),(401,814),(439,905),(494,995),(552,1067),(587,1113),(579,1137),(553,1132),(526,1086),(477,1021),(431,947),(386,866),(352,799),(316,771)])
with_ulna=Image.alpha_composite(humerus,ulna)
long_bones=masked(skeleton,[(0,0),(1024,0),(1024,1088),(660,1088),(643,1105),(616,1121),(584,1129),(570,1141),(539,1141),(0,900)])
biceps=masked(load('arm-biceps'),[(262,145),(280,151),(282,202),(308,247),(336,293),(357,392),(366,481),(357,571),(345,617),(358,663),(387,703),(426,735),(460,765),(469,797),(446,798),(408,760),(379,728),(347,699),(329,672),(313,634),(284,590),(261,529),(246,464),(235,393),(237,327),(248,267),(261,229),(254,186)])
triceps_source=load('arm-muscles')
triceps=masked(triceps_source,[(413,184),(435,246),(454,334),(463,418),(457,487),(441,550),(418,609),(401,645),(392,625),(403,551),(407,450),(402,337),(393,251)])
triceps_back=masked(triceps_source,[(310,612),(326,641),(315,667),(298,697),(301,720),(326,737),(339,752),(312,755),(293,743),(283,719),(282,691),(293,650)])
triceps=Image.alpha_composite(triceps,triceps_back)
with_biceps=Image.alpha_composite(skeleton,biceps)
with_muscles=Image.alpha_composite(Image.alpha_composite(skeleton,triceps),biceps)
stages={'arm-shoulder':shoulder,'arm-humerus':humerus,'arm-humerus-ulna':with_ulna,'arm-long-bones':long_bones,'arm-skeleton':skeleton,'arm-with-biceps':with_biceps,'arm-with-muscles':with_muscles}
for name,im in stages.items():
    # Shared crop and uniform resize preserve registration even for shoulder-only.
    im=im.crop((45,0,900,1536)).resize((735,1320),L)
    store(im,name,'id:'+name)
    box=im.getchannel('A').point(lambda a:255 if a>40 else 0).getbbox()
    x0,y0,x1,y1=box
    mapping['hotspots']['4']['id:'+name]={'center':[780,1010],'hitbox':{'center':[round(780-735/2+(x0+x1)/2),round(1010-1320/2+(y0+y1)/2)],'size':[x1-x0+30,y1-y0+30]}}
store(trim(with_muscles),'arm-complete-isolated')
store(trim(biceps),'biceps-isolated')
store(trim(triceps),'triceps-isolated')

materials=load('bone-materials')
part(materials,(0,0,510,480),(310,310),'bone-cells','id:arm-bone-cells')
part(materials,(1030,0,1536,480),(240,240),'bone-mineral','id:school-bone-mineral')
part(materials,(0,490,510,1024),(330,330),'soft-bone','id:arm-soft-bone')
part(materials,(515,490,1024,1024),(330,330),'bone-tissue','id:arm-bone-tissue')

enzymes=load('enzymes')
amylase=part(enzymes,(0,0,625,625),(240,160),'amylase','id:meal-amylase')
part(enzymes,(625,0,1254,625),(300,240),'sugar-enzymes','id:meal-sugar-enzymes')
part(enzymes,(0,625,625,1254),(300,240),'proteases','id:meal-proteases')
part(enzymes,(625,625,1254,1254),(280,240),'lipase','id:meal-lipase')
fluids=load('fluids')
saliva=part(fluids,(0,0,625,620),(430,340),'salivary-fluid','id:meal-salivary-fluid')
part(fluids,(625,0,1254,620),(350,280),'bile','name:Bile')
part(fluids,(0,620,625,1254),(420,360),'fat-food','name:Fat food')
part(fluids,(625,620,1254,1254),(420,360),'fat-droplets','name:Small fat droplets')
saliva_enzyme=saliva.copy()
# The exact supplied enzyme remains at the same scale inside the supplied fluid.
small=amylase.copy()
saliva_enzyme.alpha_composite(small,((saliva.width-small.width)//2,(saliva.height-small.height)//2))
store(saliva_enzyme,'saliva-amylase','id:meal-saliva')
foods=load('foods')
part(foods,(0,0,600,625),(400,340),'starchy-food','name:Starchy food')
part(foods,(600,0,1254,625),(450,360),'short-starch','name:Shorter starch chains')
part(foods,(0,625,600,1254),(380,310),'protein-food','name:Protein food')
part(foods,(600,625,1254,1254),(450,350),'fat-products','name:Fat digestion products')
# These are the same molecule identities and depictions used earlier/later.
mapping['itemIcons']['name:Meal glucose']='atlas/opening/assets/glucose.png'
mapping['itemIcons']['name:Meal amino acids']='atlas/opening/assets/amino-acids.png'
(ROOT/'map.json').write_text(json.dumps(mapping,indent=2)+'\n')

if __name__=='__main__': print(f'Built {len(mapping["itemIcons"])} mapped identities and registered arm stages.')

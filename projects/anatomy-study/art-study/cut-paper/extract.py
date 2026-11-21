"""Mechanical extraction and registered composition of generated cut-paper art.
No anatomy is drawn here: masks separate generated components, and repeated
assembly stages reuse the same pixels at the same magnification.
Run: uv run --with pillow python projects/anatomy-study/art-study/cut-paper/extract.py
"""
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageChops
import json
ROOT=Path(__file__).parent
OUT=ROOT/'assets'
OUT.mkdir(exist_ok=True)
L=Image.Resampling.LANCZOS
registry={}

def save(im,name):
    im.save(OUT/(name+'.png'))
    return im

def blank(size): return Image.new('RGBA',size)
def bounds(im): return im.getchannel('A').point(lambda a:255 if a>30 else 0).getbbox()
def trim(im):
    b=bounds(im)
    return im.crop(b) if b else im

def fit(im,size,padding=0):
    result=blank(size); copy=im.copy();copy.thumbnail((size[0]-padding*2,size[1]-padding*2),L)
    result.alpha_composite(copy,((size[0]-copy.width)//2,(size[1]-copy.height)//2));return result

def atlas(name,cols,rows):
    im=Image.open(ROOT/'masters'/(name+'-atlas.png')).convert('RGBA');parts=[]
    for i in range(cols*rows):
        box=(round(i%cols*im.width/cols),round(i//cols*im.height/rows),round((i%cols+1)*im.width/cols),round((i//cols+1)*im.height/rows))
        if name=='cell' and i==5:box=(831,421,1254,808)
        tile=im.crop(box);b=bounds(tile);parts.append(tile.crop(b) if b else tile)
        registry[f'{name}:{i}']={'cell':box,'visible_bounds':b}
    return parts

def place(canvas,im,box):
    x,y,w,h=box;canvas.alpha_composite(fit(im,(w,h)),(x,y))

def label(im,words,xy,size=30):
    ImageDraw.Draw(im).text(xy,words,font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size),fill='#486463')

# Blank paper only. This source crop contains no diagram, text, or anatomy.
bg=Image.open(ROOT/'masters/background-atlas.png').convert('RGBA')
paper=bg.crop((30,400,480,730)).resize((1560,2340),L)
for name in ['cell','arm','hearing','meal']:save(paper,'background-'+name)
neutral=paper.crop((0,0,280,200));save(neutral,'neutral');save(blank(neutral.size),'neutral-overlay')

cell=atlas('cell',3,3)
# Separate the actual aqueous interior from the generated bag. Complementary
# alpha masks guarantee that the original bag is reconstructed exactly.
bag=fit(cell[5],(600,550),10)
# Interior polygon follows the aqueous face, stopping before inner lipid heads.
source=Image.open(ROOT/'masters/cell-atlas.png').convert('RGBA').crop((831,421,1254,808))
mask=Image.new('L',source.size)
ImageDraw.Draw(mask).polygon([(130,133),(160,115),(190,105),(220,103),(250,110),(280,122),(307,139),(329,159),(348,183),(359,205),(351,226),(335,244),(308,260),(273,272),(239,280),(205,282),(169,278),(136,270),(107,258),(83,243),(66,225),(58,206),(62,185),(73,168),(89,153),(108,142)],fill=255)
water=source.copy();water.putalpha(ImageChops.multiply(source.getchannel('A'),mask))
wall=source.copy();wall.putalpha(ImageChops.multiply(source.getchannel('A'),ImageChops.invert(mask)))
# Same source-to-bag transformation, then crop each current geometry without resizing.
# Sources use the same canvas so membrane and aqueous volume have identical scale.
water=fit(water,(600,550),10);wall=fit(wall,(600,550),10)
save(trim(water),'prelude-water');save(trim(wall),'prelude-phospholipids')
bag=Image.alpha_composite(wall,water);save(bag,'opening-cell')
# DNA and nuclear envelope are assembled from the exact standalone pieces.
envelope=fit(cell[3],(230,230),5);dna=fit(cell[2],(95,145),3)
save(trim(envelope),'opening-nuclear-envelope');save(trim(dna),'opening-dna')
nucleus=envelope.copy();nucleus.alpha_composite(dna,(68,42));save(trim(nucleus),'opening-nucleus')
nucleus_layer=blank(bag.size);nucleus_layer.alpha_composite(nucleus,(190,170));save(nucleus_layer,'cell-nucleus-overlay')
save(blank(bag.size),'cell-neutral-overlay')
save(fit(cell[6],(360,300),10),'prelude-myoblasts')
save(fit(cell[7],(340,300),10),'school-bone-mineral')
save(fit(cell[8],(360,300),10),'muscle-reference')

# One common hearing coordinate system. Components are never independently
# enlarged on export; each stage is cropped to its occupied geometry only.
ear=atlas('hearing',3,4)
hearing_canvas=(850,530)
components={
 'outer':(fit(ear[0],(320,280)),(0,0)),
 'drum':(fit(ear[1],(44,100)),(257,110)),
 'bones':(fit(ear[3],(108,90)),(293,126)),
 'cochlea':(fit(ear[5],(220,220)),(395,64)),
 'sensory':(fit(ear[6],(252,190)),(422,340)),
 'pathways':(fit(ear[9],(222,180)),(595,14)),
}
# Locator leader and magnification label belong to the sensory component.
sensory_canvas=blank(hearing_canvas)
place(sensory_canvas,ear[6],(422,340,252,190))
ImageDraw.Draw(sensory_canvas).line([(527,270),(548,320),(548,340)],fill='#486463',width=3)
label(sensory_canvas,'SENSORY TISSUE / ENLARGED',(420,318),15)
stages={
 'outer-ear':['outer'],'eardrum':['drum'],'ear-drum':['outer','drum'],
 'ear-bones':['bones'],'conducting-ear':['outer','drum','bones'],
 'cochlea':['cochlea'],'hair-cells':['sensory'],
 'sensing-ear':['cochlea','sensory'],
 'receiving-ear':['outer','drum','bones','cochlea','sensory'],
 'hearing-pathways':['pathways'],'inner-pathways':['cochlea','sensory','pathways'],
 'ears':['outer','drum','bones','cochlea','sensory','pathways'],
}
hearing_registration={}
for name,parts in stages.items():
    result=blank(hearing_canvas)
    for part in parts:
        if part=='sensory':result.alpha_composite(sensory_canvas)
        else:
            im,xy=components[part];result.alpha_composite(im,xy)
    b=bounds(result);save(result.crop(b),name)
    hearing_registration[name]={'parts':parts,'crop':b,'canvas':hearing_canvas}

meal=atlas('meal',3,4)
meal_names=['starch','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat','bile','small-droplets','fat-products','bone-mineral-window-reference']
for i,name in enumerate(meal_names):
    im=fit(meal[i],(340,300),10)
    cutoff={'fat-products':304,'amino-acids':295,'fat':311}.get(name)
    if cutoff is not None:im.paste((0,0,0,0),(cutoff,0,im.width,im.height))
    save(im,name)

arm=atlas('arm',2,3)
# Exactly one skeleton is partitioned between the two receivers. Both
# transparent stacks share one scene origin and have complementary alpha.
skeleton=Image.open(ROOT/'masters/arm-skeleton-transparent.png').convert('RGBA').resize((1560,2340),L)
front=skeleton.copy();front.paste((0,0,0,0),(805,0,1560,2340))
back=skeleton.copy();back.paste((0,0,0,0),(0,0,805,2340))
place(front,arm[2],(140,1150,420,360));label(front,'RADIUS',(140,1100))
place(back,arm[2],(1030,1150,420,360));label(back,'ULNA',(1030,1100))
label(front,'FRONT',(400,230),34);label(back,'BACK',(1030,230),34)
ImageDraw.Draw(front).line([(805,1130),(655,1100),(560,1260)],fill='#557977',width=4)
ImageDraw.Draw(back).line([(900,1140),(990,1100),(1030,1260)],fill='#557977',width=4)
save(front,'arm-front-base');save(back,'arm-back-base')
arm_layers={}
for side,index,box,window in [('front',0,(620,180,210,820),(140,1150,420,360)),('back',1,(820,220,180,700),(1030,1150,420,360))]:
    muscle=blank(front.size)
    # Transform generated vertical muscle onto the receiver tendon route.
    x,y,w,h=box;part=trim(arm[index]).resize((w,h),L)
    for row in range(h):
        shift=70 if side=='front' else -30
        muscle.alpha_composite(part.crop((0,row,w,row+1)),(x+round(shift*row/(h-1)),y+row))
    label(muscle,'BENDS ELBOW' if side=='front' else 'STRAIGHTENS ELBOW',(120 if side=='front' else 1030,990),28)
    if side=='front':
        place(muscle,arm[4],(115,1600,520,350));label(muscle,'FIBRES IN CONNECTIVE TISSUE',(115,1980),27)
    else:
        place(muscle,arm[5],(890,1640,560,300));label(muscle,'CELLS JOIN INTO LONG FIBRES',(890,1980),27)
    save(muscle,f'arm-{side}-muscle-overlay')
    mineral=blank(front.size);place(mineral,arm[3],window);save(mineral,f'arm-{side}-mineral-overlay')
    arm_layers[side]={'muscle':muscle,'mineral':mineral}
# Explicit complete and partial states for coordinator comparison panels.
state_catalog={'cell':[],'arm':[]}
for filled in [False,True]:
    result=bag.copy()
    if filled:result.alpha_composite(nucleus_layer)
    name='state-cell-'+('nucleus' if filled else 'empty');save(result,name)
    state_catalog['cell'].append({'name':'Nucleus fitted' if filled else 'Empty membrane bag','asset':'assets/'+name+'.png'})
for f in range(4):
    for b in range(4):
        result=Image.alpha_composite(front,back);parts=[]
        for side,bits in [('front',f),('back',b)]:
            for bit,part in [(1,'mineral'),(2,'muscle')]:
                if bits&bit:result.alpha_composite(arm_layers[side][part]);parts.append(side+' '+part)
        name=f'state-arm-f{f}-b{b}';save(result,name)
        state_catalog['arm'].append({'name':', '.join(parts) or 'Bare receiver','asset':'assets/'+name+'.png','front':f,'back':b})
(ROOT/'state-catalog.json').write_text(json.dumps(state_catalog,indent=2)+'\n')
(ROOT/'registration.json').write_text(json.dumps({'background_size':[1560,2340],'paper_source_crop':[30,400,480,730],'icon_reference_scale':0.25,'atlas_extractions':registry,'cell':{'bag_canvas':[600,550],'nucleus_origin':[190,170],'nucleus_size':[230,230],'water_and_membrane':'Complementary masks from cell-atlas crop [831,421,1254,808]; common 600x550 transform, cropped standalone without rescaling.'},'hearing':{'components':{k:{'size':im.size,'origin':xy} for k,(im,xy) in components.items()},'stages':hearing_registration,'sensory_detail':'Identical anchored tissue + locator in every applicable stage.'},'arm':{'art_center':[780,1170],'front_hitbox':[535,900,540,1360],'back_hitbox':[1090,900,500,1360],'skeleton_partition_x':805,'mineral_windows':{'front':[140,1150,420,360],'back':[1030,1150,420,360]}}},indent=2)+'\n')
print('Exported 33 comparison identities, five relevant fittings, 18 complete/partial compound states, four blank backgrounds.')
# Retained artwork contact sheet is assembled only from final exports.
contact_names=[
 'prelude-phospholipids','prelude-water','opening-dna','opening-nuclear-envelope','opening-nucleus','opening-cell',
 'prelude-myoblasts','school-bone-mineral','arm-front-base','arm-back-base',
 *stages.keys(),*meal_names[:11],
 'cell-nucleus-overlay','arm-front-mineral-overlay','arm-front-muscle-overlay','arm-back-mineral-overlay','arm-back-muscle-overlay',
 *[Path(s['asset']).stem for family in state_catalog.values() for s in family],
]
contact=Image.new('RGB',(1440,((len(contact_names)+3)//4)*310),'#faf9f4')
for i,name in enumerate(contact_names):
    im=Image.open(OUT/(name+'.png')).convert('RGBA');im.thumbnail((340,270),L)
    x=i%4*360;y=i//4*310;contact.paste(im,(x+(340-im.width)//2,y),im)
    ImageDraw.Draw(contact).text((x+5,y+280),name,fill='#334c4b',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',15))
contact.save(ROOT/'contact-sheet.jpg',quality=90)

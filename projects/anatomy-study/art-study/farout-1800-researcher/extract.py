"""Mechanical atlas extraction, masking and registration; no anatomy is painted.
Run from the repository root with uv run --with pillow python PATH/extract.py.
Only this theme's selected built-in imagegen masters are used.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
R = Image.Resampling.LANCZOS

def masked(im, mask):
    result = im.copy()
    result.putalpha(ImageChops.multiply(im.getchannel('A'), mask))
    return result

def polygon(size, points):
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).polygon(points,fill=255)
    return mask

def tight(im, pad=8):
    box=im.getbbox()
    if not box: raise ValueError('Empty illustration')
    # Cropping changes canvas bounds, never anatomical magnification.
    out=Image.new('RGBA',(box[2]-box[0]+2*pad,box[3]-box[1]+2*pad))
    out.alpha_composite(im.crop(box),(pad,pad))
    return out

groups = {
    1: ['lipids','water','dna','envelope','nucleus','cell','muscle-cells','mineral'],
    8: ['outer-ear','eardrum','ear-drum','ossicles','conducting-ear','cochlea','hair-cells','sensing-cochlea','receiving-ear','hearing-pathways','inner-ear-pathways','ears'],
    18: ['starch','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat','bile','droplets','fat-products'],
}
raw={}
for chapter,names in groups.items():
    master=Image.open(ROOT/'source'/f'atlas-{chapter}.png').convert('RGBA')
    rows=2 if chapter==1 else 3
    for i,name in enumerate(names):
        x,y=i%4,i//4
        crop=master.crop((round(x*master.width/4),round(y*master.height/rows),round((x+1)*master.width/4),round((y+1)*master.height/rows)))
        size=384 if name=='cell' else 320
        exported=crop.resize((size,size),R)
        cutoff={'hair-cells':295,'hearing-pathways':300,'inner-ear-pathways':298,'amino-acids':280}.get(name)
        if cutoff is not None: exported.paste((0,0,0,0),(cutoff,0,size,size))
        raw[name]=exported
        exported.save(ASSETS/f'{name}.png')

# All four backgrounds are only a selected clear paper region of our old master.
# The source crop contains no labels, diagrams, anatomy or decorative objects.
page=Image.open(ROOT/'source'/'chapter-4.png').convert('RGB')
tile=page.crop((100,1220,930,1480))
paper=Image.new('RGB',(1024,1536))
for row in range(6):
    for col in range(2):
        piece=ImageOps.mirror(tile) if col%2 else tile
        if row%2:piece=ImageOps.flip(piece)
        paper.paste(piece,(col*tile.width,row*tile.height))
for chapter in [1,4,8,18]: paper.save(ASSETS/f'chapter-{chapter}.png')

# Backward-plan the opening from the actual bag pixels. Water is the open aqueous
# volume; lipid material is the remaining curved wall with identical unit scale.
bag=raw['cell']
water_mask=polygon(bag.size,[(49,185),(64,163),(95,144),(129,133),(170,124),(209,124),(243,135),(274,150),(301,176),(319,198),(303,213),(276,228),(240,242),(204,253),(164,255),(125,247),(94,233),(70,215),(56,200)])
water=masked(bag,water_mask)
lipids=masked(bag,ImageChops.invert(water_mask))
water.save(ASSETS/'water.png');lipids.save(ASSETS/'lipids.png')
# The fitted nucleus is also the portable artwork, at exactly its installed size.
nucleus=raw['nucleus'].resize((138,138),R)
nucleus.save(ASSETS/'nucleus.png')
overlay=Image.new('RGBA',bag.size);overlay.alpha_composite(nucleus,(120,118))
overlay.save(ASSETS/'cell-nucleus.png')
Image.new('RGBA',bag.size).save(ASSETS/'cell-neutral-overlay.png')
Image.new('RGBA',(320,320)).save(ASSETS/'neutral-icon.png')

# Ear stages are sums of six registered actual constituents, not six independently
# drawn atlas states. The cochlear detail and its inset are split from ONE source.
# The original locator/leader is retained with the cochlea; every stage containing
# hearing cells has precisely the same inset pixels, dimensions and relative site.
ear_size=(900,420)
parts={}
def ear_part(name,im,xy):
    out=Image.new('RGBA',ear_size);out.alpha_composite(im,xy);parts[name]=out

ear_part('outer',raw['outer-ear'],(0,50))
ear_part('drum',raw['eardrum'].resize((64,128),R),(278,145))
ear_part('bones',raw['ossicles'].resize((125,105),R),(310,142))
cochlear=raw['sensing-cochlea']
coil=cochlear.copy();coil.paste((0,0,0,0),(204,0,320,320))
hairs=cochlear.copy();hairs.paste((0,0,0,0),(0,0,204,320))
ear_part('coil',coil,(414,62))
ear_part('hairs',hairs,(414,62))
ear_part('nerve',raw['hearing-pathways'].resize((240,240),R),(610,0))
ear_states={
 'outer-ear':['outer'],'eardrum':['drum'],'ear-drum':['outer','drum'],
 'ossicles':['bones'],'conducting-ear':['outer','drum','bones'],
 'cochlea':['coil'],'hair-cells':['hairs'],'sensing-cochlea':['coil','hairs'],
 'receiving-ear':['outer','drum','bones','coil','hairs'],
 'hearing-pathways':['nerve'],'inner-ear-pathways':['coil','hairs','nerve'],
 'ears':['outer','drum','bones','coil','hairs','nerve'],
}
registration={}
for name,keys in ear_states.items():
    out=Image.new('RGBA',ear_size)
    for key in keys: out.alpha_composite(parts[key])
    registration[name]={'constituents':keys,'workingBounds':out.getbbox()}
    tight(out).save(ASSETS/f'{name}.png')

# The arm is traced from the pre-fitting master. Both visible receivers own
# disjoint halves of the single scaffold, with no anatomy baked into the paper.
# Existing generated muscle spans and bone detail provide all fitted pixels.
SIZE=(1560,2340)
base=page.convert('RGBA')
outline=polygon(base.size,[(72,290),(83,242),(115,198),(133,150),(176,105),(220,96),(241,108),(239,150),(270,145),(284,114),(312,117),(320,157),(344,174),(379,175),(409,196),(434,252),(465,325),(500,420),(516,550),(541,639),(557,687),(647,695),(705,711),(820,769),(928,806),(980,814),(1005,843),(1023,894),(1000,931),(967,950),(940,913),(850,874),(742,831),(632,803),(560,780),(480,766),(416,735),(383,700),(371,652),(347,609),(317,574),(272,547),(233,492),(221,432),(215,378),(176,364),(130,381),(98,365),(74,335)])
polygons={
 'front-muscle':[(252,235),(284,247),(290,290),(326,368),(351,459),(370,558),(398,640),(394,669),(379,648),(361,602),(324,571),(270,533),(235,476),(225,409),(233,348),(252,292)],
 'back-muscle':[(359,238),(383,246),(398,282),(460,326),(492,383),(508,458),(518,551),(535,626),(543,670),(524,678),(510,634),(474,592),(429,535),(398,470),(375,392),(365,316)],
}
# Removing future muscle regions also removes the earlier text in those gaps.
for pts in polygons.values(): outline=ImageChops.subtract(outline,polygon(base.size,pts))
# Include the two located matrix enlargements and their original leader lines.
d=ImageDraw.Draw(outline)
for box in [(538,880,695,1030),(734,880,890,1030)]:d.ellipse(box,fill=255)
d.line([(653,805),(624,884)],fill=255,width=5)
d.line([(763,772),(798,884)],fill=255,width=5)
front_half=polygon(base.size,[(0,0),(301,0),(301,180),(318,330),(360,490),(405,650),(449,707),(560,745),(660,773),(780,823),(1024,926),(1024,1536),(0,1536)])
mineral_windows={
 'front-mineral':[(584,744),(615,747),(658,766),(684,788),(689,807),(670,812),(640,802),(610,790),(583,774),(571,758)],
 'back-mineral':[(664,710),(688,712),(731,731),(770,751),(784,770),(775,781),(749,778),(713,762),(680,744),(656,725)],
}
mineral_masks={}
for name,points in mineral_windows.items():
    mask=polygon(base.size,points)
    ImageDraw.Draw(mask).ellipse((538,880,695,1030) if name=='front-mineral' else (734,880,890,1030),fill=255)
    mineral_masks[name]=mask
# Each receiver owns its entire mineral window even where the dividing line
# through the arm would otherwise cross it. Independent layers cannot erase it.
front_half=ImageChops.lighter(front_half,mineral_masks['front-mineral'])
front_half=ImageChops.subtract(front_half,mineral_masks['back-mineral'])
for name,region in [('front',front_half),('back',ImageChops.invert(front_half))]:
    masked(base,ImageChops.multiply(outline,region)).resize(SIZE,R).save(ASSETS/f'arm-{name}-base.png')
complete=Image.open(ROOT/'source'/'chapter-arm.png').convert('RGBA')
for name,pts in polygons.items():
    masked(complete,polygon(complete.size,pts)).resize(SIZE,R).save(ASSETS/f'{name}.png')
for name,mask in mineral_masks.items():
    masked(complete,mask).resize(SIZE,R).save(ASSETS/f'{name}.png')
# Old transparent receiver no longer participates in the manuscript.
old=ASSETS/'arm-base.png'
if old.exists(): old.unlink()

icons={}
for identity,name in zip(['id:prelude-phospholipids','id:prelude-water','id:opening-dna','id:opening-nuclear-envelope','id:opening-nucleus','id:opening-cell','id:prelude-myoblasts','id:school-bone-mineral'],groups[1]):icons[identity]=f'assets/{name}.png'
ear_names=['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears']
food_names=['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products']
for names,chapter in [(ear_names,8),(food_names,18)]:
    for identity,name in zip(names,groups[chapter]):icons['name:'+identity]=f'assets/{name}.png'
icons['id:arm-front-tendons']='assets/arm-front-base.png'
icons['id:arm-back-tendons']='assets/arm-back-base.png'
art={
 'headingIcon':'assets/nucleus.png','defaultIcon':'assets/neutral-icon.png','defaultOverlay':'assets/neutral-icon.png','defaultBackground':'../../placeholder.svg',
 'chapterBackgrounds':{str(n):f'assets/chapter-{n}.png' for n in [1,4,8,18]},'itemIcons':icons,
 'slotIcons':{
   'id:opening-cell':{'id:opening-nucleus':'assets/cell-nucleus.png',**{i:'assets/cell-neutral-overlay.png' for i in ['id:opening-mitochondria','id:school-sugar-carrier','id:school-ribosome']}},
   'id:arm-front-tendons':{'id:school-bone-mineral':'assets/front-mineral.png','id:prelude-myoblasts':'assets/front-muscle.png'},
   'id:arm-back-tendons':{'id:school-bone-mineral':'assets/back-mineral.png','id:prelude-myoblasts':'assets/back-muscle.png'}},
 'hotspots':{'4':{
   'id:arm-front-tendons':{'center':[512,768],'hitbox':{'center':[290,450],'size':[180,360]}},
   'id:arm-back-tendons':{'center':[512,768],'hitbox':{'center':[458,450],'size':[150,360]}}}}
}
(ROOT/'art-map.json').write_text(json.dumps(art,indent=2)+'\n')
(ROOT/'registration.json').write_text(json.dumps({'earWorkingCanvas':ear_size,'earStates':registration,'armSourceCanvas':base.size,'armExportCanvas':SIZE,'paperSource':'source/chapter-4.png','paperCrop':[100,1220,930,1480]},indent=2)+'\n')

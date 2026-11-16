"""Mechanical atlas extraction and exact scene registration. Run with uv --with pillow.
All original marks come from retained imagegen masters; no anatomy is drawn here.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json

ROOT=Path(__file__).resolve().parent
A=ROOT/'assets'; M=ROOT/'masters'; A.mkdir(exist_ok=True)
S=1560/1024; SIZE=(1560,3376)

def paper_page(source):
    im=Image.open(M/source).convert('RGB')
    # Extend only blank notebook paper; do not stretch anatomical drawings.
    page=Image.new('RGB',(1024,2216))
    page.paste(im,(0,0))
    strip=im.crop((0,1152,1024,1536))
    for y in range(1536,2216,384):page.paste(strip,(0,y))
    return page.resize(SIZE,Image.Resampling.LANCZOS)

for name,src in [('cell','cell-background.png'),('arm','arm-empty.png'),('hearing','hearing-background.png'),('digestion','digestion-corrected.png')]:
    paper_page(src).save(A/f'{name}-background.webp',quality=94)
Image.new('RGB',SIZE,'#f7f5f1').save(A/'unillustrated.webp',quality=90)
Image.new('RGBA',(1,1)).save(A/'empty.png')
Image.new('RGBA',(400,400)).save(A/'empty-cell.png')
Image.new('RGBA',SIZE).save(A/'arm-base.png')

def isolate(im):
    im=im.convert('RGBA')
    px=[]
    for r,g,b,a in im.getdata():
        # White-paper removal preserves coloured pencil and pale blue water.
        alpha=0 if min(r,g,b)>246 else 255
        px.append((r,g,b,alpha))
    im.putdata(px)
    box=im.getbbox()
    return im.crop(box) if box else im

families={
 'cell':['lipids','water','dna','envelope','nucleus','cell','muscle-cells','mineral','identity','fitted-nucleus','unused-mitochondrion'],
 'hearing':['outer-ear','eardrum','ear-eardrum','bones','conducting-ear','cochlea','hair-cells','sensing-ear','receiving-ear','hearing-pathways','inner-pathways','ears'],
 'digestion':['starch','saliva','short-starch','enzymes','glucose','protein','amino-acids','fat','bile','fat-droplets','fat-products']
}
registry={}
for family,names in families.items():
    atlas=Image.open(M/f'{family}-atlas.png')
    for i,name in enumerate(names):
        if name=='unused-mitochondrion': continue
        col,row=i%3,i//3
        # Measured actual atlas: 1086x1448, 362px cells. Bounds exclude neighbours.
        box=(col*362+4,row*362+4,(col+1)*362-4,(row+1)*362-4)
        art=isolate(atlas.crop(box))
        target=400 if name=='cell' else 320
        if name=='identity':target=256
        art.thumbnail((target-20,target-20),Image.Resampling.LANCZOS)
        out=Image.new('RGBA',(target,target))
        out.alpha_composite(art,((target-art.width)//2,(target-art.height)//2))
        if name=='inner-pathways':
            # Remove the neighbouring atlas cell's fragment without moving anatomy.
            out.paste((0,0,0,0),(300,0,target,target))
        out.save(A/f'{name}.png')
        registry[name]={'master':f'{family}-atlas.png','bounds':box,'export':[target,target]}

# The nucleus is deliberately inspection-magnified when loose; its installed
# appearance is mechanically scaled and placed inside the existing cell fluid.
nuc=Image.open(A/'fitted-nucleus.png');nuc.thumbnail((146,146),Image.Resampling.LANCZOS)
overlay=Image.new('RGBA',(400,400));overlay.alpha_composite(nuc,(140,163));overlay.save(A/'cell-nucleus.png')

# Fittings use precise polygons from the original complete arm. All four are
# independent and registered to the empty edit at identical original coordinates.
polygons={
 'front-muscle':[(574,172),(556,202),(533,270),(513,295),(478,328),(450,366),(428,408),(420,452),(420,510),(425,548),(436,576),(456,552),(475,524),(499,484),(515,439),(535,386),(553,317),(562,260),(581,207),(598,173)],
 'back-muscle':[(642,226),(632,264),(626,303),(631,344),(644,385),(645,426),(636,470),(615,518),(588,559),(564,587),(545,578),(535,540),(531,497),(537,451),(549,409),(566,364),(584,318),(604,272),(623,228)],
 'front-mineral':[(419,747),(440,750),(431,808),(410,803)],
 'back-mineral':[(474,770),(491,777),(480,831),(459,826)]
}
complete=Image.open(M/'arm-background.png').convert('RGBA')
for name,poly in polygons.items():
    mask=Image.new('L',complete.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(.65))
    layer=complete.copy();layer.putalpha(mask)
    full=Image.new('RGBA',(1024,2216));full.alpha_composite(layer)
    full.resize(SIZE,Image.Resampling.LANCZOS).save(A/f'{name}.png')
    registry[name]={'master':'arm-background.png','polygon':poly,'registeredCanvas':SIZE}

# Refresh: blank paper, shared physical constituents, and anatomy owned by objects.
from PIL import ImageChops
# Blank lower sheet only: same generated ruling and grain, zero labels/anatomy.
paper=Image.open(M/'arm-empty.png').convert('RGB').crop((0,1030,1024,1536))
page=Image.new('RGB',(1024,2216))
for y in range(0,2216,paper.height):page.paste(paper,(0,y))
for family in ['cell','arm','hearing','digestion']:
    page.resize(SIZE,Image.Resampling.LANCZOS).save(A/f'{family}-background.webp',quality=94)
registry['backgrounds']={'master':'arm-empty.png','blankCrop':[0,1030,1024,1536],'method':'repeat blank paper vertically; no content'}

# Water and the entire membrane shell come from the actual completed bag pixels.
cell=Image.open(A/'cell.png').convert('RGBA')
water=cell.copy(); shell=cell.copy()
wa=[]; sa=[]
for r,g,b,a in cell.getdata():
    fluid=b>r*1.18 and g>r*1.08
    wa.append(a if fluid else 0);sa.append(0 if fluid else a)
water.putalpha(Image.frombytes('L',cell.size,bytes(wa)))
shell.putalpha(Image.frombytes('L',cell.size,bytes(sa)))
water.save(A/'water.png');shell.save(A/'lipids.png')
registry['water']=registry['lipids']={'master':'cell-atlas.png','bounds':[728,366,1082,720],'sharedCanvas':[400,400],'method':'blue aqueous-volume and complementary membrane masks of bag, no individual normalization'}
# Envelope and DNA use one physical scale, with nucleus assembled from those pixels.
env=Image.open(A/'envelope.png').convert('RGBA').resize((150,150),Image.Resampling.LANCZOS)
dna=Image.open(A/'dna.png').convert('RGBA').resize((58,100),Image.Resampling.LANCZOS)
nucleus=env.copy();nucleus.alpha_composite(dna,(46,25))
env.save(A/'envelope.png');dna.save(A/'dna.png');nucleus.save(A/'nucleus.png')
overlay=Image.new('RGBA',(400,400));overlay.alpha_composite(nucleus,(125,140));overlay.save(A/'cell-nucleus.png')
registry['nucleus']={'constituents':['envelope.png','dna.png'],'canvas':[150,150],'DNAoffset':[46,25],'fittedOffset':[125,140],'fittedCanvas':[400,400],'scale':'identical loose and fitted'}

# Ear families use immutable constituent images at constant pixel magnification.
# Existing sensing-ear includes its generated located enlargement and leader.
outer=Image.open(A/'outer-ear.png').convert('RGBA')
drum=Image.open(A/'eardrum.png').convert('RGBA').resize((49,82),Image.Resampling.LANCZOS)
bones=Image.open(A/'bones.png').convert('RGBA').resize((99,99),Image.Resampling.LANCZOS)
sensing=Image.open(A/'sensing-ear.png').convert('RGBA')
pathway=Image.open(A/'hearing-pathways.png').convert('RGBA').resize((255,255),Image.Resampling.LANCZOS)
# Take cochlea and the located hair-cell panel from exactly the sensing master.
cochlea=Image.open(A/'cochlea.png').convert('RGBA').resize((190,160),Image.Resampling.LANCZOS)
# Reuse the original generated locator and circular enlargement, masking out
# its earlier coil so the supplied coil itself survives every assembled state.
located=sensing.copy(); lm=Image.new('L',sensing.size)
ImageDraw.Draw(lm).polygon([(125,110),(211,143),(262,140),(306,168),(320,222),(315,280),(278,316),(208,320),(164,293),(146,251),(147,196)],fill=255)
located.putalpha(ImageChops.multiply(located.getchannel('A'),lm))
sensing=Image.new('RGBA',(320,320));sensing.alpha_composite(cochlea,(0,20));sensing.alpha_composite(located)
hair=located.crop((143,130,320,320))
# Cut only blank margins, with no rescaling. Offsets retain assembly positions.
def save_parts(name,parts):
    canvas=Image.new('RGBA',(880,410))
    for art,pos in parts:canvas.alpha_composite(art,pos)
    box=canvas.getbbox();canvas.crop(box).save(A/f'{name}.png')
    registry[name]={'constituentOffsets':[[pos[0],pos[1]] for art,pos in parts],'assemblyCrop':list(box),'method':'same constituent pixels, tight crop without rescaling'}
O=(outer,(0,0));D=(drum,(264,123));B=(bones,(297,110));Sense=(sensing,(380,75));P=(pathway,(525,85))
for name,parts in [('outer-ear',[O]),('eardrum',[D]),('ear-eardrum',[O,D]),('bones',[B]),('conducting-ear',[O,D,B]),('cochlea',[(cochlea,(380,75))]),('hair-cells',[(hair,(523,205))]),('sensing-ear',[Sense]),('receiving-ear',[O,D,B,Sense]),('hearing-pathways',[P]),('inner-pathways',[P,Sense]),('ears',[P,O,D,B,Sense])]:save_parts(name,parts)

# Disjoint anatomical receiver regions compose one arm. Both own visible bones
# and tendons; neither is an invisible rectangle over a completed background.
empty=Image.open(M/'arm-empty.png').convert('RGBA')
frontpoly=[(591,159),(623,189),(644,219),(631,263),(607,327),(583,401),(563,478),(547,548),(543,589),(516,619),(493,706),(464,800),(440,896),(438,944),(415,971),(396,991),(314,991),(355,939),(377,891),(399,806),(413,719),(429,648),(423,592),(412,549),(416,475),(426,403),(449,349),(490,298),(530,250),(552,200)]
backpoly=[(591,159),(623,189),(644,219),(631,263),(607,327),(583,401),(563,478),(547,548),(543,589),(516,619),(493,706),(464,800),(440,896),(438,944),(460,922),(477,857),(495,783),(516,699),(537,634),(572,598),(605,549),(636,485),(655,426),(648,364),(649,315),(687,312),(716,257),(731,183),(713,145),(673,119),(631,107),(604,121)]
# Keep actual paper-light bone surfaces inside precise subject masks. Remove
# unoccupied muscle-space polygons (which otherwise contain notebook ruling).
for name,poly,holes in [('arm-front',frontpoly,['front-muscle']),('arm-back',backpoly,['back-muscle'])]:
    mask=Image.new('L',empty.size);d=ImageDraw.Draw(mask);d.polygon(poly,fill=255)
    for hole in holes:d.polygon(polygons[hole],fill=0)
    # Exclude an unrelated caption tail outside the lower radius.
    d.rectangle((0,835,394,929),fill=0)
    layer=empty.copy();layer.putalpha(mask)
    full=Image.new('RGBA',(1024,2216));full.alpha_composite(layer)
    full.resize(SIZE,Image.Resampling.LANCZOS).save(A/f'{name}.png')
    registry[name]={'master':'arm-empty.png','polygon':poly,'removedMuscleSpace':holes,'registeredCanvas':SIZE,'center':[780,1688]}
# The muscle and mineral overlays remain the same exact master coordinates.

item={
 'id:prelude-phospholipids':'lipids','id:prelude-water':'water','id:opening-dna':'dna','id:opening-nuclear-envelope':'envelope','id:opening-nucleus':'nucleus','id:opening-cell':'cell','id:prelude-myoblasts':'muscle-cells','id:school-bone-mineral':'mineral','id:arm-front-tendons':'arm-front','id:arm-back-tendons':'arm-back',
 'name:Outer ears and canals':'outer-ear','name:Eardrums':'eardrum','name:Outer ears with eardrums':'ear-eardrum','name:Middle-ear bones':'bones','name:Sound-conducting ears':'conducting-ear','name:Coiled inner-ear chambers and fluid':'cochlea','name:Hearing cells with tiny hairs':'hair-cells','name:Vibration-sensitive inner ears':'sensing-ear','name:Sound-receiving ears':'receiving-ear','name:Hearing pathways':'hearing-pathways','name:Inner ears with hearing pathways':'inner-pathways','name:Ears':'ears',
 'name:Starchy food':'starch','name:Saliva':'saliva','name:Shorter starch chains':'short-starch','name:Digestive enzymes':'enzymes','name:Meal glucose':'glucose','name:Protein food':'protein','name:Meal amino acids':'amino-acids','name:Fat food':'fat','name:Bile':'bile','name:Small fat droplets':'fat-droplets','name:Fat digestion products':'fat-products'
}
positions={}
for ids in [['id:prelude-phospholipids','id:prelude-water','id:opening-dna','id:opening-nuclear-envelope'],['name:Outer ears and canals','name:Eardrums','name:Middle-ear bones','name:Coiled inner-ear chambers and fluid','name:Hearing cells with tiny hairs','name:Hearing pathways'],['name:Starchy food','name:Saliva','name:Digestive enzymes','name:Protein food','name:Fat food','name:Bile']]:
    for i,k in enumerate(ids):positions[k]=[360+(i%3)*420,2180+(i//3)*510]
positions['id:school-bone-mineral']=[1120,2470]
def hit(x,y,w,h):return {'center':[780,1688],'icon':'assets/arm-base.png','hitbox':{'center':[round(x*S),round(y*S)],'size':[round(w*S),round(h*S)]}}
artmap={'headingIcon':'assets/identity.png','defaultIcon':'../../placeholder.svg','defaultOverlay':'assets/empty.png','defaultBackground':'assets/unillustrated.webp',
 'chapterBackgrounds':{str(n):f'assets/{name}-background.webp' for n,name in [(1,'cell'),(4,'arm'),(8,'hearing'),(18,'digestion')]},
 'itemIcons':{k:f'assets/{v}.png' for k,v in item.items()},'itemPositions':positions,
 'slotIcons':{
  'id:opening-cell':{'id:opening-nucleus':'assets/cell-nucleus.png','id:opening-mitochondria':'assets/empty-cell.png','id:school-sugar-carrier':'assets/empty-cell.png','id:school-ribosome':'assets/empty-cell.png'},
  'id:arm-front-tendons':{'id:school-bone-mineral':'assets/front-mineral.png','id:prelude-myoblasts':'assets/front-muscle.png'},
  'id:arm-back-tendons':{'id:school-bone-mineral':'assets/back-mineral.png','id:prelude-myoblasts':'assets/back-muscle.png'}},
 'hotspots':{'4':{'id:arm-front-tendons':{**hit(456,520,150,600),'icon':'assets/arm-front.png'},'id:arm-back-tendons':{**hit(593,520,120,600),'icon':'assets/arm-back.png'}}}}
(ROOT/'art-map.json').write_text(json.dumps(artmap,indent=2)+'\n')
(ROOT/'extraction.json').write_text(json.dumps(registry,indent=2)+'\n')

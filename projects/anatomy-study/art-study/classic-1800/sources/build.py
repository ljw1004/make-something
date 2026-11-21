"""Reproduce mechanical exports and presentation-only manuscript.
Run from repository root: uv run --with pillow python projects/anatomy-study/art-study/classic-1800/sources/build.py
All illustrated pixels come from selected built-in imagegen masters.
"""
from pathlib import Path
from collections import deque
import re, json
from PIL import Image, ImageDraw, ImageEnhance, ImageChops

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'; OUT=ROOT/'assets'
OUT.mkdir(exist_ok=True)
SCALE=1560/1024

def cut_bg(im):
    """Border-connected ivory removal, preserving enclosed anatomical whites."""
    im=im.convert('RGBA'); w,h=im.size; px=im.load(); seen=set(); queue=deque()
    def put(x,y):
        if (x,y) in seen: return
        seen.add((x,y)); r,g,b,a=px[x,y]
        if r>230 and g>220 and b>200 and r-b<48: queue.append((x,y))
    for x in range(w): put(x,0); put(x,h-1)
    for y in range(h): put(0,y); put(w-1,y)
    while queue:
        x,y=queue.popleft(); r,g,b,a=px[x,y]; px[x,y]=(r,g,b,0)
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<w and 0<=yy<h: put(xx,yy)
    return im

def export_crop(atlas,index,cols,rows,name,edge=360,transparent=False):
    im=Image.open(SRC/atlas).convert('RGBA'); w,h=im.size
    x=index%cols; y=index//cols
    im=im.crop((round(x*w/cols),round(y*h/rows),round((x+1)*w/cols),round((y+1)*h/rows)))
    if not transparent: im=cut_bg(im)
    box=im.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox()
    if box: im=im.crop(box)
    factor=(edge-20)/max(im.size)
    im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(im.width+20,im.height+20)); canvas.alpha_composite(im,(10,10))
    # Preserve canvas registration while removing adjacent atlas specimens.
    cutoff={'muscle-cells':268, 'dna':195, 'eardrums':245}.get(name)
    if cutoff is not None:
        canvas.paste((0,0,0,0),(cutoff,0,canvas.width,canvas.height))
    canvas.save(OUT/f'{name}.png')
    return canvas

cellnames=['lipids','water','dna','nuclear-envelope','nucleus','cell','muscle-cells','bone-mineral']

def masked(im,mask):
    result=im.copy(); result.putalpha(ImageChops.multiply(im.getchannel('A'),mask)); return result

def fitted_export(im,name,factor=1,pad=12):
    box=im.getchannel('A').getbbox()
    if box: im=im.crop(box)
    im=im.resize((max(1,round(im.width*factor)),max(1,round(im.height*factor))),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(im.width+pad*2,im.height+pad*2));out.alpha_composite(im,(pad,pad));out.save(OUT/f'{name}.png');return out

# One generated cutaway establishes the material scale for every opening part.
master=Image.open(SRC/'cell-material-master.png').convert('RGBA')
cell=master.crop((54,49,989,984)); base=cell.resize((640,640),Image.Resampling.LANCZOS);base.save(OUT/'cell.png')
factor=640/935
volume_mask=Image.new('L',cell.size);ImageDraw.Draw(volume_mask).ellipse((66,62,858,858),fill=255)
fitted_export(masked(cell,volume_mask),'water',factor)
wall_mask=Image.new('L',cell.size);ImageDraw.Draw(wall_mask).rectangle((160,0,790,220),fill=255)
ImageDraw.Draw(wall_mask).ellipse((66,62,858,858),fill=0)
fitted_export(masked(cell,wall_mask),'lipids',factor)
nucleus=master.crop((1094,335,1487,727))
fitted_export(nucleus,'nucleus',factor)
inner=Image.new('L',nucleus.size);ImageDraw.Draw(inner).ellipse((48,48,343,343),fill=255)
fitted_export(masked(nucleus,inner),'dna',factor)
fitted_export(masked(nucleus,ImageChops.invert(inner)),'nuclear-envelope',factor)
nucleus=nucleus.resize((round(nucleus.width*factor),round(nucleus.height*factor)),Image.Resampling.LANCZOS)
overlay=Image.new('RGBA',(640,640));overlay.alpha_composite(nucleus,((640-nucleus.width)//2,(640-nucleus.height)//2));overlay.save(OUT/'cell-nucleus.png')
Image.new('RGBA',(640,640)).save(OUT/'cell-future-slot.png')
icon=Image.new('RGBA',(256,256)); thumb=base.copy(); thumb.thumbnail((240,240)); icon.alpha_composite(thumb,((256-thumb.width)//2,(256-thumb.height)//2)); icon.save(OUT/'icon.png')

ears=['outer-ears','eardrums','outer-eardrums','ear-bones','conducting-ears','coiled-chambers','hearing-cells','sensitive-ears','receiving-ears','hearing-pathways','inner-pathways','ears']
# Preserve auricle, eardrum and cochlea magnification through the family.
ear_factors=[1.35,.26,1.35,.48,1.35,.52,.48,.75,1.35,1.05,1.05,1.35]
for i,name in enumerate(ears):
    atlas=Image.open(SRC/'ear-atlas.png').convert('RGBA');w,h=atlas.size;x=i%4;y=i//4
    im=cut_bg(atlas.crop((round(x*w/4),round(y*h/3),round((x+1)*w/4)-(32 if name=='eardrums' else 0),round((y+1)*h/3))))
    fitted_export(im,name,ear_factors[i])

# A single constituent layout keeps the sensory inset in every later state.
ear_parts={n:Image.open(OUT/f'{n}.png').convert('RGBA') for n in ['outer-ears','eardrums','ear-bones','coiled-chambers','hearing-cells','hearing-pathways']}
ear_parts={n:im.crop(im.getbbox()) for n,im in ear_parts.items()}
ear_xy={'outer-ears':(0,0),'eardrums':(355,205),'ear-bones':(397,195),'coiled-chambers':(525,190),'hearing-cells':(550,400),'hearing-pathways':(650,40)}
def ear_stage(name,parts):
    im=Image.new('RGBA',(970,560))
    if 'hearing-cells' in parts:ImageDraw.Draw(im).line([(600,340),(620,400)],fill=(90,87,72,255),width=2)
    for n in parts:im.alpha_composite(ear_parts[n],ear_xy[n])
    fitted_export(im,name)
conducting=['outer-ears','eardrums','ear-bones'];sensory=['coiled-chambers','hearing-cells']
ear_stage('outer-eardrums',conducting[:2]);ear_stage('conducting-ears',conducting)
ear_stage('sensitive-ears',sensory);ear_stage('receiving-ears',conducting+sensory)
ear_stage('inner-pathways',sensory+['hearing-pathways']);ear_stage('ears',conducting+sensory+['hearing-pathways'])
foods=['starchy-food','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat-food','bile','fat-droplets','fat-products']
food_factors=[1.2,.8,.52,.8,.65,1.15,.65,1,.9,1,1]
for i,name in enumerate(foods):
    atlas=Image.open(SRC/'digestion-atlas.png').convert('RGBA');w,h=atlas.size;x=i%4;y=i//4
    im=cut_bg(atlas.crop((round(x*w/4),round(y*h/3),round((x+1)*w/4),round((y+1)*h/3))))
    fitted_export(im,name,food_factors[i])

for name in ['cell','arm','ear','digestion']:
    Image.new('RGB',(1560,2340),(250,247,238)).save(OUT/f'{name}-background.png')

# Register independent pieces to the one arm master. These masks only extract
# generated art. A low contrast ghost of each absent part is its receiving cue.
arm=Image.open(SRC/'arm-complete.png').convert('RGBA')
# Remove the old sheet title and blank margins before extracting its engraving.
arm.paste((0,0,0,0),(0,0,1024,88));arm.paste((0,0,0,0),(0,1190,1024,1536))
arm.paste((0,0,0,0),(0,0,12,1536));arm.paste((0,0,0,0),(1008,0,1024,1536))
px=arm.load()
for y in range(88,1190):
    for x in range(1024):
        r,g,b,a=px[x,y]
        if r>213 and g>190 and b>145 and r-g<42: px[x,y]=(r,g,b,0)
polygons={
 'biceps':[(386,238),(384,315),(399,387),(405,468),(397,555),(375,620),(355,650),(332,625),(302,573),(279,513),(265,452),(265,401),(283,345),(318,294),(352,255)],
 'triceps':[(500,258),(526,278),(551,311),(577,358),(598,413),(608,467),(601,524),(582,581),(556,630),(539,650),(523,610),(503,560),(490,500),(485,436),(490,363)],
}
masks={}
for name,points in polygons.items():
    m=Image.new('L',arm.size); ImageDraw.Draw(m).polygon(points,fill=255); masks[name]=m
for name,bounds in [('radius-mineral',(62,722,331,990)),('ulna-mineral',(690,402,978,691))]:
    m=Image.new('L',arm.size); ImageDraw.Draw(m).ellipse(bounds,fill=255); masks[name]=m
empty=arm.copy()
for name,m in masks.items():
    ghost=arm.copy();ghost.putalpha(arm.getchannel('A').point(lambda a:round(a*.16)))
    empty.paste(ghost,(0,0),m)
    piece=masked(arm,m)
    piece.resize((1560,2340),Image.Resampling.LANCZOS).save(OUT/f'arm-{name}.png')
# Two complementary receiving regions together show exactly one shared arm.
front_mask=Image.new('L',arm.size);ImageDraw.Draw(front_mask).rectangle((0,0,470,1535),fill=255)
masked(empty,front_mask).resize((1560,2340),Image.Resampling.LANCZOS).save(OUT/'arm-front-base.png')
masked(empty,ImageChops.invert(front_mask)).resize((1560,2340),Image.Resampling.LANCZOS).save(OUT/'arm-back-base.png')
empty.resize((1560,2340),Image.Resampling.LANCZOS).save(OUT/'arm-base.png')
# Preserve the separately nucleated precursor cells; a complete muscle is not
# an accurate icon for the supplied population of cells.
cells=Image.open(SRC/'cell-atlas.png').convert('RGBA').crop((778,540,1115,984))
fitted_export(cells,'muscle-cells',.65)
fitted_export(arm.crop((135,795,255,915)),'bone-mineral',SCALE)

mapping=dict(zip(['prelude-phospholipids','prelude-water','opening-dna','opening-nuclear-envelope','opening-nucleus','opening-cell','prelude-myoblasts','school-bone-mineral'],cellnames))
mapping.update(dict(zip(['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears'],ears)))
mapping.update(dict(zip(['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products'],foods)))
mapping.update({'arm-front-tendons':'arm-front-base','arm-back-tendons':'arm-back-base'})
backgrounds={'cell-boundary':'cell','full-strong-and-movable':'arm','full-hearing':'ear','full-nutrition-meal':'digestion'}

def identity(text):
    match=re.match(r'`([^`]+)`',text)
    return match.group(1) if match else re.sub(r' \((compound|exclusive with .*?)\)$','',text)

source=(ROOT.parents[1]/'anatomy.md').read_text()
lines=source.splitlines(); result=[]; section=''; chapter=''; owner=''; seen=set()
for line in lines:
    if line.startswith('# '): line='# ![Engraved cell atlas](assets/icon.png) Anatomy'
    if line.startswith('## '): chapter=re.search(r'`([^`]+)`',line).group(1); section=''
    if line.startswith('background:'):
        line=line.replace('placeholder.svg',f'assets/{backgrounds[chapter]}-background.png' if chapter in backgrounds else '../../placeholder.svg')
    if line.startswith('**'): section=line
    if section=='**Hotspots**' and chapter=='full-strong-and-movable' and line.startswith('- `'):
        key=identity(line[2:]); front=key=='arm-front-tendons'
        result.append(line+' (center 780px, 1170px)')
        cx,cy,w,h=(300,630,330,850) if front else (750,490,470,650)
        result.append(f'  - hitbox: (center {cx*SCALE:g}px, {cy*SCALE:g}px) (size {w*SCALE:g}px, {h*SCALE:g}px)')
        continue
    if section=='**Items**' and line.startswith('- ') and '->' not in line:
        owner=identity(line[2:]); result.append(line)
        if owner not in seen:
            seen.add(owner); path=f'assets/{mapping[owner]}.png' if owner in mapping else '../../placeholder.svg'
            result.append(f'  - icon: ![Anatomical illustration]({path})')
        continue
    if re.match(r'  - (unnamed )?slot:',line):
        accepted=identity(line.split('accepts ',1)[1]); path='../../placeholder.svg'
        if owner=='opening-cell': path='assets/cell-nucleus.png' if accepted=='opening-nucleus' else 'assets/cell-future-slot.png'
        if owner in ['arm-front-tendons','arm-back-tendons']:
            front=owner=='arm-front-tendons'
            name=('radius-mineral' if front else 'ulna-mineral') if accepted=='school-bone-mineral' else ('biceps' if front else 'triceps')
            path=f'assets/arm-{name}.png'
        line+=f', icon: ![Fitted anatomical part]({path})'
    result.append(line)
(ROOT/'anatomy.md').write_text('\n'.join(result)+'\n')
(SRC/'registration.json').write_text(json.dumps({'backgroundSize':[1560,2340],'backgroundColour':[250,247,238],'sourceSize':[1024,1536],'scale':SCALE,'muscleMasks':polygons,'boneWindows':{'radius':[62,722,331,990],'ulna':[690,402,978,691]},'armBasePartitionX':470,'artCentre':[780,1170],'cellCanvas':[640,640],'cellSourceCrop':[54,49,989,984],'nucleusSourceCrop':[1094,335,1487,727],'cellFamilyScale':factor,'earFactors':ear_factors,'digestionFactors':food_factors},indent=2)+'\n')

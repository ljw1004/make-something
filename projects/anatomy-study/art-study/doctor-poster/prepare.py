from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json,re

ROOT=Path(__file__).parent
SRC=ROOT/'sources'; ASSET=ROOT/'assets'
W,H=780,1688
names={}
# Source pixels are never painted: these operations extract, mask, resize and register
# the retained imagegen paintings. Runtime is one quarter of export dimensions.
def save(im, ident):
    im.save(ASSET/(ident+'.png')); names[ident]=ident+'.png'

def crop_cell(file, cols, rows, index):
    im=Image.open(SRC/file).convert('RGBA'); x,y=index%cols,index//cols
    return im.crop((round(x*im.width/cols)+3,round(y*im.height/rows)+3,round((x+1)*im.width/cols)-3,round((y+1)*im.height/rows)-3))

def tight(im):
    bbox=im.getchannel('A').point(lambda a:255 if a>70 else 0).getbbox()
    return im.crop(bbox) if bbox else im

def resize_width(im,width):
    return im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)

def masked(im,box,ellipse=True):
    mask=Image.new('L',im.size); d=ImageDraw.Draw(mask)
    (d.ellipse if ellipse else d.rectangle)(box,fill=255)
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return out

# One cell master establishes water volume, wall microstructure and viewing scale.
cell=resize_width(tight(crop_cell('cell-atlas-v2.png',3,3,5)),420)
canvas=Image.new('RGBA',(440,440));canvas.alpha_composite(cell,((440-cell.width)//2,(440-cell.height)//2));save(canvas,'opening-cell')
# Exact interior of that same illustration, without its surrounding membrane.
water=masked(canvas,(82,83,359,360));save(tight(water),'prelude-water')
# A curved cross-section of the same bilayer: identical repeating-unit scale.
wall=canvas.crop((48,14,392,107));save(wall,'prelude-phospholipids')
# The exact assembled nucleus is the source for both its DNA and envelope.
nucleus=resize_width(tight(crop_cell('cell-atlas-v2.png',3,3,4)),192)
core=masked(nucleus,(42,39,151,147));save(tight(core),'opening-dna')
mask=Image.new('L',nucleus.size,255);ImageDraw.Draw(mask).ellipse((42,39,151,147),fill=0)
envelope=nucleus.copy();envelope.putalpha(ImageChops.multiply(envelope.getchannel('A'),mask));save(envelope,'opening-nuclear-envelope')
save(nucleus,'opening-nucleus');nucleus.save(ASSET/'fitted-nucleus.png')
overlay=Image.new('RGBA',(440,440));overlay.alpha_composite(nucleus,((440-nucleus.width)//2,(440-nucleus.height)//2));overlay.save(ASSET/'cell-nucleus-overlay.png')
Image.new('RGBA',(440,440)).save(ASSET/'cell-blank-overlay.png')
# Micrographs are inspection views, not arm-sized individual cells or crystals.
for i,ident,width in [(6,'prelude-myoblasts',280),(7,'school-bone-mineral',230)]:
    save(resize_width(tight(crop_cell('cell-atlas-v2.png',3,3,i)),width),ident)

hearing=['outer-ears-and-canals','eardrums','outer-ears-with-eardrums','middle-ear-bones','sound-conducting-ears','coiled-inner-ear-chambers-and-fluid','hearing-cells-with-tiny-hairs','vibration-sensitive-inner-ears','sound-receiving-ears','hearing-pathways','inner-ears-with-hearing-pathways','ears']
# Keep the visible auricle near 200 export px high throughout its assemblies.
# Eardrum and ossicles use their installed size; hair cells are a named located enlargement.
widths=[230,73,230,106,230,165,230,250,390,166,285,440]
for i,(ident,width) in enumerate(zip(hearing,widths)):
    save(resize_width(tight(crop_cell('hearing-atlas.png',4,3,i)),width),ident)

# One registered ear composition carries exactly the same source parts through
# every alternate assembly. The located hair-cell enlargement stays below the
# cochlea instead of shrinking into it when the nerve is added.
ear_parts={name:Image.open(ASSET/(name+'.png')).convert('RGBA') for name in [hearing[i] for i in [0,1,3,5,6,9]]}
ear_xy={'outer-ears-and-canals':(0,0),'eardrums':(190,106),'middle-ear-bones':(240,110),'coiled-inner-ear-chambers-and-fluid':(330,88),'hearing-cells-with-tiny-hairs':(335,285),'hearing-pathways':(450,115)}
def ear_stage(name,parts):
    im=Image.new('RGBA',(640,540))
    if 'hearing-cells-with-tiny-hairs' in parts:
        ImageDraw.Draw(im).line([(412,220),(450,285)],fill=(83,122,139,255),width=3)
    for part in parts:im.alpha_composite(ear_parts[part],ear_xy[part])
    save(tight(im),name)
conducting=['outer-ears-and-canals','eardrums','middle-ear-bones']
sensory=['coiled-inner-ear-chambers-and-fluid','hearing-cells-with-tiny-hairs']
ear_stage('outer-ears-with-eardrums',conducting[:2])
ear_stage('sound-conducting-ears',conducting)
ear_stage('vibration-sensitive-inner-ears',sensory)
ear_stage('sound-receiving-ears',conducting+sensory)
ear_stage('inner-ears-with-hearing-pathways',sensory+['hearing-pathways'])
ear_stage('ears',conducting+sensory+['hearing-pathways'])

digestion=['starchy-food','saliva','shorter-starch-chains','digestive-enzymes','meal-glucose','protein-food','meal-amino-acids','fat-food','bile','small-fat-droplets','fat-digestion-products']
# Retain each atlas cell at a common magnification, so glucose units and the
# successive fat molecular illustrations do not grow between stages.
for i,ident in enumerate(digestion):
    icon=crop_cell('digestion-atlas.png',4,3,i)
    icon=icon.resize((280,round(icon.height*280/icon.width)),Image.Resampling.LANCZOS)
    save(icon,ident)

# Every backdrop is a blank white sheet; no anatomy, labels, or example diagrams.
for name in ['cell','arm','hearing','digestion']:
    Image.new('RGB',(W,H),'white').save(ASSET/(name+'-background.jpg'),quality=94)
Image.new('RGBA',(280,280)).save(ASSET/'blank-overlay.png')
Image.new('RGB',(280,280),'#f5f2e9').save(ASSET/'draft-item.png')
Image.new('RGB',(W,H),'#f5f2e9').save(ASSET/'draft-background.jpg')

# The two fixed receivers jointly own ONE painted skeleton, including their own
# located bone micrographs. A disjoint partition prevents duplicate skeletons.
base=Image.open(SRC/'arm-background.png').convert('RGBA')
finished=Image.open(SRC/'arm-finished.png').convert('RGBA')
scene_box=(0,75,1024,820)
scene_size=(1400,1019)
back_mask=Image.new('L',base.size);d=ImageDraw.Draw(back_mask)
d.polygon([(0,75),(232,75),(232,485),(287,612),(0,612)],fill=255)
d.rounded_rectangle((595,382,1004,606),radius=38,fill=255)
front_mask=ImageChops.invert(back_mask)
def registered(im,mask):
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
    return out.crop(scene_box).resize(scene_size,Image.Resampling.LANCZOS)
for ident,mask in [('arm-front-tendons',front_mask),('arm-back-tendons',back_mask)]:save(registered(base,mask),ident)
polygons={
 'front-muscle':[(239,155),(259,170),(259,211),(282,258),(317,318),(338,383),(336,432),(323,493),(340,541),(385,574),(349,584),(309,551),(287,513),(260,467),(246,416),(236,350),(228,276),(231,215)],
 'back-muscle':[(143,208),(175,213),(197,253),(212,303),(220,373),(228,449),(235,509),(253,558),(284,591),(259,609),(225,589),(209,548),(200,503),(173,458),(145,406),(126,354),(114,307),(121,256)],
}
for name,poly in polygons.items():
    mask=Image.new('L',finished.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
    registered(finished,mask).save(ASSET/(name+'.png'))
for name,box in [('front-mineral',(599,143,999,370)),('back-mineral',(599,386,999,602))]:
    mask=Image.new('L',finished.size);ImageDraw.Draw(mask).rounded_rectangle(box,radius=38,fill=255)
    # Populate the located matrix with the actual supplied mineral specimen;
    # the previous finished painting barely distinguished mineral addition.
    mineralized=finished.copy()
    crystals=resize_width(Image.open(ASSET/'school-bone-mineral.png').convert('RGBA'),168)
    mineralized.alpha_composite(crystals,(box[0]+25,box[1]+40))
    mineralized.alpha_composite(crystals,(box[0]+205,box[1]+45))
    registered(mineralized,mask).save(ASSET/(name+'.png'))

def key(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
items=json.loads((SRC/'item-metadata.json').read_text());byid={i['id']:i for i in items}
source=(ROOT.parent.parent/'anatomy.md').read_text()
lines=source.replace('(placeholder.svg)','(../../placeholder.svg)').splitlines()
out=[];section='';seen=set();chapter=0;owner=None
backgrounds={1:'cell',4:'arm',8:'hearing',18:'digestion'}
positions={'prelude-phospholipids':(180,560),'prelude-water':(570,560),'opening-dna':(180,950),'opening-nuclear-envelope':(570,950)}
for line in lines:
    if line.startswith('## '):chapter+=1
    if line.startswith('background:') and chapter in backgrounds:line=re.sub(r'\]\([^)]*\)','](assets/'+backgrounds[chapter]+'-background.jpg)',line)
    elif line.startswith('background:'):line=line.replace('../../placeholder.svg','assets/draft-background.jpg')
    if line.startswith('**'):section=line
    if section=='**Hotspots**' and chapter==4 and line in ['- `arm-front-tendons`','- `arm-back-tendons`']:
        front='front' in line
        out.append(line+' (center 390px, 520px)')
        out.append('  - icon: ![Registered arm region](assets/arm-'+('front' if front else 'back')+'-tendons.png)')
        x,y=(225,440) if front else (135,440)
        out.append(f'  - hitbox: (center {x}px, {y}px) (size 80px, 280px)')
        continue
    if section=='**Items**' and line.startswith('- '):
        token=line[2:];ident=None
        m=re.match(r'`([^`]+)`',token)
        if m:ident='id:'+m.group(1)
        else:
            plain=re.sub(r' \(compound\)$','',token)
            for it in items:
                if it['name']==plain:ident=it['id'];break
        owner=ident
        out.append(line)
        if ident and ident not in seen:
            seen.add(ident);item=byid[ident];slug=ident[3:] if ident.startswith('id:') else key(item['name'])
            asset=names.get(slug)
            if slug in ['arm-front-tendons','arm-back-tendons']:asset=slug+'.png'
            path='assets/'+asset if asset else 'assets/draft-item.png'
            center=''
            if slug in positions:center=' (center %spx, %spx)'%positions[slug]
            out.append(f'  - icon: ![{item["name"]}]({path}){center}')
        continue
    if re.match(r'  - (unnamed slot:|slot:)',line):
        overlay='blank-overlay.png'
        if owner=='id:opening-cell':overlay='cell-nucleus-overlay.png' if 'accepts `opening-nucleus`' in line else 'cell-blank-overlay.png'
        if owner in ['id:arm-front-tendons','id:arm-back-tendons']:
            overlay=('front' if 'front' in owner else 'back')+('-mineral.png' if 'school-bone-mineral' in line else '-muscle.png')
        line+=f', icon: ![Fitted appearance](assets/{overlay})'
    out.append(line)
(ROOT/'anatomy.md').write_text('\n'.join(out)+'\n')
(ROOT/'asset-catalogue.json').write_text(json.dumps(names,indent=2)+'\n')
print('Prepared',len(names),'selected item pictures and four scenes')

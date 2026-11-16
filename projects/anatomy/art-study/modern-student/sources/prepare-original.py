"""Mechanical extraction and manuscript artwork metadata; no synthesized artwork."""
from PIL import Image, ImageOps, ImageDraw, ImageChops
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'sources'
OUT = ROOT / 'assets'
atlas = Image.open(SRC/'atlas.png').convert('RGBA')
names = ['lipids','water','dna','envelope','nucleus','cell','outer-ear','eardrum','outer-drum','ossicles','conducting-ear','cochlea','hair-cells','sensing-cochlea','receiving-ear','hearing-nerve','cochlea-nerve','ears','starch','saliva','short-starch','enzymes','glucose','protein','amino-acids','fat','bile','fat-droplets','fat-products','mineral','muscle-cells','biceps','triceps','bone-matrix','mitochondria','ribosome']
crops = {}
# Remove neighboring atlas slivers in final-canvas coordinates without changing
# the selected object's scale or placement. Apply the same cut to fitted sources.
right_edge_masks = {'nucleus':310, 'ossicles':315, 'conducting-ear':312,
                    'cochlea-nerve':308, 'mitochondria':303}
bounds=[(8,38,212,225),(219,42,415,232),(470,28,597,241),(626,32,831,241),(835,30,1048,246),(1049,27,1254,246),
 (0,248,216,451),(244,253,408,454),(422,250,624,447),(625,280,828,430),(834,255,1049,444),(1052,250,1254,455),
 (0,468,215,640),(218,470,421,640),(421,469,625,635),(625,470,829,630),(833,470,1048,640),(1048,470,1254,640),
 (0,655,216,831),(220,652,418,835),(432,665,611,829),(632,650,825,835),(839,660,1039,834),(1043,653,1254,835),
 (3,853,211,1020),(219,850,417,1022),(423,841,620,1022),(628,847,831,1024),(840,858,1045,1015),(1048,851,1254,1023),
 (8,1036,215,1234),(240,1027,374,1243),(462,1028,603,1242),(628,1028,832,1250),(837,1041,1047,1238),(1048,1039,1254,1239)]
for i, name in enumerate(names):
    x,y = i%6,i//6
    crop=atlas.crop(bounds[i])
    box=crop.getbbox()
    if box: crop=crop.crop(box)
    crops[name]=crop
    size=416 if name=='cell' else 336
    im=Image.new('RGBA',(size,size))
    fit=ImageOps.contain(crop,(size-20,size-20),Image.Resampling.LANCZOS)
    im.alpha_composite(fit,((size-fit.width)//2,(size-fit.height)//2))
    if name in right_edge_masks:
        cutoff=right_edge_masks[name]
        im.paste((0,0,0,0),(cutoff,0,size,size))
        source_cutoff=round((cutoff-(size-fit.width)//2)*crop.width/fit.width)
        crop.paste((0,0,0,0),(source_cutoff,0,crop.width,crop.height))
    im.save(OUT/f'{name}.png')

for name in ['cell','arm','hearing','digestion']:
    im=Image.open(SRC/f'{name}-background.png').convert('RGB')
    fit=ImageOps.contain(im,(780,1440),Image.Resampling.LANCZOS)
    bg=fit.crop((0,fit.height-1,fit.width,fit.height)).resize((780,1688))
    bg.paste(fit,((780-fit.width)//2,0))
    bg.save(OUT/f'{name}-background.webp',quality=93)

Image.new('RGBA',(256,256)).save(OUT/'unillustrated.png')
Image.new('RGB',(780,1688),(245,242,233)).save(OUT/'unillustrated-background.png')
Image.new('RGBA',(416,416)).save(OUT/'cell-empty-overlay.png')
for name,xy,sz in [('nucleus',(136,134),(144,144)),('mitochondria',(229,210),(92,92)),('ribosome',(72,220),(78,78))]:
    im=Image.new('RGBA',(416,416))
    im.alpha_composite(ImageOps.contain(crops[name],sz,Image.Resampling.LANCZOS),xy)
    im.save(OUT/f'cell-{name}-overlay.png')

# Full scene canvases align fitted art to background coordinates. Each image is
# twice the background dimensions because icons display at quarter-size.
Image.new('RGBA',(1560,3376)).save(OUT/'arm-base.png')
registration = {
    'front-muscle':('biceps',(267,83,103,422)),
    'back-muscle':('triceps',(177,139,110,360)),
    'front-mineral':('bone-matrix',(526,379,239,246)),
    'back-mineral':('bone-matrix',(18,475,244,248)),
}
for key,(name,(x,y,w,h)) in registration.items():
    im=Image.new('RGBA',(1560,3376))
    source=crops[name]
    if key=='front-muscle':
        source=ImageOps.mirror(source)
    if name=='bone-matrix':
        # Measure the actual teal specimen rim rather than transparent dust.
        # Fit that rim to the existing located enlargement, avoiding nested rings.
        source=Image.open(OUT/'bone-matrix.png').convert('RGBA').crop((20,27,299,305))
    fit=source.resize((w*2,h*2),Image.Resampling.LANCZOS)
    if name=='bone-matrix':
        mask=Image.new('L',fit.size)
        ImageDraw.Draw(mask).ellipse((0,0,fit.width-1,fit.height-1),fill=255)
        fit.putalpha(ImageChops.multiply(fit.getchannel('A'),mask))
    im.alpha_composite(fit,(x*2,y*2))
    im.save(OUT/f'arm-{key}.png')

catalogue=json.loads((SRC/'catalogue.json').read_text())
mapping={
    'id:prelude-phospholipids':'lipids','id:prelude-water':'water','id:opening-dna':'dna','id:opening-nuclear-envelope':'envelope','id:opening-nucleus':'nucleus','id:opening-cell':'cell',
    'id:prelude-myoblasts':'muscle-cells','id:school-bone-mineral':'mineral','id:arm-front-tendons':'arm-base','id:arm-back-tendons':'arm-base',
    'name:Outer ears and canals':'outer-ear','name:Eardrums':'eardrum','name:Outer ears with eardrums':'outer-drum','name:Middle-ear bones':'ossicles','name:Sound-conducting ears':'conducting-ear','name:Coiled inner-ear chambers and fluid':'cochlea','name:Hearing cells with tiny hairs':'hair-cells','name:Vibration-sensitive inner ears':'sensing-cochlea','name:Sound-receiving ears':'receiving-ear','name:Hearing pathways':'hearing-nerve','name:Inner ears with hearing pathways':'cochlea-nerve','name:Ears':'ears',
    'name:Starchy food':'starch','name:Saliva':'saliva','name:Shorter starch chains':'short-starch','name:Digestive enzymes':'enzymes','name:Meal glucose':'glucose','name:Protein food':'protein','name:Meal amino acids':'amino-acids','name:Fat food':'fat','name:Bile':'bile','name:Small fat droplets':'fat-droplets','name:Fat digestion products':'fat-products',
}
positions={
    'id:prelude-phospholipids':(190,1050),'id:prelude-water':(570,1050),'id:opening-dna':(190,1350),'id:opening-nuclear-envelope':(570,1350),
    'id:prelude-myoblasts':(220,1220),'id:school-bone-mineral':(560,1220),
    'name:Outer ears and canals':(140,1110),'name:Eardrums':(390,1110),'name:Middle-ear bones':(640,1110),'name:Coiled inner-ear chambers and fluid':(140,1380),'name:Hearing cells with tiny hairs':(390,1380),'name:Hearing pathways':(640,1380),
    'name:Starchy food':(140,1110),'name:Saliva':(390,1110),'name:Digestive enzymes':(640,1110),'name:Protein food':(140,1380),'name:Fat food':(390,1380),'name:Bile':(640,1380),
}
# Shared primitive origins must satisfy earlier placeholder scene bounds; leave
# muscle cells on automatic arrival rather than assigning chapter-four coordinates.
positions.pop('id:prelude-myoblasts')
lines=(ROOT.parent.parent/'anatomy.md').read_text().splitlines()
insert={}; replace={}
declaration_lines={}
section=''
for n,line in enumerate(lines,1):
    if line.startswith('**'): section=line
    if line.startswith('## '): section=''
    if section=='**Items**' and line.startswith('- '):
        content=line[2:]
        match=re.match(r'`([^`]+)`',content)
        key='id:'+match[1] if match else 'name:'+re.sub(r' \(compound\)$','',content)
        declaration_lines.setdefault(key,n)
for item in catalogue['items']:
    key=item['id']; asset=mapping.get(key,'unillustrated')
    pos=positions.get(key)
    suffix=f' (center {pos[0]}px, {pos[1]}px)' if pos else ''
    insert.setdefault(declaration_lines[key],[]).append(f'  - icon: ![{item["name"]}](assets/{asset}.png){suffix}')
    for slot in item['slots']:
        overlay='unillustrated'
        if key=='id:opening-cell':
            overlay={'id:opening-nucleus':'cell-nucleus-overlay','id:opening-mitochondria':'cell-mitochondria-overlay','id:school-ribosome':'cell-ribosome-overlay'}.get(slot['accepts'],'cell-empty-overlay')
        elif key in ['id:arm-front-tendons','id:arm-back-tendons']:
            side='front' if 'front' in key else 'back'
            overlay=f'arm-{side}-'+('mineral' if slot['accepts']=='id:school-bone-mineral' else 'muscle')
        replace[slot['line']]=lines[slot['line']-1]+f', icon: ![Fitted appearance](assets/{overlay}.png)'

backgrounds={0:'cell',3:'arm',7:'hearing',17:'digestion'}
for ch,name in backgrounds.items():
    line=catalogue['chapters'][ch]['line']+1
    replace[line]=re.sub(r'\(placeholder.svg\)',f'(assets/{name}-background.webp)',lines[line-1])
section=''
for i,line in enumerate(lines,1):
    if line.startswith('**'): section=line
    if line=='- `arm-front-tendons`' and section=='**Hotspots**' and i<160:
        replace[i]=line+' (center 390px, 844px)\n  - hitbox: (center 530px, 375px) (size 500px, 750px)'
    if line=='- `arm-back-tendons`' and section=='**Hotspots**' and i<160:
        replace[i]=line+' (center 390px, 844px)\n  - hitbox: (center 140px, 400px) (size 280px, 800px)'
out=[]
for i,line in enumerate(lines,1):
    revised=replace.get(i,line).replace('(placeholder.svg)','(assets/unillustrated-background.png)' if line.startswith('background:') else '(assets/cell.png)')
    out.append(revised)
    out.extend(insert.get(i,[]))
(ROOT/'anatomy.md').write_text('\n'.join(out)+'\n')
(SRC/'registration.json').write_text(json.dumps({'background':[780,1688],'fixedIconCanvas':[1560,3376],'arm':registration,'armTransforms':{'front-muscle':'horizontal mirror','mineral':'crop exported bone-matrix.png to [20,27,299,305], then ellipse mask'},'atlasGrid':[6,6],'atlasBounds':bounds,'atlasNames':names,'itemAssets':mapping},indent=2))

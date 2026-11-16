"""Export selected generated masters. Mechanical crops, scale, masks and registration only."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageChops
import json, subprocess

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'; OUT=ROOT/'assets'
old=json.loads((SRC/'registration.json').read_text())
atlas=Image.open(SRC/'atlas.png').convert('RGBA')
new=Image.open(SRC/'refresh-atlas.png').convert('RGBA')
mapping=old['itemAssets'].copy()
def export(im,name,width=None,canvas=None):
    box=im.getbbox()
    if box: im=im.crop(box)
    if width: im=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)
    if canvas:
        page=Image.new('RGBA',canvas); page.alpha_composite(im,((canvas[0]-im.width)//2,(canvas[1]-im.height)//2)); im=page
    im.save(OUT/f'{name}.png'); return im

# Original selected ear/digestion artwork remains the source. These scales retain
# the size of the pinna through the accumulating outer/middle/inner-ear family.
crops={name:atlas.crop(bounds) for name,bounds in zip(old['atlasNames'],old['atlasBounds'])}
widths={'outer-ear':340,'eardrum':135,'outer-drum':340,'ossicles':160,
 'conducting-ear':360,'cochlea':190,'hair-cells':260,'sensing-cochlea':260,
 'receiving-ear':430,'hearing-nerve':190,'cochlea-nerve':270,'ears':470}
for name in old['atlasNames']:
    if name in ['lipids','water','dna','envelope','nucleus','cell']: continue
    im=crops[name]
    # Known right-hand neighboring fragments in the original tightly packed atlas.
    if name in ['ossicles','conducting-ear','cochlea-nerve']:
        im=im.crop((0,0,im.width-9,im.height))
    export(im,name,widths.get(name,280))

# Keep installed sensory tissue visible throughout the complete hearing family.
# Use actual source components at one magnification, with a persistent locator.
earp={name:Image.open(OUT/f'{name}.png').convert('RGBA') for name in ['outer-ear','eardrum','ossicles','cochlea','hair-cells','hearing-nerve']}
earp['eardrum']=export(earp['eardrum'],'eardrum',100)
earxy={'outer-ear':(0,0),'eardrum':(290,135),'ossicles':(360,160),'cochlea':(495,130),'hair-cells':(520,370),'hearing-nerve':(640,175)}
def ear_stage(name,parts):
    im=Image.new('RGBA',(850,700))
    if 'hair-cells' in parts:ImageDraw.Draw(im).line([(595,290),(640,370)],fill=(60,134,146,255),width=3)
    for part in parts:im.alpha_composite(earp[part],earxy[part])
    export(im,name)
conducting=['outer-ear','eardrum','ossicles'];sensory=['cochlea','hair-cells']
ear_stage('outer-drum',conducting[:2]);ear_stage('conducting-ear',conducting)
ear_stage('sensing-cochlea',sensory);ear_stage('receiving-ear',conducting+sensory)
ear_stage('cochlea-nerve',sensory+['hearing-nerve']);ear_stage('ears',conducting+sensory+['hearing-nerve'])

# Cell construction: all subjects come from one matched generated master.
# Water matches the membrane's interior diameter; lipid repeated heads match
# those in the completed membrane. Nuclear parts share their own smaller scale.
bounds={'lipids':(8,98,403,318),'water':(470,65,786,386),
 'cell':(850,50,1215,409),'dna':(126,531,310,714),
 'envelope':(499,497,756,752),'nucleus':(902,493,1154,748),
 'mineral':(438,874,788,1183),'fat-products':(855,887,1215,1157)}
spec={'lipids':(435,None),'water':(360,None),'cell':(500,(560,560)),
 'dna':(132,None),'envelope':(185,None),'nucleus':(185,None),
 'mineral':(280,None),'fat-products':(280,None)}
for name,box in bounds.items(): export(new.crop(box),name,*spec[name])
cell=Image.open(OUT/'cell.png').convert('RGBA')
nucleus=Image.open(OUT/'nucleus.png').convert('RGBA')
overlay=Image.new('RGBA',cell.size); overlay.alpha_composite(nucleus,(187,187))
overlay.save(OUT/'cell-nucleus-overlay.png')
Image.new('RGBA',cell.size).save(OUT/'cell-empty-overlay.png')

# Blank work surfaces: literal plain paper, no diagrams or anatomical marks.
Image.new('RGB',(780,1688),(250,252,251)).save(OUT/'blank-sheet.png')

# Preserve the former scene's exact anatomical scale, but make its entire
# anatomy belong to the interactive receivers. The two complementary masks
# sum to one continuous arm, with no duplicated bone or baked-in background.
arm=Image.open(SRC/'arm-transparent.png').convert('RGBA')
arm=ImageOps.contain(arm,(1560,2880),Image.Resampling.LANCZOS)
base=Image.new('RGBA',(1560,3376)); base.alpha_composite(arm,((1560-arm.width)//2,0))
mask=Image.new('L',base.size)
ImageDraw.Draw(mask).polygon([(0,0),(540,0),(540,880),(750,1360),(530,1520),(0,1520)],fill=255)
back=base.copy(); back.putalpha(ImageChops.multiply(base.getchannel('A'),mask))
front=base.copy(); front.putalpha(ImageChops.multiply(base.getchannel('A'),ImageOps.invert(mask)))
front.save(OUT/'arm-front-base.png'); back.save(OUT/'arm-back-base.png')
mapping['id:arm-front-tendons']='arm-front-base'; mapping['id:arm-back-tendons']='arm-back-base'
for key,(name,(x,y,w,h)) in old['arm'].items():
    im=Image.new('RGBA',(1560,3376)); part=crops[name]
    if key=='front-muscle': part=ImageOps.mirror(part)
    if name=='bone-matrix':
        part=atlas.crop((628,1028,832,1250)).crop((9,15,193,211))
    part=part.resize((w*2,h*2),Image.Resampling.LANCZOS)
    if name=='bone-matrix':
        m=Image.new('L',part.size);ImageDraw.Draw(m).ellipse((0,0,part.width-1,part.height-1),fill=255)
        part.putalpha(ImageChops.multiply(part.getchannel('A'),m))
    im.alpha_composite(part,(x*2,y*2));im.save(OUT/f'arm-{key}.png')

slot={
 'id:opening-cell':{'id:opening-nucleus':'assets/cell-nucleus-overlay.png',
  **{k:'assets/cell-empty-overlay.png' for k in ['id:opening-mitochondria','id:school-sugar-carrier','id:school-ribosome']}},
 **{f'id:arm-{side}-tendons':{'id:school-bone-mineral':f'assets/arm-{side}-mineral.png','id:prelude-myoblasts':f'assets/arm-{side}-muscle.png'} for side in ['front','back']}}
positions={'id:prelude-phospholipids':[185,540],'id:prelude-water':[585,540],
 'id:opening-dna':[220,1040],'id:opening-nuclear-envelope':[560,1040]}
for chapter,ys in [('8',[500,1000]),('18',[500,1000])]:
    ids=([ 'Outer ears and canals','Eardrums','Middle-ear bones','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Hearing pathways'] if chapter=='8' else ['Starchy food','Saliva','Digestive enzymes','Protein food','Fat food','Bile'])
    for i,name in enumerate(ids): positions['name:'+name]=[140+250*(i%3),ys[i//3]]
positions['id:school-bone-mineral']=[550,1280]
art={'headingIcon':'assets/cell.png','defaultIcon':'../../placeholder.svg','defaultOverlay':'../../placeholder.svg',
 'defaultBackground':'assets/blank-sheet.png','chapterBackgrounds':{str(n):'assets/blank-sheet.png' for n in [1,4,8,18]},
 'itemIcons':{k:f'assets/{v}.png' for k,v in mapping.items()},'slotIcons':slot,'itemPositions':positions,
 'hotspots':{'4':{
  'id:arm-front-tendons':{'center':[390,844],'hitbox':{'center':[530,375],'size':[500,750]}},
  'id:arm-back-tendons':{'center':[390,844],'hitbox':{'center':[140,400],'size':[280,800]}}}}}
(ROOT/'art-map.json').write_text(json.dumps(art,indent=2)+'\n')
# Keep only selected runtime exports; original artwork remains in sources.
used=set(art['itemIcons'].values())|{'assets/blank-sheet.png'}
used|={v for slots in slot.values() for v in slots.values()}
for path in OUT.iterdir():
    if path.is_file() and f'assets/{path.name}' not in used: path.unlink()
(SRC/'registration-refresh.json').write_text(json.dumps({'background':[780,1688],'cellCanvas':[560,560],'nucleusOrigin':[187,187],
 'cellCrops':bounds,'cellWidths':spec,'earWidths':widths,'armCanvas':[1560,3376],
 'armMaskPolygon':[(0,0),(540,0),(540,880),(750,1360),(530,1520),(0,1520)],'armFittings':old['arm']},indent=2)+'\n')
subprocess.run(['node',str(ROOT.parent/'integrate-art.ts'),str(ROOT/'art-map.json')],check=True)

"""Mechanical exports only: crop generated raster, clean faint alpha, frame and register.
Run: uv run --with pillow python projects/anatomy-study/art-study/farout-graphic-design/produce.py
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageOps

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)
def save(im,name): im.save(OUT/(name+'.png')); return 'assets/'+name+'.png'
def isolated(sheet,box,size=(320,300)):
    im=Image.open(ROOT/'masters'/sheet).convert('RGBA').crop(box)
    cutoff=100 if sheet=='digestion.png' else 24
    im.putalpha(im.getchannel('A').point(lambda a:0 if a<cutoff else a))
    bb=im.getbbox()
    if bb: im=im.crop(bb)
    im.thumbnail((size[0]-24,size[1]-24),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',size); canvas.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2))
    return canvas

cell_ids=['id:prelude-phospholipids','id:prelude-water','id:opening-dna','id:opening-nuclear-envelope','id:opening-nucleus','id:opening-cell','id:prelude-myoblasts','id:school-bone-mineral','id:opening-mitochondria','id:school-sugar-carrier','id:school-ribosome','cover']
hearing_names=['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears']
digestion_names=['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products','tract-emblem']
icons={}; registration={}
for sheet,ids,ys in [('cells.png',cell_ids,[0,340,660,965,1312]),('hearing.png',['name:'+s for s in hearing_names],[0,353,662,967,1312]),('digestion.png',['name:'+s for s in digestion_names],[0,344,672,959,1312])]:
    src=Image.open(ROOT/'masters'/sheet)
    # Digestion generation can use a different canvas; boxes scale from atlas coordinates.
    sx,sy=src.width/1199,src.height/1312
    for i,key in enumerate(ids):
        r,c=divmod(i,3)
        right=788 if sheet=='hearing.png' and c==1 else min(1199,(c+1)*400)
        box=tuple(round(v*f) for v,f in zip([c*400,ys[r],right,ys[r+1]],[sx,sy,sx,sy]))
        size=(560,500) if key=='id:opening-cell' else (320,300)
        im=isolated(sheet,box,size)
        name=key.replace('id:','').replace('name:','').lower().replace(' ','-')
        icons[key]=save(im,name); registration[key]={'master':sheet,'crop':box,'canvas':size}

# Fit the nucleus inside the same membrane canvas; all later cell slots share it.
cell=Image.open(OUT/'opening-cell.png').convert('RGBA')
slots={'id:opening-cell':{}}
for key,wh,at in [('id:opening-nucleus',(185,174),(145,148)),('id:opening-mitochondria',(130,110),(317,257)),('id:school-sugar-carrier',(110,105),(412,142)),('id:school-ribosome',(95,85),(315,110))]:
    part=Image.open(ROOT/icons[key]).convert('RGBA');part=part.crop(part.getbbox());part.thumbnail(wh,Image.Resampling.LANCZOS)
    layer=Image.new('RGBA',cell.size);layer.alpha_composite(part,at)
    slots['id:opening-cell'][key]=save(layer,'fitted-'+key[3:])

# The background and every arm fitting share exact generated source pixels.
arm=Image.open(ROOT/'masters/arm.png').convert('RGBA')
polygons={
 'front-muscle':[(422,288),(442,281),(439,365),(430,442),(425,535),(408,620),(380,690),(359,718),(341,682),(320,634),(305,577),(304,525),(317,464),(340,404),(378,351),(400,320)],
 'back-muscle':[(505,343),(532,386),(551,432),(565,490),(569,551),(561,612),(545,670),(525,713),(507,730),(490,692),(477,640),(471,590),(473,528),(483,453),(495,394)],
 'front-mineral':[(443,883),(464,875),(507,932),(489,945)],
 'back-mineral':[(534,925),(553,917),(586,970),(566,983)]
}
masks={}; base=arm.copy()
for name,points in polygons.items():
    mask=Image.new('L',arm.size);ImageDraw.Draw(mask).polygon(points,fill=255);masks[name]=mask
    # Preserve a faint structural ghost as a neutral construction placeholder.
    pale=Image.blend(Image.new('RGBA',arm.size,(248,231,202,255)),ImageOps.grayscale(arm).convert('RGBA'),.12)
    base.paste(pale,(0,0),mask)

W,H=1560,3376
def page_from(im,height):
    # Neutral framing is sampled from the generated paper, not new illustration.
    page=Image.new('RGBA',(W,H),(248,232,205,255))
    paper=Image.open(ROOT/'masters/arm.png').crop((20,1350,1004,1510)).resize((W,254))
    for y in range(0,H,254): page.paste(paper,(0,y))
    page.alpha_composite(im.resize((W,height),Image.Resampling.LANCZOS),(0,0));return page
backgrounds={'4':save(page_from(base,2340),'chapter-4')}
for side in ['front','back']:
    owner='id:arm-'+side+'-tendons'
    icons[owner]=save(Image.new('RGBA',(W,H)),'arm-'+side+'-base')
    slots[owner]={}
    for part,key in [('mineral','id:school-bone-mineral'),('muscle','id:prelude-myoblasts')]:
        layer=arm.copy();layer.putalpha(masks[side+'-'+part]);full=Image.new('RGBA',(W,H));full.alpha_composite(layer.resize((W,2340),Image.Resampling.LANCZOS),(0,0))
        slots[owner][key]=save(full,'arm-'+side+'-'+part)
        registration[side+'-'+part]={'master':'arm.png','maskPolygon':polygons[side+'-'+part],'sourceSize':arm.size,'exportCanvas':[W,H],'sourceToExportScale':1560/1024,'artworkCenter':[780,1688]}
atlas=Image.open(ROOT/'masters/backgrounds.png').convert('RGBA')
for ch,box in [('1',(0,0,489,820)),('8',(505,0,1014,820)),('18',(1030,0,1536,820))]:
    panel=atlas.crop(box)
    # Keep true aspect ratio and place the explanatory plate above the work area.
    # Scale up the generated plate too: thumbnail() silently kept the small
    # source crop at native size. Reserve a visible working area on short phones.
    panel=ImageOps.contain(panel,(1456,1500),Image.Resampling.LANCZOS)
    page=page_from(Image.new('RGBA',(W,1)),1)
    page.alpha_composite(panel,((W-panel.width)//2,30))
    backgrounds[ch]=save(page,'chapter-'+ch)

neutral=Image.new('RGBA',(W,H),(242,240,235,255)); save(neutral,'unillustrated-background')
placeholder=Image.new('RGBA',(320,300),(224,223,218,255));save(placeholder,'unillustrated-item')
save(Image.new('RGBA',(320,300)),'unillustrated-overlay')
cover=Image.open(ROOT/icons['cover']).convert('RGBA');square=Image.new('RGBA',(320,320));square.alpha_composite(cover,(0,10));save(square,'cover')
import sys
sys.dont_write_bytecode = True
from refresh import refresh
refresh(ROOT,OUT,icons,slots,backgrounds,registration,save)
positions={}
for ids,y in [(cell_ids[:4],700),(['name:'+x for x in ['Outer ears and canals','Eardrums','Middle-ear bones','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Hearing pathways']],700),(['name:'+x for x in ['Starchy food','Saliva','Digestive enzymes','Protein food','Fat food','Bile']],700)]:
    for i,key in enumerate(ids): positions[key]=[280+(i%3)*500,y+(i//3)*390]
artmap={'headingIcon':'assets/cover.png','defaultIcon':'assets/unillustrated-item.png','defaultOverlay':'assets/unillustrated-overlay.png','defaultBackground':'assets/unillustrated-background.png','chapterBackgrounds':backgrounds,'itemIcons':{k:v for k,v in icons.items() if k.startswith(('id:','name:'))},'slotIcons':slots,'itemPositions':positions,'hotspots':{'4':{'id:arm-front-tendons':{'center':[780,1688],'hitbox':{'center':[590,1050],'size':[330,1200]}},'id:arm-back-tendons':{'center':[780,1688],'hitbox':{'center':[825,1080],'size':[210,1160]}}}}}
(ROOT/'art-map.json').write_text(json.dumps(artmap,indent=2)+'\n')
(ROOT/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')

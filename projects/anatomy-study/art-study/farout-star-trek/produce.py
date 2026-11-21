"""Mechanical crop, alpha extraction, registration and manuscript-map production.
Run: uv run --with pillow --with numpy python projects/anatomy-study/art-study/farout-star-trek/produce.py
No anatomy is drawn here: all anatomical pixels derive from retained imagegen masters.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import json
ROOT=Path(__file__).resolve().parent
A=ROOT/'assets'; S=ROOT/'sources'
BG=(3,21,37,255)
records={}
def save(im,name):
    im.save(A/(name+'.png'))
    return 'assets/'+name+'.png'
def load(name): return Image.open(S/(name+'-atlas.png')).convert('RGBA')
def cut(im,box,navy=False):
    out=im.crop(box)
    if navy:
        ar=np.array(out); lum=ar[:,:,:3].max(axis=2).astype(float)
        # Remove only the dark backing; preserve luminous translucent outlines.
        ar[:,:,3]=(np.clip((lum-48)/30,0,1)*255).astype('uint8')
        out=Image.fromarray(ar)
    else:
        ar=np.array(out); ar[:,:,3]=(np.clip((ar[:,:,3].astype(float)-65)/190,0,1)*255).astype('uint8');out=Image.fromarray(ar)
    return out
def portable(im,box,name,navy=False,size=(340,260)):
    out=cut(im,box,navy)
    bbox=out.getbbox()
    if bbox: out=out.crop(bbox)
    out.thumbnail((size[0]-16,size[1]-16),Image.Resampling.LANCZOS)
    result=Image.new('RGBA',size)
    result.alpha_composite(out,((size[0]-out.width)//2,(size[1]-out.height)//2))
    records[name]={'source_box':box,'output_size':size,'navy_alpha':navy}
    return save(result,name)
def scene(name,width):
    if name=='digest':
        out=Image.new('RGBA',(780,1688),BG)
        locator=load(name).crop((0,0,400,510)).resize((360,459),Image.Resampling.LANCZOS)
        out.alpha_composite(locator,(20,10))
        return save(out,'background-'+name)
    src=load(name).crop((0,0,width,1024))
    # Keep the full anatomy in the top; tile only the empty lower field for height.
    src=src.resize((780,round(1024*780/width)),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(780,1688),BG)
    out.alpha_composite(src.crop((0,0,780,min(1688,src.height))))
    if src.height<1688:
        band=src.crop((0,src.height-100,780,src.height))
        for y in range(src.height,1688,100): out.alpha_composite(band,(0,y))
    return save(out,'background-'+name)
cell=load('cell'); ear=load('ear'); digest=load('digest'); arm=load('arm')
icons={}; slots={}
cell_specs=[('prelude-phospholipids',(640,0,965,300)),('prelude-water',(1070,0,1505,300)),('opening-dna',(680,310,930,637)),('opening-nuclear-envelope',(1060,310,1500,645)),('opening-nucleus',(590,650,1030,1015)),('opening-cell',(1070,645,1500,1016))]
for key,box in cell_specs: icons['id:'+key]=portable(cell,box,key,size=(340,300) if key!='opening-cell' else (520,520))
envelope=Image.open(A/'opening-nuclear-envelope.png').convert('RGBA')
# Preserve the envelope and canvas; remove a fragment from the next atlas row.
envelope.paste((0,0,0,0),(0,280,340,300));save(envelope,'opening-nuclear-envelope')
nuc=Image.open(A/'opening-nucleus.png').convert('RGBA'); nuc.thumbnail((255,225),Image.Resampling.LANCZOS)
overlay=Image.new('RGBA',(520,520)); overlay.alpha_composite(nuc,(135,145)); save(overlay,'cell-nucleus-fitted')
save(Image.new('RGBA',(520,520)),'cell-unillustrated-fitting')
slots['id:opening-cell']={ 'id:opening-nucleus':'assets/cell-nucleus-fitted.png', **{ 'id:'+key:'assets/cell-unillustrated-fitting.png' for key in ['opening-mitochondria','school-sugar-carrier','school-ribosome']}}
cover=Image.open(A/'opening-cell.png').convert('RGBA');cover.alpha_composite(overlay); save(cover,'heading')
ear_names=['Outer ears and canals','Eardrums','Outer ears with eardrums','Middle-ear bones','Sound-conducting ears','Coiled inner-ear chambers and fluid','Hearing cells with tiny hairs','Vibration-sensitive inner ears','Sound-receiving ears','Hearing pathways','Inner ears with hearing pathways','Ears']
# Actual inspected boundaries; these are not equal atlas cells.
ear_boxes=[(435,8,715,252),(865,15,1030,250),(1150,10,1490,250),(445,265,735,465),(775,265,1135,480),(1155,260,1510,490),(411,495,750,720),(772,497,1128,723),(1137,500,1526,721),(409,740,760,986),(765,740,1128,985),(1134,730,1534,992)]
for i,(name,box) in enumerate(zip(ear_names,ear_boxes)): icons['name:'+name]=portable(ear,box,'hearing-'+str(i+1),True,size=(344,244))
digest_names=['Starchy food','Saliva','Shorter starch chains','Digestive enzymes','Meal glucose','Protein food','Meal amino acids','Fat food','Bile','Small fat droplets','Fat digestion products']
# Digestive atlas coordinates are set after source inspection.
digest_boxes=[(423,38,775,255),(802,25,1135,255),(1200,61,1517,230),(425,275,754,490),(807,274,1105,479),(1152,280,1524,484),(438,520,736,705),(782,499,1133,736),(1170,503,1526,711),(424,739,758,950),(789,770,1124,925)]
for i,(name,box) in enumerate(zip(digest_names,digest_boxes)): icons['name:'+name]=portable(digest,box,'digestion-'+str(i+1),True,size=(324,244))
icons['id:prelude-myoblasts']=portable(arm,(690,300,1050,450),'muscle-cells',True,size=(340,180))
icons['id:school-bone-mineral']=portable(arm,(1080,284,1435,454),'bone-mineral',True,size=(340,180))
# One shared arm silhouette. The exact same source pixels produce its four fittings.
box=(48,62,785,965); full=cut(arm,box,True)
ar=np.array(full); rgb=ar[:,:,:3].astype(float); yy,xx=np.indices(ar.shape[:2]); gx=xx+box[0]; gy=yy+box[1]
def polygon(points):
    mask=Image.new('L',full.size);ImageDraw.Draw(mask).polygon([(x-box[0],y-box[1]) for x,y in points],fill=255)
    return np.array(mask)>0
front=polygon([(264,220),(290,220),(313,262),(341,307),(362,357),(369,410),(358,468),(335,516),(325,557),(306,557),(296,514),(271,468),(251,411),(246,355),(250,299)])
back=polygon([(136,230),(156,246),(182,232),(200,264),(217,311),(221,379),(216,446),(198,504),(187,573),(165,573),(152,530),(122,479),(101,432),(91,370),(98,311),(112,270)])
pink=(rgb[:,:,0]>rgb[:,:,1]*1.32)&(rgb[:,:,0]>rgb[:,:,2]*.85)&(rgb[:,:,0]>70)
front|=pink&(gx>238)&(gx<374)&(gy>205)&(gy<559)
back|=pink&(gx>87)&(gx<224)&(gy>215)&(gy<580)
gold=(rgb[:,:,0]>rgb[:,:,2]*1.5)&(rgb[:,:,0]>rgb[:,:,1]*1.07)&(rgb[:,:,0]>80)
radius=gold&(gx>393)&(gx<483)&(gy>626)&(gy<693)
ulna=gold&(gx>325)&(gx<418)&(gy>669)&(gy<730)
# Exclude the locator line, which is unrelated to the isolated arm canvas.
line=((gx>281)&(gy<184))|((gx>650)&(gy<650)); ar[line,3]=0
base=ar.copy(); base[front|back,3]=0
# Unmineralized windows retain their source's living matrix, with cyan rather than gold.
for mask in [radius,ulna]:
    brightness=rgb[mask].max(axis=1); base[mask,0]=(brightness*.30).astype('uint8');base[mask,1]=(brightness*.70).astype('uint8');base[mask,2]=(brightness*.90).astype('uint8')
scale=.82; display=(round(full.width*scale),round(full.height*scale)); canvas=(display[0]*2,display[1]*2)
arm_scene=Image.new('RGBA',(780,1688),BG)
arm_scene.alpha_composite(Image.fromarray(base).resize(display,Image.Resampling.LANCZOS),(74,190))
locator=cut(arm,(1024,0,1260,278),True); locator.thumbnail((144,170));arm_scene.alpha_composite(locator,(585,28))
save(arm_scene,'background-arm')
empty=Image.new('RGBA',canvas);save(empty,'arm-region-base')
for name,mask in [('biceps',front),('triceps',back),('radius-mineral',radius),('ulna-mineral',ulna)]:
    layer=ar.copy();layer[~mask,3]=0
    save(Image.fromarray(layer).resize(canvas,Image.Resampling.LANCZOS),'fitted-'+name)
for region,muscle,mineral in [('arm-front-tendons','biceps','radius-mineral'),('arm-back-tendons','triceps','ulna-mineral')]:
    icons['id:'+region]='assets/arm-region-base.png'
    slots['id:'+region]={'id:prelude-myoblasts':'assets/fitted-'+muscle+'.png','id:school-bone-mineral':'assets/fitted-'+mineral+'.png'}
save(Image.new('RGBA',(240,160),(226,224,216,255)),'unillustrated-item');save(Image.new('RGBA',(240,160)),'unillustrated-fitting')
mapping={'headingIcon':'assets/heading.png','defaultIcon':'assets/unillustrated-item.png','defaultOverlay':'assets/unillustrated-fitting.png','defaultBackground':'../../placeholder.svg','chapterBackgrounds':{'1':scene('cell',569),'4':'assets/background-arm.png','8':scene('ear',402),'18':scene('digest',400)},'itemIcons':icons,'slotIcons':slots,'hotspots':{'4':{}}}
center=[74+display[0]/2,190+display[1]/2]
mapping['hotspots']['4']={'id:arm-front-tendons':{'center':center,'hitbox':{'center':[340,580],'size':[210,510]}},'id:arm-back-tendons':{'center':center,'hitbox':{'center':[180,580],'size':[150,510]}}}
(ROOT/'art-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
records['arm']={'source_box':box,'scene_origin':[74,190],'scene_scale':scale,'overlay_canvas':canvas,'center':center,'mask_method':'Hand-traced polygons isolate full muscle bellies including pale striations; colour-select gold mineral pixels inside separate radius/ulna windows. Preserve ivory tendons in background. Mineral-free bone matrix retains source geometry with cyan tint. Exclude locator stroke and neighbouring muscle-cell tips from arm crop.'}
(ROOT/'registration.json').write_text(json.dumps(records,indent=2)+'\n')

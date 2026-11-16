from PIL import Image, ImageOps
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent.parent
ASSETS=ROOT/'assets'
def save(im,name): im.save(ASSETS/name)
for name in ['cell','arm','ear','digestion']:
    im=Image.open(ROOT/'sources'/f'{name}.png').convert('RGB')
    im=im.resize((780,round(im.height*780/im.width)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(780,1688))
    canvas.paste(im,(0,0))
    # Stretch only the already empty paper below the anatomical painting.
    # One continuous extension avoids repeated texture seams or row streaks.
    paper_start=900
    tail=im.crop((0,paper_start,780,im.height)).resize((780,1688-paper_start),Image.Resampling.BICUBIC)
    canvas.paste(tail,(0,paper_start))
    save(canvas,f'{name}-background.webp')

catalog={
 'cell-icons':['lipids','water','dna','envelope','nucleus','cell','muscle-cells','mineral','biceps','triceps','bone-matrix','crystals'],
 'ear-icons':['outer-ear','eardrum','outer-eardrum','ossicles','sound-conducting','cochlea','hair-cells','sensing-cochlea','sound-receiving','hearing-nerve','cochlea-nerve','ears'],
 'food-icons':['starch','saliva','short-starch','enzymes','glucose','protein-food','amino-acids','fat','bile','small-droplets','fat-products','enzyme-fat']
}
raw={}
record={}
for atlas,names in catalog.items():
    im=Image.open(ROOT/'sources'/f'{atlas}.png').convert('RGBA')
    for i,name in enumerate(names):
        col,row=i%4,i//4
        bounds=(round(col*im.width/4)+3,round(row*im.height/3)+3,round((col+1)*im.width/4)-3,round((row+1)*im.height/3)-3)
        # This generated atlas's middle row ends above the nominal grid line.
        # Exclude the next row's tendon tips and matrix rather than exporting them.
        if atlas=='cell-icons':
            bounds={
                'nucleus':(10,356,343,682),
                'cell':(352,365,726,676),
                'muscle-cells':(727,359,1083,683),
                'mineral':(1088,366,1448,685),
            }.get(name,bounds)
        crop=im.crop(bounds)
        bb=crop.getchannel('A').point(lambda x:255 if x>80 else 0).getbbox()
        if bb: crop=crop.crop(bb)
        raw[name]=crop
        target= (540,480) if name=='cell' else ((440,340) if name in ['ears','sound-receiving','sound-conducting'] else (300,260))
        cut=ImageOps.contain(crop,(target[0]-20,target[1]-20),Image.Resampling.LANCZOS)
        out=Image.new('RGBA',target)
        out.alpha_composite(cut,((target[0]-cut.width)//2,(target[1]-cut.height)//2))
        save(out,name+'.png')
        record[name]={'source':atlas+'.png','cell':i,'bounds':bounds,'alpha_bounds':bb,'output':target}

# Same-canvas overlay at the cell's interior.
out=Image.new('RGBA',(540,480))
part=ImageOps.contain(raw['nucleus'],(200,185),Image.Resampling.LANCZOS)
out.alpha_composite(part,(175,135))
save(out,'cell-nucleus.png')
save(Image.new('RGBA',(540,480)),'cell-empty-overlay.png')
save(Image.new('RGBA',(256,256)),'unillustrated.png')

# Fixed artwork uses a 2x background canvas so quarter-size rendering fills
# the same 390x844 reference frame as the 780x1688 scene.
fixed=(1560,3376)
save(Image.new('RGBA',fixed),'arm-base.png')
for side,partname,box,window in [
 ('front','biceps',(686,122,160,670),(342,1038)),
 ('back','triceps',(850,152,175,570),(1214,1038))]:
    out=Image.new('RGBA',fixed)
    x,y,w,h=box
    part=raw[partname].resize((w,h),Image.Resampling.LANCZOS)
    if side=='back':
        # Keep proximal heads beside the humerus; align distal tendon with
        # the olecranon behind the shared elbow rather than floating beside it.
        part=part.transform((w+120,h),Image.Transform.AFFINE,(1,0.20,-114,0,1,0),Image.Resampling.BICUBIC)
        x-=114
    out.alpha_composite(part,(x,y))
    save(out,f'arm-{side}-muscle.png')
    out=Image.new('RGBA',fixed)
    crystals=ImageOps.contain(raw['crystals'],(240,190),Image.Resampling.LANCZOS)
    out.alpha_composite(crystals,(window[0]-crystals.width//2,window[1]-crystals.height//2))
    save(out,f'arm-{side}-mineral.png')

# Catalogue identity is a square crop of the selected cell painting.
im=Image.open(ROOT/'sources/cell.png').convert('RGB')
save(im.crop((0,0,977,977)).resize((256,256),Image.Resampling.LANCZOS),'identity.png')
(ROOT/'sources/extraction.json').write_text(json.dumps(record,indent=2)+'\n')

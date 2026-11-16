"""Mechanical exports from own selected raster masters. Run after export.py.
No illustrated scene is used as a background. Coordinates are retained here.
"""
from PIL import Image,ImageDraw,ImageOps
from pathlib import Path
import json,itertools
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'assets'
S=ROOT/'sources'
RUN=ROOT.parents[3]/'runs/anatomy-style-refresh/vintage-1950'
RUN.mkdir(parents=True,exist_ok=True)
# A plain ivory sheet has no scientific content to pre-empt interaction.
for name in ['cell','arm','ear','digestion']:
 Image.new('RGB',(780,1688),(246,236,212)).save(A/f'{name}-background.webp',lossless=True)
# Cut material from the very same membrane bag; keep its pixel magnification.
cell=Image.open(A/'cell.png').convert('RGBA')
polygons={
 'water':[(80,205),(92,173),(130,151),(204,124),(282,113),(367,96),(424,83),(450,87),(468,104),(471,133),(466,161),(477,206),(478,245),(461,277),(420,313),(370,340),(322,353),(230,354),(160,351),(115,349),(89,329),(75,292),(75,250)],
 'lipids':[(110,93),(150,62),(190,44),(230,29),(315,25),(380,24),(385,82),(315,98),(250,107),(190,120),(140,140)]
}
for name,points in polygons.items():
 mask=Image.new('L',cell.size);ImageDraw.Draw(mask).polygon(points,fill=255)
 out=cell.copy();out.putalpha(mask);out=out.crop(mask.getbbox());out.save(A/f'{name}.png')
# Nuclear components retain the same magnification before and after fitting.
for name,target in [('nucleus',(184,180)),('envelope',(184,180)),('dna',(86,124))]:
 im=Image.open(A/f'{name}.png').convert('RGBA');im=im.crop(im.getbbox())
 im=ImageOps.contain(im,target,Image.Resampling.LANCZOS);im.save(A/f'{name}.png')
n=Image.open(A/'nucleus.png');out=Image.new('RGBA',cell.size);out.alpha_composite(n,(200,163));out.save(A/'cell-nucleus.png')
# Partition ONE transparent skeleton and two tissue windows into receiver layers.
# Shared skeleton + radius detail belong to front; ulna window and rear tendon
# scaffold belong to back. Their sum preserves a single arm, never two skeletons.
master=Image.open(S/'arm-transparent.png').convert('RGBA')
scale=1560/master.width
fixed=(1560,3376)
master=master.resize((1560,round(master.height*scale)),Image.Resampling.LANCZOS)
whole=Image.new('RGBA',fixed);whole.alpha_composite(master)
back=Image.new('RGBA',fixed)
box=(round(590*scale),round(510*scale),round(900*scale),round(785*scale))
back.alpha_composite(whole.crop(box),(box[0],box[1]))
front=whole.copy();front.paste((0,0,0,0),box)
# Triceps' pale tendons are supplied, the red belly remains an independent fit.
muscle=Image.open(A/'arm-back-muscle.png').convert('RGBA')
tendon=muscle.copy();px=tendon.load()
for y in range(tendon.height):
 for x in range(tendon.width):
  r,g,b,a=px[x,y]
  if a and not (r-g<65 and g-b<75 and g>115): px[x,y]=(0,0,0,0)
back.alpha_composite(tendon)
front.save(A/'arm-front-base.png');back.save(A/'arm-back-base.png')
# Bone mineral is one shared material at the same inset scale.
crystal=Image.open(A/'crystals.png').convert('RGBA');crystal=crystal.crop(crystal.getbbox())
crystal=ImageOps.contain(crystal,(210,170),Image.Resampling.LANCZOS)
crystal.save(A/'mineral.png')
for side,c in [('front',(215,653)),('back',(752,653))]:
 out=Image.new('RGBA',fixed);x,y=[round(v*scale) for v in c]
 out.alpha_composite(crystal,(x-crystal.width//2,y-crystal.height//2));out.save(A/f'arm-{side}-mineral.png')
# Related ear parts use a shared macroscopic magnification, with a tissue
# inspection family for cochlear hair cells (explicitly labelled in object art).
for name,box in [('outer-ear',(330,320)),('outer-eardrum',(330,320)),('sound-conducting',(390,320)),('sound-receiving',(430,320)),('ears',(480,320)),('eardrum',(84,86)),('ossicles',(125,105)),('cochlea',(150,150)),('hearing-nerve',(158,92))]:
 im=Image.open(A/f'{name}.png').convert('RGBA');im=im.crop(im.getbbox())
 ImageOps.contain(im,box,Image.Resampling.LANCZOS).save(A/f'{name}.png')
# Carry the same located tissue enlargement through every assembled ear that
# contains sensory cells; the coil gives the cross-section a physical address.
detail=Image.open(A/'sensing-cochlea.png').convert('RGBA')
detail=ImageOps.contain(detail.crop(detail.getbbox()),(210,210),Image.Resampling.LANCZOS)
for name,mainname in [('sensing-cochlea','cochlea'),('cochlea-nerve','cochlea-nerve'),('sound-receiving','sound-receiving'),('ears','ears')]:
 main=Image.open(A/f'{mainname}.png').convert('RGBA')
 if name=='cochlea-nerve': main=ImageOps.contain(main.crop(main.getbbox()),(190,160),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(main.width+250,max(main.height,250)))
 out.alpha_composite(main,(0,0))
 x=main.width+35
 out.alpha_composite(detail,(x,20))
 draw=ImageDraw.Draw(out)
 draw.line([(main.width-25,min(125,main.height//2)),(x,120)],fill=(114,79,46,255),width=2)
 draw.text((x+40,232),'ENLARGED',fill=(90,55,30,255),font_size=17)
 out.save(A/f'{name}.png')
# Small playing-scale proofs are scratch, not evidence deliverables.
proof=Image.new('RGB',(780*4,844*4),(246,236,212))
for i,bits in enumerate(itertools.product([False,True],repeat=4)):
 im=Image.alpha_composite(front,back)
 for yes,name in zip(bits,['front-mineral','front-muscle','back-mineral','back-muscle']):
  if yes:im.alpha_composite(Image.open(A/f'arm-{name}.png'))
 im=im.resize((390,844),Image.Resampling.LANCZOS)
 proof.paste(im,((i%4)*780,(i//4)*844),im)
 ImageDraw.Draw(proof).text(((i%4)*780+400,(i//4)*844+40),str(bits),fill='black')
proof.save(RUN/'arm-partial-states.png')
record={'backgrounds':'plain ivory RGB 246,236,212; 780x1688','cellComponentMasks':polygons,'cellFittedNucleusTopLeft':[200,163],'armSource':'arm-transparent.png','armSourceSize':[977,1609],'armCanvas':fixed,'armScale':scale,'backWindowBox':[round(590*scale),round(510*scale),round(900*scale),round(785*scale)],'armMineralCentersInMaster':{'front':[215,653],'back':[752,653]},'inspectionScaleException':'Cochlear tissue strips are enlarged views, not literal organ size.'}
(S/'refresh-extraction.json').write_text(json.dumps(record,indent=2)+'\n')

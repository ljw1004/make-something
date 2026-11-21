"""Requested chapter sheets and gallery, from runtime exports + disposable captures.
Requires Pillow. Run after check-player.mjs with a 390x844 viewport.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from html import escape
import subprocess,json,math,textwrap,sys,shutil,hashlib
P=Path(__file__).resolve().parent;R=P.parent
CAP=P.parents[2]/'runs/anatomy-atlas/captures-390x844'
OUT=P/'chapter-sheets';OUT.mkdir(exist_ok=True)
if len(sys.argv)!=2:raise SystemExit('Usage: make-sheets.py runs/anatomy-composition-review/NEW_ROUND')
packet_root=Path(sys.argv[1])
if packet_root and (packet_root/'source.md').read_bytes()!=(R/'anatomy.md').read_bytes():raise ValueError('Recipe packet must match current manuscript')
if packet_root:
 # The manuscript can stay identical while an illustration changes. Reject
 # stale frozen recipe art before writing any retained deliverables.
 frozen_assets=(packet_root/'assets').resolve()
 for packet_file in packet_root.glob('*/packet.json'):
  packet=json.loads(packet_file.read_text())
  for operation in packet['operations']:
   for role in ['a','b','result']:
    obj=operation[role]
    for filename in [obj['base'],*obj['layers']]:
     frozen=Path(filename).resolve();current=R/frozen.relative_to(frozen_assets)
     if hashlib.sha256(frozen.read_bytes()).digest()!=hashlib.sha256(current.read_bytes()).digest():
      raise ValueError(f'Recipe packet artwork must match current export: {current}')
chapters=json.loads(subprocess.check_output(['node',str(P/'catalogue.ts')]))
font=lambda n:ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
BG=(250,247,238);ink=(65,51,42)
def fit(im,w,h):
 s=min(w/im.width,h/im.height);return im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
def scene(path):
 im=Image.open(path).convert('RGB')
 # The wide atlas sheet is letterboxed in a tall phone. Retain the actual paper.
 rows=[]
 for y in range(im.height):
  r,g,b=im.getpixel((im.width//2,y))
  if r+g+b>150:rows.append(y)
 if rows:im=im.crop((0,min(rows),im.width,max(rows)+1))
 return im
cards=[];overview=Image.new('RGB',(1600,7*670),BG);od=ImageDraw.Draw(overview)
for c in chapters:
 n=c['number'];icons=[]
 for it in c['icons']:
  icons.append((it['name'],it['path'],None))
  for sl in it['slots']:icons.append((it['name']+' + '+sl['name']+' (fitted)',sl['path'],it['path']))
 recipes=[];recipe_html=''
 if packet_root:
  packet=json.loads((packet_root/f'{n:02}'/'packet.json').read_text())
  destination=P/'recipes'/f'chapter-{n}';destination.mkdir(parents=True,exist_ok=True)
  expected={f'operation-{j:02}.png' for j in range(1,len(packet['operations'])+1)}
  for old in destination.glob('operation-*.png'):
   if old.name not in expected:old.unlink()
  recipe_lines=[];figures=[]
  for j,op in enumerate(packet['operations'],1):
   rule=op['rule']
   if op['fates'][1] is None:
    rule=rule.replace(f"{op['a']['name']} + {op['b']['name']}",f"{op['a']['name']} @ {op['b']['name']}",1)
   label=f"{j}. {rule}";recipes.extend(textwrap.wrap(label.replace('→','->'),112))
   fates=', '.join(f"{op[k]['name']}: {fate if fate is not None else 'fixed context'}" for k,fate in zip(['a','b'],op['fates']))
   filename=f'operation-{j:02}.png';shutil.copyfile(packet_root/f'{n:02}'/filename,destination/filename)
   recipe_lines.append(label+' — '+fates+'.')
   figures.append(f'<figure><figcaption>{escape(label)}<br><small>{escape(fates)}</small></figcaption><a href="recipes/chapter-{n}/{filename}"><img loading="lazy" src="recipes/chapter-{n}/{filename}" alt="{escape(label)}"></a></figure>')
  (destination/'recipes.md').write_text(f"# {n}. {c['title']}\n\n"+'\n\n'.join(recipe_lines)+'\n')
  recipe_html='<details><summary>See each combination at a shared scale</summary>'+''.join(figures)+'</details>'
 rows=math.ceil(len(icons)/5);height=700+rows*170+(65+len(recipes)*20 if recipes else 0)
 sheet=Image.new('RGB',(1000,height),BG);d=ImageDraw.Draw(sheet)
 d.text((18,12),f"{n}. {c['title']}",font=font(25),fill=ink)
 for i,suffix in enumerate(['-entry','']):
  label=['Starting pieces','Completed chapter'][i];d.text((i*500+16,52),label,font=font(18),fill=ink)
  im=fit(scene(CAP/f'chapter-{n}{suffix}.png'),475,570);sheet.paste(im,(i*500+(500-im.width)//2,85))
 d.text((18,665),'Complete object and fitting inventory · inspection thumbnails',font=font(17),fill=ink)
 for i,(name,path,basepath) in enumerate(icons):
  im=Image.open(R/path).convert('RGBA')
  if basepath:
   base=Image.open(R/basepath).convert('RGBA');base.alpha_composite(im.resize(base.size,Image.Resampling.LANCZOS));im=base
  box=im.getchannel('A').point(lambda a:255 if a>10 else 0).getbbox();im=im.crop(box) if box else im
  im=fit(im,174,116);x=(i%5)*200;y=705+(i//5)*170;sheet.paste(im,(x+(200-im.width)//2,y),im)
  lines=textwrap.wrap(name,29)[:3]
  for j,line in enumerate(lines):d.text((x+8,y+122+j*16),line,font=font(13),fill=ink)
 if recipes:
  y=710+rows*170;d.text((18,y),'Construction sequence · detailed ingredient/result strips in the gallery',font=font(17),fill=ink)
  for j,line in enumerate(recipes):d.text((18,y+30+j*20),line,font=font(15),fill=ink)
 sheet.save(OUT/f'chapter-{n}.jpg',quality=90,subsampling=0)
 completed=fit(scene(CAP/f'chapter-{n}.png'),386,610);x=((n-1)%4)*400;y=((n-1)//4)*670
 for j,line in enumerate(textwrap.wrap(f"{n}. {c['title']}",32)[:2]):od.text((x+10,y+8+j*22),line,font=font(18),fill=ink)
 overview.paste(completed,(x+(400-completed.width)//2,y+56))
 cards.append(f'<section id="chapter-{n}"><h2>{n}. {escape(c["title"])}</h2><a href="chapter-sheets/chapter-{n}.jpg"><img loading="lazy" width="1000" height="{height}" src="chapter-sheets/chapter-{n}.jpg" alt="Starting and completed chapter with every object and fitted layer"></a>{recipe_html}</section>')
overview.save(P/'all-chapters.jpg',quality=92,subsampling=0)
study=Image.new('RGB',(1200,470),BG);sd=ImageDraw.Draw(study)
sd.text((20,15),'Nuclear envelope studies',font=font(28),fill=ink)
for i,(name,label) in enumerate([('nuclear-envelope','Selected: porous frontal cutaway'),('nuclear-envelope-alternative','Alternative: oblique cutaway'),('nucleus','Selected envelope with tangled DNA')]):
 im=fit(Image.open(P/'opening/assets'/f'{name}.png').convert('RGBA'),330,330);study.paste(im,(i*400+(400-im.width)//2,70),im);sd.text((i*400+16,420),label,font=font(18),fill=ink)
study.save(P/'nuclear-envelope-studies.jpg',quality=93,subsampling=0)
nav=' '.join(f'<a href="#chapter-{n}">{n}</a>' for n in range(1,29))
(P/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anatomy · 1800s atlas</title><style>
*{box-sizing:border-box}body{margin:0;background:#eee7d9;color:#41332a;font:17px/1.5 system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:32px}h1{font:clamp(34px,5vw,62px)/1.1 Georgia,serif;margin:12px 0}a{color:#79513a;text-underline-offset:3px}p{max-width:900px}.actions{display:flex;gap:24px;align-items:center;flex-wrap:wrap;margin:24px 0}.play{background:#513d30;color:#fffaf0;padding:12px 22px;border-radius:5px;text-decoration:none}nav{display:flex;gap:14px;flex-wrap:wrap;margin:28px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}section{background:#faf7ee;border:1px solid #ccbfac;scroll-margin-top:16px}h2{font:23px/1.3 Georgia,serif;padding:16px;margin:0}img{display:block;width:100%;height:auto}details{padding:16px}summary{cursor:pointer}figure{margin:20px 0}figcaption{margin-bottom:8px}footer{margin-top:30px;font-size:14px}@media(max-width:900px){main{padding:20px 12px}.grid{grid-template-columns:1fr}}</style><main><p>Anatomy · Selected art direction</p><h1>The anatomical atlas</h1><p>Build the whole book: 28 illustrated chapters, from the cell boundary to the assembled body. Each object shows its present physical structure. The page stays blank until you combine its parts.</p><div class="actions"><a class="play" href="../../../make-something.html?story=projects/anatomy-study/anatomy.md">Play the entire story ↗</a><a href="all-chapters.jpg">All-chapter contact sheet</a><a href="nuclear-envelope-studies.jpg">Nuclear envelope studies</a><a href="README.md">Production notes</a></div><p>Each panel contains the starting and completed player views, plus every object and fitted appearance needed for that chapter. Inventory thumbnails enlarge small details; the player views preserve their relative sizes. Each sheet lists its construction sequence. Expand its combinations to compare both ingredients and the result at the same scale, with consumed and preserved inputs identified.</p><nav aria-label="Chapters">'''+nav+'</nav><div class="grid">'+''.join(cards)+'</div><footer>1800s engraving direction with modern anatomical cutaways. Original comparison studies remain available <a href="../art-study/gallery.html">here</a>.</footer></main></html>')
print('Wrote 28 complete chapter sheets, contact sheet and review gallery.')

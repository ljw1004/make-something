"""Compose requested entry/completion sheets from disposable browser captures."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from html import escape
import re
R=Path(__file__).resolve().parent.parent
CAP=R.parents[3]/'runs/anatomy-star-rework/captures'
OUT=R/'chapter-sheets';OUT.mkdir(exist_ok=True)
font=lambda n:ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
titles=[re.sub(r'^`[^`]+`\s*','',s) for s in re.findall(r'^## (.+)$',(R/'anatomy.md').read_text(),re.M)][:28]
sheets=[]
for n,title in enumerate(titles,1):
 files=[CAP/f'chapter-{n}-entry.png',CAP/f'chapter-{n}.png']
 if not all(p.exists() for p in files):raise RuntimeError(f'Missing chapter{n} captures')
 sheet=Image.new('RGB',(800,936),'#e8ecec');d=ImageDraw.Draw(sheet)
 d.text((14,9),f'{n}. {title}',font=font(23),fill='#16313b')
 for i,(label,p) in enumerate(zip(['Starting pieces','Completed chapter'],files)):
  d.text((i*400+12,49),label,font=font(19),fill='#31535e')
  im=Image.open(p).convert('RGB').resize((390,844),Image.Resampling.LANCZOS);sheet.paste(im,(i*400+5,86))
 sheet.save(OUT/f'chapter-{n}.jpg',quality=93,subsampling=0);sheets.append(sheet)
all=Image.new('RGB',(1600,936*14),'#e8ecec')
for i,im in enumerate(sheets):all.paste(im,((i%2)*800,(i//2)*936))
all.save(R/'all-chapters.jpg',quality=91,subsampling=0)
# Keep the thirteen-direction gallery's four-view slot current too.
sample=Image.new('RGB',(1600,952),'#f5f3ed');d=ImageDraw.Draw(sample)
d.text((16,12),'Futuristic holographic · revised full-book treatment',font=font(27),fill='#18272d')
d.text((16,47),'Anatomy · Interactive anatomy on a blank sheet · Completed chapter views',font=font(17),fill='#49565b')
for i,(n,name) in enumerate([(1,'Cell boundary'),(4,'Bones and muscles'),(8,'Hearing'),(18,'Digestion')]):
 d.text((i*400+10,79),f'{n}. {name}',font=font(18),fill='#18272d');im=Image.open(CAP/f'chapter-{n}.png').convert('RGB').resize((390,844),Image.Resampling.LANCZOS);sample.paste(im,(i*400+5,105))
sample.save(R/'contact-sheet.jpg',quality=95,subsampling=0)
play='../../../../make-something.html?story=projects/anatomy/art-study/farout-star-trek/anatomy.md'
cards='\n'.join(f'<section id="chapter-{n}"><h2>{n}. {escape(t)}</h2><a href="chapter-sheets/chapter-{n}.jpg"><img loading="lazy" width="800" height="936" src="chapter-sheets/chapter-{n}.jpg" alt="Starting pieces and completed chapter: {escape(t)}"></a></section>' for n,t in enumerate(titles,1))
nav=' '.join(f'<a href="#chapter-{n}">{n}</a>' for n in range(1,29))
(R/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anatomy · Star Trek rework</title><style>
*{box-sizing:border-box}body{margin:0;background:#031525;color:#e8f3f6;font:17px/1.5 system-ui,sans-serif}main{max-width:1660px;margin:auto;padding:30px}h1{font-size:clamp(30px,4vw,54px);line-height:1.1;margin:0 0 20px}p{max-width:900px}a{color:#8ee0ed;text-underline-offset:3px}.actions{display:flex;gap:24px;flex-wrap:wrap;margin:24px 0}.play{background:#dbf6f6;color:#082c3a;padding:11px 20px;border-radius:6px;text-decoration:none;font-weight:650}nav{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}section{border:1px solid #254b5d;border-radius:6px;overflow:hidden;scroll-margin-top:15px}h2{font-size:19px;padding:14px;margin:0}img{display:block;width:100%;height:auto}footer{margin-top:30px;color:#9cb6c3;font-size:14px}@media(max-width:900px){main{padding:20px 12px}.grid{grid-template-columns:1fr}}</style><main><p>Anatomy · Revised Star Trek direction</p><h1>Build the page</h1><p>All 28 playable chapters are illustrated. Compare the starting pieces with each completed chapter: the grid remains blank, and the anatomy comes from the pieces you combine.</p><div class="actions"><a class="play" href="'''+play+'''">Play the revised book ↗</a><a href="all-chapters.jpg">Open the complete contact sheet ↗</a><a href="README.md">Production notes</a></div><p>Use the player’s bug button to jump to any chapter. Chapters 1 and 2 show the revised membrane, water, cell and organelle construction.</p><nav aria-label="Chapters">'''+nav+'</nav><div class="grid">'+cards+'</div><footer>Local artwork trial. The original manuscript and the other twelve art directions remain unchanged.</footer></main></html>')
print('Wrote28 chapter sheets, all-chapters.jpg, four-view sample and review.html')

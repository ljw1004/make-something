"""Assemble requested comparison deliverables from inspected player captures.

Run from the repository root with uv run --with pillow python followed by this
path. Inputs stay in ignored runs/anatomy-sample-flow/captures; outputs are deliverables. Each chapter panel includes its complete icon inventory and fitted states. --gallery-only updates links without requiring captures.
This composes existing pictures and does not draw or generate anatomy.
"""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
THEMES = [
    ('modern-student', 'Modern student textbook'),
    ('doctor-poster', "Doctor’s office poster"),
    ('vintage-1950', '1950s medical illustration'),
    ('classic-1800', '1800s anatomical atlas'),
    ('cut-paper', 'Contemporary cut-paper atlas'),
    ('farout-1800-researcher', 'Researcher’s notebook'),
    ('farout-cozy', 'Cozy'),
    ('farout-fun', 'Playful collage'),
    ('farout-graphic-design', 'Graphic design'),
    ('farout-lecture-notes', 'Lecture notes'),
    ('farout-macabre', 'Macabre'),
    ('farout-star-trek', 'Futuristic holographic'),
    ('farout-watercolor', 'Watercolor'),
]
CHAPTERS = [(1, 'Cell boundary'), (4, 'Bones and muscles'), (8, 'Hearing'), (18, 'Digestion')]


def font(size):
    return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', size)


def wrap(draw,text,limit,ft):
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if draw.textlength(candidate,font=ft)>limit and line:lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    return lines


def main():
    import json,sys
    from statistics import median
    capture_root=ROOT.parents[2]/'runs/anatomy-sample-flow/captures'
    gallery_only='--gallery-only' in sys.argv
    selected=set() if gallery_only else set(sys.argv[1:]) or {s for s,_ in THEMES}
    for slug,title in THEMES:
        if slug not in selected:continue
        directory=ROOT/slug
        manifest=json.loads((directory/'comparison-assets.json').read_text())
        out=directory/'comparison';out.mkdir(exist_ok=True)
        panels=[]
        for chapter in manifest['chapters']:
            n=chapter['number'];capture=capture_root/slug
            entry=Image.open(capture/f'chapter-{n}-entry.png').convert('RGB')
            done=Image.open(capture/f'chapter-{n}.png').convert('RGB')
            samples=[entry.getpixel((round(entry.width*x),round(entry.height*y))) for x in [.1,.5,.9] for y in [.3,.4,.5,.6,.7]]
            samples=[c for c in samples if max(c)>5]
            ground=tuple(round(median(c[k] for c in samples)) for k in range(3))
            panel=Image.new('RGB',(1600,1120),'#f1f1ec');draw=ImageDraw.Draw(panel)
            draw.text((20,14),title,font=font(30),fill='#18313b')
            draw.text((20,55),f"{n}. {chapter['title']}",font=font(25),fill='#18313b')
            draw.text((20,104),'Starting pieces',font=font(20),fill='#405761')
            draw.text((330,104),'Completed chapter',font=font(20),fill='#405761')
            for x,im in [(20,entry),(330,done)]:panel.paste(im.resize((300,649),Image.Resampling.LANCZOS),(x,138))
            for i,line in enumerate(['Player views preserve the actual scale.', 'The inventory shows every input and result,', 'plus the chapter’s fitted parts and states.', 'Isolated details are enlarged for inspection.']):
                draw.text((20,825+i*30),line,font=font(19),fill='#405761')
            draw.text((656,104),'Complete icon family',font=font(21),fill='#18313b')
            for i,asset in enumerate(chapter['assets']):
                x=650+(i%3)*312;y=138+(i//3)*190
                draw.rounded_rectangle((x,y,x+302,y+180),radius=5,fill=ground)
                if 'layers' in asset:
                    layers=[Image.open(directory/p).convert('RGBA') for p in asset['layers']]
                    im=layers[0].copy()
                    for layer in layers[1:]:
                        if layer.size!=im.size:raise ValueError(f"Unregistered fitting {slug}: {asset['id']}")
                        im.alpha_composite(layer)
                else:im=Image.open(directory/asset['path']).convert('RGBA')
                box=im.getchannel('A').point(lambda a:255 if a>20 else 0).getbbox()
                if box:im=im.crop(box)
                im.thumbnail((282,126),Image.Resampling.LANCZOS)
                panel.paste(im,(x+(302-im.width)//2,y+6+(126-im.height)//2),im)
                luminance=sum(ground)/3
                ink='#f3f6f7' if luminance<125 else '#18313b'
                lines=wrap(draw,asset['label'],282,font(16))
                for j,line in enumerate(lines[:3]):draw.text((x+10,y+134+j*15),line,font=font(16),fill=ink)
            panel.save(out/f'chapter-{n}.jpg',quality=93,subsampling=0);panels.append(panel)
        sheet=Image.new('RGB',(3200,2240),'#f1f1ec')
        for i,panel in enumerate(panels):sheet.paste(panel,((i%2)*1600,(i//2)*1120))
        sheet.save(directory/'contact-sheet.jpg',quality=92,subsampling=0)
        print(f'{slug}: four chapter panels, 33 identities, 5 fitted layers and 7 fitted states')
    sheets=[];cards=[];nav=[]
    for slug,title in THEMES:
        path=ROOT/slug/'contact-sheet.jpg'
        if not path.exists():
            print(f'Overview awaits {slug} contact sheet');return
        sheets.append(Image.open(path).convert('RGB').resize((1600,1120),Image.Resampling.LANCZOS))
        nav.append(f'<a href="#{slug}">{escape(title)}</a>')
        play=f'../../../index.html?story=projects/anatomy-study/art-study/{slug}/sample.md'
        details=' · '.join(f'<a href="{slug}/comparison/chapter-{n}.jpg">Chapter {n}</a>' for n,_ in CHAPTERS)
        cards.append(f'<section id="{slug}"><div class="caption"><h2>{escape(title)}</h2><p><a class="play" href="{play}">Play all four chapters ↗</a> · <a href="{slug}/contact-sheet.jpg">Full contact sheet ↗</a> · <a href="{slug}/README.md">Sources and production notes</a></p><p>{details}</p></div><a href="{slug}/contact-sheet.jpg"><img loading="lazy" width="3200" height="2240" src="{slug}/contact-sheet.jpg" alt="Four chapters and their complete icon families in {escape(title)}"></a></section>')
    overview=Image.new('RGB',(1600,1120*len(sheets)),'#f1f1ec')
    for i,sheet in enumerate(sheets):overview.paste(sheet,(0,i*1120))
    if not gallery_only:overview.save(ROOT/'all-themes.jpg',quality=90,subsampling=0)
    (ROOT/'gallery.html').write_text("""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anatomy · Thirteen artwork directions</title><style>
*{box-sizing:border-box}body{margin:0;background:#eceeea;color:#18313b;font:17px/1.5 system-ui,sans-serif}main{max-width:1660px;padding:30px 20px;margin:auto}h1{font-size:clamp(30px,4vw,50px);line-height:1.1}p{max-width:1000px}a{color:#265d70;text-underline-offset:3px}nav{display:flex;gap:10px 22px;flex-wrap:wrap;margin:28px 0}section{background:#f1f1ec;border:1px solid #ccd5d3;border-radius:6px;overflow:hidden;margin:0 0 34px;scroll-margin-top:15px}.caption{padding:15px 20px}.caption h2,.caption p{margin:0 0 8px}img{display:block;width:100%;height:auto}.play{font-weight:650}footer{margin-top:30px;font-size:14px;color:#4b626c}</style><main><p>Anatomy · Revised artwork comparison</p><h1>Thirteen ways to draw the same textbook</h1><p>Each direction covers <strong>1. Cell boundary · 4. Bones and muscles · 8. Hearing · 18. Digestion.</strong> Every chapter panel shows its starting and completed playable views alongside the complete icon family, including intermediate results and fitted parts.</p><p>Backgrounds are blank sheets. The pieces carry the anatomy, with constituent materials and scales planned around what they become. Play all four chapters consecutively: cell boundary → bones and muscles → hearing → digestion. No chapter jumps are needed. The sheets retain the original book’s chapter numbers; the playable samples number these chapters 1–4.</p><p><a href="all-themes.jpg">Complete comparison sheet ↗</a> · <a href="farout-star-trek/review.html">Previously completed Star Trek full-book trial ↗</a></p><nav>"""+' '.join(nav)+'</nav>'+''.join(cards)+'<footer>Local comparison candidates. Every play link opens a complete four-chapter sample. The separate Star Trek full-book trial remains available. No production style has been selected. See <a href="README.md">the study notes</a> for sources, production and verification.</footer></main></html>')


if __name__=='__main__':main()

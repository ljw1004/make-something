"""Mechanical family registration, run by produce.py; no code-drawn anatomy."""
from PIL import Image, ImageDraw, ImageChops
import json

def refresh(root, out, icons, slots, backgrounds, registration, save):
    def opened(name): return Image.open(root/'masters'/name).convert('RGBA')
    def masked(im,points):
        m=Image.new('L',im.size); ImageDraw.Draw(m).polygon(points,fill=255)
        x=im.copy(); x.putalpha(ImageChops.multiply(im.getchannel('A'),m)); return x
    def sized(im,scale):
        return im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    def clean(im):
        im.putalpha(im.getchannel('A').point(lambda a:0 if a<32 else a));return im
    def tight(im,pad=12):
        b=im.getbbox()
        if not b:return im
        x=im.crop(b);c=Image.new('RGBA',(x.width+pad*2,x.height+pad*2));c.alpha_composite(x,(pad,pad));return c
    def write(key,im):
        name=key.removeprefix('id:').removeprefix('name:').lower().replace(' ','-')
        icons[key]=save(im,name)
    old=Image.open(out/'chapter-4.png').convert('RGBA')
    # Blank sheet. No anatomical or explanatory pixels appear in any background.
    paper=opened('arm.png').crop((30,1360,990,1500)).resize((1560,228))
    blank=Image.new('RGBA',(1560,3376))
    for y in range(0,3376,228):blank.paste(paper,(0,y))
    for ch in ['1','4','8','18']:backgrounds[ch]=save(blank,'chapter-'+ch)
    # Retain original arm's exact base and fitting pixels. Split the full plate
    # into complementary receivers, rather than painting anatomy on the sheet.
    left=Image.new('L',old.size);ImageDraw.Draw(left).rectangle((0,0,715,2339),fill=255)
    right=Image.new('L',old.size);ImageDraw.Draw(right).rectangle((716,0,1559,2339),fill=255)
    for side,m in [('front',left),('back',right)]:
        layer=old.copy();layer.putalpha(m);icons['id:arm-'+side+'-tendons']=save(layer,'arm-'+side+'-base')
    # Cell: water and membrane are extracted at precisely the same 0.4167 scale.
    master=clean(opened('cell-volume.png'))
    # Deliberate cutout follows only the outer silhouette, removing generated glow.
    outer=[(35,566),(85,441),(240,286),(480,162),(790,72),(1065,49),(1260,93),(1405,201),(1487,357),(1493,511),(1424,660),(1260,788),(1030,897),(766,973),(496,993),(282,942),(130,826),(62,678)]
    master=masked(master,outer)
    waterpts=[(189,588),(235,492),(408,358),(642,257),(880,202),(1092,194),(1244,241),(1351,336),(1364,434),(1293,521),(1130,607),(919,673),(699,713),(471,714),(289,667)]
    water=masked(master,waterpts)
    lipid=masked(master,[(350,738),(528,772),(768,761),(1026,700),(1056,823),(833,890),(571,919),(392,885)])
    scale=640/master.width
    cell=sized(master,scale);write('id:opening-cell',cell)
    write('id:prelude-water',tight(sized(water,scale)))
    write('id:prelude-phospholipids',tight(sized(lipid,scale)))
    oldcell=opened('cells.png')
    envelope=clean(oldcell.crop((0,340,400,660)));envelope=tight(envelope,0);envelope=sized(envelope,200/envelope.width)
    dna=clean(oldcell.crop((800,0,1199,340)));dna=tight(dna,0);dna=sized(dna,130/dna.width)
    nucleus=envelope.copy();nucleus.alpha_composite(dna,((envelope.width-dna.width)//2,(envelope.height-dna.height)//2))
    for key,im in [('id:opening-dna',dna),('id:opening-nuclear-envelope',envelope),('id:opening-nucleus',nucleus)]:write(key,tight(im))
    layer=Image.new('RGBA',cell.size);layer.alpha_composite(nucleus,(223,110));slots['id:opening-cell']['id:opening-nucleus']=save(layer,'fitted-opening-nucleus')
    # Later slots remain illustrated, registered to the resized cell master.
    for key,wh,at in [('id:opening-mitochondria',(100,80),(425,200)),('id:school-sugar-carrier',(90,85),(490,110)),('id:school-ribosome',(70,65),(353,85))]:
        p=Image.open(root/icons[key]).convert('RGBA');p=p.crop(p.getbbox());p.thumbnail(wh,Image.Resampling.LANCZOS)
        lay=Image.new('RGBA',cell.size);lay.alpha_composite(p,at);slots['id:opening-cell'][key]=save(lay,'fitted-'+key[3:])
    registration['refresh-cell']={'master':'cell-volume.png','scale':scale,'outerMask':outer,'waterMask':waterpts,'lipidMask':[(350,738),(528,772),(768,761),(1026,700),(1056,823),(833,890),(571,919),(392,885)],'nucleusAt':[223,110],'sameSizeConstituents':True}
    # Hearing is additive: every occurrence reuses these exact transformed pixels.
    h=opened('hearing.png')
    def part(box,scale):return sized(tight(clean(h.crop(box)),0),scale)
    parts={
      'outer':(part((0,0,400,353),.70),(0,40)),
      'drum':(part((400,0,788,353),.34),(193,123)),
      'bones':(part((0,353,400,662),.34),(247,145)),
      'nerve':(part((0,967,400,1312),.46),(601,10)),
    }
    inner=clean(h.crop((400,662,788,967)))
    # Same inner-ear master supplies both coil and located enlargement. The
    # triangular locator is kept with the enlargement in every subsequent stage.
    coilmask=[(0,0),(206,0),(206,125),(174,151),(144,165),(174,181),(206,198),(206,305),(0,305)]
    coil=masked(inner,coilmask)
    hair=inner.copy();hair.putalpha(ImageChops.subtract(inner.getchannel('A'),coil.getchannel('A')))
    parts['coil']=(sized(coil,.90),(343,45));parts['hair']=(sized(hair,.90),(343,45))
    stages={
      'Outer ears and canals':['outer'],'Eardrums':['drum'],'Middle-ear bones':['bones'],
      'Outer ears with eardrums':['outer','drum'],'Sound-conducting ears':['outer','drum','bones'],
      'Coiled inner-ear chambers and fluid':['coil'],'Hearing cells with tiny hairs':['hair'],
      'Vibration-sensitive inner ears':['coil','hair'],
      'Sound-receiving ears':['outer','drum','bones','coil','hair'],
      'Hearing pathways':['nerve'],'Inner ears with hearing pathways':['coil','hair','nerve'],
      'Ears':['outer','drum','bones','coil','hair','nerve']}
    for name,keys in stages.items():
        c=Image.new('RGBA',(850,370))
        for k in keys:c.alpha_composite(*parts[k])
        write('name:'+name,tight(c))
    registration['refresh-hearing']={'master':'hearing.png','components':{k:{'size':list(v[0].size),'origin':list(v[1])} for k,v in parts.items()},'stages':stages,'coilMask':coilmask,'samePixelsAtEveryStage':True,'locatedEnlargementRetained':True}
    registration['refresh-arm']={'baseSource':'arm.png','canvas':[1560,3376],'complementarySplitX':716,'plateHeight':2340,'anatomyOnBackground':False}
    # Retained concise review aids: all four independently reachable states per arm.
    states=out/'states';states.mkdir(exist_ok=True)
    for side in ['front','back']:
        owner='id:arm-'+side+'-tendons';base=Image.open(root/icons[owner]).convert('RGBA')
        for state,keys in [('empty',[]),('mineral',['id:school-bone-mineral']),('muscle',['id:prelude-myoblasts']),('complete',['id:school-bone-mineral','id:prelude-myoblasts'])]:
            x=base.copy()
            for k in keys:x.alpha_composite(Image.open(root/slots[owner][k]).convert('RGBA'))
            x.save(states/(side+'-'+state+'.png'))
    c=cell.copy();c.alpha_composite(layer);c.save(states/'cell-with-nucleus.png')
    inventory=json.loads((root.parent/'checks/comparison-inventory.json').read_text())
    entries=[item for chapter in inventory.values() for item in chapter['items']]
    sheet=Image.new('RGB',(1400,((len(entries)+4)//5)*220),(246,232,209));d=ImageDraw.Draw(sheet)
    for n,item in enumerate(entries):
        art=Image.open(root/icons[item['id']]).convert('RGBA')
        if item['id'].startswith('id:arm-'):art=art.crop((0,0,1560,2340))
        art.thumbnail((260,180),Image.Resampling.LANCZOS);x=(n%5)*280;y=(n//5)*220
        sheet.paste(art,(x+(280-art.width)//2,y+(180-art.height)//2),art)
        d.text((x+8,y+190),item['name'],fill=(30,35,40))
    sheet.save(root/'contact-sheet.jpg',quality=90)

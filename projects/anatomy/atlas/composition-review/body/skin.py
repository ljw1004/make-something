"""Selected skin-family extraction; executed by produce.py with shared helpers."""
from PIL import ImageFilter

healthy = Image.open(ROOT / 'sources/skin-master.png').convert('RGBA')
skinbase = Image.open(ROOT / 'sources/skin-base.png').convert('RGBA')
unvascularized = Image.open(ROOT / 'sources/skin-unvascularized.png').convert('RGBA')
assert healthy.size == skinbase.size == unvascularized.size
skin_scale = 0.72

# Trace the actual wavy epidermis/dermis boundary from the selected painting.
boundary = [(65,388),(103,372),(139,372),(175,387),(209,403),(246,409),
            (289,400),(327,383),(363,371),(398,370),(437,386),(474,405),
            (512,409),(548,394),(585,376),(620,374),(657,389),(694,407),
            (733,409),(769,391),(804,374),(842,375),(878,392),(917,406),
            (956,400),(994,381),(1031,371),(1068,380),(1107,398),
            (1144,405),(1181,390),(1218,371),(1256,370),(1294,385),
            (1333,401),(1385,404)]
epidermis_polygon = [(0,0),(1448,0),(1448,410)] + list(reversed(boundary)) + [(0,388)]
epidermis = masked(skinbase, [epidermis_polygon])
cells = masked(unvascularized, [epidermis_polygon])
dermis_mask = ImageChops.invert(masked(Image.new('RGBA', healthy.size, (255,255,255,255)),
                                     [epidermis_polygon]).getchannel('A'))
def dermis(image):
    result=image.copy()
    result.putalpha(ImageChops.multiply(result.getchannel('A'),dermis_mask))
    return result
def skin_item(identity, filename, image, tight=True):
    if tight:
        bbox=image.getchannel('A').point(lambda a:255 if a>30 else 0).getbbox()
        image=image.crop(bbox)
    return save(filename,resize(image,skin_scale),identity)

skin_item('name:Outer skin cells','outer-skin-cells',cells)
skin_item('name:Water-resistant skin surface','water-resistant-skin-surface',epidermis)
skin_item('name:Supporting skin tissue','supporting-skin-tissue',dermis(unvascularized))
skin_item('name:Living deeper skin','living-deeper-skin',dermis(skinbase))
without_vessels=dermis(unvascularized)
without_vessels.alpha_composite(epidermis)
skin_item('name:Skin layers awaiting blood vessels','skin-layers-awaiting-blood-vessels',without_vessels,False)
skin_item('name:Skin segment','skin-segment',skinbase,False)

# Supplies are actual local vessel and lipid preparations; a sample represents
# the corresponding material throughout the section, as the brief permits.
vessel = skinbase.crop((520,719,810,776))
skin_item('name:Skin blood vessels','skin-blood-vessels',vessel)
lipids=epidermis.crop((290,126,745,188))
hsv=lipids.convert('HSV'); alpha=lipids.getchannel('A')
gold=Image.new('L',lipids.size)
gold.putdata([a if 17<=h<=50 and s>60 else 0 for (h,s,v),a in zip(hsv.getdata(),alpha.getdata())])
lipids.putalpha(gold)
skin_item('name:Lipids between skin cells','lipids-between-skin-cells',lipids)

# Gland contours and gold sensory branches are extracted from the complete
# painting; no synthetic anatomical strokes are added during registration.
gland_polygon=[(208,104),(235,108),(237,140),(230,280),(230,421),(212,621),
               (217,686),(265,704),(298,738),(313,797),(298,860),(265,902),
               (214,921),(165,912),(117,881),(107,831),(123,768),(162,727),
               (183,707),(183,632),(197,477),(208,350),(210,223)]
gland=masked(healthy,[gland_polygon])
nerve=masked(healthy,[[(730,410),(1380,410),(1390,988),(730,988)]])
hsv=nerve.convert('HSV'); alpha=nerve.getchannel('A')
gold=Image.new('L',nerve.size)
gold.putdata([a if 17<=h<=53 and s>55 else 0 for (h,s,v),a in zip(hsv.getdata(),alpha.getdata())])
gold=gold.filter(ImageFilter.MaxFilter(3))
nerve.putalpha(ImageChops.multiply(healthy.getchannel('A'),gold))
skin_item('name:Sweat gland and duct','sweat-gland-and-duct',gland)
skin_item('name:Sweat gland coil','sweat-gland-coil',gland.crop((90,692,330,940)))
skin_item('name:Sweat gland duct','sweat-gland-duct',gland.crop((180,100,245,718)))
skin_item('name:Skin nerve endings','skin-nerve-endings',nerve)
save('skin-gland-fitted',resize(gland,skin_scale))
save('skin-nerves-fitted',resize(nerve,skin_scale))
slots['name:Skin segment']={
    'name:Sweat gland and duct':PREFIX+'skin-gland-fitted.png',
    'name:Skin nerve endings':PREFIX+'skin-nerves-fitted.png',
}

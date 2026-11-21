"""Matched exterior cardiac family; only registration and anatomical selections.

All myocardial tissue and vessel connections are generated paintings. The common
peripheral pulmonary branches are selected from the whole master without repaint.
"""
from PIL import Image, ImageDraw, ImageChops, ImageFilter

def build(read, emit, mapping):
    whole=read('exterior-cardiac-master')
    size=whole.size
    def source(name):
        return read(name).resize(size, Image.Resampling.LANCZOS)
    def polygon(points):
        mask=Image.new('L',size); ImageDraw.Draw(mask).polygon(points,fill=255)
        return mask
    def selected(im,mask):
        result=im.copy();result.putalpha(ImageChops.multiply(im.getchannel('A'),mask));return result
    # The complete prepared pulmonary painting is shared literally. Separate
    # generated aorta and foreground heart selections establish normal depth:
    # arch posterior, pulmonary trunk anterior, atria/myocardium at its outlets.
    pulmonary=source('exterior-pulmonary')
    heart_mask=polygon([(300,700),(326,625),(367,587),(380,570),(380,418),(467,416),(467,550),(499,565),(550,610),(550,650),(652,650),(670,545),(701,515),(764,520),(810,558),(846,641),(884,726),(923,811),(931,921),(916,996),(887,1067),(848,1135),(805,1195),(758,1229),(708,1229),(585,1185),(474,1128),(454,1168),(338,1168),(338,1020),(308,900)])
    whole_heart=selected(whole,heart_mask)
    whole=source('exterior-aorta-matched')
    whole.alpha_composite(pulmonary)
    whole.alpha_composite(whole_heart)
    # Restrict the plain-surface twin to the convex myocardial surface. The
    # complete master retains every great vessel, outer edge and lateral window.
    surface=polygon([(333,752),(340,720),(390,700),(430,661),(480,651),(545,662),(625,651),(685,654),(729,658),(771,671),(809,696),(844,737),(866,796),(873,835),(851,845),(840,864),(840,906),(858,942),(893,949),(900,1006),(875,1086),(841,1149),(790,1195),(732,1210),(660,1189),(592,1153),(530,1111),(467,1064),(422,1016),(403,970),(405,927),(388,882),(365,849),(344,853),(331,809)])
    surface=surface.filter(ImageFilter.GaussianBlur(2))
    before=whole.copy();before.alpha_composite(selected(source('exterior-bare'),ImageChops.multiply(surface,heart_mask)))
    before.putalpha(whole.getchannel('A'))
    right_mask=polygon([(292,700),(328,623),(367,588),(381,570),(381,416),(467,416),(467,550),(511,574),(550,613),(548,648),(635,650),(697,698),(760,737),(807,800),(837,916),(827,1036),(786,1150),(732,1211),(635,1230),(510,1191),(450,1145),(455,1165),(335,1165),(335,1020),(300,900)])
    right=pulmonary.copy()
    right.alpha_composite(selected(source('exterior-right-route-section'),right_mask))
    emit('Right side of heart',source('exterior-right-section-input'),.62)
    emit('Left side of heart',source('exterior-left-section-input'),.62)
    emit('Lung blood-vessel network',pulmonary,.62)
    emit('Right heart and lung route',right,.62)
    emit('Left heart and body route',source('exterior-left-route-section'),.62)
    path=emit('Body vessel thoracic trunks',source('exterior-aorta-matched'),.62,key=False)
    mapping['presentations']['name:Body blood-vessel network']=[{'chapter':'full-a-pump-with-two-routes','path':path}]
    # Isolated preparations were framed larger by the painter. Restore the
    # master cardiac scale with one identical similarity transform for all three.
    def coronary(name):
        im=source(name); im=im.resize((round(size[0]*.55),round(size[1]*.55)),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',size);canvas.alpha_composite(im,(300,560));return canvas
    arteries=coronary('exterior-coronary-arteries')
    veins=coronary('exterior-coronary-veins')
    network=veins.copy();network.alpha_composite(arteries)
    emit('Arteries for the heart muscle',arteries,.62)
    emit('Heart-muscle capillaries and veins',veins,.62)
    emit('Heart-muscle vessel network',network,.62)
    emit('Heart and two routes',before,.62,False)
    emit('Heart with connected vessels',whole,.62,False)

"""Registered wound states and repair patches from a painted continuous family."""
sheet=Image.open(ROOT/'sources/wound-family.png').convert('RGBA')
wounds=[]
for index in range(6):
    col,row=index%3,index//3
    state=sheet.crop((col*512,row*512,(col+1)*512,(row+1)*512))
    bounds=state.getchannel('A').point(lambda a:255 if a>30 else 0).getbbox()
    # Match the healthy section's physical width and thickness, shared by all
    # six successive states. Transparent source gutters are not anatomy.
    wounds.append(state.crop(bounds).resize((950,620),Image.Resampling.LANCZOS))
# The builtin correction paints the same fibrin mesh through debris clearance
# and repair. Adopt only that local edit, preserving all accepted surrounding
# anatomy and every chapter25 state exactly.
clot_sheet=Image.open(ROOT/'sources/wound-clot-continuity.png').convert('RGBA')
for col,index in [(0,3),(1,4)]:
    correction=clot_sheet.crop((col*512,512,(col+1)*512,1024))
    bounds=correction.getchannel('A').point(lambda a:255 if a>30 else 0).getbbox()
    correction=correction.crop(bounds).resize((950,620),Image.Resampling.LANCZOS)
    region=Image.new('L',(950,620))
    ImageDraw.Draw(region).ellipse((401,440,534,515),fill=255)
    region=region.filter(ImageFilter.GaussianBlur(3))
    correction.putalpha(ImageChops.multiply(correction.getchannel('A'),region))
    wounds[index].alpha_composite(correction)
for index,identity,filename in [
    (0,'Skin with a cut','skin-with-a-cut'),
    (1,'Skin with a platelet plug','skin-with-a-platelet-plug'),
    (2,'Skin with a reinforced clot','skin-with-a-reinforced-clot'),
    (3,'Skin with a cleared wound','skin-with-a-cleared-wound'),
    (5,'Repaired skin segment','repaired-skin-segment'),
]:save(filename,wounds[index],'name:'+identity)

def repair_patch(polygon):
    region=Image.new('L',wounds[4].size)
    ImageDraw.Draw(region).polygon(polygon,fill=255)
    region=region.filter(ImageFilter.GaussianBlur(9))
    patch=wounds[4].copy()
    patch.putalpha(ImageChops.multiply(patch.getchannel('A'),region))
    # The clearing cells remain intact in all partial fittings. Their final
    # departure is shown by the mature repaired state, not a clipped mask edge.
    alpha=patch.getchannel('A');draw=ImageDraw.Draw(alpha)
    draw.ellipse((330,332,427,434),fill=0)
    draw.ellipse((521,335,621,434),fill=0)
    patch.putalpha(alpha)
    return patch

cell_patch=repair_patch([(370,0),(589,0),(585,222),(370,222)])
fibre_patch=repair_patch([(360,195),(595,195),(610,408),(350,408)])
vessel_patch=repair_patch([(305,388),(625,388),(630,512),(304,512)])
for name,filename,patch in [
    ('New skin cells','wound-cells-fitted',cell_patch),
    ('New supporting protein fibres','wound-fibres-fitted',fibre_patch),
    ('Capillary sprout','wound-sprout-fitted',vessel_patch),
]:
    save(filename,patch)
    slots.setdefault('name:Skin with a cleared wound',{})['name:'+name]=PREFIX+filename+'.png'

# The isolated growth has one attached end and one free distal tip. Fitting
# completes the distal junction, while the clot-bearing baseline stays broken.
growth=Image.open(ROOT/'sources/capillary-growth.png').convert('RGBA')
for identity,filename,box in [
    ('Nearby capillary','nearby-capillary',(0,0,800,growth.height)),
    ('Capillary sprout','capillary-sprout',(800,0,growth.width,growth.height)),
]:
    part=growth.crop(box)
    bounds=part.getchannel('A').point(lambda a:255 if a>30 else 0).getbbox()
    save(filename,resize(part.crop(bounds),0.29),'name:'+identity)
edge=healthy.crop((430,205,680,400))
skin_item("name:Skin cells at the cut's edge",'skin-cells-at-the-cut-s-edge',edge)

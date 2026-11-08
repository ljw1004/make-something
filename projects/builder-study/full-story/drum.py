"""A slit drum with insertable floor tabs and an explicitly folded underside."""
import math
from early_common import libraries, owned, show, inspection, entry

PLAN={};NAMES={}
def item(identity,name,parts,group=None,css=115,**kwargs):
    NAMES[identity]=name;PLAN[identity]=entry(parts,group or identity,css,**kwargs)
for identity,name,parts,css in [
 ('bf-film-wall','Drum wall',['wall-flat'],245),('bf-film-tape','Tape',['loose-tape'],95),
 ('bf-film-floor','Floor',['floor'],150),('bf-film-base','Base',['base'],150),
 ('bf-film-bearing','Turntable',['bearing'],115),('bf-film-strip','Picture strip',['strip-flat'],245)]:item(identity,name,parts,css=css)
item('bf-film-cut','Drum wall',['wall-cut'],group='film-paper',css=245)
item('bf-film-rolled','Drum',['wall-round'],group='film-shell',css=245)
item('bf-film-seamed','Drum',['wall-round','tape'],group='film-shell',css=245)
item('bf-film-under','Drum',['wall-round','tape'],group='film-under',css=245,under=True)
item('bf-film-prepared','Drum',['wall-round','tape'],group='film-under',css=245,under=True,tabs='insertable')
item('bf-film-seated','Drum',['wall-round','tape','floor'],group='film-under',css=245,under=True,tabs='insertable')
item('bf-film-shell','Drum',['wall-round','tape','floor'],group='film-under',css=245,under=True,tabs='folded')
item('bf-film-turntable','Base',['base','bearing'],css=185)
item('bf-film-mounted-under','Drum',['wall-round','tape','floor','base','bearing'],group='film-under',css=245,under=True,tabs='folded')
item('bf-film-standing','Drum',['wall-round','tape','floor','base','bearing'],group='film-standing',css=245,tabs='folded')
item('bf-film-loop','Picture ring',['strip-round'],css=220)
item('animation-drum','Animation drum',['wall-round','tape','floor','base','bearing','strip-round'],css=350,tabs='folded')
CHAPTERS=[dict(id='bf-film-build',title='A slit drum',reference='animation-drum',processes={'bf-film-cut-process':'cut','bf-film-roll-process':'roll'},steps=[
 ('bf-film-wall','bf-film-cut-process','bf-film-cut','Cut the marked viewing slits'),
 ('bf-film-cut','bf-film-roll-process','bf-film-rolled','Roll the Drum wall'),
 ('bf-film-rolled','bf-film-tape','bf-film-seamed','Tape the seam')]),
dict(id='bf-film-floor-build',title='A turning drum',reference='animation-drum',processes={'bf-film-flip-process':'flip','bf-film-fold-process':'fold'},steps=[
 ('bf-film-seamed','bf-film-flip-process','bf-film-under','Flip the Drum over'),
 ('bf-film-under','bf-film-fold-process','bf-film-prepared','Fold the scored tabs inward'),
 ('bf-film-prepared','bf-film-floor','bf-film-seated','Slide the Floor over the straight tips'),
 ('bf-film-seated','bf-film-fold-process','bf-film-shell','Fold the tabs under the Floor'),
 ('bf-film-base','bf-film-bearing','bf-film-turntable','Fit the Turntable to the Base'),
 ('bf-film-shell','bf-film-turntable','bf-film-mounted-under','Fit the Base beneath the Drum'),
 ('bf-film-mounted-under','bf-film-flip-process','bf-film-standing','Flip the Drum upright')]),
dict(id='bf-film-pictures',title='A tiny picture show',reference='animation-drum',processes={'bf-film-picture-roll':'roll'},steps=[
 ('bf-film-strip','bf-film-picture-roll','bf-film-loop','Roll the Picture strip'),
 ('bf-film-standing','bf-film-loop','animation-drum','Fit the Picture ring inside the Drum')])]
DESCRIPTIONS={
 'bf-film-wall':'One card strip with twelve marked slots and scored floor tabs. Their tips stay straight until the floor is seated. Cut down to the stopping line; the lower band stays continuous.',
 'bf-film-floor':'A 178.8 mm disc, smaller than the wall opening, with twelve slots for the straight tabs. Fold the tips underneath only after inserting it.',
 'bf-film-bearing':'One retained spindle, sleeve bearing and platform. The spindle stays fixed in the base while the platform turns.',
 'bf-film-strip':'A printed sequence of twelve fish pictures, one per viewing slit, with a prepared adhesive overlap. The pictures face inward when rolled.',
 'animation-drum':'Looking through the slits gives brief separated glimpses of successive pictures, with darkness between them.',
}

def build():
    S=libraries()
    import picture_drum as source
    from early_geometry import bore_frame,cut_frame
    root=S.empty('canonical picture drum with explicit paper poses')
    parts={};all_source={}
    cases=[('film-wall',{'wall-flat':'film-wall'}),('film-slotted',{'wall-cut':'film-wall'}),
           ('film-cylinder',{'wall-round':'film-wall','tape':'film-joining-tape'}),
           ('film-coloured-strip',{'strip-flat':'film-blank-strip'}),
           ('animation-drum',{'strip-round':'film-blank-strip','floor':'film-floor','base':'film-base','bearing':'film-bearing'}),
           ('film-joining-tape',{'loose-tape':'film-joining-tape'})]
    for index,(state,mapping) in enumerate(cases):
        instance=source.build_model();instance['root'].parent=root;source.set_state(instance,state)
        for key,source_key in mapping.items():parts[key]=list(instance['parts'][source_key])
        for key,objects in instance['parts'].items():all_source[str(index)+'-'+key]=list(objects)
    # A new floor has actual side clearance inside the 179.5 mm wall opening.
    floor=S.cylinder('178.8 mm tab-slotted drum floor',(0,0,.040),.0894,.006,'birch','Z')
    floor.parent=root
    bore_frame(S,floor,root,(0,0,.0355),.010,.012)
    for i in range(source.FRAMES):
        angle=(i+.5)*math.tau/source.FRAMES
        cutter=S.box('prepared straight-tab receiving slot',(.087*math.sin(angle),-.087*math.cos(angle),.040),(.0044,.0012,.012),'ink')
        cutter.rotation_euler.z=angle;cut_frame(floor,cutter,root)
    parts['floor']=[floor]
    # Raising the wall by its half-thickness puts the folded top tab surfaces
    # against the floor top, with the final hooks against the underside.
    for key in ('wall-flat','wall-cut','wall-round','tape'):
        for obj in parts[key]:obj.location.z+=.00025
    # The picture ring rests on the twelve upper tab surfaces at 43.5 mm.
    # The tabs stand 0.5 mm above the floor; lowering the ring to the wood
    # would make it penetrate those real card supports.
    for key in ('strip-flat','strip-round'):
        for obj in parts[key]:obj.location.z-=.0005
    tabs=[o for o in parts['wall-round'] if o.name.startswith('folded retaining floor tab')]
    tab_angles=[math.atan2((o.data.vertices[0].co.x+o.data.vertices[1].co.x)/2,
                           -(o.data.vertices[0].co.y+o.data.vertices[1].co.y)/2) for o in tabs]
    model={'root':root,'parts':all_source,'source':source,'tabs':list(zip(tabs,tab_angles))}
    return owned(model,parts)

def stage(m,identity):
    info=PLAN[identity]
    m['root'].rotation_euler=(math.pi if info.get('under') else 0,0,0)
    for obj,angle in m['tabs']:
        if info.get('tabs') in {'insertable','folded'}:
            path=[(.090,.043),(.087,.043),(.087,.0365),(.083,.0365) if info.get('tabs')=='folded' else (.087,.0325)]
        else:
            path=[(.090,.043),(.090,.040),(.090,.0335),(.090,.0295)]
        for row,(radius,z) in enumerate(path):
            for side,d in enumerate((-.002,.002)):
                obj.data.vertices[row*2+side].co=(radius*math.sin(angle)+d*math.cos(angle),-radius*math.cos(angle)+d*math.sin(angle),z)
        obj.data.update()
    show(m,info['parts'])
    if info['group']=='film-paper':return {'location':(.02,-1.,.30),'target':(0,0,.08),'scale':.65}
    if info['group'] in {'film-shell','film-standing'}:return {'location':(.40,-.70,.48),'target':(0,0,.075),'scale':.245}
    if info['group']=='film-under':return {'location':(.40,-.70,.48),'target':(0,0,-.075),'scale':.255}
    return inspection(m,info['parts'],direction=(.40,-.70,.48),margin=1.23)

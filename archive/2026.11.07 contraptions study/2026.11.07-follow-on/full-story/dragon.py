"""One eccentric cam, two separate bearings, wings and fixed-length links."""
import math
from dataclasses import replace
from early_common import libraries, owned, show, inspection, entry, descendants

PLAN={};NAMES={}
def item(identity,name,parts,group=None,css=105):
    NAMES[identity]=name;PLAN[identity]=entry(parts,group or identity,css)
supplies=[('base','Base'),('front-bearing','Front bearing'),('rear-bearing','Rear bearing'),('shaft','Shaft'),
          ('front-collar','Front collar'),('rear-collar','Rear collar'),
          ('cam','Cam'),('handle','Crank'),('crank-clip','Crank clip'),('guide','Guide'),('follower','Follower'),('cover','Cover'),
          ('spring','Spring'),('body','Body'),('left-wing','Left wing'),('right-wing','Right wing'),('tail','Tail'),
          ('left-link','Left link'),('right-link','Right link')]
for key,name in supplies:item('bf-cd-'+key,name,[key],css=160 if key in {'body','base'} else 105)
PLAN['bf-cd-shaft'].update(group='cd-crank',css=240)
PLAN['bf-cd-body'].update(group='cd-body',css=240)
PLAN['bf-cd-guide'].update(group='cd-follower',css=180)
CHAPTERS=[]
def chain(cid,title,initial,parts,rows,group):
    steps=[];state=list(parts);current=initial
    for reagent,result,goal,added in rows:
        state+=added;item(result,'Dragon' if result=='crank-dragon' else ('Frame' if group=='cd-crank' else 'Lifter' if group=='cd-lifter' else 'Dragon'),state,
                            group=result if result=='crank-dragon' else group,css=350 if result=='crank-dragon' else 240)
        steps.append((current,reagent,result,goal));current=result
    CHAPTERS.append(dict(id=cid,title=title,steps=steps,reference='crank-dragon'))
    return current,state

crank,crank_parts=chain('bf-cd-crank','Round and round','bf-cd-shaft',['shaft'],[
 ('bf-cd-cam','bf-cd-cammed','Slide the Cam onto the Shaft',['cam']),
 ('bf-cd-front-bearing','bf-cd-bearing-1','Fit the Front bearing',['front-bearing']),
 ('bf-cd-rear-bearing','bf-cd-bearings','Fit the Rear bearing',['rear-bearing']),
 ('bf-cd-front-collar','bf-cd-front-retained','Fit the Front collar',['front-collar']),
 ('bf-cd-flip','bf-cd-rear-facing','Flip to the back of the bearings',[]),
 ('bf-cd-rear-collar','bf-cd-retained-rear','Fit the Rear collar',['rear-collar']),
 ('bf-cd-flip','bf-cd-retained','Flip back to the front',[]),
 ('bf-cd-handle','bf-cd-cranked','Fit the Crank',['handle']),
 ('bf-cd-crank-clip','bf-cd-clipped','Secure the Crank with its clip',['crank-clip'])],'cd-crank')
CHAPTERS[0]['processes']={'bf-cd-flip':'flip'}
CHAPTERS[0]['reference']='bf-cd-clipped'
NAMES['bf-cd-clipped']='Crank'
for identity in ('bf-cd-rear-facing','bf-cd-retained-rear'):PLAN[identity]['group']='cd-crank-rear'
# The crank's small collars and clip are worked on before the broad base or
# tall follower enters the picture. On the next page it becomes an incoming
# subassembly; the base is the stationary recipient at the lifter's scale.
item('bf-cd-crank-carried','Crank',crank_parts,group='cd-crank-carried',css=165)
PLAN['bf-cd-base'].update(group='cd-lifter',css=240)
frame='bf-cd-frame';mechanism=crank_parts+['base']
item(frame,'Frame',mechanism,group='cd-lifter',css=240)
item('bf-cd-open-follower','Follower',['guide','follower'],group='cd-follower',css=180)
item('bf-cd-guided','Follower',['guide','follower','cover'],group='cd-follower',css=180)
item('bf-cd-mounted','Lifter',mechanism+['guide','follower','cover'],group='cd-lifter',css=240)
item('bf-cd-lifter','Lifter',mechanism+['guide','follower','cover','spring'],group='cd-lifter',css=240)
CHAPTERS.append(dict(id='bf-cd-lift',title='Round becomes up',reference='crank-dragon',steps=[
 ('bf-cd-base',crank,frame,'Mount the Crank on the Base'),
 ('bf-cd-guide','bf-cd-follower','bf-cd-open-follower','Slide the Follower into the Guide'),
 ('bf-cd-open-follower','bf-cd-cover','bf-cd-guided','Snap on the Cover'),
 (frame,'bf-cd-guided','bf-cd-mounted','Mount the Follower above the Cam'),
 ('bf-cd-mounted','bf-cd-spring','bf-cd-lifter','Hook on the Spring')]))
item('bf-cd-body-left','Body',['body','left-wing'],group='cd-body',css=240)
item('bf-cd-winged','Body',['body','left-wing','right-wing'],group='cd-body',css=240)
item('bf-cd-winged-rear','Body',['body','left-wing','right-wing'],group='cd-body-rear',css=240)
item('bf-cd-bodied-rear','Body',['body','left-wing','right-wing','tail'],group='cd-body-rear',css=240)
item('bf-cd-bodied','Dragon',['body','left-wing','right-wing','tail'],group='cd-body',css=240)
complete=mechanism+['guide','follower','cover','spring','body','left-wing','right-wing','tail']
item('bf-cd-mounted-body','Dragon',complete,group='cd-whole',css=250)
item('bf-cd-linked-left','Dragon',complete+['left-link'],group='cd-whole',css=250)
item('crank-dragon','Crank dragon',complete+['left-link','right-link'],css=350)
CHAPTERS.append(dict(id='bf-cd-dragon',title='The dragon',reference='crank-dragon',processes={'bf-cd-body-flip':'flip'},steps=[
 ('bf-cd-body','bf-cd-left-wing','bf-cd-body-left','Attach the Left wing'),
 ('bf-cd-body-left','bf-cd-right-wing','bf-cd-winged','Attach the Right wing'),
 ('bf-cd-winged','bf-cd-body-flip','bf-cd-winged-rear','Flip the Body to its back'),
 ('bf-cd-winged-rear','bf-cd-tail','bf-cd-bodied-rear','Attach the Tail'),
 ('bf-cd-bodied-rear','bf-cd-body-flip','bf-cd-bodied','Flip the Body to its front'),
 ('bf-cd-lifter','bf-cd-bodied','bf-cd-mounted-body','Mount the Dragon on the Lifter'),
 ('bf-cd-mounted-body','bf-cd-left-link','bf-cd-linked-left','Fit the Left link'),
 ('bf-cd-linked-left','bf-cd-right-link','crank-dragon','Fit the Right link')]))
DESCRIPTIONS={
 'bf-cd-cam':'The shaft hole sits off centre. Turning the round disc raises and lowers the broad follower foot.',
 'bf-cd-guide':'An open square channel with a mounting foot and spring anchor. The separate cover closes around the follower; its broad foot never has to pass through the narrow channel.',
 'bf-cd-follower':'A sliding rod with a broad cam foot, spring collar and retained crosshead pin for two independently pivoting links.',
 'bf-cd-shaft':'A plain six-millimetre shaft, supplied without its collars. The cam and bearings slide on before the separate collars retain the shaft.',
 'bf-cd-handle':'A D-shaped socket fits the matching shaft end. Its separate retaining clip enters the aligned cross holes after the crank is fitted.',
 'bf-cd-crank-clip':'One spring-wire clip. Its straight leg passes through the aligned crank and shaft holes; the curved leg grips outside the socket.',
 'bf-cd-left-wing':'One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.',
 'bf-cd-right-wing':'One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.',
 'bf-cd-tail':'The tail carries a split snap pin. Its tapered tip passes through the body hole before its flexible barbs reopen.',
 'bf-cd-left-link':'One rigid 55 mm polymer link with two open snap eyes. Fit both eyes sideways over the exposed pin necks; their heads stay in place.',
 'bf-cd-right-link':'One rigid 55 mm polymer link with two open snap eyes. It pivots independently beside the other link.',
}


def set_open_spring(model,z0,z1):
    """One continuous wire: two side-entry C hooks, leads and the same helix.

    Both 120-degree mouths face +x. The spring approaches the two headed
    1.6 mm pin necks from the left, in the free plane behind their heads.
    The lower closed arc carries upward tension; the upper arc carries
    downward tension. Neither free tip is welded to its outgoing lead.
    """
    radius=.00145;wire=model['dimensions'].spring_wire_radius
    x,y=.014,-.0145;end_z=radius*math.sqrt(3)/2
    def hook(z):
        return [(x+radius*math.cos(-math.pi/3-4*math.pi*i/(3*48)),y,
                 z+radius*math.sin(-math.pi/3-4*math.pi*i/(3*48))) for i in range(49)]
    points=hook(z0)
    # Keep both leads outside the hook arcs and above/below the mouth.
    # A straight lead back across an arc would create a false self-contact.
    lead_x=x+.0024
    points += [(lead_x,y,z0+end_z),(lead_x,y,z0+.004),(x,y,z0+.004)]
    turns=8;steps=128;coil_span=z1-z0-.008
    free_coil_span=model['dimensions'].spring_free_span-.008
    wire_length=math.hypot(2*math.pi*turns*.0025,free_coil_span)
    coil_radius=math.sqrt(wire_length**2-coil_span**2)/(2*math.pi*turns)
    coil_start=len(points)
    for i in range(steps+1):
        t=i/steps;angle=2*math.pi*turns*t
        points.append((x+coil_radius*math.sin(angle),-.010+coil_radius*math.cos(angle),z0+.004+coil_span*t))
    coil_end=len(points)
    points += [(x,y,z1-.004),(lead_x,y,z1-.004),(lead_x,y,z1-end_z)]
    top_start=len(points);points+=hook(z1)
    curve=model['spring'].data;curve.splines.clear();spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
    for vertex,co in zip(spline.points,points):vertex.co=(*co,1)
    model['spring_geometry']={'lower_hook':(0,49),'coil':(coil_start,coil_end),
                              'upper_hook':(top_start,len(points)),
                              'mouth_free_width':2*end_z-2*wire,
                              'coil_centreline_length':wire_length,'span':z1-z0}


class OpenSpringSource:
    """Keep canonical rigid motion; replace only its closed-eye spring path."""
    def __init__(self,source):self.source=source
    def __getattr__(self,name):return getattr(self.source,name)
    def apply_pose(self,model,theta,follower_height=None,*,relaxed_spring=False):
        pose=self.source.apply_pose(model,theta,follower_height)
        d=model['dimensions'];top=d.spring_fixed_z+d.spring_free_span if relaxed_spring else pose['foot_z']+d.spring_collar_above_foot
        set_open_spring(model,d.spring_fixed_z,top)
        return pose


def build():
    S=libraries()
    import cam_dragon as source
    from early_geometry import bore_frame,slot_frame,split_barb
    from construction import surface
    # Retain the accepted 0.7 mm wire, original hook centres, helix length
    # and moving anchors. The canonical dark matte finish reads on white.
    m=source.build_model('eccentric',d=replace(source.DIMS,spring_wire_radius=.00035),include_handle=True)
    m['spring'].data.use_fill_caps=True
    old=m['parts'];parts={k:[] for k,_ in supplies}
    for obj in old['cd-base']:
        if obj.name.startswith('birch base'):parts['base'].append(obj)
        elif obj.name.startswith('body-tab'):parts['body'].append(obj)
    for obj in old['cd-bearing-frames']:
        if obj.name.startswith(('bearing frame rear collar cradle','bearing frame collar axial stop')):continue
        parts['front-bearing' if obj.location.y<0 else 'rear-bearing'].append(obj)
    parts['shaft']=[o for o in old['cd-shaft'] if o.name.startswith('straight 6')]
    parts['front-collar']=[o for o in old['cd-shaft'] if o.get('service_role')=='front_collar']
    parts['rear-collar']=[o for o in old['cd-shaft'] if o.get('service_role')=='rear_collar']
    parts['cam']=list(old['cd-cam'])
    for obj in old['cd-crank-key']:
        parts['crank-clip' if obj.name.startswith('crank retaining clip') else 'handle'].append(obj)
    for obj in old['cd-guide']:
        if obj.name.startswith(('guide keeper','guide service')):continue
        parts['cover' if descendants(obj,m['guide_cover']) else 'guide'].append(obj)
    parts['follower']=list(old['cd-follower']);parts['spring']=list(old['cd-return-spring'])
    for obj in old['cd-cutouts']:
        if obj.name.startswith('fixed decorative'):key='tail'
        elif descendants(obj,m['wings']['left']):key='left-wing'
        elif descendants(obj,m['wings']['right']):key='right-wing'
        else:key='body'
        parts[key].append(obj)
    for obj in old['cd-hinge-pins']:
        if 'hinge cap rear' in obj.name or obj.name.startswith('tail attachment broad head'):continue
        key='tail' if obj.name.startswith('tail attachment') else 'left-wing' if obj.name.startswith('left') else 'right-wing'
        parts[key].append(obj)
    # Wing pins enter from the wing side. The flexible split tips replace the
    # former 6 mm rigid rear heads, which could not pass a 3.4 mm body eye.
    for side,sign in [('left',-1),('right',1)]:
        pin=next(o for o in parts[side+'-wing'] if o.name.startswith(side+' fixed wing hinge pin'))
        slot_frame(S,pin,m['static'],(sign*source.DIMS.hinge_x,.030,source.DIMS.hinge_z),(.0012,.010,.008))
        surface(pin,S.material('teal'))
        parts[side+'-wing'].append(split_barb(S,side+' compliant hinge barb',m['static'],sign*source.DIMS.hinge_x,
                                             source.DIMS.hinge_z,.0318,.0348))
    # The tail enters from behind, so its fixed head stays behind the tail and
    # its split tip points forwards through the body.
    tail_pin=next(o for o in parts['tail'] if o.name=='tail attachment pin')
    slot_frame(S,tail_pin,m['static'],(.040,.0295,.191),(.0012,.008,.008))
    surface(tail_pin,S.material('teal'))
    parts['tail'].append(split_barb(S,'tail compliant forward barb',m['static'],.040,.191,.0282,.0252))
    for obj in old['cd-linkage']:
        if obj.name.startswith(('shared pin','follower pin','follower-eye','independent rod-eye')):key='follower'
        elif 'wing drive pin' in obj.name or 'drive spacer' in obj.name:key='left-wing' if obj.name.startswith('left') else 'right-wing'
        else:key='left-link' if obj.name.startswith('left') else 'right-link'
        parts[key].append(obj)
    # Both eyes snap sideways over 3 mm pin necks; the 2.8 mm mouths flex by
    # 0.1 mm per side. Pivot centres and rigid 55 mm link lengths are unchanged.
    for side in ('left','right'):
        for obj in parts[side+'-link']:
            for z in (0,source.DIMS.rod_length):
                slot_frame(S,obj,m['rods'][side],(.004,0,z),(.008,.012,.0028))
            surface(obj,S.material('teal'))
    base=parts['base'][0]
    # Actual receivers for every retained mounting screw. The original four
    # corner holes remain available for later mounting the completed dragon.
    for y in (-source.DIMS.bearing_y,source.DIMS.bearing_y):
        for x in (-.015,.015):bore_frame(S,base,m['static'],(x,y-.008,.006),.0016,.020)
    for x in (-.036,-.016):bore_frame(S,base,m['static'],(x,.020,.006),.0016,.020)
    for x in (-.054,.054):bore_frame(S,base,m['static'],(x,.020,.006),.0016,.020)
    m['source']=OpenSpringSource(source)
    return owned(m,parts)

def stage(m,identity):
    info=PLAN[identity];m['handle_state']='fitted';m['source'].apply_pose(m,.6,relaxed_spring=identity=='bf-cd-spring');m['source'].set_guide_cover(m,False)
    show(m,info['parts'])
    group=info['group']
    if group=='cd-crank':return {'location':(.55,-.85,.48),'target':(0,0,.06),'scale':.24}
    if group=='cd-crank-rear':return {'location':(-.55,.85,.52),'target':(0,0,.10),'scale':.34}
    if group=='cd-lifter':return {'location':(.55,-.85,.52),'target':(0,0,.10),'scale':.34}
    if group=='cd-body':return {'location':(.55,-.83,.59),'target':(0,.02,.17),'scale':.40}
    if group=='cd-body-rear':return {'location':(-.55,.87,.59),'target':(0,.02,.17),'scale':.40}
    if group=='cd-follower':return {'location':(.55,-.85,.53),'target':(0,0,.110),'scale':.29}
    if group=='cd-whole' or identity=='crank-dragon':return {'location':(.55,-.85,.57),'target':(0,0,.150),'scale':.42}
    if identity=='bf-cd-tail':direction=(-.55,.85,.42)
    elif identity=='bf-cd-rear-collar':direction=(-.55,.85,.42)
    elif identity in {'bf-cd-body','bf-cd-left-wing','bf-cd-right-wing'}:direction=(.55,-.85,.42)
    elif identity in {'bf-cd-guide','bf-cd-follower','bf-cd-cover','bf-cd-open-follower','bf-cd-guided','bf-cd-spring'}:direction=(.55,-.85,.42)
    else:direction=(.55,-.85,.42)
    return inspection(m,info['parts'],direction=direction,margin=1.22)


def write():
    """Generate this family's chapter-dependent carried crank illustration."""
    from pathlib import Path
    from types import SimpleNamespace
    from early_common import write_fragment as write_early_fragment
    write_early_fragment(SimpleNamespace(__name__='dragon',CHAPTERS=CHAPTERS,
                                        NAMES=NAMES,DESCRIPTIONS=DESCRIPTIONS))
    path=Path(__file__).with_suffix('.md');text=path.read_text()
    primary='  - icon: ![Crank](assets/items/bf-cd-clipped.webp)\n'
    carried='  - from chapter `bf-cd-lift` icon: ![Crank](assets/items/bf-cd-crank-carried.webp)\n'
    text=text.replace(primary,primary+carried,1)
    path.write_text(text.rstrip()+'\n')


if __name__=='__main__':write()

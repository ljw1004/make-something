"""A level pinball tray, literal rails/paddles/arches and real underside work."""
import math
from dataclasses import replace
from early_common import libraries, owned, show, inspection, entry

PLAN = {}
NAMES = {}
def item(identity, name, parts, group=None, css=105, **kw):
    NAMES[identity] = name
    PLAN[identity] = entry(parts, group or identity, css, **kw)
    return identity

supplies = [('tray','Tray'),('left-rail','Left rail'),('right-rail','Right rail'),('top-rail','Top rail'),
            ('lane','Lane rail'),('left-lip','Left return'),('right-lip','Right return'),('cup','Marble cup'),
            ('plate','Pivot plate'),('support','Support'),('left-paddle','Left paddle'),('right-paddle','Right paddle'),
            ('barrel','Launcher cradle'),('rod','Plunger rod'),('tip','Plunger tip'),('cover','Launcher cover'),('spring','Spring'),('arch-low','Lower arch'),('arch-mid','Middle arch'),
            ('arch-high','Upper arch'),('score','Score wheel'),('marble','Marble')]
for key, name in supplies: item('bf-pb-'+key, name, [key], css=220 if key=='tray' else 105)
PLAN['bf-pb-tray'].update(group='pb-rails',css=245,pose='top')
PLAN['bf-pb-rod'].update(group='pb-launcher-build',css=190)

CHAPTERS=[]
state=['tray']; current='bf-pb-tray'
def chapter(cid,title,rows,group,processes=None):
    global current,state
    steps=[]
    for key,result,goal in rows:
        if key.startswith('process:'):
            reagent=key[8:]; pose='under' if result.endswith('under') else 'top'
        else:
            reagent='bf-pb-'+key;state=state+[key];pose='under' if group=='pb-underside' else 'top'
        item(result,'Table',state,group=group if pose=='under' else ('pb-top' if 'upright' in result or group=='pb-underside' else group),css=245,pose=pose)
        steps.append((current,reagent,result,goal));current=result
    CHAPTERS.append(dict(id=cid,title=title,steps=steps,reference='pinball-table',processes=processes or {}))

chapter('bf-pb-rails','A marble table',[
 ('left-rail','bf-pb-rail-1','Fit the Left rail'),('right-rail','bf-pb-rail-2','Fit the Right rail'),
 ('top-rail','bf-pb-rail-3','Fit the Top rail'),('lane','bf-pb-rail-4','Fit the Lane rail'),
 ('left-lip','bf-pb-rail-5','Fit the Left return'),('right-lip','bf-pb-rail-6','Fit the Right return'),
 ('cup','bf-pb-rimmed','Fit the Marble cup')],'pb-rails')
chapter('bf-pb-flippers','Two flippers',[
 ('process:bf-pb-flip','bf-pb-under','Flip the Table'),('plate','bf-pb-plated-under','Fit the Pivot plate'),
 ('support','bf-pb-supported-under','Fit the Support'),('process:bf-pb-flip','bf-pb-upright','Flip the Table upright'),
 ('left-paddle','bf-pb-left','Snap on the Left paddle'),('right-paddle','bf-pb-flipped','Snap on the Right paddle')],
 'pb-underside',{'bf-pb-flip':'flip'})
# Paddles are fitted above the tray after its deliberate flip.
for identity in ('bf-pb-left','bf-pb-flipped'):
    PLAN[identity].update(group='pb-top',pose='top')
launcher_parts=['rod','spring','tip','barrel','cover']
item('bf-pb-sprung-rod','Plunger',['rod','spring'],group='pb-launcher-build',css=190)
item('bf-pb-tipped','Plunger',['rod','spring','tip'],group='pb-launcher-build',css=190)
item('bf-pb-open-launcher','Launcher',['rod','spring','tip','barrel'],group='pb-launcher-build',css=190)
item('bf-pb-launcher','Launcher',launcher_parts,group='pb-launcher-build',css=190)
third=[('bf-pb-rod','bf-pb-spring','bf-pb-sprung-rod','Slide the Spring onto the Plunger rod'),
       ('bf-pb-sprung-rod','bf-pb-tip','bf-pb-tipped','Fit the Plunger tip'),
       ('bf-pb-tipped','bf-pb-barrel','bf-pb-open-launcher','Lower the Plunger into the Launcher cradle'),
       ('bf-pb-open-launcher','bf-pb-cover','bf-pb-launcher','Clip on the Launcher cover')]
state+=launcher_parts
item('bf-pb-launched','Table',state,group='pb-targets',css=245,pose='top')
third.append((current,'bf-pb-launcher','bf-pb-launched','Fit the Launcher to the Table'));current='bf-pb-launched'
CHAPTERS.append(dict(id='bf-pb-launcher-build',title='A spring launcher',steps=third,reference='pinball-table'))
third=[]
for key,result,goal in [('arch-low','bf-pb-target-1','Fit the Lower arch'),
                       ('arch-mid','bf-pb-target-2','Fit the Middle arch'),('arch-high','bf-pb-target-3','Fit the Upper arch'),
                       ('score','bf-pb-scored','Fit the Score wheel'),('marble','pinball-table','Set the Marble on the Table')]:
    if key=='score':
        item('bf-pb-score-facing','Table',state,group='pb-score-work',css=245,pose='top')
        third.append((current,'bf-pb-score-flip','bf-pb-score-facing','Turn the Table toward the Score wheel'))
        current='bf-pb-score-facing'
    reagent='bf-pb-'+key
    state += [key]
    item(result,'Pinball table' if result=='pinball-table' else 'Table',state,group=('pb-score-work' if key=='score' else 'pb-targets') if result!='pinball-table' else result,css=350 if result=='pinball-table' else 245,pose='top')
    third.append((current,reagent,result,goal));current=result
CHAPTERS.append(dict(id='bf-pb-targets',title='One more go',steps=third,reference='pinball-table',processes={'bf-pb-score-flip':'flip'}))
# The existing upright Flip starts a high working view. Keep its scale and
# direction through both paddles, launcher and arches, until the score Flip.
for info in PLAN.values():
    if info['group'] in {'pb-top','pb-targets'}:info['css']=300
DESCRIPTIONS={
 'bf-pb-tray':'Prepared plywood with rail slots, flipper holes and integral carrying handles.',
 'bf-pb-plate':'A plate with retained spindles, finger buttons and return loops. The shoulders pass through the prepared tray clearances. Captive screws enter the tray’s threaded receivers from beneath.',
 'bf-pb-left-paddle':'One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.',
 'bf-pb-right-paddle':'One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.',
 'bf-pb-rod':'A six-millimetre plunger rod with a fitted pull handle and an open front end for threading the spring.',
 'bf-pb-tip':'A soft striking tip and piston with a blind gripping socket for the rod.',
 'bf-pb-barrel':'An open-topped cradle with half-round end guides, mounting feet and a travel stop. The assembled plunger lowers through its open top.',
 'bf-pb-cover':'A clear upper shell with matching half-guides and flexible retaining clips. Closing it captures the plunger and encloses the spring.',
 'bf-pb-support':'One connected U-shaped support with locating tongues and retaining clips. It slopes the table towards its marble cup without tilting sideways.',
}

def build():
    S=libraries()
    import pinball_table as source
    from construction import special_material, surface
    from early_geometry import bore_frame,slot_frame,half_tube
    from early_common import descendants
    original=source.terrain;original_profile=source._xy;original_box=S.box
    active_rail=None
    rail_names={'left retaining rail','right retaining rail','curved top rail',
                'launch-lane divider','left curved inward return lip','right inward return lip'}
    def prepared_profile(name,points,*args,**kwargs):
        nonlocal active_rail
        active_rail=name if name in rail_names else None
        if name in {'left retaining rail','right retaining rail'}:
            # Separate butt joints: the curved top's end face reaches down
            # to y=229.53 mm, and the left return starts at y=-183.53 mm.
            low=-.183 if name=='left retaining rail' else -.260
            points=[(x,min(.2292,max(low,y))) for x,y in points]
        return original_profile(name,points,*args,**kwargs)
    def prepared_box(name,centre,*args,**kwargs):
        rail=active_rail if name=='receiving rail mortise' else next((r for r in rail_names if name==r+' integral push-fit foot'),None)
        x,y,z=centre
        # Relocate each integral foot AND its prepared mortise together.
        # Adjacent rails must never supply duplicate pegs for one socket.
        if rail in {'left retaining rail','right retaining rail'} and abs(y-.230)<1e-8:y=.215
        elif rail=='left retaining rail' and abs(y+.260)<1e-8:y=-.170
        elif rail=='curved top rail' and abs(y-.230)<1e-8:
            x=math.copysign(.185*math.cos(math.pi/8),x);y=.230+.062*math.sin(math.pi/8)
        elif rail=='left curved inward return lip' and abs(x+.060)<1e-8:
            x,y=-.0785,-.2845
        elif rail=='right inward return lip' and abs(x-.065)<1e-8:
            x,y=.090,-.287+.017*.025/.065
        elif rail=='right inward return lip' and abs(x-.029)<1e-8:
            x,y=.073,-.287+.017*.008/.065
        elif name=='apron mortise':
            # Match the actual 22 mm bridges centred at -290 mm. These
            # 22.3 mm channels remain open through the front tray edge.
            y=-.290
        elif name=='catch apron side rim' and x<0:
            # End this rim after the curved return; neither adjoining part
            # may occupy the other's material at the cup entrance.
            size,*rest=args
            return original_box(name,(x,-.327,z),(size[0],.058,size[2]),*rest,**kwargs)
        return original_box(name,(x,y,z),*args,**kwargs)
    source.terrain=lambda x,y:0.
    source._xy=prepared_profile;S.box=prepared_box
    try: m=source.build_model(replace(source.DIMS,crossfall=0.))
    finally: source.terrain=original;source._xy=original_profile;S.box=original_box
    # The cup slides in from the front, beneath the fitted return rails.
    # Its 6 mm apron seats on a real 6 mm-deep open rebate, leaving 4 mm
    # of tray below it. The two deeper bridge channels guide that slide.
    # Side/end clearance is 0.2 mm; the apron bottom contacts the shelf.
    slot_frame(S,m['board'],m['table'],(0,-.30015,-.0005),(.1324,.0197,.011))
    # The plate carries retained spindle shoulders. They must pass through
    # the tray from below; the plate's own close bearings still locate them.
    # These 14.8 mm tray clearances admit the 14 mm shoulders and drive keys.
    for x in (-m['dimensions'].flipper_x,m['dimensions'].flipper_x):
        bore_frame(S,m['board'],m['table'],(x,m['dimensions'].flipper_y,-.005),.0074,.040,'Z')
    old=m['parts'];parts={k:[] for k,_ in supplies}
    fixtures=set(o for group in m['props'].values() for o in group)
    for obj in old['pb-tray']:
        if obj not in fixtures and not obj.name.startswith('prepared bench-clamp'):parts['tray'].append(obj)
    rail_prefixes={'left retaining rail':'left-rail','right retaining rail':'right-rail','curved top rail':'top-rail',
                   'launch-lane divider':'lane','left curved inward return lip':'left-lip','right inward return lip':'right-lip'}
    for obj in old['pb-rails']:
        key=next((key for prefix,key in rail_prefixes.items() if obj.name.startswith(prefix)),'cup')
        parts[key].append(obj)
    # A visible storage cup holds the 22 mm marble with its centre below the
    # rim. The canonical 26 mm-deep cup hid the final added marble entirely.
    cup=next(o for o in parts['cup'] if o.name.startswith('marble storage cup wall'))
    for vertex in cup.data.vertices:vertex.co.y*=.5
    cup.location.z=-.0065
    next(o for o in parts['cup'] if o.name.startswith('storage cup closed floor')).location.z=-.014
    for key,source_key in [('plate','pb-pivot-plate'),('support','pb-wedge'),('spring','pb-spring'),('marble','pb-marble')]:
        parts[key]=list(old[source_key])
    for obj in old['pb-plunger-tube']:
        if obj.name.startswith(('closed spring enclosure','removable rear bearing cap','front captive piston stop')):continue
        if obj.name.startswith('launcher captive mount retaining shoulder') and obj.location.z<0:continue
        if descendants(obj,m['pull']):
            key='tip' if obj.name.startswith(('captive piston','soft striking tip')) else 'rod'
        else:key='barrel'
        parts[key].append(obj)
    # Plate screws have only lower heads. Their plain upper ends enter actual
    # threaded receivers, instead of trying to push an upper cap through wood.
    for obj in list(parts['plate']):
        if obj.name.startswith('plate captive mounting screw retaining shoulder'):
            if obj.location.z>0:parts['plate'].remove(obj)
            else:obj.location.z+=.001
        elif obj.name.startswith('plate captive mounting screw captive shaft'):
            for vertex in obj.data.vertices:vertex.co.z*=.022/.024
            obj.location.z-=.001
    for x in (-.090,.090):
        for y in (-.225,-.105):
            bore_frame(S,m['board'],m['table'],(x,y,-.005),.0034,.030)
            insert=S.annulus('prepared threaded plate receiver',(0,0,0),.0034,.0019,.008,'paper')
            insert.rotation_euler.x=math.pi/2;insert.location=(x,y,-.004);insert.parent=m['table']
            insert['interface']='Nominal M4 threaded insert: minor radius 1.9 mm, screw major radius 2 mm.'
            parts['tray'].append(insert)
    # Launcher screws enter from above. Retire the inaccessible lower caps;
    # threaded foot sleeves retain each screw before its tray insert is fitted.
    for y in (-.268,-.235):
        bore_frame(S,m['board'],m['table'],(.151,y,-.005),.0034,.030)
        for key,name,z,outer,depth in [('tray','prepared threaded launcher receiver',-.004,.0034,.008),
                                      ('barrel','launcher foot threaded sleeve',.002,.0022,.004)]:
            insert=S.annulus(name,(0,0,0),outer,.0019,depth,'paper')
            insert.rotation_euler.x=math.pi/2;insert.location=(.151,y,z);insert.parent=m['table']
            insert['interface']='Nominal M4 threaded insert: minor radius 1.9 mm, screw major radius 2 mm.'
            parts[key].append(insert)
    for left,frame in [(True,m['flippers'][0]),(False,m['flippers'][1])]:
        side=-1 if left else 1
        # Extend the canonical blade around the back of its spindle. The old
        # outline ended at the spindle centre, so merely cutting its edge
        # could not make a retaining C socket. This continuous rounded root
        # has two actual lips around its narrower 7.8 mm open mouth.
        points=[(0,-.009),(.105,-.007),(.112,0),(.105,.007),(0,.009)]
        points += [(.009*math.cos(math.pi/2+math.pi*i/24),.009*math.sin(math.pi/2+math.pi*i/24)) for i in range(1,24)]
        points=[(-side*x,y) for x,y in points]
        obj=source._xy(('left' if left else 'right')+' rounded snap paddle',points,.006,.0096,'orange');obj.parent=frame
        # 0.2 mm axial running clearance at both shoulders, with the drive
        # key on the closed side and a real lateral insertion path opposite.
        bore_frame(S,obj,frame,(0,0,.006),.0043,.030)
        slot_frame(S,obj,frame,(-side*.004,0,.007),(.0043,.0033,.030))
        slot_frame(S,obj,frame,(side*.010,0,.006),(.020,.0078,.030))
        parts['left-paddle' if left else 'right-paddle'].append(obj)
    for obj in old['pb-targets']:
        if obj.name.startswith(('score ','manual numbered','actual score')): key='score'
        else:
            y=obj.location.y
            key=min([('arch-low',-.015),('arch-mid',.100),('arch-high',.218)],key=lambda row:abs(y-row[1]))[0]
        parts[key].append(obj)
    clear=special_material('clear enclosed marble launcher',(.78,.83,.78),roughness=.12,transmission=.82)
    x,z=m['dimensions'].launcher_x,m['dimensions'].launcher_z
    # The rod enters the piston through a real blind socket before the entire
    # plunger lowers into the cradle; neither handle nor tip crosses a coil.
    piston=next(o for o in parts['tip'] if o.name.startswith('captive piston'))
    bore_frame(S,piston,m['pull'],(x,-.226,z),.0032,.008,'Y')
    for key,upper in [('barrel',False),('cover',True)]:
        for name,y,length,inner in [('spring shell',-.251,.068,.010),('rear guide',-.283,.004,.0033),('front guide',-.219,.004,.0073)]:
            shell=half_tube(S,key+' '+name,(x,y,z),.013,inner,length,upper)
            shell.parent=m['table'];surface(shell,clear);parts[key].append(shell)
    # Clips occupy the clear 21 mm bay BETWEEN the mounting feet. Their
    # outside edge is x=180.5 mm, 0.5 mm inside the right rail; the rear stop
    # spine ends at y=-267 mm. Closing the separate launcher leaves room for
    # snap flex before it is lowered onto the prepared tray.
    for y in (-.255,-.245):
        for sign in (-1,1):
            ear=S.box('cradle retaining ear',(x+sign*.0085,y,.0022),(.010,.007,.002),'teal');ear.parent=m['table'];parts['barrel'].append(ear)
            for name,centre,size in [
                ('cover clip shoulder',(x+sign*.012,y,.016),(.005,.007,.002)),
                ('cover flexible clip leg',(x+sign*.014,y,.0087),(.001,.007,.016)),
                ('cover retaining hook',(x+sign*.01325,y,.0007),(.0025,.007,.001))]:
                obj=S.box(name,centre,size,'teal');obj.parent=m['table'];parts['cover'].append(obj)
    m['source']=source
    return owned(m,parts)

def stage(m,identity):
    info=PLAN[identity];parts=info['parts'];source=m['source']
    m['root'].rotation_euler=(0,0,0);m['root'].location=(0,0,0)
    # Adding the support must not tilt the tray already being worked on.
    # Its final resting slope appears only at the deliberate upright Flip.
    under=info.get('pose')=='under' or identity in {'bf-pb-plate','bf-pb-support'}
    later_parts={'left-paddle','right-paddle','rod','spring','tip','barrel','cover','arch-low','arch-mid','arch-high','score','marble'}
    supported=not under and ('support' in parts or bool(set(parts)&later_parts))
    m['table'].rotation_euler=(m['dimensions'].slope if supported else 0,0,0)
    m['table'].location.z=.074+.300*math.sin(m['dimensions'].slope) if supported else .074
    source.apply_pose(m,pull=0,flippers=(0,0),long=False)
    m['marble'].location=(0,-.327,-.0015)
    m['marble'].rotation_euler=(0,0,0)
    if identity=='pinball-table':
        # Match frame zero of the existing working loop without adding an
        # operation step or changing its rally/impact timing.
        q=7/48;low=-.0938254;x=.040
        y=low+(.255-low)*4*q*(1-q)
        m['marble'].location=(x,y,source.marble_support_height(m,x,y))
        m['marble'].rotation_euler.x=-(y-low)/m['dimensions'].marble_radius
    if under:m['root'].rotation_euler.x=math.pi
    show(m,parts)
    if info['group']=='pb-launcher-build':
        return {'location':(.475,-.735,1.640),'target':(.175,-.285,.090),'scale':.22}
    if info['group'] in {'pb-top','pb-targets'}:
        return {'location':(.30,-.465,1.635),'target':(0,-.015,.085),'scale':.83}
    if info['group']=='pb-score-work' or identity=='pinball-table':
        return {'location':(-.78,-1.05,.95),'target':(0,-.015,.085),'scale':.83}
    if info['group'].startswith('pb-'):
        return {'location':(.78,-1.05,.95 if info.get('pose')!='under' else .85),'target':(0,-.015,.085 if info.get('pose')!='under' else -.085),'scale':.83}
    if identity in {'bf-pb-plate','bf-pb-support'}:
        return inspection(m,parts,direction=(.78,-1.035,.935),margin=1.2)
    if identity=='bf-pb-score':return inspection(m,parts,direction=(-.78,-1.035,.865),margin=1.2)
    if identity in {'bf-pb-left-paddle','bf-pb-right-paddle','bf-pb-spring','bf-pb-tip','bf-pb-barrel','bf-pb-cover','bf-pb-arch-low','bf-pb-arch-mid','bf-pb-arch-high'}:
        return inspection(m,parts,direction=(.30,-.45,1.55),margin=1.2)
    # The asymmetric T handle extends beyond a world-box-centred tight view.
    return inspection(m,parts,direction=(.78,-1.035,.865),margin=1.65 if identity=='bf-pb-rod' else 1.2)

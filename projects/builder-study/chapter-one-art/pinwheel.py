"""Chapter-one pinwheel: one paper shape, explicit reversible viewing states.

Metres; paper-local XY is the sheet, +Z is the coloured front. The frozen
original supplies the paper dimensions and hole factory, not its old hardware
or sloping-tip bend. This version uses exact180-degree parallel-tip bends.
Prepared plastic snap fits are nominal geometry; elasticity is not simulated.
"""
from pathlib import Path
import math
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
BASE = ROOT/'archive/2026.11.07 builder study/art'
sys.path.insert(0, str(BASE))
import bpy
from mathutils import Vector
import scene_parts as S
import wind_toys as W
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import materials
materials.apply(S)


STATES = {
    'pw-paper': ('front', False, ('pw-paper',)),
    'pw-loose-rotor': ('front', True, ('pw-paper',)),
    'pw-folded-rotor': ('front', True, ('pw-paper', 'pw-hub')),
    'pw-rear-rotor': ('rear', True, ('pw-paper', 'pw-hub')),
    'pw-bearing-rotor': ('rear', True, ('pw-paper', 'pw-hub', 'pw-axle')),
    'pw-mounted': ('complete-rear', True, ('pw-paper', 'pw-hub', 'pw-axle', 'pw-handle')),
    'pinwheel': ('complete-front', True, ('pw-paper', 'pw-hub', 'pw-axle', 'pw-handle')),
    'pw-hub': ('hub', True, ('pw-hub',)),
    'pw-axle': ('axle', True, ('pw-axle',)),
    'pw-handle': ('handle', True, ('pw-handle',)),
}


def folded_point(x, y, height, folded=True):
    """An exact semicircular bend followed by a parallel horizontal tip.

    Arc length is the material coordinate: the sheet does not stretch. A
    distinct radius for each supplied paper layer makes the four tip planes
    horizontal at their own heights rather than crossing angled tip planes.
    """
    if not folded:return x,y,0.
    distance=math.hypot(*W.HOLE)
    nx,ny=W.HOLE[0]/distance,W.HOLE[1]/distance
    u=x*nx+y*ny;v=-x*ny+y*nx
    radius=height/2
    arc_length=math.pi*radius
    start=(distance-arc_length)/2
    d=u-start
    if d<=0:position,z=u,0.
    elif d<arc_length:position,z=start+radius*math.sin(d/radius),radius*(1-math.cos(d/radius))
    else:position,z=start-(d-arc_length),height
    return position*nx-v*ny,position*ny+v*nx,z


def set_paper(model, folded):
    for i,(obj,uv,height) in enumerate(model['paper']):
        for vertex,(x,y) in zip(obj.data.vertices,uv):vertex.co=folded_point(x,y,height,folded)
        x,y,z=folded_point(*W.HOLE,height,folded)
        angle=i*math.pi/2
        cutter=model['cutters'][i]
        cutter.location=(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z)
        cutter.rotation_euler=(0,0,0)


def make():
    model = W.build_pinwheel()
    rotor = model['rotor']
    # The new hardware is genuinely front-fitting. Do not mirror the old part:
    # its rear flange and cap had a different assembly order.
    for part in ('pw-hub', 'pw-axle', 'pw-handle'):
        for obj in model['parts'][part]:
            bpy.data.objects.remove(obj, do_unlink=True)
        model['parts'][part] = []
    for obj in list(model['parts']['pw-paper']):
        if obj.name.startswith('printed diagonal'):
            model['parts']['pw-paper'].remove(obj)
            bpy.data.objects.remove(obj, do_unlink=True)
    # A real 0.7mm kerf separates the four prepared incisions. The uncut web
    # remains attached along each full 24mm inner edge.
    replacement = []
    for obj, uv, height in model['paper']:
        # Fine flat-shaded faces avoid smoothing thick bevels into a 0.25mm
        # sheet at its booleans and open boundaries. The curved fold is still
        # sampled densely enough for its genuine cylindrical surface.
        n=100
        uv=[(W.WEB_HALF+(W.PAPER_HALF-W.WEB_HALF)*i/n,
             (2*j/n-1)*(W.WEB_HALF+(W.PAPER_HALF-W.WEB_HALF)*i/n))
            for i in range(n+1) for j in range(n+1)]
        kerfed = [(x, y*(1-.00035*(x-W.WEB_HALF)/(W.PAPER_HALF-W.WEB_HALF)/x)) for x, y in uv]
        faces=[]
        for i in range(n):
            for j in range(n):
                k=i*(n+1)+j;faces.append((k,k+n+1,k+n+2,k+1))
        obj.data.clear_geometry()
        obj.data.from_pydata([(x,y,0) for x,y in kerfed],[],faces)
        obj.data.update()
        for polygon in obj.data.polygons:polygon.use_smooth=False
        replacement.append((obj, kerfed, height))
    model['paper'] = replacement

    paper=S.material('orange')
    reverse=bpy.data.materials.new('lighter brick red reverse of paper')
    reverse.use_nodes=True
    shader=reverse.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=S.PALETTE['paper_reverse']
    shader.inputs['Roughness'].default_value=.82
    for obj in [model['core'], *(entry[0] for entry in model['paper'])]:
        obj.data.materials.clear()
        obj.data.materials.append(paper)
        obj.data.materials.append(reverse)
        obj.data.materials.append(S.material('ink'))
        for polygon in obj.data.polygons:
            polygon.material_index=1 if obj==model['core'] and polygon.normal.z<0 else 0
        for modifier in obj.modifiers:
            if modifier.type == 'SOLIDIFY':
                modifier.material_offset = 1
                modifier.material_offset_rim = 2

    def add(part, obj):
        obj.parent = rotor
        obj['part_id'] = part
        obj['assembly'] = model['root'].name
        model['parts'][part].append(obj)
        return obj

    def cylinder(part, name, center, radius, depth, color):
        return add(part, S.cylinder(name, center, radius, depth, color, 'Z', 96))

    def ring(part, name, center, outer, inner, depth, color, gap=0):
        obj = S.annulus(name, (0,0,0), outer, inner, depth, color, gap=gap)
        obj.rotation_euler.x = math.pi/2
        obj.location = center
        return add(part, obj)

    def local_bore(obj, center, radius, depth):
        # Boolean cutters share paper-local coordinates, unlike S.bore's
        # world-coordinate convenience function.
        cutter = S.cylinder('hidden manufacturing cutter', center, radius, depth, 'ink', 'Z')
        cutter.parent = rotor
        cutter.hide_render = True
        modifier = obj.modifiers.new('real prepared bore or pocket', 'BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = cutter
        return cutter

    # Hub: 24mm visible face, 6mm stem through 6.4mm paper holes. Its closed
    # front contains a real annular recess for the axle's resilient split tip.
    stem = cylinder('pw-hub', 'front-fitting hollow hub stem', (0,0,.0057), .003, .0194, 'teal')
    local_bore(stem, (0,0,.007), .0018, .040)
    face = cylinder('pw-hub', 'broad teal retaining face', (0,0,.0188), .012, .0024, 'teal')
    # This short collar connects the stem to the broad face around its pocket.
    collar = cylinder('pw-hub', 'hub face neck', (0,0,.0165), .0042, .003, 'teal')
    local_bore(collar, (0,0,.0168), .0024, .004)
    local_bore(face, (0,0,.0177), .0024, .0018)
    # A tiny star is moulded into the actual face; it is retained in every view.
    for angle in (0, math.pi/2, math.pi, 3*math.pi/2):
        x,y = .0038*math.cos(angle), .0038*math.sin(angle)
        d = cylinder('pw-hub', 'moulded face dimple', (x,y,.02002), .00055, .00015, 'ink')
    # Two flexible tabs pass through the centre hole and spring out behind it.
    # Their nominal insertion interference is 0.4mm, modelled slots allow
    # flexure but no elastic force/stress claim is made.
    for sign in (-1, 1):
        points=[(sign*x,z) for x,z in [(.0024,-.0022),(.0030,-.0022),(.0036,-.0005),(.0024,-.0005)]]
        if sign<0:points.reverse()
        obj = S.profile('tapered rear flexible hub retaining lip', points, .0024, color='teal', edge='teal')
        add('pw-hub', obj)
    flex_slot=S.box('hidden rear hub flexure slot',(0,0,.001),(.0022,.010,.011),'ink')
    flex_slot.parent=rotor;flex_slot.hide_render=True
    modifier=stem.modifiers.new('two flexible rear tongues','BOOLEAN')
    modifier.operation='DIFFERENCE';modifier.object=flex_slot
    # Axle: one connected prepared unit. Continuous shaft, bonded white spacer,
    # keyed mounting post and split snap tip. The shaft turns inside the hub.
    shaft = cylinder('pw-axle', 'continuous blunt axle', (0,0,-.00625), .0015, .0485, 'ink')
    cylinder('pw-axle', 'bonded smooth bearing spacer', (0,0,-.00825), .006, .0075, 'paper')
    cylinder('pw-axle', 'rear handle mounting post', (0,0,-.0215), .004, .023, 'teal')
    # Broad rear flange prevents the handle sliding axially off its post.
    cylinder('pw-axle', 'rear mounting post flange', (0,0,-.0325), .0068, .002, 'teal')
    tips=[]
    for sign in (-1,1):
        points=[(sign*x,z) for x,z in [(.0009,.0164),(.0022,.0164),(.0015,.018),(.0009,.018)]]
        if sign<0:points.reverse()
        tip=S.profile('tapered resilient axle capture barb', points, .0013, color='teal', edge='teal')
        tips.append(add('pw-axle',tip))
    slot = S.box('hidden axle snap flexure slot', (0,0,.0145), (.0015,.008,.009), 'ink')
    slot.parent = rotor; slot.hide_render = True
    for obj in (*tips, shaft):
        mod = obj.modifiers.new('split end permits snap insertion', 'BOOLEAN')
        mod.operation='DIFFERENCE';mod.object=slot
    # Handle: an open side-entry C-clip joined to a short arm embedded in the
    # wooden stick. Unlike a closed bore, it can clip onto an installed axle.
    clip = ring('pw-handle', 'open side-entry axle clip', (0,0,-.022), .0068, .0042, .009, 'teal', gap=2.30)
    arm = add('pw-handle', S.box('clip mounting arm', (0,-.01275,-.022), (.008,.0145,.008), 'teal'))
    handle = add('pw-handle', S.box('wooden handle', (0,-.100,-.024), (.015,.184,.009), 'birch', bevel=.00065))
    for y in (-.178,-.166):
        local_bore(handle, (0,y,-.024), .0017, .025)
    for y in (-.013,-.018):
        cylinder('pw-handle', 'captive clip mounting rivet', (0,y,-.027), .0015, .009, 'ink')
    model['hub_face'] = face
    set_state(model, 'pinwheel')
    return model


def set_state(model, identity):
    if identity not in STATES:
        raise ValueError('Unknown pinwheel identity '+identity)
    camera, folded, parts = STATES[identity]
    set_paper(model, folded)
    for part, objects in model['parts'].items():
        for obj in objects:
            obj.hide_render = part not in parts
    model['uncut'].hide_render = True
    model['root'].hide_render = True
    bpy.context.view_layer.update()
    return camera


def view(model, family):
    definitions = {
        'front': ((.15,.12,.8), (0,0,.005), .188),
        'rear': ((.50,.12,-.8), (0,-.055,-.01), .310),
        'complete-front': ((.28,.16,.8), (0,-.055,-.01), .310),
        'complete-rear': ((.50,.12,-.8), (0,-.055,-.01), .310),
        'hub': ((.15,.12,.8), (0,0,.008), .036),
        'axle': ((.50,.12,-.8), (0,0,-.008), .065),
        'handle': ((.50,.12,-.8), (0,-.093,-.024), .225),
    }
    offset, target, scale = definitions[family]
    matrix = model['rotor'].matrix_world
    center = matrix @ Vector(target)
    location = matrix @ (Vector(target)+Vector(offset))
    return {'location': tuple(location), 'target': tuple(center), 'scale': scale}


def checks():
    return {
        'paper_side_m': .160,
        'paper_hole_diameter_m': .0064,
        'hub_stem_diameter_m': .006,
        'paper_to_hub_radial_clearance_m': .0002,
        'shaft_radius_m': .0015,
        'hub_bore_radius_m': .0018,
        'shaft_running_radial_clearance_m': .0003,
        'hub_rear_m': -.004,
        'spacer_front_m': -.0045,
        'rear_running_axial_clearance_m': .0005,
        'snap_tip_x_extent_m': .0022,
        'snap_tip_y_halfwidth_m': .00065,
        'snap_pocket_radius_m': .0024,
        'handle_post_radius_m': .004,
        'handle_clip_inner_radius_m': .0042,
        'handle_clip_gap_radians': 2.30,
        'limits': 'Ideal nominal geometry. Prepared snap-fit plastic flexure, retention forces, paper stiffness, wind torque and friction are not simulated or manufactured validation.',
        'corner_hole_target_error_m':max(math.dist(folded_point(*W.HOLE,h),(0,0,h)) for h in [.012+i*.00035 for i in range(4)]),
        'paper_bend':'Exact180-degree semicircle; radius=layer height/2; equal material arc length; parallel stacked tips.',
    }

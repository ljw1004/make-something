"""Dimensioned, independently assembled mast, straw axles and snap-bearing racer.

All coordinates are metres, z up; front axle is +X. The underside is a rigid
half turn around the chassis centre. Materials and views never resize parts.
"""
from pathlib import Path
import sys
import math
import json
import bpy
from mathutils import Vector

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'src/story/parser.ts').is_file())
BASE = ROOT/'archive/2026.11.07 builder study/art'
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(Path(__file__).parent.parent))
import scene_parts as S
from construction import Assembly, special_material
import materials
materials.apply(S)

PLAN = json.loads((Path(__file__).parent/'construction-plan.json').read_text())
AXLE_RADIUS = .003
BEARING_INNER = .0032
BEARING_GAP = 2.4


def cut_box(obj, centre, size):
    cutter = S.box('temporary slot', centre, size)
    bpy.context.view_layer.objects.active = obj
    modifier = obj.modifiers.new('receiving slot', 'BOOLEAN')
    modifier.operation = 'DIFFERENCE'; modifier.object = cutter
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def ring(a, part, name, centre, outer, inner, depth, color, axis='Y', gap=0, mouth='positive'):
    obj = S.annulus(name, (0,0,0), outer, inner, depth, color, gap=gap)
    if axis == 'Z': obj.rotation_euler.x = math.pi/2
    if mouth == 'bottom': obj.rotation_euler.y = math.pi/2
    if mouth == 'negative':
        if axis == 'Z': obj.rotation_euler.z = math.pi
        else: obj.rotation_euler.y = math.pi
    obj.location = centre
    return a.add(part, obj)


def build():
    a = Assembly('independent wind racer')
    chassis = a.box('chassis','honey wood chassis',(0,0,.045),(.220,.110,.008),'birch')
    S.bore(chassis,(0,0,.045),.0042,.020,'Z')
    # Flat printed fitting marks distinguish top and underside without textures.
    ring(a,'chassis','printed mast socket ring',(0,0,.049005),.009,.007,.00001,'teal','Z')
    for side,x in [('front',.075),('rear',-.075)]:
        part = side+'-bearing'
        ring(a,part,'open axle bearing',(x,0,.030),.006,BEARING_INNER,.130,'teal',gap=BEARING_GAP,mouth='bottom')
        for y in (-.042,.042):
            ring(a,part,'bearing saddle',(x,y,.030),.009,.006,.016,'teal',gap=1.3,mouth='bottom')
            a.box(part,'saddle shoulder',(x,y,.0395),(.013,.016,.003),'teal')
            cut_box(chassis,(x,y,.045),(.0084,.0104,.020))
            for sign in (-1,1):
                a.box('chassis','printed bearing guide',(x+sign*.010,y,.040995),(.0008,.022,.00001),'teal')
                a.box('chassis','printed bearing guide',(x,y+sign*.011,.040995),(.0208,.0008,.00001),'teal')
            for sign in (-1,1):
                a.box(part,'saddle snap leg',(x+sign*.003,y,.046),(.002,.009,.012),'teal')
                profile=[(x+sign*px,z) for px,z in [(.0027,.0495),(.0057,.0495),(.0057,.0500),(.0037,.0530),(.0027,.0530)]]
                if sign<0: profile.reverse()
                a.add(part,S.profile('ramped saddle retaining barb',profile,.009,y,'teal','teal'))
        ring(a,side+'-axle','hollow plastic straw',(x,0,.030),AXLE_RADIUS,.002,.152,'ink')
        for end,sign in [('near',-1),('far',1)]:
            part = side+'-wheel-'+end
            wheel = a.cylinder(part,'brick red wheel',(x,sign*.075,.030),.030,.012,'orange','Y')
            # A blind socket, open at the inner face and ending at the straw tip.
            S.bore(wheel,(x,sign*.072,.030),.003,.008,'Y')
            ring(a,part,'integral wheel spacer',(x,sign*.06775,.030),.005,.003,.0025,'orange')
            a.cylinder(part,'cream hub cap',(x,sign*.0815,.030),.008,.001,'paper','Y')
            # Three short compliant socket ribs provide explicit push-fit retention.
            for angle in (0,2*math.pi/3,4*math.pi/3):
                a.cylinder(part,'socket grip rib',(x+.00315*math.cos(angle),sign*.072,.030+.00315*math.sin(angle)),.00020,.006,'orange','Y',)
    a.cylinder('mast','long wooden mast',(0,0,.166),.004,.228,'birch')
    joint = a.box('connector','offset two-socket connector',(.0045,0,.180),(.020,.020,.018),'teal')
    S.bore(joint,(0,0,.180),.0041,.030,'Z')
    S.bore(joint,(.010,0,.180),.0031,.030,'Y')
    for angle in (0,2*math.pi/3,4*math.pi/3):
        a.cylinder('connector','mast gripping rib',(.00415*math.cos(angle),.00415*math.sin(angle),.180),.00030,.012,'teal','Z')
        a.cylinder('connector','crossbar gripping rib',(.010+.00315*math.cos(angle),0,.180+.00315*math.sin(angle)),.00025,.014,'teal','Y')
    a.cylinder('crossbar','wooden crossbar',(.010,0,.180),.003,.140,'birch','Y')
    a.cylinder('foot','prepared foot stem',(0,0,.047),.0039,.006,'teal')
    a.cylinder('foot','mast seating collar',(0,0,.050),.007,.002,'teal')
    ring(a,'foot','mast foot socket',(0,0,.0545),.007,.0041,.007,'teal','Z')
    ring(a,'foot','compressible socket lining',(0,0,.055),.0041,.00395,.006,'paper','Z')
    for sign in (-1,1):
        a.box('foot','split locking foot arm',(sign*.0028,0,.038),(.0016,.004,.018),'teal')
        profile=[(sign*px,z) for px,z in [(.0028,.0345),(.0033,.0345),(.0052,.0385),(.0052,.039),(.0028,.039)]]
        if sign<0: profile.reverse()
        a.add('foot',S.profile('ramped foot retaining barb',profile,.004,0,'teal','teal'))
    vertices=[(.0163,-.060,.180),(.0163,.060,.180),(.006,0,.276)]
    mesh=bpy.data.meshes.new('plain canvas sail'); mesh.from_pydata(vertices,[],[(0,1,2)]);mesh.update()
    cloth=bpy.data.objects.new('untextured cream sail',mesh);bpy.context.collection.objects.link(cloth)
    cloth.data.materials.append(S.material('paper'));a.add('cloth',cloth)
    solid=cloth.modifiers.new('real cloth thickness','SOLIDIFY');solid.thickness=.0003
    # Bound edge is simple geometry, not a fabric texture.
    a.line('cloth','forest green bound sail edge',vertices+[vertices[0]],.00065,'teal')
    for y in (-.060,.060):
        a.box('cloth','integral sail clip tab',(.0153,y,.180),(.0024,.003,.0012),'teal')
        ring(a,'cloth','open crossbar sail clip',(.010,y,.180),.0047,.0031,.003,'teal',gap=2.4,mouth='negative')
    ring(a,'cloth','open mast sail clip',(0,0,.276),.006,.0041,.003,'teal','Z',gap=2.4,mouth='negative')
    return a.result()


def set_stage(model, identity):
    info=PLAN[identity];allowed=set(info['parts'])
    model['root'].rotation_euler=(0,0,0);model['root'].location=(0,0,0)
    for part,objects in model['parts'].items():
        for obj in objects: obj.hide_render=part not in allowed;obj.hide_set(obj.hide_render)
    if info['view']=='underside':
        model['root'].rotation_euler.x=math.pi;model['root'].location.z=.090
    bpy.context.view_layer.update()
    return info


def bounds(model):
    points=[obj.matrix_world@Vector(corner) for objects in model['parts'].values() for obj in objects if not obj.hide_render for corner in obj.bound_box]
    return [min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]


def view(model, info):
    if info['view']=='mast': return dict(location=(.6,-.8,.4),target=(.004,0,.155),scale=.34,roll=-.55)
    if info['view'] in ('underside','upright'): return dict(location=(.55,-.8,.65),target=(0,0,.045),scale=.34,roll=0)
    if info['view']=='axle':
        x=.075 if info['parts'][0].startswith('front') else -.075
        centre=Vector((x,0,.030))
        return dict(location=tuple(centre+Vector((.6,-.8,.5))),target=tuple(centre),scale=.25,roll=-.45)
    if info['view']=='complete': return dict(location=(.55,-.8,.48),target=(0,0,.145),scale=.38,roll=0)
    lo,hi=bounds(model);centre=Vector([(a+b)/2 for a,b in zip(lo,hi)])
    scale=max(hi[i]-lo[i] for i in range(3))*1.5
    # The bearing's underside and mouth are inspection features, not hidden backs.
    direction=Vector((.6,-.8,-.7) if any(p.endswith('bearing') for p in info['parts']) else (.6,-.8,.5))
    return dict(location=tuple(centre+direction),target=tuple(centre),scale=scale,roll=-.45)

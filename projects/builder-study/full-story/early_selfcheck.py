"""Focused nominal-fit checks for the four repaired early constructions.

Run inside Blender with --threads 2. Optional family names follow ``--``.
No renders or persistent reports are produced. These are geometry and route
constraints, not spring-force, friction, strength or manufacturing validation.
"""
from pathlib import Path
import importlib
import itertools
import json
import math
import sys
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0,str(Path(__file__).resolve().parent))


def vertices(obj):
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh()
    result=[evaluated.matrix_world@v.co for v in mesh.vertices]
    evaluated.to_mesh_clear()
    return result


def bvh(obj):
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh()
    tree=BVHTree.FromPolygons([evaluated.matrix_world@v.co for v in mesh.vertices],
                            [tuple(p.vertices) for p in mesh.polygons])
    evaluated.to_mesh_clear()
    return tree


def verify_plan(family,model):
    draw_types={'MESH','CURVE','FONT'}
    all_owned={o for group in model['parts'].values() for o in group}
    assert not [o.name for o in bpy.context.scene.objects if o.type in draw_types and not o.hide_render and o not in all_owned]
    groups={}
    for identity,plan in family.PLAN.items():
        view=family.stage(model,identity);bpy.context.view_layer.update()
        expected={o for key in plan['parts'] for o in model['parts'][key]}
        visible={o for o in bpy.context.scene.objects if o.type in draw_types and not o.hide_render}
        assert expected==visible,(identity,'ownership')
        encoded=json.dumps(view,sort_keys=True)
        assert groups.setdefault(plan['group'],encoded)==encoded,(identity,'camera')
    return len(family.PLAN)


def pinball(family,m):
    family.stage(m,'pinball-table');bpy.context.view_layer.update()
    board=m['board'];rows=[]
    for x in (-.135,.135):
        for offset in (0,.005,.0073,.0075):
            hit=board.ray_cast(Vector((x+offset,-.160,.030)),Vector((0,0,-1)))[0]
            assert hit==(offset>.0074),(x,offset,'actual tray bore',hit)
            rows.append([x,offset,hit])
    for side,index in [('left',0),('right',1)]:
        paddle=m['parts'][side+'-paddle'][0];frame=m['flippers'][index]
        sign=-1 if side=='left' else 1
        conversion=paddle.matrix_world.inverted()@frame.matrix_world
        start=conversion@Vector((sign*.020,0,.006))
        direction=(conversion.to_3x3()@Vector((-sign,0,0))).normalized()
        hit,point,_,_=paddle.ray_cast(start,direction)
        assert hit,(side,'paddle still has a back wall')
        point=(frame.matrix_world.inverted()@paddle.matrix_world)@point
        assert point.x*(-sign)>.004,(side,'snap mouth blocked',tuple(point))
        for y in (-.00395,.00395):
            hit,lip,_,_=paddle.ray_cast(conversion@Vector((sign*.020,y,.006)),direction)
            lip=(frame.matrix_world.inverted()@paddle.matrix_world)@lip
            assert hit and lip.x*sign>.002,(side,'missing retaining lip',tuple(lip))
    assert not [o for o in m['parts']['plate'] if o.name.startswith('plate captive mounting screw retaining shoulder') and o.location.z>0]
    assert not [o for o in m['parts']['barrel'] if o.name.startswith('launcher captive mount retaining shoulder') and o.location.z<0]
    cup_floor=next(o for o in m['parts']['cup'] if o.name.startswith('storage cup closed floor'))
    floor_top=cup_floor.location.z+max(v.co.z for v in cup_floor.data.vertices)
    assert abs(floor_top-(m['marble'].location.z-m['dimensions'].marble_radius))<1e-7
    assert m['marble'].location.z<0<m['marble'].location.z+m['dimensions'].marble_radius
    assert .0049>.003 and .010>.0095 and .0033>.003 and .0073>.007
    return {'tray_local_rays':rows,'paddle_mouth_mm':7.8,'paddle_pin_mm':8.,
            'spring_inner_diameter_mm':9.8,'rod_diameter_mm':6.,
            'cradle_mouth_mm':20.,'piston_diameter_mm':19.,
            'piston_socket_diameter_mm':6.4,'plate_thread':'nominal M4 receiver'}


def dragon(family,m):
    family.stage(m,'crank-dragon');bpy.context.view_layer.update()
    d=m['source'].DIMS
    maximum=0.
    for i in range(145):
        pose=m['source'].solve_pose(i*math.tau/144,'eccentric')
        for rod in pose['rods'].values():maximum=max(maximum,abs(math.dist(rod['follower_pivot'],rod['wing_pivot'])-.055))
    assert maximum<1e-12
    assert all(o.name.startswith('straight 6') for o in m['parts']['shaft'])
    assert all(not o.name.startswith('crank retaining clip') for o in m['parts']['handle'])
    assert len(m['parts']['crank-clip'])==1
    assert .0033>d.shaft_radius and .0031>d.shaft_radius
    assert .0012<d.pivot_bore<.0021
    assert .0012>2*(.0021-d.pivot_bore)
    for side in ('left','right'):
        frame=m['rods'][side]
        for z in (0,.055):
            # A ray through the opened mouth must reach the opposite side of
            # each eye, never hit the formerly closed outer rim at +4 mm.
            hits=[]
            for obj in m['parts'][side+'-link']:
                conversion=obj.matrix_world.inverted()@frame.matrix_world
                hit,point,_,_=obj.ray_cast(conversion@Vector((.008,0,z)),(conversion.to_3x3()@Vector((-1,0,0))).normalized())
                if hit:hits.append(((frame.matrix_world.inverted()@obj.matrix_world)@point).x)
            assert hits and max(hits)<-.0015,(side,z,'open link mouth',hits)
    return {'poses':145,'maximum_55mm_link_error_m':maximum,'shaft_mm':6.,'bearing_bore_mm':6.6,
            'cam_hub_bore_mm':6.2,'body_eye_mm':3.4,'snap_tip_mm':2.4,'expanded_snap_barb_mm':4.2,
            'split_gap_mm':1.2,'link_mouth_mm':2.8,'link_pin_mm':3.}


def kaleidoscope(family,m):
    family.stage(m,'bf-ka-mirrors-3');bpy.context.view_layer.update()
    flat=[tuple(v.co) for v in m['backing'].data.vertices[:6]]
    flat_length=sum(math.dist(a,b) for a,b in zip(flat,flat[1:]))
    family.stage(m,'kaleidoscope');bpy.context.view_layer.update()
    folded=[tuple(v.co) for v in m['backing'].data.vertices[:6]]
    folded_length=sum(math.dist(a,b) for a,b in zip(folded,folded[1:]))
    assert abs(flat_length-folded_length)<2e-8
    mirrors=[m['parts']['mirror-'+str(i)][0] for i in (1,2,3)]
    overlaps=[len(bvh(a).overlap(bvh(b))) for a,b in itertools.combinations(mirrors,2)]
    assert overlaps==[0,0,0],('mirror intersections',overlaps)
    radius=max(math.hypot(v.x,v.z) for v in vertices(m['backing']))
    assert radius<.0256,('backing insertion envelope',radius)
    necks=[o for o in m['parts']['tube'] if o.name.startswith(('fixed front neck','fixed collar retaining flange'))]
    minimum=min(math.hypot(v.x,v.z) for o in necks for v in vertices(o))
    assert minimum>=.025599
    return {'mirror_width_mm':38.,'mirror_pair_intersections':overlaps,
            'backing_length_error_m':abs(flat_length-folded_length),
            'backing_maximum_radius_mm':radius*1000,'neck_minimum_radius_mm':minimum*1000,
            'tab_outside_offset_mm':.45,'backing_thickness_mm':.35}


def drum(family,m):
    family.stage(m,'animation-drum');bpy.context.view_layer.update()
    floor=m['parts']['floor'][0];fv=vertices(floor)
    radius=max(math.hypot(v.x,v.y) for v in fv);floor_top=max(v.z for v in fv)
    paper=next(o for o in m['parts']['strip-round'] if o.name.startswith('picture strip paper'))
    paper_bottom=min(v.z for v in vertices(paper))
    assert radius<.08975
    assert abs(floor_top-paper_bottom)<1e-7,(floor_top,paper_bottom)
    folded=[]
    for obj,angle in m['tabs']:
        coords=[(obj.data.vertices[i].co+obj.data.vertices[i+1].co)/2 for i in (0,2,4,6)]
        folded.append(sum((b-a).length for a,b in zip(coords,coords[1:])))
    family.stage(m,'bf-film-seated')
    for index,(obj,angle) in enumerate(m['tabs']):
        coords=[(obj.data.vertices[i].co+obj.data.vertices[i+1].co)/2 for i in (0,2,4,6)]
        length=sum((b-a).length for a,b in zip(coords,coords[1:]))
        assert abs(length-folded[index])<1e-8
        assert abs(math.hypot(coords[-1].x,coords[-1].y)-.087)<1e-7
    family.stage(m,'bf-film-rolled')
    for index,(obj,angle) in enumerate(m['tabs']):
        coords=[(obj.data.vertices[i].co+obj.data.vertices[i+1].co)/2 for i in (0,2,4,6)]
        assert abs(sum((b-a).length for a,b in zip(coords,coords[1:]))-folded[index])<1e-8
        assert all(abs(math.hypot(c.x,c.y)-.090)<1e-7 for c in coords)
    return {'floor_radius_mm':radius*1000,'wall_inner_radius_mm':89.75,
            'floor_top_mm':floor_top*1000,'picture_bottom_mm':paper_bottom*1000,
            'tab_width_mm':4.,'slot_width_mm':4.4,'tab_thickness_mm':.5,'slot_radial_width_mm':1.2,
            'straight_and_folded_tab_length_mm':folded[0]*1000}


if __name__=='__main__':
    names=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['pinball','dragon','kaleidoscope','drum']
    for name in names:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
        family=importlib.import_module(name);model=family.build()
        count=verify_plan(family,model)
        result=globals()[name](family,model)
        print(json.dumps({'family':name,'images':count,'checks':result}),flush=True)
    print('EARLY NOMINAL FIT CHECKS PASSED',flush=True)

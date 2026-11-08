"""Targeted nominal contact checks; writes disposable concise JSON under runs/."""
from pathlib import Path
import argparse
import json
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from adapters import Adapter

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
args = p.parse_args(sys.argv[sys.argv.index('--')+1:])
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
records = {}

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
adapter = Adapter('pinball')
m = adapter.model
objects = [obj for values in m['parts'].values() for obj in values
           if obj.type == 'MESH' and not obj.hide_render and obj != m['marble']]
trees = {}
for obj in objects:
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = ev.to_mesh()
    trees[obj.name] = BVHTree.FromPolygons([v.co for v in mesh.vertices], [tuple(p.vertices) for p in mesh.polygons])
    ev.to_mesh_clear()
collisions = []
nearest = (1, '')
flipper_nearest = (1, '', 0)
flipper_contact = None
for phase in [i/192 for i in range(193)]:
    adapter.pose(phase)
    point = m['marble'].matrix_world.translation
    for obj in objects:
        local = obj.matrix_world.inverted() @ point
        hit = trees[obj.name].find_nearest(local)
        if hit and hit[0] is not None:
            clearance = (obj.matrix_world @ hit[0]-point).length-m['dimensions'].marble_radius
            if clearance < nearest[0]:
                nearest = (clearance, obj.name)
            if obj in m['parts']['left-paddle']+m['parts']['right-paddle'] and clearance < flipper_nearest[0]:
                flipper_nearest = (clearance, obj.name, phase)
                flipper_contact = tuple(m['table'].matrix_world.inverted() @ (obj.matrix_world @ hit[0]))
            if clearance < -.0004:
                collisions.append(dict(phase=phase, object=obj.name, penetration=clearance))
records['pinball'] = dict(samples=193, minimumClearanceM=nearest[0], nearestObject=nearest[1],
                          flipperMinimumClearanceM=flipper_nearest[0], flipperPhase=flipper_nearest[2],
                          flipperContactLocal=flipper_contact,
                          penetrations=collisions, limit='Nominal sphere-to-surface distance; not contact dynamics.')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
adapter = Adapter('gantry')
lengths = []
endpoint_errors = []
for i in range(97):
    adapter.pose(i/96)
    m = adapter.model
    points = [Vector(point.co[:3]) for point in m['cord'].data.splines[0].points]
    lengths.append(sum((a-b).length for a, b in zip(points, points[1:])))
    endpoint_errors.append((points[-1]-m['hook'].location).length)
records['gantry'] = dict(samples=97, cordLengthRangeM=[min(lengths), max(lengths)],
                         lengthVariationM=max(lengths)-min(lengths), hookEndpointErrorM=max(endpoint_errors),
                         limit='Finite polyline winding, no elastic cord or load-force simulation.')
(out/'contacts.json').write_text(json.dumps(records, indent=2)+'\n')
print(json.dumps({key: {k: v for k, v in value.items() if k != 'penetrations'} for key, value in records.items()}, indent=2))
print('Pinball penetrations:', len(collisions))

"""Planar ratchet/pawl overlap check over the prescribed lift/lower cycle."""
from pathlib import Path
import json
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from adapters import Adapter

def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def inside(p, poly):
    hit = False
    for a, b in zip(poly, poly[1:]+poly[:1]):
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0] < x:
                hit = not hit
    return hit

def crosses(a, b, c, d):
    r, s = sub(b, a), sub(d, c)
    den = cross(r, s)
    if abs(den) < 1e-12:
        return False
    u, v = cross(sub(c, a), s)/den, cross(sub(c, a), r)/den
    return 1e-5 < u < 1-1e-5 and 1e-5 < v < 1-1e-5

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
adapter = Adapter('gantry')
m = adapter.model
tooth = next(obj for obj in m['parts']['pawl'] if obj.name.startswith('pawl tooth'))
ratchet = m['parts']['ratchet'][0]

def outline(obj):
    # Their profile meshes contain two copies of the polygon, one on each Y face.
    result = []
    for vertex in obj.data.vertices:
        co = obj.matrix_world @ vertex.co
        point = (co.x, co.z)
        if not any(math.dist(point, existing) < 1e-7 for existing in result):
            result.append(point)
    return result

overlaps = []
for i in range(193):
    adapter.pose(i/192)
    a = outline(tooth)
    theta = adapter.controls['winch'].rotation_euler.y
    b = []
    for j in range(16):
        angle = math.tau*j/16
        b += [(-.112+.019*math.cos(angle-theta), .058+.019*math.sin(angle-theta)),
              (-.112+.016*math.cos(angle+.34-theta), .058+.016*math.sin(angle+.34-theta))]
    crossed = any(crosses(p, q, r, s) for p, q in zip(a, a[1:]+a[:1]) for r, s in zip(b, b[1:]+b[:1]))
    if crossed:
        overlaps.append(i/192)
print(json.dumps(dict(samples=193, crossingPhases=overlaps,
                      limit='Planar polygon edge crossings; exact face contacts are allowed.'), indent=2))
if overlaps:
    raise RuntimeError('Pawl enters ratchet teeth during working motion')

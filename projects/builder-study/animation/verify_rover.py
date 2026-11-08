"""Check actual evaluated wheel contact velocities for the closed rover path."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from adapters import Adapter

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
adapter = Adapter('rover')
m = adapter.model
d = m['dimensions']
step = 5e-4
slips = {'drive_wheels': [], 'caster': []}
members = [('drive_wheels', wheel, Vector((0, side*d.wheel_track/2, -d.wheel_radius)))
           for side, wheel in zip((-1, 1), m['wheels'])]
members.append(('caster', m['caster_ball'], Vector((0, 0, -d.caster_radius))))
for sample in range(24):
    p = sample/24
    adapter.pose(p)
    for label, wheel, local_ground in members:
        # Choose the material point touching the ground at this exact pose.
        rotation = wheel.rotation_quaternion.to_matrix() if wheel.rotation_mode == 'QUATERNION' else wheel.rotation_euler.to_matrix()
        local_material = rotation.inverted() @ local_ground
        adapter.pose(p-step)
        before = wheel.matrix_world @ local_material
        adapter.pose(p+step)
        after = wheel.matrix_world @ local_material
        velocity = (after-before)/(2*step)
        slips[label].append((velocity.x**2+velocity.y**2)**.5)
        adapter.pose(p)
maximum = {label: max(values) for label, values in slips.items()}
result = dict(samples=24, maximumHorizontalContactSpeedMPerCycle=maximum,
              finiteDifferencePhase=step, limit='Kinematic no-slip check; no traction or motor simulation.')
print(json.dumps(result, indent=2))
if max(maximum.values()) > .001:
    raise RuntimeError('Rover wheels slide instead of rolling')

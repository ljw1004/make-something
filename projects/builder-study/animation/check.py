"""Lightweight Blender kinematic coverage, with optional representative renders."""
from pathlib import Path
import argparse
import json
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Matrix, Vector
from adapters import Adapter, FAMILIES, S

p = argparse.ArgumentParser()
p.add_argument('--families', default=','.join(FAMILIES))
p.add_argument('--output', required=True)
p.add_argument('--no-renders', action='store_true')
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
records = []
for family in args.families.split(','):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = S.configure_render(320)
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 2
    scene.cycles.samples = 4
    scene.view_settings.exposure = -2.75
    try:
        adapter = Adapter(family)
        m = adapter.model
        visible = [o for o in scene.objects if o.type in {'MESH', 'CURVE'} and not o.hide_render]
        samples = []
        rest = {o.name: o.matrix_world.copy() for o in visible}
        vertex_rest = {o.name: [tuple(v.co) for v in o.data.vertices] for o in visible if o.type == 'MESH'}
        if family == 'pinwheel' or (family == 'carrier' and 'pinwheel' in m):
            rotor_model = m if family == 'pinwheel' else m['pinwheel']
            blade = rotor_model['paper'][0][0]
            point = blade.data.vertices[-1].co
            # Remove whole-toy travel: a hovering carrier alone must not be
            # mistaken for a working carried pinwheel.
            relative = m['root'].matrix_world.inverted()
            start_point = relative @ blade.matrix_world @ point
            fixed = rotor_model['parts']['pw-handle'][0]
            fixed_rest = relative @ fixed.matrix_world
            adapter.pose(1/16)
            relative = m['root'].matrix_world.inverted()
            if ((relative @ blade.matrix_world @ point)-start_point).length < .01:
                raise ValueError('Pinwheel paper does not move around its real axle')
            fixed_now = relative @ fixed.matrix_world
            if any(abs(fixed_now[r][c]-fixed_rest[r][c]) > 1e-7 for r in range(4) for c in range(4)):
                raise ValueError('Pinwheel handle rotates with its paper')
            adapter.pose(0)
        moved = set()
        for i in range(97):
            phase = i / 96
            adapter.pose(phase)
            for obj in visible:
                if any(abs(obj.matrix_world[r][c]-rest[obj.name][r][c]) > 1e-7 for r in range(4) for c in range(4)):
                    moved.add(obj.name)
                flexible_sleeve = family == 'spinner' and obj.type == 'MESH' and obj.data == m.get('joiner_mesh')
                if obj.type == 'MESH' and not flexible_sleeve and obj.get('motion_role') != 'light_projection' and [tuple(v.co) for v in obj.data.vertices] != vertex_rest[obj.name]:
                    raise ValueError('Rigid mesh vertices changed: ' + obj.name)
            if i in (0, 24, 48, 72, 96):
                points = [obj.matrix_world @ Vector(v) for obj in visible for v in obj.bound_box]
                samples.append(dict(phase=phase, lo=[min(v[k] for v in points) for k in range(3)],
                                    hi=[max(v[k] for v in points) for k in range(3)]))
        if not moved:
            raise ValueError('No real mechanism movement')
        # A loop may finish at whole rotations, whose matrices are equal to rest.
        # Symmetric wheels can accumulate a non-integer rotation while a vehicle
        # closes its trajectory; their visible seam is checked in the exported loop.
        records.append(dict(family=family, ok=True, samples=samples, moving=len(moved), view=adapter.view))
        if not args.no_renders:
            adapter.pose(0)
            scene.camera = S.camera(family, adapter.view['location'], adapter.view['target'], adapter.view['scale'])
            for phase in (0, .25, .5, .75):
                adapter.pose(phase)
                view = adapter.camera_view(phase)
                scene.camera.location = view['location']
                scene.camera.data.ortho_scale = view['scale']
                S.look_at(scene.camera, view['target'])
                scene.camera.rotation_euler = (scene.camera.rotation_euler.to_matrix() @ Matrix.Rotation(view.get('roll', 0), 3, 'Z')).to_euler()
                scene.render.filepath = str(out / f'{family}-{round(phase*100):02d}.png')
                bpy.ops.render.render(write_still=True)
        print('CHECK', family, 'OK', len(moved), flush=True)
    except Exception as error:
        import traceback
        traceback.print_exc()
        records.append(dict(family=family, ok=False, error=str(error)))
        print('CHECK', family, 'FAILED', error, flush=True)
(out / 'checks.json').write_text(json.dumps(records, indent=2) + '\n')
if not all(record['ok'] for record in records):
    raise RuntimeError('One or more mechanism checks failed')

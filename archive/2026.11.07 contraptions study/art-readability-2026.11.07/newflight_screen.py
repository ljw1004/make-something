"""Render one truthful front-screen detail without altering frozen flight art.

Blender --background --factory-startup --python newflight_screen.py --
  --catalogue FILE --baseline-manifest FILE --output DIR

Only the existing reward's projected_light function is loaded from its AST;
the historical CLI and reward batch never execute. All geometry is canonical.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'src/story/parser.ts').exists())
BASE = ROOT/'archive/2026.11.07 builder study/art'
sys.path.insert(0, str(BASE))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import presentation as P
import scene_parts as S
import shadow_theatre as T
import garden as G


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument('--catalogue', required=True)
parser.add_argument('--baseline-manifest', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
baseline = json.loads(Path(args.baseline_manifest).read_text())
for path, expected in baseline['sourceHashes'].items():
    if digest(ROOT/path) != expected:
        raise ValueError('Frozen source changed: '+path)
catalogue = json.loads(Path(args.catalogue).read_text())
item = next(item for item in catalogue['items'] if item['id'] == 'fair-in-the-air')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = S.configure_render(960)
scene.render.threads_mode = 'FIXED'
scene.render.threads = 2
scene.cycles.samples = 24
bpy.context.view_layer.update()
# The same evening environment as the accepted final reward lets the small
# projected light read on its cloth; construction lighting clips it to white.
G.build(bench=False, evening=True, extent=8)
model = P.build('whale')
P.stage(model, item, 'whale')
bpy.context.view_layer.update()
assert model['root'].location.z == 1.0
assert tuple(model['root'].rotation_euler) == (0.0, 0.0, 0.0)
original = {obj: tuple(tuple(row) for row in obj.matrix_world)
            for obj in scene.objects if obj.type in {'MESH', 'CURVE', 'FONT'}}

# Reuse the historical reward's exact mathematical footprint and material.
reward_source = BASE/'render_rewards.py'
tree = ast.parse(reward_source.read_text(), filename=str(reward_source))
function = next(node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name == 'projected_light')
module = ast.Module(body=[function], type_ignores=[])
namespace = {'bpy': bpy}
exec(compile(ast.fix_missing_locations(module), str(reward_source), 'exec'), namespace)
theatre = model['theatre']
cloth = model['parts']['theatre-cloth'][0]
theta = -model['theatre_spindle'].rotation_euler.y
before_names = set(obj.name for obj in scene.objects)
target = namespace['projected_light'](theatre, cloth, theta)
projected_objects = [obj for obj in scene.objects if obj.name not in before_names]
view = {'location': (target[0], target[1]+.50, target[2]),
        'target': target, 'scale': .18}
camera = S.camera('actual front-screen detail', **view)
scene.camera = camera
bpy.context.view_layer.update()

world = theatre['root'].matrix_world
screen_y = (world.inverted() @ cloth.matrix_world.translation).y
corners = [cloth.matrix_world @ Vector(p) for p in cloth.bound_box]
limits = {'x': [min(p.x for p in corners), max(p.x for p in corners)],
          'z': [min(p.z for p in corners), max(p.z for p in corners)]}
checks = []
for star in T.projected_stars(theta, screen_y=screen_y):
    footprint = [world @ Vector(p) for p in star['polygon_m']]
    if not all(limits['x'][0] <= p.x <= limits['x'][1]
               and limits['z'][0] <= p.z <= limits['z'][1] for p in footprint):
        continue
    obj = next(obj for obj in projected_objects
               if obj.name == 'actual projected star '+str(star['hole_index']))
    expected = [p+Vector((0., .001, 0.)) for p in footprint]
    actual = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
    error = max((a-b).length for a, b in zip(actual, expected))
    assert len(actual) == len(expected) == 10 and error < 1e-6
    camera_points = [world_to_camera_view(scene, camera, p) for p in actual]
    assert all(0 < p.x < 1 and 0 < p.y < 1 and p.z > 0 for p in camera_points)
    checks.append({'holeIndex': star['hole_index'],
                   'footprintWorldMetres': [list(p) for p in footprint],
                   'renderedSurfaceOffsetMetres': [0., .001, 0.],
                   'maximumVertexErrorMetres': error,
                   'maximumIdealBlurDiameterMetres': star['max_blur_diameter_m'],
                   'cameraBoundsNormalized': [min(p.x for p in camera_points), min(p.y for p in camera_points),
                                              max(p.x for p in camera_points), max(p.y for p in camera_points)]})
assert len(checks) == len(projected_objects) == 2
assert camera.location.y > cloth.matrix_world.translation.y
assert all(tuple(tuple(row) for row in obj.matrix_world) == transform
           for obj, transform in original.items())
path = out/'fair-in-the-air--screen.png'
scene.render.filepath = str(path)
bpy.ops.render.render(write_still=True)
bpy.context.view_layer.update()
assert all(tuple(tuple(row) for row in obj.matrix_world) == transform
           for obj, transform in original.items())
sources = {Path(module.__file__).resolve() for module in tuple(sys.modules.values())
           if getattr(module, '__file__', None) and Path(module.__file__).resolve().parent == BASE}
sources.update({Path(__file__).resolve(), reward_source})
manifest = {'id': item['id'], 'file': path.name, 'pixels': [960, 960],
            'label': 'Screen detail', 'sha256': digest(path), 'camera': view,
            'lighting': 'Canonical final-reward evening garden environment',
            'heightMetres': model['root'].location.z, 'discPhaseRadians': theta,
            'clothBoundsMetres': limits, 'projectedStars': checks,
            'existingGeometryTransformsUnchanged': True,
            'baselineSourceHashesMatch': True, 'baselineManifestSha256': digest(Path(args.baseline_manifest)),
            'sourceHashes': {str(p.relative_to(ROOT)): digest(p) for p in sorted(sources)},
            'evidenceLimit': 'Exact reuse of the reward chief-ray diagram at the same mask phase and physical cloth. Ideal thin-lens illustration, not photometric simulation or measured projector performance.'}
(out/'screen-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print('Rendered one front-screen detail; both real-mask footprints fit the cloth and camera; existing transforms unchanged.', flush=True)

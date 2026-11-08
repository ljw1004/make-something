"""Blender -b --python render.py -- --family pinwheel --output runs/... .

Exactly one two-thread render process. Frames are sampled over [0, 1), avoiding
a doubled seam frame. All inputs are fingerprinted before and after rendering.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Matrix, Vector
from adapters import Adapter, FAMILIES, ROOT, S

p = argparse.ArgumentParser()
p.add_argument('--family', required=True, choices=FAMILIES)
p.add_argument('--output', required=True)
p.add_argument('--frames', type=int, default=96)
p.add_argument('--fps', type=int, default=15)
p.add_argument('--resolution', type=int, default=640)
p.add_argument('--samples', type=int, default=12)
p.add_argument('--poster-resolution', type=int, default=1600)
p.add_argument('--poster-samples', type=int, default=24)
p.add_argument('--camera-scale', type=float, help='Explicit physical orthographic scale for a reviewed motion envelope')
p.add_argument('--only-frames', help='Comma-separated frame numbers for a disposable probe')
p.add_argument('--engine', choices=('CYCLES', 'BLENDER_EEVEE_NEXT'), default='CYCLES')
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = S.configure_render(args.resolution)
scene.render.engine = args.engine
scene.render.threads_mode = 'FIXED'
scene.render.threads = 2
scene.view_settings.exposure = -2.75
scene.cycles.samples = args.samples
scene.render.use_persistent_data = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
scene.render.fps = args.fps
adapter = Adapter(args.family)
if args.camera_scale is not None:
    if args.camera_scale <= 0:
        raise ValueError('Camera scale must be positive')
    adapter.view['scale'] = args.camera_scale
view = adapter.view
camera = S.camera(adapter.identity, view['location'], view['target'], view['scale'])
scene.camera = camera
camera.rotation_euler = (camera.rotation_euler.to_matrix() @ Matrix.Rotation(view.get('roll', 0), 3, 'Z')).to_euler()
light_view = getattr(adapter, 'lighting_view', view)
forward = (Vector(light_view['location']) - Vector(light_view['target'])).normalized()
right = camera.rotation_euler.to_matrix() @ Vector((1, 0, 0))
up = camera.rotation_euler.to_matrix() @ Vector((0, 1, 0))
light_scale = max(.08, light_view['scale'] / .35)
for name, r, u, f, power, size in [('large soft key', -.35, .5, .5, 28, .7), ('soft fill', .35, .1, .35, 16, .5)]:
    light = scene.objects[name]
    light.location = Vector(light_view['target']) + (right * r + up * u + forward * f) * light_scale
    light.data.energy = power * light_scale ** 2
    light.data.size = size * light_scale
    S.look_at(light, light_view['target'])

def source_hashes():
    files = {Path(__file__).resolve()}
    for module in list(sys.modules.values()):
        path = getattr(module, '__file__', None)
        if path and Path(path).is_file() and Path(path).resolve().is_relative_to(ROOT):
            files.add(Path(path).resolve())
    if args.family == 'racer':
        files.add(ROOT / 'projects/builder-study/racer-art/construction-plan.json')
    if args.family in {'carrier', 'window'}:
        files.add(ROOT / 'projects/builder-study/chapter-one-art/pinwheel.py')
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(files)}

sources = source_hashes()
start = time.monotonic()
indices = [int(i) for i in args.only_frames.split(',')] if args.only_frames else range(args.frames)
for index in indices:
    adapter.pose(index / args.frames)
    current = adapter.camera_view(index / args.frames)
    camera.location = current['location']
    camera.data.ortho_scale = current['scale']
    S.look_at(camera, current['target'])
    camera.rotation_euler = (camera.rotation_euler.to_matrix() @ Matrix.Rotation(current.get('roll', 0), 3, 'Z')).to_euler()
    scene.render.filepath = str(out / f'{index:04d}.png')
    bpy.ops.render.render(write_still=True)
    print(f'LOOP {args.family} {index + 1}/{args.frames}', flush=True)
adapter.pose(0)
camera.location = view['location']
camera.data.ortho_scale = view['scale']
S.look_at(camera, view['target'])
camera.rotation_euler = (camera.rotation_euler.to_matrix() @ Matrix.Rotation(view.get('roll', 0), 3, 'Z')).to_euler()
scene.render.resolution_x = scene.render.resolution_y = args.poster_resolution
scene.cycles.samples = args.poster_samples
scene.render.filepath = str(out / 'poster.png')
bpy.ops.render.render(write_still=True)
after = source_hashes()
changed = sorted(key for key in sources if after.get(key) != sources[key])
record = dict(family=args.family, identity=adapter.identity, frames=args.frames, fps=args.fps,
              resolution=args.resolution, posterResolution=args.poster_resolution, samples=args.samples,
              posterSamples=args.poster_samples,
              engine=args.engine, view=view, sources=sources, changedSources=changed,
              elapsedSeconds=round(time.monotonic() - start, 1), probe=bool(args.only_frames),
              cinematic=bool(getattr(adapter, 'cinematic', False)),
              limits='Prescribed kinematic motion over canonical geometry; no material, force, friction, electrical or fluid simulation.')
(out / 'render-manifest.json').write_text(json.dumps(record, indent=2) + '\n')
if changed:
    raise RuntimeError('Source changed during render: ' + ', '.join(changed))

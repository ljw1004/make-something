"""Render all four animation-strip inspections with one physical pose and view.

Blender --background --factory-startup --python render_paper_views.py --
  --output DIR [--resolution 960] [--phase -0.8]
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import part_views as V
import paper_views as Q
import bpy
import scene_parts as S
import presentation as P
import picture_drum as D

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--resolution', type=int, default=960)
parser.add_argument('--phase', type=float, default=-.8)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
paths = [Path(__file__), Path(Q.__file__), Path(V.__file__), Path(D.__file__), Path(S.__file__), Path(P.__file__)]
sources_before = {str(p.relative_to(V.repository_root())): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = S.configure_render(args.resolution)
scene.render.threads_mode = 'FIXED'
scene.render.threads = 2
scene.cycles.samples = 24
model = P.build('film')
route = Q.spiral_route(phase=args.phase)
D.set_state(model, 'film-coloured-strip')
Q.apply(model, 'film-coloured-strip', route)
view = V.inspection_view(V.visible_geometry(model), model['flat_view'], (-.2, -1., .9), .85)
V.inspection_lights(scene, view)
scene.camera = S.camera('shared open paper coil inspection', view['location'], view['target'], view['scale'])
records = []
for identity in Q.STRIP_IDS:
    D.set_state(model, identity)
    physical = Q.apply(model, identity, route)
    scene.render.filepath = str(out/(identity+'.png'))
    bpy.ops.render.render(write_still=True)
    records.append({'id': identity, 'view': view, 'pixels': [args.resolution, args.resolution],
                    'physical': physical, 'sharedPaperGroup': list(Q.STRIP_IDS),
                    'sha256': hashlib.sha256((out/(identity+'.png')).read_bytes()).hexdigest()})
    print('PAPER', identity, flush=True)
sources_after = {str(p.relative_to(V.repository_root())): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
if sources_before != sources_after:
    raise ValueError('Paper production source files changed during the run')
(out/'manifest-paper.json').write_text(json.dumps({'images': records, 'sourceFileHashesBefore': sources_before,
                                                  'sourceFileHashesAfter': sources_after}, indent=2)+'\n')
print('Rendered four registered physical paper inspections', flush=True)

"""Render the two new subsets plus baseline proofs with the old camera/rig."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import bpy
import racer_stages as R
import scene_parts as S
from construction_lighting import frame_lights

p=argparse.ArgumentParser();p.add_argument('--output',required=True)
args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=S.configure_render(960)
scene.render.threads_mode='FIXED';scene.render.threads=2;scene.cycles.samples=24
model=R.make();records=[]
for identity in R.STATES:
    view=R.set_stage(model,identity)
    frame_lights(scene,view['scale'])
    camera=S.camera('unchanged racer construction camera',view['location'],view['target'],view['scale'])
    scene.camera=camera
    scene.render.filepath=str(out/(identity+'.png'))
    bpy.ops.render.render(write_still=True)
    records.append({'id':identity,'view':view,'visibleMeshes':[o.name for objects in model['parts'].values() for o in objects if not o.hide_render and o.type=='MESH'],'sha256':hashlib.sha256((out/(identity+'.png')).read_bytes()).hexdigest()})
    bpy.data.objects.remove(camera,do_unlink=True)
(out/'render-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(R.ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [HERE/'racer_stages.py',HERE/'render.py',R.BASE/'wind_toys.py',R.BASE/'presentation.py',R.BASE/'scene_parts.py',R.BASE/'construction.py']},'images':records},indent=2)+'\n')

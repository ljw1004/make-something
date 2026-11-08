"""Render only the three partial folds using the frozen front-view settings.

Blender --background --factory-startup --python render_folds.py -- --output DIR
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import bpy
from mathutils import Vector
import pinwheel as P
import fold_stages as F
import scene_parts as S
sys.path.insert(0,str(HERE.parent))
import materials
materials.apply(S)

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
parser.add_argument('--resolution',type=int,help='Override the production-settings square render size')
parser.add_argument('--samples',type=int,help='Override the production-settings Cycles sample count')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
settings=json.loads((HERE/'production-settings.json').read_text())
assert hashlib.sha256((HERE/'pinwheel.py').read_bytes()).hexdigest()==settings['modelSha256']
resolution=args.resolution if args.resolution is not None else settings['render']['resolution'][0]
samples=args.samples if args.samples is not None else settings['render']['samples']
if resolution<=0 or samples<=0:raise ValueError('Resolution and sample count must be positive')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=S.configure_render(resolution)
scene.view_settings.exposure=settings['render']['exposure']
scene.cycles.samples=samples
scene.render.threads_mode='FIXED';scene.render.threads=2
model=P.make()
view=P.view(model,'front')
camera=S.camera('unchanged front construction camera',**view)
scene.camera=camera
# Exact camera-relative lighting calculation from the frozen renderer.
forward=(Vector(view['location'])-Vector(view['target'])).normalized()
right=camera.rotation_euler.to_matrix()@Vector((1,0,0))
up=camera.rotation_euler.to_matrix()@Vector((0,1,0))
scale=max(.16,view['scale']/.35)
for name,r,u,f,power,size in [('large soft key',-.35,.5,.5,28,.7),('soft fill',.35,.1,.35,16,.5)]:
    light=scene.objects[name]
    light.location=Vector(view['target'])+(right*r+up*u+forward*f)*scale
    light.data.energy=power*scale**2
    light.data.size=size*scale
    S.look_at(light,view['target'])
records=[]
for identity,count in F.FOLDS.items():
    F.set_stage(model,identity)
    scene.render.filepath=str(out/(identity+'.png'))
    bpy.ops.render.render(write_still=True)
    records.append({'id':identity,'completedBlades':count,'view':view,'sha256':hashlib.sha256((out/(identity+'.png')).read_bytes()).hexdigest()})
(out/'render-manifest.json').write_text(json.dumps({'render':{'resolution':[resolution,resolution],'samples':samples,'threads':2,'exposure':scene.view_settings.exposure},'sources':{str(p.relative_to(P.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'pinwheel.py',HERE/'fold_stages.py',HERE/'render_folds.py',HERE/'production-settings.json',HERE.parent/'materials.py',P.BASE/'wind_toys.py',P.BASE/'scene_parts.py']},'images':records},indent=2)+'\n')

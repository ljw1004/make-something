"""Render connected parts and additive states from one dimensioned assembly."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import bpy
from mathutils import Vector, Matrix
import build as R
import scene_parts as S

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--ids');p.add_argument('--resolution',type=int,default=1536);p.add_argument('--samples',type=int,default=24)
args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=S.configure_render(args.resolution);scene.view_settings.exposure=-2.75
scene.render.threads_mode='FIXED';scene.render.threads=2;scene.cycles.samples=args.samples
model=R.build();records=[];done=set()
for identity,info in R.PLAN.items():
    if args.ids and identity not in args.ids.split(','):continue
    if info['image'] in done:continue
    done.add(info['image']);R.set_stage(model,identity)
    view=R.view(model,info);camera=S.camera(identity,view['location'],view['target'],view['scale'])
    camera.rotation_euler=(camera.rotation_euler.to_matrix()@Matrix.Rotation(view['roll'],3,'Z')).to_euler()
    scene.camera=camera
    forward=(Vector(view['location'])-Vector(view['target'])).normalized()
    right=camera.rotation_euler.to_matrix()@Vector((1,0,0));up=camera.rotation_euler.to_matrix()@Vector((0,1,0))
    scale=max(.08,view['scale']/.35)
    for name,r,u,f,power,size in [('large soft key',-.35,.5,.5,28,.7),('soft fill',.35,.1,.35,16,.5)]:
        light=scene.objects[name];light.location=Vector(view['target'])+(right*r+up*u+forward*f)*scale
        light.data.energy=power*scale**2;light.data.size=size*scale;S.look_at(light,view['target'])
    bpy.context.view_layer.update();scene.render.filepath=str(out/(info['image']+'.png'))
    bpy.ops.render.render(write_still=True)
    records.append(dict(id=identity,image=info['image'],parts=info['parts'],view=view,sha256=hashlib.sha256((out/(info['image']+'.png')).read_bytes()).hexdigest()))
    bpy.data.objects.remove(camera,do_unlink=True)
(out/'render-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(R.ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [HERE/'build.py',HERE/'render.py',HERE/'construction-plan.json',HERE.parent/'materials.py',R.BASE/'scene_parts.py',R.BASE/'construction.py']},'images':records},indent=2)+'\n')

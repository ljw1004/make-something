"""Blender --background --factory-startup --python render.py -- --output DIR

Outputs disposable 1536px transparent masters. Production crops come from
export.py; there are no hand-edited raster states.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import pinwheel as P
import bpy
import scene_parts as S
from mathutils import Vector

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
parser.add_argument('--ids',default=','.join(P.STATES))
parser.add_argument('--samples',type=int,default=32)
parser.add_argument('--resolution',type=int,default=1536)
parser.add_argument('--exposure',type=float,default=-2.75)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=S.configure_render(args.resolution)
scene.view_settings.exposure=args.exposure
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.cycles.samples=args.samples
model=P.make()
records=[]
for identity in args.ids.split(','):
    family=P.set_state(model,identity)
    view=P.view(model,family)
    camera=S.camera(identity+' physical view',**view)
    scene.camera=camera
    # Light the currently exposed face from its actual camera side. The same
    # setup remains fixed within each front/rear construction sequence.
    forward=(Vector(view['location'])-Vector(view['target'])).normalized()
    right=camera.rotation_euler.to_matrix() @ Vector((1,0,0))
    up=camera.rotation_euler.to_matrix() @ Vector((0,1,0))
    light_scale=max(.16,view['scale']/.35)
    for name, r, u, f, power, size in [
        ('large soft key',-.35,.5,.5,28,.7),
        ('soft fill',.35,.1,.35,16,.5),
    ]:
        light=scene.objects[name]
        light.location=Vector(view['target'])+(right*r+up*u+forward*f)*light_scale
        light.data.energy=power*light_scale**2
        light.data.size=size*light_scale
        S.look_at(light,view['target'])
    bpy.context.view_layer.update()
    scene.render.filepath=str(out/(identity+'.png'))
    bpy.ops.render.render(write_still=True)
    records.append({'id':identity,'family':family,'view':view,'renderSha256':hashlib.sha256((out/(identity+'.png')).read_bytes()).hexdigest()})
    bpy.data.objects.remove(camera,do_unlink=True)
(out/'render-manifest.json').write_text(json.dumps({'sources':{str(p.relative_to(P.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'pinwheel.py',HERE/'render.py',P.BASE/'wind_toys.py',P.BASE/'scene_parts.py']},'images':records,'checks':P.checks()},indent=2)+'\n')

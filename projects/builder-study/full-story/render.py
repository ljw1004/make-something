"""Strict family renderer: Blender -b --python render.py -- --family NAME --output DIR."""
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import bpy
from mathutils import Vector,Matrix
import core

p=argparse.ArgumentParser();p.add_argument('--family',required=True);p.add_argument('--output',required=True);p.add_argument('--ids');p.add_argument('--resolution',type=int,default=1280);p.add_argument('--samples',type=int,default=24)
args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);module=importlib.import_module(args.family)
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=core.S.configure_render(args.resolution);scene.view_settings.exposure=-2.75
scene.render.threads_mode='FIXED';scene.render.threads=2;scene.cycles.samples=args.samples
model=module.build();done=set();records=[];group_views={}
def source_hashes():
    return {str(Path(m.__file__).resolve().relative_to(core.ROOT)):hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).startswith(str(core.ROOT)) and str(m.__file__).endswith('.py')}
initial_sources=source_hashes()
owned={obj for objects in model['parts'].values() for obj in objects}
unowned=[obj.name for obj in scene.objects if obj.type in {'MESH','CURVE'} and obj not in owned and not obj.hide_render]
if unowned:raise ValueError('Unowned visible model geometry: '+str(unowned))
for identity,info in module.PLAN.items():
    if args.ids and identity not in args.ids.split(','):continue
    filename=info.get('image',identity)
    if filename in done:continue
    done.add(filename);view=module.stage(model,identity)
    actual={key for key,objects in model['parts'].items() if any(not obj.hide_render for obj in objects)}
    if actual!=set(info['parts']):raise ValueError(f'{identity}: visible ownership differs from PLAN: {actual^set(info["parts"])}')
    signature=json.dumps(view,sort_keys=True)
    if info['group'] in group_views and group_views[info['group']]!=signature:raise ValueError(f'{identity}: shared crop group changes camera')
    group_views[info['group']]=signature
    camera=core.S.camera(identity,view['location'],view['target'],view['scale'])
    camera.rotation_euler=(camera.rotation_euler.to_matrix()@Matrix.Rotation(view.get('roll',0),3,'Z')).to_euler();scene.camera=camera
    forward=(Vector(view['location'])-Vector(view['target'])).normalized();right=camera.rotation_euler.to_matrix()@Vector((1,0,0));up=camera.rotation_euler.to_matrix()@Vector((0,1,0));light_scale=max(.08,view['scale']/.35)
    for name,r,u,f,power,size in [('large soft key',-.35,.5,.5,28,.7),('soft fill',.35,.1,.35,16,.5)]:
        light=scene.objects[name];light.location=Vector(view['target'])+(right*r+up*u+forward*f)*light_scale;light.data.energy=power*light_scale**2;light.data.size=size*light_scale;core.S.look_at(light,view['target'])
    bpy.context.view_layer.update();scene.render.filepath=str(out/(filename+'.png'));bpy.ops.render.render(write_still=True)
    records.append(dict(id=identity,image=filename,group=info['group'],css=info['css'],parts=info['parts'],view=view,sha256=hashlib.sha256((out/(filename+'.png')).read_bytes()).hexdigest()))
    bpy.data.objects.remove(camera,do_unlink=True)
sources=source_hashes()
changed=[path for path,digest in initial_sources.items() if sources.get(path)!=digest]
(out/(args.family+'-manifest.json')).write_text(json.dumps(dict(family=args.family,sources=sources,changedSources=changed,selectedIds=args.ids,images=records),indent=2)+'\n')
if changed:raise RuntimeError('Sources changed during render: '+str(changed))

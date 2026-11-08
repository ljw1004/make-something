"""Render the native one-shot ending; Blender -b --python this.py -- --output DIR."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
import core
from ending_scene import Ending

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--frames',type=int,default=150)
p.add_argument('--resolution',type=int,default=390,help='Animation width; height follows the 780 by 1688 instruction page')
p.add_argument('--poster-resolution',type=int,default=780);p.add_argument('--samples',type=int,default=12);p.add_argument('--only-frames')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=core.S.configure_render(args.resolution);scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_y=round(args.resolution*1688/780)
scene.cycles.samples=args.samples;scene.render.use_persistent_data=True;scene.view_settings.exposure=-2.75
ending=Ending();view=ending.view;camera=core.S.camera('one exchange',**view);scene.camera=camera
forward=(Vector(view['location'])-Vector(view['target'])).normalized();right=camera.rotation_euler.to_matrix()@Vector((1,0,0));up=camera.rotation_euler.to_matrix()@Vector((0,1,0));scale=view['scale']/.35
for name,r,u,f,power,size in [('large soft key',-.35,.5,.5,28,.7),('soft fill',.35,.1,.35,16,.5)]:
 light=scene.objects[name];light.location=Vector(view['target'])+(right*r+up*u+forward*f)*scale
 light.data.energy=power*scale**2;light.data.size=size*scale;core.S.look_at(light,view['target'])
def hashes():
 files={Path(__file__).resolve()}
 for module in list(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path and Path(path).is_file() and Path(path).resolve().is_relative_to(core.ROOT):files.add(Path(path).resolve())
 return {str(f.relative_to(core.ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(files)}
sources=hashes();bounds=ending.passage_bounds()
assert bounds['minimum'][0]>-.325 and bounds['maximum'][0]<.325,bounds
assert bounds['minimum'][2]>bounds['aperture']['bottom'] and bounds['maximum'][2]<bounds['aperture']['top'],bounds
indices=[int(i) for i in args.only_frames.split(',')] if args.only_frames else range(args.frames)
for frame in indices:
 ending.pose(frame/(args.frames-1));scene.render.filepath=str(out/f'{frame:04d}.png');bpy.ops.render.render(write_still=True)
 print(f'ENDING {frame+1}/{args.frames}',flush=True)
if not args.only_frames:
 ending.pose(1);scene.render.resolution_x=args.poster_resolution;scene.render.resolution_y=round(args.poster_resolution*1688/780)
 scene.cycles.samples=max(24,args.samples);scene.render.filepath=str(out/'poster.png');bpy.ops.render.render(write_still=True)
changed=[f for f,h in sources.items() if hashes().get(f)!=h]
(out/'manifest.json').write_text(json.dumps(dict(frames=args.frames,fps=15,resolution=args.resolution,size=[args.resolution,round(args.resolution*1688/780)],posterSize=[args.poster_resolution,round(args.poster_resolution*1688/780)],samples=args.samples,sources=sources,changedSources=changed,passage=bounds,probe=bool(args.only_frames)),indent=2)+'\n')
if changed:raise RuntimeError('Sources changed during render: '+str(changed))

"""Three intermediate folding states over the frozen complete pinwheel model.

Paper-local order is upper-right, upper-left, lower-left, lower-right. Every
completed blade has exactly its final mesh; every remaining blade stays flat.
No new geometry, material or physical scale is introduced by this adapter.
"""
import math
import bpy
import pinwheel as P

FOLDS={'pw-one-blade':1,'pw-two-blades':2,'pw-three-blades':3}


def set_stage(model,identity):
    if identity not in FOLDS:raise ValueError('Unknown partial fold '+identity)
    P.set_state(model,'pw-paper')
    count=FOLDS[identity]
    for i,(obj,uv,height) in enumerate(model['paper']):
        folded=i<count
        for vertex,(x,y) in zip(obj.data.vertices,uv):
            vertex.co=P.folded_point(x,y,height,folded)
        x,y,z=P.folded_point(*P.W.HOLE,height,folded)
        angle=i*math.pi/2
        cutter=model['cutters'][i]
        cutter.location=(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z)
        cutter.rotation_euler=(0,0,0)
    bpy.context.view_layer.update()

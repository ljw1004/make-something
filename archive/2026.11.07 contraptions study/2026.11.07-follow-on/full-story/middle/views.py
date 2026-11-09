"""Camera groups include all their eventual geometry, even in early stages."""
import core


def stage_view(model,plan,identity,direction=(.65,-.85,.65),roll=0):
    core.reset_root(model)
    info=core.select(model,plan,identity)
    group=info['group']; cache=model.setdefault('views',{})
    if group not in cache:
        keys={key for entry in plan.values() if entry['group']==group for key in entry['parts']}
        objects=[obj for key in keys for obj in model['parts'][key]]
        lo,hi=core.world_bounds(objects)
        target=tuple((a+b)/2 for a,b in zip(lo,hi))
        scale=max(hi[i]-lo[i] for i in range(3))*1.65
        cache[group]=core.frame(target,max(.035,scale),direction,roll)
    return cache[group]


def curve_points(obj,points):
    obj.data.splines.clear()
    spline=obj.data.splines.new('POLY');spline.points.add(len(points)-1)
    for vertex,point in zip(spline.points,points):vertex.co=(*point,1)

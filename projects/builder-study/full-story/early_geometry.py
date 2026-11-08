"""Local-frame construction cuts and explicit compliant receiving geometry.

All nominal dimensions are metres. These helpers model clear insertion routes;
they do not infer the force or fatigue life of a manufactured snap fitting.
"""
import math


def cut_frame(obj, cutter, frame):
    import bpy, bmesh
    cutter.parent=frame
    bpy.context.view_layer.update()
    for mesh_obj in (obj,cutter):
        bm=bmesh.new();bm.from_mesh(mesh_obj.data)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh_obj.data);bm.free()
    bpy.context.view_layer.objects.active=obj
    modifier=obj.modifiers.new('explicit local-frame receiving clearance','BOOLEAN')
    modifier.operation='DIFFERENCE';modifier.solver='EXACT';modifier.object=cutter
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter,do_unlink=True)


def bore_frame(S,obj,frame,centre,radius,depth,axis='Z'):
    cut_frame(obj,S.cylinder('temporary local bore',centre,radius,depth,'ink',axis),frame)


def slot_frame(S,obj,frame,centre,size):
    cut_frame(obj,S.box('temporary open receiver',centre,size,'ink'),frame)


def half_tube(S,name,centre,outer,inner,length,upper,color='teal',samples=64):
    """A connected Y-axis semicircular shell with a genuinely open mouth."""
    import bpy
    cx,cy,cz=centre
    angles=[(0 if upper else math.pi)+math.pi*i/samples for i in range(samples+1)]
    n=len(angles)
    vertices=[(cx+r*math.cos(a),cy+y,cz+r*math.sin(a))
              for y in (-length/2,length/2) for r in (outer,inner) for a in angles]
    faces=[]
    for i in range(samples):
        j=i+1;faces += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),
                       (i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
    faces += [(0,n,3*n,2*n),(samples,2*n+samples,3*n+samples,n+samples)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    return S.finish(obj,name,color)


def split_barb(S,name,frame,x,z,seat_y,tip_y,radius=.0021,tip_radius=.0012):
    """Two tapered snap legs, joined through the supplied pin's unsplit root."""
    import bpy
    n=48;vertices=[]
    for y,r in ((seat_y,radius),(tip_y,tip_radius)):
        vertices += [(x+r*math.cos(i*math.tau/n),y,z+r*math.sin(i*math.tau/n)) for i in range(n)]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    S.finish(obj,name,'teal');obj.parent=frame
    slot_frame(S,obj,frame,(x,(seat_y+tip_y)/2,z),(.0012,abs(tip_y-seat_y)+.004,.008))
    return obj

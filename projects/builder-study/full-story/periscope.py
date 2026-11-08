"""Connected four-panel net with explicit folds, two mirrors and two shades."""
import math
from early_common import libraries, owned, show, inspection, entry

PLAN={};NAMES={}
def item(identity,name,parts,group=None,css=110,fold=3,ends=3,face='front'):
    NAMES[identity]=name;PLAN[identity]=entry(parts,group or identity,css,fold=fold,ends=ends,face=face)
item('bf-pe-net','Tube net',['body'],css=245,fold=0,ends=0)
for key,name in [('upper','Upper mirror'),('lower','Lower mirror'),('top-shade','Top shade'),('eye-shade','Eye shade')]:
    item('bf-pe-'+key,name,[key])
state=['body'];current='bf-pe-net';steps=[]
rows=[('bf-pe-fold','bf-pe-fold-1','Fold the first side',None,1,0,'front'),
      ('bf-pe-fold','bf-pe-fold-2','Fold the second side',None,2,0,'front'),
      ('bf-pe-fold','bf-pe-tube','Fold and close the long seam',None,3,0,'front'),
      ('bf-pe-flip','bf-pe-rear','Flip to the upper opening',None,3,0,'rear'),
      ('bf-pe-upper','bf-pe-upper-fit','Fit the Upper mirror','upper',3,0,'rear'),
      ('bf-pe-fold','bf-pe-top-closed','Fold the top closed',None,3,2,'rear'),
      ('bf-pe-top-shade','bf-pe-shaded','Fit the Top shade','top-shade',3,2,'rear'),
      ('bf-pe-flip','bf-pe-front','Flip to the lower opening',None,3,2,'front'),
      ('bf-pe-lower','bf-pe-mirrored','Fit the Lower mirror','lower',3,2,'front'),
      ('bf-pe-fold','bf-pe-closed','Fold the bottom closed',None,3,3,'front'),
      ('bf-pe-eye-shade','periscope','Fit the Eye shade','eye-shade',3,3,'front')]
for reagent,result,goal,part,fold,ends,face in rows:
    if part:state=state+[part]
    item(result,'Periscope' if result=='periscope' else 'Tube',state,
         group='pe-paper' if fold<3 else 'pe-'+face if result!='periscope' else result,
         css=350 if result=='periscope' else 245,fold=fold,ends=ends,face=face)
    steps.append((current,reagent,result,goal));current=result
CHAPTERS=[dict(id='bf-pe-build',title='A look over the hedge',reference='periscope',steps=steps,
              processes={'bf-pe-flip':'flip','bf-pe-fold':'fold'})]
DESCRIPTIONS={
 'bf-pe-net':'One scored card net with dark inner faces, two end flaps, mirror ledges and prepared adhesive seam tabs. The end flaps stay open while you fit the mirrors.',
 'bf-pe-upper':'An unbreakable mirror with retained edge clips. It seats on the upper forty-five-degree ledges.',
 'bf-pe-top-shade':'One stepped window hood. Its narrow neck enters the opening while its prepared adhesive flange rests on the card outside.',
 'bf-pe-eye-shade':'A matching stepped hood for the lower window, with prepared adhesive on its outer flange.',
 'bf-pe-lower':'A matching mirror in retained clips. Its reflecting face remains parallel to the upper mirror, redirecting the light towards your eye.',
}

def build():
    S=libraries()
    import optical_toys as source
    m=source.build_periscope();old=m['parts']
    # Matte silver diagram shading keeps a fitted plate visible inside the dark
    # tube; the shared dimensions and mirror planes remain unchanged.
    mirror=next(o for o in old['pe-upper-mirror'] if o.name.startswith('parallel reflecting plate')).data.materials[0]
    shader=mirror.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Metallic'].default_value=.25
    shader.inputs['Roughness'].default_value=.3
    retired=tuple(m['tabs'])+tuple(m['adhesive'])
    parts={'body':[o for o in old['pe-net']+old['pe-lining'] if o not in retired],
           'upper':old['pe-upper-mirror'],'lower':old['pe-lower-mirror'],
           'top-shade':[],'eye-shade':[]}
    # A narrow neck enters the actual window; a wider flange remains outside.
    # The previous full-width sleeve would intersect the card's window margins.
    def shade_box(part,name,centre,size):
        obj=S.box(name,centre,size,'ink');obj.parent=m['root'];parts[part].append(obj)
    def rectangle(part,name,y,z,outer,inner,depth):
        w,h=outer;iw,ih=inner
        for x in (-(w+iw)/4,(w+iw)/4):
            shade_box(part,name+' side',(x,y,z),((w-iw)/2,depth,h))
        for zz in (z-(h+ih)/4,z+(h+ih)/4):
            shade_box(part,name+' edge',(0,y,zz),(iw,depth,(h-ih)/2))
    for part,sign,z in [('eye-shade',-1,.03),('top-shade',1,.27)]:
        rectangle(part,'window shade body',sign*.0363,z,(.059,.059),(.051,.051),.010)
        rectangle(part,'connected stepped flange',sign*.0312,z,(.059,.059),(.0456,.0496),.0008)
        rectangle(part,'clearance insertion neck',sign*.0295,z,(.048,.052),(.0456,.0496),.0032)
        for x in (-.0275,.0275):
            shade_box(part,'prepared adhesive strip',(x,sign*.030775,z),(.004,.00005,.052))
    # A real seam tongue belongs to the final panel and follows its crease.
    seam=S.box('integral adhesive seam tongue',(.063,-.0004,.15),(.006,.0006,.296),'card')
    seam.parent=m['panels'][3];parts['body'].append(seam)
    adhesive=S.box('prepared seam adhesive',(.064,-.0008,.15),(.004,.0002,.292),'paper')
    adhesive.parent=m['panels'][3];parts['body'].append(adhesive)
    m['seam']=seam;m['seam_adhesive']=adhesive
    m['ends']=[o for o in old['pe-net'] if o.name.startswith('tube end flap')]
    m['source']=source
    return owned(m,parts)

def stage(m,identity):
    info=PLAN[identity];fold=info['fold'];ends=info['ends']
    position=(-.03,-.03)
    for i,panel in enumerate(m['panels']):
        angle=min(i,fold)*math.pi/2
        panel.location=(*position,0);panel.rotation_euler=(0,0,angle)
        position=(position[0]+.06*math.cos(angle),position[1]+.06*math.sin(angle))
    for i,flap in enumerate(m['ends']):
        closed=bool(ends&(1<<i))
        flap.location=(0,0,.001 if i==0 else .299) if closed else (0,-.03,-.03 if i==0 else .33)
        flap.rotation_euler=(0,0,0) if closed else (math.pi/2,0,0)
    for obj,flat,closed in [(m['seam'],(.063,-.0004,.15),(.0588,.003,.15)),
                            (m['seam_adhesive'],(.064,-.0008,.15),(.05915,.003,.15))]:
        obj.location=closed if fold==3 else flat
        obj.rotation_euler=(0,0,math.pi/2 if fold==3 else 0)
    show(m,info['parts'])
    if info['group']=='pe-paper':return {'location':(.55,-.85,.50),'target':(.06,0,.15),'scale':.52}
    if info['group']=='pe-rear':return {'location':(-.55,.85,.50),'target':(0,0,.15),'scale':.46}
    if info['group']=='pe-front':return {'location':(.55,-.85,.50),'target':(0,0,.15),'scale':.46}
    return inspection(m,info['parts'],direction=(.55,-.85,.35),margin=1.2)

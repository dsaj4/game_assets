"""Build one continuous rolled-hide mesh, two ties and two full-length staffs."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from md11_tools import *
import random
from mathutils import Quaternion

bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.name='MD11_Native_Source';s.unit_settings.system='METRIC'
col=bpy.data.collections.new('MD-11_ASSET');s.collection.children.link(col)
root=bpy.data.objects.new('MD-11_ROOT',None);col.objects.link(root);root['asset_id']='MD-11'
root['placement']='Horizontal rear ledge; replaces cat position';root.empty_display_size=.06
leather=material('MD11 Worn russet hide',(.16,.07,.025),ROOT/'references/md-11-native/leather-albedo-v01.png')
suede=material('MD11 Suede inner face',(.15,.085,.037));edge=material('MD11 Raw worn edge',(.36,.24,.115))
ink=material('MD11 Deep brown ink',(.035,.014,.005));thread=material('MD11 Old repair thread',(.39,.285,.16))
wood=material('MD11 Honey old wood',(.29,.18,.073));woodlight=material('MD11 Worn wood ridges',(.43,.31,.15))
rng=random.Random(91311)
START=-.26;SPAN=math.tau+.98

def shellp(t,u,lift=0):
    theta=START+u*SPAN
    fold=min(1,t/.044)
    x=-.951+1.902*t
    theta+=.025*math.sin(t*113)+.013*math.sin(t*311)
    ry=.088*(.96+.04*math.sin(math.pi*t));rz=.076*(.97+.03*math.sin(math.pi*t))
    pinch=sum(.095*math.exp(-((t-c)/.011)**2) for c in (.27,.73))
    wrinkle=.0019*math.sin(t*119+theta*3)+.0008*math.sin(t*231-theta*5)
    fold_wave=.009*math.sin(theta*7+fold*2)*(1-fold)
    extra=.0038*max(0,min(1,(theta-math.tau+.22)/.3))
    radial=(1-pinch)*fold
    a=ry*radial+wrinkle*fold+fold_wave+extra*fold+lift
    b=rz*radial+wrinkle*fold+fold_wave+extra*fold+lift
    if t<.044:x=-.948-.011*math.sin(math.pi*fold)+.075*fold
    if t>.98:x+=.0045*math.sin(theta*9)*(t-.98)/.02
    z=.076+b*math.sin(theta);z=max(.003+lift,z)
    return Vector((x,-a*math.cos(theta),z))

# One connected quad sheet, with an integral pleated fold at its left boundary.
NX=176;NU=90
verts=[(-.951,0,.076)];uvs=[(0,.5)]
for i in range(1,NX+1):
    for j in range(NU+1):
        t=i/NX;u=j/NU;verts.append(shellp(t,u));uvs.append((t*3.1,u))
faces=[(0,1+j,2+j) for j in range(NU)]
for i in range(NX-1):
    for j in range(NU):
        a=1+i*(NU+1)+j;b=a+NU+1;faces.append((a,b,b+1,a+1))
body=mesh('MD11_LeatherBody_SINGLE_CONTINUOUS_HIDE',verts,faces,leather,col,root,uvs,True)
body.data.materials.append(suede);body.data.materials.append(edge)
body['construction']='One connected surface, overlapping free edge and integral pleated fold; no separate end cap'
body['length_target_m']=1.90
sol=body.modifiers.new('Leather thickness 3mm','SOLIDIFY');sol.thickness=.003;sol.offset=-.5;sol.material_offset=1;sol.material_offset_rim=2
paths=[[shellp(i/250,1,.0006) for i in range(12,251)], [shellp(1,j/120,.0006) for j in range(121)]]
curves('MD11_Frayed_overlap_and_mouth',paths,.0011,edge,col,root)
curves('MD11_Overlap_shadow',[[shellp(i/240,.979,.0005) for i in range(12,241)]],.00055,ink,col,root)
stitches=[]
for k in range(135):
    t=.06+k*.0068
    stitches.append([shellp(t+dt,.974+du,.0019) for dt,du in ((-.0019,-.009),(0,-.003),(.0019,.003))])
curves('MD11_Editable_edge_repair_stitches',stitches,.00062,thread,col,root)
creasepaths=[]
for k in range(100):
    t=rng.uniform(.075,.97);u=rng.uniform(.01,.98)
    creasepaths.append([shellp(t+q*.0025,u+math.sin(q*1.6+k)*.006,.0018) for q in range(5)])
curves('MD11_Seated_fine_crazing',creasepaths,.00023,ink,col,root)

def outer_at(t,theta,lift):
    if theta<START+.98:theta+=math.tau
    return shellp(t,(theta-START)/SPAN,lift)

for n,t in enumerate((.27,.73)):
    tie_root=bpy.data.objects.new('MD11_TIE_'+('A' if n==0 else 'B'),None);col.objects.link(tie_root);tie_root.parent=root
    tie_root['part_role']='One of exactly two leather bindings';tie_root.empty_display_size=.012
    vs=[];uv=[];N=112
    for k in range(N):
        theta=START+math.tau*k/N
        for side in (-1,1):
            p=outer_at(t+side*.006,theta,.0039);vs.append(p);uv.append((k/N,0 if side<0 else .065))
    fs=[(2*k,2*((k+1)%N),2*((k+1)%N)+1,2*k+1) for k in range(N)]
    band=mesh('MD11_Tie_band_'+str(n),vs,fs,leather,col,tie_root,uv,True)
    thick=band.modifiers.new('Tie leather thickness','SOLIDIFY');thick.thickness=.0023
    knot=outer_at(t,.43,.010)
    loops=[]
    for ring in range(3):
        loops.append([knot+Vector((.012*math.cos(math.tau*k/32),-.006*math.sin(math.tau*k/32)-ring*.0015,(ring-1)*.005+.006*math.sin(math.tau*k/32))) for k in range(33)])
    curves('MD11_Tie_square_knot_'+str(n),loops,.0038,leather,col,tie_root)
    for sign in (-1,1):
        centers=[knot+Vector((sign*(.007+.019*q/5),-.004-.012*q/5,-.067*q/5)) for q in range(6)]
        verts=[];uv=[]
        for i,c in enumerate(centers):
            for side in (-1,1):verts.append(c+Vector((side*.0055,0,0)));uv.append((i/6,0 if side<0 else .04))
        fs=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(5)]
        tail=mesh('MD11_Tie_loose_tail',verts,fs,leather,col,tie_root,uv,True)
        so=tail.modifiers.new('Tail thickness','SOLIDIFY');so.thickness=.0018
        curves('MD11_Tail_raw_edge',[[c+Vector((side*.0057,-.0005,0)) for c in centers] for side in (-1,1)],.0006,edge,col,tie_root)

def shaft(groupname,loc,ring=False):
    g=bpy.data.objects.new(groupname,None);col.objects.link(g);g.parent=root;g.location=loc;g.empty_display_size=.04
    g['part_role']='Full solid wooden staff, independently editable'
    length=2.06 if ring else 2.20
    centers=[];radii=[]
    for i in range(49):
        x=length*i/48;y=.0018*math.sin(x*9);z=.003*math.sin(x*6)
        centers.append((x,y,z));radii.append(.013+.0027*i/48+.0018*math.sin(x*11)**6)
    tube(groupname+'_shaft',centers,radii,wood,col,g)
    grain=[]
    for j in range(12):
        a=math.tau*j/12
        grain.append([(x,y+(r+.00035)*math.cos(a+.03*math.sin(x*15+j)),z+(r+.00035)*math.sin(a+.03*math.sin(x*15+j))) for (x,y,z),r in zip(centers,radii)])
    curves(groupname+'_grain',grain,.00023,ink,col,g)
    if ring:
        c=Vector((2.095,0,.008));a=.040
        circle=[c+Vector((a*math.cos(math.tau*k/56),0,a*math.sin(math.tau*k/56))) for k in range(57)]
        tube('MD11_Ring_head',circle,[.008]*len(circle),wood,col,g,10)
        curves('MD11_Ring_carved_ridge',[[c+Vector((r*math.cos(math.tau*k/64),-.0068,r*math.sin(math.tau*k/64))) for k in range(65)] for r in (.035,.044)],.00055,woodlight,col,g)
        for x in (1.94,1.955,2.01):
            curves('MD11_Ring_shaft_collar',[[(x,.018*math.cos(math.tau*k/32),.018*math.sin(math.tau*k/32)) for k in range(33)]],.0025,wood,col,g)
    else:
        tube('MD11_Fork_upper_branch',[(1.91,0,0),(1.99,.002,.027),(2.05,.006,.057),(2.09,.012,.069)],[.017,.015,.012,.009],wood,col,g)
        tube('MD11_Fork_lower_branch',[(1.97,0,0),(2.06,-.004,-.026),(2.14,-.011,-.049)],[.017,.013,.009],wood,col,g)
        curves('MD11_Fork_branch_cuts', [[(1.94,-.014,.009),(2.005,-.011,.036),(2.076,-.001,.068)],[(1.995,-.018,-.003),(2.061,-.018,-.023),(2.133,-.019,-.047)]],.0008,ink,col,g)
        for xx in (1.87,1.98,2.13):
            curves('MD11_Fork_knot_eye',[[(xx+.016*math.cos(math.tau*k/28),-.0165,.006*math.sin(math.tau*k/28)) for k in range(29)]],.00075,ink,col,g)
    return g

fork=shaft('MD11_STAFF_FORK',(-.9,.023,.102))
ring=shaft('MD11_STAFF_RING',(-.9,-.030,.054),True)
root['body_length_m']=1.90;root['staff_fork_length_m']=2.20;root['staff_ring_length_m']=2.143
cam=rig(s)
bpy.ops.object.select_all(action='DESELECT');fork.select_set(True);bpy.context.view_layer.objects.active=fork
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_perspective='CAMERA'
            a.spaces.active.show_region_ui=True
pack_images();OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'md11-generated.blend'),compress=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'md11-source.blend'),compress=True)
s.render.filepath=str(OUT/'renders/first-pass.png');bpy.ops.render.render(write_still=True)
print('MD11 BUILT',len(col.objects),'objects',flush=True)

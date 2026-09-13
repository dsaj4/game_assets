"""E1 native asset source. Blender 4.5 bpy + bundled numpy, no downloaded art.
Run through tools/build-e1.ps1. All coordinates are Blender Z-up metres.
"""
from pathlib import Path
import bpy, math, random, json, hashlib
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/e1'
ASSETS = ROOT / 'game/assets/e1'
EVIDENCE = ROOT / 'artifacts/ui-experiment/E1'
for p in (ART, ASSETS, EVIDENCE): p.mkdir(parents=True, exist_ok=True)
random.seed(41)
bpy.ops.wm.read_factory_settings(use_empty=True)

def stroke(a, points, color, radius=1, alpha=1):
    h,w,_=a.shape
    for (x,y),(xx,yy) in zip(points,points[1:]):
        n=max(2,int(max(abs(xx-x),abs(yy-y))*1.5))
        xs=np.linspace(x,xx,n).astype(int); ys=np.linspace(y,yy,n).astype(int)
        for dx in range(-radius,radius+1):
            for dy in range(-radius,radius+1):
                if dx*dx+dy*dy>radius*radius: continue
                ix=np.clip(xs+dx,0,w-1); iy=np.clip(ys+dy,0,h-1)
                a[iy,ix,:3]=a[iy,ix,:3]*(1-alpha)+np.array(color)*alpha

def texture(kind, ink):
    w,h=(1536,192) if kind=='wood' else (1024,1024)
    rng=np.random.default_rng(96)
    y,x=np.mgrid[0:h,0:w]; u=x/w; v=y/h
    noise=rng.normal(0,.011,(h,w))
    if kind=='wood':
        grain=np.sin(v*22+np.sin(u*19)*.8+np.sin(u*5+v*7)*2)
        tone=noise+grain*.010+np.sin(u*9+v*4)*.025
        rgb=np.array([.34,.32,.235])
    else:
        edge=np.minimum.reduce([u,1-u,v,1-v])
        tone=noise*.5-.13*np.exp(-edge*35)+.017*np.sin(u*12)*np.sin(v*7)
        rgb=np.array([.81,.775,.60])
    a=np.ones((h,w,4),dtype=np.float32)
    a[:,:,:3]=rgb+tone[:,:,None]
    if ink and kind=='wood':
        # Long wandering cuts, sparse highlights and elongated knots, fixed in UV.
        for k in range(48):
            y0=random.uniform(5,h-5); x0=random.uniform(0,w)
            length=random.uniform(40,650)
            pts=[(x0+t*length,y0+3*math.sin(t*7+k)+6*math.sin((x0+t*length)/160+k)) for t in np.linspace(0,1,40)]
            stroke(a,pts,(.06,.07,.045),random.choice([0,1,1]),random.uniform(.55,.9))
        for cx,cy in [(330,50),(1080,130)]:
            for r in [6,10,16,23,31,41,52]:
                pts=[(cx+2.6*r*math.cos(t)*(1+.035*math.sin(t*7)),cy+r*.6*math.sin(t)) for t in np.linspace(0,math.tau,130)]
                stroke(a,pts,(.08,.09,.06),1,.65)
        for k in range(150):
            px=random.randrange(w); py=random.randrange(h)
            stroke(a,[(px,py),(px+random.randint(6,22),py+random.randint(8,16))],(.10,.11,.08),0,.5)
    if ink and kind!='wood':
        for margin in [27,33]:
            pts=[]
            for x0,y0,x1,y1 in [(margin,margin,w-margin,margin),(w-margin,margin,w-margin,h-margin),(w-margin,h-margin,margin,h-margin),(margin,h-margin,margin,margin)]:
                pts.extend([(x0+(x1-x0)*t+1.2*math.sin(t*90),y0+(y1-y0)*t+1.5*math.sin(t*80)) for t in np.linspace(0,1,180)])
            stroke(a,pts+[pts[0]],(.23,.235,.17),1,.8)
        for k in range(500):
            px=random.randrange(w); py=random.randrange(h)
            if min(px,w-px,py,h-py)<60:
                stroke(a,[(px,py),(px+random.randint(2,8),py+random.randint(4,14))],(.33,.32,.23),0,.3)
    if kind=='map' and ink:
        # Ornament only: no gameplay edges or extra encounter nodes.
        for row in range(3):
            for col in range(7):
                px=85+col*130+random.uniform(-20,20); py=130+row*100
                height=random.uniform(40,90)
                stroke(a,[(px-40,py),(px,py+height),(px+45,py+3)],(.30,.33,.25),1,.6)
                for j in range(7):
                    t=j/8
                    stroke(a,[(px-36+t*36,py+t*height),(px-13+t*20,py+t*height-10)],(.32,.34,.26),0,.5)
        for px,py in [(120,690),(180,740),(870,650),(820,720),(870,780),(180,620),(790,390)]:
            stroke(a,[(px,py-20),(px,py+55)],(.24,.29,.21),1,.65)
            for j in range(4):
                z=py+j*10
                stroke(a,[(px-22+j*4,z),(px,z+25),(px+22-j*4,z)],(.24,.29,.21),1,.65)
        # Compass rose at lower left.
        cx,cy=120,500
        for j in range(8):
            t=j*math.pi/4
            stroke(a,[(cx,cy),(cx+36*math.cos(t),cy+36*math.sin(t))],(.29,.31,.22),1,.8)
    a[:,:,:3]=np.clip(a[:,:,:3],0,1)
    image=bpy.data.images.new(f'{kind}_{"ink" if ink else "base"}',width=w,height=h)
    image.pixels.foreach_set(a.ravel())
    image.filepath_raw=str(ART/(image.name+'.png')); image.file_format='PNG'; image.save()
    return image

textures={(k,ink):texture(k,ink) for k in ['wood','paper','map'] for ink in [False,True]}
textured=[]; outline_materials=[]

def mat(name,color,kind=None,metal=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=.92; bs.inputs['Metallic'].default_value=metal
    if kind:
        tex=m.node_tree.nodes.new('ShaderNodeTexImage'); tex.image=textures[kind,True]
        m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']); textured.append((tex,kind))
    return m

wood=mat('Etched olive wood',(.29,.26,.18),'wood')
paper=mat('Quiet parchment',(.8,.76,.58),'paper')
mapmat=mat('Etched map parchment',(.8,.76,.58),'map')
dark=mat('Charcoal contours',(.018,.023,.016)); outline_materials.append(dark)
bark=mat('Wand bark',(.16,.105,.057),'wood')
gold=mat('Aged brass',(.36,.265,.105),metal=.16)
stone=mat('Warm stone',(.35,.36,.265))
roof=mat('Faded plum cloth',(.16,.10,.18))
green=mat('Fixed emerald inlay',(.15,.49,.055))
green.node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(.08,.19,.025,1)
green.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=.3
shine=mat('Inlay pale facets',(.65,.85,.33))

def assign(ob,m): ob.data.materials.append(m); return ob

def line(name,points,radius=.015,material=dark):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.resolution_u=2
    c.bevel_depth=radius; c.bevel_resolution=0
    s=c.splines.new('POLY'); s.points.add(len(points)-1)
    for p,v in zip(s.points,points): p.co=(*v,1)
    o=bpy.data.objects.new(name,c); bpy.context.collection.objects.link(o); assign(o,material)
    return o

def cube(name,loc,scale,material,bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    # All major faces use unit UVs so one texture can be regenerated independently.
    uv=o.data.uv_layers.active
    for p in o.data.polygons:
        axis=max(range(3),key=lambda i:abs(p.normal[i])); axes=[i for i in range(3) if i!=axis]
        for li in p.loop_indices:
            co=o.data.vertices[o.data.loops[li].vertex_index].co
            uv.data[li].uv=(co[axes[0]]/scale[axes[0]]+.5,co[axes[1]]/scale[axes[1]]+.5)
    assign(o,material)
    if bevel: b=o.modifiers.new('Worn corners','BEVEL'); b.width=bevel; b.segments=1
    return o

def plank(name,x,y,w,h,z=.05,rot=0):
    o=cube(name,(x,y,z),(w,h,.28),wood,.055); o.rotation_euler.z=rot
    offset=random.random()*.22
    for uv in o.data.uv_layers.active.data: uv.uv.x=uv.uv.x*.76+offset
    for offset in [-h*.42,h*.42]:
        pts=[]
        for j in range(28):
            xx=-w*.47+j*w*.94/27; yy=offset+.014*math.sin(j*1.3+x)
            pts.append((x+xx*math.cos(rot)-yy*math.sin(rot),y+xx*math.sin(rot)+yy*math.cos(rot),z+.16))
        line(name+' edge',pts,.012)
    return o

def anchor(name,loc):
    ob=bpy.data.objects.new(name,None); ob.location=loc; bpy.context.collection.objects.link(ob)

def parchment(name,cx,cy,w,h,material,z=.45):
    nx,ny=16,18; verts=[]; faces=[]
    for j in range(ny+1):
        for i in range(nx+1):
            u=i/nx; v=j/ny
            edge=min(u,1-u,v,1-v)
            xx=(u-.5)*w; yy=(v-.5)*h
            if i in (0,nx): xx+=random.uniform(-.035,.035)
            if j in (0,ny): yy+=random.uniform(-.04,.04)
            zz=z+.018*math.sin(i*.7+j)+.07*math.exp(-edge*36)*math.sin(j*.5+1)
            verts.append((cx+xx,cy+yy,zz))
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i; faces.append((a,a+1,a+nx+2,a+nx+1))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    for poly in mesh.polygons: poly.use_smooth=True
    uv=mesh.uv_layers.new()
    for p in mesh.polygons:
        for li in p.loop_indices:
            vi=mesh.loops[li].vertex_index; uv.data[li].uv=((vi%(nx+1))/nx,(vi//(nx+1))/ny)
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o); assign(o,material)
    s=o.modifiers.new('Paper thickness','SOLIDIFY'); s.thickness=.028
    boundary=[verts[i] for i in range(nx+1)]+[verts[j*(nx+1)+nx] for j in range(1,ny+1)]+[verts[ny*(nx+1)+i] for i in range(nx-1,-1,-1)]+[verts[j*(nx+1)] for j in range(ny-1,-1,-1)]
    line(name+' cut edge',[(x,y,z+.005) for x,y,z in boundary],.013)
    return o

# One cropped cabinet section, with a low-relief work surface.
cube('Backdrop',(0,0,-.35),(17,8.5,.3),dark,.08)
for j in range(10): plank('Backboard',0,-3.55+j*.79,16,.76,-.12,random.uniform(-.002,.002))
plank('Top frame',0,3.55,16.9,.55,.32,-.005)
plank('Bottom frame',0,-3.55,16.9,.6,.32,.006)
plank('Left frame',-8.1,0,7.4,.56,.32,math.pi/2)
plank('Right frame',8.1,0,7.4,.56,.32,math.pi/2)
plank('Middle rail',.7,0,6.6,.32,.25,math.pi/2)
plank('Wand shelf',-3.7,-1.2,7.9,.4,.42)
for x in [-7.85,7.85]:
    for y in [-3.4,3.4]:
        cube('Iron corner plate',(x,y,.53),(.47,.56,.06),dark,.045)
        for dy in [-.15,.15]:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.07,location=(x,y+dy,.61)); assign(bpy.context.object,gold)

# Two paper word tags; UI text is deliberately absent from every texture.
for name,x in [('TagAcquire',-5.4),('TagArmor',-2.8)]:
    parchment(name,x,1.05,2.14,1.85,paper,.47)
    line('Tag cord',[(x,2.22,.34),(x-.07,1.92,.59),(x+.03,1.76,.59)],.024,gold)
    anchor(name+'Text',(x,1.07,.53))

# Irregular tapered shaft, with explicit UVs and hand-cut angular cross section.
verts=[]; faces=[]; n,rings=45,9
for i in range(n):
    t=i/(n-1); x=-7.05+t*5.85; rad=.075+.095*t
    for j in range(rings):
        a=j/rings*math.tau
        verts.append((x,-.30+.045*math.sin(t*22)+rad*math.sin(a),.85+.03*math.sin(t*17)+rad*math.cos(a)))
for i in range(n-1):
    for j in range(rings): faces.append((i*rings+j,i*rings+(j+1)%rings,(i+1)*rings+(j+1)%rings,(i+1)*rings+j))
faces.extend([tuple(range(rings-1,-1,-1)),tuple((n-1)*rings+j for j in range(rings))])
mesh=bpy.data.meshes.new('Wand shaft'); mesh.from_pydata(verts,[],faces); mesh.update(); uv=mesh.uv_layers.new()
for p in mesh.polygons:
    for li in p.loop_indices:
        idx=mesh.loops[li].vertex_index; uv.data[li].uv=((idx//rings)/(n-1),(idx%rings)/rings)
o=bpy.data.objects.new('OneWand',mesh); bpy.context.collection.objects.link(o); assign(o,bark)
for sign in [-1,1]:
    line('Shaft ink edge',[(x,y+sign*.12,z+.09) for x,y,z in [(-7.05+t*5.85,-.30+.045*math.sin(t*22),.86+.03*math.sin(t*17)) for t in np.linspace(0,1,60)]],.017)
for phase in [0,math.pi]:
    pts=[(-6.8+t*5.4,-.30+(.10+t*.08)*math.sin(t*24+phase),.85+(.10+t*.08)*math.cos(t*24+phase)) for t in np.linspace(0,1,130)]
    line('Spiral carved vine',pts,.035,gold)
for x in [-6.3,-1.65]:
    cube('Wand support',(x,-.30,.47),(.3,.7,.5),wood,.07)

# Fixed inlay is physically at the end of the only wand, not a word card.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.49,location=(-.87,-.30,.91)); gem=bpy.context.object; gem.name='FixedInlay'; gem.scale=(1.05,.73,.7); assign(gem,green)
gem.data.materials.append(shine)
for poly in gem.data.polygons:
    if poly.normal.z>.5 and poly.center.x<0: poly.material_index=1
for radius in [.46,.56]:
    line('Inlay socket',[( -.87+radius*math.cos(t),-.30+radius*.73*math.sin(t),.88+.05*math.sin(t*3)) for t in np.linspace(0,math.tau,65)],.048,gold)
line('Inlay highlight',[(-1.07,-.34,1.24),(-.87,-.12,1.25),(-.70,-.30,1.24)],.024,shine)
anchor('InlayCaption',(-1.1,-1.65,.7))
anchor('WandCaption',(-4.8,-2.15,.5))

# One paper map and exactly one encounter miniature (a crooked watchtower).
parchment('MapPaper',4.35,0,5.65,6.1,mapmat,.48)
anchor('MapTitle',(4.35,2.32,.57))
anchor('MapCaption',(4.35,-2.45,.56))
bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.85,depth=.14,location=(4.3,-.2,.66)); assign(bpy.context.object,gold); bpy.context.object.name='EncounterTokenBase'
bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.71,depth=.16,location=(4.3,-.2,.79)); assign(bpy.context.object,stone)
cube('Tower',(4.3,-.2,1.36),(.8,.78,1.1),stone,.045)
cube('Door',(4.3,-.601,1.12),(.29,.025,.5),dark,.06)
for z in [1.0,1.26,1.53,1.78]:
    line('Stone courses',[(3.90,-.603,z),(4.70,-.603,z)],.012)
    line('Stone courses',[(3.889,-.6,z),(3.889,.18,z)],.012)
for x,z in [(4.10,1.14),(4.47,1.40),(4.19,1.66)]:
    line('Stone joints',[(x,-.608,z-.1),(x,-.608,z+.1)],.012)
bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.81,radius2=.06,depth=.85,location=(4.3,-.2,2.22),rotation=(0,.06,math.pi/4)); assign(bpy.context.object,roof); bpy.context.object.name='TowerRoof'
for x in [-.46,-.23,0,.23,.46]:
    line('Roof hatch',[(4.3+x,-.78,1.82),(4.36+x*.15,-.30,2.57)],.012)
line('Finial',[(4.36,-.2,2.58),(4.39,-.2,2.92)],.027,gold)
anchor('EncounterCaption',(4.3,-1.35,.75))

# Camera is exported in both GLBs: Godot uses its actual transform and lens.
bpy.ops.object.camera_add(location=(0,-5.6,17.5)); camera=bpy.context.object; camera.name='E1Camera'
camera.rotation_euler=(Vector((0,0,.2))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO'; camera.data.ortho_scale=18.6; bpy.context.scene.camera=camera
for name,loc,energy,size in [('Key',(-5,-3,10),1500,8),('Fill',(6,2,8),650,7)]:
    bpy.ops.object.light_add(type='AREA',location=loc); light=bpy.context.object; light.name=name
    light.data.energy=energy; light.data.shape='DISK'; light.data.size=size
    light.rotation_euler=(Vector((0,0,0))-light.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=24
scene.render.resolution_x=1920; scene.render.resolution_y=1080; scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Warm ambient'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.19,.21,.17,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='Standard'; scene.view_settings.look='Medium High Contrast'; scene.view_settings.exposure=0
stats={}
for ink in [False,True]:
    variant='ink' if ink else 'base'
    for node,kind in textured: node.image=textures[kind,ink]
    dark.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=((.018,.023,.016,1) if ink else (.10,.105,.07,1))
    path=ASSETS/f'e1_{variant}.glb'
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',export_cameras=True,export_lights=False,export_apply=True)
    scene.render.filepath=str(EVIDENCE/f'blender-{variant}-1080.png'); bpy.ops.render.render(write_still=True)
    stats[variant]={'glb_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
# Pack textures so the editable master is self-contained, retain external PNG sources too.
bpy.ops.file.pack_all(); bpy.ops.wm.save_as_mainfile(filepath=str(ART/'e1-style-master.blend'))
deps=bpy.context.evaluated_depsgraph_get(); triangles=0; mesh_objects=0
for o in scene.objects:
    if o.type not in {'MESH','CURVE'}: continue
    evaluated=o.evaluated_get(deps); mesh=evaluated.to_mesh(); mesh.calc_loop_triangles()
    triangles+=len(mesh.loop_triangles); mesh_objects+=1; evaluated.to_mesh_clear()
stats.update(seed=41,mesh_objects=mesh_objects,triangles=triangles,camera=list(camera.location),ortho_width=18.6,
             content={'wands':1,'fixed_inlays':1,'word_tags':2,'maps':1,'encounter_tokens':1},
             texture_dimensions={'wood':[1536,192],'paper':[1024,1024],'map':[1024,1024]},
             provenance='Procedural original geometry and pixels from art/build_e1.py; no reference pixels imported.')
(ART/'asset-manifest.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('E1_ASSETS_READY '+json.dumps(stats))

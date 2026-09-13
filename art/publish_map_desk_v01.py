"""Refine the saved native UI source, write nine .blend/.glb assets and renders.

This always starts from map-desk-ui.blend, so the actual UI hinge edit survives.
Run in a separate background Blender. Does not alter E1 or any runtime scene.
"""
from pathlib import Path
import bpy
import math
import random
import json
import hashlib
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/map-desk-v01'
UI=OUT/'map-desk-ui.blend'
PARTS=OUT/'assets'
RENDERS=OUT/'renders'
for p in (PARTS,RENDERS):p.mkdir(parents=True,exist_ok=True)
rng=random.Random(130926)
C=.01
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

bpy.ops.wm.open_mainfile(filepath=str(UI))
assembly=bpy.context.scene
hinge=bpy.data.objects['MD08_LID_HINGE']
hinge_angle=math.degrees(hinge.rotation_euler.x)
assert abs(hinge_angle+60)<.01,('Native UI hinge edit missing',hinge_angle)
hinge_matrix=[list(row) for row in hinge.matrix_local]
assert not any(o.name.startswith('MD-09') for o in assembly.objects)

def attach(o,col,parent,material):
    for old in list(o.users_collection):old.objects.unlink(o)
    col.objects.link(o);o.parent=parent
    o.data.materials.append(material)
    return o

def stroke(name,pts,radius,material,col,parent,closed=False):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=radius*C;d.bevel_resolution=0
    s=d.splines.new('POLY');s.points.add(len(pts)-1);s.use_cyclic_u=closed
    for p,v in zip(s.points,pts):p.co=(*tuple(Vector(v)*C),1)
    o=bpy.data.objects.new(name,d);return attach(o,col,parent,material)

def simple_mat(name,color,metal=0):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
    bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=.85
    return m

ink=bpy.data.materials['Charcoal ink'];brass=bpy.data.materials['Aged brass']
gold=bpy.data.materials['Dull gold'];bone=bpy.data.materials['Pale carved wood']

# Replace the conspicuous gold underfill by shadow, and cover it with seated coins.
chest=bpy.data.collections['MD-08_Coin_chest'];cr=bpy.data.objects['MD-08_ROOT']
under=bpy.data.objects['Chest_Gold_underfill']
under.location.z-=.03
under.data.materials.clear();under.data.materials.append(simple_mat('Deep coin-pile shadow',(.067,.049,.017)))
for old in list(chest.objects):
    if old.name.startswith(('Chest_Coin_','Chest_Coin_emboss')):
        bpy.data.objects.remove(old,do_unlink=True)
for j in range(8):
    for i in range(13):
        x=-18.4+i*3.03+rng.uniform(-.24,.24);y=-10.4+j*2.96+rng.uniform(-.22,.22)
        z=15.1+.9*math.sin(i*1.2+j*.9)+.2*(1-abs(x)/20)
        r=rng.uniform(1.48,1.68)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r*C,depth=.27*C,location=Vector((x,y,z))*C)
        coin=bpy.context.object;coin.name='Chest_Seated_Coin_%02d_%02d'%(j,i)
        attach(coin,chest,cr,gold)
        coin.rotation_euler=(rng.uniform(-.16,.16),rng.uniform(-.16,.16),rng.uniform(0,math.tau))
        b=coin.modifiers.new('Coin rolled edge','BEVEL');b.width=.035*C;b.segments=1
        pts=[(r*.78*math.cos(a),r*.78*math.sin(a),.17) for a in [math.tau*k/24 for k in range(24)]]
        stroke('Coin_embossed_ring',pts,.04,brass,chest,coin,True)
        for sign in (-1,1):stroke('Coin_mint_cut',[(-.4,sign*.16,.174),(.4,sign*.16,.174)],.035,brass,chest,coin)

# Leaf-shaped feather silhouettes with proper lanceolate edges and real quills.
desk=bpy.data.collections['MD-01_Desk_and_clutter'];dr=bpy.data.objects['MD-01_ROOT']
for o in list(desk.objects):
    if o.name.startswith(('Quill_feather','Quill_barbs','Quill_spine')):bpy.data.objects.remove(o,do_unlink=True)
for q,(base,tip,width) in enumerate((((-92,66,13),(-98,67,43),2.2),((-89,66,13),(-83,67,48),2.6),((-87,66,13),(-80,65,38),2.0))):
    a,b=Vector(base),Vector(tip);direction=b-a;right=Vector((direction.z,0,-direction.x)).normalized()
    pts=[]
    for sign,ts in ((1,[k/16 for k in range(17)]),(-1,[k/16 for k in range(16,-1,-1)])):
        for t in ts:
            v=a.lerp(b,t)+right*(sign*width*math.sin(math.pi*t)**.8);pts.append(tuple(v))
    d=bpy.data.meshes.new('Feather_blade');d.from_pydata([tuple(Vector(p)*C) for p in pts],[],[tuple(range(len(pts)))])
    d.update();o=bpy.data.objects.new('Quill_Leaf_%d'%q,d);attach(o,desk,dr,bone)
    stroke('Quill_leaf_ink',pts,.035,ink,desk,dr,True)
    stroke('Quill_true_spine',[a,b],.11,bone,desk,dr)
    for k in range(3,15):
        t=k/16;v=a.lerp(b,t);v.y-=.05
        for sign in (-1,1):
            end=v+right*(sign*width*math.sin(math.pi*t)*.94)-direction*.045
            stroke('Quill_fine_barb',[v,end],.029,ink,desk,dr)

# Weather the previously plain leather with localized cracks and edge stitching.
books=bpy.data.collections['MD-10_Old_books']
for index,length,width,z,thick in ((0,30,22,15.5,7.5),(1,33,23,8,7.5),(2,34,25,0,8)):
    parent=bpy.data.objects['Book_%d_ROOT'%index]
    zz=z+thick+.038
    for sign in (-1,1):
        for k in range(30):
            x=-length/2+1.3+k*(length-2.6)/29;y=sign*(width/2-1.25)
            stroke('Book_Edge_stitch',[(x-.12,y-.16,zz),(x+.12,y+.16,zz)],.027,brass,books,parent)
    for k in range(48):
        sign=-1 if k%2 else 1;x=rng.uniform(-length/2+1.5,length/2-1.5);y=sign*rng.uniform(width*.30,width*.44)
        stroke('Book_Leather_crazing',[(x,y,zz),(x+.2,y+.35,zz),(x+.05,y+.75,zz),(x+.25,y+1.1,zz)],.024,ink,books,parent)

# Round tapered beard locks and keep all robe engraving on the carved surface.
mage=bpy.data.collections['MD-04_Mage_woodcarving'];mr=bpy.data.objects['MD-04_ROOT']
for old in list(mage.objects):
    if old.name.startswith(('Mage_Beard_lock','Beard_engraved_fibre','Mage_Robe_knife_cut')):bpy.data.objects.remove(old,do_unlink=True)
for i in range(9):
    x=-1.55+i*.3875;end=5.25+abs(x)*1.30+(i%3)*.13
    rings=[(x,-2.36,10.55+(.2 if i%2 else 0),.47,.28),(x*.97,-2.52,9.35,.54,.39),(x*.77,-2.44,7.6+abs(x)*.8,.36,.31),(x*.51,-2.25,end,.025,.025)]
    verts=[];n=8
    for xx,yy,zz,rx,ry in rings:
        verts.extend([(xx+rx*math.cos(math.tau*k/n),yy+ry*math.sin(math.tau*k/n),zz) for k in range(n)])
    faces=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(3) for k in range(n)]+[tuple(range(24,32))]
    d=bpy.data.meshes.new('Carved_beard_lock');d.from_pydata([tuple(Vector(p)*C) for p in verts],[],faces);d.update()
    o=bpy.data.objects.new('Mage_Carved_beard_%02d'%i,d);attach(o,mage,mr,bone)
    stroke('Beard_surface_cut',[(xx,yy-ry-.014,zz) for xx,yy,zz,rx,ry in rings],.016,ink,mage,mr)
for i in range(12):
    a=math.tau*i/12;pts=[]
    for j in range(9):
        z=1.5+j*.9
        if z<=4:
            t=(z-1.3)/2.7;rx=3.4-.3*t;ry=2.8-.3*t;cy=.1*t
        else:
            t=(z-4)/5;rx=3.1-.3*t;ry=2.5-.2*t;cy=.1+.15*t
        pts.append(((rx+.014)*math.cos(a),cy+(ry+.014)*math.sin(a),z))
    stroke('Mage_Robe_seated_cut',pts,.020,ink,mage,mr)

# Place sparse stone fissures directly on actual upward-facing polygon faces.
camp=bpy.data.collections['MD-05_Campfire'];fr=bpy.data.objects['MD-05_ROOT']
for old in list(camp.objects):
    if old.name.startswith('Stone_cut'):bpy.data.objects.remove(old,do_unlink=True)
for stone in [o for o in camp.objects if o.name.startswith('Camp_Stone_')]:
    candidates=[p for p in stone.data.polygons if p.normal.z>.45]
    for p in candidates[:2]:
        vs=[stone.data.vertices[k].co for k in p.vertices];center=sum(vs,Vector())/len(vs)
        a=center.lerp(vs[0],.7)+p.normal*.00012;b=center.lerp(vs[1],.6)+p.normal*.00012
        pts=[stone.matrix_local@v/C for v in (a,center+p.normal*.00012,b)]
        stroke('Camp_Stone_seated_fissure',pts,.018,ink,camp,fr)

# Correct front/back iron straps and rivets so they sit outside the plank faces.
for o in chest.objects:
    if o.name.startswith('Chest_Box_iron_strap'):o.location.y=math.copysign(.1574,o.location.y)
    elif o.name.startswith('Chest_Rivet'):o.location.y=math.copysign(.1615,o.location.y)

# Real transmissive glass shell with an opaque mist core; still no volume shader.
orb=bpy.data.materials['Cloudy green glass'].node_tree.nodes['Principled BSDF']
orb.inputs['Roughness'].default_value=.18
orb.inputs['Metallic'].default_value=0
orb.inputs['Transmission Weight'].default_value=.78
orb.inputs['IOR'].default_value=1.32
orb.inputs['Coat Weight'].default_value=.2
orb.inputs['Specular IOR Level'].default_value=.4
orbcol=bpy.data.collections['MD-06_Crystal_ball'];orr=bpy.data.objects['MD-06_ROOT']
for old in list(orbcol.objects):
    if old.name.startswith('Orb_Painted_reflection'):bpy.data.objects.remove(old,do_unlink=True)
    elif old.name.startswith('Orb_Cloud_fleck'):
        old.location=Vector((0,0,.125))+(old.location-Vector((0,0,.125)))*.77
question=bpy.data.objects['Orb_Mist_question']
for sp in question.data.splines:
    for p in sp.points:p.co.y=-.047
bpy.data.objects['Orb_Mist_dot'].location.y=-.047
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=.049,location=(0,0,.125))
core=bpy.context.object;core.name='Orb_Internal_cloud_core';attach(core,orbcol,orr,simple_mat('Inner cloud green',(.023,.082,.055)))
for p in core.data.polygons:p.use_smooth=True
orr['material_note']='Transmissive glass shell, internal mist-shaped curves and opaque cloudy core; not a volumetric simulation'

assembly.camera.data.lens=48
assembly.camera.location=(0,-2.42,2.72)
assembly.camera.rotation_euler=(Vector((0,.10,.04))-assembly.camera.location).to_track_quat('-Z','Y').to_euler()
assembly.render.resolution_x=1536;assembly.render.resolution_y=1280
assembly.cycles.samples=48
assembly['ui_review']='Native UI changed MD08_LID_HINGE local X from -48 to -60 degrees; verified and retained'
assembly['status']='NativeAssetsCreated / NeedsArtReview'

def outlines(s,width=.85):
    s.render.use_freestyle=True
    fs=s.view_layers[0].freestyle_settings
    ls=fs.linesets[0] if fs.linesets else fs.linesets.new('Silhouette ink')
    if ls.linestyle is None:ls.linestyle=bpy.data.linestyles.new('Hand-ink outline')
    ls.select_crease=False;ls.select_border=True;ls.select_silhouette=True
    ls.select_contour=True;ls.select_external_contour=True
    ls.linestyle.color=(.017,.021,.017);ls.linestyle.thickness=width

outlines(assembly,.8)
assert all(abs(a-b)<1e-7 for ra,rb in zip(hinge_matrix,hinge.matrix_local) for a,b in zip(ra,rb))
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'map-desk-master.blend'),compress=True)
assembly.render.filepath=str(RENDERS/'assembly.png')
bpy.ops.render.render(write_still=True)

catalog=[('MD-01','desk','旧木桌与保留杂物'),('MD-02','environment-map','环境地图与纸面'),('MD-03','red-route','红色路线'),('MD-04','mage','法师木雕'),('MD-05','campfire','篝火'),('MD-06','crystal-ball','水晶球'),('MD-07','building','地点建筑'),('MD-08','chest','金币宝箱'),('MD-10','books','旧书组合')]
records=[]

def bounds(objects,depsgraph):
    points=[]
    for o in objects:
        if o.type in ('MESH','CURVE'):
            e=o.evaluated_get(depsgraph)
            evaluated_mesh=e.to_mesh()
            points.extend(o.matrix_world@v.co for v in evaluated_mesh.vertices)
            e.to_mesh_clear()
    lo=Vector([min(p[k] for p in points) for k in range(3)])
    hi=Vector([max(p[k] for p in points) for k in range(3)])
    return lo,hi

def make_rig(s,center,extent,top=False):
    d=bpy.data.cameras.new('Asset_Camera');o=bpy.data.objects.new('Asset_Camera',d);s.collection.objects.link(o)
    if top:o.location=center+Vector((0,0,extent*3))
    else:o.location=center+Vector((extent*1.55,-extent*2.75,extent*1.65))
    o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
    d.type='ORTHO';d.ortho_scale=extent*1.32;d.clip_start=.001;d.clip_end=100;s.camera=o
    for name,off,power in (('Key',(-1.8,-2,3.2),200),('Fill',(2,1.3,2.5),75)):
        ld=bpy.data.lights.new(name,'AREA');ld.energy=power*extent*extent;ld.shape='DISK';ld.size=extent*2.5
        li=bpy.data.objects.new(name,ld);s.collection.objects.link(li);li.location=center+Vector(off)*extent
        li.rotation_euler=(center-li.location).to_track_quat('-Z','Y').to_euler()

for aid,slug,title in catalog:
    print('PUBLISH',aid,flush=True)
    # Reopen the saved master for each asset, keeping object ownership and
    # evaluated transforms independent from prior preview/export scenes.
    bpy.ops.wm.open_mainfile(filepath=str(OUT/'map-desk-master.blend'))
    assembly=bpy.context.scene
    source_col=next(c for c in assembly.collection.children if c.name.startswith(aid+'_'))
    s=bpy.data.scenes.new(aid+'_'+slug)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
    s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
    s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
    s.view_settings.look='Medium High Contrast';s.world=assembly.world
    copies={}
    assetcol=bpy.data.collections.new(aid+'_ASSET');s.collection.children.link(assetcol)
    for original in source_col.objects:
        new=original.copy()
        if original.data:new.data=original.data.copy()
        assetcol.objects.link(new);copies[original]=new
    for original,new in copies.items():new.parent=copies.get(original.parent)
    ar=copies[bpy.data.objects[aid+'_ROOT']]
    ar.location=(0,0,0);ar.rotation_euler=(0,0,0)
    bpy.context.window.scene=s;bpy.context.view_layer.update()
    native_path=PARTS/(aid+'-'+slug+'.blend')
    bpy.data.libraries.write(str(native_path),{s},path_remap='RELATIVE',fake_user=True,compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(native_path))
    s=bpy.context.scene
    assetcol=next(c for c in s.collection.children if c.name.startswith(aid+'_ASSET'))
    ar=next(o for o in assetcol.objects if o.get('asset_id')==aid)
    lo,hi=bounds(assetcol.objects,bpy.context.evaluated_depsgraph_get());extent=max(hi-lo);center=(lo+hi)/2
    make_rig(s,center,extent,aid in ('MD-02','MD-03'))
    # A neutral presentation plane, isolated from the exported ASSET collection.
    bpy.ops.mesh.primitive_plane_add(size=extent*200,location=(0,0,lo.z-.0015))
    floor=bpy.context.object;floor.name='DISPLAY_GROUND_not_exported'
    floor.data.materials.append(simple_mat('Display paper '+aid,(.34,.35,.31)))
    outlines(s,.9)
    # Save each native asset with geometry/curves, packed textures and a preview rig.
    s.render.filepath=str(RENDERS/(aid+'-'+slug+'.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(native_path),compress=True)
    bpy.ops.render.render(write_still=True,scene=s.name)
    triangles=0
    for o in assetcol.objects:
        if o.type in ('MESH','CURVE'):
            evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=evaluated.to_mesh();me.calc_loop_triangles()
            triangles+=len(me.loop_triangles);evaluated.to_mesh_clear()
    record={'id':aid,'name':title,'blend':'assets/'+aid+'-'+slug+'.blend','glb':'assets/'+aid+'-'+slug+'.glb','render':'renders/'+aid+'-'+slug+'.png','objects':len(assetcol.objects),'evaluated_triangles':triangles,'bounds_m':{'min':list(lo),'max':list(hi)},'local_root_origin_m':list(ar.location)}
    # Convert only the copied objects for the exchange file; saved .blend curves stay editable.
    bpy.ops.object.select_all(action='DESELECT')
    for o in assetcol.objects:
        if o.type=='CURVE':o.select_set(True);bpy.context.view_layer.objects.active=o
    if any(o.select_get() for o in assetcol.objects):bpy.ops.object.convert(target='MESH')
    bpy.ops.object.select_all(action='DESELECT')
    for o in assetcol.objects:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(PARTS/(aid+'-'+slug+'.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False)
    for key in ('blend','glb','render'):record[key+'_sha256']=sha(OUT/record[key])
    records.append(record)

manifest={'date':'2026-09-13','status':'NativeAssetsCreated / NeedsArtReview','user_scope':'开始生成blender资产，猫先不用生成','omitted':['MD-09 cat'],'blender_version':bpy.app.version_string,'units':'metres, +Z up, -Y front in .blend; glTF +Y up','native_ui':{'input':'map-desk-ui.blend','sha256':sha(UI),'object':'MD08_LID_HINGE','before_x_degrees':-48,'after_x_degrees':hinge_angle,'preserved':True},'assembly':'map-desk-master.blend','assembly_sha256':sha(OUT/'map-desk-master.blend'),'render':'renders/assembly.png','assets':records,'textures':[{'path':str(ROOT/'references/map-desk-assets-v01/map-environment-albedo-v01.png'),'sha256':sha(ROOT/'references/map-desk-assets-v01/map-environment-albedo-v01.png'),'role':'Flat map albedo, imagegen output unchanged'},{'path':str(ROOT/'references/e1-r2-generated/wood-ink-albedo-v01.png'),'sha256':sha(ROOT/'references/e1-r2-generated/wood-ink-albedo-v01.png'),'role':'Wood albedo reused unchanged from E1 R2 generated originals'}],'limitations':['First 3D asset pass; fine hatching and carved silhouettes need continued art review against design sheets.','Crystal ball uses a transmissive shell, internal curves and an opaque cloudy core; no volumetric mist simulation.','Flame is a static crossed-mesh silhouette, not simulation or animation.','Freestyle outline is Blender-render-only; it is not carried in GLB.','No new Godot runtime integration, collision, LOD, performance, interaction or gameplay acceptance.']}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PUBLISHED',len(records),'ASSETS',flush=True)

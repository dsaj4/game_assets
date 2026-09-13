"""Small native-Blender helpers shared by the MD-11 build and publication."""
from pathlib import Path
import bpy
import math
import hashlib
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art/md-11-v01'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def material(name, color, image=None, rough=.87):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
    p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough
    if image:
        t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(image),check_existing=True)
        t.extension='REPEAT';m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
    return m

def mesh(name, vertices, faces, mat, col, parent=None, uvs=None, smooth=False):
    d=bpy.data.meshes.new(name);d.from_pydata(vertices,[],faces);d.update()
    o=bpy.data.objects.new(name,d);col.objects.link(o);o.parent=parent;d.materials.append(mat)
    if uvs:
        layer=d.uv_layers.new(name='UVMap')
        for loop in d.loops:layer.data[loop.index].uv=uvs[loop.vertex_index]
    for p in d.polygons:p.use_smooth=smooth
    return o

def curves(name, paths, radius, mat, col, parent=None):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=1
    d.bevel_depth=radius;d.bevel_resolution=1;d.resolution_u=1
    for pts in paths:
        s=d.splines.new('POLY');s.points.add(len(pts)-1)
        for p,v in zip(s.points,pts):p.co=(*v,1)
    o=bpy.data.objects.new(name,d);col.objects.link(o);o.parent=parent;d.materials.append(mat)
    return o

def tube(name, centers, radii, mat, col, parent=None, sides=12):
    pts=[Vector(p) for p in centers];vs=[];uv=[]
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        up=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
        a=tangent.cross(up).normalized();b=tangent.cross(a).normalized()
        for k in range(sides):
            t=math.tau*k/sides;vs.append(p+radii[i]*(math.cos(t)*a+math.sin(t)*b));uv.append((i/(len(pts)-1),k/sides))
    fs=[tuple(reversed(range(sides)))]
    fs.extend((i*sides+k,i*sides+(k+1)%sides,(i+1)*sides+(k+1)%sides,(i+1)*sides+k) for i in range(len(pts)-1) for k in range(sides))
    fs.append(tuple(range((len(pts)-1)*sides,len(pts)*sides)))
    return mesh(name,vs,fs,mat,col,parent,uv,True)

def bounds(objects):
    points=[];triangles=0;dg=bpy.context.evaluated_depsgraph_get()
    for o in objects:
        if o.type in ('MESH','CURVE'):
            e=o.evaluated_get(dg);me=e.to_mesh();me.calc_loop_triangles();triangles+=len(me.loop_triangles)
            points.extend(o.matrix_world@v.co for v in me.vertices);e.to_mesh_clear()
    lo=Vector([min(v[k] for v in points) for k in range(3)])
    hi=Vector([max(v[k] for v in points) for k in range(3)])
    return lo,hi,triangles

def point_camera(camera, target):
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()

def rig(scene, target=(.15,0,.09), scale=2.65, size=(1800,740)):
    col=bpy.data.collections.new('PRESENTATION');scene.collection.children.link(col)
    cam=bpy.data.objects.new('MD11_Camera',bpy.data.cameras.new('MD11_Camera'));col.objects.link(cam)
    cam.location=Vector(target)+Vector((.6,-3.4,1.75));point_camera(cam,target)
    cam.data.type='ORTHO';cam.data.ortho_scale=scale;cam.data.clip_start=.001;scene.camera=cam
    for name,loc,power,width in [('Key',(-.6,-2,3),420,3),('Fill',(2,1.5,2),180,2.5)]:
        d=bpy.data.lights.new('MD11_'+name,'AREA');d.energy=power;d.shape='DISK';d.size=width
        o=bpy.data.objects.new(d.name,d);col.objects.link(o);o.location=loc;point_camera(o,target)
    floor=mesh('DISPLAY_GROUND', [(-20,-20,-.004),(20,-20,-.004),(20,20,-.004),(-20,20,-.004)],[(0,1,2,3)],material('Warm grey backdrop',(.24,.245,.22)),col)
    scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True
    scene.render.resolution_x,scene.render.resolution_y=size;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
    scene.view_settings.look='Medium High Contrast'
    if scene.world is None:scene.world=bpy.data.worlds.new('MD11 World')
    scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs[0].default_value=(.26,.27,.24,1);bg.inputs[1].default_value=.32
    scene.render.use_freestyle=True
    settings=scene.view_layers[0].freestyle_settings;ls=settings.linesets[0] if settings.linesets else settings.linesets.new('Ink silhouette')
    if ls.linestyle is None:ls.linestyle=bpy.data.linestyles.new('MD11 ink')
    ls.select_crease=False;ls.select_silhouette=True;ls.select_border=True;ls.select_contour=True;ls.select_external_contour=True
    ls.linestyle.color=(.025,.017,.008);ls.linestyle.thickness=.85
    return cam

def pack_images():
    for im in bpy.data.images:
        if im.source=='FILE' and not im.packed_file:im.pack()

def export_glb(col,path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:
        if o.type=='CURVE':o.select_set(True);bpy.context.view_layer.objects.active=o
    if any(o.select_get() for o in col.all_objects):bpy.ops.object.convert(target='MESH')
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False)

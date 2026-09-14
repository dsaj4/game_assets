"""Publish seven editable native components and GLB exchanges from the saved WM master."""
from pathlib import Path
import sys,json,struct
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from wm_tools import *

if (OUT/'manifest.json').exists() and '--republish' not in sys.argv:
    raise RuntimeError('Published components exist. Reopen the master and use -- --republish only when intentionally updating exports.')

catalog=json.loads((OUT/'source-catalog.json').read_text(encoding='utf-8'))
master=OUT/'wand-management-master.blend'
records=[]
sizes={'WM-01':(1000,1200),'WM-02':(720,1200),'WM-03':(720,1200),'WM-04':(720,1200),'WM-05':(720,1200),'WM-06':(1500,800),'WM-07':(1100,1500)}

for entry in catalog:
    aid=entry['id'];slug=entry['slug']
    print('PUBLISH',aid,flush=True)
    bpy.ops.wm.open_mainfile(filepath=str(master))
    source=bpy.data.collections[entry['collection']]
    source_root=bpy.data.objects[entry['root']]
    single=bpy.data.scenes.new(aid+'_Native_component')
    single.unit_settings.system='METRIC'
    ac=bpy.data.collections.new(aid+'_ASSET')
    single.collection.children.link(ac)
    copies={}
    for o in source.objects:
        cp=o.copy()
        if o.data:cp.data=o.data.copy()
        ac.objects.link(cp);copies[o]=cp
    for o,cp in copies.items():cp.parent=copies.get(o.parent)
    ar=copies[source_root];ar.location=(0,0,0);ar.rotation_euler=(0,0,0)
    for prop in ('staff_instance','deployed'):
        if prop in ar:del ar[prop]
    bpy.context.window.scene=single
    bpy.context.view_layer.update()
    lo,hi,tri=bounds(ac.all_objects)
    center=(lo+hi)/2
    cam=rig(single,center,max(hi-lo),sizes[aid],front=aid in ('WM-06','WM-07'))
    # Independent rear studio board, never selected for GLB.
    display=bpy.data.collections.new('DISPLAY_NOT_EXPORTED');single.collection.children.link(display)
    shade=material('WM Display neutral '+aid,(.27,.24,.18))
    box('DISPLAY_BACKDROP',(center.x,hi.y+.07,center.z),(max(hi-lo)*4,.018,max(hi-lo)*4),shade,display,None)
    native=OUT/'assets'/(aid+'-'+slug+'.blend')
    render=OUT/'renders'/(aid+'-'+slug+'.png')
    single.render.filepath=str(render)
    pack_images();bpy.ops.file.pack_all()
    bpy.data.libraries.write(str(native),{single},path_remap='RELATIVE',fake_user=True,compress=True)
    # Reopen the written file; publication proves the native asset is usable independently.
    bpy.ops.wm.open_mainfile(filepath=str(native))
    single=bpy.context.scene
    ac=next(c for c in single.collection.children if c.name.startswith(aid+'_ASSET'))
    bpy.context.view_layer.update()
    lo,hi,tri=bounds(ac.all_objects)
    # Library reload resolves the copied root transform. Recenter the preview rig
    # from these final native bounds; pre-write dependency-graph bounds can be stale.
    shift=(lo+hi)/2-center
    for collection in single.collection.children:
        if collection.name.startswith(('PRESENTATION','DISPLAY_NOT_EXPORTED')):
            for obj in collection.objects:obj.location+=shift
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
    record={'id':aid,'slug':slug,'blend':'assets/'+native.name,'glb':'assets/'+aid+'-'+slug+'.glb','render':'renders/'+render.name,
      'objects':len(ac.all_objects),'editable_texts':sum(o.type=='FONT' for o in ac.all_objects),'editable_curves':sum(o.type=='CURVE' for o in ac.all_objects),
      'triangles':tri,'bounds_m':{'min':list(lo),'max':list(hi)},'render_size':list(sizes[aid])}
    bpy.ops.render.render(write_still=True)
    export_selected(list(ac.all_objects),OUT/record['glb'])
    for field in ('blend','glb','render'):record[field+'_sha256']=sha(OUT/record[field])
    records.append(record)

# Exchange of the full page contains geometry/clutter, not the render rig.
bpy.ops.wm.open_mainfile(filepath=str(master))
scene=bpy.context.scene
objects=[o for c in scene.collection.children if c.name!='PRESENTATION' for o in c.all_objects]
objects=list(dict.fromkeys(objects))
lo,hi,tri=bounds(objects)
exchange={'file':'wand-management-assembly.glb','triangles':tri,'bounds_m':{'min':list(lo),'max':list(hi)}}
export_selected(objects,OUT/exchange['file'])
exchange['sha256']=sha(OUT/exchange['file'])
bpy.ops.wm.open_mainfile(filepath=str(master))
scene=bpy.context.scene
# Refresh the saved master camera view as well, including future manual edits.
scene.render.filepath=str(OUT/'renders/assembly.png')
bpy.ops.render.render(write_still=True)
# A side-biased real render demonstrates the independent depth and supports.
cam=scene.camera
cam.location=(2.2,-9.3,3.25);point_camera(cam,(.01,0,1.96))
cam.data.ortho_scale=4.48
scene.render.filepath=str(OUT/'renders/assembly-oblique.png')
bpy.ops.render.render(write_still=True)

textures=[
 ('references/md-11-native/leather-albedo-v01.png','Existing imagegen old leather; unchanged'),
 ('references/e1-r2-generated/wood-ink-albedo-v01.png','Existing imagegen dark wood for wall and rack; unchanged'),
 ('references/wm-native/wood-staff-albedo-v01.png','New imagegen color edit for staff wood; original pixels'),
 ('art/e1/paper_base.png','Existing E1 procedural paper albedo; unchanged')]
renders=[]
for name in ('assembly.png','assembly-oblique.png','assembly-first-pass.png'):
    p=OUT/'renders'/name
    renders.append({'path':'renders/'+name,'sha256':sha(p),'size_px':list(struct.unpack('>II',p.read_bytes()[16:24])),'role':'historical first pass' if 'first-pass' in name else 'current actual Blender render'})
manifest={'date':'2026-09-14','status':'NativeAssetsCreated / NeedsArtReview','user_scope':'开始建模: left staff-management page only',
 'blender_version':bpy.app.version_string,'method':'Blender bundled Python / native editable mesh, curves and fonts; computer-use tool unavailable',
 'design_overall':'concepts/wand-management-overall-v03.png','design_components':'concepts/wand-management-sheets-v01/manifest.json',
 'native':'wand-management-master.blend','native_sha256':sha(master),'assembly_exchange':exchange,'assets':records,'renders':renders,
 'textures':[{'path':p,'sha256':sha(ROOT/p),'role':role} for p,role in textures],
 'text':'Native editable FONT objects use local SimKai font, packed into .blend; GLB texts converted to meshes',
 'preserved_files':[
 {'path':'art/e1/e1-r2-master.blend','sha256':'9bf43acd899ef5daba2aa50aa98fc8205e967fbccc2e7cb5c601e25dcdc35082'},
 {'path':'art/map-desk-v02/map-desk-master.blend','sha256':'d21ef1bdbff88661de4b3d478d28e5512cebb747bb9e7554b3bd76bd1f674752'},
 {'path':'art/md-11-v01/MD-11-wand-roll.blend','sha256':'2e0694fcfb736bf1add700f463fee9e4b43223c92ab80722ae19eaa07398742e'}],
 'limitations':['First native art pass; not accepted as final FLASK-level art or game UI',
 'Static six-staff scene and selected detail; no management interactions, simulation or gameplay testing',
 'Fonts become fixed glyph meshes in GLB; runtime must replace with real UI text for dynamic values',
 'Freestyle outlines are Blender render-only; native cloth thickness, curves and image textures remain available in .blend',
 'No LOD, engine profiling, collision or real paper/bag animation; large reserve inventory navigation not implemented']}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('WM PUBLISHED',len(records),'assets',flush=True)

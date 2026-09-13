"""Publish MD-11 from the frozen native UI source; preserve older asset versions."""
from pathlib import Path
import sys, json, math
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from md11_tools import ROOT, OUT, bounds, point_camera, pack_images, export_glb, sha

UI = OUT/'md11-ui.blend'
NATIVE = OUT/'MD-11-wand-roll.blend'
GLB = OUT/'MD-11-wand-roll.glb'
OLD = ROOT/'art/map-desk-v01/map-desk-master.blend'
ASSEMBLY = ROOT/'art/map-desk-v02'
for p in (OUT/'renders', ASSEMBLY/'renders'): p.mkdir(parents=True, exist_ok=True)
old_sha = sha(OLD)
assert old_sha == 'b09dcc2e658dd68aba06c23fecc3542da14991fe0a5af399128896076148351e'

def render(scene, path, size):
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    return {'path': str(path.relative_to(ROOT)).replace('\\','/'), 'sha256': sha(path), 'size_px': list(size)}

bpy.ops.wm.open_mainfile(filepath=str(UI))
s = bpy.context.scene
fork = bpy.data.objects['MD11_STAFF_FORK']
angle = math.degrees(fork.rotation_euler.x)
assert abs(angle-12) < .001, ('Native Blender UI edit missing', angle)
ui_matrix = [list(row) for row in fork.matrix_local]
col = bpy.data.collections['MD-11_ASSET']
root = bpy.data.objects['MD-11_ROOT']
# Keep the actual UI rotation while refining the wood in the staff's local frame.
# A two-prong fork reads more clearly beside the second staff's ring head.
bpy.data.objects.remove(bpy.data.objects['MD11_Fork_lower_branch'], do_unlink=True)
branch_cuts = bpy.data.objects['MD11_Fork_branch_cuts'].data
branch_cuts.splines.remove(branch_cuts.splines[1])
def bend_wood(p):
    x,y,z = p
    t = max(0,min(1,(x-1.83)/.37))
    swell = 1 + .38*math.exp(-((x-1.995)/.026)**2) + .18*math.exp(-((x-2.145)/.021)**2)
    return Vector((x, y*swell+.004*math.sin(t*math.pi*3)*t,
                   z*swell+.012*math.sin(t*math.pi*2.6)*t))
for o in list(fork.children):
    if o.type == 'MESH':
        for v in o.data.vertices: v.co = bend_wood(v.co)
    elif o.type == 'CURVE':
        for spline in o.data.splines:
            for p in spline.points: p.co = (*bend_wood(p.co.xyz),1)
# Unite the two intersecting wood volumes so the branch grows out of the shaft.
bpy.ops.object.select_all(action='DESELECT')
shaft = bpy.data.objects['MD11_STAFF_FORK_shaft']
shaft.select_set(True); bpy.data.objects['MD11_Fork_upper_branch'].select_set(True)
bpy.context.view_layer.objects.active = shaft
bpy.ops.object.join()
remesh = shaft.modifiers.new('Continuous carved fork volume','REMESH')
remesh.mode = 'VOXEL'; remesh.voxel_size = .0016; remesh.use_smooth_shade = True
bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth = shaft.modifiers.new('Soften branch junction','SMOOTH'); smooth.factor = .7; smooth.iterations = 3
bpy.ops.object.modifier_apply(modifier=smooth.name)
for polygon in shaft.data.polygons: polygon.use_smooth = True
root['fork_refinement'] = 'Two-prong continuous wooden mesh, gently curved and swollen at wood knots'
assert all(abs(a-b)<1e-7 for ra,rb in zip(ui_matrix,fork.matrix_local) for a,b in zip(ra,rb))
root['status'] = 'NativeAssetCreated / NeedsArtReview'
root['ui_refinement'] = 'Fork staff local X rotated to 12 degrees in native Blender UI'
root['source_design'] = 'Approved overall v05; MD-11 appearance v01 / construction v02'
s['status'] = 'NativeAssetCreated / NeedsArtReview'
s['scope'] = 'MD-11 long staff roll only; preview rig excluded from GLB'
# A quieter studio exposure reveals the russet texture without orange highlights.
bpy.data.lights['MD11_Key'].energy = 175
bpy.data.lights['MD11_Fill'].energy = 65
s.view_settings.exposure = -.25
s.cycles.samples = 48
cam = s.camera
cam.data.ortho_scale = 2.60
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.overlay.show_overlays = False
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
            area.spaces.active.region_3d.view_camera_zoom = 12
pack_images()
s.render.filepath = str(OUT/'renders/hero.png')
bpy.ops.wm.save_as_mainfile(filepath=str(NATIVE), compress=True)
bpy.context.view_layer.update()
lo, hi, triangles = bounds(col.all_objects)
native_record = {'bounds_m': {'min': list(lo), 'max': list(hi)}, 'dimensions_m': list(hi-lo),
                 'evaluated_triangles': triangles, 'objects': len(col.all_objects),
                 'root_origin_m': list(root.location)}
images = [render(s, OUT/'renders/hero.png', (1800,740))]
cam.location = (1.62,-1.85,.91)
point_camera(cam, (1.035,0,.095)); cam.data.ortho_scale = .82
images.append(render(s, OUT/'renders/mouth-detail.png', (1200,1000)))
cam.location = (.15,-4,.09)
point_camera(cam, (.15,0,.09)); cam.data.ortho_scale = 2.60
images.append(render(s, OUT/'renders/front.png', (1800,600)))
# Reopen the published native source before converting curves for exchange.
bpy.ops.wm.open_mainfile(filepath=str(NATIVE))
export_glb(bpy.data.collections['MD-11_ASSET'], GLB)

bpy.ops.wm.open_mainfile(filepath=str(OLD))
s = bpy.context.scene
previous_names = set(o.name for o in s.objects)
previous_ids = sorted(o.get('asset_id') for o in s.objects if o.get('asset_id'))
hinge_before = [list(row) for row in bpy.data.objects['MD08_LID_HINGE'].matrix_local]
with bpy.data.libraries.load(str(NATIVE), link=False) as (available, appended):
    assert 'MD-11_ASSET' in available.collections
    appended.collections = ['MD-11_ASSET']
s.collection.children.link(appended.collections[0])
root = bpy.data.objects['MD-11_ROOT']
# The roll rests on the existing 7 cm ledge and leans against its rear board.
root.location = (-.05,.728,.0705-lo.z)
# Keep every original prop. Move only two clutter groups forward to make space.
clutter_adjustments = []
for o in bpy.data.collections['MD-01_Desk_and_clutter'].objects:
    delta = -.24 if o.name.startswith(('Armillary_', 'Globe_')) else -.085 if o.name.startswith('Quill_') else 0
    if delta:
        before = list(o.location); o.location.y += delta
        clutter_adjustments.append({'object': o.name, 'before_m': before, 'after_m': list(o.location)})
s.camera.data.lens = 43
s.camera.location = (.10,-2.42,2.72)
point_camera(s.camera, (.10,.10,.04))
s.render.resolution_x = 1700; s.render.resolution_y = 1400
s.cycles.samples = 48
s['status'] = 'NativeAssetsCreated / NeedsArtReview'
s['revision'] = 'Map desk v02: MD-11 replaces the omitted cat at rear ledge'
s['md11_source'] = 'art/md-11-v01/MD-11-wand-roll.blend'
s['clutter_note'] = 'All original clutter retained; armillary and quills moved forward to clear the long roll'
assert previous_names.issubset(set(o.name for o in s.objects))
assert not any(o.get('asset_id') == 'MD-09' for o in s.objects)
assert all(abs(a-b) < 1e-7 for row_a,row_b in zip(hinge_before,bpy.data.objects['MD08_LID_HINGE'].matrix_local) for a,b in zip(row_a,row_b))
pack_images(); bpy.context.view_layer.update()
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.overlay.show_overlays = False
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
bpy.ops.object.select_all(action='DESELECT')
root.select_set(True); bpy.context.view_layer.objects.active = root
s.render.filepath = str(ASSEMBLY/'renders/assembly.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ASSEMBLY/'map-desk-master.blend'), compress=True)
images.append(render(s, ASSEMBLY/'renders/assembly.png', (1700,1400)))
assert sha(OLD) == old_sha

texture = ROOT/'references/md-11-native/leather-albedo-v01.png'
im = bpy.data.images.load(str(texture), check_existing=True)
provenance = {'date':'2026-09-13', 'provider':'Built-in image_gen.imagegen', 'model':'Not reported by tool',
 'role':'Generated leather albedo, original image bytes used unchanged',
 'image':'leather-albedo-v01.png', 'sha256':sha(texture), 'size_px':list(im.size),
 'prompt':'leather-albedo-v01-prompt.md','prompt_sha256':sha(texture.with_name('leather-albedo-v01-prompt.md')),
 'source_output':'C:/Users/Administrator/.codex/generated_images/01a09889-9886-77c2-b7f6-9054d97a682e/exec-0f3b28dd-8b18-478f-a70c-c8a1962cdbd2.png',
 'reference':'concepts/blender-sheets-v02/md-11-wand-roll-appearance-v01.png',
 'reference_sha256':sha(ROOT/'concepts/blender-sheets-v02/md-11-wand-roll-appearance-v01.png')}
(texture.parent/'manifest.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest = {'date':'2026-09-13','asset_id':'MD-11','status':'NativeAssetCreated / NeedsArtReview',
 'blender_version':bpy.app.version_string, 'scope':'Long whole-leather roll, two ties, two full wooden staffs; cat omitted',
 'native':str(NATIVE.relative_to(ROOT)), 'native_sha256':sha(NATIVE), 'glb':str(GLB.relative_to(ROOT)), 'glb_sha256':sha(GLB),
 'native_geometry':native_record, 'native_ui':{'source':str(UI.relative_to(ROOT)),'sha256':sha(UI),
 'baseline_sha256':sha(OUT/'md11-generated.blend'),'object':'MD11_STAFF_FORK','before_degrees':0,'after_degrees':angle,
 'preserved_matrix_local':ui_matrix,'evidence':'art/md-11-v01/ui-fork-roll-12deg.png'},
 'assembly':{'file':'art/map-desk-v02/map-desk-master.blend','sha256':sha(ASSEMBLY/'map-desk-master.blend'),
 'previous_file':str(OLD.relative_to(ROOT)),'previous_sha256':old_sha,'previous_asset_ids':previous_ids,
 'root_location_m':list(root.location),'clutter_adjustments':clutter_adjustments,'old_objects_retained':True,
 'chest_ui_angle_degrees':math.degrees(bpy.data.objects['MD08_LID_HINGE'].rotation_euler.x)},
 'renders':images, 'texture_provenance':'references/md-11-native/manifest.json',
 'limitations':['First native art pass; visual similarity remains an art-review question.',
 'Fine outline is Blender Freestyle and is not exported in GLB.',
 'No Godot integration, rigging, interaction, collision, LOD or performance acceptance.']}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('MD11 PUBLISHED', native_record, flush=True)

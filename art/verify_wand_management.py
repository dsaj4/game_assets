"""Verify saved native WM assets, actual GLB re-import, scene structure and prior-file preservation."""
from pathlib import Path
import sys,json,math,struct
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0,str(Path(__file__).resolve().parent))
from wm_tools import *

manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
checks=[]
completed=False
def check(name,ok,detail=None):
    checks.append({'name':name,'pass':bool(ok),'detail':detail})
    if not ok:raise AssertionError((name,detail))

try:
    for old in manifest['preserved_files']:
        check('preserved_'+old['path'],sha(ROOT/old['path'])==old['sha256'])
    check('master_sha',sha(OUT/manifest['native'])==manifest['native_sha256'])
    bpy.ops.wm.open_mainfile(filepath=str(OUT/manifest['native']))
    scene=bpy.context.scene
    ids=[o['asset_id'] for o in scene.objects if 'asset_id' in o]
    check('seven_asset_roots',sorted(ids)==['WM-%02d'%i for i in range(1,8)],ids)
    staffs=[o for o in scene.objects if 'staff_instance' in o]
    check('six_staffs_four_deployed',len(staffs)==6 and sum(bool(o['deployed']) for o in staffs)==4,[(o.name,o['staff_instance'],o['deployed']) for o in staffs])
    check('no_extra_bells_or_cat',not any('bell' in o.name.lower() or 'cat'==o.get('part_role') for o in scene.objects))
    hide=bpy.data.objects['WM01_SINGLE_CONTINUOUS_HIDE']
    adjacency=[[] for _ in hide.data.vertices]
    for e in hide.data.edges:
        a,b=e.vertices;adjacency[a].append(b);adjacency[b].append(a)
    seen={0};stack=[0]
    while stack:
        for other in adjacency[stack.pop()]:
            if other not in seen:seen.add(other);stack.append(other)
    check('continuous_hide',len(seen)==len(adjacency),len(seen))
    check('native_hide_thickness_4mm',any(m.type=='SOLIDIFY' and abs(m.thickness-.004)<1e-7 for m in hide.modifiers))
    check('four_retention_loops',sum(o.get('part_role')=='retention_loop' for o in scene.objects)==4)
    check('four_toe_supports',sum(o.get('part_role')=='toe_support' for o in scene.objects)==4)
    check('rack_open_back',bpy.data.objects['WM-02_reserve-rack_ROOT']['open_back'])
    check('two_changeable_slots',sorted(o['changeable_slot'] for o in scene.objects if 'changeable_slot' in o)==[1,2])
    grid=[o for o in scene.objects if 'grid_row' in o]
    check('ten_cells_2x5',len(grid)==10 and {(o['grid_row'],o['grid_column']) for o in grid}=={(r,c) for r in ('B','F') for c in range(1,6)})
    check('F3_clipped_cross',{o['grid_row']+str(o['grid_column']) for o in grid if o['highlighted']}=={'B3','F2','F3','F4'})
    texts=[o.data.body for o in scene.objects if o.type=='FONT']
    check('read_only_and_no_editors','只读' in texts and '移至备战架' in texts and not any(t in texts for t in ('更换法术','编辑法术','法术','词卡')))
    check('timing_labels',all(t in texts for t in ('冷却 4刻  |  释放 1刻','0–10刻','首次释放 4刻','① 4刻','② 5刻','③ 7–9刻','④ 8刻')))
    check('native_texts_editable',len(texts)>40,len(texts))
    check('fonts_packed',any(getattr(f,'packed_file',None) for f in bpy.data.fonts))
    check('images_packed',all(im.packed_file for im in bpy.data.images if im.source=='FILE'))
    # Validate exact transform bounds for the bag/rack gap, and the staff toe floor heights.
    lo,hi,_=bounds(bpy.data.collections['WM-01_deployed-leather'].all_objects)
    rlo,rhi,_=bounds(bpy.data.collections['WM-02_reserve-rack'].all_objects)
    check('bag_rack_separate',rlo.x-hi.x>.015,{'gap_m':rlo.x-hi.x})
    check('staff_roots_at_toe_supports',all(abs(o.location.z-1.715)<1e-5 for o in staffs))
    frame=[]
    for col in scene.collection.children:
        if col.name.startswith('WM-') or col.name=='WM_Additional_staff_instances':
            for o in col.all_objects:
                if o.type in GEO_TYPES:
                    frame.extend(world_to_camera_view(scene,scene.camera,o.matrix_world@Vector(c)) for c in o.bound_box)
    check('complete_asset_groups_in_frame',all(.015<p.x<.985 and .015<p.y<.985 and p.z>0 for p in frame),{'min_x':min(p.x for p in frame),'max_x':max(p.x for p in frame),'min_y':min(p.y for p in frame),'max_y':max(p.y for p in frame)})

    for asset in manifest['assets']:
        aid=asset['id']
        for field in ('blend','glb','render'):check(aid+'_'+field+'_sha',sha(OUT/asset[field])==asset[field+'_sha256'])
        bpy.ops.wm.open_mainfile(filepath=str(OUT/asset['blend']))
        col=next(c for c in bpy.context.scene.collection.children if c.name.startswith(aid+'_ASSET'))
        root=next(o for o in col.objects if o.get('asset_id')==aid)
        check(aid+'_native_origin',root.location.length<1e-6)
        bpy.context.view_layer.update()
        lo,hi,tri=bounds(col.all_objects)
        check(aid+'_saved_geometry_count',tri==asset['triangles'],tri)
        check(aid+'_native_editable_curves',sum(o.type=='CURVE' for o in col.all_objects)==asset['editable_curves'])
        check(aid+'_native_editable_text',sum(o.type=='FONT' for o in col.all_objects)==asset['editable_texts'])
        projected=[]
        for obj in col.all_objects:
            if obj.type in GEO_TYPES:
                projected.extend(world_to_camera_view(bpy.context.scene,bpy.context.scene.camera,obj.matrix_world@Vector(c)) for c in obj.bound_box)
        check(aid+'_component_fully_in_frame',all(.01<p.x<.99 and .01<p.y<.99 and p.z>0 for p in projected),
           {'min_x':min(p.x for p in projected),'max_x':max(p.x for p in projected),'min_y':min(p.y for p in projected),'max_y':max(p.y for p in projected)})
        native_lo,native_hi=list(lo),list(hi)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(OUT/asset['glb']))
        bpy.context.view_layer.update()
        glo,ghi,gtri=bounds(bpy.context.scene.objects)
        delta=max(abs(a-b) for aa,bb in ((glo,native_lo),(ghi,native_hi)) for a,b in zip(aa,bb))
        check(aid+'_actual_glb_bounds',delta<.002,delta)
        check(aid+'_actual_glb_triangles',tri==gtri,{'native':tri,'import':gtri})
        check(aid+'_no_display_in_glb',not any(o.type in ('CAMERA','LIGHT') or o.name.startswith('DISPLAY') for o in bpy.context.scene.objects))
        png=(OUT/asset['render']).read_bytes()
        check(aid+'_render_dimensions',list(struct.unpack('>II',png[16:24]))==asset['render_size'],asset['render_size'])

    ex=manifest['assembly_exchange']
    check('assembly_glb_hash',sha(OUT/ex['file'])==ex['sha256'])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/ex['file']))
    bpy.context.view_layer.update()
    lo,hi,tri=bounds(bpy.context.scene.objects)
    delta=max(abs(a-b) for aa,bb in ((lo,ex['bounds_m']['min']),(hi,ex['bounds_m']['max'])) for a,b in zip(aa,bb))
    check('assembly_actual_glb_bounds',delta<.002,delta)
    check('assembly_actual_glb_triangles',tri==ex['triangles'],tri)
    check('assembly_glb_no_camera_or_light',not any(o.type in ('CAMERA','LIGHT') for o in bpy.context.scene.objects))
    for render in manifest['renders']:
        p=OUT/render['path'];data=p.read_bytes()
        check('render_'+p.name,sha(p)==render['sha256'] and list(struct.unpack('>II',data[16:24]))==render['size_px'])
    for item in manifest['textures']:check('texture_'+item['path'],sha(ROOT/item['path'])==item['sha256'])
    completed=True
finally:
    report={'date':manifest['date'],'status':'PASS' if completed and checks and all(c['pass'] for c in checks) else 'FAIL','checks':checks,
       'visual_scope':'Structural checks and actual file reopens/imports; image similarity and gameplay are not inferred',
       'native_ui':'Not used; pipeline executed with Blender bundled Python',
       'runtime_interaction':'NotRun'}
    (OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('WM VERIFICATION',report['status'],len(checks),flush=True)

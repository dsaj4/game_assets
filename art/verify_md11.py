"""Check MD-11 editable structure, native UI provenance and actual GLB round trip."""
from pathlib import Path
import sys, json, math, struct
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0, str(Path(__file__).resolve().parent))
from md11_tools import ROOT, OUT, bounds, sha

manifest = json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
checks = []
def check(name, ok, details=None):
    checks.append({'name':name,'pass':bool(ok),'details':details})
    assert ok, (name,details)

bpy.ops.wm.open_mainfile(filepath=str(OUT/'md11-generated.blend'))
check('baseline_fork_rotation_zero',abs(bpy.data.objects['MD11_STAFF_FORK'].rotation_euler.x)<1e-7)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/manifest['native']))
col = bpy.data.collections['MD-11_ASSET']
body = bpy.data.objects['MD11_LeatherBody_SINGLE_CONTINUOUS_HIDE']
root = bpy.data.objects['MD-11_ROOT']
check('root_local_origin', root.location.length<1e-7)
check('two_ties',set(o.name for o in col.objects if o.type=='EMPTY' and o.name.startswith('MD11_TIE_'))=={'MD11_TIE_A','MD11_TIE_B'})
check('two_full_staffs',all(bpy.data.objects.get(n) for n in ('MD11_STAFF_FORK_shaft','MD11_STAFF_RING_shaft')))
check('native_ui_12_degrees',abs(math.degrees(bpy.data.objects['MD11_STAFF_FORK'].rotation_euler.x)-12)<.001)
adj=[[] for _ in body.data.vertices]
for edge in body.data.edges:
    a,b=edge.vertices;adj[a].append(b);adj[b].append(a)
visited={0}; stack=[0]
while stack:
    v=stack.pop()
    for nxt in adj[v]:
        if nxt not in visited: visited.add(nxt); stack.append(nxt)
check('single_connected_hide',len(visited)==len(adj),{'visited_vertices':len(visited),'total_vertices':len(adj)})
check('editable_3mm_hide',any(m.type=='SOLIDIFY' and abs(m.thickness-.003)<1e-7 for m in body.modifiers))
check('editable_curves_retained',sum(o.type=='CURVE' for o in col.objects)>10)
packed=[im for im in bpy.data.images if im.source=='FILE' and im.packed_file]
check('native_packed_albedo',any('leather-albedo' in im.name for im in packed),[im.name for im in packed])
bpy.context.view_layer.update()
lo,hi,tri=bounds(col.all_objects)
check('long_proportions',(hi-lo).x>2.20 and 1.89<body.dimensions.x<1.93,{'overall_m':list(hi-lo),'body_m':list(body.dimensions),'triangles':tri})
check('finite_geometry',all(math.isfinite(v) for vec in (lo,hi) for v in vec))
native_lo,native_hi=list(lo),list(hi)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/manifest['glb']))
bpy.context.view_layer.update()
lo,hi,round_tri=bounds(bpy.context.scene.objects)
delta=max(abs(a-b) for vs,ns in ((lo,native_lo),(hi,native_hi)) for a,b in zip(vs,ns))
check('glb_actual_import_bounds',delta<.002,{'max_error_m':delta})
check('glb_triangle_round_trip',round_tri==tri,{'native':tri,'glb':round_tri})
check('glb_no_presentation',not any(o.type in ('CAMERA','LIGHT') or o.name.startswith('DISPLAY_') for o in bpy.context.scene.objects))
check('glb_embedded_albedo',any(im.packed_file for im in bpy.data.images if im.source=='FILE'))

assembly=manifest['assembly']
check('previous_assembly_hash_unchanged',sha(ROOT/assembly['previous_file'])==assembly['previous_sha256'])
bpy.ops.wm.open_mainfile(filepath=str(ROOT/assembly['previous_file']))
old_objects={o.name:{'type':o.type,'matrix':[list(r) for r in o.matrix_local],
              'vertices':len(o.data.vertices) if o.type=='MESH' else None} for o in bpy.context.scene.objects}
bpy.ops.wm.open_mainfile(filepath=str(ROOT/assembly['file']))
s=bpy.context.scene
new_objects={o.name:o for o in s.objects}
expected_ids=['MD-01','MD-02','MD-03','MD-04','MD-05','MD-06','MD-07','MD-08','MD-10','MD-11']
check('ten_asset_groups_no_cat',sorted(o.get('asset_id') for o in s.objects if o.get('asset_id'))==expected_ids)
check('all_original_objects_preserved',set(old_objects).issubset(set(new_objects)),len(old_objects))
allowed={r['object'] for r in assembly['clutter_adjustments']}
unchanged=True
for name,record in old_objects.items():
    o=new_objects[name]
    if o.type=='MESH' and len(o.data.vertices)!=record['vertices']:unchanged=False
    if name not in allowed and o.type not in ('CAMERA','LIGHT'):
        if any(abs(a-b)>1e-6 for ra,rb in zip(o.matrix_local,record['matrix']) for a,b in zip(ra,rb)):unchanged=False
check('old_meshes_and_other_transforms_preserved',unchanged)
check('chest_native_ui_edit_preserved',abs(math.degrees(new_objects['MD08_LID_HINGE'].rotation_euler.x)+60)<.001)
check('assembly_fork_native_ui_edit_preserved',abs(math.degrees(new_objects['MD11_STAFF_FORK'].rotation_euler.x)-12)<.001)
bpy.context.view_layer.update()
roll=bpy.data.collections['MD-11_ASSET'];blo,bhi,_=bounds(roll.all_objects)
check('roll_rear_ledge_contact',abs(blo.z-.0705)<.001,{'bottom_m':blo.z,'ledge_top_m':.07,'gap_m':blo.z-.07})
projections=[]
for o in roll.all_objects:
    if o.type in ('MESH','CURVE'):
        projections.extend(world_to_camera_view(s,s.camera,o.matrix_world@Vector(c)) for c in o.bound_box)
check('whole_roll_in_assembly_frame',all(.01<p.x<.99 and .01<p.y<.99 and p.z>0 for p in projections),
      {'min_x':min(p.x for p in projections),'max_x':max(p.x for p in projections),'min_y':min(p.y for p in projections),'max_y':max(p.y for p in projections)})
for item in manifest['renders']:
    path=ROOT/item['path'];data=path.read_bytes()
    size=list(struct.unpack('>II',data[16:24]))
    check('render_file_'+path.name,data[:8]==b'\x89PNG\r\n\x1a\n' and size==item['size_px'] and sha(path)==item['sha256'],size)
report={'status':'PASS','date':'2026-09-13','blender_version':bpy.app.version_string,'checks':checks,
        'visual_review':'Actual rendered images require separate human/model visual inspection; structural checks do not establish style approval.'}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('MD11 VERIFIED',len(checks),'checks',flush=True)

"""Reopen every native asset, then import every GLB to check packaged geometry."""
from pathlib import Path
import bpy
import json
import hashlib
import math
import struct
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/map-desk-v01'
manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh_bounds(objects):
    points=[];triangles=0;dg=bpy.context.evaluated_depsgraph_get()
    for o in objects:
        if o.type in ('MESH','CURVE'):
            e=o.evaluated_get(dg);me=e.to_mesh();me.calc_loop_triangles();triangles+=len(me.loop_triangles)
            for v in me.vertices:
                p=o.matrix_world@v.co
                assert all(math.isfinite(n) for n in p),o.name
                points.append(p)
            e.to_mesh_clear()
    return ([min(p[k] for p in points) for k in range(3)], [max(p[k] for p in points) for k in range(3)],triangles)

rows=[]
for record in manifest['assets']:
    print('VERIFY',record['id'],flush=True)
    for k in ('blend','glb','render'):
        assert sha(OUT/record[k])==record[k+'_sha256'],(record['id'],k,'hash')
    bpy.ops.wm.open_mainfile(filepath=str(OUT/record['blend']))
    scene=bpy.context.scene
    col=next(c for c in scene.collection.children if c.name.startswith(record['id']+'_ASSET'))
    assert len(col.objects)==record['objects']
    assert not any(o.get('asset_id')=='MD-09' for o in scene.objects)
    root=next(o for o in col.objects if o.get('asset_id')==record['id'])
    assert root.parent is None and root.location.length<1e-8
    assert all(im.packed_file for im in bpy.data.images if im.source=='FILE' and im.users>0)
    curves=sum(o.type=='CURVE' for o in col.objects)
    lo,hi,tri=mesh_bounds(col.objects)
    assert tri==record['evaluated_triangles'],(record['id'],'triangle mismatch',tri)
    if record['id']=='MD-08':
        hinge=next(o for o in col.objects if o.name.startswith('MD08_LID_HINGE'))
        assert abs(math.degrees(hinge.rotation_euler.x)+60)<.01
    png=(OUT/record['render']).read_bytes()
    assert png[:8]==b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>II',png[16:24])==(1100,1100)
    data=(OUT/record['glb']).read_bytes()
    magic,version,length=struct.unpack('<III',data[:12])
    assert magic==0x46546c67 and version==2 and length==len(data)
    json_size,json_kind=struct.unpack('<II',data[12:20]);assert json_kind==0x4e4f534a
    gltf=json.loads(data[20:20+json_size]);assert len(gltf.get('meshes',[]))>0
    assert all('uri' not in im for im in gltf.get('images',[])), 'GLB must embed images'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/record['glb']))
    ilo,ihi,itri=mesh_bounds(bpy.context.scene.objects)
    error=max(abs(a-b) for a,b in zip(lo+hi,ilo+ihi))
    assert error<.002,(record['id'],'roundtrip bound error',error)
    assert tri==itri,(record['id'],'GLB triangle mismatch',tri,itri)
    assert not any(o.name.startswith('DISPLAY_GROUND') for o in bpy.context.scene.objects)
    rows.append({'id':record['id'],'native_reopen':'PASS','native_objects':record['objects'],'editable_curves':curves,'triangles':tri,'root_origin':'zero','packed_textures':'PASS','glb_import':'PASS','glb_embedded_images':len(gltf.get('images',[])),'glb_bounds_error_m':error,'no_presentation_ground_in_glb':True,'render_png':'1100 x 1100'})

bpy.ops.wm.open_mainfile(filepath=str(OUT/'map-desk-master.blend'))
ids=sorted(o.get('asset_id') for o in bpy.context.scene.objects if o.get('asset_id'))
assert ids==['MD-01','MD-02','MD-03','MD-04','MD-05','MD-06','MD-07','MD-08','MD-10'],ids
assert sha(OUT/'map-desk-master.blend')==manifest['assembly_sha256']
assert abs(math.degrees(bpy.data.objects['MD08_LID_HINGE'].rotation_euler.x)+60)<.01
assembly_png=(OUT/'renders/assembly.png').read_bytes()
assert struct.unpack('>II',assembly_png[16:24])==(1536,1280)
verification={'date':'2026-09-13','status':'PASS','asset_count':len(rows),'cat_omitted':True,'assembly_reopened':True,'assembly_render':'1536 x 1280','native_ui_hinge_preserved':True,'assets':rows,'scope':'Native .blend reopen, packed textures, evaluated geometry, GLB reimport and bounds; no Godot runtime or visual-similarity acceptance'}
(OUT/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('VERIFIED',len(rows),'ASSETS',flush=True)

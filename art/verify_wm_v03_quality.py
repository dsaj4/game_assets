"""Checks preservation and generated-skin integration beyond the shared export checks."""
from pathlib import Path
import sys,json,hashlib
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from wm_tools import ROOT, sha
OUT=ROOT/'art/wand-management-v03'
checks=[]

def check(name, condition, detail=None):
    checks.append({'name':name,'pass':bool(condition),'detail':detail})
    assert condition, (name,detail)

def inventory(version):
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'art/wand-management-{version}/wand-management-master.blend'))
    result={}
    for col in bpy.context.scene.collection.children:
        if not (col.name.startswith(('WM-01','WM-02','WM-03','WM-04','WM-05')) or col.name=='WM_Additional_staff_instances'):
            continue
        for o in col.all_objects:
            row={'type':o.type,'transform':[list(r) for r in o.matrix_local],
                 'materials':[m.name if m else None for m in getattr(o.data,'materials',[])]}
            if o.type=='MESH':
                row['mesh']=[[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]]
            elif o.type=='CURVE':
                row['curve']=[[[*p.co] for p in spline.points] for spline in o.data.splines]
            result[o.name]=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
    texts={o.name:o.data.body for o in bpy.context.scene.objects if o.type=='FONT'}
    return result,texts

completed=False
try:
    prior,texts_prior=inventory('v02')
    current,texts_current=inventory('v03')
    check('all_bag_rack_staff_objects_geometry_transforms_material_slots_preserved',prior==current,len(prior))
    check('all_editable_text_content_preserved',texts_prior==texts_current,len(texts_current))
    scene=bpy.context.scene
    check('three_separate_paper_leaves',sum(o.name.startswith('WM06_Stacked_leaf_') for o in scene.objects)==2)
    for name in ('WM06_Parchment_body','WM07_Back_body','WM07_Save_body'):
        obj=bpy.data.objects[name]
        check(name+'_physical_thickness',any(m.type=='SOLIDIFY' and m.thickness>=.004 for m in obj.modifiers))
        check(name+'_uv',bool(obj.data.uv_layers))
        mat=obj.data.materials[0]
        tex=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE')
        bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        check(name+'_packed_image_drives_color',bool(tex.image.packed_file) and bs.inputs['Base Color'].is_linked)
        check(name+'_opaque_not_alpha_card',not bs.inputs['Alpha'].is_linked and bs.inputs['Alpha'].default_value==1)
    check('eight_physical_main_button_rivets',sum('_raised_rivet' in o.name for o in scene.objects)==8)
    audit=json.loads((OUT/'silhouette-audit.json').read_text(encoding='utf-8'))
    check('no_key_background_on_sampled_geometry',len(audit)==3 and all(a['key_color_leaks']==0 for a in audit),sum(a['key_color_probe_count'] for a in audit))
    source=json.loads((ROOT/'references/wm-panel-v03/provenance.json').read_text(encoding='utf-8'))
    check('all_generated_originals_and_prompts_intact',all(sha(ROOT/item['path'])==item['sha256'] and sha(ROOT/item['prompt'])==item['prompt_sha256'] for item in source['outputs']))
    completed=True
finally:
    report={'date':'2026-09-19','status':'PASS' if completed else 'FAIL','checks':checks,
       'visual_review':'See quality-review.md: real Blender renders reviewed separately; no final-art approval inferred.'}
    (OUT/'quality-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('WM V03 QUALITY',report['status'],len(checks),flush=True)

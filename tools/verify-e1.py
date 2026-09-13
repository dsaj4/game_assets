"""Verify actual E1 captures, imported-asset A/B geometry parity and evidence provenance."""
from pathlib import Path
import argparse, struct, json, hashlib, re

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--revision',choices=('r1','r2'),default='r2',
    help='Verify captures from this revision; build the matching revision first (default: r2).')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
out=root/('artifacts/ui-experiment/E1' if args.revision=='r1' else 'artifacts/ui-experiment/E1-r2')
asset_manifest=root/('art/e1/asset-manifest.json' if args.revision=='r1' else 'art/e1/asset-manifest-r2.json')
source_paths=[root/'art/build_e1.py',root/'game/builders/BuildE1.cs',root/'game/scripts/E1View.cs']
if args.revision=='r2':
    source_paths.extend([root/'art/refine_e1_r2.py',root/'art/e1/e1-r2-ui.blend'])
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def project_path(relative):
    path=(root/relative.replace('\\','/')).resolve()
    assert path.is_relative_to(root), f'Provenance path outside project: {relative}'
    return path
assets=json.loads(asset_manifest.read_text(encoding='utf-8'))
provenance={}
if args.revision=='r2':
    assert assets['revision']=='E1-r2', 'Wrong asset manifest revision'
    input_blend=assets['input_blend']
    ui_path=project_path(input_blend['path'])
    assert ui_path==root/'art/e1/e1-r2-ui.blend', 'Wrong native UI source'
    assert sha(ui_path)==input_blend['sha256'], 'Native UI source changed after build'
    source_hashes={name.replace('\\','/'):value for name,value in assets['sources'].items()}
    assert 'art/refine_e1_r2.py' in source_hashes, 'Refinement source hash missing'
    for name,expected in source_hashes.items():
        assert sha(project_path(name))==expected, f'Asset input changed after build: {name}'
    master=assets['master']
    assert sha(project_path(master['path']))==master['sha256'], 'R2 master changed after build'
    for variant in ('base','ink'):
        assert sha(root/f'game/assets/e1/e1_{variant}.glb')==assets[variant]['sha256'], f'Wrong {variant} runtime asset'
    audit_path=out/'ui-edit-audit.json'
    audit=json.loads(audit_path.read_text(encoding='utf-8-sig'))
    assert audit['status']=='PASS' and audit['object']=='TowerRoof', 'Native UI audit failed'
    assert len(audit['changed_vertices'])==4, 'Expected four UI-edited roof vertices'
    assert {'topology','object transform'}<=set(audit['unchanged']), 'UI edit changed unintended structure'
    for version in audit['versions'].values():
        assert sha(project_path(version['file']))==version['sha256'], 'UI audit source has changed'
    assert audit['versions']['r2_ui']['sha256']==input_blend['sha256'], 'Build and UI audit use different sources'
    native_edit=assets['native_ui_edit']
    assert native_edit['object']=='TowerRoof' and native_edit['preserved'] is True
    ui_mesh={name:audit['versions']['r2_ui'][name] for name in ('vertices','faces')}
    ui_mesh_sha=hashlib.sha256(json.dumps(ui_mesh,sort_keys=True).encode()).hexdigest()
    assert native_edit['mesh_sha256_before']==native_edit['mesh_sha256_after']==ui_mesh_sha, 'UI roof mesh was not preserved'
    provenance=dict(asset_manifest_sha256=sha(asset_manifest),
        ui_edit_audit=dict(file=str(audit_path.relative_to(root)).replace('\\','/'),
            sha256=sha(audit_path),status=audit['status'],changed_vertices=4),
        native_ui_source_sha256=input_blend['sha256'],native_ui_roof_preserved=True,
        all_manifest_source_hashes_match=True,runtime_glb_hashes_match=True,master_hash_matches=True)
def glb(path):
    data=path.read_bytes(); magic,version,length=struct.unpack_from('<III',data)
    assert magic==0x46546c67 and version==2 and length==len(data)
    n,kind=struct.unpack_from('<II',data,12); assert kind==0x4e4f534a
    doc=json.loads(data[20:20+n]); length,kind=struct.unpack_from('<II',data,20+n)
    assert kind==0x004e4942
    return doc,data[28+n:28+n+length]
docs=[]; positions=[]
for variant in ('base','ink'):
    doc,blob=glb(root/f'game/assets/e1/e1_{variant}.glb'); docs.append(doc)
    geometry=[]
    for mesh in doc['meshes']:
        for primitive in mesh['primitives']:
            for accessor_id in [primitive['attributes']['POSITION'],primitive['indices']]:
                accessor=doc['accessors'][accessor_id]; view=doc['bufferViews'][accessor['bufferView']]
                start=view.get('byteOffset',0)
                geometry.append(hashlib.sha256(blob[start:start+view['byteLength']]).hexdigest())
    positions.append(geometry)
    for name in ['OneWand','FixedInlay','TagAcquire','TagArmor','MapPaper','EncounterTokenBase','E1Camera']:
        assert sum(node.get('name')==name for node in doc['nodes'])==1, name
assert positions[0]==positions[1], 'Base/ink geometry changed'
assert docs[0]['nodes']==docs[1]['nodes'], 'Base/ink transforms changed'
assert docs[0]['cameras']==docs[1]['cameras'], 'Base/ink lens changed'
captures=[]
for size in [(1920,1080),(1280,720)]:
    for variant in ('base','ink'):
        stem=f'godot-{variant}-{size[0]}x{size[1]}'
        path=out/f'{stem}-final.png'; header=path.read_bytes()[:24]
        assert header[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',header[16:24])==size
        log=(out/f'{stem}.log').read_text(encoding='utf-8-sig')
        assert 'E1_TEXT_BOUNDS=PASS glyphs=PASS' in log
        assert f'E1_CAPTURE_SAVED={size[0]}x{size[1]}' in log
        assert 'NVIDIA GeForce RTX 5060 Laptop GPU' in log
        assert not (out/f'{stem}-error.log').read_text(encoding='utf-8-sig').strip()
        captures.append(dict(file=path.name,width=size[0],height=size[1],sha256=sha(path)))
for variant in ('Base','Ink'):
    scene=root/f'game/scenes/E1{variant}.tscn'
    assert scene.stat().st_size<10000
    assert 'type="PackedScene"' in scene.read_text(encoding='utf-8')
build=(out/'build.log').read_text(encoding='utf-8-sig')
for variant in ('base','ink'):
    assert re.search(f'E1_PACK_{variant}=PASS nodes_before=(\\d+) nodes_after=\\1',build)
result=dict(revision=args.revision,status='PASS_TECHNICAL',visual_status='NeedsRevision / user review pending',
    checks=['same geometry and transforms across A/B','same exported camera',
            'E1 required asset counts','packed scene node parity, no GLB inlining',
            'native NVIDIA Vulkan capture','4 PNG dimensions verified from headers',
            'Chinese glyph coverage and label bounds at both resolutions','no runtime stderr'],
    assets=assets,
    source_sha256={str(p.relative_to(root)).replace('\\','/'):sha(p) for p in source_paths},
    captures=captures,not_tested=['E2','E3','E4','60-second performance','user style acceptance','font redistribution'])
if args.revision=='r2':
    result['checks'].extend(['R2 source, master and GLB hashes match manifest',
        'native Blender UI audit PASS and source hashes match',
        'four UI-edited roof vertices preserved through refinement'])
    result['provenance']=provenance
(out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

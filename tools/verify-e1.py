"""Verify actual E1 captures, imported-asset A/B geometry parity and evidence provenance."""
from pathlib import Path
import struct, json, hashlib, re

root=Path(__file__).resolve().parents[1]
out=root/'artifacts/ui-experiment/E1'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
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
result=dict(status='PASS_TECHNICAL',visual_status='NeedsRevision / user review pending',
    checks=['same geometry and transforms across A/B','same exported camera',
            'E1 required asset counts','packed scene node parity, no GLB inlining',
            'native NVIDIA Vulkan capture','4 PNG dimensions verified from headers',
            'Chinese glyph coverage and label bounds at both resolutions','no runtime stderr'],
    assets=json.loads((root/'art/e1/asset-manifest.json').read_text(encoding='utf-8')),
    source_sha256={str(p.relative_to(root)).replace('\\','/'):sha(p) for p in [root/'art/build_e1.py',root/'game/builders/BuildE1.cs',root/'game/scripts/E1View.cs']},
    captures=captures,not_tested=['E2','E3','E4','60-second performance','user style acceptance','font redistribution'])
(out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

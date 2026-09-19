"""Read-only mesh/state comparison and generated PNG channel inspection."""
from pathlib import Path
import sys, json, hashlib
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'artifacts/wm-quality-audit'
out.mkdir(parents=True, exist_ok=True)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def snapshot(version):
    path = ROOT / f'art/wand-management-{version}/wand-management-master.blend'
    bpy.ops.wm.open_mainfile(filepath=str(path))
    result = {}
    for obj in bpy.context.scene.objects:
        record = {'type': obj.type, 'matrix': [list(r) for r in obj.matrix_local]}
        if obj.type == 'MESH':
            record['geometry'] = digest([[list(v.co) for v in obj.data.vertices], [list(p.vertices) for p in obj.data.polygons]])
        elif obj.type == 'FONT':
            record['text'] = obj.data.body
        result[obj.name] = record
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'objects': result}

a, b = snapshot('v01'), snapshot('v02')
changes = [n for n in a['objects'].keys() & b['objects'].keys() if a['objects'][n] != b['objects'][n]]
report = {'v01_sha256': a['sha256'], 'v02_sha256': b['sha256'],
          'changed_geometry_transforms_or_text': changes,
          'removed': sorted(a['objects'].keys() - b['objects'].keys()),
          'added': sorted(b['objects'].keys() - a['objects'].keys())}
report['images'] = []
for name in sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []:
    im = bpy.data.images.load(name, check_existing=False)
    pixels = np.array(im.pixels[:], dtype=np.float32).reshape(im.size[1], im.size[0], 4)
    alpha = pixels[:, :, 3]
    report['images'].append({'file': name, 'size': list(im.size), 'channels': im.channels,
       'alpha_min': float(alpha.min()), 'alpha_max': float(alpha.max()),
       'transparent_fraction': float(np.mean(alpha < .01))})
(out/'baseline-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True, indent=2))

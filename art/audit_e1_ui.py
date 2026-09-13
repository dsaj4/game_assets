"""Read-only comparison of the preserved R1 roof and the native Blender UI edit."""
from pathlib import Path
import hashlib
import json
import bpy

root = Path(__file__).resolve().parents[1]
versions = {}
for name, file in (("r1", "e1-style-master.blend"), ("r2_ui", "e1-r2-ui.blend")):
    path = root / "art/e1" / file
    bpy.ops.wm.open_mainfile(filepath=str(path))
    roof = bpy.data.objects["TowerRoof"]
    versions[name] = dict(file=f"art/e1/{file}", sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          vertices=[list(v.co) for v in roof.data.vertices],
                          faces=[list(p.vertices) for p in roof.data.polygons],
                          matrix=[list(row) for row in roof.matrix_world])
before, after = versions["r1"], versions["r2_ui"]
assert before["faces"] == after["faces"]
assert before["matrix"] == after["matrix"]
assert len(before["vertices"]) == len(after["vertices"])
changed = []
for index, (a, b) in enumerate(zip(before["vertices"], after["vertices"])):
    delta = [b[i] - a[i] for i in range(3)]
    if max(abs(x) for x in delta) > 1e-6:
        changed.append(dict(index=index, local_delta=delta))
assert len(changed) == 4, changed
result = dict(status="PASS", object="TowerRoof", operation="Native Blender UI: move top face +0.18 on world X",
              unchanged=["topology", "object transform"], changed_vertices=changed, versions=versions)
out = root / "artifacts/ui-experiment/E1-r2/ui-edit-audit.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print("E1_UI_EDIT=PASS changed_vertices=4")

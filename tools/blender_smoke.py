"""Temporary environment probe; never a game asset or visual-style sample."""
import json
from pathlib import Path
import sys
import bpy

output = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "EnvironmentProbe"
bpy.ops.wm.save_as_mainfile(filepath=str(output / "probe.blend"))
bpy.ops.export_scene.gltf(filepath=str(output / "cube.glb"), export_format="GLB")
(output / "blender.json").write_text(json.dumps({
    "blender": bpy.app.version_string,
    "python": sys.version,
    "objects": len(bpy.data.objects),
    "glb_bytes": (output / "cube.glb").stat().st_size,
    "scope": "environment-only; no UI/gameplay/style evaluation",
}, indent=2), encoding="utf-8")
print("BLENDER_ENVIRONMENT_PASS")

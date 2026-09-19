"""Actual Blender detail renders; never flatten or modify source texture images."""
from pathlib import Path
import sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from wm_tools import *
OUT=ROOT/'art/wand-management-v03'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'wand-management-master.blend'))
scene=bpy.context.scene
for o in scene.objects:
    if o.type in GEO_TYPES:
        o.hide_render=not o.name.startswith(('WM07_Back_','WM07_Save_'))
col=bpy.data.collections.new('DETAIL_BACKDROP');scene.collection.children.link(col)
neutral=material('Detail warm neutral',(.12,.105,.08))
box('DETAIL_BACKGROUND',(-.27,.07,.236),(4,.01,2),neutral,col,None)
scene.camera.location=(-.08,-2.2,.60)
point_camera(scene.camera,(-.27,-.075,.236))
scene.camera.data.ortho_scale=1.55
scene.render.resolution_x=1600;scene.render.resolution_y=460;scene.render.resolution_percentage=100
scene.cycles.samples=40
scene.render.filepath=str(OUT/'renders/buttons-detail.png')
bpy.ops.render.render(write_still=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'assets/WM-06-configuration-parchment.blend'))
scene=bpy.context.scene
col=next(c for c in scene.collection.children if c.name.startswith('WM-06_ASSET'))
lo,hi,_=bounds(col.all_objects);center=(lo+hi)/2
scene.camera.location=center+Vector((.62,-3.6,.75))
point_camera(scene.camera,center);scene.camera.data.ortho_scale=2.90
scene.render.resolution_x=1600;scene.render.resolution_y=850
scene.render.filepath=str(OUT/'renders/panel-oblique-detail.png')
bpy.ops.render.render(write_still=True)

"""Refine the saved v01 master using four user-provided image textures; never rebuild v01."""
from pathlib import Path
import sys, json
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wm_tools import *
OUT = ROOT / 'art/wand-management-v02'
SRC = ROOT / 'art/wand-management-v01'
TEX = ROOT / 'references/wm-textures-v02'
if (OUT/'wand-management-master.blend').exists() and '--replace-v02' not in sys.argv:
    raise RuntimeError('v02 exists; explicit --replace-v02 required')
for folder in ('assets','renders'):(OUT/folder).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SRC/'wand-management-master.blend'))
bpy.context.preferences.filepaths.save_version=0

def textured(name, filename, rough, bump_strength, bump_distance):
    mat=material(name,(.4,.3,.2),TEX/filename,rough=rough)
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    tex=next(n for n in nodes if n.type=='TEX_IMAGE');tex.extension='EXTEND'
    bs=nodes['Principled BSDF'];bs.inputs['Specular IOR Level'].default_value=.20
    bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=bump_strength
    bump.inputs['Distance'].default_value=bump_distance
    links.new(tex.outputs['Color'],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])
    return mat
paper=textured('WM Ivory parchment v02','parchment-ivory.jpg',.95,.10,.0007)
back=textured('WM Charcoal stitched return v02','button-return-charcoal.jpg',.86,.13,.0009)
save=textured('WM Burgundy stitched save v02','button-save-burgundy.jpg',.84,.13,.0009)
fine=textured('WM Fine brown leather v02','leather-fine-brown.jpg',.91,.15,.0008)
# Preserve full-surface coordinates for bounded sheets. For the plain leather,
# each component is deliberately sampled once; it is not advertised as seamless.
for obj in bpy.data.objects:
    if obj.type not in GEO_TYPES:continue
    for slot in obj.material_slots:
        if slot.material and slot.material.name=='WM Warm parchment':slot.material=paper
        elif slot.material and slot.material.name=='WM Russet whole hide':slot.material=fine

def assign(obj,mat):obj.data.materials.clear();obj.data.materials.append(mat)
def planar(obj):
    uv=obj.data.uv_layers.active or obj.data.uv_layers.new(name='UVMap')
    xs=[v.co.x for v in obj.data.vertices];zs=[v.co.z for v in obj.data.vertices]
    for loop in obj.data.loops:
        p=obj.data.vertices[loop.vertex_index].co
        uv.data[loop.index].uv=((p.x-min(xs))/(max(xs)-min(xs)),(p.z-min(zs))/(max(zs)-min(zs)))
# The two primary faces keep original full 0..1 sheet UVs and native lettering.
for prefix,mat in [('WM07_Back',back),('WM07_Save',save)]:
    body=bpy.data.objects[prefix+'_body'];assign(body,mat)
    for mod in body.modifiers:
        if mod.type=='SOLIDIFY':mod.thickness=.009
    col=next(c for c in body.users_collection if c.name.startswith('WM-07'))
    vs=body.data.vertices
    center=tuple((min(v.co[i] for v in vs)+max(v.co[i] for v in vs))/2 for i in range(3))
    box(prefix+'_leather_backing',(center[0],center[1]+.012,center[2]),(.617,.018,.178),fine,col,body.parent,.005)
    # Printed stitch border is already complete; the old corner pins would overlap it.
    for obj in list(bpy.data.objects):
        if obj.name.startswith(prefix+'_pin') or obj.name==prefix+'_ink_edge':bpy.data.objects.remove(obj,do_unlink=True)
light=bpy.data.materials['WM Warm text highlight']
light.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.87,.77,.57,1)
for name in ('WM07_Move_forward','WM07_Move_back'):
    obj=bpy.data.objects[name];assign(obj,fine);planar(obj)
# Clear action hierarchy: brown leather for small +/- and transfer controls;
# numeric value, timeline, labels remain ivory paper with dark ink.
for prefix in ('WM06_To_reserve','WM06_Start_-','WM06_Start_+'):
    body=bpy.data.objects[prefix+'_body'];assign(body,fine)
    assign(bpy.data.objects[prefix+'_text'],light)
    for mod in body.modifiers:
        if mod.type=='SOLIDIFY':mod.thickness=.005
excluded=next(c for c in bpy.data.collections if c.name.startswith('TEXT_WITHOUT_FREESTYLE'))
for obj in bpy.data.objects:
    if obj.type=='FONT' and obj.active_material==light and obj.name not in excluded.objects:excluded.objects.link(obj)
scene=bpy.context.scene
scene['texture_revision']='v02 / four user-supplied JPEGs / 2026-09-18'
scene.render.filepath=str(OUT/'renders/assembly.png')
pack_images();bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'wand-management-master.blend'),compress=True)
(OUT/'source-catalog.json').write_bytes((SRC/'source-catalog.json').read_bytes())
revision={'date':'2026-09-18','status':'TextureRefined / NeedsArtReview','user_scope':'User supplied four external textures; refine existing left management page',
'method':'Blender bundled Python; editable native meshes, curves, fonts; no GUI modeling claimed',
'additional_textures':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'role':'User supplied external image; original bytes; service/model unknown'} for p in sorted(TEX.glob('*.jpg'))],
'additional_preserved_files':[{'path':'art/wand-management-v01/wand-management-master.blend','sha256':sha(SRC/'wand-management-master.blend')} ]}
(OUT/'revision.json').write_text(json.dumps(revision,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Quick actual preview, after saving the full-resolution master.
scene.render.resolution_percentage=65
scene.cycles.samples=24
scene.render.filepath=str(OUT/'renders/preview.png')
bpy.ops.render.render(write_still=True)

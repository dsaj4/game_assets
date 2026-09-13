"""Refine the existing E1 page after the native Blender UI roof edit.

Run with Blender --background --python-exit-code 1 --python art/refine_e1_r2.py.
The only scene input is art/e1/e1-r2-ui.blend. Never rebuild or import build_e1.
Generated images are read unchanged; variation comes from UVs and real geometry.
"""
from pathlib import Path
import hashlib
import json
import math
import random

import bmesh
import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "art/e1"
INPUT = ART / "e1-r2-ui.blend"
REFERENCES = ROOT / "references/e1-r2-generated"
ASSETS = ROOT / "game/assets/e1"
EVIDENCE = ROOT / "artifacts/ui-experiment/E1-r2"
SEED = 213
rng = random.Random(SEED)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh_sha(obj):
    # Exact local coordinates and topology preserve the hand-edited roof.
    payload = {"vertices": [list(v.co) for v in obj.data.vertices],
               "faces": [list(p.vertices) for p in obj.data.polygons]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


if not INPUT.is_file():
    raise FileNotFoundError(f"Save the native UI edit first: {INPUT}")
input_sha = sha(INPUT)
bpy.ops.wm.open_mainfile(filepath=str(INPUT))
if bpy.context.object and bpy.context.object.mode != "OBJECT":
    bpy.ops.object.mode_set(mode="OBJECT")
scene = bpy.context.scene
roof = bpy.data.objects["TowerRoof"]
roof_mesh_before = mesh_sha(roof)
roof_matrix_before = [list(row) for row in roof.matrix_world]
for directory in (ART, ASSETS, EVIDENCE):
    directory.mkdir(parents=True, exist_ok=True)

required_anchors = ["TagAcquireText", "TagArmorText", "MapTitle", "MapCaption",
                    "EncounterCaption", "InlayCaption", "WandCaption"]
for name in required_anchors:
    if bpy.data.objects.get(name) is None:
        raise ValueError(f"Missing original UI anchor: {name}")

wood_path = REFERENCES / "wood-ink-albedo-v01.png"
map_path = REFERENCES / "map-paper-albedo-v01.png"
board_path = REFERENCES / "wand-tower-modeling-board-v01.png"
wood_image = bpy.data.images.load(str(wood_path), check_existing=True)
map_image = bpy.data.images.load(str(map_path), check_existing=True)
variant_textures = []
variant_ink = []


def material(name, color, image=None, metal=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = .96
    bsdf.inputs["Metallic"].default_value = metal
    if image:
        tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = image
        tex.extension = "EXTEND"
        tex.interpolation = "Linear"
        variant_textures.append((mat, bsdf, tex))
    return mat


wood = material("R2 AI etched grey olive wood", (.115, .119, .087), wood_image)
bark = material("R2 old branch bark", (.070, .075, .053), wood_image)
paper = material("R2 quiet grey ivory word paper", (.67, .65, .56), map_image)
mapmat = material("R2 AI border terrain paper", (.67, .65, .56), map_image)
ink = material("R2 charcoal cuts", (.014, .019, .015))
variant_ink.append(ink)
rootmat = material("R2 dark exposed roots", (.069, .074, .046))
root_highlight = material("R2 rubbed root ridges", (.235, .195, .125))
wood_highlight = material("R2 worn warm grey wood ridges", (.31, .275, .19))
lining = material("R2 deep charcoal wand lining", (.021, .031, .024))
lining_edge = material("R2 lining folded edge", (.051, .061, .042))
hemp = material("R2 short worn hemp loops", (.23, .205, .135))
bronze = material("R2 oxidised copper bands", (.155, .139, .079), metal=.12)
stone = material("R2 cold weathered stone", (.28, .295, .25))
stones = [material(f"R2 masonry {i}", (.25 + i*.017, .263 + i*.018, .224 + i*.014))
          for i in range(4)]
slates = [material(f"R2 grey slate {i}", (.047+i*.009, .061+i*.010, .052+i*.009))
          for i in range(4)]
emerald = material("R2 deep emerald", (.008, .145, .065))
emerald_shine = material("R2 emerald light facets", (.10, .39, .22))
emerald_mid = material("R2 emerald middle facets", (.014, .225, .105))


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def line(name, points, radius=.012, mat=ink, taper=None):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = radius
    curve.bevel_resolution = 1
    spline = curve.splines.new("POLY")
    spline.points.add(len(points)-1)
    for i, (point, position) in enumerate(zip(spline.points, points)):
        point.co = (*position, 1)
        if taper:
            point.radius = taper(i/max(1, len(points)-1))
    obj = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(obj)
    return assign(obj, mat)


def block(name, location, dimensions, mat, bevel=.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    if bevel:
        modifier = obj.modifiers.new("Hand worn block edges", "BEVEL")
        modifier.width = bevel
        modifier.segments = 1
    return obj


def face(name, points, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(points, [], [tuple(range(len(points)))])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    return assign(obj, mat)


def remove_named_prefixes(prefixes):
    # Only specified old decorative pieces, never the hand-edited tower roof.
    for obj in list(scene.objects):
        if any(obj.name.startswith(prefix) for prefix in prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)


# Each existing plank gets a narrow, nonrepeating window into the original square
# image. A physically proportional UV band avoids flattening every knot.
wood_objects = [obj for obj in scene.objects if obj.type == "MESH"
                and any(m and m.name == "Etched olive wood" for m in obj.data.materials)]
wood_uv_windows = {}
for number, obj in enumerate(sorted(wood_objects, key=lambda item: item.name)):
    local = [vertex.co.copy() for vertex in obj.data.vertices]
    bounds_min = Vector([min(v[axis] for v in local) for axis in range(3)])
    bounds_max = Vector([max(v[axis] for v in local) for axis in range(3)])
    spans = bounds_max - bounds_min
    if spans.x > 2:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=5, use_grid_fill=True)
        bm.to_mesh(obj.data)
        bm.free()
        for vertex in obj.data.vertices:
            t = (vertex.co.x-bounds_min.x)/spans.x
            envelope = math.sin(math.pi*t)
            vertex.co.y += .015*math.sin(t*7.0 + number*.77)*envelope
            vertex.co.z += (.024*math.sin(t*5.2 + number*.59)
                            + .011*math.sin(t*12.0+number))*envelope
    uv = obj.data.uv_layers.active or obj.data.uv_layers.new(name="UVMap")
    u0, u_span = .02+(number%4)*.025, .79+(number%3)*.04
    ratio = min(.45, max(.015, spans.y/max(spans.x, .01)))
    v_span = u_span*ratio
    v0 = .03+((number*.173)%(.89-v_span))
    for polygon in obj.data.polygons:
        normal_axis = max(range(3), key=lambda axis: abs(polygon.normal[axis]))
        for loop_index in polygon.loop_indices:
            vertex = obj.data.vertices[obj.data.loops[loop_index].vertex_index].co
            along = (vertex.x-bounds_min.x)/max(spans.x, .01)
            cross_axis = 1 if normal_axis == 2 else 2
            cross = (vertex[cross_axis]-bounds_min[cross_axis])/max(spans[cross_axis], .01)
            uv.data[loop_index].uv = (u0+along*u_span, v0+cross*v_span)
    obj.data.update()
    assign(obj, wood)
    wood_uv_windows[obj.name] = [u0, u_span, v0, v_span]

# The same original paper image supplies clean tag centres and the map's full
# border terrain. No image pixels are transformed, painted over or resaved.
assign(bpy.data.objects["MapPaper"], mapmat)
for name in ("TagAcquire", "TagArmor"):
    obj = bpy.data.objects[name]
    assign(obj, paper)
    for point in obj.data.uv_layers.active.data:
        point.uv = (.32+point.uv.x*.31, .60+point.uv.y*.29)

# A real, shallow lining lies behind this one existing wand. Its top is below
# both support feet and the tags, leaving their silhouettes unobscured. This
# quiet patch separates bark from cabinet grain; it is not an extra wand slot.
lining_outline = [(-7.58,-.66,.155),(-7.53,.31,.158),(-7.34,.39,.160),
                  (-.05,.38,.156),(.13,.28,.155),(.13,-.61,.153),
                  (-.05,-.72,.154),(-7.37,-.74,.156)]
lining_object = face("R2 lining behind existing wand", list(reversed(lining_outline)), lining)
lining_object.modifiers.new("Thin fabric backing", "SOLIDIFY").thickness = .027
line("R2 folded lining perimeter", [Vector(p)+Vector((0,0,.014))
     for p in lining_outline+[lining_outline[0]]], .018, lining_edge)

# Replace the two angular cord strokes with small loops around the same pegs.
remove_named_prefixes(("Tag cord",))
for x in (-5.4,-2.8):
    points = [(x+.066*math.cos(a),2.005+.176*math.sin(a),.625+.018*math.cos(a))
              for a in [i*math.tau/48 for i in range(49)]]
    line("R2 tag tied cord loop", points, .016, hemp)
    line("R2 tag cord short tail", [(x+.025,1.865,.643),(x+.042,1.82,.647),
                                    (x+.079,1.79,.631)], .012, hemp,
         taper=lambda t:1-.45*t)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.041,
                                         location=(x,2.175,.615))
    peg = bpy.context.object
    peg.name = "R2 existing tag peg head"
    peg.scale = (1,.8,.65)
    assign(peg,bronze)

# Rework the existing 45-ring shaft instead of replacing its mesh. Keep its
# endpoints and the fixed inlay's transform, varying only local branch thickness.
wand = bpy.data.objects["OneWand"]
assign(wand, bark)
rings = {}
for vertex in wand.data.vertices:
    rings.setdefault(round(vertex.co.x, 5), []).append(vertex)
xs = sorted(rings)
centres = []
for x in xs:
    vertices = rings[x]
    centre = sum((v.co for v in vertices), Vector())/len(vertices)
    t = (x-xs[0])/(xs[-1]-xs[0])
    thickness = (.90+.09*math.sin(t*17)
                 + .38*math.exp(-((t-.70)/.07)**2)
                 + .24*math.exp(-((t-.38)/.055)**2))
    centre.y += .022*math.sin(t*9)*math.sin(t*math.pi)
    centre.z += .023*math.sin(t*13)*math.sin(t*math.pi)
    original = sum((v.co for v in vertices), Vector())/len(vertices)
    for vertex in vertices:
        offset = vertex.co-original
        vertex.co = centre+Vector((offset.x, offset.y*thickness, offset.z*thickness))
    centres.append(centre)
for loop in wand.data.uv_layers.active.data:
    loop.uv = (.05+loop.uv.x*.89, .53+loop.uv.y*.055)
wand.data.update()
remove_named_prefixes(("Spiral carved vine", "Shaft ink edge", "Roof hatch", "Stone courses", "Stone joints"))


def centre_at(t):
    index = min(len(centres)-2, max(0, int(t*(len(centres)-1))))
    fraction = t*(len(centres)-1)-index
    return centres[index].lerp(centres[index+1], fraction)


def shaft_radius(t):
    return (.075+.095*t)*(.90+.09*math.sin(t*17)
            + .38*math.exp(-((t-.70)/.07)**2)
            + .24*math.exp(-((t-.38)/.055)**2))


for edge_phase in (.15, math.pi+.12, 1.55):
    points = []
    for i in range(100):
        t = i/99
        c = centre_at(t)
        radius = shaft_radius(t)*1.015
        points.append(c+Vector((0, math.sin(edge_phase)*radius, math.cos(edge_phase)*radius)))
    line("R2 shaft ink fissure", points, .010)

# Short rubbed ridges catch the key light on the exposed upper-front bark.
# Break the highlight around knots, rather than drawing a uniform bright rail.
for start,end in ((.018,.30),(.45,.63),(.78,.91)):
    points = []
    for i in range(48):
        t = start+(end-start)*i/47
        c = centre_at(t)
        angle = -.65+.11*math.sin(t*23)
        radius = shaft_radius(t)*1.035
        points.append(c+Vector((0,math.sin(angle)*radius,math.cos(angle)*radius)))
    line("R2 exposed warm grey bark ridge",points,.012,wood_highlight,
         taper=lambda t:.30+.70*math.sin(math.pi*t))

# Two uneven roots with pauses and a few short curled ends replace the old
# uniform bright double helix. Their silhouette stays close to the branch.
for index, (start, end, phase) in enumerate(((.14, .92, .4), (.57, 1.0, 3.2))):
    points = []
    for i in range(100):
        u = i/99
        t = start+(end-start)*u
        c = centre_at(t)
        a = phase+u*(10.8 if index == 0 else 6.4)+.40*math.sin(u*8)
        radius = shaft_radius(t)+.027+.022*math.sin(u*6)**2
        points.append(c+Vector((0, radius*math.sin(a), radius*math.cos(a))))
    line("R2 wandering bark root", points, .028, root_highlight,
         taper=lambda t: .55+.45*math.sin(math.pi*t))
for t in (.37, .70):
    c = centre_at(t)
    radius = shaft_radius(t)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1,
                                         location=c+Vector((0, -.018, radius*.75)))
    knot = bpy.context.object
    knot.name = "R2 grown branch knot"
    knot.scale = (.23, .115, .077)
    assign(knot, rootmat)
    for ring in (1.0, .62):
        points = [(c.x+.175*ring*math.cos(a), c.y+.086*ring*math.sin(a),
                   c.z+radius+.036+.008*math.sin(a*3))
                  for a in [i*math.tau/48 for i in range(49)]]
        line("R2 knot heart ring", points, .010, ink)

for t, width in ((.075, .09), (.255, .035), (.83, .07)):
    c = centre_at(t)
    radius = shaft_radius(t)+.018
    for offset in (-width, 0, width):
        points = [(c.x+offset, c.y+radius*math.sin(a), c.z+radius*math.cos(a))
                  for a in [i*math.tau/40 for i in range(41)]]
        line("R2 worn copper grip band", points, .021, bronze)

gem = bpy.data.objects["FixedInlay"]
gem_transform = [list(row) for row in gem.matrix_world]
assign(gem, emerald)
gem.data.materials.append(emerald_mid)
gem.data.materials.append(emerald_shine)
light_facets = sorted(gem.data.polygons, key=lambda p: p.normal.z-.4*p.normal.x, reverse=True)
for polygon in gem.data.polygons:
    polygon.material_index = 1 if polygon.normal.y < -.25 else 0
for polygon in light_facets[:2]:
    polygon.material_index = 2
for obj in scene.objects:
    if obj.name.startswith("Inlay socket"):
        assign(obj, bronze)
    elif obj.name.startswith("Inlay highlight"):
        assign(obj, emerald_shine)
        obj.data.bevel_depth = .014
for phase in (.3, 2.0, 3.7, 5.1):
    points = []
    for i in range(40):
        t = i/39
        angle = phase+.30*math.sin(t*math.pi)
        points.append((-1.88+t*.87,
                       -.30+(.19+t*.15)*math.sin(angle),
                       .89+(.17+t*.07)*math.cos(angle)))
    line("R2 root prong around fixed inlay", points, .036, root_highlight,
         taper=lambda t: 1.0-.58*t)

# Keep the single encounter miniature and the manual roof. Masonry is added to
# the current tower's sides; it creates no extra encounter token or map node.
tower = bpy.data.objects["Tower"]
assign(tower, stone)
assign(roof, slates[0])
for obj in scene.objects:
    if obj.type == "MESH" and any(m and m.name == "Warm stone" for m in obj.data.materials):
        assign(obj, stone)
    elif obj.name.startswith("Finial"):
        assign(obj, bronze)


def arch_points(cx, y, base, radius, spring):
    points = [(cx-radius, y, base), (cx+radius, y, base)]
    points += [(cx+radius*math.cos(i*math.pi/12), y,
                spring+radius*math.sin(i*math.pi/12)) for i in range(13)]
    return points


door = bpy.data.objects["Door"]
door.data = bpy.data.meshes.new("R2 arched door opening")
door.location = (0,0,0)
door.rotation_euler = (0,0,0)
door.scale = (1,1,1)
door.data.from_pydata(arch_points(4.3, -.628, .90, .145, 1.24), [], [tuple(range(15))])
door.data.update()
door.modifiers.clear()
assign(door, ink)
for side in (-1, 1):
    for j in range(3):
        block("R2 door jamb stone", (4.3+side*.178, -.646, .97+j*.108),
              (.075, .065, .097), stones[(j+1)%4], .008)
for j in range(7):
    a0, a1 = j*math.pi/7+.012, (j+1)*math.pi/7-.012
    points = [(4.3+r*math.cos(a), -.658, 1.24+r*math.sin(a))
              for r, a in ((.148,a0),(.225,a0),(.225,a1),(.148,a1))]
    obj = face("R2 arch voussoir", points, stones[j%4])
    obj.modifiers.new("Stone arch depth", "SOLIDIFY").thickness = .045
for x in (4.22, 4.29, 4.36):
    line("R2 door timber slit", [(x,-.636,.92),(x,-.636,1.22)], .007, rootmat)
block("R2 doorway threshold", (4.3,-.697,.886), (.39,.19,.07), stones[2], .011)

for row in range(5):
    z = .91+row*.175
    for col in range(5):
        x = 3.925+col*.164+(row%2)*.075
        if x > 4.68 or (abs(x-4.3)<.26 and z<1.51):
            continue
        block("R2 front staggered masonry", (x,-.606-rng.uniform(.006,.018),z),
              (.15,.035,.145), stones[(row+col)%4], .009)
    for col in range(4):
        y = -.515+col*.18+(row%2)*.065
        if y > .145:
            continue
        block("R2 side staggered masonry", (4.710+rng.uniform(.001,.008),y,z),
              (.026,.16,.147), stones[(row+col+1)%4], .008)
for x in (4.09, 4.51):
    face("R2 narrow tower window", arch_points(x,-.647,1.52,.041,1.69), ink)
    line("R2 window lower sill", [(x-.052,-.655,1.514),(x+.052,-.655,1.514)], .012, stones[2])
line("R2 side slit window", [(4.737,-.16,1.54),(4.737,-.16,1.74)], .027, ink)

for x in (3.91, 4.69):
    for row in range(4):
        z = .90+row*.14
        depth = .22-row*.026
        block("R2 stepped corner buttress", (x,-.622,z),
              (.17-row*.016,depth,.132), stones[(row+1)%4], .012)

# Subdivide the actual four roof sides into slightly overlapping slate sheets.
# These are independent shallow pieces laid on the existing hand-edited mesh;
# the original roof vertices, topology and transform are never written to.
roof_slopes = 0
for polygon in roof.data.polygons:
    vertices = [roof.matrix_world @ roof.data.vertices[i].co for i in polygon.vertices]
    if len(vertices) != 4 or max(v.z for v in vertices)-min(v.z for v in vertices) < .4:
        continue
    middle = (max(v.z for v in vertices)+min(v.z for v in vertices))*.5
    pair = next((i for i in range(4) if vertices[i].z<middle and vertices[(i+1)%4].z<middle), None)
    if pair is None:
        continue
    a,b,c,d = [vertices[(pair+i)%4] for i in range(4)]
    normal = (b-a).cross(d-a).normalized()
    if normal.z < 0:
        normal = -normal

    def surface(u, t):
        return a.lerp(b,u).lerp(d.lerp(c,u),t)

    roof_slopes += 1
    for row in range(7):
        t0, t1 = .025+row*.125, min(.94,.025+(row+1)*.125+.021)
        columns = max(2, 7-row)
        for col in range(columns):
            u0, u1 = col/columns+.007, (col+1)/columns-.007
            lift = normal*(.012+(6-row)*.0015)
            points = [surface(u,t)+lift for u,t in ((u0,t0),(u1,t0),(u1,t1),(u0,t1))]
            obj = face("R2 fitted slate tile", points, slates[(col+row)%4])
            obj.modifiers.new("Slate thickness", "SOLIDIFY").thickness = .011
            line("R2 slate lower lip", [points[0]+normal*.004,points[1]+normal*.004], .007)
        line("R2 roof row seam", [surface(i/20,t0)+normal*.014 for i in range(21)], .007)
    for u in (0,1):
        line("R2 roof hip seam", [surface(u,i/24)+normal*.014 for i in range(25)], .012)
if roof_slopes != 4:
    raise ValueError(f"Expected the four original roof slopes, found {roof_slopes}")
if mesh_sha(roof) != roof_mesh_before or [list(row) for row in roof.matrix_world] != roof_matrix_before:
    raise ValueError("The native UI roof edit was changed by the refinement script")
if [list(row) for row in gem.matrix_world] != gem_transform:
    raise ValueError("Fixed inlay position changed")

camera = bpy.data.objects["E1Camera"]
camera.location = (0,-9.5,17.5)
camera.rotation_euler = (Vector((0,0,.2))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 18.6
scene.camera = camera
bpy.data.objects["EncounterCaption"].location.y = -1.6
scene.render.engine = "CYCLES"
scene.cycles.samples = 24
scene.render.resolution_x, scene.render.resolution_y = 1920,1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 0
if scene.world and scene.world.use_nodes:
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs[0].default_value = (.18,.20,.175,1)
    background.inputs[1].default_value = .60
for obj in scene.objects:
    if obj.type == "LIGHT":
        obj.data.color = (.965,.979,.936)

# Export one fixed scene twice. Material input links and ink colour alone vary.
old_contours = bpy.data.materials.get("Charcoal contours")
if old_contours:
    variant_ink.append(old_contours)
stats = {}
for is_ink in (False, True):
    variant = "ink" if is_ink else "base"
    for mat, bsdf, tex in variant_textures:
        for link in list(bsdf.inputs["Base Color"].links):
            mat.node_tree.links.remove(link)
        if is_ink:
            mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    for mat in variant_ink:
        mat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (
            (.014,.019,.015,1) if is_ink else (.078,.087,.066,1))
    path = ASSETS / f"e1_{variant}.glb"
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB", export_cameras=True,
                              export_lights=False, export_apply=True)
    scene.render.filepath = str(EVIDENCE / f"blender-{variant}-1080.png")
    bpy.ops.render.render(write_still=True)
    stats[variant] = {"glb_bytes":path.stat().st_size, "sha256":sha(path)}

# Pack raw input textures without changing their source files. Preserve r1 master
# and manifest; this revision has its own editable source and provenance record.
bpy.ops.file.pack_all()
master = ART / "e1-r2-master.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(master))
depsgraph = bpy.context.evaluated_depsgraph_get()
triangles = 0
mesh_objects = 0
for obj in scene.objects:
    if obj.type not in {"MESH","CURVE"}:
        continue
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    triangles += len(mesh.loop_triangles)
    mesh_objects += 1
    evaluated.to_mesh_clear()
stats.update(
    revision="E1-r2", seed=SEED, mesh_objects=mesh_objects, triangles=triangles,
    camera=list(camera.location), ortho_width=18.6,
    content={"wands":1,"fixed_inlays":1,"word_tags":2,"maps":1,"encounter_tokens":1},
    anchors=required_anchors, wood_uv_windows=wood_uv_windows,
    input_blend={"path":str(INPUT.relative_to(ROOT)),"sha256":input_sha},
    native_ui_edit={"object":"TowerRoof", "mesh_sha256_before":roof_mesh_before,
                    "mesh_sha256_after":mesh_sha(roof), "preserved":True},
    sources={str(path.relative_to(ROOT)):sha(path) for path in
             (Path(__file__).resolve(), wood_path, map_path, board_path)},
    generated_image_usage={"wood":"Unchanged source image, per-plank narrow UV strips",
                           "map":"Unchanged source image, full map UV and clean tag UV crop",
                           "modeling_board":"Visual modeling reference only; never runtime art"},
    master={"path":str(master.relative_to(ROOT)),"sha256":sha(master)},
    provenance="Original r1 assets + preserved native Blender UI roof edit + bpy refinement; AI-generated wood/paper albedo originals used with recorded source hashes.")
(ART / "asset-manifest-r2.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("E1_R2_ASSETS_READY " + json.dumps(stats,ensure_ascii=False))

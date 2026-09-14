"""Native Blender helpers for the left management-page assets; metres, front -Y."""
from pathlib import Path
import math
import random
import hashlib
import bpy
from mathutils import Vector
from md11_tools import mesh, curves, tube, material, pack_images, point_camera

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art/wand-management-v01'
FONT_PATH = Path('C:/Windows/Fonts/simkai.ttf')
GEO_TYPES = {'MESH', 'CURVE', 'FONT'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def group(scene, name, location=(0, 0, 0), asset_id=None):
    col = bpy.data.collections.new(name)
    scene.collection.children.link(col)
    root = bpy.data.objects.new(name + '_ROOT', None)
    col.objects.link(root)
    root.location = location
    root.empty_display_size = .035
    if asset_id:
        root['asset_id'] = asset_id
    root['front_axis'] = '-Y'
    return col, root


def box(name, center, size, mat, col, parent, bevel=.003):
    x, y, z = center
    a, b, c = [v / 2 for v in size]
    vs = [(x+dx*a, y+dy*b, z+dz*c) for dz in (-1, 1) for dy in (-1, 1) for dx in (-1, 1)]
    fs = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    obj = mesh(name, vs, fs, mat, col, parent)
    uv = obj.data.uv_layers.new(name='UVMap')
    lengths = Vector(size)
    for p in obj.data.polygons:
        normal_axis = max(range(3), key=lambda k: abs(p.normal[k]))
        axes = sorted([k for k in range(3) if k != normal_axis], key=lambda k: lengths[k], reverse=True)
        for li in p.loop_indices:
            v = obj.data.vertices[obj.data.loops[li].vertex_index].co - Vector(center) + lengths / 2
            uv.data[li].uv = (.035 + .91*v[axes[0]]/lengths[axes[0]], .19 + .21*v[axes[1]]/lengths[axes[1]])
    if bevel:
        m = obj.modifiers.new('Worn rounded edge', 'BEVEL')
        m.width = bevel
        m.segments = 2
    return obj


def ring(name, center, radius, thickness, mat, col, parent, plane='XZ', n=40):
    pts = []
    for k in range(n + 1):
        a = math.tau * k / n
        v = (radius*math.cos(a), 0, radius*math.sin(a)) if plane == 'XZ' else (radius*math.cos(a), radius*math.sin(a), 0)
        pts.append(Vector(center) + Vector(v))
    return curves(name, [pts], thickness, mat, col, parent)


def pin(name, center, radius, mat, col, parent):
    x, y, z = center
    return tube(name, [(x, y+.006, z), (x, y, z), (x, y-.003, z)], [radius*.7, radius, radius*.63], mat, col, parent, 12)


def text(name, body, location, size, mat, col, parent, max_width=None, align='CENTER'):
    data = bpy.data.curves.new(name, 'FONT')
    data.body = body
    data.font = bpy.data.fonts.get('WM_Kai') or bpy.data.fonts.load(str(FONT_PATH))
    data.font.name = 'WM_Kai'
    data.align_x = align
    data.align_y = 'CENTER'
    data.size = size
    data.space_line = 1.1
    data.resolution_u = 4
    data.extrude = .00012
    obj = bpy.data.objects.new(name, data)
    col.objects.link(obj)
    obj.parent = parent
    obj.location = location
    obj.rotation_euler.x = math.pi/2
    data.materials.append(mat)
    obj['role'] = 'Editable text; not baked into albedo'
    obj.visible_shadow = False
    bpy.context.view_layer.update()
    if max_width and obj.dimensions.x > max_width:
        data.size *= max_width / obj.dimensions.x
    return obj


def sheet(name, center, size, mat, col, parent, curl=.012, thickness=.002, seed=1, nx=32, nz=18):
    """One connected grid, with curved and ragged free edges; explicit UVs."""
    x, y, z = center
    w, h = size
    def point(u, v):
        edge_x = abs(2*u-1)**18
        edge_z = abs(2*v-1)**18
        xx = x + (u-.5)*w + .006*edge_x*math.sin(v*51+seed)
        zz = z + (v-.5)*h + .004*edge_z*math.sin(u*67+seed)
        yy = y - curl*(edge_x*(.6+.4*math.sin(v*16+seed)) + edge_z*(.55+.45*math.cos(u*13+seed)))
        yy += curl*.11*math.sin(u*13+v*18+seed)
        return (xx, yy, zz)
    vs = [point(i/nx, j/nz) for j in range(nz+1) for i in range(nx+1)]
    uv = [(i/nx, j/nz) for j in range(nz+1) for i in range(nx+1)]
    fs = []
    for j in range(nz):
        for i in range(nx):
            a = j*(nx+1)+i
            fs.append((a, a+1, a+nx+2, a+nx+1))
    obj = mesh(name, vs, fs, mat, col, parent, uv, True)
    sol = obj.modifiers.new('Editable sheet thickness', 'SOLIDIFY')
    sol.thickness = thickness
    sol.offset = .2
    return obj, point


def border(name, point, inset, mat, col, parent, radius=.0014):
    a = inset
    pts = [point(a+(1-2*a)*i/60, a) for i in range(61)]
    pts += [point(1-a, a+(1-2*a)*i/60) for i in range(61)]
    pts += [point(1-a-(1-2*a)*i/60, 1-a) for i in range(61)]
    pts += [point(a, 1-a-(1-2*a)*i/60) for i in range(61)]
    return curves(name, [[(x,y-.001,z) for x,y,z in pts]], radius, mat, col, parent)


def stitch_border(name, point, mat, col, parent, count=55):
    paths = []
    for k in range(count):
        t = .03 + .94*k/(count-1)
        for u, v, du, dv in ((t,.018,.003,.002),(t,.982,.003,.002),(.018,t,.003,.002),(.982,t,.003,.002)):
            paths.append([(x,y-.002,z) for x,y,z in [point(u-du,v-dv),point(u+du,v+dv)]])
    return curves(name, paths, .00095, mat, col, parent)


def clone_group(src_col, src_root, dst_col, name, location, scale=1):
    src_objects = [src_root] + list(src_root.children_recursive)
    copies = {}
    for o in src_objects:
        new = o.copy()
        # Preserve shared mesh datablocks across instances; fonts remain editable per instance.
        if o.type == 'FONT':
            new.data = o.data.copy()
        new.name = name + '__' + o.name
        dst_col.objects.link(new)
        copies[o] = new
    for old, new in copies.items():
        new.parent = copies.get(old.parent)
    result = copies[src_root]
    result.location = location
    result.scale = (scale,)*3
    if 'asset_id' in result:
        del result['asset_id']
    return result


def bounds(objects):
    dg = bpy.context.evaluated_depsgraph_get()
    points = []
    triangles = 0
    for obj in objects:
        if obj.type in GEO_TYPES:
            ev = obj.evaluated_get(dg)
            me = ev.to_mesh()
            me.calc_loop_triangles()
            triangles += len(me.loop_triangles)
            points.extend(obj.matrix_world@v.co for v in me.vertices)
            ev.to_mesh_clear()
    lo = Vector([min(v[k] for v in points) for k in range(3)])
    hi = Vector([max(v[k] for v in points) for k in range(3)])
    return lo, hi, triangles


def setup_render(scene, size=(1440,1920), samples=32):
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    prefs = bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type = 'CUDA'
        prefs.get_devices()
        available = [d for d in prefs.devices if d.type == 'CUDA']
        for d in prefs.devices:
            d.use = d in available
        if available:
            scene.cycles.device = 'GPU'
    except TypeError:
        scene.cycles.device = 'CPU'
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'Medium High Contrast'
    scene.world = scene.world or bpy.data.worlds.new('WM warm studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.32,.29,.24,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .26
    scene.view_settings.exposure = -.40
    scene.render.use_freestyle = True
    fs = scene.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new('Ink contours')
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new('WM ink outlines')
    ls.select_crease = False
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_contour = True
    ls.select_external_contour = True
    ls.linestyle.color = (.022,.014,.008)
    ls.linestyle.thickness = .75
    # Pale glyphs on dark leather must not be swallowed by silhouette strokes.
    # This is an extra collection link, not copied or flattened text geometry.
    excluded = bpy.data.collections.new('TEXT_WITHOUT_FREESTYLE')
    scene.collection.children.link(excluded)
    for obj in list(scene.objects):
        if obj.type == 'FONT' and obj.active_material and obj.active_material.name.startswith('WM Warm text highlight'):
            excluded.objects.link(obj)
    ls.select_by_collection = True
    ls.collection = excluded
    ls.collection_negation = 'EXCLUSIVE'


def rig(scene, center, extent, size=(1100,1100), front=True):
    setup_render(scene, size)
    col = bpy.data.collections.new('PRESENTATION')
    scene.collection.children.link(col)
    cam = bpy.data.objects.new('WM_Camera', bpy.data.cameras.new('WM_Camera'))
    col.objects.link(cam)
    cam.location = Vector(center) + Vector((0,-extent*3,extent*.035) if front else (extent*.9,-extent*3,extent*.6))
    point_camera(cam, center)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = extent*1.15
    cam.data.clip_start = .001
    cam.data.clip_end = 100
    scene.camera = cam
    for label, offset, power in [('Key',(-.9,-1.5,1.4),68),('Fill',(.9,-.4,.5),27)]:
        data = bpy.data.lights.new('WM_'+label, 'AREA')
        data.energy = power*extent*extent
        data.shape = 'DISK'
        data.size = extent*1.15
        obj = bpy.data.objects.new(data.name,data)
        col.objects.link(obj)
        obj.location = Vector(center)+Vector(offset)*extent
        point_camera(obj,center)
    return cam


def export_selected(objects, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        if o.type in {'CURVE','FONT'}:
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
    if any(o.select_get() for o in objects):
        bpy.ops.object.convert(target='MESH')
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path), export_format='GLB', use_selection=True,
        export_apply=True, export_yup=True, export_extras=True, export_cameras=False, export_lights=False)

"""Build the approved nine map-desk groups in native Blender (MD-09 omitted).

Coordinates in the construction functions are centimetres; stored geometry is metres.
The script writes a new source, never loads or overwrites E1. All bitmap inputs are
unchanged image-model outputs. Fine curves remain editable in the Blender masters.
"""
from pathlib import Path
import math
import random
import json
import hashlib
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art/map-desk-v01'
TEX = ROOT / 'references/map-desk-assets-v01/map-environment-albedo-v01.png'
WOOD = ROOT / 'references/e1-r2-generated/wood-ink-albedo-v01.png'
OUT.mkdir(parents=True, exist_ok=True)
rng = random.Random(91326)
C = .01
TAU = math.tau
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = 'MapDesk_Assembly'
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.render.resolution_x = 1440
scene.render.resolution_y = 1440
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'Medium High Contrast'
scene.view_settings.exposure = 0
scene.world = bpy.data.worlds.new('Soft charcoal room')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.23,.25,.23,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .32

def mat(name, color, image=None, metal=0, rough=.85, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1)
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if image:
        t = m.node_tree.nodes.new('ShaderNodeTexImage')
        t.image = bpy.data.images.load(str(image), check_existing=True)
        t.extension = 'REPEAT'
        m.node_tree.links.new(t.outputs['Color'], p.inputs['Base Color'])
    if emission:
        p.inputs['Emission Color'].default_value = (*color,1)
        p.inputs['Emission Strength'].default_value = emission
    return m

ink = mat('Charcoal ink',(.012,.016,.013))
wood = mat('Hand-inked old timber',(.20,.18,.13), WOOD)
edge = mat('Worn timber edges',(.22,.18,.105))
paperedge = mat('Parchment edge',(.43,.40,.28))
paper = mat('Printed environment map',(.55,.53,.36),TEX)
red = mat('Dry vermilion route',(.48,.045,.022))
brass = mat('Aged brass',(.22,.165,.067), metal=.42)
gold = mat('Dull gold',(.46,.30,.055),metal=.52,rough=.66)
iron = mat('Blackened iron',(.045,.054,.047),metal=.32)
steel = mat('Rubbed iron rim',(.16,.18,.155),metal=.4)
bone = mat('Pale carved wood',(.49,.45,.32))
ivory = mat('Light engraving strokes',(.68,.66,.48))
slates = [mat('Slate %02d'%i,(.067+i*.011,.082+i*.011,.095+i*.013)) for i in range(4)]
stones = [mat('Grey stone %02d'%i,(.14+i*.026,.148+i*.026,.121+i*.025)) for i in range(4)]
coal = mat('Charred log',(.025,.031,.022))
ember = mat('Ember cuts',(.48,.09,.015),emission=.35)
flame = mat('Amber flame',(.85,.27,.022),emission=.7)
hot = mat('Cream flame core',(.98,.69,.16),emission=.8)
orbmat = mat('Cloudy green glass',(.055,.18,.14),metal=.16,rough=.22)
orbmat.node_tree.nodes['Principled BSDF'].inputs['Coat Weight'].default_value=.6
mistmat = mat('Pale interior mist',(.31,.58,.41),emission=.45)
leathers = [mat('Green leather',(.048,.084,.052)),mat('Burgundy leather',(.115,.045,.035)),mat('Charcoal leather',(.035,.042,.031))]

groups = {}
col = None
root = None

def begin(asset_id, name):
    global col, root
    col = bpy.data.collections.new(asset_id+'_'+name)
    scene.collection.children.link(col)
    root = bpy.data.objects.new(asset_id+'_ROOT', None)
    root.empty_display_size = .035
    col.objects.link(root)
    root['asset_id'] = asset_id
    root['design_status'] = 'First native Blender asset pass'
    root['front_axis'] = '-Y'
    groups[asset_id] = (col,root)
    return root

def finish(location=(0,0,0), rz=0):
    root.location = Vector(location)*C
    root.rotation_euler.z = math.radians(rz)

def attach(o, material, parent=None):
    for old in list(o.users_collection):
        old.objects.unlink(o)
    col.objects.link(o)
    o.parent = parent or root
    if hasattr(o.data,'materials'):
        o.data.materials.append(material)
    if o.type=='MESH':
        uv_project(o)
    return o

def uv_project(o):
    """Per-face proportional UV windows; no bitmap crops or resampling."""
    me=o.data
    me.update()
    if not me.vertices: return
    lo=Vector([min(v.co[k] for v in me.vertices) for k in range(3)])
    hi=Vector([max(v.co[k] for v in me.vertices) for k in range(3)])
    size=hi-lo
    uv=me.uv_layers.active or me.uv_layers.new(name='UVMap')
    offset=rng.uniform(.02,.58)
    for p in me.polygons:
        n=max(range(3),key=lambda k:abs(p.normal[k]))
        axes=sorted([k for k in range(3) if k!=n],key=lambda k:size[k],reverse=True)
        for li in p.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co
            u=(v[axes[0]]-lo[axes[0]])/max(size[axes[0]],.0001)
            vv=(v[axes[1]]-lo[axes[1]])/max(size[axes[1]],.0001)
            ratio=min(.32,max(.012,size[axes[1]]/max(size[axes[0]],.001)*.6))
            uv.data[li].uv=(.03+u*.9,offset+vv*ratio)

def mesh(name, verts, faces, material=wood, parent=None):
    d=bpy.data.meshes.new(name)
    d.from_pydata([tuple(Vector(v)*C) for v in verts],[],faces)
    d.update()
    o=bpy.data.objects.new(name,d)
    return attach(o,material,parent)

def box(name, loc, size, material=wood, bevel=.08, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=Vector(loc)*C)
    o=bpy.context.object
    o.name=name
    o.scale=Vector(size)*C
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    attach(o,material,parent)
    if bevel:
        b=o.modifiers.new('Worn corner','BEVEL');b.width=bevel*C;b.segments=1
    return o

def line(name, points, radius=.06, material=ink, closed=False,parent=None):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=1
    d.bevel_depth=radius*C;d.bevel_resolution=0
    s=d.splines.new('POLY');s.points.add(len(points)-1)
    for p,v in zip(s.points,points):p.co=(*tuple(Vector(v)*C),1)
    s.use_cyclic_u=closed
    o=bpy.data.objects.new(name,d)
    return attach(o,material,parent)

def sphere(name,loc,size,material,sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=Vector(loc)*C)
    o=bpy.context.object;o.name=name;o.scale=Vector(size)*C
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return attach(o,material)

def cylinder(name,loc,radius,depth,material=wood,n=16,radius2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=n,radius1=radius*C,radius2=(radius if radius2 is None else radius2)*C,depth=depth*C,location=Vector(loc)*C)
    o=bpy.context.object;o.name=name
    return attach(o,material)

def rod(name,a,b,r,material=wood,n=10):
    av,bv=Vector(a),Vector(b)
    o=cylinder(name,(av+bv)/2,r,(bv-av).length,material,n)
    o.rotation_euler=(bv-av).to_track_quat('Z','Y').to_euler()
    return o

def ring(name,center,radius,tube,material=ink,plane='XY',n=40,parent=None):
    c=Vector(center);points=[]
    for i in range(n):
        a=TAU*i/n
        off=Vector((radius*math.cos(a),radius*math.sin(a),0))
        if plane=='XZ':off=Vector((off.x,0,off.y))
        if plane=='YZ':off=Vector((0,off.x,off.y))
        points.append(c+off)
    return line(name,points,tube,material,True,parent)

def loft(name,rings,material=wood,n=12):
    verts=[]
    for x,y,z,rx,ry in rings:
        verts.extend([(x+rx*math.cos(TAU*i/n),y+ry*math.sin(TAU*i/n),z) for i in range(n)])
    faces=[tuple(reversed(range(n)))]
    for k in range(len(rings)-1):
        for i in range(n):faces.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i))
    faces.append(tuple((len(rings)-1)*n+i for i in range(n)))
    return mesh(name,verts,faces,material)

def plate(name,outline,depth,material=wood):
    # Outline lies in XZ; extrude along Y. Points are (x,y,z).
    verts=list(outline)+[(x,y+depth,z) for x,y,z in outline];n=len(outline)
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,verts,faces,material)

def stitch(name,points,r=.025,material=ink):return line(name,points,r,material)

def build_desk():
    begin('MD-01','Desk_and_clutter')
    # Eight thick, individually edged planks, a front drawer and narrow rear ledge.
    for j in range(8):
        y=-85+(j+.5)*170/8
        box('Desk_Plank_%02d'%j,(0,y,-3.5),(200,170/8-.24,7),wood,.28)
        for x in (-95,95):
            cylinder('Desk_Iron_pin',(x,y,0.08),.43,.18,iron,8)
    box('Desk_Apron',(0,-82,-13),(196,5,18),wood,.4)
    box('Desk_Drawer_face',(0,-85.05,-11),(70,1.5,12),wood,.32)
    for x in (-34,34):box('Drawer_iron_trim',(x,-85.9,-11),(1.5,.45,11.3),iron)
    ring('Drawer_pull',(0,-86.4,-11),2.9,.42,iron,'XZ')
    cylinder('Drawer_pull_mount',(0,-86.2,-8.3),1.1,.6,iron,12).rotation_euler.x=math.pi/2
    box('Rear_Ledge',(0,79,3.5),(200,12,7),wood,.3)
    box('Rear_Backboard',(0,84,14),(201,4,21),wood,.3)
    for z in (4,13,22):line('Rear_seam',[(-100,81.9,z),(100,81.9,z)],.13)
    # Quill cup; rim and dark hollow top; real feather silhouettes and spines.
    cylinder('Quill_Cup',(-89,66,9),5.8,18,wood,14,5.2)
    cylinder('Quill_Cup_Opening',(-89,66,18.05),4.5,.16,ink,24)
    for z in (1.3,16.7):ring('Quill_Cup_Iron',(-89,66,z),5.5,.46,iron)
    for q in range(3):
        x=-91+q*2.7;y=66;h=30+q*4
        rod('Quill_spine',(x,y,13),(x+5-q*3,y,h+9),.2,bone)
        pts=[(x,y-.1,18),(x-3,y-.2,24),(x-3+q,y-.1,h),(x+5-q*3,y,h+9),(x+5,y-.1,h-3),(x+2,y-.2,23)]
        plate('Quill_feather',pts,.12,bone)
        for t in range(8):
            z=23+t*1.7
            line('Quill_barbs',[(x+1,y-.25,z),(x-1.8,y-.25,z+1.6)],.04,ink)
    # Armillary globe: lathed base, gimbal rings, central marked globe.
    ax,ay=-65,75
    for z,r,d in ((1,8,2),(3,6.3,2),(4.4,5,1),(9,1.3,9),(14,4,.8)):
        cylinder('Armillary_stand',(ax,ay,z),r,d,brass,32)
    center=(ax,ay,24)
    sphere('Armillary_globe',center,(7,7,7),brass,3)
    ring('Armillary_equator',center,9,.28,brass)
    ring('Armillary_meridian',center,10,.28,brass,'XZ')
    ring('Armillary_outer',center,11,.42,brass,'YZ')
    for z in (-4,0,4):ring('Globe_latitude',(ax,ay,24+z),math.sqrt(49-z*z)+.06,.055,ink)
    for angle in (.3,1.2,2.1):
        pts=[(ax+7.07*math.sin(t)*math.cos(angle),ay+7.07*math.sin(t)*math.sin(angle),24+7.07*math.cos(t)) for t in [i*TAU/80 for i in range(81)]]
        line('Globe_longitude',pts,.07,ink)
    # Lantern at right edge, with pierced-looking cage and restrained flame.
    lx,ly=91,56
    for z,r,d in ((1,7,2),(3,6,2),(19,6,2),(22,4,4)):
        cylinder('Lantern_frame',(lx,ly,z),r,d,iron,8)
    for i in range(6):
        a=TAU*i/6
        rod('Lantern_rib',(lx+5*math.cos(a),ly+5*math.sin(a),4),(lx+5*math.cos(a),ly+5*math.sin(a),18),.38,iron)
    sphere('Lantern_amber',(lx,ly,10),(1.5,1.5,4.7),flame,2)
    ring('Lantern_handle',(lx,ly,27),4,.38,iron,'XZ')
    finish()

def paper_z(x,y):
    return .20 + .75*(abs(x)/83)**16 + .42*(abs(y)/71)**18*(.6+.4*math.sin(x*.11))

def build_map():
    begin('MD-02','Environment_map')
    nx,ny=64,56;verts=[]
    for j in range(ny+1):
        for i in range(nx+1):
            x=-83+166*i/nx;y=-71+142*j/ny
            if i in (0,nx):x+=.19*math.sin(y*1.13)
            if j in (0,ny):y+=.17*math.cos(x*.79)
            verts.append((x,y,paper_z(x,y)))
    faces=[]
    for j in range(ny):
        for i in range(nx):
            k=j*(nx+1)+i;faces.append((k,k+1,k+nx+2,k+nx+1))
    o=mesh('Map_Thin_Paper',verts,faces,paper)
    uv=o.data.uv_layers.active
    for p in o.data.polygons:
        for li in p.loop_indices:
            v=o.data.vertices[o.data.loops[li].vertex_index].co/C
            uv.data[li].uv=((v.x+83)/166,(v.y+71)/142)
    o.data.materials.append(paperedge)
    s=o.modifiers.new('Paper_1_5mm','SOLIDIFY');s.thickness=.0015;s.offset=-1;s.material_offset=1
    o['surface_role']='Printed environment: houses and paths are albedo, not raised geometry'
    # A restrained inked paper perimeter follows the actual curled mesh.
    per=[]
    for x in [-83+i*166/64 for i in range(65)]:per.append((x,-71,paper_z(x,-71)+.035))
    for y in [-71+i*142/56 for i in range(57)]:per.append((83,y,paper_z(83,y)+.035))
    for x in [83-i*166/64 for i in range(65)]:per.append((x,71,paper_z(x,71)+.035))
    for y in [71-i*142/56 for i in range(57)]:per.append((-83,y,paper_z(-83,y)+.035))
    line('Paper_ink_edge',per,.09,ink,True)
    finish()

ROUTES=[[(0,-44),(-12,-30),(-18,-12),(-35,3)],[(0,-44),(17,-33),(27,-12),(35,4)], [(-35,3),(-23,17),(-12,29),(0,41)],[(35,4),(28,19),(13,31),(0,41)]]

def build_routes():
    begin('MD-03','Red_route')
    def cubic(points,t):
        p=[Vector(v) for v in points];u=1-t
        return p[0]*u**3+3*p[1]*u*u*t+3*p[2]*u*t*t+p[3]*t**3
    for branch,control in enumerate(ROUTES):
        for k in range(11):
            vs=[]
            for q in range(5):
                t=min(.998,(k+.60*q/4)/11)
                p=cubic(control,t);tangent=cubic(control,min(.9999,t+.001))-p
                tangent.normalize();normal=Vector((-tangent.y,tangent.x))
                width=.53*(.86+.14*math.sin(q*2.3+k))
                for side in (-1,1):
                    v=p+normal*width*side
                    vs.append((v.x,v.y,paper_z(v.x,v.y)+.10))
            mesh('Route_%d_dash_%02d'%(branch,k),vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(4)],red)
    for i in range(60):
        a=TAU*i/60;b=TAU*(i+.85)/60
        verts=[]
        for t in (a,b):
            for r in (6.3,7.25):
                x=r*math.cos(t);y=-44+r*math.sin(t)
                verts.append((x,y,paper_z(x,y)+.11))
        mesh('Current_ring_stroke',verts,[(0,2,3,1)],red)
    root['route_semantics']='Illustrative art only; no gameplay topology'
    finish()

def build_mage():
    begin('MD-04','Mage_woodcarving')
    cylinder('Mage_Base',(0,0,.65),4.5,1.3,wood,12)
    ring('Mage_Base_cut',(0,0,1.31),4.15,.075,edge,n=12)
    loft('Mage_Robe',[(0,0,1.3,3.4,2.8),(0,.1,4,3.1,2.5),(0,.25,9,2.8,2.3),(0,.25,12.1,1.8,1.65)],wood,12)
    # Mantle panels carry the jagged carved silhouette.
    for side in (-1,1):
        plate('Mage_Mantle',[(side*.6,-1.9,11.7),(side*2.3,-1.8,11),(side*4,-1.2,6.8),(side*2,-2.4,8.1),(side*.8,-2.5,9.7)],1.2,wood)
    sphere('Mage_Shadow_face',(0,-1.05,11.1),(1.65,1.3,1.65),ink)
    sphere('Mage_Nose',(0,-2.37,10.9),(.47,.47,.68),bone)
    for x in (-.72,.72):
        plate('Mage_Sleepy_eye',[(x-.27,-2.17,11.4),(x+.27,-2.17,11.4),(x+.13,-2.2,11.17),(x-.15,-2.2,11.2)],.05,ivory)
    # Tapered carved beard blades with lengthwise ink cuts.
    for i in range(9):
        x=-1.65+i*.41;endz=5.3+abs(x)*1.9+rng.uniform(-.2,.2)
        outline=[(x-.45,-2.5,10.7),(x+.4,-2.48,10.8),(x+.2,-2.9,8.8),(x*.48,-2.4,endz)]
        plate('Mage_Beard_lock_%02d'%i,outline,.40,bone)
        line('Beard_engraved_fibre',[(x,-2.94,10.2),(x+.04,-3.00,8.8),(x*.5,-2.49,endz+.3)],.035,ink)
    hatrings=[(0,.15,12.1,4.05,3.35),(0,.1,12.65,2.7,2.25),(.05,.12,14.3,2.12,1.78),(.55,.15,16.2,1.32,1.13),(1.05,.12,17.5,.72,.63),(2.25,.13,17.2,.10,.13)]
    hat=loft('Mage_Bent_Hat',hatrings,wood,10)
    for j,(x,y,z,rx,ry) in enumerate(hatrings[:-1]):
        pts=[(x+rx*math.cos(TAU*i/10),y+ry*math.sin(TAU*i/10),z+.025) for i in range(10)]
        line('Mage_Hat_Cut_%d'%j,pts,.045,ink,True)
    # Long, face-following robe cuts (not uniformly stamped knots).
    for i in range(15):
        a=TAU*i/15;pts=[]
        for j in range(8):
            z=1.5+j*1.12;rr=3.45-.067*(z-1.5)
            pts.append((rr*math.cos(a+.025*math.sin(j)),.15+rr*.81*math.sin(a+.025*math.sin(j)),z))
        line('Mage_Robe_knife_cut',pts,.03,ink)
    rod('Mage_Detachable_staff',(4.1,-.1,1.1),(4.7,-.15,12.5),.37,wood)
    ring('Mage_Staff_eye',(4.8,-.15,13.75),1.15,.32,wood,'XZ',24)
    ring('Mage_Staff_eye_cut',(4.8,-.5,13.75),1.14,.035,ink,'XZ',24)
    for z in (11.6,12.05):ring('Mage_Staff_band',(4.68,-.15,z),.48,.12,brass)
    box('Mage_Gripping_hand',(4.3,-.25,7.6),(1.15,1.2,1.75),wood,.20)
    for z in (7.1,7.6,8.1):line('Mage_fingers',[(3.8,-.88,z),(4.85,-.88,z)],.055,ink)
    finish((0,-44,paper_z(0,-44)+.02),-5)

def build_campfire():
    begin('MD-05','Campfire')
    cylinder('Camp_Ash',(0,0,.18),7.6,.36,coal,32)
    for i in range(9):
        a=TAU*i/9;r=7.15
        o=sphere('Camp_Stone_%02d'%i,(r*math.cos(a),r*math.sin(a),1.75),(2.05,1.65,1.70),stones[i%4],1)
        o.rotation_euler.z=a
        for j in range(3):
            x=r*math.cos(a)+(j-1)*.5;y=r*math.sin(a)
            line('Stone_cut',[(x,y-.9,2.9),(x+.35,y-.2,3.5),(x+.6,y+.5,3.05)],.045,ink)
    for i in range(5):
        a=TAU*i/5
        v=Vector((math.cos(a),math.sin(a),0));p=v*5.5+Vector((0,0,1.8));q=-v*4.3+Vector((0,0,3))
        rod('Camp_Charred_log',p,q,.93,wood,9)
        for k in (-.35,.35):line('Camp_ember_cut',[p+Vector((0,k,.6)),q+Vector((0,k,.6))],.08,ember)
    shape=[(-3.0,0,3),(-3.8,0,6),(-1.8,0,8),(-2.2,0,11),(-.3,0,9.8),(.6,0,15.7),(2.6,0,12),(2.1,0,9),(3.9,0,11),(3.2,0,6),(2.3,0,3)]
    for i,angle in enumerate((0,65,125)):
        o=plate('Camp_Flame_%d'%i,shape,.07,flame);o.rotation_euler.z=math.radians(angle)
        c=plate('Camp_Flame_core',[(x*.55,y-.09,3+(z-3)*.68) for x,y,z in shape],.05,hot);c.rotation_euler.z=o.rotation_euler.z
        e=line('Camp_Flame_ink',[(x,y-.06,z) for x,y,z in shape],.055,ink,True);e.rotation_euler.z=o.rotation_euler.z
    finish((-35,3,paper_z(-35,3)+.02),-8)

def build_orb():
    begin('MD-06','Crystal_ball')
    loft('Orb_Brass_Bowl',[(0,0,3,3.9,3.9),(0,0,4,5,5),(0,0,5,6.1,6.1),(0,0,6,6.3,6.3)],brass,40)
    for z,r in ((4.5,5.6),(5.8,6.35),(6.2,6.3)):ring('Orb_engraved_rim',(0,0,z),r,.15,ink if z==5.8 else brass)
    for i in range(3):
        a=TAU*i/3-math.pi/2
        pts=[(r*math.cos(a),r*math.sin(a),z) for r,z in ((4.6,4.3),(5.7,3.4),(5.5,2.1),(6,.9),(6.9,.45))]
        line('Orb_Curled_foot',pts,.49,brass)
        sphere('Orb_Foot_pad',pts[-1],(.75,.75,.40),brass,1)
    o=sphere('Orb_Cloud_Glass',(0,0,12.5),(6.5,6.5,6.5),orbmat,4)
    for p in o.data.polygons:p.use_smooth=True
    # A stylized opaque cloudy core, with shallow raised mist and reflected arcs.
    question=[(-1.9,-6.02,14.6),(-1.5,-6.24,15.6),(-.1,-6.30,15.95),(1.45,-6.23,15.4),(1.9,-6.19,14.3),(1.4,-6.32,13.4),(.1,-6.51,12.5),(.1,-6.44,11.45)]
    line('Orb_Mist_question',question,.30,mistmat)
    sphere('Orb_Mist_dot',(.1,-6.10,10.10),(.38,.18,.38),mistmat,2)
    for angle0,angle1,r in ((.4,1.2,6.58),(1.5,2.0,6.60)):
        pts=[]
        for i in range(16):
            a=angle0+(angle1-angle0)*i/15
            pts.append((r*.82*math.cos(a),-3.75,12.5+r*.82*math.sin(a)))
        line('Orb_Painted_reflection',pts,.15,ivory)
    for i in range(35):
        a=rng.uniform(0,TAU);z=rng.uniform(-4.7,4.7);rr=math.sqrt(6.51**2-z*z)
        if math.sin(a) < -.25:
            sphere('Orb_Cloud_fleck',(rr*math.cos(a),rr*math.sin(a),12.5+z),(.09,.065,.09),mistmat,1)
    root['material_note']='Stylized opaque cloudy glass; mist geometry near front shell, no physical volumetric shader yet'
    finish((35,4,paper_z(35,4)+.02),-7)

def arch_outline(cx,y,zbase,width,height):
    r=width/2;spring=zbase+height-r
    pts=[(cx-r,y,zbase),(cx+r,y,zbase),(cx+r,y,spring)]
    pts += [(cx+r*math.cos(t),y,spring+r*math.sin(t)) for t in [math.pi*i/16 for i in range(1,17)]]
    return pts

def build_building():
    begin('MD-07','Place_building')
    box('Building_Plank_base',(0,0,.65),(14,12,1.3),wood,.2)
    box('Building_Wall_body',(0,0,7),(10,8.6,11.4),wood,.18)
    for x in (-5.05,5.05):box('Building_Corner_post',(x,-4.22,7),(.8,.8,11.4),edge,.07)
    # Arched black door, carved surround and wood door planks.
    door=arch_outline(0,-4.37,1.35,3.7,6.5)
    plate('Building_Door_shadow',door,.04,ink)
    line('Building_Door_arch',arch_outline(0,-4.48,1.35,4.35,7),.25,edge)
    for x in (-1.1,-.36,.38,1.12):box('Building_Door_plank',(x,-4.46,3.7),(.67,.16,4.55),wood,.02)
    ring('Building_Door_pull',(.65,-4.63,3.7),.26,.065,iron,'XZ',16)
    for x in (-2.7,2.7):
        w=arch_outline(x,-4.43,9.2,1.45,2.5)
        plate('Building_Upper_window',w,.03,ink)
        line('Building_Window_carving',w,.12,bone,True)
        rod('Building_Window_mullion',(x,-4.60,9.25),(x,-4.60,11.0),.085,wood)
    # Small side window projected onto the right wall.
    side=plate('Building_Side_window',arch_outline(0,-5.09,7.1,1.8,2.8),.05,ink)
    side.rotation_euler.z=math.pi/2
    # Hipped roof with individually seated slate shingles on all four slopes.
    low=[(-6,-5.4,12.8),(6,-5.4,12.8),(6,5.4,12.8),(-6,5.4,12.8)]
    top=[(-1.8,-.9,21),(1.8,-.9,21),(1.8,.9,21),(-1.8,.9,21)]
    mesh('Building_Hip_roof',low+top,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],slates[0])
    for side_idx in range(4):
        a,b=Vector(low[side_idx]),Vector(low[(side_idx+1)%4]);ta,tb=Vector(top[side_idx]),Vector(top[(side_idx+1)%4])
        for row in range(7):
            v0=row/7;v1=min(1,(row+1.13)/7)
            n=7 if side_idx%2==0 else 5
            for k in range(n):
                u0=(k+.03)/n;u1=(k+.94)/n
                corners=[]
                for u,v in ((u0,v0),(u1,v0),(u1,v1),(u0,v1)):
                    corners.append((a.lerp(b,u).lerp(ta.lerp(tb,u),v)+Vector((0,0,.16))).to_tuple())
                tile=mesh('Building_Slate_tile',corners,[(0,1,2,3)],slates[(row+k)%4])
                so=tile.modifiers.new('Slate thickness','SOLIDIFY');so.thickness=.0006
                line('Building_Slate_lower_ink',corners[:2],.035,ink)
    for a,b in zip(low,top):line('Building_Hip_seam',[a,b],.085,ink)
    box('Building_Chimney',(1.3,2.5,20),(1.9,1.7,5.3),wood,.15)
    box('Building_Chimney_cap',(1.3,2.5,22.8),(2.4,2.2,.7),slates[2])
    for i in range(18):
        x=-4.6+i*.54
        line('Building_Wall_engraving',[(x,-4.33,1.5),(x+.06,-4.34,6.2),(x-.05,-4.34,12.4)],.025,ink)
    finish((0,41,paper_z(0,41)+.02),-4)

def build_chest():
    begin('MD-08','Coin_chest')
    # Open box walls: a visible cavity, not a solid cube filled with coins.
    box('Chest_Floor',(0,0,1.1),(46,31,2.2),wood,.18)
    for j in range(4):
        z=3+j*4.3
        for y in (-14.55,14.55):box('Chest_Horizontal_plank',(0,y,z),(46,1.9,4.14),wood,.13)
        for x in (-22,22):box('Chest_End_plank',(x,0,z),(2,27.2,4.14),wood,.13)
    for y in (-14.7,14.7):
        for x in (-21,-7,7,21):
            box('Chest_Box_iron_strap',(x,y*1.011,9.3),(1.75,.65,17.5),iron,.12)
            for z in (1.7,5.7,12.9,17):sphere('Chest_Rivet',(x,y*1.04,z),(.34,.18,.34),steel,1)
    box('Chest_Front_lock',(0,-15.9,11.7),(5,.55,5.7),iron,.26)
    sphere('Chest_Keyhole_round',(0,-16.25,12.2),(.55,.08,.55),ink,2)
    plate('Chest_Keyhole_stem',[(-.2,-16.34,12),(.2,-16.34,12),(.43,-16.34,10.4),(-.43,-16.34,10.4)],.04,ink)
    # Closed lid defined at the actual rear hinge; UI will refine its opening.
    pivot=bpy.data.objects.new('MD08_LID_HINGE',None);col.objects.link(pivot);pivot.parent=root
    pivot.location=(0,15.5*C,18*C);pivot.empty_display_size=.035
    pivot['editable_axis']='Local X; negative opens lid'
    lid_objects=[]
    start=set(col.objects)
    for j in range(12):
        a=math.pi*j/12;b=math.pi*(j+1)/12
        verts=[]
        for x in (-23,23):
            for r,t in ((15.5,a),(15.5,b),(14.5,b),(14.5,a)):
                verts.append((x,r*math.cos(t),18+r*.77*math.sin(t)))
        mesh('Chest_Lid_curved_stave',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(1,5,6,2),(0,3,7,4)],wood)
    # Solid arched ends and iron perimeter strips.
    for x in (-23,23):
        verts=[(x,15.5*math.cos(math.pi*i/20),18+11.935*math.sin(math.pi*i/20)) for i in range(21)]
        mesh('Chest_Lid_end',verts,[tuple(range(21))],wood)
    for x in (-21,-7,7,21):
        for j in range(24):
            a=math.pi*j/24;b=math.pi*(j+1)/24
            verts=[(xx,15.8*math.cos(t),18+12.18*math.sin(t)) for xx,t in ((x-.85,a),(x+.85,a),(x+.85,b),(x-.85,b))]
            mesh('Chest_Lid_iron_band',verts,[(0,1,2,3)],iron)
        for j in range(7):
            a=math.pi*(j+.2)/7
            sphere('Chest_Lid_Rivet',(x,16*math.cos(a),18+12.35*math.sin(a)),(.34,.34,.34),steel,1)
    box('Chest_Lid_latch',(0,-15.9,18.3),(4.6,.5,3.2),iron,.15)
    for o in set(col.objects)-start:
        o.parent=pivot;o.location-=pivot.location
    pivot.rotation_euler.x=math.radians(-48)
    for x in (-14,14):
        rod('Chest_Hinge_barrel',(x-2,15.5,18),(x+2,15.5,18),.8,iron,16)
    for x in (-23.4,23.4):
        ring('Chest_Side_handle',(x,0,10),2.5,.4,iron,'YZ',24)
    # Shallow pile with distinct top coins; hidden interior is left simple.
    sphere('Chest_Gold_underfill',(0,0,13.2),(20,12,3.3),gold,2)
    for i in range(65):
        x=rng.uniform(-19.3,19.3);y=rng.uniform(-11.5,11.5);z=15.5+.9*(1-abs(x)/21)+rng.uniform(-.3,.4)
        o=cylinder('Chest_Coin_%02d'%i,(x,y,z),rng.uniform(.86,1.20),.19,gold,20)
        o.rotation_euler=(rng.uniform(-.16,.16),rng.uniform(-.16,.16),rng.uniform(0,TAU))
        ring('Chest_Coin_emboss',(x,y,z+.13),.70,.035,brass,n=20)
    for i,(x,y) in enumerate(((-26,-10),(-27,-17),(-20,-20))):
        cylinder('Chest_Loose_coin',(x,y,.18),1.45,.26,gold,24)
        ring('Chest_Loose_coin_etch',(x,y,.32),1.13,.052,brass,n=24)
    finish((74,-66,.02),-6)

def book_geometry(index,size,z,angle):
    length,width,thick=size
    parent=bpy.data.objects.new('Book_%d_ROOT'%index,None);col.objects.link(parent);parent.parent=root
    before=set(col.objects)
    box('Book_Page_block',(0,0,z+thick/2),(length-1.1,width-1.1,thick-1),bone,.15)
    for zz in (z+.3,z+thick-.3):
        box('Book_Leather_cover',(0,0,zz),(length+.45,width+.45,.62),leathers[index],.22)
        # Gold double rules sit on the actual cover.
        for inset in (1,1.35):
            pts=[(-length/2+inset,-width/2+inset,zz+.33),(length/2-inset,-width/2+inset,zz+.33),(length/2-inset,width/2-inset,zz+.33),(-length/2+inset,width/2-inset,zz+.33)]
            line('Book_Cover_rule',pts,.065,brass,True)
    box('Book_Rounded_spine',(0,width/2,z+thick/2),(length,1.3,thick-.6),leathers[index],.5)
    for x in (-length*.37,-length*.18,length*.18,length*.37):
        box('Book_Spine_rib',(x,width/2+.47,z+thick/2),(.45,.65,thick-.6),edge,.15)
    for k in range(18):
        zz=z+.78+k*(thick-1.5)/18
        pts=[(-length/2+.55,-width/2+.50,zz),(length*.01,-width/2+.43,zz+.05),(length/2-.55,-width/2+.50,zz)]
        line('Book_Page_edges',pts,.027,ink)
        line('Book_Page_side',[(length/2-.51,-width/2+.5,zz),(length/2-.50,width/2-.7,zz+.07)],.027,ink)
    for r in (4.6,5.05):ring('Book_Gilt_seal',(0,0,z+thick+.065),r,.10,brass,n=48)
    star=[(3.6*math.cos(math.pi/2+TAU*i*2/5),3.6*math.sin(math.pi/2+TAU*i*2/5),z+thick+.065) for i in range(5)]
    line('Book_Gilt_star',star,.12,brass,True)
    for x in (-length/2+1,length/2-1):
        for y in (-width/2+1,width/2-1):
            line('Book_Worn_corner',[(x,y+1.4,z+thick+.06),(x,y,z+thick+.06),(x+1.4*(1 if x<0 else -1),y,z+thick+.06)],.15,edge)
    for o in set(col.objects)-before:o.parent=parent
    parent.rotation_euler.z=math.radians(angle)
    return parent

def build_books():
    begin('MD-10','Old_books')
    book_geometry(2,(34,25,8),0,-7)
    book_geometry(1,(33,23,7.5),8,4)
    book_geometry(0,(30,22,7.5),15.5,-2)
    finish((-75,-63,.02),15)

for fn in (build_desk,build_map,build_routes,build_mage,build_campfire,build_orb,build_building,build_chest,build_books):
    fn();print('BUILT',fn.__name__,flush=True)

# Presentation rig is a separate collection, never part of component exports.
rig=bpy.data.collections.new('PRESENTATION');scene.collection.children.link(rig)
def rig_object(o):
    for c in list(o.users_collection):c.objects.unlink(o)
    rig.objects.link(o)

def area(name,loc,power,size,color,target=(0,0,0)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
    d.color=color;o=bpy.data.objects.new(name,d);rig.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o

area('Large_softbox',(-1.5,-1.2,3.5),170,3.4,(1,.91,.76))
area('Cool_fill',(1.6,.8,2),75,3,(.74,.83,1))
bpy.ops.object.camera_add(location=(0,-2.42,2.72))
camera=bpy.context.object;camera.name='CAM_Desk_Overall';rig_object(camera)
camera.rotation_euler=(Vector((0,.02,0))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='PERSP';camera.data.lens=46;camera.data.clip_start=.01;scene.camera=camera
scene.render.film_transparent=False
scene.world.color=(.03,.035,.027)

# Include a small in-file note for a person opening the asset.
text=bpy.data.texts.new('READ_ME_MapDesk')
text.write('Map desk assets v01. Nine groups MD-01..08 and MD-10. MD-09 CAT intentionally omitted.\nUnits metres, +Z up, -Y front. Editable components, curves and packed textures.\nMD08_LID_HINGE is the real rear hinge; local X negative opens the lid.\nBitmap maps/wood are unchanged image-model outputs. This is a first native 3D asset pass, not a verified engine material pack.\n')
for im in bpy.data.images:
    if im.source=='FILE':im.pack()

bpy.ops.object.select_all(action='DESELECT')
pivot=bpy.data.objects['MD08_LID_HINGE'];pivot.select_set(True);bpy.context.view_layer.objects.active=pivot
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':
            ar.spaces.active.region_3d.view_perspective='CAMERA'
            ar.spaces.active.overlay.show_overlays=False
            ar.spaces.active.shading.type='MATERIAL'
            ar.spaces.active.shading.use_scene_lights=True
            ar.spaces.active.shading.use_scene_world=True

scene['user_scope']='Generate Blender assets; omit cat'
scene['source_sheets']='concepts/blender-sheets-v01/manifest.json'
scene['geometry_units']='metres'
scene['ui_review']='Pending native Blender UI refinement'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'map-desk-source.blend'),compress=True)
scene.render.filepath=str(OUT/'assembly-first-pass.png')
bpy.ops.render.render(write_still=True)
print('COMPLETE',str(OUT/'map-desk-source.blend'),flush=True)

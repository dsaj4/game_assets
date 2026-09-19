"""Build physical panel silhouettes from generated skins; retain all text and game state.

Run with Blender --background --python-exit-code 1 --python this-file.
Generated image bytes are never edited: magenta is outside the UV-mapped mesh.
"""
from pathlib import Path
import sys, json, math
import bpy
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wm_tools import *

OUT = ROOT / 'art/wand-management-v03'
SRC = ROOT / 'art/wand-management-v02'
TEX = ROOT / 'references/wm-panel-v03'
if (OUT/'wand-management-master.blend').exists() and '--replace-v03' not in sys.argv:
    raise RuntimeError('v03 exists; use --replace-v03 only for intentional rebuild from preserved v02')
for folder in ('assets', 'renders'):
    (OUT/folder).mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SRC/'wand-management-master.blend'))
bpy.context.preferences.filepaths.save_version = 0
scene = bpy.context.scene
brass = bpy.data.materials['WM Muted brass']
iron = bpy.data.materials['WM Blackened iron']
fine = bpy.data.materials['WM Fine brown leather v02']
ink = bpy.data.materials['WM Hand ink']
edge = bpy.data.materials['WM Rubbed leather edge']
audit = []

def remove_named(names):
    for name in names:
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

def skin(name, filename):
    mat = material(name, (.5,.35,.2), TEX/filename, rough=.94)
    tex = next(n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE')
    tex.extension = 'EXTEND'
    mat.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = .10
    return mat, tex.image

def silhouette(name, image, center, size, mat, col, parent, thickness, kind):
    """Sample a star-shaped silhouette into a native UV mesh, not an image cutout."""
    w,h = image.size
    rgb = np.array(image.pixels[:], dtype=np.float32).reshape(h,w,4)[:,:,:3]
    bg = (rgb[:,:,0]>.45)&(rgb[:,:,2]>.4)&(rgb[:,:,1]<.28)&(np.minimum(rgb[:,:,0],rgb[:,:,2])>rgb[:,:,1]*1.8)
    assert bg[0,0] and bg[-1,-1], 'Expected solid magenta exterior'
    n, rings = (512, 12) if kind=='paper' else (256, 10)
    c = np.array([(w-1)/2,(h-1)/2])
    contour=[]
    for k in range(n):
        a=math.tau*k/n
        direction=np.array([math.cos(a)*w/2, math.sin(a)*h/2])
        radii=np.linspace(0,1.5,max(w,h)*2)
        points=c+radii[:,None]*direction
        ids=np.rint(points).astype(int)
        outside=(ids[:,0]<0)|(ids[:,0]>=w)|(ids[:,1]<0)|(ids[:,1]>=h)
        ids[:,0]=np.clip(ids[:,0],0,w-1);ids[:,1]=np.clip(ids[:,1],0,h-1)
        stop=np.flatnonzero(outside|bg[ids[:,1],ids[:,0]])[0]
        # Keep filtering footprint and tiny edge concavities away from key color.
        radius=max(0,float(radii[stop])-6/np.linalg.norm(direction))
        contour.append(c+radius*direction)
    contour=np.array(contour)
    lo=contour.min(axis=0);hi=contour.max(axis=0)
    vertices=[];uvs=[]
    x,y,z=center
    def vertex(p, t):
        q=(p-lo)/(hi-lo)
        if kind=='paper':
            relief=.009*t**9*(.5+.5*math.sin(q[0]*16+q[1]*21))
        else:
            rim=max(abs(q[0]-.5)*2,abs(q[1]-.5)*2)
            relief=.008*math.exp(-((rim-.90)/.10)**2)
        vertices.append((x+(q[0]-.5)*size[0],y-relief,z+(q[1]-.5)*size[1]))
        uvs.append((float(p[0]/(w-1)),float(p[1]/(h-1))))
    vertex(c,0)
    for r in range(1,rings+1):
        t=r/rings
        for p in contour:vertex(c+(p-c)*t,t)
    faces=[(0,1+k,1+(k+1)%n) for k in range(n)]
    for r in range(rings-1):
        base=1+r*n;nxt=base+n
        faces.extend((base+k,nxt+k,nxt+(k+1)%n,base+(k+1)%n) for k in range(n))
    obj=mesh(name,vertices,faces,mat,col,parent,uvs,True)
    obj.data.materials.append(fine if kind=='button' else edge)
    solid=obj.modifiers.new('Physical cut edge and backing', 'SOLIDIFY')
    solid.thickness=thickness;solid.offset=-1;solid.material_offset=1;solid.material_offset_rim=1
    obj['generated_skin']=str(Path(image.filepath).name)
    obj['construction']='Opaque silhouette mesh; no alpha cards or edited image bytes'
    obj['skin_kind']=kind
    # Check every vertex and every polygon centroid against the key color.
    probes=list(uvs)
    probes.extend(tuple(np.mean([uvs[i] for i in face],axis=0)) for face in faces)
    pp=np.rint(np.array(probes)*np.array([w-1,h-1])).astype(int)
    leaks=int(bg[pp[:,1],pp[:,0]].sum())
    assert leaks==0, (name,'key-color leakage',leaks)
    audit.append({'object':name,'image':Path(image.filepath).name,'vertices':len(vertices),
                  'faces':len(faces),'key_color_probe_count':len(probes),'key_color_leaks':leaks,
                  'physical_thickness_m':thickness,'uv_bounds':[list(lo/[w-1,h-1]),list(hi/[w-1,h-1])]})
    return obj

paper, paper_im=skin('WM Sculpted parchment skin v03','panel-production.png')
back, back_im=skin('WM Armored charcoal control v03','return-production.png')
save, save_im=skin('WM Armored burgundy control v03','save-production.png')
col=bpy.data.collections['WM-06_configuration-parchment']
parent=bpy.data.objects['WM-06_configuration-parchment_ROOT']
remove_named(['WM06_Parchment_body','WM06_Torn_dark_edge'])
panel=silhouette('WM06_Parchment_body',paper_im,(0,0,.55),(2.45,1.10),paper,col,parent,.004,'paper')
# Real offset leaves and a leather back can be inspected from an oblique camera.
for i in range(2):
    cp=panel.copy();cp.data=panel.data.copy();col.objects.link(cp)
    cp.name='WM06_Stacked_leaf_'+str(i+1)
    cp.location=(.004*(-1 if i==0 else 1),.006*(i+1),-.006*(i+1))
    cp.scale=(1.003,1,1.003)
    cp['part_role']='separate paper leaf'
    cp.data.materials.clear();cp.data.materials.append(edge)
    for modifier in cp.modifiers:
        if modifier.type=='SOLIDIFY':modifier.material_offset=0;modifier.material_offset_rim=0
for x in (-1.15,1.15):
    for z in (.055,1.045):
        ring('WM06_Aged_pin_washer',(x,-.010,z),.021,.005,iron,col,parent)
        ring('WM06_Brass_washer_rim',(x,-.014,z),.024,.002,brass,col,parent)

controls=bpy.data.collections['WM-07_tags-and-controls']
controls_root=bpy.data.objects['WM-07_tags-and-controls_ROOT']
for prefix,im,mat,x in [('WM07_Back',back_im,back,-.64),('WM07_Save',save_im,save,.10)]:
    remove_named([prefix+'_body',prefix+'_leather_backing'])
    silhouette(prefix+'_body',im,(x,-.075,.236),(.65,.195),mat,controls,controls_root,.023,'button')
    bpy.data.objects[prefix+'_text'].location.y=-.100
    # Geometry pin caps sit on top of the four painted mounting locations.
    for dx in (-.301,.301):
        for dz in (-.063,.063):
            pin(prefix+'_raised_rivet',(x+dx,-.085,.236+dz),.010,brass,controls,controls_root)
            ring(prefix+'_rivet_seat',(x+dx,-.083,.236+dz),.014,.002,iron,controls,controls_root)

# Transfer button becomes a thick pale inset plaque, consistent with the approved sheet.
remove_named([o.name for o in list(col.objects) if o.name.startswith('WM06_To_reserve') and o.type!='FONT'])
button=box('WM06_To_reserve_body',(.80,-.027,.845),(.62,.022,.155),fine,col,parent,.008)
inset=box('WM06_To_reserve_inset',(.80,-.041,.845),(.596,.008,.132),paper,col,parent,.004)
for loop in inset.data.uv_layers.active.data:
    loop.uv=(.20+loop.uv.x*.60,.30+loop.uv.y*.40)
curves('WM06_To_reserve_brass_frame', [[(.80+dx,-.048,.845+dz) for dx,dz in [(-.298,-.066),(.298,-.066),(.298,.066),(-.298,.066),(-.298,-.066)]]],.0025,brass,col,parent)
for dx in (-.28,.28):
    for dz in (-.051,.051):pin('WM06_To_reserve_rivet',(.80+dx,-.048,.845+dz),.005,brass,col,parent)
txt=bpy.data.objects['WM06_To_reserve_text'];txt.data.materials.clear();txt.data.materials.append(ink);txt.location.y=-.057

# Smaller controls get a physical socket and brass face surround, rather than ragged scraps.
for label,x in [('-',.70),('+',1.0)]:
    prefix='WM06_Start_'+label
    remove_named([o.name for o in list(col.objects) if o.name.startswith(prefix) and o.type!='FONT'])
    box(prefix+'_socket',(x,-.020,.44),(.126,.018,.106),iron,col,parent,.007)
    box(prefix+'_body',(x,-.032,.44),(.113,.012,.094),brass,col,parent,.006)
    face=box(prefix+'_leather_face',(x,-.040,.44),(.098,.008,.078),fine,col,parent,.004)
    bpy.data.objects[prefix+'_text'].location.y=-.049

# Refine the two replaceable sockets; retain their original property-bearing rings.
for x in (-.55,-.27):
    ring('WM06_Socket_dark_recess',(x,-.038,.315),.053,.006,iron,col,parent)
    ring('WM06_Socket_inner_bevel',(x,-.045,.315),.047,.0018,brass,col,parent)

scene['texture_revision']='v03 / generated physical panel skins + native silhouette/relief / 2026-09-19'
scene.render.resolution_percentage=100
scene.render.filepath=str(OUT/'renders/assembly.png')
pack_images();bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'wand-management-master.blend'),compress=True)
(OUT/'source-catalog.json').write_bytes((SRC/'source-catalog.json').read_bytes())
revision=json.loads((SRC/'revision.json').read_text(encoding='utf-8'))
revision.update({'date':'2026-09-19','status':'PhysicalPanelRefined / NeedsArtReview',
 'user_scope':'Review v01/v02 quality first; generate real panel form and optimize only left wand management page',
 'method':'Built-in image_gen for blank object skins; Blender bundled Python for opaque silhouette meshes, relief, thickness and independent text',
 'skin_limitations':'Illustrative skins include painted microrelief; no pure PBR extraction. Original magenta backgrounds are outside actual geometry; no alpha blending needed.'})
revision['additional_textures'] += [{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'role':'Built-in image_gen original bytes; magenta outside silhouette UV geometry'} for p in sorted(TEX.glob('*-production.png'))]
revision['additional_preserved_files'] += [{'path':str((SRC/'wand-management-master.blend').relative_to(ROOT)).replace('\\','/'),'sha256':sha(SRC/'wand-management-master.blend')}]
(OUT/'revision.json').write_text(json.dumps(revision,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'silhouette-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
scene.render.resolution_percentage=65
scene.cycles.samples=24
scene.render.filepath=str(OUT/'renders/preview.png')
bpy.ops.render.render(write_still=True)

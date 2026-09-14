"""Build the approved left management page in native Blender, without changing old assets."""
from pathlib import Path
import sys
import json
import math
import random
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wm_tools import *

if (OUT/'wand-management-master.blend').exists() and '--rebuild' not in sys.argv:
    raise RuntimeError('Native master exists. Preserve manual edits; use -- --rebuild only for an intentional full rebuild.')

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = 'WM_Management_Assembly'
scene.unit_settings.system = 'METRIC'
scene['user_scope'] = '开始建模; left management page; deployed bag / reserve rack; spell read-only'
scene['implementation'] = 'Native Blender Python; no computer-use tool available in this session'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'renders').mkdir(exist_ok=True)
(OUT/'assets').mkdir(exist_ok=True)
rng = random.Random(91426)
leather = material('WM Russet whole hide',(.22,.08,.035),ROOT/'references/md-11-native/leather-albedo-v01.png')
wood = material('WM Inked old timber',(.25,.19,.10),ROOT/'references/e1-r2-generated/wood-ink-albedo-v01.png')
paper = material('WM Warm parchment',(.65,.58,.38),ROOT/'art/e1/paper_base.png')
ink = material('WM Hand ink',(.020,.012,.008))
edge = material('WM Rubbed leather edge',(.32,.185,.085))
thread = material('WM Linen stitching',(.52,.37,.20))
lightwood = material('WM Raw wood',(.36,.235,.12),ROOT/'references/wm-native/wood-staff-albedo-v01.png')
ridge = material('WM Wood worn ridges',(.51,.37,.20))
brass = material('WM Muted brass',(.32,.21,.075),rough=.67)
brass.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=.5
iron = material('WM Blackened iron',(.049,.051,.043),rough=.78)
iron.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=.28
coal = material('WM Charred grain',(.031,.022,.014))
redhide = material('WM Russet binding',(.18,.044,.021))
olive = material('WM Range fill',(.23,.255,.115))
ivory = material('WM Warm text highlight',(.75,.62,.39))
ember = material('WM Recessed amber ember',(.75,.12,.009))
bsdf=ember.node_tree.nodes['Principled BSDF']
bsdf.inputs['Emission Color'].default_value=(1,.16,.007,1)
bsdf.inputs['Emission Strength'].default_value=.9
assets={}


def begin(aid,slug,location=(0,0,0)):
    col,root=group(scene,aid+'_'+slug,location,aid)
    assets[aid]=(col,root,slug)
    return col,root


def ribbon(name,centers,width,mat,col,parent,axis=(0,0,1),thick=.003):
    vs=[]
    uv=[]
    for i,p in enumerate(centers):
        for side in (-1,1):
            vs.append(Vector(p)+Vector(axis)*width*.5*side)
            uv.append((i/max(1,len(centers)-1), .2 if side<0 else .3))
    fs=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(centers)-1)]
    obj=mesh(name,vs,fs,mat,col,parent,uv,True)
    sol=obj.modifiers.new('Leather strap thickness','SOLIDIFY');sol.thickness=thick
    return obj


def plate(name,body,loc,size,col,parent,mat=paper,font_size=.046,outline=True):
    x,y,z=loc;w,h=size
    obj,point=sheet(name+'_body',loc,size,mat,col,parent,curl=.006,thickness=.0025,seed=len(name),nx=14,nz=8)
    if outline: border(name+'_ink_edge',point,.025,ink,col,parent,.0011)
    for dx in (-w*.45,w*.45):
        for dz in (-h*.35,h*.35):pin(name+'_pin',(x+dx,y-.011,z+dz),.007,brass,col,parent)
    if body:
        text(name+'_text',body,(x,y-.019,z),font_size,ink if mat==paper else ivory,col,parent,w*.90)
    return obj


# Four-position continuous hide, with independent loops and shallow toe supports.
col,root=begin('WM-01','deployed-leather',(-.36,0,1.60))
body,point=sheet('WM01_SINGLE_CONTINUOUS_HIDE',(0,0,.91),(1.66,1.84),leather,col,root,curl=.045,thickness=.004,nx=64,nz=64,seed=14)
body['construction']='One connected hide; four attached retention loops and toe rests'
body['deployed_positions']=4
border('WM01_Raw_turned_edge',point,.006,edge,col,root,.009)
border('WM01_Inner_shadow',point,.023,ink,col,root,.002)
stitch_border('WM01_Linen_edge_stitches',point,thread,col,root,74)
# Turned top and bottom lips have actual curvature, not a flat printed border.
for z in (.04,1.78):
    pts=[(-.79+i*1.58/75,-.036-.016*math.sin(i*.22),z+.008*math.sin(i*.31)) for i in range(76)]
    ribbon('WM01_Soft_folded_lip',pts,.11,leather,col,root)
for i,cx in enumerate((-.60,-.20,.20,.60),1):
    centers=[(cx-.064*math.cos(math.pi*k/30),-.016-.145*math.sin(math.pi*k/30),1.12) for k in range(31)]
    loop=ribbon('WM01_Retention_'+str(i),centers,.077,leather,col,root)
    loop['slot_index']=i;loop['part_role']='retention_loop'
    for sign in (-1,1):
        pin('WM01_Loop_rivet',(cx+sign*.065,-.029,1.12),.008,brass,col,root)
    curves('WM01_Loop_edge_stitches_'+str(i), [[(x,y-.001,z+dz) for x,y,z in centers] for dz in (-.030,.030)],.0012,thread,col,root)
    # The toe plate top at local .115 meets the metal ferrule at global 1.715.
    floor=box('WM01_Toe_floor_'+str(i),(cx,-.115,.109),(.17,.12,.012),leather,col,root,.004)
    floor['part_role']='toe_support';floor['slot_index']=i
    lippts=[(cx-.092*math.cos(math.pi*k/24),-.027-.17*math.sin(math.pi*k/24),.145-.025*math.sin(math.pi*k/24)) for k in range(25)]
    ribbon('WM01_Open_toe_rest_'+str(i),lippts,.07,leather,col,root)
    curves('WM01_Toe_rim_'+str(i),[[(x,y-.002,z+.035) for x,y,z in lippts]],.0025,edge,col,root)
for cx in (-.70,.70):
    ribbon('WM01_Hanging_strap',[(cx,.06,1.72),(cx,.03,1.92),(cx,-.022,1.96),(cx,-.044,1.78)],.048,leather,col,root,axis=(1,0,0))
    ring('WM01_Suspension_ring',(cx,-.025,1.79),.029,.006,iron,col,root)
    pin('WM01_Suspension_rivet',(cx,-.03,1.89),.009,brass,col,root)


# Physically separate, open-backed reserve rack.
col,root=begin('WM-02','reserve-rack',(.94,.025,1.60))
root['open_back']=True
for sign in (-1,1):
    x=sign*.325
    box('WM02_Upright',(x,0,.94),(.066,.095,1.88),wood,col,root,.007)
    box('WM02_Foot',(x,-.008,.024),(.105,.32,.048),wood,col,root,.006)
    tube('WM02_Rear_brace',[(x,.01,.29),(x,.135,.055)],[.021,.027],wood,col,root,8)
    for zz in (.10,1.67,1.78):
        box('WM02_Iron_joint',(x,-.053,zz),(.092,.010,.064),iron,col,root,.002)
        pin('WM02_Joint_nail',(x,-.062,zz),.008,brass,col,root)
for zz in (.085,1.70,1.80):
    box('WM02_Crossbar',(0,0,zz),(.77,.08,.07),wood,col,root,.006)
for j,x in enumerate((-.145,.145),1):
    hookpts=[(x,-.046,1.655),(x,-.066,1.54),(x,-.10,1.49),(x,-.145,1.50),(x,-.17,1.54)]
    tube('WM02_Iron_hook_'+str(j),hookpts,[.009]*5,iron,col,root,10)
    # Retention bands are seated on a cross support, not floating in the empty rack.
    box('WM02_Retention_backing_'+str(j),(x,0,1.12),(.20,.07,.048),wood,col,root,.003)
    centers=[(x-.057*math.cos(math.pi*k/24),-.031-.12*math.sin(math.pi*k/24),1.12) for k in range(25)]
    ribbon('WM02_Reserve_loop_'+str(j),centers,.037,leather,col,root)
    box('WM02_Toe_support_'+str(j),(x,-.115,.109),(.16,.14,.012),wood,col,root,.003)
    for sign in (-1,1):box('WM02_Toe_separator',(x+sign*.075,-.07,.15),(.027,.14,.07),wood,col,root,.003)


def build_staff(aid,slug,kind,location,slot):
    col,root=begin(aid,slug,location)
    root['staff_type']=kind;root['staff_instance']=slot;root['deployed']=True
    root['fixed_core']={'raw':'木纹芯','rhythm':'节律芯','ember':'余火芯'}[kind]
    mat=coal if kind=='ember' else lightwood
    # A tapered solid shaft, with a persistent gentle bend and faceted carved silhouette.
    centers=[];radii=[]
    height=1.31
    for i in range(55):
        z=height*i/54
        centers.append((.015*math.sin(z*7)+.009*math.sin(z*18),.005*math.sin(z*13),z))
        bulge=sum(.008*math.exp(-((z-c)/.035)**2) for c in (.43,.80,1.10))
        radii.append(.014+.007*i/54+.0025*math.sin(z*15)**6+bulge)
    tube(aid+'_Solid_wood_shaft',centers,radii,mat,col,root,14)
    paths=[]
    for k in range(19):
        angle=math.tau*k/19
        paths.append([(x+(r+.00045)*math.cos(angle+.08*math.sin(z*16+k)),y+(r+.00045)*math.sin(angle+.08*math.sin(z*16+k)),z) for (x,y,z),r in zip(centers,radii)])
    curves(aid+'_Long_carved_grain',paths,.00055,ink,col,root)
    for j in range(7):
        z=.20+j*.17
        n=min(54,round(z/height*54));cx,cy,_=centers[n];radius=radii[n]
        knot=[]
        for k in range(35):
            a=math.tau*k/34
            dx=.008*math.cos(a)
            knot.append((cx+dx,cy-math.sqrt(max(.00002,radius*radius-dx*dx))-.0008,z+.022*math.sin(a)))
        curves(aid+'_Wood_knot',[knot],.0008,ink,col,root)
    grip_z=.89 if kind!='rhythm' else .32
    for z0,turns in ((grip_z,5),(.48,2),(.17,2)):
        pts=[]
        for k in range(turns*20+1):
            a=math.tau*k/20;z=z0+k*.0015
            pts.append((.026*math.cos(a),.026*math.sin(a),z))
        ribbon(aid+'_Helical_grip',pts,.018,redhide if kind=='ember' else leather,col,root)
    for z in (.015,1.22):
        tube(aid+'_Metal_ferrule',[(0,0,z),(0,0,z+.035)],[.020 if z<.1 else .027]*2,brass,col,root,16)
    if kind=='rhythm':
        center=Vector((0,0,1.43));r=.105
        circle=[center+Vector((r*math.cos(math.tau*k/72),0,r*math.sin(math.tau*k/72))) for k in range(73)]
        tube('WM04_Open_wood_ring',circle,[.019]*73,lightwood,col,root,12)
        for k in range(9):
            a=math.tau*k/9
            p=center+Vector((r*math.cos(a),0,r*math.sin(a)))
            v=Vector((-math.sin(a),0,math.cos(a)))
            tube('WM04_Ring_copper_band',[p-v*.007,p+v*.007],[.022,.022],brass,col,root,12)
        curves('WM04_Ring_ink_carving',[[center+Vector((rr*math.cos(math.tau*k/80),-.017,rr*math.sin(math.tau*k/80))) for k in range(81)] for rr in (.098,.111)],.0008,ink,col,root)
        for z in (1.27,1.30):ring('WM04_Fixed_collar',(0,0,z),.028,.005,brass,col,root,'XY')
    else:
        branches=[[(0,0,1.21),(-.036,0,1.32),(-.065,-.01,1.41),(-.074,.006,1.53)],[(0,0,1.25),(.044,.007,1.35),(.079,.016,1.43),(.096,.006,1.56)]]
        if kind=='ember':
            branches.append([(0,.020,1.25),(.004,.026,1.43),(.028,.028,1.57)])
            branches[0][-1]=(-.071,-.005,1.48)
        for b,pts in enumerate(branches):
            tube(aid+'_Fork_branch_'+str(b),pts,[.027-.013*k/(len(pts)-1) for k in range(len(pts))],mat,col,root,12)
            for dx in (-.008,.006):curves(aid+'_Branch_cuts',[[Vector(p)+Vector((dx,-.019,0)) for p in pts]],.0008,ink,col,root)
        if kind=='raw':
            tube('WM03_Natural_branch_stub',[(-.025,-.003,1.31),(-.038,-.020,1.34),(-.045,-.021,1.35)],[.020,.014,.012],lightwood,col,root,12)
            for k in range(3):
                ring('WM03_Knot_growth',(-.031,-.031,1.313),.009+k*.004,.0008,ink,col,root)
        if kind=='ember':
            # Recessed, small faceted coal, with black wooden prongs occluding its boundary.
            tube('WM05_Recessed_ember',[(0,-.004,1.31),(.013,-.007,1.37),(.025,0,1.44)],[.015,.027,.005],ember,col,root,7)
            for k in range(8):
                a=math.tau*k/8
                pts=[(.030*math.cos(a),.030*math.sin(a),1.21),(.036*math.cos(a),.028*math.sin(a),1.36),(.033*math.cos(a),.029*math.sin(a),1.43)]
                curves('WM05_Charred_crack',[pts],.0010,ink,col,root)
    return col,root


rawcol,rawroot=build_staff('WM-03','raw-wood-staff','raw',(-.56,-.115,1.715),2)
rhythmcol,rhythmroot=build_staff('WM-04','rhythm-staff','rhythm',(-.96,-.115,1.715),1)
embercol,emberroot=build_staff('WM-05','ember-staff','ember',(-.16,-.115,1.715),3)
for staff in (rawroot,rhythmroot,emberroot):staff.scale=(1,1,.90)
instances,instroot=group(scene,'WM_Additional_staff_instances')
for label,loc,slot in [('Active_4',(.24,-.115,1.715),4),('Reserve_1',(.795,-.09,1.715),5),('Reserve_2',(1.085,-.09,1.715),6)]:
    obj=clone_group(rawcol,rawroot,instances,label,loc)
    obj.scale=(1,1,.90)
    obj['staff_instance']=slot;obj['deployed']=slot<=4
    obj.rotation_euler.z=(-.04 if slot==4 else .03 if slot==6 else 0)


# Configuration parchment. Each label remains a FONT object in .blend.
col,root=begin('WM-06','configuration-parchment',(0,-.195,.44))
obj,point=sheet('WM06_Parchment_body',(0,0,.55),(2.45,1.10),paper,col,root,curl=.015,seed=22,nx=52,nz=28)
border('WM06_Torn_dark_edge',point,.008,edge,col,root,.002)
for x in (-1.15,1.15):
    for z in (.055,1.045):pin('WM06_Corner_pin',(x,-.018,z),.015,brass,col,root)
text('WM06_Selected_name','① 节律杖',(-.52,-.045,.972),.085,ink,col,root,.70)
plate('WM06_Type','简易',(.05,-.025,.97),(.18,.072),col,root,mat=paper,font_size=.044)
text('WM06_Bound_spell','绑定法术 伤害敌人',(-.50,-.045,.837),.062,ink,col,root,.91)
text('WM06_ReadOnly','只读',(.04,-.045,.836),.031,ink,col,root,.09)
text('WM06_Spell_timing','冷却 4刻  |  释放 1刻',(-.49,-.045,.742),.044,ink,col,root,.81)
plate('WM06_To_reserve','移至备战架',(.80,-.030,.845),(.62,.155),col,root,font_size=.057)
curves('WM06_Information_dividers',[[(-.85,-.04,.66),(1.10,-.04,.66)],[(-.02,-.04,.22),(-.02,-.04,.62)],[(.59,-.04,.22),(.59,-.04,.62)],[(-.85,-.04,.22),(1.10,-.04,.22)]],.0012,edge,col,root)
text('WM06_Fixed_core','固定芯  节律芯',(-.48,-.045,.567),.044,ink,col,root,.66)
box('WM06_Lock_body',(-.82,-.05,.569),(.045,.018,.039),iron,col,root)
ring('WM06_Lock_bow',(-.82,-.048,.594),.018,.004,iron,col,root)
text('WM06_Core_effect','偶数次冷却 -1刻（简易）',(-.48,-.045,.492),.032,ink,col,root,.72)
text('WM06_Socket_label','可换镶嵌',(-.62,-.045,.403),.043,ink,col,root,.40)
for i,x in enumerate((-.55,-.27),1):
    obj=ring('WM06_Empty_socket_'+str(i),(x,-.045,.315),.056,.007,brass,col,root)
    obj['changeable_slot']=i
    text('WM06_Empty_'+str(i),'空',(x,-.047,.241),.030,ink,col,root)
text('WM06_Range_anchor','范围锚点 F3',(.283,-.045,.567),.041,ink,col,root,.55)
for row in range(2):
    for column in range(5):
        xx=.04+column*.108;zz=.46-row*.122
        highlighted=(column==2) if row==0 else column in (1,2,3)
        cell=box('WM06_Grid_'+('B' if row==0 else 'F')+str(column+1),(xx,-.006,zz),(.098,.004,.108),olive if highlighted else paper,col,root,.001)
        cell['grid_row']='B' if row==0 else 'F';cell['grid_column']=column+1;cell['highlighted']=highlighted
        curves('WM06_Grid_border',[[ (xx+dx,-.012,zz+dz) for dx,dz in [(-.049,-.054),(.049,-.054),(.049,.054),(-.049,.054),(-.049,-.054)]]],.0010,ink,col,root)
pin('WM06_Anchor_dot',(.256,-.016,.338),.011,ink,col,root)
text('WM06_Initial_label','首次冷却起点',(.86,-.045,.567),.040,ink,col,root,.50)
for label,x in [('-',.70),('0',.85),('+',1.0)]:plate('WM06_Start_'+label,label,(x,-.03,.44),(.12,.10),col,root,font_size=.059)
text('WM06_Initial_range','0–10刻',(.85,-.045,.335),.036,ink,col,root)
text('WM06_First_release','首次释放 4刻',(.85,-.045,.257),.041,ink,col,root,.45)
text('WM06_Timeline_label','首轮名义释放',(-.59,-.045,.17),.036,ink,col,root)
for x,body in [(-.60,'① 4刻'),(-.16,'② 5刻'),(.28,'③ 7–9刻'),(.72,'④ 8刻')]:
    plate('WM06_Timing_'+body,body,(x,-.015,.073),(.38,.071),col,root,font_size=.034,outline=True)
text('WM06_Nominal_notice','名义计划，战中可能改期',(.56,-.045,.17),.025,ink,col,root,.83)
portrait=clone_group(rhythmcol,rhythmroot,col,'WM06_Selected_staff_portrait',(-1.06,-.041,.05),.63)
portrait.parent=root
if 'staff_instance' in portrait:del portrait['staff_instance']
portrait['illustration_only']=True


# Shared signs, paper tags, medal numbers and operations, individually editable.
col,root=begin('WM-07','tags-and-controls')
plate('WM07_Main_title','法杖管理',(-.02,-.028,3.64),(1.42,.22),col,root,font_size=.136)
plate('WM07_Deployed_heading','出战法杖 4/4',(-.68,-.098,3.375),(.78,.127),col,root,font_size=.054)
text('WM07_Total_held','持有 6 根',(.08,-.098,3.372),.048,ivory,col,root,.32)
plate('WM07_Reserve_heading','备战陈列架',(.94,-.047,3.355),(.60,.12),col,root,font_size=.053)
for i,x in enumerate((-.96,-.56,-.16,.24),1):
    pin('WM07_Number_medal_'+str(i),(x,-.068,3.215),.043,brass,col,root)
    ring('WM07_Medal_rim',(x,-.072,3.215),.042,.002,ink,col,root)
    text('WM07_Number_'+str(i),str(i),(x,-.078,3.215),.052,ink,col,root)
names=['节律杖','原木杖','余火杖','原木杖','原木杖','原木杖']
xs=[-.96,-.56,-.16,.24,.795,1.085]
for i,(x,name) in enumerate(zip(xs,names),1):
    # Paper tags sit alongside the shaft, preserving the main wood silhouette.
    tx=x+.059
    obj,pt=sheet('WM07_Staff_name_tag_'+str(i),(tx,-.205,2.52),(.080,.278),paper,col,root,curl=.003,seed=i,nx=8,nz=12)
    border('WM07_Tag_edge_'+str(i),pt,.025,ink,col,root,.0009)
    text('WM07_Staff_name_'+str(i),'\n'.join(name),(tx,-.219,2.52),.040,ink,col,root,.067)
    ring('WM07_Tag_hole',(tx,-.21,2.635),.005,.0012,iron,col,root)
    curves('WM07_Name_tag_string_'+str(i),[[(x,-.155,2.75),(tx-.012,-.21,2.67),(tx,-.212,2.635)]],.0016,thread,col,root)
    if i>4:plate('WM07_Reserve_status_'+str(i),'未出战',(tx,-.181,2.15),(.115,.085),col,root,font_size=.031)
for x,spell in zip(xs[:4],['伤害敌人','获得护甲','释放火焰','火焰伤害敌人']):
    plate('WM07_ReadOnly_spell_'+spell,spell,(x,-.201,1.675),(.365,.09),col,root,font_size=.039)


def arrow(name,label,x,z,left):
    sign=-1 if left else 1
    vs=[(x-sign*.085,-.13,z-.062),(x+sign*.027,-.13,z-.062),(x+sign*.027,-.13,z-.094),(x+sign*.10,-.13,z),(x+sign*.027,-.13,z+.094),(x+sign*.027,-.13,z+.062),(x-sign*.085,-.13,z+.062)]
    o=mesh(name,vs,[tuple(range(7))],leather,col,root)
    m=o.modifiers.new('Wood arrow thickness','SOLIDIFY');m.thickness=.012
    curves(name+'_rim',[vs+[vs[0]]],.0025,brass,col,root)
    text(name+'_text',label,(x-sign*.006,-.15,z),.039,ivory,col,root,.125)
arrow('WM07_Move_forward','前置',-1.17,2.12,True)
arrow('WM07_Move_back','后置',.444,2.12,False)
plate('WM07_Back','返回地图',(-.64,-.072,.236),(.62,.182),col,root,mat=leather,font_size=.067)
plate('WM07_Save','保存配置',(.10,-.072,.236),(.62,.182),col,root,mat=leather,font_size=.067)
plate('WM07_Unsaved','有未保存修改',(.88,-.05,.236),(.60,.142),col,root,font_size=.042)
# Restrained selected outline is a separate state object, not baked into the hide.
pts=[(-1.085,-.182,1.73),(-1.085,-.182,3.12),(-1.06,-.182,3.18),(-.86,-.182,3.18),(-.84,-.182,3.12),(-.84,-.182,1.73)]
selection=curves('WM07_Selected_staff_outline',[pts],.0017,brass,col,root)
selection['state']='selected deployed slot 1'


# Framing and peripheral clutter retained as actual scene geometry.
stage,stage_root=group(scene,'WM_PAGE_CONTEXT')
for i in range(12):
    box('WM_Wall_plank',(-1.48+i*.269,.13,1.95),(.26,.075,4.03),wood,stage,stage_root,.006)
for z in (.043,1.585,3.78):box('WM_Back_crossbeam',(.025,.046,z),(3.10,.08,.063),wood,stage,stage_root,.008)
for x in (-1.46,1.48):
    box('WM_Frame_post',(x,.047,1.98),(.078,.16,3.99),wood,stage,stage_root,.009)
    for z in (.16,1.55,3.75):pin('WM_Frame_nail',(x,-.048,z),.012,iron,stage,stage_root)
# Books nest at the lower left, with visible page-block edges.
for i in range(3):
    z=.10+i*.115;x=-1.21+.02*i;y=-.22
    box('WM_Book_pages',(x,y,z),(.43,.21,.077),paper,stage,stage_root,.006)
    for zz in (z-.046,z+.046):box('WM_Book_cover',(x,y-.005,zz),(.46,.235,.020),leather,stage,stage_root,.006)
    box('WM_Book_spine',(x-.221,y,z),(.022,.23,.075),leather,stage,stage_root,.005)
    curves('WM_Book_page_lines', [[(x-.18,y-.107,z-.028+k*.01),(x+.20,y-.107,z-.027+k*.01)] for k in range(6)],.0006,edge,stage,stage_root)
    for xx in (x-.17,x+.17):box('WM_Book_metal_corner',(xx,y-.121,z+.056),(.036,.012,.010),brass,stage,stage_root,.003)
# Small caged lantern with geometry light source.
lampx=-1.39;lampz=2.71
for z in (lampz-.13,lampz+.13):box('WM_Lantern_cap',(lampx,-.24,z),(.16,.16,.022),iron,stage,stage_root,.008)
for dx in (-.061,.061):
    for dy in (-.061,.061):tube('WM_Lantern_bar',[(lampx+dx,-.24+dy,lampz-.13),(lampx+dx,-.24+dy,lampz+.13)],[.007,.007],brass,stage,stage_root,8)
tube('WM_Lantern_candle',[(lampx,-.24,lampz-.1),(lampx,-.24,lampz-.006)],[.017,.017],ivory,stage,stage_root,12)
tube('WM_Lantern_flame',[(lampx,-.24,lampz-.005),(lampx+.008,-.24,lampz+.044)],[.014,0],ember,stage,stage_root,7)
ring('WM_Lantern_handle',(lampx,-.24,lampz+.20),.055,.006,iron,stage,stage_root)
# Quill silhouette along the right edge.
quill=[]
for k in range(25):quill.append((1.385+.045*math.sin(k*.10),-.18,.17+k*.029))
curves('WM_Quill_shaft',[quill],.0028,ivory,stage,stage_root)
feather=[]
for i,p in enumerate(quill[4:-2]):
    w=.045*math.sin(math.pi*(i+1)/22)
    feather.extend([[Vector(p),Vector(p)+Vector((w,0,.033))],[Vector(p),Vector(p)+Vector((-w,0,.025))]])
curves('WM_Quill_barbs',feather,.0017,ivory,stage,stage_root)

bpy.context.view_layer.update()
cam=rig(scene,(.015,-.02,1.965),3.63,(1440,1920),front=True)
cam.data.ortho_scale=4.14
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.shading.type='MATERIAL'
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.clip_start=.001
pack_images()
bpy.ops.file.pack_all()
bpy.ops.object.select_all(action='DESELECT')
hide_body=bpy.data.objects['WM01_SINGLE_CONTINUOUS_HIDE']
hide_body.select_set(True);bpy.context.view_layer.objects.active=hide_body
scene.render.filepath=str(OUT/'renders/assembly.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'wand-management-master.blend'),compress=True)
(OUT/'source-catalog.json').write_text(json.dumps([{'id':a,'slug':s,'collection':c.name,'root':r.name} for a,(c,r,s) in assets.items()],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('WM BUILT',len(scene.objects),'objects; rendering',flush=True)
bpy.ops.render.render(write_still=True)
print('WM FIRST PASS DONE',flush=True)

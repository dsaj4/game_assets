# 法杖管理 v03 · 实体面板优化

2026-09-19。**PhysicalPanelRefined / NeedsArtReview**。这是实际 Blender 静态资产；生图原稿另存，不以效果图冒充模型渲染。

[组合母版](wand-management-master.blend) · [组合 GLB](wand-management-assembly.glb) · [文件清单](manifest.json) · [复查报告](quality-review.md) · [结构回导验证](verification.json) · [质量保护验证](quality-verification.json) · [图像来源与提示词](../../references/wm-panel-v03/provenance.json)

[v01／v02／v03真实渲染对照](comparison.md)。126项结构验证及18项质量保护检查通过。

![实际总装渲染](renders/assembly-oblique.png)

![实际面板近景](renders/WM-06-configuration-parchment.png)

![实际按钮近景](renders/buttons-detail.png)

本版重点是生成整件空白面板形态，再用轮廓网格、层叠纸页、边缘厚度和独立五金件承接画面。保留 v02 细皮革；袋中四出战、独立架上两备用、绑定法术只读、两镶嵌槽及 B3/F2/F3/F4 范围不变。

## 原生组件

| 组件 | Blender | GLB |
| --- | --- | --- |
| 展开皮袋 | [WM-01](assets/WM-01-deployed-leather.blend) | [GLB](assets/WM-01-deployed-leather.glb) |
| 备战架 | [WM-02](assets/WM-02-reserve-rack.blend) | [GLB](assets/WM-02-reserve-rack.glb) |
| 原木杖 | [WM-03](assets/WM-03-raw-wood-staff.blend) | [GLB](assets/WM-03-raw-wood-staff.glb) |
| 节律杖 | [WM-04](assets/WM-04-rhythm-staff.blend) | [GLB](assets/WM-04-rhythm-staff.glb) |
| 余火杖 | [WM-05](assets/WM-05-ember-staff.blend) | [GLB](assets/WM-05-ember-staff.glb) |
| 配置面板 | [WM-06](assets/WM-06-configuration-parchment.blend) | [GLB](assets/WM-06-configuration-parchment.glb) |
| 吊签与操作件 | [WM-07](assets/WM-07-tags-and-controls.blend) | [GLB](assets/WM-07-tags-and-controls.glb) |

## 打开和复现

在实验仓库根目录运行：

```powershell
.\open-wand-management.ps1
.\open-wand-management.ps1 -Asset parchment
.\open-wand-management.ps1 -Version v02
.\open-wand-management.ps1 -Version v01
. .\tools\env.ps1
& $BlenderExe -b --python-exit-code 1 --python art/wm_v03_pipeline.py -- verify
& $BlenderExe -b --python-exit-code 1 --python art/verify_wm_v03_quality.py
```

修改并保存母版后，用 `art/wm_v03_pipeline.py -- publish --republish` 重新导出，用 `art/render_wm_v03_details.py` 重渲近景，再运行两项验证。`art/refine_wand_management_v03.py` 是从保留的 v02 制作 v03 的初始生成器，有覆盖保护；人工编辑后不要用生成器覆盖母版。

图片和字体打包在 .blend，图片也内嵌 GLB。全部 49 个中文对象仍可编辑；GLB 中是固定字形网格。生成皮肤含手绘微阴影，不是经过分离的物理 PBR 材质；纸层和按钮主体厚度是几何，微裂纹、细缝线主要是画面信息。没有 Godot 交互、LOD、碰撞或运行性能验收。

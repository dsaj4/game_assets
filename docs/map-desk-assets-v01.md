# 地图桌面 · 原生 Blender 资产 01

2026-09-13。用户：“开始生成blender资产，猫先不用生成”。状态：**NativeAssetsCreated / NeedsArtReview**。

本批按[组件设计稿](blender-component-design-v01.md)制作 MD-01–08 和 MD-10，共九类；MD-09 猫暂缓。它们是可编辑的原生 Blender 网格／曲线，包含单件源文件和桌面组合工程。当前为首轮三维资产，美术细节仍可继续调整。

[资产与渲染图册](../art/map-desk-v01/README.md) · [组合工程](../art/map-desk-v01/map-desk-master.blend) · [组合渲染](../art/map-desk-v01/renders/assembly.png) · [文件与来源清单](../art/map-desk-v01/manifest.json) · [验证结果](../art/map-desk-v01/verification.json)

## 本批资产

| 编号 | 内容与可编辑结构 | 本轮处理 |
| --- | --- | --- |
| MD-01 | 木板桌面、抽屉前沿、后沿与铁件；羽毛笔／笔筒、天球仪、灯具 | 零件分别建模，杂物保留；羽片有轮廓与羽轴 |
| MD-02 | 薄纸网格、卷边、环境地图贴图 | 纸厚1.5 mm，中央平整；房屋、山地、桥与小路均画在纸上 |
| MD-03 | 独立红色断线、当前点红圈 | 真正独立的面片层；沿同一纸面函数贴合，未定义玩法路线数据 |
| MD-04 | 木雕袍身、尖帽、胡须、手杖和底座 | 帽顶折面、袍身刀痕、浅色胡须条与环形杖首可单独调整 |
| MD-05 | 九块围石、木柴、灰烬、火焰片 | 静态实体围石／木柴和交叉火焰轮廓片，无火焰模拟 |
| MD-06 | 透射球壳、托碗、三足、内部问号与云雾核心 | 使用真实透射玻璃材质、内部几何雾纹与不透明混浊核心；尚非体积雾模拟 |
| MD-07 | 底座、木墙、拱门、窗框、四坡瓦顶和烟囱 | 屋瓦分块，门窗轮廓与地点棋子底座均有厚度 |
| MD-08 | 中空箱体、弧形箱盖、铁箍、铆钉、锁片、铰链、金币 | 后铰链独立；电脑插件将开角从48°调整到60°，后处理保留；金币铺在降低后的底层上 |
| MD-10 | 三本闭合旧书，各自包含封皮、书脊与页块 | 错落书叠，封皮压纹／边缝／细裂纹、纸页侧线可编辑 |

## 文件怎么用

- 日常整体修改打开 `art/map-desk-v01/map-desk-master.blend`。九个 MD 集合按职责分开，`PRESENTATION` 单独保存相机和灯光。
- 逐件编辑打开 `art/map-desk-v01/assets/` 内的 `.blend`。各件的父级原点归零，保留米制、+Z向上、-Y为正面，带单件预览相机和不参与导出的展示地面。
- 导入其他工具使用同目录的 `.glb`。导出副本将曲线转换为网格，应用修改器，并内嵌所需图片；Blender源文件中的曲线仍然可编辑。
- 宝箱箱盖由 `MD08_LID_HINGE`（分件文件中名称可能带编号后缀）控制，绕本地X轴负向开启。闭合为0°，本轮展示为-60°；箱盖子件跟随真实后铰链。
- 保存的纹理已打包进 `.blend`，移动文件后仍能读取。地图原图与提示词另见 `references/map-desk-assets-v01/`；木纹沿用上一批已归档生成素材，通过UV取样映射。

## 生成与原生界面修改

1. `art/build_map_desk_v01.py` 生成本批全新源文件和首轮组合渲染，不读取或覆盖旧E1场景。
2. 用电脑插件打开原生Blender，在对象变换面板修改宝箱铰链角度并保存。
3. `map-desk-generated.blend` 保留界面修改前的工程；`map-desk-ui.blend` 保存界面修改后的工程，`ui-hinge-60deg.png` 为操作证据。
4. `art/publish_map_desk_v01.py` 只从UI源文件继续加工，补齐金币、羽片与书皮细节、校准单件取景，并生成组合母版、九个分件源、GLB和渲染。它会验证箱盖角度并保留该变换。
5. `art/verify_map_desk_v01.py` 重新打开原生资产，再实际导入每个GLB，检查几何、包围范围、打包图片、文件哈希和无猫范围。

在实验工作区PowerShell中可运行：

```powershell
. ./tools/env.ps1
& $BlenderExe --background --factory-startup --python-exit-code 1 --python art/publish_map_desk_v01.py
& $BlenderExe --background --factory-startup --python-exit-code 1 --python art/verify_map_desk_v01.py
```

需要重做基础造型时再运行生成脚本；之后重新进行或迁移UI修改，并更新UI源。不要用生成脚本覆盖已手工细化的母版。初始生成文件 `map-desk-source.blend` 曾在UI中保存，正式后处理输入固定为另行归档的 `map-desk-ui.blend`。

## 已检查与保留限制

组合图和逐件图均由Blender实际渲染。审阅后修正了金币底层遮挡、羽片形状、书皮细节、法师胡须、石面刻线和宝箱铁箍位置；独立载入分件解决了取景变换未刷新的问题。GLB回导还捕获并修复了跨场景选中金币混入单件的问题。最终文件验证结果以链接中的 `verification.json` 为准。

本轮保留墨线木纹、地图插画与几何轮廓，并以Blender Freestyle补充描边。Freestyle不会随GLB导出；因此这些GLB是可交换模型，尚不能据此声称Godot中已达到同样渲染效果。

猫按用户要求未制作。球内雾、透明玻璃、动态火焰、精细雕刻排线和整体光照仍需后续美术迭代；本批不等于已达到设计图／FLASK参考的最终完成度。没有新增Godot运行场景、碰撞、LOD、性能、交互或玩法验收，旧E1 R2运行入口继续保留。

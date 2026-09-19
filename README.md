# game-002 Godogen 3D Lab

独立 demo 工作区：`E:\Project\game-002-godogen-lab`。

**2026-09-19 第二轮布局探索：** 按用户选择保留自然手作、黄铜仪器风格，并新增横置法杖主体／简单悬浮投影；[三张新效果图](concepts/wand-management-independent-v02/index.md)均由独立agent构思并生图。画面改用横向3:2，围绕当前单杖组织配置，库存侧收，次要说明折叠；[实图复查](concepts/wand-management-independent-v02/comparison.md)记录简化效果和符号／高亮限制。状态VisualExplorationDraft / NeedsReview，尚未选择或建模，v03母版保持原样。

**2026-09-19 新设计探索：** 用户认为面板UI仍呆板，已让三名不继承旧对话的agent仅依据功能与风格背景独立构思，并各自使用内置生图生成[三个新方向](concepts/wand-management-independent-v01/index.md)：旅途手作、暗黑木刻、黄铜天文仪器。来源、设计说明、提示词及实图检查分别归档，状态 VisualExplorationDraft / NeedsReview；尚未选择方向，现有 v03 原生资产未变。

**2026-09-19 字体效果探索：** 按用户提供的 Jacquard 24 像素哥特参考，用生图完成[整页及局部中文字体示意](concepts/wand-management-type-v01/index.md)。状态 TypographyVisualDraft / NeedsReview；这是绘制效果，未制作字体文件，未修改下方 v03 Blender 资产。

**2026-09-19 当前：法杖管理实体面板 v03。** 已先复查 v01/v02，保留有效皮纹，修正主按钮被贴图化的立体感退步。新生成空白层叠羊皮板与黑／红皮革按钮，接入真实轮廓网格、纸层、厚度和独立固定件；全部文字与配置状态保持独立。[当前资产与真实渲染](art/wand-management-v03/README.md)、[质量复查](art/wand-management-v03/quality-review.md)、[生图来源／提示词](references/wm-panel-v03/provenance.json)。默认启动脚本打开 v03，支持 `-Version v01/v02/v03`；旧版保留。状态 PhysicalPanelRefined / NeedsArtReview，仍是静态 Blender 美术，未接入管理交互。以下为历史记录。

**最新：法杖管理左页已完成首版原生建模。** 用户2026-09-14明确“开始建模”，七组模型、组合母版、独立.blend／GLB与实际渲染见[原生资产图册](art/wand-management-v01/README.md)和[制作报告](docs/wand-management-native-report.md)。袋中四出战、独立架上两备用，绑定法术只读，配置纸面和操作牌文字可编辑；当前为NativeAssetsCreated / NeedsArtReview。通过原生重开、GLB回导及结构检查，仍待美术评议，Godot与交互未新增。本轮采用Blender内置Python，电脑控制工具当前不可用。下方“尚未建模”均为此前设计阶段记录。

**最新：法杖管理整体03已通过，七组组件稿完成。** 用户2026-09-14确认“设计通过，下一步开始细化组件”。[组件图册](concepts/wand-management-sheets-v01/index.md)含展开皮袋、独立备战架、原木／节律／余火三种法杖、配置羊皮纸及吊牌操作件；[中文建模说明](docs/blender-wand-management-components-v01.md)记录分件、材质、建议尺度和校准项。状态 OverallDirectionConfirmed / ComponentDesignDraft。[整体03](concepts/wand-management-overall-v03.png)及[原视觉说明](docs/wand-management-visual-design-v01.md)继续约束袋中四出战、架上备用，法术／词卡不在本页编辑。七张选用稿均1448×1086，另保留两张去除额外铜铃前的历史图；本页尚未新建原生模型或交互。其余功能来源仍为[全游戏GDD RC1局部快照](references/design/2026-09-14-wand-management-rc1/manifest.json)。

**前批：MD-11 长法杖袋已完成首版原生建模。** 用户明确“开始建模”，交付[单件源文件与真实渲染](art/md-11-v01/README.md)、[加入长袋的桌面组合 v02](art/map-desk-v02/README.md)和[制作报告](docs/md-11-native-report.md)。整皮袋身约1.9米，两支长杖独立可编辑，替代猫的位置横放后沿，杂物保留。状态 NativeAssetCreated / NeedsArtReview；本轮未新增 Godot 或交互实现。

**前轮：整体05已确认，法杖袋两张设计稿已完成。** [MD-11图册](concepts/blender-sheets-v02/index.md)包含外观多视图和整皮包卷拆件；[中文建模说明](docs/blender-wand-roll-design-v01.md)记录建议尺度、分件与校准项。[整体效果图05](concepts/map-desk-overall-v05.png)无需重复确认；下方保留此前九类资产及E1的来源。

**前批：9 类 Blender 原生资产已生成，猫暂缓。** 用户在确认整体及分件设计图后明确“开始生成blender资产，猫先不用生成”。本批含桌面与保留杂物、环境地图、红线、法师木雕、篝火、水晶球、建筑、宝箱和书；提供[旧组合母版](art/map-desk-v01/map-desk-master.blend)、[分件源与渲染图册](art/map-desk-v01/README.md)和[制作说明](docs/map-desk-assets-v01.md)。状态 NativeAssetsCreated / NeedsArtReview；实际Godot运行实现仍为 [E1 R2](docs/e1-r2-report.md)，E2–E4 未启动。

| 层 | 固定环境 |
| --- | --- |
| 工作流 | Godogen 05cebffc，Godot / Codex 的本地适配 |
| 引擎 | Godot 4.7.2 .NET，C#，Forward+ / Jolt |
| 编译 | .NET SDK 8.0.419，net8.0 |
| 资产 | Blender 4.5.13 LTS，原生 UI + 内置 bpy |
| 外部脚本 | Python 3.14.0，独立 .venv，无第三方依赖 |
| 已验证 GPU | NVIDIA RTX 5060 Laptop，Vulkan 1.4.341 |

工具安装在本项目 .tools；现有 .NET 与 Python 通过本地配置引用，不修改全局 PATH。版本、下载地址及校验值见 [toolchain.lock.json](toolchain.lock.json)。

在此目录的 PowerShell 中：

```powershell
.\tools\check-environment.ps1
.\open-godot.ps1
.\open-blender.ps1
.\open-e1.ps1
.\open-map-desk.ps1
.\open-wand-management.ps1
# 单件示例：.\open-map-desk.ps1 -Asset mage
```

Godot 入口是 `game/project.godot`，默认打开当前 E1 墨线小样；按 1/2 对比材质，Esc 退出。`tools/build-e1-r2.ps1` 从保存的 Blender UI 修改重建 R2；`tools/capture-e1.ps1 -Revision r2` 采集 GPU 实机图。旧 `tools/build-e1.ps1` 是 R1 生成器，会覆盖运行资产，不用于重建 R2。`setup.ps1` 可重建便携工具、Python 环境和本机路径并复查；在其他机器上用参数指定已有 Python/.NET 路径，所需 SDK 见 global.json。上游参考源码抓取和技能登记单独处理，非启动必需。

先前环境验收包括空场景、工具链与 Vulkan 探针，见 [环境报告](docs/environment-report.md)。本轮另完成一个 E1 法杖/纸签/地图摆件样本与 A/B、1080p/720p 实机图，见 E1 报告；尚无装配、选路、战斗或发行包验证。

| 资料/资产 | 状态与来源 |
| --- | --- |
| references/flask-style-user-reference.png | 用户提供的视觉参考，未作为游戏资产使用 |
| references/design/ | game-002 启动时固定设计快照与文件哈希 |
| artifacts/environment-smoke/ | 标准立方体与空场景工具探针，仅本地生成 |
| art/e1 与 game/assets/e1 | E1 原生模型；R2 保留电脑插件操作的屋顶修改，bpy 补充模型细节并映射生成材质；可编辑 .blend、GLB 和独立版本哈希清单 |
| references/e1-r2-generated | 三份图像模型原创输出、完整提示词与 SHA；造型板仅参考，木纹和地图纸原图用于模型 albedo，未复制 FLASK 资产 |
| concepts/visual-direction-v01.png | 两屏概念效果图，imagegen生成，非实机、非运行资产；提示词同目录保存 |
| concepts/map-desk-overall-v02.png | 右侧地图桌面整体概念图；用户已确认整体方向并启动分件设计，杂物保留；生成时清单保留原始状态，后续确认以当前设计文稿为准 |
| concepts/map-desk-overall-v03.png | 法杖袋整体修订，内置imagegen编辑02；整皮卷袋／两支杖头位于右后桌沿，原猫仅保留在概念图；完整提示词与哈希留档，整体待确认 |
| concepts/map-desk-overall-v04.png | 历史位置修订：猫移除，已认可形象的法杖袋加长、横置原猫位置；提示词与哈希归档，新版整体待确认 |
| concepts/map-desk-overall-v05.png | 当前整体修订：长袋横贯后沿，法杖允许接近或超过桌宽；用户已确认整体并启动MD-11组件设计，提示词与哈希归档 |
| concepts/blender-sheets-v02/ | MD-11两张选用设计板，1448×1086；外观v01、拆件v02，另保留拆件修订前图；对应模型现位于art/md-11-v01 |
| art/md-11-v01 与 art/map-desk-v02 | 长袋原生母版、GLB、保留UI调整的来源、真实渲染、加入长袋的新桌面组合；旧九件资产未覆盖 |
| references/md-11-native/ | 1254×1254旧皮革 albedo 原图、完整提示词与来源哈希；原图字节未修改 |
| concepts/blender-sheets-v01/ | 10 张选用组件设计稿（1536 × 1024）、2 张修订前图、12 份完整提示词与来源 SHA256；地图／红线选用 v02，图册和中文建模说明记录尺度、拆件及校准项；仅作建模参考 |
| art/map-desk-v01/ | MD-01–08、MD-10九类原生资产；组合母版、独立.blend／GLB、渲染和验证；UI调整宝箱开角后保存并保留，MD-09猫未制作 |
| references/map-desk-assets-v01/ | imagegen生成的无标注环境地图albedo、完整提示词和来源清单；原图按字节复制，未把设计板标注映射进游戏表面 |
| references/flask-map-user-reference-2026-09-13.png | 用户最新地图截图，作为图像模型风格／构图参考，不是运行资产 |

继续入口：[左页原生资产](art/wand-management-v01/README.md)、[制作报告](docs/wand-management-native-report.md)、[已完成右侧长袋与桌面](art/map-desk-v02/README.md)。下一步评议左页真实模型并细化造型／材质，当前无后台自动开发任务。

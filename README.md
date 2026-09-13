# game-002 Godogen 3D Lab

独立 demo 工作区：`E:\Project\game-002-godogen-lab`。

**最新：法杖袋整体修订待确认。** [整体效果图03](concepts/map-desk-overall-v03.png)在右后桌沿增加整张旧皮革卷成的法杖袋，露出两支杖头，作为后续法杖管理入口的视觉物件；[设计说明](docs/map-desk-visual-design-v03.md)记录形态与制作顺序。状态 OverallRevisionAwaitingConfirmation；用户确认整体后，先新增MD-11组件效果图，再新建Blender资产。当前模型仍为下方九类，猫模型暂缓。

**当前：9 类 Blender 原生资产已生成，猫暂缓。** 用户在确认整体及分件设计图后明确“开始生成blender资产，猫先不用生成”。本批含桌面与保留杂物、环境地图、红线、法师木雕、篝火、水晶球、建筑、宝箱和书；提供[组合母版](art/map-desk-v01/map-desk-master.blend)、[分件源与渲染图册](art/map-desk-v01/README.md)和[制作说明](docs/map-desk-assets-v01.md)。状态 NativeAssetsCreated / NeedsArtReview；实际Godot运行实现仍为 [E1 R2](docs/e1-r2-report.md)，E2–E4 未启动。

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
| concepts/blender-sheets-v01/ | 10 张选用组件设计稿（1536 × 1024）、2 张修订前图、12 份完整提示词与来源 SHA256；地图／红线选用 v02，图册和中文建模说明记录尺度、拆件及校准项；仅作建模参考 |
| art/map-desk-v01/ | MD-01–08、MD-10九类原生资产；组合母版、独立.blend／GLB、渲染和验证；UI调整宝箱开角后保存并保留，MD-09猫未制作 |
| references/map-desk-assets-v01/ | imagegen生成的无标注环境地图albedo、完整提示词和来源清单；原图按字节复制，未把设计板标注映射进游戏表面 |
| references/flask-map-user-reference-2026-09-13.png | 用户最新地图截图，作为图像模型风格／构图参考，不是运行资产 |

继续入口：[法杖袋整体修订](docs/map-desk-visual-design-v03.md)、[原生资产图册](art/map-desk-v01/README.md)、[制作与验证说明](docs/map-desk-assets-v01.md)、[十张参考设计稿](concepts/blender-sheets-v01/index.md)。下一步先确认法杖袋整体构图，再依次做新增组件图与Blender资产；猫模型继续暂缓，当前无后台自动开发任务。

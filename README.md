# game-002 Godogen 3D Lab

独立 demo 工作区：`E:\Project\game-002-godogen-lab`。

**当前：E1 R2 同页美术修订，图像参考＋原生 Blender UI／Python。** 用户 2026-09-13 要求继续当前页面，增加图像模型参考并通过电脑插件细化 Blender 模型；最新结果见 [R2 实机报告](docs/e1-r2-report.md)，[首轮报告](docs/e1-report.md)保留。E2–E4 仍未启动。参考入口：[视觉方向01](docs/visual-direction-v01.md)、[实验计划v0.1](docs/experiment-plan-v01.md)。

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

继续入口：[最新设计背景](docs/design-context.md)、[分阶段 UI 任务](docs/deferred-ui-experiment.md)、[Godogen 适配说明](docs/godogen-adaptation.md)、[原生资产方式](docs/native-assets.md)。下一步仍为 E1 风格修订与用户评议；当前无后台自动开发任务。

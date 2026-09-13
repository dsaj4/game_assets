# game-002 Godogen 3D Lab

独立 demo 工作区：`E:\Project\game-002-godogen-lab`。

**当前：环境就绪；法杖装配与地图 UI 实验待启动。** 用户 2026-09-13 要求采用 Godogen + 原生 Blender + Python，从零探索 3D，暂不开始长期任务。

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
```

Godot 入口是 `game/project.godot`，目前只有空 Node3D 场景。`setup.ps1` 可重建便携工具、Python 环境和本机路径并复查；在其他机器上用参数指定已有 Python/.NET 路径，所需 SDK 见 global.json。上游参考源码抓取和技能登记单独处理，非启动必需。

环境验收包括：C# 编译零错误/警告、构建时生成空场景、Godot 编辑器导入与无头启动、Blender 保存 .blend/导出 GLB、Godot C# 读取 GLB，以及原生 Vulkan 输出两张空场景 PNG。证据见 [环境报告](docs/environment-report.md)。没有制作或验收法杖、地图、美术样件和玩法；当前不含发布打包验证。

| 资料/资产 | 状态与来源 |
| --- | --- |
| references/flask-style-user-reference.png | 用户提供的视觉参考，未作为游戏资产使用 |
| references/design/ | game-002 启动时固定设计快照与文件哈希 |
| artifacts/environment-smoke/ | 标准立方体与空场景工具探针，仅本地生成 |
| 正式游戏资产 | 尚无 |

继续入口：[最新设计背景](docs/design-context.md)、[待启动 UI 任务](docs/deferred-ui-experiment.md)、[Godogen 适配说明](docs/godogen-adaptation.md)、[原生资产方式](docs/native-assets.md)。后续须由用户明确启动，再补具体交互与验收；当前无后台自动开发任务。

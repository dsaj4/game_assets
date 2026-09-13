# 环境验收记录

日期：2026-09-13。状态：EnvironmentReady。范围限定为工具与空项目，不是 UI 可行性或玩法测试。

| 检查 | 实际结果 |
| --- | --- |
| Godot 二进制 | 4.7.2.stable.mono.official.ed1daf0bf；ZIP SHA256 与官方 release digest 一致 |
| Blender 二进制 | 4.5.13 LTS，daeeeca98fb0；ZIP SHA256 与官方校验文件一致 |
| .NET | 已有 8.0.419；net8.0 项目与捆绑 Godot.NET.Sdk 4.7.2 配合构建成功，0 警告/0 错误 |
| 外部 Python | 3.14.0；项目独立 .venv，未安装第三方包 |
| Blender Python | 原生背景进程运行 bpy，保存 probe.blend 和导出 cube.glb，退出 0 |
| 场景生成 | C# SceneTree 构建器成功保存空 Node3D 场景并验证重新实例化 |
| 导入/启动 | Godot 编辑器导入成功、空项目无头运行后正常退出 |
| 资产读取 | Godot C# GltfDocument 读取临时 GLB 并找到 MeshInstance3D，PASS |
| GPU/截图 | Vulkan 1.4.341，Forward+，RTX 5060 Laptop，进程退出 0，输出 2 张 1280×720 PNG |

本地原始证据：`artifacts/environment-smoke/check.log`、`result.json`、`blender.json`、`gpu.log`、`gpu-error.log` 和 `frame00000000.png` / `frame00000001.png`。关键日志副本在 [evidence](evidence/)；完整临时文件不进入 Git。

初次导入在主场景尚未生成时失败（Cannot open EnvironmentOnly.tscn）。已改为先编译和运行构建器，再执行编辑器导入；整条检查随后通过。这个启动顺序已固定在 tools/check-environment.ps1。

GPU 探针只验证输出能力，两帧空场景不能评价画面、性能目标或交互。没有进行样张生成、视频内容分析、装配流程、地图流程、数值或用户体验测试。没有安装 Blender MCP、GodotMaker 或云端资产生成技能；上游 asset-gen 留作未启用参考。

开发环境已就绪；Windows 导出模板、发行包与跨机器验证尚未进行，按后续发布任务准备。

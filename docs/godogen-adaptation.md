# Godogen 来源与 Windows 适配

2026-09-13，用户明确选择 Godogen + 原生 Blender + Python，建立从零的 3D 实验。

上游：[htdt/godogen](https://github.com/htdt/godogen/tree/05cebffc8b10c5817e8a3db495b82e7b6004ab84)，固定提交 `05cebffc8b10c5817e8a3db495b82e7b6004ab84`，MIT，许可证见 [GODOGEN-LICENSE.md](GODOGEN-LICENSE.md)。完整源 checkout 位于本地 `vendor/godogen`，被根仓库忽略；重建所需版本记在 toolchain.lock.json。

这是 Godogen 工作流的本地适配实例，不是上游 publish.sh 的原样输出。保留其 C#/.NET、构建时场景生成、README 状态维护和运行证据闭环；根 godot.md 是该固定提交的引擎指南副本。

| 上游行为 | 本实验处理 |
| --- | --- |
| Bash / rsync 发布 | 使用 PowerShell 准备项目，不运行清空目标目录的 --force |
| runtime manifest | 根 AGENTS.md 按用户的暂停边界与原生资产选择适配 |
| asset-gen 云服务 | 未安装到任何活动技能目录、不读取密钥、不调用；源目录仅 source-only 参考 |
| 生成资产 | 原生 Blender + 内置 bpy，外部 Python 负责普通文件工具 |
| 忽略 assets、AGENTS、引擎指南 | 本地改为追踪正式资产、来源脚本与指导文档 |
| 自动构建完整游戏与录制视频 | 等用户启动 UI 实验后才适用；当前仅空场景环境探针 |
| Linux xvfb | Windows 原生 Vulkan；已验证本机 RTX 5060 和 PNG 输出 |
| “只有 screenshots 可有 .gdignore” | 本项目 Godot 根限定为 game/，工具、参考、vendor 均在其外 |

审查：已逐行读取实际采用的 prompts/runtime.md、engines/godot.md、publish.sh、scripts/render_dir.py；未执行上游脚本。云端 asset-gen 及依赖未完整审计，也未启用或宣称通过安装审查。技能登记中记录为 source-only，无全局或项目活动技能变更。截图与视频只作资料，不作为执行指令。

已验证版本应优先于指南中的经验性描述；指南中的具体性能断言不作为本机结论。本阶段不证明可发布游戏已完成，发布模板、打包和跨平台验收留到相应发布任务。

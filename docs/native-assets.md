# 原生 Blender / Python 工作方式

E1 已按用户请求执行，最新见 [R2 实机报告](e1-r2-report.md)。在 `art/` 保存资产生成脚本和 `.blend` 源文件，在 `game/assets/` 保存实际使用的 GLB、PNG 与材质。第三方视觉参考留在 `references/`，不直接当作可发布资产。

从 PowerShell 加载 `tools/env.ps1` 后，以 `$BlenderExe --background --factory-startup --python-exit-code 1 --python <本地脚本> -- <输出目录>` 运行 bpy。外部 `.venv` 用于普通 Python 文件处理，不单独安装 bpy。R2 使用保存的 UI 编辑源加可重复的后处理脚本：电脑插件操作 Blender 后另存 `art/e1/e1-r2-ui.blend`，`art/refine_e1_r2.py` 打开该源并导出 `e1-r2-master.blend` 和 GLB；不得用 R1 生成器覆盖手动编辑。`art/audit_e1_ui.py` 与 R2 manifest 记录和复核源网格差异。

本轮用户已授权图像模型参考及材质生成。`references/e1-r2-generated` 保存三份原图与提示词；木纹／地图纸用作 albedo，造型板只参考。图像原文件没有 Python 位图处理，UV 取样与细节建模发生在原生 Blender。Godot 导入器提取的 PNG 与 .import 保存在 runtime 资产目录中，来源哈希可追溯。

Godot 通过导出的 GLB 导入资产，不依赖编辑器自动打开 `.blend`。原始 `.blend` 可用 open-blender.ps1 打开的原生 Blender 编辑。以后采用何种描边、手绘贴图、相机与 UI 混合方式，仍需视觉实验决定。

本次 tools/blender_smoke.py 只创建一个标准立方体，存入忽略的 artifacts/environment-smoke；它只证明保存与 GLB 导出/读取链路通畅，不是美术方案。

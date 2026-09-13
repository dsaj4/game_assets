# 原生 Blender / Python 工作方式

E1 已按用户请求执行，见 [实机报告](e1-report.md)。在 `art/` 保存资产生成脚本和 `.blend` 源文件，在 `game/assets/` 保存实际使用的 GLB、PNG 与材质。第三方视觉参考留在 `references/`，不直接当作可发布资产。

从 PowerShell 加载 `tools/env.ps1` 后，以 `$BlenderExe --background --factory-startup --python-exit-code 1 --python <本地脚本> -- <输出目录>` 运行 bpy。外部 `.venv` 用于普通 Python 文件处理，不单独安装 bpy。修改和导出应由同一个资产脚本可重复生成；坐标、单位、材质与命名在具体样件时再定。

Godot 通过导出的 GLB 导入资产，不依赖编辑器自动打开 `.blend`。原始 `.blend` 可用 open-blender.ps1 打开的原生 Blender 编辑。以后采用何种描边、手绘贴图、相机与 UI 混合方式，仍需视觉实验决定。

本次 tools/blender_smoke.py 只创建一个标准立方体，存入忽略的 artifacts/environment-smoke；它只证明保存与 GLB 导出/读取链路通畅，不是美术方案。

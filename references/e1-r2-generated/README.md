# E1 R2 图像参考与材质候选

日期：2026-09-13。使用内置 `image_gen.imagegen`，每个资产独立调用；未使用外部 API。三份图片均为原始生成文件的直接复制，没有裁切、调色或重新编码；生成目录中的原图仍保留。

任务范围：当前 E1 页面。图片只提供建模参考或材质候选，不代表 Godot 实机结果，也不表示美术方向已验收。

同轮后续：木纹与地图纸已贴到 R2 的原生模型上，并完成 Blender/Godot 实机验证，见 [R2 报告](../../docs/e1-r2-report.md)。建模板仍只作造型参考；生成时清单中的 Candidate 状态保留为来源记录，实际使用状态以 R2 资产清单为准。

## 输入与用途

已目视阅读 [用户 FLASK 风格参考](../flask-style-user-reference.png) 与 [方向图 01](../../concepts/visual-direction-v01.png)。本次依据观察将风格写成文本提示词，工具输入没有附带图片，也没有对既有图片执行编辑。

| 文件 | 实际尺寸 | 用途与观察 |
| --- | --- | --- |
| [wand-tower-modeling-board-v01.png](wand-tower-modeling-board-v01.png) | 1536 × 1024 | 法杖双角度与石塔三角度建模参考。法杖渐细、有木节、黄铜根须抱住固定翡翠；塔楼门洞、侧墙、扶壁和斜顶体积可辨。示意视图并非严格工程三视图。 |
| [wood-ink-albedo-v01.png](wood-ink-albedo-v01.png) | 1254 × 1254 | 木板漫反射／albedo 候选。横向灰褐墨线、稀疏木节，无物体边框。基色较暗，实机避免再次大幅压暗；未验证无缝平铺，优先每根木板单独展开映射。 |
| [map-paper-albedo-v01.png](map-paper-albedo-v01.png) | 1536 × 1024 | 地图纸漫反射／albedo 候选。山林集中下缘与两侧，中央上方留白；无路线、节点、文字、塔楼。纸纹略密，需在最终画幅检查文字可读性。 |

请求方向分别是横向 3:2、方形 1:1、横向 3:2；工具实际输出尺寸见表。

## 原始提示词

### wand-tower-modeling-board-v01.png

```text
Use case: stylized-concept. Asset type: a single landscape 3:2 modeling-reference sheet for handcrafted fantasy game props. Create an original asset design, not a screenshot and not a game UI. On aged pale gray-beige paper, upper half shows TWO matching views of one long horizontal crooked dark-wood magic wand, one direct side view and one slightly rotated three-quarter view: subtly asymmetric tapering branch shaft, small scars and knots, sparse thin curling bronze roots wrapping the shaft, a permanently set faceted emerald-green gem at the right-hand tip inside an irregular antique brass root/claw setting. The wand is slender, not a massive battle staff. Lower half shows THREE consistent views of the same crooked squat medieval stone watchtower miniature: front, clear three-quarter view, and side. The tower has a readable irregular rectangular main volume, short projecting masonry buttresses, a deeply recessed narrow arched door, two tiny slit windows, and a steep dark slate roof leaning a little to one side. The side walls and roof depth must be clearly legible so a Blender modeler can infer volume. Props spaced apart with quiet empty margins, no full environment. Style: exceptionally fine hand-inked engraving, irregular charcoal contours, varied line weight, tight woodcut hatching following material direction, restrained flat painted washes, muted gray olive and dark brown, the emerald is the sole vivid accent. Should feel like a dark whimsical handmade storybook strategy-game shop, not glossy realistic PBR, not clean vector. No text, no arrows, no labels, no watermarks, no decorative border, no interface widgets. High quality detailed landscape image.
```

### wood-ink-albedo-v01.png

```text
Use case: stylized-concept. Asset type: original square 1:1 diffuse/albedo surface texture for wooden 3D beams in a handcrafted dark fantasy game. Fill the complete image edge to edge with ONE continuous flat wood surface viewed precisely face-on, no perspective and no represented object. Grain runs generally horizontally across the texture, with natural undulating drift, fine long charcoal ink fibers, intermittent tapering dark grooves and several sparse small uneven knots, line density varying in rhythm rather than regular stripes. Woodcut engraving and hand-drawn scratchboard ink detail, narrow ink lines with occasional thicker cracks, subtle low-frequency painted variation underneath. Palette very muted gray olive, aged dark gray-brown and charcoal; middle value reasonably readable so it can be shaded in a 3D engine. Matte diffuse color only, uniform illumination, no cast shadows, no highlights, no bevel shading, no ambient occlusion along edges. Absolutely no plank separations, no plank borders, no frame, no boards viewed in perspective, no furniture, no leaves, no symbols, no writing or watermark. Avoid golden yellow, orange wood stain, bright tan, highly regular black zebra stripes, photorealistic photographic noise, or heavy black scribbles. Intricate but understated ink drawing suitable for repeated use on small medieval wooden cabinet trim.
```

### map-paper-albedo-v01.png

```text
Use case: stylized-concept. Asset type: original landscape 3:2 flat diffuse texture for a physical parchment map prop in a dark hand-inked fantasy strategy game. Image is precisely front-facing flat paper, filling canvas to all four edges, no perspective or object mockup. A muted gray-ivory aged parchment surface with restrained subtle fibers and occasional faint irregular age speckles. Sparse tiny engraved mountains, hilly contours and groups of pointed conifer trees appear mainly along the lower left and lower right edges and a little along side edges, hand-drawn in low-contrast gray ink with irregular woodcut hatching. Keep the CENTRAL 65 percent and TOP 25 percent almost empty parchment so an actual 3D tower and Chinese interface text can be overlaid clearly. This is quiet map backing, not a complete illustrated world. No route lines, no dotted paths, no nodes or circular marks, no buildings, no tower, no compass rose, no labels, no letters, no numbers, no icons, no UI border, no cast shadows. Paper is gray beige rather than bright yellow, even diffuse illumination, subtle age patina and handcrafted fine charcoal linework. No watermarks. High quality detailed landscape image.
```

## 追踪

[manifest.json](manifest.json) 记录每份原图路径、尺寸、字节数、SHA-256、用途与上述原始提示词。建模参考板不应作为整页图片覆盖游戏画面；地图上的模型和中文界面仍应由可编辑模型与 Godot UI 分开呈现。

# 地图桌面整体效果图 v02 提示词

2026-09-13。内置 image_gen.imagegen。输入为用户新截图，任务是以其右侧地图桌面为风格参考重新构图；输出为整体美术概念图，非实机。用户明确要求整体确认后才制作组件单图。

## 输入

- `references/flask-map-user-reference-2026-09-13.png`：style/composition reference，重点阅读右侧地图、纸上棋子和桌边物件；左侧柜体及原作 UI 不进入本轮画面。

## 完整提示词

```text
Use case: style-transfer / stylized-concept.
Transform the RIGHT-HAND MAP DESK area of the supplied game screenshot into a standalone, beautifully finished overall visual-design concept for a new fantasy game's map interface. Recompose it as ONE SQUARE 1:1 image entirely devoted to the map desk, viewed from the player's seated position looking down at an inclined tabletop. Do not include the left inventory cabinet. The provided screenshot is a close style/composition reference: deeply emulate its dense irregular black ink outlines, fine woodcut crosshatching, slightly warped hand-drawn forms, subdued grey-olive palette, pale greenish parchment, dark planked surroundings, whimsical slightly sinister mood, and the clear distinction between painted scenery and physical miniature props. Preserve the reference's richly drawn game-illustration look, not a glossy 3D render, not a clean board-game infographic, not watercolor concept art, not a blank parchment with a few icons.

COMPOSITION AND SPATIAL LAYERS:
The map is a large slightly irregular canvas laid onto a worn dark timber desk. Map fills roughly 75 percent of the picture; lower edge is near the viewer, far edge recedes toward a narrow dark wooden back ledge. The illustrated map should remain readable between all the props. Desk and room timber edges form an organic enclosing frame; no huge empty header or card UI.

MAP BASE, PHYSICALLY FLAT PAINTED ENVIRONMENT:
Draw an intricate contiguous medieval-fantasy town and surrounding country directly onto the pale grey-olive map: many small ink-drawn crooked houses, little towers, roof tiles, narrow alleys, winding dirt lanes, masonry walls, rock outcrops, sparse trees and grass, tiny bridges. Ink-hatched, varied little roofs in desaturated slate blue, muted ochre and dusty red. These environmental buildings are ILLUSTRATIONS ON THE FLAT CANVAS, with almost no real extrusion or cast shadows: they must not become a landscape diorama full of 3D buildings. Avoid a giant empty middle, ornamental-only mountain borders, contour-map minimalism and grids. Use open pale lanes to support route readability through the rich detail. A hand-painted vermilion RED DASHED ROUTE lies on the canvas, clearly distinct from the fine grey roads: starts at the mage's current-position ring in the lower central area and branches through clear pale lanes toward the campfire, crystal ball and a place marker farther back. Keep the red route visible rather than hiding it under roofs. This is illustrative route layout, not a labeled flowchart. Very few faint ink endpoint rings, no text labels, no numerical rules.

FOUR MAIN PHYSICAL PROPS STANDING ON THE MAP, EACH EXACTLY ONCE:
1. PLAYER MAGE WOODCARVING in the lower central-left area, at about x=40%, y=72% of the full image. A small unmistakably carved wooden wizard pawn with a tall bent pointed hat, cloaked shoulders, tiny staff and visible carved beard and knife cuts. Entire figure is stained dark umber wood, slightly imperfect, on a simple small integral wooden foot. It is a WOODEN FIGURINE, not a living mage, not a painted token card. A small red position ring remains visible around its feet. Readable silhouette; contact shadow anchors it to the canvas.
2. REST CAMPFIRE at about x=28%, y=46%. A miniature ring of rough stones, crossed little logs and restrained warm orange flames, with a physical low-profile base and clear contact shadow. Rest is represented by this object alone; do not add a tent, bed, sign, label or character.
3. QUESTION-EVENT CRYSTAL BALL at about x=69%, y=47%. One cloudy subdued blue-green glass orb on a dark carved wooden/aged brass three-footed stand, with a single pale question-mark-shaped curl in its mist. Small restrained highlights and visible ink outline; NOT neon, not a huge glowing portal. It must be distinct from the mage and readable against the illustrated buildings behind it.
4. PLACE MARKER near the upper middle at about x=49%, y=30%. One simple, stout freestanding wooden house/watchtower miniature with crooked slate roof, narrow doorway, visible shallow side face, rough cut details and small wooden plinth. This single solid location piece should be slightly larger and simpler than the drawn buildings around it, with an obvious contact shadow so it reads as a tabletop object. Do not add additional freestanding building pawns.

THREE PERIPHERAL DESK OBJECT GROUPS, OUTSIDE THE MAP'S PLAY AREA:
- UPPER RIGHT: one large curled shaggy charcoal-grey cat with slightly lavender-grey fur, wary sleepy eyes and tail wrapped along the rear desk edge. Dense hand-inked fur texture and irregular silhouette, body sitting on the exposed timber beyond the map's top-right border; no collar symbols or gameplay badge. Do not obstruct the crystal ball or the route.
- LOWER RIGHT: one sturdy old wood-and-black-iron treasure chest at the near desk corner, partially open so several dull gold coins can be seen inside. Chest signifies the gold resource. The chest overlaps the outside corner of the map just slightly, but sits on exposed timber and leaves the route clear. Chunky iron straps, lock plate and carved grain. No currency number or text.
- LOWER LEFT: a small group of three old closed books with worn dark green, burgundy and brown covers, two stacked and one leaning against them, frayed pale page edges and subtle cover embossing. Books rest outside the map on the near timber ledge; do not cover the mage or routes. No readable title text.

FINISH:
Use nuanced line-weight hierarchy: fine dense environmental ink; stronger irregular contours and contact shadows on the four raised props; dense scratched wood and fur at the edges. Moderate fixed perspective, compact screen-space composition, objects visually nestled in the illustrated setting. Keep the pale map high enough in value to carry the red route and dark wooden mage, but avoid yellow sepia. Limited accent colors: route vermilion, campfire ochre-orange, cloudy green-blue orb, subdued gold coins. The rest is grey olive, charcoal, muted parchment and worn wood. No bright rim lighting, no glossy PBR plastic, no photoreal fur, no large bloom, no modern interface boxes. Show the whole map desk in one coherent scene, no split panels, no exploded components, no separate reference sheet.

Exclude screenshot overlays, player name, health icons, bottles, inventory cabinet, television, hourglass, candles, extra characters, numbers, subtitles, logos and watermarks. No text anywhere except the one question-mark-shaped mist inside the orb. Deliver a refined overall art-direction illustration with every requested object clearly present.
```

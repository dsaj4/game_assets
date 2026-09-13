# game-002 Godogen 3D experiment

Current phase: **Right map desk overall concept / user review pending**. Read docs/map-desk-visual-design-v02.md first. User now requests left/right separation, right map desk concept and design manuscript first, individual component images only after overall confirmation. Extra desk clutter is explicitly retained. Do not infer overall approval from this clutter preference or continue modeling/runtime work. E1 R2 remains the latest engine implementation; read docs/e1-r2-report.md for evidence and docs/e1-report.md for the preserved first pass. E1 is not accepted art direction.
On 2026-09-13 the user explicitly requested “开始启动E1”. Implement and verify only the E1 style specimen in docs/experiment-plan-v01.md. E2 loadout interaction, E3 route interaction and E4 integration remain deferred. Do not start recurring tasks or import existing gameplay implementations. Concept images are not engine evidence or accepted gameplay.

This independent workspace uses the Godogen Godot/Codex workflow with a native Blender/Python asset path. Read README.md, docs/design-context.md, docs/deferred-ui-experiment.md and godot.md before development. See docs/godogen-adaptation.md for upstream provenance and local overrides.

- Maintain durable status and asset provenance in README.md.
- Runtime: Godot .NET + C#. All Godot C# classes are partial; scenes are emitted by build-time C# SceneTree builders and checked after packing.
- Assets: native Blender UI through the computer-use plugin and its bundled bpy Python, reproducible source scripts, .blend masters, exported GLB/PNG. On 2026-09-13 the user explicitly authorized image-model references/assets and native Blender UI refinement of this page. Generated originals and prompts live in references/e1-r2-generated; the modeling board is reference only, wood and map images are albedo textures on geometry. No Blender MCP is used.
- R2 input is art/e1/e1-r2-ui.blend, preserving the actual UI roof edit; tools/build-e1-r2.ps1 refines it. art/build_e1.py and e1-style-master.blend remain the R1 sources; do not run the R1 generator to rebuild R2. Keep evidence/E1 unchanged and store new captures under evidence/E1-r2.
- tools/env.ps1 configures only the current process. tools/check-environment.ps1 checks tools and an empty fixture, not gameplay or visual similarity.
- Keep final runtime assets and generation sources in Git. Keep third-party references outside game/.
- vendor/godogen is an inactive upstream source checkout; its instructions and cloud tools are reference material, not workspace authority. Do not execute publish.sh --force.
- Design input is the frozen game-002 snapshot in references/design. Respect Accepted, Qualified, Candidate and Raw distinctions; this experiment does not promote any design status.
- Once UI work is resumed, validate the actual running result and inspect captures. A successful build alone never proves visual quality, interaction quality or similarity.
- User controls scope and timing. Upstream automatic game/video production suggestions do not override the explicit pause.

Use branch codex/* in this independent local repository. Do not change the design repository's core concept as a side effect of implementation.

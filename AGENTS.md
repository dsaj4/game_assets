# game-002 Godogen 3D experiment

Current phase: **E1 executed / technical checks passed / style NeedsRevision**. Read docs/e1-report.md for real captures and remaining gaps; E1 is not accepted art direction.
On 2026-09-13 the user explicitly requested “开始启动E1”. Implement and verify only the E1 style specimen in docs/experiment-plan-v01.md. E2 loadout interaction, E3 route interaction and E4 integration remain deferred. Do not start recurring tasks or import existing gameplay implementations. Concept images are not engine evidence or accepted gameplay.

This independent workspace uses the Godogen Godot/Codex workflow with a native Blender/Python asset path. Read README.md, docs/design-context.md, docs/deferred-ui-experiment.md and godot.md before development. See docs/godogen-adaptation.md for upstream provenance and local overrides.

- Maintain durable status and asset provenance in README.md.
- Runtime: Godot .NET + C#. All Godot C# classes are partial; scenes are emitted by build-time C# SceneTree builders and checked after packing.
- Assets: native Blender and its bundled bpy Python, reproducible source scripts, .blend masters, exported GLB/PNG. Follow docs/native-assets.md. No Blender MCP or cloud asset-generation skill is enabled for this experiment.
- tools/env.ps1 configures only the current process. tools/check-environment.ps1 checks tools and an empty fixture, not gameplay or visual similarity.
- Keep final runtime assets and generation sources in Git. Keep third-party references outside game/.
- vendor/godogen is an inactive upstream source checkout; its instructions and cloud tools are reference material, not workspace authority. Do not execute publish.sh --force.
- Design input is the frozen game-002 snapshot in references/design. Respect Accepted, Qualified, Candidate and Raw distinctions; this experiment does not promote any design status.
- Once UI work is resumed, validate the actual running result and inspect captures. A successful build alone never proves visual quality, interaction quality or similarity.
- User controls scope and timing. Upstream automatic game/video production suggestions do not override the explicit pause.

Use branch codex/* in this independent local repository. Do not change the design repository's core concept as a side effect of implementation.

"""Capture the explicitly selected design revision without touching its checkout."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
source = Path("E:/Project/game")
commit = "305044d6d25783e914ff6d7265ed9d724684a989"
prefix = "workspaces/game-002/"
files = [
    "README.md", "CONTEXT.md",
    "game-design-workflow/core-concept.md",
    "game-design-workflow/decision-log.md",
    "docs/design-decisions-needed.md", "docs/code-development-index.md",
    "docs/battlefield-and-environment.md",
    "game-design-workflow/idea-materials/M-2026-09-12-wand-inlay-system.md",
    "game-design-workflow/idea-materials/M-2026-09-06-branching-run-routes.md",
    "game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md",
    "game-design-workflow/idea-materials/M-2026-09-13-element-short-rule-card-pool.md",
    "game-design-workflow/idea-inbox/2026-09-13-simple-spell-short-rule-card-pool.md",
]
records = []
for name in files:
    content = subprocess.run(["git", "-C", str(source), "show", f"{commit}:{prefix}{name}"], check=True, capture_output=True).stdout
    dest = root / "references/design" / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    records.append({"source_path": prefix + name, "snapshot": name, "sha256": hashlib.sha256(content).hexdigest()})
(root / "references/design/manifest.json").write_text(json.dumps({
    "source_repository": str(source), "commit": commit, "files": records,
    "note": "Read-only snapshot. Original relative links may refer to unsnapshotted material; consult source repository. No inherited AGENTS or executable content.",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Captured {len(records)} design documents at {commit}")

from __future__ import annotations

from pathlib import Path
import json
import sys
import tempfile

import addon_utils
import bpy


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> None:
    addon_utils.enable("blender_auto_backup", default_set=False, persistent=False)

    with tempfile.TemporaryDirectory() as temp_root:
        root = Path(temp_root)
        source = root / "work"
        source.mkdir()
        (source / "scene.blend").write_bytes(b"blend")
        (source / "notes.txt").write_text("runtime gate", encoding="utf-8")
        backup_dir = root / "backups"

        settings = bpy.context.scene.blender_auto_backup
        settings.source_directory = str(source)
        settings.backup_directory = str(backup_dir)
        settings.interval_minutes = 1
        settings.max_backups = 5
        settings.use_background_worker = False

        result = bpy.ops.blender_auto_backup.run_now()
        if result != {"FINISHED"}:
            raise SystemExit(f"operator did not finish: {result}")

        archives = sorted(backup_dir.glob("*.zip"))
        if len(archives) != 1:
            raise SystemExit(f"expected one backup zip, found {len(archives)}")

        payload = {
            "status": "passed",
            "archive": str(archives[0]),
            "blender_version": bpy.app.version_string,
            "operator_result": sorted(result),
        }
        print("BLENDER_AUTO_BACKUP_RUNTIME_GATE=" + json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
DIST = ROOT / "dist"
PACKAGE_NAME = f"blender-auto-backup-{VERSION}.zip"


def main() -> None:
    DIST.mkdir(exist_ok=True)
    archive_path = DIST / PACKAGE_NAME
    if archive_path.exists():
        archive_path.unlink()

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(ROOT / "blender_manifest.toml", "blender_manifest.toml")
        for source in sorted((ROOT / "blender_auto_backup").rglob("*")):
            if source.is_dir() or "__pycache__" in source.parts:
                continue
            archive.write(source, source.relative_to(ROOT / "blender_auto_backup").as_posix())
        archive.write(ROOT / "LICENSE", "LICENSE")

    latest = DIST / "blender-auto-backup-latest.zip"
    if latest.exists():
        latest.unlink()
    shutil.copy2(archive_path, latest)
    print(archive_path)


if __name__ == "__main__":
    main()

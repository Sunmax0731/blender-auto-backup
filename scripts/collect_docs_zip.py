from __future__ import annotations

from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
DIST = ROOT / "dist"

DOC_FILES = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "TODO.md",
    "docs/installation-guide.md",
    "docs/manual-test.md",
    "docs/specification.md",
    "docs/architecture.md",
    "docs/test-plan.md",
    "docs/qcds-evaluation.md",
    "docs/qcds-strict-metrics.json",
    "docs/release-checklist.md",
]


def main() -> None:
    DIST.mkdir(exist_ok=True)
    archive_path = DIST / f"blender-auto-backup-docs-{VERSION}.zip"
    if archive_path.exists():
        archive_path.unlink()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in DOC_FILES:
            path = ROOT / relative
            if not path.exists():
                raise FileNotFoundError(path)
            archive.write(path, relative)
    print(archive_path)


if __name__ == "__main__":
    main()


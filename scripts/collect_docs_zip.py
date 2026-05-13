from __future__ import annotations

from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.1"
DIST = ROOT / "dist"

DOC_FILES = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "TODO.md",
    "docs/installation-guide.md",
    "docs/user-guide.md",
    "docs/manual-test.md",
    "docs/specification.md",
    "docs/architecture.md",
    "docs/backlog-triage.md",
    "docs/test-plan.md",
    "docs/qcds-evaluation.md",
    "docs/qcds-strict-metrics.json",
    "docs/release-checklist.md",
    "docs/release-evidence.json",
    "docs/releases/v0.1.0.md",
    "docs/releases/v0.1.1.md",
]


def iter_doc_files() -> list[str]:
    files = list(DOC_FILES)
    img_dir = ROOT / "docs" / "img"
    if img_dir.exists():
        files.extend(
            path.relative_to(ROOT).as_posix()
            for path in sorted(img_dir.glob("*.png"))
        )
    issues_dir = ROOT / "Issues"
    if issues_dir.exists():
        files.extend(
            path.relative_to(ROOT).as_posix()
            for path in sorted(issues_dir.glob("*.md"))
        )
    return files


def main() -> None:
    DIST.mkdir(exist_ok=True)
    archive_path = DIST / f"blender-auto-backup-docs-{VERSION}.zip"
    if archive_path.exists():
        archive_path.unlink()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in iter_doc_files():
            path = ROOT / relative
            if not path.exists():
                raise FileNotFoundError(path)
            archive.write(path, relative)
    print(archive_path)


if __name__ == "__main__":
    main()

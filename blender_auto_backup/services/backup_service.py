"""Pure Python backup service used by Blender operators and tests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os
import re
import zipfile


class BackupError(RuntimeError):
    """Raised when a backup cannot be created from user-supplied settings."""


@dataclass(frozen=True)
class BackupResult:
    archive_path: Path
    file_count: int
    byte_count: int
    created_at: datetime
    deleted_archives: tuple[Path, ...]


def run_backup(
    *,
    source_directory: str | os.PathLike[str],
    backup_directory: str | os.PathLike[str] | None = None,
    max_backups: int = 20,
    project_label: str | None = None,
    created_at: datetime | None = None,
) -> BackupResult:
    """Create a ZIP backup and remove older backups beyond max_backups."""

    source = _resolve_source(source_directory)
    backup_dir = _resolve_backup_dir(source, backup_directory)
    keep = _validate_keep_count(max_backups)
    timestamp = created_at or datetime.now()
    label = _safe_label(project_label or source.name or "project")

    backup_dir.mkdir(parents=True, exist_ok=True)
    archive_path = _unique_archive_path(backup_dir, label, timestamp)
    partial_path = archive_path.with_suffix(archive_path.suffix + ".partial")

    file_count = 0
    byte_count = 0
    try:
        with zipfile.ZipFile(partial_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in _iter_source_files(source, backup_dir):
                relative = file_path.relative_to(source)
                archive_name = Path(source.name) / relative
                archive.write(file_path, archive_name.as_posix())
                file_count += 1
                byte_count += file_path.stat().st_size
        if file_count == 0:
            raise BackupError(f"source folder has no files to back up: {source}")
        os.replace(partial_path, archive_path)
    except Exception:
        if partial_path.exists():
            partial_path.unlink()
        raise

    deleted = cleanup_old_backups(backup_dir=backup_dir, label=label, keep=keep)
    return BackupResult(
        archive_path=archive_path,
        file_count=file_count,
        byte_count=byte_count,
        created_at=timestamp,
        deleted_archives=tuple(deleted),
    )


def cleanup_old_backups(
    *,
    backup_dir: str | os.PathLike[str],
    label: str,
    keep: int,
) -> list[Path]:
    """Keep the newest backup ZIP files for label and delete older files."""

    folder = Path(backup_dir).resolve()
    if not folder.exists():
        return []
    safe_label = _safe_label(label)
    archives = sorted(
        folder.glob(f"{safe_label}-*.zip"),
        key=lambda path: (path.stat().st_mtime, path.name),
        reverse=True,
    )
    deleted: list[Path] = []
    for archive in archives[keep:]:
        archive.unlink()
        deleted.append(archive)
    return deleted


def _resolve_source(source_directory: str | os.PathLike[str]) -> Path:
    if not source_directory:
        raise BackupError("source folder is required")
    source = Path(source_directory).expanduser().resolve()
    if not source.exists():
        raise BackupError(f"source folder does not exist: {source}")
    if not source.is_dir():
        raise BackupError(f"source path is not a folder: {source}")
    return source


def _resolve_backup_dir(
    source: Path,
    backup_directory: str | os.PathLike[str] | None,
) -> Path:
    backup_dir = (
        Path(backup_directory).expanduser().resolve()
        if backup_directory
        else source / ".blender-auto-backup"
    )
    if backup_dir == source:
        raise BackupError("backup folder must not be the same as source folder")
    return backup_dir


def _validate_keep_count(max_backups: int) -> int:
    try:
        keep = int(max_backups)
    except (TypeError, ValueError) as exc:
        raise BackupError("max backups must be a positive integer") from exc
    if keep < 1:
        raise BackupError("max backups must be at least 1")
    return keep


def _iter_source_files(source: Path, backup_dir: Path):
    resolved_backup = backup_dir.resolve()
    for path in sorted(source.rglob("*")):
        if path.is_dir():
            continue
        resolved = path.resolve()
        if _is_relative_to(resolved, resolved_backup):
            continue
        yield path


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _safe_label(value: str) -> str:
    label = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    label = label.strip(".-_")
    return label or "project"


def _unique_archive_path(backup_dir: Path, label: str, timestamp: datetime) -> Path:
    base = f"{label}-{timestamp.strftime('%Y%m%d-%H%M%S')}"
    candidate = backup_dir / f"{base}.zip"
    suffix = 1
    while candidate.exists() or candidate.with_suffix(candidate.suffix + ".partial").exists():
        candidate = backup_dir / f"{base}-{suffix:02d}.zip"
        suffix += 1
    return candidate


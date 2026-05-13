from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import unittest
import zipfile

from blender_auto_backup.services.backup_service import BackupError, run_backup


class BackupServiceTests(unittest.TestCase):
    def test_run_backup_creates_zip_and_excludes_backup_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            source = root / "work"
            source.mkdir()
            (source / "scene.blend").write_bytes(b"blend")
            nested = source / "textures"
            nested.mkdir()
            (nested / "albedo.png").write_bytes(b"png")
            backup_dir = source / ".blender-auto-backup"
            backup_dir.mkdir()
            (backup_dir / "old.zip").write_bytes(b"old")

            result = run_backup(
                source_directory=source,
                backup_directory=backup_dir,
                created_at=datetime(2026, 5, 14, 12, 0, 0),
            )

            self.assertTrue(result.archive_path.exists())
            self.assertEqual(result.file_count, 2)
            with zipfile.ZipFile(result.archive_path) as archive:
                names = set(archive.namelist())
            self.assertIn("work/scene.blend", names)
            self.assertIn("work/textures/albedo.png", names)
            self.assertNotIn("work/.blender-auto-backup/old.zip", names)
            self.assertFalse(list(backup_dir.glob("*.partial")))

    def test_run_backup_keeps_newest_archives(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            source = root / "work"
            source.mkdir()
            (source / "scene.blend").write_bytes(b"blend")
            backup_dir = root / "backups"

            for index in range(4):
                run_backup(
                    source_directory=source,
                    backup_directory=backup_dir,
                    max_backups=2,
                    project_label="sample",
                    created_at=datetime(2026, 5, 14, 12, 0, 0) + timedelta(seconds=index),
                )

            archives = sorted(path.name for path in backup_dir.glob("sample-*.zip"))
            self.assertEqual(len(archives), 2)
            self.assertEqual(
                archives,
                [
                    "sample-20260514-120002.zip",
                    "sample-20260514-120003.zip",
                ],
            )

    def test_run_backup_rejects_missing_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            missing = Path(temp_root) / "missing"
            with self.assertRaises(BackupError):
                run_backup(source_directory=missing)

    def test_run_backup_rejects_same_source_and_backup_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            source = Path(temp_root)
            (source / "scene.blend").write_bytes(b"blend")
            with self.assertRaises(BackupError):
                run_backup(source_directory=source, backup_directory=source)


if __name__ == "__main__":
    unittest.main()


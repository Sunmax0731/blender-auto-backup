"""Blender operators for manual and scheduled backup control."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os
import subprocess
import sys

import bpy

from . import scheduler
from .services.backup_service import BackupError, run_backup


def _settings(context: bpy.types.Context):
    return context.scene.blender_auto_backup


def _abspath(path_value: str) -> str:
    if not path_value:
        return ""
    return bpy.path.abspath(path_value)


def _status_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def perform_backup_for_settings(settings) -> str:
    source_directory = _abspath(settings.source_directory)
    backup_directory = _abspath(settings.backup_directory) if settings.backup_directory else None
    result = run_backup(
        source_directory=source_directory,
        backup_directory=backup_directory,
        max_backups=settings.max_backups,
        project_label=settings.backup_label or None,
    )
    settings.last_backup_path = str(result.archive_path)
    settings.last_run_at = _status_time()
    settings.last_status = (
        f"OK: {result.file_count} files, {result.byte_count} bytes -> "
        f"{result.archive_path.name}"
    )
    return settings.last_status


class BLENDER_AUTO_BACKUP_OT_run_now(bpy.types.Operator):
    bl_idname = "blender_auto_backup.run_now"
    bl_label = "Backup Now"
    bl_description = "Create a backup ZIP immediately"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = _settings(context)
        try:
            message = perform_backup_for_settings(settings)
        except BackupError as exc:
            settings.last_run_at = _status_time()
            settings.last_status = f"Error: {exc}"
            self.report({"ERROR"}, settings.last_status)
            return {"CANCELLED"}
        self.report({"INFO"}, message)
        return {"FINISHED"}


class BLENDER_AUTO_BACKUP_OT_start(bpy.types.Operator):
    bl_idname = "blender_auto_backup.start"
    bl_label = "Start Auto Backup"
    bl_description = "Start the automatic backup timer"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = _settings(context)
        try:
            source = Path(_abspath(settings.source_directory)).resolve()
        except OSError as exc:
            settings.last_status = f"Error: invalid source folder: {exc}"
            self.report({"ERROR"}, settings.last_status)
            return {"CANCELLED"}
        if not source.is_dir():
            settings.last_status = f"Error: source folder does not exist: {source}"
            self.report({"ERROR"}, settings.last_status)
            return {"CANCELLED"}

        settings.enabled = True
        scheduler.start_for_settings(settings)
        settings.last_status = "Auto backup timer started"
        self.report({"INFO"}, settings.last_status)
        return {"FINISHED"}


class BLENDER_AUTO_BACKUP_OT_stop(bpy.types.Operator):
    bl_idname = "blender_auto_backup.stop"
    bl_label = "Stop Auto Backup"
    bl_description = "Stop automatic backups for the active scene"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = _settings(context)
        settings.enabled = False
        settings.next_run_at = ""
        settings.last_status = "Auto backup timer stopped"
        self.report({"INFO"}, settings.last_status)
        return {"FINISHED"}


class BLENDER_AUTO_BACKUP_OT_open_backup_folder(bpy.types.Operator):
    bl_idname = "blender_auto_backup.open_backup_folder"
    bl_label = "Open Backup Folder"
    bl_description = "Open the configured backup folder"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = _settings(context)
        target = _abspath(settings.backup_directory) if settings.backup_directory else ""
        if not target and settings.last_backup_path:
            target = str(Path(settings.last_backup_path).parent)
        if not target and settings.source_directory:
            target = str(Path(_abspath(settings.source_directory)) / ".blender-auto-backup")
        if not target:
            self.report({"ERROR"}, "Backup folder is not configured yet")
            return {"CANCELLED"}

        folder = Path(target).resolve()
        folder.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(folder))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(folder)])
        else:
            subprocess.Popen(["xdg-open", str(folder)])
        return {"FINISHED"}


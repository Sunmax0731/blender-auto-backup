"""Blender operators for manual and scheduled backup control."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os
import subprocess
import sys

import bpy

from . import scheduler
from .services.backup_service import BackupError, resolve_backup_directory, run_backup

ADDON_ID = __package__ or "blender_auto_backup"


def _settings(context: bpy.types.Context):
    return context.scene.blender_auto_backup


def _abspath(path_value: str) -> str:
    if not path_value:
        return ""
    return bpy.path.abspath(path_value)


def _status_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _addon_preferences():
    addon = bpy.context.preferences.addons.get(ADDON_ID)
    return addon.preferences if addon else None


def _configured_backup_directory(settings) -> str | None:
    if settings.backup_directory:
        return _abspath(settings.backup_directory)
    preferences = _addon_preferences()
    default_backup_directory = getattr(preferences, "default_backup_directory", "") if preferences else ""
    return _abspath(default_backup_directory) if default_backup_directory else None


def _destination_mode(settings) -> str:
    return getattr(settings, "backup_destination_mode", "DIRECT")


def _effective_backup_directory(settings) -> str | None:
    source = _abspath(settings.source_directory)
    configured = _configured_backup_directory(settings)
    if not source:
        return configured
    try:
        return str(
            resolve_backup_directory(
                source_directory=source,
                backup_directory=configured,
                project_label=settings.backup_label or None,
                destination_mode=_destination_mode(settings),
            )
        )
    except BackupError:
        return configured


def _backup_kwargs_from_settings(settings) -> dict:
    return {
        "source_directory": _abspath(settings.source_directory),
        "backup_directory": _configured_backup_directory(settings),
        "max_backups": settings.max_backups,
        "project_label": settings.backup_label or None,
        "include_globs": settings.include_globs,
        "exclude_globs": settings.exclude_globs,
        "destination_mode": _destination_mode(settings),
    }


def _success_status(result) -> str:
    return (
        f"OK: {result.file_count} files, {result.byte_count} bytes -> "
        f"{result.archive_path.name}"
    )


def perform_backup_for_settings(settings) -> str:
    result = run_backup(**_backup_kwargs_from_settings(settings))
    settings.last_backup_path = str(result.archive_path)
    settings.last_run_at = _status_time()
    settings.last_status = _success_status(result)
    return settings.last_status


def start_background_backup_for_settings(settings) -> tuple[bool, str]:
    started = scheduler.start_background_backup(**_backup_kwargs_from_settings(settings))
    if not started:
        settings.last_status = "Backup already running in background"
        return False, settings.last_status
    settings.last_status = "Backup running in background"
    return True, settings.last_status


class BLENDER_AUTO_BACKUP_OT_run_now(bpy.types.Operator):
    bl_idname = "blender_auto_backup.run_now"
    bl_label = "Backup Now"
    bl_description = "Create a backup ZIP immediately"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = _settings(context)
        if settings.use_background_worker:
            started, message = start_background_backup_for_settings(settings)
            self.report({"INFO" if started else "WARNING"}, message)
            return {"FINISHED"} if started else {"CANCELLED"}
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
        target = _effective_backup_directory(settings) or ""
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

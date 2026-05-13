"""Scene properties for Blender Auto Backup."""

from __future__ import annotations

import bpy


class BlenderAutoBackupSettings(bpy.types.PropertyGroup):
    source_directory: bpy.props.StringProperty(
        name="Source Folder",
        description="Folder to back up",
        subtype="DIR_PATH",
        default="",
    )
    backup_directory: bpy.props.StringProperty(
        name="Backup Folder",
        description="Folder where backup ZIP files are stored. Empty uses .blender-auto-backup inside Source Folder.",
        subtype="DIR_PATH",
        default="",
    )
    backup_label: bpy.props.StringProperty(
        name="Backup Label",
        description="Optional file-name label. Empty uses the source folder name.",
        default="",
    )
    interval_minutes: bpy.props.IntProperty(
        name="Interval Minutes",
        description="Minutes between automatic backups",
        default=15,
        min=1,
        max=1440,
    )
    max_backups: bpy.props.IntProperty(
        name="Max Backups",
        description="Number of backup ZIP files to keep for this source",
        default=20,
        min=1,
        max=999,
    )
    enabled: bpy.props.BoolProperty(
        name="Auto Backup Enabled",
        description="Whether the timer should create backups for the active scene",
        default=False,
    )
    last_status: bpy.props.StringProperty(
        name="Last Status",
        default="Not started",
    )
    last_backup_path: bpy.props.StringProperty(
        name="Last Backup Path",
        subtype="FILE_PATH",
        default="",
    )
    last_run_at: bpy.props.StringProperty(
        name="Last Run At",
        default="",
    )
    next_run_at: bpy.props.StringProperty(
        name="Next Run At",
        default="",
    )


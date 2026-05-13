"""Scene properties for Blender Auto Backup."""

from __future__ import annotations

import bpy

ADDON_ID = __package__ or "blender_auto_backup"


class BlenderAutoBackupPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    default_backup_directory: bpy.props.StringProperty(
        name="Default Backup Folder",
        description="Global backup folder used when a scene Backup Folder is empty",
        subtype="DIR_PATH",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_backup_directory")


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
    backup_destination_mode: bpy.props.EnumProperty(
        name="Destination Layout",
        description="Choose whether ZIP files are saved directly in Backup Folder or inside a project subfolder",
        items=(
            ("DIRECT", "Direct", "Save ZIP files directly in Backup Folder"),
            ("SUBFOLDER", "Subfolder", "Create a project subfolder in Backup Folder and save ZIP files there"),
        ),
        default="DIRECT",
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
    use_background_worker: bpy.props.BoolProperty(
        name="Run in Background",
        description="Run backup ZIP creation on a worker thread and update the panel when it finishes",
        default=False,
    )
    include_globs: bpy.props.StringProperty(
        name="Include Globs",
        description="Optional semicolon or newline separated globs. Empty includes all files.",
        default="",
    )
    exclude_globs: bpy.props.StringProperty(
        name="Exclude Globs",
        description="Optional semicolon or newline separated globs. Excludes take precedence.",
        default="",
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

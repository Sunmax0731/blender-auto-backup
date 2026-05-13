"""Blender UI panels."""

from __future__ import annotations

import bpy


class BLENDER_AUTO_BACKUP_PT_scene_panel(bpy.types.Panel):
    bl_label = "Auto Backup"
    bl_idname = "BLENDER_AUTO_BACKUP_PT_scene_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.blender_auto_backup

        layout.prop(settings, "source_directory")
        layout.prop(settings, "backup_directory")
        layout.prop(settings, "backup_label")

        row = layout.row(align=True)
        row.prop(settings, "interval_minutes")
        row.prop(settings, "max_backups")

        row = layout.row(align=True)
        row.operator("blender_auto_backup.run_now", icon="FILE_TICK")
        if settings.enabled:
            row.operator("blender_auto_backup.stop", icon="PAUSE")
        else:
            row.operator("blender_auto_backup.start", icon="PLAY")

        layout.operator("blender_auto_backup.open_backup_folder", icon="FILE_FOLDER")

        box = layout.box()
        box.label(text=f"Enabled: {'Yes' if settings.enabled else 'No'}")
        box.label(text=f"Last: {settings.last_status}")
        if settings.last_run_at:
            box.label(text=f"Last Run: {settings.last_run_at}")
        if settings.next_run_at:
            box.label(text=f"Next Run: {settings.next_run_at}")


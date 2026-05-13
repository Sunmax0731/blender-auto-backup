"""Blender Auto Backup add-on."""

from __future__ import annotations

bl_info = {
    "name": "Blender Auto Backup",
    "author": "Sunmax0731",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "Scene Properties > Auto Backup",
    "description": "Back up a selected working folder on a configured interval.",
    "category": "System",
}

try:
    import bpy
except ModuleNotFoundError:  # Allows service-layer tests outside Blender.
    bpy = None


def _load_classes():
    from . import operators, panels, properties

    return (
        properties.BlenderAutoBackupPreferences,
        properties.BlenderAutoBackupSettings,
        operators.BLENDER_AUTO_BACKUP_OT_preview,
        operators.BLENDER_AUTO_BACKUP_OT_run_now,
        operators.BLENDER_AUTO_BACKUP_OT_start,
        operators.BLENDER_AUTO_BACKUP_OT_stop,
        operators.BLENDER_AUTO_BACKUP_OT_open_backup_folder,
        panels.BLENDER_AUTO_BACKUP_PT_scene_panel,
    )


def register() -> None:
    if bpy is None:
        raise RuntimeError("Blender Python API is required to register this add-on")
    from . import properties, scheduler

    for cls in _load_classes():
        bpy.utils.register_class(cls)
    bpy.types.Scene.blender_auto_backup = bpy.props.PointerProperty(
        type=properties.BlenderAutoBackupSettings
    )
    scheduler.ensure_timer()


def unregister() -> None:
    if bpy is None:
        return
    from . import scheduler

    scheduler.disable_timer()
    if hasattr(bpy.types.Scene, "blender_auto_backup"):
        del bpy.types.Scene.blender_auto_backup
    for cls in reversed(_load_classes()):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

# 0004 Global Default Backup Location

- Priority: P3
- Status: done
- Linked TODO: [TODO.md](../TODO.md)

## Contract

Add add-on preferences for a global default backup location used when a scene-specific backup folder is empty.

## Checklist

- [x] Add add-on preferences with a folder path.
- [x] Use the preference when `Backup Folder` is empty.
- [x] Keep the existing `.blender-auto-backup` fallback when no global default is set.
- [x] Reflect the effective location in the UI.
- [x] Update docs and QCDS evidence.

## Evidence

- Implementation: `blender_auto_backup/properties.py`, `blender_auto_backup/operators.py`, `blender_auto_backup/panels.py`, `blender_auto_backup/__init__.py`.
- Docs: `README.md`, `docs/specification.md`, `docs/manual-test.md`, `docs/qcds-evaluation.md`.
- Validation: `npm test` completed with compile, package, QCDS, text integrity, and unittest steps passing. Blender runtime validation remains tracked by Issue 0001.

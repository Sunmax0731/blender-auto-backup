# SKILL

description: Build, verify, package, and release the Blender Auto Backup add-on under `D:\AI\BlenderAddon\blender-auto-backup`.

## Workflow

1. Read `README.md`, `AGENTS.md`, `SKILL.md`, then `TODO.md`.
2. Check whether the requested work changes user-facing behavior, packaging, tests, or release evidence.
3. Update `TODO.md` first when a new task is discovered.
4. Keep core backup behavior in `blender_auto_backup/services/backup_service.py`.
5. Keep Blender registration and UI in `__init__.py`, `properties.py`, `operators.py`, `panels.py`, and `scheduler.py`.
6. Run `npm test` before release or push.
7. If Blender is available, confirm `dist/runtime-gate.json` reports `passed`. If it is not available, record `not_run` and keep QCDS Quality/Satisfaction at B+ or lower.

## Commands

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
npm test
npm run runtime:gate
```

Manual Blender 5.1.1 validation is documented in `docs/manual-test.md`.


# 0002 Background Worker Support

- Priority: P3
- Status: done
- Phase: 04-implementation
- Linked TODO: [TODO.md](../TODO.md)

## Contract

Add optional background worker execution so very large backup jobs can run without keeping the Blender UI thread in the ZIP creation path.

## Checklist

- [x] Add a user-facing setting for background execution.
- [x] Run backup work on a Python worker thread using a snapshot of scene settings.
- [x] Apply completed worker results back on the Blender timer thread.
- [x] Prevent duplicate backup jobs while a worker job is active.
- [x] Update docs and tests.

## Evidence

- Implementation: `blender_auto_backup/properties.py`, `blender_auto_backup/operators.py`, `blender_auto_backup/scheduler.py`, `blender_auto_backup/panels.py`.
- Docs: `README.md`, `docs/architecture.md`, `docs/manual-test.md`, `docs/test-plan.md`, `docs/qcds-evaluation.md`.
- Validation: `npm test` completed with compile, package, QCDS, text integrity, and unittest steps passing. Blender runtime validation remains tracked by Issue 0001.

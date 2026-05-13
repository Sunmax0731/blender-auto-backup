# 0003 Include and Exclude Glob Rules

- Priority: P3
- Status: done
- Phase: 04-implementation
- Linked TODO: [TODO.md](../TODO.md)

## Contract

Add optional include and exclude glob rules for selecting which source files are written into the backup ZIP.

## Checklist

- [x] Add service-layer include glob support.
- [x] Add service-layer exclude glob support.
- [x] Make exclude rules take precedence over include rules.
- [x] Expose the rules in Blender settings and UI.
- [x] Add unittest coverage.
- [x] Update docs and QCDS evidence.

## Evidence

- Implementation: `blender_auto_backup/services/backup_service.py`, `blender_auto_backup/properties.py`, `blender_auto_backup/operators.py`, `blender_auto_backup/panels.py`.
- Tests: `tests/test_backup_service.py` covers include globs, exclude precedence, and no-match failures without `.partial` leftovers.
- Validation: `npm test` completed with 6 unittest cases passing.

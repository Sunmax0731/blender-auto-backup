# 0005 Runtime Gate BLENDER_EXE Diagnostics

- Priority: P3
- Status: done
- Phase: 05-test
- Linked TODO: [TODO.md](../TODO.md)

## Contract

When `BLENDER_EXE` is set but the runtime gate still reports `not_run`, the result should show enough evidence to distinguish a missing Blender install from a malformed path. The gate should also tolerate path separators copied as U+00A5 or U+FFE5 in `BLENDER_EXE`.

## Checklist

- [x] Normalize U+00A5 and U+FFE5 path separators in `BLENDER_EXE`.
- [x] Include `env_path`, `env_path_exists`, and checked candidate paths in `dist/runtime-gate.json` when Blender is not found.
- [x] Keep the command exit code 0 for `not_run`.
- [x] Add automated tests for env path normalization and `not_run` payload evidence.
- [x] Update docs and QCDS evidence.

## Evidence

- User screenshot showed `BLENDER_EXE` was set before `npm run runtime:gate`, but the result only said `blender.exe was not found`.
- Implementation: `scripts/run_blender_runtime_gate.py`.
- Tests: `tests/test_runtime_gate.py`.
- Validation: runtime gate diagnostics tests pass and are included in `npm test`.

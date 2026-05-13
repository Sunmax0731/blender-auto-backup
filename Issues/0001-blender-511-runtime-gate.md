# 0001 Blender 5.1.1 Runtime Gate

- Priority: P3
- Status: done
- Phase: 05-test-validation
- Linked TODO: [TODO.md](../TODO.md)

## Contract

Run the Blender runtime gate on a machine where Blender 5.1.1 `blender.exe` is available and confirm the add-on can be enabled and execute a backup through Blender.

## Checklist

- [x] `BLENDER_EXE` points to Blender 5.1.1.
- [x] `npm run runtime:gate` exits with code 0.
- [x] `dist/runtime-gate.json` reports `passed`.
- [x] `docs/qcds-evaluation.md` and `docs/qcds-strict-metrics.json` record the passed gate state.

## Evidence

- `npm run runtime:gate` completed with status `passed`.
- `dist/runtime-gate.json` reports `status: passed`.
- Blender version: `5.1.1`.
- Blender executable: `D:\SteamLibrary\steamapps\common\Blender\blender.exe`.
- Command used:

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
$env:BLENDER_EXE='D:\SteamLibrary\steamapps\common\Blender'
npm run runtime:gate
```

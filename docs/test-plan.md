# Test Plan

## Automated

Command:

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
npm test
```

Expected result:

- unittest passes
- add-on package compile check passes
- add-on ZIP is generated
- docs ZIP is generated
- QCDS JSON validates
- text integrity check passes
- runtime gate is `passed` when Blender is available, or `not_run` when Blender is not available
- when Blender is available, extension package validation runs before the headless operator scenario

## Representative scenarios covered by unittest

- ZIP is created from a source folder
- Nested files are included
- Backup folder inside source folder is excluded
- `.partial` files are not left after success
- Missing source folder fails
- Source and backup folder cannot be identical
- Old archives are removed beyond `Max Backups`

## Manual

Manual Blender 5.1.1 checks are in `docs/manual-test.md`.

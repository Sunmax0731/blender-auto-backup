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
- runtime gate regenerates the add-on ZIP before extension validation

## Representative scenarios covered by unittest

- ZIP is created from a source folder
- Backup Preview counts target files and bytes without creating ZIP, destination folder, or `.partial` files
- Nested files are included
- Backup folder inside source folder is excluded
- Subfolder destination layout writes ZIP files under `Backup Folder/<safe label>`
- Subfolder destination layout excludes the configured backup root when it is inside the source folder
- Backup Preview uses the same subfolder destination exclusion logic as ZIP creation
- Unknown destination layout values fail before ZIP creation
- `.partial` files are not left after success
- Missing source folder fails
- Source and backup folder cannot be identical
- Old archives are removed beyond `Max Backups`
- Include globs restrict the ZIP payload
- Exclude globs take precedence over include globs
- Filter rules that match no files fail without leaving `.partial` files
- Runtime gate accepts `BLENDER_EXE` paths using U+00A5 or U+FFE5 separators
- Runtime gate accepts `BLENDER_EXE` pointing at a folder containing `blender.exe`
- Runtime gate includes the discovered Steam Blender install path in standard candidates
- Runtime gate `not_run` payload includes env path evidence when `BLENDER_EXE` is set but missing

## Compile coverage

`npm test` compiles the add-on package, including Blender-facing preferences, panel, operator, and scheduler modules. Background worker behavior depends on Blender timer polling and is covered by manual Blender 5.1.1 checks and the runtime gate's operator scenario.

## Manual

Manual Blender 5.1.1 checks are in `docs/manual-test.md`.

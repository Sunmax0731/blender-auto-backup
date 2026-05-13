# 0006 Runtime Gate Steam Blender Detection

- Priority: P3
- Status: done
- Linked TODO: [TODO.md](../TODO.md)

## Contract

Runtime gate should find a Steam-installed Blender at `D:\SteamLibrary\steamapps\common\Blender\blender.exe`, and `BLENDER_EXE` should accept either the executable path or the containing directory.

## Checklist

- [x] Add the discovered Steam Blender path to runtime gate candidates.
- [x] Allow `BLENDER_EXE` to point to a directory containing `blender.exe`.
- [x] Add tests for directory-valued `BLENDER_EXE`.
- [x] Update manual test docs.

## Evidence

- User reported Blender directory: `D:\SteamLibrary\steamapps\common\Blender`.
- Local verification found `D:\SteamLibrary\steamapps\common\Blender\blender.exe`.
- `npm run runtime:gate` passed when `BLENDER_EXE` was set to the Steam Blender directory.

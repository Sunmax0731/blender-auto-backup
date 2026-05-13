# Release Checklist

## Release 0.1.0

- [x] README matches current MVP behavior.
- [x] AGENTS.md and SKILL.md describe repo-local workflow.
- [x] Add-on metadata targets Blender 4.2+.
- [x] Core backup service has automated unittest coverage.
- [x] `npm test` command exists.
- [x] Add-on ZIP packaging exists.
- [x] Docs ZIP packaging exists.
- [x] QCDS evaluation exists.
- [x] Strict QCDS metrics JSON exists and validates.
- [x] Manual test guide includes working directory, commands, expected result, and URL status.
- [x] Local Issue backlog exists under `Issues/` and is linked from `TODO.md`.
- [x] Include / exclude glob rules are implemented and covered by unittest.
- [x] Add-on preferences provide a global default backup location.
- [x] Optional background worker support is implemented with timer-thread result application.
- [x] Runtime gate reports detailed `BLENDER_EXE` diagnostics when Blender is not found.
- [x] Runtime gate detects the Steam Blender install path at `D:\SteamLibrary\steamapps\common\Blender`.
- [x] Blender extension manifest passes 5.1.1 validation.
- [x] Blender 5.1.1 runtime gate is passed on a machine with `blender.exe`.
- [x] P2 backlog triage is complete and duplicate local Issues are resolved.

## Publish notes

The initial public GitHub remote is:

`https://github.com/Sunmax0731/blender-auto-backup`

This repo can be treated as MVP-ready. Blender 5.1.1 runtime gate reports `passed`.

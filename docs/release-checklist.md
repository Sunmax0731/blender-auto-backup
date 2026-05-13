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
- [ ] Blender 5.1.1 runtime gate is passed on a machine with `blender.exe`.

## Publish notes

The initial public GitHub remote is:

`https://github.com/Sunmax0731/blender-auto-backup`

This repo can be treated as MVP-ready after Blender 5.1.1 runtime gate reports `passed`.


# TODO

## MVP release contract

- [x] Create repo at `D:\AI\BlenderAddon\blender-auto-backup`.
- [x] Create public GitHub remote and set local `origin`.
- [x] Use one work branch: `codex/blender-auto-backup-mvp`.
- [x] Add repo-local `README.md`, `AGENTS.md`, and `SKILL.md`.
- [x] Implement ZIP backup service with source-folder exclusion for the backup destination.
- [x] Implement Blender 4.2+ add-on registration, settings, panel, manual backup operator, and timer start/stop.
- [x] Add automated unittest coverage for backup creation, cleanup, and validation errors.
- [x] Add package generation for `dist/blender-auto-backup-0.1.0.zip`.
- [x] Add install guide, manual test guide, QCDS, release checklist, and docs ZIP generation.
- [x] Add strict metrics JSON and validator.
- [x] Add text integrity check for mojibake markers and control characters.
- [ ] Run Blender 5.1.1 runtime gate on a machine where `blender.exe` is available.

## Deferred backlog

- [ ] Add background worker support for very large project folders.
- [ ] Add optional include/exclude glob rules.
- [ ] Add add-on preferences for global default backup location.


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
- [x] [P3] Run Blender 5.1.1 runtime gate on a machine where `blender.exe` is available. ([Issue 0001](Issues/0001-blender-511-runtime-gate.md))

## Deferred backlog

- [x] [P3] Detect Steam Blender installs and directory-valued `BLENDER_EXE`. ([Issue 0006](Issues/0006-runtime-gate-steam-blender-detection.md))
- [x] [P3] Fix Blender extension manifest tagline validation failure. ([Issue 0007](Issues/0007-extension-manifest-tagline-validation.md))
- [x] [P3] Improve runtime gate diagnostics when `BLENDER_EXE` is set but not found. ([Issue 0005](Issues/0005-runtime-gate-blender-exe-diagnostics.md))
- [x] [P3] Add background worker support for very large project folders. ([Issue 0002](Issues/0002-background-worker-support.md))
- [x] [P3] Add optional include/exclude glob rules. ([Issue 0003](Issues/0003-include-exclude-glob-rules.md))
- [x] [P3] Add add-on preferences for global default backup location. ([Issue 0004](Issues/0004-global-default-backup-location.md))

## Work Items
- [x] [P2] 未整理課題のフェーズ振り分け [Issue](Issues/0008-issue.md) [QCDS:Cost,Delivery]
- [x] [P2] 未整理課題のフェーズ振り分け（0008 に統合） [Issue](Issues/0009-issue.md) [QCDS:Cost,Delivery]

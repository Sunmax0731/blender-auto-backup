# TODO

This file is the phase TODO source for local Work Items. Keep a `phase=...` token on every TODO line so completed and open items do not fall back to `00-inbox`.

## 00-inbox TODO

No current TODO. New uncategorized work should be moved into one of the phase sections below before it is started.

## 01-requirements TODO

- [x] Create repo at `D:\AI\BlenderAddon\blender-auto-backup`. [phase=01-requirements]
- [x] Create public GitHub remote and set local `origin`. [phase=01-requirements]
- [x] Use one work branch: `codex/blender-auto-backup-mvp`. [phase=01-requirements]
- [x] Add repo-local `README.md`, `AGENTS.md`, and `SKILL.md`. [phase=01-requirements]
- [x] [P2] 未整理課題のフェーズ振り分け [Issue](Issues/0008-issue.md) [phase=01-requirements] [QCDS:Cost,Delivery]
- [x] [P2] 未整理課題のフェーズ振り分け（0008 に統合） [Issue](Issues/0009-issue.md) [phase=01-requirements] [QCDS:Cost,Delivery]

## 02-specification TODO

No current standalone TODO. Specification evidence is maintained in `docs/specification.md`.

## 03-design TODO

No current standalone TODO. Design evidence is maintained in `docs/architecture.md`.

## 04-implementation TODO

- [x] Implement ZIP backup service with source-folder exclusion for the backup destination. [phase=04-implementation]
- [x] Implement Blender 4.2+ add-on registration, settings, panel, manual backup operator, and timer start/stop. [phase=04-implementation]
- [x] [P3] Add background worker support for very large project folders. ([Issue 0002](Issues/0002-background-worker-support.md)) [phase=04-implementation]
- [x] [P3] Add optional include/exclude glob rules. ([Issue 0003](Issues/0003-include-exclude-glob-rules.md)) [phase=04-implementation]
- [x] [P3] Add add-on preferences for global default backup location. ([Issue 0004](Issues/0004-global-default-backup-location.md)) [phase=04-implementation]

## 05-test TODO

- [x] Add automated unittest coverage for backup creation, cleanup, and validation errors. [phase=05-test]
- [x] Add text integrity check for mojibake markers and control characters. [phase=05-test]
- [x] [P3] Run Blender 5.1.1 runtime gate on a machine where `blender.exe` is available. ([Issue 0001](Issues/0001-blender-511-runtime-gate.md)) [phase=05-test]
- [x] [P3] Detect Steam Blender installs and directory-valued `BLENDER_EXE`. ([Issue 0006](Issues/0006-runtime-gate-steam-blender-detection.md)) [phase=05-test]
- [x] [P3] Improve runtime gate diagnostics when `BLENDER_EXE` is set but not found. ([Issue 0005](Issues/0005-runtime-gate-blender-exe-diagnostics.md)) [phase=05-test]

## 06-release TODO

- [x] Add package generation for `dist/blender-auto-backup-0.1.0.zip`. [phase=06-release]
- [x] Add install guide, manual test guide, QCDS, release checklist, and docs ZIP generation. [phase=06-release]
- [x] Add strict metrics JSON and validator. [phase=06-release]
- [x] [P3] Fix Blender extension manifest tagline validation failure. ([Issue 0007](Issues/0007-extension-manifest-tagline-validation.md)) [phase=06-release]

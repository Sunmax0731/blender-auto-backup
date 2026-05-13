# v0.1.1 リリース公開

- Status: done
- Priority: P2
- Type: release
- Source: local
- Draft source: codex-cli
- Phase: 06-release
- Created: 2026-05-14
- QCDS: Quality, Delivery, Satisfaction

## Context

Issue 0013 で追加した `Preview Backup` を公開するため、既存 `v0.1.0` release を上書きせず、次版 `v0.1.1` としてパッケージ、docs、QCDS、GitHub release を同期する。

## Acceptance Criteria

- [x] アドオン版数と package/docs ZIP 版数が `0.1.1` に更新されている
- [x] `npm test` が成功し、Blender 5.1.1 runtime gate が `passed` で記録されている
- [x] release notes、release evidence、QCDS、release checklist が `v0.1.1` と一致している
- [x] `main` に release commit が反映され、tag `v0.1.1` と GitHub release が公開されている

## Evidence

- Version files: `package.json`, `blender_manifest.toml`, `blender_auto_backup/__init__.py`
- Artifacts: `dist/blender-auto-backup-0.1.1.zip`, `dist/blender-auto-backup-latest.zip`, `dist/blender-auto-backup-docs-0.1.1.zip`, `dist/test-summary.json`, `dist/runtime-gate.json`
- Release notes: `docs/releases/v0.1.1.md`
- Verification: `npm test` passed on 2026-05-14; Blender 5.1.1 runtime gate `passed`.
- GitHub release: `https://github.com/Sunmax0731/blender-auto-backup/releases/tag/v0.1.1`

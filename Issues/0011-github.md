# リリース資料整備とGitHubリリース

- Status: done
- Priority: P2
- Type: release
- Source: local
- Draft source: codex-cli
- Phase: 06-release
- Created: 2026-05-13
- QCDS: Quality, Delivery, Satisfaction

## Context

動作確認は完了済み。リリースに必要な手順書などのドキュメントを整備し、QCDS評価を反映したうえでGitHubリリースまで進める。

## Acceptance Criteria

- [x] リリース手順書など必要なドキュメントが最新状態に更新されている
- [x] QCDS評価結果がリリース前提として記録されている
- [x] GitHubリリースに必要な成果物と説明文が準備されている
- [x] GitHubリリースが作成され、公開状態を確認できる

## Notes

- Release tag: `v0.1.0`
- Release URL: `https://github.com/Sunmax0731/blender-auto-backup/releases/tag/v0.1.0`
- Release notes: `docs/releases/v0.1.0.md`
- Release evidence: `docs/release-evidence.json`
- Assets: `dist/blender-auto-backup-0.1.0.zip`, `dist/blender-auto-backup-latest.zip`, `dist/blender-auto-backup-docs-0.1.0.zip`, `dist/test-summary.json`, `dist/runtime-gate.json`
- Verification: `npm test`
- Runtime gate: `passed` on Blender 5.1.1.

## Codex Sessions

- 2026-05-13T20:57:51.781Z `codex-session-20260513205751-lp5o7g` - All Work Items (VS Code Codex handoff); access=danger-full-access; model=gpt-5.5; intelligence=high; [prompt](c:/Users/gkkjh/AppData/Roaming/Code/User/workspaceStorage/c3f13110f602d3f98fbe6ea1c39016d9/sunmax0731.codex-friendly-project-starter/first-prompt-20260513T205751Z.md)

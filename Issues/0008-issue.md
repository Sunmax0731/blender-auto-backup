# 未整理課題のフェーズ振り分け

- Status: done
- Priority: P2
- Type: feature
- Source: local
- Draft source: codex-cli
- Phase: 01-requirements
- Created: 2026-05-13
- QCDS: Cost, Delivery

## Context

未整理の課題が多く、作業契約や進行順が把握しづらい状態になっている。既存の課題を要件、仕様、設計、実装、テスト、リリースなどのフェーズに分類し、優先度と作業単位を判断しやすくする。

## Acceptance Criteria

- [x] 未整理の課題が各フェーズに分類されている
- [x] 分類後の課題が重複や粒度の不一致を確認できる形で整理されている
- [x] 次に着手すべき課題がフェーズ単位で判断できる

## Notes

- `docs/backlog-triage.md` にフェーズ分類、重複確認、次アクションを記録した。
- Issue 0009 は Issue 0008 と同一内容のため、0008 に統合して完了扱いにした。
- 追加の follow-up Issue は不要。

## Evidence

- `docs/backlog-triage.md` records the phase taxonomy, current classification, duplicate review, and next work.
- `TODO.md` has no unchecked local work item after this issue is closed.
- `docs/qcds-evaluation.md`, `docs/qcds-strict-metrics.json`, and `docs/release-checklist.md` include the backlog triage evidence.

## Codex Sessions

- 2026-05-13T19:32:35.982Z `codex-session-20260513193235-cqfb4z` - All Work Items (VS Code Codex handoff); access=danger-full-access; model=gpt-5.5; intelligence=high; [prompt](c:/Users/gkkjh/AppData/Roaming/Code/User/workspaceStorage/c3f13110f602d3f98fbe6ea1c39016d9/sunmax0731.codex-friendly-project-starter/first-prompt-20260513T193235Z.md)

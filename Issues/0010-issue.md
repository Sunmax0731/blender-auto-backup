# バックアップ保存先のサブフォルダ方式を追加

- Status: done
- Priority: P2
- Type: feature
- Source: local
- Draft source: codex-cli
- Phase: 04-implementation
- Created: 2026-05-13
- QCDS: Quality, Satisfaction

## Context

Backupフォルダ指定時の保存先構成に追加要望がある。現状のBackupフォルダ直下へ保存する方式に加えて、Backupフォルダ直下にフォルダを作成し、その配下へバックアップする方式をオプションで選択できるようにする。既存の保存先挙動は維持し、ユーザーが用途に応じてバックアップ階層を整理できることを目的とする。

## Acceptance Criteria

- [x] 設定またはUIから、Backupフォルダ直下へ保存する方式と、サブフォルダを作成してその配下へ保存する方式を選択できる。
- [x] サブフォルダ方式を選択した場合、指定したBackupフォルダ直下に対象フォルダが作成され、その配下にバックアップZIPが保存される。
- [x] 直下保存方式を選択した場合、既存の保存先挙動と互換性が保たれる。
- [x] 保存先が作業フォルダ内にある場合でも、バックアップ保存先フォルダはバックアップ対象から除外される。

## Notes

- `Destination Layout` 設定を追加し、既定は既存互換の `Direct` とした。
- `Subfolder` は有効なバックアップラベルをフォルダ名に使い、`Backup Folder\<safe label>\*.zip` へ保存する。
- サービス層 unittest で直下保存互換、サブフォルダ保存、作業フォルダ内保存先除外、不正 mode 拒否を確認した。
- Verification: `python -m unittest tests.test_backup_service`
- Verification: `npm test`
- Manual verification: user confirmed behavior OK on 2026-05-14.

## Codex Sessions

- 2026-05-13T20:43:06.564Z `codex-session-20260513204306-8phq7h` - Work Item: バックアップ保存先のサブフォルダ方式を追加 (VS Code Codex handoff); access=danger-full-access; model=gpt-5.5; intelligence=high; [prompt](c:/Users/gkkjh/AppData/Roaming/Code/User/workspaceStorage/c3f13110f602d3f98fbe6ea1c39016d9/sunmax0731.codex-friendly-project-starter/first-prompt-20260513T204306Z.md)

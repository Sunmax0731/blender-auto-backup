# AGENTS

この repo は `D:\AI\BlenderAddon\blender-auto-backup` の Blender アドオンです。Blender 作業フォルダを指定間隔で ZIP バックアップすることが目的です。

## 作業順

1. `README.md` を読む。
2. `AGENTS.md` を読む。
3. `SKILL.md` を読む。
4. `TODO.md` と `docs/` のチェックリストを作業契約として扱う。
5. 実装前に `blender_auto_backup/` と `scripts/` の責務境界を確認する。

## 実装ルール

- 対象 Blender は 4.2 以降。ユーザー検証は 5.1.1 を前提にする。
- Blender API 依存は `operators.py`、`panels.py`、`properties.py`、`scheduler.py` に寄せる。
- フォルダ走査、ZIP 作成、保持数整理は `blender_auto_backup/services/backup_service.py` に置き、通常 Python の unittest で検証できるようにする。
- 保存先が作業フォルダ内にある場合、保存先フォルダをバックアップ対象から除外する。
- 不完全な ZIP を正式成果物にしないため、`.partial` で作成してから置換する。
- 新しい作業を見つけたら `TODO.md` に同じ粒度で追記してから処理する。
- 文字化け断片や制御文字を docs/code に入れない。`npm test` の文字検査を通す。

## Git / release

- 作業ブランチは `codex/<task-summary>` 形式を使う。
- リリース準備では `npm test`、`docs/qcds-evaluation.md`、`docs/qcds-strict-metrics.json`、`docs/release-checklist.md`、docs ZIP をそろえる。
- Blender 実行ファイルがない環境では runtime gate を未達として記録し、Quality と Satisfaction は B+ 以下にする。


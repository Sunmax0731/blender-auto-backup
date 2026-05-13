# Architecture

## Module boundaries

- `blender_auto_backup/services/backup_service.py`
  - Blender API に依存しないコア処理
  - 入力検証、glob filter 判定、保存先レイアウト解決、Preview 用の対象数算出、ZIP 作成、保存先除外、保持数整理
- `blender_auto_backup/properties.py`
  - Scene に保存される設定と add-on preferences
- `blender_auto_backup/operators.py`
  - 手動実行、開始、停止、保存先を開く操作
- `blender_auto_backup/panels.py`
  - Scene Properties の UI
- `blender_auto_backup/scheduler.py`
  - Blender timer による定期実行
- `scripts/`
  - package、test、QCDS、runtime gate、docs ZIP

## Decision

3 つの方式を比較した。

| Option | Summary | Pros | Cons | Decision |
| --- | --- | --- | --- | --- |
| A | Blender add-on の timer と任意 worker で ZIP を作成 | 導入が軽い。Blender 内で完結する | worker は同時 1 件で、Blender API 更新は timer 経由に限る | 採用 |
| B | 外部 Windows 常駐アプリ | 大容量や非同期に強い | installer と常駐権限が必要 | Deferred |
| C | Git 連携だけで版管理 | 差分管理に強い | Blender 非技術ユーザーには負担が大きい | 不採用 |

MVP は Option A を採用する。P3 backlog では Option A のまま任意の Python worker thread を追加し、外部常駐アプリなしで大容量フォルダ時の UI thread 負荷を下げる。

## Background worker

`Run in Background` が有効な場合、operators / scheduler は scene 設定を文字列と数値に snapshot して worker thread に渡す。worker は Blender API に触れず `run_backup` だけを呼ぶ。完了結果は queue に入り、Blender timer が UI thread 側で panel status と last backup path に反映する。

同時実行は 1 件だけ許可する。worker 実行中に manual backup または timer backup が重なった場合は新しいジョブを開始しない。

## Data flow

1. User sets Source Folder, Backup Folder, Destination Layout, Interval, Max Backups.
2. If Backup Folder is empty, operators resolve add-on preference `Default Backup Folder`; if that is empty, the service uses `.blender-auto-backup` under Source Folder.
3. If Destination Layout is `Subfolder`, the service creates a safe project-label subfolder under the effective backup folder and writes ZIP files there.
4. `Preview Backup` calls `plan_backup`, which validates folders, applies destination exclusion and include / exclude globs, then counts files and bytes without creating folders or ZIP files.
5. Operator or timer calls `run_backup` directly, or starts a worker that calls `run_backup`.
6. `run_backup` uses the same planning path as Preview before writing files.
7. Service writes `label-yyyymmdd-hhmmss.zip.partial`.
8. Service replaces it with `.zip`.
9. Service deletes old matching ZIP files beyond `Max Backups`.
10. Operator or timer updates panel status.

## Backup Preview

`BackupPlan` is a pure-Python result object that contains the resolved source folder, effective backup folder, planned archive path, file count, byte count, normalized glob filters, and backup destination exclusion roots. The Blender operator only converts scene settings into plain values and displays the result in panel status.

Preview intentionally does not create the backup destination folder. This keeps it safe to run while users are still adjusting settings, and the automated tests can verify the behavior without Blender.

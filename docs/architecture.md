# Architecture

## Module boundaries

- `blender_auto_backup/services/backup_service.py`
  - Blender API に依存しないコア処理
  - 入力検証、ZIP 作成、保存先除外、保持数整理
- `blender_auto_backup/properties.py`
  - Scene に保存される設定
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
| A | Blender add-on の timer で ZIP を作成 | 導入が軽い。Blender 内で完結する | 大容量では UI thread が重くなる | 採用 |
| B | 外部 Windows 常駐アプリ | 大容量や非同期に強い | installer と常駐権限が必要 | Deferred |
| C | Git 連携だけで版管理 | 差分管理に強い | Blender 非技術ユーザーには負担が大きい | 不採用 |

MVP は Option A を採用する。バックアップ処理は純 Python service に隔離し、将来 Option B の worker へ移しやすくする。

## Data flow

1. User sets Source Folder, Backup Folder, Interval, Max Backups.
2. Operator or timer calls `run_backup`.
3. Service validates folders.
4. Service writes `label-yyyymmdd-hhmmss.zip.partial`.
5. Service replaces it with `.zip`.
6. Service deletes old matching ZIP files beyond `Max Backups`.
7. Operator updates panel status.


# Manual Test

## 目的

Blender 5.1.1 で、アドオン導入、手動バックアップ、自動バックアップ、保持数整理が動くことを確認します。

## 作業ディレクトリ

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
```

## Access URL

ローカル Blender アドオンのため URL はありません。

## 事前準備

```powershell
npm test
```

期待結果:

- `dist/blender-auto-backup-0.1.0.zip` が存在する
- Blender 実行ファイルが見つかる環境では `dist/runtime-gate.json` の `status` が `passed`
- Blender 実行ファイルが見つからない環境では `status` が `not_run`

## Blender 5.1.1 手動シナリオ

1. Blender 5.1.1 を起動する。
2. `Edit > Preferences > Add-ons > Install from Disk...` から `dist/blender-auto-backup-0.1.0.zip` を導入する。
3. `Blender Auto Backup` を有効化する。
4. 任意の一時フォルダを作り、`scene.blend` と `notes.txt` を置く。
5. Scene Properties > `Auto Backup` を開く。
6. `Source Folder` に一時フォルダを指定する。
7. `Backup Folder` を空のままにする。
8. `Destination Layout` を `Direct` にする。
9. `Max Backups` を `2` にする。
10. `Run in Background` を off にする。
11. `Backup Now` を押す。

期待結果:

- `Source Folder\.blender-auto-backup` が作成される
- `SourceFolderName-yyyymmdd-hhmmss.zip` が作成される
- ZIP 内に `scene.blend` と `notes.txt` が入っている
- ZIP 内に `.blender-auto-backup` は含まれない
- `Last` 表示が `OK:` で始まる

## Subfolder destination layout シナリオ

1. `Backup Folder` に一時保存先フォルダを指定する。
2. `Destination Layout` を `Subfolder` にする。
3. `Backup Label` を空にする。
4. `Backup Now` を押す。

期待結果:

- `Backup Folder\SourceFolderName` が作成される
- `Backup Folder\SourceFolderName\SourceFolderName-yyyymmdd-hhmmss.zip` が作成される
- `Backup Folder` 直下には新しい ZIP が直接作成されない
- Scene 側の `Last` 表示が `OK:` で始まる

作業フォルダ内の保存先除外確認:

1. `Backup Folder` に `Source Folder\Backups` を指定する。
2. `Destination Layout` を `Subfolder` にする。
3. `Backup Now` を押す。

期待結果:

- `Source Folder\Backups\SourceFolderName` に ZIP が作成される
- ZIP 内に `Backups` フォルダ配下のファイルは含まれない

## Global default backup folder シナリオ

1. `Edit > Preferences > Add-ons > Blender Auto Backup` を開く。
2. `Default Backup Folder` に一時保存先フォルダを指定する。
3. Scene Properties > `Auto Backup` で `Backup Folder` を空にする。
4. `Backup Now` を押す。

期待結果:

- `Default Backup Folder` に ZIP が作成される
- Scene 側の `Backup Folder` が空でも `Last` 表示が `OK:` で始まる

## Include / exclude glob シナリオ

1. `Source Folder` に `scene.blend`、`notes.txt`、`cache/temp.blend` を置く。
2. `Include Globs` に `*.blend` を入れる。
3. `Exclude Globs` に `cache/**` を入れる。
4. `Backup Now` を押す。

期待結果:

- ZIP 内に `scene.blend` が入る
- ZIP 内に `notes.txt` は入らない
- ZIP 内に `cache/temp.blend` は入らない

## Background worker シナリオ

1. `Run in Background` を on にする。
2. `Backup Now` を押す。
3. Panel の `Last` が `Backup running in background` になることを確認する。
4. timer 更新後に `Last` が `OK:` で始まることを確認する。
5. worker 実行中にもう一度 `Backup Now` を押す。

期待結果:

- Blender UI が backup operator の完了待ちで固まり続けない
- 完了後に ZIP が作成される
- 同時実行しようとした場合、`Backup already running in background` が表示される

## 自動バックアップシナリオ

1. `Interval Minutes` を `1` にする。
2. `Start Auto Backup` を押す。
3. `Next Run` が表示されることを確認する。
4. 1 分以上待つ。

期待結果:

- 新しい ZIP が追加される
- `Last Run` が更新される
- `Max Backups` が `2` の場合、3 個目以降の古い ZIP が削除される

## Runtime gate コマンド

Blender 5.1.1 のパスが分かる場合:

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
$env:BLENDER_EXE='D:\SteamLibrary\steamapps\common\Blender'
Test-Path -LiteralPath $env:BLENDER_EXE
npm run runtime:gate
```

期待結果:

- `Test-Path` が `True` を返す
- コマンドが exit code 0
- `dist/runtime-gate.json` の `status` が `passed`
- `dist/runtime-gate.json` の `blender_version` が `5.1.1`
- `dist/extension-validate.log` に extension package validation の失敗がない
- `dist/runtime-gate.log` に Blender 側の例外がない

`BLENDER_EXE` は `blender.exe` そのもの、または `blender.exe` を含むディレクトリを指定できます。Steam 版 Blender の既定候補として `D:\SteamLibrary\steamapps\common\Blender\blender.exe` も runtime gate が確認します。

`Test-Path` が `False` の場合、`npm run runtime:gate` は `status: not_run` を返し、`dist/runtime-gate.json` に `env_path`、`env_path_exists`、`env_path_normalized`、`env_candidate`、`checked_paths` を記録します。

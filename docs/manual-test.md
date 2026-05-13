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
8. `Max Backups` を `2` にする。
9. `Backup Now` を押す。

期待結果:

- `Source Folder\.blender-auto-backup` が作成される
- `SourceFolderName-yyyymmdd-hhmmss.zip` が作成される
- ZIP 内に `scene.blend` と `notes.txt` が入っている
- ZIP 内に `.blender-auto-backup` は含まれない
- `Last` 表示が `OK:` で始まる

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
$env:BLENDER_EXE='C:\Program Files\Blender Foundation\Blender 5.1\blender.exe'
npm run runtime:gate
```

期待結果:

- コマンドが exit code 0
- `dist/runtime-gate.json` の `status` が `passed`
- `dist/extension-validate.log` に extension package validation の失敗がない
- `dist/runtime-gate.log` に Blender 側の例外がない

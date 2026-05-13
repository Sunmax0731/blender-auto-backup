# Blender Auto Backup

Blender 4.2 以降向けのアドオンです。Blender 作業中のフォルダを指定した時間間隔で ZIP バックアップし、作業フォルダ内または任意の保存先に履歴を残します。

対象リポジトリ: `D:\AI\BlenderAddon\blender-auto-backup`

## 利用者向けマニュアル

Blender 上での画面の開き方、バックアップ設定、ZIP の確認手順は [画面付きユーザーガイド](docs/user-guide.md) を参照してください。

## 主な機能

- Scene Properties > Auto Backup からバックアップ対象フォルダ、保存先、間隔、保持数を設定
- 手動バックアップ実行
- Blender timer による定期バックアップ
- 大容量フォルダ向けの任意のバックグラウンド実行
- 任意の include / exclude glob によるバックアップ対象選別
- アドオン設定による global default backup folder
- Backup Folder 直下へ保存する方式と、対象フォルダ名のサブフォルダ配下へ保存する方式を選択可能
- `.partial` を使った一時 ZIP 作成と置換で、不完全な ZIP を正式成果物にしない
- 保存先が作業フォルダ内にある場合も、バックアップ ZIP 自身を再帰的に取り込まない
- 古い ZIP を `max_backups` 件まで自動整理

## 必要環境

- Windows 10/11
- Blender 4.2 以降
- 動作検証予定: Blender 5.1.1
- 開発検証: Python 3.10+、Node.js 20+、npm 11+

## インストール

1. `npm test` を実行して `dist/blender-auto-backup-0.1.0.zip` を生成します。
2. Blender を起動します。
3. `Edit > Preferences > Add-ons > Install from Disk...` で ZIP を選択します。
4. `Blender Auto Backup` を有効化します。

インストールの詳細は [installation guide](docs/installation-guide.md) を参照してください。

## 使い方

1. Blender の Scene Properties を開きます。
2. `Auto Backup` パネルで `Source Folder` を指定します。
3. 必要に応じて `Backup Folder`、`Destination Layout`、`Interval Minutes`、`Max Backups` を設定します。
4. 必要に応じて `Run in Background`、`Include Globs`、`Exclude Globs` を設定します。
5. `Backup Now` で代表動作を確認します。
6. `Start Auto Backup` で定期バックアップを開始します。

保存先を空にした場合、アドオン設定の `Default Backup Folder` が使われます。そこも空の場合は `Source Folder\.blender-auto-backup` に ZIP が作成されます。`Destination Layout` が `Subfolder` の場合は、有効な保存先フォルダの直下に対象フォルダ名のサブフォルダを作り、その配下に ZIP を作成します。

## 開発コマンド

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
npm test
```

`npm test` は次を実行します。

- Python unittest
- Python compile check for the add-on package
- アドオン ZIP 作成
- docs ZIP 作成
- QCDS JSON 検査
- 文字化け・制御文字検査
- Blender runtime gate

Blender 実行ファイルが PATH または標準候補にない場合、runtime gate は `not_run` として記録されます。その場合の手動確認手順は [docs/manual-test.md](docs/manual-test.md) にあります。

## リリース成果物

- `dist/blender-auto-backup-0.1.0.zip`
- `dist/blender-auto-backup-docs-0.1.0.zip`
- `dist/test-summary.json`
- `dist/runtime-gate.json`

The add-on ZIP uses the Blender 4.2 extension layout: `blender_manifest.toml` and `__init__.py` are placed at the archive root.

## 現在の制限

- MVP は active scene の設定を対象にします。
- バックグラウンド実行は同時に 1 件だけ実行します。実行中に次のバックアップ時刻へ到達した場合、新しいジョブは開始されません。
- Codex 実行環境では Blender 実行ファイルが見つからない場合、Blender 5.1.1 の実機 runtime gate はユーザー側で実行してください。

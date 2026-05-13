# Installation Guide

## 前提

- Windows 10/11
- Blender 4.2 以降
- ユーザー側の実機確認ターゲット: Blender 5.1.1

## ZIP を作成する

```powershell
cd D:\AI\BlenderAddon\blender-auto-backup
npm test
```

期待結果:

- `dist/blender-auto-backup-0.1.0.zip` が作成される
- `dist/blender-auto-backup-docs-0.1.0.zip` が作成される
- `dist/test-summary.json` が作成される
- アドオン ZIP の root に `blender_manifest.toml` と `__init__.py` が含まれる

## Blender に導入する

1. Blender を起動する。
2. `Edit > Preferences > Add-ons` を開く。
3. `Install from Disk...` を押す。
4. `D:\AI\BlenderAddon\blender-auto-backup\dist\blender-auto-backup-0.1.0.zip` を選ぶ。
5. `Blender Auto Backup` を有効化する。
6. Scene Properties に `Auto Backup` パネルが表示されることを確認する。

## 手動更新

新しい ZIP を導入する場合は、既存の `Blender Auto Backup` を無効化してから同じ手順で ZIP を入れ直してください。

## トラブルシュート

- `Source Folder does not exist`: 実在するフォルダを指定してください。
- ZIP が増え続ける: `Max Backups` を確認してください。
- 保存先が作業フォルダ内にある: アドオンは保存先フォルダをバックアップ対象から除外します。
- headless runtime gate を実行したい: `BLENDER_EXE` を設定してください。

```powershell
$env:BLENDER_EXE='C:\Program Files\Blender Foundation\Blender 5.1\blender.exe'
npm run runtime:gate
```

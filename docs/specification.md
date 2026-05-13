# Specification

## Goal

Blender 作業中のフォルダを、ユーザーが指定した時間間隔で自動的にバックアップする。

## Target

- Blender 4.2 以降
- Windows 10/11
- ユーザー側 runtime validation: Blender 5.1.1

## MVP scope

- バックアップ対象フォルダを 1 つ指定できる
- バックアップ保存先を指定できる
- 保存先未指定時は対象フォルダ内の `.blender-auto-backup` を使う
- バックアップ形式は ZIP
- 保持数を超えた古い ZIP は削除する
- 手動バックアップと timer による自動バックアップを持つ

## Non-goals

- 差分バックアップ
- バックグラウンド worker
- クラウド保存
- UI からの glob include/exclude 編集

## Error handling

- Source Folder 未指定または不存在はエラーとして Blender report と panel status に表示する。
- Backup Folder が Source Folder と同一の場合は拒否する。
- ZIP 作成中に失敗した場合、`.partial` は削除する。
- 保存先が Source Folder 内の場合、保存先フォルダ配下は ZIP に含めない。


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
- Add-on Preferences の `Default Backup Folder` が設定されている場合、scene の保存先未指定時はそのフォルダを使う
- `Destination Layout` で、保存先フォルダ直下へ ZIP を置く方式と、保存先フォルダ直下の対象フォルダ名サブフォルダへ ZIP を置く方式を選択できる
- バックアップ形式は ZIP
- 任意の include / exclude glob で ZIP に入れるファイルを選別できる
- Exclude glob は include glob より優先される
- 保持数を超えた古い ZIP は削除する
- 手動バックアップと timer による自動バックアップを持つ
- `Run in Background` が有効な場合、手動バックアップと自動バックアップは worker thread で ZIP 作成を実行する

## Non-goals

- 差分バックアップ
- クラウド保存
- 複数バックアップ job の同時実行

## Error handling

- Source Folder 未指定または不存在はエラーとして Blender report と panel status に表示する。
- Backup Folder が Source Folder と同一の場合は拒否する。
- ZIP 作成中に失敗した場合、`.partial` は削除する。
- 保存先が Source Folder 内の場合、直下保存方式でもサブフォルダ方式でも保存先フォルダ配下は ZIP に含めない。
- Include / exclude glob の結果、対象ファイルが 0 件になった場合はエラーにする。
- Background worker が実行中の場合、新しい background backup は開始せず status に表示する。

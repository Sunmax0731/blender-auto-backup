# 0012 画面画像を使った利用者向けドキュメント整備

- Status: done
- Priority: P3
- Type: docs
- Source: local
- Phase: 06-release
- Created: 2026-05-14
- QCDS: Satisfaction, Delivery
- Linked TODO: ../TODO.md

## Contract

`docs/img` に追加された Blender 画面画像を使い、利用者が Scene プロパティから `Auto Backup` パネルを開き、バックアップを作成し、生成された ZIP を確認できるようにドキュメントを整備する。

## Checklist

- [x] 画像付きの利用者向けガイドを追加する
- [x] README / installation / manual test docs から利用者向けガイドへ誘導する
- [x] docs ZIP に利用者向けガイドと画像を含める
- [x] 文字検査と docs ZIP 生成を検証する

## Evidence

- `docs/user-guide.md`
- `README.md`
- `docs/img/img1.png`
- `docs/img/img2.png`
- `docs/img/img3.png`
- `scripts/collect_docs_zip.py`

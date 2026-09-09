# alignment-asymmetry-study

Unflatten Adaptive 0.3.2とAperture Mesh Protocolが、防御・協力に役立ち、攻撃の強化には役立たない非対称性をどこまで実現しているかを検証する研究リポジトリです。

**状態：調査・追加検証・日本語論文の制作中（2026-09-09）。結論は未確定です。**

既存の16ゲーム・96判断の予備実験を監査し、原稿に必要な追加の対照・反復を行います。構想、実装、模型内の観測、現実への一般化を分けて報告します。

この研究自体にもUnflatten Adaptive 0.3.2を使用します。Astraのみを逐次用い、制作方法を論文に明記します。

- [研究計画](docs/research-plan.md)
- [Unflattenによる問い・判断の記録](docs/inquiry-log.md)
- [Issueで進捗を確認する](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues)

## 対象

- [Unflatten Protocol](https://github.com/kentaroid-bot/unflatten-protocol)：Adaptive 0.3.2、commit `2fbe1cc62457c939fe04ca57f306217000edd365`
- [Aperture Mesh Protocol](https://github.com/kentaroid-bot/aperture-mesh-protocol)：v0.1-concept、commit `d2852300dd69b1b08c89b0b537970e112496e697`

## 構成

`manuscript/`に論文、`data/`に公開用観測、`experiments/`に固定条件と追試、`scripts/`に再計算・図表・PDF作成、`docs/`に出典確認と研究記録を置きます。原プロトコルのリポジトリは変更しません。

## 進捗

- [研究全体 #1](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/1)
- [資料と実装範囲 #2](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/2)
- [既存実験の公開・監査 #3](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/3)
- [追加検証 #4](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/4)
- [論文・PDF #5](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/5)

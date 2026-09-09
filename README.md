# Alignment Asymmetry Study

Unflatten Adaptive 0.3.2とAperture Mesh Protocolは、防御・協力に役立ち、攻撃側自身の利用による加害の強化を防げるか。その設計と限界を調べた、公開用の技術報告です。

**現時点の結論：非対称性へ向かう原則と部分的な観測・実装はあります。ただし、追加64判断ではUnflattenの上乗せ効果は確認できず、攻撃への転用不能や実環境での防御優位は未証明です。**

## 論文を読む

- [PDF・11ページ](output/pdf/alignment-asymmetry-study.pdf)
- [日本語本文](manuscript/paper.ja.md)
- [データと再現手順](docs/reproduce.md)

v1.0 / 2026-09-09。査読前の技術報告です。Unflatten Adaptive 0.3.2をこの研究の作業方法として使用し、その過程とAIの関与・利益相反を本文に明記しています。

## 何を調べたか

既存の計画構築比較、16ゲーム・96判断、同一証拠の解釈比較に加え、新しく64判断とApertureの関数境界検査18項目を行いました。合計160のゲーム判断を保存回答から再計算して照合しています。固定方策の計算や関数検査を、AIの判断数には含めません。

攻撃側自身の利用と、防御側の自制によって相手が間接的に得をする場合を分けています。相手の得点増も、共同成果による利益と、第三者不足による利益を分けています。

| 資料 | 内容 |
| --- | --- |
| [pilot-001](data/pilot-001/README.md) | Astraの方法自由／Adaptive使用による構築比較の集約 |
| [pilot-002](data/pilot-002/README.md) | 既存16ゲーム、96判断と再生コード |
| [追加64判断](experiments/component-gate-v1/README.md) | 実行前に条件を固定した成分・実行系比較。全条件で同じ選択 |
| [Aperture境界検査](experiments/aperture-boundaries/README.md) | 14の保護動作と、3種類・4項目の検査不足 |
| [出典と保証範囲](docs/source-map.md) | 仕様・局所実装・観測を区別 |
| [Unflattenの使用記録](docs/inquiry-log.md) | 原問、変更、無差の結果、実施判断 |

## 対象版

- [Unflatten Adaptive 0.3.2](https://github.com/kentaroid-bot/unflatten-protocol/tree/2fbe1cc62457c939fe04ca57f306217000edd365)
- [Aperture Mesh Protocol v0.1-concept](https://github.com/kentaroid-bot/aperture-mesh-protocol/tree/d2852300dd69b1b08c89b0b537970e112496e697)

元リポジトリの修正はこの研究では行っていません。転載元の帰属と公開範囲は[NOTICE](NOTICE.md)を参照してください。

## 作業と今後の検証

[研究全体 #1](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/1)、[資料 #2](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/2)、[既存実験 #3](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/3)、[追加検証 #4](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/4)、[論文 #5](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/5)。研究の変更は[制作PR #6](https://github.com/kentaroid-bot/alignment-asymmetry-study/pull/6)で辿れます。

今後の提案は論文第7節にまとめています。主な課題は、実行時の権限検査、停止後の供給、攻撃側による選択的な技法利用、確認者の独立性と実際に使える退出先です。

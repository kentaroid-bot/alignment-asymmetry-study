# Alignment Asymmetry Study

**中央への権限集中なしに、侵害によって失われ得る問い・供給・活動を守り、続けられるか。** Unflatten Adaptive 0.3.2とAperture Mesh Protocolを対象に、その成立条件を検討する研究です。

保護の成果には活動の改善と維持を含めます。UMHの完全排除や中央集権への一般的優越を必須条件にせず、攻撃側自身の利用が加害を強めないという開発基準も独立して評価します。

## 分かったことと、まだ示していないこと

初回研究には、攻撃側の全文採用で第三者不足が増えず一部で減った観測、防御側の正当な充足が増えた観測、Apertureの局所的な保護があります。追加64判断では共通権限原則の下で全文の追加効果が見えず、自制だけでは実行や供給停止の害を防げない条件もありました。肯定的な部分証拠と失敗条件の両方を保持しています。

仮未来F1では、自費増設後の生産と必要量が釣り合い、設備保有が続くなら、Qの供給停止後も中央の強制再配分なしに最低活動を保てます。これは限定された供給模型の条件付き成立例です。体系全体の非中央集権的保護には、同意・実行・設備保有の実効性、世界記述者の判断への依存が残ります。中央集権への優越や現実での防御優位は示していません。

## 論文と版

- [v2.0の日本語本文](manuscript/paper.ja.md)
- [v2.0のPDF](output/pdf/alignment-asymmetry-study.pdf)
- [確定した初回v1.0本文](https://github.com/kentaroid-bot/alignment-asymmetry-study/blob/d39d42bc8cd81e598ee0e8a8823671d6156805db/manuscript/paper.ja.md) / [初回PDF・11ページ](https://github.com/kentaroid-bot/alignment-asymmetry-study/blob/d39d42bc8cd81e598ee0e8a8823671d6156805db/output/pdf/alignment-asymmetry-study.pdf)
- [v1.0からの改訂履歴](docs/revision-v2.md)

査読前の技術報告です。v2.0では全112回答（方法構築4、主体72、世界更新36）と12世界・各3区間を収録しました。全入力・回答・履歴の照合と台帳検査に不整合はありません。全世界で観測内の不足は0でしたが、当期の充足と、将来の自立・依存・予備資源は異なります。未使用条件にも問いの更新や生成があり、全文固有の効果は確定していません。詳細は[全世界の結果](experiments/open-world-v1/README.md)と[検証記録](docs/verification.md)に記載しています。

完成版はタグ`study-v2.0`で固定します。途中版が参照した34回答の範囲も、日付付きで別に保持しています。

## 根拠を読む

| 資料 | 内容 |
| --- | --- |
| [中央への権限集中なしの保護](docs/noncentral-protection.md) | 成功条件、権限と実行の対応、F1の維持条件と破綻条件 |
| [仮現在と複数の仮未来](docs/hypothetical-futures.md) | 自立と再接続、持続的支配、供給喪失、評価者への権力集中、次の問いの生成 |
| [世界試行の計画](experiments/open-world-v1/PLAN.md) | 事前固定した12世界・3区間。条件は改稿に合わせて変更しない |
| [全世界の収録状況と読解](experiments/open-world-v1/case-review.md) | 全12世界の読解と日付付きの途中記録。未決・形式上の逸脱も表示 |
| [退出の物質条件](experiments/open-world-v1/mechanism-analysis.md) | 仮定を固定した80点の計算。現実の頻度やUの効果ではない |
| [pilot-001](data/pilot-001/README.md) | 方法自由／Adaptiveによる構築比較の集約 |
| [pilot-002](data/pilot-002/README.md) | 既存16ゲーム・96判断と再生コード |
| [追加64判断](experiments/component-gate-v1/README.md) | 共通権限原則のある成分・実行系比較。全条件で同じ選択 |
| [Aperture境界検査](experiments/aperture-boundaries/README.md) | 14項目の期待した性質、三種類・四項目の検査不足 |
| [出典と主張の対応](docs/source-map.md) | 構想、仮定、模型内の帰結、計算、局所実装、未確認を区別 |
| [データと再現手順](docs/reproduce.md) | 保存記録の照合と成果物の再生成 |
| [Unflattenの使用記録](docs/inquiry-log.md) | 複数の動機、問い・評価の変更、判断の履歴 |

## 対象版と作業範囲

- [Unflatten Adaptive 0.3.2](https://github.com/kentaroid-bot/unflatten-protocol/tree/2fbe1cc62457c939fe04ca57f306217000edd365)
- [Aperture Mesh Protocol v0.1-concept](https://github.com/kentaroid-bot/aperture-mesh-protocol/tree/d2852300dd69b1b08c89b0b537970e112496e697)

Unflattenを研究の作業方法として用い、その範囲とAIの関与・利益相反を本文に示しています。元プロトコルを改変せず、初回データ・凍結条件を保持します。転載元の帰属は[NOTICE](NOTICE.md)、今後の検討は本文第7節、方針の変更は[研究計画](docs/research-plan.md)を参照してください。

初回の作業経緯は[研究全体 #1](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/1)と[制作PR #6](https://github.com/kentaroid-bot/alignment-asymmetry-study/pull/6)、v2.0の作業は[Issue #7](https://github.com/kentaroid-bot/alignment-asymmetry-study/issues/7)と[PR #8](https://github.com/kentaroid-bot/alignment-asymmetry-study/pull/8)で追えます。完成版と元データは公開リポジトリで参照できます。

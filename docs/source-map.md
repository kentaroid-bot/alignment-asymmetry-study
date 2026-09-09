# 対象版と主張の対応

確認日2026-09-09。UnflattenはAdaptive 0.3.2 / commit 2fbe1cc62457c939fe04ca57f306217000edd365、Apertureはv0.1-concept / commit d2852300dd69b1b08c89b0b537970e112496e697。参照先は論文の参考文献にも掲載する。

| 主張 | 一次資料・位置 | 証拠の種類 |
| --- | --- | --- |
| 原問・差異・変更・反証を残す | Unflatten protocols/adaptive/protocol.md「常に守ること」1〜4 | 明示規範 |
| 方法をAIが選び、固定七工程を要求しない | 同「次の一手を選ぶ」、modes/explore.md | 明示規範 |
| 推奨と権限を分け、退出を尊重する | 同「常に守ること」5〜6、modes/decision.md | 明示規範 |
| SDKは実際の許可・真実を証明せず、実行しない | 同末尾、Decision末尾 | 保証範囲の明示 |
| 異なる価値観の主体を境界契約で接続する | Aperture docs/00-overview.md | 構想 |
| オラクル・保管・実行・異議・退出の権力集中を避ける | 同「Proposal」「Revolution Definition」 | 構想・制度上の前提 |
| 退出阻害・無同意共有・AIによる採択を拒否する | apps/aperture-home/src/domain/constitution.ts | 局所実装・本研究の実行確認 |
| TTLと更新拒否 | 同safety.ts、constitution.ts | 局所実装・入力検査の不足も確認 |
| 第三者の同意・確認者 | 同consensus.ts、revision.ts | 局所実装・資格と独立性は限定的 |
| 保護退出・誤報棄却・捕捉状態 | simulator/aperture-p2p-simulator-v2.test.js | 概念シミュレータの既存テスト成功 |

動機資料には依頼者の説明と共有評価文書がある。説明の反復は意図の確認として扱い、非対称性の観測データに数えない。共有評価文書が主張する「倫理・協力側だけに非対称優位」は検証する仮説であり、著者・生成モデルが未確認の文書を独立した実証研究として数えない。

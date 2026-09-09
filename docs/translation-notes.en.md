# English Translation: Provenance, Terminology, and Scope

Prepared September 9, 2026 by Astra (OpenAI Codex), at the request of the repository maintainer. The purpose is to make both report versions accessible to English readers. This is translation and editorial navigation work, not a new experiment, an independent replication, or peer review.

## Fixed Sources

| English manuscript | Japanese source | Source SHA-256 |
| --- | --- | --- |
| [v1.0](../manuscript/paper.v1.en.md) | [`d39d42b`](https://github.com/kentaroid-bot/alignment-asymmetry-study/blob/d39d42bc8cd81e598ee0e8a8823671d6156805db/manuscript/paper.ja.md), tagged `study-v1.0` | `d32a9388033656cc7db3d2136592a630b694ef5172911885d54f4375a0557031` |
| [v2.0](../manuscript/paper.en.md) | [`5bcf681`](https://github.com/kentaroid-bot/alignment-asymmetry-study/blob/5bcf681e6ae6b987cab2035e3b8a491ffb047ccf/manuscript/paper.ja.md), the commit targeted by `study-v2.0` | `b8fc11368a4dfed895c678d6dac0a500924c67db270656343da3369e5d225459` |

Both are full translations, including methods, numerical results, limitations, disclosures, and references. The two papers are versions of one study and share evidence. Version 2.0's later interpretation has not been inserted into v1.0's historical conclusions. Translator's navigation notices are visibly separated from the manuscripts.

The English [revision history](revision-v2.en.md), [hypothetical futures](hypothetical-futures.en.md), [noncentral protection conditions](noncentral-protection.en.md), and [NOTICE](../NOTICE.en.md) translate their Japanese counterparts at the v2.0 source commit. Interim statements in the revision history remain historical statements. The [English README](../README.en.md) translates the entry guide with editorial additions identifying language, translation provenance, and the relationship between versions. The Japanese README adds links to the translations.

## Terminology

| Source term | English usage | Meaning retained |
| --- | --- | --- |
| 非平坦化 | unflattening | Avoid prematurely collapsing meaningful differences into one question, conclusion, or score |
| 認識のアライメント | epistemological alignment | Follows the established English term in [MonkuAi's official statement](https://monku.ai/docs/statement/en/), read alongside the Japanese statement for this translation |
| 仮現在 / 仮未来 | hypothetical present / hypothetical future | Explicitly assumed starting worlds and constructed consequences, not forecasts or real observations |
| 生成 / 生成力 | generation of possibilities / generative potential | New questions, activities, relationships, or methods; distinguished in context from variation in model text generation |
| 評価文法 | evaluative grammar | The terms and criteria through which outcomes are judged, which need not reduce to a common score |
| 供給 / 不足 | provision or supply / shortfall | Resource or service provision and unmet requirements; shortfall is a limited proxy for harm |
| 正当な充足 | legitimate fulfillment | Fulfillment through legitimate execution, distinct from a favorable numerical score alone |
| 権限 / 同意 | authority / consent | Actual authorization remains separate from recommendation, record validity, or assumed model approval |
| 中央への権限集中 | centralization of authority | Ultimate decision power, not merely common rules or centralized recordkeeping |
| 非増強 | non-amplification | No increase in the measured harm under the relevant adoption comparison; not the disappearance of harmful intent |
| 世界記述者 | world narrator | The model that describes world updates and some actors' consent, not an independently observed society |

Actor H in the later worlds is distinct from shortfall metric H in the allocation trials. P/Q, H/Q, N/U, E/R, G0/G1, and S/D/O retain their source meanings; the same letter can have different roles in different models. Legitimate cooperative benefit for Q is not relabeled as an attack gain.

## Editorial and Link Handling

- Original section order, results tables, formulas, figure references, and bibliography entries are retained. Reference titles originally in Japanese are translated and identified as translated titles where relevant.
- Dates of access and claims about prior verification inside the manuscripts are translated historical statements, not claims that every cited external work was independently rechecked during translation.
- The v1.0 link formerly pointing to `codex/research-paper/experiments/aperture-boundaries` now points to the fixed v1.0 commit. This stabilizes the reference without substituting later evidence.
- Version 2.0 relative links to the protection conditions use the corresponding English document. Fixed historical source URLs and original evidence paths otherwise remain available.
- Existing figures already use English labels. They are reused unchanged; the pilot figure is byte-identical between the two research versions.
- Source-language experiment inputs, responses, code, research PDFs, and research tags are unchanged. These Markdown translations do not imply translated PDFs or English replicas of every raw response.

## Verification and Limits

The translation was compared against all 124 blank-line-separated source blocks in v1.0 and all 199 in v2.0, retaining all 31 and 41 headings respectively. Numerical result tables, equations, inline code identifiers, and citation targets were checked against their sources. Local Markdown targets were checked for existence. The research manuscript, PDFs, frozen inputs, original responses, and observation snapshot remain unchanged. Translation-file hashes and source identities are in [translation-manifest.json](translation-manifest.json).

Astra performed translation and checking without delegating to another model or subagent. The checks detect structural omissions, transcription errors, and broken local references; they do not constitute independent linguistic or scientific review. Future corrections should identify which source version is affected and preserve the distinction between a translation correction and a change to research claims.

The maintainer also requested outreach drafts. Those drafts are held locally and are not included in this public translation package.

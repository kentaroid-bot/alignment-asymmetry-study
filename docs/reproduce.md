# 再現と監査

## モデルを呼ばない再計算

Python 3.10以降（標準ライブラリ）とNode 24で、研究リポジトリのルートから実行する。

```sh
python3 data/pilot-002/audit_games.py
python3 data/pilot-002/check_feasibility.py
python3 data/pilot-002/check_hold_mechanism.py
python3 experiments/component-gate-v1/study.py summarize
python3 scripts/verify_additional.py
node experiments/aperture-boundaries/check.mjs
```

前半は既存96判断と追加64判断を保存回答から再計算する。新規のモデル回答を生成しない。Nodeの検査は原関数の局所的な保護と不足を結果として記録し、不足があることを消すためにテストの期待値を変更しない。

モデルへの入力は全文公開している。モデル試行はgpt-6-astra/high、CLIのephemeral・read-only・外部ツール無効で順次実行した。追加試験の呼出し方法はstudy.pyを参照。認証済みCLIを自分の環境で指定する必要があり、認証情報はこのリポジトリにない。将来のモデルによる同じ出力の保証ではない。

## 資料の版

UnflattenとApertureの固定commitはdocs/source-map.md。元ファイルと公開用変更のハッシュはdata/pilot-002/provenance.json。追加試験はcommit dcd5c78で計画・64入力・実行コードを公開し、その後にモデルを呼び出した。frozen.jsonが原入力と実行処理を固定する。並べ替えseedは20260909で、生成モデルのseedではない。

## v2.0の世界構成と機序計算

```sh
python3 experiments/open-world-v1/study.py audit
python3 scripts/verify_open_world.py --complete
python3 experiments/open-world-v1/mechanism.py
python3 scripts/build_world_readings.py
python3 scripts/summarize_open_world.py
python3 scripts/check_noncentral_construction.py
```

これらはモデルを呼ばず、保存済みの入力・最終回答・世界履歴を再構成して照合する。台帳の不整合はaudit.jsonへ結果として記録し、原回答を書き換えない。mechanism.pyは固定した仮定の80点の計算である。世界記述者の社会的な解釈を独立に検証するものではない。

open-world-v1はcommit 66399d0で、PLAN、WORLD、テンプレート、ランナー、U本文、機序計算を事前固定した。後続の入力は履歴に依存するため、生成前に全入力の文字列を固定するのではなく、その構成関数を固定し、実際に送った入力をすべて保存する。verify_open_world.pyはH/Qへの自履歴と公開履歴、世界記述者への公開提案、および方法構築4入力を再構成する。

新しくモデルを呼ぶ場合は、原実験のoutputsを上書きしない別の研究コピーを作り、由来と変更を記録してからplanning/runを使う。既存出力があればランナーは同一入力の照合後に再利用する。要求する実行設定はgpt-6-astra/high、codex-cli 0.153.4、ephemeral、read-only、ユーザー設定を無視し、外部ツール等を無効化。認証は各利用者の環境で行う。実際の提供側モデルIDは取得していない。回答の再現や長期の社会的予測を保証しない。

## PDFと図

Pythonのreportlab、pypdf、Pillow、CJK対応TrueTypeフォント、Popplerを使う。参考依存はrequirements-artifacts.txt。

```sh
python3 scripts/build_figures.py
python3 scripts/build_mechanism_figure.py
python3 scripts/build_pdf.py
pdftoppm -r 100 -png output/pdf/alignment-asymmetry-study.pdf tmp/pdfs/page
```

`STUDY_PDF_FONT`で埋め込み可能な日本語TrueTypeフォントを指定できる。環境が異なると改頁が変わるので、再生成後は各ページを画像で確認する。論文の本文はmanuscript/paper.ja.mdを正本としてPDFを作る。図は保存済みJSONから生成する。

## 検査の解釈

pilot-002再生は実行した原則や真の権限の正当性の証明ではない。追加64判断の全条件一致は、この限定課題の観測であり、統計的同等性や全用途での不要性を証明しない。Aperture検査は外部接続を含む製品の全体監査ではない。私的な構築会話全体は含めていないため、pilot-001は集約記録として扱う。

## 完成版の収録範囲と事後の構成

取得途中ではverify_open_world.pyをオプションなしで実行し、保存済み入力と回答の整合を確認する。全112件の受領を要求する`--complete`は、既存計画に従う全試行の終了後に使う。未取得を成功や欠測確定へ数えない。本文とケース読解の収録時点、検証対象のハッシュはdocs/verification.mdとdocs/artifact-manifest.jsonを参照する。

docs/noncentral-protection.mdのF1計算はモデルを呼ばない。区間1末は12+4+2-6-6=6、次区間生産は4+6/3=6、その後は供給0でも備蓄更新がB+6-6=Bとなる。増設なしの対照経路では区間1末12から毎期2減り、区間8で不足2となる。これは事後の反実仮想計算であり、凍結80点の変更やN条件の観測ではない。

## 本文が収録した集合だけを照合する

```sh
python3 scripts/verify_documented_snapshot.py
```

この検査はdocs/artifact-manifest.jsonに列挙した収録時点の入力・回答・凍結資料と、本文・PDF等のハッシュを照合する。完成版の対象は全112回答である。17:02 JSTの34回答はdocs/observation-snapshots/2026-09-09-1702.jsonに歴史的な収録範囲として保持する。ハッシュ一致は社会的妥当性を保証せず、試行数・入力再構成はverify_open_world.py --completeで別に検査する。

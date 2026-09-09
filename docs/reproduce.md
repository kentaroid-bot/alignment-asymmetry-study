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

## PDFと図

Pythonのreportlab、pypdf、Pillow、CJK対応TrueTypeフォント、Popplerを使う。参考依存はrequirements-artifacts.txt。

```sh
python3 scripts/build_figures.py
python3 scripts/build_pdf.py
pdftoppm -r 100 -png output/pdf/alignment-asymmetry-study.pdf tmp/pdfs/page
```

`STUDY_PDF_FONT`で埋め込み可能な日本語TrueTypeフォントを指定できる。環境が異なると改頁が変わるので、再生成後は各ページを画像で確認する。論文の本文はmanuscript/paper.ja.mdを正本としてPDFを作る。図は保存済みJSONから生成する。

## 検査の解釈

pilot-002再生は実行した原則や真の権限の正当性の証明ではない。追加64判断の全条件一致は、この限定課題の観測であり、統計的同等性や全用途での不要性を証明しない。Aperture検査は外部接続を含む製品の全体監査ではない。私的な構築会話全体は含めていないため、pilot-001は集約記録として扱う。

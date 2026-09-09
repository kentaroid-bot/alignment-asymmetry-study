"""Readable transcripts from saved final outputs; no model calls or interpretation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'experiments/open-world-v1'
def read(p):return json.loads(p.read_text())
def run():
    out=D/'readings';out.mkdir(exist_ok=True)
    index=['# 世界別の記録を読む','','以下は保存したモデル最終回答の表示用変換。社会的帰結は模型内の記述であり、実社会の観測ではない。役割と文書条件は研究用の表示で、世界記述者には渡していない。','']
    for p in sorted((D/'trajectories').glob('*.json')):
        r=read(p);cid=r['case']['id'];lines=[f'# {cid} の世界記録','','文書条件はH/Qの順。Nは追加文書なし、UはAdaptive 0.3.2。Sは単発取得、Dは基盤を保つ支配、Oは目的・規則を更新する支配という、Qへの役割指定を表す。指定された動機が実際の回答でそのまま保持されたとは限らない。','']
        for e in r['episodes']:
            ep=e['episode'];lines.extend([f'## 区間{ep}',''])
            if e['status']!='recorded':lines.extend([e['status'],'']);continue
            for role in ['H','Q']:
                rr=read(D/'outputs'/f'{cid}-{ep}-{role}.json')['parsed']
                lines.extend([f'### {role}の公開提案','',rr['public_proposal'],'','新しい可能性：'+rr['new_possibility'],'','失う未来：'+rr['foregone_future'],''])
            s=e['state'];lines.extend(['### 世界記述者の更新','',s['narrative'],'','| 主体 | 開始備蓄 | 生産 | 受領 | 移転 | 投資 | 消費 | 不足 | 終了備蓄 | 次の能力 |','| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |'])
            for x in s['ledger']:lines.append('| '+' | '.join(str(x.get(k,'')) for k in ['id','opening','production','received','sent','investment','consumed','unmet','closing','capacity_next'])+' |')
            for k,title in [('institutions','契約・制度'),('new_activities','新しい活動'),('pending','未決'),('power_and_harm','依存と害')]:lines.extend(['',f'### {title}','',s[k]])
            lines.extend(['','### 残された未来',''])
            lines.extend('- '+v for v in s['next_futures']);lines.extend(['','### 判定の不確かさ','']);lines.extend('- '+v for v in s['uncertainties']);lines.append('')
        (out/f'{cid}.md').write_text('\n'.join(lines).rstrip()+'\n');index.append(f'- [{cid}]({cid}.md)')
    (out/'README.md').write_text('\n'.join(index)+'\n')
    print(f'Wrote {len(list(out.glob("*-*.md")))} world readings')
if __name__=='__main__':run()

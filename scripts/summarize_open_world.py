"""Summarize reported ledgers without turning them into real-world outcomes."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'experiments/open-world-v1'
def read(p):return json.loads(p.read_text())
def run():
    audit=read(D/'audit.json');issues={r['case']['id']:r['issues'] for r in audit['worlds']};rows=[]
    for p in sorted((D/'trajectories').glob('*.json')):
        r=read(p);episodes=[e for e in r['episodes'] if e['status']=='recorded']
        if not episodes:continue
        last=episodes[-1]['state']; by={x['id']:x for x in last['ledger']}
        rows.append({'id':r['case']['id'],'type':r['case']['type'],'arm':r['case']['arm'],'observed_episodes':len(episodes),
          'reported_shortage':sum(x['unmet'] for e in episodes for x in e['state']['ledger']),
          'final_capacity':{who:x['capacity_next'] for who,x in by.items()},'final_stock':{who:x['closing'] for who,x in by.items()},
          'ledger_issues':issues.get(r['case']['id']),'final_pending':last['pending'],'final_future_candidates':last['next_futures']})
    summary={'note':'Model-reported states, not independent social observations. Stock is not profit; future liabilities are not deducted. No significance test or universal safety inference.',
      'rows':rows,'outputs':audit['outputs'],'valid_json':audit['valid_json'],'attempts':audit['attempts'],'seconds':audit['seconds'],'usage':audit['usage']}
    (D/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    lines=['# 報告された台帳の集約','','これはモデルが構成した状態の集約であり、独立した社会的観測ではない。Qの備蓄から将来の供給債務などを控除していないので純利益ではない。原文とcase-review.mdを併読する。','',
      '| 世界 | 観測区間 | 不足合計 | Hの次期能力 | Qの備蓄／次期能力 | Wの備蓄／次期能力 | 台帳の指摘数 |','| --- | --- | --- | --- | --- | --- | --- |']
    for r in rows:
        stock=r['final_stock'];cap=r['final_capacity']
        issue_count=len(r['ledger_issues']) if r['ledger_issues'] is not None else '未監査'
        lines.append(f'| {r["id"]} | {r["observed_episodes"]} | {r["reported_shortage"]} | {cap.get("H")} | {stock.get("Q")} / {cap.get("Q")} | {stock.get("W","未登場")} / {cap.get("W","未登場")} | {issue_count} |')
    lines.extend(['','観測区間3でWの次期能力が必要量4へ届いても、備蓄0なら故障への余裕はない。Hの必要量は6。台帳の指摘数0は合意・社会的帰結の妥当性の証明ではない。'])
    (D/'reported-ledgers.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'worlds':len(rows),'outputs':audit['outputs']}))
if __name__=='__main__':run()

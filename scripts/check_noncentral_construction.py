"""Post-hoc arithmetic check of F1; no model calls or empirical treatment effect."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def path(investment):
    stock = 12
    capacity = 4
    rows = []
    for episode in range(1, 9):
        supplied = 2 if episode == 1 else 0
        spent = investment if episode == 1 else 0
        available = stock + capacity + supplied - spent
        consumed = min(6, available)
        stock = available - consumed
        capacity_next = capacity + spent / 3
        rows.append(dict(episode=episode, supply=supplied, investment=spent,
                         closing=stock, capacity_next=capacity_next, unmet=6-consumed))
        capacity = capacity_next
    return rows

def main():
    independent = path(6)
    unchanged = path(0)
    report = {
        'analysis_status': 'Post-hoc construction, separate from preregistered model trials.',
        'scope': 'Each of H and Z separately; identical initial resources, voluntary own investment.',
        'assumptions': ['Initial supply contract is fulfilled in episode 1.',
                        'Investment 6 succeeds at the stated cost and raises owned capacity to 6.',
                        'Need and production stay 6; no extra shocks, maintenance costs, transfers or confiscation.',
                        'The actor can continue using its equipment and knowledge.'],
        'invariant': {'base_stock_end_episode_1': independent[0]['closing'],
                      'step_stock_change_after_supply_stop': 6-6,
                      'argument': 'Base B(1)=6. For all t>=1, B(t+1)=B(t)+6-6=B(t), so B(t)=6 and unmet need is zero under the assumptions.'},
        'construction': independent,
        'no_investment_counterfactual': unchanged,
        'checks': {'initial_stock_is_6': independent[0]['closing']==6,
                   'computed_construction_keeps_stock': all(r['closing']==6 and r['unmet']==0 for r in independent),
                   'counterfactual_first_shortage_episode_8': next(r['episode'] for r in unchanged if r['unmet'])==8},
        'limits': ['The induction is conditional, not inferred from eight successful observations.',
                   'This is not an observed N/U comparison: N can also invest.',
                   'No claim of protection against equipment seizure, all forms of domination, or real-world feasibility.',
                   'Ordinary self-provision is not a new mechanism invented by these protocols. Their role in generating or implementing it is a separate question.']
    }
    target = ROOT/'docs/noncentral-construction-check.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['checks']))
    if not all(report['checks'].values()):
        raise SystemExit(1)

if __name__ == '__main__':
    main()

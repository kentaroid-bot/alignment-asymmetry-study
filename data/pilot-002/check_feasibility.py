"""Finite engine calculation, not another model actor or observed behaviour."""
import itertools
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'runtime'))
import trial as t
records=[]
for state in (0,1):
    paths=[]
    for actions in itertools.product(t.B.ACTIONS,repeat=2):
        stock=120;rows=[]
        for event,action in zip(t.B.event_table(state,'E1')[:2],actions):
            row=t.B.transition(stock,event,dict(P=action,Q=action));stock=row['stock_after'];rows.append(row)
        game=dict(complete=True,setting=dict(world='B'),rounds=rows,stock=stock)
        paths.append(dict(actions=actions,metrics=t.metrics(game)))
    states=[]
    for event in t.B.event_table(state,'E1')[:2]:
        available_rows=[t.B.transition(120,event,dict(P=a,Q=a)) for a in t.B.ACTIONS]
        states.append(dict(round=event['round'],Z_demand=event['demands']['Z'],consent_required=.75*event['demands']['Z'],
                           largest_possible_Z_allocation=max(r['allocations']['Z'] for r in available_rows),
                           consent_feasible_with_full_resource=any(r['true_authority']['Z_consents'] for r in available_rows)))
    records.append(dict(world='B',state=state,rounds=states,possible_effective_paths=len(paths),
                        minimum_H=min(p['metrics']['H'] for p in paths),
                        paths_with_minimum_H=[p for p in paths if p['metrics']['H']==min(x['metrics']['H'] for x in paths)]))
t.save(ROOT/'feasibility.json',{'kind':'deterministic_full_event_information_reference_not_actor','records':records})
print(t.dump(records))

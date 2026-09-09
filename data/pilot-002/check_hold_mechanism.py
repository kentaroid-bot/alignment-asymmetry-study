"""Post-observation one-step counterfactual; not a new actor or policy recommendation."""
import copy
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'runtime'))
import trial as t

records=[]
for path in sorted((ROOT/'games').glob('*.json')):
    game=json.loads(path.read_text())
    if not game['complete'] or game['setting']['world']!='A':continue
    for row in game['rounds']:
        for group in ('P','Q'):
            if row['decisions'][group]['action']!='HOLD' or row['proposals'].get(group) is None:continue
            changed=copy.deepcopy(row['decisions'])
            changed[group]=dict(action='REQUEST',allocation=row['proposals'][group]['proposal'],note='counterfactual_own_proposal')
            cf=t.A.resolve(row['environment'],changed,row['proposals'],motive='M2',gate='G0')
            records.append(dict(setting=game['setting'],round=row['environment']['round'],group=group,
                actual_action='HOLD',counterfactual_action=changed[group],opponent_action_fixed=row['decisions']['Q' if group=='P' else 'P'],
                actual={k:row[k] for k in ('H','C','unauthorized_execution','executed','reward')},
                counterfactual={k:cf[k] for k in ('H','C','unauthorized_execution','executed','reward')}))
t.save(ROOT/'hold-mechanism.json',dict(kind='post_observation_one_step_counterfactual',
    limitation='Only replaces one saved action, holding the simultaneous opponent answer and current environment fixed. Does not estimate how changing Unflatten changes behaviour, later reactions, or what should be authorized.',records=records))
print(t.dump(dict(cases=len(records),H_reduced=sum(r['counterfactual']['H']<r['actual']['H'] for r in records),H_unchanged=sum(r['counterfactual']['H']==r['actual']['H'] for r in records))))

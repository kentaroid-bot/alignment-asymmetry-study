"""Conditional participation constraint; not a simulation of all infinite play."""
import itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def participation_bound(reserve, exit_cost, alternative, need=6, gross=12):
    # One-time exit cost can be financed from reserve, ongoing alternative covers need.
    feasible=reserve>=exit_cost and alternative>=need
    # Stylized best-response participation constraint, no coercion beyond dependency.
    bound=max(0,gross-max(need,alternative)) if feasible else gross-need
    return {'exit_feasible':feasible,'dependency_rent_bound':bound}
def run():
    rows=[]
    for b,k,a in itertools.product([0,6,12,24],[0,4,12,24],[4,6,8,10,12]):
        rows.append({'reserve':b,'exit_cost':k,'alternative':a,**participation_bound(b,k,a)})
    # Each row is an assumption-conditioned calculation, not an empirical frequency.
    out={'assumptions':{'need':6,'gross':12,'grid':'4 reserves x 4 exit costs x 5 alternatives',
      'meaning':'Affordable sufficient alternative bounds extractable dependency rent under the stated participation constraint. No Unflatten effect is estimated.'},
      'rows':rows,'feasible':sum(r['exit_feasible'] for r in rows),'lower_bound':sum(r['dependency_rent_bound']<6 for r in rows),
      'zero_bound':sum(r['dependency_rent_bound']==0 for r in rows),
      'countermodel':{'description':'A harmful institution with continuing voluntary internal production can benefit from lower internal coordination costs, while external harm is unchanged.',
          'internal_output':12,'maintenance_before':4,'maintenance_after':2,'surplus_before':8,'surplus_after':10,
          'status':'Logical countermodel to open-ended continuation alone implying no UMH benefit. NOT an observed Unflatten improvement.'}}
    (ROOT/'mechanism-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['feasible','lower_bound','zero_bound']}))
if __name__=='__main__':run()

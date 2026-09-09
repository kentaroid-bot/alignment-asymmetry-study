"""Check frozen observations and enumerate all actions; never calls a model."""
import hashlib, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'experiments/component-gate-v1'
spec=importlib.util.spec_from_file_location('study',base/'study.py');study=importlib.util.module_from_spec(spec);spec.loader.exec_module(study)
frozen=json.loads((base/'frozen.json').read_text());rows=[]
for name,h in frozen['files'].items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==h,name
for c in frozen['cases']:
 assert hashlib.sha256((base/'inputs'/f'{c["id"]}.txt').read_bytes()).hexdigest()==c['prompt_sha256']
 r=json.loads((base/'outputs'/f'{c["id"]}.json').read_text());assert r['case']==c;assert r['status']=='valid'
 assert json.loads(r['raw'])==r['parsed'];assert r['metrics']==study.score(c,r['parsed']['choice'])
 assert isinstance(r['parsed']['note'],str);assert len(r['parsed']['note'])<=120
 assert all(a['returncode']==0 and not a['unexpected_item_types'] for a in r['attempts'])
 rows.append(r)
checks=[]
for f in [0,1]:
 for g in [0,1]:
  for choice in ['k2','k7','k4','k9','HOLD']:
   m=study.score({'fixture':f,'gate':g},choice)
   if g==1:assert m['unauthorized_execution']==0
   checks.append({'fixture':f,'gate':g,'choice':choice,**m})
usage={}
for r in rows:
 for a in r['attempts']:
  for k,v in (a['usage'] or {}).items():usage[k]=usage.get(k,0)+v
report={'frozen_hashes':'match','cases_replayed':len(rows),'valid_choices':len(rows),'technical_attempts':sum(len(r['attempts']) for r in rows),'usage_totals':usage,'all_action_enumeration':checks,'interpretation':'Post-observation deterministic verification of a preregistered gate property; not additional model observations.'}
(base/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='all_action_enumeration'},ensure_ascii=False))

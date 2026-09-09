"""Replay only saved actor answers to verify transitions and input boundaries."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'runtime'))
import trial as t

frozen=json.loads((ROOT/'frozen.json').read_text())
for name,h in frozen['runtime_hashes'].items():
    assert t.sha((ROOT/name).read_bytes())==h
records=[]
for setting in frozen['games']:
    path=ROOT/'games'/(setting['id']+'.json')
    if not path.exists():continue
    saved=json.loads(path.read_text())
    if not saved['complete']:continue
    replay=t.new_game(setting)
    for c in saved['calls']:
        t.prepare(replay)
        call=replay['pending'][0]
        for key in ('id','group','role','round','prompt','prompt_sha256'):
            assert call[key]==c[key],(setting['id'],key)
        parsed=t.parse(c['raw_output'],replay,c['role']) if c['parsed'] is not None else None
        assert parsed==c['parsed']
        assert all(not m['unexpected_tool_items'] and m['model_requested']=='gpt-6-astra' and m['reasoning_requested']=='high' for m in c['attempts'])
        t.accept(replay,call,c['raw_output'],parsed,c['attempts'])
    for key in ('history','rounds','complete','stock'):
        assert replay[key]==saved[key],(setting['id'],key)
    assert t.metrics(replay)==saved['metrics']
    records.append(dict(id=setting['id'],calls=len(saved['calls']),status='passed'))
report={'runtime_hashes':'unchanged','completed_game_count':len(records),'decisions_replayed':sum(r['calls'] for r in records),'games':records,
        'scope':'saved inputs, final answers, transitions, histories, metrics and requested model settings; not a provider-side identity or total OS isolation audit'}
t.save(ROOT/('preflight-audit.json' if len(records)<=2 else 'final-audit.json'),report)
print(t.dump(report))

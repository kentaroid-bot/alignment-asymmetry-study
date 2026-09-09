"""Reconstruct saved prompts and trajectories without calling a model."""
import argparse, importlib.util, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'experiments/open-world-v1'
spec=importlib.util.spec_from_file_location('open_world_study',D/'study.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(p):return json.loads(p.read_text())
def verify(require_complete=False):
    frozen=m.frozen(); outputs={p.stem:read(p) for p in sorted((D/'outputs').glob('*.json'))}
    errors=[];checked=0;char_excess=[];world_char_excess=[];planning_char_excess=[];planning_checked=[]
    expected_ids={f'planning-{arm}-{step}' for arm in ['A','B'] for step in [1,2]}
    expected_ids.update(f'{case["id"]}-{ep}-{role}' for case in frozen['cases'] for ep in range(1,4) for role in ['H','Q','world'])
    for cid in sorted(set(outputs)-expected_ids):errors.append(cid+':unexpected_receipt')
    # Replace the sole model-call function before replaying the frozen planning constructor.
    # This captures prompts and returns saved answers; it cannot invoke the CLI.
    original_call=m.call
    def saved_planning_call(cid,prompt):
        if cid not in outputs:return {'status':'missing'}
        if prompt!=(D/'inputs'/f'{cid}.txt').read_text():errors.append(cid+':prompt_reconstruction')
        planning_checked.append(cid)
        return outputs[cid]
    m.call=saved_planning_call
    try:m.planning()
    finally:m.call=original_call
    for cid,r in outputs.items():
        p=(D/'inputs'/f'{cid}.txt').read_text()
        if hashlib.sha256(p.encode()).hexdigest()!=r['prompt_sha256']:errors.append(cid+':input_hash')
        if r['status']=='valid' and m.parse(r['raw'])!=r['parsed']:errors.append(cid+':raw_parse')
        if any(a['unexpected_item_types'] for a in r['attempts']):errors.append(cid+':tool_used')
        if '-planning' not in cid and cid[-1:] in ['H','Q'] and r['status']=='valid':
            for key,limit in [('public_proposal',600),('new_possibility',250),('private_record',250),('foregone_future',200)]:
                if isinstance(r['parsed'].get(key),str) and len(r['parsed'][key])>limit:
                    char_excess.append({'id':cid,'field':key,'length':len(r['parsed'][key]),'limit':limit})
        if cid.endswith('-world') and r['status']=='valid':
            for key,limit in [('narrative',800),('institutions',400),('new_activities',350),('pending',400),('power_and_harm',350)]:
                if isinstance(r['parsed'].get(key),str) and len(r['parsed'][key])>limit:
                    world_char_excess.append({'id':cid,'field':key,'length':len(r['parsed'][key]),'limit':limit})
            for index,value in enumerate(r['parsed'].get('next_futures',[])):
                if isinstance(value,str) and len(value)>200:
                    world_char_excess.append({'id':cid,'field':f'next_futures[{index}]','length':len(value),'limit':200})
        if cid.startswith('planning-') and r['status']=='valid':
            for key,limit in [('method',1600),('example_future',800)]:
                if isinstance(r['parsed'].get(key),str) and len(r['parsed'][key])>limit:
                    planning_char_excess.append({'id':cid,'field':key,'length':len(r['parsed'][key]),'limit':limit})
    for case in frozen['cases']:
        history=[];own={'H':[],'Q':[]};episodes=[]
        for ep in range(1,4):
            rr={}
            for role in ['H','Q']:
                cid=f'{case["id"]}-{ep}-{role}'
                if cid not in outputs:continue
                expected=m.actor_prompt(case,ep,role,history,own[role])
                if expected!=(D/'inputs'/f'{cid}.txt').read_text():errors.append(cid+':prompt_reconstruction')
                rr[role]=outputs[cid];checked+=1
            if len(rr)<2 or any(r['status']!='valid' for r in rr.values()):break
            cid=f'{case["id"]}-{ep}-world'
            if cid not in outputs:break
            props={role:{k:rr[role]['parsed'][k] for k in ['public_proposal','new_possibility','foregone_future']} for role in rr}
            if m.world_prompt(ep,history,props)!=(D/'inputs'/f'{cid}.txt').read_text():errors.append(cid+':prompt_reconstruction')
            checked+=1;wr=outputs[cid]
            if wr['status']!='valid':break
            state=wr['parsed'];history.append({'episode':ep,'proposals':props,'state':state})
            for role in own:own[role].append(rr[role]['parsed'])
            episodes.append({'episode':ep,'status':'recorded','state':state})
        path=D/'trajectories'/f'{case["id"]}.json'
        if path.exists():
            saved=read(path)['episodes']
            if [e for e in saved if e['status']=='recorded']!=episodes:errors.append(case['id']+':trajectory')
    if require_complete:
        for cid in sorted(expected_ids-set(outputs)):errors.append(cid+':missing_receipt')
    report={'outputs':len(outputs),'reconstructed_world_prompts':checked,'reconstructed_planning_prompts':len(planning_checked),'errors':errors,'actor_character_limit_excess':char_excess,'world_character_limit_excess':world_char_excess,'planning_character_limit_excess':planning_char_excess,
        'meaning':'Mechanical record consistency only. Ledger findings are in audit.json; social causality and real consent remain unverified.'}
    (D/'record-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--complete',action='store_true');a=p.parse_args();verify(a.complete)

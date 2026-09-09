"""Reconstruct saved prompts and trajectories without calling a model."""
import argparse, importlib.util, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'experiments/open-world-v1'
spec=importlib.util.spec_from_file_location('open_world_study',D/'study.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(p):return json.loads(p.read_text())
def verify(require_complete=False):
    frozen=m.frozen(); outputs={p.stem:read(p) for p in sorted((D/'outputs').glob('*.json'))}
    errors=[];checked=0;char_excess=[]
    for cid,r in outputs.items():
        p=(D/'inputs'/f'{cid}.txt').read_text()
        if hashlib.sha256(p.encode()).hexdigest()!=r['prompt_sha256']:errors.append(cid+':input_hash')
        if r['status']=='valid' and m.parse(r['raw'])!=r['parsed']:errors.append(cid+':raw_parse')
        if any(a['unexpected_item_types'] for a in r['attempts']):errors.append(cid+':tool_used')
        if '-planning' not in cid and cid[-1:] in ['H','Q'] and r['status']=='valid':
            for key,limit in [('public_proposal',600),('new_possibility',250),('private_record',250),('foregone_future',200)]:
                if isinstance(r['parsed'].get(key),str) and len(r['parsed'][key])>limit:
                    char_excess.append({'id':cid,'field':key,'length':len(r['parsed'][key]),'limit':limit})
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
    if require_complete and len(outputs)!=112:errors.append('Expected 112 final receipts')
    report={'outputs':len(outputs),'reconstructed_world_prompts':checked,'errors':errors,'actor_character_limit_excess':char_excess,
        'meaning':'Mechanical record consistency only. Ledger findings are in audit.json; social causality and real consent remain unverified.'}
    (D/'record-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--complete',action='store_true');a=p.parse_args();verify(a.complete)

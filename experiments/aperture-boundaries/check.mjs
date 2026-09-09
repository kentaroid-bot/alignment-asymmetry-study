// Unmodified upstream functions, with only TypeScript/module syntax removed by Node.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
import { fileURLToPath } from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const ctx=vm.createContext({crypto:crypto.webcrypto});
const hashes={};
for(const file of ['constitution.ts','consensus.ts','safety.ts']){
 const source=fs.readFileSync(path.join(root,'vendor',file),'utf8');
 hashes[file]=crypto.createHash('sha256').update(source).digest('hex');
 const js=stripTypeScriptTypes(source).replace(/^import .+;$/gm,'').replace(/^export /gm,'');
 vm.runInContext(js,ctx);
}
const evalCode=(s)=>vm.runInContext(s,ctx);
evalCode(`var nodes=[{id:'n1',active:true},{id:'n2',active:true},{id:'n3',active:true}];
var votes=(ids)=>ids.map(memberId=>({memberId,decision:'approve',revisionId:'r1'}));
var validLease={id:'l1',scope:['safety-check'],purpose:'check',issuedAt:'2026-01-01T00:00:00Z',expiresAt:'2026-01-01T00:05:00Z'};`);
const tests=[
 ['reject_blocked_exit','inspectPatch({blocksExit:true},"member").ok',false],
 ['reject_sos_disable','inspectPatch({disablesSos:true},"member").ok',false],
 ['reject_private_sharing_without_consent','inspectPatch({sharesPrivateMonkuOf:["n1"]},"member").ok',false],
 ['accept_consented_private_sharing','inspectPatch({sharesPrivateMonkuOf:["n1"]},"member",["n1"]).ok',true],
 ['reject_removed_veto','inspectPatch({removesProtectedVeto:true},"member").ok',false],
 ['reject_ai_activation','inspectPatch({status:"active"},"ai").ok',false],
 ['reject_automatic_physical_restriction','inspectPatch({automaticPhysicalRestriction:true},"member").ok',false],
 ['reject_audit_deletion','inspectPatch({requiresAuditDeletion:true},"member").ok',false],
 ['reject_missing_ttl','inspectLease({scope:["safety-check"],purpose:"check"}).ok',false],
 ['accept_valid_lease','inspectLease(validLease).ok',true],
 ['expire_valid_lease','leaseState(validLease,new Date("2026-01-01T00:06:00Z"))','expired'],
 ['reject_automatic_renewal','(()=>{try{renewLease();return false}catch{return true}})()',true],
 ['reject_rights_change_without_owner','evaluateConsensus({kind:"shared-resource",affectedNodes:nodes,consents:votes(["n1","n2"]),rightsRestrictedFor:["n3"]}).accepted',false],
 ['accept_qualified_majority','evaluateConsensus({kind:"shared-resource",affectedNodes:nodes,consents:votes(["n1","n2"])}).accepted',true],
 ['reject_nonmember_votes','evaluateConsensus({kind:"shared-resource",affectedNodes:nodes,consents:votes(["outsider1","outsider2"])}).accepted',false],
 ['reject_same_subject_and_verifier','canSafetySubjectSelfRelease("n1",["n1"],"n1")',false],
 ['reject_invalid_date_strings','inspectLease({...validLease,issuedAt:"invalid",expiresAt:"invalid"}).ok',false],
 ['invalid_expiry_not_active','leaseState({...validLease,expiresAt:"invalid"},new Date("2026-01-01T00:06:00Z"))!=="active"',true],
];
const results=tests.map(([name,expression,expected])=>{const observed=evalCode(expression);return {name,expression,expected,observed,property_holds:observed===expected}});
const report={source_commit:'d2852300dd69b1b08c89b0b537970e112496e697',node_version:process.version,source_hashes:hashes,scope:'Domain function input boundaries; not an end-to-end UI or deployed exploit test.',test_selection:'Exploratory, selected after source inspection; not a representative or preregistered sample of all requirements.',results};
fs.writeFileSync(path.join(root,'results.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({checked:results.length,hold:results.filter(x=>x.property_holds).length,gaps:results.filter(x=>!x.property_holds).map(x=>x.name)}));

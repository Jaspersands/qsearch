"use strict";
// Exact effect, causal transcript, posterior-phase and source-cost certificates.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_phase_feedback.json"),"utf8"));
function check(x,m){if(!x)throw Error(m);}
const mod=(x,q)=>(x%q+q)%q,same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a;}
function F(a,b=1n){check(b!==0n,"denominator");if(b<0n)[a,b]=[-a,-b];const g=gcd(a,b);return[a/g,b/g];}
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]),eq=(a,b)=>a[0]*b[1]===b[0]*a[1],le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
function Q(x){check(typeof x==="string","rational string");const t=x.split("/");check(t.length<=2,"rational syntax");const v=F(BigInt(t[0]),t.length===2?BigInt(t[1]):1n);check(x===(v[1]===1n?String(v[0]):v[0]+"/"+v[1]),"canonical rational");return v;}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_PHASE_FEEDBACK.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="COSTED_PUBLIC_PHASE_FEEDBACK_ACCESS_AUDIT_REVIEW_PENDING","derivation review status");
for(const k of["quantum_speedup_proved","candidate_record_accepted","novelty_claim","original_DCP_inputs_classically_simulated","arbitrary_non_covariant_or_collective_readouts_covered"])check(report[k]===false,"scope not a general dequantization: "+k);

function put(poly,e,c,q){e=mod(e,q);const terms=e<2*q/3?[[e,c]]:[[e-2*q/3,-c],[e-q/3,-c]];for(const[x,v]of terms){const a=(poly.get(x)||0n)+v;if(a)poly.set(x,a);else poly.delete(x);}}
function encoded(poly){return[...poly].sort((a,b)=>a[0]-b[0]).map(([e,c])=>[String(e),String(c)]);}
let effectEntries=0,orbitEntries=0;
for(const q of[3,9,27])for(const[alpha,beta]of[[0,0],[1,q-1],[q-1,1]]){
  const settings=[0,alpha,beta];
  for(let y1=0;y1<q;y1++)for(let y2=0;y2<q;y2++){const y=[0,y1,y2],raw=[0,mod(y1+alpha,q),mod(y2+beta,q)];for(let i=0;i<3;i++)for(let j=0;j<3;j++){check(mod(y[i]-y[j]+settings[i]-settings[j],q)===mod(raw[i]-raw[j],q),"arbitrary-input covariant effect identity");effectEntries++;}}
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){const sum=new Map();for(let z=0;z<3;z++){const y=[0,mod(alpha+q/3*z,q),mod(beta+2*q/3*z,q)];put(sum,y[i]-y[j],1n,q);}same(encoded(sum),i===j?[["0","3"]]:[],"exact orbit effect equals3I/q^2");orbitEntries++;}
}
check(report.physical_phase_and_filter_controls.length===27,"complete prespecified native phase schedule");let index=0;
for(const q of[3,9,27])for(const s of[0,3%q,q-1])for(const settings of[[0,0],[1,q-1],[q-1,1]]){
  const c=report.physical_phase_and_filter_controls[index++];same([c.modulus,c.first,c.second,c.calibration_secret,c.public_phase_pair],[q,[1],[q-1],[s],settings],"actual native phase control");
  check(eq(Q(c.orbit_acceptance_probability),F(3n,BigInt(q*q)))&&c.all_covariant_outcomes_kept_in_control===q*q&&c.calibration_secret_not_an_input_to_policy_or_decoder===true,"complete physical orbit cost/law");
  for(const k of["covariant_output_relabel_residual","orbit_acceptance_residual","fixed_trine_conditional_Born_residual"])check(Number.isFinite(c[k])&&c[k]>=0&&c[k]<3e-11,"physical law residual: "+k);
}

function choose(policy,first,second,q,history){if(policy.kind==="zero")return[0,0];if(policy.kind==="known_offset")return[first,second].map(row=>mod(row.reduce((s,a,j)=>s+a*policy.known_offset[j],0),q));check(policy.kind==="quadratic_feedback","auditable causal policy");const f=mod(history.reduce((s,[a,b])=>s+a+2*b,0),q);return[mod(first.reduce((s,a,j)=>s+a*a+second[j],0)+f+history.length,q),mod(first.reduce((s,a,j)=>s+a*second[j],0)+f*f*f-history.length,q)];}
const roots=[[1,0],[-1,0],[0,1],[0,-1],[1,-1],[-1,1]];
function exactPosteriorCoefficients(records,q){let table=new Map([[0,new Map([[0,1n]])]]);for(const r of records){const terms=[[0,0,3n],...roots.map(([u,v])=>[mod(-u*r.first[0]-v*r.second[0],q),mod(u*r.outcome[0]+v*r.outcome[1],q),1n])],next=new Map();for(const[f,poly]of table)for(const[g,e,w]of terms){const key=mod(f+g,q);if(!next.has(key))next.set(key,new Map());for(const[h,c]of poly)put(next.get(key),h+e,c*w,q);}table=next;}return[0,q/3,2*q/3].map(f=>encoded(table.get(f)||new Map()));}
check(report.causal_feedback_controls.length===3,"all causal policies");const policyNames=["zero","known_offset","quadratic_feedback"];
let originals=null;
report.causal_feedback_controls.forEach((c,j)=>{check(c.policy.kind===policyNames[j]&&c.readout_model==="FULL_ROOT_COVARIANT","readout model not fixed trine");
  check(c.steps.length===4&&c.cost_ledger.supplied_covariant_records_consumed===4&&c.cost_ledger.new_source_records_or_unknown_phase_states_created===0&&c.cost_ledger.public_policy_evaluation_calls===4&&c.cost_ledger.policy_computation_is_classical_and_must_be_charged===true,"conserved sources/public classical cost");
  check(c.original_unknown_states_or_DCP_classically_simulated===false&&c.arbitrary_non_diagonal_or_collective_operations_covered===false&&c.source_independence_not_proved_by_unique_IDs===true&&c.prespecified_frequency_rows_not_IID_population_evidence===true,"coupling not a classical input simulator");
  const history=[],raw=[];
  for(let i=0;i<4;i++){const step=c.steps[i],q=step.modulus;check(q===9&&step.original_id===i,"source ancestor schedule");const phase=choose(c.policy,step.first,step.second,q,history);same(step.phase_pair,phase,"causal policy uses no current/future outcome");const recovered=step.reported_outcome.map((y,k)=>mod(y+phase[k],q));raw.push({first:step.first,second:step.second,outcome:recovered,modulus:q});history.push(step.reported_outcome);}
  same(raw,c.original_supplied_records_calibration_only,"exact invertible full transcript");if(originals===null)originals=raw;else same(raw,originals,"same source pool across policies");
  const result=c.exact_feedback_removed_posterior;check(result.feedback_removed_by_exact_classical_inverse===true&&result.feedback_adds_information_about_secret===false&&result.physical_covariant_record_source_still_required===true,"no extra information/no source acquisition");
  same(result.coefficient_numerators,exactPosteriorCoefficients(raw,9),"independent exact seven-term posterior after removing feedback");same(result.records,raw,"posterior uses recovered raw records, not a changed observation law");
});

const schedule=[4,8,16,32,64];check(report.scaling_resampling_ledgers.length===5,"source-cap scaling schedule");
report.scaling_resampling_ledgers.forEach((c,i)=>{const r=schedule[i],T=r-2,K=T*r*r,q=3n**BigInt(r),p=F(3n,q*q),fill=div(mul(F(BigInt(K)),p),F(BigInt(T))),bound=le(fill,F(1n))?fill:F(1n);
  check(c.digits===r&&c.modulus===String(q)&&c.target_fixed_basis_records===T&&c.maximum_covariant_source_records===K,"source budget geometry");
  for(const[k,v]of[["acceptance_probability_per_consumed_record",p],["uncapped_expected_covariant_records",div(F(BigInt(T)),p)],["expected_accepted_records_under_cap",mul(F(BigInt(K)),p)],["probability_of_filling_target_upper_by_Markov",bound]])check(eq(Q(c[k]),v),"exact resampling source formula: "+k);
  check(c.cost_polynomial_in_q_not_log_q===true&&c.polynomial_in_n_only_if_q_is_polynomial_and_source_supply_permits===true&&c.batch_label_lookahead_fixed_trine_compilation_covered===false&&c.same_record_can_be_retried_as_fresh_source===false&&c.input_states_classically_simulated===false,"parameter regime and access scope");
});
const shortage=report.finite_shortage_control,accepted=[],rejected=[];
originals.forEach((r,i)=>{const q=r.modulus,Q0=q/3;if(r.outcome[0]%Q0===0&&r.outcome[1]===mod(2*r.outcome[0],q)){const z=r.outcome[0]/Q0;accepted.push({digit:z,phase_pair:[0,0],first:r.first,second:r.second,modulus:q,fixed_trine_phases_are_not_paired_covariant_outcomes:true,original_id:i});}else rejected.push(i);});
same(shortage.accepted_records,accepted,"every accepted source record");same(shortage.rejected_original_ids,rejected,"every failed source record charged");same(shortage.consumed_original_ids,[0,1,2,3],"no cloning/resampling same ancestor");same(shortage.unused_original_ids,[],"finite stream accounting");
check(accepted.length<4&&shortage.status==="SOURCE_CAP_EXHAUSTED_NO_COMPLETE_FIXED_TRINE_STREAM"&&shortage.cost_ledger.supplied_covariant_records_consumed===4&&shortage.cost_ledger.conditional_success_not_treated_as_unconditional===true&&shortage.quantum_unknown_states_classically_simulated===false,"shortage not hidden as success");
console.log(JSON.stringify({status:"independent_public_phase_feedback_certificates_passed",effectEntries,orbitMatrixEntries:orbitEntries,physicalControls:27,causalTranscripts:3,exactPosteriors:3,sourceLedgers:5,finiteShortagePreserved:true,originalDCPClassicallySimulated:false}));

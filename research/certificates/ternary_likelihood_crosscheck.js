"use strict";
// Direct Born likelihood Gram and exact rational ledgers, independent of Python.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../classical_baselines/ternary_likelihood_gate.json"),"utf8"));
function check(x,message){if(!x)throw Error(message);}
function mod(x,q=3){return((x%q)+q)%q;}
function dot(a,b,q){return mod(a.reduce((v,x,i)=>v+x*b[i],0),q);}
function likelihood(a,c,s,q,b,o){
  const A=2*Math.PI*(dot(a,s,q)/q-(b+o)/3),C=2*Math.PI*(dot(c,s,q)/q-(4*b+2*o)/3);
  return((1+Math.cos(A)+Math.cos(C))**2+(Math.sin(A)+Math.sin(C))**2)/3;
}
function gcd(a,b){while(b){[a,b]=[b,a%b];}return a;}
function rational(a,b=1n){const d=gcd(a,b);return[a/d,b/d];}
function parse(s){const v=s.split("/").map(BigInt);return[v[0],v[1]||1n];}
function sameFraction(x,y,message){check(x[0]*y[1]===y[0]*x[1],message);}
let records=0,gramEntries=0;
for(const control of report.dense_native_source_controls){
  const q=control.phase_modulus,S=control.secret_vectors,N=S.length,gram=Array.from({length:N},()=>Array(N).fill(0));
  let count=0;
  for(const a of S)for(const c of S)for(let b=0;b<3;b++)for(let o=0;o<3;o++){
    const centered=S.map(s=>likelihood(a,c,s,q,b,o)-1);
    for(let i=0;i<N;i++)for(let j=0;j<N;j++)gram[i][j]+=centered[i]*centered[j];count++;
  }
  check(count===control.complete_public_label_basis_outcome_records,"complete source count");
  for(let i=0;i<N;i++)for(let j=0;j<N;j++){
    const x=gram[i][j]/count;check(Math.abs(x-(i===j?2/3:0))<1e-12,"orthogonal native likelihoods");
    check(Math.abs(x-control.centered_Gram_matrix[i][j])<1e-12,"report Gram replay");gramEntries++;
  }records+=count;
}
for(const c of report.SQ_scaling_ledgers){
  const N=3n**BigInt(c.dimension*c.root_digits),k=BigInt(c.records_per_query),a=5n**k,b=3n**k,d=[a-b,b],tau=parse(c.absolute_tolerance);
  check(BigInt(c.secret_count)===N,"secret count");sameFraction(parse(c.centered_likelihood_norm_squared),d,"k-record norm");
  const affected=(d[0]*tau[1]*tau[1])/(d[1]*tau[0]*tau[0]);check(BigInt(c.secrets_affected_per_reference_answer_upper)===affected,"Bessel bound");
  const upper=BigInt(c.bounded_expectation_queries)*affected+1n;
  sameFraction(parse(c.uniform_secret_identification_success_upper),upper>N?[1n,1n]:rational(upper,N),"SQ success gate");
  check(!c.raw_samples_or_growing_arity_joint_inference_ruled_out && !c.source_label_adaptive_measurements_covered && !c.general_classical_hardness_proved,"SQ scope promoted");
}
for(const c of report.near_entropy_observation_ledgers){
  const M=BigInt(c.measurement_records),N=3n**BigInt(c.dimension*c.root_digits),a=5n**M,b=3n**M*N;
  sameFraction(parse(c.uniform_secret_success_squared_upper),a>b?[1n,1n]:rational(a,b),"observation density gate");
  check(!c.arbitrary_or_collective_quantum_measurements_covered && !c.more_legitimately_charged_records_ruled_out,"density scope promoted");
}
const easy=report.raw_sample_field_decoder_counterexample,s=easy.result.secret;
check(easy.result.status==="FIELD_SECRET_CERTIFIED" && easy.result.phase_modulus===3 && easy.result.rank===easy.result.feature_dimension-1,"mandatory known-easy counterexample missing");
for(const c of easy.public_measurement_records){const A=mod(dot(c.alpha,s,3)-c.outcome),B=mod(dot(c.beta,s,3)-c.basis);check(mod((1-B*B)*A)===0,"counterexample constraints");}
check(Object.values(report.claim_gate).every(x=>x===false),"native lower bound promoted to algorithm/hardness");
console.log(JSON.stringify({status:"independent_replay_passed",complete_native_classical_records:records,
  likelihood_Gram_entries:gramEntries,SQ_ledgers:report.SQ_scaling_ledgers.length,
  known_easy_raw_sample_counterexample:true,new_algorithm:false}));

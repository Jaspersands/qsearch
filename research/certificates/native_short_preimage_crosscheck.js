"use strict";
// Original-data receipts, complete bounded helper costs and exact moment ledgers.
// This replays the reduction, not a scalable preimage solver or source-law proof.
const fs=require("fs"), path=require("path"), crypto=require("crypto");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one}=require("./cyclotomic_exact.js");
const ROOT=path.resolve(__dirname,"../.."), REPORT=path.join(ROOT,"research/reductions/native_short_preimage_reduction.json");
const LABEL="LABEL_ONLY_HELPER_INDEPENDENT_ZERO_MEAN_ORIGINAL_ERRORS";
const GLOBAL="GLOBAL_ORIGINAL_MOMENT_BOUNDED_WORDS_DATA_DEPENDENCE_ALLOWED";
const COMPLETE="COMPLETE_RECEIPT_CHECKED_CLASSICAL_RECONSTRUCTION", INCOMPLETE="INCOMPLETE_SHORT_PREIMAGE_HELPER";
const mod=(x,q)=>(x%q+q)%q;
const encode=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const min=(a,b)=>cmp(a,b)<=0n?a:b;
const digest=x=>crypto.createHash("sha256").update(x).digest("hex");
function canonical(x) {
  if(Array.isArray(x))return x.map(canonical);
  if(x&&typeof x==="object")return Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])]));
  return x;
}
function digits(q) {
  check(q>=3n,"positive ternary modulus");
  let r=0; while(q%3n===0n){q/=3n;r++;}
  check(q===1n,"full ternary prime-power root"); return r;
}
function pos(x,label){check(Number.isSafeInteger(x)&&x>0,label);return x;}
function plan(n,q) {
  const r=digits(q), out=[];
  for(let i=0;i<n;i++)for(let d=0;d<r;d++)out.push({coordinate:i,digit:d,
    frequency:Array.from({length:n},(_,j)=>encode(i===j?3n**BigInt(r-1-d):0n))});
  return out;
}
function frequency(f,b,w) {
  check(Number.isSafeInteger(b)&&b>=0&&b<f.cohorts&&w.length===f.sites&&w.every(t=>Number.isInteger(t)&&t>=0&&t<3),"legal bounded word and cohort");
  const q=BigInt(f.modulus), out=Array(f.dimension).fill(0n);
  w.forEach((t,j)=>f.paired_labels[b][j][0].forEach((a,i)=>{
    const x=BigInt(a),y=BigInt(f.paired_labels[b][j][1][i]);out[i]=mod(out[i]+[x,y-x,-y][t],q);
  }));
  return out.map(encode);
}
function* words(M,prefix=[]) {
  if(prefix.length===M){yield prefix;return;}
  for(let t=0;t<3;t++)yield* words(M,[...prefix,t]);
}
function decode(probes,n,q) {
  const scheduled=plan(n,q), recovered=Array(n).fill(0n), decisions=[];
  check(probes.length===scheduled.length,"complete original-data probe batch");
  scheduled.forEach((p,j)=>{
    const row=probes[j];same(row.requested_frequency,p.frequency,"actual chosen-frequency order");
    const value=BigInt(row.derived_masked_response),i=p.coordinate;
    check(value>=0n&&value<q,"canonical observed response");
    const prefix=recovered[i],correction=mod(BigInt(p.frequency[i])*prefix,q),residual=mod(value-correction,q);
    const distances=[0n,1n,2n].map(k=>{
      const a=mod(residual-k*(q/3n),q),b=mod(k*(q/3n)-residual,q);return a<b?a:b;
    });
    const nearest=distances.reduce((a,b)=>a<b?a:b), selected=distances.map((x,k)=>x===nearest?k:-1).filter(k=>k>=0);
    check(selected.length===1,"unique integer nearest ternary centre");
    const trit=selected[0];recovered[i]+=BigInt(trit)*3n**BigInt(p.digit);
    decisions.push({...p,lower_prefix_before:encode(prefix),known_phase_correction:encode(correction),corrected_response:encode(residual),
      circular_integer_distances:distances.map(encode),chosen_trit:trit,lower_prefix_after:encode(recovered[i])});
  });
  return {masked:recovered.map(encode),decisions};
}
function control(c) {
  const result=c.result,f=result.public_family,raw=c.original_records,mask=c.known_mask,q=BigInt(f.modulus),n=pos(f.dimension,"positive original dimension");
  pos(f.cohorts,"positive cohorts");pos(f.sites,"positive sites");
  check((f.cohorts&(f.cohorts-1))===0,"power-two native cohorts");
  const count=f.cohorts*3**f.sites;
  check(Number.isSafeInteger(count)&&count<=512&&raw.length===2*f.cohorts*f.sites,"finite exhaustive control cap and paid data");
  check(new Set(raw.map(r=>r.source_id)).size===raw.length&&raw.every(r=>typeof r.source_id==="string"&&r.source_id.length>0),"unique actual original identities");
  check(mask.length===n&&mask.every(m=>BigInt(m)>=0n&&BigInt(m)<q),"known canonical mask");
  raw.forEach(r=>check(BigInt(r.modulus)===q&&r.label.length===n&&r.label.every(a=>BigInt(a)>=0n&&BigInt(a)<q)&&BigInt(r.value)>=0n&&BigInt(r.value)<q,"original canonical records"));
  const expected={modulus:String(q),dimension:n,cohorts:f.cohorts,sites:f.sites,
    paired_labels:Array.from({length:f.cohorts},(_,b)=>Array.from({length:f.sites},(_,j)=>raw.slice(2*(b*f.sites+j),2*(b*f.sites+j)+2).map(r=>r.label))),
    responses_masks_source_IDs_and_errors_supplied:false};
  same(f,expected,"helper contains only the actual original paired labels");
  const familyHash=digest(JSON.stringify(canonical(expected)));
  check(result.public_family_sha256===familyHash,"public-family fingerprint");
  const scheduled=plan(n,q);same(result.planned_probes,scheduled,"complete nonadaptive targets");
  const support=new Set();
  for(let b=0;b<f.cohorts;b++)for(const w of words(f.sites))support.add(JSON.stringify(frequency(f,b,w)));
  same(c.helper_cost,{kind:"BOUNDED_EXHAUSTIVE_LABEL_ONLY_CONTROL",word_evaluations:count,lookup_calls:scheduled.length,
    public_frequency_support:support.size,word_work_is_exponential_in_sites:true,polynomial_scalable_helper_supplied:false},"all exhaustive helper cost is charged");
  const missing=scheduled.filter(p=>!support.has(JSON.stringify(p.frequency)));
  const covered=scheduled.filter(p=>support.has(JSON.stringify(p.frequency))),probes=result.completed_probe_receipts;
  check(probes.length===covered.length,"all and only supported targets have receipts");
  probes.forEach((p,j)=>{
    const target=covered[j].frequency,r=p.receipt;
    check(r.public_family_sha256===familyHash,"receipt hash");same(r.target,target,"receipt target");
    same(frequency(f,r.cohort,r.word),target,"actual requested word preimage");
    let response=0n;const beta=Array(raw.length).fill(0),ids=[];
    r.word.forEach((t,k)=>[[1,0],[-1,1],[0,-1]][t].forEach((weight,l)=>{
      const i=2*(r.cohort*f.sites+k)+l,row=raw[i];beta[i]=weight;
      const masked=mod(BigInt(row.value)+row.label.reduce((s,a,d)=>s+BigInt(a)*BigInt(mask[d]),0n),q);
      response=mod(response+BigInt(weight)*masked,q);if(weight)ids.push(row.source_id);
    }));
    same(p,{requested_frequency:target,receipt:r,signed_original_coefficients:beta,
      coefficient_squared_norm:beta.reduce((s,b)=>s+b*b,0),derived_masked_response:encode(response),
      active_original_source_IDs:ids,fresh_original_errors_created:false},"exact signed original-data response and ancestry");
    check(p.coefficient_squared_norm<=2*f.sites,"true short coefficient norm");
  });
  check(result.helper_calls===scheduled.length&&result.original_records_paid_once===raw.length,"all batch helper calls and originals paid");
  ["helper_classical_polynomial_runtime_proved_by_receipts","helper_label_only_independence_proved_by_API","new_quantum_algorithm_or_speedup"].forEach(k=>check(result[k]===false,"receipt is not a proof of access or advantage: "+k));
  let recovered=null;
  if(missing.length) {
    check(result.status===INCOMPLETE&&result.original_secret===null&&result.partial_batch_promoted_to_recovery===false,"missing targets are not recovery");
    same(result.missing_probes,missing,"missing frequencies independently enumerated");
  } else {
    const d=decode(probes,n,q);recovered=d.masked.map((s,i)=>encode(mod(BigInt(s)-BigInt(mask[i]),q)));
    check(result.status===COMPLETE&&result.correctness_requires_the_stated_noise_bound===true,"conditional exact decoder only");
    same(result.masked_secret,d.masked,"trit reconstruction");same(result.original_secret,recovered,"known mask removal");same(result.decisions,d.decisions,"complete exact trit decisions");
  }
  const truth=c.truth_fixture_only;
  check(truth.masked_secret.length===n&&truth.original_secret.length===n&&truth.original_errors.length===raw.length,"complete truth fixture only");
  same(truth.masked_secret,truth.original_secret.map((s,i)=>encode(mod(BigInt(s)+BigInt(mask[i]),q))),"truth mask consistent");
  raw.forEach((r,j)=>check(mod(r.label.reduce((s,a,i)=>s+BigInt(a)*BigInt(truth.original_secret[i]),0n)+BigInt(truth.original_errors[j]),q)===BigInt(r.value),"actual fixture errors and original data agree"));
  check(c.matches_truth_fixture===(JSON.stringify(recovered)===JSON.stringify(truth.original_secret)),"wrong noisy outputs preserved");
  check(c.secret_or_errors_used_by_decoder===false&&c.bounded_control_is_a_scalable_solver===false,"finite truth control, not algorithm claim");
  return {words:count,probes:probes.length,missing:missing.length,noisyFailure:recovered!==null&&!c.matches_truth_fixture};
}
function ledger(L) {
  const n=pos(L.dimension,"dimension"),B=pos(L.cohorts,"cohorts"),M=pos(L.sites,"sites"),q=BigInt(L.modulus),r=digits(q);
  check((B&(B-1))===0&&L.root_digits===r,"legal source shape and root");
  check(L.source_helper_model===LABEL||L.source_helper_model===GLOBAL,"explicit helper source model");
  const label=L.source_helper_model===LABEL,V=parse(L.true_original_second_moment_upper),h=parse(L.whole_batch_helper_failure_upper);
  check(V[0]>=0n&&h[0]>=0n&&cmp(h,one)<=0n,"true nonnegative moments and batch failure promise");
  const coefficient=label?72n*BigInt(n*r*M):144n*BigInt(B*M*M),intrinsic=div(mul(rat(coefficient),V),rat(q*q)),total=min(one,add(intrinsic,h));
  check(L.source_failure_upper_unclipped===str(intrinsic)&&L.complete_reconstruction_failure_upper===str(total)&&L.full_recovery_lower_if_helper_is_supplied===str(sub(one,total)),"exact unconditional union/global-moment budget");
  check(L.nonadaptive_probe_count===n*r&&L.original_classical_record_count===2*B*M&&L.coefficient_squared_norm_upper===2*M,"real original-data and coefficient counts");
  check(L.original_error_independence_and_zero_mean_required===label&&L.original_errors_independent_of_labels_and_helper_coins_required===label&&L.marginal_original_second_moments_suffice_for_global_bound===!label,"different source promises are not interchangeable");
  ["derived_probe_independence_required","fresh_source_noise_per_helper_call_required","source_moment_or_helper_access_established_from_small_receipts",
    "classical_polynomial_preimage_helper_supplied","efficient_original_problem_decoder_supplied","quantum_preimage_algorithms_excluded","accepted_speedup_candidate"].forEach(k=>check(L[k]===false,"ledger scope "+k));
}
function verify(p) {
  check(p.status==="CONDITIONAL_CLASSICAL_SHORT_PREIMAGE_TO_ORIGINAL_LWE_REDUCTION_REVIEW_PENDING","review-pending reduction");
  check(p.producer_sha256===digest(fs.readFileSync(path.join(ROOT,"theorems/native_short_preimage_reduction.py")))&&p.derivation_sha256===digest(fs.readFileSync(path.join(ROOT,"research/NATIVE_SHORT_PREIMAGE_REDUCTION.md"))),"current producer and derivation hashes");
  const deps=["native_known_seed_group_workbench.py","native_noisy_phase_input.py","known_preparation_coherent_reflection.py","ternary_certified_noise_sampler.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"complete direct dependency provenance");
  deps.forEach(f=>check(p.dependency_sha256[f]===digest(fs.readFileSync(path.join(ROOT,"theorems",f))),"dependency hash "+f));
  check(p.bounded_original_data_controls.length===5&&p.scalable_source_helper_ledgers.length===8,"live calibration and scaling coverage");
  const stats=p.bounded_original_data_controls.map(control);p.scalable_source_helper_ledgers.forEach(ledger);
  check(stats.some(s=>s.missing)&&stats.some(s=>s.noisyFailure)&&p.bounded_original_data_controls.some(c=>c.matches_truth_fixture),"both successes and falsifying controls retained");
  ["classical_polynomial_short_preimage_solver_constructed","general_quantum_fibre_processing_ruled_out","accepted_speedup_candidate","new_active_negative_result_created"].forEach(k=>check(p[k]===false,"report scope "+k));
  check(p.research_decision==="DO_NOT_GRANT_CLASSICAL_SHORT_PREIMAGE_COMPILATION_AS_A_FREE_QUANTUM_INGREDIENT","helper admission decision");
  return {verified:true,controls:stats.length,enumerated_words:stats.reduce((s,x)=>s+x.words,0),verified_probes:stats.reduce((s,x)=>s+x.probes,0),missing_probes:stats.reduce((s,x)=>s+x.missing,0),scalable_ledgers:p.scalable_source_helper_ledgers.length};
}
module.exports={verify,control,ledger,decode,frequency,plan};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

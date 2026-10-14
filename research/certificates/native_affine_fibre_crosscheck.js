"use strict";
// Exact unit-minor coordinates, all bounded selector memberships and F3 escape.
// No physical compiler, source hardness or general row lower bound is certified.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,str}=require("./cyclotomic_exact.js"),H=require("./native_short_preimage_crosscheck.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_affine_fibre_relaxation.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),mod=(x,q)=>(x%q+q)%q;
const encode=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const tuples=(q,n)=>n?tuples(q,n-1).flatMap(a=>Array.from({length:q},(_,i)=>[...a,i])):[[]];
function rank3(matrix) {
  const a=matrix.map(row=>row.map(x=>Number(BigInt(x)%3n)));let rank=0;
  for(let j=0;j<a[0].length&&rank<a.length;j++) {
    let p=rank;while(p<a.length&&!a[p][j])p++;if(p===a.length)continue;
    [a[p],a[rank]]=[a[rank],a[p]];const inverse=a[rank][j]===1?1:2;
    a[rank]=a[rank].map(x=>x*inverse%3);
    for(let k=0;k<a.length;k++)if(k!==rank){const c=a[k][j];a[k]=a[k].map((x,i)=>(x-c*a[rank][i]+6)%3);}
    rank++;
  }
  return rank;
}
function matrixFor(f,b) {return Array.from({length:f.dimension},(_,i)=>f.paired_labels[b].flatMap(pair=>pair.map(a=>a[i])));}
function multiply(A,B,q){return A.map(row=>B[0].map((_,j)=>mod(row.reduce((s,a,k)=>s+BigInt(a)*BigInt(B[k][j]),0n),q)));}
function checkFamily(f) {
  const q=BigInt(f.modulus);let root=q;while(root%3n===0n&&root>1n)root/=3n;
  check(root===1n&&q>=3n&&Number.isInteger(f.dimension)&&f.dimension>0&&Number.isInteger(f.sites)&&f.sites>0&&Number.isInteger(f.cohorts)&&f.cohorts>0&&(f.cohorts&(f.cohorts-1))===0,"actual native public shape");
  check(f.paired_labels.length===f.cohorts&&f.paired_labels.every(c=>c.length===f.sites&&c.every(p=>p.length===2&&p.every(a=>a.length===f.dimension&&a.every(x=>BigInt(x)>=0n&&BigInt(x)<q)))),"canonical complete label pairs");
  check(f.responses_masks_source_IDs_and_errors_supplied===false,"no response source in row recipe");
}
function recipe(r,expected) {
  same(r.matrix,expected,"actual public coordinate matrix");const q=BigInt(r.modulus),n=expected.length,d=expected[0].length;
  check(r.pivot_columns.length===n&&r.free_columns.length===d-n,"complete pivot/free coordinates");
  same([...r.pivot_columns,...r.free_columns].sort((a,b)=>a-b),Array.from({length:d},(_,i)=>i),"physical coordinate partition");
  const S=expected.map(row=>r.pivot_columns.map(j=>row[j])),X=r.pivot_minor_inverse;
  check(X.length===n&&X.every(row=>row.length===n&&row.every(x=>BigInt(x)>=0n&&BigInt(x)<q)),"canonical full-root minor inverse");
  const I=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>BigInt(i===j)));
  same(multiply(S,X,q).map(row=>row.map(String)),I.map(row=>row.map(String)),"actual right unit inverse");
  same(multiply(X,S,q).map(row=>row.map(String)),I.map(row=>row.map(String)),"actual left unit inverse");
  let root=q,rd=0;while(root>1n){check(root%3n===0n,"ternary root");root/=3n;rd++;}
  let step=1;const steps=[1];while(step<rd){step=Math.min(2*step,rd);steps.push(step);}
  same(r.inverse_lift_digits,steps,"doubling Hensel precision rather than prime-field inversion");
  check(r.free_registers===d-n&&r.uniform_free_register_trits===(d-n)*rd&&r.coordinate_bijection==="z <-> (A*z,z_free)","charged free coordinate recipe");
  same(r.free_fibre_size,{base:String(q),exponent:d-n},"whole unrestricted affine fibre");
  check(r.unit_minor_verified_modulo_full_root===true&&r.uses_composite_modulus_field_inverse===false&&r.physical_gate_synthesis_and_precision_supplied===false,"modular algebra is not a physical compiler");
  return {solve(target,free){
    check(target.length===n&&free.length===d-n,"complete coordinate inputs");
    const rhs=expected.map((row,i)=>mod(BigInt(target[i])-r.free_columns.reduce((s,j,k)=>s+BigInt(row[j])*BigInt(free[k]),0n),q));
    const pivot=X.map(row=>mod(row.reduce((s,a,i)=>s+BigInt(a)*rhs[i],0n),q)),out=Array(d).fill(0n);
    r.pivot_columns.forEach((j,i)=>out[j]=pivot[i]);r.free_columns.forEach((j,i)=>out[j]=BigInt(free[i]));
    same(expected.map(row=>encode(mod(row.reduce((s,a,j)=>s+BigInt(a)*out[j],0n),q))),target,"exact affine target");
    return out.map(encode);
  }};
}
function word(z,q) {
  const allowed=[[1n,0n],[q-1n,1n],[0n,q-1n]],out=[];
  for(let j=0;j<z.length;j+=2){const t=allowed.findIndex(p=>p[0]===BigInt(z[j])&&p[1]===BigInt(z[j+1]));if(t<0)return null;out.push(t);}
  return out;
}
function bounded(c) {
  const f=c.public_family;checkFamily(f);const q=Number(f.modulus),n=f.dimension,B=f.cohorts,M=f.sites;
  check([3,9].includes(q)&&B*q**(2*M)<=8192,"complete bounded coordinate preflight");
  if(c.status==="NONFREE_RANK_UNSUPPORTED_NOT_NO_SOLUTIONS") {
    check(Array.from({length:B},(_,b)=>rank3(matrixFor(f,b))).some(rank=>rank<n),"genuine unsupported mod3 rank");
    check(c.target_failure_or_general_no_go_inferred===false,"unsupported is not no solutions");return {coordinates:0,words:0,unsupported:1};
  }
  check(c.status==="COMPLETE_EXACT_PUBLIC_AFFINE_FILTER_CONTROL"&&c.public_affine_recipes.length===B,"complete exact recipe control");
  const targets=tuples(q,n),free=tuples(q,2*M-n),counts=new Map(),accepted=[],seen=[];
  c.public_affine_recipes.forEach((r,b)=>{
    check(r.modulus===f.modulus,"same relaxation root");const P=recipe(r,matrixFor(f,b)),zs=new Set();
    targets.forEach(target=>free.forEach(t=>{
      const z=P.solve(target,t);zs.add(JSON.stringify(z));const w=word(z,BigInt(q));
      if(w!==null){same(H.frequency(f,b,w),target,"native filter really hits target");accepted.push({cohort:b,target,free_coordinates:t,coefficients:z,word:w});const key=JSON.stringify(target);counts.set(key,(counts.get(key)||0)+1);}
    }));
    check(zs.size===q**(2*M),"whole public coordinate map is bijective");seen.push(zs.size);
  });
  same(c.complete_coordinates_checked_per_cohort,seen,"all coordinates charged");same(c.accepted_word_receipts,accepted,"all and only actual native memberships");
  check(c.complete_native_memberships_checked===B*3**M&&accepted.length===B*3**M,"native coefficient mapping is one-to-one");
  const K=BigInt(q)**BigInt(2*M-n),laws=targets.map(target=>{
    const count=counts.get(JSON.stringify(target))||0,p=rat(BigInt(count),BigInt(B)*K);
    return {target,native_word_count:count,raw_filter_acceptance:str(p),complete_failure_probability:str(rat(p[1]-p[0],p[1])),conditional_word_probability:count?str(rat(1n,BigInt(count))):null};
  });
  same(c.all_target_filter_laws,laws,"exact raw, failure and conditional probabilities");
  check(c.uniform_target_mean_acceptance_exact===str(rat(3n**BigInt(M),BigInt(q)**BigInt(2*M))),"uniform-target average without balance assumption");
  ["source_values_mask_secret_and_errors_used_by_relaxation","discarding_failure_is_free","bounded_exhaustive_replay_is_polynomial_algorithm","physical_uniform_affine_state_circuit_executed","all_quantum_fibre_preparation_excluded"].forEach(k=>check(c[k]===false,"control scope "+k));
  return {coordinates:seen.reduce((a,b)=>a+b,0),words:accepted.length,unsupported:0};
}
function canonical(x){if(Array.isArray(x))return x.map(canonical);if(x&&typeof x==="object")return Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])]));return x;}
function endpoint(c) {
  const raw=c.original_records,mask=c.known_mask,result=c.actual_original_data_reconstruction,f=result.public_family;
  checkFamily(f);check(f.modulus==="3"&&f.cohorts===1&&f.dimension===2&&f.sites===3&&raw.length===6,"actual F3 original-data control");
  same(f.paired_labels,[Array.from({length:3},(_,j)=>raw.slice(2*j,2*j+2).map(r=>r.label))],"endpoint public rows");
  const digest=crypto.createHash("sha256").update(JSON.stringify(canonical(f))).digest("hex");check(result.public_family_sha256===digest,"actual public-family binding");
  const r=c.public_endpoint_recipes[0],offset=f.paired_labels[0][0][0].map((_,i)=>f.paired_labels[0].reduce((s,[a])=>s+a[i],0)%3),slopes=offset.map((_,i)=>f.paired_labels[0].map(([a,b])=>(a[i]+b[i])%3));
  check(r.cohort===0,"native endpoint cohort");same(r.offset,offset,"actual affine offset");check(r.affine_recipe.modulus==="3","F3 endpoint recipe root");const P=recipe(r.affine_recipe,slopes);
  tuples(3,2).forEach(target=>{
    const corrected=target.map((x,i)=>(x-offset[i]+3)%3);const prepared=tuples(3,1).map(t=>P.solve(corrected,t));
    prepared.forEach(w=>same(H.frequency(f,0,w),target,"direct uniform native endpoint fibre without membership filter"));
  });
  const schedule=H.plan(2,3n),probes=result.completed_probe_receipts;check(probes.length===2,"complete original endpoint probes");same(result.planned_probes,schedule,"nonadaptive original-data schedule");
  probes.forEach((p,j)=>{
    const target=schedule[j].frequency,r=p.receipt,corrected=target.map((x,i)=>(x-offset[i]+3)%3),w=P.solve(corrected,[0]);
    check(r.public_family_sha256===digest&&r.cohort===0,"endpoint receipt provenance");same(r.word,w,"polynomial F3 chosen preimage");same(r.target,target,"chosen target");same(p.requested_frequency,target,"actual response probe");
    const beta=w.flatMap(t=>[[1,0],[-1,1],[0,-1]][t]),response=raw.reduce((s,r,i)=>s+beta[i]*(r.value+r.label.reduce((a,x,k)=>a+x*mask[k],0)),0);
    same(p.signed_original_coefficients,beta,"actual signed original coefficients");check(p.derived_masked_response===(response%3+3)%3&&p.fresh_original_errors_created===false,"actual original response reused");
  });
  const decoded=H.decode(probes,2,3n),original=decoded.masked.map((s,i)=>(s-mask[i]+3)%3);
  same(result.masked_secret,decoded.masked,"exact reconstructed masked endpoint");same(result.decisions,decoded.decisions,"exact original trit decisions");same(result.original_secret,original,"known mask removal");same(original,c.truth_fixture_only.original_secret,"ideal endpoint true original secret");
  raw.forEach(r=>check(r.modulus===3&&r.value===r.label.reduce((s,a,i)=>s+a*original[i],0)%3,"ideal original-data calibration"));
  check(result.status==="COMPLETE_RECEIPT_CHECKED_CLASSICAL_RECONSTRUCTION"&&result.helper_calls===2&&result.original_records_paid_once===6&&result.new_quantum_algorithm_or_speedup===false&&c.matches_truth_fixture===true&&c.label_only_helper_calls===2&&c.growing_root_helper_or_new_quantum_algorithm===false,"endpoint classical counterpart, not new quantum discovery");
}
function ledger(L) {
  const n=L.dimension,r=L.root_digits,B=L.cohorts,M=L.sites;check([n,r,B,M].every(x=>Number.isSafeInteger(x)&&x>0)&&(B&(B-1))===0&&2*M>=n,"legal growing relaxation shape");
  const E=Math.max(0,r*(2*M-n)-M);
  check(L.per_cohort_unrestricted_affine_fibre_trits===r*(2*M-n),"free affine entropy");
  same(L.per_target_filter_acceptance_upper,{base:3,negative_exponent:E},"deterministic per-target upper, no target balance");
  same(L.uniform_target_mean_filter_acceptance,{base:3,negative_exponent:(2*r-1)*M},"distinct uniform-target mean");
  same(L.half_success_requires_ordinary_amplification_multiplier_square_at_least,{base:3,exponent:E,denominator:2},"necessary ordinary-amplification cost");
  check(L.full_row_rank_modulo3_in_every_cohort_is_an_assumption===true&&L.bound_is_only_for_uniform_unrestricted_affine_fibre_filter===true,"explicit scoped relaxation premise");
  ["target_word_counts_or_population_balance_assumed","arbitrary_coherent_fibre_algorithms_excluded","endpoint_linear_bypass_excluded","physical_gate_compiler_supplied","accepted_speedup_candidate"].forEach(k=>check(L[k]===false,"ledger scope "+k));
}
function verify(p) {
  check(p.status==="SCOPED_NATIVE_AFFINE_RELAXATION_FILTER_AND_ENDPOINT_COUNTERCONTROL_REVIEW_PENDING","review-pending scoped result");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_affine_fibre_relaxation.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_AFFINE_FIBRE_RELAXATION.md")),"live source and derivation");
  const deps=["native_short_preimage_reduction.py","native_known_seed_group_workbench.py","known_preparation_coherent_reflection.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct source dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.bounded_filter_controls.length===6&&p.growing_relaxation_ledgers.length===4&&p.selector_linearization_checks.length===4,"declared live coverage");
  const stats=p.bounded_filter_controls.map(bounded);endpoint(p.actual_F3_endpoint_countercontrol);p.growing_relaxation_ledgers.forEach(ledger);
  p.selector_linearization_checks.forEach(c=>{
    const q=BigInt(c.modulus);same(c.third_selector_affine_extrapolation_defect,[encode(3n%q),encode(mod(-3n,q))],"actual third-selector carry");same(c.F3_slope_cyclic_closure_defect,[encode(mod(-6n,q)),encode(3n%q)],"actual cyclic F3 closure");
    check(c.native_selector_is_an_F3_affine_line_for_arbitrary_public_pairs===(q===3n)&&c.higher_root_carries_may_be_discarded===false,"F3 endpoint not promoted to higher roots");
  });
  ["accepted_speedup_candidate","new_active_negative_result_created","general_quantum_fibre_lower_bound_proved"].forEach(k=>check(p[k]===false,"report scope "+k));
  return {verified:true,exact_coordinates:stats.reduce((a,s)=>a+s.coordinates,0),native_memberships:stats.reduce((a,s)=>a+s.words,0),unsupported_controls:stats.reduce((a,s)=>a+s.unsupported,0),growing_ledgers:4,endpoint_classical_reconstruction:true};
}
module.exports={verify,recipe,rank3,bounded,ledger};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

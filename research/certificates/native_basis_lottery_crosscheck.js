"use strict";
// Independent original-record ring solving and rational source-event replay.
// Gaussian special functions require the separate, explicitly trusted Arb replay.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),M=require("./native_small_multiple_completion_crosscheck.js");
const {check,rat,parse,str,add,mul,sub,cmp,one,zero}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_basis_lottery.json");
const mod=(x,q)=>(x%q+q)%q,enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,msg)=>E.same(canonical(a),canonical(b),msg);
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min=(a,b)=>cmp(a,b)<=0n?a:b,bits=x=>x===0n?0:x.toString(2).length;
function exact(v){
  check(typeof v==="number"?Number.isSafeInteger(v):typeof v==="string"&&/^-?(0|[1-9][0-9]*)$/.test(v),"exact canonical integer");
  const n=BigInt(v);same(enc(n),v,"canonical large integer encoding");return n;
}
function root(q){check(q>=3n,"positive ternary root");let d=0;while(q%3n===0n){q/=3n;d++;}check(q===1n,"actual ternary prime power");return d;}
function inv(x,q){let a=mod(x,q),b=q,s=1n,t=0n;while(b){const k=a/b;[a,b]=[b,a-k*b];[s,t]=[t,s-k*t];}check(a===1n,"true ring unit");return mod(s,q);}
function bank(raw){
  check(Array.isArray(raw)&&raw.length>0,"actual original bank");const q=exact(raw[0].modulus),n=raw[0].label.length;root(q);
  check(n>0&&new Set(raw.map(r=>r.source_id)).size===raw.length,"positive dimension and distinct original IDs");
  raw.forEach(r=>{check(typeof r.source_id==="string"&&r.source_id.length>0&&exact(r.modulus)===q&&r.label.length===n,"original shape and IDs");
    r.label.forEach(a=>check(exact(a)>=0n&&exact(a)<q,"canonical original labels"));check(exact(r.value)>=0n&&exact(r.value)<q,"canonical original response");});
  return {q,n};
}
function rank(rows){
  const A=rows.map(row=>row.map(x=>Number(mod(BigInt(x),3n))));let r=0;
  for(let j=0;j<A[0].length&&r<A.length;j++){
    let p=r;while(p<A.length&&!A[p][j])p++;if(p===A.length)continue;
    [A[p],A[r]]=[A[r],A[p]];const a=A[r][j];A[r]=A[r].map(x=>x*a%3);
    for(let i=0;i<A.length;i++)if(i!==r){const t=A[i][j];A[i]=A[i].map((x,k)=>(x-t*A[r][k]+6)%3);}r++;
  }return r;
}
function inverse(rows,g){
  const n=rows.length,S=rows.map(row=>row.map(a=>mod(BigInt(a),g))),A=S.map((row,i)=>[...row,...Array.from({length:n},(_,j)=>BigInt(i===j))]);
  for(let j=0;j<n;j++){
    let p=j;while(p<n&&A[p][j]%3n===0n)p++;check(p<n,"invertible actual minor");[A[p],A[j]]=[A[j],A[p]];
    const z=inv(A[j][j],g);A[j]=A[j].map(a=>mod(a*z,g));
    for(let i=0;i<n;i++)if(i!==j){const t=A[i][j];A[i]=A[i].map((a,k)=>mod(a-t*A[j][k],g));}
  }
  const X=A.map(row=>row.slice(n));
  for(const [B,C] of [[S,X],[X,S]])for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(B[i].reduce((v,a,k)=>v+a*C[k][j],0n),g)===BigInt(i===j),"both full-ring inverse identities");
  const steps=[1],d=root(g);while(steps.at(-1)<d)steps.push(Math.min(2*steps.at(-1),d));
  return {modulus:enc(g),minor:S.map(row=>row.map(enc)),inverse:X.map(row=>row.map(enc)),inverse_lift_digits:steps,
    response_values_entered_basis_selection:false,composite_field_inverse_used:false};
}
function fit(raw,s,R){
  const q=BigInt(raw[0].modulus),ds=raw.map(r=>{const e=mod(BigInt(r.value)-r.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(s[i]),0n),q);return e<q-e?e:q-e;});
  return {radius:enc(R),original_circular_error_distances:ds.map(enc),original_records_checked:raw.length,
    fits_public_radius:ds.every(x=>x<=R),fit_certifies_planted_truth_or_source_law:false};
}
function complete(raw,c,w,R,caps={max_blocks:10000,max_minor_entries:65536},cache=null){
  const {q,n}=bank(raw);check(R>=0n&&4n*R<q&&caps.max_blocks>0&&caps.max_minor_entries>0,"declared radius and caps");
  const model=M.quotient(q,c,w),base={signed_coefficient:enc(c),supplied_multiple:w,candidate_secret:null,original_records_paid_once:raw.length,
    verification_radius:enc(R),original_records_sha256:digest(raw),trial_records:[],blocks_attempted:0,
    original_candidate_verification_evaluations:0,original_response_rounding_evaluations:0,cubic_features_compiled:0,
    new_independent_original_samples_created:false,actual_planted_secret_or_noise_law_certified:false,fixed_instance_radius_uniqueness_certified:false,
    multiple_producer_supplied:false,max_blocks:caps.max_blocks,max_minor_entries:caps.max_minor_entries,
    minor_cap_includes_inverse_certificate_or_interpreter_overhead:false,paired_original_records_required:false,schedule_orbits_are_new_IID_samples:false};
  if(model===null)return {...base,status:"EXACT_NONUNIT_IMAGE_INCOMPATIBILITY"};base.quotient_model=model;
  const g=BigInt(model.nonunit_factor),Q=BigInt(model.remaining_modulus),x=model.known_quotient_IF_multiple_is_true;
  if(g===1n){const F=fit(raw,x,R);return {...base,status:F.fits_public_radius?"UNIT_PREIMAGE_ORIGINAL_RADIUS_FIT_NOT_TRUTH":"UNIT_PREIMAGE_ORIGINAL_RADIUS_FIT_FAILED",
    candidate_secret:F.fits_public_radius?x:null,unit_fit:F,original_candidate_verification_evaluations:raw.length,complete_schedule_or_original_fit_found:true};}
  const T=Math.floor(raw.length/n);Object.assign(base,{planned_disjoint_blocks:T,block_width:n,
    unused_tail_original_IDs:raw.slice(T*n).map(r=>r.source_id),public_label_bank_sha256:digest({modulus:enc(q),labels:raw.map(r=>r.label),source_ids:raw.map(r=>r.source_id)}),
    public_rank_or_inverse_preprocessing_free:false,arithmetic_order:"O(T*n^3*log(d+1)+T*m*n) on O(log(q))-bit operands; cached label-only bases",
    certificate_storage_order:"O(m*n+attempted_blocks*n^2)"});
  if(T>caps.max_blocks||n*n>caps.max_minor_entries)return {...base,status:"COMPLETE_BLOCK_SCHEDULE_CAP_EXCEEDED_NOT_NO_SECRET",complete_schedule_or_original_fit_found:false};
  if(!T)return {...base,status:"INSUFFICIENT_ORIGINAL_ROWS_NOT_NO_SECRET",complete_schedule_or_original_fit_found:true};
  for(let j=0;j<T;j++){
    const block=raw.slice(j*n,(j+1)*n),labelrank=rank(block.map(r=>r.label)),t={block_index:j,original_indices:Array.from({length:n},(_,i)=>j*n+i),
      original_source_IDs:block.map(r=>r.source_id),label_rank_mod3:labelrank};
    if(cache)cache.ranks.add(j);
    if(labelrank<n){base.trial_records.push({...t,status:"SINGULAR_UNIT_MINOR_NOT_NO_SECRET"});continue;}
    if(cache)cache.inverses.add(`${j}:${g}`);
    const B=inverse(block.map(r=>r.label),g),receipts=block.map(r=>{
      const e=mod(BigInt(r.value)-r.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(x[i]),0n),q);
      return {source_id:r.source_id,parent_record_sha256:digest(r),corrected_original_response:enc(e),rounded_missing_quotient_equation:enc(mod((e+Q/2n)/Q,g))};
    }),h=B.inverse.map(row=>enc(mod(row.reduce((v,a,i)=>v+BigInt(a)*BigInt(receipts[i].rounded_missing_quotient_equation),0n),g))),s=x.map((v,i)=>enc(BigInt(v)+Q*BigInt(h[i]))),F=fit(raw,s,R);
    check(s.every((v,i)=>mod(c*BigInt(v),q)===BigInt(w[i])),"actual original-root multiple equation");
    base.trial_records.push({...t,status:F.fits_public_radius?"ORIGINAL_RADIUS_FIT":"ORIGINAL_RADIUS_FIT_FAILED",public_basis_model:B,response_receipts:receipts,
      missing_quotient_candidate:h,candidate_secret:s,multiple_equation_verified:true,original_fit:F});
    base.original_candidate_verification_evaluations+=raw.length;base.original_response_rounding_evaluations+=n;
    if(F.fits_public_radius)return {...base,status:"ONE_ORIGINAL_RADIUS_FIT_SOURCE_CERTIFICATION_REQUIRED",candidate_secret:s,
      blocks_attempted:base.trial_records.length,complete_schedule_or_original_fit_found:true};
  }
  return {...base,status:"NO_RADIUS_FIT_IN_DECLARED_BLOCKS_NOT_NO_SECRET",blocks_attempted:base.trial_records.length,complete_schedule_or_original_fit_found:true};
}
function scan(raw,S){
  const {q}=bank(raw),C=BigInt(S.effective_centered_coefficient_bound),declared=BigInt(S.declared_coefficient_bound),cache={ranks:new Set(),inverses:new Set()};
  check(C===(declared<q/2n?declared:q/2n)&&S.maximum_supported_valuation<root(q),"declared complete centered coefficient scope");
  check(S.planned_coefficient_trials===Number(2n*C)*S.supplied_multiples.length&&S.trials_evaluated===S.trial_records.length&&S.trials_evaluated<=S.planned_coefficient_trials&&S.planned_coefficient_trials<=S.max_pair_trials,"complete scan cap and paid count");
  let count=0,verifications=0,roundings=0,blocks=0,found=null;
  outer:for(const w of S.supplied_multiples)for(let j=0;j<Number(2n*C);j++){
    const c=j<Number(C)?-C+BigInt(j):1n+BigInt(j-Number(C));let a=c,d=0;while(a%3n===0n){a/=3n;d++;}
    const trial=S.trial_records[count++];check(trial!==undefined,"no silent partial coefficient scan");
    if(d>S.maximum_supported_valuation){same(trial,{coefficient:enc(c),multiple:w,status:"OUTSIDE_DECLARED_VALUATION_SCOPE"},"valuation exclusions not extra IID data");continue;}
    const R=complete(raw,c,w,BigInt(S.verification_radius),{max_blocks:S.max_blocks,max_minor_entries:65536},cache);
    same(trial,{coefficient:enc(c),multiple:w,completion:R},"all attempted original-root completions");
    verifications+=R.original_candidate_verification_evaluations;roundings+=R.original_response_rounding_evaluations;blocks+=R.blocks_attempted;
    if(R.candidate_secret!==null){found=R.candidate_secret;break outer;}
  }
  check(count===S.trials_evaluated&&(found!==null||count===S.planned_coefficient_trials),"only a verified fit allows early stopping");
  same(S.candidate_secret,found,"first fit, not secretly selected planted solution");
  check(S.status===(found!==null?"FIRST_RADIUS_FIT_SOURCE_CERTIFICATION_REQUIRED":"NO_RADIUS_FIT_IN_COMPLETE_DECLARED_SCAN_NOT_NO_SECRET")&&S.complete_scan_or_original_fit_found===true,"scan outcome");
  check(S.public_basis_rank_calls===cache.ranks.size&&S.public_basis_inverse_calls===cache.inverses.size&&S.original_candidate_verification_evaluations===verifications&&S.original_response_rounding_evaluations===roundings&&S.block_attempts===blocks,"all preprocessing, rounding and radius work paid");
  check(S.original_records_paid_once===raw.length&&S.public_label_preprocessing_is_free===false&&S.new_original_samples_created===false&&S.multiple_list_coverage_supplied===false&&S.actual_planted_truth_certified===false&&S.first_fit_requires_global_original_code_and_noise_events===true,"scan is not source coverage or planted truth");return count;
}
function power(box){
  const a=parse(box.base),n=box.exponent,b=box.bits,cap=box.max_bit_work;
  check(cmp(a,zero)>=0n&&cmp(a,one)<=0n&&Number.isSafeInteger(n)&&n>=0&&Number.isSafeInteger(b)&&b>0&&Number.isSafeInteger(cap)&&cap>0,"probability power inputs");
  const work=n*Math.max(bits(a[0]),bits(a[1]));check(box.required_operand_bits_upper===work,"whole exact integer work charged");
  if(work>cap){check(box.status==="UNKNOWN_EXACT_POWER_CAP"&&box.lower==="0"&&box.upper==="1","large power remains unknown");return;}
  const N=a[0]**BigInt(n),D=a[1]**BigInt(n),scale=2n**BigInt(b);
  check(box.status==="CERTIFIED_INTEGER_DYADIC_POWER"&&box.lower===str(rat(N*scale/D,scale))&&box.upper===str(rat((N*scale+D-1n)/D,scale)),"directed exact power endpoints");
}
function probability(B){
  const n=B.dimension,T=B.disjoint_original_trials,g=exact(B.derived_modulus),Z=B.Gaussian_derived_error_law,W=B.nonzero_ring_wrap_tail;root(g);
  check(n>0&&T>=0&&Number.isSafeInteger(n)&&Number.isSafeInteger(T)&&cmp(parse(Z.continuous_Gaussian_width),zero)>0n,"positive source dimensions and width");
  const intervals=[Z.zero,Z.each_signed_one,Z.outside_triplet,W];
  intervals.forEach(a=>check(cmp(parse(a.lower),zero)>=0n&&cmp(parse(a.lower),parse(a.upper))<=0n&&cmp(parse(a.upper),one)<=0n,"valid Gaussian probability enclosures"));
  check(W.continuous_Gaussian_width===Z.continuous_Gaussian_width&&BigInt(W.integer_error_radius)===g-1n&&W.enclosure_bits===Z.enclosure_bits&&Z.independent_transcendental_certificate_supplied===false&&Z.conditioning_erases_outside_triplet_mass===false,"wrapped ring tails and honest transcendental provenance");
  const C=B.unwrapped_clean_basis_probability_box,F=B.all_trials_fail_power_box,K=B.all_selected_ring_errors_zero_power_box;
  [C,F,K].forEach(x=>{check(x.bits===Z.enclosure_bits&&x.max_bit_work===524288,"same precision and explicit power cap");power(x);});
  const success=mul(parse(C.lower),rat(1n,2n)),block=success[0]?((success[1]+success[0]-1n)/success[0]):null;
  const h=block?Math.min(64,Number(BigInt(T)/block)):0,half=rat(1n,2n**BigInt(h)),ring=min(one,add(parse(Z.zero.upper),parse(W.upper))),any=min(one,mul(rat(BigInt(T)),parse(K.upper)));
  check(C.base===Z.zero.lower&&C.exponent===n&&B.unit_minor_probability_lower==="1/2"&&B.one_trial_success_probability_lower===str(success),"clean unit-basis source success");
  check(F.base===str(sub(one,success))&&F.exponent===T&&B.reciprocal_Bernoulli_half_block===(block===null?null:enc(block))&&B.half_block_failure_upper===str(half)&&B.all_trials_fail_probability_upper===str(min(parse(F.upper),half)),"disjoint trials only and Bernoulli fallback");
  check(B.one_row_ring_zero_probability_upper===str(ring)&&K.base===str(ring)&&K.exponent===n&&B.any_correct_basis_probability_upper===str(any)&&B.no_correct_basis_probability_lower===str(sub(one,any)),"strategy failure accounts for harmless nonzero wraps");
  check(B.IID_uniform_original_labels_and_independent_Gaussian_errors_required===true&&B.source_IDs_establish_independence===false&&B.reused_blocks_count_as_independent_trials===false&&B.unwrapped_clean_event_is_necessary_for_correctness===false&&B.correctness_upper_bound_includes_nonzero_wrapped_errors===true&&B.general_decoder_lower_bound_proved===false,"source-specific sufficient event, not a general lower bound");
}
function source(S){
  const n=S.dimension,r=S.root_digits,m=S.original_rows,d=S.maximum_supported_valuation,q=3n**BigInt(r),alpha=parse(S.original_Gaussian_width),O=S.original_radius_Gaussian_law,C=S.global_original_code_separation_ledger,B=S.maximum_valuation_basis_event;
  check(n>0&&m>0&&d>=0&&d<r&&cmp(alpha,zero)>0n&&cmp(alpha,one)<0n,"nonzero multiple source scope");M.separation(C);
  check(BigInt(C.original_modulus)===q&&C.dimension===n&&C.original_rows===m&&BigInt(C.verification_radius)===BigInt(O.integer_error_radius)&&O.continuous_Gaussian_width===str(mul(alpha,rat(q))),"same original Gaussian source and global code");
  check(cmp(parse(O.lower),zero)>=0n&&cmp(parse(O.lower),parse(O.upper))<=0n&&cmp(parse(O.upper),one)<=0n,"original Gaussian tail enclosure");
  if(d){probability(B);check(B.dimension===n&&B.disjoint_original_trials===Math.floor(m/n)&&BigInt(B.derived_modulus)===3n**BigInt(d)&&B.Gaussian_derived_error_law.continuous_Gaussian_width===str(mul(alpha,rat(3n**BigInt(d))))&&B.Gaussian_derived_error_law.enclosure_bits===O.enclosure_bits,"maximum valuation nested SAME-source clean event");}else check(B===null,"unit pairs require no lottery");
  const radius=min(one,mul(rat(BigInt(m)),parse(O.upper))),local=min(one,add(add(radius,parse(C.global_code_separation_failure_upper_used)),B?parse(B.all_trials_fail_probability_upper):zero)),coverage=S.external_true_usable_pair_or_complete_scan_coverage_failure_upper;
  check(S.whole_original_radius_failure_upper===str(radius)&&S.uniform_local_failure_upper===str(local)&&S.recovery_failure_upper_IF_source_coverage_and_complete_work_hold===(coverage===null?null:str(min(one,add(local,parse(coverage))))),"source-wide UNION not conditional independent product");
  check(S.maximum_valuation_clean_event_covers_all_smaller_true_quotients===true&&S.valuation_or_unit_part_union_multiplier_required===false&&S.conditioning_on_data_selected_multiple_truth_used===false&&S.whole_derived_bank_triplet_truncation_required===false&&S.original_rows_need_not_be_paired===true,"single coupled event without data-selected conditioning");
  check(S.source_alpha_q_at_least_2_sqrt_n===(cmp(mul(mul(alpha,rat(q)),mul(alpha,rat(q))),rat(BigInt(4*n)))>=0n)&&S.worst_case_lattice_reduction_compatibility_established===false&&S.default_complete_schedule_cap_feasible===(Math.floor(m/n)<=10000&&n*n<=65536)&&S.source_laws_or_multiple_producer_supplied===false,"source scalar guard is not a hardness reduction or runtime guarantee");
}
function control(C){
  const raw=C.original_records,{q,n}=bank(raw),truth=C.truth_fixture_only,c=exact(C.coefficient),R=exact(C.radius);
  check(truth.original_secret.length===n&&truth.original_errors.length===raw.length,"full calibration truth shape");
  raw.forEach((r,j)=>check(mod(r.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(truth.original_secret[i]),0n)+BigInt(truth.original_errors[j]),q)===BigInt(r.value),"actual original observations"));
  same(C.multiple,truth.original_secret.map(s=>enc(mod(c*BigInt(s),q))),"truth prepares only calibration multiple");
  const result=complete(raw,c,C.multiple,R);same(C.completion,result,"independent exact disjoint original-basis completion");
  check(C.matches_truth_fixture===(JSON.stringify(result.candidate_secret)===JSON.stringify(truth.original_secret))&&C.external_multiple_prepared_from_truth_FOR_CALIBRATION_ONLY===true&&C.calibration_is_unbounded_Gaussian_source===false,"truth check after algorithm, not supplied source law");
  return result;
}
function verify(P){
  check(P.status==="DISJOINT_CLEAN_BASIS_CLASSICAL_COMPLETION_AND_MONOTONE_SOURCE_EVENT_REVIEW_PENDING","scoped review-pending theorem");
  check(P.producer_sha256===hash(path.join(ROOT,"theorems/native_basis_lottery.py"))&&P.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_BASIS_LOTTERY.md")),"current producer and derivation");
  const deps=["native_affine_fibre_relaxation.py","native_small_multiple_completion.py","native_classical_modulus_descent.py","native_gaussian_quotient_completion.py","native_full_root_slice.py","ternary_covariant_noise.py","ternary_noise_degradation.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(P.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");deps.forEach(f=>check(P.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(P.actual_original_controls.length===3&&P.actual_original_falsifiers.length===3&&P.Gaussian_source_profiles.length===3,"full declared live scope");
  P.actual_original_controls.forEach(C=>check(control(C).candidate_secret!==null&&C.matches_truth_fixture,"actual calibration successes"));
  const trials=scan(P.actual_original_controls[0].original_records,P.actual_unknown_coefficient_scan);
  const bad=P.actual_original_falsifiers;bad.forEach(control);
  check(bad[0].kind==="full_bank_rank_but_every_fixed_block_singular"&&rank(bad[0].original_records.map(r=>r.label))===2&&bad[0].completion.candidate_secret===null&&bad[0].completion.trial_records.every(t=>t.label_rank_mod3<2),"combined rank does not establish a scheduled clean basis");
  check(bad[1].kind==="wrong_planted_secret_with_an_original_radius_fit"&&bad[1].completion.candidate_secret!==null&&!bad[1].matches_truth_fixture,"radius fit is not truth");
  check(bad[2].kind==="nonzero_unwrapped_error_is_harmless_modulo_missing_ring"&&bad[2].matches_truth_fixture&&BigInt(bad[2].truth_fixture_only.original_errors[0])===81n,"unwrapped-zero necessity falsified");
  P.Gaussian_source_profiles.forEach(source);probability(P.constant_width_large_dimension_countercontrol);
  check(cmp(parse(P.constant_width_large_dimension_countercontrol.no_correct_basis_probability_lower),rat(99n,100n))>0n,"large-dimension strategy-specific failure control");
  check(P.accepted_speedup_candidate===false&&P.new_active_negative_result_created===false&&P.Gaussian_LWE_solver_or_new_quantum_algorithm===false&&P.novelty_claim===false&&P.research_decision==="PAY_SOURCE_AWARE_CLEAN_BASIS_COMPARISON_BEFORE_CUBIC_MATRICES_OR_QUANTUM_SIGNAL","no unsupported solver or algorithm admission");
  return {verified:true,actual_original_calibrations:3,actual_falsifiers:3,coefficient_trials_replayed:trials,conditional_Gaussian_source_profiles:3,
    Gaussian_transcendental_endpoints_independently_verified:false,separate_Arb_probability_replay_required:true,multiple_producer_or_quantum_algorithm_supplied:false};
}
module.exports={verify,complete,scan,source,probability,power};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

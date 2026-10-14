"use strict";
// Independent ring preimages, original-value rounding and source-wide code events.
// This does not certify a distinguisher, list coverage or one observed code distance.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,parse,str,add,mul,div,cmp,one}=require("./cyclotomic_exact.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_small_multiple_completion.json");
const mod=(x,q)=>(x%q+q)%q,enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),min=(a,b)=>cmp(a,b)<=0n?a:b;
const bits=x=>x===0n?0:x.toString(2).length;
function root(q){check(q>=3n,"positive actual root");let r=0;while(q%3n===0n){r++;q/=3n;}check(q===1n,"ternary prime power");return r;}
function inv(x,q){let a=mod(x,q),b=q,s=1n,t=0n;while(b){const k=a/b;[a,b]=[b,a-k*b];[s,t]=[t,s-k*t];}check(a===1n,"only a true ring unit may be inverted");return mod(s,q);}
function quotient(q,c,w){
  check(mod(c,q)!==0n&&w.length>0,"nonzero full-root coefficient");let a=mod(c,q),g=1n,d=0;
  while(a%3n===0n){a/=3n;g*=3n;d++;}
  if(w.some(x=>BigInt(x)%g!==0n))return null;
  const Q=q/g,u=mod(c/g,Q),x=w.map(v=>enc(mod(BigInt(v)/g*inv(u,Q),Q)));
  check(x.every((v,i)=>mod(c*BigInt(v),q)===BigInt(w[i])),"entire original-root multiple image");
  return {original_modulus:enc(q),signed_coefficient:enc(c),multiple:w,nonunit_factor:enc(g),valuation:d,remaining_modulus:enc(Q),unit_coefficient:enc(u),
    known_quotient_IF_multiple_is_true:x,lost_secret_trits_per_coordinate:d,multiple_membership_in_original_secret_orbit_established:false,free_multiple_producer_or_decision_oracle_supplied:false};
}
function pivots(raw){
  const n=raw[0].label.length,A=Array.from({length:n},(_,i)=>raw.map(s=>Number(BigInt(s.label[i])%3n))),cols=[];let r=0;
  for(let j=0;j<raw.length&&r<n;j++){
    let p=r;while(p<n&&!A[p][j])p++;if(p===n)continue;[A[r],A[p]]=[A[p],A[r]];const z=A[r][j];A[r]=A[r].map(x=>x*z%3);
    for(let i=0;i<n;i++)if(i!==r){const t=A[i][j];A[i]=A[i].map((x,k)=>(x-t*A[r][k]+6)%3);}cols.push(j);r++;
  }return {cols,rank:r};
}
function model(raw,g){
  const P=pivots(raw),n=raw[0].label.length,q=BigInt(raw[0].modulus);if(P.rank<n)return null;
  const S=P.cols.map(j=>raw[j].label.map(x=>mod(BigInt(x),g)));
  const A=S.map((row,i)=>[...row,...Array.from({length:n},(_,j)=>BigInt(i===j))]);
  for(let j=0;j<n;j++){
    let p=j;while(p<n&&A[p][j]%3n===0n)p++;check(p<n,"unit minor over the actual composite ring");[A[j],A[p]]=[A[p],A[j]];
    const s=inv(A[j][j],g);A[j]=A[j].map(x=>mod(x*s,g));
    for(let i=0;i<n;i++)if(i!==j){const t=A[i][j];A[i]=A[i].map((x,k)=>mod(x-t*A[j][k],g));}
  }
  const X=A.map(row=>row.slice(n));
  for(const [B,C] of [[S,X],[X,S]])for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(B[i].reduce((v,x,k)=>v+x*C[k][j],0n),g)===BigInt(i===j),"both exact inverse identities");
  let d=1;const steps=[1],r=root(g);while(d<r){d=Math.min(2*d,r);steps.push(d);}
  return {modulus:enc(g),label_only_basis_rows:P.cols,minor:S.map(row=>row.map(enc)),inverse:X.map(row=>row.map(enc)),inverse_lift_digits:steps,
    public_label_sha256:digest({modulus:enc(q),labels:raw.map(s=>s.label)}),composite_field_inverse_used:false,response_values_entered_basis_selection:false};
}
function complete(raw,c,w){
  const q=BigInt(raw[0].modulus),Qm=quotient(q,c,w),base={signed_coefficient:enc(c),multiple:w,candidate_secret:null,original_response_residual_evaluations:0,
    multiple_truth_premise_verified:false,rounded_consistency_is_an_original_secret_certificate:false};
  if(!Qm)return {...base,status:"EXACT_NONUNIT_IMAGE_INCOMPATIBILITY"};base.quotient_model=Qm;
  if(Qm.valuation===0)return {...base,status:"UNIT_MULTIPLE_ALGEBRAIC_PREIMAGE_NOT_TRUTH_CERTIFICATE",candidate_secret:Qm.known_quotient_IF_multiple_is_true,rounding_transcript:[]};
  const g=BigInt(Qm.nonunit_factor),Q=BigInt(Qm.remaining_modulus),lower=Qm.known_quotient_IF_multiple_is_true,M=model(raw,g);
  if(!M)return {...base,status:"ORIGINAL_LOW_LABEL_RANK_UNSUPPORTED_NOT_NO_SOLUTION"};
  const transcript=raw.map(s=>{
    const residual=mod(BigInt(s.value)-s.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(lower[i]),0n),q),round=mod((residual+Q/2n)/Q,g),a=mod(residual-Q*round,q),b=mod(Q*round-residual,q);
    return {source_id:s.source_id,corrected_original_response:enc(residual),rounded_missing_quotient_equation:enc(round),distance_to_nearest_center:enc(a<b?a:b)};
  }),rhs=M.label_only_basis_rows.map(j=>BigInt(transcript[j].rounded_missing_quotient_equation));
  const h=M.inverse.map(row=>mod(row.reduce((s,a,j)=>s+BigInt(a)*rhs[j],0n),g));
  const consistent=raw.every((s,j)=>mod(s.label.reduce((v,a,i)=>v+BigInt(a)*h[i],0n),g)===BigInt(transcript[j].rounded_missing_quotient_equation));
  const candidate=consistent?lower.map((a,i)=>enc(BigInt(a)+Q*h[i])):null;
  if(candidate)check(candidate.every((s,i)=>mod(c*BigInt(s),q)===BigInt(w[i])),"completion remains in actual multiple fibre");
  return {...base,status:consistent?"CONDITIONAL_ORIGINAL_BANK_MULTIPLE_COMPLETION":"INCONSISTENT_ROUNDED_MISSING_QUOTIENT",candidate_secret:candidate,
    missing_quotient_solution:consistent?h.map(enc):null,public_basis_model:M,rounding_transcript:transcript,original_response_residual_evaluations:raw.length};
}
function fit(raw,s,R){
  const q=BigInt(raw[0].modulus),distances=raw.map(r=>{const e=mod(BigInt(r.value)-r.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(s[i]),0n),q);return e<q-e?e:q-e;});
  return {fits_public_radius:distances.every(x=>x<=R),radius:enc(R),original_circular_error_distances:distances.map(enc),original_records_checked:raw.length,bounded_fit_alone_certifies_truth:false};
}
function scan(raw,S){
  const q=BigInt(raw[0].modulus),C=BigInt(S.effective_centered_coefficient_bound),R=BigInt(S.public_verification_radius),attempts=S.trial_records;
  check(4n*R<q&&R>=0n&&S.supplied_multiples.length*Number(2n*C)===S.planned_coefficient_trials,"whole supplied list and declared verification radius");
  check(C===(BigInt(S.declared_coefficient_bound)<q/2n?BigInt(S.declared_coefficient_bound):q/2n)&&attempts.length===S.planned_coefficient_trials&&attempts.length===S.trials_evaluated,"all centered coefficients and complete trials charged");
  check(attempts.length>0&&attempts.length<=10000&&attempts.length%Number(2n*C)===0,"finite whole scan");
  const fits=new Map(),models=new Map();let residuals=0;
  for(let start=0;start<attempts.length;start+=Number(2n*C)){
    const w=S.supplied_multiples[start/Number(2n*C)];
    for(let j=0;j<Number(2n*C);j++){
      const c=j<Number(C)?-C+BigInt(j):1n+BigInt(j-Number(C)),expected=complete(raw,c,w);
      same(attempts[start+j],expected,"independent full-root completion for every supplied list/coefficient");
      residuals+=expected.original_response_residual_evaluations;
      if(expected.public_basis_model)models.set(String(expected.public_basis_model.modulus),expected.public_basis_model);
      if(expected.candidate_secret){const key=JSON.stringify(expected.candidate_secret);if(!fits.has(key))fits.set(key,{candidate_secret:expected.candidate_secret,fit:fit(raw,expected.candidate_secret,R)});}
    }
  }
  const survivors=[...fits.values()].filter(x=>x.fit.fits_public_radius).sort((a,b)=>{for(let i=0;i<a.candidate_secret.length;i++){const d=BigInt(a.candidate_secret[i])-BigInt(b.candidate_secret[i]);if(d)return d<0n?-1:1;}return 0;});
  same(S.bounded_fit_candidates,survivors,"actual all-original-record bounded fit is not truth");
  same(S.public_basis_inversions,[...models.values()].sort((a,b)=>Number(BigInt(a.modulus)-BigInt(b.modulus))),"only public inverses cached by missing modulus");
  check(S.public_basis_rref_calls===1&&S.public_basis_inversion_calls===models.size&&S.public_matrix_preprocessing_is_free===false&&S.public_matrix_preprocessing_arithmetic_order==="O(n^2*m) field RREF once; O(n^3*log(d+1)) modular arithmetic per cached3^d inverse","public preprocessing paid and reused by valuation");
  check(S.original_response_residual_evaluations===residuals&&S.original_candidate_verification_evaluations===raw.length*fits.size&&S.original_records_paid_once===raw.length,"same original bank and every repeated response calculation charged");
  check(S.status===(survivors.length===1?"ONE_BOUNDED_FIT_CANDIDATE_SOURCE_CERTIFICATION_REQUIRED":survivors.length?"AMBIGUOUS_BOUNDED_FIT_CANDIDATES":"NO_BOUNDED_FIT_CANDIDATE_NOT_NO_SECRET"),"complete scan outcome remains conditional");
  check(S.list_coverage_or_decision_solver_supplied===false&&S.new_independent_original_samples_created===false&&S.unconditional_secret_recovery_claim===false,"scan has no hidden oracle");return attempts.length;
}
function separation(L){
  const q=BigInt(L.original_modulus),r=root(q),n=L.dimension,m=L.original_rows,R=BigInt(L.verification_radius);check(4n*R<q&&R>=0n&&n>0&&m>0,"source verifier radius and dimensions");
  check(L.valuation_small_ball_certificates.length===r,"all3-adic difference strata");let exact=rat(0n),max=-Infinity;
  L.valuation_small_ball_certificates.forEach((row,d)=>{
    const order=3n**BigInt(r-d),numerator=2n*(2n*R/(3n**BigInt(d)))+1n,b=row.exact_probability_power_block,
      D=order**BigInt(b),N=numerator**BigInt(b),k=bits(D/N)-1,a=(r-d)*n,pop=3n**BigInt(a),popbits=bits(pop-1n),blocks=Math.floor(m/b),e=popbits-k*blocks;
    check(b>0&&2n**BigInt(k)*N<=D&&D<2n**BigInt(k+1)*N,"certified probability-power logarithm using integers");
    same(row,{difference_valuation:d,subgroup_order:enc(order),small_ball_numerator:enc(numerator),small_ball_denominator:enc(order),difference_population_base3_exponent:a,
      population_upper_ceil_log2:popbits,exact_probability_power_block:b,power_negative_log2_floor:k,complete_power_blocks:blocks,term_upper_power2_exponent:e},"actual cyclic subgroup geometry and whole population bound");
    max=Math.max(max,e);
    if(r*m<=2048)exact=add(exact,mul(rat(pop-3n**BigInt((r-d-1)*n)),rat(numerator**BigInt(m),order**BigInt(m))));
  });
  const exponent=max+bits(BigInt(r-1));let budget=rat(1n,2n**BigInt(Math.min(64,Math.max(0,-exponent))));
  if(r*m<=2048)budget=min(budget,min(exact,one));
  check(L.dyadic_union_upper_exponent===exponent&&L.exact_union_upper_if_short===(r*m<=2048?str(min(exact,one)):null)&&L.global_code_separation_failure_upper_used===str(budget),"conservative global code failure union, no fitted exponent");
  check(L.IID_uniform_original_label_rows_required===true&&L.separation_event_covers_all_secrets_and_adaptive_candidates===true&&L.candidate_count_union_multiplier_required===false&&L.fixed_instance_distance_certified===false,"ensemble bound, not individual-code proof");
}
function event(L){
  const q=BigInt(L.original_modulus),n=L.dimension,m=L.original_rows,R=BigInt(L.public_radius),d=L.maximum_supported_valuation,V=parse(L.true_original_second_moment_upper),spacing=q/3n**BigInt(d),T=R<spacing/2n?R:spacing/2n;
  check(Number.isSafeInteger(d)&&d>=0&&d<root(q)&&V[0]>=0n,"valid nonzero-multiple valuation and true moment upper");
  separation(L.code_separation_ledger);const S=L.code_separation_ledger;
  check(BigInt(S.original_modulus)===q&&S.dimension===n&&S.original_rows===m&&BigInt(S.verification_radius)===R,"same actual source in noise and verifier event");
  const errors=min(one,div(mul(rat(BigInt(m)),V),rat((T+1n)**2n))),local=min(one,add(errors,parse(S.global_code_separation_failure_upper_used))),coverage=L.external_covered_usable_multiple_list_failure_upper;
  check(BigInt(L.minimum_original_center_spacing)===spacing&&BigInt(L.uniform_good_original_error_threshold)===T&&L.original_error_event_failure_upper===str(errors)&&L.uniform_local_event_failure_upper===str(local),"uniform original-error good event, including integer threshold");
  check(L.composed_recovery_failure_upper_IF_external_coverage_is_proved===(coverage===null?null:str(min(one,add(local,parse(coverage))))),"no fabricated list coverage");
  check(L.complete_declared_coefficient_scan_without_caps_is_required===true,"source event does not silently override runtime caps");
  check(L.conditioning_on_data_selected_multiple_truth_used===false&&L.original_errors_assumed_independent===false&&L.arbitrary_correlations_between_coverage_noise_and_labels_allowed_by_union===true&&L.source_promises_or_published_reduction_applicability_established===false&&L.decision_algorithm_supplied===false,"unconditional source union, no secret oracle");
}
function census(c){
  const q=c.modulus,m=c.original_rows,R=c.radius;check(q**m<=10000&&c.dimension===1,"complete finite original-label census");let collisions=0;
  for(let code=0;code<q**m;code++){let z=code;const a=[];for(let j=0;j<m;j++){a.push(z%q);z=Math.floor(z/q);}let found=false;
    for(let h=1;h<q&&!found;h++)found=a.every(x=>Math.min(x*h%q,(q-x*h%q)%q)<=2*R);if(found)collisions++;
  }
  separation(c.ledger);check(c.original_label_banks_checked===q**m&&c.banks_with_nonzero_close_codeword===collisions&&c.exact_separation_failure_probability===str(rat(BigInt(collisions),BigInt(q**m))),"all original-code collisions, not chosen easy labels");
  check(cmp(parse(c.exact_separation_failure_probability),parse(c.ledger.global_code_separation_failure_upper_used))<=0n,"union bound covers complete code population");return q**m;
}
function control(c){
  const raw=c.original_records,truth=c.truth_fixture_only,q=BigInt(raw[0].modulus),n=raw[0].label.length;
  check(raw.length>0&&raw.length%2===0&&new Set(raw.map(s=>s.source_id)).size===raw.length,"actual unique original paired bank");root(q);
  raw.forEach((s,j)=>check(BigInt(s.modulus)===q&&s.label.length===n&&s.label.every(x=>BigInt(x)>=0n&&BigInt(x)<q)&&mod(s.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(truth.original_secret[i]),0n)+BigInt(truth.original_errors[j]),q)===BigInt(s.value),"actual original noisy observations"));
  c.known_coefficient_completions.forEach(a=>{
    const w=truth.original_secret.map(x=>enc(mod(BigInt(a.signed_coefficient)*BigInt(x),q)));same(a.supplied_multiple,w,"truth multiple ONLY in calibration");
    const result=complete(raw,BigInt(a.signed_coefficient),w);same(a.completion,result,"independent original-root conditional completion");
    check(a.matches_truth_fixture===(JSON.stringify(result.candidate_secret)===JSON.stringify(truth.original_secret)),"truth comparison not receiver access");
  });
  const S=c.unknown_coefficient_list_scan;
  same(S.supplied_multiples,[truth.original_secret.map(x=>enc(mod(3n*BigInt(x),q))),Array(n).fill(0)],"same declared calibration list, not a substituted easy one");
  check(BigInt(S.public_verification_radius)===(q/32n>0n?q/32n:1n)&&S.declared_coefficient_bound===3,"actual calibration scan settings");
  check(c.multiple_inputs_prepared_from_truth_FOR_CALIBRATION_ONLY===true&&c.secret_or_errors_entered_completion===false,"no fabricated multiple source");return scan(raw,S);
}
function scaling(c){
  const n=c.dimension,q=3n**BigInt(n),m=2*(n+1)**3,R=q/BigInt(n),V=add(rat(q*q,3n*BigInt(n)**6n),rat(1n,2n));let d=0,g=1n;
  while(3n*g<=BigInt(n)){g*=3n;d++;}
  const L=c.safe_valuation_source_ledger;event(L);
  check(c.usable_valuation_budget===d&&BigInt(L.original_modulus)===q&&L.dimension===n&&L.original_rows===m&&BigInt(L.public_radius)===R&&L.maximum_supported_valuation===d&&L.true_original_second_moment_upper===str(V)&&L.external_covered_usable_multiple_list_failure_upper===null,"declared source parameters, no coverage probability");
  const C=c.declared_size_only_gap;let bound=BigInt(C.coefficient_size_bound),effective=bound<q/2n?bound:q/2n;g=1n;d=0;
  while(3n*g<=effective){g*=3n;d++;}
  event(C.worst_factor_local_source_event);
  const W=C.worst_factor_local_source_event;
  check(BigInt(W.original_modulus)===q&&W.dimension===n&&W.original_rows===m&&BigInt(W.public_radius)===R&&W.true_original_second_moment_upper===str(V)&&W.external_covered_usable_multiple_list_failure_upper===null,"size-only gap uses the SAME original source, no substituted favorable noise law");
  check(bound===BigInt(n)**9n&&BigInt(C.largest_allowed_ternary_factor)===g&&C.worst_allowed_valuation===d&&C.worst_factor_local_source_event.maximum_supported_valuation===d&&C.small_integer_coefficient_bound_guarantees_a_safe_valuation===false&&C.bound_is_derived_from_an_implemented_decision_reduction===false,"size is not useful valuation coverage");
}
function verify(p){
  check(p.status==="ORIGINAL_BANK_SMALL_MULTIPLE_COMPLETION_AND_UNIFORM_VERIFICATION_REVIEW_PENDING","review-pending result");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_small_multiple_completion.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_SMALL_MULTIPLE_COMPLETION.md")),"current producer and derivation");
  const deps=["native_affine_fibre_relaxation.py","native_classical_modulus_descent.py","native_full_root_slice.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.original_data_controls.length===3&&p.complete_original_code_censuses.length===2&&p.scaling_source_events_and_size_gaps.length===4,"declared live scope");
  const trials=p.original_data_controls.map(control),banks=p.complete_original_code_censuses.map(census);p.scaling_source_events_and_size_gaps.forEach(scaling);
  check(p.accepted_speedup_candidate===false&&p.new_active_negative_result_created===false,"neither speedup nor broad negative admitted");
  return {verified:true,known_multiple_calibrations:p.original_data_controls.reduce((s,c)=>s+c.known_coefficient_completions.length,0),complete_list_trials:trials.reduce((a,b)=>a+b,0),original_label_banks_censused:banks.reduce((a,b)=>a+b,0),decision_algorithm_or_list_coverage_supplied:false};
}
module.exports={verify,quotient,complete,separation,event};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

"use strict";
// Independent exact RREF, coordinate uniqueness, canonical substitution and ring lift.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),C=require("./native_small_alphabet_decoder_crosscheck.js"),M=require("./native_small_multiple_completion_crosscheck.js");
const {check,same,rat,parse,str,add,mul,cmp,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_partial_coordinate_decoder.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod=(x,q)=>(x%q+q)%q,F=x=>(x%3+3)%3,min=(a,b)=>cmp(a,b)<=0n?a:b;
const enc=x=>x>=-9007199254740991n&&x<=9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
function integer(x){check((typeof x==="number"&&Number.isSafeInteger(x))||typeof x==="string","exact integer transport");const y=BigInt(x);check(enc(y)===x,"canonical integer");return y;}
function flags(o,yes,no){yes.forEach(k=>check(o[k]===true,"required scope "+k));no.forEach(k=>check(o[k]===false,"unsupported claim "+k));}
function affine(rows,rhs,D,coordinates){
  const A=rows.map((r,i)=>[...r,rhs[i]]);let rank=0;const augmentedPivots=[];
  for(let j=0;j<=D&&rank<A.length;j++){
    let p=rank;while(p<A.length&&!A[p][j])p++;if(p===A.length)continue;
    [A[rank],A[p]]=[A[p],A[rank]];const unit=A[rank][j];A[rank]=A[rank].map(x=>x*unit%3);
    for(let i=0;i<A.length;i++)if(i!==rank&&A[i][j]){const a=A[i][j];A[i]=A[i].map((x,k)=>F(x-a*A[rank][k]));}
    augmentedPivots.push(j);rank++;
  }
  const reduced=A.slice(0,rank),pivots=augmentedPivots.filter(j=>j<D),free=Array.from({length:D},(_,j)=>j).filter(j=>!pivots.includes(j)),inconsistent=augmentedPivots.includes(D);
  const certs=coordinates.map(j=>{const row=pivots.includes(j)?pivots.indexOf(j):null,depend=row===null?[]:free.filter(k=>reduced[row][k]).map(k=>[k,reduced[row][k]]),fixed=!inconsistent&&row!==null&&!depend.length;
    return{column:j,pivot_row:row,free_variable_dependence:depend,fixed,value:fixed?reduced[row][D]:null};});
  return{feature_dimension:D,equations:rows.length,augmented_rank:rank,coefficient_rank:pivots.length,inconsistent,
    pivot_columns:pivots,free_columns:free,reduced_nonzero_rows:reduced,coordinate_certificates:certs,all_requested_coordinates_fixed:certs.every(c=>c.fixed),
    input_system_sha256:digest({rows,rhs}),free_variables_assigned:false};
}
function features(u,v,method){return C.layout(u.length,method).map(([kind,ij])=>{
  if(kind==="v")return v[ij[0]];if(kind==="u")return u[ij[0]];if(kind==="u2")return u[ij[0]]**2%3;
  if(kind==="u2j")return u[ij[0]]**2*u[ij[1]]%3;return ij.reduce((a,j)=>a*u[j],1)%3;
});}
function result(raw,R){
  const q=integer(raw[0].modulus),n=raw[0].label.length,m=raw.length,method=R.method,D=C.layout(n,method).length,entries=m*(D+1),alphabet=method==="cubic"?[-1,0,1]:[-1,1];
  check(m>0&&m%2===0&&new Set(raw.map(r=>r.source_id)).size===m&&n>0,"complete distinct original pairs");
  let a=q;while(a%3n===0n)a/=3n;check(a===1n&&q>=3n&&(method!=="cubic"||q>=9n),"actual full-root ring");
  raw.forEach(r=>check(integer(r.modulus)===q&&r.label.length===n&&r.label.every(x=>integer(x)>=0n&&integer(x)<q)&&integer(r.value)>=0n&&integer(r.value)<q&&typeof r.source_id==="string"&&r.source_id,"canonical original record"));
  check(R.algorithm==="CERTIFIED_AFFINE_SECRET_COORDINATES_AND_CANONICAL_SUBSTITUTION"&&integer(R.original_modulus)===q&&R.dimension===n&&R.original_records_paid_once===m&&R.feature_dimension===D&&R.logical_augmented_matrix_entries===entries,"same actual original system");
  same(R.required_original_error_alphabet,alphabet,"correct strict signed/triplet alphabet");
  flags(R,[],["matrix_cap_includes_Python_and_FLINT_overhead","actual_planted_secret_or_noise_law_certified","full_feature_rank_required","free_feature_coordinates_guessed","truth_or_error_input_used","new_quantum_algorithm_or_general_Gaussian_solver"]);
  check(R.classical_secret_hypotheses_enumerated===0,"no free-variable search");
  if(entries>R.max_matrix_entries){check(R.status==="WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION"&&R.compiled_rows===0&&R.field_elimination_calls===0&&R.candidate_secret===null,"whole preflight cap before any field solve");return{rows:0,rank:null};}
  const base=method==="cubic"?9n:3n,equations=raw.map(r=>C.equation(r.label.map(a=>Number(integer(a)%base)),Number(integer(r.value)%base),method)),rows=equations.map(a=>a[0]),rhs=equations.map(a=>a[1]);
  check(R.original_records_sha256===digest(raw)&&R.compiled_system_sha256===digest({basis:C.layout(n,method),rows,rhs})&&R.compiled_rows===m,"actual integer-polynomial equations");
  const columns=Array.from({length:n},(_,j)=>method==="cubic"?j:D-n+j),low=affine(rows,rhs,D,columns);
  same(R.low_coordinate_model,low,"exact independent augmented RREF and low-coordinate dependence");check(R.coefficient_rank===low.coefficient_rank,"actual rank retained even when deficient");
  if(low.inconsistent){check(R.status==="INCONSISTENT_SMALL_ALPHABET_EQUATIONS"&&R.candidate_secret===null&&R.field_elimination_calls===1,"inconsistent data rejected");return{rows:m,rank:low.coefficient_rank};}
  if(!low.all_requested_coordinates_fixed){check(R.status==="SECRET_COORDINATES_NOT_LINEARLY_UNIQUE_NOT_NO_SECRET"&&R.candidate_secret===null&&R.field_elimination_calls===1,"unknown coordinates are not assigned");return{rows:m,rank:low.coefficient_rank};}
  const u=low.coordinate_certificates.map(c=>c.value);same(R.low_trit_coordinates,u,"actual certified low secret");let v=null,physical,lower,prefix;
  if(method==="cubic"){
    const initial=features(u,Array(n).fill(0),method),nextRows=rows.map(r=>r.slice(-n)),nextRhs=rhs.map((b,i)=>F(b-rows[i].reduce((a,x,j)=>a+x*initial[j],0))),next=affine(nextRows,nextRhs,n,Array.from({length:n},(_,j)=>j));
    same(R.next_coordinate_model,next,"canonical feature substitution before next digits");check(R.field_elimination_calls===2,"both field eliminations charged");
    if(next.inconsistent){check(R.status==="INCONSISTENT_CANONICAL_FEATURE_SUBSTITUTION"&&R.candidate_secret===null,"nonphysical feature fit rejected");return{rows:m,rank:low.coefficient_rank};}
    if(!next.all_requested_coordinates_fixed){check(R.status==="NEXT_SECRET_COORDINATES_NOT_LINEARLY_UNIQUE_NOT_NO_SECRET"&&R.candidate_secret===null,"next digits not guessed");return{rows:m,rank:low.coefficient_rank};}
    v=next.coordinate_certificates.map(c=>c.value);physical=features(u,v,method);lower=u.map((x,i)=>x+3*v[i]);prefix=9n;
  }else{check(R.field_elimination_calls===1,"quadratic needs only secret coordinates");physical=features(u,null,method);lower=u;prefix=3n;}
  const consistent=rows.every((r,i)=>F(r.reduce((a,x,j)=>a+x*physical[j],0)-rhs[i])===0);
  if(!consistent){check(R.status==="CANONICAL_FEATURES_FAIL_COMPILED_EQUATIONS"&&R.candidate_secret===null,"nonlinear equations all verified");return{rows:m,rank:low.coefficient_rank};}
  same(R.canonical_feature_vector,physical,"actual physical nonlinear features");same(R.low_secret,lower,"recovered low prefix");check(R.prefix_modulus===Number(prefix)&&R.nonlinear_features_verified===true,"canonical verification required");
  let candidate;
  if(q===prefix){candidate=lower;same(R.full_root_lift,{applied:false,prefix_modulus:Number(prefix),remaining_modulus:1,root_already_complete:true},"root already complete");}
  else{
    const c=q/prefix,w=lower.map(x=>enc(c*BigInt(x))),lift=M.complete(raw,c,w),H=R.full_root_lift;
    if(lift.candidate_secret===null){check(R.status==="INCONSISTENT_OR_UNSUPPORTED_ORIGINAL_HIGHER_ROOT_LIFT"&&R.candidate_secret===null,"original higher lift stays incomplete");return{rows:m,rank:low.coefficient_rank};}
    same(H,{applied:true,prefix_modulus:Number(prefix),remaining_modulus:enc(c),public_basis_model:lift.public_basis_model,
      rounding_transcript:lift.rounding_transcript.map(t=>({source_id:t.source_id,corrected_original_response:t.corrected_original_response,rounded_higher_equation:t.rounded_missing_quotient_equation})),
      higher_solution:lift.missing_quotient_solution,all_original_higher_equations_consistent:true,new_independent_samples_created:false},"independent actual full-root lift");candidate=lift.candidate_secret;
  }
  const residuals=raw.map(r=>enc(mod(integer(r.value)-r.label.reduce((a,x,i)=>a+integer(x)*integer(candidate[i]),0n)+q/2n,q)-q/2n));same(R.original_candidate_residuals,residuals,"all full original residuals");
  if(!residuals.every(e=>alphabet.includes(e))){check(R.status==="FULL_ROOT_ALPHABET_FIT_FAILED"&&R.candidate_secret===null,"strict original alphabet still required");return{rows:m,rank:low.coefficient_rank};}
  same(R.candidate_secret,candidate,"actual full-root classical candidate");flags(R,["fixed_instance_alphabet_uniqueness_certified","planted_secret_recovery_requires_true_alphabet_promise"],[]);
  check(R.status==="UNIQUE_ALPHABET_COMPATIBLE_FULL_ROOT_SECRET_FROM_FIXED_COORDINATES","coordinate-certified success");return{rows:m,rank:low.coefficient_rank};
}
function source(S){
  const G=require("./native_gaussian_quotient_completion_crosscheck.js"),R=S.full_feature_reference_same_source;G.source(R);
  const terms=S.secret_coordinate_valuation_terms;check(terms.length===R.valuation_terms.length,"same declared counterfactual valuations");
  let total=add(parse(R.original_radius_event_failure_upper),parse(R.original_code_separation_ledger.global_code_separation_failure_upper_used));
  terms.forEach((t,i)=>{const old=R.valuation_terms[i],base=old.conditional_rank_ledger.zero_row_base_rank_budget;
    check(t.valuation===old.valuation&&t.whole_bank_outside_triplet_failure_upper===old.whole_original_bank_outside_triplet_failure_upper,"same full bank tail and valuation");
    same(t.Gaussian_derived_error_law,old.Gaussian_derived_error_law,"same actual derived width");same(t.zero_error_base_coordinate_budget,base,"only base event is needed");
    const failure=min(one,add(parse(base.rank_failure_upper),parse(t.whole_bank_outside_triplet_failure_upper)));
    check(t.fixed_valuation_secret_recovery_failure_upper===str(failure),"base rank plus retained truncation");total=add(total,failure);
    flags(t,["secret_translation_is_only_a_proof_operation"],["nonzero_noise_probability_floor_required"]);
  });
  check(S.uniform_local_secret_recovery_failure_upper===str(min(one,total)),"all original noise/separation/valuation events retained");
  check(S.default_matrix_cap_feasible===(integer(R.logical_matrix_entries_for_each_decoder)<=2000000n),"logical matrix cap not erased");
  flags(S,["all_original_radius_separation_truncation_and_valuation_events_retained"],["actual_source_or_multiple_producer_supplied","recovery_with_missing_external_coverage_claimed"]);
  const budgets=R.valuation_terms[0].conditional_rank_ledger,required=[budgets.zero_row_base_rank_budget,budgets.nonzero_row_quadratic_rank_budget].map(b=>integer(b.power_block)*BigInt(2*b.feature_block_dimension+66));
  const old=required.reduce((a,b)=>a>b?a:b);check(integer(S.full_feature_rank_sufficient_original_rows_reference)===2n*((old+1n)/2n),"sample comparison is sufficient, not a lower bound");
}
function verify(p){
  check(p.status==="CERTIFIED_PARTIAL_SECRET_COORDINATES_AND_BASE_ONLY_GAUSSIAN_COMPLETION_REVIEW_PENDING","review pending");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_partial_coordinate_decoder.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_PARTIAL_COORDINATE_DECODER.md")),"current provenance");
  const deps=["native_small_alphabet_decoder.py","native_small_multiple_completion.py","native_classical_modulus_descent.py","native_full_root_slice.py","native_gaussian_quotient_completion.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.actual_original_data_controls.length===4&&p.falsifier_controls.length===5&&p.base_only_Gaussian_source_profiles.length===3,"declared controls and source profiles");
  let equations=0;p.actual_original_data_controls.forEach(c=>{const r=result(c.original_records,c.partial_decoder);C.result(c.original_records,c.full_feature_reference);
    const truth=c.truth_fixture_only.original_secret,q=integer(c.original_records[0].modulus);c.original_records.forEach((row,j)=>check(mod(row.label.reduce((a,x,i)=>a+integer(x)*integer(truth[i]),0n)+integer(c.truth_fixture_only.original_errors[j]),q)===integer(row.value),"actual frozen original source equations"));
    check(c.matches_truth_fixture===(JSON.stringify(c.partial_decoder.candidate_secret)===JSON.stringify(truth))&&c.calibration_is_unbounded_Gaussian_source===false,"calibration not a Gaussian advantage");equations+=r.rows;});
  p.falsifier_controls.forEach(c=>{result(c.original_records,c.partial_decoder);check(c.matches_planted_truth===(JSON.stringify(c.partial_decoder.candidate_secret)===JSON.stringify(c.truth_fixture_only.original_secret))&&c.false_source_promise_repaired_by_truth===false,"false planted premise not repaired");});
  p.base_only_Gaussian_source_profiles.forEach(source);
  flags(p,[],["accepted_speedup_candidate","new_active_negative_result_created","Gaussian_LWE_solver_or_new_quantum_algorithm","novelty_claim"]);
  return{verified:true,actual_original_equations:equations,rank_deficient_success_controls:3,falsifiers:5,base_only_Gaussian_profiles:3,
    Gaussian_transcendental_boxes_recomputed:false,independent_source_proof_review_pending:true};
}
module.exports={verify,result,affine,source};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

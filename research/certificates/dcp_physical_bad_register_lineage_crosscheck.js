"use strict";
// Exact density and lineage replay. No private phase evaluator is a resource.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js");
const {check,rat,parse,str,add,sub,mul,div,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/phase_workbench/dcp_physical_bad_register_lineage.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m),min=(a,b)=>cmp(a,b)<=0n?a:b;
const enc=x=>x<=9007199254740991n?Number(x):String(x),bits=x=>x===0n?0:x.toString(2).length;
function density(A){
  const a=parse(A.PRIVATE_density_zero_population),v=parse(A.PRIVATE_density_phase_visibility),ids=A.original_state_receipt_IDs;
  check(cmp(a,zero)>=0n&&cmp(a,one)<=0n&&cmp(v,zero)>=0n&&cmp(mul(v,v),mul(rat(4n),mul(a,sub(one,a))))<=0n,"positive density cone");
  check(Number.isSafeInteger(A.modulus)&&A.modulus>=2&&Number.isSafeInteger(A.measured_Fourier_label)&&A.measured_Fourier_label>=0&&A.measured_Fourier_label<A.modulus&&ids.length>0&&new Set(ids).size===ids.length&&ids.every(s=>typeof s==="string"&&s.length>0),"physical source identities and label");
  check(A.source_noise_parameters_or_phase_given_to_solver===false&&A.phase_visibility_alone_certifies_secret_information_at_zero_label===false&&A.density_expression==="[[a,v*exp(-2*pi*i*k*s/N)/2],[v*exp(2*pi*i*k*s/N)/2,1-a]]","private statistics and visibility are not oracle access or zero-label information");return {a,v};
}
function controls(C){
  const [L,R]=C.input_audits,l=density(L),r=density(R),params=C.private_source_parameters;
  const checkInput=(A,p,b)=>{const P=parse(p),B=parse(b);check(A.PRIVATE_density_zero_population===str(add(div(sub(one,P),rat(2n)),mul(P,B)))&&A.PRIVATE_density_phase_visibility===str(sub(one,P)),"physical good/basis mixture");};
  checkInput(L,params.left_bad_probability,params.left_bad_zero_probability);checkInput(R,params.right_bad_probability,params.right_bad_zero_probability);
  check(L.modulus===R.modulus&&L.modulus===32&&L.measured_Fourier_label===11&&R.measured_Fourier_label===7&&C.hidden_s_ONLY_FOR_LITERAL_CALIBRATION===13,"literal reference parameters");
  check(C.literal_branches.length===2,"both actual outcomes retained");
  C.literal_branches.forEach((X,branch)=>{
    const A=X.merge,b=branch===0?r.a:sub(one,r.a),prob=add(mul(l.a,b),mul(sub(one,l.a),sub(one,b)));
    check(A.branch===branch&&A.exact_branch_probability===str(prob)&&A.branch_chosen_for_free===false&&A.coherent_phase_evaluator_or_chosen_label_query_supplied===false,"true quantum branch probability");
    check(A.conditional_product_source_model_required===true&&A.receipt_IDs_prove_statistical_independence===false,"disjoint physical receipts are necessary, not a statistical independence proof");
    const view=I=>({modulus:I.modulus,measured_Fourier_label:I.measured_Fourier_label,original_state_receipt_IDs:I.original_state_receipt_IDs,merge_depth:I.merge_depth});
    same(A.input_public_views,[view(L),view(R)],"solver sees no private noise, phase or bad flags");
    check(Number.isFinite(X.diagnostic_literal_probability)&&Math.abs(X.diagnostic_literal_probability-Number(prob[0])/Number(prob[1]))<1e-12,"literal target probability");
    if(cmp(prob,zero)===0n){check(A.status==="IMPOSSIBLE_BRANCH_NOT_A_POSTSELECTED_STATE"&&A.output_audit===null&&X.literal_density_agrees_with_exact_output===false&&X.diagnostic_output_visibility===0,"impossible output is not an accepted state");return;}
    const population=div(mul(l.a,b),prob),visibility=div(mul(l.v,r.v),mul(rat(2n),prob)),out=A.output_audit;density(out);
    check(A.status==="ACTUAL_CNOT_MEASURED_TARGET_BRANCH"&&out.PRIVATE_density_zero_population===str(population)&&out.PRIVATE_density_phase_visibility===str(visibility),"normalized physical density");
    const label=(L.measured_Fourier_label+(branch===0?1:-1)*R.measured_Fourier_label+L.modulus)%L.modulus;
    check(out.measured_Fourier_label===label&&out.modulus===L.modulus&&out.merge_depth===1,"sum/difference label and physical depth");same(out.original_state_receipt_IDs,[...L.original_state_receipt_IDs,...R.original_state_receipt_IDs],"all disjoint ancestors retained");
    check(X.literal_density_agrees_with_exact_output===true&&Math.abs(X.diagnostic_output_visibility-Number(visibility[0])/Number(visibility[1]))<1e-12,"literal normalized coherence");
  });
}
function power(B){
  const a=parse(B.base),e=BigInt(B.exponent),b=B.bits,cap=B.max_bit_work,required=e*BigInt(Math.max(bits(a[0]),bits(a[1])));
  check(cmp(a,zero)>=0n&&cmp(a,one)<=0n&&e>=0n&&Number.isSafeInteger(b)&&b>0&&cap===524288&&BigInt(B.required_operand_bits_upper)===required,"whole exact rational power scope");
  if(required>BigInt(cap)){check(B.status==="UNKNOWN_EXACT_POWER_CAP"&&B.lower==="0"&&B.upper==="1","capped exact power is unknown, not zero");return;}
  const numerator=a[0]**e,denominator=a[1]**e,scale=2n**BigInt(b);
  check(B.status==="CERTIFIED_INTEGER_DYADIC_POWER"&&B.lower===str(rat(numerator*scale/denominator,scale))&&B.upper===str(rat((numerator*scale+denominator-1n)/denominator,scale)),"directed exact visibility power");
}
function lineage(L){
  const n=L.log2_original_modulus,f=L.failure_parameter,d=L.balanced_merge_depth;check(Number.isSafeInteger(n)&&n>=3&&Number.isSafeInteger(f)&&f>0&&f<=64&&Number.isSafeInteger(d)&&d>=0&&d<=4096,"scoped lineage model");
  const denominator=BigInt(n)**BigInt(f),leaves=2n**BigInt(d),p=rat(1n,denominator),B=L.visibility_exact_power_box;power(B);
  check(L.legal_per_register_bad_probability===str(p)&&L.bad_conditional_density==="I/2 from equal bad basis-state mixture"&&BigInt(L.disjoint_original_state_leaves)===leaves&&B.base===str(sub(one,p))&&BigInt(B.exponent)===leaves&&L.exact_visibility_formula==="(1-p_bad)^original_leaves","physical balanced-error visibility, not label-only progress");
  const blocks=leaves/denominator,budget=blocks<BigInt(B.bits)?blocks:BigInt(B.bits),bernoulli=rat(1n,2n**budget),upper=min(bernoulli,parse(B.upper));
  check(BigInt(L.reciprocal_Bernoulli_complete_blocks)===blocks&&L.visibility_Bernoulli_upper===str(bernoulli)&&L.output_phase_visibility_upper===str(upper)&&L.best_single_target_parity_success_upper===str(div(add(one,upper),rat(2n))),"safe visibility and Helstrom parity ceiling");
  let copies=null;if(cmp(upper,rat(1n,2n))<=0n){const need=div(one,mul(rat(8n),mul(upper,upper)));copies=(need[0]+need[1]-1n)/need[1];}
  check(L.necessary_INDEPENDENT_target_copies_for_parity_success3over4_lower===(copies===null?null:enc(copies))&&L.parity_copy_lower_bound_uses_Pinsker_and_gamma_at_most_half===(copies!==null),"independent target-copy information price");
  ["visibility_bound_is_for_LEGAL_MAX_RATE_BALANCED_subclass_NOT_all_smaller_rates","target_label_would_encode_only_parity_not_full_secret","parity_copy_bound_requires_actual_label_N_over_2_AND_independent_targets","all_realized_branches_have_probability_half_IN_balanced_model"].forEach(k=>check(L[k]===true,"legal restricted source gate "+k));
  ["label_target_success_certifies_phase_information","any_output_ancestor_reuse_is_free","source_bad_flags_given_to_algorithm","arbitrary_collective_DCP_decoder_or_fault_correction_excluded"].forEach(k=>check(L[k]===false,"no additional resource or global no-go "+k));
  check(L.independent_source_noise_conditional_on_common_secret_required===true&&L.source_ID_uniqueness_establishes_statistical_independence===false,"conditional independent source law, not separate secret twirls or receipt guesses");
}
function tradeoff(T){
  const n=T.lattice_dimension,N=n*(4*n+1);check(Number.isSafeInteger(n)&&n>=2&&n<=4096,"source lattice dimension");
  let d=Math.floor(Math.sqrt(N));if(d*d<N)d++;const leaves=2n**BigInt(d);let f=1;while(BigInt(N)**BigInt(f)<2n*leaves)f++;
  same(T.published_M,{base:2,exponent:4*n},"primary embedding box");
  check(T.published_DCP_log2N===N&&T.illustrative_sqrt_log_depth_NOT_universal_sieve_requirement===d&&BigInt(T.balanced_original_leaves_at_illustrative_depth)===leaves&&T.minimum_integer_f_for_Bernoulli_visibility_lower_at_least_half===f&&T.diagnostic_unique_SVP_approximation_n_power===str(rat(BigInt(1+4*f),2n))&&T.published_prime_lower_bound_n_power===2+2*f,"noise repair changes the source promise and resources");
  check(T.diagnostic_approximation_exceeds_LLL_2_to_nminus1over2===(BigInt(n)**BigInt(1+4*f)>2n**BigInt(n-1))&&T.variable_f_is_covered_by_constant_f_polynomial_reduction===false&&T.raising_f_removes_all_algorithmic_blockers===false&&T.different_sieves_or_collective_noise_handling_excluded===false,"no variable-f uniformity or universal sieve exclusion");
}
function verify(R){
  check(R.status==="PHYSICAL_DCP_BAD_REGISTER_CNOT_LINEAGE_AUDIT_NOT_A_GENERAL_DCP_NO_GO"&&R.producer_sha256===hash(path.join(ROOT,"theorems/dcp_physical_bad_register_lineage.py"))&&R.derivation_sha256===hash(path.join(ROOT,"research/DCP_PHYSICAL_BAD_REGISTER_LINEAGE.md"))&&R.primary_latex_sha256===hash(path.join(ROOT,"research/literature_cache/cs_0304005_source/quantum_average.tex")),"current model and actual primary source");
  const deps=["dcp_sample_workbench.py","dcp_carry_packets.py","dcp_physical_phase_noise.py","native_basis_lottery.py","native_small_multiple_completion.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"direct source/math dependencies");deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  const C=R.existing_state_input_theorem_contract;
  check(C.theorem_contract_id==="THM-REGEV-USVP-TO-DCP-2003"&&C.failure_parameter===1&&C.maximum_bad_register_probability==="1/log2(N) for the f=1 theorem specialization"&&C.current_workbench_models_bad_registers===false&&C.full_family_coverage===false&&C.bad_register_state==="arbitrary computational-basis state |b,x> rather than a coset state"&&C.forbidden_resources.includes("coherent phase evaluator"),"do not silently promote old ideal source contract to full bad-register coverage");
  check(R.literal_physical_merge_controls.length===6&&R.balanced_bad_register_lineage_profiles.length===12&&R.source_reduction_failure_tradeoffs.length===4,"all declared source controls");
  check(R.pure_bad_controls_are_components_NOT_all_promised_source_distributions===true,"basis-state components are not full always-bad promised distributions");
  R.literal_physical_merge_controls.forEach(controls);R.balanced_bad_register_lineage_profiles.forEach(lineage);R.source_reduction_failure_tradeoffs.forEach(tradeoff);
  const correlated=R.correlated_bad_register_countercontrol,p=parse(correlated.legal_marginal_bad_probability);
  check(correlated.legal_marginal_bad_probability==="1/32"&&correlated.noise_recipe==="all good with1-p; all bad00 or bad11 with p/2 each"&&correlated.marginal_zero_population==="1/2"&&correlated.marginal_phase_visibility===str(sub(one,p)),"explicit correlated source has same marginals");
  same(correlated.disjoint_receipt_IDs,["correlated:left","correlated:right"],"disjoint IDs do not rescue statistical product");
  same(correlated.literal_joint_branches,[{branch:0,exact_branch_probability:str(div(add(one,p),rat(2n))),exact_output_visibility:str(div(sub(one,p),add(one,p)))},{branch:1,exact_branch_probability:str(div(sub(one,p),rat(2n))),exact_output_visibility:"1"}],"correlated CNOT can herald a clean difference branch");
  check(correlated.marginal_product_CNOT_formula_applies===false&&correlated.IDs_or_marginal_rates_prove_independence===false&&correlated.countercontrol_claimed_as_all_published_source_models===false,"correlation scope counterexample only");
  const herald=R.single_register_heralding_countercontrol;
  check(herald.actual_DCP_modulus===32&&herald.nonzero_measured_label===7&&herald.complete_hidden_sweep_FOR_CALIBRATION_ONLY===32&&herald.exact_uniform_secret_good_density==="I/2"&&herald.exact_balanced_bad_density==="I/2","nontrivial character twirl, not a phase evaluator");
  same(herald.fixed_effects,["Z0","Z1","Xplus","Yplus","identity"],"fixed one-copy instruments");same(herald.exact_good_AND_bad_acceptance_probabilities,["1/2","1/2","1/2","1/2","1"],"good and bad twirled states coincide");
  check(herald.diagnostic_same_good_bad_probabilities.length===5&&herald.diagnostic_same_good_bad_probabilities.every((x,j)=>Number.isFinite(x)&&Math.abs(x-(j===4?1:.5))<1e-12)&&herald.PSD_effect_rejecting_both_bad_basis_states_must_be_zero===true&&herald.source_phase_or_other_register_information_given_to_filter===false&&herald.label_zero_EXCEPTION_has_known_phase_but_no_hidden_secret_information===true&&herald.all_collective_or_posterior_conditioned_purification_excluded===false,"no free universal clean flag or collective no-go");
  const bridge=R.existing_physical_Z_balanced_subclass_bridge;
  check(bridge.legal_balanced_bad_rate_at_logN5==="1/5"&&bridge.equivalent_physical_Z_flip_rate==="1/10"&&bridge.exact_one_register_phase_contrast==="4/5","bad mixture corresponds to HALF the phase-flip rate");
  same(bridge.left_public_packet_labels,[[1,1,1]],"actual left packet chart");same(bridge.right_public_packet_labels,[[1,1,0]],"actual right packet chart");
  // Solve the actual one-equation F2 kernels, not a fitted noise multiplier.
  same(bridge.left_actual_kernel_rows,[3,1,2],"left nullspace coordinate rows");same(bridge.right_actual_kernel_rows,[1,1,2],"right nullspace coordinate rows");
  const countbits=x=>x.toString(2).replaceAll("0","").length;
  same(bridge.existing_packet_noise_contrasts,[0,1,2,3].map(h=>{const support=[3,1,2,1,1,2].reduce((s,r)=>s+(countbits(r&h)%2),0),v=str(rat(4n**BigInt(support),5n**BigInt(support)));return {logical_Fourier_mask:h,original_physical_phase_error_support:support,exact_existing_physical_Z_contrast:v,exact_balanced_bad_contrast:v};}),"all packet physical error Fourier masks");
  check(bridge.diagnostic_balanced_density_channel_error>=0&&bridge.diagnostic_balanced_density_channel_error<1e-12&&Math.abs(bridge.diagnostic_biased_basis_density_channel_error-.1)<1e-12&&bridge.balanced_independent_subclass_covered_by_existing_physical_Z===true&&bridge.FULL_arbitrary_basis_contamination_promise_covered_by_existing_physical_Z===false&&bridge.unknown_coset_phases_are_made_classically_known_by_noise_bridge===false,"reuse specific noise tools without granting full bad-source coverage or known phases");
  ["actual_lattice_to_coset_state_generator_implemented","coherent_phase_evaluator_or_chosen_label_queries_supplied","full_bad_register_DCP_solver_supplied","additional_state_preparation_or_gate_errors_certified","accepted_speedup_candidate","new_active_negative_result_created"].forEach(k=>check(R[k]===false,"no granted source or unproved solver "+k));
  check(R.research_decision==="REQUIRE_PHASE_VISIBILITY_AND_REAL_BAD_REGISTER_COVERAGE_NOT_JUST_SIEVE_LABEL_SUCCESS","research priority is physical information");
  return {verified:true,physical_CNOT_branch_controls:12,balanced_lineage_profiles:12,source_tradeoffs:4,correlation_and_single_copy_scope_controls:2,full_DCP_solver_supplied:false};
}
module.exports={verify,lineage,tradeoff,controls};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

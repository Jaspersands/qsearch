"use strict";
// Exact parameter/abort inequalities. Gaussian law and a decision solver are premises.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one}=require("./cyclotomic_exact.js"),M=require("./native_small_multiple_completion_crosscheck.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_rounded_gaussian_tolerance.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),bits=x=>x===0n?0:x.toString(2).length;
const min=(a,b)=>cmp(a,b)<=0n?a:b,enc=x=>x<=9007199254740991n?Number(x):String(x);
function root(q){let r=0;check(q>=9n,"Gaussian tolerance root at least9");while(q%3n===0n){r++;q/=3n;}check(q===1n,"actual ternary root");return r;}
function ceilLog2(x){if(cmp(x,one)<=0n)return 0;let k=Math.max(0,bits(x[0])-bits(x[1]));if(2n**BigInt(k)*x[1]<x[0])k++;return k;}
function isqrt(n){check(n>=0n,"nonnegative exact square-root input");if(n===0n)return 0n;let x=1n<<BigInt(Math.ceil(bits(n)/2));for(;;){const y=(x+n/x)/2n;if(y>=x)return x;x=y;}}
function budget(L){
  const q=BigInt(L.original_modulus),n=L.dimension,m=BigInt(L.original_rows),a=parse(L.D_alpha_width),eps=parse(L.hypothetical_decision_advantage),delta=parse(L.whole_bank_unconditioned_adapter_failure_upper);
  root(q);check(n>0&&m>0n&&cmp(a,rat(0n))>0n&&cmp(a,one)<0n&&cmp(eps,rat(0n))>0n&&cmp(eps,one)<=0n&&cmp(delta,rat(0n))>=0n&&cmp(delta,one)<=0n,"explicit exact Gaussian and advantage parameters");
  const ratio=div(rat(q*m),eps),ratio4=rat(ratio[0]**4n,ratio[1]**4n),t=ceilLog2(ratio4),eta=div(eps,rat(BigInt(4*t))),margin=sub(eta,mul(rat(2n),delta)),cap=q/4n-1n;
  const squareA=mul(a,a),threshold=cmp(margin,rat(0n))>0n?div(mul(mul(rat(7n*q*q,11n),squareA),mul(margin,margin)),rat(m)):rat(0n);
  const b=cmp(margin,rat(0n))>0n?isqrt(threshold[0]/threshold[1]):0n,B=b<cap?b:cap,square=div(rat(11n*m*B*B,7n),mul(squareA,rat(q*q)));
  const prime=B?div(mul(rat(B),eps),rat(2n*q*BigInt(t))):null,C=prime?div(rat(32n),mul(prime,prime)):null,ceiling=C?(C[0]+C[1]-1n)/C[1]:null;
  check(2n**BigInt(t)*ratio4[1]>=ratio4[0]&&2n**BigInt(t-1)*ratio4[1]<ratio4[0],"exact terminal hybrid count, not a floating logarithm");
  const hybrid=rat(m*m*q,4n*2n**BigInt(t)),target=div(rat(eps[0]**4n,eps[1]**4n),rat(4n*q*q*m*m));
  check(L.terminal_hybrid_steps===t&&L.terminal_hybrid_distance_squared_upper===str(hybrid)&&L.target_terminal_hybrid_distance_squared_upper===str(target)&&cmp(hybrid,target)<=0n,"conditional terminal randomization inequality");
  check(L.noise_tolerance_target===str(eta)&&L.two_adapter_losses===str(mul(rat(2n),delta))&&L.ideal_tolerance_margin===str(margin)&&BigInt(L.maximum_integer_shift_certified)===B&&BigInt(L.modulus_tolerance_cap)===cap&&L.ideal_translation_TV_squared_upper===str(square),"Gaussian translation and BOTH encoding losses");
  if(B)check(cmp(square,mul(margin,margin))<=0n,"positive integer tolerance fits exact TV budget");
  check(L.status===(B?"POSITIVE_SOURCE_TOLERANCE_UNDER_EXPLICIT_GAUSSIAN_PROMISE":"NO_POSITIVE_TOLERANCE_CERTIFIED_BY_THIS_BUDGET")&&L.epsilon_prime_IF_published_reduction_contract_is_met===(prime?str(prime):null)&&L.coefficient_size_ceiling_IF_published_reduction_contract_is_met===(ceiling?enc(ceiling):null),"hypothetical reduction ceiling is not a solver");
  check(L.uniform_secret_nonprimitive_probability_IF_uniform===str(rat(1n,3n**BigInt(n)))&&L.Gaussian_width_is_standard_deviation===false&&L.rounding_commutes_with_integer_translation===true&&L.coprime_secret_required_for_terminal_hybrid_argument===true&&L.source_is_IID_continuous_D_alpha_then_exact_integer_rounding_required===true,"normalization and primitive-secret premises");
  check(L.actual_Gaussian_law_or_adapter_failure_established===false&&L.conditioning_on_adapter_success_erases_its_loss===false&&L.published_discrete_Gaussian_corollary_imported===false&&L.full_general_reduction_or_decision_algorithm_implemented===false,"source contract, no oracle");
  check(L.translation_bound_is_for_fixed_or_original_noise_independent_shifts===true&&L.conditioning_on_data_selected_shift_or_query_history_is_covered===false,"fixed-shift TV is not a postselected/adaptive-history guarantee");
}
function profile(c){
  const n=c.dimension,q=3n**BigInt(n),m=BigInt(2*(n+1)**3),a=rat(1n,BigInt(n)**3n),I=c.ideal_exact_rounding_budget,A=c.charged_adapter_budget,Z=c.adapter_budget_with_no_margin;
  [I,A,Z].forEach(budget);check(BigInt(I.original_modulus)===q&&BigInt(I.original_rows)===m&&I.D_alpha_width===str(a)&&I.dimension===n&&I.hypothetical_decision_advantage==="1/10"&&I.whole_bank_unconditioned_adapter_failure_upper==="0","same actual declared source grid");
  [A,Z].forEach(L=>check(BigInt(L.original_modulus)===q&&BigInt(L.original_rows)===m&&L.D_alpha_width===str(a)&&L.dimension===n&&L.hypothetical_decision_advantage===I.hypothetical_decision_advantage,"adapter comparisons cannot substitute another source or advantage"));
  const P=c.containing_interval_precision_plan,eps=parse(I.hypothetical_decision_advantage),t=I.terminal_hybrid_steps,x=div(mul(rat(128n*BigInt(t)*m),add(rat(q),div(one,a))),eps),precision=ceilLog2(x),width=rat(1n,2n**BigInt(precision));
  const per=min(one,mul(mul(rat(2n),width),add(rat(q),div(one,a)))),loss=min(one,mul(rat(m),per)),R=P.rounding_abort_ledger;
  check(P.normalized_source_interval_precision_bits===precision&&P.containing_interval_maximum_width===str(width)&&P.whole_bank_unconditioned_abort_union_upper===str(loss)&&R.maximum_normalized_observation_interval_width===str(width)&&R.per_input_rounding_abort_probability_upper===str(per)&&R.two_M_input_rounding_abort_union_upper===str(loss)&&R.source_interval_contains_true_observation_is_assumed_not_inferred===true&&R.input_errors_are_continuous_D_alpha_before_rounding===true,"entire paired-bank precision loss, no hidden conditioning");
  check(P.source_supplies_containing_intervals_at_this_precision_is_a_premise===true&&P.successful_rounding_is_not_an_IID_source_certificate===true&&cmp(loss,div(parse(I.noise_tolerance_target),rat(16n)))<=0n,"certified precision plan still requires an actual interval supplier");
  check(A.whole_bank_unconditioned_adapter_failure_upper===str(loss)&&Z.whole_bank_unconditioned_adapter_failure_upper===str(div(parse(I.noise_tolerance_target),rat(2n)))&&Z.maximum_integer_shift_certified===0,"two charged adapters/no remaining margin");
  const L=c.useful_valuation_completion;M.event(L);
  check(BigInt(L.original_modulus)===q&&L.dimension===n&&BigInt(L.original_rows)===m&&L.true_original_second_moment_upper===str(add(div(mul(rat(q*q),mul(a,a)),rat(3n)),rat(1n,2n))),"same rounded-Gaussian moment budget in completion");
  const G=c.published_size_ceiling_completion_gap;
  if(I.coefficient_size_ceiling_IF_published_reduction_contract_is_met===null)check(G===null,"zero positive tolerance is not a coefficient guarantee");
  else{
    check(BigInt(G.coefficient_size_bound)===BigInt(I.coefficient_size_ceiling_IF_published_reduction_contract_is_met),"conditional Fourier ceiling tied to tolerance");
    const cap=q/2n,C=BigInt(G.coefficient_size_bound),effective=C<cap?C:cap;let g=1n,d=0;while(3n*g<=effective){g*=3n;d++;}
    M.event(G.worst_factor_local_source_event);check(BigInt(G.largest_allowed_ternary_factor)===g&&G.worst_allowed_valuation===d&&G.worst_factor_local_source_event.maximum_supported_valuation===d&&G.small_integer_coefficient_bound_guarantees_a_safe_valuation===false&&G.bound_is_derived_from_an_implemented_decision_reduction===false,"no usable-valuation guarantee from a size ceiling");
    const W=G.worst_factor_local_source_event;check(BigInt(W.original_modulus)===q&&W.dimension===n&&BigInt(W.original_rows)===m&&W.public_radius===L.public_radius&&W.true_original_second_moment_upper===L.true_original_second_moment_upper&&W.external_covered_usable_multiple_list_failure_upper===null,"the coefficient gap is bound to the SAME original source");
  }
  check(c.decision_advantage_assumed_not_measured===true&&c.positive_noise_tolerance_is_not_secret_recovery===true,"positive compatibility is not a breakthrough");
  const F=c.nonprimitive_threshold_correlation_countercontrol,W=c.coarse_predictor_original_completion_budget;
  if(!I.maximum_integer_shift_certified)check(F===null&&W===null,"no unsupported tolerance promoted to a predicate");
  else{
    let g=1n,d=0;while(3n*g<=BigInt(n)**3n&&d+1<n){g*=3n;d++;}
    const B=BigInt(I.maximum_integer_shift_certified);while(d&&(2n*B+1n)*g>=q){g/=3n;d--;}
    if(!d)check(F===null&&W===null,"no nontrivial coarse period");
    else{
      const Q=q/g,p=rat(2n*B+1n,q),coarse=mul(rat(g),p),cov=mul(p,sub(one,coarse)),variance=mul(p,sub(one,p));
      same(F,{original_modulus:enc(q),window_radius:enc(B),censoring_valuation:d,coarse_factor:enc(g),coarse_modulus:enc(Q),full_window_probability:str(p),
        censored_window_probability:str(coarse),window_predictor_joint_probability:str(p),centered_covariance:str(cov),uncensored_window_variance:str(variance),
        fraction_of_uncensored_covariance_preserved:str(div(sub(one,coarse),sub(one,p))),predictor_period:enc(Q),Fourier_coefficient_indices_must_be_divisible_by:enc(g),
        all_primitive_character_coefficients_zero:true,scalar_inner_product_available_to_real_original_source_receiver:false,
        this_is_a_counterexample_to_correlation_implying_primitive_support_not_a_decision_algorithm:true},"high threshold covariance with exact nonprimitive periodic support");
      M.event(W);check(BigInt(W.original_modulus)===q&&W.dimension===n&&BigInt(W.original_rows)===m&&W.public_radius===L.public_radius&&W.true_original_second_moment_upper===L.true_original_second_moment_upper&&W.maximum_supported_valuation===d,"coarse predictor completion charged at its actual valuation");
    }
  }
}
function heavy(c){
  const q=BigInt(c.original_modulus),a=parse(c.Gaussian_D_alpha_width_for_comparison),law=c.heavy_tail_law.map(([e,p])=>[BigInt(e),parse(p)]);let V=rat(0n);
  law.forEach(([e,p])=>V=add(V,mul(rat(e*e),p)));
  const shared=add(div(mul(rat(q*q),mul(a,a)),rat(3n)),rat(1n,2n)),keys=new Set(law.map(([e])=>String(e))),mod=(x)=>(x%q+q)%q;
  check(law.every(([e])=>!keys.has(String(e+1n)))&&law.every(([e])=>!law.some(([b])=>mod(b)===mod(e+1n))),"integer and circular translated supports are disjoint");
  check(c.shared_second_moment_upper===str(shared)&&c.heavy_tail_true_second_moment===str(V)&&c.heavy_tail_obeys_shared_moment_upper===(cmp(V,shared)<=0n)&&c.heavy_tail_integer_translation_TV==="1"&&c.heavy_tail_modular_translation_TV==="1","matching-moment upper is not Gaussian smoothing");
  check(c.Gaussian_translation_TV_squared_upper_for_comparison===str(div(rat(11n,7n),mul(rat(q*q),mul(a,a))))&&c.Gaussian_smoothness_inferred_from_matching_moment_upper===false,"countercontrol prevents moment-only substitution");
}
function verify(p){
  check(p.status==="ROUNDED_GAUSSIAN_GENERAL_NOISE_TOLERANCE_AND_REDUCTION_INTERFACE_REVIEW_PENDING","review-pending noise interface");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_rounded_gaussian_tolerance.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_ROUNDED_GAUSSIAN_TOLERANCE.md")),"current source/derivation");
  const deps=["native_small_multiple_completion.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"actual dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  same(p.scaling_controls.map(c=>c.dimension),[8,32,64,128],"declared growing-root profile");
  p.scaling_controls.forEach(profile);heavy(p.moment_only_smoothness_countercontrol);
  check(p.accepted_speedup_candidate===false&&p.new_active_negative_result_created===false,"neither speedup nor broad no-go admitted");
  return {verified:true,source_tolerance_budgets:12,precision_plans:4,positive_ideal_tolerance_dimensions:p.scaling_controls.filter(c=>c.ideal_exact_rounding_budget.maximum_integer_shift_certified).map(c=>c.dimension),moment_only_countercontrol:true,decision_algorithm_implemented:false};
}
module.exports={verify,budget,profile};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

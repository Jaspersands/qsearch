"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_translation_stability.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);};
function gcd(a,b){a=a<0n?-a:a;while(b)[a,b]=[b,a%b];return a;}
function rat(a,b=1n){const g=gcd(a,b);return[a/g,b/g];}
const parse=s=>{const a=s.split("/");return rat(BigInt(a[0]),a.length===1?1n:BigInt(a[1]));},str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1],mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]),div=(a,b)=>rat(a[0]*b[1],a[1]*b[0]),cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
function digits(q){let r=0;while(q>1n&&q%3n===0n){q/=3n;r++;}check(q===1n&&r>0,"actual prime-power3 root");return r;}
function gate(g,q,delta){
  const eta=mul(rat(q-1n,2n),delta),yes=cmp(eta,rat(1n))<0n;
  check(g.modulus===String(q)&&g.commutator_operator_norm_upper===str(delta)&&g.pinching_distance_upper===str(eta)&&g.sufficient_invertibility_condition_met===yes,"finite-order pinching error and invertibility");
  check(g.status===(yes?"CONDITIONAL_EXACT_Q_ORDER_PAIR_ROUNDING":"UNKNOWN_PINCHING_INVERTIBILITY")&&g.distance_to_commuting_exact_q_order_pair_upper===(yes?str(mul(rat(2n*(q-1n)),delta)):null)&&g.first_generator_unchanged===yes,"conditional positive pair theorem");
  check(BigInt(g.averaging_terms_charged)===q&&g.requires_exact_input_unitarity_and_q_order===true&&g.requires_valid_operator_norm_bound_not_entrywise_error===true&&g.arbitrary_float_operator_premises_certified===false&&g.native_noisy_recovery_proved===false&&g.quantum_speedup_proved===false,"pair law access/norm/cost scope");
}
check(R.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_TRANSLATION_STABILITY.md"))).digest("hex"),"pinned translation stability derivation");
for(const w of R.weyl_falsifiers){
  const q=BigInt(w.modulus),r=digits(q),lo=rat(4n,q),rawhi=rat(44n,7n*q),hi=cmp(rawhi,rat(2n))>0n?rat(2n):rawhi,t=parse(w.commutator_threshold);
  check(w.root_digits===r&&w.operator_dimension===String(q)&&w.both_qth_powers_identity===true,"full-root orders and dimension charged");
  check(w.clock_action==="Z|j>=chi_q(j)|j>"&&w.shift_action==="X|j>=|j+1 modq>","fixed full-root Weyl action schema");
  // There are exactly two clock/shift wrap branches. Their phase differences
  // are1 and1-q, both1 modq; no large-dimensional sample audit is substituted.
  check((1n%q+q)%q===1n&&((1n-q)%q+q)%q===1n&&w.group_commutator_scalar_phase_exponent===1,"all symbolic basis branches of ZX=chi_q(1)XZ");
  check(w.principal_log_winding_index_exact===1&&w.commutator_negative_axis_gap_lower==="1"&&w.homotopy_commutator_perturbation_factor===4&&w.distance_to_every_commuting_unitary_pair_operator_norm_lower==="1/4","analytic winding/homotopy separation certificate");
  check(w.commutator_operator_norm_lower===str(lo)&&w.commutator_operator_norm_upper===str(hi),"rational full-root commutator bounds");
  const state=cmp(hi,t)<=0n?"PASSES_CERTIFIED":cmp(lo,t)>0n?"FAILS_CERTIFIED":"UNKNOWN_BETWEEN_RATIONAL_BOUNDS";check(w.commutator_only_threshold_status===state,"small residual can pass while rounding fails");
  gate(w.finite_order_pair_gate,q,hi);check(w.finite_order_pair_gate.sufficient_invertibility_condition_met===false&&w.operator_norm_rounding_from_small_commutator_alone_rejected===true,"positive law does not contradict topology");
  for(const k of["dense_q_by_q_operators_allocated","is_supplied_native_flat_moment_completion","normalized_Hilbert_Schmidt_rounding_obstructed","all_source_specific_approximate_flatness_ruled_out","candidate_record_accepted"])check(w[k]===false,"overclaimed Weyl obstruction: "+k);
}
for(const c of R.positive_pair_calibrations){
  const q=BigInt(c.modulus),t=parse(c.rotation_parameter),c0=parse(c.rotation_cosine_exact),s0=parse(c.rotation_sine_exact),tt=mul(t,t),one=rat(1n),den=rat(tt[0]+tt[1],tt[1]);
  check(c.rotation_cosine_exact===str(div(rat(tt[1]-tt[0],tt[1]),den))&&c.rotation_sine_exact===str(div(mul(rat(2n),t),den)),"rational unitary conjugation");const cs=mul(c0,c0),ss=mul(s0,s0);check(cs[0]*ss[1]+ss[0]*cs[1]===cs[1]*ss[1],"rotation norm exactly1");
  const delta=mul(rat(8n),t);check(c.commutator_upper_follows_from_conjugation_not_measured_tolerance===str(delta),"analytic commutator bound");gate(c.finite_order_pair_gate,q,delta);
  const m=c.numerical_metrics,bound=Number(parse(c.finite_order_pair_gate.distance_to_commuting_exact_q_order_pair_upper)[0])/Number(parse(c.finite_order_pair_gate.distance_to_commuting_exact_q_order_pair_upper)[1]);check(Object.values(m).every(Number.isFinite)&&m.commutator_norm_observed<=Number(delta[0])/Number(delta[1])+1e-10&&m.rounding_distance_observed<=bound+1e-10&&m.rounded_commutator_norm_observed<1e-9&&m.rounded_q_power_error_observed<1e-9&&m.rounded_unitarity_error_observed<1e-9,"bounded numerical polar/Schur calibration");
  check(c.input_exact_q_order_follows_from_rational_unitary_conjugation===true&&c.numerical_output_is_exact_operator_certificate===false&&c.actual_native_unknown_secret_or_flat_completion_used===false,"calibration is not exact numerical certification/recovery");
}
for(const l of R.sequential_precision_ledgers){const q=BigInt(l.modulus),a=2n*(q-1n),e=[0n];digits(q);for(let j=1;j<l.generators;j++)e.push(a*(BigInt(j)+2n*e.reduce((s,x)=>s+x,0n)));check(JSON.stringify(l.sequential_error_coefficients)===JSON.stringify(e.map(String)),"conservative multi-generator precision recurrence");check(l.sufficient_uniform_commutator_error_upper===str(div(parse(l.target_operator_norm_error),rat(e[e.length-1])))&&BigInt(l.conditional_expectation_terms_per_round_upper)===BigInt(l.generators-1)*q,"precision and averaging costs retained");check(l.coefficient_growth_is_a_strategy_bound_not_general_impossibility===true&&l.polynomial_precision_in_n_established===false&&l.group_size_q_to_n_enumerated===false&&l.native_source_premises_certified===false,"no generic many-generator impossibility/precision claim");}
check(R.status==="FULL_ROOT_TRANSLATION_STABILITY_FALSIFIER_AND_CONDITIONAL_PAIR_REPAIR_REVIEW_PENDING"&&R.known_operator_theory_not_novelty_claim===true,"known-theory scope");for(const k of["native_approximate_flatness_proved","native_noisy_decoder_supplied","quantum_speedup_proved","candidate_record_accepted"])check(R[k]===false,"unsupported native algorithm claim: "+k);
console.log(JSON.stringify({status:"PASS",symbolic_full_root_weyl_falsifiers:R.weyl_falsifiers.length,positive_pair_calibrations:R.positive_pair_calibrations.length,sequential_precision_ledgers:R.sequential_precision_ledgers.length,native_noisy_decoder_supplied:false}));

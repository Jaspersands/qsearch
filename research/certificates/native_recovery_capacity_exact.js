"use strict";
const C=require("./cyclotomic_exact.js");
const {check,rat:F,add,mul,div,str,parse,cmp}=C;
const one=F(1n),zero=F(0n),B=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact integer encoding");return BigInt(x);};
const bitlen=x=>x===0n?0:x.toString(2).length;
function root(q){let d=0,r=q;check(q>=3n,"positive root");while(r%3n===0n){r/=3n;d++;}check(r===1n,"full ternary root");return d;}
const cache=new Map();
function count(K,W){
  check(K>=0n&&W>=0n,"nonnegative signed-ball parameters");const id=`${K}:${W}`;
  if(cache.has(id))return cache.get(id);
  const length=K<W?K:W;check(length<=8192n,"bounded exact combinatorial verifier budget");
  // Separate binomial recurrences, independent of the producer's term recurrence.
  let chooseK=1n,chooseW=1n,power=1n,total=1n;
  for(let j=1n;j<=length;j++){chooseK=chooseK*(K-j+1n)/j;chooseW=chooseW*(W-j+1n)/j;power*=2n;total+=power*chooseK*chooseW;}
  cache.set(id,total);return total;
}
function ball(b,K,W){
  check(B(b.coordinates)===K&&B(b.radius)===W&&B(b.required_terms)===(K<W?K:W)&&!b.partial_count_promoted,"complete exact combinatorial scope");
  const terms=K<W?K:W;
  if(terms>B(b.max_terms)){check(b.status==="UNKNOWN_EXACT_BALL_TERM_CAP"&&b.count===null,"term cap stays UNKNOWN, no partial upper bound");return null;}
  const c=count(K,W);check(b.status==="EXACT_SIGNED_INTEGER_L1_BALL"&&B(b.count)===c,"all exact signed-ball terms");return c;
}
function copy(c,n,q,M){
  const r=root(q),G=q**BigInt(n),D=3n**M,target=parse(c.target_success),upper=D>=G?one:F(D,G),minimum=B(c.minimum_qutrits_required_by_dimension);
  check(c.status==="UNIFORM_FULL_SECRET_COPY_CAPACITY_BOUND"&&c.dimension===n&&B(c.modulus)===q&&B(c.native_qutrits)===M&&c.uniform_secret_trits===n*r&&c.full_secret_recovery_success_upper===str(upper)&&c.target_not_excluded_by_capacity===(cmp(upper,target)>=0n),"full-secret qutrit dimension bound, separate from noise validity");
  check(minimum>=0n&&cmp(F(3n**minimum),mul(target,F(G)))>=0n&&(minimum===0n||cmp(F(3n**(minimum-1n)),mul(target,F(G)))<0n),"exact minimum copy threshold, no float logs");
  check(c.applies_to_noisy_qutrits_and_arbitrary_collective_receiver&&!c.secret_bearing_classical_values_or_extra_inputs_allowed&&!c.nonuniform_small_secret_prior_covered&&!c.capacity_pass_is_receiver_existence_or_efficiency,"uniform copy-only scope, passing does not provide a receiver");
}
function query(c,n,q,M,W){
  root(q);const total=ball(c.ball,2n*M,W),G=q**BigInt(n);
  if(total===null){check(c.status==="UNKNOWN_COMPLETE_QUERY_CAPACITY"&&c.full_secret_recovery_success_upper===null&&c.target_not_excluded_by_capacity===null&&!c.unknown_is_capacity_pass,"unknown combinatorial capacity cannot pass");return;}
  const upper=total>=G?one:F(total,G),target=parse(c.target_success);
  check(c.status==="UNIFORM_FULL_SECRET_INDEXED_QUERY_CAPACITY_BOUND"&&c.dimension===n&&B(c.modulus)===q&&B(c.bank_size)===M&&B(c.weighted_phase_exposure)===W&&B(c.secret_count)===G&&c.full_secret_recovery_success_upper===str(upper)&&c.target_not_excluded_by_capacity===(cmp(upper,target)>=0n),"Laurent-support dimension capacity at charged weighted exposure");
  check(c.labels_may_be_arbitrary_and_algorithm_may_be_label_adaptive&&c.adaptive_measurements_and_secret_independent_ancillas_covered&&!c.additional_unpaid_phase_inputs_or_classical_values_allowed&&c.is_an_IDEAL_fixed_bank_query_bound&&c.also_applies_to_exact_noisy_bank_with_no_classical_value_leak&&!c.noise_independence_or_smallness_needed_for_capacity&&!c.capacity_pass_is_receiver_existence_or_efficiency,"no source side channel; exact noisy monomial support shares the same bound");
}
function minimum(c,n,q,M){
  const W=B(c.minimum_exposure),G=q**BigInt(n),target=parse(c.target_success),at=count(2n*M,W),before=W?count(2n*M,W-1n):null;
  check(c.status==="EXACT_NECESSARY_WEIGHTED_EXPOSURE"&&c.dimension===n&&B(c.modulus)===q&&B(c.bank_size)===M&&B(c.coefficient_ball_at_threshold)===at&&(before===null?c.coefficient_ball_before_threshold===null:B(c.coefficient_ball_before_threshold)===before),"complete threshold boundary counts");
  check(cmp(F(at),mul(target,F(G)))>=0n&&(before===null||cmp(F(before),mul(target,F(G)))<0n)&&!c.necessary_condition_is_sufficient_for_receiver,"necessary exposure is minimal but not a decoder");
}
function isqrt(n){if(n<2n)return n;let x=1n<<BigInt(Math.ceil(bitlen(n)/2));for(;;){const y=(x+n/x)/2n;if(y>=x)return x;x=y;}}
function incompatibility(c,n,q,M,V){
  const squared=div(mul(F(80n*M),V),F(q*q)),bits=c.sqrt_bits,scale=2n**BigInt(bits),k=isqrt(squared[0]*scale*scale/squared[1]),lo=F(k,scale),hi=cmp(mul(lo,lo),squared)===0n?lo:F(k+1n,scale);
  check(c.dimension===n&&B(c.modulus)===q&&B(c.bank_size)===M&&c.source_integer_second_moment_upper===str(V)&&c.RMS_upper_bound_squared===str(squared)&&c.sqrt_upper_bound_lower_enclosure===str(lo)&&c.sqrt_upper_bound_upper_enclosure===str(hi),"exact rational enclosure of an UPPER error proxy, not actual error lower bound");
  check(!c.actual_noise_error_lower_bound_claimed&&!c.noisy_receiver_impossibility_claimed&&!c.secret_bearing_classical_preprocessing_covered&&c.gate_and_rounding_omission_only_strengthens_this_falsifier,"generic-certificate incompatibility is not quantum impossibility");
  if(lo[0]===0n){check(c.status==="NO_POSITIVE_PROXY_LOWER_ENCLOSURE"&&!c.global_incompatibility_certified,"zero proxy or unresolved enclosure is not a no-go");return;}
  const boundary=lo[1]/lo[0];
  if(c.status==="UNKNOWN_GLOBAL_INCOMPATIBILITY_TERM_CAP"){
    check(ball(c.ball,2n*M,boundary)===null&&!c.global_incompatibility_certified,"incomplete global witness stays unknown");return;
  }
  const total=ball(c.ball_at_boundary,2n*M,boundary),G=q**BigInt(n);
  check(total!==null,"complete global witness required");
  const proved=boundary===0n||cmp(F(total,G),mul(F(boundary),lo))<=0n;
  check(B(c.last_exposure_before_proxy_reaches_one)===boundary&&c.global_incompatibility_certified===proved&&c.only_W_zero_chance_guessing_survives_this_certificate===proved&&!c.capacity_and_proxy_combination_is_algorithmic_no_go&&c.status===(proved?"NO_NONTRIVIAL_TRANSFER_WITH_THIS_GENERIC_LEDGER":"GLOBAL_INCOMPATIBILITY_NOT_ESTABLISHED"),"all-exposure monotone-ratio witness with the correct scope");
}
module.exports={count,ball,copy,query,minimum,incompatibility};

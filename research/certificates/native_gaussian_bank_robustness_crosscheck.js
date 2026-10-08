"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const C=require("./cyclotomic_exact.js"),Capacity=require("./native_recovery_capacity_exact.js");
const {check,same,rat:F,add,sub,mul,div,str,parse,cmp}=C;
const zero=F(0n),one=F(1n),two=F(2n);
const B=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact serialized integer");return BigInt(x);};
const min=(x,y)=>cmp(x,y)<=0n?x:y,abs=x=>F(x[0]<0n?-x[0]:x[0],x[1]);
const bitlen=x=>x===0n?0:x.toString(2).length;
function root(q){check(q>=3n,"positive root");let x=q;while(x%3n===0n)x/=3n;check(x===1n,"ternary root");}
function sqrtBox(x,bits){
  const scale=2n**BigInt(bits),v=x[0]*scale*scale/x[1];let k;
  if(v<2n)k=v;else{let a=1n<<BigInt(Math.ceil(bitlen(v)/2));for(;;){let b=(a+v/a)/2n;if(b>=a){k=a;break;}a=b;}}
  const lo=F(k,scale);return [lo,cmp(mul(lo,lo),x)===0n?lo:F(k+1n,scale)];
}
const piCache=new Map();
function piBox(bits){
  if(piCache.has(bits))return piCache.get(bits);
  const tolerance=F(1n,2n**BigInt(bits+10));
  function atan(d){let total=zero,p=d,j=0;for(;;){total=add(total,F(j%2?-1n:1n,BigInt(2*j+1)*p));j++;p*=d*d;let next=F(j%2?-1n:1n,BigInt(2*j+1)*p);if(cmp(abs(next),tolerance)<=0n){let end=add(total,next);return cmp(total,end)<=0n?[total,end,j]:[end,total,j];}}}
  const a=atan(5n),b=atan(239n),r=[sub(mul(F(16n),a[0]),mul(F(4n),b[1])),sub(mul(F(16n),a[1]),mul(F(4n),b[0])),[a[2],b[2]]];piCache.set(bits,r);return r;
}
function logarithm(c,argument,bits){
  check(B(c.argument)===argument&&c.bits===bits&&argument>=1n,"pinned logarithm argument and precision");
  const k=bitlen(argument)-1,y=F(argument,2n**BigInt(k)),z=div(sub(y,one),add(y,one)),t=F(1n,3n),J=c.series_terms;
  check(Number.isSafeInteger(J)&&J>=0&&J<=512&&c.dyadic_exponent===k&&c.normalized_argument===str(y),"bounded dyadic logarithm reduction");
  function series(u){
    let total=zero,power=u;
    for(let j=0;j<J;j++){total=add(total,div(mul(two,power),F(BigInt(2*j+1))));power=mul(power,mul(u,u));}
    const tail=div(mul(two,power),mul(F(BigInt(2*J+1)),sub(one,mul(u,u))));return [total,add(total,tail),tail];
  }
  const a=series(t),b=series(z),lo=add(mul(F(BigInt(k)),a[0]),b[0]),hi=add(mul(F(BigInt(k)),a[1]),b[1]),tolerance=F(1n,2n**BigInt(bits)*BigInt(k+1));
  check(cmp(a[2],tolerance)<=0n&&cmp(sub(hi,lo),F(1n,2n**BigInt(bits)))<=0n&&c.lower===str(lo)&&c.upper===str(hi),"positive atanh series and complete geometric remainders");return [lo,hi];
}
function budget(b){
  const q=B(b.modulus),M=B(b.bank_size),alpha=parse(b.alpha),W=B(b.weighted_phase_exposure),T=B(b.nonidentity_phase_calls),f=b.failure_bits;
  root(q);check(M>=1n&&cmp(alpha,zero)>0n&&cmp(alpha,one)<0n&&W>=0n&&T<=W&&(T===0n)===(W===0n)&&Number.isSafeInteger(f)&&f>=1,"actual Gaussian width, bank and committed exposure");
  const bits=f+(W?bitlen(4n*W-1n):0)+8,p=piBox(bits),log=logarithm(b.logarithm_certificate,4n*M,bits),squared=mul(p[1],log[1]),s=sqrtBox(squared,bits),operator=min(two,add(mul(mul(two,alpha),s[1]),div(p[1],F(q)))),noise=min(one,mul(F(W),operator)),gateBits=f+(T?bitlen(2n*T-1n):0),gate=F(2n*T,2n**BigInt(gateBits)),total=min(one,add(noise,gate));
  check(b.status==="GAUSSIAN_FIXED_BANK_EXPECTED_HYBRID_BOUND_REVIEW_PENDING"&&B(b.original_scalar_errors)===2n*M&&b.interval_bits===bits&&b.pi_lower===str(p[0])&&b.pi_upper===str(p[1]),"maximum over original scalar errors with exact pi bounds");
  check(B(b.index_comparison_compute_uncompute_pairs_upper)===M*T&&B(b.diagonal_branch_phase_gates_upper)===2n*M*T&&!b.QRAM_or_full_table_secret_access_assumed,"explicit fixed-bank branch costs, no full-table secret oracle");
  same(b.Machin_terms,p[2],"complete Machin series lengths");
  check(b.sqrt_argument_upper===str(squared)&&b.sqrt_lower===str(s[0])&&b.sqrt_upper===str(s[1])&&b.expected_operator_norm_error_upper===str(operator)&&b.expected_complete_receiver_noise_success_loss_upper===str(noise)&&b.local_gate_precision_bits===gateBits&&b.complete_phase_gate_error_upper===str(gate)&&b.complete_pre_rounding_success_loss_upper===str(total)&&b.bound_is_nonvacuous===(cmp(total,one)<0n),"Gaussian maximum, rounding, exposure and synthesis ledger");
  check(b.source_law==="nearest-integer rounded lifts of continuous D_alpha torus noise"&&b.Gaussian_lift_variance==="alpha^2/(2*pi)"&&b.Gaussian_tails_are_an_explicit_source_premise&&!b.Gaussian_law_inferred_from_values_or_second_moment&&!b.independence_required_for_maximum_bound&&!b.fixed_errors_are_refreshed_on_reuse&&!b.bound_is_pointwise_for_every_source_realization&&b.caller_and_source_rounding_error_still_to_be_added&&!b.ideal_source_inverse_supplied_exactly&&!b.hardware_synthesis_implemented&&!b.receiver_supplied&&!b.hardness_transfer_admitted&&!b.accepted_speedup_candidate,"stronger distributional promise; still no receiver or hardware claim");
  return total;
}
function tail(b){
  const q=B(b.modulus),M=B(b.bank_size),alpha=parse(b.alpha),k=b.confidence_bits,bits=b.interval_bits;
  root(q);check(M>=1n&&cmp(alpha,zero)>0n&&cmp(alpha,one)<0n&&Number.isSafeInteger(k)&&k>=1,"Gaussian tail source and confidence");
  const log=logarithm(b.logarithm_certificate,4n*M*2n**BigInt(k),bits),p=piBox(bits),radius=mul(alpha,sqrtBox(div(log[1],p[0]),bits)[1]),operator=min(two,add(mul(mul(two,p[1]),radius),div(p[1],F(q))));
  check(b.status==="GAUSSIAN_BANK_HIGH_PROBABILITY_BOUND_REVIEW_PENDING"&&b.failure_probability_upper===str(F(1n,2n**BigInt(k)))&&b.pi_lower===str(p[0])&&b.pi_upper===str(p[1])&&b.Gaussian_lift_absolute_radius_upper===str(radius)&&b.rounded_integer_error_absolute_radius_upper===str(add(mul(F(q),radius),F(1n,2n)))&&b.operator_norm_error_upper_on_good_event===str(operator),"Gaussian union-bound failure and certified good-event cutoff");
  check(!b.independence_required_for_union_bound&&b.Gaussian_law_is_source_premise_not_fitted_from_records&&b.no_exceptions_conditioned_away,"tail exceptions and source premise preserved");
}
function compact(c,n,M,W){
  const logs=c.logarithm_certificates,K=2n*M,trits=n*n,bits=96;
  const twoLog=logarithm(logs.two,2n,bits),threeLog=logarithm(logs.three,3n,bits),kLog=logarithm(logs.K,K,bits),sumLog=logarithm(logs.K_plus_W,K+W,bits);
  const logBall=W?mul(F(K),add(add(twoLog[1],one),sub(sumLog[1],kLog[0]))):zero,logG=mul(F(trits),threeLog[0]),logP=min(zero,sub(logBall,logG)),excluded=cmp(logP,F(-twoLog[1][0],twoLog[1][1]))<0n,envelope=M>=trits&&W>=trits;
  check(c.status==="COMPACT_SIGNED_SUPPORT_CAPACITY_BOUNDS_NOT_RECEIVER"&&B(c.dimension)===n&&B(c.root_digits)===n&&B(c.bank_size)===M&&B(c.weighted_phase_exposure)===W&&B(c.uniform_secret_trits)===trits&&c.signature_count_log_upper===str(logBall)&&c.secret_count_log_lower===str(logG)&&c.recovery_success_log_upper===str(logP)&&c.half_success_excluded_by_support_upper_bound===excluded&&c.signature_envelope_reaches_secret_count_by_single_term===envelope,"compact logarithmic upper and single-term lower support certificates");
  check(!(excluded&&envelope)&&!c.secret_count_or_full_signature_sum_materialized&&!c.signature_envelope_pass_proves_actual_frequency_spread&&!c.signature_envelope_pass_proves_receiver_existence&&!c.original_value_dependent_additional_gates_covered,"support envelope is not actual frequency coverage or efficient recovery");
}
function run(r){
  check(r.status==="GAUSSIAN_BANK_ROBUSTNESS_CORRECTS_GENERIC_TRANSFER_EXCLUSION_REVIEW_PENDING"&&!r.receiver_supplied&&!r.general_LWE_algorithm_impossibility_claimed&&!r.second_moment_promise_alone_supports_this_refinement&&!r.accepted_speedup_candidate,"sharper noise budget, not an algorithm or a moment-only theorem");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../NATIVE_GAUSSIAN_BANK_ROBUSTNESS.md"))).digest("hex"),"pinned derivation");
  check(r.logarithm_controls.length===10&&r.bound_controls.length===4&&r.tail_controls.length===2&&r.joint_profiles.length===3,"complete precommitted controls");
  r.logarithm_controls.forEach((c,i)=>logarithm(c,[1n,2n,3n,2048n,4096n][Math.floor(i/2)],i%2?64:16));
  const controls=[[9n,8n,"1/4",3n],[3n**64n,512n,"1/1048576",0n],[3n**64n,512n,"1/1048576",128n],[3n**64n,512n,"1/1048576",2n**20n]];
  r.bound_controls.forEach((b,i)=>{let c=controls[i];check(B(b.modulus)===c[0]&&B(b.bank_size)===c[1]&&b.alpha===c[2]&&B(b.weighted_phase_exposure)===c[3]&&B(b.nonidentity_phase_calls)===c[3],"committed unit-power call controls");budget(b);});
  r.tail_controls.forEach((b,i)=>{check(B(b.modulus)===3n**64n&&B(b.bank_size)===(i?1024n:512n)&&b.alpha==="1/1048576"&&b.confidence_bits===(i?64:32)&&b.interval_bits===96,"precommitted Gaussian tail controls");tail(b);});
  let reopened=0;
  r.joint_profiles.forEach((p,i)=>{
    const q=3n**64n,M=i===1?1024n:512n,alpha=parse(i===2?"1/16777216":"1/1048576"),target=F(1n,2n),V=add(div(mul(F(q*q),mul(alpha,alpha)),F(3n)),F(1n,2n));
    check(p.status==="NECESSARY_CAPACITY_WITH_SHARPER_CONDITIONAL_NOISE_BUDGET_NOT_RECEIVER"&&p.dimension===64&&B(p.modulus)===q&&B(p.bank_size)===M&&p.alpha===str(alpha)&&p.source_parameter_guard===(cmp(mul(mul(alpha,F(q)),mul(alpha,F(q))),F(256n))>=0n),"same Gaussian source regime, no free noise change");
    Capacity.minimum(p.minimum_exposure_certificate,64,q,M);const W=B(p.minimum_exposure_certificate.minimum_exposure);
    Capacity.query(p.capacity,64,q,M,W);Capacity.incompatibility(p.moment_only_global_exclusion,64,q,M,V);
    const b=p.Gaussian_refined_budget;check(B(b.modulus)===q&&B(b.bank_size)===M&&b.alpha===str(alpha)&&B(b.weighted_phase_exposure)===W&&B(b.nonidentity_phase_calls)===W,"same source and W unit-power budget at necessary threshold");
    const total=budget(b),margin=cmp(total,target)>=0n?zero:sub(target,total);
    check(p.hypothetical_ideal_receiver_success===str(target)&&p.conditional_pre_rounding_success_lower_if_that_receiver_exists===str(margin)&&!p.ideal_receiver_has_been_constructed&&!p.passing_support_dimension_and_noise_is_sufficient_for_recovery&&!p.caller_source_and_hardware_precision_debt_resolved&&!p.accepted_speedup_candidate,"positive conditional margin is not demonstrated recovery");
    if(p.moment_only_global_exclusion.global_incompatibility_certified&&cmp(margin,zero)>0n)reopened++;
  });
  const h=r.heavy_tail_countercontrol,q=3n**40n,N=1024n,alpha=F(1n,1024n),moment=F(q*q,N*81n**2n),G=add(div(mul(F(q*q),mul(alpha,alpha)),F(3n)),F(1n,2n)),hit=sub(one,F((N-1n)**N,N**N)),lower=mul(F(4n,81n),hit);
  check(h.status==="IID_HEAVY_TAILS_FALSIFY_MOMENT_ONLY_GAUSSIAN_REFINEMENT"&&B(h.modulus)===q&&B(h.bank_size)===512n&&h.alpha===str(alpha)&&B(h.independent_scalar_errors)===N&&h.nonzero_error_probability===str(F(1n,N))&&B(h.nonzero_error_magnitude)===q/81n&&h.true_integer_second_moment===str(moment)&&h.Gaussian_moment_upper===str(G)&&h.same_second_moment_promise_satisfied===(cmp(moment,G)<=0n)&&h.probability_some_error_nonzero===str(hit)&&h.expected_operator_error_lower===str(lower),"independent centered heavy tails with matching moment promise");
  check(B(h.Gaussian_proxy.modulus)===q&&B(h.Gaussian_proxy.bank_size)===512n&&h.Gaussian_proxy.alpha===str(alpha)&&B(h.Gaussian_proxy.weighted_phase_exposure)===1n,"same moment-width bank for the countercontrol");budget(h.Gaussian_proxy);
  check(cmp(lower,parse(h.Gaussian_proxy.expected_operator_norm_error_upper))>0n&&h.Gaussian_norm_certificate_falsified&&h.errors_are_independent_and_centered&&!h.Gaussian_marginal_law_satisfied&&!h.quantum_receiver_impossibility_claimed,"the Gaussian refinement does not follow from second moments alone");
  check(r.scaling_profiles.length===9,"three bank/source regimes at three precommitted dimensions");
  let scalingExclusions=0;
  r.scaling_profiles.forEach((p,i)=>{
    const n=[64n,256n,1024n][Math.floor(i/3)],quadratic=i%3!==0,improved=i%3===2,M=quadratic?n*n:8n*n,W=quadratic?n*n:n**3n,q=3n**n,alpha=F(1n,n**(improved?3n:4n));
    check(B(p.dimension)===n&&B(p.root_digits)===n&&p.bank_scaling===(quadratic?"n^2":"8n")&&p.exposure_scaling===(quadratic?"n^2":"n^3")&&p.source_alpha_scaling===(improved?"n^-3":"n^-4"),"precommitted asymptotic source and exposure families");
    compact(p.compact_capacity,n,M,W);
    const b=p.Gaussian_refined_budget;check(B(b.modulus)===q&&B(b.bank_size)===M&&b.alpha===str(alpha)&&B(b.weighted_phase_exposure)===W&&B(b.nonidentity_phase_calls)===W,"same scaling family reaches the Gaussian ledger");budget(b);
    check(p.source_parameter_guard===(cmp(mul(mul(alpha,F(q)),mul(alpha,F(q))),F(4n*n))>=0n)&&p.source_worst_case_factor_conditional_on_efficient_LWE_solver===(improved?"~O(n^4)":"~O(n^5)")&&!p.efficient_LWE_solver_supplied&&!p.actual_phase_support_spread_proved&&!p.accepted_speedup_candidate,"conditional source consequence, no lattice algorithm or decoder supplied");
    if(p.compact_capacity.half_success_excluded_by_support_upper_bound)scalingExclusions++;
  });
  return {status:"PASS",logarithm_controls:10,hybrid_controls:4,tail_controls:2,joint_profiles:3,generic_ledger_exclusions_reopened_by_Gaussian_tails:reopened,heavy_tail_countercontrols:1,scaling_profiles:9,scaling_support_exclusions:scalingExclusions,receiver_supplied:false};
}
if(require.main===module){const input=process.argv[2]||path.join(__dirname,"../reductions/native_gaussian_bank_robustness.json");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));}
module.exports={logarithm,budget,tail,run};

"use strict";
// Replays actual characters and rational ledgers, not a scalable quantum effect.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one,zero}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_word_span_decision.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b;
const mod=(a,q)=>(a%q+q)%q;
function integer(a,name,lower=0) {check(Number.isSafeInteger(a)&&a>=lower,name);return a;}
function exactInteger(a,name) {
  if(typeof a==="number") {integer(a,name);return BigInt(a);}
  check(typeof a==="string"&&/^(0|[1-9][0-9]*)$/.test(a),name);return BigInt(a);
}
function* words(M,p=[]) {if(p.length===M){yield p;return;}for(let t=0;t<3;t++)yield*words(M,[...p,t]);}
function scopes(object,positive,negative) {
  positive.forEach(k=>check(object[k]===true,"required scope "+k));
  negative.forEach(k=>check(object[k]===false,"missing implementation/limited scope "+k));
}
function bounded(c) {
  const s=c.preparation_contract,f=s.public_family,q=Number(f.modulus),n=integer(f.dimension,"dimension",1),M=integer(f.sites,"sites",1);
  E.field(q);const D=3**M,N=q**n;
  check(f.cohorts===1&&D<=256&&N<=256,"one bounded original cohort");
  const raw=c.original_records,mask=c.known_mask,truth=c.truth_fixture_only.masked_secret,errors=c.truth_fixture_only.original_errors;
  check(raw.length===2*M&&mask.length===n&&truth.length===n&&errors.length===2*M,"complete source shape");
  const ids=new Set();raw.forEach((r,j)=>{
    check(r.modulus===q&&r.label.length===n&&typeof r.source_id==="string"&&r.source_id.length&&!ids.has(r.source_id),"original identity and shape");ids.add(r.source_id);
    [...r.label,r.value,...mask,...truth].forEach(x=>check(Number.isSafeInteger(x)&&x>=0&&x<q,"canonical finite source integer"));
    check(Number.isSafeInteger(errors[j]),"unwrapped integer error");
    check(mod(r.value+r.label.reduce((a,x,i)=>a+x*mask[i],0)-r.label.reduce((a,x,i)=>a+x*truth[i],0),q)===mod(errors[j],q),"truth-only original source equation");
  });
  const pairs=Array.from({length:M},(_,j)=>[raw[2*j].label,raw[2*j+1].label]);
  same(f.paired_labels,[pairs],"actual public original labels");check(f.responses_masks_source_IDs_and_errors_supplied===false,"public map has no secret response");
  const phases=pairs.map((pair,j)=>{
    const a=mod(raw[2*j].value+pair[0].reduce((a,x,i)=>a+x*mask[i],0),q),b=mod(raw[2*j+1].value+pair[1].reduce((a,x,i)=>a+x*mask[i],0),q);
    return [a,mod(b-a,q),mod(-b,q)];
  });
  same(s,{public_family:f,known_word_phases_by_cohort:[phases],original_records_paid_once:2*M,
    cohort_controlled_local_diagonal_gates:M,uniform_index_qubits:0,uniform_qutrits:M,
    word_domain_size:String(D),frequency_group_size:String(N),frequency_coordinate_trits:n*Math.round(Math.log(q)/Math.log(3)),
    secret_or_errors_supplied_to_preparation:false,same_as_previous_native_point_seed:false,
    all_word_table_required_for_indexed_preparation:false,normalized_fibre_oracle_supplied:false,
    physical_gate_synthesis_and_precision_supplied:false},"paid known preparation, no projection oracle");
  const rows=[],groups=new Map(),counts=Array(N).fill(0),betas=new Set();let squareError=0n;
  for(const w of words(M)) {
    const beta=w.flatMap(t=>[[1,0],[-1,1],[0,-1]][t]),freq=Array.from({length:n},(_,i)=>mod(beta.reduce((a,b,j)=>a+b*raw[j].label[i],0),q));
    const phase=mod(beta.reduce((a,b,j)=>a+b*(raw[j].value+raw[j].label.reduce((a,x,i)=>a+x*mask[i],0)),0),q);
    const row={cohort:0,word:w,frequency:freq,known_phase:phase};rows.push(row);
    const id=JSON.stringify(freq);if(!groups.has(id))groups.set(id,[]);groups.get(id).push(phase);
    counts[freq.reduce((a,x)=>a*q+x,0)]++;
    const character=JSON.stringify(beta.map(x=>mod(x,q)));check(!betas.has(character),"distinct null characters");betas.add(character);
    const e=beta.reduce((a,b,j)=>a+BigInt(b)*BigInt(errors[j]),0n);squareError+=e*e;
  }
  same(c.actual_word_rows,rows,"whole original word phase map");same(c.actual_fibre_counts,counts,"complete fibre counts");
  check(c.span_rank===groups.size&&c.word_dimension===D,"exact span dimension");
  const K=E.field(q);let probability=K.F(),rawProbability=K.F();
  let spanFloat=0,rawFloat=0;
  for(const phases of groups.values()) {
    let x=0,y=0;
    for(const a of phases) {
      x+=Math.cos(2*Math.PI*a/q);y+=Math.sin(2*Math.PI*a/q);
      for(const b of phases) {
        probability=K.plus(probability,K.scale(K.powers[mod(b-a,q)],rat(1n,BigInt(D*phases.length))));
        rawProbability=K.plus(rawProbability,K.scale(K.powers[mod(b-a,q)],rat(1n,BigInt(D*D))));
      }
    }
    spanFloat+=(x*x+y*y)/(D*phases.length);rawFloat+=(x*x+y*y)/(D*D);
  }
  same(c.exact_span_acceptance_root_polynomial,K.encode(probability),"exact cyclotomic span expectation");
  check(K.eq(probability,K.conj(probability))&&E.sign(K,probability)>=0&&E.sign(K,K.plus(K.unit,K.scale(probability,rat(-1n))))>=0,"effect probability in [0,1]");
  const close=(a,b)=>check(Number.isFinite(a)&&Math.abs(a-b)<2e-10,"floating diagnostic agreement only");
  close(c.diagnostic_span_acceptance_probability,spanFloat);close(c.diagnostic_raw_comparison_acceptance_probability,rawFloat);
  check(c.exact_uniform_raw_value_null_acceptance===str(rat(BigInt(groups.size),BigInt(D))),"IID uniform raw null trace");
  check(c.ideal_raw_comparison_acceptance===str(rat(BigInt(counts.reduce((a,x)=>a+x*x,0)),BigInt(D*D))),"raw absolute scale");
  let pairSquare=0n;for(let j=0;j<2*M;j+=2){const a=BigInt(errors[j]),b=BigInt(errors[j+1]);pairSquare+=a*a+b*b-a*b;}
  const moment=rat(2n*pairSquare,3n),actual=rat(squareError,BigInt(D));check(cmp(moment,actual)===0n,"exact frozen error averaging");
  const bound=min(one,div(mul(rat(40n),moment),rat(BigInt(q*q))));check(c.pathwise_span_rejection_upper===str(bound),"source pathwise bound");
  const lower=K.plus(probability,K.scale(K.unit,sub(bound,one)));check(E.sign(K,lower)>=0,"exact source acceptance above pathwise bound");
  scopes(c,[],["dense_reference_is_an_efficient_decision_algorithm","source_calibration_is_unbounded_Gaussian_advantage_evidence","span_effect_implementation_supplied"]);
  return {words:D,character_pairs:D*D,probability};
}
function decision(L) {
  const n=integer(L.dimension,"dimension",1),r=integer(L.root_digits,"root digits",1),M=integer(L.original_pairs,"pairs",1),q=3n**BigInt(r);
  check(exactInteger(L.original_modulus,"modulus")===q&&L.original_classical_values===2*M&&L.word_dimension_base3_exponent===M&&L.frequency_group_base3_exponent===n*r,"source and Hilbert exponents");
  const V=parse(L.true_original_marginal_second_moment_upper),eps=parse(L.hypothetical_span_effect_operator_norm_error),delta=parse(L.hypothetical_each_ensemble_preparation_trace_distance_upper);
  check(V[0]>=0n&&cmp(eps,zero)>=0n&&cmp(eps,one)<=0n&&cmp(delta,zero)>=0n&&cmp(delta,one)<=0n,"valid hypothetical moments/accuracy");
  const nullBound=M>=n*r?rat(1n,3n**BigInt(M-n*r)):one,loss=min(one,div(mul(rat(BigInt(80*M)),V),rat(q*q)));
  const gap=max(zero,sub(sub(sub(sub(one,loss),nullBound),mul(rat(2n),eps)),mul(rat(2n),delta)));
  check(L.uniform_null_acceptance_upper_without_balance===str(nullBound)&&L.source_span_rejection_upper===str(loss)&&L.decision_advantage_lower_IF_effect_and_source_promises_hold===str(gap),"exact conditional gap and both accuracy losses");
  scopes(L,["null_raw_values_IID_uniform_independent_of_labels_required","uniform_operator_norm_approximation_is_sufficient_not_necessary","span_null_acceptance_invariant_under_data_adaptive_known_mask"],
    ["original_noise_independence_or_label_independence_required_for_moment_bound","balanced_fibres_or_full_frequency_coverage_assumed","all_other_ensemble_decision_tests_excluded","span_projection_proved_easier_than_coherent_row_preparation","source_noise_and_gate_precision_promises_established","efficient_span_effect_supplied","identity_null_density_after_data_adaptive_mask_claimed"]);
}
function route(L) {
  const n=integer(L.dimension,"dimension",1),r=integer(L.root_digits,"root digits",1),q=3n**BigInt(r),h=(BigInt(n)+1n).toString(2).length;
  check(exactInteger(L.original_modulus,"modulus")===q&&L.declared_omega_sqrt_log_function==="ceil(log2(n+2))"&&L.smoothing_function_value===h,"declared asymptotic smoothing function");
  const a=parse(L.decision_continuous_D_alpha_width),s=parse(L.search_continuous_D_alpha_width),added=sub(mul(a,a),mul(s,s));
  check(cmp(a,zero)>0n&&cmp(a,one)<0n&&str(s)===str(div(a,rat(BigInt(h*h))))&&L.search_to_decision_width_multiplier===h*h,"width-changing route, not fixed-width recovery");
  check(L.fresh_auxiliary_Gaussian_width_squared===str(added)&&added[0]>0n,"independent smoothing width");
  const guards=cmp(s,rat(1n,BigInt(h)))<=0n&&cmp(mul(a,rat(q)),rat(BigInt(h)))>=0n&&cmp(mul(rat(3n),s),rat(BigInt(h)))<0n;
  check(L.selected_prime_power_theorem_parameter_guards===guards&&L.search_alpha_q_at_least_2_sqrt_n===(cmp(mul(mul(s,s),rat(q*q)),rat(BigInt(4*n)))>=0n),"selected theorem guards, separate necessary hardness interface");
  const m=integer(L.decision_rows,"original rows per call",1),tv2=div(rat(BigInt(11*m),28n*q*q),added);
  check(L.rounded_search_input_then_fresh_Gaussian_widening_TV_squared_upper===str(tv2),"bounded rounding coupling, not exact Gaussian law");
  scopes(L,["fresh_Gaussian_auxiliary_noise_is_not_a_fresh_original_sample","polynomial_expansion_of_disjoint_original_samples_is_required"],
    ["worst_case_lattice_reduction_compatibility_established","fixed_existing_source_bank_suffices_proved","same_width_search_recovery_claimed","rounding_then_widening_claimed_exact","full_source_adapter_or_published_reduction_implemented","actual_decision_algorithm_supplied"]);
  check(L.source_statement_url==="https://eprint.iacr.org/2011/501"&&L.source_statement.includes("review pending"),"primary theorem reference, adapted proof pending");
}
function normalization(L) {
  const n=integer(L.dimension,"dimension",1),r=integer(L.root_digits,"digits",1),M=integer(L.word_trits,"trits",1);
  check(M>n*r,"positive symbolic surplus");
  same(L.hypothetical_balanced_fibre_size,{base:3,exponent:M-n*r},"symbolic balanced count");
  same(L.hypothetical_raw_comparison_positive_eigenvalue,{base:3,exponent:-n*r},"tiny absolute eigenvalue");
  same(L.ideal_raw_comparison_accepts_codewords,{base:3,exponent:-n*r},"raw codeword acceptance");
  check(L.ideal_span_effect_accepts_codewords==="1"&&L.supported_condition_number==="1","condition one is not scale one");
  scopes(L,[],["small_condition_number_supplies_absolute_spectral_normalization","balanced_source_assumed_by_decision_ledger","known_single_seed_reflection_is_the_span_reflection","efficient_group_twirl_or_label_forward_map_supplies_span_projection"]);
}
function verify(p) {
  check(p.status==="SOURCE_SPECIFIC_WORD_SPAN_DECISION_AND_WIDTH_CHANGING_REDUCTION_TARGET_REVIEW_PENDING","review pending");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_word_span_decision.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_WORD_SPAN_DECISION.md")),"current mathematical provenance");
  const deps=["native_word_frame_access.py","native_full_root_slice.py","native_small_multiple_completion.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct dependency set");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.actual_original_data_controls.length===4&&p.scaling_decision_route_ledgers.length===4,"reference coverage");
  const stats=p.actual_original_data_controls.map(bounded);
  p.scaling_decision_route_ledgers.forEach((s,i)=>{
    const d=s.decision,w=s.width_changing_search_route;decision(d);route(w);normalization(s.raw_normalization_countercontrol);
    check(d.dimension===[8,32,64,128][i]&&d.dimension===d.root_digits&&d.original_pairs===d.dimension*d.dimension+12,"live quadratic bank profile");
    check(d.dimension===w.dimension&&d.root_digits===w.root_digits&&w.decision_rows===d.original_classical_values,"same source scope across route");
    const q=exactInteger(d.original_modulus,"modulus"),a=parse(w.decision_continuous_D_alpha_width);
    check(str(a)===str(rat(1n,BigInt(d.dimension)**3n))&&d.true_original_marginal_second_moment_upper===str(add(div(mul(rat(q*q),mul(a,a)),rat(3n)),rat(1n,2n))),"true rounded-Gaussian hypothetical moment profile");
    check(s.raw_normalization_countercontrol.dimension===d.dimension&&s.raw_normalization_countercontrol.root_digits===d.root_digits,"same normalization countercontrol");
  });
  const c=p.null_independence_countercontrol,banks=c.complete_equal_weight_original_banks;check(banks.length===3,"complete correlated null support");
  banks.forEach((b,t)=>{
    const result=bounded(b);check(E.field(3).eq(result.probability,E.field(3).unit),"correlated null codewords accepted exactly");
    same(b.known_mask,[0],"countercontrol has no hidden mask");same(b.truth_fixture_only.masked_secret,[t],"complete uniform scalar mixture");
    check(b.original_records.length===4&&b.original_records.every(r=>r.modulus===3&&r.value===t&&JSON.stringify(r.label)==="[1]"),"uniform marginal but dependent raw observations");
  });
  check(c.kind==="UNIFORM_RAW_MARGINALS_WITH_CODEWORD_DEPENDENCE_ARE_NOT_THE_NULL"&&c.exact_correlated_null_mean_span_acceptance==="1"&&c.exact_IID_null_mean_span_acceptance==="1/3","null countercontrol laws");
  scopes(c,["each_raw_value_marginal_uniform","countercontrol_is_not_a_hard_source_or_speedup_candidate"],["raw_values_jointly_IID"]);
  scopes(p,[],["accepted_speedup_candidate","new_active_negative_result_created"]);
  check(p.research_decision==="SEARCH_SOURCE_COMPATIBLE_DECISION_MECHANISMS_TOO; DO_NOT_REQUIRE_FIXED_BANK_FULL_COHERENT_DECODING_BY_FIAT","research objective not narrowed to receiver by fiat");
  return {verified:true,exact_actual_word_rows:stats.reduce((a,s)=>a+s.words,0),distinct_null_character_pairs:stats.reduce((a,s)=>a+s.character_pairs,0),
    exact_scale_ledgers:4,correlated_null_countercontrols:3,efficient_decision_effect_supplied:false,published_reduction_implemented:false};
}
module.exports={verify,bounded,decision,route,normalization};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

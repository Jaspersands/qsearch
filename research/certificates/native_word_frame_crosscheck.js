"use strict";
// Exact public maps, counts, noise/access ledgers; floating bounded receiver replay.
// The receiver replay is diagnostic, NOT a scalable circuit or exact gate certificate.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),H=require("./native_short_preimage_crosscheck.js");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one,zero}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_word_frame_access.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod=(x,q)=>(x%q+q)%q,min=(a,b)=>cmp(a,b)<=0n?a:b;
function isqrt(x) {
  check(x>=0n,"nonnegative integer square root");if(x<2n)return x;
  let a=1n<<BigInt(Math.ceil(x.toString(2).length/2)),b=(a+x/a)/2n;
  while(b<a){a=b;b=(a+x/a)/2n;}return a;
}
function sqrtBox(x,bits) {
  check(x[0]>=0n&&Number.isInteger(bits)&&bits>0&&bits<=256,"bounded rational square-root enclosure");
  const scale=1n<<BigInt(bits),k=isqrt(x[0]*scale*scale/x[1]),a=rat(k,scale);
  return [a,cmp(mul(a,a),x)===0n?a:rat(k+1n,scale)];
}
function rootDigits(q) {let r=0;while(q%3n===0n&&q>1n){q/=3n;r++;}check(q===1n&&r>0,"ternary root");return r;}
function tuples(q,n) {return n?tuples(q,n-1).flatMap(w=>Array.from({length:q},(_,a)=>[...w,a])):[[]];}
function* words(M,p=[]) {if(p.length===M){yield p;return;}for(let t=0;t<3;t++)yield*words(M,[...p,t]);}
function idealInterval(counts,D,N,bits) {
  let lo=zero,hi=zero;
  counts.forEach(c=>{const [a,b]=sqrtBox(rat(BigInt(c)),bits);lo=add(lo,a);hi=add(hi,b);});
  const denominator=rat(BigInt(D*N));
  return {lower:str(div(mul(lo,lo),denominator)),upper:str(min(one,div(mul(hi,hi),denominator))),
    enclosure_bits:bits,source:"ACTUAL_COMPLETE_PUBLIC_FIBRE_COUNTS",coverage_is_inferred_from_small_controls:false};
}
const cadd=(a,b)=>[a[0]+b[0],a[1]+b[1]],cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],
  scale=(a,b)=>[a[0]*b,a[1]*b],abs2=a=>a[0]*a[0]+a[1]*a[1];
const close=(a,b,message)=>check(Number.isFinite(a)&&Math.abs(a-b)<=2e-10,message);
function bounded(c) {
  const s=c.preparation_contract,f=s.public_family,q=Number(f.modulus),n=f.dimension,B=f.cohorts,M=f.sites,D=B*3**M,N=q**n;
  check([3,9].includes(q)&&Number.isSafeInteger(D)&&D<=256&&N<=256&&[1,2,4].includes(B)&&Number.isInteger(M)&&M>0,"bounded native calibration");
  const raw=c.original_records,mask=c.known_mask;
  check(raw.length===2*B*M&&mask.length===n&&new Set(raw.map(r=>r.source_id)).size===raw.length,"actual originals and mask");
  raw.forEach(r=>check(r.modulus===q&&r.label.length===n&&r.label.every(a=>Number.isInteger(a)&&a>=0&&a<q)&&Number.isInteger(r.value)&&r.value>=0&&r.value<q,"canonical original records"));
  const pairs=Array.from({length:B},(_,b)=>Array.from({length:M},(_,j)=>raw.slice(2*(b*M+j),2*(b*M+j)+2).map(r=>r.label)));
  same(f,{modulus:String(q),dimension:n,cohorts:B,sites:M,paired_labels:pairs,responses_masks_source_IDs_and_errors_supplied:false},"actual public family");
  const masked=r=>mod(r.value+r.label.reduce((v,a,i)=>v+a*mask[i],0),q);
  const phases=Array.from({length:B},(_,b)=>Array.from({length:M},(_,j)=>{
    const [a,c]=raw.slice(2*(b*M+j),2*(b*M+j)+2).map(masked);return [a,mod(c-a,q),mod(-c,q)];
  }));
  same(s,{public_family:f,known_word_phases_by_cohort:phases,original_records_paid_once:2*B*M,
    cohort_controlled_local_diagonal_gates:B*M,uniform_index_qubits:Math.log2(B),uniform_qutrits:M,
    word_domain_size:String(D),frequency_group_size:String(N),frequency_coordinate_trits:n*rootDigits(BigInt(q)),
    secret_or_errors_supplied_to_preparation:false,same_as_previous_native_point_seed:false,
    all_word_table_required_for_indexed_preparation:false,normalized_fibre_oracle_supplied:false,
    physical_gate_synthesis_and_precision_supplied:false},"all local feature preparation access charged");
  const order=tuples(q,n),positions=new Map(order.map((x,i)=>[JSON.stringify(x),i])),counts=Array(N).fill(0),rows=[];
  for(let b=0;b<B;b++)for(const w of words(M)) {
    const freq=H.frequency(f,b,w),phase=mod(w.reduce((a,t,j)=>a+phases[b][j][t],0),q);
    counts[positions.get(JSON.stringify(freq))]++;rows.push({cohort:b,word:w,frequency:freq,known_phase:phase});
  }
  same(c.frequency_order,order,"product group order");same(c.word_rows,rows,"all actual word phases and forward labels");same(c.fibre_counts,counts,"complete actual fibre counts");
  same(c.public_singular_values_squared_exact,counts.map(x=>str(rat(BigInt(x),BigInt(D)))),"absolute public incidence singular values");
  const positive=counts.filter(x=>x>0);check(c.supported_condition_number_squared_exact===str(rat(BigInt(Math.max(...counts)),BigInt(Math.min(...positive)))),"supported relative condition");
  same(c.ideal_clean_receiver_success_interval,idealInterval(counts,D,N,c.ideal_clean_receiver_success_interval.enclosure_bits),"exact ideal success enclosure");
  const sums=Array.from({length:N},()=>[0,0]),target=c.truth_fixture_only.masked_secret,errors=c.truth_fixture_only.original_errors;
  check(target.length===n&&errors.length===raw.length,"complete truth-only errors");
  raw.forEach((r,j)=>check(mod(r.value+r.label.reduce((a,t,i)=>a+t*mask[i],0)-r.label.reduce((a,t,i)=>a+t*target[i],0),q)===mod(errors[j],q),"actual masked source errors"));
  let overlap=[0,0],squaredWordError=0n;
  rows.forEach(row=>{
    const angle=2*Math.PI*row.known_phase/q,point=[Math.cos(angle),Math.sin(angle)],i=positions.get(JSON.stringify(row.frequency));
    sums[i]=cadd(sums[i],point);
    const actualError=row.word.reduce((a,t,j)=>{
      const [e1,e2]=errors.slice(2*(row.cohort*M+j),2*(row.cohort*M+j)+2).map(BigInt);return a+[e1,e2-e1,-e2][t];
    },0n);
    squaredWordError+=actualError*actualError;
    const theta=2*Math.PI*Number(mod(actualError,BigInt(q)))/q;overlap=cadd(overlap,[Math.cos(theta)/D,Math.sin(theta)/D]);
  });
  let pairError=0n;for(let j=0;j<errors.length;j+=2){const a=BigInt(errors[j]),b=BigInt(errors[j+1]);pairError+=a*a+b*b-a*b;}
  const exactMoment=rat(2n*pairError,3n*BigInt(B));check(c.word_error_mean_square_exact===str(exactMoment)&&str(rat(squaredWordError,BigInt(D)))===str(exactMoment),"exact pathwise word averaging identity");
  check(c.pathwise_trace_distance_squared_rational_upper===str(min(one,div(mul(rat(40n),exactMoment),rat(BigInt(q*q))))),"pathwise phase-noise bound");
  const transform=(values)=>order.map(secret=>values.reduce((a,value,j)=>{
    const angle=-2*Math.PI*order[j].reduce((a,x,i)=>a+x*secret[i],0)/q;
    return cadd(a,scale(cmul(value,[Math.cos(angle),Math.sin(angle)]),1/Math.sqrt(N)));
  },[0,0]));
  const good=transform(sums.map((z,i)=>counts[i]?scale(z,1/Math.sqrt(D*counts[i])):[0,0]));
  const comparison=transform(sums.map(z=>scale(z,1/D)));
  const law=good.map(abs2),mass=law.reduce((a,b)=>a+b,0),index=positions.get(JSON.stringify(target));
  c.reference_good_outcome_probabilities.forEach((p,i)=>close(p,law[i],"bounded floating full good law"));
  close(c.reference_good_mass,mass,"all good mass");close(c.reference_failure_mass,1-mass,"orthogonal leakage remains failure");
  close(c.reference_correct_and_good_probability,law[index],"unconditional true good probability");
  close(c.reference_ideal_correct_probability,positive.reduce((a,c)=>a+Math.sqrt(c),0)**2/(D*N),"ideal clean reference law");
  close(c.comparison_good_mass,comparison.map(abs2).reduce((a,b)=>a+b,0),"raw comparison mass");
  close(c.comparison_correct_and_good_probability,abs2(comparison[index]),"raw comparison correct probability");
  check(c.ideal_comparison_good_mass_exact===str(rat(BigInt(counts.reduce((a,c)=>a+c*c,0)),BigInt(D*D)))&&c.ideal_comparison_correct_and_good_exact===str(rat(1n,BigInt(N))),"ideal comparison normalization");
  check(c.pointer_discarded_Fourier_probabilities.length===N,"complete discarded pointer law");c.pointer_discarded_Fourier_probabilities.forEach(p=>close(p,1/N,"discarded pointer gives no secret phase"));
  close(c.pure_source_trace_distance_squared,Math.max(0,1-abs2(overlap)),"whole feature source distance");
  check(c.maximum_diagnostic_matrix_residual>=0&&c.maximum_diagnostic_matrix_residual<1e-10,"reported finite matrix tolerance");
  check(c.dense_control_is_exponential_calibration===true&&c.finite_float_laws_are_exact_certificates===false&&c.normalized_row_oracle_is_supplied_at_polynomial_cost===false&&c.new_speedup_claim===false,"diagnostic receiver is not an implemented scalable algorithm");
  return {words:D,outcomes:N};
}
function noise(L) {
  const q=BigInt(L.modulus),M=L.sites,V=parse(L.true_marginal_original_second_moment_upper);rootDigits(q);
  check(Number.isInteger(M)&&M>0&&V[0]>=0n,"marginal original noise promise");
  const bound=min(one,div(mul(rat(BigInt(80*M)),V),rat(q*q))),[lo,hi]=sqrtBox(bound,L.enclosure_bits);
  check(L.mean_pure_trace_distance_squared_upper===str(bound)&&L.mean_unconditional_measurement_loss_bound_lower_enclosure===str(lo)&&L.mean_unconditional_measurement_loss_upper===str(min(one,hi)),"exact marginal-noise and Jensen enclosure");
  check(L.bound_is_on_complete_good_and_failure_measurement===true,"unconditional measurement loss");
  ["original_independence_or_zero_mean_required","errors_independent_of_public_labels_required","fresh_original_errors_per_word_required",
    "ideal_fibre_coverage_or_success_proved_by_moments","generic_physical_gate_errors_included","efficient_normalized_fibre_circuit_supplied","accepted_speedup_candidate"].forEach(k=>check(L[k]===false,"noise scope "+k));
}
function balanced(L) {
  const n=L.dimension,r=L.root_digits,N=3n**BigInt(n*r),D=BigInt(L.word_domain_size),surplus=D/N;
  check(Number.isInteger(n)&&n>0&&Number.isInteger(r)&&r>0&&D===N*3n**24n,"declared balanced symbolic countercontrol");
  check(L.frequency_group_size===String(N)&&L.hypothetical_exact_balanced_fibre_size===String(surplus)&&L.comparison_singular_value_squared===str(rat(1n,N)),"absolute balanced singular values");
  check(L.supported_condition_number_squared==="1"&&L.ideal_clean_receiver_success==="1"&&L.raw_comparison_correct_and_good_probability===str(rat(1n,N))&&L.normalization_multiplier_squared===String(N),"relative conditioning does not remove absolute scale");
  check(L.this_is_a_symbolic_access_countercontrol_not_generated_source===true,"no claimed balanced generated source");
  ["actual_random_native_family_is_proved_balanced","polynomial_clean_row_implementation_supplied","all_decoders_have_this_normalization_cost"].forEach(k=>check(L[k]===false,"countercontrol scope "+k));
}
function randomLabel(L) {
  const n=L.dimension,r=L.root_digits,B=L.cohorts,M=L.sites,N=3n**BigInt(n*r),D=BigInt(B)*3n**BigInt(M);
  check(Number.isInteger(n)&&n>0&&Number.isInteger(r)&&r>0&&Number.isInteger(B)&&B>0&&(B&(B-1))===0&&Number.isInteger(M)&&M>0,"random original label source shape");
  check(L.frequency_group_size===String(N)&&L.word_domain_size===String(D)&&BigInt(L.noise.modulus)===3n**BigInt(r)&&L.noise.sites===M,"actual word and frequency population sizes and same noise source");noise(L.noise);
  const failure=min(one,rat(N-1n,D)),success=sub(one,failure),loss=parse(L.noise.mean_unconditional_measurement_loss_upper),raw=sub(success,loss),noisy=cmp(raw,zero)>0n?raw:zero;
  check(L.ideal_ensemble_receiver_failure_upper===str(failure)&&L.ideal_ensemble_receiver_success_lower===str(success)&&L.noisy_complete_ensemble_receiver_success_lower===str(noisy),"pairwise collision / Hellinger / complete-noise ensemble bound");
  ["IID_uniform_original_public_labels_for_each_fixed_secret_required","bound_is_unconditional_over_original_dataset_and_complete_receiver","normalized_fibre_circuit_is_an_explicit_missing_assumption"].forEach(k=>check(L[k]===true,"ensemble promise "+k));
  ["original_errors_independent_of_labels_required","source_population_promises_established_by_small_artifacts","per_dataset_success_or_exact_balance_guaranteed","efficient_receiver_constructed","accepted_speedup_candidate"].forEach(k=>check(L[k]===false,"ensemble scope "+k));
}
function verify(p) {
  check(p.status==="NATIVE_WORD_FRAME_ROW_ACCESS_AND_NOISE_CONTRACT_EXTERNAL_REVIEW_PENDING","review pending");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_word_frame_access.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_WORD_FRAME_ACCESS.md")),"current source and derivation provenance");
  const deps=["native_short_preimage_reduction.py","native_known_seed_group_workbench.py","native_noisy_phase_input.py","ternary_certified_noise_sampler.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py","known_preparation_coherent_reflection.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct dependency provenance");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"current dependency "+f));
  check(p.bounded_reference_controls.length===4&&p.scalable_conditional_access_ledgers.length===4,"declared reference coverage");
  const stats=p.bounded_reference_controls.map(bounded);p.scalable_conditional_access_ledgers.forEach(s=>{noise(s.noise);balanced(s.hypothetical_balanced_access);randomLabel(s.random_label_reference);same(s.noise,s.random_label_reference.noise,"same source moment budget");check(s.dimension===s.hypothetical_balanced_access.dimension&&s.dimension===s.random_label_reference.dimension,"scale identity");});
  ["accepted_speedup_candidate","new_active_negative_result_created","efficient_normalized_fibre_circuit_supplied","general_quantum_decoder_lower_bound_proved"].forEach(k=>check(p[k]===false,"report scope "+k));
  return {verified:true,exact_word_rows:stats.reduce((a,s)=>a+s.words,0),floating_receiver_outcomes:stats.reduce((a,s)=>a+s.outcomes,0),exact_scale_ledgers:4,floating_receiver_replay_is_exact_certificate:false};
}
module.exports={verify,bounded,noise,balanced,sqrtBox};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

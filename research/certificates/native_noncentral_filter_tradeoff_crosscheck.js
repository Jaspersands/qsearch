"use strict";

const fs=require("fs"), path=require("path");
const {check,same,rat,add,sub,mul,div,parse,str,cmp,mod,field,matrices}=require("./cyclotomic_exact");
const out=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../reductions/native_noncentral_filter_tradeoff.json"),"utf8"));
const near=(x,y,msg)=>check(Number.isFinite(x)&&Math.abs(x-y)<2e-10,msg);
const num=x=>Number(x[0])/Number(x[1]);
const trim=a=>{while(a.length&&a[a.length-1]===0n)a.pop();return a;};
const plus=(a,b)=>trim(Array.from({length:Math.max(a.length,b.length)},(_,i)=>(a[i]||0n)+(b[i]||0n)));
const scale=(a,n)=>trim(a.map(x=>x*n));
const times=(a,b)=>{const c=Array(a.length+b.length?Math.max(0,a.length+b.length-1):0).fill(0n);a.forEach((x,i)=>b.forEach((y,j)=>c[i+j]+=x*y));return trim(c);};
const encode=a=>a.map(String), X=[0n,1n], oneMinusX=[1n,-1n];
function amplitude(k) {let a=[1n],b=[3n,-4n];if(!k)return a;for(let i=1;i<k;i++)[a,b]=[b,plus(times([2n,-4n],b),scale(a,-1n))];return b;}
function second(k) {let a=[1n],b=[2n,-4n];if(!k)return a;for(let i=1;i<k;i++)[a,b]=[b,plus(times([2n,-4n],b),scale(a,-1n))];return b;}
function spectral(x,k) {let a=rat(0n);for(const c of amplitude(k).slice().reverse())a=add(mul(a,x),rat(c));return mul(x,mul(a,a));}
const probability=(x,s,msg)=>check(cmp(x,parse(s))===0n,msg);
check(out.status==="NATIVE_NONCENTRAL_FIXED_FILTER_RANK_DEPTH_AUDIT_REVIEW_PENDING","local scoped audit status");
check(out.group_filter_must_ignore_observed_frequency_labels_for_exponential_rank_bound===true,"critical label-independence premise");
check(out.only_fixed_filter_two_reflection_sequences_covered===true,"only fixed two-reflection sequence covered");
for(const name of ["label_adaptive_filters_ruled_out","rank_lower_bound_is_a_memory_lower_bound","arbitrary_adaptive_collective_or_high_rank_receivers_ruled_out","new_quantum_speedup_claimed","novelty_claimed"])check(out[name]===false,"no broad cut or speedup");
check(out.same_group_diagonal_tensor_orbit_group_marginal_independent_of_copy_count===true,"same group, unconditioned source marginal");
check(out.bound==="p_k <= min(1,(2k+1)^2*rank(P)/3^(nr))","rank/depth bound");
check(out.exact_amplification_interval_SOS_certificates.length===9,"whole finite SOS cohort");
for(const [k,c] of out.exact_amplification_interval_SOS_certificates.entries()) {
  check(c.iterations===k,"SOS iteration");
  const a=amplitude(k),n=BigInt(2*k+1),gap=plus(scale(X,n*n),scale(times(X,times(a,a)),-1n));
  same(c.amplitude_polynomial_ascending_integer_coefficients,encode(a),"exact seed amplitude polynomial");
  same(c.exact_gap_polynomial_ascending_integer_coefficients,encode(gap),"exact bound gap");
  check(c.positive_SOS_terms.length===2*k,"all pair-separation SOS terms");
  let reconstructed=[];
  c.positive_SOS_terms.forEach((t,i)=>{
    const d=i+1,odd=d%2,p=odd?amplitude((d-1)/2):second(d/2-1),weight=(odd?4:16)*(2*k+1-d);
    check(t.separation===d&&t.positive_weight===weight,"positive SOS coefficient");
    check(t.nonnegative_interval_factor===(odd?"x_squared":"x_squared_times_one_minus_x"),"interval nonnegative factor");
    same(t.squared_polynomial_ascending_integer_coefficients,encode(p),"known squared polynomial");
    let term=times(times(X,X),times(p,p));if(!odd)term=times(term,oneMinusX);
    reconstructed=plus(reconstructed,scale(term,BigInt(weight)));
  });
  same(encode(reconstructed),encode(gap),"integer-polynomial SOS reconstruction");
}

function smallSourceOverlap(level,secret) {
  const K=field(3),M=matrices(K),h1=level===1?1:3,cross=level===1?2:0;
  const reduce=([a,b])=>[mod(a-cross*Math.floor(b/h1),3),mod(b,h1)];
  const ringMul=(a,b)=>reduce([a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1]]);
  const phase=(a,b)=>{const v=ringMul(a,b);return mod(level===1?2*v[0]-v[1]:-v[0]+v[1],3);};
  const roots=[[1,0],[0,1],[-1,-1]],lambdas=[[0,0],[1,0],[1,1]];
  let mean=K.F();
  for(let a=0;a<3;a++)for(let b=0;b<h1;b++) {
    const label=[a,b],v=lambdas.map(l=>[K.powers[phase(label,ringMul(secret,l))]]),R=M.zeroM(3,3);
    for(let j=0;j<3;j++){const out=mod(j-1,3);R[out][j]=K.powers[phase(label,ringMul([-1,0],roots[out]))];}
    mean=K.plus(mean,M.times(M.times(M.star(v),R),v)[0][0]);
  }
  mean=K.scale(mean,rat(1n,BigInt(9*h1)));
  check(mean.slice(1).every(x=>x[0]===0n),"exact original source overlap real rational");
  return mean[0];
}

same(out.complete_actual_native_controls.map(c=>[c.native_level,c.native_secret,c.original_source_copies]),[1,2].flatMap(r=>[[1,0],[2,0]].flatMap(s=>[1,2].map(m=>[r,s,m]))),"actual cohort, not selected records");
let histories=0;
for(const c of out.complete_actual_native_controls) {
  const r=c.native_level,m=c.original_source_copies,N=3**(r+1),E=3**r,phi=smallSourceOverlap(r,c.native_secret),matches=cmp(phi,rat(1n))===0n;
  check(c.group_dimension===N&&c.seed_dimension_per_public_label_cohort===3**m&&c.complete_public_label_cohort_count===E**m,"actual complete source sizes");
  same(c.public_fixed_generator_guess,[[[2,0]],1],"public fixed generator, not supplied hidden secret");
  check(c.fixed_guess_matches_hidden_generator===matches,"source overlap gives guess match");
  near(c.same_group_coset_density_error,0,"same group diagonal copies retain coset density");
  near(c.maximum_actual_vs_seed_polynomial_good_vector_error,0,"actual full good vector obeys compression polynomial");
  same(c.noncentral_filters.map(f=>f.public_group_filter),["identity_coordinate","public_hidden_generator_pair","zero_rotation_coordinates"],"all source-filter controls");
  for(const f of c.noncentral_filters) {
    const rank=f.public_group_filter==="zero_rotation_coordinates"?E:1;
    check(f.group_filter_rank===rank,"actual group rank");
    check(f.high_rank_filter_has_a_single_public_rotation_digit_test===(rank===E),"high rank can be one cheap digit predicate");
    check(f.source_weighted_iteration_history.length===7,"complete depth history");
    for(const [k,h] of f.source_weighted_iteration_history.entries()) {
      check(h.iterations===k&&h.known_original_controlled_R_calls===m*(2*k+1),"paid depth and copies");
      let p;
      if(f.public_group_filter==="identity_coordinate")p=spectral(rat(1n,BigInt(N)),k);
      else if(f.public_group_filter==="zero_rotation_coordinates")p=spectral(rat(1n,3n),k);
      else {const high=spectral(rat(2n,BigInt(N)),k),low=spectral(rat(1n,BigInt(2*N)),k);p=matches?high:div(add(high,mul(rat(2n),low)),rat(3n));}
      probability(p,h.exact_raw_success_probability,"source-weighted exact relative probability");
      near(h.actual_raw_success_probability,num(p),"actual source probability");
      let bound=rat(BigInt(rank*(2*k+1)**2),BigInt(E));if(cmp(bound,rat(1n))>0n)bound=rat(1n);
      probability(bound,h.exact_rank_depth_upper_bound,"capped rank/depth bound");
      check(cmp(p,bound)<=0n,"actual probability within scoped bound");histories++;
    }
  }
  const base=c.direct_order_three_stabilizer_baseline,diagonal=matches?rat(1n):rat(1n,3n),separate=matches?rat(1n):rat(1n,BigInt(3**m));
  probability(diagonal,base.exact_diagonal_tensor_acceptance,"direct diagonal stabilizer baseline");
  probability(separate,base.exact_separate_copy_all_acceptance,"separate stabilizer copies, not diagonal averaging");
  near(base.actual_diagonal_tensor_acceptance,num(diagonal),"actual direct baseline");near(base.actual_separate_copy_all_acceptance,num(separate),"actual separate baseline");
  check(base.known_controlled_original_R_calls_for_separate_copy_baseline===m,"direct baseline action cost");
  same(base.hidden_generator_search_space,{base:3,exponent:r},"native guess search space");
  for(const n of ["baseline_ignores_information_in_the_recorded_public_labels","no_lower_bound_on_label_aware_inference_claimed"])check(base[n]===true,"label-aware inference remains outside guess-baseline claim");
  for(const n of ["efficient_full_secret_search_supplied","classical_dequantization_claimed"])check(base[n]===false,"verification baseline is not a classical solver");
  check(c.unknown_seed_reflection_supplied===false&&c.full_depth_receiver_supplied===false,"no stronger oracle or decoder");
}

let exactFrequencyRows=0;
check(out.growing_root_label_adaptive_countercontrols.length===2,"label-adaptive countercontrols retained");
for(const [i,c] of out.growing_root_label_adaptive_countercontrols.entries()) {
  const r=i+3,h0=9,h1=r===3?3:9,cross=r===3?6:0,E=h0*h1,N=3*E,K=field(9),M=matrices(K);
  check(c.native_level===r&&c.group_dimension===N&&c.label_adaptive_group_filter_rank===3,"growing root conditional group rank");
  same(c.public_frequency_label,[[1,0]],"actual observed label, not an unobserved oracle");
  const reduce=([a,b])=>[mod(a-cross*Math.floor(b/h1),h0),mod(b,h1)];
  const ringMul=(a,b)=>reduce([a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1]]);
  const phase=b=>mod(r===3?b[0]-2*b[1]:b[1],9);
  const roots=[[1,0],[0,1],[-1,-1]];
  for(let t=0;t<3;t++) {
    const S=M.zeroM(3,3);
    for(let a=0;a<h0;a++)for(let b=0;b<h1;b++) {
      const v=[a,b];
      for(let j=0;j<3;j++) {const o=mod(j-t,3),k=mod(phase(ringMul(v,roots[o]))-phase(v),9);S[o][j]=K.plus(S[o][j],K.powers[k]);}
    }
    const target=M.zeroM(3,3);target[0][t]=K.scale(K.unit,rat(BigInt(E)));
    check(M.eq(S,target),"exact abelian-frequency projection is seed-row relocation, for every input vector");exactFrequencyRows++;
  }
  probability(rat(9n,BigInt(N)),c.source_label_blind_rank_bound_at_zero_iterations_NOT_APPLICABLE,"blind bound fails on label-dependent filter");
  check(c.compressed_operator==="I_seed/3"&&c.source_copies_used===1,"conditional compression and source cost");
  for(const n of ["selected_abelian_frequency_is_the_observed_native_label","conditional_original_seed_and_reference_recovered_in_rotation_register","seed_qutrit_output_is_known_basis_state_on_success","no_cloning_or_deterministic_success_claimed"])check(c[n]===true,"label-adaptive source relocation scope");
  for(const n of ["filter_depends_on_secret","new_secret_information_extracted","unknown_seed_reflection_supplied","full_depth_secret_decoder_supplied"])check(c[n]===false,"relocation is not secret decoding");
  check(c.iteration_histories.length===3,"full relocation history");
  c.iteration_histories.forEach((h,k)=>{const p=spectral(rat(1n,3n),k);check(h.iterations===k&&h.known_controlled_original_R_calls===2*k+1,"relocation action cost");probability(p,h.exact_raw_success_probability,"conditional exact success");near(h.actual_raw_success_probability,num(p),"conditional actual success");near(h.raw_failure_probability,1-num(p),"failure branches charged");near(h.normalized_reference_entangled_seed_relocation_error,0,"reference-preserving relocation");});
}
same(out.growing_rank_depth_ledgers.map(r=>[r.native_level,r.native_dimension]),[[2,1],[8,8],[32,32],[128,128]],"growing symbolic ledgers");
for(const r of out.growing_rank_depth_ledgers) {
  const e=r.native_level*r.native_dimension,k=e,rank=e+1;
  check(r.relative_iterations===k&&r.group_filter_rank===rank&&r.original_IID_native_copies_in_same_group_orbit===e,"declared polynomial-resource probe");
  same(r.raw_success_probability_upper_bound,{cap:1,numerator:rank*(2*k+1)**2,denominator:{base:3,exponent:e}},"no enormous coset table, symbolic raw bound");
  check(r.known_controlled_original_R_calls===e*(2*k+1)&&r.same_group_coordinate_trits===e+1,"actual controlled-action ledger");
  for(const n of ["same_group_orbit_copy_count_does_not_change_group_marginal","rank_is_not_qubits_or_memory_bits","filter_must_be_independent_of_observed_native_frequency_labels"])check(r[n]===true,"rank bound assumptions");
  for(const n of ["label_adaptive_filters_covered","different_or_adaptive_filters_covered","arbitrary_noncentral_or_collective_receivers_covered","unknown_seed_reflection_used"])check(r[n]===false,"escape routes and access boundary");
}
console.log(JSON.stringify({status:"PASS",exact_interval_SOS_certificates:9,actual_native_source_histories:histories,exact_growing_root_frequency_row_identities:exactFrequencyRows,label_adaptive_escape_preserved:true,arbitrary_receiver_lower_bound_claimed:false}));

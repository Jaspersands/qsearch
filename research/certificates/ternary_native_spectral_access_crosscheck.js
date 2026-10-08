"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp}=require("./cyclotomic_exact.js");
const root=path.join(__dirname,"../.."),R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(root,"research/phase_workbench/ternary_native_spectral_access.json"),"utf8"));
const key=JSON.stringify,mod=(x,q)=>(x%q+q)%q,min=(a,b)=>cmp(a,b)<0n?a:b,max=(a,b)=>cmp(a,b)>0n?a:b;
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_NATIVE_SPECTRAL_ACCESS.md")),"pinned native access derivation");
for(const flag of["generic_quantum_receiver_lower_bound","native_spectral_generator_compiler_supplied","quantum_speedup_proved","candidate_record_accepted","novelty_claim"])check(R[flag]===false,"unsupported access claim: "+flag);
function cube(q,n){let out=[[]];for(let i=0;i<n;i++)out=out.flatMap(v=>Array.from({length:q},(_,t)=>[...v,t]));return out;}
function nativeChart(level){
  check([2,4,6].includes(level),"bounded complete native chart");
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(level/2),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);
  check(a%den===0n&&b%den===0n,"native integer chart");const u=a/den,v=b/den;
  return label=>{const[x,y]=label.map(BigInt);return[Number((u*x+v*y)%q+q)%Number(q),Number(((u+v)*x-u*y)%q+q)%Number(q)];};
}
function isqrt(x){check(x>=0n,"nonnegative radical");if(x<2n)return x;let a=1n<<BigInt(Math.ceil(x.toString(2).length/2));while(true){const b=(a+x/a)/2n;if(b>=a)return a;a=b;}}
function sqrtInterval(x,bits){const scale=1n<<BigInt(bits),a=BigInt(x)*scale*scale,lo=isqrt(a);return[rat(lo,scale),rat(lo*lo===a?lo:lo+1n,scale)];}
function frequencies(c){
  const chart=nativeChart(c.native_level),F=c.original_ring_labels.map(row=>{const a=row.map(chart);return[a.map(x=>x[0]),a.map(x=>x[1])];});
  same(F,c.native_frequencies,"actual native ring chart, not convenient substitute frequencies");return F;
}
function values(F,q){return cube(3,F.length).map(word=>F[0][0].map((_,j)=>mod(word.reduce((s,t,i)=>s+(t===0?0:F[i][t-1][j]),0),q)));}
function counts(values){const out=new Map();values.forEach(y=>out.set(key(y),(out.get(key(y))||0)+1));return out;}
let terms=0,permutations=0,nativeWords=0,populations=0;
function translation(C,group,d,q,D,c){
  check(d.length===group[0].length&&d.every(a=>Number.isInteger(a)&&a>=0&&a<q),"full-root offset");same(d,c.fixed_frequency_offset,"offset pinned");
  const bits=c.sqrt_interval_bits;check(Number.isInteger(bits)&&bits>0&&bits<=128,"bounded radical interval");
  let lower=zero,upper=zero,matched=0,pairs=0;const entries=[];
  for(const y of group){const z=y.map((a,i)=>mod(a+d[i],q)),a=C.get(key(y))||0,b=C.get(key(z))||0;matched+=Math.min(a,b);pairs+=a*b;
    if(a*b){const[lo,hi]=sqrtInterval(a*b,bits);lower=add(lower,div(lo,rat(BigInt(D))));upper=add(upper,div(hi,rat(BigInt(D))));entries.push({source_frequency:y,target_frequency:z,source_fiber_count:a,target_fiber_count:b,sqrt_product_lower:str(lo),sqrt_product_upper:str(hi)});terms++;}}
  same(entries,c.all_nonzero_radical_terms,"complete radical sum and independently recomputed integer square-root bounds");
  check(c.native_words===D&&c.optimal_arbitrary_public_unitary_mean_overlap_lower===str(lower)&&c.optimal_arbitrary_public_unitary_mean_overlap_upper===str(min(one,upper))&&c.optimal_public_permutation_mean_overlap_exact===str(rat(BigInt(matched),BigInt(D))),"exact unitary/permutation overlap envelopes");
  check(c.minimum_arbitrary_unitary_mean_squared_phase_error_lower===str(max(zero,sub(rat(2n),mul(rat(2n),upper))))&&c.minimum_arbitrary_unitary_mean_squared_phase_error_upper===str(sub(rat(2n),mul(rat(2n),lower)))&&c.ordered_frequency_shift_pair_count===pairs&&c.integer_collision_overlap_upper===str(min(one,rat(BigInt(pairs),BigInt(D))))&&c.exact_frequency_translation_permutation_exists===(matched===D),"phase-error and integer collision envelope");
  check(c.unitary_optimized_without_cost_or_q_order_constraints===true&&c.full_secret_recovery_or_general_receiver_lower_bound===false&&c.efficient_fiber_transform_supplied===false,"narrow target, not a compiler or general receiver no-go");
  return{lower,upper,matched,pairs};
}
same(R.native_controls.map(c=>[c.dimension,c.modulus,c.source_inputs,c.seed]),[[2,9,2,89811],[3,3,1,89813],[1,9,3,89821],[1,3,3,89823]],"prespecified under/overfull source controls");
for(const c of R.native_controls){
  const F=frequencies(c),q=c.modulus,group=cube(q,c.dimension),W=cube(3,c.source_inputs),V=values(F,q),C=counts(V);
  same(W,c.complete_words,"complete native word table");same(V,c.complete_frequency_values,"complete native frequency evaluator");same(group.map(y=>({frequency:y,count:C.get(key(y))||0})),c.complete_fiber_counts,"all occupied AND empty native fibers");
  check(c.native_level===2*Math.round(Math.log(q)/Math.log(3))&&F.length===c.source_inputs,"actual source root and dimension");
  for(const t of c.translations){const cert=t.certificate,d=cert.fixed_frequency_offset,bounds=translation(C,group,d,q,V.length,cert),P=t.reference_word_permutation;check(P.length===V.length&&new Set(P).size===V.length&&P.every(a=>Number.isInteger(a)&&a>=0&&a<V.length),"complete reference permutation");
    const matched=P.reduce((s,j,i)=>s+Number(key(V[i].map((a,k)=>mod(a+d[k],q)))===key(V[j])),0);check(matched===bounds.matched&&t.reference_matched_word_count===matched,"reference permutation attains exact optimum");
    const err=t.dense_arbitrary_unitary_mean_squared_phase_error,lo=Number(parse(cert.minimum_arbitrary_unitary_mean_squared_phase_error_lower)[0])/Number(parse(cert.minimum_arbitrary_unitary_mean_squared_phase_error_lower)[1]),hi=Number(parse(cert.minimum_arbitrary_unitary_mean_squared_phase_error_upper)[0])/Number(parse(cert.minimum_arbitrary_unitary_mean_squared_phase_error_upper)[1]);
    check(Number.isFinite(err)&&err>=lo-1e-10&&err<=hi+1e-10&&t.dense_unitarity_operator_norm_defect<1e-10&&t.floating_reference_is_exact_proof===false&&t.dense_reference_is_efficient_compiler===false,"floating calibration not exact proof");permutations++;}
  check(c.diagonal_computational_readout_secret_independent===true&&c.commutant_projective_readout_information_exact==="0"&&c.source_has_IID_population_law_from_calibration_seed===false,"commutant scope and seeded calibration disclosure");nativeWords+=V.length;
}
function population(L){
  const n=L.dimension,q=BigInt(L.modulus),m=L.original_source_qutrits,D=3n**BigInt(m),G=q**BigInt(n),overlap=min(one,rat(D-1n,G));
  check(L.native_word_dimension===String(D)&&L.full_frequency_group===String(G)&&L.mean_optimal_arbitrary_unitary_phase_overlap_upper===str(overlap)&&L.mean_minimum_squared_nondemolition_phase_error_lower===str(mul(rat(2n),sub(one,overlap)))&&L.mean_minimum_squared_nondemolition_phase_error_upper===str(min(rat(2n),rat(4n*(G-1n),D)))&&L.expected_chi_squared_frequency_nonuniformity_exact===str(rat(G-1n,D)),"symbolic fixed-offset native population ledgers");
  check(L.offset_must_be_fixed_nonzero_before_random_labels===true&&L.public_unitary_may_depend_on_all_labels===true&&L.requires_all_IID_uniform_full_native_frequency_rows===true&&L.general_receiver_lower_bound===false&&L.efficient_unitary_construction_supplied===false,"population scope");
}
[...R.underfull_population_ledgers,...R.overfull_population_ledgers].forEach(population);
for(const L of R.underfull_population_ledgers)check(cmp(parse(L.mean_minimum_squared_nondemolition_phase_error_lower),rat(16n,9n))>0n,"underfull generator error remains constant even with free gate cost");
const adaptive=R.adaptive_offset_scope_countercontrol,F=frequencies(adaptive),q=27,V=values(F,q),C=counts(V),group=cube(q,1);
same(adaptive.complete_words,cube(3,1),"adaptive control word cube");same(adaptive.complete_frequency_values,V,"adaptive native map");population(adaptive.fixed_offset_population_ledger);
const bound=translation(C,group,adaptive.certificate.fixed_frequency_offset,q,3,adaptive.certificate);
check(cmp(bound.lower,parse(adaptive.fixed_offset_population_ledger.mean_optimal_arbitrary_unitary_phase_overlap_upper))>0n&&adaptive.offset_was_chosen_from_labels===true&&adaptive.fixed_offset_population_bound_applies_to_this_selected_offset===false&&adaptive.one_instance_is_an_ensemble_refutation===false,"adaptive direction cannot inherit a fixed-direction population statement");
same(R.complete_small_native_populations.map(c=>[c.modulus,c.original_source_inputs]),[[3,1],[3,2],[9,1]],"whole small population specifications");
for(const c of R.complete_small_native_populations){
  const q=c.modulus,m=c.original_source_inputs,D=3**m,N=q**(2*m),group=cube(q,1);let edge=zero,chi=zero,lower=zero,upper=zero;
  const chart=nativeChart(q===3?2:4),chartImages=cube(q,2).map(chart);
  check(new Set(chartImages.map(key)).size===q*q&&chartImages.every(row=>row.every(x=>Number.isInteger(x)&&x>=0&&x<q)),"entire even-level native chart is a full-frequency bijection");
  for(const row of cube(q,2*m)){
    const F=Array.from({length:m},(_,i)=>[[row[2*i]],[row[2*i+1]]]),C=counts(values(F,q));let pairs=0,squares=0,lo=zero,hi=zero;
    group.forEach(y=>{const a=C.get(key(y))||0,b=C.get(key([mod(y[0]+1,q)]))||0;pairs+=a*b;squares+=a*a;const[l,h]=sqrtInterval(a*b,40);lo=add(lo,l);hi=add(hi,h);});
    edge=add(edge,rat(BigInt(pairs),BigInt(D*N)));chi=add(chi,sub(rat(BigInt(q*squares),BigInt(D*D*N)),rat(1n,BigInt(N))));lower=add(lower,div(lo,rat(BigInt(D*N))));upper=add(upper,div(hi,rat(BigInt(D*N))));
  }
  check(c.entire_native_label_matrices_checked===N&&c.mean_ordered_pair_over_word_dimension_exact===str(edge)&&c.mean_frequency_chi_squared_exact===str(chi)&&c.mean_optimal_unitary_overlap_lower===str(lower)&&c.mean_optimal_unitary_overlap_upper===str(upper)&&str(edge)===str(rat(BigInt(D-1),BigInt(q)))&&str(chi)===str(rat(BigInt(q-1),BigInt(D))),"entire native population and exact two-point identities");
  check(c.complete_native_chart_replayed===true&&c.finite_population_check_is_asymptotic_proof===false,"population reference not an asymptotic theorem");populations+=N;
}
console.log(JSON.stringify({status:"PASS",native_words_checked:nativeWords,reference_translation_permutations:permutations,radical_terms_checked:terms,complete_native_label_matrices_checked:populations,native_generator_compiler_supplied:false}));

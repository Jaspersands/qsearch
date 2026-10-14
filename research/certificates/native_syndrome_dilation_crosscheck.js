"use strict";
// Exact original-data overlaps, secret twirl, noncommutation and access prices.
// Numerical circuit arrays are independently covered by bounded matrix tests.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js"),S=require("./native_word_spectral_filter_audit_crosscheck.js");
const {check,rat,parse,str,add,sub,mul,div,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_syndrome_dilation.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m),mod=(x,q)=>(x%q+q)%q;
const dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),num=x=>Number(x[0])/Number(x[1]);
function* words(q,n,p=[]){if(p.length===n){yield p;return;}for(let t=0;t<q;t++)yield*words(q,n,[...p,t]);}
function approximate(K,v){const c=K.encode(v).slice().reverse();return c.reduce((s,x,j)=>s+num(parse(x))*Math.cos(2*Math.PI*j/K.q),0);}
const close=(a,b,m)=>check(Number.isFinite(a)&&Math.abs(a-b)<1e-9,m);
function control(C){
  const B=C.native_source_reference;S.control(B);
  check(B.spectral_filter_controls.length===1&&B.spectral_filter_controls[0].filter.degree===1,"actual raw Gram moment");
  const raw=B.original_records,q=raw[0].modulus,n=raw[0].label.length,M=raw.length/2,D=B.word_dimension,N=q**n,rows=B.actual_native_word_rows,K=E.field(q),space=[...words(q,n)];
  check(D*N<=8192&&N<=81&&C.joint_word_syndrome_dimension===D*N&&C.expanded_ground_rank===N&&C.exact_unnormalized_Hamiltonian_gap==="1"&&C.exact_Hamiltonian_norm===M&&C.exact_norm1_Hamiltonian_gap===str(rat(1n,BigInt(M))),"joint dimension, exact spectrum gap and norm");
  check(C.dense_joint_Hamiltonian_or_joint_projector_allocated===false&&C.physical_gate_and_precision_certificates_supplied===false,"finite reference not physical certificate");
  const T=C.truth_ONLY_FOR_SOURCE_SWEEP_CALIBRATION,secret=T.masked_secret,errors=T.original_errors;
  check(secret.length===n&&errors.length===2*M,"whole source calibration only");
  raw.forEach((r,j)=>check(mod(r.value+dot(r.label,B.known_mask)-dot(r.label,secret)-errors[j],q)===0,"original calibration equation"));
  const err=rows.map(r=>mod(r.word.reduce((s,t,j)=>s+[[1,0],[-1,1],[0,-1]][t][0]*errors[2*j]+[[1,0],[-1,1],[0,-1]][t][1]*errors[2*j+1],0),q));
  rows.forEach((r,j)=>check(mod(err[j]+dot(r.frequency,secret),q)===r.known_phase,"actual source word phases"));
  const overlap=space.map(h=>{
    let amplitude=K.F();rows.forEach((row,j)=>amplitude=K.plus(amplitude,K.scale(K.powers[mod(err[j]+dot(h,row.frequency),q)],rat(1n,BigInt(D)))));
    return K.times(amplitude,K.conj(amplitude));
  });
  const key=v=>JSON.stringify(v),indices=new Map(space.map((v,j)=>[key(v),j]));
  let mean=K.F();overlap.forEach(v=>mean=K.plus(mean,K.scale(v,rat(1n,BigInt(N)))));
  same(K.encode(mean),B.spectral_filter_controls[0].exact_source_acceptance_root_polynomial,"exact whole uniform-secret twirl equals raw Gram, not conditional normalization");
  const sector=Array.from({length:n},(_,j)=>mod(raw.reduce((s,r)=>s+r.label[j],0),q)),other=[mod(sector[0]+1,q),...sector.slice(1)],i=indices.get(key(sector)),j=indices.get(key(other));
  const kinds=["ZERO_COMPUTATIONAL","PUBLIC_FOURIER_SECTOR","PUBLIC_TWO_FOURIER_SECTORS"];
  check(C.public_ancilla_experiments.length===3,"all public ancillas");
  const counts=new Map();rows.forEach(r=>counts.set(key(r.frequency),(counts.get(key(r.frequency))||0)+1));
  let witness=null;
  outer:for(let u=0;u<D;u++)for(let v=0;v<D;v++){
    const a=rows[u].frequency,b=rows[v].frequency,ca=counts.get(key(a)),cb=counts.get(key(b));
    if(ca!==cb){witness={word_indices:[u,v],commutator_root_of_unity_prefactor:str(rat(BigInt(ca-cb),BigInt(D*D))),commutator_phase_exponent:mod(dot(sector,a.map((x,j)=>x-b[j])),q),nonzero_entry_certified_from_counts_and_root_of_unity:true};break outer;}
  }
  C.public_ancilla_experiments.forEach((F,k)=>{
    check(F.ancilla_kind===kinds[k],"declared public source-independent work preparation");
    const weights=space.map((_,t)=>k===0?rat(1n,BigInt(N)):k===1?rat(BigInt(t===i)):rat(BigInt(t===i||t===j),2n));
    same(F.exact_syndrome_Fourier_weights,weights.map(str),"public work Fourier diagonals from labels only");same(F.public_sector_parameters,k===0?[]:k===1?[sector]:[sector,other],"public sector coordinates");
    let actual=K.F();weights.forEach((p,t)=>{const h=secret.map((x,j)=>mod(x-space[t][j],q));actual=K.plus(actual,K.scale(overlap[indices.get(key(h))],p));});
    same(F.exact_original_data_ground_probability_root_polynomial,K.encode(actual),"exact original-data compressed ground probability");
    same(F.exact_uniform_secret_mean_root_polynomial,K.encode(mean),"same exact mean for every label-only ancilla");
    check(F.exact_IID_uniform_original_value_null_ground_probability===str(rat(1n,BigInt(D))),"null trace(E)=1");
    close(F.diagnostic_ground_probability,approximate(K,actual),"literal ground probability diagnostic matches exact overlap");
    close(F.diagnostic_uniform_secret_mean,approximate(K,mean),"whole source-family mean");
    check(F.complete_uniform_secret_sweep_ground_probabilities.length===N,"complete, not lucky-sector source sweep");
    space.forEach((s,u)=>{let expected=K.F();weights.forEach((p,t)=>{const h=s.map((x,j)=>mod(x-space[t][j],q));expected=K.plus(expected,K.scale(overlap[indices.get(key(h))],p));});close(F.complete_uniform_secret_sweep_ground_probabilities[u],approximate(K,expected),"every secret ground overlap");});
    same(F.exact_noncommutation_witness,k===1?witness:null,"exact noncommuting raw-Gram word entry");
    check(Number.isFinite(F.diagnostic_compressed_effect_commutator_norm)&&F.diagnostic_compressed_effect_commutator_norm>=0,"finite diagnostic norm");
    if(k===1&&witness)check(F.diagnostic_compressed_effect_commutator_norm>0,"noncommuting witness not denied");
    close(F.diagnostic_entire_readout_mass,1,"full measured readout keeps failures");
    check(F.diagnostic_ground_Hamiltonian_residual>=0&&F.diagnostic_ground_Hamiltonian_residual<1e-9&&F.diagnostic_complete_measured_law_max_error_against_classical>=0&&F.diagnostic_complete_measured_law_max_error_against_classical<1e-9,"bounded literal ground/readout diagnostics");
    check(F.original_responses_enter_ancilla_preparation===false&&F.normalized_fibre_access_supplied===false&&F.all_failure_readout_mass_kept===true,"source access and mass");
    const P=F.known_rank_one_driver_interpolation;
    same(P.minimum_active_two_dimensional_gap_squared_root_polynomial,K.encode(actual),"specific adiabatic active minimum gap squared is source overlap");
    close(P.diagnostic_minimum_active_gap,Math.sqrt(Math.max(0,approximate(K,actual))),"active gap diagnostic only");
    check(P.path==="(1-lambda)*(I-|initial><initial|)+lambda*(I-P_ground)"&&P.minimum_active_gap_location==="1/2"&&P.other_target_ground_directions===N-1&&P.other_target_ground_directions_energy==="1-lambda"&&P.full_lowest_level_gap_is_same_as_active_gap===false&&P.constant_endpoint_band_gap_removes_this_path_bottleneck===false&&P.general_different_driver_or_path_lower_bound_claimed===false,"specific rank-one path, not general adiabatic no-go");
  });
  return {words:D,sectors:N,noncommuting:witness!==null};
}
function sqrtFloor(N){if(N<2n)return N;let x=1n<<BigInt(Math.ceil(N.toString(2).length/2));while(true){const y=(x+N/x)/2n;if(y>=x)return x;x=y;}}
function ledger(L){
  const n=L.dimension,r=L.root_digits,s=L.word_surplus;[n,r,s].forEach(x=>check(Number.isSafeInteger(x)&&x>0,"positive scoped population"));check(n*r<=16384&&s<=128,"whole bit scope");
  const M=n*r+s,factor=add(one,rat(1n,3n**BigInt(s))),primitive=div(factor,sub(one,rat(1n,3n**BigInt(n)))),target=parse(L.target_mean_amplified_ground_mass);
  check(cmp(target,zero)>0n&&cmp(target,one)<=0n,"desired ground mass");const squared=div(mul(target,rat(3n**BigInt(n*r))),factor);
  let d=sqrtFloor(squared[0]/squared[1]);if(d*d*squared[1]<squared[0])d++;
  check(L.word_sites===M&&L.syndrome_ancilla_trits===n*r&&L.exact_unnormalized_Hamiltonian_gap==="1"&&L.exact_Hamiltonian_norm===M&&L.exact_norm1_Hamiltonian_gap===str(rat(1n,BigInt(M))),"norm and positive gap are distinct");
  check(L.word_preparation_uniform_qutrits===M&&L.known_response_phase_gates===M&&L.known_rank_one_initial_reflection_response_phase_gates===2*M&&L.coherent_ground_test_word_Fourier_gates===2*M&&L.forward_and_inverse_conditioned_label_shift_terms_upper===6*M*n,"paid actual logical primitives");
  same(L.uniform_secret_mean_ground_acceptance_upper,{coefficient:str(factor),base:3,exponent:-n*r},"uniform population overlap bound");
  same(L.uniform_primitive_secret_mean_ground_acceptance_upper,{coefficient:str(primitive),base:3,exponent:-n*r},"nonnegative primitive conditioning, not loose additive TV");
  check(BigInt(L.necessary_standard_amplification_iterations_lower_FULL_uniform_secret)===d/2n,"standard amplification price only on full-uniform source");
  ["arbitrary_label_only_pure_or_mixed_syndrome_ancillas_covered","fixed_or_label_only_mask_AND_errors_independent_of_secret_required","IID_full_root_original_labels_required_only_for_population_collision_bound","uniform_original_value_null_IID_required","noncommuting_effects_possible_but_not_sufficient_for_advantage","response_dependent_masks_or_work_preprocessing_excluded_by_this_bound","inverse_for_arbitrary_mixed_ancilla_preparation_is_not_granted"].forEach(k=>check(L[k]===true,"scope gate "+k));
  ["per_secret_success_upper_or_universal_quantum_lower_bound_claimed","scalable_quantum_speedup_supplied"].forEach(k=>check(L[k]===false,"no overbroad claim "+k));
}
function counter(C){
  const raw=C.original_records,q=raw[0].modulus;check(q===9&&raw.length===8&&raw.every(r=>r.label.length===1&&r.modulus===q),"same-source scalar noiseless countercontrol");
  let selected=raw.findIndex(r=>r.label[0]%3!==0);check(selected>=0,"public unit basis exists");
  const a=raw[selected].label[0];let inv=1;while(mod(inv*a,q)!==1)inv++;
  const decoded=mod(inv*raw[selected].value,q);check(raw.every(r=>mod(r.label[0]*decoded-r.value,q)===0),"public original equations, no truth used");
  same(C.public_noiseless_decoder,{candidate_secret:[decoded],public_label_rank_calls:selected+1,public_ring_inverse_calls:1,original_equations_checked:8,truth_supplied_to_decoder:false},"paid public one-variable unit-basis solve");
  same(C.original_response_dependent_known_mask,[mod(-decoded,q)],"response-dependent phase correction");same(C.label_only_work_ancilla_sector,[0],"public work sector remains label-only");
  close(C.diagnostic_ground_probability_after_paid_classical_mask,1,"masked noiseless uniform words lie in public zero-sector ground");
  check(C.word_phase_preparation_is_uniform_AFTER_paid_classical_mask===true&&C.general_label_only_ancilla_average_bound_with_response_adaptive_mask_applies===false&&C.zero_computational_work_raw_Gram_mask_invariance_is_not_falsified===true&&C.noiseless_control_is_a_hard_source_or_quantum_speedup===false,"mask scope counterexample not new algorithm");
}
function verify(R){
  check(R.status==="CONSTRUCTIVE_CONSTANT_GAP_SYNDROME_DILATION_NONCOMMUTING_EFFECTS_NO_OVERLAP_GAIN"&&R.producer_sha256===hash(path.join(ROOT,"theorems/native_syndrome_dilation.py"))&&R.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_SYNDROME_DILATION.md")),"current constructive model");
  const deps=["native_word_spectral_filter_audit.py","native_word_span_decision.py","native_basis_lottery.py","native_full_root_slice.py","native_small_multiple_completion.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"scientific dependencies");deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.actual_source_controls.length===4&&R.scaling_dilation_ledgers.length===4,"all declared original controls and populations");
  const stats=R.actual_source_controls.map(control);R.scaling_dilation_ledgers.forEach(ledger);counter(R.response_adaptive_mask_countercontrol);
  check(R.matched_classical_readout==="measure public work Fourier sector first, then sample independent original-data one-qutrit F3 outputs; all word and sector outcomes retained"&&R.certified_finite_precision_classical_sampler_implemented_here===false&&R.coherent_amplification_or_noncommuting_work_interleaving_classically_simulated===false&&R.accepted_speedup_candidate===false&&R.new_active_negative_result_created===false&&R.research_decision==="GAP_AND_NONCOMMUTATION_ARE_NOT_ENOUGH_CHARGE_SOURCE_OVERLAP_AND_MEASURED_CLASSICAL_SECTOR_CLOSURE","matched measured-only law, no general dequantization or speedup");
  return {verified:true,actual_native_word_rows:stats.reduce((s,x)=>s+x.words,0),public_ancilla_experiments:12,exact_noncommutation_witnesses:stats.filter(x=>x.noncommuting).length,complete_secret_sweeps:12,scaling_access_ledgers:4,efficient_receiver_supplied:false};
}
module.exports={verify,control,ledger,counter};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js"),S=require("./native_word_spectral_filter_audit_crosscheck.js");
const {check,rat,parse,str,add,sub,mul,div,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_word_collision_symmetry.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m),mod=(x,q)=>(x%q+q)%q;
const min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b;
function control(C){
  const B=C.native_spectral_reference;S.control(B);
  check(B.spectral_filter_controls.length===1&&B.spectral_filter_controls[0].filter.family==="GEOMETRIC"&&B.spectral_filter_controls[0].filter.degree===1,"actual raw moment");
  const D=B.word_dimension,q=B.original_records[0].modulus,M=B.original_records.length/2,n=B.original_records[0].label.length,K=E.field(q),collision=parse(B.collision_probability);
  const raw=K.decode(B.spectral_filter_controls[0].exact_source_acceptance_root_polynomial),half=rat(1n,2n);
  same(C.exact_equal_plus_root_polynomial,K.encode(K.plus(K.scale(K.unit,mul(collision,half)),K.scale(raw,half))),"exact symmetric collision law");
  same(C.exact_equal_minus_root_polynomial,K.encode(K.plus(K.scale(K.unit,mul(collision,half)),K.scale(raw,rat(-1n,2n)))),"exact antisymmetric collision law");
  check(C.exact_equal_total_probability===str(collision)&&C.IID_null_equal_plus_probability===str(mul(add(collision,rat(1n,BigInt(D))),half))&&C.IID_null_equal_minus_probability===str(mul(sub(collision,rat(1n,BigInt(D))),half)),"all collision mass and IID null");
  check(C.effective_original_word_effect_commutes_with_raw_Gram===true&&C.phase_independent_diagonal_term_cancels_source_vs_IID_null===true,"joint SWAP does not yield an escaping noncommuting effective word observable");
  const mass={equal_plus:0,equal_minus:0,unequal_plus:0,unequal_minus:0};
  B.actual_native_word_rows.forEach(a=>B.actual_native_word_rows.forEach(b=>{
    const eq=JSON.stringify(a.frequency)===JSON.stringify(b.frequency),v=Math.cos(2*Math.PI*(a.known_phase-b.known_phase)/q);
    mass[eq?"equal_plus":"unequal_plus"]+=(1+v)/(2*D*D);mass[eq?"equal_minus":"unequal_minus"]+=(1-v)/(2*D*D);
  }));
  const actual=C.literal_joint_branches;Object.entries(mass).forEach(([k,v])=>check(Number.isFinite(actual[k])&&Math.abs(actual[k]-v)<1e-9,"full classical measured-word/flag branch law "+k));
  check(Math.abs(actual.complete_mass-1)<1e-9&&actual.whole_joint_amplitudes_evaluated===2*D*D&&actual.branch_discarded_for_free===false,"no dropped failure mass");
  same(C.classical_full_measured_readout_identity,{word_pair_probability:str(rat(1n,BigInt(D*D))),conditional_plus_probability:"(1+cos(2*pi*(phase_w-phase_v)/q))/2",conditional_minus_probability:"(1-cos(2*pi*(phase_w-phase_v)/q))/2",predicate:"f_A(w)==f_A(v)",original_phase_evaluator_and_frequency_work_paid:true,entire_measured_word_pair_and_flag_law_matched:true,finite_precision_classical_sampler_implemented_here:false,coherent_amplification_or_retained_unmeasured_output_simulated:false},"measured-only classical identity with finite-coin debt");
  same(C.scalable_logical_recipe,{original_records_paid_once:2*M,uniform_qutrits:2*M,original_response_phase_gates:M,controlled_qutrit_swaps:M,forward_and_uncompute_label_coordinate_accumulations:4*M*n,frequency_comparison_coordinates:n,known_initial_preparation_inverse_available_on_this_source:true,normalized_fibre_preparation_required_by_one_pass:false,full_word_table_required_by_logical_recipe:false,physical_gate_compilation_and_precision_certified:false},"paid logical primitives, not hardware certificate");
  check(C.accepted_speedup_candidate===false,"not a new speedup");return 2*D*D;
}
function sqrtFloor(N){if(N<2n)return N;let x=1n<<BigInt(Math.ceil(N.toString(2).length/2));while(true){const y=(x+N/x)/2n;if(y>=x)return x;x=y;}}
function ledger(L){
  const n=L.dimension,r=L.root_digits,s=L.word_surplus;[n,r,s].forEach(v=>check(Number.isSafeInteger(v)&&v>0,"positive original scope"));check(n*r<=4096,"conditional bit cap");
  const N=3n**BigInt(n*r),D=3n**BigInt(n*r+s),M=n*r+s,V=parse(L.true_original_error_second_moment_over_q_squared_upper),target=parse(L.target_mean_amplified_equality_probability);
  check(cmp(V,zero)>=0n&&cmp(target,zero)>0n&&cmp(target,one)<=0n,"true moment and target mass");
  const den=add(one,rat(N-1n,D)),mean=div(den,rat(N)),loss=min(one,mul(rat(BigInt(80*M)),V));
  const source=min(rat(1n,2n),div(loss,mul(rat(2n),den))),nullAnti=div(sub(one,rat(1n,D)),mul(rat(2n),den)),squared=div(target,mean);
  let d=sqrtFloor(squared[0]/squared[1]);if(d*d*squared[1]<squared[0])d++;
  check(L.word_sites===M&&L.mean_equality_probability===str(mean)&&L.conditional_IID_null_antisymmetric_probability===str(nullAnti)&&L.conditional_source_antisymmetric_probability_upper===str(source)&&L.conditional_antisymmetric_gap_lower===str(max(zero,sub(nullAnti,source)))&&BigInt(L.necessary_standard_amplification_iterations_lower)===d/2n,"unamplified ensemble signal AND amplification price");
  ["original_errors_independent_of_full_root_original_labels_required","IID_uniform_full_root_original_labels_and_IID_uniform_null_values_required","conditional_bounds_are_unamplified_source_and_branch_ensemble_bounds"].forEach(k=>check(L[k]===true,"required premise "+k));
  ["amplified_ensemble_source_gap_certified","generic_trace_error_safe_after_rare_branch_conditioning","arbitrary_nonstandard_quantum_algorithm_lower_bound"].forEach(k=>check(L[k]===false,"scope not extended "+k));
}
function census(C,dependent){
  let totalC=zero,totalR=zero,totalF=zero;
  const cos=x=>mod(x,3)===0?one:rat(-1n,2n),beta=[];
  for(let t=0;t<3;t++)for(let u=0;u<3;u++)beta.push([...[[1,0],[-1,1],[0,-1]][t],...[[1,0],[-1,1],[0,-1]][u]]);
  for(let code=0;code<81;code++){
    let v=code;const A=[];for(let j=0;j<4;j++){A.push(v%3);v=Math.floor(v/3);}
    const errors=dependent?A.map(a=>-a):[1,0,0,0],values=A.map((a,j)=>mod(a+errors[j],3));
    const dot=(b,x)=>b.reduce((s,c,j)=>s+c*x[j],0),freq=beta.map(b=>mod(dot(b,A),3)),phase=beta.map(b=>mod(dot(b,values),3)),err=beta.map(b=>mod(dot(b,errors),3));
    for(let i=0;i<9;i++)for(let j=0;j<9;j++){totalF=add(totalF,div(cos(err[j]-err[i]),rat(81n)));if(freq[i]===freq[j]){totalC=add(totalC,rat(1n,81n));totalR=add(totalR,div(cos(phase[j]-phase[i]),rat(81n)));}}
  }
  const c=div(totalC,rat(81n)),r=div(totalR,rat(81n)),f=div(totalF,rat(81n)),lhs=sub(c,r),rhs=div(sub(one,f),rat(3n));
  same(C,{complete_original_label_banks:81,words_per_bank:9,original_secret_USED_ONLY_TO_GENERATE_CONTROL:1,original_error_recipe:dependent?"e_i=-a_i":"(1,0,0,0)",errors_independent_of_labels:!dependent,exact_mean_collision:str(c),exact_mean_raw_acceptance:str(r),exact_mean_error_fidelity:str(f),exact_mean_C_minus_R:str(lhs),one_over_N_times_mean_one_minus_error_fidelity:str(rhs),independent_error_averaging_identity_holds:cmp(lhs,rhs)===0n,is_hard_source_or_algorithm_candidate:false},"complete label-error census");
}
function verify(R){
  check(R.status==="ACTUAL_TWO_WORD_COLLISION_SYMMETRY_REFERENCE_MEASURED_LAW_CLASSICAL_RARE_BRANCH_PAID"&&R.producer_sha256===hash(path.join(ROOT,"theorems/native_word_collision_symmetry.py"))&&R.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_WORD_COLLISION_SYMMETRY.md")),"current constructive reference");
  const deps=["native_word_spectral_filter_audit.py","native_word_span_decision.py","native_full_root_slice.py","native_small_multiple_completion.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"direct dependencies");deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.actual_source_controls.length===4&&R.scaling_ensemble_ledgers.length===3,"declared control coverage");
  const amplitudes=R.actual_source_controls.reduce((sum,c)=>sum+control(c),0);R.scaling_ensemble_ledgers.forEach(ledger);census(R.independent_error_label_census,false);census(R.label_dependent_error_countercensus,true);
  check(R.accepted_speedup_candidate===false&&R.new_active_negative_result_created===false&&R.research_decision==="KEEP_AS_CONSTRUCTIVE_COLLECTIVE_BASELINE_NOT_A_NEW_SPEEDUP_OR_FREE_FIBRE_NORMALIZER","no unproved speedup or universal negative");
  return {verified:true,actual_joint_amplitudes_replayed:amplitudes,complete_label_error_censuses:2,conditional_ledgers:3,efficient_quantum_algorithm_supplied:false};
}
module.exports={verify,control,ledger,census};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

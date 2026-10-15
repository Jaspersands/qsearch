"use strict";
// Exact mathematical ledger replay; not hardware or generic circuit verification.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js");
const {check,rat,parse,str,add,sub,mul,div,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/lattice_qft_precision.json");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m),hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b,abs=a=>a[0]<0n?[-a[0],a[1]]:a;
function integer(x){check(typeof x==="string"||Number.isSafeInteger(x),"exact certificate integer");const n=BigInt(x);check(n>=0n,"nonnegative integer");return n;}
const jsonInt=x=>x<=9007199254740991n?Number(x):String(x);
function machin(N){
  function atan(k){let sum=zero,power=rat(1n,BigInt(k)),square=rat(1n,BigInt(k*k));
    for(let j=0;j<N;j++){const term=div(power,rat(BigInt(2*j+1)));sum=add(sum,j%2?[-term[0],term[1]]:term);power=mul(power,square);}
    const next=div(power,rat(BigInt(2*N+1))),end=add(sum,N%2?[-next[0],next[1]]:next);return [min(sum,end),max(sum,end)];
  }
  const a=atan(5),b=atan(239);return [sub(mul(rat(16n),a[0]),mul(rat(4n),b[1])),sub(mul(rat(16n),a[1]),mul(rat(4n),b[0]))];
}
function verifyPlan(P){
  const ell=P.QFT_wires,b=P.retained_maximum_separation;
  check(Number.isSafeInteger(ell)&&ell>=1&&ell<=1000000&&Number.isSafeInteger(b)&&b>=0&&b<ell&&b<=4096,"bounded plan representation");
  const use=P.query_usage,F=integer(use.direct_forward_calls),I=integer(use.direct_inverse_calls),R=integer(use.phase_parent_reflections),T=F+I+2n*R;
  check(T>0n&&integer(use.total_approximate_QFT_or_inverse_calls)===T&&use.receiver_usage_bound_is_external_not_proved_here===true,"inverse and reflection calls included");
  const target=parse(P.target_complete_experiment_trace_error);check(cmp(target,zero)>0n&&cmp(target,one)<=0n,"exact positive target");
  const retained=BigInt(b)*BigInt(ell)-BigInt(b*(b+1)/2),full=BigInt(ell)*BigInt(ell-1)/2n;
  const keptWeight=add(rat(BigInt(ell-2)),rat(BigInt(b+2-ell),2n**BigInt(b)));
  const [piLo,piHi]=machin(16),base=rat(884279719003555n,281474976710656n);
  const piError=max(abs(sub(base,piLo)),abs(sub(base,piHi)));
  let trunc;
  if(b===ell-1)trunc=zero;
  else if(ell<=4096)trunc=min(rat(2n),mul(piHi,add(rat(BigInt(ell-b-2),2n**BigInt(b)),rat(1n,2n**BigInt(ell-1)))));
  else trunc=min(rat(2n),rat(BigInt(4*(ell-b-1)),2n**BigInt(b)));
  const supported=b<=1022,angle=mul(piError,keptWeight),encodedSingle=min(rat(2n),add(trunc,angle));
  const logical=min(one,mul(rat(T),trunc)),encoded=supported?min(one,mul(rat(T),encodedSingle)):null;
  const gates=BigInt(ell)+retained+BigInt(Math.floor(ell/2));
  const eta=P.external_per_logical_gate_operator_error===null?null:parse(P.external_per_logical_gate_operator_error);
  if(eta!==null)check(cmp(eta,zero)>=0n,"external error is nonnegative but not proved");
  const conditional=eta===null||!supported?null:min(one,mul(rat(T),add(encodedSingle,mul(rat(gates),eta))));
  same(P,{QFT_wires:ell,retained_maximum_separation:b,qiskit_approximation_degree:ell-1-b,
    query_usage:{direct_forward_calls:jsonInt(F),direct_inverse_calls:jsonInt(I),phase_parent_reflections:jsonInt(R),total_approximate_QFT_or_inverse_calls:jsonInt(T),receiver_usage_bound_is_external_not_proved_here:true},
    target_complete_experiment_trace_error:str(target),logical_controlled_phases_retained:jsonInt(retained),logical_controlled_phases_omitted:jsonInt(full-retained),
    logical_H_gates:ell,logical_swaps:Math.floor(ell/2),exact_ideal_QFT_selected:b===ell-1,
    retained_dyadic_angle_weight:str(keptWeight),omitted_weight_symbolic:{coefficient_at_2_pow_minus_cutoff:ell-b-2,cutoff_exponent:b,unit_term_exponent:ell-1},
    single_use_ideal_truncation_operator_upper:str(trunc),truncation_bound_method:ell<=4096?"EXACT_FINITE_TAIL_MACHIN_PI_UPPER":"SYMBOLIC_TAIL_4_TIMES_REMAINING_SPAN",
    Machin_terms:16,pi_rational_lower:str(piLo),pi_rational_upper:str(piHi),exact_encoded_binary64_pi:str(base),
    single_use_encoded_CP_parameter_operator_error_upper:supported?str(angle):null,
    single_use_encoded_QFT_operator_error_upper:supported?str(encodedSingle):null,
    complete_experiment_ideal_truncation_trace_upper:str(logical),complete_experiment_encoded_QFT_trace_upper:supported?str(encoded):null,
    ideal_truncation_target_met:cmp(logical,target)<=0n,encoded_QFT_parameter_target_met:supported&&cmp(encoded,target)<=0n,
    numeric_normal_angle_encoding_supported:supported,external_per_logical_gate_operator_error:eta===null?null:str(eta),
    complete_experiment_upper_IF_external_gate_bound_holds:conditional===null?null:str(conditional),
    arithmetic_preparation_and_hardware_errors_covered:false,statevector_MPS_roundoff_certified:false,
    normalized_rare_branch_accuracy_certified_without_mass_bound:false,logical_query_budget_proves_efficient_receiver:false},"independent precision/query/encoded-angle ledger");
  return {ell,b,T,trunc,encodedSingle};
}
function checkLargeSource(C){
  const P=C.QFT_precision_plan,{ell,b}=verifyPlan(P),S=C.clean_evaluator.public_source;
  check(ell===264&&b===25&&S.basis_rows.length===8&&S.box===2**32&&S.cube_width===2&&S.prime===3,"declared growing resource-only source");
  const n=8,boxBits=32,out=265,w=35,input=257,work=71;
  // Independent enumeration of constant bit patterns, not producer's closed popcount formula.
  let calls=0,pops=0;
  const mask=(1n<<35n)-1n,term=x=>{x&=mask;if(x){calls++;pops+=x.toString(2).split("1").length-1;}};
  for(let i=0;i<n;i++){
    for(let j=0;j<n;j++)for(let h=0;h<boxBits;h++)term(BigInt((i===j?1:0)*(j===0?3:1))*(1n<<BigInt(h)));
    term(BigInt(i===0?1:0));term(-1n);
  }
  const A=C.clean_evaluator;
  check(A.input_qubits===input&&A.cell_output_qubits===out&&A.shared_arithmetic_workspace_qubits===work&&A.compiled_qubits===593,"all source register wires charged");
  check(A.constant_additions_including_uncompute===2*calls&&A.logical_instruction_count===4*pops+2*calls+out,"enumerated signed constant/addition resource counts");
  same(S.basis_rows,Array.from({length:8},(_,i)=>Array.from({length:8},(_,j)=>Number(i===j))),"classically easy identity basis only for resource validation");
  check(integer(S.input_population)===(2n<<256n)&&integer(S.phase_modulus)===(1n<<264n),"exact huge populations never a dense table");
  check(C.compiled_phase_parent_qubits===601&&C.position_qubits===264&&C.zero_padding_qubits===8,"actual beyond128 position compiler");
  check(C.logical_QFT_controlled_phase_gates===6275&&C.logical_QFT_H_gates===264&&C.logical_QFT_swap_gates===132,"actual sparse QFT gate resources");
  same(C.QFT_usage_ledger,{charged_forward_calls:0,charged_inverse_calls:0,charged_parent_reflections:0,charged_total_QFT_or_inverse_calls:0,manual_untracked_circuit_calls_are_outside_accuracy_contract:true},"compiled is not executed");
  check(C.original_position_wires_reused_in_place===true&&C.copied_original_position_garbage_retained===false&&C.hidden_shift_or_preimages_enter_compiler===false&&C.hardware_or_fault_tolerant_QFT_precision_certified===false,"source access and physical scope");
}
function verify(R){
  check(R.status==="LATTICE_QFT_PRECISION_QUERY_AND_POSTSELECTION_DEBT_REVIEW_PENDING","review-pending status");
  [["producer_sha256","theorems/lattice_qft_precision.py"],["derivation_sha256","research/LATTICE_QFT_PRECISION.md"],["contract_sha256","research/hypotheses/lattice_qft_precision_contract.json"]].forEach(([k,f])=>check(R[k]===hash(path.join(ROOT,f)),"provenance "+k));
  const deps=["ternary_flat_character_certificate.py","ternary_measured_lattice_decoder.py","lattice_cube_source_circuit.py","lattice_cube_dcp_readout.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.scaling_precision_profiles.length===4&&R.actual_synthesis_controls.length===4,"declared complete controls");
  R.scaling_precision_profiles.forEach(P=>{
    const q=verifyPlan(P),target=parse(P.target_complete_experiment_trace_error),x=div(rat(8n*BigInt(q.ell)*q.T),target);
    let b=0;while(cmp(rat(1n<<BigInt(b)),x)<0n)b++;
    check(q.b===Math.min(q.ell-1,b),"automatic exact integer cutoff selection");
  });
  R.actual_synthesis_controls.forEach(C=>{
    const q=verifyPlan(C.plan),counts={h:q.ell};if(q.b)counts.cp=q.b*q.ell-q.b*(q.b+1)/2;if(q.ell>1)counts.swap=Math.floor(q.ell/2);
    same(C.actual_synthesized_gate_counts,counts,"actual library count mapping");
    check(Number.isFinite(C.numerical_dense_operator_difference)&&C.numerical_dense_operator_difference>=0&&C.numerical_dense_operator_difference<=Number(q.encodedSingle[0])/Number(q.encodedSingle[1])+1e-12&&C.numerical_check_is_a_formal_gate_error_certificate===false,"finite operator diagnostic not generic proof");
  });
  check(R.rare_postselection_countercontrols.length===3,"three rare-event counterexamples");
  R.rare_postselection_countercontrols.forEach((C,i)=>{const k=[8,32,128][i],p=str(rat(1n,1n<<BigInt(k)));
    same(C,{success_mass:p,complete_accept_reject_trace_distance:p,normalized_accepted_payload_trace_distance:"1",free_conditional_accuracy_inference_valid:false},"rare payload can be completely wrong");});
  checkLargeSource(R.actual_beyond_old_128_wire_compile);
  check(R.large_control_is_resource_only_classically_easy_not_a_DCP_promise===true,"no hard-source claim from resources");
  ["hardware_or_full_source_channel_error_certified","efficient_receiver_supplied","accepted_speedup_candidate","new_active_negative_result_created","novelty_claim"].forEach(k=>check(R[k]===false,"no unproved result "+k));
  return {verified:true,scaling_profiles:4,actual_QFT_synthesis_controls:4,compiled_position_wires:264,verifies_math_ledgers_not_generic_hardware_or_source_correctness:true,accepted_speedup_candidate:false};
}
module.exports={verify,verifyPlan,machin};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));

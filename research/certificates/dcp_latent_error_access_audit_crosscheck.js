#!/usr/bin/env node
"use strict";
// Independent rational arithmetic in Q[z]/(z^2+u*z+1), u=1(q3),0(q4).
const fs=require("fs"),path=require("path");
function need(v,m){if(!v)throw new Error(m);}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function gcd(a,b){for(;b;){const c=a%b;a=b;b=c;}return a<0n?-a:a;}
function Q(a,b=1n){need(b>0n,"positive rational denominator");const g=gcd(a,b);return[a/g,b/g];}
function read(s){const[a,b="1"]=String(s).split("/");return Q(BigInt(a),BigInt(b));}
function plus(a,b){return Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function times(a,b){return Q(a[0]*b[0],a[1]*b[1]);}
function neg(a){return[-a[0],a[1]];}
function equal(a,b){return a[0]*b[1]===a[1]*b[0];}
function R(a=0n,b=0n){return[Q(a),Q(b)];}
function radd(a,b){return[plus(a[0],b[0]),plus(a[1],b[1])];}
function rneg(a){return[neg(a[0]),neg(a[1])];}
function rscale(a,c){return[times(a[0],c),times(a[1],c)];}
function rtimes(a,b,u){const bd=times(a[1],b[1]);return[plus(times(a[0],b[0]),neg(bd)),
  plus(plus(times(a[0],b[1]),times(a[1],b[0])),neg(times(Q(BigInt(u)),bd)))];}
function conj(a,u){return[plus(a[0],neg(times(Q(BigInt(u)),a[1]))),neg(a[1])];}
function req(a,b){return equal(a[0],b[0])&&equal(a[1],b[1]);}
function checkMatrix(record,M,message){need(record.length===M.length&&record.every((row,i)=>row.length===M[i].length&&
  row.every((v,j)=>v.length===2&&req(v.map(read),M[i][j]))),message);}
function perms(values){if(!values.length)return[[]];return values.flatMap((v,i)=>perms(values.filter((_,j)=>i!==j)).map(t=>[v,...t]));}
function determinant(M,u){let sum=R();for(const p of perms([0,1,2,3])){
  let term=R(1n),inversions=0;for(let i=0;i<4;i++){term=rtimes(term,M[i][p[i]],u);for(let j=i+1;j<4;j++)if(p[i]>p[j])inversions++;}
  sum=radd(sum,inversions%2?rneg(term):term);
}return sum;}
function checkSpan(C,q){
  const u=q===3?1:0,phases=[R(1n),R(0n,1n),R(BigInt(-u),-1n)],pairs=[[0,1],[1,0],[0,2],[1,2]];
  const vectors=pairs.map(([e,f])=>[R(1n),phases[f],phases[e],rtimes(phases[e],phases[f],u)].map(v=>rscale(v,Q(1n,2n))));
  const gram=vectors.map(v=>vectors.map(w=>v.reduce((sum,x,j)=>radd(sum,rtimes(x,conj(w[j],u),u)),R())));
  need(C.modulus===q&&same(C.possible_error_exponents,[0,1,q-1])&&same(C.unequal_error_index_pairs,pairs),"distinct unequal error family");
  checkMatrix(C.normalized_product_vectors_in_quadratic_field,vectors,"original product input vectors");
  checkMatrix(C.unequal_input_Gram_matrix_in_quadratic_field,gram,"independent exact Gram matrix");
  const det=determinant(gram,u),expected=q===3?Q(81n,256n):Q(1n,8n);
  need(equal(det[1],Q(0n))&&equal(det[0],expected)&&equal(read(C.Gram_determinant_exact_rational),expected)&&
       C.input_Hilbert_dimension===4&&C.unequal_input_span_dimension===4&&
       C.positive_effect_rejecting_all_unequal_inputs_must_be_zero===true&&C.general_quantum_purification_impossible===false,"span/access conclusion");
}
function checkCNOT(rows){
  need(rows.length===9,"physical branch coverage");const errors=[0,1,3],phases=[R(1n),R(0n,1n),R(0n,-1n)],u=0;
  rows.forEach((C,index)=>{
    const e=Math.floor(index/3),f=index%3,ze=phases[e],zf=phases[f];
    need(same(C.input_error_exponents,[errors[e],errors[f]])&&C.errors_equal===(e===f)&&C.branches.length===2,"input error calibration");
    // Actual CNOT permutation on amplitudes, not assumed convolution weights.
    const input=[R(1n),zf,ze,rtimes(ze,zf,u)].map(v=>rscale(v,Q(1n,2n))),output=[input[0],input[1],input[3],input[2]];
    C.branches.forEach((B,r)=>{
      const v=[output[r],output[r+2]],mass=v.reduce((s,a)=>radd(s,rtimes(a,conj(a,u),u)),R());
      need(equal(mass[1],Q(0n))&&equal(mass[0],Q(1n,2n)),"CNOT target measurement is equality-blind");
      const density=v.map(a=>v.map(b=>rscale(rtimes(a,conj(b,u),u),Q(2n))));
      need(B.measured_target_Z===r&&equal(read(B.Born_probability),Q(1n,2n))&&
           B.root_error_exponent_mod4===(errors[e]+(r===0?1:-1)*errors[f]+4)%4,"physical sum/difference labels");
      checkMatrix(B.root_density_quadratic_field,density,"actual conditional root density");
    });
  });
}
function checkClassical(C){
  const A=C.q4_p_half;
  need(equal(read(A.formal_latent_equality_probability),Q(3n,8n))&&
       same(A.formal_retained_error_kernel,{"0":"2/3","1":"1/6","3":"1/6"})&&
       same(A.CNOT_sum_error_kernel_IF_latent_equality_were_known,{"0":"2/3","1":"0","2":"1/3","3":"0"})&&
       equal(read(A.formal_retained_error_visibility),Q(2n,3n))&&
       equal(read(A.CNOT_sum_branch_visibility_given_magic_equality),Q(1n,3n))&&
       A.latent_error_equality_measurement_available===false,"classical retained vs physical doubled error");
  const B=C.q3_p_two_thirds;
  ["exact_input_visibility","exact_formal_pruned_visibility","leaf_SNR_exact","pruned_SNR_exact"].forEach(k=>need(equal(read(B[k]),Q(0n)),"exact critical zero signal"));
  need(B.strict_leaf_dominance===false&&C.endpoint_p_zero_or_one.strict_purifying_or_degrading===false&&
       equal(read(C.endpoint_p_zero_or_one.formal_retained_error_visibility_gain),Q(0n)),"strict endpoint claim counterexample");
}
function verify(RR){
  need(RR.contract_id==="phase_qubit_latent_error_equality_access_falsifier_v1"&&
       RR.status==="EXACT_ACCESS_FALSIFIERS_EXTERNAL_REVIEW_PENDING"&&RR.accepted_speedup_candidate===false&&RR.novelty_claim===false&&
       RR.external_theorem_review_complete===false&&RR.source_quantum_preparations_executed===0,"global admission");
  need(RR.unequal_input_span_controls.length===2,"span control coverage");RR.unequal_input_span_controls.forEach((C,i)=>checkSpan(C,[3,4][i]));
  checkCNOT(RR.physical_CNOT_Z_controls);checkClassical(RR.conditional_classical_vs_physical_controls);
  const A=RR.access_receipts;need(A.length===2&&A[0].access_model==="phase-qubits-only"&&A[0].possible_phase_errors===3&&
    A[0].status==="ZERO_FALSE_POSITIVE_EQUALITY_HERALD_HAS_ZERO_SUCCESS"&&A[0].latent_error_equality_available===false&&
    A[1].access_model==="orthogonal-error-register-supplied"&&A[1].possible_phase_errors===3&&
    A[1].status==="CONDITIONAL_EXTRA_SOURCE_ACCESS_NOT_CERTIFIED"&&
    A[1].latent_error_equality_available==="ONLY_IF_THE_EXTRA_REGISTER_IS_ACTUALLY_SUPPLIED"&&
    A.every(C=>C.full_product_error_support_assumed===true&&C.extra_source_access_proved===false&&C.accepted_speedup_candidate===false),"no latent-error oracle granted");
  need(RR.tensor_extension_q4.length===5,"tensor extension coverage");
  RR.tensor_extension_q4.forEach((C,i)=>{const k=[2,3,4,8,16][i];need(C.input_qubits===k&&C.non_all_equal_product_basis_dimension===2**k&&
    C.Gram_determinant_one_over_two_exponent===(3+2*(k-2))*2**(k-2)&&C.same_no_false_positive_all_equal_herald_obstruction===true,"tensor span certificate");});
  const s=RR.scope;
  ["comparison_goal_is_exact_hidden_error_equality","three_distinct_possible_phase_errors_required",
   "four_unequal_product_inputs_allowed_by_source_promise",
   "unknown_secret_may_be_fixed_to_zero_for_counterexample","original_hidden_error_labels_used_only_for_calibration"].forEach(k=>need(s[k]===true,"comparison premise"));
  ["false_positive_purification_protocols_excluded","orthogonal_error_register_or_encoded_redundancy_excluded",
   "ensemble_equivalent_false_positive_channels_excluded",
   "correlated_equal_error_source_promises_excluded",
   "all_noise_mitigation_or_quantum_algorithms_excluded","classical_conditional_kernel_identity_is_a_physical_instrument"].forEach(k=>need(s[k]===false,"overbroad no-go: "+k));
  need(RR.review_target==="research/DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT.md"&&
       same(RR.literature,["https://arxiv.org/abs/quant-ph/0202087"]),"review context");
  return{status:"ok",exact_Gram_determinants:["81/256","1/8"],physical_CNOT_inputs:9,general_purification_no_go:false};
}
module.exports={verify};
if(require.main===module){const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_latent_error_access_audit.json");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));}

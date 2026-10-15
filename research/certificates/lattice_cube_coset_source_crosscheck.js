"use strict";
// Exhaustive public-cell replay; no short-vector oracle or circuit certificate.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),{check,rat,str,add,sub,mul,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/lattice_cube_coset_source.json");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m);
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod=(x,q)=>(x%q+q)%q;
function* positions(M,n,p=[]){if(!n){yield p;return;}for(let x=0;x<M;x++)yield*positions(M,n-1,[...p,x]);}
function encode(a,M){return a.reduce((s,x,i)=>s+x*(2*M)**i,0);}

function audit(S) {
  const B=S.basis_rows,n=B.length,p=S.prime,m=S.residue_guess,i0=S.coordinate,M=S.box,W=S.cube_width,J=S.offsets;
  check(n===2&&B.every(r=>r.length===n)&&J.length===n,"two-dimensional complete replay scope");
  [p,m,i0,M,W,...B.flat(),...J].forEach(x=>check(Number.isSafeInteger(x),"exact safe public integers"));
  check(M>=2&&(M&(M-1))===0&&W>=2&&(W&(W-1))===0&&2*M**n<=200000,"dyadic source and full domain cap");
  check(p>=2&&m>0&&m<p&&i0>=0&&i0<n&&J.every(j=>j>=1&&j<=W),"public residue and offset scope");
  for(let d=2;d*d<=p;d++)check(p%d!==0,"public prime");
  check(B[0][0]*B[1][1]-B[0][1]*B[1][0]!==0,"full rank public basis");
  const D=2*M**n,N=(2*M)**n,fibres=new Map();
  for(let t=0;t<2;t++)for(const a of positions(M,n)) {
    const c=a.slice();c[i0]=p*a[i0]+t*m;
    const point=Array.from({length:n},(_,i)=>c.reduce((s,x,j)=>s+x*B[j][i],0));
    point.forEach(x=>check(Number.isSafeInteger(x),"no point arithmetic overflow"));
    const cell=point.map((x,i)=>Math.floor((x-J[i])/W)).join(",");
    if(!fibres.has(cell))fibres.set(cell,[]);
    fibres.get(cell).push([t,a]);
  }
  const sizes=new Map(),shifts=new Map(),bad=[0,0];let good=0,valid=true;
  for(const fibre of fibres.values()) {
    sizes.set(fibre.length,(sizes.get(fibre.length)||0)+1);
    if(fibre.length>2||new Set(fibre.map(([t])=>t)).size!==fibre.length)valid=false;
    if(fibre.length===2&&fibre[0][0]!==fibre[1][0]) {
      const a=fibre.find(([t])=>t===0)[1],b=fibre.find(([t])=>t===1)[1];
      const delta=b.map((x,i)=>x-a[i]),key=delta.join(",");
      if(!shifts.has(key))shifts.set(key,[delta,0]);
      shifts.get(key)[1]++;good++;
    } else if(fibre.length===1)bad[fibre[0][0]]++;
  }
  valid=valid&&shifts.size<=1;
  const publicSource={basis_rows:B,prime:p,residue_guess:m,coordinate:i0,box:M,cube_width:W,offsets:J,
    input_population:D,phase_modulus:N,explicit_cell_evaluator_available:true,
    uniform_hidden_shift_prior_assumed:false,uniform_secret_twirl_bounds_transferred_to_source:false,
    shortest_vector_or_shift_given_to_constructor:false,normalized_conditional_state_inverse_available:false,
    scalable_coherent_evaluator_circuit_compiled:false};
  same(S,publicSource,"public-only evaluator contract");
  const maxima=Array(n).fill(M-1);maxima[i0]=p*(M-1)+m;
  const shift=Math.log2(W), bitLength=x=>BigInt(x).toString(2).length;
  const coordinates=Array.from({length:n},(_,i)=>{
    const bound=B.reduce((s,row,j)=>s+Math.abs(row[i])*maxima[j],0)+W;
    const bits=Math.max(bitLength(bound)+1,shift+1);
    return {absolute_point_minus_offset_bound:bound,signed_point_workspace_bits:bits,
      low_remainder_bits_to_uncompute:shift,signed_cell_output_bits:bits-shift,
      strict_signed_range_certified:bound<2**(bits-1)};
  });
  const plan={initial_uniform_source_qubits:1+n*Math.log2(M),public_coefficient_maxima:maxima,
    position_embedding_padding_qubits:n,position_phase_register_qubits:n*(Math.log2(M)+1),
    coordinate_width_certificates:coordinates,classical_constant_multiply_accumulate_terms:n*n,
    signed_floor_implemented_by_high_bit_copy:true,physical_point_carry_remainder_workspace_must_return_zero:true,
    clean_reversible_arithmetic_gates_compiled:false};
  return {public_source:publicSource,clean_arithmetic_plan:plan,complete_original_domain_censused:D,measured_cell_count:fibres.size,
    fibre_size_histogram:[...sizes].sort((a,b)=>a[0]-b[0]).map(([k,v])=>({size:k,cells:v,Born_mass:str(rat(BigInt(k*v),BigInt(D)))})),
    PRIVATE_AUDIT_ONLY_common_differences:[...shifts.values()].sort((a,b)=>a[0][0]-b[0][0]||a[0][1]-b[0][1]).map(([delta,count])=>({difference:delta,cells:count,scalar_shift:mod(encode(delta,M),N)})),
    PRIVATE_AUDIT_ONLY_singleton_colour_counts:bad,good_two_point_cell_count:good,
    good_two_point_Born_mass:str(rat(BigInt(2*good),BigInt(D))),valid_two_point_source_on_full_domain:valid,
    bad_register_rate:valid?str(rat(BigInt(bad[0]+bad[1]),BigInt(D))):null,
    position_Fourier_label_uniformity_proved:valid,balanced_bad_basis_mixture_proved:valid&&bad[0]===bad[1],
    full_growing_family_reduction_promise_proved:false,
    reference_enumeration_is_scalable_quantum_source_circuit:false,multipoint_fibres_are_valid_bad_basis_registers:false};
}
function verify(R) {
  check(R.status==="PUBLIC_LATTICE_CUBE_COSET_SOURCE_REFERENCE_REVIEW_PENDING","review-pending status");
  [["producer_sha256","theorems/lattice_cube_coset_source.py"],["derivation_sha256","research/LATTICE_CUBE_COSET_SOURCE.md"],["contract_sha256","research/hypotheses/lattice_cube_coset_source_contract.json"],["cached_primary_sha256","research/literature_cache/cs_0304005_source/quantum_average.tex"]].forEach(([k,f])=>check(R[k]===hash(path.join(ROOT,f)),"provenance "+k));
  check(R.complete_source_controls.length===3,"three complete source offsets");
  const B=[[10000,1000],[9999,1000]],offsets=[[1,1],[64,127],[128,64]];
  let inputs=0;
  R.complete_source_controls.forEach((c,i)=>{
    same(c.public_source.basis_rows,B,"actual public calibration lattice");
    same(c.public_source.offsets,offsets[i],"complete declared fixed offsets");
    check(c.public_source.prime===389&&c.public_source.residue_guess===1&&c.public_source.coordinate===0&&c.public_source.box===256&&c.public_source.cube_width===128,"declared complete source parameters");
    const replay=audit(c.public_source);same(c,replay,"every original source input and Born-weighted cell");
    check(replay.valid_two_point_source_on_full_domain&&replay.balanced_bad_basis_mixture_proved,"valid source shape and balanced contamination");
    check(replay.PRIVATE_AUDIT_ONLY_common_differences.length===1,"nonempty common shift");
    same(replay.PRIVATE_AUDIT_ONLY_common_differences[0].difference,[0,-1],"common vector shift");
    inputs+=replay.complete_original_domain_censused;
  });
  const invalid=audit(R.invalid_geometry_countercontrol.public_source);
  same(R.invalid_geometry_countercontrol,invalid,"invalid multipoint geometry replay");
  check(!invalid.valid_two_point_source_on_full_domain&&invalid.fibre_size_histogram.some(r=>r.size>2),"multipoint source refused");
  inputs+=invalid.complete_original_domain_censused;
  const C=R.public_classical_LLL_control,T=C.unimodular_row_transform,A=C.reduced_basis_rows;
  check(T.length===2&&T.every(r=>r.length===2)&&Math.abs(T[0][0]*T[1][1]-T[0][1]*T[1][0])===1,"unimodular public LLL certificate");
  same(T.map(row=>[0,1].map(i=>row.reduce((s,x,j)=>s+x*B[j][i],0))),A,"public basis reduction identity");
  const minRow=A.reduce((a,b)=>a.reduce((s,x)=>s+x*x,0)<=b.reduce((s,x)=>s+x*x,0)?a:b);
  same(C.shortest_reduced_row,minRow,"shortest public reduced row");
  check(C.squared_norm===1&&minRow.reduce((s,x)=>s+x*x,0)===1&&C.norm1_in_integer_lattice_proves_global_shortest===true&&C.shortest_vector_truth_given_to_baseline===false&&C.LLL_solves_general_unique_SVP_claimed===false,"classically solved integer norm-one control only");
  same(R.fixture_geometry_certificate,{integer_lattice_vertical_spacing:1000,shortest_squared_norm:1,
    nonparallel_squared_norm_lower:1000000,cube_squared_diameter_upper:32768,
    other_congruent_multiple_squared_norm_lower:150544,LLL_preprocessed_basis_promise_inferred:false},"direct calibration geometry certificate");
  const good=mul(rat(255n,256n),rat(127n,128n)),bad=sub(one,good);
  same(R.fresh_offset_average,{private_calibration_difference:[0,-1],private_calibration_displacement:[1,0],
    exact_good_Born_mass:str(good),exact_bad_Born_mass:str(bad),failure_parameter_f1_budget:"1/18",
    bad_mass_within_declared_f1_budget:E.cmp(bad,rat(1n,18n))<=0n,average_is_per_offset_guarantee:false},"box and cube overlap price, not per-offset bound");
  same(R.known_parent_inverse_prices,{good_specified_cell_inverse_zero_probability:str(rat(2n,131072n)),
    good_specified_cell_and_Fourier_label_inverse_zero_probability:str(rat(2n,131072n*262144n)),
    conditional_normalized_coset_inverse_is_free:false,prices_apply_to_sampling_any_good_cell:false},"specified conditional inverse price");
  check(R.coherent_workspace_obligation==="COMPUTE_CELL_COPY_UNCOMPUTE_POINT_CARRY_AND_REMAINDER_GARBAGE"&&R.source_public_geometry_can_enable_more_than_copy_only_DCP===true,"clean workspace and actual access model");
  ["scalable_quantum_source_circuit_compiled","efficient_noisy_DCP_decoder_supplied","accepted_speedup_candidate","new_active_negative_result_created","novelty_claim"].forEach(k=>check(R[k]===false,"unresolved obligation "+k));
  return {verified:true,original_source_inputs_replayed:inputs,valid_source_controls:3,multipoint_source_refused:true,classical_control_solved:true,accepted_speedup_candidate:false};
}
module.exports={verify,audit};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));

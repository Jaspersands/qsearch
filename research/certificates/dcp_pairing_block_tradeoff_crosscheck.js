// Independent native counting, integer bounds, full gate permutations and
// closed-form Holevo controls. No general decoding/independent-noise promise certified.
"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert/strict");
const dir=path.join(__dirname,"../phase_workbench");
const args=process.argv.slice(2),blockMode=args[0]==="--block";
const barrierPath=!blockMode&&args[0]?args[0]:path.join(dir,"dcp_pairing_composition_barrier.json");
const blockPath=blockMode?args[1]:path.join(dir,"dcp_correlated_phase_block.json");
const barrier=JSON.parse(fs.readFileSync(barrierPath,"utf8"));
const block=JSON.parse(fs.readFileSync(blockPath,"utf8"));
const eq=(a,b)=>assert.deepEqual(a,b);
const near=(a,b)=>assert(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const bits=a=>a===0n?0:a.toString(2).length;
const pop=a=>a.toString(2).split("1").length-1;
const dyadic=(num,den)=>{
  num=BigInt(num);den=BigInt(den);
  if(num===0n)return {numerator_hex:"0x0",denominator_binary_exponent:0};
  while(den>1n&&num%2n===0n){num/=2n;den/=2n;}
  assert((den&(den-1n))===0n);
  return {numerator_hex:"0x"+num.toString(16),denominator_binary_exponent:bits(den)-1};
};
const premises={
  original_noise:"independent-balanced-dephasing-with-visibility-at-most-1-minus-1-over-n",
  fresh_IID_uniform_coarse_label_pools_before_selection:true,
  flat_input_diagonal_at_each_pair_projection:true,
  each_successful_outcome_retains_exactly_one_original_basis_pair:true,
  retained_pair_channel_is_basis_isometry_with_balanced_phase_density:true,
  no_intermediate_collective_purification_or_interference_between_pairs:true,
  latent_error_flags_or_environment_access_supplied:false,
  second_pool_labels_IID_uniform_given_retained_coarse_records_and_visibility_tags:true,
  higher_parent_label_transcripts_discarded:true,independent_fresh_batches_no_qubit_reuse:true,
  all_first_level_attempts_including_failures_and_tag_selection_charged:true,
  all_second_level_available_parents_included_in_pool_width:true,
  only_final_phase_qubit_retained_as_secret_bearing_quantum_output:true,
  all_retained_classical_records_secret_independent:true,
  zero_replacement_preserves_visibility_not_pure_plus:true};
eq(barrier.contract_id,"two_level_fresh_pair_compression_noise_converse_v1");
eq(barrier.status,"CONDITIONAL_LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING");
for(const flag of ["accepted_speedup_candidate","new_active_negative_result_created","novelty_claim","external_theorem_review_complete","actual_natural_source_noise_certified"])eq(barrier[flag],false);
eq(barrier.source_quantum_preparations_executed,0);
eq(barrier.native_short_mask_censuses.length,3);
for(const C of barrier.native_short_mask_censuses){
  const n=C.components,m=C.pool_width,r=C.short_threshold;
  assert(n>=1&&n<=2&&m>=2&&m<=3&&r<=m+1);
  let events=0,degree=0;
  const masks=Array.from({length:2**m-1},(_,i)=>i+1).filter(u=>pop(u)<r);
  for(let code=0;code<4**(n*m);code++){
    const flat=Array.from({length:n*m},(_,i)=>(code>>2*i)&3);
    for(let x=0;x<2**m;x++){
      let count=0;
      for(const u of masks){
        let ok=true;
        for(let l=0;l<n;l++){
          let sum=0;for(let i=0;i<m;i++)if((u>>i)&1)sum+=flat[l*m+i]*(1-2*((x>>i)&1));
          if(sum%4!==0)ok=false;
        }
        if(ok)count++;
      }
      degree+=count;if(count)events++;
    }
  }
  const total=4**(n*m)*2**m;
  eq(C.all_native_label_assignments_and_basis_endpoints,total);
  eq(C.short_relation_endpoint_count,events);eq(C.sum_short_relation_degrees,degree);
  eq(C.short_endpoint_probability,dyadic(events,total));
  eq(C.expected_short_degree,dyadic(masks.length,4**n));
  assert(events*4**n<=masks.length*total);eq(degree*4**n,masks.length*total);
}
function threshold(n,pool){
  const ell=bits(pool-1n),r=Math.min(Number(pool),Math.ceil(n/ell));
  return {components:n,pool_width_hex:"0x"+pool.toString(16),ceil_log2_pool_width:ell,
    long_mask_minimum_width:r,short_means_weight_strictly_less_than:r,
    native_short_endpoint_probability_upper:{one_over_two_exponent:n},
    counting_exponent_check:ell*(r-1)<=n-1,bound_is_pointwise_in_labels:false};
}
eq(barrier.polynomial_budget_frontiers.length,8);
for(const B of barrier.polynomial_budget_frontiers){
  const n=B.components,R=BigInt(B.first_level_attempt_budget_hex),Q=BigInt(B.final_attempt_budget_hex);
  const first=threshold(n,BigInt(B.first_pool.pool_width_hex)),second=threshold(n,BigInt(B.second_pool.pool_width_hex));
  eq(B.first_pool,first);eq(B.second_pool,second);eq(B.assumed_source_promises_not_inferred,premises);
  const product=first.long_mask_minimum_width*second.long_mask_minimum_width;
  const tail=Math.floor(product/(n-1)),signal=Math.max(0,Math.min(n-bits(R),tail)-1),readout=Math.max(0,signal-bits(Q-1n)+1);
  eq(B.long_long_original_visibility_exponent_lower,product);
  eq(B.original_visibility_upper_exact_rational,`${n-1}/${n}`);
  eq(B.long_long_visibility_power_of_two_upper_exponent,tail);
  eq(B.unconditional_final_visibility_power_of_two_upper_exponent,signal);
  eq(B.joint_output_distance_from_secret_independent_reference_power_of_two_upper_exponent,readout);
  eq(B.runtime_or_tree_merge_rule_restricted,false);eq(B.source_and_pair_output_architecture_restricted,true);
  eq(B.actual_natural_source_noise_certified,false);eq(B.general_DHSP_or_retained_block_no_go,false);
  eq(B.bound_uses_unconditional_Born_weight_not_free_postselection,true);
  eq(B.conditional_visibility_requires_dividing_by_paid_acceptance,true);
}

eq(block.contract_id,"native_correlated_phase_block_gate_and_information_control_v1");
eq(block.status,"PHYSICAL_GATE_EXPORT_INFORMATION_BOUND_REVIEW_PENDING");
eq(block.hardware_gate_export_implemented,true);
for(const flag of ["accepted_speedup_candidate","novelty_claim","external_theorem_review_complete","hardware_transpilation_or_execution_performed","implicit_block_is_fresh_product_source","efficient_block_decoder_supplied"])eq(block[flag],false);
eq(block.source_quantum_preparations_executed,0);eq(block.source_noise_and_IID_labels_are_assumed_not_inferred,true);
const h2=p=>p===0||p===1?0:-p*Math.log2(p)-(1-p)*Math.log2(1-p);
const fraction=s=>s.split("/").reduce((a,b)=>Number(a)/Number(b));
const value=(A,x,q)=>A.map(row=>row.reduce((s,a,i)=>s+a*((x>>i)&1),0)%q);
let wireChecks=0;
eq(block.finite_controls.length,4);
for(const [index,C] of block.finite_controls.entries()){
  const A=C.full_labels,n=A.length,m=A[0].length,q=2**C.phase_bits,G=C.exported_circuit;
  const expected=[];
  for(let l=0;l<n;l++)for(let i=0;i<m;i++){
    const lo=m+2*l,hi=lo+1,a=A[l][i]%4;
    if(a===1)expected.push(["CCX",i,lo,hi],["CX",i,lo]);
    if(a===2)expected.push(["CX",i,hi]);
    if(a===3)expected.push(["CX",i,lo],["CCX",i,lo,hi]);
  }
  eq(G.gates,expected);eq(G.kind,"COMPONENTWISE_MOD4_CONTROLLED_ADD");
  eq(G.input_phase_qubits,m);eq(G.measured_syndrome_qubits,2*n);eq(G.total_qubits,m+2*n);
  eq(G.extra_zero_work_qubits,0);eq(G.retained_original_phase_qubits,m);
  eq(G.hardware_gate_export_implemented,true);eq(G.hardware_transpilation_executed,false);eq(G.unknown_source_inverse_used,false);
  const gateCounts={};for(const g of expected)gateCounts[g[0]]=(gateCounts[g[0]]||0)+1;
  eq(G.gate_counts,gateCounts);assert(expected.length<=2*n*m);
  function apply(word,gates){
    for(const gate of gates)if(gate.slice(1,-1).every(i=>(word>>i)&1))word^=1<<gate[gate.length-1];
    return word;
  }
  const outputs=new Set();
  for(let word=0;word<2**G.total_qubits;word++){
    const x=word&(2**m-1),z=word>>m,f=value(A,x,4);
    let want=x;for(let l=0;l<n;l++)want|=(((z>>2*l)&3)+f[l])%4 << (m+2*l);
    const out=apply(word,expected);eq(out,want);eq(apply(out,[...expected].reverse()),word);outputs.add(out);wireChecks++;
  }
  eq(outputs.size,2**G.total_qubits);
  const fibers=new Map(),frequencies=new Set();
  for(let x=0;x<2**m;x++){
    const key=JSON.stringify(value(A,x,4));fibers.set(key,(fibers.get(key)||0)+1);frequencies.add(JSON.stringify(value(A,x,q)));
  }
  const sizes=[...fibers].map(([syndrome,size])=>({syndrome:JSON.parse(syndrome),size})).sort((a,b)=>{
    for(let i=0;i<n;i++)if(a.syndrome[i]!==b.syndrome[i])return a.syndrome[i]-b.syndrome[i];return 0;
  });
  eq(C.fiber_sizes,sizes);eq(C.full_frequency_map_injective,frequencies.size===2**m);
  eq(C.all_secret_states_checked,q**n);eq(C.syndrome_probabilities_sum,"1");
  const H=sizes.reduce((s,row)=>{const p=row.size/2**m;return s-p*Math.log2(p);},0),v=fraction(C.visibility_exact);
  near(C.syndrome_entropy_bits,H);
  if(C.full_frequency_map_injective){near(C.scoped_Holevo_lower_bits,Math.max(0,m-H-m*h2((1-v)/2)));assert(C.injective_uniform_block_average_max_residual<1e-9);}
  else eq(C.scoped_Holevo_lower_bits,null);
  let chi;
  if(index===0||index===1){eq(A,[[1,4,0,0],[0,0,1,4]]);chi=2*(1-h2((1-v)/2));}
  if(index===2){eq(A,[[1,2,5,12]]);chi=1-h2((1-v)/2)+(1-h2((1-v*v)/2))/2+(1-h2((1-v**3)/2))/2;}
  if(index===3){eq(A,[[1,1,1,1]]);chi=(1-h2((1-v**4)/2))/8;}
  near(C.retained_block_Holevo_bits,chi);
  eq(C.efficient_decoder_or_accessible_information_lower_bound,false);
  const B=C.sample_block_record;
  eq(B.kind,"IMPLICIT_CORRELATED_PHASE_BLOCK");eq(B.public_full_labels,A);eq(B.original_phase_bits,C.phase_bits);
  eq(B.coarse_projection_bits,2);eq(B.factored_phase_modulus_bits,C.phase_bits-2);eq(B.retained_original_quantum_wires,m);
  for(const flag of ["compact_quantum_index_supplied","fiber_cardinality_known_without_paid_computation","fiber_inverse_or_uniform_fiber_state_oracle_supplied","fresh_IID_product_phase_source_certified"])eq(B[flag],false);
  eq(B.all_measurement_outcomes_retained,true);eq(B.retained_correlations_may_not_be_replaced_by_marginal_qubits,true);
  eq(B.measured_syndrome_provenance_not_certified_by_record_alone,true);
}
eq(block.native_information_frontiers.length,6);
for(const F of block.native_information_frontiers){
  const n=F.components,e=Math.ceil(Math.log2(n));
  eq(F.original_phase_qubits,4*n);eq(F.original_phase_bits,n+8);eq(F.measured_syndrome_bits,2*n);
  eq(F.exported_gate_count_upper,8*n*n);eq(F.extra_arithmetic_work_qubits,0);
  eq(F.live_quantum_wires_before_measurement,6*n);eq(F.live_quantum_wires_after_measurement,4*n);
  eq(F.full_frequency_noninjectivity_probability_power_of_two_upper_exponent,n*n);
  eq(F.entropy_loss_bits_upper,2*(e+3));eq(F.retained_block_Holevo_bits_lower_IF_injective,Math.max(0,2*n-2*(e+3)));
  for(const flag of ["bound_is_pointwise_in_public_labels","Holevo_is_accessible_information_or_efficient_decoder","compact_fiber_index_or_fiber_inverse_supplied","actual_natural_source_noise_certified"])eq(F[flag],false);
}
console.log(JSON.stringify({status:"ok",native_censuses_replayed:3,integer_pairing_frontiers:8,
  complete_gate_wire_checks:wireChecks,closed_form_Holevo_controls:4,native_information_frontiers:6,
  general_DHSP_no_go:false,efficient_decoder:false}));

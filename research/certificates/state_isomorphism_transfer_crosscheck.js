"use strict";
// Independent support-permutation, native orbit and exact admission-ledger replay.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../reductions/state_isomorphism_transfer.json"), "utf8"));
function check(v,m) { if(!v) throw new Error(m); }
function close(a,b,m) { check(Math.abs(a-b)<4e-12, `${m}: ${a} != ${b}`); }
function gcd(a,b) { while(b) [a,b]=[b,a%b]; return a; }
function exact(r) { return [BigInt(r.numerator),BigInt(r.denominator)]; }
let graphOverlaps=0, graphEntries=0, packetOverlaps=0, programs=0;
check(report.graph_lift_controls.length===36,"missing graph controls");
for(const r of report.graph_lift_controls) {
  const N=r.rotation_order,s=r.hidden_element_calibration,pi=r.source_label_permutation;
  const support=[];
  for(let b=0;b<2;b++) for(let x=0;x<N;x++) for(let u=0;u<N;u++) support.push(b*N**4+x*N**3+pi[(x+b*s)%N]*N**2+u*N+pi[(u+b*s)%N]);
  check(JSON.stringify(support)===JSON.stringify(r.lifted_graph_support),"source lift mismatch");
  const original=new Set(support);
  const H=[];
  for(let b=0;b<2;b++) for(let g=0;g<N;g++) {
    let count=0;
    for(const v of support) {
      const c=Math.floor(v/N**4)^b, x=Math.floor(v/N**3)%N,y=Math.floor(v/N**2)%N,u=Math.floor(v/N)%N,w=v%N,delta=c ? -g : g;
      const moved=c*N**4+((x+delta+N)%N)*N**3+y*N**2+((u+delta+N)%N)*N+w;
      count+=Number(original.has(moved));
    }
    const index=g+b*N;
    check(count===r.exact_support_intersection_counts[index],"support count");
    close(count/(2*N*N),r.executed_representation_overlaps[index],"state overlap");
    if(count===2*N*N) H.push(index);
    graphOverlaps++;
  }
  check(JSON.stringify(H)===JSON.stringify([0,N+s]),"hidden reflection was not preserved");
  check(r.standard_right_coset_DHSP_hidden_reflection_shift===(N-s)%N && r.known_sign_map_preserves_full_target,"right-coset source sign map");
  let reflectionInCore=true;
  for(let a=0;a<2;a++) for(let g=0;g<N;g++) if((2*g+(-1)**a*s+N)%N!==s) reflectionInCore=false;
  check(!reflectionInCore && JSON.stringify(r.normal_core_indices)==="[0]","normal core target loss");
  close(r.executed_inverse_return_probability,1,"inverse preparation");
  check(r.selector_function_queries_per_lifted_superposition_preparation===2 && r.selector_function_queries_per_preparation_inverse===2,"missing function query charges");
  check(!r.generalized_dihedral_group_is_abelian && !r.full_hidden_shift_problem_removed,"cyclic lift shortcut");
  graphEntries+=support.length;
}
for(const r of report.native_packet_controls) {
  const N=r.modulus,labels=r.native_labels,D=2**labels.length;
  let kernel=N;
  for(const k of labels) kernel=gcd(kernel,k);
  check(r.cyclic_lift_image_order===N/kernel,"cyclic order collapsed");
  for(let delta=0;delta<N;delta++) {
    let re=0,im=0;
    for(let x=0;x<D;x++) {
      const k=labels.reduce((a,k,j)=>a+(((x>>j)&1) ? k : 0),0);
      const theta=2*Math.PI*((k*delta)%N)/N;
      re+=Math.cos(theta)/D; im+=Math.sin(theta)/D;
    }
    close(Math.hypot(re,im),r.actual_native_rotation_orbit_overlaps[delta],"literal native orbit");
    packetOverlaps++;
  }
  check(r.all_hidden_secrets_are_YES_for_unrestricted_isomorphism_decision && !r.decision_YES_alone_recovers_hidden_element,"decision/search conflation");
  const p=exact(r.literal_ordered_packet_rejection_resampling_probability);
  check(p[0]*BigInt(N)**BigInt(labels.length)===p[1],"literal packet repetition charge");
  check(!r.rejection_resampling_cost_is_optimal_lower_bound,"resampling bound overreach");
}
for(const r of report.orbit_gap_scaling_ledgers) {
  const N=BigInt(r.modulus),bits=BigInt(r.modulus_bits),size=BigInt(r.IID_native_packet_size), alpha=exact(r.maximum_nonidentity_orbit_overlap_threshold),bound=exact(r.source_probability_of_any_overlap_above_threshold_upper);
  check(N===2n**bits,"modulus precision");
  check(bound[0]*(2n**size)*alpha[0]**2n===bound[1]*(N-1n)*alpha[1]**2n,"Markov union bound");
  check(bound[0]*1024n<=bound[1],"claimed source failure budget");
  check(r.literal_ordered_packet_rejection_resampling_probability.base===2 && BigInt(r.literal_ordered_packet_rejection_resampling_probability.exponent)===-bits*size,"exact resampling exponent");
  check(!r.good_gap_solves_preparation_or_decoding && !r.Markov_union_bound_is_computational_lower_bound,"source metric promotion");
}
for(const r of report.exact_programming_countercontrols) {
  const theta=2*Math.PI/r.modulus;
  close(r.program_overlap_log_abs,r.identical_program_copy_count*Math.log(Math.cos(theta/2)),"finite program overlap");
  close(r.reflection_unitary_product_distance_from_scalar,Math.sqrt(2)*Math.abs(Math.sin(theta)),"distinct reflection unitary");
  check(r.exact_finite_program_overlap_is_nonzero && !r.deterministic_exact_universal_programming_of_both_reflections_possible,"exact program admission");
  check(!r.approximate_or_heralded_programs_excluded && !r.generic_DCP_sample_runtime_lower_bound,"exact theorem overreach");
  programs++;
}
check(Object.values(report.claim_gate).every(v=>v===false),"unsupported promotion");
console.log(JSON.stringify({graph_controls:report.graph_lift_controls.length,graph_support_entries:graphEntries,
  exact_graph_overlaps:graphOverlaps,native_orbit_overlaps:packetOverlaps,finite_program_controls:programs,
  exact_gap_ledgers:report.orbit_gap_scaling_ledgers.length,new_algorithm:false,independent_theorem_review:false}));

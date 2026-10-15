#!/usr/bin/env node
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {verify:verifyGeometry}=require("./dcp_adaptive_affine_packet_receiver_crosscheck.js");
const {readProbability,sameProbability}=require("./dcp_adaptive_direction_rank_gate_crosscheck.js");
function need(ok,message){if(!ok)throw new Error(message);}
function useful(label){return label.every(a=>!(a&1n))&&label.some(a=>a!==0n);}
function originalLabel(A,t,x,y){
  const Q=1n<<BigInt(t-1);
  return A.map(row=>{
    const delta=row.reduce((v,a,i)=>v+a*BigInt(((y>>i)&1)-((x>>i)&1)),0n);
    need(delta%2n===0n,"nonintegral source pair");
    return ((delta/2n)%Q+Q)%Q;
  });
}
function chartPoints(state){
  const basis=state.basis_hex.map(v=>Number(BigInt(v))),origin=Number(BigInt(state.origin_hex));
  return Array.from({length:2**basis.length},(_,z)=>basis.reduce((x,u,j)=>z>>j&1?x^u:x,origin)).sort((a,b)=>a-b);
}
function checkNoise(c,source){
  const m=source.input_qubits,states=source.states;
  const vis=c.visibility_by_original_register.map(readProbability);
  need(vis.length===m&&vis.every(v=>v.e<=256&&v.p>=0n&&v.p<=(1n<<BigInt(v.e))),"visibility bounds");
  const D=vis.reduce((d,v)=>d+v.e,0);
  need(c.integer_visibility_scale_exponent===D,"visibility scale");
  function weight(u){
    let p=1n,e=0;
    vis.forEach((v,i)=>{if(u>>i&1){p*=v.p;e+=v.e;}});
    return p<<BigInt(D-e);
  }
  const scores=[],frozen=[],chosen=[];
  states.forEach((s,i)=>{
    if(s.dimension===1){
      const v=s.useful_descent?2n*weight(Number(BigInt(s.basis_hex[0]))):0n;
      scores.push(v);frozen.push(v);chosen.push(null);
    }else{
      let best=-1n,form=null;
      s.actions.forEach(a=>{
        const value=a.children.reduce((v,j)=>v+scores[j],0n);
        if(value>best){best=value;form=a.form;}
      });
      scores.push(best);chosen.push(form);
      frozen.push(s.actions.find(a=>a.form===s.chosen_form).children.reduce((v,j)=>v+frozen[j],0n));
    }
    need(BigInt(c.scaled_optimal_weighted_good_assignments_by_state[i])===scores[i]&&
         c.chosen_form_by_state[i]===chosen[i],"noisy Bellman optimum");
  });
  need(c.scaled_optimal_weighted_good_assignments_by_state.length===states.length&&
       c.chosen_form_by_state.length===states.length,"policy coverage");
  let staticValue=0n;
  need(c.noise_aware_best_static.length===source.static_comparator_all_syndromes.length,"static source scope");
  source.static_comparator_all_syndromes.forEach((s,i)=>{
    let best=-1n,u=null;
    s.all_direction_scores.forEach(row=>{
      const direction=Number(BigInt(row.physical_direction_hex));
      const value=BigInt(row.good_assignments)*weight(direction);
      if(value>best){best=value;u=direction;}
    });
    const saved=c.noise_aware_best_static[i];
    need(saved.origin_hex===s.origin_hex&&Number(BigInt(saved.best_direction_hex))===u&&
         BigInt(saved.scaled_weighted_good_assignments)===best,"matched noisy static comparator");
    staticValue+=best;
  });
  const A=source.public_labels_hex.map(row=>row.map(BigInt));
  let arbitrary=0n;
  need(c.arbitrary_weighted_pairings.length===source.root_ids_all_syndromes.length,"weighted matching scope");
  source.root_ids_all_syndromes.forEach((root,index)=>{
    const vertices=chartPoints(states[root]),N=vertices.length;
    need(N<=20,"UNKNOWN: independent weighted-matching replay cap");
    const edge=vertices.map(x=>vertices.map(y=>x!==y&&useful(originalLabel(A,source.phase_bits,x,y))?weight(x^y):null));
    const cache=new Map();
    // An independent subset DP, not the producer's blossom algorithm.
    function maximum(mask){
      if(!mask)return 0n;
      if(cache.has(mask))return cache.get(mask);
      let i=0;while(!(mask&(1<<i)))i++;
      const rest=mask&~(1<<i);
      let best=maximum(rest);
      for(let j=i+1;j<N;j++)if((rest&(1<<j))&&edge[i][j]!==null){
        const v=edge[i][j]+maximum(rest&~(1<<j));if(v>best)best=v;
      }
      cache.set(mask,best);return best;
    }
    const optimum=maximum(2**N-1),saved=c.arbitrary_weighted_pairings[index];
    need(saved.root_id===root,"weighted matching root");
    const used=new Set();let witness=0n;
    saved.edges.forEach(([x,y,w])=>{
      need(vertices.includes(x)&&vertices.includes(y)&&x<y&&!used.has(x)&&!used.has(y)&&
           useful(originalLabel(A,source.phase_bits,x,y)),"weighted matching edges");
      need(BigInt(w)===weight(x^y),"physical XOR visibility weight");
      used.add(x);used.add(y);witness+=BigInt(w);
    });
    need(witness===optimum&&BigInt(saved.scaled_weight_sum)===optimum,"weighted matching optimality");
    arbitrary+=2n*optimum;
  });
  const roots=source.root_ids_all_syndromes;
  const adaptive=roots.reduce((v,i)=>v+scores[i],0n),pure=roots.reduce((v,i)=>v+frozen[i],0n);
  need(adaptive>=staticValue&&adaptive>=pure&&adaptive<=arbitrary,"noise-aware comparison");
  sameProbability(c.noise_aware_useful_retained_visibility,adaptive,m+D,"noisy feedback utility");
  sameProbability(c.frozen_pure_policy_useful_retained_visibility,pure,m+D,"frozen utility");
  sameProbability(c.noise_aware_best_static_useful_retained_visibility,staticValue,m+D,"static utility");
  sameProbability(c.arbitrary_pairing_useful_retained_visibility_upper_bound,arbitrary,m+D,"pairing utility");
  const leaves=[];
  function collect(i){
    const s=states[i];if(s.dimension===1){leaves.push(i);return;}
    s.actions.find(a=>a.form===chosen[i]).children.forEach(collect);
  }
  roots.forEach(collect);
  need(JSON.stringify(c.chosen_leaf_ids)===JSON.stringify(leaves),"noisy leaf census");
  const good=leaves.filter(i=>states[i].useful_descent).length;
  sameProbability(c.useful_label_probability_under_selected_noisy_policy,BigInt(2*good),m,"label-event probability");
  let product=1n;vis.forEach(v=>product*=((1n<<BigInt(v.e))+v.p));
  sameProbability(c.exact_product_input_trace_distance_from_ideal,
                  (1n<<BigInt(D+m))-product,D+m,"product input trace distance");
  need(c.source_model==="independent-balanced-original-phase-depolarization"&&
       c.source_independence_established_by_workflow===false&&c.actual_lattice_noise_matched===false&&
       c.all_measurement_branch_probabilities_unchanged===true&&
       c.visibility_exponent_is_physical_Hamming_distance_not_merge_depth===true&&
       c.retained_visibility_is_complete_decoder_success===false,"noise model scope");
}
function checkCorrelation(c){
  const matrix=c.joint_density_numerators_denominator_8;
  need(matrix.length===8&&matrix.every(row=>row.length===8),"correlated source size");
  for(let x=0;x<8;x++)for(let y=0;y<8;y++){
    const parity=z=>{let p=0;for(;z;z&=z-1)p^=1;return p;};
    need(matrix[x][y]===Number(parity(x)===parity(y)),"actual correlated density");
  }
  sameProbability(c.actual_even_weight_pair_visibility,1n,0,"correlated pair visibility");
  sameProbability(c.incorrect_product_of_marginals_prediction,0n,0,"correlated marginal trap");
  need(JSON.stringify(c.individual_phase_visibilities)==="[0,0,0]"&&JSON.stringify(c.retained_pair)==="[0,3]"&&
       c.correlation_covered_by_product_noise_law===false&&
       c.flat_diagonal_alone_implies_visibility_factorization===false,"correlation scope");
}
function verify(report,geometryRaw){
  need(report.contract_id==="original_register_balanced_product_noise_affine_packet_v1"&&
       report.accepted_speedup_candidate===false&&report.efficient_receiver_supplied===false&&
       report.source_quantum_preparations_executed===0,"claim admission");
  need(report.source_geometry_artifact==="research/phase_workbench/dcp_adaptive_affine_packet_receiver.json"&&
       report.source_geometry_sha256===crypto.createHash("sha256").update(geometryRaw).digest("hex"),"geometry provenance");
  const geometry=JSON.parse(geometryRaw);verifyGeometry(geometry);
  const sources={"unfiltered-seed-2":geometry.source_controls[2],"unfiltered-seed-5":geometry.source_controls[5],
                 "selected-grammar-gap-94":geometry.affine_grammar_gap_counterexample};
  const settings=["1","15/16","3/4","1/2","0","heterogeneous"];
  need(report.noise_controls.length===18,"noise coverage");
  let index=0;
  for(const source of Object.keys(sources))for(const setting of settings){
    const c=report.noise_controls[index++];
    need(c.source_control===source&&c.noise_setting===setting,"fixed noise grid");
    const constants={"1":[1n,0],"15/16":[15n,4],"3/4":[3n,2],"1/2":[1n,1],"0":[0n,0]};
    c.visibility_by_original_register.forEach((v,i)=>{
      const expected=setting==="heterogeneous"?[[1n,0],[1n,1],[3n,2]][i%3]:constants[setting];
      sameProbability(v,expected[0],expected[1],"noise grid parameter");
    });
    checkNoise(c,sources[source]);
  }
  const s=report.scope;
  need(s.source_independence_proved_from_marginals===false&&s.arbitrary_correlated_contamination_covered===false&&
       s.unbalanced_source_populations_covered===false&&s.actual_lattice_source_noise_certified===false&&
       s.optimality_is_general_quantum_measurement_optimum===false&&s.visibility_metric_is_decoding_success===false&&
       s.growing_family_speedup_proved===false,"scope expansion");
  checkCorrelation(report.correlation_counterexample);
  return {status:"ok",noise_controls:18,weighted_matching_checker:"independent exact subset DP",actual_lattice_noise_matched:false};
}
module.exports={verify};
if(require.main===module){
  const root=path.resolve(__dirname,"../..");
  const file=process.argv[2]||path.join(root,"research/phase_workbench/dcp_affine_packet_noise.json");
  const raw=fs.readFileSync(path.join(root,"research/phase_workbench/dcp_adaptive_affine_packet_receiver.json"));
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")),raw)));
}

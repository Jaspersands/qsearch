#!/usr/bin/env node
"use strict";
const fs = require("fs");
const path = require("path");
const {parity, map, sameProbability} = require("./dcp_adaptive_direction_rank_gate_crosscheck.js");

function need(ok, message) { if (!ok) throw new Error(message); }
function binomial2(k,d) {
  let p=1n,q=1n;
  for(let j=0;j<d;j++) { p*=(1n<<BigInt(k-j))-1n; q*=(1n<<BigInt(d-j))-1n; }
  need(p%q===0n,"Gaussian binomial integrality");
  return p/q;
}
function cost(k,rank) {
  const strata=[];
  let states=0n,actions=0n;
  for(let d=1;d<=k;d++) {
    const s=(1n<<BigInt(rank+k-d))*binomial2(k,d);
    const a=d>1?s*((1n<<BigInt(d))-1n):0n;
    strata.push([d,s,a]); states+=s; actions+=a;
  }
  return {states,actions,strata};
}
function checkCost(record) {
  const k=record.logical_dimension, rank=record.initial_parity_rank;
  const result=cost(k,rank);
  need(BigInt(record.all_syndromes_chart_states)===result.states &&
       BigInt(record.all_syndromes_chart_actions)===result.actions,"search work count");
  need(record.dimension_strata.length===k,"cost strata coverage");
  record.dimension_strata.forEach((row,i)=>{
    const [d,s,a]=result.strata[i];
    need(row[0]===d && BigInt(row[1])===s && BigInt(row[2])===a,"cost dimension stratum");
  });
  return result;
}
function assignments(basis,origin) {
  const out=[];
  for(let z=0;z<2**basis.length;z++) {
    let x=origin;
    basis.forEach((u,j)=>{if(z>>j&1)x^=u;});
    out.push({x,z});
  }
  return out;
}
function key(points) {return points.map(v=>v.x===undefined?v:v.x).sort((a,b)=>a-b).join(",");}
function label(A,t,x,y) {
  const Q=1n<<BigInt(t-1);
  return A.map(row=>{
    let difference=0n;
    row.forEach((a,i)=>{difference+=a*BigInt(((y>>i)&1)-((x>>i)&1));});
    need(difference%2n===0n,"nonintegral native phase label");
    return ((difference/2n)%Q+Q)%Q;
  });
}
function useful(label) {return label.every(a=>!(a&1n))&&label.some(a=>a!==0n);}
function checkCase(c) {
  const A=c.public_labels_hex.map(row=>row.map(BigInt)),n=A.length,m=A[0].length,t=c.phase_bits;
  need(m<=10&&n>0&&A.every(row=>row.length===m),"source dimensions/cap");
  need(c.component_count===n&&c.input_qubits===m&&t>=3,"source metadata");
  const q=1n<<BigInt(t),full=(1<<m)-1;
  need(A.every(row=>row.every(a=>a>=0n&&a<q)),"canonical labels");
  const B=A.map(row=>row.reduce((b,a,i)=>b|((a&1n)<<BigInt(i)),0n));
  const D=Array.from({length:1<<m},(_,x)=>x).filter(x=>map(B,BigInt(x))===0n);
  const k=Math.log2(D.length),rank=m-k;
  need(c.root_kernel_dimension===k&&c.initial_parity_rank===rank,"native kernel dimension");
  const geometry=checkCost(c.search_cost);
  need(BigInt(c.states.length)===geometry.states,"state coverage");
  const sets=[],pointKeys=new Set();
  c.states.forEach((s,i)=>{
    need(s.id===i&&s.dimension>=1&&s.dimension===s.basis_hex.length,"state identity");
    const basis=s.basis_hex.map(v=>Number(BigInt(v))),origin=Number(BigInt(s.origin_hex));
    need(basis.every(v=>v>0&&v<=full&&D.includes(v))&&origin>=0&&origin<=full,"physical affine chart");
    const coords=assignments(basis,origin),pts=coords.map(v=>v.x),sig=key(pts);
    need(new Set(pts).size===2**s.dimension&&!pointKeys.has(sig),"dependent or duplicate affine chart");
    pointKeys.add(sig); sets.push(sig);
    if(s.dimension===1) {
      const out=label(A,t,origin,origin^basis[0]);
      need(JSON.stringify(out.map(a=>`0x${a.toString(16)}`))===JSON.stringify(s.output_label_hex),"terminal physical phase");
      need(s.useful_descent===useful(out)&&s.good_assignments===2*Number(useful(out))&&
           s.actions.length===0&&s.chosen_form===null,"zero label or leaf score");
    } else {
      need(s.actions.length===2**s.dimension-1,"all affine measurements must be considered");
      let best=-1,chosen=null;
      s.actions.forEach((action,j)=>{
        need(action.form===j+1&&action.children.length===2,"measurement action coverage");
        const childSets=[[],[]];
        coords.forEach(({x,z})=>childSets[parity(BigInt(z&action.form))].push(x));
        action.children.forEach((child,b)=>{
          need(Number.isInteger(child)&&child>=0&&child<i,"noncausal or missing Bellman child");
          need(c.states[child].dimension===s.dimension-1&&sets[child]===key(childSets[b]),"actual affine measurement branches");
        });
        const good=action.children.reduce((v,child)=>v+c.states[child].good_assignments,0);
        need(action.good_assignments===good,"Bellman branch score");
        if(good>best){best=good;chosen=action.form;}
      });
      need(s.good_assignments===best&&s.chosen_form===chosen,"optimal feedback policy");
    }
  });
  const roots=c.root_ids_all_syndromes;
  need(roots.length===2**rank&&new Set(roots).size===roots.length,"all initial syndromes");
  const rootPoints=[];
  roots.forEach(i=>{
    const s=c.states[i],pts=sets[i].split(",").map(Number);
    need(s.dimension===k&&pts.length===D.length,"initial chart dimension");
    const syndromes=new Set(pts.map(x=>map(B,BigInt(x)).toString()));
    need(syndromes.size===1,"initial parity fibre");
    rootPoints.push(...pts);
  });
  need(rootPoints.length===1<<m&&new Set(rootPoints).size===1<<m,"unpaid initial syndrome postselection");
  need(c.static_comparator_all_syndromes.length===roots.length,"static comparator syndrome scope");
  need(c.root_quadratic_maps.length===roots.length&&
       c.arbitrary_basis_pairing_bounds_all_syndromes.length===roots.length,"structural comparator coverage");
  let adaptive=0,staticGood=0,pairingGood=0;
  roots.forEach((root,index)=>{
    const s=c.states[root],row=c.static_comparator_all_syndromes[index];
    need(row.origin_hex===s.origin_hex,"static comparison source");
    const pts=sets[root].split(",").map(Number),choices=D.filter(u=>u!==0);
    need(row.all_direction_scores.length===choices.length,"static direction menu");
    let best=-1,chosen=null;
    choices.forEach((u,j)=>{
      const good=pts.reduce((sum,x)=>sum+(x<(x^u)?2*Number(useful(label(A,t,x,x^u))):0),0);
      const saved=row.all_direction_scores[j];
      need(BigInt(saved.physical_direction_hex)===BigInt(u)&&saved.good_assignments===good,"matched static original-phase score");
      if(good>best){best=good;chosen=u;}
    });
    need(row.best_good_assignments===best&&Number(BigInt(row.best_direction_hex))===chosen,"best static score");
    need(s.good_assignments>=best,"feedback must include precommitted measurements");
    const quadratic=c.root_quadratic_maps[index],basis=s.basis_hex.map(v=>Number(BigInt(v))),origin=Number(BigInt(s.origin_hex));
    need(quadratic.root_id===root&&quadratic.linear_coefficients_hex.length===k&&
         quadratic.cross_terms.length===k*(k-1)/2&&quadratic.constant_coefficient===0&&
         quadratic.degree_at_most_two===true&&quadratic.public_polynomial_is_unknown_state_preparation_oracle===false,
         "quadratic representation scope");
    let termIndex=0;
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){
      const term=quadratic.cross_terms[termIndex++];
      need(term.i===i&&term.j===j&&BigInt(term.coefficient_hex)===map(B,BigInt(basis[i]&basis[j])),"polar overlap coefficient");
    }
    const classes=new Map();
    assignments(basis,origin).forEach(({x,z})=>{
      const phase=label(A,t,origin,x);
      const low=phase.reduce((v,a,j)=>v|((a&1n)<<BigInt(j)),0n);
      let predicted=0n;
      quadratic.linear_coefficients_hex.forEach((a,j)=>{if(z>>j&1)predicted^=BigInt(a);});
      quadratic.cross_terms.forEach(term=>{if((z>>term.i)&(z>>term.j)&1)predicted^=BigInt(term.coefficient_hex);});
      need(low===predicted,"quadratic map vs ORIGINAL public phase");
      const color=low.toString(),value=phase.map(String).join(",");
      if(!classes.has(color))classes.set(color,new Map());
      const counts=classes.get(color); counts.set(value,(counts.get(value)||0)+1);
    });
    const bound=c.arbitrary_basis_pairing_bounds_all_syndromes[index];
    need(bound.origin_hex===s.origin_hex&&bound.color_blocks.length===classes.size,"basis pairing source");
    let good=0;
    const seenColors=new Set();
    bound.color_blocks.forEach(block=>{
      need(block.low_phase_bits.length===n&&block.low_phase_bits.every(v=>v===0||v===1),"phase color bits");
      const color=block.low_phase_bits.reduce((v,a,j)=>v|(BigInt(a)<<BigInt(j)),0n).toString();
      const counts=classes.get(color);
      need(counts&&!seenColors.has(color),"phase color coverage"); seenColors.add(color);
      const population=[...counts.values()].reduce((a,b)=>a+b,0),largest=Math.max(...counts.values());
      const pairs=Math.min(Math.floor(population/2),population-largest);
      need(block.population===population&&block.largest_equal_full_phase_class===largest&&
           block.maximum_useful_pairs===pairs,"complete multipartite matching bound");
      good+=2*pairs;
    });
    need(bound.maximum_good_assignments===good&&s.good_assignments<=good,"pairing upper bound");
    pairingGood+=good;
    adaptive+=s.good_assignments; staticGood+=best;
  });
  sameProbability(c.optimal_feedback_useful_descent_probability,BigInt(adaptive),m,"feedback probability");
  sameProbability(c.best_static_useful_descent_probability,BigInt(staticGood),m,"static probability");
  sameProbability(c.feedback_gain,BigInt(adaptive-staticGood),m,"feedback gain");
  sameProbability(c.arbitrary_basis_pairing_useful_descent_upper_bound,BigInt(pairingGood),m,"pairing probability");
  need(c.affine_policy_saturates_arbitrary_pairing_bound===(adaptive===pairingGood)&&
       c.arbitrary_basis_pairing_bound_is_general_quantum_optimum===false,"pairing optimality scope");
  const leaves=[];
  function descend(i) {
    const s=c.states[i];
    if(s.dimension===1){leaves.push(i);return;}
    s.actions.find(a=>a.form===s.chosen_form).children.forEach(descend);
  }
  roots.forEach(descend);
  need(leaves.length===2**(m-1)&&new Set(leaves).size===leaves.length&&
       JSON.stringify(leaves)===JSON.stringify(c.chosen_policy_leaf_ids),"paid feedback leaf census");
  const histogram=new Map();
  leaves.forEach(i=>{
    const k=c.states[i].output_label_hex.join(",");
    histogram.set(k,(histogram.get(k)||0)+1);
  });
  need(c.retained_label_distribution_all_outcomes.length===histogram.size,"label distribution support");
  const seen=new Set();
  c.retained_label_distribution_all_outcomes.forEach(row=>{
    const k=row.label_hex.join(","),count=histogram.get(k);
    need(count!==undefined&&!seen.has(k)&&row.physical_outcome_pairs===count&&
         row.useful_descent===useful(row.label_hex.map(BigInt)),"retained output distribution");
    sameProbability(row.probability,BigInt(2*count),m,"retained output mass");
    seen.add(k);
  });
  const ledger=c.resource_ledger_per_supplied_packet;
  need(ledger.original_unknown_phase_qubits===m&&ledger.initial_syndrome_Z_measurements===rank&&
       ledger.adaptive_complement_Z_measurements===k-1&&ledger.retained_qubits===1&&
       ledger.every_branch_probability_charged===true&&ledger.initial_syndromes_postselected===false&&
       ledger.secret_or_unknown_state_evaluator_available_to_policy===false&&
       ledger.source_preparation_inverse_available===false,"physical resource scope");
  need(c.objective_excludes_zero_labels===true&&c.guarantee_conditional_on_supplied_public_A===true&&
       c.noise_model==="pure-flat-native-phase-packet"&&c.classical_policy_search_polynomial_time===false&&
       c.general_quantum_optimum===false,"receiver scope");
  return adaptive>staticGood;
}
function verify(report) {
  need(report.contract_id==="native_carry_packet_affine_feedback_receiver_v1"&&
       report.accepted_speedup_candidate===false&&report.novelty_claim===false&&
       report.efficient_receiver_supplied===false&&report.zero_output_labels_counted_as_success===false&&
       report.source_quantum_preparations_executed===0,"claim admission");
  const s=report.scope;
  need(s.all_branches_charged===true&&s.optimality_only_over_this_affine_measurement_grammar===true&&
       s.mixed_noise_covered===false&&s.efficient_search_or_uniform_policy_family_supplied===false&&
       s.finite_seed_cohort_implies_asymptotic_advantage===false&&s.classical_hardness_or_speedup_proved===false,
       "global claim scope");
  need(report.source_controls.length===6,"source control coverage");
  const gains=report.source_controls.map(checkCase).filter(Boolean).length;
  const gap=report.affine_grammar_gap_counterexample;
  checkCase(gap);
  const feedback=gap.optimal_feedback_useful_descent_probability;
  const pairing=gap.arbitrary_basis_pairing_useful_descent_upper_bound;
  sameProbability(feedback,9n,4,"selected affine grammar gap");
  sameProbability(pairing,11n,4,"selected arbitrary pairing comparison");
  need(gap.public_source_selection.kind.startsWith("SELECTED-")&&
       gap.affine_policy_saturates_arbitrary_pairing_bound===false,"selected counterexample scope");
  const boundary=report.known_algorithm_boundary;
  need(boundary.fixed_t_full_HSP_oracle_novelty_claim_allowed===false&&
       boundary.exact_theorem_requires_subgroup_state_creating_unitary_and_inverse===true&&
       boundary.nonexact_forward_only_HSMC_variant_in_Proposition3_exists===true&&
       boundary.missing_inverse_alone_blocks_all_published_methods===false&&
       boundary.copy_only_phase_source_transfer_proved===false&&
       boundary.uniform_polynomial_bound_when_t_grows_supplied===false,"known algorithm access boundary");
  need(JSON.stringify(report.scaling_cost_ledgers_not_executed.map(c=>c.logical_dimension))==="[4,8,16,32,64]","cost scaling coverage");
  report.scaling_cost_ledgers_not_executed.forEach(checkCost);
  return {status:"ok",source_controls:6,strict_feedback_gains:gains,
          selected_grammar_gap:"9/16 versus 11/16",efficient_receiver_supplied:false};
}
module.exports={verify};
if(require.main===module){
  const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_adaptive_affine_packet_receiver.json");
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));
}

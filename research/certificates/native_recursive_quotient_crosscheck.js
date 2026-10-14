"use strict";
// Independent exact same-original chain replay. No source/producer oracle is assumed.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),M=require("./native_small_multiple_completion_crosscheck.js"),B=require("./native_basis_lottery_crosscheck.js");
const {check,rat,parse,str,mul,sub,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_recursive_quotient_audit.json");
const mod=(x,q)=>(x%q+q)%q,enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,msg)=>E.same(canonical(a),canonical(b),msg),digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex"),hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const nearest=(e,Q)=>(e+Q/2n)/Q;
function chain(raw,hypotheses,R,maxSteps=128){
  // B independently checks typed/canonical originals and EVERY radius distance.
  const q0=BigInt(raw[0].modulus),n=raw[0].label.length;
  check(R>=0n&&4n*R<q0&&hypotheses.length>0&&maxSteps>0,"complete supplied chain scope");
  B.complete(raw,1n,Array(n).fill(0),R);
  const base={original_records_sha256:digest(raw),original_records_paid_once:raw.length,max_steps:maxSteps,verification_radius:enc(R),declared_path_length:hypotheses.length,
    steps:[],candidate_secret:null,sequential_response_rounding_evaluations:0,canonical_composition_rounding_evaluations:0,
    new_independent_original_samples_created:false,multiple_producer_supplied:false,true_prefix_or_Gaussian_law_certified:false,planted_truth_or_uniqueness_certified:false};
  if(hypotheses.length>maxSteps)return {...base,status:"COMPLETE_PATH_CAP_EXCEEDED_NOT_NO_SECRET",complete_declared_path_or_terminal_preimage:false};
  let current=raw,prefix=Array(n).fill(0n),scale=1n;
  for(let index=0;index<hypotheses.length;index++){
    const [c0,w]=hypotheses[index],c=BigInt(c0),q=BigInt(current[0].modulus),model=M.quotient(q,c,w),step={index,parent_modulus:enc(q),parent_scale:enc(scale),parent_original_prefix:prefix.map(enc),coefficient:c0,multiple:w,parent_records_sha256:digest(current)};
    if(model===null){base.steps.push({...step,status:"EXACT_CURRENT_RING_IMAGE_INCOMPATIBILITY"});return {...base,status:"INCOMPATIBLE_SUPPLIED_PATH_NOT_NO_ORIGINAL_SECRET",complete_declared_path_or_terminal_preimage:false};}
    step.quotient_model=model;const g=BigInt(model.nonunit_factor),Q=BigInt(model.remaining_modulus),x=model.known_quotient_IF_multiple_is_true.map(BigInt);
    if(g===1n){
      const s=prefix.map((a,i)=>enc(a+scale*x[i])),F=B.complete(raw,1n,s,R).unit_fit;
      base.steps.push({...step,status:"TERMINAL_UNIT_PREIMAGE_NOT_SOURCE_CERTIFICATE",current_algebraic_preimage:x.map(enc)});
      const equations=base.steps.map(t=>s.every((v,i)=>mod(BigInt(t.coefficient)*(BigInt(v)/BigInt(t.parent_scale)),BigInt(t.parent_modulus))===BigInt(t.multiple[i])));
      check(equations.every(Boolean),"all supplied path equations after full-original lift");
      return {...base,status:F.fits_public_radius?"ONE_ORIGINAL_RADIUS_FIT_SOURCE_CERTIFICATION_REQUIRED":"TERMINAL_PREIMAGE_ORIGINAL_RADIUS_FIT_FAILED",candidate_secret:F.fits_public_radius?s:null,
        terminal_original_algebraic_preimage:s,original_fit:F,supplied_multiple_chain_equations_verified:equations,
        unconsumed_supplied_hypotheses:hypotheses.length-index-1,complete_declared_path_or_terminal_preimage:true};
    }
    const P=prefix.map((a,i)=>a+scale*x[i]),L=scale*Q;check(q0/L===g&&g<q&&P.every(a=>a>=0n&&a<L),"strict original-root descent and canonical prefix");
    const children=[],receipts=[];
    current.forEach((parent,j)=>{
      const origin=raw[j],e=mod(BigInt(parent.value)-parent.label.reduce((v,a,i)=>v+BigInt(a)*x[i],0n),q),v=mod(nearest(e,Q),g),e0=mod(BigInt(origin.value)-origin.label.reduce((v,a,i)=>v+BigInt(a)*P[i],0n),q0),direct=mod(nearest(e0,L),g),label=origin.label.map(a=>enc(mod(BigInt(a),g)));
      same(label,parent.label.map(a=>enc(mod(BigInt(a),g))),"one-to-one original labels");check(v===direct&&parent.source_id===origin.source_id,"nested and direct original rounding, no reindexed noise");
      children.push({label,value:enc(v),modulus:enc(g),source_id:origin.source_id});
      receipts.push({source_id:origin.source_id,parent_record_sha256:digest(parent),original_record_sha256:digest(origin),corrected_parent_response:enc(e),corrected_original_response:enc(e0),sequential_derived_response:enc(v),direct_original_derived_response:enc(direct)});
    });
    const node={original_records_sha256:base.original_records_sha256,modulus:enc(g),original_scale:enc(L),known_original_lower_prefix_IF_path_true:P.map(enc)};
    base.steps.push({...step,status:"CANONICAL_ORIGINAL_QUOTIENT_NODE_NOT_TRUE_PREFIX_CERTIFICATE",canonical_node:node,canonical_node_sha256:digest(node),derived_records:children,record_receipts:receipts,source_IDs_preserved:true,composition_verified_on_every_original:true});
    base.sequential_response_rounding_evaluations+=raw.length;base.canonical_composition_rounding_evaluations+=raw.length;
    current=children;prefix=P;scale=L;
  }
  return {...base,status:"SUPPLIED_PATH_EXHAUSTED_MISSING_TERMINAL_DECODER_NOT_NO_SECRET",complete_declared_path_or_terminal_preimage:true,final_canonical_node:base.steps.at(-1).canonical_node};
}
function cost(C){
  const b=BigInt(C.declared_branches_per_level),d=C.declared_depth,p=parse(C.each_fixed_true_root_marginal_coverage_lower_EXTERNAL),c=C.conditional_on_every_previous_true_choice_coverage_lower_EXTERNAL;
  check(b>=1n&&Number.isSafeInteger(d)&&d>=1&&d*b.toString(2).length<=65536&&cmp(p,zero)>=0n&&cmp(p,one)<=0n,"complete cost and probability scope");
  const leaves=b**BigInt(d),nodes=b===1n?BigInt(d+1):(b**BigInt(d+1)-1n)/(b-1n),frechet=sub(mul(rat(BigInt(d)),p),rat(BigInt(d-1)));
  check(BigInt(C.complete_tree_leaves_upper)===leaves&&BigInt(C.complete_tree_nodes_upper)===nodes&&C.random_one_branch_success_IF_every_visited_true_list_covers===str(rat(1n,leaves))&&C.all_required_fixed_root_events_Frechet_lower===str(cmp(frechet,zero)<0n?zero:frechet),"no hidden free ambiguity or multiplied marginal coverage");
  if(c!==null){const x=parse(c);check(cmp(x,zero)>=0n&&cmp(x,one)<=0n&&C.all_levels_coverage_lower_IF_conditional_contract_proved===str(rat(x[0]**BigInt(d),x[1]**BigInt(d))),"conditional product only under external stronger contract");}else check(C.all_levels_coverage_lower_IF_conditional_contract_proved===null,"no invented conditional producer contract");
  check(C.marginal_success_product_is_justified===false&&C.same_bank_repetition_amplifies_source_good_fraction===false&&C.fixed_root_Frechet_bound_covers_unknown_adaptive_root_selection===false&&C.polynomial_branch_budget_implies_polynomial_total_work===false&&C.actual_coverage_or_producer_contract_established===false&&C.tree_bound_is_a_general_reduction_lower_bound===false,"cost is scoped and source promises stay missing");
}
function source(S){
  const n=S.dimension,r=S.root_digits,q=3n**BigInt(r),C=BigInt(S.declared_centered_coefficient_bound),alpha=parse(S.normalized_Gaussian_width);let g=1n,d=0;
  check(n>0&&r>0&&C>=1n&&cmp(alpha,zero)>0n&&cmp(alpha,one)<0n&&BigInt(S.original_modulus)===q,"valid fixed-root source scope");
  while(3n*g<=C&&d+1<r){g*=3n;d++;}
  const bad=rat(BigInt(Math.max(0,r-1)),3n**BigInt(n));
  check(S.nonunit_child_possible_within_declared_bound===(C>=3n&&r>1)&&S.first_nonunit_child_root_digits_upper===d&&BigInt(S.first_nonunit_child_modulus_upper)===g&&S.additional_strict_nonunit_steps_upper_after_first===Math.max(0,d-1)&&S.all_proper_fixed_true_root_primitive_failure_union_upper_IF_original_secret_uniform===str(cmp(bad,one)>0n?one:bad),"coefficient valuation and true high-quotient primitive union");
  check(S.fixed_true_quotient_normalized_width_preserved===true&&S.fixed_true_quotient_laws_share_original_noise_and_are_not_independent===true&&S.adaptively_selected_root_has_unconditioned_Gaussian_law_certified===false&&S.original_primitive_secret_implies_every_high_quotient_primitive===false&&S.same_normalized_width_guarantees_a_distinguisher_at_every_root===false&&S.published_rounded_Gaussian_reduction_applicable_at_all_roots===false&&S.actual_decision_algorithm_or_uniform_conditional_coverage_supplied===false,"no free recursive source or decision oracle");
}
function verify(P){
  check(P.status==="EXACT_QUOTIENT_COMPOSITION_AND_RECURSION_COST_AUDIT_REVIEW_PENDING"&&P.producer_sha256===hash(path.join(ROOT,"theorems/native_recursive_quotient_audit.py"))&&P.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_RECURSIVE_QUOTIENT_AUDIT.md")),"current scoped derivation");
  const deps=["native_basis_lottery.py","native_affine_fibre_relaxation.py","native_small_multiple_completion.py","native_classical_modulus_descent.py","native_gaussian_quotient_completion.py","ternary_covariant_noise.py","ternary_noise_degradation.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(P.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");deps.forEach(f=>check(P.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(P.actual_chain_calibrations.length===2&&P.source_contract_profiles.length===3&&P.ambiguity_profiles.length===3,"declared live scope");
  let originalEquations=0;P.actual_chain_calibrations.forEach(C=>{
    const raw=C.original_records,q=BigInt(raw[0].modulus),s=C.original_secret_FOR_CALIBRATION_ONLY,e=C.original_errors_FOR_CALIBRATION_ONLY;
    raw.forEach((r,j)=>check(mod(r.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(s[i]),0n)+BigInt(e[j]),q)===BigInt(r.value),"actual calibration observations"));
    const result=chain(raw,C.supplied_hypotheses_FOR_CALIBRATION_ONLY,BigInt(C.chain.verification_radius),C.chain.max_steps);same(C.chain,result,"independent complete supplied chain replay");
    same(result.candidate_secret,s,"only post-solve truth comparison");check(C.matches_truth_after_solving===true&&C.actual_multiple_producer_supplied===false,"no truth multiple producer granted");originalEquations+=result.sequential_response_rounding_evaluations;
  });
  const W=P.wrong_prefix_subgroup_countercontrol,raw=W.original_records;
  check(raw.length===81&&W.true_secret_FOR_COUNTERCONTROL_ONLY===5&&W.supplied_wrong_prefix===2,"complete wrong-prefix label population");
  raw.forEach((r,a)=>same(r,{label:[a],value:a*5%81,modulus:81,source_id:`wrong-prefix:${a}`},"all original labels enumerated once"));
  const result=chain(raw,[[9,[18]]],0n);same(W.chain,result,"actual false-prefix quotient path");
  const child=result.steps[0].derived_records,counts=Array.from({length:9},(_,b)=>Array.from({length:9},(_,v)=>child.filter(r=>r.label[0]===b&&r.value===v).length));
  same(W.conditional_child_value_counts_by_child_label,counts,"conditional subgroup support, not full uniform");
  counts.forEach(row=>check(row.filter(x=>x===3).length===3&&row.filter(x=>x===0).length===6,"exact three-point conditional support"));
  same(W.conditional_TV_from_full_uniform,Array(9).fill("2/3"),"wrong prefix need not be full-uniform null");
  check(W.wrong_prefix_implies_full_uniform_child===false&&W.candidate_or_decision_oracle_created===false,"scoped mathematical countercontrol");
  P.source_contract_profiles.forEach(source);P.ambiguity_profiles.forEach(cost);cost(P.conditional_contract_reference);
  same(P.shared_source_coverage_countercontrol,{two_disjoint_source_good_events_each_probability:"1/2",their_joint_probability:"0",naive_marginal_product:"1/4",decision_oracle_or_toy_problem_generated:false},"marginal source success cannot be multiplied");
  same(P.published_interface_scope,{literature_id:"LIT-BTV-2026-SAMPLE-PRESERVING",nonzero_coefficient_is_nonzero_modulo_current_q:true,list_outputs_are_certified_true_pairs:false,source_average_success_is_uniform_per_instance:false,general_noise_theorem_not_discrete_Gaussian_corollary_required:true},"audited published interface, no invented strengthening");
  check(P.accepted_speedup_candidate===false&&P.new_active_negative_result_created===false&&P.actual_quantum_decision_or_multiple_producer===false&&P.complete_recursive_search_to_decision_reduction_established===false&&P.novelty_claim===false,"no recursive solver or quantum claim");
  return {verified:true,actual_original_composition_equations:originalEquations+81,calibration_chains:2,wrong_prefix_conditional_TV:"2/3",recursive_producer_or_reduction_supplied:false};
}
module.exports={verify,chain,cost,source};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

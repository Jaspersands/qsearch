"use strict";
// Independent exact replay for modulo-scale prefix pruning and canonical DAG collapse.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),M=require("./native_small_multiple_completion_crosscheck.js"),B=require("./native_basis_lottery_crosscheck.js"),S=require("./native_source_refresh_crosscheck.js");
const {check,rat,parse,str,add,mul,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_prefix_ambiguity_pruning.json");
const mod=(x,q)=>(x%q+q)%q,enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,msg)=>E.same(canonical(a),canonical(b),msg),hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min=(a,b)=>cmp(a,b)<=0n?a:b;
function root(q){check(q>=3n,"positive ternary root");let d=0;while(q%3n===0n){q/=3n;d++;}check(q===1n,"actual ternary prime power");return d;}

function moduloScaleFit(raw,scale0,prefix0,R0){
  const q0=BigInt(raw[0].modulus),n=raw[0].label.length,L=BigInt(scale0),R=BigInt(R0);
  root(L);check(q0%L===0n&&R>=0n&&4n*R<q0,"valid scale L and radius R");
  const P=prefix0.map(BigInt);check(P.length===n&&P.every(x=>x>=0n&&x<L),"canonical scale-L prefix");
  const ds=raw.map(rec=>{
    const rMod=mod(BigInt(rec.value)-rec.label.reduce((v,a,i)=>v+BigInt(a)*P[i],0n),L);
    return rMod<L-rMod?rMod:L-rMod;
  });
  return {original_modulus:enc(q0),scale:enc(L),remaining_child_modulus:enc(q0/L),candidate_prefix:P.map(enc),radius:enc(R),
    non_wrapping_unique_decoding_regime_4R_lt_L:4n*R<L,complete_wrap_zero_pruning_regime_L_le_2R:L<=2n*R,
    modulo_scale_circular_distances:ds.map(enc),original_records_checked:raw.length,fits_modulo_scale_radius:ds.every(d=>d<=R),
    upper_quotient_annihilated_modulo_scale:true,pruning_soundness_requires_4R_lt_L_and_code_separation:true};
}

function pruneNode(raw,scale0,prefix0,candidates,R0,requireNonWrapping=true){
  const q0=BigInt(raw[0].modulus),n=raw[0].label.length,L=BigInt(scale0),R=BigInt(R0);
  check(R>=0n&&4n*R<q0&&candidates.length>0,"valid node pruning inputs");
  const parentNode=S.canonicalNode(raw,L,prefix0),g=BigInt(parentNode.canonical_node.modulus);
  const evals=[],surviving=new Map(),terminals=[];let checksCount=0,roundings=parentNode.original_response_rounding_evaluations;
  candidates.forEach(([c0,mult0],idx)=>{
    const c=BigInt(c0),mult=mult0.map(x=>enc(mod(BigInt(x),g)));
    const model=M.quotient(g,c,mult),entry={candidate_index:idx,coefficient:c0,multiple:mult};
    if(model===null){evals.push({...entry,status:"REJECTED_INCOMPATIBLE_RING_IMAGE"});return;}
    const x=model.known_quotient_IF_multiple_is_true.map(BigInt),Q=BigInt(model.remaining_modulus),gChild=BigInt(model.nonunit_factor);
    const nextP=parentNode.canonical_node.known_original_lower_prefix_IF_path_true.map((p,i)=>enc(BigInt(p)+L*x[i])),nextL=L*Q;
    Object.assign(entry,{quotient_model:model,candidate_next_scale:enc(nextL),candidate_next_prefix:nextP});
    if(gChild===1n){
      const F=B.complete(raw,1n,nextP,R).unit_fit;checksCount+=raw.length;
      if(F.fits_public_radius){if(!terminals.some(t=>JSON.stringify(t)===JSON.stringify(nextP)))terminals.push(nextP);evals.push({...entry,status:"SURVIVING_TERMINAL_ORIGINAL_FIT",original_fit:F});}
      else evals.push({...entry,status:"PRUNED_BY_FULL_ORIGINAL_RADIUS",original_fit:F});
      return;
    }
    const pfit=moduloScaleFit(raw,nextL,nextP,R);checksCount+=raw.length;entry.modulo_scale_fit=pfit;
    if(requireNonWrapping&&!pfit.non_wrapping_unique_decoding_regime_4R_lt_L){evals.push({...entry,status:"UNPRUNED_WRAPPING_SCALE_4R_GE_L"});return;}
    if(!pfit.fits_modulo_scale_radius){evals.push({...entry,status:"PRUNED_BY_MODULO_SCALE_ORIGINAL_RESIDUAL"});return;}
    const child=S.canonicalNode(raw,nextL,nextP),h=child.canonical_node_sha256,merged=surviving.has(h);
    roundings+=child.original_response_rounding_evaluations;
    if(!merged)surviving.set(h,child);
    evals.push({...entry,status:merged?"MERGED_INTO_EXISTING_CANONICAL_NODE":"SURVIVING_NEW_CANONICAL_NODE",canonical_node_sha256:h});
  });
  return {parent_canonical_node:parentNode.canonical_node,parent_canonical_node_sha256:parentNode.canonical_node_sha256,
    candidates_evaluated:candidates.length,original_modulo_distance_evaluations:checksCount,canonical_node_original_rounding_evaluations:roundings,candidate_evaluations:evals,
    surviving_canonical_child_nodes:Array.from(surviving.values()),surviving_canonical_child_count:surviving.size,
    surviving_terminal_secrets:terminals,require_non_wrapping_4R_lt_L:requireNonWrapping,false_branch_null_assumption_used:false,multiple_producer_supplied:false};
}

function traverse(raw,levelLists,R0){
  const n=raw[0].label.length,R=BigInt(R0),rootNode=S.canonicalNode(raw,1n,Array(n).fill(0));
  let active=new Map([[rootNode.canonical_node_sha256,rootNode]]),totalCands=0,totalDists=0,calls=0,totalRoundings=rootNode.original_response_rounding_evaluations;
  const levels=[],seen=new Set(),terminals=[];
  for(let depth=0;depth<levelLists.length;depth++){
    const next=new Map(),reports=[],list=levelLists[depth];
    for(const [hash,node] of active){
      const g=node.canonical_node.modulus,cands=list[String(g)]||[];if(!cands.length)continue;
      seen.add(hash);calls++;
      const rep=pruneNode(raw,node.canonical_node.original_scale,node.canonical_node.known_original_lower_prefix_IF_path_true,cands,R,true);
      totalCands+=rep.candidates_evaluated;totalDists+=rep.original_modulo_distance_evaluations;reports.push(rep);
      totalRoundings+=rep.canonical_node_original_rounding_evaluations;
      rep.surviving_terminal_secrets.forEach(s=>{if(!terminals.some(t=>JSON.stringify(t)===JSON.stringify(s)))terminals.push(s);});
      rep.surviving_canonical_child_nodes.forEach(child=>next.set(child.canonical_node_sha256,child));
    }
    levels.push({depth_index:depth,expanded_canonical_nodes:reports.length,node_pruning_reports:reports,distinct_surviving_child_nodes:next.size});
    active=next;if(terminals.length||!active.size)break;
  }
  return {status:terminals.length===1?"CANONICAL_PRUNED_DAG_TERMINAL_FIT":"CANONICAL_PRUNED_DAG_INCOMPLETE_OR_AMBIGUOUS",
    original_records_sha256:rootNode.canonical_node.original_records_sha256,original_records_paid_once:raw.length,verification_radius:enc(R),
    levels_traversed:levels.length,level_reports:levels,total_candidates_evaluated:totalCands,total_original_distance_evaluations:totalDists,
    total_canonical_node_original_rounding_evaluations:totalRoundings,
    max_active_canonical_nodes_per_level:levels.length?Math.max(...levels.map(l=>l.distinct_surviving_child_nodes)):0,
    surviving_terminal_secrets:terminals,candidate_secret:terminals.length===1?terminals[0]:null,
    actual_canonical_node_expansion_calls:calls,actual_distinct_canonical_nodes_expanded:seen.size,actual_repeated_canonical_node_expansions:calls-seen.size,
    global_candidate_list_per_node_cache_used:false,unpruned_exponential_tree_elimination_certified_on_observed_bank:false,
    polynomial_work_bound_requires_radius_code_separation_and_scope_events:true,multiple_producer_or_source_law_certified:false};
}

function onePass(raw,candidates,R0){
  const R=BigInt(R0),trials=[],fits=[],models=new Set();let roundings=0,distances=0;
  check(raw.length%2===0,"existing reference parity, not a mathematical source condition");
  candidates.forEach(([c,w])=>{const result=M.complete(raw,BigInt(c),w);roundings+=result.original_response_residual_evaluations;
    if(result.public_basis_model)models.add(String(result.public_basis_model.modulus));
    let fit=null;if(result.candidate_secret!==null){fit=B.complete(raw,1n,result.candidate_secret,R).unit_fit;distances+=raw.length;
      if(fit.fits_public_radius&&!fits.some(s=>JSON.stringify(s)===JSON.stringify(result.candidate_secret)))fits.push(result.candidate_secret);}
    trials.push({coefficient:c,multiple:w,completion:result,original_fit:fit});
  });
  return {original_records_paid_once:raw.length,public_label_rref_calls:1,cached_ring_inversions:models.size,
    original_response_rounding_evaluations:roundings,original_candidate_distance_evaluations:distances,root_trials:trials,fitting_secrets:fits,
    additional_multiple_or_decision_producer_calls:0,Gaussian_flooded_samples_requested:0,reference_API_parity_is_not_a_mathematical_condition:true,
    planted_truth_or_source_law_certified:false};
}

function checkProfile(P){
  const n=P.dimension,r=P.original_root_digits,q0=3n**BigInt(r),m=P.original_rows,alpha=parse(P.alpha_original),C=BigInt(P.declared_centered_coefficient_bound),Blevel=P.candidates_per_expanded_node;
  check(n>0&&r>=2&&m>0&&C>=3n&&Blevel>0&&BigInt(P.original_modulus)===q0&&cmp(alpha,zero)>0n&&cmp(alpha,one)<0n,"valid DAG pruning profile");
  let gMax=1n,dMax=0;while(3n*gMax<=C&&dMax+1<r){gMax*=3n;dMax++;}
  const scaled=mul(rat(8n*q0),alpha),Rgauss=(scaled[0]+scaled[1]-1n)/scaled[1];
  let gPrune=1n,dPrune=0;while(4n*(3n*gPrune)*Rgauss<q0&&dPrune+1<r){gPrune*=3n;dPrune++;}
  const crudeR=q0/BigInt(n);let crudeD=0;while(4n*(3n**BigInt(crudeD+1))*crudeR<q0&&crudeD+1<r)crudeD++;
  const covered=dMax<=dPrune;
  check(P.first_step_max_child_root_digits===dMax&&BigInt(P.first_step_max_child_modulus)===gMax&&BigInt(P.tight_Gaussian_verification_radius)===Rgauss&&P.max_prunable_child_root_digits_under_tight_radius===dPrune&&BigInt(P.max_prunable_child_modulus_under_tight_radius)===gPrune&&P.crude_q_over_n_radius_max_prunable_child_root_digits===crudeD&&P.tight_radius_covers_all_declared_nonunit_children===covered,"tight vs crude radius pruning horizons");
  const O=P.original_Gaussian_radius_law;
  check(O.continuous_Gaussian_width===str(mul(alpha,rat(q0)))&&BigInt(O.integer_error_radius)===Rgauss&&cmp(parse(O.lower),zero)>=0n&&cmp(parse(O.lower),parse(O.upper))<=0n&&cmp(parse(O.upper),one)<=0n,"Gaussian radius enclosure");
  const tail=min(one,mul(rat(BigInt(m)),parse(O.upper)));
  check(P.whole_bank_Gaussian_radius_failure_upper===str(tail),"whole-bank Gaussian tail union");
  check(P.reachable_scale_separation_ledgers.length===Math.min(dMax,dPrune),"reachable non-wrapping scale count");
  let sepSum=zero;
  P.reachable_scale_separation_ledgers.forEach((sl,idx)=>{
    const d=idx+1,L=3n**BigInt(r-d);
    M.separation(sl.modulo_scale_code_separation_ledger);
    check(sl.child_root_digits===d&&BigInt(sl.child_modulus)===3n**BigInt(d)&&BigInt(sl.cumulative_scale_L)===L&&sl.non_wrapping_4R_lt_L===(4n*Rgauss<L)&&BigInt(sl.modulo_scale_code_separation_ledger.original_modulus)===L&&BigInt(sl.modulo_scale_code_separation_ledger.verification_radius)===Rgauss&&sl.modulo_scale_code_separation_ledger.dimension===n&&sl.modulo_scale_code_separation_ledger.original_rows===m,"per-scale code separation ledger");
    sepSum=add(sepSum,parse(sl.modulo_scale_code_separation_ledger.global_code_separation_failure_upper_used));
  });
  M.separation(P.terminal_full_modulus_separation_ledger);
  check(BigInt(P.terminal_full_modulus_separation_ledger.original_modulus)===q0&&BigInt(P.terminal_full_modulus_separation_ledger.verification_radius)===Rgauss&&P.terminal_full_modulus_separation_ledger.dimension===n&&P.terminal_full_modulus_separation_ledger.original_rows===m,"terminal full-modulus separation");
  const sepUnion=min(one,add(sepSum,parse(P.terminal_full_modulus_separation_ledger.global_code_separation_failure_upper_used))),totFail=min(one,add(tail,sepUnion));
  check(P.all_scales_code_separation_failure_union_upper===str(sepUnion)&&P.total_local_pruning_and_radius_failure_upper===str(totFail),"all-scale separation and total failure union");
  const treeLeaves=BigInt(Blevel)**BigInt(Math.max(1,dMax));
  const expansions=1+dMax*(dMax+1)/2;
  check(BigInt(P.unpruned_complete_tree_leaves_at_depth_d_max)===treeLeaves&&P.pruned_canonical_DAG_internal_nodes_upper_IF_covered===(covered?dMax:null)&&P.internal_node_bound_counts_unique_nonroot_nodes_not_expansion_calls===true&&P.pruned_canonical_DAG_expansion_calls_upper_IF_covered===(covered?expansions:null)&&P.pruned_canonical_DAG_candidate_checks_upper_IF_covered===(covered?expansions*Blevel:null)&&P.pruning_eliminates_exponential_tree_IF_4_g_max_R_lt_q0===covered&&P.pruning_supplies_missing_multiple_producer===false&&P.coefficient_bound_derived_from_actual_or_published_producer===false&&P.all_actual_producer_coefficients_covered===false,"unique nodes are not free globally memoized expansion calls; producer scope stays missing");
  check(P.same_successful_pruning_events_imply_exact_one_pass_classical_completion===true&&P.pruning_opens_a_new_completion_regime_beyond_the_one_pass_baseline===false,"same events already support the exact classical baseline");
}

function verify(P){
  check(P.status==="MODULO_SCALE_PREFIX_PRUNING_AND_CANONICAL_DAG_COLLAPSE_AUDIT_REVIEW_PENDING"&&P.producer_sha256===hash(path.join(ROOT,"theorems/native_prefix_ambiguity_pruning.py"))&&P.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_PREFIX_AMBIGUITY_PRUNING.md")),"current producer and derivation");
  const deps=["native_affine_fibre_relaxation.py","native_basis_lottery.py","native_classical_modulus_descent.py","native_gaussian_quotient_completion.py","native_small_multiple_completion.py","native_source_refresh.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(P.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");deps.forEach(f=>check(P.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(P.actual_dag_pruning_controls.length===2&&P.Gaussian_DAG_pruning_profiles.length===3,"declared live scope");
  let replayedCandidateChecks=0,replayedDistanceChecks=0;
  P.actual_dag_pruning_controls.forEach(C=>{
    const raw=C.original_records,q0=BigInt(raw[0].modulus),s=C.original_secret_FOR_CALIBRATION_ONLY.map(BigInt),e=C.original_errors_FOR_CALIBRATION_ONLY.map(BigInt),D=C.dag_traversal,R=BigInt(D.verification_radius);
    raw.forEach((r,j)=>check(mod(r.label.reduce((v,a,i)=>v+BigInt(a)*s[i],0n)+e[j],q0)===BigInt(r.value),"actual calibration observations"));
    let totalCands=0,totalDists=0;
    D.level_reports.forEach(lv=>{
      check(lv.expanded_canonical_nodes===lv.node_pruning_reports.length,"expanded node count");
      const nextHashes=new Set();
      lv.node_pruning_reports.forEach(rep=>{
        const scale=rep.parent_canonical_node.original_scale,prefix=rep.parent_canonical_node.known_original_lower_prefix_IF_path_true;
        const cands=rep.candidate_evaluations.map(ev=>[ev.coefficient,ev.multiple]);
        const replayed=pruneNode(raw,scale,prefix,cands,R,true);
        same(rep,replayed,"independent node pruning and canonical merge replay");
        totalCands+=replayed.candidates_evaluated;totalDists+=replayed.original_modulo_distance_evaluations;
        replayed.surviving_canonical_child_nodes.forEach(ch=>nextHashes.add(ch.canonical_node_sha256));
      });
      check(lv.distinct_surviving_child_nodes===nextHashes.size,"distinct surviving canonical nodes");
    });
    same(D,traverse(raw,C.supplied_level_candidate_lists,R),"whole graph reachability, supplied lists, repeated expansion work and stopping rule");
    const baseline=onePass(raw,C.supplied_level_candidate_lists[0][String(q0)],R);
    same(C.one_pass_classical_root_comparison,baseline,"ALL root hypotheses compared against same-original one-pass classical completion");
    same(baseline.fitting_secrets,[C.original_secret_FOR_CALIBRATION_ONLY],"no new completion power or extra producer supplied by safe prefix recursion");
    check(D.total_candidates_evaluated===totalCands&&D.total_original_distance_evaluations===totalDists&&D.unpruned_exponential_tree_elimination_certified_on_observed_bank===false&&D.multiple_producer_or_source_law_certified===false,"conditional DAG work totals are not source certificates");
    same(D.candidate_secret,C.original_secret_FOR_CALIBRATION_ONLY,"unique terminal fit matches calibration secret");
    check(C.matches_truth_after_solving===true&&C.actual_multiple_producer_supplied===false,"calibration honesty flags");
    replayedCandidateChecks+=totalCands;replayedDistanceChecks+=totalDists;
  });
  P.Gaussian_DAG_pruning_profiles.forEach(checkProfile);
  const F=P.wrap_around_falsifiers,w1=F.complete_wrap_L_le_2R_falsifier,w2=F.half_modulus_collision_2R_lt_L_le_4R_falsifier;
  check(w1.scale===3&&w1.radius===2&&w1.all_tested_prefixes_fit_trivially===true&&w1.pruner_refuses_wrapping_scale===true&&w1.surviving_canonical_child_count===0,"L<=2R complete wrap falsifier");
  check(w2.scale===9&&w2.radius===3&&w2.non_wrapping_4R_lt_L===false&&w2.true_prefix_fits===true&&w2.colliding_wrong_prefix_also_fits===true&&w2.four_R_lt_L_is_sufficient_scope_not_instance_necessity===true,"2R<L<=4R collision witness, not universal instance necessity");
  const X=P.scope_and_revisit_countercontrols,V=X.canonical_node_revisited_at_different_depths,U=X.unique_instance_outside_nonwrapping_proof_scope;
  same(V.original_records,[{label:[1],value:5,modulus:81,source_id:"repeated-node"}],"unit-label zero-error revisit control");
  const revisited=traverse(V.original_records,V.supplied_level_candidate_lists,0n);same(V.dag_traversal,revisited,"actual canonical-node revisit control");
  check(revisited.total_candidates_evaluated===8&&revisited.actual_canonical_node_expansion_calls===4&&revisited.actual_distinct_canonical_nodes_expanded===3&&V.claimed_old_linear_candidate_bound===6&&V.actual_candidate_checks_exceed_old_bound===true&&V.different_depth_lists_must_not_be_silently_cached_as_one_list===true,"old linear work bound independently falsified");
  same(U.original_records,Array.from({length:27},(_,a)=>({label:[a],value:a*5%81,modulus:81,source_id:`nonnecessary:${a}`})),"complete scale27 zero-error label population");
  const fits=Array.from({length:27},(_,p)=>p).filter(p=>moduloScaleFit(U.original_records,27,[p],7).fits_modulo_scale_radius);
  same(U.compatible_prefixes,fits,"complete original-prefix fit census");same(fits,[5],"unique observed fit despite failed sufficient proof gate");
  check(U.scale===27&&U.radius===7&&U.complete_prefixes_checked===27&&U.four_R_lt_L===false&&U.proof_gate_is_not_a_general_instance_impossibility_claim===true,"nonwrapping scope is sufficient, not necessary on all instances");
  check(P.accepted_speedup_candidate===false&&P.new_active_negative_result_created===false&&P.actual_quantum_decision_or_multiple_producer===false&&P.complete_recursive_search_to_decision_reduction_established===false&&P.novelty_claim===false,"no unproved reduction or speedup admitted");
  check(P.research_decision==="KEEP_PREFIX_PRUNING_AS_AUDIT_WHERE_ONE_PASS_CLASSICAL_COMPLETION_ALREADY_SUFFICES","deprioritize classically dominated safe prefix recursion");
  return {verified:true,dag_controls:2,replayed_candidate_checks:replayedCandidateChecks,replayed_distance_checks:replayedDistanceChecks,gaussian_profiles:3,multiple_producer_supplied:false};
}
module.exports={verify,moduloScaleFit,pruneNode,traverse,checkProfile};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));

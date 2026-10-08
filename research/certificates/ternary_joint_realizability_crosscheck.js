"use strict";
// Replays the original source, PSD gap and ALL local native inequalities first.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {local}=require("./ternary_local_marginals_crosscheck.js");
const {support,objective,supportResult}=require("./ternary_psd_support_lift_crosscheck.js");
const {primal,matrix,positivity,appendCut,dual}=require("./ternary_moment_psd_crosscheck.js");
const {exactFace,mix,separator}=require("./ternary_moment_psd_mixtures_crosscheck.js");
const {check,sameSet,prepare,geometry,momentModel,report,load}=require("./ternary_prefix_integrality_crosscheck.js");
const joint=load("ternary_joint_realizability"),sources={local:"ternary_local_marginals",support:"ternary_psd_support_lift",prefix:"ternary_prefix_integrality",fixture:"ternary_pair_cell_coverage"};
for(const[key,name]of Object.entries(sources)){
  const bytes=fs.readFileSync(path.join(__dirname,"../phase_workbench/"+name+".json"));
  check(crypto.createHash("sha256").update(bytes).digest("hex")===joint.source_sha256[key],"all joint source reports hash-pinned");
}
check(!joint.novelty_claim&&!joint.polynomial_pair_finder_proved&&!joint.population_gap_proved,"joint audit not algorithm/population result");
check(joint.hull_denominator===8&&joint.hull_exact_candidate_budget===8&&joint.support_tests_per_case_budget===1&&joint.support_hull_refinement_budget===1,"explicit bounded hull/support schedule");
let cases=0,localCuts=0,PSDCuts=0,LPcalls=0,negativeForms=0,hullChecks=0,positiveHullChecks=0,jointGaps=0,globalObstructions=0,unknowns=0;
function hull(model,certs,h){
  const points=certs.map(c=>matrix(model,primal(model,c,c.required_winding))),C=exactFace(model,points,h.face);
  check(h.cost.point_count===certs.length&&h.cost.exact_psd_checks===h.attempts.length&&h.attempts.length<=joint.hull_exact_candidate_budget&&!h.full_SDP_infeasibility_proved&&!h.global_native_distribution_proved,"finite joint hull, not full model");
  let positive=false;for(let i=0;i<h.attempts.length;i++){
    const a=h.attempts[i];if(positivity(mix(C,a.weights),a.compressed_positivity)){positive=true;positiveHullChecks++;check(i===h.attempts.length-1,"stop after exact positive mixture");}hullChecks++;
  }
  if(positive)check(h.status==="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF"&&h.matrix_psd_from_exact_face_and_compressed_LDL,"exact positive hull flag");
  else if(h.status==="EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION")separator(C,h.hull_separator);
  else check(h.status==="CONVEX_HULL_PSD_SEARCH_UNKNOWN"||h.status==="CONVEX_PSD_GRID_PREFLIGHT_UNKNOWN","negative mixture cap not full infeasibility");
  return positive;
}
sameSet(joint.cases.map(c=>[c.fixture_probe_index,c.target,c.winding_branch]),local.cases.filter(c=>c.cut_resolve.analysis&&c.cut_resolve.analysis.primal).map(c=>[c.fixture_probe_index,c.target,c.winding_branch]),"ALL exact strengthened local continuations tested");
for(const c of joint.cases){
  const lc=local.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index&&x.target===c.target&&x.winding_branch===c.winding_branch),pc=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),pt=pc.trials.find(x=>x.target===c.target);
  check(c.fingerprint===pc.fingerprint&&c.local_cut_count===lc.cut_resolve.cuts.length,"same original source and complete local-cut count");
  const g=geometry(prepare(pc),BigInt(c.target),pt.frontier),base=momentModel(g,c.winding_branch);
  for(const[i,cut]of lc.cut_resolve.cuts.entries()){
    check(cut.slack_variable===base.variables.length,"same certified local slack ordering");
    const row=new Map(Object.entries(cut.integer_coefficients).map(([j,a])=>[Number(j),BigInt(a)]));row.set(base.variables.length,-1n);
    base.variables.push(["LOCAL_SLACK",i]);base.E.push(row);base.B.push(0n);localCuts++;
  }
  const initial=lc.cut_resolve.analysis.primal,N=base.variables.length,model={...base,E:base.E.map(row=>new Map(row)),B:[...base.B],variables:base.variables.map(k=>[...k])},points=[initial];
  const loop=c.loop;check(loop.required_winding===c.winding_branch&&loop.cut_budget===joint.PSD_cut_budget&&loop.cuts_added<=loop.cut_budget&&!loop.integer_prefix_completion_proved,"bounded fixed-winding PSD loop");
  let applied=0,terminal="",calls=0;
  for(let i=0;i<loop.steps.length;i++){
    const step=loop.steps[i],a=step.analysis;calls+=a.cost.LP_calls;let cert=a.primal;
    if(i===0){check(a.primal_from_local_report===true&&cert===null&&a.cost.LP_calls===0,"initial exact proof reused ONLY from local report");cert=initial;}
    else check(!a.primal_from_local_report&&a.cost.variables===model.variables.length&&a.cost.equations===model.E.length,"every mixed-model resolve retains ALL local and PSD rows/slacks");
    if(a.dual){check(!step.positivity&&!step.added_cut,"mixed-model dual not a point proof");dual(model,a.dual,c.winding_branch);terminal="EXACT_VALID_PSD_CUT_OBSTRUCTION";}
    else if(cert){const p=primal(model,cert,c.winding_branch),M=matrix(model,p),positive=positivity(M,step.positivity);
      if(i){const truncated={...cert,moments:cert.moments.slice(0,N)};primal(base,truncated,c.winding_branch);points.push(truncated);}
      if(positive){check(!step.added_cut,"positive point not cut off");terminal="EXACT_PSD_CONTINUATION_NOT_NATIVE";}
      else if(step.added_cut){check(applied<loop.cut_budget,"no PSD cut past cap");
        base.variables.forEach((key,j)=>{if(key[0]==="LOCAL_SLACK")check(step.added_cut.integer_coefficients[j]==="0","local slacks NEVER enter indicator squares");});
        appendCut(model,M,step.added_cut,step.positivity.negative.vector);applied++;PSDCuts++;negativeForms++;
      }else{check(applied===loop.cut_budget,"negative point only terminal at explicit cap");terminal="PSD_CUT_CAP_UNKNOWN";negativeForms++;}
    }else{check(!step.positivity&&!step.added_cut,"unknown not PSD/global obstruction");terminal="PSD_CUT_RECONSTRUCTION_UNKNOWN";}
    if(terminal)check(i===loop.steps.length-1,"no continuation past terminal result");
  }
  check(loop.status===terminal&&loop.steps.length===applied+1&&loop.cuts_added===applied&&loop.LP_calls===calls,"complete mixed cut/resolve ledger");LPcalls+=calls;
  let positiveHull=false,supportObstruction=false;
  if(c.hull)positiveHull=hull(base,points,c.hull);
  if(c.support){check(c.hull&&c.hull.hull_separator&&c.support_objective,"support ONLY after exact hull SOS obstruction");
    const obj=objective(base,c.support_objective,c.hull,c.winding_branch);supportResult(base,obj,c.support,c.winding_branch);LPcalls+=c.support.cost.LP_calls;supportObstruction=!!c.support.dual;
    if(c.refined_hull){check(c.support.escape,"refine only with exact jointly valid escape");const escaped={...c.support.escape,moments:c.support.escape.moments.slice(0,N)};primal(base,escaped,c.winding_branch);positiveHull=hull(base,[...points,escaped],c.refined_hull)||positiveHull;}
  }else check(!c.support_objective&&!c.refined_hull,"no invented support/refinement result");
  check(!c.whole_prefix_infeasibility_proved,"ONE winding, not entire prefix");
  if(c.joint_gap_point){const p=primal(base,c.joint_gap_point.primal,c.winding_branch);check(positivity(matrix(base,p),c.joint_gap_point.positivity),"retained whole-model joint point has exact ORIGINAL matrix LDL");
    check(c.status==="EXACT_NATIVE_JOINT_LOCAL_PSD_RELAXATION_GAP"&&!c.full_joint_PSD_infeasibility_proved&&c.native_empty_from_original_prefix_report&&pt.status==="EXACT_WINDING_PREFIX_INTEGRALITY_GAP"&&pt.native_truth.native_prefix_words.length===0&&!c.joint_gap_point.global_native_distribution_proved,"native joint GAP needs independently replayed original emptiness");jointGaps++;
  }else if(c.full_joint_PSD_infeasibility_proved){check(c.status==="EXACT_FIXED_WINDING_JOINT_PSD_OBSTRUCTION"&&(terminal==="EXACT_VALID_PSD_CUT_OBSTRUCTION"||supportObstruction),"no full joint obstruction without exact dual");globalObstructions++;}
  else{check(c.status==="JOINT_LOCAL_PSD_AUDIT_UNKNOWN"&&!positiveHull,"bounded joint unknown not infeasible");unknowns++;}cases++;
}
console.log(JSON.stringify({status:"independent_joint_native_local_PSD_checks_passed",cases,localCuts,PSDCuts,LPcalls,negativeForms,hullChecks,positiveHullChecks,jointGaps,globalObstructions,unknowns,wholePrefixInfeasibilityProved:false,populationGapProved:false}));
module.exports={joint};

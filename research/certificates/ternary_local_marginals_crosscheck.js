"use strict";
// The imported checker FIRST verifies PSD/native gap and its full source chain.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {support}=require("./ternary_psd_support_lift_crosscheck.js");
const {primal,matrix,positivity}=require("./ternary_moment_psd_crosscheck.js");
const {check,gcd,F,fraction,commonIntegers,sameSet,prepare,geometry,momentModel,report,load}=require("./ternary_prefix_integrality_crosscheck.js");
const local=load("ternary_local_marginals"),bytes=fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_psd_support_lift.json"));
check(crypto.createHash("sha256").update(bytes).digest("hex")===local.source_support_report_sha256,"local probes pinned to verified PSD gap");
check(!local.novelty_claim&&!local.polynomial_pair_finder_proved&&!local.global_distribution_proved&&!local.population_gap_proved,"no population or algorithm claim");
const same=(a,b,message)=>check(JSON.stringify(a)===JSON.stringify(b),message);
const fractionEq=(a,d,s)=>{const q=fraction(s);return a*q[1]===q[0]*d;};
function triples(M){const out=[];for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(let k=j+1;k<M;k++)out.push([i,j,k]);return out;}
function projection(model,g,point,blocks){
  const assignments=[];for(const a of g.domains[blocks[0]])for(const b of g.domains[blocks[1]])for(const c of g.domains[blocks[2]])assignments.push([a,b,c]);
  const lookup=new Map(model.variables.map((key,i)=>[JSON.stringify(key),i])),rows=[],indices=[];
  for(const[i,j]of [[0,1],[0,2],[1,2]])for(const a of g.domains[blocks[i]])for(const b of g.domains[blocks[j]]){
    rows.push(assignments.map(w=>w[i]===a&&w[j]===b?1n:0n));indices.push(lookup.get(JSON.stringify(["J",blocks[i],a,blocks[j],b])));
  }
  check(indices.every(j=>j!==undefined),"all original retained pair variables present");return {assignments,rows,indices};
}
let triplesChecked=0,extensions=0,obstructions=0,unknowns=0,localLPcalls=0,cuts=0,resolves=0,newPrimalProofs=0,newDualProofs=0;
function localDual(p,point,cert,winding){
  check(cert.valid&&cert.required_winding===winding&&cert.proves_no_three_block_extension&&!cert.proves_no_full_moment_PSD_point,"local obstruction, not entire PSD space");
  same(cert.pair_variable_indices,p.indices,"correct original pair-moment ordering");
  const q=commonIntegers(cert.pair_marginal_multipliers),y=q.values;check(y.length===p.rows.length,"complete exact local dual");
  const columns=p.assignments.map((_,j)=>p.rows.reduce((s,row,i)=>s+row[j]*y[i],0n));
  check(columns.length===cert.exact_assignment_coefficients.length&&columns.every((a,j)=>a>=0n&&fractionEq(a,q.den,cert.exact_assignment_coefficients[j])),"EVERY local original native assignment satisfies inequality");
  const rhs=p.indices.reduce((s,j,i)=>s+y[i]*point.x[j],0n);check(rhs<0n&&fractionEq(rhs,q.den*point.den,cert.exact_gap_point_value),"exact strict negative value at saved PSD gap");return q;
}
function globalDual(model,cert,winding){
  check(cert.valid&&cert.required_winding===winding&&cert.proves_no_coupled_moments,"exact full cut-model dual");
  const q=commonIntegers(cert.signed_equation_multipliers);check(q.values.length===model.E.length,"ALL original and local cut equations retained");
  const column=Array(model.variables.length).fill(0n);let rhs=0n;
  for(let i=0;i<q.values.length;i++){rhs+=q.values[i]*model.B[i];for(const[j,a]of model.E[i])column[j]+=q.values[i]*a;}
  check(column.length===cert.exact_column_coefficients.length&&column.every((a,j)=>a>=0n&&fractionEq(a,q.den,cert.exact_column_coefficients[j])),"all original and local SLACK columns nonnegative");
  check(rhs<0n&&fractionEq(rhs,q.den,cert.exact_combined_rhs),"global strict contradiction using native-valid local cuts");newDualProofs++;
}
const expected=support.cases.flatMap(c=>c.trials.flatMap(t=>t.winding_trials.filter(r=>r.PSD_native_gap_certificate).map(r=>[c.fixture_probe_index,t.target,r.winding_branch])));
sameSet(local.cases.map(c=>[c.fixture_probe_index,c.target,c.winding_branch]),expected,"all certified PSD gaps, no favorable selection");
for(const c of local.cases){
  const pc=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),sc=support.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),pt=pc.trials.find(x=>x.target===c.target),st=sc.trials.find(x=>x.target===c.target),sr=st.winding_trials.find(x=>x.winding_branch===c.winding_branch);
  check(c.fingerprint===pc.fingerprint,"original source fingerprint");const g=geometry(prepare(pc),BigInt(c.target),pt.frontier),model=momentModel(g,c.winding_branch),point=primal(model,sr.PSD_native_gap_certificate.moment_certificate,c.winding_branch);
  check(c.block_count===g.base.M&&c.complete_triple_schedule&&c.gap_PSD_rechecked_exactly,"complete original block count and exact upstream PSD recheck");same(c.triple_trials.map(t=>t.blocks),triples(c.block_count),"EVERY original triple in lexicographic order");
  const dualTrials=[];
  for(const t of c.triple_trials){const p=projection(model,g,point,t.blocks);check(t.cost.assignments===p.assignments.length&&t.cost.pair_marginal_rows===p.rows.length,"actual local problem sizes charged");localLPcalls+=t.cost.LP_calls;
    if(t.extension){check(!t.dual&&t.status==="EXACT_THREE_BLOCK_EXTENSION_NOT_GLOBAL"&&t.extension.valid&&t.extension.required_winding===c.winding_branch&&!t.extension.global_native_realization_proved,"local extension is not global recovery");
      const q=commonIntegers(t.extension.assignment_probabilities);check(q.values.length===p.assignments.length&&q.values.every(a=>a>=0n)&&q.values.reduce((a,b)=>a+b,0n)===q.den,"complete normalized exact triple distribution");
      for(let i=0;i<p.rows.length;i++){const value=p.rows[i].reduce((s,a,j)=>s+a*q.values[j],0n);check(value*point.den===point.x[p.indices[i]]*q.den,"all THREE pair marginal tables match exactly");}extensions++;
    }else if(t.dual){check(t.status==="EXACT_NONPSD_THREE_BLOCK_OBSTRUCTION","no dual from failed numerical status");localDual(p,point,t.dual,c.winding_branch);dualTrials.push(t);obstructions++;}
    else{check(t.status==="THREE_BLOCK_EXACT_RECONSTRUCTION_UNKNOWN","unverified triple remains unknown");unknowns++;}triplesChecked++;
  }
  check(c.nonPSD_local_obstructions===dualTrials.length&&c.all_triples_extend_exactly===c.triple_trials.every(t=>!!t.extension),"complete triple conclusion, not partial feasibility");
  const r=c.cut_resolve;check(r.cut_budget===local.local_cut_budget&&r.available_obstructions===dualTrials.length&&!r.whole_prefix_infeasibility_proved,"explicit cut cap, not whole prefix");
  check(r.cuts.length===Math.min(dualTrials.length,r.cut_budget),"deterministic bounded first-cut schedule");
  for(let i=0;i<r.cuts.length;i++){
    const cut=r.cuts[i],t=dualTrials[i],p=projection(model,g,point,t.blocks),q=localDual(p,point,t.dual,c.winding_branch);
    same(cut.blocks,t.blocks,"exact originating triple");same(cut.pair_marginal_multipliers,t.dual.pair_marginal_multipliers,"certified originating multipliers");
    const divisor=q.values.reduce(gcd,0n),row=new Map();p.indices.forEach((j,l)=>{const a=q.values[l]/divisor;if(a)row.set(j,(row.get(j)||0n)+a);});
    const saved=Object.fromEntries([...row].filter(([,a])=>a).map(([j,a])=>[String(j),String(a)]));same(cut.integer_coefficients,saved,"primitive integer native-valid cut, ALL pair columns");
    check(cut.clearing_denominator===String(q.den)&&cut.primitive_divisor===String(divisor)&&cut.slack_variable===model.variables.length,"exact local-cut normalization and nonnegative slack");
    row.set(model.variables.length,-1n);model.E.push(row);model.B.push(0n);model.variables.push(["LOCAL_SLACK",i]);cuts++;
  }
  if(r.cuts.length){const a=r.analysis;check(a&&a.cost.variables===model.variables.length&&a.cost.equations===model.E.length,"re-solved whole strengthened model");
    check(!r.ordinary_two_witness_recovery_proved&&r.full_base_plus_selected_local_cuts_infeasible===!!a.dual,"no unproved native recovery");
    if(a.primal){primal(model,a.primal,c.winding_branch);positivity(matrix(model,primal(model,a.primal,c.winding_branch)),r.primal_positivity);newPrimalProofs++;}
    else if(a.dual)globalDual(model,a.dual,c.winding_branch);
    else check(a.status==="PRIMAL_PROPOSAL_NO_EXACT_CERTIFICATE"||a.status==="COUPLED_MOMENT_ANALYSIS_UNKNOWN","bounded re-solve unknown not infeasible");resolves++;
  }else check(!r.analysis,"no unsupported resolve after zero cuts");
}
console.log(JSON.stringify({status:"independent_native_three_block_marginals_and_cut_resolve_checks_passed",triplesChecked,extensions,obstructions,unknowns,localLPcalls,cuts,resolves,newPrimalProofs,newDualProofs,wholePrefixInfeasibilityProved:false,populationGapProved:false}));
module.exports={local};

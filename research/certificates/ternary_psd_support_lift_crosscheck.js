"use strict";
// Replays source geometry and the earlier hull proofs before global support.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {mixtures,exactFace,mix,separator}=require("./ternary_moment_psd_mixtures_crosscheck.js");
const {primal,matrix,positivity,psd,moments}=require("./ternary_moment_psd_crosscheck.js");
const {check,gcd,abs,F,fraction,commonIntegers,sameSet,prepare,geometry,momentModel,report,load}=require("./ternary_prefix_integrality_crosscheck.js");
const support=load("ternary_psd_support_lift");
const sources={hull:"ternary_moment_psd_mixtures",psd:"ternary_moment_psd",moment:"ternary_prefix_moments",prefix:"ternary_prefix_integrality",fixture:"ternary_pair_cell_coverage"};
for(const[key,name]of Object.entries(sources)){
  const bytes=fs.readFileSync(path.join(__dirname,"../phase_workbench/"+name+".json"));
  check(crypto.createHash("sha256").update(bytes).digest("hex")===support.source_sha256[key],"every support source is hash-pinned");
}
check(!support.novelty_claim&&!support.population_obstruction_proved&&!support.polynomial_pair_finder_proved,"support results not algorithms");
const same=(a,b,message)=>check(JSON.stringify(a)===JSON.stringify(b),message);
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),twice=a=>mul(F(2n),a);
const fractionEq=(a,d,s)=>{const q=fraction(s);return a*q[1]===q[0]*d;};
let functionals=0,escapes=0,globalObstructions=0,unknowns=0,negativeEscapes=0,positiveEscapes=0,LPcalls=0,expandedHulls=0,expandedHullObstructions=0,expandedHullUnknowns=0,positiveExpandedHulls=0,nativePSDGaps=0;
check(support.hull_refinement_round_budget===1&&support.refinement_grid_denominator===8&&support.refinement_exact_candidate_budget===8,"explicit ONE source-aware refinement, no hidden loops");
function objective(model,record,saved,winding){
  const indicators=model.variables.filter(key=>key[0]==="p"),n=indicators.length+1,free=saved.face.free_indices,c=saved.hull_separator.certificate;
  check(record.required_winding===winding&&!record.hull_specific_constraints_added,"same winding, NO hull constraints");
  same(record.principal_indices,free,"same principal coordinates");same(record.nonnegative_weights,c.nonnegative_weights,"original exact positive SOS weights");
  const full=c.vectors.map(v=>{check(v.length===free.length,"complete saved compressed vector");const out=Array(n).fill("0");free.forEach((i,j)=>{out[i]=v[j];});return out;});
  same(record.embedded_vectors,full,"ZERO embedding, not the hull-specific reconstruction T");
  const weights=c.nonnegative_weights.map(fraction),vectors=full.map(v=>v.map(fraction));
  check(weights.length===vectors.length&&weights.every(w=>w[0]>=0n)&&weights.reduce(add,F(0n)).toString()===F(1n).toString(),"nonnegative normalized SOS");
  const lookup=new Map(indicators.map((key,i)=>[JSON.stringify(key),i+1]));
  const coefficients=model.variables.map(key=>{
    if(key[0]!=="p"&&key[0]!=="J"){
      check(record.allow_slacks===true&&record.support_model_scope==="SUPPLIED_MODEL_WITH_EXPLICIT_NONNEGATIVE_SLACKS"&&(key[0]==="LOCAL_SLACK"||key[0]==="PSD_SLACK"),"explicit nonnegative slack-model support scope");return F(0n);
    }
    const i=lookup.get(JSON.stringify(key[0]==="p"?key:["p",key[1],key[2]]));
    const j=key[0]==="J"?lookup.get(JSON.stringify(["p",key[3],key[4]])):null;
    return vectors.reduce((s,v,l)=>weights[l][0]===0n?s:add(s,mul(weights[l],key[0]==="p"?add(twice(mul(v[0],v[i])),mul(v[i],v[i])):twice(mul(v[i],v[j])))),F(0n));
  });
  const constant=vectors.reduce((s,v,l)=>weights[l][0]===0n?s:add(s,mul(weights[l],mul(v[0],v[0]))),F(0n));
  const all=[...coefficients,constant],D=all.reduce((d,q)=>d/gcd(d,q[1])*q[1],1n),ints=all.map(q=>q[0]*(D/q[1])),d=ints.reduce(gcd,0n);
  check(d>0n,"nontrivial exact objective");const cs=ints.map(a=>a/d),k=cs.pop();
  same(record.integer_coefficients,cs.map(String),"ALL original SOS objective columns");
  check(record.integer_constant===String(k)&&record.clearing_denominator===String(D)&&record.primitive_divisor===String(d),"exact positive normalization");
  check(record.maximum_integer_coefficient_bits===[...cs,k].reduce((b,x)=>Math.max(b,x===0n?0:abs(x).toString(2).length),0),"objective bit complexity charged");
  functionals++;return {c:cs,k,D,d};
}
function evaluate(obj,p){return obj.k*p.den+obj.c.reduce((s,a,j)=>s+a*p.x[j],0n);}
function supportDual(model,obj,cert,winding){
  check(cert&&cert.valid&&cert.required_winding===winding&&cert.full_degree_two_SDP_infeasibility_proved&&!cert.whole_prefix_infeasibility_proved,"fixed-winding exact support dual, not whole prefix");
  const {den,values:y}=commonIntegers(cert.signed_equation_multipliers);check(y.length===model.E.length,"complete original dual multiplier array");
  const slack=obj.c.map(c=>-c*den);let upper=obj.k*den;
  for(let i=0;i<y.length;i++){upper+=y[i]*model.B[i];if(y[i])for(const[j,a]of model.E[i])slack[j]+=a*y[i];}
  check(slack.length===cert.exact_column_slacks.length&&slack.every((s,j)=>s>=0n&&fractionEq(s,den,cert.exact_column_slacks[j])),"EVERY column E^T y >= c, not float tolerance");
  check(upper<0n&&fractionEq(upper,den,cert.exact_functional_upper_bound),"exact GLOBAL strictly negative support bound");globalObstructions++;
}
function supportResult(model,obj,run,k){
  check(run.cost.variables===model.variables.length&&run.cost.equations===model.E.length&&run.cost.exact_reconstruction_cells_budget===support.max_exact_reconstruction_cells,"same full base model and exact preflight");LPcalls+=run.cost.LP_calls;
  check(!run.whole_prefix_infeasibility_proved,"support is not whole-prefix solver");
  if(run.status==="EXACT_BASE_MOMENT_ESCAPE_FROM_HULL_DUAL"){
    check(run.escape&&!run.dual&&!run.full_degree_two_SDP_infeasibility_proved&&run.escape.proves_escape_from_THIS_dual_only&&!run.escape.matrix_PSD_proved,"escape only THIS functional, not PSD");
    const p=primal(model,run.escape,k),value=evaluate(obj,p);check(value>=0n&&fractionEq(value,p.den,run.escape.exact_functional_value),"complete EXACT base-point escape");
    if(positivity(matrix(model,p),run.escape_positivity))positiveEscapes++;else negativeEscapes++;escapes++;return p;
  }else if(run.status==="EXACT_GLOBAL_DEGREE_TWO_PSD_OBSTRUCTION"){
    check(!run.escape&&run.full_degree_two_SDP_infeasibility_proved,"only exact global support bound excludes full SDP");supportDual(model,obj,run.dual,k);
  }else{check(run.status==="GLOBAL_PSD_SUPPORT_RECONSTRUCTION_UNKNOWN"&&!run.escape&&!run.dual&&!run.full_degree_two_SDP_infeasibility_proved,"numerical failures stay UNKNOWN");unknowns++;}
  return null;
}
sameSet(support.cases.flatMap(c=>c.trials.map(t=>[c.fixture_probe_index,t.target])),mixtures.cases.flatMap(c=>c.trials.map(t=>[c.fixture_probe_index,t.target])),"same complete prefix schedule");
for(const c of support.cases){
  const pc=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),hc=mixtures.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),mc=moments.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),sc=psd.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index);
  check(pc&&hc&&mc&&sc&&c.fingerprint===pc.fingerprint,"same original source");const base=prepare(pc);
  for(const t of c.trials){
    const pt=pc.trials.find(x=>x.target===t.target),ht=hc.trials.find(x=>x.target===t.target),mt=mc.trials.find(x=>x.target===t.target),st=sc.trials.find(x=>x.target===t.target),g=geometry(base,BigInt(t.target),pt.frontier);
    sameSet(t.all_allowed_windings,g.windings,"all allowed windings retained even when not optimized");
    sameSet(t.winding_trials.map(r=>r.winding_branch),ht.winding_trials.filter(r=>r.status==="EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION").map(r=>r.winding_branch),"exactly all four saved hull duals tested");
    check(!t.prefix_eliminated&&t.old_winding_unknowns_not_resolved,"other winding unknowns preserved");
    for(const run of t.winding_trials){
      const k=run.winding_branch,model=momentModel(g,k),hr=ht.winding_trials.find(r=>r.winding_branch===k),mr=mt.winding_trials.find(r=>r.winding_branch===k),sr=st.winding_trials.find(r=>r.winding_branch===k),obj=objective(model,run.objective,hr,k),N=model.variables.length;
      const certs=[mr.primal,...sr.steps.slice(1).map(s=>s.analysis.primal).filter(Boolean)];
      check(run.old_hull_functional_values.length===certs.length,"all old negative vertices verified");
      certs.forEach((cert,i)=>{const p=primal(model,{...cert,moments:cert.moments.slice(0,N)},k),value=evaluate(obj,p),trace=fraction(hr.hull_separator.certificate.point_trace_values[i]);
        check(value<0n&&fractionEq(value,p.den,run.old_hull_functional_values[i])&&value*trace[1]*obj.d===trace[0]*obj.D*p.den,"old traces equal zero-embedded original functional");});
      const escaped=supportResult(model,obj,run,k);
      if(escaped){
        const r=run.refinement,h=r.expanded_hull;check(r.refinement_rounds===1,"one refinement per actual escape");
        const points=[...certs.map(c=>matrix(model,primal(model,{...c,moments:c.moments.slice(0,N)},k))),matrix(model,escaped)],C=exactFace(model,points,h.face);
        check(h.cost.point_count===points.length&&h.attempts.length===h.cost.exact_psd_checks&&h.attempts.length<=support.refinement_exact_candidate_budget&&!h.full_SDP_infeasibility_proved&&!h.global_native_distribution_proved,"expanded hull is still not full moment model");
        let positive=false;for(let i=0;i<h.attempts.length;i++){
          const a=h.attempts[i];check(a.weights.map(fraction).every(q=>(q[0]*8n)%q[1]===0n),"fixed refined grid");
          if(positivity(mix(C,a.weights),a.compressed_positivity)){positive=true;check(i===h.attempts.length-1,"stop on positive mixture");same(a.weights,h.exact_convex_weights,"positive mixture weights retained");}
        }
        if(positive){check(h.status==="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF"&&!r.next_objective&&!r.next_support,"positive expanded hull still not integer/native realization");positiveExpandedHulls++;
          const gap=run.PSD_native_gap_certificate;check(gap&&gap.PSD_proof_is_expanded_hull_exact_face_and_LDL&&gap.native_prefix_empty_from_independently_checked_original_report&&gap.proves_degree_two_gap_for_THIS_prefix_winding&&!gap.population_gap_or_general_hierarchy_lower_bound_proved&&pt.status==="EXACT_WINDING_PREFIX_INTEGRALITY_GAP"&&pt.native_truth.native_prefix_words.length===0,"native GAP needs independently replayed original-prefix emptiness");
          const p=primal(model,gap.moment_certificate,k),input=[...certs.map(c=>primal(model,{...c,moments:c.moments.slice(0,N)},k)),escaped],w=h.exact_convex_weights.map(fraction);
          for(let j=0;j<N;j++){const value=input.reduce((s,x,i)=>add(s,mul(w[i],F(x.x[j],x.den))),F(0n));check(fractionEq(p.x[j],p.den,value[1]===1n?String(value[0]):value[0]+"/"+value[1]),"every retained PSD-gap moment equals the exact positive mixture");}
          nativePSDGaps++;
        }
        else if(h.status==="EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION"){
          separator(C,h.hull_separator);expandedHullObstructions++;
          const next=objective(model,r.next_objective,h,k);supportResult(model,next,r.next_support,k);
        }else{check(h.status==="CONVEX_HULL_PSD_SEARCH_UNKNOWN"||h.status==="CONVEX_PSD_GRID_PREFLIGHT_UNKNOWN","expanded grid failure remains unknown");check(!r.next_support&&!r.next_objective,"no invented refined dual");expandedHullUnknowns++;}
        if(!positive)check(!run.PSD_native_gap_certificate,"no native PSD gap from negative or unknown mixture");expandedHulls++;
      }else check(!run.refinement,"only exact escaping base points refine hulls");
    }
  }
}
console.log(JSON.stringify({status:"independent_native_global_PSD_support_checks_passed",functionals,escapes,globalObstructions,unknowns,negativeEscapes,positiveEscapes,LPcalls,expandedHulls,expandedHullObstructions,expandedHullUnknowns,positiveExpandedHulls,nativePSDGaps,wholeNewPrefixEliminations:0,populationObstructionProved:false}));
module.exports={support,objective,supportResult};

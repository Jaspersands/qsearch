"use strict";
// Replays BOTH upstream proof audits, then independently checks hull proofs.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {primal,matrix,positivity,psd,moments,momentBytes}=require("./ternary_moment_psd_crosscheck.js");
const {check,gcd,F,fraction,det,commonIntegers,sameSet,prepare,geometry,momentModel,report,load}=require("./ternary_prefix_integrality_crosscheck.js");
const mixtures=load("ternary_moment_psd_mixtures"),psdBytes=fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_moment_psd.json"));
const sha=x=>crypto.createHash("sha256").update(x).digest("hex"),same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
check(sha(psdBytes)===mixtures.source_psd_report_sha256&&sha(momentBytes)===mixtures.source_moment_report_sha256,"both exact source reports hash-pinned");
check(!mixtures.polynomial_pair_finder_proved&&!mixtures.population_obstruction_proved&&!mixtures.novelty_claim,"mixture proof claims scoped");
let hulls=0,faces=0,negativeMixtures=0,positiveMixtures=0,hullObstructions=0;
function exactFace(model,points,record){const first=points[0],n=first.A.length,free=record.free_indices,k=free.length;
  check(record.matrix_dimension===n&&record.face_dimension===k&&k>0&&new Set(free).size===k&&free.every(i=>Number.isInteger(i)&&i>=0&&i<n),"nonempty principal native face");
  const indicators=model.variables.filter(key=>key[0]==="p"),relations=[];
  const M=(n-1?Math.max(...indicators.map(key=>key[1]))+1:0);
  for(let j=0;j<M;j++)relations.push([-1n,...indicators.map(key=>key[1]===j?1n:0n)]);
  for(const[a,B]of model.sourceEquations)relations.push([-B,...indicators.map(key=>a[key[1]][key[2]])]);
  same(record.source_relations,relations.map(row=>row.map(String)),"every original conditioned source relation");check(record.source_relation_rows===relations.length,"source relation count");
  const zero=[];for(let i=0;i<n;i++)if(points.every(p=>p.A[i].every(x=>x===0n)))zero.push(i);
  same(zero,record.hull_specific_zero_rows,"complete HULL-specific zero rows, not global constraints");check(record.hull_zero_rows_not_a_global_native_constraint,"zero-row scope retained");
  for(const i of zero)relations.push(Array.from({length:n},(_,j)=>i===j?1n:0n));
  check(record.transformation.length===n&&record.transformation.every(row=>row.length===k),"full exact reconstruction map");
  const t=commonIntegers(record.transformation.flat()),T=Array.from({length:n},(_,i)=>t.values.slice(i*k,(i+1)*k));
  free.forEach((i,a)=>check(T[i].every((x,b)=>x===(a===b?t.den:0n)),"principal free rows give full column rank"));
  for(const h of relations)for(let j=0;j<k;j++)check(h.reduce((s,x,i)=>s+x*T[i][j],0n)===0n,"all actual source/hull relations annihilate reconstruction map");
  const rr=record.independent_relation_rows,cc=record.independent_relation_columns,r=n-k;
  check(record.relation_rank===r&&rr.length===r&&cc.length===r&&new Set(rr).size===r&&new Set(cc).size===r&&rr.every(i=>Number.isInteger(i)&&i>=0&&i<relations.length)&&cc.every(j=>Number.isInteger(j)&&j>=0&&j<n),"exact independent minor indices");
  const determinant=det(rr.map(i=>cc.map(j=>relations[i][j])));check(determinant!==0n&&String(determinant)===record.nonzero_relation_minor_determinant,"exact nonzero minor lower rank plus full-rank rational null map upper rank");
  for(const p of points)for(let i=0;i<n;i++)for(let j=0;j<n;j++){let value=0n;for(let a=0;a<k;a++)value+=T[i][a]*p.A[free[a]][j];
    check(value===p.A[i][j]*t.den,"EVERY supplied original matrix reconstructs from its principal free rows");}
  check(record.all_original_matrices_reconstruct_exactly,"no unverified compression claim");faces++;
  return points.map(p=>({den:p.den,A:free.map(i=>free.map(j=>p.A[i][j]))}));}
function mix(points,weights){const w=commonIntegers(weights);check(w.values.length===points.length&&w.values.every(x=>x>=0n)&&w.values.reduce((a,b)=>a+b,0n)===w.den,"exact convex weights");
  const D=points.reduce((d,p)=>d/gcd(d,p.den)*p.den,1n),n=points[0].A.length,A=Array.from({length:n},()=>Array(n).fill(0n));
  points.forEach((p,k)=>{const scale=w.values[k]*(D/p.den);for(let i=0;i<n;i++)for(let j=0;j<n;j++)A[i][j]+=p.A[i][j]*scale;});return {A,den:D*w.den};}
function separator(points,record){const c=record.certificate;check(c&&c.valid&&c.positive_semidefinite_dual_is_sum_of_squares&&c.proves_ONLY_supplied_convex_hull_has_no_psd_matrix&&!c.full_SDP_infeasibility_proved,"SOS dual proves only the SUPPLIED hull");
  const w=commonIntegers(c.nonnegative_weights),v=c.vectors.map(commonIntegers),n=points[0].A.length;
  check(w.values.length===v.length&&w.values.every(x=>x>=0n)&&w.values.reduce((a,b)=>a+b,0n)===w.den&&v.every(q=>q.values.length===n),"nonnegative normalized exact outer-product weights");
  const L=v.reduce((d,q)=>d/gcd(d,q.den*q.den)*(q.den*q.den),1n);
  check(c.point_trace_values.length===points.length,"strict negativity retained for EVERY supplied vertex");
  points.forEach((p,k)=>{let trace=0n;v.forEach((q,l)=>{let value=0n;for(let i=0;i<n;i++)for(let j=0;j<n;j++)value+=q.values[i]*p.A[i][j]*q.values[j];trace+=w.values[l]*value*(L/(q.den*q.den));});
    const saved=fraction(c.point_trace_values[k]);check(trace<0n&&trace*saved[1]===saved[0]*p.den*L*w.den,"exact strict negative PSD-dual trace at every hull point");});hullObstructions++;}
sameSet(mixtures.cases.flatMap(c=>c.trials.map(t=>[c.fixture_probe_index,t.target])),psd.cases.flatMap(c=>c.trials.map(t=>[c.fixture_probe_index,t.target])),"same explicit source prefix schedule");
for(const c of mixtures.cases){const pc=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),mc=moments.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),sc=psd.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index);
  check(pc&&mc&&sc&&c.fingerprint===pc.fingerprint,"original native source geometry");const base=prepare(pc);
  for(const t of c.trials){const pt=pc.trials.find(x=>x.target===t.target),mt=mc.trials.find(x=>x.target===t.target),st=sc.trials.find(x=>x.target===t.target),g=geometry(base,BigInt(t.target),pt.frontier);let survives=false;
    sameSet(t.winding_trials.map(r=>r.winding_branch),st.winding_trials.filter(r=>r.status==="PSD_CUT_CAP_UNKNOWN").map(r=>r.winding_branch),"all capped PSD windings, no favorable selection");
    for(const run of t.winding_trials){const sr=st.winding_trials.find(r=>r.winding_branch===run.winding_branch),mr=mt.winding_trials.find(r=>r.winding_branch===run.winding_branch),model=momentModel(g,run.winding_branch),N=model.variables.length;
      const certs=[mr.primal,...sr.steps.slice(1).map(s=>s.analysis.primal).filter(Boolean)];
      const points=certs.map(c=>matrix(model,primal(model,{...c,moments:c.moments.slice(0,N)},run.winding_branch))),C=exactFace(model,points,run.face);
      check(run.cost.point_count===points.length&&!run.global_native_distribution_proved&&!run.full_SDP_infeasibility_proved,"hull not full moment space");
      check(run.attempts.length===run.cost.exact_psd_checks&&run.attempts.length<=mixtures.exact_candidate_budget,"all exact mixture checks charged");let positive=false;
      for(let i=0;i<run.attempts.length;i++){const a=run.attempts[i],w=a.weights.map(fraction);check(w.length===points.length&&w.every(q=>(q[0]*BigInt(mixtures.grid_denominator))%q[1]===0n),"candidate weights really lie on stated rational grid");
        const p=positivity(mix(C,a.weights),a.compressed_positivity);if(p){positiveMixtures++;positive=true;check(i===run.attempts.length-1,"stop after exact PSD mixture");same(a.weights,run.exact_convex_weights,"accepted mixture weights");}else negativeMixtures++;}
      if(positive){check(run.status==="EXACT_PSD_NATIVE_RELAXATION_GAP"&&run.base_native_truth_verified_empty&&pt.native_truth.native_prefix_words.length===0&&run.matrix_psd_from_exact_face_and_compressed_LDL&&!run.integer_prefix_completion_proved,"PSD relaxation GAP needs actual independent native emptiness");survives=true;}
      else if(run.status==="EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION"){check(run.hull_separator.status==="EXACT_SUPPLIED_HULL_PSD_OBSTRUCTION","exact hull separator required");separator(C,run.hull_separator);}
      else check(run.status==="CONVEX_HULL_PSD_SEARCH_UNKNOWN"||run.status==="CONVEX_PSD_GRID_PREFLIGHT_UNKNOWN","no inference from failed grid");hulls++;
    }
    check(t.psd_gap_survives===survives&&!t.prefix_eliminated&&t.only_cap_unknown_windings_probed,"prefix not eliminated by a finite-hull obstruction");
  }}
console.log(JSON.stringify({status:"independent_native_moment_face_and_convex_hull_checks_passed",hulls,faces,negativeMixtures,positiveMixtures,hullObstructions,
  fullMomentSDPInfeasibilityProved:false,populationObstructionProved:false}));
module.exports={mixtures,exactFace,mix,separator};

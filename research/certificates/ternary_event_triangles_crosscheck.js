"use strict";
// First replay both exact PSD witnesses and the full upstream source proof chain.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {joint}=require("./ternary_joint_realizability_crosscheck.js");
const {local}=require("./ternary_local_marginals_crosscheck.js");
const {support}=require("./ternary_psd_support_lift_crosscheck.js");
const {primal}=require("./ternary_moment_psd_crosscheck.js");
const {check,F,fraction,sameSet,prepare,geometry,momentModel,report,load}=require("./ternary_prefix_integrality_crosscheck.js");
const events=load("ternary_event_triangles"),sources={joint:"ternary_joint_realizability",support:"ternary_psd_support_lift",local:"ternary_local_marginals",prefix:"ternary_prefix_integrality",fixture:"ternary_pair_cell_coverage"};
for(const[key,name]of Object.entries(sources))check(crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../phase_workbench/"+name+".json"))).digest("hex")===events.source_sha256[key],"every event source is hash-pinned");
check(!events.novelty_claim&&!events.polynomial_pair_finder_proved&&!events.complete_local_polytope_separator_proved,"necessary-condition separator only");
const same=(a,b,message)=>check(JSON.stringify(a)===JSON.stringify(b),message),fractionEq=(a,d,s)=>{const q=fraction(s);return a*q[1]===q[0]*d;};
const subsets=D=>Array.from({length:(1<<D.length)-2},(_,k)=>D.filter((_,j)=>(k+1)&(1<<j)));
const key=(b,S)=>JSON.stringify([b,S]),pairkey=(i,S,j,T)=>JSON.stringify([i,S,j,T]);
let points=0,triplesChecked=0,combinationsChecked=0,negativeTriangles=0,referenceMatches=0;
const expected=local.cases.flatMap(c=>[[c.fixture_probe_index,c.target,c.winding_branch,"INITIAL_PSD_GAP"],...joint.cases.filter(j=>j.fixture_probe_index===c.fixture_probe_index&&j.target===c.target&&j.winding_branch===c.winding_branch&&j.joint_gap_point).map(()=>[c.fixture_probe_index,c.target,c.winding_branch,"JOINT_SELECTED_LOCAL_CUTS_PSD_GAP"])]);
sameSet(events.cases.map(c=>[c.fixture_probe_index,c.target,c.winding_branch,c.source_point]),expected,"BOTH actual source PSD witnesses tested, no synthetic oracle cases");
for(const c of events.cases){
  const pc=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),pt=pc.trials.find(t=>t.target===c.target),g=geometry(prepare(pc),BigInt(c.target),pt.frontier),model=momentModel(g,c.winding_branch),N=model.variables.length;
  check(c.fingerprint===pc.fingerprint,"original native fingerprint");
  let sourcePoint;if(c.source_point==="INITIAL_PSD_GAP"){
    const sc=support.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),st=sc.trials.find(t=>t.target===c.target),sr=st.winding_trials.find(r=>r.winding_branch===c.winding_branch);sourcePoint=sr.PSD_native_gap_certificate.moment_certificate;
  }else sourcePoint=joint.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index&&x.target===c.target&&x.winding_branch===c.winding_branch).joint_gap_point.primal;
  const p=primal(model,{...sourcePoint,moments:sourcePoint.moments.slice(0,N)},c.winding_branch),M=g.base.M,families=g.domains.map(subsets),lookup=new Map(model.variables.map((k,i)=>[JSON.stringify(k),i])),marg=new Map(),pairs=new Map();
  for(let b=0;b<M;b++)for(const S of families[b])marg.set(key(b,S),S.reduce((s,a)=>s+p.x[lookup.get(JSON.stringify(["p",b,a]))],0n));
  for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(const S of families[i])for(const T of families[j]){
    let sum=0n;for(const a of S)for(const b of T)sum+=p.x[lookup.get(JSON.stringify(["J",i,a,j,b]))];pairs.set(pairkey(i,S,j,T),sum);
  }
  const triples=[];for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(let k=j+1;k<M;k++)triples.push([i,j,k]);
  same(c.triple_trials.map(t=>t.blocks),triples,"complete original triple schedule");let evaluated=0;
  for(let q=0;q<triples.length;q++){
    const blocks=triples[q],trial=c.triple_trials[q];let best=null,count=0;
    for(let center=0;center<3;center++){
      const choices=blocks.map((b,j)=>j===center?families[b].filter(S=>S.includes(g.domains[b][0])):families[b]);
      for(const S of choices[0])for(const T of choices[1])for(const U of choices[2]){
        const event=[S,T,U];let value=marg.get(key(blocks[center],event[center]));
        for(const[i,j]of [[0,1],[0,2],[1,2]])value+=(i===center||j===center?-1n:1n)*pairs.get(pairkey(blocks[i],event[i],blocks[j],event[j]));
        count++;if(value<0n&&(!best||value<best.value))best={value,event,center};
      }
    }
    check(count===trial.event_combinations_evaluated,"EVERY complement-canonical event tested exactly");evaluated+=count;
    if(best){const cert=trial.certificate;check(trial.status==="EXACT_EVENT_TRIANGLE_NATIVE_OBSTRUCTION"&&cert&&cert.valid_native_inequality&&cert.rejects_THIS_point&&cert.proves_no_native_realization_of_THIS_point&&!cert.proves_entire_relaxation_infeasible&&cert.required_winding===c.winding_branch,"scoped exact native inequality");
      same(cert.blocks,blocks,"same original triple");same(cert.events,best.event,"deterministic most-negative exact event");check(cert.center_position===best.center&&fractionEq(best.value,p.den,cert.exact_point_value),"exact strict negative value, no LP or tolerance");
      const coef=new Map(),add=(k,a)=>{const j=lookup.get(JSON.stringify(k));coef.set(j,(coef.get(j)||0n)+a);};
      for(const a of best.event[best.center])add(["p",blocks[best.center],a],1n);
      for(const[i,j]of [[0,1],[0,2],[1,2]])for(const a of best.event[i])for(const b of best.event[j])add(["J",blocks[i],a,blocks[j],b],i===best.center||j===best.center?-1n:1n);
      same(cert.integer_coefficients,Object.fromEntries([...coef].filter(([,a])=>a).map(([j,a])=>[String(j),String(a)])),"ALL original p/J event coefficients");
      check([...coef].reduce((s,[j,a])=>s+a*p.x[j],0n)===best.value,"cached event value equals original full-moment functional");
      const values=[];for(const a of g.domains[blocks[0]])for(const b of g.domains[blocks[1]])for(const d of g.domains[blocks[2]]){
        const word=[a,b,d],bits=word.map((x,i)=>best.event[i].includes(x)?1n:0n),other=[0,1,2].filter(i=>i!==best.center),x=bits[best.center],y=bits[other[0]],z=bits[other[1]],value=(x-y)*(x-z);
        let linear=0n;for(const[j,v]of coef){const k=model.variables[j];let indicator=word[blocks.indexOf(k[1])]===k[2]?1n:0n;if(k[0]==="J")indicator*=word[blocks.indexOf(k[3])]===k[4]?1n:0n;linear+=v*indicator;}
        check((value===0n||value===1n)&&linear===value,"EVERY native assignment proves event-product nonnegativity");values.push(Number(value));
      }
      same(cert.local_assignment_values,values,"complete original native truth table");negativeTriangles++;
    }else check(!trial.certificate&&trial.status==="NO_EVENT_TRIANGLE_VIOLATION_NOT_LOCAL_PROOF","no failed projection promoted to local proof");triplesChecked++;
  }
  check(c.cost.LP_calls===0&&c.cost.pair_event_sums_computed===pairs.size&&c.cost.event_combinations_evaluated===evaluated&&c.cost.event_combinations_preflight===evaluated&&c.cost.selected_native_inequality_checks===c.triple_trials.filter(t=>t.certificate).length&&evaluated<=c.cost.event_budget,"exact zero-LP cost/preflight ledger");combinationsChecked+=evaluated;
  const bits=a=>a===0n?0:(a<0n?-a:a).toString(2).length;
  check(c.cost.exact_common_denominator_bits===bits(p.den)&&c.cost.maximum_scaled_moment_bits===Math.max(...p.x.map(bits))&&c.cost.full_original_point_verification_calls===1+c.cost.selected_native_inequality_checks,"exact integer bit complexity and all source-point rechecks charged");
  check(c.no_violations_is_not_local_extendability_proof&&!c.global_native_distribution_proved,"event separator is not complete local/native solver");
  if(c.source_point==="INITIAL_PSD_GAP"){
    const lc=local.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index&&x.target===c.target&&x.winding_branch===c.winding_branch);let matches=0,misses=0;
    c.triple_trials.forEach((t,i)=>{const r=lc.triple_trials[i];same(t.blocks,r.blocks,"same complete exact LP reference schedule");if(r.extension)check(!t.certificate,"no event inequality can contradict a certified local distribution");if(r.dual){if(t.certificate)matches++;else misses++;}});
    same(c.local_reference_comparison,{reference_local_obstructions:lc.nonPSD_local_obstructions,detected_reference_obstructions:matches,reference_obstructions_not_detected:misses,contradictions_with_exact_extensions:0},"reference agreement recorded without completeness extrapolation");referenceMatches+=matches;
  }else check(!c.local_reference_comparison,"new PSD witness has no unperformed exact local LP reference");points++;
}
console.log(JSON.stringify({status:"independent_native_event_triangle_checks_passed",points,triplesChecked,combinationsChecked,negativeTriangles,referenceMatches,LPcalls:0,completeLocalSeparatorProved:false,quantumSpeedupProved:false}));

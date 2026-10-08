"use strict";
// Independent numerical replay; this is deliberately NOT an exact SDP certificate.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_character_sdp_decoder.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify;
const same=(a,b,m)=>check(key(a)===key(b),m);
const near=(a,b,m,t=1e-7)=>check(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=t,m);
const mod=(x,q)=>(x%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],sub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],conj=a=>[a[0],-a[1]],abs=a=>Math.hypot(...a);
function score(records,s){const q=records[0].modulus;return records.reduce((v,r)=>{
  const e=r.outcome.map((y,j)=>mod(y-dot(j?r.second:r.first,s),q));
  return v+[e[0],e[1],mod(e[0]-e[1],q)].reduce((z,x)=>z+Math.cos(2*Math.PI*x/q),0);
},0)/records.length;}
function chart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(Math.ceil(level/2)),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]);
  const a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);
  check(a%den===0n&&b%den===0n,"exact native source chart");const u=a/den,v=b/den;
  return label=>{const[x,y]=label.map(BigInt);return[Number(mod(u*x+v*y,q)),Number(mod((u+v)*x-u*y,q))];};
}
function compile(records,m){
  const q=records[0].modulus,n=records[0].first.length,A=records.flatMap(r=>[r.first,r.second]),basis=m.unit_basis_frequency_rows,I=m.basis_inverse;
  const B=basis.map(j=>A[j]);check(basis.length===n&&new Set(basis).size===n,"full original-row unit basis");
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(B[i].reduce((v,a,k)=>v+a*I[k][j],0),q)===Number(i===j),"exact composite-ring inverse");
  const nodes=[],index=new Map(),node=raw=>{const x=raw.map(a=>mod(a,q)),k=key(x);if(!index.has(k)){index.set(k,nodes.length);nodes.push(x);}return index.get(k);};
  const zero=node(Array(n).fill(0)),native=A.map(node);
  function plus(i,j){const k=node(nodes[i].map((a,l)=>a+nodes[j][l]));node(nodes[j].map(a=>-a));return k;}
  const powers=new Map();function multiply(i,c){let total=zero,power=i,bit=0;while(c){if(c%2)total=plus(total,power);c=Math.floor(c/2);bit++;if(c){const k=key([i,bit]);if(!powers.has(k))powers.set(k,plus(power,power));power=powers.get(k);}}return total;}
  for(const j of basis)check(multiply(native[j],q)===zero,"qth-root circuit loops");
  for(const a of A){let total=zero;const coeff=Array.from({length:n},(_,j)=>mod(a.reduce((v,x,k)=>v+x*I[k][j],0),q));
    basis.forEach((j,k)=>{if(coeff[k])total=plus(total,multiply(native[j],coeff[k]));});
    same(nodes[total],a,"original native target reconstruction");}
  same(nodes,m.nodes,"independently compiled complete quotient circuit frequencies");
  same(basis.map(j=>native[j]),m.basis_nodes,"basis phase-node map");
  same(records.map((_,i)=>[native[2*i],native[2*i+1]]),m.native_nodes,"original native score-node map");
  check(m.matrix_nodes===nodes.length&&m.complete_difference_entries===nodes.length**2,"full matrix ledger");
  check(m.full_secret_group_size===q**n&&m.full_group_saturation===(nodes.length===q**n),"full-group calibration flag");
  check(m.templates_read_outcomes===false&&m.rank_one_character_soundness_inherited===true,"public template contract");return nodes;
}
function matrixReplay(records,d){
  const m=d.model,S=d.solver,K=m.matrix_nodes,q=m.modulus,nodes=compile(records,m);
  check(S.matrix_real.length===K&&S.matrix_imag.length===K,"complete saved matrix");
  const X=S.matrix_real.map((r,i)=>{check(r.length===K&&S.matrix_imag[i].length===K,"complete matrix row");return r.map((v,j)=>{check(Number.isFinite(v)&&Number.isFinite(S.matrix_imag[i][j]),"finite entries");return[v,S.matrix_imag[i][j]];});});
  let herm=0,diag=0,delta=0;const reps=new Map();
  for(let i=0;i<K;i++){diag=Math.max(diag,abs(sub(X[i][i],[1,0])));for(let j=0;j<K;j++){
    herm=Math.max(herm,abs(sub(X[i][j],conj(X[j][i]))));const v=key(nodes[i].map((a,k)=>mod(a-nodes[j][k],q)));
    if(!reps.has(v))reps.set(v,X[i][j]);delta=Math.max(delta,abs(sub(X[i][j],reps.get(v))));
  }}
  check(reps.size===m.distinct_differences&&K*K-reps.size===m.difference_equalities,"complete difference-constraint count");
  const audit=S.audit,t=audit.feasibility_tolerance;near(herm,audit.hermitian_residual,"Hermiticity residual");near(diag,audit.unit_diagonal_residual,"unit diagonals");near(delta,audit.all_equal_difference_residual,"ALL difference residuals");
  check(Math.max(herm,diag,delta)<=t&&audit.numerically_feasible===true&&audit.exact_PSD_or_optimality_certificate===false,"numerical feasibility is not proof");
  // Literal Cholesky of X+2*t*I independently checks a numerical PSD slack.
  const L=Array.from({length:K},()=>Array.from({length:K},()=>[0,0]));
  for(let j=0;j<K;j++){
    let v=X[j][j][0]+2*t;for(let k=0;k<j;k++)v-=abs(L[j][k])**2;
    check(v>0,"shifted numerical PSD check");L[j][j]=[Math.sqrt(v),0];
    for(let i=j+1;i<K;i++){let a=X[i][j];for(let k=0;k<j;k++)a=sub(a,mul(L[i][k],conj(L[j][k])));L[i][j]=a.map(x=>x/L[j][j][0]);}
  }
  let objective=0;records.forEach((r,i)=>{const[a,c]=m.native_nodes[i];for(const[u,v,e]of[[a,0,r.outcome[0]],[c,0,r.outcome[1]],[a,c,mod(r.outcome[0]-r.outcome[1],q)]]){
    const angle=2*Math.PI*e/q;objective+=mul([Math.cos(angle),-Math.sin(angle)],X[u][v])[0];
  }});near(objective,audit.objective_score,"original paired three-feature objective",1e-6);
  check(S.dual_optimality_or_integrality_gap_certified===false&&d.efficient_population_recovery_proved===false,"unproved SDP conclusions");return K*K;
}
function refine(records,r){
  const q=records[0].modulus,n=records[0].first.length,starts=[...new Map(r.initial_proposals.map(s=>[key(s),s])).values()],scored=new Map();let evaluations=0;
  for(const initial of starts){let trial=initial.slice(),value=score(records,trial);evaluations++;scored.set(key(trial),[trial,value]);
    for(let c=0;c<r.coordinate_sweeps;c++){let changed=false;for(let j=0;j<n;j++){
      let best=0,bestValue=-Infinity;for(let a=0;a<q;a++){const v=trial.slice();v[j]=a;const s=score(records,v);evaluations++;if(s>bestValue){best=a;bestValue=s;}}
      if(bestValue>value+1e-10){trial=trial.slice();trial[j]=best;value=bestValue;changed=true;scored.set(key(trial),[trial,value]);}
    }if(!changed)break;}
  }
  const sorted=[...scored.values()].sort((a,b)=>{for(let i=0;i<n;i++)if(a[0][i]!==b[0][i])return a[0][i]-b[0][i];return 0;});
  let best=sorted[0];for(const row of sorted)if(row[1]>best[1])best=row;
  same(best[0],r.candidate,"independent training-only coordinate candidate");near(best[1],r.training_score,"training score");
  check(evaluations===r.complete_score_evaluations&&scored.size===r.distinct_candidates_scored_or_retained,"all coordinate/root evaluation costs");
  check(r.runtime_polynomial_in_q_not_logq===true&&r.training_truth_or_holdout_used===false,"root scan scope / no heldout selection");return evaluations;
}
function verify(records,v,trainIDs){
  near(score(records,v.candidate),v.score,"fresh native score");check(v.threshold_passed===(v.score>=.5),"raw verification threshold");
  check(v.fresh_original_ids.length===records.length&&new Set(v.fresh_original_ids).size===records.length&&!v.fresh_original_ids.some(x=>trainIDs.includes(x)),"fresh disjoint original records");
  check(v.candidate_selected_before_holdout===true&&v.distinct_IDs_prove_physical_IID_supply===false&&v.speedup_claim_allowed===false,"no source/algorithm promotion");
  const g=v.gate;check(g.fresh_native_qutrit_records===records.length&&g.tested_candidates===1&&g.candidates_independent_of_this_holdout_required,"frozen single candidate gate");
  near(g.false_acceptance_union_bound_approximation,Math.exp(-2*records.length/81),"existing heldout native false-accept bound");
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_CHARACTER_SDP_DECODER.md"))).digest("hex");
check(R.derivation_sha256===hash&&R.status==="NATIVE_CHARACTER_SDP_DECODER_NUMERICAL_RESEARCH_ONLY","pinned numerical research contract");
for(const name of["accepted_candidate_or_speedup","population_recovery_or_tightness_proved","algorithm_input_contains_truth","exact_PSD_dual_or_integrality_gap_certificates_supplied"])check(R[name]===false,"unsupported claim: "+name);
check(R.raw_failures_and_cap_exhaustions_retained===true,"no discarded failures");
let entries=0,evaluations=0,failed=0,solved=0;
for(const c of R.native_controls){const d=c.decoder,train=c.training_records,held=c.heldout_records,q=3**c.root_digits;
  for(const[records,b]of[[train,c.original_source_batches[0]],[held,c.original_source_batches[1]]]){
    const at=chart(b.original_level);check(b.original_level===2*c.root_digits&&b.original_ring_labels.length===records.length,"original even-native source batch");
    b.original_ring_labels.forEach((label,i)=>{const f=label.map(at);same(records[i].first,f.map(x=>x[0]),"first actual source frequency");same(records[i].second,f.map(x=>x[1]),"second actual source frequency");check(records[i].modulus===q,"retained full root");});
  }
  check(c.charged_original_native_qutrits===train.length+held.length&&d.charged_training_qutrits===train.length&&new Set(d.original_ids).size===train.length,"complete raw source costs");
  check(c.independent_source_supply_is_an_assumption_not_PRNG_evidence===true,"IID is not proved by seeds");
  evaluations+=refine(train,d.matched_nonSDP_baseline)+refine(train,d.stronger_nonSDP_baseline);
  const strongStarts=new Set(d.stronger_nonSDP_baseline.initial_proposals.map(key));
  check(d.matched_nonSDP_baseline.initial_proposals.every(s=>strongStarts.has(key(s))),"stronger portfolio includes every weaker start");
  check(d.stronger_nonSDP_baseline.training_score>=d.matched_nonSDP_baseline.training_score-1e-9,"stronger training objective is monotone, not recovery");
  verify(held,c.matched_baseline_fresh_verification,d.original_ids);verify(held,c.stronger_baseline_fresh_verification,d.original_ids);
  check(c.matched_baseline_calibration_recovery===(key(d.matched_nonSDP_baseline.candidate)===key(c.calibration_secret_NOT_decoder_input))&&c.stronger_baseline_calibration_recovery===(key(d.stronger_nonSDP_baseline.candidate)===key(c.calibration_secret_NOT_decoder_input)),"post-hoc baseline recovery only");
  if(d.candidate===null){failed++;check(d.failed_or_uncertified_attempt_retained===true,"retained failed attempt");continue;}
  solved++;entries+=matrixReplay(train,d);evaluations+=refine(train,d.refinement);
  same(d.candidate,d.refinement.candidate,"pipeline candidate");verify(held,c.fresh_verification,d.original_ids);
  check(c.calibration_recovery===(key(d.candidate)===key(c.calibration_secret_NOT_decoder_input))&&c.baseline_calibration_recovery===(key(d.matched_nonSDP_baseline.candidate)===key(c.calibration_secret_NOT_decoder_input)),"truth used only for post-hoc recovery calibration");
  check(d.same_quantum_produced_classical_records_for_both_decoders===true&&d.nonSDP_baseline_pays_no_SDP_cost===true,"matched actual input model");
  const ref=c.reference_calibration;if(ref.status==="CAPPED_EXHAUSTIVE_CALIBRATION"){
    let best=-Infinity;for(let k=0;k<q**c.dimension;k++){let t=k,s=[];for(let j=0;j<c.dimension;j++){s.push(t%q);t=Math.floor(t/q);}best=Math.max(best,score(train,s));}
    near(best,ref.best_score,"capped full-secret reference");near(score(train,ref.best_secret),best,"reference witness score");
    near(c.numerical_relaxation_minus_best_character_score,d.solver.audit.objective_score/train.length-best,"numerical not certified integrality gap");check(c.integrality_gap_proved===false,"no numerical gap theorem");
  }
  check(ref.reference_used_by_decoder===false,"no exhaustive decoder initializer");
}
console.log(JSON.stringify({status:"PASS",solved_controls:solved,retained_failed_controls:failed,matrix_entries_checked:entries,coordinate_score_evaluations_replayed:evaluations,exact_PSD_optimality_or_population_recovery_certified:false}));

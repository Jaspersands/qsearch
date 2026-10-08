"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_collective_character_receiver.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
const mod=(x,q)=>(x%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=JSON.stringify;
const words=(k,q=3)=>Array.from({length:q**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/q**(k-j-1))%q));
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function rref(A,width){
  A=A.map(row=>row.map(x=>mod(x,3)));const pivots=[];let r=0;
  for(let j=0;j<width&&r<A.length;j++){
    const p=A.findIndex((row,i)=>i>=r&&row[j]);if(p<0)continue;
    [A[r],A[p]]=[A[p],A[r]];A[r]=A[r].map(x=>x*A[r][j]%3);
    for(let i=0;i<A.length;i++)if(i!==r){const c=A[i][j];A[i]=A[i].map((x,k)=>mod(x-c*A[r][k],3));}
    pivots.push(j);r++;
  }
  return {rows:A.slice(0,r),pivots};
}
function value(p,z){
  const N=Number(p.numerator_modulus),out=Array(p.components).fill(0);
  check(N===3*Number(p.phase_modulus)&&p.exact_shared_denominator===3,"native modulus/denominator");
  for(const g of p.projective_ridge_groups)g.component_tables.forEach((row,l)=>out[l]+=row[dot(g.direction,z)%3]);
  return out.map(x=>{x=mod(x,N);check(x%3===0,"exact native division");return x/3;});
}
function ledger(x){
  const n=BigInt(x.components),d=BigInt(x.width),r=BigInt(x.phase_digits),B=BigInt(x.outputs);
  const G=3n**(n*r),D=3n**(d*B),source=B*(n*((3n**d-1n)/2n-d)+1n)*(n+d)*(n+1n)**2n;
  check(x.full_secret_count===String(G)&&x.joint_dimension===String(D)&&x.provided_original_inputs_per_attempt===String(source),"all original source and joint dimensions charged");
  check(x.mean_ideal_PGM_failure_upper_under_IID_source===frac(G-1n>D?D:G-1n,D),"information-only failure bound");
  check(x.uncorrected_erasure_joint_success===frac(1n,G)&&x.uncorrected_expected_fresh_original_inputs_per_correct_readout===String(source*G),"exponential normalization not conditional success");
  check(x.best_exact_character_feedforward_joint_success_ceiling===frac(3n**n,G),"universal exact-character ceiling");
  for(const k of["population_bound_is_fixed_instance_certificate","ideal_PGM_is_an_implemented_efficient_receiver","one_use_unknown_source_reflection_or_inverse_granted","all_outcome_classical_inference_ruled_out_by_character_ceiling","reciprocal_yield_is_a_correctness_flag_or_stopping_rule"])check(x[k]===false,"scope: "+k);
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_COLLECTIVE_CHARACTER_RECEIVER.md"))).digest("hex");
check(R.derivation_sha256===hash&&R.status==="COLLECTIVE_CHARACTER_FEEDFORWARD_COSTED_NEGATIVE_REVIEW_PENDING","pinned local derivation");
for(const k of["general_collective_receiver_ruled_out","quantum_speedup_proved","candidate_record_accepted"])check(R[k]===false,"unsupported claim: "+k);
same(R.native_controls.map(c=>c.source_cohorts.map(s=>s.seed)),[[89000],[89000],[89001,89002],[89128,89131],[89031,89103]],"structural native controls retained");
let jointWords=0,ringCorrections=0,branches=0;
for(const c of R.native_controls){
  ledger(c.ledger);const n=c.ledger.components,d=c.ledger.width,q=3**c.ledger.phase_digits,B=c.source_cohorts.length,G=q**n,H=q/3;
  const ws=words(d),table=c.source_cohorts.map(s=>ws.map(z=>value(s.public_phase,z))),ids=c.source_cohorts.flatMap(s=>s.original_ancestry_ids);
  check(new Set(ids).size===ids.length&&BigInt(ids.length)===BigInt(c.ledger.provided_original_inputs_per_attempt),"original cohort ancestry and full supply");
  for(const s of c.source_cohorts)check(s.original_ancestry_ids.length===s.source_cap&&s.source_premise_physically_certified===false,"IDs do not establish IID");
  const k=c.corrections,f=c.joint_reference;
  same(k.complete_frequency_tables,table,"local frequencies independently reconstructed from compact phase");
  const point=j=>Array.from({length:d},(_,i)=>Number(i===j)),index=z=>ws.findIndex(x=>key(x)===key(z)),matrices=[],linears=[];
  for(const T of table){
    const beta=[],diag=[],mix=[];
    for(let l=0;l<n;l++){
      const a=Array.from({length:d},(_,j)=>mod(2*(T[index(point(j).map(x=>2*x))][l]-2*T[index(point(j))][l]),3));
      const b=Array.from({length:d},(_,j)=>mod(T[index(point(j))][l]-a[j],3)),cross=[];
      for(let i=0;i<d;i++)for(let j=i+1;j<d;j++)cross.push([i,j,mod(T[index(point(i).map((x,k)=>x+point(j)[k]))][l]-T[index(point(i))][l]-T[index(point(j))][l],3)]);
      for(let u=0;u<ws.length;u++)check(mod(dot(b,ws[u])+dot(a,ws[u].map(x=>x*x))+cross.reduce((s,[i,j,v])=>s+v*ws[u][i]*ws[u][j],0),3)===T[u][l]%3,"ordinary quadratic checked, not declared");
      beta.push(b);diag.push(a);mix.push(cross);
    }
    const rows=Array.from({length:d},(_,j)=>diag.map(a=>a[j]));
    for(let j=0;j<mix[0].length;j++)rows.push(mix.map(row=>row[j][2]));matrices.push(rows);linears.push(beta);
  }
  same(k.program_quadratic_rows,matrices,"quadratic nullspace inputs");same(k.program_linear_rows,linears,"linear character image inputs");
  const span=rref(table.flat().map(v=>v.map(x=>x%3)),n).pivots.length;
  check(k.public_frequency_span_rank_mod3===span&&k.complete_correction_image_certified===(span===n),"actual full-ring span certificate");
  const exact=new Map();
  for(const delta of words(n,q)){
    const t=[];let ok=true;
    for(const T of table){
      const tr=Array.from({length:d},(_,j)=>mod(dot(delta,T[index(point(j))]),q));
      if(tr.some(x=>x%H)){ok=false;break;}const tv=tr.map(x=>x/H);
      if(ws.some((z,i)=>mod(dot(delta,T[i])-H*dot(tv,z),q))){ok=false;break;}t.push(...tv);
    }
    if(ok)exact.set(key(t),delta);ringCorrections++;
  }
  if(span===n)check(String(exact.size)===k.all_exact_rescuable_erasure_outcomes,"exhaustive full-ring correction completeness");
  else check(k.all_exact_rescuable_erasure_outcomes===null,"deficient span is incomplete");
  check(k.word_character_basis.length===k.word_character_image_rank&&rref(k.word_character_basis,d*B).pivots.length===k.word_character_image_rank,"independent implemented image basis");
  k.word_character_basis.forEach((t,i)=>same(exact.get(key(t)),k.full_root_secret_corrections[i],"exact character feedforward on every local word"));
  check(k.joint_correct_and_accepted_probability===frac(3n**BigInt(k.word_character_image_rank),BigInt(G))&&k.universal_exact_character_feedforward_ceiling===frac(3n**BigInt(n),BigInt(G)),"feedforward yield");
  check(k.joint_word_table_used_for_character_search===false&&k.approximate_or_noncharacter_outcome_corrections_ruled_out===false,"polynomial local audit / no universal lower bound");
  const jw=words(d*B),values=jw.map(z=>Array.from({length:n},(_,l)=>mod(table.reduce((s,T,j)=>s+T[index(z.slice(j*d,(j+1)*d))][l],0),q))),counts=new Map(),coarse=new Map();
  same(f.joint_words,jw,"joint words");same(f.joint_frequencies,values,"one shared secret on actual summed maps");jointWords+=jw.length;
  for(const v of values){counts.set(key(v),(counts.get(key(v))||0)+1);const C=key(v.map(x=>x%H));if(!coarse.has(C))coarse.set(C,[]);coarse.get(C).push(v);}
  const D=jw.length,squares=Array.from(counts.values()).reduce((s,x)=>s+x*x,0),full=Array.from(counts.values()).reduce((s,x)=>s+Math.sqrt(x),0)**2/(G*D);
  check(f.zero_erasure_herald_probability===frac(BigInt(squares),BigInt(D)**2n)&&f.zero_erasure_conditional_correct_probability===frac(BigInt(D)**2n,BigInt(G*squares))&&f.zero_erasure_joint_correct_probability===frac(1n,BigInt(G)),"exact herald/conditional/joint distinction");
  check(f.frequency_chi_square_from_uniform===frac(BigInt(G*squares-D*D),BigInt(D)**2n)&&Math.abs(f.ideal_full_secret_PGM_success-full)<2e-10,"ideal PGM information certificate only");
  let digit=0;for(const entries of coarse.values()){
    const base=entries[0],fine=new Map();for(const v of entries){const F=key(v.map((x,l)=>mod(x-base[l],q)/H));fine.set(F,(fine.get(F)||0)+1);}digit+=Array.from(fine.values()).reduce((s,x)=>s+Math.sqrt(x),0)**2;
  }
  check(Math.abs(f.ideal_lowest_digit_success_shared_high_secret-digit/(3**n*D))<2e-10&&f.independent_high_secret_twirl_per_program_used===false&&f.exact_reference_not_efficient_fiber_compiler===true,"correct shared-higher-secret twirl");
  const L=c.all_outcome_likelihood_reference,secrets=words(n,q),probabilities=secrets.map(u=>table.map(T=>ws.map(t=>{
    let re=0,im=0;ws.forEach((z,i)=>{const angle=2*Math.PI*(mod(dot(u,T[i]),q)/q-mod(dot(t,z),3)/3);re+=Math.cos(angle);im+=Math.sin(angle);});return(re*re+im*im)/ws.length**2;
  })));
  for(const row of probabilities)for(const p of row)check(Math.abs(p.reduce((s,x)=>s+x,0)-1)<2e-10,"all-record local likelihood normalization");
  check(L.MAP_witnesses.length===D&&L.secret_hypotheses_enumerated===String(G)&&L.joint_outcomes_enumerated===D,"exponential classical MAP reference dimensions");
  let mapSum=0;L.MAP_witnesses.forEach((w,i)=>{
    const t=Array.from({length:B},(_,j)=>jw[i].slice(j*d,(j+1)*d));same(w.local_word_Fourier_outcomes,t,"all word Fourier records retained");
    const indices=t.map(index),likelihood=probabilities.map(row=>indices.reduce((p,k,j)=>p*row[j][k],1)),maximum=Math.max(...likelihood),arg=secrets.findIndex(u=>key(u)===key(w.maximizing_shifted_secret));
    check(arg>=0&&Math.abs(likelihood[arg]-maximum)<2e-10&&Math.abs(w.maximum_likelihood-maximum)<2e-10,"actual all-record MAP witness");mapSum+=maximum;
  });
  check(Math.abs(L.mean_all_outcome_classical_MAP_success-mapSum/G)<2e-10&&mapSum/G<=full+2e-10,"MAP mean success and optimal collective upper bound");
  for(const k of["public_shared_frequency_shift_changes_uniform_prior_MAP_success","polynomial_time_classical_likelihood_optimizer_supplied"])check(L[k]===false,"all-record inference scope: "+k);
  check(L.classical_maximization_enumerates_all_secrets===true&&L.all_erasure_outcomes_used_not_only_exact_characters===true,"not character-only postselection");
  const replay=c.instrument_replay;
  check(replay.unknown_state_preparation_inverse_used===false,"unknown source inverse not granted");
  for(const b of replay.branches){
    const amps=new Map();jw.forEach((z,i)=>{const angle=2*Math.PI*(dot(replay.full_root_secret,values[i])/q-dot(b.erasure_word,z)/3),v=key(values[i]),old=amps.get(v)||[0,0];amps.set(v,[old[0]+Math.cos(angle)/D,old[1]+Math.sin(angle)/D]);});
    let mass=0,re=0,im=0;for(const[v,[a,beta]]of amps){mass+=a*a+beta*beta;const angle=-2*Math.PI*dot(b.group_Fourier_output,JSON.parse(v))/q;re+=a*Math.cos(angle)-beta*Math.sin(angle);im+=a*Math.sin(angle)+beta*Math.cos(angle);}
    check(Math.abs(mass-b.herald_probability)<2e-10&&Math.abs((re*re+im*im)/G-b.joint_correct_probability)<2e-10&&Math.abs(b.joint_correct_probability-1/G)<2e-10,"actual erasure/Fourier replay");
    same(b.group_Fourier_output,replay.full_root_secret.map((s,l)=>mod(s-b.secret_correction[l],q)),"feedforward sign");branches++;
  }
}
for(const x of R.scaling_ledgers)ledger(x);
console.log(JSON.stringify({status:"PASS",joint_words:jointWords,full_ring_corrections_examined:ringCorrections,actual_erasure_branches:branches,all_record_MAP_witnesses:jointWords,upstream_source_law_independently_certified:false}));

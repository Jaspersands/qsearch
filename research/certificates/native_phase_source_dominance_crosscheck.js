"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const C=require("./cyclotomic_exact.js");
const {check,same,rat:F,add,sub,mul,div,str,parse,cmp,field,matrices}=C;
const zero=F(0n),one=F(1n),I=x=>F(BigInt(x));
const B=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact integer encoding");return BigInt(x);};
const mod=(a,q)=>(a%q+q)%q,min=(a,b)=>cmp(a,b)<=0n?a:b;
const bitlen=x=>x===0n?0:x.toString(2).length;
function words(q,n){if(!n)return [[]];return words(q,n-1).flatMap(a=>Array.from({length:q},(_,j)=>[...a,j]));}
function law(labels,q,secrets){
  const chi=[[-1,F(1n,4n)],[0,F(1n,2n)],[1,F(1n,4n)]],errors=words(3,labels.length),law=new Map();
  secrets.forEach((s,k)=>{
    const center=labels.map(a=>C.mod(a.reduce((v,x,j)=>v+x*s[j],0),q));
    for(const indices of errors){
      const values=indices.map((index,i)=>C.mod(center[i]+chi[index][0],q)),key=values.join(","),probability=indices.reduce((p,index)=>mul(p,chi[index][1]),one);
      if(!law.has(key))law.set(key,{values,probabilities:secrets.map(()=>zero)});
      const p=law.get(key).probabilities;p[k]=add(p[k],probability);
    }
  });
  return law;
}
function control(c){
  const q=Number(B(c.modulus)),n=c.dimension,M=c.native_inputs,D=3**M,K=field(q),A=matrices(K),secrets=words(q,n),G=secrets.length,source=law(c.labels,q,secrets),W=words(3,M);
  check(c.status==="EXACT_ORIGINAL_SOURCE_QUANTUM_DUAL_REVIEW_PENDING"&&c.labels.length===2*M&&c.labels.every(a=>a.length===n&&a.every(x=>Number.isSafeInteger(x)&&x>=0&&x<q)),"complete native source control labels");
  same(c.uniform_prior_secret_order,secrets,"complete canonical shared-secret prior");
  check(c.classical_originals===2*M&&B(c.classical_transcript_space)===BigInt(q)**BigInt(2*M)&&c.complete_nonzero_transcripts.length===source.size,"no truncated original data or hidden secret space");
  const rho=secrets.map(()=>A.zeroM(D,D)),gamma=A.zeroM(D,D),readout=W.map(()=>secrets.map(K.F)),seen=new Set();
  let ceilingTrace=zero;
  for(const record of c.complete_nonzero_transcripts){
    const key=record.values.join(","),item=source.get(key);check(item&&!seen.has(key),"every nonzero transcript represented exactly once");seen.add(key);
    same(record.values,item.values,"original source transcript");same(record.conditional_probabilities,item.probabilities.map(str),"all source error vectors summed with modular collisions");
    const largest=item.probabilities.reduce((a,b)=>cmp(a,b)>=0n?a:b,zero),weight=div(largest,I(G));
    check(record.max_joint_probability===str(weight),"correct original-data Bayes weight");ceilingTrace=add(ceilingTrace,weight);
    item.probabilities.forEach(p=>check(cmp(sub(weight,div(p,I(G))),zero)>=0n,"EVERY quantum dual difference has nonnegative pure-state weights"));
    const phases=W.map(word=>word.reduce((s,j,i)=>s+(j===0?0:record.values[2*i+j-1]),0));
    for(let i=0;i<D;i++)for(let j=0;j<D;j++){
      const pure=K.scale(K.powers[C.mod(phases[i]-phases[j],q)],F(1n,BigInt(D)));
      gamma[i][j]=K.plus(gamma[i][j],K.scale(pure,weight));
      item.probabilities.forEach((p,k)=>{rho[k][i][j]=K.plus(rho[k][i][j],K.scale(pure,p));});
    }
    W.forEach((t,outcome)=>{
      let amplitude=K.F();W.forEach((word,i)=>{const tritPhase=word.reduce((s,x,j)=>s+x*t[j],0);amplitude=K.plus(amplitude,K.powers[C.mod(phases[i]-(q/3)*tritPhase,q)]);});
      const probability=K.scale(K.times(amplitude,K.conj(amplitude)),F(1n,BigInt(D*D)));
      item.probabilities.forEach((p,k)=>{readout[outcome][k]=K.plus(readout[outcome][k],K.scale(probability,p));});
    });
  }
  check(seen.size===source.size,"complete original source coverage");
  check(c.original_source_Bayes_success_exact===str(ceilingTrace),"exact source optimal classical decision success");
  check(A.eq(gamma,A.decode(c.quantum_discrimination_dual_exact,D,D)),"independent exact feasible quantum dual matrix");
  let trace=K.F();gamma.forEach((row,i)=>trace=K.plus(trace,row[i]));check(K.eq(trace,K.scale(K.unit,ceilingTrace)),"dual trace is original-data Bayes success");
  check(c.conditional_quantum_densities_exact.length===G&&c.native_F3_readout_likelihoods_exact.length===D,"complete quantum ensemble and downstream outcome table");
  rho.forEach((R,k)=>{
    check(A.eq(R,A.decode(c.conditional_quantum_densities_exact[k],D,D)),"exact actual error-averaged native density");
    let mass=K.F();R.forEach((row,i)=>mass=K.plus(mass,row[i]));check(K.eq(mass,K.unit),"every complete native source state has unit trace");
    check(c.native_F3_readout_likelihoods_exact.every(row=>row.length===G),"complete readout conditional secret columns");
    let outcomes=K.F();readout.forEach((row,i)=>{check(K.eq(row[k],K.decode(c.native_F3_readout_likelihoods_exact[i][k])),"actual F3 outcome likelihood, no invented source");outcomes=K.plus(outcomes,row[k]);});
    check(K.eq(outcomes,K.unit),"all F3 outcomes retained and normalized");
  });
  check(!c.numerical_diagnostics_are_optimality_certificates&&!c.complete_Bayes_reference_is_efficient_classical_algorithm&&!c.calibration_is_LWE_hardness_source&&!c.computational_quantum_advantage_refuted,"statistical dominance is not efficient dequantization or cryptanalysis");
  return {nonzeroTranscripts:source.size,dualEntries:D*D,densityEntries:G*D*D,readoutEntries:D*G,dualDifferences:G};
}
function budget(p){
  const q=B(p.modulus),M=B(p.native_inputs),alpha=parse(p.alpha),epsilon=parse(p.hypothetical_ideal_receiver_success_lower),V=add(div(mul(F(q*q),mul(alpha,alpha)),I(3)),F(1n,2n));
  const bits=64+bitlen(2n*M-1n),noise=min(one,div(mul(I(20),V),F(q*q))),gate=min(one,F(2n*M,2n**BigInt(bits))),loss=min(one,add(mul(F(M),noise),gate)),positive=cmp(loss,epsilon)<0n;
  check(p.published_source_parameter_guard===(cmp(mul(F(q*q),mul(alpha,alpha)),I(4*p.dimension))>=0n)&&p.noise_and_gate_success_loss_upper===str(loss)&&p.pre_rounding_transfer_success_lower===str(positive?sub(epsilon,loss):zero)&&p.pre_rounding_transfer_is_positive===positive,"sample-count and quality joint transfer accounting");
  check(!p.noise_budget_failure_is_a_receiver_impossibility_proof&&p.source_rounding_not_included_in_this_pre_rounding_profile&&!p.receiver_implemented&&!p.hardness_transfer_admitted,"vacuous sufficient budget is not a no-go theorem");
}
function run(r){
  check(r.status==="ORIGINAL_CLASSICAL_SOURCE_STATISTICAL_DOMINANCE_REVIEW_PENDING"&&r.any_quantum_receiver_Bayes_success_at_most_original_source_MAP&&!r.information_gain_over_original_classical_source&&!r.efficient_classical_dequantization_proved&&!r.quantum_speedup_refuted&&!r.accepted_speedup_candidate,"original source statistical ceiling, computational advantage still open");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../NATIVE_PHASE_SOURCE_DOMINANCE.md"))).digest("hex"),"pinned scientific derivation");
  same(r.controls.map(c=>[c.dimension,Number(B(c.modulus)),c.native_inputs,c.seed]),[[1,3,1,132000],[2,3,1,132001],[1,9,1,132002],[1,3,2,132003],[2,3,2,132004]],"precommitted native calibration regimes");
  const counts=r.controls.map(control),sum=k=>counts.reduce((s,c)=>s+c[k],0);
  same(r.source_budget_controls.map(p=>[p.dimension,String(B(p.modulus)),p.alpha,String(B(p.native_inputs)),p.hypothetical_ideal_receiver_success_lower]),[[64,String(3n**64n),"1/1048576","512","1/2"],[64,String(3n**64n),"1/1048576",String(2n**40n),"1/2"]],"same noise/source different hypothetical copy count");r.source_budget_controls.forEach(budget);
  return {status:"PASS",complete_controls:counts.length,nonzero_source_transcripts:sum("nonzeroTranscripts"),exact_dual_entries:sum("dualEntries"),exact_conditional_density_entries:sum("densityEntries"),exact_readout_likelihood_entries:sum("readoutEntries"),positive_dual_difference_decompositions:sum("dualDifferences"),source_budget_controls:r.source_budget_controls.length,efficient_classical_dequantization_proved:false,quantum_speedup_refuted:false};
}
const input=process.argv[2]||path.join(__dirname,"../classical_baselines/native_phase_source_dominance.json");
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));

"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const C=require("./cyclotomic_exact.js"),{check,same,rat:F,add,sub,mul,div,str,parse,cmp}=C;
const zero=F(0n),one=F(1n),two=F(2n),min=(a,b)=>cmp(a,b)<=0n?a:b,abs=a=>F(a[0]<0n?-a[0]:a[0],a[1]);
const pow=(a,k)=>F(a[0]**BigInt(k),a[1]**BigInt(k));
const parity=x=>{let y=0;for(;x;x>>>=1)y^=x&1;return y;};
function rank(rows){let pivots=new Map();for(let x of rows){while(x){let p=31-Math.clz32(x);if(pivots.has(p))x^=pivots.get(p);else{pivots.set(p,x);break;}}}return pivots.size;}
function local(c){
  const r=c.recipe,a=parse(r.overlap),a2=mul(a,a),p0=div(add(one,a),two),p1=div(sub(one,a),two),qmin=div(sub(one,a2),F(4n));
  check(cmp(a,zero)>0n&&cmp(a,one)<0n&&r.rows.length===4,"actual binary channel overlap");
  r.rows.forEach((row,v)=>{
    let masses=[];for(let t=0;t<2;t++)masses.push(mul(mul(((v>>1)^t)?p1:p0,((v&1)^t)?p1:p0),t?p1:p0));
    let q=add(masses[0],masses[1]),ratio=div(qmin,q),residual=sub(q,qmin);
    check(row.frequency_quotient===v&&row.total_mass===str(q)&&row.compression_cosine_squared===str(div(masses[0],q))&&row.compression_sine_squared===str(div(masses[1],q))&&row.filter_success_squared===str(ratio)&&row.filter_failure_squared===str(sub(one,ratio)),"controlled compression and filter norm");same(row.mass,masses.map(str),"both conditional frequency amplitudes");
    check(str(residual)===(v===0?str(a2):"0"),"only zero quotient fails, with no codeword phase");
  });
  check(r.joint_success===str(sub(one,a2))&&r.joint_erasure===str(a2)&&r.product_USD_with_parity_success===str(add(sub(one,mul(F(3n),a2)),mul(two,pow(a,3))))&&r.coherent_failure_state_is_codeword_independent&&r.per_block_quantum_register_bits===4&&!r.unknown_codeword_in_gate_parameters&&!r.hardware_synthesis_implemented,"collective improvement with known four-qubit operations");
  same(r.operations,["xor frequency bit3 into bits1 and2","four quotient-controlled real rotations on bit3","quotient-controlled herald rotation","Hadamards on bits1 and2 conditioned on success"],"clean literal operation order");
  same(c.input_and_output_Gram_entries,Array.from({length:16},(_,k)=>k%4===Math.floor(k/4)?"1":str(a2)),"all exact input/output inner products");
  const coherentErasure=div(mul(F(4n),a2),add(one,mul(F(3n),a2)));
  check(c.normalized_equal_superposition_erasure_probability===str(coherentErasure)&&Math.abs(c.equal_superposition_erasure_diagnostic-Number(coherentErasure[0])/Number(coherentErasure[1]))<1e-12&&!c.classical_codeword_erasure_law_applies_to_every_coherent_prior,"explicit coherent-prior counterexample to unqualified erasure probability");
  check(c.coherent_four_codeword_errors_diagnostic.length===4&&c.coherent_four_codeword_errors_diagnostic.every(x=>Number.isFinite(x)&&x<1e-12)&&Number.isFinite(c.unitarity_error_diagnostic)&&c.unitarity_error_diagnostic<1e-12&&!c.numerical_controls_are_theorem_certificates,"bounded numerical gate conformance, separate from exact identities");
}
function p0(labels,signs,x,i,c){let plus=one,minus=one;for(let k=0;k<3;k++){let f=parity(labels[i][k]&x)^signs[i][k];let term=f?F(-c[0],c[1]):c;plus=mul(plus,add(one,term));minus=mul(minus,sub(one,term));}return div(plus,add(plus,minus));}
function law(r){
  const h=r.outer_bits,B=r.labels.length,labels=r.labels,j=r.signs,c=parse(r.overlap),p=mul(c,c),size=2**(h+B),proposal=Array(size).fill(zero),exact=[],tilts=[];
  check(r.status==="EXACT_FULL_GIBBS_AND_BLOCK_PRANGE_CONTROL"&&h>=1&&h+B<=14&&B<=8,"bounded full-law census only");
  let bad=zero,Zt=zero;
  check(r.subsets.length===2**B,"complete subset mass, no success conditioning");
  for(let mask=0;mask<2**B;mask++){
    const selected=Array.from({length:B},(_,i)=>i).filter(i=>(mask>>i)&1),eq=selected.flatMap(i=>[0,1].map(k=>[labels[i][k]^labels[i][2],j[i][k]^j[i][2]])),solutions=Array.from({length:2**h},(_,i)=>i).filter(x=>eq.every(([a,b])=>parity(a&x)===b)),rk=rank(eq.map(x=>x[0])),q=mul(pow(p,selected.length),pow(sub(one,p),B-selected.length)),tilt=F(BigInt(solutions.length)*2n**BigInt(2*selected.length),2n**BigInt(h)),good=solutions.length>0&&rk===2*selected.length,s=r.subsets[mask];
    check(s.mask===mask&&s.rank===rk&&s.consistent===(solutions.length>0)&&s.solution_count===solutions.length&&s.proposal_mass===str(q)&&s.tilt===str(tilt)&&s.good===good,"rank, frustration, multiplicity and subset tilt");
    tilts.push(mul(q,tilt));Zt=add(Zt,mul(q,tilt));
    if(!good){bad=add(bad,q);proposal[0]=add(proposal[0],q);continue;}
    for(const x of solutions)for(let z=0;z<2**B;z++){let probability=div(q,F(BigInt(solutions.length)));for(let i=0;i<B;i++){let a=p0(labels,j,x,i,c);probability=mul(probability,((z>>i)&1)?sub(one,a):a);}proposal[x+(z<<h)]=add(proposal[x+(z<<h)],probability);}
  }
  for(let z=0;z<2**B;z++)for(let x=0;x<2**h;x++){let weight=one;for(let i=0;i<B;i++)for(let k=0;k<3;k++){let f=parity(labels[i][k]&x)^j[i][k]^((z>>i)&1);weight=mul(weight,add(one,f?F(-c[0],c[1]):c));}exact.push(weight);}
  const Z=exact.reduce(add,zero),G=exact.map(x=>div(x,Z)),tv=div(G.reduce((s,x,i)=>add(s,abs(sub(x,proposal[i]))),zero),two),subsetTV=div(r.subsets.reduce((s,x,i)=>add(s,abs(sub(parse(x.proposal_mass),div(tilts[i],Zt)))),zero),two);
  check(r.bad_subset_mass===str(bad)&&r.tilted_subset_normalization===str(Zt)&&r.subset_TV===str(subsetTV)&&r.complete_output_TV===str(tv)&&cmp(tv,add(subsetTV,bad))<=0n&&str(proposal.reduce(add,zero))==="1"&&!r.failures_conditioned_away&&!r.bounded_exact_law_is_scalable_sampler,"complete Gibbs comparison with fallback and normalization paid");
  same(r.Gibbs_probabilities,G.map(str),"every Gibbs atom");same(r.sampler_probabilities,proposal.map(str),"every actual sampler atom including fallback");return [tv,bad];
}
function scaling(r){
  const B=r.blocks,h=r.outer_bits,c=parse(r.overlap),p=mul(c,c),ceilLog=B>1?(BigInt(B)-1n).toString(2).length:0,cutoff=Math.max(0,Math.min(B,Math.floor((h-(ceilLog+8))/2)));
  // Common integer denominator avoids thousands of large rational gcd calls.
  let term=(p[1]-p[0])**BigInt(B),tailNumerator=0n;
  for(let s=0;s<=B;s++){
    if(s>cutoff)tailNumerator+=term;
    if(s<B){const numerator=term*BigInt(B-s)*p[0],denominator=BigInt(s+1)*(p[1]-p[0]);check(numerator%denominator===0n,"integer binomial term recurrence");term=numerator/denominator;}
  }
  const tail=F(tailNumerator,p[1]**BigInt(B));
  const rk=min(one,F(2n**BigInt(2*cutoff)-1n,2n**BigInt(h))),bad=min(one,add(tail,rk)),rho=F(BigInt(h),BigInt(B)),joint=mul(two,p),naive=sub(mul(F(3n),p),pow(c,3));
  check(r.cutoff===cutoff&&r.exact_binomial_tail===str(tail)&&r.good_size_rank_failure_union_upper===str(rk)&&r.mean_bad_subset_probability_upper===str(bad)&&r.mean_classical_Gibbs_TV_upper===str(min(one,mul(F(3n),bad)))&&r.outer_constraints_per_block===str(rho)&&r.joint_quantum_erasure_load_per_block===str(joint)&&r.matched_classical_block_constraint_load_per_block===str(joint)&&r.independent_clause_Prange_load_per_block===str(naive)&&r.naive_baseline_would_suggest_quantum_threshold_improvement===(cmp(joint,rho)<0n&&cmp(rho,naive)<0n)&&r.matched_classical_threshold_same&&!r.efficient_quantum_advantage_established,"large exact tail and same-rank matched classical threshold");
  const planted=div(pow(add(one,mul(F(3n),p)),B),F(2n**BigInt(h))),zeroSampler=min(one,div(one,planted)),prangeAtom=min(one,add(add(tail,rk),F(2n**BigInt(2*cutoff),2n**BigInt(h)))),difference=sub(sub(one,zeroSampler),prangeAtom),lower=cmp(difference,zero)<0n?zero:difference;
  check(r.all_zero_sign_partition_tilt_lower===str(planted)&&r.all_zero_sign_block_Prange_mean_TV_lower===str(lower)&&r.all_zero_sign_zero_outer_sampler_mean_TV_upper===str(zeroSampler)&&!r.fixed_sign_claim_inferred_from_random_sign_average&&!r.failure_of_one_classical_sampler_proves_quantum_advantage,"planted normalization failure and matched alternative classical attack");
}
function run(r){
  check(r.status==="CONSTRUCTIVE_PARITY_BLOCK_USD_CLASSICALLY_MATCHED_REVIEW_PENDING"&&!r.general_DQI_impossibility_claimed&&!r.native_LWE_decoder_supplied&&!r.accepted_speedup_candidate&&!r.hardware_synthesis_implemented,"scoped negative result, not a general decoder or no-go");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../PARITY_BLOCK_USD_PRANGE.md"))).digest("hex"),"pinned derivation");
  check(r.local_quantum_controls.length===3&&r.complete_sign_censuses.length===3&&r.scaling_controls.length===4&&r.live_classical_samples.length===32,"complete committed controls");
  r.local_quantum_controls.forEach((c,i)=>{check(c.recipe.overlap===["1/3","1/2","2/3"][i],"fixed overlap controls");local(c);});
  const configs=[[2,[[1,2,3],[1,3,2]]],[3,[[1,2,4],[2,3,5]]],[1,[[1,1,1],[0,1,1]]]];
  r.complete_sign_censuses.forEach((s,k)=>{check(s.outer_bits===configs[k][0]&&s.random_sign_cases.length===64,"all random signs for a fixed public matrix");same(s.labels,configs[k][1],"committed label matrix");let total=zero,bad;
    s.random_sign_cases.forEach((x,i)=>{same(x.labels,s.labels,"unchanged matrix across signs");check(x.outer_bits===s.outer_bits&&x.overlap==="1/2","same source");same(x.signs,[Array.from({length:3},(_,j)=>(i>>(5-j))&1),Array.from({length:3},(_,j)=>(i>>(2-j))&1)],"all six sign bits, in order");let t=law(x);total=add(total,t[0]);if(bad===undefined)bad=t[1];else check(str(t[1])===str(bad),"rank failure is sign independent");});
    const mean=div(total,F(64n)),bound=min(one,mul(F(3n),bad));check(s.mean_complete_output_TV===str(mean)&&s.bad_subset_probability===str(bad)&&s.mean_TV_upper===str(bound)&&cmp(mean,bound)<=0n,"complete sign-average finite dequantization bound");});
  r.scaling_controls.forEach((s,i)=>{check(s.blocks===[32,128,512,4096][i]&&s.outer_bits===Math.floor((11*s.blocks+19)/20)&&s.overlap==="1/2","fixed scaling family");scaling(s);});
  const instance=r.live_classical_instance;check(instance.outer_bits===16&&instance.labels.length===24&&instance.signs.length===24,"public live instance");
  let successes=0;
  r.live_classical_samples.forEach(s=>{check(s.fallback_mass_is_charged&&new Set(s.selected).size===s.selected.length&&s.selected.every(i=>Number.isInteger(i)&&i>=0&&i<24),"all drawn subsets and fallback retained");let eq=s.selected.flatMap(i=>[0,1].map(k=>[instance.labels[i][k]^instance.labels[i][2],instance.signs[i][k]^instance.signs[i][2]])),rk=rank(eq.map(e=>e[0]));check(s.rank===rk,"live affine rank");if(s.success){check(rk===eq.length&&eq.every(([a,b])=>parity(a&s.outer)===b)&&s.outer>=0&&s.outer<65536&&s.inner>=0&&s.inner<2**24,"actual live outer solution and inner sample domain");successes++;}else check(rk<eq.length&&s.outer===0&&s.inner===0,"rank-defect fallback is explicit");});
  check(r.negative_result_scope==="joint three-message parity USD does not establish a Gibbs sampling speedup over correlated block-Prange on this family","negative scope fixed");
  return {status:"PASS",local_quantum_programs:3,exact_codeword_Gram_entries:48,complete_signed_instances:192,scaling_profiles:4,live_classical_samples:32,live_successes:successes,quantum_advantage_established:false};
}
if(require.main===module){const input=process.argv[2]||path.join(__dirname,"../classical_baselines/parity_block_usd_prange.json");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));}
module.exports={run};

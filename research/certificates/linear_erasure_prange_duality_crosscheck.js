"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {check, same, rat:F, add, sub, mul, div, str, parse, cmp} = require("./cyclotomic_exact.js");
const zero=F(0n), one=F(1n), two=F(2n);
const pow=(a,n)=>F(a[0]**BigInt(n),a[1]**BigInt(n));
const min=(a,b)=>cmp(a,b)<=0n?a:b;
const abs=a=>F(a[0]<0n?-a[0]:a[0],a[1]);
const sum=a=>a.reduce(add,zero);
function integer(x){
  check((typeof x==="bigint"&&x>=0n)||(typeof x==="number"&&Number.isSafeInteger(x)&&x>=0)||(typeof x==="string"&&/^(0|[1-9][0-9]*)$/.test(x)),"exact nonnegative integer encoding");
  return BigInt(x);
}
function parity(x){let p=0;for(x=integer(x);x;x>>=1n)p^=Number(x&1n);return p;}
function rank(rows){
  const pivots=new Map();
  for(let x of rows.map(integer))while(x){const p=x.toString(2).length-1;if(pivots.has(p))x^=pivots.get(p);else{pivots.set(p,x);break;}}
  return pivots.size;
}
function space(basis){let S=[0];for(const b of basis)S=[...new Set([...S,...S.map(x=>x^b)])];return S.sort((a,b)=>a-b);}
function linearSpaces(width){
  const out=[];
  // Enumeration by subsets is independent of the producer's basis enumeration.
  for(let mask=1;mask<2**(2**width);mask+=2){
    const S=Array.from({length:2**width},(_,i)=>i).filter(i=>(mask>>i)&1);
    if((S.length&(S.length-1))===0&&S.every(a=>S.every(b=>S.includes(a^b))))out.push(S);
  }
  return out.sort((a,b)=>a.length-b.length||a.reduce((d,x,i)=>d||x-b[i],0));
}
function completeSpaces(width){
  const unique=new Map();
  for(const S of linearSpaces(width))for(let a=0;a<2**width;a++){
    const shifted=S.map(x=>x^a).sort((x,y)=>x-y);unique.set(JSON.stringify(shifted),shifted);
  }
  return [...unique.values()].sort((a,b)=>a.length-b.length||a.reduce((d,x,i)=>d||x-b[i],0));
}
const bases=[[1,2,4],[1],[2],[4],[7],[]];
function expectedMixture(c){
  const p=mul(c,c),weights=[pow(sub(one,p),2),...Array(4).fill(div(mul(p,sub(one,p)),two)),pow(p,2)];
  const branches=bases.map((basis,i)=>({basis,weight:weights[i],members:space(basis),dimension:basis.length}));
  const q=Array.from({length:8},(_,y)=>sum(branches.filter(b=>b.members.includes(y)).map(b=>div(b.weight,F(BigInt(b.members.length))))));
  return {branches,q,load:sub(mul(F(4n),p),pow(c,4))};
}
function mixture(record, c){
  const expected=expectedMixture(c);
  check(record.width===3&&record.branches.length===6&&!record.codeword_branch_law_is_universal_coherent_prior_law&&!record.universal_quantum_dequantization_claimed,"origin-linear instrument contract, not arbitrary coherent priors");
  record.branches.forEach((r,i)=>{
    const b=expected.branches[i],dim=b.dimension,ann=r.annihilator_basis;
    same(r.basis,b.basis,"fixed independent branch basis");
    check(r.offset===0&&r.dimension===dim&&r.weight===str(b.weight)&&r.unknown_quantum_bits===3-dim&&r.classical_affine_constraints===3-dim,"same quantum erasure and classical constraint dimension");
    check(ann.length===3-dim&&rank(ann)===ann.length&&ann.every(u=>Number.isInteger(u)&&u>0&&u<8&&b.basis.every(v=>parity(u&v)===0)),"complete independent annihilator basis");
  });
  same(record.frequency_probabilities,expected.q.map(str),"exact entire frequency distribution");
  check(record.branch_codeword_phase==="(-1)^(d dot offset), retained until recovery permits correction","affine branch phase retained");
  check(record.mean_unknown_bits===str(expected.load),"exact expected unknown dimension");
  // Exact Stinespring column norms and branch character orthogonality.
  for(let y=0;y<8;y++)check(str(sum(expected.branches.filter(b=>b.members.includes(y)).map(b=>div(b.weight,mul(F(BigInt(b.members.length)),expected.q[y])))))==="1","split isometry column norm");
  return expected;
}
function quantum(r){
  const c=parse(r.overlap),p0=div(add(one,c),two),p1=div(sub(one,c),two),E=mixture(r.mixture,c);
  check(cmp(c,zero)>0n&&cmp(c,one)<0n&&r.compression.length===8,"physical four-message channel");
  r.compression.forEach((row,y)=>{
    const w=parity(y)===1?(y===7?3:1):(y===0?0:2);
    const masses=[mul(pow(p0,4-w),pow(p1,w)),mul(pow(p0,w),pow(p1,4-w))];
    check(row.quotient===y&&row.quotient_mass===str(sum(masses))&&row.quotient_mass===str(E.q[y]),"source compression equals positive mixture");
    same(row.conditional_masses,masses.map(str),"both conditional parity-scratch masses");
  });
  const grams=[];
  for(let d=0;d<8;d++)for(let e=0;e<8;e++){
    const z=d^e,cw=z|(parity(z)<<3),weight=cw.toString(2).split("1").length-1;
    const target=sum(E.branches.filter(b=>b.basis.every(v=>parity(z&v)===0)).map(b=>b.weight));
    check(str(target)===str(pow(c,weight)),"exact preservation of every codeword inner product");grams.push(str(target));
  }
  same(r.exact_input_output_Gram_entries,grams,"all64 exact Gram entries");
  const prior=E.branches.map(b=>div(b.weight,mul(F(BigInt(b.members.length)),E.q[0])));
  same(r.normalized_equal_superposition_branch_probabilities,prior.map(str),"coherent-prior branch law differs from single codewords");
  check(r.coherent_prior_branch_probabilities_diagnostic.length===6&&r.coherent_prior_branch_probabilities_diagnostic.every((x,i)=>Number.isFinite(x)&&Math.abs(x-Number(prior[i][0])/Number(prior[i][1]))<1e-12),"actual coherent input numerical check");
  check(r.constant_local_input_dimension===16&&r.constant_local_output_dimension===96&&Number.isFinite(r.isometry_error_diagnostic)&&r.isometry_error_diagnostic<1e-12&&r.eight_codeword_output_errors_diagnostic.length===8&&r.eight_codeword_output_errors_diagnostic.every(x=>Number.isFinite(x)&&x<1e-12)&&!r.global_coherent_Gibbs_sampler_implemented&&!r.hardware_synthesis_implemented,"bounded real program conformance, not complete hardware or global Gibbs algorithm");
  const product=sub(add(mul(F(6n),pow(c,2)),pow(c,4)),mul(F(4n),pow(c,3))),full=sub(mul(F(6n),pow(c,2)),mul(F(3n),pow(c,4)));
  check(r.mean_unknown_bits===str(E.load)&&r.product_USD_parity_mean_unknown_bits===str(product)&&r.full_block_USD_only_mean_unknown_bits===str(full)&&cmp(E.load,product)<0n&&cmp(E.load,full)<0n,"partial outcome beats weaker decoders but is classically matched");
  return E;
}
function optimality(r,E){
  const z=Array.from({length:8},(_,y)=>y===0?F(3n):parity(y)?one:F(-7n,3n)),spaces=completeSpaces(3);
  same(r.exact_dual_coefficients,z.map(str),"fixed exact optimization dual");
  check(spaces.length===51&&r.all_affine_subspaces.length===51,"all51 affine subspaces, not just instrument support");
  r.all_affine_subspaces.forEach((s,i)=>{
    const S=spaces[i],cost=3-Math.log2(S.length),avg=div(sum(S.map(y=>z[y])),F(BigInt(S.length)));
    same(s.members,S,"complete ordered subspace census");
    check(s.unknown_bits===cost&&s.dual_average===str(avg)&&cmp(avg,F(BigInt(cost)))<=0n,"every exact dual inequality");
  });
  const dual=sum(E.q.map((q,y)=>mul(q,z[y])));
  check(str(dual)===str(E.load)&&r.primal_mean_unknown_bits===str(dual)&&r.dual_lower_bound===str(dual)&&r.optimal_within_positive_affine_subspace_instruments&&!r.optimal_among_all_quantum_measurements,"exact primal-dual equality with restricted scope");
}
function equations(instance,record,selected){
  return selected.flatMap((s,i)=>record.branches[s].annihilator_basis.map(u=>{
    let a=0n;instance.labels[i].forEach((v,j)=>{if((u>>j)&1)a^=integer(v);});
    return [a,parity(u&(instance.signs[i]^record.branches[s].offset))];
  }));
}
function law(r,record,E){
  const h=r.outer_bits,B=r.labels.length,N=E.branches.length,proposal=Array(2**h).fill(zero),tilts=[];
  let bad=zero,Z=zero;
  check(h<=10&&B===2&&r.branches.length===N**B&&!r.fixed_sign_bound_inferred_from_sign_average,"complete bounded signed law");
  r.branches.forEach((s,index)=>{
    const selected=[Math.floor(index/N),index%N];same(s.branches,selected,"complete branch pair population");
    const rows=equations(r,record,selected),rk=rank(rows.map(x=>x[0])),solutions=Array.from({length:2**h},(_,i)=>i).filter(x=>rows.every(([a,b])=>parity(a&BigInt(x))===b));
    const q=mul(E.branches[selected[0]].weight,E.branches[selected[1]].weight),t=F(BigInt(solutions.length)*2n**BigInt(rows.length),2n**BigInt(h)),good=solutions.length>0&&rk===rows.length;
    same(s.solutions,solutions,"every affine solution including empty frustration");
    check(s.constraints===rows.length&&s.rank===rk&&s.proposal_mass===str(q)&&s.tilt===str(t)&&s.good===good,"rank, multiplicity, proposal and tilted mass");
    tilts.push(mul(q,t));Z=add(Z,mul(q,t));
    if(!good){bad=add(bad,q);proposal[0]=add(proposal[0],q);}else for(const x of solutions)proposal[x]=add(proposal[x],div(q,F(BigInt(solutions.length))));
  });
  const weights=Array.from({length:2**h},(_,x)=>r.labels.reduce((p,a,i)=>{
    let y=r.signs[i];a.forEach((label,j)=>{y^=parity(integer(label)&BigInt(x))<<j;});
    return mul(p,mul(F(2n**BigInt(record.width)),E.q[y]));
  },one));
  const normalization=sum(weights),G=weights.map(w=>div(w,normalization)),tv=div(sum(G.map((g,i)=>abs(sub(g,proposal[i])))),two),subsetTV=div(sum(r.branches.map((s,i)=>abs(sub(parse(s.proposal_mass),div(tilts[i],Z))))),two);
  check(str(div(normalization,F(2n**BigInt(h))))===str(Z)&&r.bad_mass===str(bad)&&r.tilted_normalization===str(Z)&&r.subset_TV===str(subsetTV)&&r.complete_output_TV===str(tv)&&cmp(tv,add(subsetTV,bad))<=0n&&str(sum(proposal))==="1","true partition weight and charged fallback inequality");
  same(r.Gibbs_probabilities,G.map(str),"entire Gibbs output law");same(r.sampler_probabilities,proposal.map(str),"entire classical sampler law");
  return {tv,bad};
}
function rankDuality(r,record,expectedInstance,selected){
  check(r.outer_bits===expectedInstance.outer_bits&&r.quantum_unique_reconstruction_iff_classical_full_row_rank&&!r.arbitrary_coherent_prior_success_from_rank_alone,"matched rank contract, not a prior success theorem");
  same(r.labels,expectedInstance.labels,"fixed rank-control label map");same(r.signs,expectedInstance.signs,"fixed rank-control signs");same(r.selected_branches,selected,"all committed branch pairs");
  const rows=equations(r,record,selected),columns=[];
  selected.forEach((s,i)=>record.branches[s].annihilator_basis.forEach(u=>{
    let col=0n;
    for(let a=0;a<r.outer_bits;a++){
      let bit=0;r.labels[i].forEach((label,j)=>{bit^=Number((integer(label)>>BigInt(a))&1n)*((u>>j)&1);});
      col|=BigInt(bit)<<BigInt(a);
    }
    columns.push(col);
  }));
  check(columns.every((c,i)=>c===rows[i][0])&&r.rank===rank(columns)&&r.unknown_bits===columns.length,"exact dual-code reconstruction matrix equals transpose of classical rows");
  same(r.quantum_reconstruction_columns.map(x=>String(integer(x))),columns.map(String),"every quantum column");same(r.classical_equation_rows.map(([a,b])=>[String(integer(a)),b]),rows.map(([a,b])=>[String(a),b]),"every signed classical equation");
}
function scaling(r){
  const B=r.blocks,h=r.outer_bits,c=parse(r.overlap),E=expectedMixture(c),t=F(9n,8n),cutoff=Math.max(0,Math.min(3*B,h-((BigInt(B)-1n).toString(2).length+8)));
  const pgf=sum(E.branches.map(b=>mul(b.weight,pow(t,3-b.dimension)))),tail=min(one,div(pow(pgf,B),pow(t,cutoff+1))),rk=min(one,F(2n**BigInt(cutoff)-1n,2n**BigInt(h))),tv=min(one,mul(F(3n),min(one,add(tail,rk))));
  const product=sub(add(mul(F(6n),pow(c,2)),pow(c,4)),mul(F(4n),pow(c,3))),rho=F(BigInt(h),BigInt(B));
  check(r.cutoff===cutoff&&r.Chernoff_tilt===str(t)&&r.constraint_count_pgf_at_tilt===str(pgf)&&r.constraint_tail_upper===str(tail)&&r.rank_failure_union_upper===str(rk)&&r.mean_classical_Gibbs_TV_upper===str(tv)&&r.matched_quantum_unknown_and_classical_constraint_load===str(E.load)&&r.product_USD_parity_load===str(product)&&r.threshold_above_joint_below_product===(cmp(E.load,rho)<0n&&cmp(rho,product)<0n)&&!r.quantum_full_coherent_prior_success_proved&&r.random_sign_average_not_arbitrary_sign_guarantee,"rational finite Chernoff and same-rank classical threshold, with correct scope");
}
function run(r){
  check(r.status==="POSITIVE_AFFINE_ERASURE_INSTRUMENT_DUALITY_REVIEW_PENDING"&&!r.universal_quantum_dequantization_claimed&&!r.novelty_verified&&!r.accepted_speedup_candidate&&!r.native_hidden_shift_receiver_supplied,"no universal no-go or breakthrough promotion");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../LINEAR_ERASURE_PRANGE_DUALITY.md"))).digest("hex"),"pinned derivation");
  check(r.four_message_quantum_controls.length===3&&r.instrument_optimality_controls.length===3&&r.complete_sign_censuses.length===2&&r.scaling_controls.length===4&&r.live_classical_samples.length===16,"committed complete controls");
  r.four_message_quantum_controls.forEach((q,i)=>{check(q.overlap===["1/3","1/2","2/3"][i],"fixed quantum input overlaps");optimality(r.instrument_optimality_controls[i],quantum(q));});
  const record=r.four_message_quantum_controls[1].mixture,E=expectedMixture(F(1n,2n)),configs=[[2,[[1,2,3],[2,3,1]]],[4,[[1,2,4],[2,4,8]]]];
  r.complete_sign_censuses.forEach((c,j)=>{
    check(c.outer_bits===configs[j][0]&&c.complete_sign_cases.length===64,"all affine sign pairs");same(c.labels,configs[j][1],"fixed matrix sign census");let total=zero,bad;
    c.complete_sign_cases.forEach((s,i)=>{check(s.outer_bits===c.outer_bits,"same dimension");same(s.labels,c.labels,"same label map");same(s.signs,[Math.floor(i/8),i%8],"complete sign ordering");const v=law(s,record,E);total=add(total,v.tv);if(bad===undefined)bad=v.bad;else check(str(bad)===str(v.bad),"rank bad mass independent of signs");});
    const mean=div(total,F(64n)),bound=min(one,mul(F(3n),bad));check(c.mean_output_TV===str(mean)&&c.mean_output_TV_upper===str(bound)&&cmp(mean,bound)<=0n,"complete random-sign classical error guarantee");
  });
  check(r.rank_duality_controls.length===36,"all six-branch pair rank controls");
  r.rank_duality_controls.forEach((c,i)=>rankDuality(c,record,{outer_bits:4,labels:[[1,2,4],[2,4,8]],signs:[1,6]},[Math.floor(i/6),i%6]));
  r.scaling_controls.forEach((s,i)=>{check(s.blocks===[64,256,1024,4096][i]&&s.outer_bits===Math.floor((21*s.blocks+19)/20)&&s.overlap==="1/2","same asymptotic scaling family");scaling(s);});
  const instance=r.live_classical_instance;check(instance.outer_bits===72&&instance.labels.length===64&&instance.signs.length===64,"nonenumerated live public map");
  instance.labels.forEach((row,i)=>check(row.length===3&&row.every(x=>integer(x)<2n**72n)&&Number.isInteger(instance.signs[i])&&instance.signs[i]>=0&&instance.signs[i]<8,"legal72-bit public labels and signs"));
  let successes=0;
  r.live_classical_samples.forEach(s=>{
    check(s.branches.length===64&&s.branches.every(x=>Number.isInteger(x)&&x>=0&&x<6)&&s.fallback_mass_is_charged,"actual branches with paid failure");
    const rows=equations(instance,record,s.branches),rk=rank(rows.map(x=>x[0])),x=integer(s.outer);
    check(s.constraints===rows.length&&s.rank===rk,"independent full-width live rank");
    if(s.success){check(rk===rows.length&&x<2n**72n&&rows.every(([a,b])=>parity(a&x)===b),"legal live affine solution");successes++;}else check(rk<rows.length&&x===0n,"actual rank failure fallback");
  });
  const outside=r.outside_linear_cone_control,q=outside.positive_frequency_probabilities.map(parse);
  same(q.map(str),["1/10","3/10","3/10","3/10"],"positive outside-cone control");
  const Walsh=[1,2,3].map(d=>sum(q.map((w,y)=>parity(d&y)?F(-w[0],w[1]):w)));
  same(outside.negative_nonzero_Walsh_coefficients,Walsh.map(str),"all exact negative character coefficients");
  check(outside.width===2&&outside.witness_frequency===1&&outside.witness_difference_q0_minus_qy===str(sub(q[0],q[1]))&&cmp(sub(q[0],q[1]),zero)<0n&&outside.violated_necessary_condition==="q(0)>=q(y) for every y"&&outside.linear_origin_subspace_mixture_excluded&&!outside.affine_coset_mixture_excluded&&!outside.classical_hardness_established&&!outside.efficient_quantum_sampler_established,"outside this cone does not establish advantage or exclude affine mixtures");
  const signed=outside.matched_affine_instrument,affineBases=[[1,2],[3],[2],[1]],offsets=[0,1,1,2],weights=[F(2n,5n),F(1n,5n),F(1n,5n),F(1n,5n)],signedBranches=affineBases.map((basis,i)=>({basis,offset:offsets[i],members:space(basis).map(x=>x^offsets[i]),weight:weights[i]}));
  check(signed.width===2&&signed.branches.length===4&&signed.mean_unknown_bits==="3/5"&&!signed.codeword_branch_law_is_universal_coherent_prior_law&&!signed.universal_quantum_dequantization_claimed&&signed.branch_codeword_phase==="(-1)^(d dot offset), retained until recovery permits correction"&&!outside.affine_branch_phases_discarded,"signed channel has a matched affine instrument with retained phases");
  signed.branches.forEach((b,i)=>{
    const e=signedBranches[i],ann=b.annihilator_basis; same(b.basis,e.basis,"fixed affine branch direction");
    check(b.offset===e.offset&&b.dimension===e.basis.length&&b.weight===str(e.weight)&&b.unknown_quantum_bits===2-e.basis.length&&b.classical_affine_constraints===2-e.basis.length&&ann.length===2-e.basis.length&&rank(ann)===ann.length&&ann.every(u=>Number.isInteger(u)&&u>0&&u<4&&e.basis.every(v=>parity(u&v)===0)),"affine offset, cost and complete annihilator");
  });
  const signedQ=Array.from({length:4},(_,y)=>sum(signedBranches.filter(b=>b.members.includes(y)).map(b=>div(b.weight,F(BigInt(b.members.length))))));
  same(signed.frequency_probabilities,signedQ.map(str),"entire affine mixture");same(signedQ.map(str),q.map(str),"actual signed-overlap source");
  const signedGrams=[];
  for(let d=0;d<4;d++)for(let e=0;e<4;e++){
    const z=d^e,source=sum(q.map((w,y)=>parity(z&y)?F(-w[0],w[1]):w)),target=sum(signedBranches.filter(b=>b.basis.every(v=>parity(z&v)===0)).map(b=>parity(z&b.offset)?F(-b.weight[0],b.weight[1]):b.weight));
    check(str(source)===str(target),"signed branch phases are necessary for Gram preservation");signedGrams.push(str(target));
  }
  same(outside.exact_input_output_Gram_entries,signedGrams,"all16 signed Gram entries");
  check(outside.codeword_output_errors_diagnostic.length===4&&outside.codeword_output_errors_diagnostic.every(x=>Number.isFinite(x)&&x<1e-12)&&Number.isFinite(outside.isometry_error_diagnostic)&&outside.isometry_error_diagnostic<1e-12,"actual signed isometry numerical conformance");
  const signedDual=[F(-3n),one,one,one],affineSpaces=completeSpaces(2);same(outside.exact_dual_coefficients,signedDual.map(str),"signed instrument dual");
  check(outside.all_affine_subspaces.length===11&&outside.optimal_affine_mean_unknown_bits==="3/5"&&str(sum(q.map((w,y)=>mul(w,signedDual[y]))))==="3/5","signed affine primal-dual equality");
  outside.all_affine_subspaces.forEach((s,i)=>{const S=affineSpaces[i],cost=2-Math.log2(S.length),avg=div(sum(S.map(y=>signedDual[y])),F(BigInt(S.length)));same(s.members,S,"all11 signed affine subspaces");check(s.unknown_bits===cost&&s.dual_average===str(avg)&&cmp(avg,F(BigInt(cost)))<=0n,"signed dual inequality");});
  const classical=outside.complete_matched_classical_control;check(classical.outer_bits===4,"signed example dimension");same(classical.labels,[[1,2],[4,8]],"signed example public matrix");same(classical.signs,[1,2],"signed example shifts");law(classical,signed,{branches:signedBranches,q});
  const signedCensus=outside.complete_sign_census;check(signedCensus.outer_bits===2&&signedCensus.cases.length===16,"complete signed affine-channel census");same(signedCensus.labels,[[1,2],[2,3]],"signed affine census matrix");
  let signedTotal=zero,signedBad;
  signedCensus.cases.forEach((s,i)=>{
    check(s.outer_bits===2,"same signed census dimension");same(s.labels,signedCensus.labels,"same signed public map");same(s.signs,[Math.floor(i/4),i%4],"all16 affine sign pairs");
    const v=law(s,signed,{branches:signedBranches,q});signedTotal=add(signedTotal,v.tv);if(signedBad===undefined)signedBad=v.bad;else check(str(signedBad)===str(v.bad),"signed affine rank bad mass independent of signs");
  });
  const signedMean=div(signedTotal,F(16n)),signedBound=min(one,mul(F(3n),signedBad));check(signedCensus.mean_output_TV===str(signedMean)&&signedCensus.mean_output_TV_upper===str(signedBound)&&cmp(signedMean,signedBound)<=0n,"complete averaged signed affine sampler guarantee");
  check(outside.rank_duality_controls.length===16,"all signed affine branch pair rank controls");outside.rank_duality_controls.forEach((c,i)=>rankDuality(c,signed,{outer_bits:4,labels:[[1,2],[4,8]],signs:[1,2]},[Math.floor(i/4),i%4]));
  check(r.negative_scope==="positive affine-subspace erasure instruments have matched affine-mixture classical rank conditions, with branch phases retained","negative result scope");
  return {status:"PASS",local_partial_quantum_decoders:4,exact_Gram_entries:208,complete_signed_instances:145,exact_dual_subspaces:164,exact_rank_transposes:52,scaling_profiles:4,live_samples:16,live_successes:successes,quantum_advantage_established:false};
}
if(require.main===module){const input=process.argv[2]||path.join(__dirname,"../classical_baselines/linear_erasure_prange_duality.json");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));}
module.exports={run};

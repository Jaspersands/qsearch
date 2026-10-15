#!/usr/bin/env node
"use strict";
// Independent public-H elimination, RREF search, unimodular lattice and exact LLL replay.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {primeCertificate,rref,determinant}=require("./planted_qary_usvp_source_crosscheck.js");
const need=(ok,msg)=>{if(!ok)throw new Error(msg);};
const I=x=>{need((typeof x==="number"&&Number.isSafeInteger(x))||
  (typeof x==="string"&&String(BigInt(x))===x),"exact canonical integer");return BigInt(x);};
const abs=x=>x<0n?-x:x,mod=(x,q)=>(x%q+q)%q;
function gcd(x,y){x=abs(x);y=abs(y);while(y)[x,y]=[y,x%y];return x;}
function R(p,q=1n){need(q!==0n,"zero rational denominator");if(q<0n){p=-p;q=-q;}const d=gcd(p,q);return {p:p/d,q:q/d};}
const add=(x,y)=>R(x.p*y.q+y.p*x.q,x.q*y.q),sub=(x,y)=>R(x.p*y.q-y.p*x.q,x.q*y.q);
const mul=(x,y)=>R(x.p*y.p,x.q*y.q),div=(x,y)=>R(x.p*y.q,x.q*y.p);
const cmp=(x,y)=>x.p*y.q-y.p*x.q,rat=x=>R(I(x.numerator),I(x.denominator));
const equalR=(x,y)=>cmp(x,y)===0n;
const norm=x=>x.reduce((s,a)=>s+a*a,0n);
const dot=(x,y)=>x.reduce((s,a,j)=>add(s,mul(a,y[j])),R(0n));
const canonical=x=>x.find(a=>a!==0n)<0n?x.map(a=>-a):x;
const lex=(x,y)=>{for(let i=0;i<x.length;i++)if(x[i]!==y[i])return x[i]<y[i]?-1:1;return 0;};
const same=(x,y)=>x.length===y.length&&x.every((a,i)=>a===y[i]);
const matrices=(A,B)=>A.length===B.length&&A.every((r,i)=>same(r,B[i]));
const parse=A=>A.map(row=>row.map(I));
const canonicalJSON=x=>Array.isArray(x)?x.map(canonicalJSON):x&&typeof x==="object"?
  Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonicalJSON(x[k])])):x;
function publicProblem(P){
  const q=I(P.prime),H=parse(P.H),n=P.dimension,m=P.constraint_rows;
  need(primeCertificate(P.prime_certificate)===q&&H.length===m&&m<n-1&&
    H.every(row=>row.length===n&&row.every(a=>a>=0n&&a<q)),"certified public modular problem");
  const payload={...P};delete payload.public_problem_sha256;
  need(P.public_problem_sha256===crypto.createHash("sha256").update(JSON.stringify(canonicalJSON(payload))).digest("hex"),"public input digest");
  const rr=rref(H,q);
  need(rr.rank===m&&matrices(parse(P.public_modular_rref),rr.matrix)&&
       JSON.stringify(P.pivot_columns)===JSON.stringify(rr.pivots),"public RREF");
  const free=Array.from({length:n},(_,i)=>i).filter(i=>!rr.pivots.includes(i));
  need(JSON.stringify(free)===JSON.stringify(P.free_columns),"free coordinates");
  const member=v=>v.length===n&&H.every(row=>mod(row.reduce((s,a,i)=>s+a*v[i],0n),q)===0n);
  const B=parse(P.row_basis);
  need(B.length===n&&B.every(member)&&abs(determinant(B))===q**BigInt(m),"full modular kernel basis");
  need(P.solver_input_contains_plant_seed_or_solution===false,"public problem not private advice");
  return {q,H,n,m,rr,free,member,B};
}
function reducedness(rows,C){
  const delta=rat(C.delta),eta=rat(C.eta),alpha=div(R(1n),sub(delta,mul(eta,eta)));
  need(equalR(delta,R(3n,4n))&&equalR(eta,R(51n,100n))&&equalR(rat(C.alpha),alpha),"LLL parameters");
  const orth=[],norms=[],mu=[];
  rows.forEach((row,i)=>{
    let v=row.map(a=>R(a)),coeff=[];
    for(let j=0;j<i;j++){
      const c=div(dot(row.map(a=>R(a)),orth[j]),norms[j]);coeff.push(c);
      v=v.map((a,k)=>sub(a,mul(c,orth[j][k])));
      need(abs(c.p)*eta.q<=eta.p*c.q,"actual size reduction");
    }
    const d=dot(v,v);need(d.p>0n,"full-rank GS");orth.push(v);norms.push(d);mu.push(coeff);
    need(equalR(rat(C.gram_schmidt_squared_norms[i]),d),"GS norms");
    if(i)need(cmp(add(d,mul(mul(coeff[i-1],coeff[i-1]),norms[i-1])),mul(delta,norms[i-1]))>=0n,"actual Lovasz inequalities");
  });
  need(C.gram_schmidt_squared_norms.length===rows.length&&C.size_reduction_verified===true&&
       C.lovasz_verified===true&&C.actual_lambda2_certified===false,"reducedness scope");
  return alpha;
}
function* vectors(length,prefix=[]){if(!length){yield prefix;return;}for(const a of [-1n,0n,1n])yield* vectors(length-1,[...prefix,a]);}
function verifyRow(row){
  const P=publicProblem(row.public_problem),{q,H,n,m,rr,free,member,B}=P;
  need(row.n===n&&row.m===m&&I(row.q)===q&&row.n_minus_m===free.length,"row dimensions");
  const plant=row.PRIVATE_AUDIT_ONLY_plant.map(I),s=Number(norm(plant));
  need(plant.every(a=>[-1n,0n,1n].includes(a))&&plant.some(a=>a!==0n)&&member(plant),"private forward calibration plant");
  const sF=free.filter(f=>plant[f]!==0n).length,sP=m?rr.pivots.filter(p=>plant[p]!==0n).length:0;
  need(s===row.total_support_s&&sF===row.free_support_s_F&&sP===row.pivot_support_s_P&&
       sF>=Math.max(1,s-m)&&sF<=Math.min(s,n-m)&&row.free_support_within_sharp_bounds===true&&
       row.theoretical_min_s_F===Math.max(1,s-m)&&row.theoretical_max_s_F===Math.min(s,n-m),"free support theorem");
  for(let i=0;i<n;i++){
    const u=Array(n).fill(0n);u[i]=1n;need(!member(u),"sparse unit attack");
    for(let j=i+1;j<n;j++)for(const sign of [-1n,1n]){
      const v=u.slice();v[j]=sign;need(!member(v),"sparse signed pair attack");
    }
  }
  need(row.sparse_column_immune_at_s_ge_3===true&&row.sparse_column_attack_status==="NO_UNIT_OR_COLUMN_PAIR_RELATION","finite sparse attack");
  const U=parse(row.public_LLL_unimodular_transform),L=parse(row.public_LLL_reduced_row_basis);
  need(U.length===n&&abs(determinant(U))===1n&&U.every(r=>r.length===n)&&L.every(member),"unimodular LLL basis");
  const product=U.map(r=>Array.from({length:n},(_,j)=>r.reduce((s,u,k)=>s+u*B[k][j],0n)));
  need(matrices(product,L),"actual LLL transform");
  const alpha=reducedness(L,row.LLL_reducedness_certificate);
  const rawBest=L.slice().sort((a,b)=>norm(a)!==norm(b)?(norm(a)<norm(b)?-1:1):lex(a,b))[0];
  const returned=row.public_LLL_vector.map(I);
  need(same(returned,canonical(rawBest))&&same(returned,plant)&&I(row.lll_recovered_squared_norm)===norm(returned),"actual finite LLL recovery");
  let ceiling=R(BigInt(s));for(let i=1;i<n;i++)ceiling=mul(ceiling,alpha);
  need(equalR(rat(row.certified_LLL_squared_norm_ceiling),ceiling)&&
       cmp(R(norm(returned)),ceiling)<=0n&&row.LLL_squared_norm_bound_verified===true&&
       row.lambda2_isolation_premise_verified===false,"conditional bound not isolation proof");
  let count=0,best=null;
  for(const v of vectors(free.length)){
    if(v.find(a=>a!==0n)!==1n)continue;
    count++;
    const full=Array(n).fill(0n);free.forEach((f,j)=>full[f]=v[j]);
    rr.pivots.forEach((p,i)=>{
      let a=mod(-free.reduce((s,f,j)=>s+rr.matrix[i][f]*v[j],0n),q);
      if(a>q/2n)a-=q;full[p]=a;
    });
    if(!full.every(a=>[-1n,0n,1n].includes(a)))continue;
    const candidate=canonical(full);
    need(member(candidate),"independent RREF reconstruction");
    if(best===null||norm(candidate)<norm(best)||(norm(candidate)===norm(best)&&lex(candidate,best)<0))best=candidate;
  }
  const expected=(3n**BigInt(free.length)-1n)/2n,mitm=3n**BigInt(Math.floor(n/2))+3n**BigInt(n-Math.floor(n/2));
  need(BigInt(count)===expected&&I(row.projective_rref_states_checked)===expected&&I(row.ambient_mitm_states)===mitm&&
       expected<mitm&&best!==null&&same(row.projective_RREF_vector.map(I),best)&&same(best,plant),"independent complete public RREF search");
  need(row.public_lll_recovered_planted_vector===true&&row.projective_rref_recovered_planted_vector===true&&
       row.projective_rref_strictly_fewer_states_than_mitm===true&&row.RREF_constant_space===false&&
       row.RREF_exponential_table_stored===false,"finite recovery and space metadata");
}
function counterfamily(C){
  const H=[[1n,-1n,0n,0n,0n],[0n,0n,1n,-1n,0n],[1n,0n,-1n,0n,-2n]];
  const u=[1n,1n,1n,1n,0n],v=[1n,1n,-1n,-1n,1n];
  need(matrices(parse(C.integer_constraint_rows),H)&&same(C.primitive_unique_shortest_plant.map(I),u)&&
       same(C.independent_next_vector.map(I),v)&&matrices(parse(C.ordinary_integer_kernel_basis),[u,v]),"counterfamily normal form");
  need(norm(u)===4n&&norm(v)===5n&&u.reduce((s,a,i)=>s+a*v[i],0n)===0n&&
       H.every(row=>row.reduce((s,a,i)=>s+a*u[i],0n)===0n&&row.reduce((s,a,i)=>s+a*v[i],0n)===0n),"counterfamily exact kernel witnesses");
  need(C.maximum_constraint_row_squared_norm===6&&C.proof_radius_squared===5&&
       C.prime_threshold_inclusive===7&&C.all_nonzero_modular_wraps_excluded_within_proof_radius===true,"integer no-wrap proof premise");
  need(C.controls.length===4,"counterfamily modulus controls");
  C.controls.forEach(c=>{
    const {q,H:publicH,member}=publicProblem(c.public_problem);
    need(q>=7n&&q*q>30n&&matrices(publicH,H.map(row=>row.map(a=>mod(a,q)))),"counterfamily public kernel/no wrap");
    need(c.lambda1_squared===4&&c.lambda2_squared===5&&I(c.determinant)===q**3n&&
         equalR(rat(c.determinant_normalized_plant_gap_fifth_power),R(q**3n,32n))&&
         equalR(rat(c.successive_minimum_gap_squared),R(5n,4n)),"growing determinant fixed true gap");
    need(member(c.lll_returned_vector.map(I))&&same(c.lll_returned_vector.map(I),u),"finite counterfamily LLL vector");
  });
  need(C.determinant_growth_proves_successive_gap_growth===false&&
       C.finite_LLL_recovery_proves_monotone_success_probability===false,"counterfamily claim scope");
}
function verify(report){
  need(report.schema_version==="2.0.0"&&report.classical_attack_threshold_audit.length===6,"corrected source scope");
  report.classical_attack_threshold_audit.forEach(verifyRow);
  counterfamily(report.determinant_growth_counterfamily);
  const p=report.LLL_parameter_arithmetic;
  need(equalR(rat(p.delta_3_4_eta_1_2_alpha),R(2n))&&equalR(rat(p.finite_certificate_alpha),R(10000n,4899n))&&
       equalR(rat(p.finite_certificates_use_delta),R(3n,4n))&&equalR(rat(p.finite_certificates_use_eta),R(51n,100n))&&
       p.library_defaults_substituted_for_verified_reducedness===false,"LLL constant correction");
  need(Object.values(report.unresolved_or_withdrawn_claims).every(x=>x===false)&&
       report.guardrails.accepted_speedup_candidate===false,"unverified claims not promoted");
  need(JSON.stringify(Object.keys(report.verification).sort())===JSON.stringify([
       "finite_LLL_membership_reducedness_and_bounds","finite_free_support_and_sparse_attack_controls","finite_projective_rref_search_controls"].sort())&&
       Object.values(report.verification).every(x=>x===true),"finite-only verification");
  return {status:"ok",instances_verified:6,actual_public_RREF_and_LLL_replayed:true,
          determinant_gap_counterexamples:4,general_LLL_monotonicity_proved:false};
}
module.exports={verify};
if(require.main===module){
  const file=process.argv[2]||path.resolve(__dirname,"../reductions/planted_qary_classical_attack_threshold_bridge.json");
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));
}

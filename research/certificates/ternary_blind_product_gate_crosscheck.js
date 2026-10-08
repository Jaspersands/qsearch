"use strict";
// Exact Q(omega) PSD certificates and native character Gram, independent of SymPy.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_blind_product_gate.json"),"utf8"));
function check(x,m){if(!x)throw Error(m);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a;}
function F(a,b=1n){check(b!==0n,"denominator");if(b<0n)[a,b]=[-a,-b];const g=gcd(a,b);return[a/g,b/g];}
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b)),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]),eq=(a,b)=>a[0]*b[1]===b[0]*a[1],le=(a,b)=>a[0]*b[1]<=b[0]*a[1],abs=a=>a[0]<0n?neg(a):a;
function Q(x){check(typeof x==="string","rational string");const t=x.split("/");check(t.length<=2,"syntax");const v=F(BigInt(t[0]),t.length===2?BigInt(t[1]):1n);check(x===(v[1]===1n?String(v[0]):v[0]+"/"+v[1]),"canonical rational");return v;}
function pow(x,n){let v=F(1n);for(let j=0;j<n;j++)v=mul(v,x);return v;}
const Z=()=>[F(0n),F(0n)],C=x=>[x,F(0n)],ca=(x,y)=>[add(x[0],y[0]),add(x[1],y[1])],cn=x=>[neg(x[0]),neg(x[1])],cs=(x,y)=>ca(x,cn(y)),cm=(x,y)=>[sub(mul(x[0],y[0]),mul(x[1],y[1])),sub(add(mul(x[0],y[1]),mul(x[1],y[0])),mul(x[1],y[1]))],cc=x=>[sub(x[0],x[1]),neg(x[1])],ce=(x,y)=>eq(x[0],y[0])&&eq(x[1],y[1]),scale=(x,a)=>[mul(x[0],a),mul(x[1],a)];
function real(x){check(eq(x[1],F(0n)),"real Qomega scalar");return x[0];}
const mod=(x,q)=>(x%q+q)%q;
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_BLIND_PRODUCT_GATE.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="LABEL_INDEPENDENT_PRODUCT_POVM_GATE_REVIEW_PENDING","review and derivation hash");
for(const k of ["quantum_speedup_proved","candidate_record_accepted","novelty_claim","all_LOCC_or_general_quantum_lower_bound"])check(report[k]===false,"no promotion: "+k);
const schedule=[8,16,32,64];check(report.universal_scaling_gates.length===4,"scaling schedule");
report.universal_scaling_gates.forEach((c,i)=>{const r=schedule[i],M=r-2,G=3n**BigInt(r),d=sub(pow(F(5n,3n),M),F(1n)),zero=mul(F(1n,G),sub(F(1n),F(1n,3n**BigInt(M)))),squared=div(d,F(G)),eps=F(1n,10n),gap=sub(eps,zero);
  check(c.dimension===1&&c.digits===r&&c.original_independent_qutrits===M,"native population geometry");
  for(const[k,v]of[["nonzero_Gram_operator_norm_upper",mul(F(2n),d)],["nonzero_contribution_advantage_upper_squared",squared],["zero_secret_advantage_upper",zero],["requested_advantage",eps]])check(eq(Q(c[k]),v),"exact universal gate: "+k);
  check(c.necessary_copy_gate_passed===(le(eps,zero)||le(mul(gap,gap),squared)),"necessary gate");
  for(const k of["different_POVM_per_original_copy_covered","shared_independent_public_measurement_randomness_covered","opposite_secret_correlations_kept"])check(c[k]===true,"covered product condition: "+k);
  for(const k of["label_dependent_quantum_measurements_covered","outcome_adaptive_quantum_measurements_covered","collective_quantum_measurements_covered","chosen_labels_or_retained_sieve_law_covered","speedup_claim_allowed"])check(c[k]===false,"restricted scope: "+k);
});
function determinant(E,indices){if(indices.length===1)return E[indices[0]][indices[0]];if(indices.length===2){const[i,j]=indices;return cs(cm(E[i][i],E[j][j]),cm(E[i][j],E[j][i]));}let v=Z();for(const[p,sign]of[[[0,1,2],1],[[0,2,1],-1],[[1,0,2],-1],[[1,2,0],1],[[2,0,1],1],[[2,1,0],-1]])v=ca(v,scale(cm(cm(E[0][p[0]],E[1][p[1]]),E[2][p[2]]),F(BigInt(sign))));return v;}
const names=["computational","inverse_F3","real_pair_basis","real_dense_basis","public_half_F3_half_real_dense"];
check(report.certified_POVM_controls.length===5,"all prespecified basis controls");let effects=0,principalMinors=0,GramPairs=0;
report.certified_POVM_controls.forEach((c,index)=>{check(c.name===names[index],"basis schedule");const E=c.effects_Qomega.map(e=>e.map(row=>row.map(x=>[Q(x[0]),Q(x[1])]))),total=Array.from({length:3},()=>Array.from({length:3},Z));let d=F(0n),eta=Z(),d0=Z();const normalized=[];
  for(const e of E){check(e.length===3&&e.every(row=>row.length===3),"qutrit effect");for(let i=0;i<3;i++)for(let j=0;j<3;j++){check(ce(e[i][j],cc(e[j][i])),"Hermitian exact effect");total[i][j]=ca(total[i][j],e[i][j]);}
    for(const subset of[[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]){check(le(F(0n),real(determinant(e,subset))),"all principal minors PSD");principalMinors++;}
    const tr=real(e.reduce((s,row,i)=>ca(s,row[i]),Z()));check(tr[0]>0n,"positive trace, no null effects");const divisor=div(F(1n),mul(F(3n),tr));let sum=Z();
    for(let i=0;i<3;i++)for(let j=0;j<3;j++){sum=ca(sum,e[i][j]);if(i!==j){d=add(d,mul(real(cm(e[i][j],cc(e[i][j]))),divisor));eta=ca(eta,scale(cm(e[i][j],e[i][j]),divisor));}}
    d0=ca(d0,scale(cm(cs(sum,C(tr)),cs(sum,C(tr))),divisor));normalized.push({e,trace:tr});effects++;
  }
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)check(ce(total[i][j],C(F(i===j?1n:0n))),"exact complete POVM");eta=real(eta);d0=real(d0);check(le(F(0n),d)&&le(d,F(2n,3n))&&le(abs(eta),d)&&le(F(0n),d0)&&le(d0,F(2n)),"universal positive POVM scalar bounds");
  for(const inv of[c.invariants,c.physical_control.exact_invariants]){check(eq(Q(inv.nonzero_diagonal),d)&&eq(Q(inv.opposite_nonzero_secret_Gram),eta)&&eq(Q(inv.zero_diagonal),d0)&&inv.exact_PSD_and_completeness_certified===true,"exact serialized invariants");}
  // Orthogonality replay directly from matrix coefficients, including zero and s=-t.
  const phases=[[0,0],[1,0],[0,1]];
  for(let s=0;s<9;s++)for(let t=0;t<9;t++){let value=Z();for(const{e,trace}of normalized){let pair=Z();for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(i!==j)for(let k=0;k<3;k++)for(let l=0;l<3;l++)if(k!==l&&[0,1].every(a=>mod((phases[i][a]-phases[j][a])*s+(phases[k][a]-phases[l][a])*t,9)===0))pair=ca(pair,cm(e[j][i],e[l][k]));value=ca(value,scale(pair,div(F(1n),mul(F(3n),trace))));}
    const expected=s===0&&t===0?d0:s===t?d:s!==0&&mod(s+t,9)===0?eta:F(0n);check(eq(real(value),expected),"complete native secret-pair Gram from actual effects");GramPairs++;
  }
  const g=c.eight_copy_scalar_gate,delta=sub(pow(add(F(1n),d),8),F(1n)),kappa=sub(pow(add(F(1n),eta),8),F(1n)),operator=add(delta,abs(kappa));
  for(const[k,v]of[["nonzero_product_diagonal",delta],["opposite_product_entry",kappa],["nonzero_Gram_operator_norm",operator],["nonzero_contribution_advantage_upper_squared",div(operator,F(2n*3n**8n))]])check(eq(Q(g[k]),v),"exact product Gram norm: "+k);
  check(g.invariant_inputs_are_assumptions_unless_POVM_certified===true,"scalar assumptions not a hidden proof");
  const p=c.physical_control;check(p.modulus===9&&p.complete_native_label_pairs===81&&p.complete_secret_pairs===81&&p.outcomes===E.length&&p.nonprimitive_and_zero_secrets_kept===true,"full bounded physical census");check(Number.isFinite(p.actual_Born_Gram_residual)&&p.actual_Born_Gram_residual>=0&&p.actual_Born_Gram_residual<3e-11,"actual physical Gram replay residual");
});
console.log(JSON.stringify({status:"independent_blind_product_POVM_certificates_passed",exactEffects:effects,PSDPrincipalMinors:principalMinors,completeGramPairs:GramPairs,scalingGates:4,physicalResidualsCheckedNotBornArraysReexecuted:true,quantumSpeedupProved:false,generalLOCCNoGo:false}));

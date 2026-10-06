"use strict";
// Independent nine Born-amplitude cross terms, not the seven-term Python DP.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../classical_baselines/ternary_posterior_dual.json"),"utf8"));
function check(x,m){if(!x)throw Error(m);}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
const mod=(x,q)=>((x%q)+q)%q;
const dot=(a,b)=>a.reduce((s,x,j)=>s+BigInt(x)*BigInt(b[j]),0n);
function add(poly,e,c,q){
  e=mod(e,q);const terms=e<2n*q/3n?[[e,c]]:[[e-2n*q/3n,-c],[e-q/3n,-c]];
  for(const[t,v]of terms){const key=t.toString(),value=(poly.get(key)||0n)+v;if(value)poly.set(key,value);else poly.delete(key);}
}
function encode(poly){return [...poly].sort((a,b)=>BigInt(a[0])<BigInt(b[0])?-1:1).map(([e,c])=>[e,c.toString()]);}
const embedding=[[0n,0n],[1n,0n],[0n,1n]],pairs=[];
for(const a of embedding)for(const b of embedding)pairs.push([a[0]-b[0],a[1]-b[1]]);
let halfLeafChecks=0,posteriors=0;
function half(records,n,q){
  const buckets=new Map();
  function recurse(i,f,e){
    if(i===records.length){
      const key=f.join(",");if(!buckets.has(key))buckets.set(key,new Map());add(buckets.get(key),e,1n,q);halfLeafChecks++;return;
    }
    const r=records[i];
    for(const[u,v]of pairs){const df=r.first.map((a,j)=>-(u*BigInt(a)+v*BigInt(r.second[j])));
      recurse(i+1,f.map((a,j)=>mod(a+df[j],q)),mod(e+u*BigInt(r.outcome[0])+v*BigInt(r.outcome[1]),q));}
  }
  recurse(0,Array(n).fill(0n),0n);return buckets;
}
function replay(baseline){
  const q=BigInt(baseline.modulus),n=baseline.dimension,M=baseline.records.length,target=baseline.target_coordinate,split=Math.floor(M/2);
  const L=half(baseline.records.slice(0,split),n,q),R=half(baseline.records.slice(split),n,q),out=[];
  for(let k=0;k<3;k++){
    const C=new Map(),F=Array.from({length:n},(_,j)=>j===target?BigInt(k)*q/3n:0n);
    for(const[key,A]of L){const f=key.split(",").map(BigInt),g=F.map((a,j)=>mod(a-f[j],q)).join(","),B=R.get(g);if(!B)continue;
      for(const[e,a]of A)for(const[h,b]of B)add(C,BigInt(e)+BigInt(h),a*b,q);
    }out.push(encode(C));
  }
  same(out,baseline.coefficient_numerators,"independent exact Born-term posterior coefficients");
  check(!baseline.cost_ledger.secret_assignments_enumerated&&!baseline.polynomial_native_weak_learner_implemented,"baseline scope/cost gates");posteriors++;
}
function numericPosterior(b){
  const q=Number(b.modulus),n=b.dimension,G=q**n,M=b.records.length;
  check(G<=6561,"secret enumeration certificate is bounded, not the baseline");
  const masses=[0,0,0];
  for(let index=0;index<G;index++){
    let rest=index;const s=[];for(let j=0;j<n;j++){s.push(rest%q);rest=Math.floor(rest/q);}
    let likelihood=1;
    for(const r of b.records){
      const angles=[Number(mod(BigInt(r.outcome[0])-dot(r.first,s),BigInt(q))),Number(mod(BigInt(r.outcome[1])-dot(r.second,s),BigInt(q)))].map(x=>2*Math.PI*x/q);
      likelihood*=((1+Math.cos(angles[0])+Math.cos(angles[1]))**2+(Math.sin(angles[0])+Math.sin(angles[1]))**2)/3;
    }masses[s[b.target_coordinate]%3]+=likelihood;
  }
  const total=masses.reduce((a,b)=>a+b,0),p=masses.map(x=>x/total);
  check(p.every((x,j)=>Math.abs(x-b.posterior.posterior_probabilities[j])<1e-10),"all-secret bounded physical posterior comparator");
  return G;
}
let boundedSecretChecks=0;
for(const c of report.native_IID_live_controls){replay(c.baseline);if(BigInt(c.baseline.modulus)**BigInt(c.baseline.dimension)<=6561n)boundedSecretChecks+=numericPosterior(c.baseline);}
replay(report.deterministic_legal_phase_cancellation_countercontrol);
const cancellation=report.deterministic_legal_phase_cancellation_countercontrol;
same(cancellation.coefficient_numerators.slice(1),[[],[]],"nonzero formal relations cancel exactly");
check(cancellation.posterior.exactly_uniform_least_trit,"relation-count false-positive guard");
// Actual q3 positive control: independently evaluate all27 secrets exactly.
const field=report.actual_field_positive_countercontrol.paired_posterior_control,n=field.dimension,G=3**n,M=field.records.length,coeffs=[new Map(),new Map(),new Map()];
let unique=null,supported=0;
for(let index=0;index<G;index++){
  let rest=index;const s=[];for(let j=0;j<n;j++){s.push(rest%3);rest=Math.floor(rest/3);}
  let numerator=3n**BigInt(M);
  for(const r of field.records){
    const a=Number(mod(BigInt(r.outcome[0])-dot(r.first,s),3n)),b=Number(mod(BigInt(r.outcome[1])-dot(r.second,s),3n));
    const density=(a===0&&b===0)?3n:((a===1&&b===2)||(a===2&&b===1))?0n:1n;
    numerator*=density;
  }
  if(numerator){unique=s;supported++;}
  for(let k=0;k<3;k++)add(coeffs[k],BigInt(-k*s[0]),numerator,3n);
}
check(supported===1,"field data unique exact support");
same(unique,report.actual_field_positive_countercontrol.independent_polynomial_field_decoder.secret,"field exact support/streaming decoder");
for(const C of coeffs)for(const[e,c]of C){check(c%BigInt(G)===0n,"exact Fourier averaging divisor");C.set(e,c/BigInt(G));}
same(coeffs.map(encode),field.coefficient_numerators,"independent exact field posterior coefficients");
for(const c of report.raw_record_least_trit_gates){
  const parts=c.mean_least_trit_advantage_squared_upper.split("/").map(BigInt),a=parts[0],b=parts[1]||1n;
  check(a*(2n*3n**BigInt(c.dimension*c.digits+c.classical_records))===b*(5n**BigInt(c.classical_records)-3n**BigInt(c.classical_records)),"exact raw-record trit mixture moment");
  check(c.necessary_copy_gate_passed===(100n*a>=b),"classical one-tenth advantage copy gate");
}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function rational(a,b){const g=gcd(a,b);return[a/g,b/g];}
function plus(a,b){return rational(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function binomial(N,k){let x=1n;for(let j=1;j<=k;j++)x=x*BigInt(N-j+1)/BigInt(j);return x;}
for(const c of report.low_record_degree_gates){
  let V=[0n,1n];for(let j=1;j<=c.record_degree;j++)V=plus(V,[binomial(c.samples,j)*2n**BigInt(j),3n**BigInt(j)]);
  const p=c.truncated_centered_likelihood_norm_squared.split("/").map(BigInt);
  check(V[0]*(p[1]||1n)===V[1]*p[0],"ANOVA truncated exact likelihood norm");
}
for(const c of report.full_label_sparse_coherence_gates){
  let words=0n;for(let j=1;j<=c.coherence_radius;j++)words+=binomial(c.native_copies,j)*6n**BigInt(j);
  check(words===BigInt(c.oriented_root_difference_words),"full-label sparse-relation union census");
  check(c.necessary_sparse_coherence_gate_passed===(20n*words>=3n*3n**BigInt(c.dimension*c.digits)),"sparse-coherence one-tenth advantage gate");
  check(!c.local_gates_sparse_generators_or_shallow_circuits_excluded,"do not equate final support with gate locality");
}
check(!report.accepted_candidate&&!report.polynomial_higher_root_native_weak_learner&&!report.general_classical_hardness_or_quantum_advantage_claim,"global claim gates");
process.stdout.write(JSON.stringify({status:"independent_replay_passed",exact_nine_term_posteriors:posteriors,
  half_Born_terms:halfLeafChecks,bounded_secret_calibration_checks:boundedSecretChecks,exact_field_secrets:G,
  polynomial_higher_root_weak_learner:false})+"\n");

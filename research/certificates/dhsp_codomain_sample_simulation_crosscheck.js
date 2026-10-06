// Independent rational enumeration and full adaptive-memory source checks.
"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert/strict");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/dhsp_codomain_sample_simulation.json"),"utf8"));
function gcd(a,b) {a=a<0n?-a:a;b=b<0n?-b:b;while(b) [a,b]=[b,a%b];return a;}
class Q {
  constructor(n,d=1n) {n=BigInt(n);d=BigInt(d);assert.notEqual(d,0n);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
  add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
  mul(b){return new Q(this.n*b.n,this.d*b.d);}
  div(b){return new Q(this.n*b.d,this.d*b.n);}
  abs(){return new Q(this.n<0n?-this.n:this.n,this.d);}
  pow(n){return new Q(this.n**BigInt(n),this.d**BigInt(n));}
  eq(b){return this.n===b.n&&this.d===b.d;}
  le(b){return this.n*b.d<=b.n*this.d;}
  number(){return Number(this.n)/Number(this.d);}
}
const q=n=>new Q(n),read=x=>new Q(x.numerator,x.denominator),zero=q(0),one=q(1);
const eq=(a,b)=>assert(a.eq(b),`${a.n}/${a.d} != ${b.n}/${b.d}`);
const close=(a,b)=>assert(Math.abs(a-b)<1e-10,`${a} != ${b}`);
const matrix=n=>Array.from({length:n},()=>Array.from({length:n},()=>zero));
function tuples(N,m) {let out=[[]];for(let t=0;t<m;t++)out=out.flatMap(row=>Array.from({length:N},(_,y)=>[...row,y]));return out;}
function sourceChoi(p,Ws) {
  const vectors=Ws.map(W=>W.flat()),s=vectors[0].length,H=matrix(s),F=matrix(s);
  const mean=Array.from({length:s},(_,i)=>p.reduce((a,w,y)=>a.add(w.mul(vectors[y][i])),zero));
  for(let i=0;i<s;i++)for(let j=0;j<s;j++) {
    H[i][j]=mean[i].mul(mean[j]);
    F[i][j]=p.reduce((a,w,y)=>a.add(w.mul(vectors[y][i]).mul(vectors[y][j])),zero).sub(H[i][j]);
  }
  return [H,F];
}
let exactEntries=0,empiricalTuples=0;
for(const r of report.empirical_channel_controls) {
  const p=r.source_probabilities.map(read),Ws=r.operators.map(W=>W.map(row=>row.map(read))),m=r.samples_per_probe,d=r.memory_dimension,s=d*d;
  const [H,F]=sourceChoi(p,Ws),EH=matrix(s),EF=matrix(s);
  for(const indices of tuples(p.length,m)) {
    const w=indices.reduce((a,y)=>a.mul(p[y]),one),counts=p.map((_,y)=>new Q(indices.filter(i=>i===y).length,m));
    const [h,f]=sourceChoi(counts,Ws);empiricalTuples++;
    for(let i=0;i<s;i++)for(let j=0;j<s;j++) {EH[i][j]=EH[i][j].add(w.mul(h[i][j]));EF[i][j]=EF[i][j].add(w.mul(f[i][j]));}
  }
  for(let i=0;i<s;i++)for(let j=0;j<s;j++) {
    eq(H[i][j],read(r.source_choi_H[i][j]));eq(F[i][j],read(r.source_choi_F[i][j]));
    eq(EH[i][j],read(r.empirical_average_choi_H[i][j]));eq(EF[i][j],read(r.empirical_average_choi_F[i][j]));
    eq(EH[i][j].sub(H[i][j]),F[i][j].div(q(m)));eq(EF[i][j].sub(F[i][j]),zero.sub(F[i][j]).div(q(m)));exactEntries+=6;
  }
  const trace=F.reduce((a,row,i)=>a.add(row[i]),zero);
  eq(trace.div(q(d*m)),read(r.normalized_choi_input_trace_distance));
  eq(new Q(1,m),read(r.dimension_independent_half_diamond_upper));
  if(r.name==="identity_Z_diamond_not_choi") {eq(F[3][3],one);eq(F[0][0],zero);close(r.maximum_input_trace_distance_numeric_only,1/m);eq(trace.div(q(d*m)),new Q(1,2*m));}
  assert(!r.source_mean_operator_given_to_simulator&&r.entangled_reference_allowed);
}
function choose(n,k) {if(k<0||k>n)return 0n;let r=1n;for(let i=1;i<=k;i++)r=r*BigInt(n-i+1)/BigInt(i);return r;}
function policy(name,prefix) {
  if(name==="zero")return 0;
  if(name==="alternating")return prefix.length%2;
  if(name==="last_label_parity")return prefix.length?prefix.at(-1)%2:0;
  assert.equal(name,"collision_feedback");return Number(new Set(prefix).size<prefix.length);
}
let transcriptEntries=0;
for(const r of report.adaptive_shared_subset_controls) {
  const N=r.rotation_order,Qcount=r.label_only_queries,totals=[zero,zero];let TV=zero;
  for(const record of r.records) {
    const labels=record.labels,weights=[];
    for(let h=0;h<2;h++) {
      const good=labels.filter((y,t)=>policy(r.policy,labels.slice(0,t))===h),c=new Set(good).size;
      const w=new Q(choose(N-c,N/2-c),choose(N,N/2)).mul(new Q(2,N).pow(good.length)).mul(new Q(1,N).pow(labels.length-good.length));
      eq(w,read(record.probabilities[h]));totals[h]=totals[h].add(w);weights.push(w);transcriptEntries++;
    }
    TV=TV.add(weights[0].sub(weights[1]).abs().div(q(2)));
  }
  eq(totals[0],one);eq(totals[1],one);eq(TV,read(r.exact_total_variation));assert(TV.le(new Q(Qcount*(Qcount-1),2*N)));
  assert(r.shared_subset&&!r.domain_indices_available_to_decoder);
}
for(const r of report.exact_posterior_controls) {
  const N=r.rotation_order,M=N/2,c=r.forced.length;
  let TV=zero,total=zero;
  for(let y=0;y<N;y++) {
    const p=r.forced.includes(y)?new Q(1,M):new Q(M-c,M*(N-c));
    eq(p,read(r.predictive_law[y]));TV=TV.add(p.sub(new Q(1,N)).abs().div(q(2)));total=total.add(p);
  }
  eq(total,one);eq(TV,new Q(c,N));eq(TV,read(r.distance_to_uniform));
}
for(const r of [...report.dimension_free_scaling_ledgers,report.precision_floor_counterledger,report.polynomial_accuracy_simulator_ledger]) {
  const N=1n<<BigInt(r.modulus_bits),T=BigInt(r.instrument_calls),m=BigInt(r.samples_per_empirical_call),Qcount=T*m;
  assert.equal(N.toString(),r.rotation_order);assert.equal(Qcount.toString(),r.total_classical_label_samples);
  const simulation=new Q(T,m),raw=new Q(Qcount*(Qcount-1n),2n*N),data=raw.le(one)?raw:one;
  const combined=simulation.mul(q(2)).add(data),ideal=combined.le(one)?combined:one;
  const error=read(r.total_composed_parity_comparison_trace_error_budget),physical=ideal.add(error).le(one)?ideal.add(error):one;
  eq(simulation,read(r.simulation_error_per_hypothesis));eq(data,read(r.simulated_label_transcript_distance_upper));
  eq(ideal,read(r.ideal_original_instrument_parity_distance_upper));eq(physical,read(r.original_instrument_distance_upper_with_error));
  eq(one.add(physical).div(q(2)),read(r.binary_parity_success_upper_with_error));
  assert(r.same_fixed_nuisance_for_every_call&&r.initial_memory_secret_independent_required_for_parity_gate);
  assert(!r.other_oracle_queries_retained_domain_or_coherent_subgroup_choices_covered&&!r.conditional_herald_accuracy_certified);
}
const cadd=(a,b)=>[a[0]+b[0],a[1]+b[1]],cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],cconj=a=>[a[0],-a[1]];
let physicalEntries=0;
for(const r of report.physical_empirical_controls) {
  const ids=r.sample_indices,m=ids.length,d=r.memory_dimension,s=d*d;
  const vectors=ids.map(y=>r.operators_real[y].flat().map((re,i)=>[re,r.operators_imag[y].flat()[i]]));
  const mean=Array.from({length:s},(_,i)=>vectors.reduce((a,v)=>cadd(a,[v[i][0]/m,v[i][1]/m]),[0,0]));
  for(let i=0;i<s;i++)for(let j=0;j<s;j++) {
    const H=cmul(mean[i],cconj(mean[j])).map(x=>x/d);
    const rho=vectors.reduce((a,v)=>cadd(a,cmul(v[i],cconj(v[j])).map(x=>x/(m*d))),[0,0]);
    close(H[0],r.H_real[i][j]);close(H[1],r.H_imag[i][j]);
    close(rho[0]-H[0],r.F_real[i][j]);close(rho[1]-H[1],r.F_imag[i][j]);physicalEntries+=4;
  }
}
const transpose=A=>A[0].map((_,i)=>A.map(row=>row[i]));
function multiply(A,B) {return A.map(row=>B[0].map((_,j)=>row.reduce((a,x,k)=>a.add(x.mul(B[k][j])),zero)));}
const sumMatrix=(A,B)=>A.map((row,i)=>row.map((x,j)=>x.add(B[i][j])));
const scaleMatrix=(A,t)=>A.map(row=>row.map(x=>x.mul(t)));
function conjugate(U,rho) {return multiply(multiply(U,rho),transpose(U));}
function kron(A,B) {const n=A.length*B.length,C=matrix(n);for(let i=0;i<A.length;i++)for(let j=0;j<A.length;j++)for(let k=0;k<B.length;k++)for(let l=0;l<B.length;l++)C[i*B.length+k][j*B.length+l]=A[i][j].mul(B[k][l]);return C;}
const I=[[one,zero],[zero,one]],Z=[[one,zero],[zero,q(-1)]],X=[[zero,one],[one,zero]],R=[[new Q(3,5),new Q(-4,5)],[new Q(4,5),new Q(3,5)]];
const Ws=[I,Z,X,R].map(W=>kron(W,I)),interleave=kron(R,I),subsets=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const initial=matrix(4);for(const i of [0,3])for(const j of [0,3])initial[i][j]=new Q(1,2);
function memoryCall(rho,S,epsilon,h,m) {
  const p=Array.from({length:4},(_,y)=>epsilon===h?(S.includes(y)?new Q(1,2):zero):new Q(1,4));
  let mean=matrix(4),E=matrix(4);
  for(let y=0;y<4;y++){mean=sumMatrix(mean,scaleMatrix(Ws[y],p[y]));E=sumMatrix(E,scaleMatrix(conjugate(Ws[y],rho),p[y]));}
  const H=conjugate(mean,rho),F=sumMatrix(E,scaleMatrix(H,q(-1)));
  return m===null?[H,F]:[sumMatrix(H,scaleMatrix(F,new Q(1,m))),scaleMatrix(F,new Q(m-1,m))];
}
function execute(h,m,resample) {
  const out=matrix(16);
  for(const S of subsets) {
    const first=memoryCall(initial,S,0,h,m);
    for(let a=0;a<2;a++) {
      const rho=conjugate(interleave,first[a]),seconds=resample?subsets:[S];
      for(const nextS of seconds) {
        const next=memoryCall(rho,nextS,a,h,m);
        for(let b=0;b<2;b++)for(let i=0;i<4;i++)for(let j=0;j<4;j++) {
          const off=4*(2*a+b);out[off+i][off+j]=out[off+i][off+j].add(next[b][i][j].div(q(6*seconds.length)));
        }
      }
    }
  }
  return out;
}
let adaptiveEntries=0;
for(const r of report.adaptive_entangled_memory_controls) {
  for(let h=0;h<2;h++)for(const [key,m,fresh] of [["source_states_by_parity",null,false],["simulated_states_by_parity",r.samples_per_call,false],["fresh_resampled_states_by_parity",null,true]]) {
    const A=execute(h,m,fresh);
    let trace=zero;
    for(let i=0;i<16;i++){trace=trace.add(A[i][i]);for(let j=0;j<16;j++){close(A[i][j].number(),r[key][h][i][j]);adaptiveEntries++;}}
    eq(trace,one);
  }
}
assert(Object.values(report.claim_gate).every(x=>x===false));
const rare=report.postselection_counterledger,M=1n<<BigInt(rare.modulus_bits-1),mRare=BigInt(rare.empirical_samples);
const herald=new Q(1n,M),empiricalHerald=herald.add(one.sub(herald).div(q(mRare)));
eq(herald,read(rare.true_full_label_herald));eq(empiricalHerald,read(rare.empirical_average_full_label_herald));
eq(one.sub(herald).div(q(mRare)),read(rare.unconditional_complete_output_trace_distance));
eq(herald.div(empiricalHerald),read(rare.empirical_heralded_pure_target_overlap));
assert(!rare.efficient_conditional_pure_image_preparation_claim_allowed);
eq(read(report.chosen_query_scope_countercontrol.classical_success),one);
console.log(JSON.stringify({empirical_sample_tuples:empiricalTuples,exact_channel_entries:exactEntries,adaptive_label_probabilities:transcriptEntries,complex_physical_entries:physicalEntries,exact_adaptive_memory_entries:adaptiveEntries,scaling_ledgers:6,general_dhsp_claim:false}));

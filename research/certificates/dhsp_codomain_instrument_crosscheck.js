// Independent exact arithmetic and literal physical-state checks. No registry writes.
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert/strict");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../classical_baselines/dhsp_codomain_instrument.json"), "utf8"));
function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b) [a,b]=[b,a%b]; return a; }
class Q {
  constructor(n,d=1n) { n=BigInt(n); d=BigInt(d); assert.notEqual(d,0n); if(d<0n) {n=-n;d=-d;} const g=gcd(n,d); this.n=n/g;this.d=d/g; }
  add(b) {return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  sub(b) {return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
  mul(b) {return new Q(this.n*b.n,this.d*b.d);}
  div(b) {return new Q(this.n*b.d,this.d*b.n);}
  abs() {return new Q(this.n<0n?-this.n:this.n,this.d);}
  pow(n) {return new Q(this.n**BigInt(n),this.d**BigInt(n));}
  eq(b) {return this.n===b.n&&this.d===b.d;}
  le(b) {return this.n*b.d<=b.n*this.d;}
  number() {return Number(this.n)/Number(this.d);}
}
const q=n=>new Q(n), zero=q(0), one=q(1), half=new Q(1,2);
const read=x=>new Q(x.numerator,x.denominator);
const eq=(a,b)=>assert(a.eq(b), `${a.n}/${a.d} != ${b.n}/${b.d}`);
const close=(a,b)=>assert(Math.abs(a-b)<1e-10, `${a} != ${b}`);
const matrix=(n)=>Array.from({length:n},()=>Array.from({length:n},()=>zero));
function choose(n,k) { let r=1n;for(let i=1;i<=k;i++) r=r*BigInt(n-i+1)/BigInt(i);return r; }
function sigma(d) {
  const A=matrix(4); A[0][0]=half; A[0][1]=A[1][0]=d;
  A[1][1]=q(2).mul(d.pow(2)); A[3][3]=half.sub(A[1][1]); return A;
}
function kron(A,B) {
  const C=matrix(A.length*B.length);
  for(let i=0;i<A.length;i++) for(let j=0;j<A.length;j++)
    for(let k=0;k<B.length;k++) for(let l=0;l<B.length;l++) C[i*B.length+k][j*B.length+l]=A[i][j].mul(B[k][l]);
  return C;
}
let physicalEntries=0, exactEntries=0;
for(const r of report.physical_controls) {
  const N=r.rotation_order,K=r.hash_bins,D=N,L=N;
  const values=[];
  for(let b=0;b<2;b++) for(let j=0;j<N/2;j++) values.push(r.output_permutation[((2*j+r.subgroup_parity*b-b*r.shift)%N+N)%N]);
  const tensor=Array(D*L*K).fill(0);
  const index=(a,v,w)=>(a*L+v)*K+w;
  for(let a=0;a<D;a++) tensor[index(a,0,0)]=1/Math.sqrt(D);
  const query=(state)=> {
    const out=Array(state.length).fill(0);
    for(let a=0;a<D;a++) for(let v=0;v<L;v++) for(let w=0;w<K;w++) out[index(a,v^values[a],w)]+=state[index(a,v,w)];
    return out;
  };
  const queried=query(tensor), hashed=Array(tensor.length).fill(0);
  for(let a=0;a<D;a++) for(let v=0;v<L;v++) for(let w=0;w<K;w++) hashed[index(a,v,(w+v%K)%K)]+=queried[index(a,v,w)];
  const erased=query(hashed), counts=Array(K).fill(0);
  for(const v of values) counts[v%K]++;
  const p=counts.map(c=>new Q(c,D));
  p.forEach((x,i)=>eq(x,read(r.histogram[i])));
  const amp=Array(K).fill(0), H=Array.from({length:K},()=>Array(K).fill(0)), F=Array.from({length:K},()=>Array(K).fill(0));
  for(let w=0;w<K;w++) for(let a=0;a<D;a++) amp[w]+=erased[index(a,0,w)]/Math.sqrt(D);
  for(let w=0;w<K;w++) for(let z=0;z<K;z++) {
    H[w][z]=amp[w]*amp[z];
    for(let a=0;a<D;a++) F[w][z]+=(erased[index(a,0,w)]-amp[w]/Math.sqrt(D))*(erased[index(a,0,z)]-amp[z]/Math.sqrt(D));
  }
  for(let i=0;i<2*K;i++) for(let j=0;j<2*K;j++) {
    const actual=i<K&&j<K?H[i][j]:(i>=K&&j>=K?F[i-K][j-K]:0);
    close(actual,r.state[i][j]);physicalEntries++;
  }
  for(let w=0;w<K;w++) for(let z=0;z<K;z++) {
    let discarded=0;
    for(let a=0;a<D;a++) for(let v=0;v<L;v++) discarded+=hashed[index(a,v,w)]*hashed[index(a,v,z)];
    close(discarded,w===z?p[w].number():0);
    close(discarded,r.discarded_state[w][z]);physicalEntries++;
  }
  close(H.flat().reduce((a,b)=>a+b,0)/K,1/K);
  assert(r.all_failure_hash_outputs_retained&&!r.failed_domain_register_retained);
}
for(const r of report.shared_nuisance_controls) {
  const N=r.rotation_order, mean=matrix(4), shared=matrix(16);
  let M2=zero,M4=zero,total=zero;
  for(let c=0;c<=N/2;c++) {
    const w=new Q(choose(N/2,c)**2n,choose(N,N/2)),d=new Q(2*c,N).sub(half);
    eq(w,read(r.hypergeometric_law[c].probability));eq(d,read(r.hypergeometric_law[c].deviation));
    const single=sigma(d),pair=kron(single,single);
    M2=M2.add(w.mul(d.pow(2)));M4=M4.add(w.mul(d.pow(4)));total=total.add(w);
    for(let i=0;i<4;i++) for(let j=0;j<4;j++) mean[i][j]=mean[i][j].add(w.mul(single[i][j]));
    for(let i=0;i<16;i++) for(let j=0;j<16;j++) shared[i][j]=shared[i][j].add(w.mul(pair[i][j]));
  }
  eq(total,one);eq(M2,read(r.second_moment));eq(M4,read(r.fourth_moment));
  eq(M2,new Q(1,4*(N-1)));eq(M4,new Q(3*N-8,16*N*(N-1)*(N-3)));
  const wrong=kron(sigma(zero),sigma(zero)),fresh=kron(mean,mean);
  const diff=shared.map((row,i)=>row.map((x,j)=>x.sub(wrong[i][j])));
  let witness=diff[0][0].add(diff[5][5]).sub(diff[0][5]).sub(diff[5][0]).mul(half);
  for(const i of [3,12,15]) witness=witness.add(diff[i][i]);
  eq(witness,q(-5).mul(M2).add(q(6).mul(M4)));
  eq(witness.abs(),read(r.fixed_measurement_absolute_difference));
  eq(q(4).mul(M2),read(r.twice_averaged_one_copy_distance));
  let different=false;
  for(let i=0;i<16;i++) for(let j=0;j<16;j++) {
    eq(shared[i][j],read(r.shared_two_copy_state[i][j]));
    eq(fresh[i][j],read(r.fresh_resampled_two_copy_state[i][j]));
    eq(wrong[i][j],read(r.wrong_two_copy_state[i][j]));
    different ||= !shared[i][j].eq(fresh[i][j]);exactEntries+=3;
  }
  assert(different&&r.shared_is_not_resampled);
  assert.equal(r.naive_averaged_one_copy_hybrid_falsified,!witness.abs().le(q(4).mul(M2)));
  if(N===8) {eq(witness.abs(),new Q(11,70));assert(!new Q(11,70).le(new Q(1,7)));}
}
for(const r of [...report.native_scaling_ledgers,report.precision_floor_counterledger]) {
  const N=1n<<BigInt(r.modulus_bits),K=BigInt(r.hash_bins),T=BigInt(r.instrument_probes),R=BigInt(r.predeclared_balanced_hash_menu_size);
  assert.equal(N.toString(),r.rotation_order);
  const delta=new Q(K-1n,K*(N-1n));eq(delta,read(r.one_copy_averaged_distance));
  let root=0n;while(root*root<K) root++;
  const C=new Q(4n+root,2n);eq(C,read(r.pointwise_distance_coefficient_upper));
  const sq=new Q(T*T*R).mul(C.pow(2)).mul(delta);eq(sq,read(r.shared_oracle_quantum_hybrid_squared_bound));
  const ideal=read(r.ideal_quantum_trace_distance_upper),err=read(r.total_composed_trace_error_budget);
  assert(sq.le(one)?sq.le(ideal.pow(2)):ideal.eq(one));
  const bound=ideal.add(err).le(one)?ideal.add(err):one;
  eq(bound,read(r.quantum_trace_distance_upper_with_error));
  eq(one.add(bound).mul(half),read(r.binary_success_upper_with_error));
  const thin=new Q(T*R).mul(delta).add(err);
  eq(thin.le(one)?thin:one,read(r.three_outcome_classical_transcript_distance_upper));
  assert.equal(r.oracle_queries,2*r.instrument_probes);
  assert(!r.independent_nuisance_resampling_assumed&&!r.other_full_oracle_algorithms_covered);
}
assert(Object.values(report.claim_gate).every(x=>x===false));
function subsets(n,k) {
  const result=[];
  function visit(start,left,S) {if(!left) {result.push(S);return;} for(let i=start;i<=n-left;i++) visit(i+1,left-1,[...S,i]);}
  visit(0,k,[]);return result;
}
for(const r of report.exact_moment_controls) {
  const N=r.rotation_order,K=r.hash_bins,Ss=subsets(N,N/2),cov=matrix(K);
  for(const S of Ss) {
    const dev=Array.from({length:K},(_,i)=>new Q(2*S.filter(y=>y%K===i).length,N).sub(new Q(1,K)));
    for(let i=0;i<K;i++) for(let j=0;j<K;j++) cov[i][j]=cov[i][j].add(dev[i].mul(dev[j]).div(q(Ss.length)));
  }
  for(let i=0;i<K;i++) for(let j=0;j<K;j++) {
    eq(cov[i][j],read(r.covariance[i][j]));
    eq(cov[i][j],new Q(i===j?1:0,K*(N-1)).sub(new Q(1,K*K*(N-1))));
  }
  eq(new Q(K-1,K*(N-1)),read(r.averaged_one_copy_trace_distance));
}
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],sub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],conj=a=>[a[0],-a[1]],norm=a=>a[0]*a[0]+a[1]*a[1];
const scale=(a,t)=>[a[0]*t,a[1]*t];
const empty=(n)=>Array.from({length:n},()=>Array.from({length:n},()=>[0,0]));
function summaries(V,S) {
  const d=V[0].length,mu=Array.from({length:d},()=>[0,0]),rho=empty(d);
  for(const y of S) for(let i=0;i<d;i++) {
    mu[i]=add(mu[i],scale(V[y][i],1/S.length));
    for(let j=0;j<d;j++) rho[i][j]=add(rho[i][j],scale(mul(V[y][i],conj(V[y][j])),1/S.length));
  }
  return {mu,rho};
}
let encoderEntries=0;
for(const r of report.general_encoder_controls) {
  const N=8,d=r.retained_encoder_dimension,V=Array.from({length:N},()=>Array.from({length:d},()=>[0,0]));
  for(let y=0;y<N;y++) {
    if(r.name==="coherent_two_hash_selector") {V[y][y%2]=[1/Math.sqrt(2),0];V[y][2+Math.floor(y/2)%2]=[0,1/Math.sqrt(2)];}
    else if(r.name==="complex_nonorthogonal_encoder") {V[y][0]=[3/5,0];V[y][1]=[[4/5,0],[0,4/5],[-4/5,0],[0,-4/5]][y%4];}
    else {assert.equal(r.name,"full_label_encoder_dimension_countercontrol");V[y][y]=[1,0];}
    for(let i=0;i<d;i++) {close(V[y][i][0],r.encoder_vectors_real[y][i]);close(V[y][i][1],r.encoder_vectors_imag[y][i]);}
  }
  const base=summaries(V,Array.from({length:N},(_,i)=>i)),Ss=subsets(N,N/2),meanH=empty(d),meanF=empty(d);
  let vectorVariance=0,densityVariance=0;
  for(const S of Ss) {
    const a=summaries(V,S);
    for(let i=0;i<d;i++) {
      vectorVariance+=norm(sub(a.mu[i],base.mu[i]))/Ss.length;
      for(let j=0;j<d;j++) {
        densityVariance+=norm(sub(a.rho[i][j],base.rho[i][j]))/Ss.length;
        const H=mul(a.mu[i],conj(a.mu[j]));
        meanH[i][j]=add(meanH[i][j],scale(H,1/Ss.length));
        meanF[i][j]=add(meanF[i][j],scale(sub(a.rho[i][j],H),1/Ss.length));
      }
    }
  }
  close(vectorVariance,(1-base.mu.reduce((a,b)=>a+norm(b),0))/(N-1));
  close(densityVariance,(1-base.rho.flat().reduce((a,b)=>a+norm(b),0))/(N-1));
  close(vectorVariance,r.mean_vector_variance);close(densityVariance,r.mean_density_frobenius_variance);
  close(vectorVariance,r.one_copy_averaged_distance);
  for(let i=0;i<d;i++) for(let j=0;j<d;j++) {
    const H=mul(base.mu[i],conj(base.mu[j])),F=sub(base.rho[i][j],H),C=scale(F,1/(N-1));
    const hdiff=sub(sub(meanH[i][j],H),C),fdiff=add(sub(meanF[i][j],F),C);
    close(norm(hdiff),0);close(norm(fdiff),0);encoderEntries+=2;
  }
}
for(const r of report.general_encoder_scaling_ledgers) {
  const n=BigInt(r.modulus_bits),d=BigInt(r.retained_encoder_hilbert_dimension),T=BigInt(r.probes),R=BigInt(r.predeclared_encoder_menu);
  let root=0n;while(root*root<d) root++;
  const C=new Q(4n+root,2n),sq=new Q(T*T*R,(1n<<n)-1n).mul(C.pow(2)),upper=read(r.shared_oracle_distance_dyadic_upper);
  eq(sq,read(r.shared_oracle_distance_squared_upper));assert(sq.le(one)?sq.le(upper.pow(2)):upper.eq(one));
  assert(!r.polynomial_qubits_implies_polynomial_hilbert_dimension&&!r.coherent_cross_call_or_domain_retaining_oracle_access_covered);
}
console.log(JSON.stringify({physical_controls:report.physical_controls.length,physical_matrix_entries:physicalEntries,exact_two_copy_entries:exactEntries,complex_encoder_entries:encoderEntries,scaling_ledgers:report.native_scaling_ledgers.length+report.general_encoder_scaling_ledgers.length+1,shared_oracle_witness:"11/70 > 1/7",candidate_accepted:false}));

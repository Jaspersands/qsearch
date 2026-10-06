// Independent Fourier-kernel reconstruction and physical four-register execution.
"use strict";
const fs = require("fs"), path = require("path"), assert = require("assert/strict");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../phase_workbench/dhsp_domain_collision_walk.json"), "utf8"));
const close = (a, b) => assert(Math.abs(a-b) < 2e-10, `${a} != ${b}`);
const add = (a,b) => [a[0]+b[0], a[1]+b[1]];
const mul = (a,b) => [a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]];
const scale = (a,b) => [a[0]*b,a[1]*b];
const conjugate = a => [a[0],-a[1]];
const norm = a => a[0]*a[0]+a[1]*a[1];
const expi = a => [Math.cos(a),Math.sin(a)];
const mod = (x,N) => (x%N+N)%N;
const matrix = D => Array.from({length:D}, () => Array.from({length:D}, () => [0,0]));
const identity = D => matrix(D).map((row,i) => row.map((_,j) => [Number(i===j),0]));
const dagger = A => A.map((row,i) => row.map((_,j) => conjugate(A[j][i])));
function mm(A,B) {
  return A.map(row => B[0].map((_,j) => row.reduce((z,a,k) => add(z,mul(a,B[k][j])),[0,0])));
}
const mv = (A,v) => A.map(row => row.reduce((z,a,k) => add(z,mul(a,v[k])),[0,0]));
function popcount(x) { let n=0; while(x) {n+=x&1;x>>>=1;} return n; }
function multiplier(N,family) {
  const n=Math.log2(N);
  return Array.from({length:N},(_,k) => {
    if(family==="local") return Math.cos(2*Math.PI*k/N);
    if(family==="dyadic") return Array.from({length:n},(_,j)=>Math.cos(2*Math.PI*mod(k*2**j,N)/N)).reduce((a,b)=>a+b,0)/n;
    if(family==="chirp") return Math.cos(2*Math.PI*mod(k*k,N)/N);
    assert.equal(family,"chirp_lifted");
    return Math.cos(Math.PI*mod(k*k,2*N)/N);
  });
}
function driver(N,family,tau) {
  const kappa=multiplier(N,family), D=2*N;
  const kernel=Array.from({length:N},(_,r)=>kappa.reduce((z,k,kindex)=>add(z,scale(expi(-tau*k/2+2*Math.PI*kindex*r/N),1/N)),[0,0]));
  const C=matrix(D);
  for(let dest=0;dest<D;dest++) for(let src=0;src<D;src++) {
    const b=Math.floor(dest/N),c=Math.floor(src/N),x=dest%N,y=src%N;
    C[dest][src]=b===c?scale(kernel[mod(x-y,N)],Math.cos(tau/2)):
      mul([0,-Math.sin(tau/2)],kernel[mod(x+y,N)]);
  }
  return C;
}
function oracle(N,s,pi) {return Array.from({length:2*N},(_,g)=>pi[mod(g%N-Math.floor(g/N)*s,N)]);}
function floquet(N,labels,family,tau=.75,potential="parity_hash",gamma=1.2) {
  const C=driver(N,family,tau);
  return C.map(row=>row.map((c,j)=>mul(c,expi(-gamma*(potential==="parity_hash"?(-1)**popcount(labels[j]):Math.cos(2*Math.PI*labels[j]/N))))));
}
function partner(N,s,g) {const b=Math.floor(g/N);return (b^1)*N+mod(g%N+(-1)**b*s,N);}
let matrixEntries=0, probabilityEntries=0, quantumControls=0;
for(const r of report.native_oracle_pilot_controls.filter(row=>row.U_real)) {
  const N=r.rotation_order,D=2*N,Q=r.clock_size,s=r.hidden_shift_calibration;
  const labels=oracle(N,s,r.output_permutation_calibration);
  assert.deepEqual(labels,r.oracle_values);
  const U=floquet(N,labels,r.driver_family,r.driver_duration,r.potential,r.oracle_phase_strength);
  const C=driver(N,r.driver_family,r.driver_duration);
  const I=mm(dagger(U),U);
  for(let i=0;i<D;i++) for(let j=0;j<D;j++) {
    close(U[i][j][0],r.U_real[i][j]);close(U[i][j][1],r.U_imag[i][j]);
    close(I[i][j][0],Number(i===j));close(I[i][j][1],0);
    const p=partner(N,s,i),q=partner(N,s,j);
    close(U[p][j][0],U[i][q][0]);close(U[p][j][1],U[i][q][1]);matrixEntries+=6;
  }
  let W=identity(D),Wfree=identity(D),freeProbability=0;
  const w=Array(D).fill(0),T=Array.from({length:D},()=>Array(D).fill(0));
  for(let t=0;t<Q;t++) {
    const psi=mv(W,Array.from({length:D},()=>[1/Math.sqrt(D),0]));
    for(let g=0;g<D;g++) {
      w[g]+=norm(psi[g])/Q;
      freeProbability+=norm(Wfree[partner(N,s,g)][g])/(Q*D);
      for(let h=0;h<D;h++) T[h][g]+=norm(W[h][g])/Q;
    }
    W=mm(U,W);Wfree=mm(C,Wfree);
  }
  let success=0;
  for(let g=0;g<D;g++) {
    close(w[g],r.initial_position_weights[g]);success+=w[g]*T[partner(N,s,g)][g];
    for(let h=0;h<D;h++) {close(T[h][g],r.average_transition[h][g]);probabilityEntries++;}
  }
  close(success,r.actual_verified_two_register_success);
  close(w.reduce((p,x)=>p+x*x,0),r.two_independent_preparations_collision_baseline);
  close(freeProbability,r.phase_free_known_driver_partner_baseline);quantumControls++;
}

// Flat state transforms use explicit register indices, independent of NumPy einsums.
function execution(N,Q,U,independent=false) {
  const D=2*N,dims=[Q,Q,D,D],strides=[Q*D*D,D*D,D,1],size=Q*Q*D*D;
  const decode=index=>dims.map((dim,a)=>Math.floor(index/strides[a])%dim);
  const encode=ids=>ids.reduce((index,x,a)=>index+x*strides[a],0);
  const H=dim=>Array.from({length:dim},(_,i)=>Array.from({length:dim},(_,j)=>[(-1)**popcount(i&j)/Math.sqrt(dim),0]));
  const powers=[identity(D)];for(let t=1;t<Q;t++)powers.push(mm(U,powers.at(-1)));
  function transform(state,axis,getMatrix) {
    return Array.from({length:size},(_,index)=> {
      const ids=decode(index),row=ids[axis],A=getMatrix(ids);
      return A[row].reduce((z,a,col)=> {const src=ids.slice();src[axis]=col;return add(z,mul(a,state[encode(src)]));},[0,0]);
    });
  }
  function seedCopy(state) {return state.map((_,index)=> {const ids=decode(index);ids[3]^=ids[2];return state[encode(ids)];});}
  function secondSeed(state) {const A=H(D);return independent?transform(state,3,()=>A):seedCopy(state);}
  function walk(state,axis,clockAxis,inverse) {return transform(state,axis,ids=>inverse?dagger(powers[ids[clockAxis]]):powers[ids[clockAxis]]);}
  function prepare(state,inverse=false) {
    if(inverse) {
      state=walk(state,3,1,true);state=secondSeed(state);state=walk(state,2,0,true);
      for(const axis of [2,1,0]) {const A=H(dims[axis]);state=transform(state,axis,()=>A);}
    } else {
      for(const axis of [0,1,2]) {const A=H(dims[axis]);state=transform(state,axis,()=>A);}
      state=walk(state,2,0,false);state=secondSeed(state);state=walk(state,3,1,false);
    }
    return state;
  }
  return {size,decode,prepare};
}
let amplifiedProbabilities=0;
for(const r of [...report.coherent_amplification_controls,...report.independent_preparations_amplification_countercontrols]) {
  const N=r.rotation_order,Q=r.clock_size,labels=oracle(N,r.hidden_shift_calibration,r.output_permutation);
  const U=floquet(N,labels,r.driver_family),e=execution(N,Q,U,r.second_domain_preparation==="fresh_uniform");
  const zero=Array.from({length:e.size},(_,i)=>[Number(i===0),0]);
  let state=e.prepare(zero),inverse=e.prepare(state,true);
  inverse.forEach((z,i)=>{close(z[0],zero[i][0]);close(z[1],zero[i][1]);});
  const good=index=> {const ids=e.decode(index);return ids[2]!==ids[3]&&labels[ids[2]]===labels[ids[3]];};
  for(let j=0;j<=r.iterations;j++) {
    const success=state.reduce((p,z,i)=>p+(good(i)?norm(z):0),0);
    close(success,r.executed_success_probabilities[j]);close(state.reduce((p,z)=>p+norm(z),0),1);
    amplifiedProbabilities++;
    if(j<r.iterations) {
      state=state.map((z,i)=>good(i)?scale(z,-1):z);
      state=e.prepare(state,true);state[0]=scale(state[0],-1);state=e.prepare(state);
    }
    assert.equal(r.function_evaluations_by_iteration[j],4*(Q-1)+j*(8*(Q-1)+4)+2);
  }
  assert(r.last_control_cost_exceeds_full_table_classical);
}
function gcd(a,b) {while(b)[a,b]=[b,a%b];return a;}
class R {
  constructor(n,d=1n) {n=BigInt(n);d=BigInt(d);const g=gcd(n<0n?-n:n,d);this.n=n/g;this.d=d/g;}
  add(b){return new R(this.n*b.d+b.n*this.d,this.d*b.d);}
  mul(b){return new R(this.n*b.n,this.d*b.d);}
  le(b){return this.n*b.d<=b.n*this.d;}
  eq(b){return this.n===b.n&&this.d===b.d;}
  number(){return Number(this.n)/Number(this.d);}
}
const rr=x=>new R(x.numerator,x.denominator),one=new R(1),minimumOne=x=>x.le(one)?x:one;
const equals=(a,b)=>assert(a.eq(b));
function choose(n,k) {if(k<0||k>n)return 0n;let r=1n;for(let i=1;i<=k;i++)r=r*BigInt(n-i+1)/BigInt(i);return r;}
for(const r of report.native_oracle_pilot_controls) {
  const N=r.rotation_order,b=r.classical_birthday_same_eval_budget,k=b.draws_per_half;
  const denominator=choose(N,k),numerator=denominator-choose(N-k,k),p=new R(numerator,denominator);
  equals(p,rr(b.verified_collision_probability));assert(p.number()>r.actual_verified_two_register_success);
  close(r.two_independent_preparations_collision_baseline,1/r.position_collision_support_after_first_walk);
  assert(p.number()>r.two_independent_preparations_collision_baseline);
  if(!r.exact_zero_from_parity_preserving_driver) assert(r.square_root_amplified_query_PROXY_not_algorithm_bound>r.phase_free_amplified_query_PROXY_not_algorithm_bound);
}
const ledgers=[...report.local_driver_scaling_certificates,report.local_driver_precision_counterledger];
for(const r of ledgers) {
  const n=r.modulus_bits,Q=r.clock_size,Rh=8*(Q+n),D=2n<<BigInt(n),eps=new R(1,1n<<BigInt(n+8));
  assert.equal(r.dyson_truncation_hops,Rh);equals(eps,rr(r.operator_tail_upper));
  const V=D<BigInt(4*Rh+2)?D:BigInt(4*Rh+2),near=D<BigInt(8*Rh+4)?D:BigInt(8*Rh+4);
  const weight=new R(2).mul(one.add(eps)).mul(one.add(eps)).mul(new R(V,D)).add(new R(2).mul(eps).mul(eps));
  const p=minimumOne(new R(near).mul(weight).add(eps.mul(eps)));
  equals(weight,rr(r.maximum_first_walk_position_weight_upper));equals(p,rr(r.verified_clocked_collision_probability_upper));
  equals(minimumOne(weight),rr(r.two_independent_preparations_collision_probability_upper));
  const ideal=minimumOne(new R((2*n*n+1)**2).mul(p));
  equals(ideal,rr(r.ideal_amplified_success_upper));equals(minimumOne(ideal.add(rr(r.assumed_total_composed_trace_error_budget))),rr(r.amplified_success_upper_with_error));
  assert(!r.dyadic_or_chirp_driver_covered&&!r.other_full_oracle_algorithms_covered);
}
let selectedFibreControls=0;
for(const r of report.selected_fibre_preparation_controls) {
  const N=r.rotation_order,D=2*N,labels=oracle(N,r.hidden_shift_calibration,r.output_permutation);
  const u=Array(D).fill(1/Math.sqrt(D)),marked=labels.map(y=>y===r.public_target_label);
  let psi=u.slice();
  for(let j=0;j<r.grover_preparation_iterations;j++) {
    psi=psi.map((a,g)=>marked[g]?-a:a);const overlap=psi.reduce((z,a,g)=>z+a*u[g],0);
    psi=psi.map((a,g)=>2*u[g]*overlap-a);
  }
  const weights=psi.map(a=>a*a),mass=weights.reduce((z,w,g)=>z+(marked[g]?w:0),0);
  close(mass,r.selected_fibre_mass);
  const collision=weights.reduce((z,w,g)=>z+w*weights[partner(N,r.hidden_shift_calibration,g)],0);
  close(collision,r.two_fresh_preparations_collision_success);
  const q=marked.map(x=>Number(x)/Math.sqrt(2)),v=u.map((a,g)=>(a-q[g]/Math.sqrt(N))/Math.sqrt(1-1/N));
  const dot=(a,b)=>a.reduce((z,x,g)=>z+x*b[g],0);
  for(const row of r.protected_path_spectral_controls) {
    const t=row.path_parameter;
    const apply=x=>x.map((a,g)=>a-(1-t)*u[g]*dot(u,x)-t*Number(marked[g])*a);
    const Hq=apply(q),Hv=apply(v),a=dot(q,Hq),b=dot(q,Hv),d=dot(v,Hv);
    close(Math.sqrt((a-d)**2+4*b*b),row.plus_sector_gap);
    close(Math.sqrt(1-4*(1-1/N)*t*(1-t)),row.known_label_search_gap_formula);
    Hq.forEach((x,g)=>close(x,a*q[g]+b*v[g]));Hv.forEach((x,g)=>close(x,b*q[g]+d*v[g]));
  }
  equals(new R(1,N),rr(r.minimum_protected_gap_squared));
  assert.equal(r.two_preparations_function_evaluations_plus_verification,4*r.grover_preparation_iterations+2);
  selectedFibreControls++;
}
let freshCosetPairs=0;
for(const r of report.random_coset_record_countercontrols) {
  const N=r.rotation_order;let good=0,total=0;
  for(let y=0;y<N;y++)for(let z=0;z<N;z++)for(let b=0;b<2;b++)for(let c=0;c<2;c++) {total++;good+=Number(y===z&&b!==c);freshCosetPairs++;}
  const actual=new R(good,total);equals(actual,rr(r.actual_unconditional_two_fresh_records_partner_probability));
  equals(actual,rr(r.position_IPR_after_averaging_independent_records));
  equals(new R(1,2),rr(r.incorrect_average_of_conditional_IPRs));
  equals(new R(1,N),rr(r.two_fresh_coset_records_match_probability));
}
for(const r of report.marker_only_scaling_certificates) {
  const N=1n<<BigInt(r.modulus_bits),j=r.ordinary_amplification_iterations;
  equals(new R(1,N),rr(r.uniform_shift_mean_initial_success_upper));
  equals(minimumOne(new R(BigInt(2*j+1)**2n,N)),rr(r.uniform_shift_mean_amplified_success_upper));
  assert.equal(r.function_evaluations_with_final_verification,4*j+2);
  assert(r.preparation_must_be_oracle_and_secret_independent&&!r.general_full_oracle_DHSP_lower_bound);
}
let allShiftProbabilities=0;
for(const r of report.phase_free_all_shift_controls) {
  const N=r.rotation_order,D=2*N,Q=r.clock_size,C=driver(N,r.driver_family,r.driver_duration);
  let W=identity(D);const probabilities=Array(N).fill(0);
  for(let t=0;t<Q;t++) {
    for(let s=0;s<N;s++)for(let g=0;g<D;g++)probabilities[s]+=norm(W[partner(N,s,g)][g])/(Q*D);
    W=mm(C,W);
  }
  probabilities.forEach((p,s)=>{close(p,r.all_shift_success_probabilities[s]);allShiftProbabilities++;});
  const average=probabilities.reduce((a,b)=>a+b,0)/N;
  close(average,r.uniform_shift_mean_success);
  close(average,Array.from({length:Q},(_,t)=>Math.sin(t*r.driver_duration/2)**2).reduce((a,b)=>a+b,0)/(Q*N));
}
{
  const r=report.finite_time_energy_record_control,N=r.rotation_order,D=2*N,Q=r.clock_size;
  const U=floquet(N,oracle(N,1,Array.from({length:N},(_,i)=>i)),"dyadic"),powers=[identity(D)];
  for(let t=1;t<Q;t++)powers.push(mm(U,powers.at(-1)));
  const filters=Array.from({length:Q},(_,k)=>matrix(D).map((row,i)=>row.map((_,j)=>powers.reduce((z,W,t)=>add(z,scale(mul(expi(-2*Math.PI*k*t/Q),W[i][j]),1/Q)),[0,0]))));
  const completeness=matrix(D);let all=0,matched=0,mass=0;
  filters.forEach(F=> {const gram=mm(dagger(F),F);for(let i=0;i<D;i++)for(let j=0;j<D;j++)completeness[i][j]=add(completeness[i][j],gram[i][j]);});
  for(const F of filters) {
    const first=mv(F,Array.from({length:D},()=>[1/Math.sqrt(D),0]));
    for(let g=0;g<D;g++) {
      const w=norm(first[g]);mass+=w;
      all+=w*filters.reduce((p,G)=>p+norm(G[partner(N,1,g)][g]),0);
      matched+=w*norm(F[partner(N,1,g)][g]);
    }
  }
  for(let i=0;i<D;i++)for(let j=0;j<D;j++){close(completeness[i][j][0],Number(i===j));close(completeness[i][j][1],0);}
  close(mass,1);close(all,r.all_second_outcomes_partner_probability);close(matched,r.same_energy_record_partner_probability_unconditional);
  assert(all>=matched);
}
let geometryControls=0;
for(const N of [8,16,32]) for(let radius=0;radius<N/2;radius++) {
  let ball=new Set([0]),frontier=new Set([0]);
  for(let depth=0;depth<radius;depth++) {
    const next=new Set();
    for(const g of frontier) {
      const b=Math.floor(g/N),x=g%N;
      for(const h of [b*N+mod(x+1,N),b*N+mod(x-1,N),(b^1)*N+mod(-x,N)])if(!ball.has(h))next.add(h);
    }
    for(const h of next)ball.add(h);frontier=next;
  }
  assert(ball.size<=4*radius+2);
  for(let s=0;s<N;s++) {
    let near=0;
    for(let g=0;g<2*N;g++) {
      const b=Math.floor(g/N),x=g%N,r=mod(2*x+(-1)**b*s,N);
      const distance=Math.min(r,N-r)+1;
      assert.equal(ball.has(N+r),distance<=radius);
      if(distance<=radius)near++;
    }
    assert(near<=8*radius+4);geometryControls++;
  }
}
assert(Object.values(report.claim_gate).every(x=>x===false));
console.log(JSON.stringify({matrixEntries,probabilityEntries,quantumControls,amplifiedProbabilities,birthdayComparisons:48,exactScalingLedgers:ledgers.length,markerOnlyLedgers:report.marker_only_scaling_certificates.length,allShiftProbabilities,selectedFibreControls,freshCosetPairs,finiteTimeEnergyInstrumentChecked:true,geometryControls,independentTheoremReview:false,speedupClaimAllowed:false}));

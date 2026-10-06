"use strict";
// Independent bounded field/rotation/QFT replay, NOT independent theorem review.
const fs = require("fs");
const path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/singer_shor_access_closure.json"), "utf8"));
function check(c, message) { if (!c) throw new Error(message); }
function close(a, b, message) { check(Math.abs(a-b) < 2e-12, `${message}: ${a} != ${b}`); }
function gcd(a, b) { while (b) [a,b] = [b,a%b]; return a < 0n ? -a : a; }
function frac(a, b=1n) { const g=gcd(a,b); return [a/g,b/g]; }
function add(a,b) { return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]); }
function mul(a,b) { return frac(a[0]*b[0],a[1]*b[1]); }
function negate(a) { return [-a[0],a[1]]; }
function exact(r) { return frac(BigInt(r.numerator),BigInt(r.denominator)); }
function eq(a,b) { return a[0]*b[1]===a[1]*b[0]; }
function approx(a) { return Number(a[0])/Number(a[1]); }
function rotation(q,j) {
  const c=frac(q*q-8n*(q-1n),q*q);
  let previous=frac(1n), current=c;
  if (!j) return frac(0n);
  for(let k=1;k<j;k++) [previous,current]=[current,add(mul(frac(2n),mul(c,current)),negate(previous))];
  return mul(frac(1n,2n),add(frac(1n),negate(current)));
}
function coords(x,q,m) { return Array.from({length:m},(_,i)=>Math.floor(x/q**i)%q); }
function field(q,m,modulus) {
  const zero=Array(m).fill(0), one=[1,...Array(m-1).fill(0)];
  const mod=x=>((x%q)+q)%q;
  const plus=(a,b)=>a.map((x,i)=>mod(x+b[i]));
  function times(a,b) {
    const c=Array(2*m-1).fill(0);
    for(let i=0;i<m;i++) for(let j=0;j<m;j++) c[i+j]=mod(c[i+j]+a[i]*b[j]);
    for(let k=2*m-2;k>=m;k--) for(let i=0;i<m;i++) c[k-m+i]=mod(c[k-m+i]-c[k]*modulus[i]);
    return c.slice(0,m);
  }
  function power(a,e) {
    let out=one; e=BigInt(e);
    while(e) { if(e&1n) out=times(out,a); a=times(a,a); e>>=1n; }
    return out;
  }
  function trace(a) {
    let out=zero;
    for(let i=0;i<m;i++) { out=plus(out,a); a=power(a,q); }
    check(out.slice(1).every(x=>x===0),"trace not in base field");
    return out[0];
  }
  return {times,power,trace,one};
}
let branches=0, probabilities=0, fieldChecks=0, sourceBits=0, ledgerChecks=0;
for(const r of report.physical_controls) {
  const q=r.base_prime,m=r.extension_degree,N=q**m,v=(N-1)/(q-1),s=Number(r.hidden_shift_calibration);
  const F=field(q,m,r.modulus_coefficients), alpha=r.primitive_element_coefficients;
  const beta=F.power(alpha,s), T=r.trace_pairing_matrix;
  const basis=Array.from({length:m},(_,j)=>coords(q**j,q,m));
  for(let i=0;i<m;i++) for(let j=0;j<m;j++) {
    check(T[i][j]===F.trace(F.times(basis[i],basis[j])),"wrong public trace pairing"); fieldChecks++;
  }
  const logs=r.known_log_calibration_permutation;
  check(logs[0]===N-1,"missing zero sentinel");
  check(new Set(logs).size===N,"log workspace not injective");
  for(let x=1;x<N;x++) {
    check(JSON.stringify(F.power(alpha,logs[x]))===JSON.stringify(coords(x,q,m)),"bad known log");
    const target=F.power(coords(x,q,m),q-1), log=logs[target.reduce((a,c,j)=>a+c*q**j,0)];
    check(log%(q-1)===0,"bad residual subgroup");
    check(r.incorrect_raw_basis_decoder_by_coordinate[x]===log/(q-1),"wrong raw-basis countercontrol");
  }
  for(let k=0;k<v;k++) {
    check(r.source_bits[k]===Number(F.trace(F.times(beta,F.power(alpha,k)))===0),"wrong membership source"); sourceBits++;
  }
  const dual=T.map(row=>row.reduce((a,t,j)=>(a+t*beta[j])%q,0));
  const line=Array.from({length:q},(_,a)=>dual.reduce((b,t,j)=>b+((a*t)%q)*q**j,0));
  check(JSON.stringify(line)===JSON.stringify(r.annihilator_coordinate_indices),"bad annihilator line");
  for(let y=1;y<N;y++) {
    const shift=r.decoded_shift_by_fourier_coordinate[y];
    const z=F.power(alpha,shift), expected=T.map(row=>row.reduce((a,t,j)=>(a+t*z[j])%q,0));
    const observed=coords(y,q,m);
    check(Array.from({length:q-1},(_,a)=>a+1).some(a=>expected.every((t,j)=>(a*t)%q===observed[j])),"wrong residual decoder");
  }
  let state=Array(N).fill(1/Math.sqrt(N)), mean=frac(0n);
  for(const b of r.branches) {
    const j=b.grover_steps;
    if(j) {
      state=state.map((a,x)=>a*(x===0 ? -1 : (-1)**r.source_bits[logs[x]%v]));
      const average=state.reduce((a,x)=>a+x,0)/N;
      state=state.map(a=>2*average-a);
    }
    let success=0;
    for(let y=0;y<N;y++) {
      const ys=coords(y,q,m); let re=0,im=0;
      for(let x=0;x<N;x++) {
        const xs=coords(x,q,m), dot=xs.reduce((a,t,i)=>a+t*ys[i],0);
        const angle=2*Math.PI*(dot%q)/q;
        re+=state[x]*Math.cos(angle)/Math.sqrt(N); im+=state[x]*Math.sin(angle)/Math.sqrt(N);
      }
      const p=re*re+im*im;
      close(p,b.all_output_probabilities[y],"full Fourier probability");
      if(r.decoded_shift_by_fourier_coordinate[y]===s) success+=p;
      if(!line.includes(y)) close(p,0,"off annihilator");
      probabilities++;
    }
    const expected=rotation(BigInt(q),j);
    check(eq(expected,exact(b.exact_nonzero_fourier_success)),"wrong rational rotation");
    close(success,approx(expected),"full recovery success");
    close(success,b.executed_shift_success,"recorded success");
    close(b.discarded_injective_log_workspace_fourier_success,(q-1)/N,"discarded workspace");
    check(b.unknown_xor_oracle_calls===j && b.known_dlog_compute_or_uncompute_calls===2*j,"uncharged query");
    mean=add(mean,expected); branches++;
  }
  mean=mul(mean,frac(1n,BigInt(r.branches.length)));
  check(eq(mean,exact(r.exact_schedule_mean_success)),"wrong schedule mean");
  check(mean[0]*4n>=mean[1],"schedule below constant bound");
}
for(const r of report.growing_base_field_ledgers) {
  const q=BigInt(r.base_order),J=BigInt(r.random_steps_exclusive_upper),R=BigInt(r.independent_repetitions);
  check(J*J*(q-1n)>=q*q && (J-1n)**2n*(q-1n)<q*q,"wrong exact schedule size");
  const Q=R*(J-1n);
  check(BigInt(r.max_total_membership_queries)===Q,"wrong total queries");
  check(BigInt(r.known_coherent_dlog_compute_or_uncompute_calls_upper)===2n*Q,"wrong known maps");
  check(BigInt(r.underlying_dlog_algorithm_or_inverse_invocations_upper)===4n*Q,"wrong BQP compute/uncompute cost");
  check(eq(exact(r.ideal_all_attempts_fail_upper),frac(3n**R,4n**R)),"wrong repeated failure");
  const e=r.coherent_error_budget;
  check(eq(mul(frac(16n*Q*Q),exact(e.per_underlying_known_dlog_computation_failure_upper)),
           mul(exact(e.whole_query_process_total_variation_error_upper),exact(e.whole_query_process_total_variation_error_upper))),"wrong coherent error budget");
  ledgerChecks++;
}
check(Object.values(report.claim_gate).every(x=>x===false),"candidate or novelty promoted");
console.log(JSON.stringify({field_trace_checks:fieldChecks, source_bits:sourceBits, full_branches:branches,
  full_fourier_probabilities:probabilities, exact_scaling_ledgers:ledgerChecks,
  independent_theorem_review:false, actual_Shor_compiler:false, novel_algorithm:false}));

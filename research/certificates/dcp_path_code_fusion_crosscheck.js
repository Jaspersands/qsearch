"use strict";
// Independent native-state, CNOT/H, orbit-sum and full cq-distance replay.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/dcp_path_code_fusion.json"), "utf8"));
function check(v, m) { if (!v) throw new Error(m); }
function close(a, b, m) { check(Math.abs(a-b)<4e-12, `${m}: ${a} != ${b}`); }
function add(a, b) { return [a[0]+b[0], a[1]+b[1]]; }
function scale(a, s) { return [a[0]*s, a[1]*s]; }
function product(a, b) { return [a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]]; }
function conjugate(a) { return [a[0], -a[1]]; }
function norm(a) { return a[0]**2+a[1]**2; }
function weight(v) { let n=0; while(v) { n+=v&1; v>>>=1; } return n; }
function prefix(v, m) { const a=[0]; for(let j=0;j<m-1;j++) a.push(a[j]^((v>>j)&1)); return a; }
function vector(r, secret) {
  const D=4**r.pairs;
  return Array.from({length:D}, (_,v)=>{
    const k=r.native_labels.reduce((a,k,j)=>a+(((v>>j)&1) ? k : 0), 0);
    const theta=2*Math.PI*((k*secret)%r.modulus)/r.modulus;
    return [Math.cos(theta)/Math.sqrt(D), Math.sin(theta)/Math.sqrt(D)];
  });
}
function compiled(r, secret) {
  const m=r.pairs, gates=[];
  for(let j=0;j<m;j++) gates.push([2*j,2*j+1]);
  for(let j=m-2;j>=0;j--) gates.push([2*j+1,2*j+3]);
  for(let j=1;j<m;j++) gates.push([2*j,0]);
  check(JSON.stringify(gates)===JSON.stringify(r.compiler.cnots_in_order), "compiler gate mismatch");
  let v=vector(r,secret);
  for(const [c,t] of gates) v=v.map((_,j)=>v[j^(((j>>c)&1)<<t)]);
  for(const bit of Array.from({length:m-1},(_,j)=>2*j+2).concat([0])) {
    v=v.map((a,j)=>scale(add(v[j&~(1<<bit)],scale(v[j|(1<<bit)], ((j>>bit)&1) ? -1 : 1)), 1/Math.sqrt(2)));
  }
  return Array.from({length:4**(m-1)}, (_,y)=>{
    const z=y%2**(m-1),x=Math.floor(y/2**(m-1)), q=prefix(x,m);
    let index=0;
    for(let j=0;j<m-1;j++) index+=((z>>j)&1)*2**(2*j+3)+q[j+1]*2**(2*j+2);
    return [0,1].map(p=>[0,1].map(t=>v[index|(p<<1)|t]));
  });
}
function orbitAmplitude(r, source, y, p, t) {
  const m=r.pairs, h=m-1, z=y%2**h, x=Math.floor(y/2**h), d=prefix(z,m), q=prefix(x,m);
  let a=[0,0];
  for(let bits=0;bits<2**m;bits++) {
    let index=0, sign=0;
    for(let j=0;j<m;j++) {
      const b=(bits>>j)&1;
      index+=b*2**(2*j)+(b^p^d[j])*2**(2*j+1);
      sign^=b&(q[j]^t);
    }
    a=add(a,scale(source[index],(-1)**sign/Math.sqrt(2**m)));
  }
  return a;
}
function branchDistance(u,v) {
  close(u.reduce((a,b)=>a+norm(b),0), v.reduce((a,b)=>a+norm(b),0), "sign branch norm symmetry");
  let frobenius=0;
  for(let i=0;i<u.length;i++) for(let j=0;j<u.length;j++) {
    const delta=add(product(u[i],conjugate(u[j])),scale(product(v[i],conjugate(v[j])),-1));
    frobenius+=norm(delta);
  }
  // Rank<=2, traceless Hermitian difference: D=sqrt(Tr(delta^2)/2).
  return Math.sqrt(frobenius/2);
}
let amplitudes=0, branches=0, measuredBlocks=0;
check(report.native_controls.length===14,"missing unfiltered controls");
for(const r of report.native_controls) {
  const m=r.pairs, source=vector(r,1), actual=compiled(r,1), other=compiled(r,r.modulus-1);
  let total=0, coherentD=0, measuredD=0;
  const zMarginals=Array(2**(m-1)).fill(0);
  for(let y=0;y<actual.length;y++) {
    let probability=0;
    for(let p=0;p<2;p++) for(let t=0;t<2;t++) {
      const a=actual[y][p][t], orbit=orbitAmplitude(r,source,y,p,t), saved=r.all_unnormalized_branch_amplitudes[y][p][t];
      for(let c=0;c<2;c++) { close(a[c],orbit[c],"orbit-sum identity"); close(a[c],saved[c],"full logical amplitude"); }
      probability+=norm(a); amplitudes++;
    }
    close(probability,r.all_syndrome_probabilities[y],"charged branch probability");
    zMarginals[y%2**(m-1)]+=probability;
    total+=probability;
    coherentD+=branchDistance(actual[y].flat(),other[y].flat());
    for(let p=0;p<2;p++) { measuredD+=branchDistance(actual[y][p],other[y][p]); measuredBlocks++; }
    branches++;
  }
  close(total,1,"full instrument completeness");
  for(const p of zMarginals) close(p,2**(1-m),"Z syndrome uniformity");
  close(coherentD,r.full_coherent_instrument_sign_trace_distance,"coherent cq sign distance");
  close(measuredD,r.measured_pair_fusion_sign_trace_distance,"measured fusion cq sign distance");
  const theta=r.native_labels.map(k=>2*Math.PI*k/r.modulus);
  const formula=m%2 ? Array.from({length:m},(_,j)=>(Math.abs(Math.sin(theta[2*j]+theta[2*j+1]))+Math.abs(Math.sin(theta[2*j]-theta[2*j+1])))/2).reduce((a,b)=>a*b,1) : 0;
  close(measuredD,formula,"exact measured sign product");
  check(measuredD<=coherentD+4e-12 && coherentD<=r.original_input_sign_trace_distance+4e-12,"data-processing broken");
  if(m%2===0) close(coherentD,0,"even-path sign erasure");
}
for(const r of report.scaling_ledgers) {
  const m=BigInt(r.pairs), K=r.fixed_code_full_classical_kernel;
  // K=1/2+((3/2)^m+(1/2)^m)/4, computed without JS float integers.
  const numerator=2n**(m+1n)+3n**m+1n, denominator=2n**(m+2n);
  check(BigInt(K.numerator)*denominator===BigInt(K.denominator)*numerator,"exact path kernel");
  const mean=r.IID_mean_fixed_measured_parity_and_syndrome_probability_nonzero_secret;
  check(BigInt(mean.numerator)*2n**(2n*m-1n)===BigInt(mean.denominator),"uncharged fixed-branch yield");
  check(r.CNOT_count===3*r.pairs-2 && r.Hadamard_count===r.pairs,"compiler resource mismatch");
  check(r.coherent_common_parity_protocol_covered_by_measured_decay===false,"measured bound overreach");
}
const counter=report.linear_label_countercontrol, diagnostic={modulus:counter.modulus, native_labels:counter.native_labels, pairs:3, compiler:report.native_controls.find(r=>r.pairs===3).compiler};
const ratios=[];
for(let s=1;s<counter.modulus;s+=2) {
  const a=compiled(diagnostic,s)[0][0], first=scale(add(a[0],a[1]),1/Math.sqrt(2)), second=scale(add(a[0],scale(a[1],-1)),1/Math.sqrt(2));
  if(norm(first)+norm(second)>1e-13) { close(norm(first),norm(second),"flat phase premise"); ratios.push([s,scale(product(second,conjugate(first)),1/norm(first))]); }
}
let best=Infinity;
for(let L=0;L<counter.modulus;L++) {
  let worst=0;
  for(const [s,ratio] of ratios) { const theta=2*Math.PI*((L*s)%counter.modulus)/counter.modulus; worst=Math.max(worst,Math.hypot(ratio[0]-Math.cos(theta),ratio[1]-Math.sin(theta))); }
  best=Math.min(best,worst);
}
close(best,counter.minimum_over_known_labels_of_worst_secret_ratio_error,"known-label closure falsifier");
check(best>.1,"standard phase-label closure was not falsified");
check(Object.values(report.claim_gate).every(v=>v===false),"unsupported research promotion");
console.log(JSON.stringify({native_controls:report.native_controls.length, logical_amplitudes:amplitudes,
  full_quantum_branches:branches, measured_fusion_blocks:measuredBlocks, exact_scaling_ledgers:report.scaling_ledgers.length,
  independent_theorem_review:false, new_algorithm:false}));

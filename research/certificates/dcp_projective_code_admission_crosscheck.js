"use strict";
// Independent code enumeration and full readout-law replay, not theorem review.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/dcp_projective_code_admission.json"), "utf8"));
function check(c,m) { if(!c) throw new Error(m); }
function close(a,b,m) { check(Math.abs(a-b)<3e-12,`${m}: ${a} != ${b}`); }
function gcd(a,b) { while(b) [a,b]=[b,a%b]; return a<0n ? -a : a; }
function frac(a,b=1n) { const d=gcd(a,b); return [a/d,b/d]; }
function add(a,b) { return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]); }
function multiply(a,b) { return frac(a[0]*b[0],a[1]*b[1]); }
function exact(r) { return frac(BigInt(r.numerator),BigInt(r.denominator)); }
function equal(a,b) { return a[0]*b[1]===a[1]*b[0]; }
function weight(x) { let n=0; while(x) { n+=x&1; x>>>=1; } return n; }
function words(rows) {
  let out=[0];
  for(const row of rows) { const v=row.reduce((a,x,j)=>a+(x<<j),0); out=out.concat(out.map(a=>a^v)); }
  return out;
}
let probabilities=0, shortenedTerms=0, signatureChecks=0;
for(const r of report.physical_controls) {
  const cert=r.certificate, rows=cert.code_rows, C=words(rows),h=rows.length,width=rows[0].length;
  check(new Set(C).size===2**h,"code lost full rank");
  for(const u of C) for(const v of C) check(weight(u&v)%2===0,"noncommuting code representation");
  let K=frac(0n);
  for(const term of cert.shortened_code_terms) {
    const v=Number(BigInt(term.codeword_hex)), count=C.filter(u=>(u&~v)===0).length;
    check(count===2**term.shortened_dimension,"wrong shortened dimension");
    check(term.weight===weight(v),"wrong support weight");
    const contribution=frac(BigInt(count),2n**BigInt(weight(v)));
    check(equal(contribution,exact(term.exact_contribution)),"wrong exact code term");
    K=add(K,contribution); shortenedTerms++;
  }
  check(equal(K,exact(cert.source_averaged_full_collision_kernel)),"wrong full kernel");
  const baseline=frac(3n**BigInt(h),2n**BigInt(h));
  check(K[0]*baseline[1]<=baseline[0]*K[1],"Bell baseline exceeded");
  check(equal(exact(cert.matched_output_bit_individual_X_kernel),frac(3n**BigInt(2*h),2n**BigInt(2*h))),"individual readout baseline omitted");
  check(equal(exact(cert.retained_register_source_quantum_collision),multiply(frac(2n**BigInt(width-2*h)),K)),"quantum remainder collision omitted");
  const permutation=cert.systematic_column_order, tail=cert.systematic_tail;
  const reordered=C.map(v=>permutation.reduce((a,j,i)=>a+(((v>>j)&1)<<i),0));
  const systematicRows=tail.map((row,i)=>Array.from({length:h},(_,j)=>Number(i===j)).concat(row));
  check(JSON.stringify(reordered.slice().sort((a,b)=>a-b))===JSON.stringify(words(systematicRows).sort((a,b)=>a-b)),"invalid systematic certificate");
  for(let i=0;i<h;i++) for(let j=0;j<h;j++) check(tail[i].reduce((a,x,k)=>a+x*tail[j][k],0)%2===Number(i===j),"tail Gram not identity");
  const theta=r.native_labels.map(k=>2*Math.PI*((k*r.secret_calibration)%r.modulus)/r.modulus);
  const L=4**h, coefficients=[];
  for(let b=0;b<2**h;b++) for(let a=0;a<2**h;a++) {
    const u=C[a],v=C[b]; let value=0;
    if((u&~v)===0) {
      value=(-1)**(weight(u)/2);
      for(let i=0;i<width;i++) if((v>>i)&1) value*=((u>>i)&1) ? Math.sin(theta[i]) : Math.cos(theta[i]);
    }
    coefficients[a+(b<<h)]=value;
    close(value,r.full_pauli_expectations[a+(b<<h)],"Pauli expectation");
  }
  for(let y=0;y<L;y++) {
    const p=coefficients.reduce((a,c,x)=>a+(-1)**(weight(x&y)%2)*c,0)/L;
    close(p,r.full_output_probabilities[y],"full probability"); probabilities++;
  }
  close(r.source_qubits_consumed,width,"consumed copies");
  check(!r.postselection_or_cloning_used,"uncharged source");
}
let remainderBranches=0;
for(const r of report.retained_quantum_register_countercontrols) {
  const C=words(r.code_rows),h=r.code_rows.length,width=r.native_labels.length,D=2**width,L=4**h;
  function instrument(secret) {
    const state=Array.from({length:D},(_,x)=>{
      const k=r.native_labels.reduce((a,t,j)=>a+(((x>>j)&1) ? t : 0),0);
      const angle=2*Math.PI*((secret*k)%r.modulus)/r.modulus;
      return [Math.cos(angle)/Math.sqrt(D),Math.sin(angle)/Math.sqrt(D)];
    });
    return Array.from({length:L},(_,y)=>Array.from({length:D},(_,x)=>{
      let re=0,im=0;
      for(let a=0;a<2**h;a++) for(let b=0;b<2**h;b++) {
        const u=C[a],v=C[b],group=a+(b<<h),sign=(-1)**((weight(group&y)+weight(u&x))%2);
        re+=sign*state[x^v][0]/L; im+=sign*state[x^v][1]/L;
      }
      return [re,im];
    }));
  }
  const first=instrument(r.first_secret_calibration),second=instrument(r.second_secret_calibration);
  check(C.includes(D-1)===r.all_ones_in_code,"wrong all-X erasure certificate");
  let distance=0;
  for(let y=0;y<L;y++) {
    let frobenius=0;
    for(let x=0;x<D;x++) for(let z=0;z<D;z++) {
      const u=first[y][x],v=first[y][z],a=second[y][x],b=second[y][z];
      const re=u[0]*v[0]+u[1]*v[1]-a[0]*b[0]-a[1]*b[1];
      const im=u[1]*v[0]-u[0]*v[1]-a[1]*b[0]+a[0]*b[1];
      frobenius+=re*re+im*im;
    }
    // These rank<=2 Hermitian differences have trace0 by exact s/-s symmetry.
    const term=Math.sqrt(frobenius/2);
    close(term,r.unnormalized_branch_trace_distance_terms[y],"retained branch trace distance");
    distance+=term; remainderBranches++;
  }
  close(distance,r.classical_and_retained_quantum_output_trace_distance,"full quantum remainder");
  check(distance<=r.original_native_input_trace_distance+3e-12,"data-processing violated");
  if(r.all_ones_in_code) close(distance,0,"all-X stabilizer failed to erase sign");
}
let logicalAmplitudes=0;
for(const r of report.overlapping_native_logical_branch_controls) {
  const theta=r.native_labels.map(k=>2*Math.PI*((k*r.secret_calibration)%r.modulus)/r.modulus);
  const global=theta.reduce((a,b)=>a+b,0)/2;
  let probability=0;
  for(let p=0;p<2;p++) for(let a=0;a<2;a++) {
    const angles=[0,1,2].map(j=>(theta[2*j]+(-1)**p*theta[2*j+1])/2);
    const C=angles.reduce((b,t)=>b*Math.cos(t),1),S=angles.reduce((b,t)=>b*Math.sin(t),1);
    const re=(Math.cos(global)*C-Math.sin(global)*(-1)**a*S)/4;
    const im=(Math.sin(global)*C+Math.cos(global)*(-1)**a*S)/4;
    let literalRe=0,literalIm=0;
    for(let first=0;first<2;first++) for(let second=0;second<2;second++) {
      const third=a^first^second,bits=[first,p^first,second,p^second,third,p^third];
      const angle=bits.reduce((b,x,j)=>b+x*theta[j],0);
      literalRe+=Math.cos(angle)/16; literalIm+=Math.sin(angle)/16;
    }
    close(literalRe,re,"logical amplitude real formula"); close(literalIm,im,"logical amplitude imaginary formula");
    close(re,r.unnormalized_logical_amplitudes[2*p+a][0],"recorded logical real");
    close(im,r.unnormalized_logical_amplitudes[2*p+a][1],"recorded logical imaginary");
    probability+=re*re+im*im; logicalAmplitudes++;
  }
  close(probability,r.zero_branch_probability,"charged logical branch");
  check(!r.conditional_success_without_branch_cost_claim,"free branch normalization");
}
for(const r of report.odd_secret_signature_controls) {
  for(let k=0;k<32;k++) {
    const phase=k*r.secret_calibration%32;
    const signature=2*phase%32===0 ? "X" : 4*phase%32===0 ? "ZX" : "identity-only";
    check(signature===r.all_public_label_signature[k],"wrong exact Pauli signature");
    check(signature===report.odd_secret_signature_controls[0].all_public_label_signature[k],"odd secret distinguishable by signature");
    signatureChecks++;
  }
}
for(const row of report.scaling_ledgers) {
  const gate=row.sq_gate,N=2n**BigInt(row.modulus_bits), h=BigInt(gate.logical_rows), Q=BigInt(gate.bounded_expectation_queries);
  const d=frac(3n**h-2n**h,2n**h),tau=exact(gate.absolute_tolerance);
  const affected=(d[0]*tau[1]*tau[1])/(d[1]*tau[0]*tau[0]);
  let p=frac(Q*affected+1n,(N-2n)/2n);
  if(p[0]>p[1]) p=frac(1n);
  check(equal(p,exact(gate.uniform_orbit_identification_success_upper)),"wrong scoped SQ gate");
  check(equal(exact(row.native_scalar_commutator_label_fraction),frac(4n,N)),"wrong scalar-commutator fraction");
  check(equal(exact(row.odd_secret_single_state_worst_gap_upper),frac(20n,N*N)),"wrong worst-gap bound");
}
check(Object.values(report.claim_gate).every(v=>v===false),"candidate, novelty or no-go promoted");
console.log(JSON.stringify({full_probabilities:probabilities,shortened_code_terms:shortenedTerms,
  exact_signature_checks:signatureChecks,retained_quantum_branches:remainderBranches,
  unnormalized_logical_amplitudes:logicalAmplitudes,
  independent_theorem_review:false,novel_algorithm:false}));

// Independent bounded state/source verification, not a scalable solver or proof review.
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const root = path.resolve(__dirname, "../..");
const syndromeIndex=process.argv.indexOf("--syndrome-correction");
const syndromeMode=syndromeIndex!==-1;
const reportPath=syndromeMode ? (process.argv[syndromeIndex+1] ||
  path.join(root,"research/reductions/ternary_syndrome_correction.json")) :
  path.join(root,"research/reductions/ternary_decoder_filter.json");
const report = JSON.parse(fs.readFileSync(reportPath));
const check = (x, message) => { if (!x) throw new Error(message); };
const close = (x,y) => check(Math.abs(x-y)<1e-10, `mismatch: ${x}, ${y}`);
const fraction = x => x.numerator/x.denominator;
const mod = x => (x%3+3)%3;
const index = a => a.reduce((x,v) => 3*x+v,0);
function vectors(length, alphabet=[0,1,2]) {
  if (length===0) return [[]];
  return alphabet.flatMap(v => vectors(length-1,alphabet).map(t => [v,...t]));
}
let rootTests=0, branches=0, outputStates=0, checkedMatrices=0;
function verify(row, reference=null) {
  const A=row.labels, n=A.length, m=A[0].length, G=3**n, B=3**m, N=2**m;
  const secrets=vectors(n), observations=vectors(m), signs=vectors(m,[1,2]);
  const decoded=row.decoder_basis_table;
  check(decoded.length===B,"full decoder table required for this finite audit");
  const linear=row.linear_erasure_classical_comparison;
  const R=linear && linear.right_inverse;
  const quadratic=row.quadratic_syndrome_program;
  let QR,QH,QC;
  if (quadratic) {
    QR=quadratic.right_inverse; QH=quadratic.kernel_rows; QC=quadratic.upper_triangle_quadratic_coefficients;
    check(JSON.stringify(A)===JSON.stringify(quadratic.labels),"program/source mismatch");
    check(QR.length===m && QR.every(r=>r.length===n),"quadratic R dimensions");
    check(QH.every(h=>h.length===m) && QC.length===n,"quadratic dimensions");
    check(QR.flat().concat(QH.flat(),QC.flat()).every(x=>Number.isInteger(x) && x>=0 && x<3),"noncanonical program");
    check(A.every((r,i)=>Array.from({length:n},(_,j)=>j).every(j=>
      mod(r.reduce((v,a,k)=>v+a*QR[k][j],0))===(i===j ? 1 : 0))),"quadratic A R != I");
    check(QH.every(h=>A.every(a=>mod(a.reduce((v,x,j)=>v+x*h[j],0))===0)),"H A^T != 0");
  }
  const classical=new Map();
  if (linear) {
    check(R.length===m && R.every(r=>r.length===n),"wrong right-inverse dimensions");
    check(A.every((r,i)=>Array.from({length:n},(_,j)=>j).every(j=>
      mod(r.reduce((v,a,k)=>v+a*R[k][j],0))===(i===j ? 1 : 0))),"A R != I");
    for (const e of signs) {
      const syndrome=A.map(r=>mod(r.reduce((v,a,i)=>v+a*e[i],0)));
      const word=e.map((v,i)=>mod(v-R[i].reduce((sum,a,j)=>sum+a*syndrome[j],0)));
      const key=index(word);
      classical.set(key,(classical.get(key)||0)+1/N);
    }
  }
  for (let j=0;j<B;j++) {
    const b=observations[j];
    // Independent bounded root enumeration; never used as an efficient decoder.
    const roots=secrets.filter(s => A[0].every((_,i) => {
      rootTests++;
      const error=mod(b[i]-1-A.reduce((v,r,k) => v+r[i]*s[k],0));
      return error===0 || error===1;
    }));
    let quadraticValue;
    if (quadratic) {
      const h=QH.map(r=>mod(r.reduce((v,a,i)=>v+a*b[i],0))), monomials=[];
      for(let i=0;i<h.length;i++) for(let j=i;j<h.length;j++) monomials.push(mod(h[i]*h[j]));
      check(QC.every(r=>r.length===monomials.length),"quadratic monomial dimensions");
      quadraticValue=QC.map((r,k)=>mod(r.reduce((v,a,j)=>v+a*monomials[j],0)+b.reduce((v,x,i)=>v+QR[i][k]*x,0)));
    }
    const expected=quadratic ? quadraticValue : linear ? Array.from({length:n},(_,k)=>mod(b.reduce((v,x,i)=>v+R[i][k]*x,0))) :
      row.decoder_mode==="constant-zero" || roots.length!==1 ? Array(n).fill(0) : roots[0];
    check(decoded[j].every((v,k) => v===mod(expected[k]+row.decoder_offset[k])),"decoder table differs from independent root verifier");
  }
  let state=new Float64Array(2*B*G);
  const missing=new Int32Array(B), amplitude=1/Math.sqrt(G*N);
  let failures=0;
  for (let k=0;k<G;k++) {
    const s=secrets[k], ell=A[0].map((_,i) => mod(A.reduce((v,r,j) => v+r[i]*s[j],0)));
    for (const d of signs) {
      const b=index(ell.map((v,i) => mod(v+d[i])));
      const sign=d.reduce((v,x) => v*(x===1 ? 1 : -1),1);
      const residual=s.map((v,i) => mod(v-decoded[b][i]));
      state[2*(b*G+index(residual))]=sign*amplitude;
      if (residual.some(v=>v!==0)) { failures++; missing[b]+=sign; }
      branches++;
    }
  }
  close(fraction(row.exact_decoder_error_probability),failures/(G*N));
  close(fraction(row.exact_missing_coherent_vector_norm_squared),missing.reduce((v,x)=>v+x*x,0)/(G*N));
  // U dagger is a ternary Fourier transform with row phases (1,-i,+i).
  for (let axis=0;axis<m;axis++) {
    const stride=3**(m-1-axis)*G, out=new Float64Array(state.length);
    for (let block=0;block<B*G;block+=3*stride) {
      for (let tail=0;tail<stride;tail++) {
        for (let y=0;y<3;y++) {
          const p=y===0 ? [1,0] : y===1 ? [0,-1] : [0,1];
          for (let x=0;x<3;x++) {
            const theta=2*Math.PI*y*x/3, c=Math.cos(theta), d=Math.sin(theta);
            const re=(p[0]*c-p[1]*d)/Math.sqrt(3), im=(p[0]*d+p[1]*c)/Math.sqrt(3);
            const src=2*(block+x*stride+tail), dst=2*(block+y*stride+tail);
            out[dst]+=re*state[src]-im*state[src+1];
            out[dst+1]+=re*state[src+1]+im*state[src];
          }
        }
      }
    }
    state=out;
  }
  let total=0, success=0, valid=0;
  const H=A.map(r=>[...r.slice(0,-1),mod(r[m-1]+r.slice(0,-1).reduce((v,x)=>v+x,0))]);
  for (let b=0;b<B;b++) {
    const c=observations[b];
    const okay=c.every(v=>v!==0) && A.every(r=>mod(r.reduce((v,a,i)=>v+a*c[i],0))===0);
    let mass=0;
    for (let r=0;r<G;r++) mass+=state[2*(b*G+r)]**2+state[2*(b*G+r)+1]**2;
    if (linear) {
      close(mass,classical.get(b)||0);
      close(mass,linear.actual_quantum_output_probabilities[b]);
      close(mass,fraction(linear.all_classical_output_probabilities[b]));
    }
    if (reference) {
      close(mass,reference.get(b)||0);
      close(mass,row.actual_quantum_word_probabilities[b]);
    }
    total+=mass;
    if (okay) {
      success+=mass; valid++;
      const word=c.map(v=>mod(v*c[m-1]-1));
      word[m-1]=1;
      check(word.every(v=>v===0 || v===1),"non-Boolean output");
      check(H.every(r=>mod(r.reduce((v,a,i)=>v+a*word[i],0))===0),"invalid mapped subset");
      const target=A.map(r=>mod(-r[m-1]-r.slice(0,-1).reduce((v,x)=>v+x,0)));
      check(A.every((r,k)=>mod(r.slice(0,-1).reduce((v,a,i)=>v+a*word[i],0))===target[k]),"incorrect full-target witness");
    }
    outputStates++;
  }
  close(total,1);
  close(success,row.executed_valid_signed_zero_sum_probability);
  close(success,row.executed_nonempty_boolean_zero_sum_probability);
  close(valid/N,fraction(row.random_signed_guess_zero_sum_probability));
  check(1-success<=fraction(row.pointwise_failure_probability_upper_bound)+1e-10,"pointwise error gate violated");
  check(!row.failure_branches_discarded_or_renormalized,"unreported postselection");
  close(success,row.specialized_full_target_source.executed_unconditional_target_success);
  check(!row.specialized_full_target_source.hidden_marker_inclusion_probability_loss,"unreported marker loss");
  checkedMatrices++;
}
if (syndromeMode) {
  check(!report.accepted_speedup_candidate && !report.novelty_claim &&
        !report.all_growing_rank_quadratic_filters_dequantized,"unearned nonlinear claim");
  for(const c of report.controls) {
    const reference=new Map();
    for(const p of c.exact_classical_output_distribution) {
      check(!reference.has(index(p.word)),"duplicate output word");
      reference.set(index(p.word),fraction(p.probability));
    }
    verify(c.actual_quantum_control,reference);
  }
} else {
  const source=report.complete_native_one_dimensional_source;
  const rows=source.all_source_instances_including_failures;
  check(rows.length===81 && new Set(rows.map(r=>JSON.stringify(r.labels))).size===81,"missing native label instances");
  rows.forEach(r=>verify(r));
  verify(report.fixed_two_dimensional_source);
  verify(report.global_decoder_offset_control);
  verify(report.no_decoder_control);
  verify(report.linear_decoder_control);
  const mean=rows.reduce((v,r)=>v+1-r.executed_valid_signed_zero_sum_probability,0)/81;
  close(mean,source.mean_executed_failure_probability);
  check(mean<=fraction(source.failure_upper_bound)+1e-10,"native average gate failed");
  close(report.no_decoder_control.executed_valid_signed_zero_sum_probability,
        fraction(report.no_decoder_control.random_signed_guess_zero_sum_probability));
  check(!report.claim_gate.speedup_claim_allowed && !report.claim_gate.novelty_claim,"unearned claim");
}
for (const [file,hash] of Object.entries(report.dependency_sha256)) {
  check(crypto.createHash("sha256").update(fs.readFileSync(path.join(root,file))).digest("hex")===hash,"stale dependency: "+file);
}
console.log(JSON.stringify({checkedMatrices,rootTests,branches,outputStates,dependencyHashes:Object.keys(report.dependency_sha256).length}));

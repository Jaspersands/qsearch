// Independent bounded state/source verification, not a scalable solver or proof review.
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const root = path.resolve(__dirname, "../..");
const report = JSON.parse(fs.readFileSync(path.join(root, "research/reductions/ternary_decoder_filter.json")));
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
function verify(row) {
  const A=row.labels, n=A.length, m=A[0].length, G=3**n, B=3**m, N=2**m;
  const secrets=vectors(n), observations=vectors(m), signs=vectors(m,[1,2]);
  const decoded=row.decoder_basis_table;
  check(decoded.length===B,"full decoder table required for this finite audit");
  for (let j=0;j<B;j++) {
    const b=observations[j];
    // Independent bounded root enumeration; never used as an efficient decoder.
    const roots=secrets.filter(s => A[0].every((_,i) => {
      rootTests++;
      const error=mod(b[i]-1-A.reduce((v,r,k) => v+r[i]*s[k],0));
      return error===0 || error===1;
    }));
    const expected=row.decoder_mode==="constant-zero" || roots.length!==1 ? Array(n).fill(0) : roots[0];
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
const source=report.complete_native_one_dimensional_source;
const rows=source.all_source_instances_including_failures;
check(rows.length===81 && new Set(rows.map(r=>JSON.stringify(r.labels))).size===81,"missing native label instances");
rows.forEach(verify);
verify(report.fixed_two_dimensional_source);
verify(report.global_decoder_offset_control);
verify(report.no_decoder_control);
const mean=rows.reduce((v,r)=>v+1-r.executed_valid_signed_zero_sum_probability,0)/81;
close(mean,source.mean_executed_failure_probability);
check(mean<=fraction(source.failure_upper_bound)+1e-10,"native average gate failed");
close(report.no_decoder_control.executed_valid_signed_zero_sum_probability,
      fraction(report.no_decoder_control.random_signed_guess_zero_sum_probability));
for (const [file,hash] of Object.entries(report.dependency_sha256)) {
  check(crypto.createHash("sha256").update(fs.readFileSync(path.join(root,file))).digest("hex")===hash,"stale dependency: "+file);
}
check(!report.claim_gate.speedup_claim_allowed && !report.claim_gate.novelty_claim,"unearned claim");
console.log(JSON.stringify({checkedMatrices,rootTests,branches,outputStates,dependencyHashes:Object.keys(report.dependency_sha256).length}));

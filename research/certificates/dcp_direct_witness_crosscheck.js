// Independent output-column contraction, Fourier law and resource arithmetic.
// Not theorem review; no efficient arithmetic finder is supplied.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname,'../..');
const report = JSON.parse(fs.readFileSync(path.join(root,'research/reductions/dcp_direct_witness_filter.json'),'utf8'));
const vec = (v,n,q) => Array.from({length:n},()=>{const x=v%q;v=Math.floor(v/q);return x;});
const idx = (a,q) => a.reduce((s,v,i)=>s+v*q**i,0);
const near = (a,b) => assert.ok(Math.abs(a-b)<1e-10,`${a} != ${b}`);
const read = a => [BigInt(a.sign)*BigInt(a.numerator_hex),BigInt(a.denominator_hex)];
const mul = (a,b) => [a[0]*b[0],a[1]*b[1]];
const add = (a,b) => [a[0]*b[1]+b[0]*a[1],a[1]*b[1]];
const eq = (a,b) => assert.equal(a[0]*b[1],b[0]*a[1]);
const le = (a,b) => a[0]*b[1]<=b[0]*a[1];
const ceilLog = n => n<=1n?0:(n-1n).toString(2).length;
let amplitudeColumns=0,blockEntries=0,secretControls=0;
for(const row of report.known_purified_quantum_finder_controls) {
  const A=row.labels,q=row.full_modulus,n=A.length,N=2**A[0].length,G=q**n,D=row.workspace_basis_dimension;
  const F=x=>idx(A.map(r=>r.reduce((s,a,i)=>s+a*(x>>i&1),0)%q),q);
  const p=Array.from({length:G},()=>Array(N).fill(0));
  row.bounded_solver_output_columns.forEach((column,t)=>{
    assert.equal(column.length,D);
    near(column.reduce((s,a)=>s+a.real**2+a.imag**2,0),1);
    column.forEach((a,w)=>{if(F(w%N)===t)p[t][w%N]+=a.real**2+a.imag**2;amplitudeColumns++;});
  });
  const a=p.map(r=>r.reduce((s,x)=>s+x,0));
  for(let t=0;t<G;t++) {
    near(a[t],row.target_verified_output_probabilities[t]);
    assert.ok(p[t].reduce((s,x)=>s+x*x,0)<=1+1e-10);
    for(let x=0;x<N;x++) {
      near(row.clean_filter_matrix[t][x],p[t][x]);blockEntries++;
      if(F(x)!==t)near(p[t][x],0);
    }
  }
  const mean=a.reduce((s,x)=>s+x,0)/G,herald=a.reduce((s,x)=>s+x*x,0)/N,correct=G*mean*mean/N;
  near(row.unconditional_independent_target_witness_coverage,mean);
  near(row.herald_probability_after_all_workspace_zero_projection,herald);
  near(row.correct_full_secret_probability_for_every_secret,correct);
  near(row.which_target_solver_output_kept_correct_probability,a.reduce((s,x)=>s+x,0)/(N*G));
  for(let secret=0;secret<G;secret++) {
    const s=vec(secret,n,q);let re=0,im=0,norm=0;
    for(let t=0;t<G;t++) {
      const z=vec(t,n,q),angle=2*Math.PI*z.reduce((u,v,i)=>u+v*s[i],0)/q;
      const sr=a[t]*Math.cos(angle)/Math.sqrt(N),si=a[t]*Math.sin(angle)/Math.sqrt(N);
      re+=(sr*Math.cos(angle)+si*Math.sin(angle))/Math.sqrt(G);
      im+=(si*Math.cos(angle)-sr*Math.sin(angle))/Math.sqrt(G);
      norm+=sr*sr+si*si;
    }
    near(re*re+im*im,correct);near(norm,herald);secretControls++;
  }
}
let resourceLedgers=0;
for(const row of report.conditional_raw_full_secret_resource_ledgers) {
  const n=row.dimension,L=row.full_modulus_bits,d=row.density_overhead_bits,beta=read(row.assumed_unconditional_full_target_witness_coverage_lower_bound);
  const amp=row.amplification,R=BigInt(amp.preallocated_disjoint_attempts),v=ceilLog(R)+32,m=n*L+d,M=m+v;
  const ideal=mul(mul(beta,beta),[1n,1n<<BigInt(d)]);
  assert.equal(row.original_phase_states_per_filter_attempt,m);
  assert.equal(row.original_states_per_complete_attempt,M);
  assert.equal(BigInt(row.original_states_preallocated_for_all_attempts),R*BigInt(M));
  assert.equal(row.fresh_candidate_verification_states,v);
  eq(read(row.ideal_full_secret_success_per_original_attempt_lower_bound),ideal);
  const mu=[BigInt(M),BigInt(n*L)],threshold=(8n*mu[0]+mu[1]-1n)/mu[1];
  eq(read(amp.expected_faults_per_complete_block_upper_bound),mu);
  assert.equal(BigInt(amp.maximum_faults_in_good_block),threshold);
  const q=mul(ideal,[1n,1n<<threshold]),den=add([1n,1n],mul([R/2n,1n],q));
  const none=[den[1],den[0]],falseAccept=[R,1n<<BigInt(v)];
  eq(read(amp.no_correct_verified_candidate_on_budget_event_probability_upper_bound),none);
  eq(read(amp.any_wrong_full_candidate_passes_fresh_tests_upper_bound),falseAccept);
  const total=add(add([1n,4n],none),falseAccept);
  eq(read(amp.total_algorithm_failure_probability_upper_bound),total);
  assert.ok(!le([1n,3n],total));
  assert.equal(row.parity_measurement_binary_rank_rejection_or_target_alignment_required,false);
  assert.equal(row.full_secret_top_bit_completion_required,false);
  assert.equal(row.candidate_record_accepted,false);resourceLedgers++;
}
for(const [file,hash] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
}
assert.equal(report.claim_gate.quantum_arithmetic_finder_constructed,false);
assert.equal(report.claim_gate.speedup_claim_allowed,false);
console.log(JSON.stringify({status:'BOUNDED_INDEPENDENT_CROSSCHECK_NOT_THEOREM_REVIEW',amplitudeColumns,
  blockEntries,secretControls,resourceLedgers,dependencyHashes:Object.keys(report.dependency_sha256).length},null,2));

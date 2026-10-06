// Independent bounded arithmetic/source controls, not independent theorem review.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/reductions/dcp_partial_witness_readout.json'), 'utf8'));
const pop = x => { let c = 0; while (x) { x &= x - 1; c++; } return c; };
const mod = (a, q) => (a % q + q) % q;
const vector = (code, n, q) => Array.from({length:n}, () => { const x = code % q; code = Math.floor(code/q); return x; });
const index = (v, q) => v.reduce((s, a, i) => s+a*q**i, 0);
const gcd = (a, b) => { a = a < 0n ? -a : a; while (b) { [a, b] = [b, a%b]; } return a; };
const frac = (a, b=1n) => { const g=gcd(a,b); return [a/g,b/g]; };
const add = (a,b) => frac(a[0]*b[1]+b[0]*a[1], a[1]*b[1]);
const mul = (a,b) => frac(a[0]*b[0], a[1]*b[1]);
const read = a => [BigInt(a.sign)*BigInt(a.numerator_hex), BigInt(a.denominator_hex)];
const eq = (a,b) => assert.equal(a[0]*b[1], b[0]*a[1]);
const le = (a,b) => a[0]*b[1] <= b[0]*a[1];
const minOne = a => le(a,[1n,1n]) ? a : [1n,1n];
const ceilLog = n => n <= 1n ? 0 : (n-1n).toString(2).length;
function chart(A) {
  const n=A.length, m=A[0].length;
  const rows=A.map(row => row.reduce((s,a,i) => s | ((a&1)<<i), 0));
  const pivots=[];
  for (let i=0; i<m; i++) {
    const j=rows.findIndex((row,k) => k>=pivots.length && (row>>i&1));
    if (j<0) continue;
    [rows[pivots.length],rows[j]]=[rows[j],rows[pivots.length]];
    for (let k=0; k<n; k++) if (k!==pivots.length && (rows[k]>>i&1)) rows[k]^=rows[pivots.length];
    pivots.push(i);
  }
  const free=Array.from({length:m},(_,i)=>i).filter(i=>!pivots.includes(i));
  const assignment = z => {
    let word=free.reduce((s,i,j)=>s | ((z>>j&1)<<i),0);
    pivots.forEach((p,j)=>{ if(pop(rows[j]&word)%2) word|=1<<p; });
    return word;
  };
  return {pivots,free,assignment};
}
const sum = (A,x,q) => A.map(row=>mod(row.reduce((s,a,i)=>s+a*(x>>i&1),0),q));
let basisChecks=0, fixedSecrets=0, noiseMasks=0;
for (const row of report.bounded_full_unitary_and_fixed_secret_controls) {
  const A=row.labels,q=row.modulus,Q=q/2,n=A.length,c=chart(A),N=2**c.free.length,G=Q**n;
  assert.equal(c.pivots.length,n);
  const F=x=>index(sum(A,c.assignment(x),q).map(v=>{ assert.equal(v%2,0); return v/2; }),Q);
  const W=new Map(row.accepted_target_witness_pairs);
  for (const [t,w] of W) assert.equal(F(w),t);
  function forward(x,t,flag) {
    const target=t^F(x),valid=W.has(target),w=valid?W.get(target):0;
    return [x^w,target,flag^Number(valid&&x===w)];
  }
  function inverse(x,t,flag) {
    const valid=W.has(t),w=valid?W.get(t):0,old=x^w;
    return [old,t^F(old),flag^Number(valid&&old===w)];
  }
  const seen=new Set();
  for (let x=0;x<N;x++) for(let t=0;t<G;t++) for(let flag=0;flag<2;flag++) {
    const output=forward(x,t,flag);
    assert.deepEqual(inverse(...output),[x,t,flag]);seen.add(output.join(','));basisChecks++;
  }
  assert.equal(seen.size,2*N*G);
  assert.equal(row.full_basis_forward_inverse_checks,2*N*G);
  eq(read(row.uniform_target_coverage),frac(BigInt(W.size),BigInt(G)));
  eq(read(row.herald_probability),frac(BigInt(W.size),BigInt(N)));
  eq(read(row.correct_readout_probability_for_every_secret),frac(BigInt(W.size**2),BigInt(N*G)));
  eq(read(row.which_path_history_not_uncomputed_correct_readout_probability),frac(BigInt(W.size),BigInt(N*G)));
  for(let secret=0;secret<G;secret++) {
    const s=vector(secret,n,Q);let re=0,im=0;
    for(let x=0;x<N;x++) {
      const [clean,t,flag]=forward(x,0,0);
      if(!flag)continue;
      assert.equal(clean,0);
      const a=vector(F(x),n,Q),b=vector(t,n,Q);
      const angle=2*Math.PI*s.reduce((v,d,i)=>v+d*(a[i]-b[i]),0)/Q;
      re+=Math.cos(angle)/Math.sqrt(N*G);im+=Math.sin(angle)/Math.sqrt(N*G);
    }
    assert.ok(Math.abs(re*re+im*im-W.size**2/(N*G))<1e-12);fixedSecrets++;
  }
  const ideal=frac(BigInt(W.size**2),BigInt(N*G));
  for(let bad=0;bad<2**A[0].length;bad++) {
    let total=0n,coins=0n;
    for(let z=0;z<2**A[0].length;z++) if(!(z&~bad)) {
      const amplitude=[...W.values()].reduce((s,w)=>s+(pop(c.assignment(w)&z)%2?-1:1),0);
      total+=BigInt(amplitude**2);coins++;
    }
    assert.ok(le(mul(ideal,[1n,1n<<BigInt(pop(bad))]),frac(total,coins*BigInt(N*G))));noiseMasks++;
  }
}

let sourceImages=0;
for(const row of report.complete_independent_full_target_source_controls) {
  const n=row.dimension,m=row.physical_width,q=row.modulus,Q=q/2,images=new Set();let good=0;
  for(let code=0;code<q**(n*m);code++) {
    const entries=vector(code,n*m,q),A=Array.from({length:n},(_,l)=>entries.slice(l*m,(l+1)*m)),c=chart(A);
    if(c.pivots.length!==n)continue;good++;
    for(let sigma=0;sigma<2**n;sigma++) {
      const origin=Array.from({length:2**n},(_,z)=>c.pivots.reduce((x,p,j)=>x|((z>>j&1)<<p),0))
        .find(x=>sum(A,x,2).every((v,l)=>v===(sigma>>l&1)));
      assert.notEqual(origin,undefined);
      const signed=A.map(r=>r.map((a,i)=>mod((origin>>i&1)?-a:a,q)));
      const offset=sum(A,origin,q);
      for(let t=0;t<Q**n;t++) {
        const target=vector(t,n,Q).map((v,l)=>mod(2*v-offset[l],q));
        const key=JSON.stringify([signed,target]);assert.ok(!images.has(key));images.add(key);
      }
    }
  }
  assert.equal(good,row.full_binary_rank_label_tables);
  assert.equal(images.size,good*q**n);
  assert.equal(images.size,row.parity_wrapper_domain_and_uniform_full_target_image_pairs);sourceImages+=images.size;
}

function envelope(mu) {
  const floor=mu[0]/mu[1],rem=mu[0]%mu[1];
  return frac(2n*mu[1]-rem,(2n*mu[1])<<floor);
}
function selectorLedger(row) {
  const n=row.dimension,L=row.full_modulus_bits,d=row.density_overhead_bits,k=n*(L-1)+d;
  const beta=read(row.assumed_unconditional_uniform_target_coverage_lower_bound),rank=[1n,1n<<BigInt(k)];
  const half=mul(beta,[1n,2n]);
  const retained=le(rank,half)?half:(le(rank,beta)?add(beta,[-rank[0],rank[1]]):[0n,1n]);
  const ideal=mul(mul(retained,retained),[1n,1n<<BigInt(d)]);
  assert.equal(row.original_phase_states_per_attempt,n*L+d);
  assert.equal(row.logical_width,k);
  eq(read(row.coverage_after_charging_full_rank_rejection_lower_bound),retained);
  eq(read(row.ideal_correct_residue_probability_per_original_attempt_lower_bound),ideal);
  const survival=envelope(read(row.expected_prelabel_packet_faults_upper_bound));
  eq(read(row.conditional_independent_fair_Z_mixture_ideal_component_weight_lower_bound),survival);
  eq(read(row.gauged_correct_residue_probability_lower_bound),mul(ideal,survival));return ideal;
}
for(const row of report.conditional_resource_scaling_assuming_missing_finder)selectorLedger(row);
let blockLedgers=0;
for(const row of report.conditional_full_secret_block_ledgers) {
  const n=row.dimension,L=row.full_modulus_bits,p=selectorLedger(row.selector),amp=row.amplification;
  const R=BigInt(amp.preallocated_disjoint_attempts),v=ceilLog(R)+32,c=row.fresh_binary_completion_states-n;
  const M=row.selector.original_phase_states_per_attempt+n+c+v,mu=frac(BigInt(M),BigInt(n*L));
  assert.equal(row.fresh_full_candidate_verification_states,v);
  assert.equal(row.original_states_per_complete_attempt,M);
  assert.equal(BigInt(row.original_states_preallocated_for_all_attempts),R*BigInt(M));
  const ideal=mul(p,frac((1n<<BigInt(c))-1n,1n<<BigInt(c)));
  eq(read(row.ideal_complete_block_success_lower_bound),ideal);
  eq(read(amp.expected_faults_per_complete_block_upper_bound),mu);
  const threshold=(8n*mu[0]+mu[1]-1n)/mu[1];
  assert.equal(BigInt(amp.maximum_faults_in_good_block),threshold);
  const good=R/2n,q=mul(ideal,[1n,1n<<threshold]),term=add([1n,1n],mul([good,1n],q));
  const none=[term[1],term[0]],falseAccept=minOne(frac(R,1n<<BigInt(v))),markov=[1n,4n];
  eq(read(amp.aggregate_budget_failure_probability_upper_bound),markov);
  eq(read(amp.no_correct_verified_candidate_on_budget_event_probability_upper_bound),none);
  eq(read(amp.any_wrong_full_candidate_passes_fresh_tests_upper_bound),falseAccept);
  const failure=minOne(add(add(markov,none),falseAccept));
  eq(read(amp.total_algorithm_failure_probability_upper_bound),failure);
  assert.ok(!le([1n,3n],failure));
  assert.equal(row.full_secret_failure_bound_below_one_third_as_declared,true);blockLedgers++;
}
for(const row of report.legal_target_source_transfer_controls) {
  assert.equal(row.planted_target_coverage_automatically_transfers,false);
  assert.equal(row.mean_of_per_label_legal_coverage_ratios_is_this_law,false);
  eq(read(row.unconditional_verified_target_coverage_lower_bound),mul(read(row.native_legal_pair_probability_lower_bound),[1n,16n]));
}
let verificationDifferences=0;
for(const [n,q] of [[1,8],[2,4]]) for(let delta=1;delta<q**n;delta++) {
  const d=vector(delta,n,q);let p=0;
  for(let label=0;label<q**n;label++) {
    const a=vector(label,n,q),angle=2*Math.PI*d.reduce((s,x,i)=>s+x*a[i],0)/q;
    p+=(1+Math.cos(angle))/2/q**n;
  }
  assert.ok(Math.abs(p-0.5)<1e-12);verificationDifferences++;
}
assert.equal(report.claim_gate.uniform_polynomial_native_finder_supplied,false);
assert.equal(report.claim_gate.candidate_record_accepted,false);
assert.equal(report.claim_gate.speedup_claim_allowed,false);
for(const [file,hash] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
}
console.log(JSON.stringify({status:'BOUNDED_INDEPENDENT_CROSSCHECK_NOT_THEOREM_REVIEW',basisChecks,fixedSecrets,
  noiseMasks,sourceImages,selectorLedgers:report.conditional_resource_scaling_assuming_missing_finder.length,
  blockLedgers,verificationDifferences,dependencyHashes:Object.keys(report.dependency_sha256).length},null,2));

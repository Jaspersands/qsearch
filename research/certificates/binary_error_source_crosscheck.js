// Independent BigInt decoder, native source controls and collision converse.
// Bounded computational crosscheck, not independent mathematical peer review.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const load = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const hensel = load('research/classical_baselines/native_binary_error_hensel.json');
const bridge = load('research/reductions/dcp_binary_error_source_bridge.json');
const noise = load('research/reductions/dcp_fourier_noise_decoder_bound.json');
const pop = x => { let count = 0; while (x) { x &= x - 1n; count++; } return count; };
const parity = x => pop(x) % 2;
const mod = (x, q) => (x % q + q) % q;
const near = (a, b) => assert.ok(Math.abs(a - b) < 1e-9, `${a} != ${b}`);
const vec = (x, n, q) => Array.from({length: n}, () => { const t = x % q; x = Math.floor(x / q); return t; });
const feature = (low, high, n) => {
  let w = low | (high << BigInt(n)), p = 2*n;
  for (let u = 0; u < n; u++) for (let v = u+1; v < n; v++, p++)
    w |= ((low >> BigInt(u) & 1n) * (low >> BigInt(v) & 1n)) << BigInt(p);
  return w;
};
const equation = (a, b) => {
  const n = a.length; let w = 0n, p = 2*n;
  a.forEach((x, j) => {
    w |= ((x*(x+1n-2n*b)/2n) & 1n) << BigInt(j);
    w |= (x & 1n) << BigInt(n+j);
  });
  for (let u = 0; u < n; u++) for (let v = u+1; v < n; v++, p++)
    w |= (a[u]*a[v] & 1n) << BigInt(p);
  return [w, Number(b*(b-1n)/2n & 1n)];
};
const solve = equations => {
  const pivots = new Map(); let inconsistent = false;
  for (let [row, rhs] of equations) {
    while (row) {
      const p = row.toString(2).length - 1;
      if (!pivots.has(p)) { pivots.set(p, [row, rhs]); break; }
      const [r, t] = pivots.get(p); row ^= r; rhs ^= t;
    }
    if (!row && rhs) inconsistent = true;
  }
  let solution = 0n;
  for (const p of [...pivots.keys()].sort((a,b) => a-b)) {
    const [row, rhs] = pivots.get(p);
    if (rhs ^ parity(row & solution)) solution |= 1n << BigInt(p);
  }
  return {rank: pivots.size, solution, inconsistent};
};
let actualNativeDecodes = 0, lifts = 0, coefficientIdentities = 0, pointwiseSourceCases = 0;
for (const trial of hensel.actual_growing_modulus_decoder_trials) {
  const n = trial.dimension, m = trial.samples, L = trial.modulus_bits, q = 1n << BigInt(L);
  const A = trial.native_labels_hex.map(row => row.map(BigInt));
  const b = trial.observations_hex.map(BigInt), expected = trial.expected_planted_secret_hex.map(BigInt);
  const columns = Array.from({length:m}, (_,i) => A.map(row => row[i]));
  const initial = solve(columns.map((a,i) => equation(a,b[i]))), d = n*(n+3)/2;
  assert.equal(initial.rank, d); assert.equal(initial.inconsistent, false);
  const mask = (1n << BigInt(n)) - 1n, low = initial.solution & mask, high = initial.solution >> BigInt(n) & mask;
  assert.equal(feature(low,high,n), initial.solution);
  let secret = Array.from({length:n}, (_,j) => (low >> BigInt(j) & 1n) + 2n*(high >> BigInt(j) & 1n));
  const B = columns.map(a => a.reduce((word,x,j) => word | ((x&1n) << BigInt(j)), 0n));
  for (let bit = 2; bit < L; bit++) {
    const step = solve(columns.map((a,i) => {
      const z = a.reduce((sum,x,j) => sum+x*secret[j], 0n) - b[i], F = z*(z+1n);
      assert.equal(F % (1n << BigInt(bit)), 0n);
      return [B[i], Number(F >> BigInt(bit) & 1n)];
    }));
    assert.equal(step.rank,n); assert.equal(step.inconsistent,false);
    secret = secret.map((s,j) => s + ((step.solution >> BigInt(j) & 1n) << BigInt(bit))); lifts++;
  }
  assert.deepEqual(secret,expected);
  columns.forEach((a,i) => assert.ok([0n,1n].includes(mod(b[i]-a.reduce((sum,x,j) => sum+x*secret[j],0n),q))));
  assert.equal(trial.planted_secret_recovered,true); actualNativeDecodes++;
}
for (const n of [1,2,3]) {
  for (let ai=0; ai<4**n; ai++) for (let b=0; b<4; b++) {
    const a=vec(ai,n,4).map(BigInt), [row,rhs]=equation(a,BigInt(b));
    for (let low=0;low<2**n;low++) for (let high=0;high<2**n;high++) {
      const x=Array.from({length:n},(_,j)=>BigInt((low>>j&1)+2*(high>>j&1)));
      const z=a.reduce((sum,v,j)=>sum+v*x[j],0n)-BigInt(b);
      assert.equal(parity(row&feature(BigInt(low),BigInt(high),n))^rhs,Number(z*(z+1n)/2n&1n));
      coefficientIdentities++;
    }
  }
  const d=n*(n+3)/2, rows=Array.from({length:4**n},(_,i)=>equation(vec(i,n,4).map(BigInt),0n)[0]);
  let minimum=rows.length;
  for(let mask=1n;mask<1n<<BigInt(d);mask++) minimum=Math.min(minimum,rows.reduce((sum,row)=>sum+parity(row&mask),0));
  assert.ok(minimum*4>=rows.length);
}
assert.equal(coefficientIdentities,hensel.polynomial_and_translation_controls.complete_mod_four_polynomial_evaluations);
for (let secret=0;secret<4;secret++) for (let error=0;error<8;error++) {
  const histogram=[0,0,0];
  for(let ai=0;ai<64;ai++) {
    const a=vec(ai,3,4), b=a.map((x,j)=>(x*secret+(error>>j&1))%4);
    const s=solve(a.map((x,j)=>equation([BigInt(x)],BigInt(b[j])))); histogram[s.rank]++;
    if(s.rank===2) assert.equal(Number((s.solution&1n)+2n*(s.solution>>1n&1n)),secret);
    pointwiseSourceCases++;
  }
  assert.equal(histogram[2],42);
}
let markerCases=0;
for(const record of bridge.complete_hidden_marker_source_controls) {
  const q=record.modulus,m=record.original_columns,M=m+1;
  const zero = H => {for(let w=1;w<2**M;w++) if(H.reduce((s,a,j)=>s+a*(w>>j&1),0)%q===0)return w;return null;};
  let accepted=0,weighted=0;
  for(let hi=0;hi<q**M;hi++) {
    const entries=vec(hi,M,q),w=zero(entries);if(w!==null)weighted+=pop(BigInt(w));
    for(let j=0;j<M;j++) {
      const H=[...entries.slice(0,m),mod(BigInt(-entries[m]),BigInt(q))]; H[m]=Number(H[m]);
      [H[j],H[m]]=[H[m],H[j]]; let word=zero(H);
      if(word!==null && (word>>j&1)) {
        if((word>>j&1)!==(word>>m&1))word^=(1<<j)|(1<<m);
        const x=word&((1<<m)-1);
        assert.equal(entries.slice(0,m).reduce((s,a,k)=>s+a*(x>>k&1),0)%q,entries[m]);accepted++;
      }
      markerCases++;
    }
  }
  assert.equal(accepted,weighted);assert.equal(accepted,record.accepted_target_trials);
}
let envelopes=0, optimalDecoders=0;
for(const row of noise.complete_envelope_collision_controls) {
  const q=row.modulus,[a,b]=row.coefficients;
  const p=Array.from({length:q},(_,v)=>{
    const c=Math.cos(-2*Math.PI*v/q),s=Math.sin(-2*Math.PI*v/q);
    const re=a.real+b.real*c-b.imag*s,im=a.imag+b.real*s+b.imag*c;
    return (re*re+im*im)/q;
  });
  p.forEach((x,i)=>near(x,row.probabilities[i]));near(p.reduce((s,x)=>s+x,0),1);
  near(q*p.reduce((s,x)=>s+x*x,0),row.collision_multiplier);assert.ok(row.collision_multiplier<=1.5+1e-10);envelopes++;
}
for(const row of noise.exhaustive_optimal_classical_decoder_controls) {
  const q=row.modulus,n=row.dimension,m=row.samples,A=row.labels,p=row.coordinate_noise_probabilities;let success=0;
  for(let bi=0;bi<q**m;bi++) {
    const b=vec(bi,m,q);let best=0;
    for(let si=0;si<q**n;si++) {
      const s=vec(si,n,q);let likelihood=1;
      for(let i=0;i<m;i++) {
        const e=Number(mod(BigInt(b[i]-A.reduce((sum,r,j)=>sum+r[i]*s[j],0)),BigInt(q)));
        likelihood*=p[i][e];
      }
      best=Math.max(best,likelihood);
    }
    success+=best/q**n;
  }
  near(success,row.actual_exhaustive_optimal_classical_correct_probability);
  assert.ok(success<=row.collision_correct_probability_upper_bound+1e-10);optimalDecoders++;
}
for(const row of noise.native_near_entropy_width_ledgers) {
  const exponent=Math.max(0,Math.floor((5*row.dimension*row.modulus_bits-3*row.columns)/10));
  assert.equal(exponent,row.conservative_correct_probability_dyadic_exponent);
  assert.equal(row.general_quantum_or_native_DCP_decoder_bounded,false);
}
let hashes=0;
let entangledBlockControls=0,subgroupFixedSecrets=0;
for(const row of noise.entangled_Boolean_block_controls) {
  const m=row.Boolean_width,q=row.modulus,amplitude=row.Boolean_amplitudes;
  const words=amplitude.map((_,i)=>Array.from({length:m},(_,j)=>i>>(m-j-1)&1));
  const polynomial=new Map();
  amplitude.forEach((a,i)=>amplitude.forEach((b,j)=>{
    const key=words[i].map((x,k)=>x+words[j][k]).join(','),z=polynomial.get(key)||[0,0];
    z[0]+=a.real*b.real-a.imag*b.imag;z[1]+=a.real*b.imag+a.imag*b.real;
    polynomial.set(key,z);
  }));
  const energy=[...polynomial.values()].reduce((s,[re,im])=>s+re*re+im*im,0);
  near(energy,row.independent_coefficient_additive_energy);
  let collision=0;
  for(let ei=0;ei<q**m;ei++) {
    const e=vec(ei,m,q);let re=0,im=0;
    amplitude.forEach((a,i)=>{
      const angle=-2*Math.PI*e.reduce((s,v,k)=>s+v*words[i][k],0)/q;
      const c=Math.cos(angle),s=Math.sin(angle);
      re+=a.real*c-a.imag*s;im+=a.real*s+a.imag*c;
    });
    collision+=(re*re+im*im)**2/q**m;
  }
  near(collision,energy);near(collision,row.q_to_m_times_Fourier_intensity_collision);
  assert.ok(collision<=(3/2)**m+1e-9);entangledBlockControls++;
}
for(const row of noise.native_subgroup_measurement_scope_countercontrols) {
  const q=row.modulus,L=row.modulus_bits;
  for(let secret=0;secret<q;secret++) {
    let re=0,im=0;
    for(let x=0;x<q;x++) {
      const target=row.labels.reduce((s,a,j)=>s+a*(x>>j&1),0);assert.equal(target,x);
      const angle=2*Math.PI*secret*(target-x)/q;
      re+=Math.cos(angle)/q;im+=Math.sin(angle)/q;
    }
    near(re*re+im*im,1);subgroupFixedSecrets++;
  }
  assert.equal(row.IID_native_literal_label_pattern_probability_dyadic_exponent,L*L);
  assert.equal(row.scalable_native_label_selector_or_quantum_algorithm_supplied,false);
}
for(const report of [hensel,bridge,noise]) {
  for(const [file,hash] of Object.entries(report.dependency_sha256)) {
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);hashes++;
  }
  assert.equal(report.claim_gate.speedup_claim_allowed??report.claim_gate.quantum_speedup_discovered,false);
  assert.equal(report.claim_gate.candidate_record_accepted,false);
}
console.log(JSON.stringify({status:'BOUNDED_INDEPENDENT_CROSSCHECK_NOT_PEER_REVIEW',actualNativeDecodes,lifts,
  coefficientIdentities,pointwiseSourceCases,markerCases,envelopes,optimalDecoders,entangledBlockControls,
  subgroupFixedSecrets,dependencyHashes:hashes},null,2));

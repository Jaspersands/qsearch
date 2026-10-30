// Independent bounded group/state checks, not a theorem or algorithm certificate.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/representation/wreath_coset_permutation_holevo_collapse.json')));
const perms = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
const comp = (a,b) => b.map(i => a[i]);
const inv = a => a.map((_,i) => a.indexOf(i));
const key = x => JSON.stringify(x);
const mul = ([a,b,s],[c,d,t]) => [comp(a,s?d:c),comp(b,s?c:d),s^t];
const ambient = perms.flatMap(a => perms.flatMap(b => [0,1].map(s => [a,b,s])));
const index = new Map(ambient.map((g,i) => [key(g),i]));
const subgroups = perms.map(tau => perms.flatMap(p => [
  [p,comp(comp(tau,p),inv(tau)),0], [comp(p,inv(tau)),comp(tau,p),1]
]));
const states = subgroups.map(hs => {
  const set = new Set(hs.map(key));
  assert.equal(set.size,12);
  for (const h of hs) for (const k of hs) assert(set.has(key(mul(h,k))));
  const matrix = Array(72*72).fill(0);
  ambient.forEach((g,j) => hs.forEach(h => matrix[index.get(key(mul(g,h)))*72+j]++));
  let trace = 0;
  for (let i=0;i<72;i++) {
    trace += matrix[i*72+i];
    for (let j=0;j<72;j++) assert.equal(matrix[i*72+j],matrix[j*72+i]);
  }
  assert.equal(trace,72);
  assert.equal(matrix.reduce((s,x) => s+x*x,0),864);
  return matrix;
});
for (let i=0;i<6;i++) for (let j=0;j<6;j++) {
  const right = new Set(subgroups[j].map(key));
  const common = subgroups[i].filter(h => right.has(key(h))).length;
  const overlapNumerator = states[i].reduce((s,x,k) => s+x*states[j][k],0);
  assert.equal(overlapNumerator,72*common);
}
assert.equal(report.status,'WREATH_SOURCE_CORRECTED_AND_REPAIRED_FAMILY_CLASSICALLY_RECOVERED');
for (const field of ['general_copy_lower_bound_proved','factorial_holevo_collapse_proved',
  'general_code_equivalence_solved','quantum_receiver_implemented','speedup_claim_allowed','accepted_speedup_candidate']) {
  assert.equal(report[field],false);
}
assert.equal(report.invalid_subgroup_counterexample.product_in_proposed_set,false);
const near = (a,b) => assert(Math.abs(a-b)<1e-10);
near(report.physical_state_control.raw_purity,1/6);
near(report.physical_state_control.compressed_purity,(1+1+16)/36);
near(report.physical_state_control.raw_holevo_bits,4/3);
near(report.physical_state_control.compressed_holevo_bits,4/3);
for (const row of report.classical_recovery_controls) {
  assert.equal(row.query_count,row.n*(row.n-1)/2+row.n+1);
  assert.equal(row.exact_recovery,true);
  assert.equal(row.labels_read_as_permutations,false);
}
for (const [field,file] of Object.entries({producer_sha256:'theorems/wreath_coset_permutation_holevo_collapse.py',
  derivation_sha256:'research/WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md'})) {
  assert.equal(report[field],crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'));
}
const active = JSON.parse(fs.readFileSync(path.join(root,'research/registry/negative_results.json')));
assert(!active.some(r => r.id === 'NEG-WREATH-COSET-PERMUTATION-HOLEVO-INFORMATION-COLLAPSE'));
console.log('PASS: six actual S3-wreath coset states, 36 overlaps, corrected scope and live hashes. No universal copy barrier certified.');

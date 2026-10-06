// Independent full-source arithmetic checks, not independent theorem review.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root,
  'research/phase_workbench/dcp_carry_source_law.json'), 'utf8'));
const strata = [
  [[[1, 1, 1, 1]], [3, 12]],
  [[[1, 1, 1, 1, 1, 1]], [15, 51]],
  [[[1, 1, 1, 1]], [3, 15]],
  [[[1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1]], [15, 51]],
  [[[1, 1, 1, 1], [1, 1, 0, 0]], [3, 15]],
];
const mod = (x, q) => (x % q + q) % q;
const phase = (A, x) => A.reduce((sum, a, i) => sum + a * (x >> i & 1), 0);
const rowSource = (B, directions, background, q = 8) => {
  const m = B.length, Q = q / 2, [u, v] = directions;
  const histogram = new Map();
  let accepted = 0;
  for (let source = 0; source < Q ** m; source++) {
    let rest = source;
    const A = B.map(b => { const z = rest % Q; rest = Math.floor(rest / Q); return b + 2 * z; });
    const base = phase(A, background);
    const mixed = phase(A, background ^ u ^ v) - phase(A, background ^ u) - phase(A, background ^ v) + base;
    if (mod(mixed, q)) continue;
    const output = directions.map(w => mod((phase(A, background ^ w) - base) / 2, Q));
    const key = output.join(',');
    histogram.set(key, (histogram.get(key) || 0) + 1);
    accepted++;
  }
  return {histogram, accepted, tableCount: Q ** m};
};
let sourceTables = 0, backgroundRows = 0;
for (let stratum = 0; stratum < strata.length; stratum++) {
  const [B, directions] = strata[stratum], row = report.source_controls[stratum];
  const cert = row.certificate, n = B.length, m = B[0].length;
  assert.equal(cert.acceptance_possible, true);
  assert.equal(cert.selection_lineage_programmatically_verified, false);
  const singleExponent = cert.native_acceptance_probability.denominator_binary_exponent / n;
  const support = 2 ** (cert.conditional_output_entropy_bits / n);
  B.forEach((component, l) => {
    let reference;
    for (let x = 0; x < 2 ** m; x++) {
      const current = rowSource(component, directions, x);
      assert.equal(current.accepted * 2 ** singleExponent, current.tableCount);
      assert.equal(current.histogram.size, support);
      assert.equal(new Set(current.histogram.values()).size, 1);
      for (const key of current.histogram.keys()) {
        const out = key.split(',').map(Number);
        for (const constraint of cert.conditional_low_output_constraints) {
          const sum = out.reduce((value, a, j) => value + ((constraint.output_low_bit_parity_mask >> j & 1) ? a & 1 : 0), 0);
          assert.equal(sum % 2, constraint.target_by_component[l]);
        }
      }
      const canonical = JSON.stringify([...current.histogram].sort(([a], [b]) => a.localeCompare(b)));
      if (reference !== undefined) assert.equal(canonical, reference);
      reference = canonical;
      sourceTables += current.tableCount;
      backgroundRows++;
    }
  });
}

// A COMPLETE two-component higher-label source, not a tensor-product shortcut.
const jointB = strata[4][0], directions = strata[4][1];
const joint = new Map();
let jointAccepted = 0;
for (let source = 0; source < 65536; source++) {
  let rest = source, valid = true;
  const outputs = [];
  for (const component of jointB) {
    const A = component.map(b => { const z = rest % 4; rest = Math.floor(rest / 4); return b + 2 * z; });
    const [u, v] = directions;
    if (mod(phase(A, u ^ v) - phase(A, u) - phase(A, v), 8)) valid = false;
    outputs.push(...directions.map(w => mod(phase(A, w) / 2, 4)));
  }
  if (!valid) continue;
  const key = outputs.join(',');
  joint.set(key, (joint.get(key) || 0) + 1);
  jointAccepted++;
}
assert.equal(jointAccepted, 16384);
assert.equal(joint.size, 64);
assert.equal(new Set(joint.values()).size, 1);

let growingTables = 0;
for (const q of [8, 16, 32]) {
  const result = rowSource([1, 1, 1, 1], [3, 15], 0, q);
  assert.equal(result.accepted * (q / 4), result.tableCount);
  assert.equal(result.histogram.size, q);
  assert.equal(new Set(result.histogram.values()).size, 1);
  growingTables += result.tableCount;
}
for (const row of [...report.overlapping_menu_bounds, ...report.growing_modulus_menu_bounds]) {
  const total = BigInt(row.low_label_defined_overlapping_options) * BigInt(row.supplied_packet_attempts);
  const exponent = row.dimension * (Math.log2(row.modulus) - 2);
  let a = total, b = 1n << BigInt(exponent);
  if (a >= b) [a, b] = [1n, 1n];
  while (a && b % 2n === 0n && a % 2n === 0n) { a /= 2n; b /= 2n; }
  const value = row.native_probability_any_accepted_overlapping_packet_upper_bound;
  assert.equal(a, BigInt(value.numerator_hex));
  assert.equal(b, 1n << BigInt(value.denominator_binary_exponent));
  assert.equal(row.outcome_adaptive_retained_subspaces_covered, false);
}
const points = Array.from({length: 64}, (_, z) => z).filter(z =>
  Array.from({length: 3}, (_, j) => (z >> (2 * j) & 1) * (z >> (2 * j + 1) & 1)).reduce((a, b) => a + b, 0) % 2 === 0);
assert.equal(points.length, 36);
const monomialWeight = indices => points.filter(z => indices.every(j => z >> j & 1)).length;
let parityChecks = 0;
for (let mask = 1; mask < 64; mask++) {
  const indices = Array.from({length: 6}, (_, j) => j).filter(j => mask >> j & 1);
  if (indices.length <= 3) { assert.equal(monomialWeight(indices) % 2, 0); parityChecks++; }
}
const weights = [[0, 1], [2, 3], [4, 5]].map(monomialWeight);
assert.deepEqual(weights, [6, 6, 6]);
assert.equal(weights.reduce((a, b) => a + b / 2, 0) % 2, 1);
assert.equal(report.quadratic_variety_inconsistency_control.certificate.acceptance_possible, false);
for (const [file, hash] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), hash);
}
assert.equal(report.claim_gate.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'SOURCE_ARITHMETIC_CROSSCHECK_ONLY',
  higher_label_tables_with_backgrounds: sourceTables, independent_background_rows: backgroundRows,
  complete_joint_source_tables: 65536, growing_modulus_tables: growingTables,
  divisibility_counterexample_parity_checks: parityChecks,
  exact_menu_bounds: report.overlapping_menu_bounds.length + report.growing_modulus_menu_bounds.length,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));

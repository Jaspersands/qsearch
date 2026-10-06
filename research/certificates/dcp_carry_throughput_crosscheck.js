// Independent exact arithmetic/identity controls, not independent theorem review.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root,
  'research/phase_workbench/dcp_carry_throughput_gate.json'), 'utf8'));
const choose = (n, k) => {
  let out = 1n;
  for (let i = 1; i <= k; i++) out = out * BigInt(n - i + 1) / BigInt(i);
  return out;
};
const gcd = (a, b) => {
  while (b) [a, b] = [b, a % b];
  return a;
};
const frac = (a, b) => { const g = gcd(a, b); return [a / g, b / g]; };
const read = value => frac(BigInt(value.numerator_hex), 1n << BigInt(value.denominator_binary_exponent));
const add = (a, b) => frac(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const clip = value => value[0] >= value[1] ? [1n, 1n] : value;
for (const row of report.native_source_bounds) {
  const n = row.dimension, m = 3 * n, w = Math.floor(m / 32);
  let cuts = 0n, ball = 0n;
  for (let a = 1; a <= n; a++) for (let b = 0; b <= n; b++) {
    if (a === n && b === n) continue;
    const edges = a * (n - b) + (n - a) * b;
    cuts += choose(n - 1, a - 1) * choose(n, b) * (1n << BigInt(n * n - edges));
  }
  for (let j = 1; j <= w; j++) ball += choose(m, j);
  const conductor = clip(add(frac(cuts, 1n << BigInt(n * n)), frac(BigInt(3 * n + 2), 1n << BigInt(n))));
  const distance = frac(ball, 1n << BigInt(n));
  assert.deepEqual(read(row.conductor_failure_bound), conductor);
  assert.deepEqual(read(row.distance_failure_bound), distance);
  assert.deepEqual(read(row.cap_failure_probability_upper_bound), clip(add(conductor, distance)));
  assert.equal(row.fixed_all_outcome_product_output_cap, Math.floor(m / (w + 1)));
  assert.equal(row.outcome_adaptive_direction_selection_covered, false);
}

const parity = x => { let out = 0; while (x) { out ^= x & 1; x >>>= 1; } return out; };
// No RREF, graph decomposition or Python chart routine: enumerate physical
// affine fibers and directly test code preservation versus phase curvature.
let implications = 0, retained = 0;
for (let encoded = 0; encoded < 512; encoded++) {
  const A = [encoded & 7, encoded >> 3 & 7, encoded >> 6 & 7];
  const B = A.reduce((mask, a, i) => mask | ((a & 1) << i), 0);
  const kernel = Array.from({length: 8}, (_, x) => x).filter(x => parity(x & B) === 0);
  const code = new Set([0, B]);
  for (let u of kernel) for (let v of kernel) {
    if (!u || !v || u >= v) continue;
    const overlap = u & v;
    const conductor = code.has(overlap & B);
    for (let syndrome = 0; syndrome < (B ? 2 : 1); syndrome++) {
      let product = true;
      for (let x = 0; x < 8; x++) if (parity(x & B) === syndrome) {
        const phase = z => A.reduce((sum, a, i) => sum + a * (z >> i & 1), 0);
        const mixed = phase(x ^ u ^ v) - phase(x ^ u) - phase(x ^ v) + phase(x);
        if ((mixed % 8 + 8) % 8) product = false;
      }
      assert(!product || conductor);
      implications++;
      retained += Number(product);
    }
  }
}
const control = report.zero_background_false_positive;
const residual = z => {
  const physical = [parity(z), ...Array.from({length: 5}, (_, j) => z >> j & 1)];
  return control.labels[0].reduce((sum, a, i) => sum + a * physical[i], 0) / 2 % 4;
};
const [u, v] = control.logical_directions;
const failures = [];
for (let z = 0; z < 32; z++) {
  const mixed = (residual(z ^ u ^ v) - residual(z ^ u) - residual(z ^ v) + residual(z)) % 4;
  const accepted = control.postselection_ledger.logical_constraint_rows.every((row, j) =>
    parity(row & z) === control.postselection_ledger.constraint_targets[j]);
  assert.equal(accepted, mixed === 0);
  if (!accepted) failures.push(z);
}
assert.deepEqual(failures, control.failing_backgrounds);
assert.equal(failures.length, 16);
for (const [file, hash] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), hash);
}
assert.equal(report.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'ARITHMETIC_AND_IDENTITY_CROSSCHECK_ONLY',
  exact_source_bounds: report.native_source_bounds.length,
  independent_physical_implications: implications, positive_pairs: retained,
  complement_outcomes: 32, dependency_hashes: Object.keys(report.dependency_sha256).length}));

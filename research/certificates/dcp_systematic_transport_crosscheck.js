// Exact source relabeling and calibration identities, not unknown-state decoding.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_systematic_source_transport.json'), 'utf8'));
const mod = (x, q) => (x % q + q) % q;
const apply = (A, x, q) => A.map(row => mod(row.reduce((v, a, i) => v + a * x[i], 0n), q));
const transpose = A => A[0].map((_, j) => A.map(row => row[j]));
const product = (A, B, q) => A.map(row => transpose(B).map(col => mod(row.reduce((v, a, i) => v + a * col[i], 0n), q)));
const decode = A => A.map(row => row.map(BigInt));
const parse = record => ({P: decode(record.binary_prefix), T: decode(record.row_transform),
  Y: decode(record.row_transform_inverse_hex), q: BigInt(record.modulus_hex)});
const tuples = function* (base, width) {
  for (let code = 0; code < base ** width; code++) {
    let x = code;
    const row = Array.from({length: width}, () => { const digit = x % base; x = Math.floor(x / base); return BigInt(digit); });
    yield row;
  }
};
const key = xs => JSON.stringify(xs.map(x => x.toString()));
const fraction = x => [BigInt(x.sign) * BigInt(x.numerator_hex), BigInt(x.denominator_hex)];
let prefixTables = 0, tailColumns = 0, phaseIdentities = 0;
function inverseChecks(f) {
  const n = f.P.length, identity = Array.from({length: n}, (_, i) => Array.from({length: n}, (_, j) => BigInt(i === j)));
  assert.deepEqual(product(f.T, f.Y, f.q), identity);
  assert.deepEqual(product(f.Y, f.T, f.q), identity);
  assert.deepEqual(product(f.T, f.P, 2n), identity);
}
for (const row of report.complete_native_source_controls) {
  const n = row.dimension, q = BigInt(row.modulus), allTailCounts = new Map();
  let localPhase = 0;
  for (const record of row.transports) {
    const f = parse(record.transport); inverseChecks(f);
    const prefixOutputs = new Set();
    for (const H of tuples(Number(q / 2n), n * n)) {
      const A = f.P.map((r, l) => r.map((a, i) => a + 2n * H[n * l + i]));
      const out = product(f.T, A, q);
      for (let l = 0; l < n; l++) for (let i = 0; i < n; i++) assert.equal(out[l][i] % 2n, BigInt(l === i));
      prefixOutputs.add(key(out.flat())); prefixTables++;
    }
    assert.equal(prefixOutputs.size, Number(q / 2n) ** (n * n));
    assert.equal(record.distinct_transformed_higher_prefix_tables, prefixOutputs.size);
    for (const low of tuples(2, n)) {
      const expectedLow = apply(f.T, low, 2n), outputs = new Set();
      for (const H of tuples(Number(q / 2n), n)) {
        const out = apply(f.T, low.map((a, i) => a + 2n * H[i]), q);
        assert.deepEqual(out.map(x => x % 2n), expectedLow);
        const k = key(out); outputs.add(k); allTailCounts.set(k, (allTailCounts.get(k) || 0) + 1); tailColumns++;
      }
      assert.equal(outputs.size, Number(q / 2n) ** n);
    }
    const A = f.P.map((r, l) => [...r.map((a, i) => a + 2n * BigInt((l + i + 1) % 4)), BigInt(3 + 2 * l)]);
    const Ap = product(f.T, A, q);
    for (const s of tuples(Number(q), n)) {
      const sp = apply(transpose(f.Y), s, q);
      assert.deepEqual(apply(transpose(f.T), sp, q), s);
      assert.deepEqual(apply(transpose(Ap), sp, q), apply(transpose(A), s, q));
      phaseIdentities += n + 1; localPhase += n + 1;
    }
    assert.equal(record.transport.selection_uses_binary_prefix_only, true);
    assert.equal(record.transport.row_transform_uses_actual_full_label_prefix_inverse, false);
  }
  assert.equal(allTailCounts.size, Number(q) ** n);
  assert.ok([...allTailCounts.values()].every(x => x === row.all_invertible_binary_prefixes));
  assert.equal(row.fixed_secret_phase_covariance_checks, localPhase);
}
const big = parse(report.arbitrary_precision_transport_control); inverseChecks(big);
const s = [big.q - 1n, big.q - 13n, 1n << 60n];
assert.deepEqual(apply(transpose(big.T), apply(transpose(big.Y), s, big.q), big.q), s);
for (const row of report.scaling_source_ledgers) {
  let num = 1n, den = 1n;
  for (let j = 1; j <= row.dimension; j++) { const power = 1n << BigInt(j); num *= power - 1n; den *= power; }
  const [p, q] = fraction(row.exact_binary_prefix_acceptance_probability);
  assert.equal(num * q, den * p);
  const [a, b] = fraction(row.all_allocated_attempts_reject_probability), R = BigInt(row.allocated_attempts);
  assert.equal(a * den ** R, b * (den - num) ** R);
  assert.ok(den < 4n * num);
  assert.equal(row.original_states_charged, row.allocated_attempts * row.original_states_per_attempt);
  assert.equal(row.transformed_prefix_full_labels_are_exact_identity, false);
  assert.equal(row.uniform_secret_average_is_automatically_a_fixed_secret_decoder_guarantee, false);
}
for (const [relative, digest] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, relative))).digest('hex'), digest);
}
assert.equal(report.claim_gate.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW',
  prefixTables, tailColumns, phaseIdentities, arbitraryPrecisionBits: 65,
  scalingLedgers: report.scaling_source_ledgers.length, dependencyHashes: Object.keys(report.dependency_sha256).length}, null, 2));

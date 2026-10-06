// Bounded independent first-layer arithmetic checks, not theorem review.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_lowbit_fiber_normalizer.json'), 'utf8'));
const mod = (x, q) => (x % q + q) % q;
const wt = x => { let n = 0; while (x) { x &= x - 1; n++; } return n; };
const apply = (rows, z) => rows.reduce((v, row, i) => v | ((wt(row & z) % 2) << i), 0);
const combine = (columns, z) => columns.reduce((v, column, i) => v ^ ((z >> i & 1) ? column : 0), 0);
const independent = rows => {
  const pivots = new Map(), original = [];
  for (const row of rows) {
    let r = row;
    for (const p of [...pivots.keys()].sort((a, b) => b - a)) if (r >> p & 1) r ^= pivots.get(p);
    if (r) { pivots.set(Math.floor(Math.log2(r)), r); original.push(row); }
  }
  return original;
};
const eq = (declared, numerator, denominator = 1n) => {
  assert.equal(BigInt(declared.sign) * BigInt(declared.numerator_hex) * denominator,
    BigInt(numerator) * BigInt(declared.denominator_hex));
};
const residual = (A, z, q) => {
  const n = A.length, k = A[0].length - n;
  A.forEach((row, l) => { for (let i = 0; i < n; i++) assert.equal(row[i] % 2, Number(l === i)); });
  const free = Array.from({length: k}, (_, j) => z >> j & 1);
  const x = [...A.map(row => row.slice(n).reduce((v, a, j) => v ^ (a % 2 & free[j]), 0)), ...free];
  return A.map(row => { const sum = row.reduce((v, a, i) => v + a * x[i], 0); assert.equal(sum % 2, 0); return mod(sum / 2, q / 2); });
};
function geometry(row) {
  const U = row.isotropic_directions_hex.map(Number), columns = row.basis_columns_hex.map(Number), inverse = row.basis_inverse_rows_hex.map(Number);
  const k = row.logical_width, d = row.isotropic_width;
  assert.equal(U.length, d); assert.equal(columns.length, k);
  assert.deepEqual(columns.slice(0, d), U); assert.equal(independent(columns).length, k);
  for (let z = 0; z < 2 ** k; z++) assert.equal(combine(columns, apply(inverse, z)), z);
  return {U, columns, inverse, k, d};
}
function plan(A, q, geo, y) {
  const {U, columns, d} = geo, n = A.length, origin = combine(columns.slice(d), y);
  const c = residual(A, origin, q).map(x => x & 1);
  const rows = Array(n).fill(0);
  U.forEach((u, j) => residual(A, origin ^ u, q).forEach((x, l) => { rows[l] |= ((x & 1) ^ c[l]) << j; }));
  const good = independent(rows).length === n;
  const T = good ? independent([...rows, ...Array.from({length: d}, (_, i) => 1 << i)]) : Array.from({length: d}, (_, i) => 1 << i);
  assert.equal(T.length, d);
  const offset = good ? c.reduce((v, x, l) => v | (x << l), 0) : 0;
  for (let u = 0; u < 2 ** d; u++) {
    const actual = residual(A, origin ^ combine(U, u), q).map(x => x & 1);
    const predicted = rows.map((r, l) => (wt(r & u) % 2) ^ c[l]);
    assert.deepEqual(actual, predicted);
  }
  return {rows, good, T, offset};
}
function permutation(A, q, geo) {
  const {k, d, inverse} = geo, plans = Array.from({length: 2 ** (k - d)}, (_, y) => plan(A, q, geo, y));
  const P = Array(2 ** k).fill(-1);
  for (let z = 0; z < 2 ** k; z++) {
    const v = apply(inverse, z), y = v >> d, u = v & (2 ** d - 1), p = plans[y];
    const w = (apply(p.T, u) ^ p.offset) | (y << d);
    assert.equal(P[w], -1); P[w] = z;
    if (p.good) assert.equal(w & (2 ** A.length - 1), residual(A, z, q).reduce((v, x, l) => v | ((x & 1) << l), 0));
  }
  assert(P.every(x => x >= 0));
  return {P, plans};
}
let sourceTables = 0, permutationChecks = 0;
for (const row of report.complete_middle_source_controls) {
  const B = row.low_labels, n = B.length, m = B[0].length, geo = geometry(row), sources = 2 ** (n * m);
  const histograms = Array.from({length: 2 ** (geo.k - geo.d)}, () => new Map());
  let good = 0;
  for (let code = 0; code < sources; code++) {
    const A = B.map((r, l) => r.map((b, i) => b + 2 * (code >> (l * m + i) & 1)));
    const {P, plans} = permutation(A, 8, geo);
    plans.forEach((p, y) => {
      const key = p.rows.join(','); histograms[y].set(key, (histograms[y].get(key) || 0) + 1);
      good += Number(p.good);
    });
    permutationChecks += P.length;
  }
  assert.equal(sources, row.all_middle_label_tables);
  histograms.forEach(h => {
    assert.equal(h.size, row.distinct_linear_matrices_per_background);
    for (const c of h.values()) assert.equal(c, row.each_linear_matrix_source_multiplicity);
  });
  eq(row.exact_source_mean_good_background_fraction, BigInt(good), BigInt(sources * histograms.length));
  assert.equal(row.whole_permutation_inverse_and_residue_checks, sources * 2 ** geo.k);
  sourceTables += sources;
}
const counter = report.higher_carry_countercontrol, geo = geometry(counter);
const {P, plans} = permutation(counter.labels, counter.modulus, geo);
assert(plans.every(p => p.good));
assert.deepEqual(P, counter.bounded_normalized_to_logical_permutation);
const values = Array.from({length: 2 ** (geo.k - 1)}, (_, r) => {
  const t = counter.fixed_first_residue_bit, F = residual(counter.labels, P[t | (r << 1)], counter.modulus)[0];
  assert.equal(F % 2, t); return (F - t) / 2;
});
assert.deepEqual(values, counter.higher_quotient_values);
const coefficients = values.map(x => x & 1);
for (let j = 0; j < geo.k - 1; j++) for (let mask = 0; mask < coefficients.length; mask++)
  if (mask >> j & 1) coefficients[mask] ^= coefficients[mask ^ (1 << j)];
const terms = coefficients.map((c, i) => c ? i : -1).filter(i => i >= 0);
assert.deepEqual(terms, counter.higher_quotient_low_bit_ANF_masks_hex.map(Number));
assert.equal(Math.max(...terms.map(wt)), counter.higher_quotient_low_bit_degree);
assert(counter.higher_quotient_low_bit_degree > 2);
assert.equal(counter.all_higher_bit_algorithms_or_other_parameterizations_ruled_out, false);
for (const row of report.lattice_regime_first_layer_bounds) {
  const n = row.dimension, k = 4 * n * n + 16, d = Math.ceil(k / (n + 1));
  assert.equal(row.logical_width, k); assert.equal(row.guaranteed_isotropic_width, d);
  let numerator = 1n, exponent = 0;
  for (let i = 0; i < n; i++) { numerator *= (1n << BigInt(d - i)) - 1n; exponent += d - i; }
  eq(row.source_mean_good_background_fraction_lower_bound, numerator, 1n << BigInt(exponent));
  eq(row.source_mean_bad_background_fraction_upper_bound, (1n << BigInt(n)) - 1n, 1n << BigInt(d));
  assert.equal(row.postselected_source_automatically_native_for_next_layer, false);
  assert.equal(row.unknown_secret_recovered, false);
}
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
assert.equal(report.claim_gate.candidate_record_accepted, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW', complete_middle_source_tables: sourceTables,
  whole_permutation_and_residue_checks: permutationChecks, higher_carry_countercontrol_degree: counter.higher_quotient_low_bit_degree,
  lattice_first_layer_scaling_rows: report.lattice_regime_first_layer_bounds.length,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));

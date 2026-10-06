// Independent physical arithmetic and full fresh-bit source controls only.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_conditional_carry_features.json'), 'utf8'));
const wt = x => { let n = 0; while (x) { x &= x - 1; n++; } return n; };
const evaluate = (terms, r) => terms.reduce((v, mask) => v ^ Number((r & mask) === mask), 0);
const decode = outputs => outputs.map(terms => terms.map(Number));
const eq = (declared, numerator, denominator = 1n) => assert.equal(
  BigInt(declared.sign) * BigInt(declared.numerator_hex) * BigInt(denominator),
  BigInt(numerator) * BigInt(declared.denominator_hex));
const rank = rows => {
  const pivots = new Map();
  for (let value of rows) {
    value = BigInt(value);
    for (const p of [...pivots.keys()].sort((a, b) => b - a)) if (value >> BigInt(p) & 1n) value ^= pivots.get(p);
    if (value) pivots.set(value.toString(2).length - 1, value);
  }
  return pivots.size;
};
const combine = (columns, r) => columns.reduce((z, x, i) => z ^ ((r >> i & 1) ? x : 0), 0);
const physical = (A, z) => {
  const n = A.length, k = A[0].length - n, free = Array.from({length: k}, (_, j) => z >> j & 1);
  A.forEach((row, l) => { for (let i = 0; i < n; i++) assert.equal(row[i] % 2, Number(l === i)); });
  return [...A.map(row => row.slice(n).reduce((v, x, j) => v ^ (x % 2 & free[j]), 0)), ...free];
};
const residual = (A, z) => {
  const x = physical(A, z);
  return A.map(row => { const value = row.reduce((v, a, i) => v + a * x[i], 0); assert.equal(value % 2, 0); return value / 2; });
};
const control = report.fixed_pivot_conditional_carry_control;
const features = decode(control.physical_features_anf_hex), offsets = decode(control.carry_offset_anf_hex);
const A0 = control.lower_labels, U = control.isotropic_directions_hex.map(Number), V = control.complement_directions_hex.map(Number);
const P = [], physicalValues = [], carryValues = [];
for (let w = 0; w < 32; w++) {
  const t = w & 1, r = w >> 1, y = r >> 2, bg = combine(V, y), u1 = r & 1, u2 = r >> 1 & 1;
  const c = residual(A0, bg)[0] & 1, L = U.map(u => (residual(A0, bg ^ u)[0] & 1) ^ c);
  assert.equal(L[0], 1);
  const u0 = t ^ c ^ (L[1] & u1) ^ (L[2] & u2), z = bg ^ combine(U, u0 | (u1 << 1) | (u2 << 2));
  P.push(z); assert.equal(residual(A0, z)[0] & 1, t);
  if (!t) {
    const x = physical(A0, z), value = A0[0].reduce((v, a, i) => v + a * x[i], 0);
    assert.equal(value % 4, 0);
    physicalValues.push(x); carryValues.push(value / 4 % 2);
    assert.deepEqual(features.map(f => evaluate(f, r)), x);
    assert.equal(evaluate(offsets[0], r), value / 4 % 2);
  }
}
assert.deepEqual(P, control.bounded_normalized_to_logical_permutation);
assert.deepEqual([...P].sort((a, b) => a - b), Array.from({length: 32}, (_, i) => i));
const cert = control.conditional_source_certificate;
const truthFunctions = features.map(f => Array.from({length: 16}, (_, r) => evaluate(f, r)).reduce((v, x, r) => v | (x << r), 0));
assert.equal(rank(truthFunctions), cert.feature_function_space_rank);
const monomials = [...new Set(features.flat().filter(mask => wt(mask) >= 2))].sort((a, b) => a - b);
assert.equal(rank(features.map(f => monomials.reduce((v, mask, i) => v | (Number(f.includes(mask)) << i), 0))), cert.nonlinear_feature_function_space_rank);
for (let r = 0; r < 16; r++) {
  const physicalMask = physicalValues[r].reduce((v, bit, i) => v | (bit << i), 0);
  cert.linear_recovery_rows_hex.forEach((mask, j) => assert.equal(wt(Number(mask) & physicalMask) % 2, r >> j & 1));
}
const functions = new Map(), weights = new Map();
let chiNumerator = 0, directionChecks = 0, physicalArithmeticChecks = 0;
const sourceFunctions = [];
for (let h = 0; h < 64; h++) {
  const values = physicalValues.map((x, r) => carryValues[r] ^ (x.reduce((v, bit, i) => v + (h >> i & 1) * bit, 0) % 2));
  values.forEach((bit, r) => {
    const value = A0[0].reduce((v, a, i) => v + (a + 4 * (h >> i & 1)) * physicalValues[r][i], 0);
    assert.equal(value % 4, 0); assert.equal(value / 4 % 2, bit); physicalArithmeticChecks++;
  });
  const weight = values.reduce((v, x) => v + x, 0), key = values.join('');
  assert.equal(weight % 2, 1);
  functions.set(key, (functions.get(key) || 0) + 1); weights.set(weight, (weights.get(weight) || 0) + 1);
  chiNumerator += (16 - 2 * weight) ** 2; sourceFunctions.push(values);
}
assert.equal(functions.size, control.distinct_next_bit_functions);
for (const count of functions.values()) assert.equal(count, control.each_next_bit_function_source_multiplicity);
assert.deepEqual(Object.fromEntries([...weights.entries()].sort((a, b) => a[0] - b[0]).map(([w, c]) => [String(w), c])), control.all_source_Hamming_weight_histogram);
eq(control.exact_mean_next_bit_histogram_chi_squared, chiNumerator, 64 * 256);
eq(cert.full_cube_uniform_input_mean_residue_chi_squared, 1, 16);
for (const gate of control.fixed_direction_affine_gates) {
  const [u, v] = gate.directions_hex.map(Number), equations = [], augmented = [];
  for (let r = 0; r < 16; r++) {
    const coefficient = features.reduce((bits, f, i) => bits | ((evaluate(f, r) ^ evaluate(f, r ^ u) ^ evaluate(f, r ^ v) ^ evaluate(f, r ^ u ^ v)) << i), 0);
    const rhs = evaluate(offsets[0], r) ^ evaluate(offsets[0], r ^ u) ^ evaluate(offsets[0], r ^ v) ^ evaluate(offsets[0], r ^ u ^ v);
    equations.push(coefficient); augmented.push(coefficient | (rhs << 6));
  }
  const consistent = rank(equations) === rank(augmented);
  assert.equal(gate.fresh_label_constraint_ranks[0], rank(equations));
  assert.equal(gate.source_constraints_consistent, consistent);
  let count = 0;
  for (const values of sourceFunctions) {
    const affine = Array.from({length: 16}, (_, r) => values[r] ^ values[r ^ u] ^ values[r ^ v] ^ values[r ^ u ^ v]).every(x => x === 0);
    count += Number(affine); assert.equal(affine, false); directionChecks++;
  }
  eq(gate.exact_fixed_direction_affine_source_mass, count, 64);
}
assert.equal(directionChecks, control.complete_source_direction_pairs_checked);
for (const row of report.constant_pivot_radical_controls) {
  const B = row.low_labels, k = row.logical_width, masks = Array.from({length: 2 ** k}, (_, z) => physical(B, z).reduce((v, x, i) => v | (x << i), 0));
  const parityMasks = B.map(b => b.reduce((v, x, i) => v | (x << i), 0));
  const radical = [];
  for (let z = 0; z < masks.length; z++)
    if (masks.every(w => parityMasks.every(b => wt(b & masks[z] & w) % 2 === 0))) radical.push(z);
  const directions = row.radical_directions_hex.map(Number);
  const generated = Array.from({length: 2 ** directions.length}, (_, z) => combine(directions, z)).sort((a, b) => a - b);
  assert.deepEqual(generated, radical); assert.equal(directions.length, row.common_binary_quadratic_radical_dimension);
  assert.equal(row.n_independent_globally_constant_pivot_directions_not_excluded, directions.length >= B.length);
  assert.equal(row.fixed_but_background_varying_nonsingular_pivot_pencils_ruled_out, false);
}
const pencil = report.nonconstant_nonsingular_pivot_pencil_control, B = pencil.low_labels;
const histogram = [0, 0, 0];
for (let h = 0; h < 1024; h++) {
  const A = B.map((row, l) => row.map((b, i) => b + 2 * (h >> (5 * l + i) & 1)));
  let good = 0;
  for (let y = 0; y < 2; y++) {
    const c = residual(A, 4 * y).map(x => x & 1), rows = [0, 0];
    for (let j = 0; j < 2; j++) residual(A, (4 * y) ^ (1 << j)).forEach((x, l) => { rows[l] |= ((x & 1) ^ c[l]) << j; });
    good += Number(rank(rows) === 2);
  }
  histogram[good]++;
}
assert.deepEqual(Object.fromEntries(histogram.map((c, i) => [String(i), c])), pencil.number_of_good_backgrounds_source_histogram);
eq(pencil.conditional_all_backgrounds_invertible_probability, histogram[2], 1024);
eq(pencil.specified_systematic_low_label_source_probability, 1, 64);
const A = pencil.specific_labels, normalized = [];
for (let z = 0; z < 8; z++) {
  const y = z >> 2, u = z & 3, rows = pencil.pivot_matrix_rows_per_background[y], c = residual(A, y << 2).map(x => x & 1);
  const v = rows.reduce((bits, row, l) => bits | ((wt(row & u) % 2 ^ c[l]) << l), 0);
  normalized.push(v | (y << 2)); assert.equal(v, residual(A, z).reduce((bits, x, l) => bits | ((x & 1) << l), 0));
}
assert.deepEqual(normalized, pencil.whole_space_normalization_permutation);
assert.deepEqual([...normalized].sort((a, b) => a - b), Array.from({length: 8}, (_, z) => z));
const counter = report.fresh_H_adaptive_feature_countercontrol;
for (const row of counter.all_fresh_label_tables) {
  assert(row.chosen_physical_direction > 0);
  assert.equal(wt(row.fresh_label_mask & row.chosen_physical_direction) % 2, 0);
}
eq(counter.actual_mean_histogram_chi_squared, 1); eq(counter.invalid_fixed_feature_injective_formula, 1, 2);
const flat = M => M.reduce((value, row, l) => {
  for (let j = 0; j < M.length; j++) value |= (row >> j & 1) << (M.length * j + l);
  return value;
}, 0);
const column = (M, j) => M.reduce((value, row, l) => value | ((row >> j & 1) << l), 0);
const pencilMatrix = (M0, generators, y) => generators.reduce((M, variation, i) =>
  y >> BigInt(i) & 1n ? M.map((row, l) => row ^ variation[l]) : M, [...M0]);
let pencilBackgroundChecks = 0, packetSlopeChecks = 0;
function checkCoverage(row) {
  const M0 = row.constant_matrix_rows, generators = row.variation_generator_rows, n = M0.length;
  const imageRank = rank(generators.map(flat)), columnRanks = Array.from({length: n}, (_, j) => rank(generators.map(M => column(M, j))));
  assert.equal(row.constant_matrix_rank, rank(M0));
  assert.equal(row.background_matrix_image_rank, imageRank);
  assert.deepEqual(row.individual_column_variation_ranks, columnRanks);
  const separable = imageRank === columnRanks.reduce((s, x) => s + x, 0);
  assert.equal(row.background_image_is_cartesian_product_of_column_spaces, separable);
  assert.equal(row.all_columns_vary_and_separability_rules_out_every_constant_part, separable && columnRanks.every(x => x > 0));
  if (row.singular_background_mask_hex !== null) {
    const M = pencilMatrix(M0, generators, BigInt(row.singular_background_mask_hex));
    const v = Number(row.singular_matrix_nonzero_kernel_vector_hex);
    assert(rank(M) < n); assert(v > 0); M.forEach(r => assert.equal(wt(r & v) % 2, 0));
  }
  if (generators.length <= 10) {
    const count = 2 ** generators.length;
    let good = 0;
    for (let y = 0; y < count; y++) { good += Number(rank(pencilMatrix(M0, generators, BigInt(y))) === n); pencilBackgroundChecks++; }
    if (row.all_backgrounds_invertible_certified) assert.equal(good, count);
    if (row.exact_uniform_background_invertibility_fraction !== null) eq(row.exact_uniform_background_invertibility_fraction, good, count);
  }
  if (imageRank === n * n) {
    let numerator = 1n, denominator = 1n;
    for (let j = 1; j <= n; j++) { numerator *= (1n << BigInt(j)) - 1n; denominator <<= BigInt(j); }
    eq(row.exact_uniform_background_invertibility_fraction, numerator, denominator);
  }
  assert.equal(row.one_singular_background_proves_large_failure_mass, false);
  assert.equal(row.approximate_transport_or_general_algorithms_ruled_out, false);
}
report.pivot_pencil_coverage_controls.forEach(checkCoverage);
function bigResidual(A, z) {
  const n = A.length, k = A[0].length - n, free = Array.from({length: k}, (_, j) => Number(z >> BigInt(j) & 1n));
  const x = [...A.map(row => row.slice(n).reduce((s, a, j) => s ^ (a % 2 & free[j]), 0)), ...free];
  return A.map(row => { const v = row.reduce((s, a, i) => s + a * x[i], 0); assert.equal(v % 2, 0); return v / 2 % 2; });
}
for (const row of report.systematic_packet_pencil_profiles) {
  checkCoverage(row);
  const A = row.labels, n = A.length, U = row.isotropic_directions_hex.map(BigInt), V = row.complement_directions_hex.map(BigInt), pivots = row.pivot_indices;
  assert.equal(rank([...U, ...V]), row.logical_width);
  const value0 = U.map(u => bigResidual(A, u));
  const M0 = Array.from({length: n}, (_, l) => pivots.reduce((mask, j, h) => mask | (value0[j][l] << h), 0));
  assert.deepEqual(M0, row.constant_matrix_rows);
  for (let i = 0; i < U.length; i++) for (let j = 0; j < i; j++) {
    const mixed = bigResidual(A, U[i] ^ U[j]);
    mixed.forEach((bit, l) => assert.equal(bit ^ value0[i][l] ^ value0[j][l], 0)); packetSlopeChecks++;
  }
  const variations = V.map(v => {
    const c = bigResidual(A, v), values = pivots.map(j => bigResidual(A, v ^ U[j]));
    return Array.from({length: n}, (_, l) => values.reduce((mask, value, h) => mask | ((value[l] ^ c[l] ^ value0[pivots[h]][l]) << h), 0));
  });
  assert.deepEqual(variations, row.variation_generator_rows);
  assert.equal(row.physical_assignments_or_secret_states_enumerated, false);
  assert.equal(row.finite_profiles_prove_typical_large_n_source_behavior, false);
}
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
assert.equal(report.claim_gate.candidate_record_accepted, false);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW', fixed_pivot_permutation_points: P.length,
  physical_fresh_bit_arithmetic_checks: physicalArithmeticChecks, complete_fresh_bit_sources: 64,
  fixed_direction_affine_gates: control.fixed_direction_affine_gates.length, source_direction_pairs: directionChecks,
  radical_controls: report.constant_pivot_radical_controls.length, native_pencil_middle_sources: 1024,
  adaptive_feature_counter_sources: 4, pivot_pencil_coverage_controls: report.pivot_pencil_coverage_controls.length,
  bounded_pencil_background_checks: pencilBackgroundChecks,
  actual_systematic_packet_profiles: report.systematic_packet_pencil_profiles.length,
  packet_isotropic_pair_checks: packetSlopeChecks,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));

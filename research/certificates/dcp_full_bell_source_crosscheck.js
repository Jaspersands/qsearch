// Independent physical root/quartet counts, not independent theorem review.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root,
  'research/phase_workbench/dcp_full_bell_source_moments.json'), 'utf8'));
const mod = (a, q) => (a % q + q) % q;
const parity = x => { let p = 0; while (x) { p ^= x & 1; x >>= 1; } return p; };
const gcd = (a, b) => { while (b) [a, b] = [b, a % b]; return a; };
const fraction = (a, b = 1n) => {
  a = BigInt(a); b = BigInt(b);
  assert(a >= 0n && b > 0n);
  const d = gcd(a, b);
  return [a / d, b / d];
};
const add = (a, b) => fraction(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const multiply = (a, b) => fraction(a[0] * b[0], a[1] * b[1]);
const power = e => 1n << BigInt(e);
const check = (value, encoded) => {
  assert(encoded.sign === 0 || encoded.sign === 1);
  assert.deepEqual(value, fraction(BigInt(encoded.numerator_hex), power(encoded.denominator_binary_exponent)));
};
const leftRows = [3, 1, 2], rightRows = [1, 1, 2];
const phase = (labels, rows, z) => {
  const sum = labels.reduce((a, b, i) => a + b * parity(rows[i] & z), 0);
  assert.equal(mod(sum, 2), 0);
  return sum / 2;
};
const numerators = (left, right, u, secret) => Array.from({length: 4}, (_, v) => {
  const roots = [0, 0, 0, 0];
  for (let z = 0; z < 4; z++) roots[mod(secret * (phase(left, leftRows, z)
    + phase(right, rightRows, z ^ u)) + 2 * parity(z & v), 4)]++;
  return (roots[0] - roots[2]) ** 2 + (roots[1] - roots[3]) ** 2;
});
const totals = new Map([[0, 0n], [3, 0n]]);
for (let source = 0; source < 4096; source++) {
  const high = Array.from({length: 6}, (_, i) => Math.floor(source / 4 ** i) % 4);
  const left = [1, 1, 1].map((b, i) => b + 2 * high[i]);
  const right = [1, 1, 0].map((b, i) => b + 2 * high[i + 3]);
  for (const u of totals.keys()) {
    const values = numerators(left, right, u, 1);
    assert.equal(values.reduce((a, b) => a + b, 0), 16);
    assert.deepEqual(values, numerators(left, right, u, 3));
    totals.set(u, totals.get(u) + BigInt(values.reduce((a, b) => a + b * b, 0)));
  }
}
const physicalMask = (rows, h) => rows.reduce((a, row, i) => a + parity(row & h) * 2 ** i, 0);
const disjointCount = (left, right) => {
  let count = 0;
  for (let h = 0; h < 4; h++) for (let j = 0; j < 4; j++)
    if (!(physicalMask(left, h) & physicalMask(left, j)) &&
        !(physicalMask(right, h) & physicalMask(right, j))) count++;
  return count;
};
const D = disjointCount(leftRows, rightRows);
const source = report.complete_q8_source;
assert.equal(source.complete_higher_label_tables, 4096);
assert.equal(source.certificate.ordered_disjoint_physical_direction_pairs, D);
for (const [u, total] of totals) {
  check(fraction(total, 64n * 4096n), source.source_mean_relative_collisions[String(u)]);
  assert.deepEqual(fraction(total, 64n * 4096n), fraction(D, 4));
}
let quartets = 0;
for (const row of report.growing_modulus_quartets) {
  let surviving = 0;
  for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++)
    for (let c = 0; c < 4; c++) for (let d = 0; d < 4; d++) {
      const valid = [leftRows, rightRows].every(rows => rows.every(r =>
        mod(parity(r & a) - parity(r & b) + parity(r & c) - parity(r & d), row.modulus / 2) === 0));
      if (valid) surviving++;
      quartets++;
    }
  assert.equal(surviving, 4 * D);
  assert.equal(surviving, row.physical_source_surviving_quartets);
  check(fraction(D, 4), row.certificate.high_label_mean_relative_full_collision);
}
let systematicTotal = 0;
for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++)
  systematicTotal += disjointCount([a, 1, 2], [b, 1, 2]);
check(fraction(systematicTotal, 64), report.systematic_source_control.mean_relative_collision);
assert.deepEqual(fraction(systematicTotal, 64), fraction(65, 32));
for (const row of report.systematic_source_scaling) {
  const n = row.dimension, k = 2 * n, N = power(k);
  let prefix = [1n, 1n];
  for (let j = 1; j <= n; j++) prefix = multiply(prefix, fraction(power(j) - 1n, power(j)));
  check(multiply(prefix, prefix), row.two_public_prefix_invertibility_probability);
  const mean = add(fraction(2n * N - 1n, N),
    fraction((3n ** BigInt(k) - 2n * N + 1n) * 3n ** BigInt(2 * n), N * 4n ** BigInt(2 * n)));
  check(mean, row.conditional_mean_relative_full_collision);
  assert.equal(row.mean_does_not_prove_typical_instance_signal, true);
  assert.equal(row.conditions_on_prefix_success_not_unconditional_claim, true);
  assert.equal(row.speedup_claim_allowed, false);
}
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
const verificationControls = [[8n, [2n]], [128n, [64n, 0n]], [1n << 64n, [2n, 0n]], [8n, [0n]]];
report.fresh_native_candidate_verification.forEach((row, index) => {
  const [q, delta] = verificationControls[index];
  const divisor = delta.reduce((a, b) => gcd(a, b), q);
  assert.equal(BigInt(row.difference_character_image_order), q / divisor);
  const equal = divisor === q;
  assert.equal(row.candidate_equals_secret, equal);
  check(equal ? fraction(1) : fraction(1, 2), row.one_test_high_source_average_acceptance);
  check(equal ? fraction(1) : fraction(1n, power(row.verification_states_consumed)),
    row.all_tests_high_source_average_acceptance);
  assert.equal(row.requires_fresh_original_native_phase_states, true);
  assert.equal(row.candidate_committed_before_verification_labels, true);
  assert.equal(row.ideal_noiseless_and_exact_measurement_model, true);
  assert.equal(row.decoder_implemented, false);
});
let residueSourceTables = 0;
report.fresh_packet_residue_verification.forEach((row, delta) => {
  let total = 0;
  for (let code = 0; code < 64; code++) {
    const A = [0, 1, 2].map(i => 1 + 2 * (Math.floor(code / 4 ** i) % 4));
    const roots = [0, 0, 0, 0];
    for (let z = 0; z < 4; z++) roots[mod(delta * phase(A, leftRows, z), 4)]++;
    total += (roots[0] - roots[2]) ** 2 + (roots[1] - roots[3]) ** 2;
    residueSourceTables++;
  }
  check(fraction(total, 16 * 64), row.one_test_conditional_high_source_mean_acceptance);
  check(delta === 0 ? fraction(1) : fraction(1, 64), row.all_tests_conditional_high_source_mean_acceptance);
  assert.equal(row.fresh_original_phase_states_consumed, 9);
  assert.equal(row.does_not_recover_lost_original_high_bit, true);
});
for (const row of report.known_residue_high_bit_completion) {
  check(fraction(power(row.dimension) - 1n, power(row.fresh_original_phase_states_consumed)),
    row.highest_bit_vector_binary_rank_failure_upper_bound);
  assert.equal(row.requires_correct_known_s_mod_q_over_two, true);
  assert.equal(row.incorrect_residue_not_covered, true);
}
const plan = report.known_residue_correction_plan;
assert.equal(plan.modulus, 8);
assert.equal(plan.reusable_clean_ancillas, 1);
assert.equal(plan.unknown_secret_or_phase_evaluator_required, false);
assert.equal(plan.physical_backend_execution_verified, false);
let cnotCount = 0, xCount = 0;
const popcount = x => { let c = 0; while (x) { c += x & 1; x >>= 1; } return c; };
plan.steps_compute_phase_uncompute.forEach(step => {
  cnotCount += 2 * popcount(Number(BigInt(step.logical_parity_mask_hex)));
  xCount += 2 * step.affine_origin;
});
assert.equal(plan.cnot_gates, cnotCount);
assert.equal(plan.x_gates, xCount);
for (let z = 0; z < 8; z++) {
  const rows = [7, 1, 2, 4], origins = [1, 0, 0, 0], A = [1, 3, 5, 7];
  const x = rows.map((r, i) => origins[i] ^ parity(r & z));
  const delta = A.reduce((a, b, i) => a + b * (x[i] - origins[i]), 0);
  assert.equal(mod(delta, 2), 0);
  const correction = plan.steps_compute_phase_uncompute.reduce((a, step) =>
    a + Number(BigInt(step.known_phase_exponent_mod_q_hex)) *
    (step.affine_origin ^ parity(Number(BigInt(step.logical_parity_mask_hex)) & z)), 0);
  assert.equal(mod(correction + delta, 8), 7);
}
assert.equal(report.claim_gate.collision_mean_is_secret_mutual_information, false);
assert.equal(report.claim_gate.negation_ambiguity_closes_general_complex_measurements, false);
assert.equal(report.claim_gate.independent_theorem_review, false);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'BOUNDED_ARITHMETIC_CROSSCHECK_ONLY',
  complete_higher_label_tables: 4096, exact_full_output_and_negation_checks: 8192,
  growing_modulus_quartets: quartets, complete_systematic_pair_tables: 16,
  exact_scaling_rows: report.systematic_source_scaling.length,
  exact_native_verification_rows: report.fresh_native_candidate_verification.length,
  packet_residue_source_tables_across_differences: residueSourceTables,
  lost_bit_completion_bounds: report.known_residue_high_bit_completion.length,
  explicit_known_residue_correction_assignments: 8,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));

// Independent exact arithmetic and bounded physical counts, not theorem review.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const load = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const physical = load('research/phase_workbench/dcp_physical_phase_noise.json');
const completion = load('research/phase_workbench/dcp_noisy_completion.json');
const gauged = load('research/phase_workbench/dcp_prelabel_fault_gauge.json');
const gcd = (a, b) => { a = a < 0n ? -a : a; while (b) [a, b] = [b, a % b]; return a; };
const R = (a, b = 1n) => {
  a = BigInt(a); b = BigInt(b); assert(b > 0n);
  if (!a) return [0n, 1n];
  const g = gcd(a, b); return [a / g, b / g];
};
const add = (a, b) => R(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const neg = a => [-a[0], a[1]];
const sub = (a, b) => add(a, neg(b));
const mul = (a, b) => R(a[0] * b[0], a[1] * b[1]);
const div = (a, b) => R(a[0] * b[1], a[1] * b[0]);
const pow = (a, k) => R(a[0] ** BigInt(k), a[1] ** BigInt(k));
const one = R(1), half = R(1, 2);
const read = a => R(BigInt(a.sign) * BigInt(a.numerator_hex), BigInt(a.denominator_hex));
const check = (a, encoded) => assert.deepEqual(a, read(encoded));
const lt = (a, b) => a[0] * b[1] < b[0] * a[1];
const parity = a => { let p = 0; while (a) { p ^= a & 1; a >>= 1; } return p; };
const wt = a => { let p = 0; while (a) { p += a & 1; a >>= 1; } return p; };
const bits = (rows, h) => rows.reduce((a, r, i) => a + parity(r & h) * 2 ** i, 0);
const errorWeight = (mask, width, epsilon) => mul(pow(epsilon, wt(mask)), pow(sub(one, epsilon), width - wt(mask)));

// Full original-mask pushforward, including correlated logical-bit marginals.
const correlation = physical.correlation_control;
const rows = [[3, 1, 2], [1, 1, 2]], distribution = Array.from({length: 4}, () => R(0));
const rate = read(correlation.rate);
for (let e1 = 0; e1 < 8; e1++) for (let e2 = 0; e2 < 8; e2++) {
  const eta = rows.reduce((a, rs, side) => a ^ rs.reduce((b, r, i) => b ^ (((side ? e2 : e1) >> i & 1) ? r : 0), 0), 0);
  distribution[eta] = add(distribution[eta], mul(errorWeight(e1, 3, rate), errorWeight(e2, 3, rate)));
}
distribution.forEach((a, i) => check(a, correlation.logical_error_distribution[i]));
const marginal = [add(distribution[1], distribution[3]), add(distribution[2], distribution[3])];
marginal.forEach((a, i) => check(a, correlation.logical_bit_error_marginals[i]));
check(distribution[3], correlation.joint_two_bit_error);
check(mul(...marginal), correlation.product_of_bit_error_marginals);
assert.notDeepEqual(distribution[3], mul(...marginal));

// Complete higher-label physical amplitudes in Z[i], followed by all 16 masks.
const full = physical.complete_noisy_full_source;
const law = [R(0), R(0)], epsilon = read(full.physical_rate);
for (let e = 0; e < 16; e++) law[parity(e)] = add(law[parity(e)], errorWeight(e, 4, epsilon));
let total = R(0);
for (let code = 0; code < 256; code++) {
  const A = Array.from({length: 4}, (_, i) => 1 + 2 * (Math.floor(code / 4 ** i) % 4));
  const p = [0, 1].map(v => {
    const roots = [0, 0, 0, 0];
    for (let z = 0; z < 2; z++) {
      // First syndrome=0, second=1, Bell XOR outcome=1.
      const rightZ = z ^ 1;
      const angle = ((A[0] + A[1]) * z + A[2] * (-rightZ) + A[3] * rightZ) / 2 + 2 * v * z;
      assert(Number.isInteger(angle));
      roots[(angle % 4 + 4) % 4]++;
    }
    return R((roots[0] - roots[2]) ** 2 + (roots[1] - roots[3]) ** 2, 4);
  });
  assert.deepEqual(add(...p), one);
  const noisy = [0, 1].map(v => add(mul(law[0], p[v]), mul(law[1], p[v ^ 1])));
  total = add(total, mul(R(2), add(pow(noisy[0], 2), pow(noisy[1], 2))));
}
check(div(total, R(256)), full.source_mean_relative_collision);
check(div(total, R(256)), full.certificate.high_source_mean_relative_full_collision);

for (const row of physical.systematic_low_controls) {
  const e = read(row.physical_rate), a = pow(sub(one, mul(R(2), e)), 2);
  let collision = R(0), correctAccept = R(0);
  for (let x = 0; x < 4; x++) for (let y = 0; y < 4; y++)
    for (let h = 0; h < 4; h++) for (let j = 0; j < 4; j++) {
      const images = [x, y].map(z => bits([z, 1, 2], h));
      if ([x, y].every((z, i) => !(images[i] & bits([z, 1, 2], j))))
        collision = add(collision, div(pow(a, images.reduce((s, v) => s + wt(v), 0)), R(64)));
    }
  for (let x = 0; x < 4; x++) for (let mask = 0; mask < 8; mask++) {
    const logical = ((mask & 1) ? x : 0) ^ ((mask & 2) ? 1 : 0) ^ ((mask & 4) ? 2 : 0);
    if (!logical) correctAccept = add(correctAccept, div(errorWeight(mask, 3, e), R(4)));
  }
  check(collision, row.source_mean_relative_collision);
  check(correctAccept, row.known_residue_all_zero_acceptance);
}
const prefix = n => {
  let value = one;
  for (let j = 1; j <= n; j++) value = mul(value, R((1n << BigInt(j)) - 1n, 1n << BigInt(j)));
  return pow(value, 2);
};
const source = row => {
  const n = row.dimension, k = 2 * n, N = R(1n << BigInt(k));
  const e = read(row.physical_phase_flip_probability), a = pow(sub(one, mul(R(2), e)), 2);
  const single = pow(add(one, pow(a, 2)), k), pair = pow(add(R(2), pow(a, 2)), k);
  const mean = div(add(add(N, mul(sub(single, one), pow(div(add(one, a), R(2)), k))),
    mul(add(sub(sub(pair, N), single), one), pow(div(add(R(2), a), R(4)), k))), N);
  check(a, row.physical_squared_contrast);
  check(mean, row.conditional_mean_relative_full_collision);
  check(sub(mean, one), row.joint_source_chi_squared_to_uniform_output);
  check(prefix(n), row.two_public_prefix_invertibility_probability);
  const leading = div(mul(add(R(2), pow(a, 2)), add(R(2), a)), R(8));
  check(leading, row.nonzero_pair_leading_base_per_logical_qubit);
  assert.equal(lt(leading, one), row.exponential_uniformization_regime);
  check(div(mul(add(one, pow(a, 2)), add(one, a)), R(4)), row.single_member_leading_base_per_logical_qubit);
  check(add(pow(sub(one, e), 3 * n), div(sub(one, pow(sub(one, e), n)), N)),
    row.single_packet_known_correct_residue_all_zero_mean_acceptance);
  check(div(one, N), row.single_packet_wrong_committed_residue_high_source_mean_acceptance);
  assert.equal(row.regev_basis_contamination_promise_covered, false);
  return sub(mean, one);
};
for (const row of physical.physical_noise_scaling) {
  const d = source(row.source), n = row.source.dimension, Q = BigInt(row.modulus / 2);
  const rho = R(2n ** BigInt(n), Q ** BigInt(n));
  check(rho, row.full_prior_order_at_most_two_exception_mass);
  const kl = mul(mul(R(row.supplied_pair_attempts), prefix(n)),
    add(mul(sub(one, rho), mul(R(2), d)), mul(rho, R(2 * n))));
  check(kl, row.transcript_kl_to_secret_independent_reference_bits_upper_bound);
  const gap = sub(R(1, 100), R(2n, Q ** BigInt(n)));
  assert.equal(lt(R(0), gap) && lt(div(kl, R(2)), pow(gap, 2)), row.orbit_success_below_one_over_100);
  assert.equal(row.original_phase_states_consumed, 6 * n * row.supplied_pair_attempts);
}
physical.vanishing_noise_controls.forEach(source);
const cancel = physical.correlated_cancellation_countercontrol;
for (let h = 0; h < 4; h++) {
  let phi = R(0);
  for (const entry of cancel.explicit_joint_physical_mask_law) {
    const e1 = Number(BigInt(entry.left_mask_hex)), e2 = Number(BigInt(entry.right_mask_hex));
    const eta = [e1, e2].reduce((value, e) => value ^ [3, 1, 2].reduce((s, r, i) => s ^ ((e >> i & 1) ? r : 0), 0), 0);
    phi = add(phi, mul(read(entry.probability), R(parity(eta & h) ? -1 : 1)));
  }
  assert.deepEqual(phi, one);
}
assert.equal(cancel.correlated_certificate.physical_mask_bits_independent, false);

// Direct 2x2 density commutators and X twirling, with exact rational entries.
const density = (p, g, bad) => {
  const base = div(sub(one, g), R(2)), off = mul(base, R(p ? -1 : 1));
  return [[add(base, bad === 0 ? g : R(0)), off], [off, add(base, bad === 1 ? g : R(0))]];
};
const mm = (a, b) => [0, 1].map(i => [0, 1].map(j => add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))));
for (const row of completion.basis_contamination_commutators) {
  const g = read(row.basis_contamination_probability), bad = row.bad_basis_bit;
  const a = density(0, g, bad), b = density(1, g, bad), ab = mm(a, b), ba = mm(b, a);
  let norm = R(0);
  for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) norm = add(norm, pow(sub(ab[i][j], ba[i][j]), 2));
  check(norm, row.commutator_frobenius_squared);
  assert.deepEqual(norm, mul(R(2), mul(pow(g, 2), pow(sub(one, g), 2))));
  check(div(g, R(2)), row.X_twirl_is_legal_degradation_to_flip_rate);
  assert.deepEqual(div(add(a[0][0], a[1][1]), R(2)), half);
  assert.deepEqual(div(add(a[0][1], a[1][0]), R(2)), div(sub(one, g), R(2)));
}
for (const row of completion.known_public_basis_bias_filters) {
  const g = read(row.basis_contamination_probability), a2 = div(sub(one, g), add(one, g));
  check(a2, row.attenuation_squared);
  check(sub(one, g), row.success_probability);
  check(div(one, sub(one, g)), row.expected_native_inputs_per_output);
  // Forward equalizes diagonals; reverse off-diagonal identity holds with positive roots.
  assert.deepEqual(mul(a2, div(add(one, g), R(2))), div(sub(one, g), R(2)));
  assert.deepEqual(mul(a2, sub(one, pow(g, 2))), pow(sub(one, g), 2));
  assert.equal(row.one_copy_lossless_equivalence_claim, false);
  assert.equal(row.physical_filter_backend_or_precision_verified, false);
}
for (const row of [...completion.low_noise_completion_scaling, completion.constant_noise_completion_control]) {
  const n = row.dimension, M = row.fresh_original_phase_states_per_trial, e = read(row.effective_parity_flip_probability);
  const f = R((1n << BigInt(n)) - 1n, 1n << BigInt(M)), clean = pow(sub(one, e), M);
  check(f, row.random_binary_rank_failure_upper_bound);
  check(clean, row.iid_label_independent_clean_block_probability);
  check(mul(clean, sub(one, f)), row.iid_clean_block_correct_completion_success_lower_bound);
  const marginalBound = sub(sub(one, mul(R(M), e)), f);
  check(lt(marginalBound, R(0)) ? R(0) : marginalBound, row.marginal_flip_bound_only_correct_completion_success_lower_bound);
  assert.equal(row.requires_known_correct_lower_residue, true);
}
const verifier = completion.robust_full_candidate_verifier;
const tail = (M, p, lo, hi) => {
  let combination = 1n, numerator = 0n;
  for (let j = 0; j <= M; j++) {
    if (j >= lo && j <= hi) numerator += combination * p[0] ** BigInt(j) * (p[1] - p[0]) ** BigInt(M - j);
    combination = combination * BigInt(M - j) / BigInt(j + 1);
  }
  return R(numerator, p[1] ** BigInt(M));
};
const gamma = read(verifier.per_trial_conditional_arbitrary_bad_probability_bound), M = verifier.fresh_original_phase_states_consumed;
const threshold = Math.ceil(3 * M / 4);
assert.equal(threshold, verifier.projection_zero_votes_required);
check(tail(M, add(half, gamma), threshold, M), verifier.false_acceptance_probability_upper_bound);
check(tail(M, sub(one, gamma), 0, threshold - 1), verifier.false_rejection_probability_upper_bound);
assert.equal(verifier.conditional_source_promise_programmatically_verified, false);
for (const row of completion.noise_transfer_gates) {
  const passes = row.model === 'iid_physical_Z' ||
    (row.model === 'classical_correlated_Z' && row.requested_capability === 'lossless_binary_classicalization');
  assert.equal(row.transfer_obligations_satisfied_as_declared, passes);
  assert.equal(row.declarations_programmatically_proven, false);
  assert.equal(row.issues.length === 0, passes);
}

const unionMean = (n, left, right) => {
  const k = 2 * n, N = 1n << BigInt(k), pivots = (1n << BigInt(n)) - 1n;
  const bigWt = value => { let count = 0; while (value) { value &= value - 1n; count++; } return count; };
  const b = bigWt(left & pivots) + bigWt(right & pivots);
  const d = k - bigWt((left | right) >> BigInt(n));
  const singles = (1n << BigInt(d)) - 1n;
  const pairs = (1n << BigInt(k - d)) * 3n ** BigInt(d) - N - (1n << BigInt(d)) + 1n;
  return div(add(add(R(N), R(singles, 1n << BigInt(b))),
    mul(R(pairs, 1n << BigInt(b)), pow(R(3, 4), 2 * n - b))), R(N));
};
// Independent complete source enumeration for EVERY n=1 union fault mask.
for (let left = 0; left < 8; left++) for (let right = 0; right < 8; right++) {
  let count = 0;
  for (let x = 0; x < 4; x++) for (let y = 0; y < 4; y++)
    for (let h = 0; h < 4; h++) for (let j = 0; j < 4; j++) {
      const images = [bits([x, 1, 2], h), bits([y, 1, 2], h)];
      if (!(images[0] & left || images[1] & right || images[0] & bits([x, 1, 2], j) || images[1] & bits([y, 1, 2], j))) count++;
    }
  assert.deepEqual(R(count, 64), unionMean(1, BigInt(left), BigInt(right)));
}
for (const row of [...gauged.complete_low_source_controls, ...gauged.correlated_all_or_none_scaling]) {
  let mean = R(0);
  for (const left of row.joint_prelabel_fault_law) for (const right of row.joint_prelabel_fault_law) {
    const union = unionMean(row.dimension, BigInt(left.left_mask_hex) | BigInt(right.left_mask_hex),
      BigInt(left.right_mask_hex) | BigInt(right.right_mask_hex));
    mean = add(mean, mul(mul(read(left.probability), read(right.probability)), union));
  }
  check(mean, row.conditional_mean_relative_full_collision);
  check(sub(mean, one), row.joint_source_chi_squared_to_uniform_output);
  check(prefix(row.dimension), row.two_public_prefix_invertibility_probability);
  assert.equal(row.logical_mask_enumeration_required, false);
  if (row.correlated_source_excess_is_clean_excess_times) {
    const clean = unionMean(row.dimension, 0n, 0n);
    check(div(sub(mean, one), sub(clean, one)), row.correlated_source_excess_is_clean_excess_times);
    assert.equal(row.does_not_prove_actual_reduction_supplies_correlated_faults, true);
  } else check(mean, row.direct_selected_row_rank_source_mean);
}
let gaugeIdentities = 0;
for (let secret = 0; secret < 8; secret++) for (let label = 0; label < 8; label++)
  for (let flip = 0; flip < 2; flip++) for (let x = 0; x < 2; x++) for (let y = 0; y < 2; y++) {
    const old = flip ? (8 - label) % 8 : label;
    const modulo = value => (value % 8 + 8) % 8;
    assert.equal(modulo(secret * old * ((x ^ flip) - (y ^ flip))), modulo(secret * label * (x - y)));
    gaugeIdentities++;
  }
assert.equal(gaugeIdentities, gauged.gauge_algebra.exact_good_density_phase_identities_checked);
assert.deepEqual(gauged.gauge_algebra.fixed_prelabel_bad_bit_conditional_counts, [1, 1]);
const adaptiveCounts = [0, 0];
for (let flip = 0; flip < 2; flip++) adaptiveCounts[Number((flip ? 7 : 1) >= 4) ^ flip]++;
assert.deepEqual(adaptiveCounts, gauged.gauge_algebra.counterexample_conditional_counts);
for (const row of gauged.two_point_completion_scaling) {
  const n = row.dimension, q = row.modulus, g = R(1n, BigInt(n * Math.log2(q)) ** BigInt(row.failure_parameter));
  check(g, row.definition_3_1_basis_failure_bound);
  check(div(g, R(2)), row.gauged_each_original_phase_flip_marginal_bound);
  assert.equal(row.two_point_coordinate_range_M, q / 2);
  const c = row.known_correct_residue_completion, M = c.fresh_original_phase_states_per_trial;
  const f = R((1n << BigInt(n)) - 1n, 1n << BigInt(M));
  check(sub(sub(one, mul(R(M), div(g, R(2)))), f), c.marginal_flip_bound_only_correct_completion_success_lower_bound);
  assert.equal(row.natural_lattice_M_and_total_state_supply_parameter_map_verified, false);
  assert.equal(row.fault_independence_or_conditional_history_budget_inferred, false);
}
gauged.source_transfer_gates.forEach((row, i) => {
  assert.equal(row.transfer_obligations_satisfied_as_declared, i < 2);
  assert.equal(row.iid_physical_phase_formula_usable_as_declared, i === 1);
  assert.equal(row.declarations_programmatically_proven, false);
});
let hashes = 0;
for (const report of [physical, completion, gauged]) {
  assert.equal(report.claim_gate.speedup_claim_allowed, false);
  for (const [file, expected] of Object.entries(report.dependency_sha256)) {
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
    hashes++;
  }
}
assert.equal(hashes, 13);
console.log(JSON.stringify({status: 'BOUNDED_SOURCE_ARITHMETIC_CROSSCHECK_ONLY',
  physical_joint_masks: 64, complete_higher_source_tables: 256, full_source_error_masks: 16,
  weighted_systematic_low_tables: 4 * 16, single_packet_source_masks: 4 * 32,
  physical_scaling_rows: physical.physical_noise_scaling.length,
  vanishing_noise_rows: physical.vanishing_noise_controls.length,
  correlated_cancellation_fourier_checks: 4,
  density_controls: completion.basis_contamination_commutators.length,
  public_bias_filter_controls: completion.known_public_basis_bias_filters.length,
  classical_completion_bounds: completion.low_noise_completion_scaling.length + 1,
  exact_binomial_envelopes: 2, promise_gates: completion.noise_transfer_gates.length,
  prelabel_gauge_good_density_identities: gaugeIdentities,
  complete_union_fault_source_enumerations: 64,
  gauged_joint_fault_source_controls: gauged.complete_low_source_controls.length,
  correlated_fault_scaling_rows: gauged.correlated_all_or_none_scaling.length,
  two_point_completion_ledgers: gauged.two_point_completion_scaling.length,
  prelabel_source_transfer_gates: gauged.source_transfer_gates.length, dependency_hashes: hashes}));

// Independent bounded arithmetic crosscheck, not independent theorem review.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_dense_phase_transport.json'), 'utf8'));
const gcd = (a, b) => { while (b) [a, b] = [b, a % b]; return a < 0n ? -a : a; };
const f = (a, b = 1n) => { a = BigInt(a); b = BigInt(b); assert(b > 0n); const g = gcd(a, b); return [a / g, b / g]; };
const read = x => f(BigInt(x.sign) * BigInt(x.numerator_hex), BigInt(x.denominator_hex));
const add = (a, b) => f(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const sub = (a, b) => f(a[0] * b[1] - b[0] * a[1], a[1] * b[1]);
const mul = (a, b) => f(a[0] * b[0], a[1] * b[1]);
const div = (a, b) => f(a[0] * b[1], a[1] * b[0]);
const power = (a, n) => f(a[0] ** BigInt(n), a[1] ** BigInt(n));
const le = (a, b) => a[0] * b[1] <= b[0] * a[1];
const min = (a, b) => le(a, b) ? a : b;
const max = (a, b) => le(a, b) ? b : a;
const eq = (declared, value) => assert.deepEqual(read(declared), value);
const zero = f(0), one = f(1);
const mod = (a, q) => (a % q + q) % q;
const vector = (t, n, q) => Array.from({length: n}, (_, i) => Math.floor(t / q ** i) % q);
const index = (t, q) => t.reduce((s, x, i) => s + x * q ** i, 0);
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const assignment = (A, z) => {
  const n = A.length, m = A[0].length;
  for (let l = 0; l < n; l++) for (let i = 0; i < n; i++) assert.equal(A[l][i] % 2, Number(l === i));
  const free = Array.from({length: m - n}, (_, j) => z >> j & 1);
  return [...A.map(row => row.slice(n).reduce((s, x, j) => s ^ (x % 2 & free[j]), 0)), ...free];
};
const residue = (A, z, Q = 4) => {
  const x = assignment(A, z);
  return A.map(row => { const v = dot(row, x); assert.equal(v % 2, 0); return mod(v / 2, Q); });
};
let sourceTables = 0, qftSecrets = 0, challengeTrials = 0;
for (const row of report.complete_native_residue_sources) {
  const B = row.low_labels, n = B.length, m = B[0].length, N = 2 ** (m - n), G = 4 ** n;
  const tables = 4 ** (n * m);
  let total = 0n;
  for (let code = 0; code < tables; code++) {
    const A = B.map((r, l) => r.map((b, i) => b + 2 * (Math.floor(code / 4 ** (l * m + i)) % 4)));
    const counts = Array(G).fill(0);
    for (let z = 0; z < N; z++) counts[index(residue(A, z), 4)]++;
    total += BigInt(G * counts.reduce((s, c) => s + c * c, 0) - N * N);
  }
  assert.equal(tables, row.all_higher_source_tables);
  eq(row.exact_mean_residue_chi_squared, f(total, BigInt(tables * N * N)));
  eq(row.exact_mean_residue_chi_squared, f(G - 1, N));
  sourceTables += tables;
}
for (const row of report.physical_and_classical_transport_controls) {
  const A = row.labels, n = A.length, N = row.permutation.length, G = 4 ** n, J = N / G, P = row.permutation;
  assert.deepEqual([...P].sort((a, b) => a - b), Array.from({length: N}, (_, z) => z));
  const F = Array.from({length: N}, (_, z) => residue(A, z));
  const offsets = Array.from({length: J}, (_, j) => Array.from({length: G}, (_, t) =>
    F[P[t + G * j]].map((x, l) => mod(x - vector(t, n, 4)[l], 4))));
  let collision = 0;
  for (const bucket of offsets) {
    const counts = new Map();
    for (const d of bucket) { const key = d.join(','); counts.set(key, (counts.get(key) || 0) + 1); }
    for (const c of counts.values()) collision += c * c;
  }
  const success = f(collision, N * G);
  let qftTotal = 0, phasedTotal = 0, witnesses = 0;
  const perSecret = [];
  for (let s = 0; s < G; s++) {
    let numerator = 0;
    for (let j = 0; j < J; j++) {
      const roots = Array(4).fill(0), phased = Array(4).fill(0);
      for (let t = 0; t < G; t++) {
        const exponent = mod(dot(vector(s, n, 4), offsets[j][t]), 4), z = t + G * j;
        roots[exponent]++;
        phased[mod(exponent + 3 * z + (z >> 1), 4)]++;
      }
      const norm = r => (r[0] - r[2]) ** 2 + (r[1] - r[3]) ** 2;
      numerator += norm(roots); phasedTotal += norm(phased);
    }
    qftTotal += numerator; perSecret.push(f(numerator, N * G)); qftSecrets++;
  }
  for (let j = 0; j < J; j++) for (let t0 = 0; t0 < G; t0++) for (let target = 0; target < G; target++) {
    const challenge = vector(target, n, 4), d = offsets[j][t0];
    const u = index(challenge.map((x, l) => mod(x - d[l], 4)), 4), logical = P[u + G * j];
    if (index(F[logical], 4) === target) {
      witnesses++;
      const physical = assignment(A, logical);
      A.forEach((component, l) => assert.equal(mod(dot(component, physical), 8), 2 * challenge[l]));
    }
    challengeTrials++;
  }
  eq(row.mean_QFT_success, f(qftTotal, N * G * G));
  assert.deepEqual(f(qftTotal, N * G * G), success);
  eq(row.independent_challenge_witness_success, f(witnesses, N * G));
  assert.deepEqual(f(witnesses, N * G), success);
  eq(row.public_monomial_phase_mean_success, f(phasedTotal, N * G * G));
  assert(le(f(phasedTotal, N * G * G), success));
  eq(row.two_call_certificate.uniform_secret_mean_QFT_decoder_success, success);
  eq(row.two_call_certificate.independent_uniform_target_witness_success, success);
  assert.equal(row.two_call_certificate.forward_transport_evaluator_calls_per_classical_trial, 2);
  assert.equal(row.two_call_certificate.whole_DCP_input_experiment_classically_simulated, false);
  if (row.calibration) {
    const counts = Array(G).fill(0); F.forEach(t => counts[index(t, 4)]++);
    const tv = f(counts.reduce((sum, c) => sum + Math.abs(c - J), 0), 2 * N);
    eq(row.calibration.residue_total_variation_to_uniform, tv);
    const matched = P.reduce((sum, x, z) => sum + Number(index(F[x], 4) === z % G), 0);
    eq(row.calibration.exact_residue_matched_fraction, f(matched, N));
    assert.deepEqual(f(matched, N), sub(one, tv));
    const lower = power(max(zero, sub(one, mul(f(2), tv))), 2);
    eq(row.calibration.pointwise_secret_success_lower_bound, lower);
    perSecret.forEach(p => assert(le(lower, p)));
    assert.equal(row.calibration.efficient_decoder, false);
  }
}
const prefix = n => { let p = one; for (let j = 1; j <= n; j++) p = mul(p, sub(one, f(1, 1n << BigInt(j)))); return p; };
for (const row of report.sparse_sign_scaling) {
  const n = row.dimension, k = row.logical_width;
  const direct = mul(f(1, 1n << BigInt(n)), power(add(one, f(1, 1n << BigInt(k))), n));
  const extra = min(one, mul(f(1n << BigInt(2 * k)), power(f(4, row.modulus), n)));
  const total = min(one, add(direct, extra));
  eq(row.conditional_full_code_direct_sign_correction_mean, direct);
  eq(row.additional_full_label_transport_source_union_bound, extra);
  eq(row.source_average_exact_reference_transport_success_upper_bound, total);
  eq(row.supplied_attempt_success_upper_bound, min(one, mul(f(n * n), mul(prefix(n), total))));
  assert.equal(row.prefix_failures_aborted_and_original_states_charged, true);
  assert.equal(row.partial_images_approximate_transport_or_branch_mixing_unitaries_covered, false);
}
for (const row of report.dense_transport_scaling) {
  const g = row.dimension * (Math.log2(row.modulus) - 1), k = g + row.density_overhead_bits;
  assert.equal(row.residue_entropy_bits, g); assert.equal(row.logical_width, k);
  eq(row.exact_high_source_mean_residue_chi_squared_to_uniform, f((1n << BigInt(g)) - 1n, 1n << BigInt(k)));
  eq(row.rational_ideal_mean_residue_success_lower_bound, power(sub(one, f(1, 1n << BigInt(row.density_overhead_bits / 2))), 2));
  eq(row.single_native_prefix_acceptance, prefix(row.dimension));
  assert.equal(row.efficient_canonical_transport_implemented, false);
}
const binomial = (n, k) => { let c = 1n; for (let j = 1; j <= k; j++) c = c * BigInt(n + 1 - j) / BigInt(j); return c; };
function checkFaultBound(row, logq = Math.log2(row.modulus)) {
  const n = row.dimension, R = row.attempts, M = row.verification_states_per_attempt, delta = row.density_overhead_bits;
  const lambda = row.completion_states_per_attempt - n, block = n * logq + delta + n + lambda + M;
  const gamma = f(1, n * logq), mean = mul(f(block), gamma), cmean = mul(f(row.markov_multiplier), mean);
  const K = Number((cmean[0] + cmean[1] - 1n) / cmean[1]);
  const a = mul(f(9, 32), mul(power(sub(one, f(1, 1n << BigInt(delta / 2))), 2), sub(one, f(1, 1n << BigInt(lambda)))));
  const rate = mul(a, f(1, 1n << BigInt(K)));
  const noCandidate = add(f(1, row.markov_multiplier), div(one, add(one, mul(f(R), rate))));
  let numerator = 0n;
  for (let j = Math.ceil(3 * M / 4); j <= M; j++) numerator += binomial(M, j);
  const tail = f(numerator, 1n << BigInt(M)), failure = min(one, add(noCandidate, mul(f(R), tail)));
  eq(row.two_point_definition_3_1_basis_failure_marginal_bound, gamma);
  eq(row.mean_basis_fault_count_per_block_upper_bound, mean);
  eq(row.clean_ideal_attempt_full_candidate_success_lower_bound, a);
  eq(row.effective_conditional_attempt_rate_on_mean_fault_event, rate);
  eq(row.no_correct_accepted_candidate_probability_upper_bound, noCandidate);
  eq(row.wrong_candidate_exact_verification_tail, tail);
  eq(row.total_failure_probability_upper_bound, failure);
  eq(row.remaining_total_probability_perturbation_margin_to_one_third, max(zero, sub(f(1, 3), failure)));
  assert.equal(row.mean_fault_event_ceiling, K);
  assert.equal(row.original_states_per_allocated_attempt_block, block);
  assert.equal(row.total_original_states_charged, R * block);
  assert.equal(row.bounded_error_below_one_third_as_declared, !le(f(1, 3), failure));
  assert.equal(row.arbitrary_entangled_basis_corruption_or_joint_Z_error_laws_covered, false);
  assert.equal(row.candidate_record_accepted, false);
}
report.correlated_basis_fault_reduction_controls.forEach(row => checkFaultBound(row));
for (const row of report.natural_lattice_parameter_controls) {
  const n = row.dimension;
  assert.equal(row.lattice_source_M_binary_exponent, 4 * n);
  assert.equal(row.coordinate_QFT_modulus_binary_exponent, 4 * n + 1);
  assert.equal(row.residue_entropy_bits, 4 * n * n);
  assert.equal(row.dense_packet_original_states, 4 * n * n + n + 16);
  eq(row.basis_failure_marginal_budget, f(1, n * (4 * n + 1)));
  checkFaultBound(row.conditional_full_decoder_bound, 4 * n + 1);
  assert.equal(row.actual_lattice_state_supply_and_total_precision_composition_verified, false);
}
let jensenChecks = 0;
for (let code = 0; code < 625; code++) {
  const faults = vector(code, 4, 5), ceiling = Math.ceil(faults.reduce((s, x) => s + x, 0) / 4), a = f(9, 32);
  let actual = one;
  faults.forEach(x => { actual = mul(actual, sub(one, mul(a, f(1, 1n << BigInt(x))))); });
  const p = mul(a, f(1, 1n << BigInt(ceiling))), jensen = power(sub(one, p), 4);
  assert(le(actual, jensen)); assert(le(jensen, div(one, add(one, mul(f(4), p))))); jensenChecks++;
}
const faultControl = report.conditional_fault_amplification_controls;
assert.equal(faultControl.conditional_clean_component_Jensen_controls, jensenChecks);
eq(faultControl.independent_fair_errors_no_clean_attempt_probability, f(1, 16));
eq(faultControl.one_shared_fair_error_coin_no_clean_attempt_probability, f(1, 2));
assert.equal(faultControl.counterexample_is_about_clean_component_amplification_not_decoder_failure, true);
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
assert.equal(report.claim_gate.candidate_record_accepted, false);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW', native_higher_source_tables: sourceTables,
  exact_QFT_secret_controls: qftSecrets, independent_challenge_trials: challengeTrials,
  sparse_scaling_rows: report.sparse_sign_scaling.length, dense_scaling_rows: report.dense_transport_scaling.length,
  correlated_fault_bound_rows: report.correlated_basis_fault_reduction_controls.length,
  exponential_modulus_lattice_ledgers: report.natural_lattice_parameter_controls.length,
  Jensen_controls: jensenChecks, dependency_hashes: Object.keys(report.dependency_sha256).length}));

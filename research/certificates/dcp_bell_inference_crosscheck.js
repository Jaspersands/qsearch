// Independent physical character/root counts; not independent theorem review.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root,
  'research/phase_workbench/dcp_bell_inference_kernel.json'), 'utf8'));
const mod = (a, q) => (a % q + q) % q;
const parity = x => { let p = 0; while (x) { p ^= x & 1; x >>= 1; } return p; };
const popcount = x => { let p = 0; while (x) { p += x & 1; x >>= 1; } return p; };
const gcd = (a, b) => { a = a < 0n ? -a : a; while (b) [a, b] = [b, a % b]; return a; };
const rational = (a, b = 1n) => {
  a = BigInt(a); b = BigInt(b); assert(b > 0n);
  if (a === 0n) return [0n, 1n];
  const abs = a < 0n ? -a : a;
  const divisor = (b & (b - 1n)) === 0n ? ((abs & -abs) < b ? abs & -abs : b) : gcd(a, b);
  return [a / divisor, b / divisor];
};
const add = (a, b) => rational(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const neg = a => [-a[0], a[1]];
const mul = (a, b) => rational(a[0] * b[0], a[1] * b[1]);
const divide = (a, b) => rational(a[0] * b[1], a[1] * b[0]);
const power = e => 1n << BigInt(e);
const less = (a, b) => a[0] * b[1] < b[0] * a[1];
const min = (a, b) => less(a, b) ? a : b;
const pow = (a, exponent) => {
  let result = rational(1);
  while (exponent) {
    if (exponent & 1) result = mul(result, a);
    a = mul(a, a); exponent = Math.floor(exponent / 2);
  }
  return result;
};
const read = value => rational(BigInt(value.sign) * BigInt(value.numerator_hex), BigInt(value.denominator_hex));
const check = (actual, value) => assert.deepEqual(actual, read(value));
const compile = (A, syndrome) => {
  const matrix = A.map(r => r.map(x => x & 1)), pivots = [];
  let rank = 0;
  for (let j = 0; j < A[0].length; j++) {
    const index = matrix.findIndex((r, i) => i >= rank && r[j]);
    if (index < 0) continue;
    [matrix[index], matrix[rank]] = [matrix[rank], matrix[index]];
    for (let i = 0; i < matrix.length; i++) if (i !== rank && matrix[i][j])
      matrix[i] = matrix[i].map((x, k) => x ^ matrix[rank][k]);
    pivots.push(j); rank++;
  }
  const free = Array.from({length: A[0].length}, (_, i) => i).filter(i => !pivots.includes(i));
  const rows = Array(A[0].length).fill(0), origin = Array(A[0].length).fill(0);
  free.forEach((f, j) => { rows[f] = 2 ** j; });
  pivots.forEach((p, i) => {
    origin[p] = syndrome >> i & 1;
    rows[p] = free.reduce((value, f, j) => value + matrix[i][f] * 2 ** j, 0);
  });
  return {A, rows, origin, k: free.length};
};
const assignment = (packet, z) => packet.rows.map((row, i) => packet.origin[i] ^ parity(row & z));
const phase = (packet, z, secret) => {
  const x = assignment(packet, z);
  return packet.A.reduce((total, row, l) => {
    const delta = row.reduce((sum, a, i) => sum + a * (x[i] - packet.origin[i]), 0);
    assert.equal(mod(delta, 2), 0);
    return total + secret[l] * delta / 2;
  }, 0);
};

// Formal cyclic character sums reduced modulo x^(Q/2)+1, no floating roots.
const characterCache = new Map();
const character = (Q, coefficient) => {
  coefficient = mod(coefficient, Q);
  const key = Q + ':' + coefficient;
  if (!characterCache.has(key)) {
    const counts = Array(Q / 2).fill(0);
    for (let z = 0; z < Q; z++) {
      const exponent = coefficient * z % Q;
      counts[exponent % (Q / 2)] += exponent < Q / 2 ? 1 : -1;
    }
    assert(counts.slice(1).every(x => x === 0));
    characterCache.set(key, counts[0] / Q);
  }
  return characterCache.get(key);
};
const control = report.character_kernels;
const packets = [compile(control.low_left, control.initial_syndrome), compile(control.low_right, control.initial_syndrome)];
let testedCharacterTerms = 0;
for (const record of control.records) {
  const Q = record.modulus / 2, N = 2 ** packets[0].k, s = record.secret_s, t = record.secret_t;
  let total = 0, survivors = 0;
  for (let a = 0; a < N; a++) for (let b = 0; b < N; b++)
    for (let c = 0; c < N; c++) for (let d = 0; d < N; d++) {
      if (a ^ b ^ c ^ d) continue;
      let coefficient = 1, angle = 0;
      packets.forEach((packet, side) => {
        const offset = side ? record.xor_outcome : 0;
        const x = [a, b, c, d].map(z => assignment(packet, z ^ offset));
        packet.rows.forEach((_, i) => s.forEach((value, l) => {
          coefficient *= character(Q, value * (x[0][i] - x[1][i]) + t[l] * (x[2][i] - x[3][i]));
        }));
        angle += phase(packet, a ^ offset, s) - phase(packet, b ^ offset, s)
          + phase(packet, c ^ offset, t) - phase(packet, d ^ offset, t);
      });
      if (coefficient) {
        angle = mod(angle, Q);
        assert(angle === 0 || angle === Q / 2);
        total += angle === 0 ? 1 : -1;
        survivors++;
      }
      testedCharacterTerms++;
    }
  check(rational(total, N * N), record.mean_relative_cross_collision);
  assert.equal(survivors, record.surviving_source_character_terms);
}

const raw = (pair, secret, u) => Array.from({length: 2}, (_, v) => {
  const roots = [0, 0, 0, 0];
  for (let z = 0; z < 2; z++) roots[mod(phase(pair[0], z, [secret])
    + phase(pair[1], z ^ u, [secret]) + 2 * parity(v & z), 4)]++;
  return (roots[0] - roots[2]) ** 2 + (roots[1] - roots[3]) ** 2;
});
const noisyTotals = Array.from({length: 4}, () => Array(4).fill(0n));
for (let code = 0; code < 256; code++) {
  const high = Array.from({length: 4}, (_, i) => Math.floor(code / 4 ** i) % 4);
  const pair = [0, 1].map(side => compile([[1 + 2 * high[2 * side], 1 + 2 * high[2 * side + 1]]], side));
  const observed = Array.from({length: 4}, (_, secret) => {
    const p = raw(pair, secret, 1);
    assert.equal(p[0] + p[1], 4);
    return p.map((a, v) => 7 * a + p[v ^ 1]);
  });
  for (let s = 0; s < 4; s++) for (let t = 0; t < 4; t++)
    noisyTotals[s][t] += BigInt(2 * (observed[s][0] * observed[t][0] + observed[s][1] * observed[t][1]));
}
for (const row of report.complete_noisy_physical_source.records)
  check(rational(noisyTotals[row.secret_s[0]][row.secret_t[0]], 1024 * 256), row.mean_relative_cross_collision);

const physical = (rows, z) => rows.reduce((x, row, i) => x + parity(row & z) * 2 ** i, 0);
let weightedTotal = rational(0);
for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) {
  for (let h = 0; h < 4; h++) for (let j = 0; j < 4; j++)
    if (!([a, b].some(p => physical([p, 1, 2], h) & physical([p, 1, 2], j))))
      weightedTotal = add(weightedTotal, divide(pow(rational(9, 16), popcount(h)), rational(64)));
}
check(weightedTotal, report.weighted_systematic_source.weighted_mean_relative_collision);
const prefixProbability = n => {
  let numerator = 1n;
  for (let j = 1; j <= n; j++) numerator *= power(j) - 1n;
  return rational(numerator * numerator, power(n * (n + 1)));
};
const sourceMean = (n, epsilon) => {
  const k = 2 * n, N = rational(power(k)), t = pow(add(rational(1), neg(mul(rational(2), epsilon))), 2);
  const zero = add(add(N, pow(add(rational(1), t), k)), rational(-1));
  const others = add(pow(add(rational(2), t), k), neg(zero));
  const mean = divide(add(zero, mul(others, pow(rational(3, 4), k))), N);
  return {t, mean, d: add(mean, rational(-1)), prefix: prefixProbability(n)};
};
for (const row of report.sq_scaling) {
  const n = row.dimension, Q = BigInt(row.modulus / 2), tau = read(row.absolute_expectation_tolerance);
  const M = (Q ** BigInt(n) - (Q / 2n) ** BigInt(n)) / 2n;
  const d = sourceMean(n, rational(0)).d;
  const ratio = divide(d, mul(tau, tau));
  const count = ratio[0] / ratio[1] < M ? ratio[0] / ratio[1] : M;
  assert.equal(BigInt(row.odd_secret_negation_orbits_hex), M);
  assert.equal(BigInt(row.max_orbits_distinguished_from_reference_per_query_hex), count);
  check(d, row.common_centered_likelihood_squared_norm);
  check(prefixProbability(n), row.two_public_prefix_invertibility_probability);
  assert.equal(row.source_rejection_not_free_and_sq_oracle_not_a_sample_factory, true);
  check(min(rational(1), rational(BigInt(row.statistical_queries) * count + 1n, M)),
    row.adversarial_valid_sq_oracle_uniform_orbit_success_upper_bound);
  assert.equal(row.raw_sample_algorithms_covered, false);
  assert.equal(row.classical_hardness_or_quantum_speedup_claim, false);
}
for (const row of report.readout_noise_scaling) {
  const n = row.dimension, Q = BigInt(row.modulus / 2), G = Q ** BigInt(n);
  const data = sourceMean(n, read(row.source.output_bit_flip_probability));
  const rho = rational(2n ** BigInt(n), G);
  check(data.mean, row.source.conditional_mean_relative_full_collision);
  check(data.d, row.source.joint_source_likelihood_chi_squared_to_uniform_reference);
  check(data.prefix, row.source.two_public_prefix_invertibility_probability);
  check(rho, row.uniform_prior_order_at_most_two_exception_mass);
  const kl = mul(mul(rational(row.supplied_pair_attempts), data.prefix),
    add(mul(add(rational(1), neg(rho)), mul(rational(2), data.d)), mul(rho, rational(2 * n))));
  check(kl, row.transcript_kl_to_secret_independent_reference_bits_upper_bound);
  check(min(rational(n * Math.log2(Number(Q))), kl), row.uniform_packet_residue_mutual_information_bits_upper_bound);
  const gap = add(rational(1, 100), rational(-2n, G));
  assert.equal(less(rational(0), gap) && less(divide(kl, rational(2)), mul(gap, gap)), row.orbit_success_below_one_over_100);
  assert.equal(row.original_phase_states_consumed, 6 * n * row.supplied_pair_attempts);
  assert.equal(row.adaptive_label_matching_covered, false);
  assert.equal(row.source.correlated_native_phase_errors_covered, false);
}
const repair = report.detector_repetition_countercontrol;
let effective = rational(0), binomial = 1n;
const R = repair.repetitions_per_logical_bit, epsilon = read(repair.detector_flip_probability);
for (let j = 0; j <= R; j++) {
  if (j > Math.floor(R / 2)) effective = add(effective, mul(rational(binomial),
    mul(pow(epsilon, j), pow(add(rational(1), neg(epsilon)), R - j))));
  binomial = binomial * BigInt(R - j) / BigInt(j + 1);
}
check(effective, repair.majority_vote_effective_flip_probability);
assert.equal(repair.remains_in_uniformization_regime, false);
assert.equal(repair.repairs_pre_hadamard_phase_errors, false);
const alias = report.fixed_chart_order_two_alias;
let aliasChecks = 0;
for (let seed = 0; seed < 4; seed++) {
  const pair = [alias.low_left, alias.low_right].map((A, side) => compile(
    A.map((row, l) => row.map((b, i) => b + 2 * ((seed + 3 * side + l + i) % 4))), side));
  for (const secret of [alias.secret_s, alias.secret_t]) for (let u = 0; u < 4; u++) {
    for (let v = 0; v < 4; v++) {
      const roots = [0, 0, 0, 0];
      for (let z = 0; z < 4; z++) roots[mod(phase(pair[0], z, secret) + phase(pair[1], z ^ u, secret)
        + 2 * parity(v & z), 4)]++;
      assert.equal((roots[0] - roots[2]) ** 2 + (roots[1] - roots[3]) ** 2, 4);
    }
    aliasChecks++;
  }
}
assert.equal(aliasChecks, alias.bounded_physical_full_law_checks);
assert.equal(alias.not_same_negation_orbit, true);
check(rational(0), alias.both_centered_likelihood_squared_norms);
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
assert.equal(report.claim_gate.l2_geometry_proves_polynomial_sample_learning, false);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
console.log(JSON.stringify({status: 'BOUNDED_SOURCE_ARITHMETIC_CROSSCHECK_ONLY',
  exact_candidate_secret_kernels: control.records.length,
  physical_cyclic_character_terms: testedCharacterTerms,
  complete_noisy_physical_source_tables: 256, weighted_systematic_pair_tables: 16,
  sq_scaling_rows: report.sq_scaling.length, full_noisy_transcript_rows: report.readout_noise_scaling.length,
  detector_only_repetition_countercontrols: 1,
  fixed_chart_order_two_alias_full_law_checks: aliasChecks,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));

// Independent bounded arithmetic crosscheck, not independent theorem review.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root,
  'research/phase_workbench/dcp_correlated_bell.json'), 'utf8'));
const mod = (a, q) => (a % q + q) % q;
const parity = a => {
  let value = 0;
  while (a) { value ^= a & 1; a = Math.floor(a / 2); }
  return value;
};
const gcd = (a, b) => {
  a = a < 0n ? -a : a;
  while (b) [a, b] = [b, a % b];
  return a;
};
const rational = (a, b = 1n) => {
  a = BigInt(a); b = BigInt(b);
  assert(b > 0n);
  const divisor = gcd(a, b);
  return [a / divisor, b / divisor];
};
const add = (a, b) => rational(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const multiply = (a, b) => rational(a[0] * b[0], a[1] * b[1]);
const less = (a, b) => a[0] * b[1] < b[0] * a[1];
const minimum = (a, b) => less(a, b) ? a : b;
const power = e => 1n << BigInt(e);
const read = value => rational(BigInt(value.sign) * BigInt(value.numerator_hex),
  power(value.denominator_binary_exponent));
const check = (actual, value) => assert.deepEqual(actual, read(value));
const hash = crypto.createHash('sha256');
let quadraticTables = 0;
for (let k = 0; k <= 3; k++) {
  const pairs = [];
  for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) pairs.push([i, j]);
  for (let c = 0; c < 4; c++) for (let code = 0; code < 4 ** k; code++) {
    const linear = Array.from({length: k}, (_, i) => Math.floor(code / 4 ** (k - i - 1)) % 4);
    for (let mask = 0; mask < 2 ** pairs.length; mask++) {
      const roots = [0, 0, 0, 0];
      for (let z = 0; z < 2 ** k; z++) {
        let phase = c;
        linear.forEach((b, i) => { phase += b * (z >> i & 1); });
        pairs.forEach(([i, j], t) => { phase += 2 * (mask >> t & 1) * (z >> i & 1) * (z >> j & 1); });
        roots[mod(phase, 4)]++;
      }
      const re = rational(roots[0] - roots[2], 2 ** k), im = rational(roots[1] - roots[3], 2 ** k);
      hash.update(JSON.stringify([k, c, linear, mask, ...re.map(String), ...im.map(String)]) + '\n');
      quadraticTables++;
    }
  }
}
assert.equal(quadraticTables, report.quadratic_gauss.complete_quadratic_phase_tables);
assert.equal(hash.digest('hex'), report.quadratic_gauss.exact_value_checksum);

const phase = (packet, z, secret) => packet.labels.reduce((total, row, l) => {
  const delta = row.reduce((sum, a, i) => sum + a *
    ((packet.origin[i] ^ parity(Number(BigInt(packet.kernel_rows_hex[i])) & z)) - packet.origin[i]), 0);
  assert.equal(mod(delta, 2), 0);
  return total + secret[l] * delta / 2;
}, 0);
const validateChart = packet => {
  const k = packet.retained_qubits, rows = packet.kernel_rows_hex.map(x => Number(BigInt(x)));
  assert(k <= 20); // This checker intentionally enumerates only bounded controls.
  assert.equal(rows.length, packet.origin.length);
  assert(packet.origin.every(x => x === 0 || x === 1));
  for (const row of packet.labels) {
    assert.equal(row.length, rows.length);
    for (let j = 0; j < k; j++) assert.equal(row.reduce((s, a, i) => s + (a & 1) * (rows[i] >> j & 1), 0) % 2, 0);
  }
  const images = new Set();
  for (let z = 0; z < 2 ** k; z++) images.add(rows.map(row => parity(row & z)).join(''));
  assert.equal(images.size, 2 ** k);
};
const bias = (left, right, secret, u, h) => {
  const roots = [0, 0, 0, 0], k = left.retained_qubits;
  for (let z = 0; z < 2 ** k; z++) {
    const delta = phase(left, z ^ h, secret) + phase(right, z ^ h ^ u, secret)
      - phase(left, z, secret) - phase(right, z ^ u, secret);
    roots[mod(4 / (left.modulus / 2) * delta, 4)]++;
  }
  assert.equal(roots[1], roots[3]);
  return rational(roots[0] - roots[2], 2 ** k);
};
const zeroParity = (left, right, secret, u, h) =>
  multiply(add([1n, 1n], bias(left, right, secret, u, h)), rational(1n, power(left.retained_qubits + 1)));
const fullQ4 = (left, right, secret, u, v) => {
  assert.equal(left.modulus, 4);
  const k = left.retained_qubits;
  let sum = 0;
  for (let z = 0; z < 2 ** k; z++) sum += mod(phase(left, z, secret)
    + phase(right, z ^ u, secret) + parity(z & v), 2) ? -1 : 1;
  return rational(sum * sum, power(3 * k));
};
let physicalAssignments = 0, fullLikelihoods = 0;
for (const row of report.physical_bell.controls) {
  validateChart(row.left); validateChart(row.right);
  check(zeroParity(row.left, row.right, row.secret_for_calibration_only,
    row.xor_outcome, row.parity_mask), row.joint_zero_parity_probability);
  physicalAssignments += 2 ** row.left.retained_qubits;
  if (row.q4_joint_full_probability !== null) {
    check(fullQ4(row.left, row.right, row.secret_for_calibration_only,
      row.xor_outcome, row.hadamard_outcome), row.q4_joint_full_probability);
    fullLikelihoods++;
  }
}
assert.equal(physicalAssignments, report.physical_bell.complete_derivative_polynomial_assignments);
assert.equal(report.physical_bell.controls.length + report.physical_bell.width_mismatch_controls_charged, 16);

// Independent small RREF, used only for the complete middle-label controls.
const packetFromLabels = labels => {
  const n = labels.length, m = labels[0].length;
  const matrix = labels.map(row => row.map(x => x & 1)), pivots = [];
  let rank = 0;
  for (let j = 0; j < m; j++) {
    const p = matrix.findIndex((row, i) => i >= rank && row[j]);
    if (p < 0) continue;
    [matrix[p], matrix[rank]] = [matrix[rank], matrix[p]];
    for (let i = 0; i < n; i++) if (i !== rank && matrix[i][j])
      matrix[i] = matrix[i].map((x, t) => x ^ matrix[rank][t]);
    pivots.push(j); rank++;
  }
  const free = Array.from({length: m}, (_, i) => i).filter(i => !pivots.includes(i));
  const rows = Array(m).fill(0);
  free.forEach((i, j) => { rows[i] = 2 ** j; });
  pivots.forEach((i, r) => { rows[i] = free.reduce((s, f, j) => s + matrix[r][f] * 2 ** j, 0); });
  return {labels, modulus: 8, origin: Array(m).fill(0),
    kernel_rows_hex: rows.map(x => '0x' + x.toString(16)), retained_qubits: free.length};
};
const binaryRank = input => {
  const basis = new Map();
  for (let row of input) {
    while (row) {
      const bit = Math.floor(Math.log2(row));
      if (basis.has(bit)) row ^= basis.get(bit);
      else { basis.set(bit, row); break; }
    }
  }
  return basis.size;
};
let middleTables = 0;
for (const row of report.middle_parseval_controls.rows) {
  let total = [0n, 1n];
  for (let code = 0; code < 64; code++) {
    const packets = [row.left_low[0], row.right_low[0]].map((low, side) => packetFromLabels(
      [low.map((b, i) => b + 2 * (code >> (i + 3 * side) & 1))]));
    const selected = packets.flatMap(packet => packet.kernel_rows_hex.map(x => Number(BigInt(x)))
      .filter(x => parity(x & row.parity_mask)));
    assert.equal(binaryRank(selected), row.middle_linear_rank);
    const value = bias(...packets, [row.secret_for_calibration_only], row.xor_outcome, row.parity_mask);
    total = add(total, multiply(value, value));
    middleTables++;
  }
  const average = multiply(total, rational(1, 64));
  check(average, row.average_squared_bias);
  assert.deepEqual(average, rational(1n, power(row.middle_linear_rank)));
}
const evenPacket = packetFromLabels([[1, 1, 1]]);
const evenBias = bias(evenPacket, evenPacket, [2], 0, 1);
check(multiply(evenBias, evenBias), report.middle_parseval_controls.all_even_secret_exception_squared_bias_witness);

const leftControl = {...packetFromLabels([[1, 1, 1]]), modulus: 4};
const rightControl = {...packetFromLabels([[1, 1, 0]]), modulus: 4};
let fullSuccess = [0n, 1n], paritySuccess = [0n, 1n];
const maximum = (a, b) => less(a, b) ? b : a;
for (let u = 0; u < 4; u++) {
  for (let v = 0; v < 4; v++) fullSuccess = add(fullSuccess,
    multiply(maximum(fullQ4(leftControl, rightControl, [0], u, v),
      fullQ4(leftControl, rightControl, [1], u, v)), rational(1, 2)));
  for (let b = 0; b < 2; b++) {
    const probabilities = [0, 1].map(s => {
      const p = zeroParity(leftControl, rightControl, [s], u, 1);
      return b ? add(rational(1, 4), multiply(p, rational(-1))) : p;
    });
    paritySuccess = add(paritySuccess, multiply(maximum(...probabilities), rational(1, 2)));
  }
}
check(fullSuccess, report.full_output_countercontrol.q4_nonmatching_full_readout_bayes_success);
check(paritySuccess, report.full_output_countercontrol.one_coordinate_parity_bayes_success);

for (const row of report.tail_unit_information_certificates) {
  const n = row.dimension, r = Math.floor(n / 2);
  let binomial = 1n, total = 0n;
  for (let c = 0; c < r; c++) {
    total += binomial;
    binomial = binomial * BigInt(2 * n - c) / BigInt(c + 1);
  }
  const count = rational(total, power(2 * n));
  const rankFail = rational(1n, power(n - 1 - r));
  const prefixFail = rational(2n, power(n));
  const bad = minimum(rational(1), add(prefixFail, multiply(rational(n), add(count, rankFail))));
  const alpha = minimum(rational(1), add(add(bad, rational(1n, power(n))), rational(BigInt(n), power(r + 1))));
  const kl = multiply(rational(row.fresh_pair_attempts), alpha);
  check(count, row.selected_pivot_count_tail_bound);
  check(rankFail, row.rank_failure_bound_given_enough_selected_pivots);
  check(prefixFail, row.two_prefix_rank_failure_bound);
  check(bad, row.public_low_rank_event_probability_upper_bound);
  check(alpha, row.one_bit_average_squared_bias_upper_bound);
  check(kl, row.transcript_kl_to_matched_fair_reference_bits_upper_bound);
  check(minimum(rational(2 * n), kl), row.uniform_secret_mutual_information_bits_upper_bound);
  for (const d of [10, 100]) {
    const gap = add(rational(1, d), rational(-1n, power(2 * n)));
    assert.equal(less(rational(0), gap) && less(multiply(kl, rational(1, 2)), multiply(gap, gap)),
      row['success_below_one_over_' + d]);
  }
  assert.equal(row.full_bell_transcript_covered, false);
  assert.equal(row.coherent_memory_or_reused_packets_covered, false);
}
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
assert.equal(report.claim_gate.full_q8_likelihood_implemented, false);
assert.equal(report.claim_gate.independent_theorem_review, false);
console.log(JSON.stringify({status: 'BOUNDED_ARITHMETIC_CROSSCHECK_ONLY',
  complete_quadratic_tables: quadraticTables, physical_derivative_assignments: physicalAssignments,
  q4_full_likelihoods: fullLikelihoods, middle_label_tables_across_conditions: middleTables,
  source_information_certificates: report.tail_unit_information_certificates.length,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));

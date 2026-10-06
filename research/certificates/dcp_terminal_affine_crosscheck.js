// Independent modular source enumeration and exact ledgers, not theorem peer review.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_terminal_affine_fibers.json'), 'utf8'));
const readFraction = x => [BigInt(x.sign) * BigInt(x.numerator_hex), BigInt(x.denominator_hex)];
const equalFraction = (record, p, q) => {
  const [a, b] = readFraction(record); assert.equal(a * q, b * p);
};
const rank = rows => {
  const pivots = new Map();
  for (let x of rows) {
    for (const [p, v] of [...pivots.entries()].sort((a, b) => b[0] - a[0])) if (x & (1 << p)) x ^= v;
    if (x) pivots.set(Math.floor(Math.log2(x)), x);
  }
  return pivots.size;
};
const planes = width => {
  const N = 2 ** width, out = [];
  // Four distinct binary points form a plane exactly when their XOR is zero.
  for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) for (let c = b + 1; c < N; c++) {
    const d = a ^ b ^ c;
    if (d > c) out.push([a, b, c, d]);
  }
  return out;
};
let sourceTables = 0, checkedPlanes = 0;
for (const row of report.complete_native_source_controls) {
  const n = row.dimension, m = row.physical_width, Q = 2 ** row.modulus_bits, N = 2 ** m;
  const P = planes(m), sources = Q ** (n * m);
  let planeIncidences = 0, incidentPoints = 0, accepted = 0, kernelPoints = 0;
  for (let code = 0; code < sources; code++) {
    let v = code;
    const A = Array.from({length: n}, () => Array.from({length: m}, () => {
      const a = v % Q; v = Math.floor(v / Q); return a;
    }));
    const values = Array.from({length: N}, (_, x) => A.map(r => r.reduce((s, a, j) => s + (x & (1 << j) ? a : 0), 0) % Q));
    const equal = (x, y) => values[x].every((a, i) => a === values[y][i]);
    const incident = new Set();
    for (const plane of P) {
      checkedPlanes++;
      if (plane.every(x => equal(x, plane[0]))) { planeIncidences += 4; plane.forEach(x => incident.add(x)); }
    }
    incidentPoints += incident.size;
    const prefix = A.map(r => r.slice(0, n).reduce((x, a, j) => x | ((a & 1) << j), 0));
    if (rank(prefix) === n) {
      accepted++;
      for (const x of incident) if (values[x].every(a => a % 2 === 0)) kernelPoints++;
    }
    sourceTables++;
  }
  assert.equal(sources, row.complete_label_tables); assert.equal(accepted, row.prefix_accepted_tables);
  equalFraction(row.source_mean_affine_planes_through_uniform_point, BigInt(planeIncidences), BigInt(sources * N));
  equalFraction(row.source_mean_full_cube_incident_point_fraction, BigInt(incidentPoints), BigInt(sources * N));
  equalFraction(row.source_mean_zero_syndrome_incident_point_fraction_conditioned_prefix,
    BigInt(kernelPoints), BigInt(accepted * 2 ** (m - n)));
}

let sourceBounds = 0;
function sourceCheck(row) {
  const n = row.dimension, m = row.physical_width, a = row.tested_modulus_bits;
  let b2 = 2 * n * a - Math.ceil(8 * m / 5) + 1, b3 = 3 * n * a - 2 * m - n + 2;
  if (row.parity_kernel_uniform_points_and_invertible_binary_prefix_conditioned) { b2 -= n + 2; b3 -= n + 2; }
  assert.equal(row.degenerate_term_dyadic_exponent, b2);
  assert.equal(row.generic_term_dyadic_exponent, b3);
  const bits = Math.max(0, Math.min(b2, b3) - 1);
  assert.equal(row.source_mean_incident_point_mass_upper_bound_dyadic_exponent, bits);
  const M = BigInt(m), info = BigInt(n * a);
  const D = 3n * (3n ** M - 2n * 2n ** M + 1n), G = 4n ** M - 3n * 3n ** M + 3n * 2n ** M - 1n;
  // Exact expected plane count: D/(6 Q^(2n)) + G*2^n/(6 Q^(3n)).
  let numerator = D * (1n << info) + G * (1n << BigInt(n)), denominator = 6n * (1n << (3n * info));
  if (row.parity_kernel_uniform_points_and_invertible_binary_prefix_conditioned) {
    numerator <<= BigInt(n);
    for (let j = 1; j <= n; j++) { numerator <<= BigInt(j); denominator *= (1n << BigInt(j)) - 1n; }
  }
  if (bits) assert.ok(numerator * (1n << BigInt(bits)) <= denominator);
  sourceBounds++;
}
for (const row of [...report.native_near_density_one_scaling, ...report.partial_modulus_affine_restart_bounds,
                    ...report.increased_density_escape_controls,
                    ...report.complete_native_source_controls.map(x => x.source_ledger)]) sourceCheck(row);
report.high_probability_packet_gates.forEach((row, i) => {
  const bits = report.native_near_density_one_scaling[i].source_mean_incident_point_mass_upper_bound_dyadic_exponent;
  assert.equal(row.incident_point_fraction_threshold_dyadic_exponent, Math.floor(bits / 2));
  assert.equal(row.packet_probability_of_exceeding_threshold_upper_bound_dyadic_exponent, bits - Math.floor(bits / 2));
});

const sqrt = n => {
  let lo = 0n, hi = n + 1n;
  while (hi - lo > 1n) { const mid = (lo + hi) / 2n; if (mid * mid <= n) lo = mid; else hi = mid; }
  return lo;
};
for (const row of report.affine_tail_compression) {
  const N = 1n << BigInt(row.physical_affine_tail_bits), cap = (1n + sqrt(8n * N - 7n)) / 2n;
  assert.equal(BigInt(row.plane_free_fiber_size_upper_bound), cap);
  equalFraction(row.nonincident_points_rank_compression_probability_upper_bound, cap * BigInt(row.target_projector_rank), N);
  assert.equal(row.general_quantum_decoder_no_go, false);
}
let maxSmallCap = 0;
for (let mask = 0; mask < 256; mask++) {
  const points = Array.from({length: 8}, (_, x) => x).filter(x => mask & (1 << x)), sums = new Set();
  let valid = true;
  for (let i = 0; i < points.length; i++) for (let j = i + 1; j < points.length; j++) {
    const sum = points[i] ^ points[j]; if (sums.has(sum)) valid = false; sums.add(sum);
  }
  if (valid) maxSmallCap = Math.max(maxSmallCap, points.length);
}
assert.equal(maxSmallCap, 4);
for (const row of report.charged_selection) {
  const menu = row.original_pool_states === null ? Math.ceil(Math.log2(row.packet_choices)) :
    1056 * Math.ceil(Math.log2(row.original_pool_states));
  assert.equal(row.menu_log2_upper_bound, menu);
  assert.equal(row.selected_packet_source_mean_incident_point_mass_upper_bound_dyadic_exponent, Math.max(0, 372 - menu));
}
for (const [name, expected] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, name))).digest('hex'), expected);
}
assert.equal(report.claim_gate.candidate_record_accepted, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW', sourceTables, checkedPlanes,
  sourceBounds, compressionBounds: report.affine_tail_compression.length, smallCapSubsets: 256,
  selectionLedgers: report.charged_selection.length, dependencyHashes: Object.keys(report.dependency_sha256).length}, null, 2));

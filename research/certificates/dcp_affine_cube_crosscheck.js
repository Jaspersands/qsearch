// Independent integer/modular arithmetic and phase countercontrol; not theorem review.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_affine_cube_hierarchy.json'), 'utf8'));
const pop = x => { let c = 0; while (x) { x &= x - 1n; c++; } return c; };
const ceilLog = x => x <= 1n ? 0 : (x - 1n).toString(2).length;
const rank = rows => {
  const pivots = new Map();
  for (let x of rows) {
    for (const p of [...pivots.keys()].sort((a, b) => b - a)) if (x >> BigInt(p) & 1n) x ^= pivots.get(p);
    if (x) pivots.set(x.toString(2).length - 1, x);
  }
  return pivots.size;
};
const sqrt = n => {
  let lo = 0n, hi = n + 1n;
  while (hi - lo > 1n) { const mid = (hi + lo) / 2n; if (mid * mid <= n) lo = mid; else hi = mid; }
  return lo;
};
const fraction = x => [BigInt(x.sign) * BigInt(x.numerator_hex), BigInt(x.denominator_hex)];
const equalFraction = (x, p, q) => { const [a, b] = fraction(x); assert.equal(a * q, b * p); };
let inverseEntries = 0, patternTables = 0;
for (const row of report.parity_inverse_controls) {
  const r = row.cube_dimension, J = 2 ** r - 1;
  const P = Array.from({length: J}, (_, x) => Array.from({length: J}, (_, p) => pop(BigInt((x + 1) & (p + 1))) % 2));
  for (let i = 0; i < J; i++) for (let j = 0; j < J; j++) {
    const value = P[i].reduce((s, a, k) => s + a * (2 * P[j][k] - 1), 0);
    assert.equal(value, i === j ? 2 ** (r - 1) : 0); inverseEntries++;
  }
  assert.equal(row.checked_product_entries, J * J);
}
for (const row of report.complete_pattern_sum_controls) {
  const r = row.cube_dimension, Q = 2 ** row.modulus_bits, J = 2 ** r - 1;
  let flat = 0;
  for (let code = 0; code < Q ** J; code++) {
    let v = code;
    const S = Array.from({length: J}, () => { const a = v % Q; v = Math.floor(v / Q); return a; });
    let valid = true;
    for (let x = 1; x <= J; x++) if (S.reduce((sum, s, p) => sum + s * (pop(BigInt(x & (p + 1))) % 2), 0) % Q) valid = false;
    if (valid) { flat++; assert.ok(S.every(s => s * 2 ** (r - 1) % Q === 0)); }
    patternTables++;
  }
  assert.equal(row.flat_tables, flat); equalFraction(row.exact_full_pattern_flatness_probability, BigInt(flat), BigInt(Q ** J));
}

function source(n, m, a, r, precision = 32) {
  const log = ceilLog(BigInt(r + 1) ** BigInt(precision));
  const entropy = Math.ceil(m * log / (r * precision));
  const gap = n * Math.max(0, a - r + 1) - r - entropy;
  const bits = gap < 1 ? 0 : Math.max(0, r * gap + r * r - n - 5);
  return {log, entropy, gap, bits};
}
function capBits(d, r) { return r > d ? 0 : r === 1 ? d : Math.max(0, Number(BigInt(d - r + 1) >> BigInt(r - 1)) - 1); }
const belowTwoThirds = (a, b) => Math.min(a, b) >= 2 || Math.min(a, b) === 1 && Math.max(a, b) >= 3;
let sourceLedgers = 0;
for (const profile of report.cube_source_and_compression_scaling) {
  const n = profile.dimension, m = profile.physical_width, a = profile.full_modulus_bits, d = m - n * a;
  const declared = profile.best_deterministic_design_gate, row = declared.source, c = declared.compression;
  const expected = source(n, m, a, row.cube_dimension);
  assert.equal(row.log2_cube_dimension_plus_one_upper_bound_numerator, expected.log);
  assert.equal(row.per_pattern_assignment_entropy_bits_upper_bound, expected.entropy);
  assert.equal(row.per_pattern_probability_gap_bits, expected.gap);
  assert.equal(row.source_mean_incident_point_mass_upper_bound_dyadic_exponent, expected.bits);
  const b = capBits(d, row.cube_dimension);
  assert.equal(c.rank_adjusted_nonincident_probability_dyadic_exponent, b);
  assert.equal(c.uniform_secret_source_mean_acceptance_proved_below_two_thirds, belowTwoThirds(b, expected.bits));
  let best = null;
  for (let r = 2; r <= Math.min(d, a, 32); r++) {
    const s = source(n, m, a, r), cb = capBits(d, r);
    const score = [Math.max(0, Math.min(cb, s.bits) - 1), Number(belowTwoThirds(cb, s.bits)), s.bits];
    if (!best || score.some((v, i) => v > best.score[i] && score.slice(0, i).every((x, j) => x === best.score[j]))) best = {r, score};
  }
  assert.equal(row.cube_dimension, best.r); sourceLedgers++;
}

let capRecurrences = 0;
for (let d = 1; d <= 64; d++) for (let r = 1; r <= Math.min(d, 12); r++) {
  let cap = 1n;
  for (let j = 2; j <= r; j++) {
    const size = 1n << BigInt(d - r + j);
    cap = (1n + sqrt(1n + 8n * (size - 1n) * cap)) / 2n;
  }
  assert.ok(cap * (1n << BigInt(capBits(d, r))) <= 1n << BigInt(d)); capRecurrences++;
}

let physicalPolars = 0;
for (const row of report.actual_packet_selected_polar_controls) {
  const R = row.parity_rows_hex.map(BigInt), W = row.physical_directions_hex.map(BigInt), m = row.physical_width;
  const actual = R.map(b => W.map(u => W.reduce((x, v, j) => x | (BigInt(pop(b & u & v) % 2) << BigInt(j)), 0n)));
  const ranks = actual.map(rank);
  assert.deepEqual(row.actual_scalar_polar_ranks, ranks);
  assert.deepEqual(row.actual_scalar_polar_matrices_hex.map(x => x.map(BigInt)), actual);
  for (const b of R) for (const w of W) assert.equal(pop(b & w) % 2, 0);
  const zeros = m - pop(R.reduce((x, b) => x | b, 0n)), gap = 2 * W.length - m - zeros;
  const lower = 2 * Math.max(0, Math.ceil(gap / (2 * R.length)));
  assert.ok(Math.max(...ranks) >= lower);
  assert.equal(row.all_block_gate.some_actual_scalar_carry_polar_rank_lower_bound, lower); physicalPolars++;
}
for (const row of report.dense_half_width_source_scaling) {
  const n = row.dimension, m = row.physical_width, a = row.full_modulus_bits, tail = m - n * a;
  const gap = 2 * tail - m, budget = Math.max(0, Math.floor(gap / 2)), half = Math.max(0, Math.ceil((gap - budget) / (2 * n)));
  assert.equal(row.allowed_zero_binary_columns, budget);
  assert.equal(row.on_good_sources_scalar_carry_bias_exponent_lower_bound, half);
  equalFraction(row.native_tail_zero_column_count_mean, BigInt(m - n), 1n << BigInt(n));
  const p = BigInt(m - n), q = BigInt(budget + 1) << BigInt(n);
  equalFraction(row.probability_zero_column_budget_exceeded_upper_bound, p > q ? q : p, q);
  const [num, den] = fraction(row.conservatively_rounded_acceptance_bound_for_two_thirds_comparison);
  assert.equal(row.uniform_secret_source_mean_acceptance_proved_below_two_thirds, 3n * num < 2n * den);
}

const positive = report.phase_separation_countercontrol;
const f = z => {
  const x = [z & 1, z & 1, z >> 1 & 1, z >> 2 & 1, z >> 3 & 1, z >> 4 & 1];
  return positive.labels[0].reduce((s, a, i) => s + a * x[i], 0) / 2 % 4;
};
let witnessTrials = 0;
for (let j = 0; j < 8; j++) for (let t = 0; t < 4; t++) {
  const c = (f(positive.logical_permutation[t + 4 * j]) - t + 4) % 4;
  assert.equal(c, positive.junk_offsets[j]);
  for (let challenge = 0; challenge < 4; challenge++) {
    assert.equal(f(positive.logical_permutation[(challenge - c + 4) % 4 + 4 * j]), challenge); witnessTrials++;
  }
}
let flatMean = 0;
for (let s = 0; s < 4; s++) {
  let correct = 0, junkRe = 0, junkIm = 0;
  for (let j = 0; j < 8; j++) {
    let re = 0, im = 0;
    for (let t = 0; t < 4; t++) {
      const angle = 2 * Math.PI * s * (f(positive.logical_permutation[t + 4 * j]) - t) / 4;
      re += Math.cos(angle); im += Math.sin(angle);
    }
    correct += (re * re + im * im) / 128;
    const angle = 2 * Math.PI * s * positive.junk_offsets[j] / 4;
    junkRe += Math.cos(angle); junkIm += Math.sin(angle);
  }
  assert.ok(Math.abs(correct - 1) < 1e-12);
  flatMean += (junkRe * junkRe + junkIm * junkIm) / 256;
}
assert.ok(Math.abs(flatMean - 0.25) < 1e-12);
assert.equal(positive.clean_fixed_junk_is_necessary_for_a_DCP_decoder, false);
equalFraction(positive.literal_label_table_conditional_native_prefix_probability, 1n, 1n << 17n);
for (const row of report.charged_cube_packet_menu_controls) {
  const menuBits = row.original_pool_states === null ? ceilLog(BigInt(row.packet_choices)) : 8256 * ceilLog(BigInt(row.original_pool_states));
  assert.equal(row.menu_log2_upper_bound, menuBits);
  assert.equal(row.selected_packet_source_mean_incident_point_mass_upper_bound_dyadic_exponent, Math.max(0, 551 - menuBits));
}
for (const [file, hash] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), hash);
}
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW', inverseEntries, patternTables,
  sourceLedgers, capRecurrences, physicalPolars, denseSourceLedgers: report.dense_half_width_source_scaling.length,
  secretQFTControls: 4, witnessTrials, selectionLedgers: report.charged_cube_packet_menu_controls.length,
  dependencyHashes: Object.keys(report.dependency_sha256).length}, null, 2));

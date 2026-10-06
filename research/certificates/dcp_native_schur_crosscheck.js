// Independent code-product and source-budget arithmetic, not theorem peer review.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_native_schur_expansion.json'), 'utf8'));
const bits = x => x ? x.toString(2).length : 0;
const pop = x => { let count = 0; while (x) { x &= x - 1n; count++; } return count; };
const parity = x => pop(x) % 2;
const basis = rows => {
  const pivots = new Map();
  for (let x of rows) {
    for (const p of [...pivots.keys()].sort((a, b) => b - a)) if (x >> BigInt(p) & 1n) x ^= pivots.get(p);
    if (x) pivots.set(bits(x) - 1, x);
  }
  for (const p of [...pivots.keys()].sort((a, b) => a - b)) {
    for (const q of pivots.keys()) if (q > p && pivots.get(q) >> BigInt(p) & 1n) pivots.set(q, pivots.get(q) ^ pivots.get(p));
  }
  return [...pivots.values()];
};
const rank = rows => basis(rows).length;
const nullspace = (rows, width) => {
  const R = basis(rows), pivots = new Set(R.map(x => bits(x) - 1)), out = [];
  for (let j = 0; j < width; j++) if (!pivots.has(j)) out.push(R.reduce((x, row) => x | ((row >> BigInt(j) & 1n) << BigInt(bits(row) - 1)), 1n << BigInt(j)));
  return out;
};
const frac = x => [BigInt(x.sign) * BigInt(x.numerator_hex), BigInt(x.denominator_hex)];
const add = (a, b) => [a[0] * b[1] + b[0] * a[1], a[1] * b[1]];
const mul = (a, b) => [a[0] * b[0], a[1] * b[1]];
const min = (...xs) => xs.reduce((a, b) => a[0] * b[1] < b[0] * a[1] ? a : b);
const eq = (declared, actual) => { const d = frac(declared); assert.equal(d[0] * actual[1], d[1] * actual[0]); };
const dyadic = (exponent, precision) => exponent > 0 ? [1n, 1n << BigInt(Math.min(exponent, precision))] : [1n, 1n];
const capacity = (n, r, p) => {
  const c = Math.max(1, p - r);
  return [c, c > n + r ? 0n : [1n << BigInt(n), (1n << BigInt(n + r - c + 1)) + BigInt(c - 1)].reduce((a, b) => a < b ? a : b) - 1n];
};
let selectedProducts = 0, exactStabilizerDimensions = 0, middleMatrices = 0;
function checkSelected(row) {
  const R = row.parity_rows_hex.map(BigInt), W = row.physical_directions_hex.map(BigInt), width = row.physical_width;
  const S = basis([...R, ...R.flatMap(b => W.map(w => b & w))]);
  assert.equal(rank(R), R.length); assert.equal(rank(W), W.length);
  for (const w of W) for (const b of R) assert.equal(parity(w & b), 0);
  assert.equal(row.extension_rank, S.length - R.length);
  assert.equal(rank([...S, ...row.product_space_basis_hex.map(BigInt)]), S.length);
  const active = R.reduce((out, b) => out | b, 0n), unit = (1n << BigInt(width)) - 1n;
  const p = rank([unit & active, ...W.map(w => w & active)]);
  assert.equal(row.active_unit_augmented_subcode_dimension, p);
  const dual = nullspace(S, width), stabilizerConstraints = S.flatMap(s => dual.map(h => s & h));
  const c = pop(active) - rank(stabilizerConstraints);
  assert.equal(row.product_stabilizer_component_count, c); exactStabilizerDimensions++;
  assert.ok(S.length >= R.length + p - c);
  let covered = 0n, blockRanks = 0;
  const columns = Array.from({length: width}, (_, i) => R.reduce((x, b, l) => x | (b >> BigInt(i) & 1n) << BigInt(l), 0n));
  for (const component of row.components) {
    const block = BigInt(component.physical_component_mask_hex);
    assert.equal(covered & block, 0n); covered |= block;
    assert.equal(rank([...S, ...S.map(s => s & block)]), S.length);
    const a = rank(R.map(b => b & block)), h = rank(S.map(s => s & block));
    assert.equal(component.dual_projection_rank, a); assert.equal(component.product_projection_rank, h); blockRanks += h;
    const signatures = new Set(columns.filter((_, i) => block >> BigInt(i) & 1n).map(String));
    assert.ok(!signatures.has('0')); assert.equal(component.nonzero_signatures_in_component, signatures.size);
    assert.ok(BigInt(signatures.size) <= (1n << BigInt(a)) - 1n);
  }
  assert.equal(covered, active); assert.equal(blockRanks, S.length);
  const g = row.signature_gate_at_actual_extension_rank, zeros = columns.filter(x => !x).length;
  const even = R.every(b => parity(b) === 0), floor = Math.max(1, W.length - zeros + Number(!even));
  const [required, cap] = capacity(R.length, row.extension_rank, floor);
  assert.equal(g.required_product_stabilizer_component_count_lower_bound, required);
  assert.equal(BigInt(g.nonzero_signature_capacity_upper_bound_decimal), cap);
  assert.equal(g.all_one_physical_vector_in_kernel, even);
  assert.equal(g.zero_binary_columns, zeros);
  assert.equal(g.every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded, false);
  selectedProducts++;
}

function envelope(n, k, r, declared) {
  const [c, cap] = capacity(n, r, n), overhead = (n + 1) * (n + r) + bits(BigInt(n + r - 1));
  const decay = cap <= 1n << BigInt(n - 1) ? k * (n - bits(cap - 1n)) :
    4n * cap <= 3n * (1n << BigInt(n)) ? 2 * Math.floor(k / 5) : 0;
  if (declared) {
    assert.equal(BigInt(declared.parity_free_signature_capacity_decimal), cap);
    assert.equal(declared.required_component_count_lower_bound, c);
    assert.equal(declared.ordered_subspace_envelope_count_binary_exponent_upper_bound, overhead);
    assert.equal(declared.tail_coverage_decay_binary_exponent_lower_bound, decay);
    assert.equal(declared.envelope_probability_dyadic_exponent_before_rounding, decay - overhead);
    assert.equal(declared.all_one_kernel_vector_exception_needed, false);
  }
  return decay - overhead;
}
for (const row of [...report.actual_selected_packet_subcodes, ...report.structured_rank_one_positive_controls]) checkSelected(row);
for (const row of report.native_source_scaling_bounds) {
  const n = row.dimension, k = row.iid_uniform_binary_tail_columns, r = row.extension_rank_budget, N = 1n << BigInt(n);
  const [c, cap] = capacity(n, r, n + 1);
  assert.equal(row.required_product_component_count_if_no_zero_columns_and_odd_row_parity, c);
  assert.equal(BigInt(row.nonzero_signature_capacity_if_no_zero_columns_and_odd_row_parity_decimal), cap);
  eq(row.expected_equal_signature_pair_count, [BigInt(k * (k - 1) / 2 + n * k), N]);
  let oldSignature;
  if (!cap) oldSignature = [0n, 1n];
  else {
    const deficit = BigInt(n + k) > cap ? BigInt(n + k) - cap : 0n;
    const collision = deficit ? min([1n, 1n], [BigInt(k * (k - 1) / 2 + n * k), N * deficit]) : [1n, 1n];
    const extra = cap > BigInt(n) ? cap - BigInt(n) : 0n;
    const gap = BigInt(n) * (BigInt(k) - extra) - BigInt(k * bits(cap - 1n));
    const cover = gap > 0n ? dyadic(Number(gap > BigInt(n) ? BigInt(n) : gap), n) : [1n, 1n];
    oldSignature = min(collision, cover); eq(row.collision_markov_signature_event_upper_bound, collision);
  }
  eq(row.signature_event_upper_bound, oldSignature);
  const exp = envelope(n, k, r, row.parity_free_subspace_envelope), geometric = dyadic(exp, n);
  eq(row.parity_free_envelope_probability_upper_bound, geometric);
  const parityFree = min([1n, 1n], add([BigInt(k), N], geometric));
  eq(row.zero_column_or_parity_free_low_variation_family_probability_upper_bound, parityFree);
  eq(row.exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound,
    min([1n, 1n], add([BigInt(k + 1), N], oldSignature), parityFree));
}
for (const row of report.adaptive_pool_bounds) {
  const n = row.dimension, k = row.packet_states - n, pool = row.iid_original_pool_states, r = row.extension_rank_budget;
  const menu = (n + k) * bits(BigInt(pool - 1)), exp = envelope(n, k, r) - menu;
  assert.equal(row.ordered_packet_menu_count_binary_exponent_upper_bound, menu);
  assert.equal(row.envelope_mass_exponent_after_charging_all_ordered_packet_menus, exp);
  eq(row.existence_probability_upper_bound_including_global_zero_label_exception,
    min([1n, 1n], add([BigInt(pool), 1n << BigInt(n)], dyadic(exp, n))));
}
for (const row of report.identity_pencil_middle_source_controls) {
  const n = row.dimension;
  let p = [1n, 1n], d = [1n, 1n], denominator = 1n;
  for (let j = 1; j <= n; j++) {
    const power = 1n << BigInt(j); p = mul(p, [power - 1n, power]); denominator *= power - 1n;
    d = add(d, [j % 2 ? -1n : 1n, denominator]);
  }
  eq(row.uniform_constant_matrix_all_background_invertibility_probability, mul(p, d));
  if (n <= 4) {
    let good = 0;
    for (let code = 0; code < 2 ** (n * n); code++) {
      const M = Array.from({length: n}, (_, l) => BigInt(code >> (n * l) & (2 ** n - 1)));
      good += Number(rank(M) === n && rank(M.map((x, l) => x ^ (1n << BigInt(l)))) === n); middleMatrices++;
    }
    eq(row.uniform_constant_matrix_all_background_invertibility_probability, [BigInt(good), 1n << BigInt(n * n)]);
  }
}
for (const [relative, digest] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, relative))).digest('hex'), digest);
}
assert.equal(report.claim_gate.all_larger_correlated_pencils_or_background_adaptive_pivots_excluded, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW', selectedProducts,
  exactStabilizerDimensions, middleMatrices, fixedSourceBounds: report.native_source_scaling_bounds.length,
  adaptivePoolBounds: report.adaptive_pool_bounds.length, dependencyHashes: Object.keys(report.dependency_sha256).length}, null, 2));

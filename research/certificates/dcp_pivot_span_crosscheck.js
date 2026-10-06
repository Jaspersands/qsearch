// Independent bounded arithmetic checks, not a theorem reviewer or DCP solver.
const assert = require('assert/strict');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_pivot_span_obstructions.json'), 'utf8'));
const parity = x => { let bit = 0; while (x) { x &= x - 1n; bit ^= 1; } return bit; };
const rank = rows => {
  const pivots = new Map();
  for (let row of rows) {
    row = BigInt(row);
    for (const p of [...pivots.keys()].sort((a, b) => b - a)) if (row >> BigInt(p) & 1n) row ^= pivots.get(p);
    if (row) pivots.set(row.toString(2).length - 1, row);
  }
  return pivots.size;
};
const decode = xs => xs.map(BigInt);
const decodeFamily = f => ({d: f.input_bits, n: f.dimension, b: f.background_bits,
  constant: decode(f.constant_rows_hex), generators: f.variation_rows_hex.map(decode)});
const flat = (rows, d) => rows.reduce((out, row, l) => out | row << BigInt(d * l), 0n);
const combine = (xs, mask) => xs.reduce((out, x, i) => out ^ (mask >> BigInt(i) & 1n ? x : 0n), 0n);
const apply = (rows, x) => rows.reduce((out, row, l) => out | BigInt(parity(row & x)) << BigInt(l), 0n);
const restrict = (rows, W) => rows.map(row => apply(W, row));
const matrix = (f, y) => f.constant.map((row, l) => row ^ combine(f.generators.map(M => M[l]), y));
const frac = x => [BigInt(x.sign) * BigInt(x.numerator_hex), BigInt(x.denominator_hex)];
let blockWitnesses = 0, sourceOperatorEntries = 0, weightedRadicals = 0, backgroundControls = 0, schurControls = 0;

function checkBlock(f, c) {
  const generators = f.generators.map(M => flat(M, f.d));
  const imageRank = rank(generators), ann = decode(c.matrix_image_annihilator_basis_hex);
  assert.equal(c.background_matrix_image_dimension, imageRank);
  assert.equal(rank(ann), f.n * f.d - imageRank);
  for (const a of ann) for (const g of generators) assert.equal(parity(a & g), 0);
  const mask = (1n << BigInt(f.d)) - 1n;
  const rows = ann.flatMap(a => Array.from({length: f.n}, (_, l) => a >> BigInt(f.d * l) & mask));
  const constraints = decode(c.annihilator_row_span_basis_hex), E = decode(c.complete_row_block_basis_hex);
  assert.equal(rank(constraints), rank(rows));
  assert.equal(rank([...rows, ...constraints]), rank(rows));
  assert.equal(rank(E), f.d - rank(rows));
  for (const e of E) for (const row of rows) assert.equal(parity(e & row), 0);
  assert.equal(c.complete_row_block_dimension, E.length);
  assert.equal(c.complete_row_block_codimension, rank(rows));
  E.forEach((e, i) => c.complete_row_block_background_witnesses_hex[i].forEach((y, l) => {
    assert.equal(combine(generators, BigInt(y)), e << BigInt(f.d * l)); blockWitnesses++;
  }));
  const floor = Math.max(0, imageRank - f.n * (f.d - f.n));
  assert.equal(c.every_n_dimensional_span_variation_image_dimension_lower_bound, floor);
  assert.equal(c.all_fixed_n_dimensional_spans_excluded_by_dimension_theorem, floor > f.n * (f.n - 1) / 2);
  assert.equal(c.every_n_dimensional_span_complete_block_rank_lower_bound, Math.max(0, f.n - rank(rows)));
  assert.equal(c.background_adaptive_pivots_or_other_isotropic_charts_excluded, false);
}

function checkWeighted(f, c) {
  if (c.status.startsWith('SKIPPED')) { assert.equal(c.all_fixed_spans_excluded, false); return; }
  const all = [];
  assert.equal(c.combinations_evaluated, 2 ** f.n - 1);
  for (const record of c.weighted_radicals) {
    const weight = BigInt(record.output_weight_hex);
    const rows = f.generators.map(M => M.reduce((x, row, l) => x ^ (weight >> BigInt(l) & 1n ? row : 0n), 0n));
    const kernel = decode(record.radical_basis_hex);
    assert.equal(rank(kernel), f.d - rank(rows));
    for (const w of kernel) for (const row of rows) assert.equal(parity(w & row), 0);
    all.push(...kernel); weightedRadicals++;
  }
  assert.equal(c.eligible_direction_span_dimension, rank(all));
  const declared = decode(c.eligible_direction_span_basis_hex);
  assert.equal(rank(declared), rank(all)); assert.equal(rank([...all, ...declared]), rank(all));
  assert.equal(c.all_fixed_spans_excluded, rank(all) < f.n);
}

function checkSelected(f, c) {
  const W = decode(c.directions_in_U_coordinates_hex), selected = decodeFamily(c.restricted_operator_family);
  assert.equal(rank(W), f.n); assert.deepEqual(restrict(f.constant, W), selected.constant);
  assert.deepEqual(f.generators.map(M => restrict(M, W)), selected.generators);
  checkBlock(selected, c.complete_row_block);
  const r = c.complete_row_block.background_matrix_image_dimension;
  assert.equal(c.dimension_theorem_excludes_every_constant_part, r > f.n * (f.n - 1) / 2);
  if (c.surjective_direction_background_witness) {
    const witness = c.surjective_direction_background_witness, w = BigInt(witness.input_direction_hex);
    assert.equal(rank([...W, w]), f.n);
    assert.equal(rank(f.generators.map(M => apply(M, w))), f.n);
    assert.equal(apply(matrix(f, BigInt(witness.background_mask_hex)), w), 0n);
  }
  if (f.b <= 8) {
    let good = 0;
    for (let y = 0; y < 2 ** f.b; y++) { good += Number(rank(restrict(matrix(f, BigInt(y)), W)) === f.n); backgroundControls++; }
    const [num, den] = frac(c.uniform_background_invertibility_fraction_upper_bound);
    assert.ok(BigInt(good) * den <= num * (1n << BigInt(f.b)));
    if (c.all_backgrounds_invertible_excluded) assert.ok(good < 2 ** f.b);
    if (c.pencil_coverage.all_backgrounds_invertible_certified) assert.equal(good, 2 ** f.b);
  }
  assert.equal(c.speedup_claim_allowed, false);
}

function checkPhysical(f, provenance, schur) {
  const A = provenance.labels.map(row => row.map(BigInt)), n = A.length, k = A[0].length - n;
  for (let l = 0; l < n; l++) for (let i = 0; i < n; i++) assert.equal(A[l][i] & 1n, BigInt(l === i));
  const kernelRows = [...A.map(row => row.slice(n).reduce((out, a, j) => out | (a & 1n) << BigInt(j), 0n)),
    ...Array.from({length: k}, (_, j) => 1n << BigInt(j))];
  const physical = w => apply(kernelRows, w);
  const U = decode(provenance.isotropic_directions_hex), V = decode(provenance.complement_directions_hex);
  assert.equal(rank([...U, ...V]), k); assert.equal(U.length, f.d); assert.equal(V.length, f.b);
  const dual = A.map(row => row.reduce((out, a, i) => out | (a & 1n) << BigInt(i), 0n));
  const slope = (w, l) => {
    const x = physical(w), total = A[l].reduce((out, a, i) => out + a * (x >> BigInt(i) & 1n), 0n);
    assert.equal(total & 1n, 0n); return total / 2n & 1n;
  };
  for (let l = 0; l < n; l++) for (let j = 0; j < U.length; j++) {
    assert.equal(f.constant[l] >> BigInt(j) & 1n, slope(U[j], l));
    for (let a = 0; a < V.length; a++) {
      assert.equal(f.generators[a][l] >> BigInt(j) & 1n, BigInt(parity(dual[l] & physical(U[j]) & physical(V[a]))));
      sourceOperatorEntries++;
    }
    for (let h = 0; h < U.length; h++) assert.equal(parity(dual[l] & physical(U[j]) & physical(U[h])), 0);
  }
  const Wphysical = decode(schur.physical_pivot_directions_hex);
  assert.deepEqual(decode(schur.dual_code_rows_hex), dual);
  const products = Wphysical.flatMap(w => dual.map(b => b & w));
  assert.equal(schur.polar_variation_dimension, rank([...dual, ...products]) - n);
  assert.deepEqual(schur.individual_column_variation_dimensions, Wphysical.map(w => rank([...dual, ...dual.map(b => b & w)]) - n));
  const used = Wphysical.reduce((x, w) => x | w, 0n), outside = [];
  for (let i = 0; i < A[0].length; i++) if (!(used >> BigInt(i) & 1n)) outside.push(apply(dual, 1n << BigInt(i)));
  assert.equal(schur.unused_physical_columns_binary_rank, rank(outside));
  schurControls++;
}

for (const row of report.abstract_countercontrols) {
  const f = decodeFamily(row.operator_family);
  checkBlock(f, row.all_span_certificate); checkWeighted(f, row.weighted_radical_screen); checkSelected(f, row.selected_span_certificate);
}
for (const row of report.systematic_actual_packet_operator_profiles) {
  const f = decodeFamily(row.operator_family);
  checkPhysical(f, row.provenance, row.physical_code_schur_certificate);
  checkBlock(f, row.all_span_certificate); checkWeighted(f, row.weighted_radical_screen);
  checkSelected(f, row.first_basis_pivot_span_certificate);
}
const positive = report.native_correlated_positive_packet, positiveFamily = decodeFamily(positive.operator_family);
checkPhysical(positiveFamily, positive.provenance, positive.physical_code_schur_certificate);
checkSelected(positiveFamily, positive.certificate);
for (const [relative, digest] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, relative))).digest('hex'), digest);
}
assert.equal(report.claim_gate.full_growing_modulus_decoder_implemented, false);
console.log(JSON.stringify({status: 'BOUNDED_EXACT_CROSSCHECK_NOT_THEOREM_REVIEW',
  blockWitnesses, sourceOperatorEntries, weightedRadicals, backgroundControls, schurControls,
  dependencyHashes: Object.keys(report.dependency_sha256).length}, null, 2));

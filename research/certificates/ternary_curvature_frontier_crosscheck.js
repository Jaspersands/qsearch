"use strict";
// Exhaustive subspace optimality, independent basis transport and exact purity.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_curvature_frontier.json"), "utf8"));
function check(x, m) { if (!x) throw Error(m); }
function same(a, b, m) { check(JSON.stringify(a) === JSON.stringify(b), m); }
const mod = (x, q) => ((x % q) + q) % q;
function words(width) {
  let result = [[]];
  for (let i = 0; i < width; i++) result = result.flatMap(w => [0, 1, 2].map(x => [...w, x]));
  return result;
}
function combinations(N, k, start = 0) {
  if (!k) return [[]];
  return Array.from({length: N - start}, (_, j) => start + j).flatMap(i => combinations(N, k - 1, i + 1).map(t => [i, ...t]));
}
function subspaces(M) {
  const all = [];
  for (let k = 0; k <= M; k++) for (const pivots of combinations(M, k)) {
    const slots = pivots.flatMap((p, i) => Array.from({length: M - p - 1}, (_, j) => p + j + 1).filter(j => !pivots.includes(j)).map(j => [i, j]));
    for (const entry of words(slots.length)) {
      const basis = pivots.map(p => Array.from({length: M}, (_, j) => Number(j === p)));
      slots.forEach(([i, j], k) => { basis[i][j] = entry[k]; }); all.push(basis);
    }
  }
  return all;
}
const gram = (B, u, v) => mod(B.reduce((s, b, i) => s + b * u[i] * v[i], 0), 3);
const spaces = subspaces(4); check(spaces.length === 212, "entire F3 four-dimensional subspace census");
let pairs = 0, curvatureArrays = 0;
function bound(B) {
  const R = B.filter(Boolean).length, radical = B.length - R, twos = B.filter(x => x === 2).length;
  return radical + Math.floor(R / 2) - Number(R > 0 && R % 2 === 0 && (R / 2 + twos) % 2 !== 0);
}
for (const B of words(4)) {
  let maximum = 0;
  for (const S of spaces) { pairs++; if (S.every(u => S.every(v => gram(B, u, v) === 0))) maximum = Math.max(maximum, S.length); }
  check(maximum === bound(B), "entire-subspace sharp bound including anisotropic cases"); curvatureArrays++;
}
same([curvatureArrays, spaces.length, pairs], [report.scalar_optimality_census.curvature_arrays,
  report.scalar_optimality_census.all_F3_subspaces, report.scalar_optimality_census.curvature_subspace_pairs_checked], "census report");
function frequency(labels, L) {
  let u = -1, v = 1;
  for (let j = 2; j < L; j += 2) [u, v] = [u + v, -u];
  const q = 3 ** (L / 2);
  return labels.map(register => [register.map(([a, b]) => mod(u * a + v * b, q)), register.map(([a, b]) => mod((u + v) * a - u * b, q))]);
}
function value(f, w, q) { return f[0][0].map((_, j) => mod(w.reduce((s, x, i) => s + (x ? f[i][x - 1][j] : 0), 0), q)); }
function gateWord(word, gates) {
  word = [...word];
  for (const g of gates) {
    if (g.gate === "SWAP") [word[g.first], word[g.second]] = [word[g.second], word[g.first]];
    else if (g.gate === "SCALE_F3") word[g.target] = mod(word[g.target] * g.coefficient, 3);
    else { check(g.gate === "SUM_F3", "only explicit finite gates"); word[g.target] = mod(word[g.target] + g.coefficient * word[g.control], 3); }
  }
  return word;
}
let branchChecks = 0, amplitudeChecks = 0, originalWords = 0, nonzeroDefects = 0;
function sourceReplay(c) {
  const q = Number(c.original_modulus), f = frequency(c.native_labels, c.original_even_level), recipe = c.recipe, M = f.length, k = recipe.retained_width;
  const B = f.map(([a, b]) => a.map((x, j) => mod(x + b[j], 3)));
  same(B, c.curvatures, "original native curvature labels");
  const columns = recipe.inverse_columns.slice(0, k);
  same(columns, c.curvature_certificate.columns, "retained columns and compiler");
  for (let l = 0; l < f[0][0].length; l++) {
    const G = columns.map(u => columns.map(v => gram(B.map(x => x[l]), u, v)));
    same(G, c.curvature_certificate.component_Gram_matrices[l], "entire simultaneous curvature Gram");
    check(G.every(row => row.every(x => x === 0)), "low-affine component restriction");
  }
  const inverse = w => Array.from({length: M}, (_, i) => mod(recipe.inverse_columns.reduce((s, column, j) => s + column[i] * w[j], 0), 3));
  const phase = F => { const a = 2 * Math.PI * mod(F.reduce((s, x, j) => s + x * c.calibration_secret_only[j], 0), q) / q;
    return [Math.cos(a) / Math.sqrt(3 ** M), Math.sin(a) / Math.sqrt(3 ** M)]; };
  const actual = new Map();
  for (const w of words(M)) {
    const logical = gateWord(w, recipe.gates);
    same(logical, recipe.forward_matrix.map(row => mod(row.reduce((s, x, j) => s + x * w[j], 0), 3)), "explicit gates implement forward matrix");
    same(inverse(logical), w, "entire-word inverse bijection");
    check(!actual.has(logical.join(",")), "no aliased coordinate outputs"); actual.set(logical.join(","), phase(value(f, w, q))); originalWords++;
  }
  let total = 0;
  for (const branch of c.all_measured_pointer_branches) {
    const logicals = words(k), physical = logicals.map(z => inverse([...z, ...branch.pointer])), F = physical.map(w => value(f, w, q));
    same(physical, branch.physical_words, "all original branch words"); same(F, branch.original_frequency_table, "all original-root frequencies");
    same(F[0], branch.original_anchor_frequency, "unknown anchor phase retained");
    let probability = 0; const defects = [];
    for (let i = 0; i < logicals.length; i++) {
      const z = logicals[i], observed = actual.get([...z, ...branch.pointer].join(",")), expected = phase(F[i]);
      check(expected.every((x, j) => Math.abs(x - observed[j]) < 2e-12 && Math.abs(x - branch.branch_amplitudes[i][j]) < 2e-12), "independent full-root Born replay");
      probability += observed[0] ** 2 + observed[1] ** 2; amplitudeChecks++;
      const axis = z.map((x, j) => value(f, inverse([...Array.from({length: k}, (_, h) => h === j ? x : 0), ...branch.pointer]), q));
      const defect = F[i].map((x, l) => mod(x + (k - 1) * F[0][l] - axis.reduce((s, v) => s + v[l], 0), q));
      if (defect.some(Boolean)) { check(defect.every(x => x % 3 === 0), "curvature cancels, high-root defect remains"); defects.push({logical_word: z, mixed_frequency_defect: defect}); nonzeroDefects++; }
    }
    same(defects, branch.nonzero_mixed_phase_defects, "exact product-state falsifier");
    check(branch.componentwise_separable_for_all_secrets === (defects.length === 0), "source-wide product promise");
    check(Math.abs(probability - 3 ** (k - M)) < 2e-12 && Math.abs(probability - branch.probability) < 2e-12, "uniform all-outcome probability");
    total += probability; branchChecks++;
  }
  check(c.all_measured_pointer_branches.length === 3 ** (M - k) && Math.abs(total - 1) < 2e-12, "no postselection");
  check(!c.low_curvature_zero_implies_full_root_product && !c.recursive_source_law_or_speedup_supplied, "no unproved product/recursive law");
  check(!c.calibration_purity_is_an_unknown_secret_estimator && !c.identically_labeled_quantum_copies_for_SWAP_test_supplied, "no free purity oracle or identical copies");
  check(!recipe.unknown_state_preparation_inverse_or_cloning_required && recipe.coherent_pointer_unknown_anchor_phases_must_be_retained, "access/coherence scope");
}
sourceReplay(report.optimal_native_mixed_phase_countercontrol.source_control);
sourceReplay(report.native_zero_curvature_product_positive_control);
const larger = report.larger_original_source_retention_screen, fLarge = frequency(larger.native_labels, larger.original_even_level);
const BLarge = fLarge.map(([a, c]) => a.map((x, j) => mod(x + c[j], 3)));
same(BLarge, larger.curvatures, "larger original higher-root source labels");
const screens = larger.screen.scalar_direction_screens; let screenedBound = BLarge.length;
check(screens.length === larger.dimension ** 2, "polynomial basis-and-pair screen");
for (const c of screens) {
  const B = BLarge.map(v => mod(v.reduce((s, x, j) => s + x * c.direction[j], 0), 3)), maximum = bound(B);
  check(maximum === c.dimension_ledger.maximum_totally_isotropic_dimension, "independent scalar-combination necessary bound");
  screenedBound = Math.min(screenedBound, maximum);
}
check(screenedBound === larger.screen.simultaneous_isotropic_dimension_upper_bound, "best implemented necessary scalar gate");
check(larger.screen.public_F3_scalar_multiply_adds === BLarge.length * larger.dimension * screens.length, "public screening cost");
check(!larger.dense_quantum_output_replayed && !larger.simultaneous_frame_or_secret_estimator_supplied && !larger.screen.all_projective_directions_enumerated && !larger.screen.simultaneous_optimal_frame_constructed, "public necessary gate is not a quantum algorithm");
const frame = report.optimal_native_mixed_phase_countercontrol.frame;
check(frame.columns.length === bound(frame.curvatures) && frame.selection_reads_only_curvature, "optimal curvature frame but not independent outputs");
const branch = report.optimal_native_mixed_phase_countercontrol.source_control.all_measured_pointer_branches[0];
const table = branch.original_frequency_table.map(x => x[0]); let squaredGram = 0;
// Every row-pair phase difference, up to a common phase, is a cube root.
for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) {
  const delta = [0, 1, 2].map(j => mod(table[3 * a + j] - table[3 * b + j], 9)), counts = [0, 0, 0];
  for (const x of delta) { const e = mod(x - delta[0], 9); check(e % 3 === 0, "exact cube-root Gram reduction"); counts[e / 3]++; }
  const [u, v, w] = counts; squaredGram += u * u + v * v + w * w - u * v - u * w - v * w;
}
check(squaredGram === 57 && 57 * 27 === 19 * 81, "exact first-register purity19/27, strictly not product");
check(report.optimal_native_mixed_phase_countercontrol.zero_pointer_exact_first_logical_purity === "19/27", "reported exact purity");
check(!branch.componentwise_separable_for_all_secrets, "mixed-phase obstruction");
check(report.native_zero_curvature_product_positive_control.all_measured_pointer_branches.every(b => b.componentwise_separable_for_all_secrets), "positive product control not declared impossible");
let retentionDistributionTerms = 0;
for (const c of report.IID_width_frontiers) {
  const M = c.original_IID_even_inputs, denominator = 2n * 3n ** BigInt(M); let numerator = 0n, choose = 1n, power = 1n;
  for (let R = 0; R <= M; R++) {
    // Average both determinant types when R is positive and even.
    numerator += choose * power * BigInt(2 * M - R - Number(R > 0)); retentionDistributionTerms++;
    if (R < M) choose = choose * BigInt(M - R) / BigInt(R + 1);
    power *= 2n;
  }
  const fraction = c.exact_expected_maximum_low_affine_width.split("/").map(BigInt);
  check(numerator * (fraction[1] || 1n) === fraction[0] * denominator, "independent binomial-rank average of exact optimum");
  check(!c.this_step_certifies_full_root_product_states && !c.applying_the_same_IID_law_after_this_joint_step_certified && !c.arbitrary_coherent_decoder_lower_bound, "do not iterate IID/product assumptions without proof");
}
check(report.nonlinear_permutations_arbitrary_POVMs_or_coherent_junk_excluded_from_bound && !report.retention_screen_is_full_root_product_compiler, "specific linear-frontier scope");
check(!report.accepted_candidate && !report.polynomial_full_depth_decoder && !report.general_quantum_algorithm_lower_bound && !report.novelty_claim, "global claim gates");
process.stdout.write(JSON.stringify({status: "independent_replay_passed", curvature_subspace_pairs: pairs,
  full_root_branches: branchChecks, original_basis_words: originalWords, full_root_amplitudes: amplitudeChecks,
  exact_mixed_defects: nonzeroDefects, binomial_rank_terms: retentionDistributionTerms,
  exact_nonproduct_purity: "19/27", larger_scalar_direction_screens: screens.length,
  larger_necessary_retained_width: screenedBound, polynomial_full_depth_decoder: false}) + "\n");

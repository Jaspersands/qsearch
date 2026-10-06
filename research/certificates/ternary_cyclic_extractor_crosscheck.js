"use strict";
// Independent GF3 elimination and original-root basis replay; no Python import.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_cyclic_extractor.json"), "utf8"));
function check(x, message) { if (!x) throw Error(message); }
function same(a, b, message) { check(JSON.stringify(a) === JSON.stringify(b), message); }
const mod = (x, q) => ((x % q) + q) % q;
const sum = (vectors, indices) => vectors[0].map((_, j) => mod(indices.reduce((s, i) => s + vectors[i][j], 0), 3));
function words(width) {
  let result = [[]];
  for (let i = 0; i < width; i++) result = result.flatMap(w => [0, 1, 2].map(x => [...w, x]));
  return result;
}
function kernel(vectors) {
  const n = vectors[0].length, m = vectors.length, A = Array.from({length: n}, (_, j) => vectors.map(v => v[j]));
  const pivots = []; let row = 0;
  for (let col = 0; col < m && row < n; col++) {
    const found = A.findIndex((r, i) => i >= row && r[col] !== 0);
    if (found < 0) continue;
    [A[row], A[found]] = [A[found], A[row]];
    const inverse = A[row][col]; A[row] = A[row].map(x => mod(x * inverse, 3));
    for (let i = 0; i < n; i++) if (i !== row) {
      const c = A[i][col]; A[i] = A[i].map((x, j) => mod(x - c * A[row][j], 3));
    }
    pivots.push(col); row++;
  }
  const free = Array.from({length: m}, (_, i) => i).find(i => !pivots.includes(i));
  check(free !== undefined, "nonzero kernel needs a free column");
  const c = Array(m).fill(0); c[free] = 1;
  pivots.forEach((p, i) => { c[p] = mod(-A[i][free], 3); });
  check(c.some(Boolean), "nontrivial homogeneous witness");
  check(vectors[0].every((_, j) => mod(vectors.reduce((s, v, i) => s + c[i] * v[j], 0), 3) === 0), "independent GF3 kernel");
  return c;
}
function support(vectors) {
  const n = vectors[0].length, inner = [];
  for (let g = 0; g <= n; g++) {
    const ids = Array.from({length: n + 1}, (_, j) => g * (n + 1) + j);
    const c = kernel(ids.map(i => vectors[i])), U = ids.filter((_, j) => c[j] === 1), V = ids.filter((_, j) => c[j] === 2);
    if (!U.length || !V.length) return U.length ? U : V;
    inner.push([U, V]);
  }
  const common = inner.map(([U]) => sum(vectors, U)), c = kernel(common);
  const L = c.flatMap((x, i) => x === 1 ? [i] : []), R = c.flatMap((x, i) => x === 2 ? [i] : []);
  if (!L.length || !R.length) return (L.length ? L : R).flatMap(i => inner[i][0]).sort((a, b) => a - b);
  return [...L.flatMap(i => inner[i][0]), ...L.flatMap(i => inner[i][1]), ...R.flatMap(i => inner[i][0])].sort((a, b) => a - b);
}
let kernelCertificates = 0, nativeBranches = 0, curvaturePointers = 0, conditionalPairs = 0;
function witness(vectors, certificate) {
  const n = vectors[0].length;
  check(certificate.window_size === (n + 1) ** 2 && certificate.dimension === n, "guaranteed SDE window");
  vectors = vectors.slice(0, certificate.window_size);
  same(support(vectors), certificate.support, "independent support finder");
  for (const [g, r] of certificate.inner_relations.entries()) {
    same(r.indices, Array.from({length: n + 1}, (_, j) => g * (n + 1) + j), "group indices");
    same(kernel(r.indices.map(i => vectors[i])), r.coefficients, "inner kernel certificate");
    same(r.first_support, r.indices.filter((_, j) => r.coefficients[j] === 1), "first kernel support");
    same(r.second_support, r.indices.filter((_, j) => r.coefficients[j] === 2), "second kernel support");
    same(sum(vectors, r.first_support), sum(vectors, r.second_support), "equal inner sums");
    same(sum(vectors, r.first_support), r.common_vector, "inner common vector"); kernelCertificates++;
  }
  if (certificate.outer_relation) {
    const r = certificate.outer_relation;
    same(r.common_vectors, certificate.inner_relations.map(x => x.common_vector), "outer problem uses certified common vectors");
    same(kernel(r.common_vectors), r.coefficients, "outer kernel certificate"); kernelCertificates++;
    same(r.first_groups, r.coefficients.flatMap((x, i) => x === 1 ? [i] : []), "outer first groups");
    same(r.second_groups, r.coefficients.flatMap((x, i) => x === 2 ? [i] : []), "outer second groups");
    same(sum(r.common_vectors, r.first_groups), sum(r.common_vectors, r.second_groups), "outer equal sums");
    same(sum(r.common_vectors, r.first_groups), r.common_vector, "outer common vector");
  }
  if (certificate.four_disjoint_equal_sum_supports) {
    const blocks = certificate.four_disjoint_equal_sum_supports, ids = blocks.flat();
    check(blocks.every(b => b.length > 0) && new Set(ids).size === ids.length, "four disjoint nonempty sets");
    for (const b of blocks) same(sum(vectors, b), certificate.outer_relation.common_vector, "four equal sums");
    same(blocks.slice(0, 3).flat().sort((a, b) => a - b), certificate.support, "three equal sums give zero in F3");
  }
  check(certificate.support.length > 0 && new Set(certificate.support).size === certificate.support.length, "nonempty binary witness");
  check(sum(vectors, certificate.support).every(x => x === 0), "zero curvature sum");
  check(certificate.Gaussian_kernel_calls <= n + 2, "polynomial kernel call budget");
}
function frequencies(labels, level) {
  // Independent recurrence for the native even/odd trace normalization.
  let u = -1n, v = 1n;
  const even = level % 2 === 0;
  const start = even ? 2 : 1;
  if (!even) { u = 2n; v = -1n; }
  for (let j = start; j < level; j += 2) [u, v] = [u + v, -u];
  const q = 3n ** BigInt(Math.ceil(level / 2));
  return labels.map(register => [register.map(([a, b]) => Number(mod(u * BigInt(a) + v * BigInt(b), q))),
    register.map(([a, b]) => Number(mod((u + v) * BigInt(a) - u * BigInt(b), q)))]);
}
function value(f, w, q) { return f[0][0].map((_, j) => mod(w.reduce((s, x, i) => s + (x ? f[i][x - 1][j] : 0), 0), q)); }
function dense(control) {
  const f = frequencies(control.native_labels, control.native_level), q = 3 ** (control.native_level / 2);
  const B = f.map(([a, c]) => a.map((x, j) => mod(x + c[j], 3)));
  same(B, control.curvatures, "original native curvature source"); witness(B, control.support_certificate);
  const active = control.support_certificate.support, t = active.length, N = 3 ** t;
  check(t === control.active_inputs && control.inactive_inputs_untouched === f.length - t, "active/retained accounting");
  check(control.all_active_complement_branches.length === N / 3, "all pointer branches recorded");
  const phase = v => {
    const e = mod(v.reduce((s, a, j) => s + BigInt(a) * BigInt(control.calibration_secret_only[j]), 0n), BigInt(q));
    const angle = 2 * Math.PI * Number(e) / q; return [Math.cos(angle) / Math.sqrt(N), Math.sin(angle) / Math.sqrt(N)];
  };
  let total = 0;
  for (const branch of control.all_active_complement_branches) {
    const o = branch.output, anchor = Array(f.length).fill(0);
    active.slice(1).forEach((i, j) => { anchor[i] = branch.active_complement[j]; });
    const orbit = [0, 1, 2].map(j => anchor.map((x, i) => mod(x + (active.includes(i) ? j : 0), 3)));
    same(orbit, o.orbit_words, "inverse coordinate map on original words");
    const F = orbit.map(w => value(f, w, q));
    const relative = [1, 2].map(k => F[k].map((x, j) => mod(x - F[0][j], q)));
    same(relative, [o.relative_first, o.relative_second], "original-root phase differences");
    same(F[0], o.original_pivot_phase_frequency, "coherent anchor phase retained");
    const outputF = frequencies([o.native_odd_output_labels], control.native_level - 1)[0];
    same(outputF, relative, "native odd label chart, not a field shadow");
    check(o.output_modulus === String(q) && o.original_modulus === String(q), "same full phase root");
    check(!o.field_shadow_replacement && !o.pivot_phase_can_be_dropped_in_coherent_pointer_mode, "source/coherence guard");
    check(o.IID_source_promise_requires_curvature_only_support_selection && !o.mask_choice_policy_verified_by_this_low_level_function, "mask provenance scope");
    const recipe = o.resources;
    same(recipe.active_support, active, "active recipe");
    same(recipe.measure_only_active_complement, active.slice(1), "measure only complements");
    same(recipe.inactive_original_registers_untouched, Array.from({length: f.length}, (_, i) => i).filter(i => !active.includes(i)), "inactive original wires");
    same(recipe.gates, active.slice(1).map(i => ({gate: "SUM_inverse_F3", control: active[0], target: i})), "explicit SUM recipe");
    check(recipe.accepted_outcomes === "ALL" && recipe.acceptance_probability === "1" && !recipe.unknown_inverse_cloning_or_postselection_required, "no free inverse or postselection");
    // Pull amplitudes through the algebraic inverse permutation, including anchor phases.
    for (let j = 0; j < 3; j++) {
      const expected = phase(F[j]), actual = branch.branch_amplitudes[j];
      check(expected.every((x, k) => Math.abs(x - actual[k]) < 2e-12), "independent full-root amplitude replay");
    }
    const probability = branch.branch_amplitudes.reduce((s, [a, b]) => s + a * a + b * b, 0);
    check(Math.abs(probability - 3 / N) < 2e-12 && Math.abs(probability - branch.probability) < 2e-12, "flat pointer Born probabilities");
    total += probability; nativeBranches++;
  }
  check(Math.abs(total - 1) < 2e-12, "no outcomes discarded");
}
for (const c of report.native_dense_gate_controls) dense(c);
for (const B of words(4)) {
  const vectors = B.map(x => [x]), active = support(vectors), pivot = active[0];
  check(active.length > 0 && mod(active.reduce((s, i) => s + B[i], 0), 3) === 0, "all curvature inputs have a binary zero sum");
  for (const pointer of words(active.length - 1)) {
    const anchor = Array(4).fill(0); active.slice(1).forEach((i, j) => { anchor[i] = pointer[j]; });
    const counts = new Map();
    for (const [a0, ha, hc] of words(3)) {
      const a = Array(4).fill(0), c = [...B]; a[pivot] = a0 + 3 * ha; c[pivot] = mod(B[pivot] - a0, 3) + 3 * hc;
      const F = [0, 1, 2].map(j => mod(active.reduce((s, i) => {
        const x = mod(anchor[i] + j, 3); return s + (x === 1 ? a[i] : x === 2 ? c[i] : 0);
      }, 0), 9));
      const A = mod(F[1] - F[0], 9), C = mod(F[2] - F[0], 9);
      check(mod(C - 2 * A, 3) === 0, "native odd promise");
      const key = `${A},${C}`; counts.set(key, (counts.get(key) || 0) + 1); conditionalPairs++;
    }
    check(counts.size === 27 && [...counts.values()].every(x => x === 1), "conditional uniform law includes zero tangent"); curvaturePointers++;
  }
}
same([curvaturePointers, conditionalPairs], [report.conditional_exact_source_census.all_active_pointer_strata, report.conditional_exact_source_census.frequency_pairs_evaluated], "full conditional census");
const large = report.larger_recyclable_native_control, f = frequencies(large.native_labels, large.native_level);
same(f.map(([a, c]) => a.map((x, j) => mod(x + c[j], 3))), large.curvatures, "larger original source");
let remaining = Array.from({length: f.length}, (_, i) => i);
for (const child of large.result.outputs) {
  same(child.window_original_indices, remaining.slice(0, (large.dimension + 1) ** 2), "recycling reads only surviving curvatures");
  witness(child.window_original_indices.map(i => large.curvatures[i]), child.certificate);
  same(child.support, child.certificate.support.map(i => child.window_original_indices[i]), "original consumed input IDs");
  check(child.support.every(i => remaining.includes(i)), "no quantum input reused");
  remaining = remaining.filter(i => !child.support.includes(i));
}
same(remaining, large.result.retained_original_registers, "all untouched original inputs accounted");
check(large.result.output_count === large.result.outputs.length && large.result.output_count >= Math.floor(f.length / (large.dimension + 1) ** 2), "worst-case yield");
check(!large.result.retained_curvature_labels_claimed_IID, "do not infer fresh IID curvatures from recycling");
for (const c of report.one_output_recursion_gates) {
  check(BigInt(c.minimum_one_output_protocol_original_copies) === BigInt(c.dimension + 1) ** BigInt(c.root_digits - 1), "one-output copy loss");
  check(BigInt(c.fresh_batch_protocol_copies_for_one_final_field_qutrit) === BigInt(c.dimension + 1) ** BigInt(3 * (c.root_digits - 1)), "fresh-batch cost");
  check(c.coherent_pointer_or_multi_output_phase_transducers_excluded_from_lower_bound && c.inactive_register_recycling_is_included_in_lower_bound, "lower-bound scope");
  check(!c.polynomial_in_r_complete_speedup_claim_allowed, "acceptance1 is not polynomial root-depth throughput");
}
check(!report.accepted_candidate && !report.new_polynomial_full_depth_quantum_algorithm && !report.novelty_claim && !report.general_corner1_incoming_oracle_supplied, "global claim guards");
process.stdout.write(JSON.stringify({status: "independent_replay_passed", native_full_root_branches: nativeBranches,
  Gaussian_kernel_certificates: kernelCertificates, curvature_pointer_strata: curvaturePointers,
  conditional_native_frequency_pairs: conditionalPairs, recycled_children: large.result.output_count,
  new_polynomial_full_depth_quantum_algorithm: false}) + "\n");

"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const check = (x, m) => { if (!x) throw Error(m); }, key = JSON.stringify, same = (a, b, m) => check(key(a) === key(b), m);
const B = x => { check(typeof x === "string" || typeof x === "bigint" || Number.isSafeInteger(x), "exact serialized integer"); return BigInt(x); };
const mod = (a, q) => (a % q+q) % q, abs = a => a < 0n ? -a : a;
function gcd(a, b) { a = abs(a); b = abs(b); while (b) [a, b] = [b, a % b]; return a; }
function F(a, b = 1n) { if (b < 0n) { a = -a; b = -b; } check(b !== 0n, "nonzero denominator"); const g = gcd(a, b); return [a/g, b/g]; }
const add = (a, b) => F(a[0]*b[1]+b[0]*a[1], a[1]*b[1]);
const sub = (a, b) => F(a[0]*b[1]-b[0]*a[1], a[1]*b[1]);
const mul = (a, b) => F(a[0]*b[0], a[1]*b[1]);
const div = (a, b) => F(a[0]*b[1], a[1]*b[0]);
const str = a => a[1] === 1n ? String(a[0]) : a[0]+"/"+a[1];
function floor(a, b) { const c = a/b; return a < 0n && a % b ? c-1n : c; }
const round = a => floor(2n*a[0]+a[1], 2n*a[1]);
const dot = (a, b) => a.reduce((s, x, i) => s+x*b[i], 0n);
function inverse(a, q) { let t = 0n, u = 1n, b = q; a = mod(a, q); while (a) { const c = b/a; [t, u] = [u, t-c*u]; [b, a] = [a, b-c*a]; } check(b === 1n, "unit target coefficient"); return mod(t, q); }
function sparse(rows, width) {
  return rows.map(row => { let old = -1; const m = new Map(); for (const [j, x] of row) { check(Number.isInteger(j) && j > old && j < width && B(x) !== 0n, "all nonzero sparse entries canonical"); m.set(j, B(x)); old = j; } return m; });
}
function dense(rows, width) { return rows.map(row => Array.from({length: width}, (_, j) => row.get(j) || 0n)); }
function determinant(rows) {
  rows = rows.map(row => new Map([...row].map(([j, x]) => [j, F(x)]))); let answer = F(1n);
  for (let k = 0; k < rows.length; k++) {
    const p = rows.findIndex((row, i) => i >= k && row.has(k)); check(p >= 0, "nonsingular exact transform");
    if (p !== k) { [rows[k], rows[p]] = [rows[p], rows[k]]; answer[0] = -answer[0]; }
    const pivot = rows[k].get(k); answer = mul(answer, pivot);
    for (let i = k+1; i < rows.length; i++) if (rows[i].has(k)) {
      const factor = div(rows[i].get(k), pivot);
      for (const [j, x] of rows[k]) if (j > k) { const value = sub(rows[i].get(j) || F(0n), mul(factor, x)); if (value[0]) rows[i].set(j, value); else rows[i].delete(j); }
      rows[i].delete(k);
    }
  }
  check(answer[1] === 1n, "integer transform determinant"); return answer[0];
}
function transform(U, H, R) {
  check(U.length === H.length && R.length === H.length, "complete basis transform shape");
  check(abs(determinant(U)) === 1n, "exact unimodularity");
  for (let i = 0; i < U.length; i++) {
    const out = new Map();
    for (const [j, x] of U[i]) for (const [k, y] of H[j]) out.set(k, (out.get(k) || 0n)+x*y);
    for (const [j, x] of out) if (!x) out.delete(j);
    check(out.size === R[i].size && [...out].every(([j, x]) => R[i].get(j) === x), "full sparse integer transform identity");
  }
}
function profile(R, width) {
  const columns = Array.from({length: width}, () => []), G = R.map(() => new Map());
  R.forEach((row, i) => [...row].forEach(([j, x]) => columns[j].push([i, x])));
  for (const col of columns) for (const [i, x] of col) for (const [j, y] of col) if (j <= i) G[i].set(j, (G[i].get(j) || 0n)+x*y);
  const mu = [], gs = []; let determinant = F(1n);
  for (let i = 0; i < R.length; i++) {
    const row = new Map();
    for (let j = 0; j < i; j++) {
      let v = F(G[i].get(j) || 0n);
      for (const [k, x] of row) if (mu[j].has(k)) v = sub(v, mul(mul(x, mu[j].get(k)), gs[k]));
      if (v[0]) row.set(j, div(v, gs[j]));
    }
    let norm = F(G[i].get(i) || 0n); for (const [j, x] of row) norm = sub(norm, mul(mul(x, x), gs[j]));
    check(norm[0] > 0n, "positive exact Euclidean profile"); mu.push(row); gs.push(norm); determinant = mul(determinant, norm);
  }
  return {mu, gs, determinant};
}
function score(records, candidate, q) {
  let value = 0, loss = 0, cost = 0n;
  for (const rec of records) {
    const e = [rec.first, rec.second].map((row, i) => mod(B(rec.outcome[i])-dot(row.map(B), candidate.map(B)), q));
    const centered = e.map(x => mod(x+q/2n, q)-q/2n); cost += dot(centered, centered);
    for (const x of [e[0], e[1], e[0]-e[1]]) { const a = Math.PI*Number(mod(x+q/2n, q)-q/2n)/Number(q); value += Math.cos(2*a); loss += Math.sin(a)**2; }
  }
  return {score: value/records.length, loss: loss/records.length, cost};
}
function verify(r) {
check(r.status === "FULL_RECORD_NATIVE_CVP_ATTEMPT_REVIEW_PENDING" && !r.near_exact_CVP_solver_implemented && !r.classical_source_dequantization_or_hardness_proved && !r.accepted_speedup_candidate, "heuristic attempt, no granted solver");
check(r.derivation_sha256 === crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname, "../TERNARY_FULL_RECORD_CVP.md"))).digest("hex"), "pinned optimizer derivation");
same(r.controls.map(c => [c.n, c.root_digits, c.density_per_n_r, c.seed]), [[2, 2], [2, 8], [4, 8], [8, 8]].flatMap(([n, p]) => [4, 8].map(d => [n, p, d, 97200+100*n+10*p+d])), "precommitted full-record regimes");
let paths = 0, reductions = 0, embeddingCandidates = 0, largest = 0, counterexamples = 0; const recoveries = {Euclidean: 0, native_likelihood: 0};
for (const c of r.controls) {
  const n = c.n, q = 3n**BigInt(c.root_digits), M = c.density_per_n_r*n*c.root_digits, m = 2*M, d = c.decoder, model = d.model;
  check(c.training_records.length === M && c.heldout_records.length === 512 && c.original_training_plus_fresh_qutrits === M+512 && B(c.modulus) === q, "complete original measured cohorts");
  check(!c.native_law_simulation_supplies_unknown_quantum_states && !c.bounded_trials_are_population_theorem && !c.meets_conservative_CVP_population_copy_budget, "bounded native-law simulation, not theorem-budget guarantee");
  check(d.status === "FULL_COHORT_LATTICE_PROPOSALS_ONLY" && d.all_original_records_in_optimization && !d.matrix_selected_using_hidden_secret && !d.Gaussian_error_promise && !d.near_exact_CVP_guarantee && !d.failure_proves_hardness && !d.accepted_speedup_candidate, "scientific optimizer scope");
  check(new Set(d.source_IDs).size === M && new Set(c.heldout_source_IDs).size === 512 && !c.heldout_source_IDs.some(x => d.source_IDs.includes(x)), "distinct and fresh original IDs");
  const A = c.training_records.flatMap(x => [x.first, x.second]).map(row => row.map(B)), y = c.training_records.flatMap(x => x.outcome).map(B);
  check(model.status === "EXACT_PUBLIC_CODE_LATTICE" && model.secret_dimension === n && model.lattice_equations === m && B(model.modulus) === q && B(model.lattice_index) === q**BigInt(m-n) && !model.basis_reads_outcomes && !model.Gaussian_error_promise, "whole systematic code lattice");
  check(A.length === model.frequency_rows.length && A.every((row, i) => row.every((x, j) => B(model.frequency_rows[i][j]) === x)), "full-root observed labels");
  const piv = model.unit_basis_rows, inv = model.unit_basis_inverse.map(row => row.map(B));
  check(piv.length === n && new Set(piv).size === n, "full unit basis");
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) check(mod(piv.map(k => A[k])[i].reduce((s, x, k) => s+x*inv[k][j], 0n), q) === BigInt(i === j), "exact lifted inverse");
  const axes = Array.from({length: m}, (_, j) => j).filter(j => !piv.includes(j)); same(model.nonpivot_axis_indices, axes, "all q-axis generators retained");
  const H = model.code_generator_rows.map(row => new Map(row.map(B).flatMap((x, j) => x ? [[j, x]] : [])));
  for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) { const v = mod(A[j].reduce((s, x, k) => s+x*inv[k][i], 0n)+q/2n, q)-q/2n; check((H[i].get(j) || 0n) === v, "exact centered code generators"); }
  H.push(...axes.map(j => new Map([[j, q]]))); check(H.length === m, "complete basis, not sublattice");
  const R = sparse(d.reduced_rows_sparse, m), U = sparse(d.transform_sparse, m); transform(U, H, R); reductions++;
  const p = profile(R, m); check(p.determinant[1] === 1n && p.determinant[0] === q**BigInt(2*(m-n)), "exact sparse GS completeness and determinant");
  function extract(point) { const values = piv.map(j => point[j]), s = inv.map(row => mod(dot(row, values), q)); check(A.every((row, j) => mod(dot(row, s)-point[j], q) === 0n), "every point obeys all original modular equations"); return s.map(Number); }
  const influence = d.rounding_influence_certificate, rowSecrets = dense(R, m).map(extract), live = [], parents = [];
  for (let i = 0; i < m; i++) { const parent = [...p.mu[i].keys()].sort((a, b) => a-b).find(j => live[j]); parents.push(parent === undefined ? null : parent); live.push(rowSecrets[i].some(Boolean) || parent !== undefined); }
  same(influence.row_code_secrets, rowSecrets, "actual code secret of EVERY reduced basis row");
  same(influence.influential_rounding_positions, live.flatMap((x, i) => x ? [i] : []), "complete GS dependency influence closure");
  same(influence.dead_rounding_positions, live.flatMap((x, i) => x ? [] : [i]), "only exact dead positions pruned");
  same(influence.earlier_influential_parent, parents, "exact earlier-parent influence witnesses");
  check(influence.any_dead_only_repair_preserves_secret_for_every_target && !influence.zero_mod_q_rows_can_be_discarded_without_GS_dependencies && !influence.influence_claims_recovery_or_approximation_guarantee, "scope: exact code-class compiler, not recovery claim");
  const inner = [], initial = [];
  for (let i = 0; i < m; i++) { let v = F([...R[i]].reduce((s, [j, x]) => s+x*y[j], 0n)); for (const [j, x] of p.mu[i]) v = sub(v, mul(x, inner[j])); inner.push(v); initial.push(div(v, p.gs[i])); }
  const discovered = new Map(); check(d.repair_paths.length === 33, "precommitted complete finite repair list");
  d.repair_paths.forEach((a, index) => {
    const repair = a.public_repair; check(repair.length === m && repair.every(x => [-1, 0, 1].includes(x)), "complete signed repair");
    check(index ? repair.filter(Boolean).length >= 1 && repair.filter(Boolean).length <= 4 : repair.every(x => !x), "Babai and public one-to-four-coordinate menu");
    const coords = initial.map(x => [...x]), coeff = Array(m).fill(0n);
    for (let i = m-1; i >= 0; i--) { coeff[i] = round(coords[i])+BigInt(repair[i]); for (const [j, x] of p.mu[i]) coords[j] = sub(coords[j], mul(F(coeff[i]), x)); }
    check(a.coefficients.length === m && coeff.every((x, j) => B(a.coefficients[j]) === x), "independent exact repaired rounding");
    const point = Array(m).fill(0n); coeff.forEach((x, i) => { if (x) for (const [j, v] of R[i]) point[j] += x*v; });
    check(a.point.length === m && point.every((x, j) => B(a.point[j]) === x), "complete repair lattice point");
    const s = extract(point); same(a.candidate, s, "actual lattice-derived candidate");
    check(B(a.supplied_Euclidean_cost) === point.reduce((v, x, j) => v+(y[j]-x)**2n, 0n), "true Euclidean supplied-point cost"); discovered.set(key(s), s); paths++;
  });
  same(d.embedding_runs.map(x => x.scale), [Number(q/4n), Number(q/2n)], "fixed public embedding scales");
  for (const e of d.embedding_runs) {
    const scale = B(e.scale), EH = [...H.map(row => new Map(row)), new Map([...y.flatMap((x, j) => x ? [[j, x]] : []), [m, scale]])], ER = sparse(e.rows_sparse, m+1), EU = sparse(e.transform_sparse, m+1);
    transform(EU, EH, ER); reductions++;
    check(e.unit_coefficients_beyond_plus_minus_one_are_modular_trials_only && !e.bounded_distance_promise_or_near_exact_factor_proved, "embedding extraction scope");
    const seen = new Set();
    for (const a of e.candidates) {
      check(!seen.has(a.row), "embedding row classified once"); seen.add(a.row);
      const row = ER[a.row], tail = row.get(m) || 0n; check(tail % scale === 0n, "integer target coefficient"); const k = tail/scale;
      check(gcd(k, q) === 1n && B(a.target_coefficient) === k, "unit-coefficient modular extraction");
      const point = y.map((x, j) => (row.get(j) || 0n)-k*x); check(a.code_lattice_point.every((x, j) => B(x) === point[j]), "actual embedding code point");
      const base = extract(point), s = base.map(x => Number(mod(-inverse(k, q)*BigInt(x), q)));
      same(a.candidate, s, "unit modular trial, no division oracle"); check(a.literal_CVP_error_vector === (abs(k) === 1n), "signed-unit versus general-unit distinction");
      discovered.set(key(s), s); embeddingCandidates++;
    }
    for (const a of e.rejected_rows) { check(!seen.has(a.row), "nonunit row classified once"); seen.add(a.row); const tail = ER[a.row].get(m) || 0n; check(tail % scale === 0n && B(a.coefficient) === tail/scale && gcd(tail/scale, q) !== 1n && a.reason === "NONUNIT_TARGET_COEFFICIENT", "all nonunit row reasons"); }
    check(seen.size === m+1, "all embedding rows accounted, no favorable filtering");
  }
  same(d.proposal_scores.map(x => key(x.candidate)).sort(), [...discovered.keys()].sort(), "all and only real proposals");
  const scores = new Map();
  for (const a of d.proposal_scores) { const v = score(c.training_records, a.candidate, q); check(B(a.Euclidean_cost) === v.cost && Math.abs(a.native_score-v.score) < 3e-11 && Math.abs(Number(a.native_loss)-v.loss) < 3e-11, "actual native and Euclidean objectives"); scores.set(key(a.candidate), v); }
  const chosen = new Set(Object.values(d.selections).map(key));
  for (const [name, s] of Object.entries(d.selections)) {
    const v = scores.get(key(s)); check(v && [...scores.values()].every(w => name === "Euclidean" ? v.cost <= w.cost : v.loss <= w.loss+2e-12), "training-only objective choice");
    const fresh = score(c.heldout_records, s, q), a = c.verification[name]; same(a.candidate, s, "frozen selection verified unchanged");
    check(Math.abs(a.fresh_score-fresh.score) < 3e-11 && a.threshold_passed === (fresh.score >= .5) && a.calibration_recovered === (key(s) === key(c.calibration_secret)), "fresh verification and truth diagnostic only"); recoveries[name] += Number(a.calibration_recovered);
  }
  const gate = c.joint_fixed_candidate_gate; check(gate.tested_candidates === chosen.size && gate.fresh_native_qutrit_records === 512 && Math.abs(gate.false_acceptance_union_bound_approximation-Math.min(1, chosen.size*Math.exp(-1024/81))) < 1e-12, "joint distinct frozen-candidate multiplicity charged");
  const trueValue = score(c.training_records, c.calibration_secret, q); check(B(c.true_Euclidean_cost_diagnostic) === trueValue.cost && c.true_cost_within_q_over_two_BDD_radius === (4n*trueValue.cost <= q*q), "actual source BDD diagnostic");
  const certificate = c.CVP_comparison_certificate, point = certificate.public_valid_lattice_point.map(B), witnessSecret = extract(point);
  same(certificate.public_point_secret, witnessSecret, "public comparison point membership, not assumed optimality");
  const W = point.reduce((v, x, j) => v+(y[j]-x)**2n, 0n), C = [...scores.values()].reduce((v, x) => v === null || x.cost < v ? x.cost : v, null), margin = 64n*C-81n*W;
  check(B(certificate.valid_point_squared_distance) === W && B(certificate.best_all_generated_candidates_squared_distance) === C && B(certificate.strict_integer_factor_failure_margin) === margin && certificate.norm_9_over_8_approximation_falsified_on_this_instance === (margin > 0n) && !certificate.globally_nearest_point_or_true_secret_optimality_assumed && !certificate.comparison_truth_supplied_to_decoder && certificate.comparison_witness_is_posthoc_not_population_hardness, "exact source-specific finite9/8 approximation counterexample");
  counterexamples += Number(margin > 0n);
  const delta = sub(F(4n, 81n), F(1n, BigInt(4*M))), exponent = delta[0] > 0n ? mul(F(BigInt(8*M)), mul(delta, delta)) : F(0n), bdd = d.BDD_gate;
  check(B(bdd.shortest_lattice_vector_length_upper) === q && bdd.true_secret_BDD_squared_distance_necessary_upper === str(F(q*q, 4n)) && bdd.Hoeffding_lower_tail_exponent === str(exponent) && !bdd.Gaussian_or_BDD_source_promise_granted && !bdd.general_CVP_or_quantum_receiver_impossibility, "scoped BDD-promise gate");
  check(d.cost.original_measured_qutrits === M && d.cost.lattice_dimension === m && d.cost.LLL_calls === 3 && d.cost.exact_repair_paths === 33 && d.cost.exact_rounding_steps === 33*m && d.cost.distinct_candidates_scored === discovered.size && !d.cost.secret_or_root_value_enumeration, "complete optimizer cost ledger");
  largest = Math.max(largest, m);
}
return {status: "PASS", full_cohorts: r.controls.length, largest_lattice_dimension: largest, exact_repair_paths: paths, exact_unimodular_reductions: reductions, modular_embedding_candidates: embeddingCandidates, recoveries, exact_9_over_8_counterexamples: counterexamples, near_exact_CVP_guarantee: false};
}
module.exports = {B, F, add, sub, mul, div, str, round, dot, mod, check, same, sparse, dense, profile, score, verify};
if (require.main === module) {
  const r = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../classical_baselines/ternary_full_record_cvp.json"), "utf8"));
  console.log(JSON.stringify(verify(r), null, 2));
}

"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../classical_baselines/ternary_measured_lattice_decoder.json"), "utf8"));
const check = (x, message) => { if (!x) throw Error(message); };
const key = JSON.stringify, same = (a, b, m) => check(key(a) === key(b), m);
const mod = (a, q) => (a % q + q) % q;
const B = x => { check(typeof x === "bigint" || typeof x === "string" || Number.isSafeInteger(x), "exact certificate integer encoding"); return BigInt(x); };
const abs = x => x < 0n ? -x : x;
function gcd(a, b) { a = abs(a); b = abs(b); while (b) [a, b] = [b, a % b]; return a; }
function F(a, b = 1n) { check(b !== 0n, "nonzero rational denominator"); if (b < 0n) { a = -a; b = -b; } const g = gcd(a, b); return [a/g, b/g]; }
const add = (a, b) => F(a[0]*b[1]+b[0]*a[1], a[1]*b[1]);
const sub = (a, b) => F(a[0]*b[1]-b[0]*a[1], a[1]*b[1]);
const mul = (a, b) => F(a[0]*b[0], a[1]*b[1]);
const div = (a, b) => F(a[0]*b[1], a[1]*b[0]);
function floor(a, b) { const q = a/b; return a < 0n && a % b ? q-1n : q; }
const round = a => floor(2n*a[0]+a[1], 2n*a[1]);
const dot = (a, b) => a.reduce((s, x, i) => s+x*b[i], 0n);
function det(rows) {
  const a = rows.map(row => row.map(B)); let previous = 1n, sign = 1n;
  for (let k = 0; k < a.length-1; k++) {
    const p = a.findIndex((row, i) => i >= k && row[k] !== 0n);
    if (p < 0) return 0n;
    if (p !== k) { [a[k], a[p]] = [a[p], a[k]]; sign = -sign; }
    const pivot = a[k][k];
    for (let i = k+1; i < a.length; i++) for (let j = k+1; j < a.length; j++) {
      const value = a[i][j]*pivot-a[i][k]*a[k][j];
      check(value % previous === 0n, "integer Bareiss determinant division"); a[i][j] = value/previous;
    }
    for (let i = k+1; i < a.length; i++) a[i][k] = 0n;
    previous = pivot;
  }
  return sign*a[a.length-1][a.length-1];
}
const multiply = (a, b) => a.map(row => b[0].map((_, j) => row.reduce((s, x, i) => s+x*b[i][j], 0n)));
const equalBig = (a, b, m) => check(a.length === b.length && a.every((row, i) => row.length === b[i].length && row.every((x, j) => B(x) === B(b[i][j]))), m);
function embed(row) { check(row.length % 2 === 0, "whole paired metric"); return row.flatMap((x, i) => i % 2 ? [] : [B(x), B(row[i+1]), B(x)-B(row[i+1])]); }
function unembed(row) { const x = row.map(B); check(x.length % 3 === 0, "embedded dimension"); const result = []; for (let i = 0; i < x.length; i += 3) { check(x[i]-x[i+1] === x[i+2], "metric subspace cleanup"); result.push(x[i], x[i+1]); } return result; }
function profile(rows) {
  const n = rows.length, a = rows.map(left => rows.map(right => dot(left, right)));
  const mu = rows.map(() => rows.map(() => F(0n))), gs = []; let previous = 1n;
  for (let k = 0; k < n; k++) {
    const pivot = a[k][k]; check(pivot > 0n, "positive exact metric profile"); gs.push(F(pivot, previous));
    for (let j = k+1; j < n; j++) mu[j][k] = F(a[k][j], pivot);
    for (let i = k+1; i < n; i++) for (let j = i; j < n; j++) {
      const value = pivot*a[i][j]-a[i][k]*a[k][j]; check(value % previous === 0n, "exact metric GS division"); a[i][j] = a[j][i] = value/previous;
    }
    previous = pivot;
  }
  return {mu, gs, gram: previous};
}
function roundPaths(rows, target, p) {
  const inner = [], initial = [];
  for (let i = 0; i < rows.length; i++) {
    let value = F(dot(rows[i], target)); for (let j = 0; j < i; j++) value = sub(value, mul(p.mu[i][j], inner[j]));
    inner.push(value); initial.push(div(value, p.gs[i]));
  }
  const menu = [[null, 0], ...rows.flatMap((_, j) => [[rows.length-1-j, -1], [rows.length-1-j, 1]])];
  return menu.map(([forced, deviation]) => {
    const coords = initial.map(x => [...x]), coefficients = rows.map(() => 0n);
    for (let i = rows.length-1; i >= 0; i--) {
      coefficients[i] = round(coords[i])+BigInt(i === forced ? deviation : 0);
      for (let j = 0; j < i; j++) coords[j] = sub(coords[j], mul(F(coefficients[i]), p.mu[i][j]));
    }
    const point = rows[0].map((_, j) => rows.reduce((s, row, i) => s+coefficients[i]*row[j], 0n));
    return {forced, deviation, coefficients, point};
  });
}
function canonicalRecord(r, n, q) {
  check(B(r.modulus) === q && r.first.length === n && r.second.length === n && r.outcome.length === 2, "original full-root record shape");
  check([...r.first, ...r.second, ...r.outcome].every(x => B(x) >= 0n && B(x) < q), "canonical full-root values");
}
function nativeValues(records, candidate, q) {
  let score = 0, loss = 0;
  for (const r of records) {
    const e = [r.first, r.second].map((row, j) => mod(B(r.outcome[j])-dot(row.map(B), candidate.map(B)), q));
    const xs = [e[0], e[1], e[0]-e[1]];
    for (const x of xs) {
      const centered = mod(x+q/2n, q)-q/2n, angle = Math.PI*Number(centered)/Number(q);
      loss += Math.sin(angle)**2; score += Math.cos(2*angle);
    }
  }
  return {score: score/records.length, loss: loss/records.length};
}
check(report.status === "FULL_ROOT_PAIRED_LATTICE_BASELINE_REVIEW_PENDING" && !report.population_or_asymptotic_recovery_theorem && !report.classical_simulation_of_original_quantum_inputs && !report.failure_implies_classical_hardness && !report.accepted_speedup_candidate, "attack scope, not source simulation or hardness");
check(report.derivation_sha256 === crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname, "../TERNARY_MEASURED_LATTICE_DECODER.md"))).digest("hex"), "pinned scientific derivation");
same(report.controls.map(c => [c.n, c.root_digits, c.seed]), [2, 4, 8].flatMap(n => [2, 8].flatMap(r => [0, 1].map(k => [n, r, 95200+100*n+10*r+k]))), "precommitted dimension/root/seed menu");
let pathCount = 0, latticeCount = 0, reductionCount = 0, recoveries = 0, passes = 0;
for (const c of report.controls) {
  const n = c.n, q = 3n**BigInt(c.root_digits), d = c.decoder, records = c.training_records;
  check(B(c.modulus) === q && records.length === 96 && c.heldout_records.length === 512 && c.training_plus_fresh_original_qutrits === 608, "charged original train/fresh supply");
  [...records, ...c.heldout_records].forEach(r => canonicalRecord(r, n, q));
  check(new Set(c.training_IDs).size === 96 && new Set(c.heldout_IDs).size === 512 && !c.heldout_IDs.some(x => c.training_IDs.includes(x)), "source IDs distinct and held-out disjoint");
  check(c.records_are_native_law_simulation_not_unknown_source_supply && !c.bounded_success_is_asymptotic_recovery && !d.training_secret_or_heldout_used && !d.asymptotic_recovery_proved && !d.failure_proves_classical_hardness && !d.native_quantum_source_simulated && !d.accepted_speedup_candidate && d.native_score_selected_via_stable_equivalent_sine_loss && !d.score_ordering_has_certified_interval_precision, "no hidden source or recovery theorem");
  same(d.cases.map(x => x.subset), d.subset_schedule, "complete public subset schedule");
  const discovered = new Map(); let paths = 0, reductions = 0, roundingSteps = 0;
  for (const cs of d.cases) {
    const selected = cs.subset.map(i => records[i]), m = 2*selected.length, model = cs.model;
    check(cs.subset.every(i => Number.isInteger(i) && i >= 0 && i < records.length) && new Set(cs.subset).size === cs.subset.length && m <= 32, "complete whole-pair subsets within cap");
    same(cs.source_IDs, cs.subset.map(i => c.training_IDs[i]), "subset ancestry retained");
    const A = selected.flatMap(r => [r.first, r.second]).map(row => row.map(B));
    if (model.status === "UNKNOWN_NO_UNIT_ROW_BASIS") { check(cs.reductions.length === 0 && cs.attempts.length === 0, "rank failure retained without partial decoder"); continue; }
    check(model.status === "EXACT_PUBLIC_PAIRED_CODE_LATTICE" && model.secret_dimension === n && B(model.modulus) === q && model.lattice_equations === m && model.ambient_metric_dimension === 3*selected.length && !model.basis_reads_outcomes && !model.Gaussian_error_promise, "whole exact native lattice model");
    equalBig(model.frequency_rows, A, "actual full labels, not field shadows");
    const pivots = model.unit_basis_rows, inv = model.unit_basis_inverse.map(row => row.map(B));
    check(pivots.length === n && new Set(pivots).size === n, "complete unit row basis");
    const BI = multiply(pivots.map(j => A[j]), inv);
    check(BI.every((row, i) => row.every((x, j) => mod(x, q) === BigInt(i === j))), "exact composite-root inverse");
    const rows = model.lattice_rows.map(row => row.map(B)), E = rows.map(embed);
    equalBig(model.embedded_rows, E, "paired correlation embedding");
    check(abs(det(rows)) === q**BigInt(m-n) && B(model.lattice_index) === q**BigInt(m-n), "complete code lattice index");
    const gram = 3n**BigInt(selected.length)*q**BigInt(2*(m-n));
    check(B(model.embedded_gram_determinant) === gram && profile(E).gram === gram, "exact paired metric determinant");
    function extract(point) {
      const raw = unembed(point), values = pivots.map(j => raw[j]);
      const secret = inv.map(row => mod(dot(row, values), q));
      check(raw.length === m && A.every((row, j) => mod(dot(row, secret)-raw[j], q) === 0n), "every lattice point has same full-root shared secret");
      return secret.map(Number);
    }
    rows.forEach(row => extract(embed(row)));
    const target = embed(selected.flatMap(r => r.outcome)); let offset = 0;
    for (let bi = 0; bi < cs.reductions.length; bi++) {
      const reduced = cs.reductions[bi], U = reduced.transform.map(row => row.map(B)), R = reduced.rows.map(row => row.map(B));
      check(abs(det(U)) === 1n, "LLL transform is unimodular"); equalBig(multiply(U, E), R, "actual exact LLL transform");
      const p = profile(R); check(p.gram === gram, "LLL preserves full metric lattice");
      const expected = roundPaths(R, target, p), actual = cs.attempts.slice(offset, offset+expected.length);
      check(actual.length === expected.length, "all exact single-rounding paths retained");
      actual.forEach((a, i) => {
        const e = expected[i]; check(a.basis_index === bi && a.forced_row === e.forced && a.forced_deviation === e.deviation && a.rounding_steps === m, "actual Babai repair policy");
        check(a.coefficients.every((x, j) => B(x) === e.coefficients[j]) && a.point.every((x, j) => B(x) === e.point[j]), "independent exact rational nearest-plane replay");
        const s = extract(e.point); same(a.candidate, s, "candidate derived from public lattice point");
        check(B(a.paired_distance_squared) === target.reduce((v, x, j) => v+(x-e.point[j])**2n, 0n), "raw paired torus representative distance");
        discovered.set(key(s), s); paths++; roundingSteps += m;
      });
      offset += expected.length; reductions++;
    }
    check(offset === cs.attempts.length, "no unaccounted proposal injection"); latticeCount++;
  }
  same([...discovered.keys()].sort(), d.proposals.map(key).sort(), "shortlist consists of actual decoded public lattice points only");
  const values = new Map(d.proposals.map(s => [key(s), nativeValues(records, s, q)]));
  d.proposal_scores.forEach(p => { const v = values.get(key(p.candidate)); check(v && Math.abs(v.score-p.score) < 2e-11 && Math.abs(v.loss-Number(p.selection_loss)) < 2e-11, "actual native-score/loss ranking, not Gaussian score"); });
  if (d.candidate !== null) {
    const best = values.get(key(d.candidate)); check(best && [...values.values()].every(v => best.loss <= v.loss+2e-12) && Math.abs(d.training_score-best.score) < 2e-11, "training-only native selection");
    const fresh = nativeValues(c.heldout_records, d.candidate, q);
    check(Math.abs(fresh.score-c.verification.score) < 2e-11 && c.verification.threshold_passed === (fresh.score >= .5) && c.verification.gate.tested_candidates === 1, "fixed single candidate verified on fresh data");
  }
  check(c.calibration_recovered === (key(d.candidate) === key(c.calibration_secret)), "calibration truth diagnostic only");
  check(Math.abs(nativeValues(records, c.calibration_secret, q).score-c.true_training_score_diagnostic) < 2e-11 && Math.abs(nativeValues(c.heldout_records, c.calibration_secret, q).score-c.true_heldout_score_diagnostic) < 2e-11, "source sanity scores retained");
  check(d.cost.original_measured_qutrits === 96 && d.cost.LLL_calls === reductions && d.cost.nearest_plane_paths === paths && d.cost.exact_rounding_steps === roundingSteps && d.cost.training_score_evaluations === discovered.size && !d.cost.distinct_source_IDs_prove_IID && d.cost.classical_record_reuse_is_charged_once && !d.cost.root_value_or_secret_grid_enumeration && !d.cost.LLL_time_deadline, "complete classical work/source ledger");
  pathCount += paths; reductionCount += reductions; recoveries += Number(c.calibration_recovered); passes += Number(c.verification.threshold_passed);
}
const mc = report.metric_countercontrol, q = BigInt(mc.modulus);
for (const item of [mc.closer_but_worse, mc.farther_but_better]) {
  const [a, c] = item.residual.map(B); let best = null;
  for (const i of [-1n, 0n]) for (const j of [-1n, 0n]) { const e = embed([a+q*i, c+q*j]), value = dot(e, e); if (best === null || value < best) best = value; }
  check(B(item.torus_paired_distance_squared) === best, "complete two-dimensional wrap minimum");
  const score = Math.cos(2*Math.PI*Number(a)/Number(q))+Math.cos(2*Math.PI*Number(c)/Number(q))+Math.cos(2*Math.PI*Number(a-c)/Number(q));
  check(Math.abs(score-item.native_score) < 2e-12, "surrogate counterexample native score");
}
check(B(mc.closer_but_worse.torus_paired_distance_squared) < B(mc.farther_but_better.torus_paired_distance_squared) && mc.closer_but_worse.native_score < mc.farther_but_better.native_score && !mc.Euclidean_CVP_equals_native_likelihood_maximization, "CVP/likelihood equivalence self-refuted");
check(report.control_count === 12 && report.recoveries === recoveries && report.fresh_threshold_passes === passes, "all bounded successes and failures retained");
console.log(JSON.stringify({status: "PASS", controls: 12, exact_code_lattices: latticeCount, unimodular_reductions: reductionCount, exact_rational_Babai_paths: pathCount, recoveries, fresh_threshold_passes: passes, classical_source_simulator_or_hardness_claim: false}, null, 2));

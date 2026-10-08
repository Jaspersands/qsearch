"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {B, F, add, sub, mul, div, str, round, dot, mod, check, same, sparse, dense, profile} = require("./ternary_full_record_cvp_crosscheck.js");
const {run: verifyQuotient} = require("./ternary_quotient_cvp_crosscheck.js");
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const compare = (a, b) => { const x = a[0]*b[1]-b[0]*a[1]; return x < 0n ? -1 : x > 0n ? 1 : 0; };
const term = (d, x) => mul(d, mul(x, x));
function conditional(R, p, initial, live, active, target, model, A, q) {
  const fixed = new Map(live.map((i, j) => [i, active[j]])), coordinates = [...initial], coefficients = Array(R.length).fill(0n);
  let cost = F(0n);
  for (let i = R.length-1; i >= 0; i--) {
    const a = fixed.has(i) ? fixed.get(i) : round(coordinates[i]); coefficients[i] = a;
    cost = add(cost, term(p.gs[i], sub(coordinates[i], F(a))));
    for (const [j, mu] of p.mu[i]) coordinates[j] = sub(coordinates[j], mul(F(a), mu));
  }
  const point = Array(R.length).fill(0n); coefficients.forEach((x, i) => { if (x) for (const [j, y] of R[i]) point[j] += x*y; });
  const distance = point.reduce((s, x, j) => s+(x-target[j])**2n, 0n);
  check(cost[1] === 1n && cost[0] === distance, "complete original distance equals conditional objective");
  const piv = model.unit_basis_rows.map(j => point[j]), secret = model.unit_basis_inverse.map(row => mod(dot(row.map(B), piv), q));
  check(A.every((row, j) => mod(dot(row, secret)-point[j], q) === 0n), "all original modular equations for incumbent");
  return {active_coefficients: active, coefficients, point, supplied_Euclidean_cost: distance, candidate: secret};
}
function search(R, p, initial, live, dead, target, model, A, q, active, cap) {
  let incumbent = conditional(R, p, initial, live, active, target, model, A, q), upper = F(incumbent.supplied_Euclidean_cost);
  const original = incumbent, descending = [...live].reverse(), deadSet = new Set(dead), deps = new Map(dead.map(j => [j, []])), finish = new Map(live.map(i => [i, []]));
  for (const i of live) for (const [j] of p.mu[i]) if (deadSet.has(j)) deps.get(j).push(i);
  let constant = F(0n);
  for (const j of dead) {
    if (deps.get(j).length) finish.get(Math.min(...deps.get(j))).push(j);
    else constant = add(constant, term(p.gs[j], sub(initial[j], F(round(initial[j])))));
  }
  const counters = {tested_coefficient_extensions: 0, partial_cost_prunes: 0, completed_live_assignments: 0, strict_incumbent_improvements: 0}, trace = [];
  let exhausted = false;
  function visit(depth, cost, assigned, coordinates) {
    if (compare(cost, upper) > 0) { counters.partial_cost_prunes++; return; }
    if (depth === descending.length) {
      const point = conditional(R, p, initial, live, [...assigned].reverse(), target, model, A, q);
      check(compare(cost, F(point.supplied_Euclidean_cost)) === 0, "exact completed tree cost"); counters.completed_live_assignments++;
      if (compare(cost, upper) < 0) {
        incumbent = point; upper = cost; counters.strict_incumbent_improvements++;
        trace.push({at_extension: counters.tested_coefficient_extensions, active_coefficients: point.active_coefficients.map(String), supplied_Euclidean_cost: String(point.supplied_Euclidean_cost)});
      }
      return;
    }
    const i = descending[depth], center = coordinates[i], base = round(center);
    for (let offset = 0n; ; offset++) {
      let relevant = false;
      for (const a of offset ? [base-offset, base+offset] : [base]) {
        const increment = term(p.gs[i], sub(center, F(a)));
        if (compare(add(cost, increment), upper) > 0) continue;
        relevant = true;
        if (counters.tested_coefficient_extensions >= cap) { exhausted = true; return; }
        counters.tested_coefficient_extensions++;
        const updated = [...coordinates]; for (const [j, mu] of p.mu[i]) updated[j] = sub(updated[j], mul(F(a), mu));
        let value = add(cost, increment);
        for (const j of finish.get(i)) value = add(value, term(p.gs[j], sub(updated[j], F(round(updated[j])))));
        visit(depth+1, value, [...assigned, a], updated);
        if (exhausted) return;
      }
      if (!relevant) break;
    }
  }
  visit(0, constant, [], initial);
  return {incumbent, original, counters, trace, exhausted};
}
function samePoint(stored, actual) {
  for (const name of ["active_coefficients", "coefficients", "point", "candidate"]) {
    check(stored[name].length === actual[name].length && actual[name].every((x, j) => x === B(stored[name][j])), "exact full point "+name);
  }
  check(B(stored.supplied_Euclidean_cost) === actual.supplied_Euclidean_cost, "exact supplied full point distance");
}
function run(report, original, quotient, originalBytes, quotientBytes) {
  verifyQuotient(quotient, original, originalBytes);
  check(report.status === "EXACT_QUOTIENT_SPHERE_SEARCH_CERTIFICATION_REVIEW_PENDING" && !report.new_training_validation_or_LLL_run && !report.near_exact_population_solver_or_classical_hardness_proved, "finite input proof or unknown, no population claim");
  check(report.original_report_sha256 === hash(originalBytes) && report.quotient_report_sha256 === hash(quotientBytes) && report.derivation_sha256 === hash(fs.readFileSync(path.join(__dirname, "../TERNARY_QUOTIENT_CVP_CERTIFIER.md"))), "pinned original, compiler and certifier derivations");
  check(report.controls.length === original.controls.length, "all input cohorts retained");
  let certified = 0, capped = 0, extensions = 0, improved = 0, comparisons = 0;
  for (let k = 0; k < original.controls.length; k++) {
    const previous = original.controls[k], parent = quotient.controls[k], c = report.controls[k], stored = c.result, model = previous.decoder.model, m = model.lattice_equations, q = B(previous.modulus);
    same([c.parent_seed, c.n, c.root_digits, c.density_per_n_r], [previous.seed, previous.n, previous.root_digits, previous.density_per_n_r], "all precommitted certification inputs");
    const R = sparse(previous.decoder.reduced_rows_sparse, m), p = profile(R, m), rows = dense(R, m), initial = [], inner = [];
    const target = previous.training_records.flatMap(r => r.outcome).map(B), A = previous.training_records.flatMap(r => [r.first, r.second]).map(row => row.map(B));
    for (let i = 0; i < m; i++) { let value = F(dot(rows[i], target)); for (const [j, mu] of p.mu[i]) value = sub(value, mul(mu, inner[j])); inner.push(value); initial.push(div(value, p.gs[i])); }
    const live = parent.decoder.certificate.live_positions, dead = parent.decoder.certificate.dead_positions;
    let proposal = parent.decoder.proposal_scores[0];
    for (const item of parent.decoder.proposal_scores) if (B(item.Euclidean_cost) < B(proposal.Euclidean_cost)) proposal = item;
    const candidate = proposal.candidate.map(B), canonical = target.map((y, j) => y-(mod(y-dot(A[j], candidate)+q/2n, q)-q/2n));
    const pointInner = [], pointCoords = [];
    for (let i = 0; i < m; i++) { let value = F(dot(rows[i], canonical)); for (const [j, mu] of p.mu[i]) value = sub(value, mul(mu, pointInner[j])); pointInner.push(value); pointCoords.push(div(value, p.gs[i])); }
    const coeff = Array(m).fill(0n);
    for (let i = m-1; i >= 0; i--) { check(pointCoords[i][1] === 1n, "exact canonical integer basis inverse"); coeff[i] = pointCoords[i][0]; for (const [j, mu] of p.mu[i]) pointCoords[j] = sub(pointCoords[j], mul(F(coeff[i]), mu)); }
    check(c.initial_incumbent_source === "BEST_PUBLIC_TRAINING_PROPOSAL_CANONICAL_POINT", "strongest known valid public bound, not arbitrary lattice lift"); same(c.initial_candidate, proposal.candidate, "public training-only incumbent");
    const result = search(R, p, initial, live, dead, target, model, A, q, live.map(i => coeff[i]), 4096);
    check(result.original.point.every((x, j) => x === canonical[j]) && result.original.supplied_Euclidean_cost === B(proposal.Euclidean_cost), "canonical source proposal is exact conditional incumbent");
    check(stored.node_cap === 4096 && stored.status === (result.exhausted ? "UNKNOWN_NODE_CAP_EXHAUSTED" : "EXACT_FINITE_CVP_OPTIMUM_CERTIFIED") && stored.CVP_optimality_certified === !result.exhausted && stored.all_live_branches_within_radius_exhausted === !result.exhausted, "exact complete-versus-capped distinction");
    same(stored.search_counters, result.counters, "every viable extension, dead-cost prune and completion");
    same(stored.strict_improvement_trace.map(t => ({at_extension: t.at_extension, active_coefficients: t.active_coefficients.map(x => String(B(x))), supplied_Euclidean_cost: String(B(t.supplied_Euclidean_cost))})), result.trace, "all strict public incumbent improvements");
    samePoint(stored.initial_incumbent, result.original); samePoint(stored.best_point, result.incumbent);
    check(B(stored.initial_squared_radius) === result.original.supplied_Euclidean_cost && B(stored.final_squared_radius) === result.incumbent.supplied_Euclidean_cost && stored.unbounded_integer_coefficients_handled_by_exact_radius && stored.cost_pruning_uses_exact_nonnegative_partial_bound && !stored.cap_exhaustion_certifies_approximation_or_hardness && !stored.efficient_population_decoder_or_speedup, "exact radius scope, no approximation by exhaustion");
    const margin = 64n*result.incumbent.supplied_Euclidean_cost-81n*B(previous.CVP_comparison_certificate.valid_point_squared_distance);
    check(B(c.strict_integer_factor_failure_margin) === margin && c.norm_9_over_8_approximation_falsified === (margin > 0n), "public point comparison, not planted optimality");
    same(c.calibration_secret_match_diagnostic_only, result.incumbent.candidate.every((x, j) => x === B(previous.calibration_secret[j])), "posthoc calibration diagnostic");
    check(c.full_dimension === m && c.active_dimension === live.length && !c.fresh_validation_performed && c.new_original_qutrits === 0 && c.new_LLL_calls === 0 && c.inherited_original_qutrits_including_both_validation_batches === parent.cumulative_original_qutrits_including_old_validation, "no reused holdout confidence or source cost erasure");
    certified += Number(!result.exhausted); capped += Number(result.exhausted); extensions += result.counters.tested_coefficient_extensions; improved += result.counters.strict_incumbent_improvements; comparisons += Number(margin > 0n);
  }
  return {status: "PASS", full_cohorts: report.controls.length, certified_finite_optima: certified,
          explicitly_unknown_capped_controls: capped, exact_tested_extensions: extensions,
          strict_incumbent_improvements: improved, exact_output_point_9_over_8_counterexamples: comparisons,
          efficient_population_solver: false};
}
if (require.main === module) {
  const read = (arg, file) => fs.readFileSync(arg || path.join(__dirname, "../classical_baselines", file));
  const report = JSON.parse(read(process.argv[2], "ternary_quotient_cvp_certifier.json"));
  const originalBytes = read(process.argv[3], "ternary_full_record_cvp.json"), quotientBytes = read(process.argv[4], "ternary_quotient_cvp.json");
  console.log(JSON.stringify(run(report, JSON.parse(originalBytes), JSON.parse(quotientBytes), originalBytes, quotientBytes), null, 2));
}
module.exports = {run, search};

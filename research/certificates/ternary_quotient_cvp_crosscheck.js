"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {B, F, add, sub, mul, div, str, round, dot, mod, check, same, sparse, dense, profile, score, verify} = require("./ternary_full_record_cvp_crosscheck.js");
const key = JSON.stringify, hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const compare = (a, b) => { const x = a[0]*b[1]-b[0]*a[1]; return x < 0n ? -1 : x > 0n ? 1 : 0; };
function tupleCompare(a, b) { for (let j = 0; j < a.length; j++) if (a[j] !== b[j]) return a[j] < b[j] ? -1 : 1; return 0; }
const square = x => mul(x, x), term = (d, x) => mul(d, square(x));
function beam(p, initial, live, dead, width, radius) {
  const finish = new Map(live.map(i => [i, []])), deps = new Map(dead.map(j => [j, []]));
  for (const i of live) for (const [j] of p.mu[i]) if (deps.has(j)) deps.get(j).push(i);
  let constant = F(0n);
  for (const j of dead) {
    const dependency = deps.get(j);
    if (dependency.length) finish.get(Math.min(...dependency)).push(j);
    else constant = add(constant, term(p.gs[j], sub(initial[j], F(round(initial[j])))));
  }
  let states = [{cost: constant, assigned: [], coordinates: initial}], stages = [];
  for (const i of [...live].reverse()) {
    const children = [];
    for (const state of states) {
      const center = state.coordinates[i], nearest = round(center);
      for (let shift = -radius; shift <= radius; shift++) {
        const a = nearest+BigInt(shift), coordinates = [...state.coordinates];
        let cost = add(state.cost, term(p.gs[i], sub(center, F(a))));
        for (const [j, mu] of p.mu[i]) coordinates[j] = sub(coordinates[j], mul(F(a), mu));
        for (const j of finish.get(i)) cost = add(cost, term(p.gs[j], sub(coordinates[j], F(round(coordinates[j])))));
        children.push({cost, assigned: [...state.assigned, a], coordinates});
      }
    }
    children.sort((a, b) => compare(a.cost, b.cost) || tupleCompare(a.assigned, b.assigned));
    states = children.slice(0, width);
    stages.push({live_position: i, expanded_states: children.length, retained_states: states.length,
                 finalized_dead_positions: finish.get(i), best_exact_partial_cost: str(states[0].cost)});
  }
  return {states, stages};
}
function run(report, parent, parentBytes) {
  verify(parent);
  check(report.status === "EXACT_QUOTIENT_COMPILER_BOUNDED_SEARCH_REVIEW_PENDING" && !report.near_exact_CVP_solver_implemented && !report.population_recovery_or_speedup_claim && report.old_cohorts_influenced_design && !report.new_IID_training_or_new_LLL_run && report.fresh_validation_after_selection, "exact compiler, bounded attack, prospective validation");
  check(report.parent_report_sha256 === hash(parentBytes) && report.derivation_sha256 === hash(fs.readFileSync(path.join(__dirname, "../TERNARY_QUOTIENT_CVP.md"))), "pinned source and derivation");
  check(report.controls.length === parent.controls.length, "all cohorts preserved");
  let largest = 0, eliminated = 0, expanded = 0, comparisons = 0, improvements = 0, finals = 0;
  const recoveries = {Euclidean: 0, native_likelihood: 0};
  for (let index = 0; index < parent.controls.length; index++) {
    const previous = parent.controls[index], c = report.controls[index], d = c.decoder, model = previous.decoder.model;
    same([c.n, c.root_digits, c.density_per_n_r, c.parent_seed, c.fresh_seed], [previous.n, previous.root_digits, previous.density_per_n_r, previous.seed, previous.seed+120200], "all precommitted source and fresh regimes");
    const m = model.lattice_equations, M = previous.training_records.length, q = B(previous.modulus);
    const critique = c.systematic_coordinate_self_critique, pivots = model.unit_basis_rows, generators = model.code_generator_rows;
    check(generators.length === c.n && generators.every((row, i) => pivots.every((j, k) => B(row[j]) === BigInt(i === k))), "systematic projection leaves exact orthonormal pivot axes");
    same(critique.projected_live_GS_norms_squared, Array(c.n).fill(1), "n unit live directions already exist without LLL");
    check(critique.systematic_integer_search_dimension === c.n && critique.orthogonal_dead_directions === m-c.n && B(critique.complete_mod_q_secret_classes) === q**BigInt(c.n) && B(critique.orthogonal_axis_norm_squared) === q*q && !critique.LLL_influence_dimension_is_intrinsic_unknown_count && !critique.systematic_projection_is_new_algorithmic_dimension_reduction && critique.periodic_objective_preserves_original_secret_search && critique.all_systematic_rows_in_original_lattice, "no algorithmic dimension-reduction claim from reparameterizing n secret coordinates");
    const R = sparse(previous.decoder.reduced_rows_sparse, m), rows = dense(R, m), p = profile(R, m);
    const y = previous.training_records.flatMap(r => r.outcome).map(B), A = previous.training_records.flatMap(r => [r.first, r.second]).map(row => row.map(B));
    function extract(point) {
      const values = model.unit_basis_rows.map(j => point[j]);
      const s = model.unit_basis_inverse.map(row => mod(dot(row.map(B), values), q));
      check(A.every((row, j) => mod(dot(row, s)-point[j], q) === 0n), "complete original code equations");
      return s.map(Number);
    }
    const rowSecrets = rows.map(extract), isLive = [];
    for (let i = 0; i < m; i++) isLive.push(rowSecrets[i].some(Boolean) || [...p.mu[i].keys()].some(j => isLive[j]));
    const live = isLive.flatMap((x, i) => x ? [i] : []), dead = isLive.flatMap((x, i) => x ? [] : [i]);
    same(d.certificate.live_positions, live, "actual live GS ancestry"); same(d.certificate.dead_positions, dead, "actual zero-code dead ancestry");
    const deadSet = new Set(dead), coupling = dead.flatMap(i => [...p.mu[i].keys()].filter(j => deadSet.has(j)).map(j => [i, j]));
    same(d.certificate.dead_dead_GS_edges, coupling, "exact diagonal dead test"); check(coupling.length === 0, "no coupled-dead shortcut");
    check(dead.every(i => p.mu[i].size === 0 && rowSecrets[i].every(x => x === 0)), "independent eliminated integer directions");
    check(d.certificate.full_dimension === m && d.certificate.integer_search_dimension === live.length && !d.certificate.conditional_minimum_is_global_CVP && !d.certificate.reduced_objective_is_ordinary_Euclidean_CVP, "periodic quotient, not granted low-dimensional CVP");
    const inner = [], initial = [];
    for (let i = 0; i < m; i++) {
      let value = F(dot(rows[i], y));
      for (const [j, mu] of p.mu[i]) value = sub(value, mul(mu, inner[j]));
      inner.push(value); initial.push(div(value, p.gs[i]));
    }
    const search = d.search;
    check(d.status === "BOUNDED_LIVE_COEFFICIENT_BEAM" && search.status === d.status && search.beam_width === 32 && search.branch_radius === 1 && search.conditional_elimination_exact && !search.CVP_optimality_certified && !search.near_exact_approximation_guarantee && !search.complete_integer_coefficient_enumeration, "fixed bounded public search, no optimality");
    const replay = beam(p, initial, live, dead, 32, 1); same(search.stages, replay.stages, "entire exact beam expansion, ranking and pruning");
    const expansions = replay.stages.reduce((s, x) => s+x.expanded_states, 0); check(search.expanded_states === expansions && search.candidates.length === replay.states.length, "full search cost and candidates");
    const discovered = new Map();
    for (let k = 0; k < replay.states.length; k++) {
      const state = replay.states[k], stored = search.candidates[k], active = [...state.assigned].reverse();
      check(stored.active_coefficients.length === active.length && active.every((x, j) => x === B(stored.active_coefficients[j])), "exact retained live coefficients");
      const fixed = new Map(live.map((i, j) => [i, active[j]])), coords = [...initial], coefficients = Array(m).fill(0n);
      let cost = F(0n);
      for (let i = m-1; i >= 0; i--) {
        coefficients[i] = fixed.has(i) ? fixed.get(i) : round(coords[i]);
        cost = add(cost, term(p.gs[i], sub(coords[i], F(coefficients[i]))));
        for (const [j, mu] of p.mu[i]) coords[j] = sub(coords[j], mul(F(coefficients[i]), mu));
      }
      check(compare(cost, state.cost) === 0 && cost[1] === 1n, "exact eliminated objective agrees with all finalized beam costs");
      const point = Array(m).fill(0n); coefficients.forEach((x, i) => { if (x) for (const [j, v] of R[i]) point[j] += x*v; });
      check(stored.coefficients.length === m && coefficients.every((x, j) => x === B(stored.coefficients[j])) && stored.point.length === m && point.every((x, j) => x === B(stored.point[j])), "complete original conditional minimizer");
      const distance = point.reduce((s, x, j) => s+(x-y[j])**2n, 0n);
      check(distance === cost[0] && B(stored.supplied_Euclidean_cost) === distance, "all original Euclidean terms retained");
      const s = extract(point); same(stored.candidate, s, "secret class of real lattice point"); discovered.set(key(s), s); finals++;
    }
    same(d.inherited_candidates.map(key).sort(), previous.decoder.proposal_scores.map(x => key(x.candidate)).sort(), "all and only inherited public training proposals");
    d.inherited_candidates.forEach(s => discovered.set(key(s), s));
    same(d.proposal_scores.map(x => key(x.candidate)).sort(), [...discovered.keys()].sort(), "all and only bounded and inherited candidates");
    const scores = new Map();
    for (const item of d.proposal_scores) {
      const value = score(previous.training_records, item.candidate, q);
      check(B(item.Euclidean_cost) === value.cost && Math.abs(Number(item.native_loss)-value.loss) < 3e-11 && Math.abs(item.native_score-value.score) < 3e-11, "exact Euclidean and numerical native training objectives");
      scores.set(key(item.candidate), value);
    }
    check(c.heldout_records.length === 512 && c.heldout_records.every(rec => B(rec.modulus) === q && [rec.first, rec.second].every(row => row.length === c.n && row.every(x => B(x) >= 0n && B(x) < q)) && rec.outcome.length === 2 && rec.outcome.every(x => B(x) >= 0n && B(x) < q)), "new full-root validation data");
    same(c.heldout_source_IDs, Array.from({length: 512}, (_, j) => `quotient-cvp-${c.fresh_seed}-fresh-${j}`), "fresh predeclared source IDs");
    const oldIDs = new Set([...previous.decoder.source_IDs, ...previous.heldout_source_IDs]);
    check(c.heldout_source_IDs.every(x => !oldIDs.has(x)) && c.parent_training_and_basis_reused && !c.old_heldout_records_used_by_optimizer_or_validator && c.old_validation_not_erased_from_total_research_cost, "no post-selection holdout recycling");
    for (const [name, candidate] of Object.entries(d.selections)) {
      const value = scores.get(key(candidate));
      check(value && [...scores.values()].every(other => name === "Euclidean" ? value.cost <= other.cost : value.loss <= other.loss+2e-12), "all-record training objective selection");
      const fresh = score(c.heldout_records, candidate, q), v = c.verification[name]; same(v.candidate, candidate, "frozen candidate unchanged");
      check(Math.abs(v.fresh_score-fresh.score) < 3e-11 && v.threshold_passed === (fresh.score >= .5) && v.calibration_recovered === (key(candidate) === key(previous.calibration_secret)), "new heldout score and diagnostic recovery"); recoveries[name] += Number(v.calibration_recovered);
    }
    const count = new Set(Object.values(d.selections).map(key)).size, gate = c.joint_fixed_candidate_gate;
    check(gate.tested_candidates === count && gate.fresh_native_qutrit_records === 512 && Math.abs(gate.false_acceptance_union_bound_approximation-Math.min(1, count*Math.exp(-1024/81))) < 1e-12, "distinct frozen selection multiplicity");
    const best = [...scores.values()].reduce((a, b) => a === null || b.cost < a ? b.cost : a, null), oldBest = previous.decoder.proposal_scores.reduce((a, b) => a === null || B(b.Euclidean_cost) < a ? B(b.Euclidean_cost) : a, null);
    const margin = 64n*best-81n*B(previous.CVP_comparison_certificate.valid_point_squared_distance);
    check(B(c.best_Euclidean_cost) === best && B(c.parent_best_Euclidean_cost) === oldBest && best <= oldBest && B(c.strict_integer_factor_failure_margin) === margin && c.norm_9_over_8_approximation_falsified === (margin > 0n), "exact9/8 falsifier without planted optimality");
    const ledger = d.cost;
    check(d.all_original_records_in_objective && !d.hidden_secret_or_validation_supplied_to_optimizer && !d.accepted_speedup_candidate && !d.classical_dequantization_or_hardness_proved && ledger.original_training_qutrits_reused === M && ledger.new_training_qutrits === 0 && ledger.new_LLL_calls === 0 && ledger.inherited_LLL_calls === previous.decoder.cost.LLL_calls && ledger.full_lattice_dimension === m && ledger.integer_search_dimension === live.length && ledger.expanded_states === expansions && ledger.distinct_candidates_scored === scores.size && c.new_original_qutrits === 512 && c.total_inherited_training_plus_new_validation === M+512 && c.cumulative_original_qutrits_including_old_validation === M+1024, "complete inherited and new resource accounting");
    largest = Math.max(largest, m); eliminated += dead.length; expanded += expansions; comparisons += Number(margin > 0n); improvements += Number(best < oldBest);
  }
  return {status: "PASS", full_cohorts: report.controls.length, largest_original_dimension: largest,
          exact_eliminated_directions: eliminated, independently_replayed_beam_expansions: expanded,
          conditional_minimizers: finals, recoveries, improved_training_Euclidean_cost: improvements,
          exact_9_over_8_counterexamples: comparisons, near_exact_CVP_guarantee: false};
}
if (require.main === module) {
  const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../classical_baselines/ternary_quotient_cvp.json"), "utf8"));
  const parentBytes = fs.readFileSync(process.argv[3] || path.join(__dirname, "../classical_baselines/ternary_full_record_cvp.json"));
  console.log(JSON.stringify(run(report, JSON.parse(parentBytes), parentBytes), null, 2));
}
module.exports = {run, beam};

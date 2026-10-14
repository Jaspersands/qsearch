"use strict";
// Independent integer carried-group chart and literal two-level/CNOT replay.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {check, same, rat, str, add: radd} = require("./cyclotomic_exact.js");
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/reductions/native_generalized_dihedral_bridge.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod = (a, m) => (a % m + m) % m;
const encode = a => a <= 9007199254740991n && a >= -9007199254740991n ? Number(a) : String(a);
function chart(L, n = 1) {
  check(Number.isInteger(L) && L >= 1 && L <= 512 && Number.isInteger(n) && n >= 1, "positive supported native chart");
  const q = 3n**BigInt(Math.floor(L/2)), Q = 3n**BigInt(Math.ceil(L/2)), orders = Array.from({length: n}, () => L % 2 ? [3n*q, q] : [q, q]).flat();
  let x = 2n, y = -1n;
  for (let j = 1; j < L; j++) [x, y] = [-2n*x-y, x-y];
  const d = 3n**BigInt(L);
  check(x*Q % d === 0n && y*Q % d === 0n, "exact native trace numerator");
  const u = x*Q/d, v = y*Q/d;
  check(!(L % 2) || (v-u) % 3n === 0n, "ramified dual cross entry divisible by3");
  const T = L % 2 ? [[u, v-u], [(v-u)/3n, -v]] : [[u, v], [v, -u-v]];
  check(T[0][0]*T[1][1]-T[0][1]*T[1][0] === -1n, "integer perfect-pairing determinant");
  const h0 = L % 2 ? 3n*q : q, cross = L % 2 ? 2n*q : 0n, h1 = q;
  function reduce(a) {
    const b = mod(a[1], h1), carry = (a[1]-b)/h1;
    return [mod(a[0]-cross*carry, h0), b];
  }
  const mul = (a, b) => reduce([a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1]]);
  function coordinates(raw) {
    check(raw.length === n, "native vector dimension");
    return raw.flatMap(a => {
      const v = a.map(BigInt), r = reduce(v);
      same(v.map(String), r.map(String), "canonical native ideal carry representative");
      return L % 2 ? [mod(r[0]+r[1], 3n*q), r[1]] : r;
    });
  }
  function dual(raw) {
    const a = coordinates(raw);
    return Array.from({length: 2*n}, (_, j) => mod(T[j % 2][0]*a[2*Math.floor(j/2)]+T[j % 2][1]*a[2*Math.floor(j/2)+1], orders[j]));
  }
  function character(k, secret) {
    check(k.length === orders.length && secret.length === orders.length, "cyclic character dimension");
    let r = rat(0n);
    k.forEach((a, j) => {
      check(a >= 0n && a < orders[j] && secret[j] >= 0n && secret[j] < orders[j], "canonical mixed cyclic character");
      r = radd(r, rat(a*secret[j], orders[j]));
    });
    return rat(mod(r[0], r[1]), r[1]);
  }
  function record(saved) {
    check(saved.native_level === L && saved.ring_dimension === n, "chart parameters");
    same(saved.cyclic_orders, orders.map(encode), "actual Smith orders, not F3 field-shadow coordinates");
    same(saved.dual_matrix_per_coordinate, T.map(a => a.map(encode)), "independent exact trace dual matrix");
    check(saved.dual_matrix_determinant === -1 && saved.group_order_log3_exact === n*L && saved.basis_chart_is_a_field_shadow === false, "perfect carried-group pairing scope");
    check(saved.additive_coordinates === (L % 2 ? "(a+b,b) in basis(1,pi)" : "(a,b) in basis(1,zeta)"), "actual additive coordinate basis");
  }
  return {orders, T, q, h0, h1, reduce, mul, coordinates, dual, character, record};
}
const angle = r => 2*Math.PI*Number(r[0])/Number(r[1]);
function complexClose(saved, expected, message) {
  check(saved.length === 2 && saved.every(Number.isFinite) && Math.abs(saved[0]-expected[0]) < 3e-12 && Math.abs(saved[1]-expected[1]) < 3e-12, message);
}
const cmul = (a, b) => [a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]];
const cscale = (a, b) => a.map(v => v*b);
const matrixClose = (a, b, message) => {
  check(a.length === 2 && a.every(row => row.length === 2), message);
  a.forEach((row, j) => row.forEach((v, k) => complexClose(v, b[j][k], message)));
};
function pureDensity(theta) {
  const c = Math.cos(theta)/2, s = Math.sin(theta)/2;
  return [[[.5, 0], [c, -s]], [[c, s], [.5, 0]]];
}
function budget(b) {
  const M = b.required_binary_outputs, bits = b.failure_bits, C = 3*(M+bits);
  check(M === 16 && bits === 16 && b.original_copy_cap === C, "committed paid extraction cap");
  check(b.ideal_IID_extraction_failure_upper_exact === str(rat(2n**BigInt(M-1+C), 3n**BigInt(C))), "exact binomial exponential-moment tail bound");
  check(b.simpler_failure_upper === str(rat(1n, 2n**BigInt(bits+1))) && b.acceptance_is_label_and_secret_independent === true && b.finite_source_or_preparation_promises_established_here === false, "conditional IID extraction guarantee, not certified physical source");
}
function run(r) {
  check(r.status === "NATIVE_TO_GENERALIZED_DIHEDRAL_PHASE_BRIDGE_REVIEW_PENDING", "review-pending known-baseline bridge");
  check(r.producer_sha256 === hash(path.join(ROOT, "theorems/native_generalized_dihedral_bridge.py")) && r.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_GENERALIZED_DIHEDRAL_BRIDGE.md")), "pinned derivation and producer");
  const dependencies = ["cyclotomic_rescaling_gate.py", "native_state_hsp_bridge.py", "native_uniform_descent_receiver.py", "cyclic_centre_state_hsp_receiver.py"];
  same(Object.keys(r.dependency_sha256).sort(), dependencies.slice().sort(), "critical source dependencies");
  dependencies.forEach(f => check(r.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "pinned source dependency "+f));
  ["known_ideal_solver_is_implemented_here", "efficient_growing_depth_receiver_supplied", "noisy_receiver_supplied", "accepted_speedup_candidate"].forEach(k => check(r[k] === false, "unjustified full solver or speedup promotion"));
  check(r.additive_dual_label_censuses.length === 4 && r.scalable_chart_controls.length === 8, "all dual-label censuses and scalable chart controls");
  r.additive_dual_label_censuses.forEach((c, index) => {
    const L = index+1, C = chart(L);
    check(c.level === L, "committed census level");
    C.record(c.chart);
    const labels = [];
    for (let a = 0n; a < C.h0; a++) for (let b = 0n; b < C.h1; b++) labels.push([encode(a), encode(b)]);
    same(c.native_ring_labels, labels, "complete canonical carried-ring labels");
    const duals = labels.map(a => C.dual([a]).map(encode));
    same(c.dual_labels, duals, "complete exact dual-label mapping");
    check(new Set(duals.map(JSON.stringify)).size === labels.length, "actual uniform dual law by bijection");
  });
  r.scalable_chart_controls.forEach((c, index) => chart([1, 2, 3, 4, 16, 64, 128, 256][index], 4).record(c));
  let projections = 0, mergeBranches = 0, rejected = 0;
  const dimensions = [[1, 2], [1, 3], [2, 3], [4, 4]];
  check(r.finite_original_source_controls.length === 4, "all complete finite source controls");
  r.finite_original_source_controls.forEach((c, index) => {
    const [n, L] = dimensions[index], C = chart(L, n), x = c.extraction, truth = c.truth_fixture_only;
    check(c.dimension === n && c.level === L, "source control dimension and level");
    C.record(c.additive_chart);
    const secret = C.coordinates(truth);
    same(c.secret_additive_coordinates_fixture_only, secret.map(encode), "actual secret additive chart, fixture only");
    budget(x.budget);
    check(x.status === "FINITE_GENERALIZED_DIHEDRAL_PHASE_BATCH_READY" && x.source_exhaustion === null && x.original_inputs_supplied <= x.budget.original_copy_cap && x.original_source_records.length === x.original_inputs_supplied && x.projection_records.length === x.original_inputs_supplied, "finite paid original-source extraction");
    ["receiver_takes_hidden_secret", "hidden_shift_solved", "quantum_hardware_executed", "new_quantum_speedup_established"].forEach(k => check(x[k] === false, "known phase-source interface only"));
    const accepted = [], rejects = [];
    x.original_source_records.forEach((s, j) => {
      check(s.original_index === j && s.public_label.length === n && s.supplied_amplitudes.length === 3, "complete supplied physical input");
      const dual = C.dual(s.public_label), p = x.projection_records[j];
      [0, 1, 2].forEach(t => {
        const lambda = [[0n, 0n], [1n, 0n], [1n, 1n]][t];
        const value = truth.map(a => C.mul(a.map(BigInt), lambda).map(encode));
        const theta = angle(C.character(dual, C.coordinates(value)));
        complexClose(s.supplied_amplitudes[t], [Math.cos(theta)/Math.sqrt(3), Math.sin(theta)/Math.sqrt(3)], "actual original native phase amplitude");
      });
      same(p.public_native_label, s.public_label, "projection consumes the actual original label");
      same(p.public_dual_label, dual.map(encode), "public perfect-pairing dual label");
      same(p.original_indices, [j], "one original register per projection");
      check(p.ideal_success_probability_exact === "2/3" && Math.abs(p.success_probability-2/3) < 3e-12 && p.projector === "|0><0|+|1><1|" && p.rejected_outcome === "|2><2|", "literal two-outcome local projector");
      check(p.state_prepared_from_secret === false && p.success_filters_higher_label_digits === false && typeof p.accepted === "boolean", "no secret-prepared or label-favored projection");
      const rho = pureDensity(angle(C.character(dual, secret)));
      matrixClose(p.normalized_retained_density, rho, "actual projected native qubit density");
      if (p.accepted) accepted.push({ids: [j], dual, rho}); else rejects.push(j);
      projections++;
    });
    same(x.rejected_original_indices, rejects, "all rejected original registers charged");
    check(accepted.length === 16 && x.outputs_accepted === 16 && x.projection_records.at(-1).accepted === true && c.binary_merge_controls.length === 8, "finite extraction stops at requested accepted count");
    c.binary_merge_controls.forEach((m, j) => {
      check(m.branches_are_alternative_counterfactual_replays_not_two_physical_outputs === true && m.both_actual_instrument_branches.length === 2, "counterfactual gate controls, not cloned sieve outputs");
      const left = accepted[2*j], right = accepted[2*j+1];
      m.both_actual_instrument_branches.forEach((b, outcome) => {
        const sign = outcome === 0 ? 1n : -1n, dual = left.dual.map((a, k) => mod(a+sign*right.dual[k], C.orders[k]));
        check(b.measured_complement_bit === outcome && b.label_sign === Number(sign), "measured sum/difference sign, not freely selected coefficients");
        same(b.input_dual_labels, [left.dual.map(encode), right.dual.map(encode)], "actual accepted inputs");
        same(b.input_original_lineages, [left.ids, right.ids], "paid distinct parent lineages");
        same(b.original_indices, [...left.ids, ...right.ids], "actual physical child ancestry");
        same(b.output_dual_label, dual.map(encode), "correct generalized-abelian sum or difference");
        const literal = [0, 1].map(t => [0, 1].map(u => cscale(cmul(left.rho[t][u], right.rho[t ^ outcome][u ^ outcome]), 2)));
        matrixClose(b.normalized_retained_density, literal, "literal CNOT/complement measurement");
        matrixClose(b.normalized_retained_density, pureDensity(angle(C.character(dual, secret))), "exact child secret character");
        check(Math.abs(b.branch_probability-.5) < 3e-12 && b.ideal_branch_probability_exact === "1/2" && b.quantum_recipe === "CNOT(control=left,target=right), measure right, retain left", "costed one-child CNOT instrument");
        check(b.unknown_secret_used === false && b.unknown_state_inverse_used === false && b.either_sign_can_be_chosen_deterministically === false, "no unknown inversion or free desired branch");
        mergeBranches++;
      });
    });
    rejected += rejects.length;
  });
  check(r.known_baseline_contracts.length === 9, "all fixed/growing-depth baseline contracts");
  r.known_baseline_contracts.forEach((c, i) => {
    const n = [8, 32, 128][Math.floor(i/3)], L = [2, 4, 2*n][i % 3], W = BigInt(n+1)**2n, K = BigInt(n+8);
    check(c.dimension === n && c.level === L && c.entropy_log3_exact === n*L, "actual full-ring additive entropy");
    let cap = 0n, p = 1n;
    for (let j = 0; j < L; j++) {cap += K*p; p *= W;}
    check(c.native_measured_descent_original_copy_upper === String(cap), "existing native upper ledger is not a lower bound");
    check(c.known_ideal_generalized_dihedral_time_query_form === "2^{O(sqrt(n*L*log2(3)))}" && c.citation === "https://arxiv.org/abs/quant-ph/0302112", "literature-backed applicability form, not a measured runtime");
    ["constants_or_finite_runtime_estimated", "complete_Kuperberg_sieve_implemented", "known_bound_is_a_new_quantum_algorithm", "noise_robustness_inherited_from_ideal_theorem", "classical_original_data_separation_established"].forEach(k => check(c[k] === false, "known-baseline scope "+k));
    check(c.fixed_level_polynomial_native_receiver_also_available === true, "do not replace favorable fixed-level polynomial baselines by a worse bound");
    check(c.conditional_integer_secret_entropy_log3_exact === n*Math.ceil(L/2) && c.integer_embedding_verified_from_data === false &&
          c.conditional_integer_secret_known_baseline_form === "2^{O(sqrt(n*ceil(L/2)*log2(3)))}", "conditional integer secret scope, not a promise inferred from data");
    same(c.conditional_integer_embedding_active_phase_axes, Array.from({length: n}, (_, j) => 2*j), "actual integer-secret active phase axes");
  });
  return {status: "PASS", native_projection_records: projections, charged_rejected_originals: rejected,
          actual_merge_branches: mergeBranches, dual_label_censuses: 4,
          complete_known_solver_implemented: false, new_quantum_speedup_established: false};
}
if (require.main === module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
module.exports = {run, chart, complexClose, matrixClose, pureDensity};

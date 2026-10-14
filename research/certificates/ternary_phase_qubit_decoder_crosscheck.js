"use strict";
// Exact F3 elimination and Q(zeta3) POVM replay; source promises remain external.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js"), native = require("./native_generalized_dihedral_crosscheck.js");
const {check, same, rat, str, parse, sub, mul, field, matrices} = E;
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/reductions/ternary_phase_qubit_decoder.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod = a => (a % 3 + 3) % 3;
function basis(n) {
  const pairs = [];
  for (let i = 0; i < n; i++) for (let j = i; j < n; j++) pairs.push([i, j]);
  return pairs;
}
function equation(k, b) {
  check(k.length >= 1 && k.every(x => Number.isInteger(x) && x >= 0 && x < 3) && Number.isInteger(b) && b >= 0 && b < 3, "canonical F3 observed exclusion");
  return [basis(k.length).map(([i, j]) => mod((i === j ? 1 : 2)*k[i]*k[j])).concat(k.map(x => mod(b*x))), mod(1-b*b)];
}
function budget(b, n, bits = 8) {
  const D = n*(n+1)/2+n, M = 3*D+2*bits;
  check(b.dimension === n && b.failure_bits === bits && b.lifted_unknown_dimension === D && b.binary_copy_cap === M, "polynomial lifted size and paid fixed sample count");
  same(b.symmetric_monomial_basis, basis(n), "actual quadratic basis, no antisymmetric or field-shadow entries");
  same(b.exact_rank_failure_upper_compact, {projective_hyperplanes: {base: 3, exponent: D, subtract: 1, denominator: 2}, single_hyperplane_capture_probability: "2/3", sample_count: M}, "exact projective hyperplane union bound expression");
  check(b.simpler_rank_failure_upper === str(rat(1n, 2n**BigInt(bits+1))) && b.source_IID_label_promise_proved_from_data === false && b.noise_and_hardware_errors_included === false && b.oracle_value_access_required === false, "conditional rank guarantee only");
  // 3^D*(2/3)^(3D+2h)/2=(8/9)^D*(4/9)^h/2 <=2^(-h-1).
  check(8n < 9n && 2n*4n < 9n, "integer bound coefficients");
  return {D, M};
}
function eliminate(rows, rhs, D) {
  const A = rows.map((r, i) => r.concat([rhs[i]]));
  const pivots = [];
  for (let j = 0; j < D; j++) {
    const p = A.findIndex((r, i) => i >= pivots.length && r[j] !== 0);
    if (p < 0) continue;
    const rank = pivots.length;
    [A[rank], A[p]] = [A[p], A[rank]];
    const scale = A[rank][j] === 1 ? 1 : 2;
    A[rank] = A[rank].map(v => mod(v*scale));
    for (let i = 0; i < A.length; i++) if (i !== rank) {
      const c = A[i][j];
      if (c) A[i] = A[i].map((v, k) => mod(v-c*A[rank][k]));
    }
    pivots.push(j);
  }
  const inconsistent = A.some(r => !r.slice(0, D).some(Boolean) && r[D] !== 0);
  const solution = Array(D).fill(0);
  pivots.forEach((p, i) => solution[p] = A[i][D]);
  return {rank: pivots.length, inconsistent, solution: !inconsistent && pivots.length === D ? solution : null};
}
function exactPOVM() {
  const K = field(3), M = matrices(K), half = rat(1n, 2n), third = rat(1n, 3n);
  const effects = [0, 1, 2].map(b => [[K.scale(K.unit, third), K.scale(K.powers[(3-b) % 3], rat(-1n, 3n))],
                                    [K.scale(K.powers[b], rat(-1n, 3n)), K.scale(K.unit, third)]]);
  check(M.eq(effects.reduce(M.plus, M.zeroM(2, 2)), M.identity(2)), "exact POVM completeness");
  effects.forEach(A => {
    check(M.eq(M.star(A), A), "Hermitian anti-trine effects");
    check(K.eq(K.times(A[0][0], A[1][1]), K.times(A[0][1], A[1][0])), "rank-one effects");
    check(K.eq(K.plus(A[0][0], A[1][1]), K.scale(K.unit, rat(2n, 3n))), "positive effect eigenvalues0,2/3");
  });
  for (const raw of ["1", "99/100", "9/10", "0"]) for (let j = 0; j < 3; j++) {
    const g = parse(raw), rho = [[K.scale(K.unit, half), K.scale(K.powers[(3-j) % 3], mul(g, half))],
                               [K.scale(K.powers[j], mul(g, half)), K.scale(K.unit, half)]];
    effects.forEach((A, b) => {
      const product = M.times(A, rho), actual = K.plus(product[0][0], product[1][1]);
      const p = b === j ? E.div(sub(E.one, g), rat(3n)) : E.div(E.add(rat(2n), g), rat(6n));
      check(K.eq(actual, K.scale(K.unit, p)), "exact supplied-density anti-trine Born law");
    });
  }
}
function dualCensuses(saved) {
  check(saved.length === 9, "all dimension2 secrets in rank support census");
  let total = 0;
  for (let s0 = 0; s0 < 3; s0++) for (let s1 = 0; s1 < 3; s1++) {
    const index = 3*s0+s1, histogram = new Map();
    for (let number = 1; number < 243; number++) {
      let x = number;
      const dual = Array.from({length: 5}, () => {const v = x % 3; x = Math.floor(x/3); return v;});
      let nonzero = 0;
      for (let k0 = 0; k0 < 3; k0++) for (let k1 = 0; k1 < 3; k1++) {
        const j = mod(k0*s0+k1*s1);
        for (let b = 0; b < 3; b++) if (b !== j) {
          const [row] = equation([k0, k1], b);
          if (mod(row.reduce((sum, a, k) => sum+a*dual[k], 0))) nonzero++;
        }
      }
      histogram.set(nonzero, (histogram.get(nonzero) || 0)+1); total++;
    }
    const c = saved[index], low = Math.min(...histogram.keys());
    same(c.secret_fixture, [s0, s1], "committed rank-census secret");
    check(c.dual_polynomials_tested === 242 && c.source_row_outcomes === 18 && c.minimum_nonzero_count === low && low >= 6, "all duals escape with probability at least1/3");
    same(c.nonzero_count_histogram, Object.fromEntries([...histogram].sort((a, b) => a[0]-b[0]).map(([k, n]) => [String(k), n])), "complete independently recomputed dual-polynomial histogram");
  }
  return total;
}
function power(x, n) {
  let result = E.one;
  while (n) {if (n % 2) result = mul(result, x); n = Math.floor(n/2); if (n) x = mul(x, x);}
  return result;
}
function run(r) {
  check(r.status === "COPY_ONLY_TERMINAL_TERNARY_PHASE_DECODER_REVIEW_PENDING", "review-pending fixed-exponent base receiver");
  check(r.producer_sha256 === hash(path.join(ROOT, "theorems/ternary_phase_qubit_decoder.py")) && r.derivation_sha256 === hash(path.join(ROOT, "research/TERNARY_PHASE_QUBIT_DECODER.md")), "pinned source and derivation");
  const dependencies = ["native_generalized_dihedral_bridge.py", "nil3_state_hsp_descent_receiver.py", "native_uniform_descent_receiver.py"];
  same(Object.keys(r.dependency_sha256).sort(), dependencies.slice().sort(), "all immediate receiver dependencies");
  dependencies.forEach(f => check(r.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "pinned scientific dependency "+f));
  ["growing_depth_receiver_supplied", "noisy_error_correcting_decoder_supplied", "algorithmic_novelty_verified", "accepted_speedup_candidate"].forEach(k => check(r[k] === false, "no unimplemented depth, robustness or novelty promotion"));
  check(r.known_fixed_exponent_baseline === "https://arxiv.org/abs/quant-ph/0211091" && r.measurement_recipe === "embed qubit in qutrit basis0,1; diag(1,-1,1); inverse_F3; measure excluded value", "known-style lifting with an actual copy-only measurement recipe");
  exactPOVM();
  const controls = r.ideal_original_source_controls.concat(r.noisy_original_source_countercontrols), dimensions = [1, 2, 4, 8, 16, 4, 4, 4], visibilities = ["1", "1", "1", "1", "1", "1", "9/10", "0"];
  check(r.ideal_original_source_controls.length === 6 && r.noisy_original_source_countercontrols.length === 2, "all ideal, zero-secret and noisy source controls");
  let measured = 0, originalCopies = 0;
  controls.forEach((c, index) => {
    const n = dimensions[index], gamma = parse(visibilities[index]), g = Number(gamma[0])/Number(gamma[1]), projection = c.original_projection, d = c.decoder, C = native.chart(1, n);
    check(c.dimension === n && c.visibility_after_original_projection === visibilities[index] && c.zero_secret_fixture === (index === 5) && c.known_native_qutrit_F3_readout_is_a_stronger_baseline_on_this_calibration_source === true, "actual source regime, not a new toy advantage");
    const truth = c.truth_fixture_only;
    check(truth.length === n && truth.every(s => Number.isInteger(s) && s >= 0 && s < 3) && (index !== 5 || truth.every(s => s === 0)), "canonical fixture secret, including zero");
    const {D, M} = budget(d.budget, n);
    check(d.consumed_binary_inputs === M && d.measurement_records.length === M && projection.outputs_accepted === M && projection.budget.required_binary_outputs === M, "paid fixed terminal measurement batch");
    const cap = 3*(M+8), tail = rat(2n**BigInt(M-1+cap), 3n**BigInt(cap));
    check(projection.budget.original_copy_cap === cap && projection.budget.failure_bits === 8 && projection.budget.ideal_IID_extraction_failure_upper_exact === str(tail) && projection.budget.simpler_failure_upper === "1/512", "all original projection rejects and confidence charged");
    check(projection.original_inputs_supplied <= cap && projection.original_source_records.length === projection.original_inputs_supplied && projection.projection_records.length === projection.original_inputs_supplied && projection.source_exhaustion === null, "complete finite original source");
    const accepted = [], rejects = [];
    projection.original_source_records.forEach((s, j) => {
      check(s.original_index === j, "distinct supplied native original indices");
      const dual = C.dual(s.public_label).map(Number), k = dual.filter((_, i) => i % 2 === 0), phase = mod(k.reduce((sum, a, i) => sum+a*truth[i], 0));
      s.supplied_amplitudes.forEach((z, t) => native.complexClose(z, [Math.cos(2*Math.PI*t*phase/3)/Math.sqrt(3), Math.sin(2*Math.PI*t*phase/3)/Math.sqrt(3)], "actual original native qutrit phase"));
      const p = projection.projection_records[j];
      same(p.public_native_label, s.public_label, "projection uses actual native labels");
      same(p.public_dual_label, dual, "exact carried-group dual labels");
      same(p.original_indices, [j], "one paid original per projection");
      check(p.ideal_success_probability_exact === "2/3" && Math.abs(p.success_probability-2/3) < 3e-12 && p.state_prepared_from_secret === false && p.success_filters_higher_label_digits === false, "literal label-independent local projection");
      native.matrixClose(p.normalized_retained_density, native.pureDensity(2*Math.PI*phase/3), "actual projected binary phase");
      if (p.accepted) accepted.push({id: j, dual, k, phase}); else rejects.push(j);
    });
    check(accepted.length === M && projection.projection_records.at(-1).accepted === true, "stop on requested paid accepted count");
    same(projection.rejected_original_indices, rejects, "all rejects preserved in resource ledger");
    const rows = [], rhs = [];
    let forbidden = 0;
    d.measurement_records.forEach((m, j) => {
      const p = accepted[j];
      same(m.public_dual_label, p.dual, "terminal input is an accepted native projection");
      same(m.cyclic_orders, C.orders.map(Number), "actual mixed-order source group");
      same(m.active_phase_axes, Array.from({length: n}, (_, i) => 2*i), "drop only genuine trivial cyclic factors");
      same(m.ternary_character_row, p.k, "actual order3 character row");
      same(m.original_indices, [p.id], "no original ancestor remeasured or replaced");
      const ideal = native.pureDensity(2*Math.PI*p.phase/3), density = ideal.map((row, t) => row.map((z, u) => z.map((x, k) => g*x+(t === u && k === 0 ? (1-g)/2 : 0))));
      native.matrixClose(m.supplied_binary_density, density, "actual supplied noisy/ideal density");
      const probabilities = [0, 1, 2].map(b => b === p.phase ? (1-g)/3 : (2+g)/6);
      check(m.actual_probabilities.length === 3 && m.actual_probabilities.every((p, b) => Math.abs(p-probabilities[b]) < 3e-12), "actual anti-trine Born probabilities");
      const b = m.excluded_value_observed;
      check(Number.isInteger(b) && b >= 0 && b < 3 && probabilities[b] > 0, "actual possible measured value, not an assigned true secret");
      if (b === p.phase) forbidden++;
      const [row, value] = equation(p.k, b);
      rows.push(row); rhs.push(value);
      check(m.measurement_uses_hidden_secret === false && m.unknown_source_inverse_used === false, "fixed known measurement only");
      measured++;
    });
    const answer = eliminate(rows, rhs, D);
    check(d.coefficient_rank === answer.rank && d.source_exhaustion === null && c.forbidden_outcomes_fixture_only === forbidden, "exact rank and actual false exclusions");
    same(d.original_indices, accepted.map(p => p.id), "all consumed paid original ancestors");
    check(d.consumed_original_ancestors === M, "one distinct ancestor per calibration binary input");
    ["receiver_takes_hidden_secret", "classical_hypotheses_enumerated", "quantum_hardware_executed", "noisy_error_correcting_decoder_supplied", "growing_depth_hidden_shift_solved", "new_quantum_speedup_established", "source_promises_verified_by_receiver"].forEach(k => check(d[k] === false, "conditional base-case scope "+k));
    check(d.decoding_correctness_is_conditional_on_common_ideal_phase_source === true, "solution does not prove unknown source promises");
    if (index < 6) {
      check(forbidden === 0 && !answer.inconsistent && answer.rank === D && d.status === "IDEAL_TERMINAL_TERNARY_SECRET_DECODED", "actual ideal base-case decoding");
      same(d.lifted_solution, answer.solution, "exact F3 solved lift");
      const secret = answer.solution.slice(-n), products = basis(n).map(([i, j]) => mod(secret[i]*secret[j]));
      same(answer.solution.slice(0, -n), products, "rank-one symmetric lift, not arbitrary linear fit");
      same(d.recovered_ternary_secret, secret, "receiver output derived from actual observations");
      same(secret, truth, "ideal fixture correctness only");
    } else {
      check(forbidden > 0 && answer.inconsistent && d.status === "INCONSISTENT_EXCLUSION_EQUATIONS" && d.recovered_ternary_secret === null && d.lifted_solution === null, "noise falsifies true equations instead of certifying robust recovery");
    }
    originalCopies += projection.original_inputs_supplied;
  });
  const duals = dualCensuses(r.complete_dual_polynomial_censuses_dimension2);
  check(r.scaling_budgets.length === 6 && r.strict_decoder_noise_contracts.length === 16, "all scaling and noise contracts");
  r.scaling_budgets.forEach((b, i) => budget(b, [8, 16, 32, 64, 128, 256][i]));
  r.strict_decoder_noise_contracts.forEach((c, i) => {
    const n = [2, 4, 8, 16][Math.floor(i/4)], gamma = parse(["1", "99/100", "9/10", "0"][i % 4]), D = n*(n+1)/2+n, M = 3*D+16;
    const clean = power(E.div(E.add(rat(2n), gamma), rat(3n)), M);
    check(c.dimension === n && c.binary_copy_cap === M && c.uniform_input_visibility === str(gamma), "fixed IID equal-visibility regime");
    check(c.forbidden_outcome_probability_exact === str(E.div(sub(E.one, gamma), rat(3n))) && c.no_forbidden_outcomes_probability_exact === str(clean), "exact false exclusion and no-false-row probability");
    check(c.this_strict_decoder_correct_recovery_upper === str(clean) && c.this_strict_decoder_correct_recovery_lower === str(mul(clean, rat(511n, 512n))), "correct scoped noisy upper/lower bounds, no error correction assumed");
    check(c.robust_error_correction_implemented === false && c.all_quantum_receivers_excluded === false, "specific strict decoder, not a general impossibility");
  });
  return {status: "PASS", ideal_source_recoveries: 6, noisy_countercontrols: 2,
          terminal_measurements_replayed: measured, paid_original_qutrits_replayed: originalCopies,
          dual_polynomials_replayed: duals, new_quantum_speedup_established: false};
}
if (require.main === module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
module.exports = {run};

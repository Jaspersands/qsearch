"use strict";
// Independent cyclotomic preparation/reflection replay and rational ledgers.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js"), {chart} = require("./native_generalized_dihedral_crosscheck.js");
const {check, same, rat, parse, str, add, sub, mul, div, cmp, zero, one, field, matrices} = E;
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/reductions/known_preparation_coherent_reflection.json");
const IID = "INDEPENDENT_SYMMETRIC_ORIGINAL_ERRORS_INDEPENDENT_OF_LABELS";
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod = (a, m) => (a % m + m) % m;
const min = (a, b) => cmp(a, b) <= 0n ? a : b;
const eq = (saved, value, message) => check(saved === str(value), message);
const scale = (x, n) => mul(x, rat(BigInt(n)));
function power(x, n) {
  let result = one;
  while (n) { if (n % 2) result = mul(result, x); n = Math.floor(n/2); if (n) x = mul(x, x); }
  return result;
}
function fpow(K, x, n) {
  let result = K.unit;
  while (n) { if (n % 2) result = K.times(result, x); n = Math.floor(n/2); if (n) x = K.times(x, x); }
  return result;
}
function words(M) {
  let result = [[]];
  for (let j = 0; j < M; j++) result = result.flatMap(a => [0, 1, 2].map(t => [...a, t]));
  return result;
}
function shape(B, M) { check(Number.isSafeInteger(B) && B > 0 && (BigInt(B) & (BigInt(B)-1n)) === 0n && Number.isSafeInteger(M) && M > 0, "finite legal cohort shape"); }
function rank(matrix, n) {
  const A = matrix.map(r => r.slice()); let pivot = 0;
  for (let j = 0; j < n && pivot < A.length; j++) {
    const k = A.findIndex((r, i) => i >= pivot && r[j]);
    if (k < 0) continue;
    [A[k], A[pivot]] = [A[pivot], A[k]];
    const inverse = A[pivot][j]; A[pivot] = A[pivot].map(x => x*inverse % 3);
    for (let i = 0; i < A.length; i++) if (i !== pivot) { const a = A[i][j]; A[i] = A[i].map((x, c) => mod(x-a*A[pivot][c], 3)); }
    pivot++;
  }
  return pivot;
}
function central(saved, labels) {
  const L = saved.native_level, n = saved.dimension, B = labels.length, M = labels[0].length, C = chart(L);
  check(B === saved.cohorts && M === saved.sites_per_cohort, "actual central cohort layout");
  let z = [1n, 0n]; for (let j = 1; j < L; j++) z = C.mul(z, [-1n, 1n]);
  same(saved.central_generator.map(String), z.map(String), "actual pi^(L-1) central generator");
  const rows = labels.map(cohort => Array.from({length:n}, (_, i) => cohort.reduce((sum, label) => {
    const r = C.character(C.dual([label[i]]), C.coordinates([z]));
    check(3n*r[0] % r[1] === 0n, "central character order divides3");
    return (sum+Number(3n*r[0]/r[1])) % 3;
  }, 0)));
  same(saved.cohort_central_character_rows, rows, "independent native central-character rows");
  const differences = rows.slice(1).map(row => row.map((x, j) => mod(x-rows[0][j], 3)));
  const vectorRank = rank(rows, n), rayRank = rank(differences, n);
  check(saved.vector_stabilizer_central_rank === vectorRank && saved.ray_stabilizer_central_rank === rayRank, "actual vector and ray support ranks");
  for (const [key, A, r] of [["nonzero_extra_vector_stabilizer_witness", rows, vectorRank], ["nonzero_extra_ray_stabilizer_witness", differences, rayRank]]) {
    const v = saved[key];
    if (r === n) check(v === null, "no fabricated full-rank central witness");
    else check(v && v.length === n && v.some(x => x) && v.every(x => [0, 1, 2].includes(x)) && A.every(row => row.reduce((s, x, j) => s+x*v[j], 0) % 3 === 0), "nonzero legal central stabilizer witness");
  }
  same(saved.vector_kernel_order, {base:3, exponent:n-vectorRank}, "vector kernel count");
  same(saved.ray_kernel_order, {base:3, exponent:n-rayRank}, "ray kernel count");
  check(saved.full_hidden_subgroup_or_gap_established === false && saved.noisy_seed_necessarily_fixed_by_H === false, "central support not a full noisy stabilizer proof");
}
function preparation(c) {
  const r = c.recipe, B = r.cohorts, M = r.sites_per_cohort, q = Number(r.modulus), source = r.source_receipts;
  shape(B, M); check(q === 9 && r.native_even_level === 4, "committed exact phase-root control");
  const originals = source.original_classical_records, mask = source.preparation_random_mask;
  check(originals.length === 2*B*M && new Set(originals.map(r => r.source_id)).size === originals.length && source.original_record_count === originals.length && r.original_classical_record_count === originals.length, "all distinct paid original records");
  const phases = [], labels = [];
  // At even root9, the native frequency map is [[0,1],[1,0]].
  for (let b = 0; b < B; b++) {
    phases.push([]); labels.push([]);
    for (let j = 0; j < M; j++) {
      const pair = originals.slice(2*(b*M+j), 2*(b*M+j)+2);
      check(pair.every(a => a.modulus === q && a.label.length === r.secret_dimension && a.label.every(x => Number.isInteger(x) && x >= 0 && x < q) && Number.isInteger(a.value) && a.value >= 0 && a.value < q), "actual raw canonical records");
      const nums = [0, ...pair.map(a => mod(a.value+a.label.reduce((s, x, k) => s+x*mask[k], 0), q))];
      phases[b].push(nums);
      labels[b].push(pair[0].label.map((a, k) => [pair[1].label[k], a]));
      const receipt = source.known_source_receipts[b*M+j];
      same(receipt.known_phase_values, nums.slice(1).map(String), "actual classical phase receipt");
      same(receipt.raw_source_ids, pair.map(a => a.source_id), "original ancestry receipt");
      check(receipt.hidden_secret_or_errors_used === false, "no secret or latent error preparation input");
    }
  }
  same(r.known_phase_numerators, phases, "complete coherent source phases");
  same(r.public_native_labels, labels, "actual native label adapter");
  same(r.preparation_order, ["Hadamard_index_tensor_F3_sites", "known_controlled_diagonal"], "preparation order");
  same(r.inverse_order, ["known_controlled_diagonal_inverse", "Hadamard_index_tensor_F3_sites_inverse"], "actual inverse order");
  same(r.reflection_order, ["preparation_inverse", "zero_register_phase_flip", "preparation"], "actual reflection gate order");
  check(r.controlled_diagonal_branches_per_preparation_upper === 2*B*M && r.index_comparison_compute_uncompute_pairs_per_preparation_upper === B && r.preparation_calls_per_reflection === 2 && r.qutrit_Fourier_gates_per_preparation === M && r.index_Hadamards_per_preparation === Math.log2(B), "paid explicit multiplexor and Fourier cost");
  ["ideal_unknown_state_inverse_supplied", "secret_or_errors_read_by_preparation", "relative_cohort_phases_may_be_discarded", "new_independent_originals_created_by_reuse", "hardware_synthesis_implemented"].forEach(k => check(r[k] === false, "preparation access scope "+k));
  check(r.source_bank_reused_with_frozen_errors === true && r.zero_test_synthesis_is_a_remaining_obligation === true, "frozen bank and zero-test debt");
  const w = words(M), D = B*w.length, K = field(q), Q = matrices(K);
  check(c.literal_dimension === D && D <= 256, "bounded literal quantum replay");
  const nums = Array.from({length:B}, (_, b) => w.map(t => t.reduce((s, x, j) => s+phases[b][j][x], 0) % q)).flat();
  same(c.seed_basis_phase_numerators, nums, "cohort relative phase gauge is preserved");
  const A = nums.map((phase, i) => Array.from({length:D}, (_, j) => {
    const b = Math.floor(i/w.length), d = Math.floor(j/w.length);
    const parity = (b & d).toString(2).replace(/0/g, "").length % 2;
    const dot = w[i % w.length].reduce((s, t, k) => s+t*w[j % w.length][k], 0);
    return K.scale(K.powers[(phase+q/3*dot) % q], rat(parity ? -1n : 1n));
  }));
  const P = nums.map(a => nums.map(b => K.scale(K.powers[mod(a-b, q)], rat(1n, BigInt(D)))));
  const R = Q.plus(Q.identity(D), Q.scale(P, K.scale(K.unit, rat(-2n))));
  const scaledIdentity = Q.scale(Q.identity(D), K.scale(K.unit, rat(BigInt(D))));
  check(Q.eq(Q.times(Q.star(A), A), scaledIdentity), "exact full known preparation unitarity");
  check(Q.eq(Q.times(R, R), Q.identity(D)), "exact full reflection involution");
  // A^dagger R A = D*(I-2|0><0|), no floating sqrt(D).
  const target = scaledIdentity.map(row => row.slice()); target[0][0] = K.scale(K.unit, rat(-BigInt(D)));
  check(Q.eq(Q.times(Q.times(Q.star(A), R), A), target), "exact preparation/zero-phase/inverse reflection identity");
  central(c.central_support, labels);
  check(c.dense_control_is_a_scalable_receiver === false, "finite replay not a solver");
  return D;
}
function characteristic(c) {
  shape(c.cohorts, c.sites_per_cohort);
  const g = parse(c.characteristic), a = div(add(one, scale(g, 2)), rat(3n)), A = mul(a, a), C = div(add(add(rat(3n), scale(g, 4)), scale(mul(g, g), 2)), rat(9n));
  check(cmp(g, rat(-1n)) >= 0n && cmp(g, one) <= 0n && c.independence_promise === IID && c.source_law_inferred_from_records === false, "legal external characteristic promise");
  const f = add(power(A, c.sites_per_cohort), div(sub(power(C, c.sites_per_cohort), power(A, c.sites_per_cohort)), rat(BigInt(c.cohorts))));
  for (const [k, x] of [["single_overlap_mean", a], ["single_overlap_mean_squared", A], ["single_overlap_squared_mean", C], ["mean_seed_fidelity", f], ["mean_pure_trace_distance_squared", sub(one, f)], ["mean_reflection_operator_error_squared", scale(sub(one, f), 4)]]) eq(c[k], x, "exact characteristic identity "+k);
}
function exactIID(c) {
  const K = field(c.modulus), B = c.cohorts, M = c.sites_per_cohort, total = 2**(2*B*M);
  shape(B, M); check(B*M <= 4 && c.error_configurations_checked === total, "complete finite IID census");
  same(c.error_law, [[-1, "1/2"], [1, "1/2"]], "actual independent signed error law");
  let mean = K.F();
  for (let bits = 0; bits < total; bits++) {
    let overlap = K.F();
    for (let b = 0; b < B; b++) {
      let r = K.unit;
      for (let j = 0; j < M; j++) {
        const i = 2*(b*M+j), signs = [i, i+1].map(k => (bits >> k) & 1 ? 1 : c.modulus-1);
        r = K.times(r, K.scale(K.plus(K.unit, K.plus(...signs.map(e => K.powers[e]))), rat(1n, 3n)));
      }
      overlap = K.plus(overlap, K.scale(r, rat(1n, BigInt(B))));
    }
    mean = K.plus(mean, K.scale(K.times(overlap, K.conj(overlap)), rat(1n, BigInt(total))));
  }
  const g = K.scale(K.plus(K.powers[1], K.powers[c.modulus-1]), rat(1n, 2n));
  const a = K.scale(K.plus(K.unit, K.scale(g, rat(2n))), rat(1n, 3n)), A = K.times(a, a);
  const C = K.scale(K.plus(K.scale(K.unit, rat(3n)), K.plus(K.scale(g, rat(4n)), K.scale(K.times(g, g), rat(2n)))), rat(1n, 9n));
  const formula = K.plus(fpow(K, A, M), K.scale(K.plus(fpow(K, C, M), K.scale(fpow(K, A, M), rat(-1n))), rat(1n, BigInt(B))));
  check(K.eq(mean, formula), "independent full error census proves coherent fidelity identity");
  same(c.mean_fidelity_exact, K.encode(mean), "exact census fidelity certificate");
  same(c.formula_fidelity_exact, K.encode(formula), "exact formula certificate");
  const distance = K.plus(K.unit, K.scale(mean, rat(-1n)));
  same(c.mean_trace_distance_squared_exact, K.encode(distance), "exact squared trace distance");
  same(c.mean_reflection_operator_error_squared_exact, K.encode(K.scale(distance, rat(4n))), "exact squared reflection error");
}
const piCache = new Map(), cosineCache = new Map();
function piBounds(terms) {
  const id = JSON.stringify(terms);
  if (piCache.has(id)) return piCache.get(id);
  function atan(k, N) {
    check(Number.isInteger(N) && N > 0 && N < 1000, "bounded alternating enclosure work");
    let sum = zero;
    for (let j = 0; j < N; j++) sum = add(sum, rat(j % 2 ? -1n : 1n, BigInt(2*j+1)*BigInt(k)**BigInt(2*j+1)));
    const next = add(sum, rat(N % 2 ? -1n : 1n, BigInt(2*N+1)*BigInt(k)**BigInt(2*N+1)));
    return cmp(sum, next) <= 0n ? [sum, next] : [next, sum];
  }
  const a = atan(5, terms[0]), b = atan(239, terms[1]);
  const result = [sub(scale(a[0], 16), scale(b[1], 4)), sub(scale(a[1], 16), scale(b[0], 4))];
  piCache.set(id, result); return result;
}
function cosineInterval(q, k, N) {
  const id = `${q}:${k}:${N}`;
  if (cosineCache.has(id)) return cosineCache.get(id);
  // Dyadic recentering retains the full Machin radius without huge denominators.
  const pi = piBounds([N, N]), midpoint = div(add(...pi), rat(2n)), grid = 2n**120n;
  const center = rat(midpoint[0]*grid/midpoint[1], grid);
  const abs = x => x[0] < 0n ? [-x[0], x[1]] : x;
  const left = abs(sub(center, pi[0])), right = abs(sub(pi[1], center)), radius = cmp(left, right) > 0n ? left : right;
  const x = div(scale(center, 2*k), rat(BigInt(q))), x2 = mul(x, x);
  let term = one, sum = one;
  for (let j = 1; j < N; j++) { term = div(scale(mul(term, x2), -1), rat(BigInt((2*j-1)*(2*j)))); sum = add(sum, term); }
  let factorial = 1n; for (let j = 2; j <= 2*N; j++) factorial *= BigInt(j);
  const error = add(div(power(x, 2*N), rat(factorial)), div(scale(radius, 2*k), rat(BigInt(q))));
  const result = [sub(sum, error), add(sum, error)]; cosineCache.set(id, result); return result;
}
function sqrtInterval(raw, x, bits) {
  const [lo, hi] = raw.map(parse);
  check(cmp(lo, zero) >= 0n && cmp(lo, hi) <= 0n && cmp(mul(lo, lo), x) <= 0n && cmp(mul(hi, hi), x) >= 0n && cmp(sub(hi, lo), rat(1n, 2n**BigInt(bits))) <= 0n, "certified tight nonnegative sqrt enclosure");
  return hi;
}
function budget(b) {
  shape(b.cohorts, b.sites_per_cohort);
  const q = BigInt(b.modulus), V = parse(b.source_integer_second_moment_upper), T = BigInt(b.reflection_query_cap), K = BigInt(b.initial_point_seed_copies), bits = b.precision_bits;
  let root = q; while (root % 3n === 0n) root /= 3n;
  check(root === 1n && q >= 3n && T >= 0n && K >= 0n && bits > 0 && cmp(V, zero) >= 0n && b.IID_promise === IID, "external IID moment and finite query contract");
  check(b.original_classical_records_paid_once === String(2n*BigInt(b.cohorts)*BigInt(b.sites_per_cohort)), "fixed-bank original costs");
  const pi = piBounds(b.Machin_terms); same(b.pi_interval, pi.map(str), "independent rational Machin enclosure");
  const constant = b.cohorts === 1 ? rat(16n, 9n) : rat(8n, 3n), e2 = min(one, div(mul(mul(mul(constant, pi[1]), pi[1]), scale(V, b.sites_per_cohort)), rat(q*q)));
  eq(b.moment_constant, constant, "correct tensor versus coherent-cohort moment constant");
  eq(b.mean_pure_trace_distance_squared_upper, e2, "B-independent composite seed error");
  const rms = sqrtInterval(b.sqrt_e2_interval, e2, bits), initial = sqrtInterval(b.sqrt_K_e2_interval, scale(e2, K), bits);
  const du = parse(b.complete_preparation_operator_error_promise), ds = parse(b.zero_phase_operator_error_promise), rounding = parse(b.source_rounding_loss_upper), other = parse(b.complete_receiver_other_operations_loss_promise);
  [du, ds, rounding, other].forEach(x => check(cmp(x, zero) >= 0n && cmp(x, one) <= 0n, "complete implementation promises"));
  const hardwareInitial = sqrtInterval(b.sqrt_K_delta_U_squared_interval, scale(mul(du, du), K), bits);
  const noise = min(one, add(initial, scale(rms, 2n*T))), hardware = min(one, add(add(hardwareInitial, scale(add(scale(du, 2), ds), T)), other)), total = min(one, add(add(noise, hardware), rounding));
  eq(b.averaged_complete_receiver_noise_loss_upper, noise, "frozen-bank complete hybrid loss");
  eq(b.complete_hardware_loss_upper, hardware, "complete unitary synthesis ledger");
  eq(b.complete_success_loss_upper, total, "composed loss includes rounding");
  check(b.bound_is_nonvacuous === (cmp(total, one) < 0n), "nonvacuity not guaranteed");
  ["noise_is_resampled_per_reflection", "averaged_copy_density_bound_used_as_operator_bound", "arbitrary_diagonal_queries_or_phase_powers_covered", "source_independence_established_by_unique_IDs", "receiver_or_classical_separation_supplied"].forEach(k => check(b[k] === false, "reflection bound scope "+k));
  check(b.arbitrary_work_register_allowed_in_hybrid === true, "hybrid covers arbitrary attached work");
}
function gap(c) {
  const n = BigInt(c.dimension), L = BigInt(c.native_level), B = BigInt(c.Hadamard_cohort_count), eps = parse(c.nonhidden_absolute_overlap_upper), h = c.bank_failure_bits;
  check(n > 0n && L >= 2n && h > 0 && B > 0n && (B & (B-1n)) === 0n && cmp(eps, zero) > 0n && cmp(eps, one) < 0n, "legal finite-bank gap parameters");
  const threshold = div(rat(4n*(2n*(n*L+1n)+2n+BigInt(h))), mul(eps, eps));
  eq(c.conservative_cohort_threshold, threshold, "correct simultaneous complex Hoeffding threshold");
  check(cmp(rat(B), threshold) >= 0n && cmp(rat(B/2n), threshold) < 0n, "smallest legal power-of-two bank");
  eq(c.ideal_absolute_overlap_gap_lower, sub(one, eps), "absolute overlap gap");
  eq(c.bank_failure_upper, rat(1n, 2n**BigInt(h)), "conditional IID ideal bank event");
  same(c.group_order_compact, {base:3, exponent:Number(n*L+1n)}, "actual native group size");
  check(c.original_classical_records_required === String(2n*B*BigInt(c.sites_per_cohort)), "cohort source accounting");
  same(c.seed_dimension_compact, {coefficient:String(B), base:3, exponent:c.sites_per_cohort}, "tensor seed dimension, no dense materialization");
  check(c.native_backend_within_current_level_cap === (L <= 512n) && c.resource_profile_is_an_executed_bank === false, "formal large-level profile does not imply backend execution");
  ["observed_bank_has_been_certified", "efficient_subgroup_decoder_supplied", "gap_guarantee_includes_noise", "accepted_speedup_candidate"].forEach(k => check(c[k] === false, "bank-gap scope "+k));
}
function falsifiers(r) {
  const f = r.frozen_bank_copy_budget_falsifier, q = f.modulus, T = f.reflections_of_noisy_bank, theta = 2*Math.PI/q;
  check(q === 81 && T === 20 && f.averaged_copy_budget_falsified === true && f.candidate_algorithm === false && f.source_model_changed_by_fresh_error_each_call === false, "fixed operational counterexample, not candidate");
  const close = (x, y) => check(Number.isFinite(x) && Math.abs(x-y) < 2e-11, "independent diagnostic counterexample replay");
  f.actual_minus_probability_per_frozen_error.forEach(x => close(x, Math.sin(T*theta)**2));
  close(f.analytic_minus_probability, Math.sin(T*theta)**2); close(f.averaged_copy_trace_distance, (1-Math.cos(theta))/2);
  close(f.invalid_T_times_copy_budget, T*(1-Math.cos(theta))/2);
  f.reflection_operator_errors.forEach(x => close(x, 2*Math.sin(theta/2)));
  const N = 24, c = cosineInterval(q, 1, N), p = cosineInterval(q, 2*T, N);
  const cb = f.copy_trace_distance_box.map(parse), pb = f.actual_minus_probability_box.map(parse);
  check(cmp(cb[0], div(sub(one, c[1]), rat(2n))) <= 0n && cmp(cb[1], div(sub(one, c[0]), rat(2n))) >= 0n && cmp(pb[0], div(sub(one, p[1]), rat(2n))) <= 0n && cmp(pb[1], div(sub(one, p[0]), rat(2n))) >= 0n, "independent analytic Born enclosures");
  check(f.falsifier_is_certified_by_rational_boxes === true && cmp(pb[0], scale(cb[1], T)) > 0n, "rational proof of copy-oracle budget failure");
  const cfail = r.correlated_bank_IID_budget_falsifier, K = field(cfail.modulus), M = cfail.sites_per_cohort;
  check(cfail.modulus === 81 && M === 8 && cfail.cohorts === 2 && cfail.source_independence_promise_satisfied === false && cfail.universal_noise_no_go === false, "explicit correlated law, not universal obstruction");
  const z = fpow(K, K.scale(K.plus(K.unit, K.scale(K.powers[1], rat(2n))), rat(1n, 3n)), M);
  const re = K.scale(K.plus(z, K.conj(z)), rat(1n, 2n));
  const opposite = fpow(K, K.scale(K.plus(K.unit, K.plus(K.powers[1], K.powers[80])), rat(1n, 3n)), M);
  const exact = K.plus(K.unit, K.scale(K.plus(K.times(re, re), K.times(opposite, opposite)), rat(-1n, 2n)));
  same(cfail.mean_trace_distance_squared_exact, K.encode(exact), "actual correlated coherent fidelity");
  // Evaluate the real reduced polynomial with independent rational cosine boxes.
  let lo = zero, hi = zero;
  exact.forEach((x, k) => { if (!x[0]) return; const box = cosineInterval(81, k, 24); lo = add(lo, mul(x, x[0] > 0n ? box[0] : box[1])); hi = add(hi, mul(x, x[0] > 0n ? box[1] : box[0])); });
  const savedBox = cfail.certified_mean_trace_distance_squared_box.map(parse);
  check(cmp(savedBox[0], lo) <= 0n && cmp(savedBox[1], hi) >= 0n, "independent correlated-error probability enclosure");
  budget(cfail.misapplied_IID_budget);
  const wrong = parse(cfail.misapplied_IID_budget.mean_pure_trace_distance_squared_upper);
  check(cfail.falsifier_is_certified_by_rational_boxes === true && cmp(lo, wrong) > 0n && cmp(savedBox[0], wrong) > 0n, "rational IID-bound violation under correlation");
}
function run(r) {
  check(r.status === "CONDITIONAL_KNOWN_BANK_REFLECTION_ACCESS_EXTERNAL_REVIEW_PENDING", "review-pending scoped access status");
  check(r.producer_sha256 === hash(path.join(ROOT, "theorems/known_preparation_coherent_reflection.py")) && r.derivation_sha256 === hash(path.join(ROOT, "research/KNOWN_PREPARATION_COHERENT_REFLECTION.md")) && r.source_constructor_sha256 === hash(path.join(ROOT, "theorems/native_noisy_phase_input.py")), "pinned actual producer, derivation and source");
  ["unknown_quantum_only_phase_sources_covered", "generic_known_preparation_classical_simulation_proved", "quantum_hardware_executed", "efficient_receiver_supplied", "hardness_transfer_admitted", "accepted_speedup_candidate", "new_active_negative_result_created"].forEach(k => check(r[k] === false, "unsupported promotion "+k));
  check(r.preparation_controls.length === 4 && r.exact_IID_error_controls.length === 4 && r.characteristic_controls.length === 5 && r.scalable_reflection_budgets.length === 4 && r.conditional_bank_gap_budgets.length === 4, "complete control coverage");
  same(r.preparation_controls.map(c => [c.recipe.cohorts, c.recipe.sites_per_cohort]), [[1,3], [2,1], [2,2], [4,2]], "committed original-data preparation controls");
  same(r.exact_IID_error_controls.map(c => [c.modulus, c.cohorts, c.sites_per_cohort]), [[3,1,1], [9,1,2], [9,2,1], [9,2,2]], "committed exact original-error censuses");
  const dimensions = r.preparation_controls.map(preparation);
  r.exact_IID_error_controls.forEach(exactIID); r.characteristic_controls.forEach(characteristic);
  r.scalable_reflection_budgets.forEach((c, j) => { budget(c.budget); check(String(c.budget.cohorts) === r.conditional_bank_gap_budgets[j].Hadamard_cohort_count && c.budget.sites_per_cohort === r.conditional_bank_gap_budgets[j].sites_per_cohort, "noise and ideal-bank ledgers share one cohort layout"); });
  r.conditional_bank_gap_budgets.forEach(gap); falsifiers(r);
  return {status:"PASS", exact_preparation_dimensions:dimensions, IID_error_censuses:4, scalable_budgets:4, falsifiers:2, accepted_speedup_candidate:false};
}
if (require.main === module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
module.exports = {run, budget, gap, central};

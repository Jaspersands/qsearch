"use strict";
// Independent integer/rational scope and original-bank baseline replay.
// Gaussian enclosures remain trusted inputs, separately replayed by Python/Arb.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js"), B = require("./native_basis_lottery_crosscheck.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one} = E;
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/reductions/native_refresh_crossover_scope_audit.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const enc = x => x <= 9007199254740991n && x >= -9007199254740991n ? Number(x) : String(x);
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, m) => E.same(canonical(a), canonical(b), m);
const min = (a, b) => cmp(a, b) <= 0n ? a : b;
const mod = (a, q) => (a % q + q) % q;

function scope(p) {
  const n = p.dimension, r = p.original_root_digits, m = p.original_rows, k = p.refreshed_rows;
  const lo = p.min_refresh_root_digits, hi = p.max_refresh_root_digits, C = p.modulo_scale_dag_pruning_ledger.declared_centered_coefficient_bound;
  [n, r, m, k, lo, hi, C].forEach(v => check(Number.isSafeInteger(v) && v > 0, "positive complete scope"));
  check(lo <= hi && hi <= r && r <= 4096, "declared root interval");
  const a = parse(p.alpha_original), q = 3n ** BigInt(r), scaled = mul(rat(8n * q), a);
  check(cmp(a, zero) > 0n && cmp(a, one) < 0n, "source width");
  const R = (scaled[0] + scaled[1] - 1n) / scaled[1];
  let dc = 0;
  while (dc + 1 < r && 3n ** BigInt(dc + 1) <= BigInt(C)) dc++;
  const rows = Array.from({length: hi - lo + 1}, (_, j) => {
    const d = lo + j, g = 3n ** BigInt(d), L = q / g;
    return {root_digits: d, modulus: enc(g), original_scale: enc(L),
      reachable_from_declared_first_coefficient_bound: d <= dc,
      covered_by_original_radius_nonwrapping_gate: 4n * R < L};
  });
  const reachable = rows.filter(x => x.reachable_from_declared_first_coefficient_bound).map(x => x.root_digits);
  const joint = rows.filter(x => x.reachable_from_declared_first_coefficient_bound && x.covered_by_original_radius_nonwrapping_gate).map(x => x.root_digits);
  const issues = [];
  if (!reachable.length) issues.push("REFRESH_WINDOW_UNREACHABLE_AFTER_DECLARED_FIRST_STEP");
  if (rows.some(x => !x.covered_by_original_radius_nonwrapping_gate)) issues.push("REFRESH_WINDOW_OUTSIDE_MODULO_SCALE_PRUNING_SCOPE");
  return {dimension: n, original_root_digits: r, original_rows: m, refreshed_rows: k,
    alpha_original: str(a), declared_centered_coefficient_bound: C, original_modulus: enc(q),
    recomputed_Gaussian_radius: enc(R), maximum_first_child_digits: dc,
    declared_refresh_min_digits: lo, declared_refresh_max_digits: hi, refresh_root_checks: rows,
    reachable_refresh_digits: reachable, jointly_covered_refresh_digits: joint, scope_issues: issues,
    composed_recovery_failure_upper_certified: null,
    external_producer_sampler_and_composition_still_required: true,
    selected_coefficient_bound_is_actual_producer_coverage: false};
}

function energy(C) {
  const m = BigInt(C.original_rows), k = BigInt(C.output_rows), a = parse(C.alpha_original);
  const b = parse(C.alpha_target), e = parse(C.eta_noise), dm = C.min_refresh_digits, dt = C.terminal_digits;
  check(m > 0n && k > 0n && Number.isSafeInteger(dt) && Number.isSafeInteger(dm) && dt > 0 && dm > dt, "energy scope");
  [a, b, e].forEach(v => check(cmp(v, zero) > 0n && cmp(v, one) < 0n, "positive widths"));
  const req = div(mul(mul(e, e), mul(b, b)), rat(4n * k));
  const hm = div(sub(req, rat(m, 2n * 3n ** BigInt(2 * dm))), rat(2n));
  const ht = div(sub(req, rat(m, 2n * 3n ** BigInt(2 * dt))), rat(2n));
  check(cmp(hm, zero) > 0n, "positive H_min");
  const delta = div(mul(rat(m), mul(a, a)), mul(rat(6n), hm)), beta = mul(a, rat(3n ** BigInt(dt)));
  const implication = cmp(ht, zero) > 0n ? null : cmp(mul(beta, beta), mul(rat(3n, 2n), delta)) < 0n;
  check(implication !== false && C.H_min === str(hm) && C.H_terminal === str(ht) && C.unclamped_energy_failure_bound === str(delta) && C.terminal_beta === str(beta), "exact crossover energy");
  check(C.beta_squared_lt_three_halves_delta_IF_H_terminal_nonpositive === implication && C.dimension_free_lottery_success_established === false, "crossover is not automatic lottery success");
}

function counter(C) {
  const n = BigInt(C.dimension), T = C.disjoint_trials, g = BigInt(C.derived_modulus);
  check(n === 3n ** 80n && T === 128 && g === 3n ** 85n, "declared analytical counterprofile");
  energy(C.energy_crossover);
  const e = C.energy_crossover, Z = C.Gaussian_zero_law, W = C.nonzero_ring_wrap_tail;
  check(BigInt(e.original_rows) === n * BigInt(T) && BigInt(e.output_rows) === n && e.alpha_original === str(rat(1n, 10n * g)) && e.alpha_target === "1/4" && e.eta_noise === "1/4" && e.min_refresh_digits === 86 && e.terminal_digits === 85, "counterprofile energy matched to bank");
  check(Z.continuous_Gaussian_width === "1/10" && W.continuous_Gaussian_width === "1/10" && BigInt(W.integer_error_radius) === g - 1n && Z.enclosure_bits === 192 && W.enclosure_bits === 192, "Gaussian laws and wraps");
  [Z.zero, W].forEach(v => check(cmp(parse(v.lower), zero) >= 0n && cmp(parse(v.lower), parse(v.upper)) <= 0n && cmp(parse(v.upper), one) <= 0n, "Gaussian enclosure range only; Arb replay separate"));
  const ring = min(one, add(parse(Z.zero.upper), parse(W.upper))), escape = sub(one, ring);
  const block = escape[0] ? (escape[1] + escape[0] - 1n) / escape[0] : null;
  const blocks = block === null ? 0n : n / block, exponent = blocks < 192n ? blocks : 192n;
  const single = rat(1n, 2n ** exponent), any = min(one, mul(rat(BigInt(T)), single));
  check(C.one_row_ring_zero_probability_upper === str(ring) && C.row_ring_escape_probability_lower === str(escape) && C.reciprocal_Bernoulli_block === (block === null ? null : enc(block)) && BigInt(C.complete_probability_blocks) === blocks, "ring-zero reciprocal Bernoulli blocks");
  check(C.one_correct_basis_probability_upper === str(single) && C.any_correct_basis_probability_upper === str(any) && C.no_correct_basis_probability_lower === str(sub(one, any)), "dimension-dependent strategy failure");
  const falsified = cmp(parse(e.unclamped_energy_failure_bound), rat(1n, 100n)) < 0n && e.beta_squared_lt_three_halves_delta_IF_H_terminal_nonpositive === true && cmp(sub(one, any), rat(99n, 100n)) > 0n;
  check(C.dimension_free_high_probability_inference_falsified === falsified && falsified, "small delta does not remove dimension debt");
  check(C.bank_was_executed === false && C.current_n32_n128_lottery_profiles_falsified === false && C.arbitrary_classical_or_quantum_decoder_lower_bound_proved === false && C.IID_Gaussian_errors_AND_true_fixed_prefix_required === true && C.basis_labels_selected_independently_of_errors_required === true, "counterexample scope and access");
  check(Z.independent_transcendental_certificate_supplied === false, "trusted transcendental provenance");
}

function control(C, source) {
  same(C.original_records, source.original_records, "same original bank");
  same(C.original_secret_FOR_POST_SOLVE_COMPARISON_ONLY, source.original_secret_FOR_CALIBRATION_ONLY, "post-solve truth only");
  const raw = C.original_records, q = BigInt(raw[0].modulus), first = source.pipeline_result.refresh_pruning_stages[0];
  const mask = first.refresh_batch.reduction_side_secret_mask;
  same(C.first_supplied_mask, mask, "original supplied mask");
  same(C.first_supplied_unmask_receipts, first.unmask_receipts, "all root receipts retained");
  const pairs = first.unmask_receipts.map(u => {
    const c = BigInt(u.signed_coefficient), w = u.masked_multiple.map((v, i) => enc(mod(BigInt(v) + c * BigInt(mask[i]), q)));
    same(w, u.unmasked_multiple, "root unmask checked");
    return [enc(c), w];
  });
  same(C.supplied_original_root_candidates, pairs, "all supplied root pairs");
  check(C.verification_radius === source.verification_radius, "matched verification radius");
  const cache = {ranks: new Set(), inverses: new Set()}, trials = pairs.map(([c, w]) => B.complete(raw, BigInt(c), w, BigInt(C.verification_radius), {max_blocks: 10000, max_minor_entries: 65536}, cache));
  const fits = [];
  trials.forEach(t => {if (t.candidate_secret !== null && !fits.some(s => JSON.stringify(s) === JSON.stringify(t.candidate_secret))) fits.push(t.candidate_secret);});
  const result = {original_records_sha256: trials[0].original_records_sha256, original_records_paid_once: raw.length,
    root_candidate_completions: trials, fitting_secrets: fits, public_label_rank_calls: cache.ranks.size,
    public_ring_inverse_calls: cache.inverses.size, original_response_rounding_evaluations: trials.reduce((s, t) => s + t.original_response_rounding_evaluations, 0),
    original_candidate_verification_evaluations: trials.reduce((s, t) => s + t.original_candidate_verification_evaluations, 0),
    additional_producer_calls: 0, additional_refresh_batches: 0, new_original_samples_created: false, source_law_or_planted_truth_certified: false};
  same(C.original_baseline, result, "independent entire original-bank completion and paid cache replay");
  const matched = fits.some(s => JSON.stringify(s) === JSON.stringify(C.original_secret_FOR_POST_SOLVE_COMPARISON_ONLY));
  check(C.same_calibration_secret_recovered_without_later_stages === matched && C.supplied_candidates_are_generated_by_an_actual_producer === false && C.calibration_dominance_proves_global_no_go === false, "conditional classical comparison only");
}

function verify(R) {
  const reviewedPath = path.join(ROOT, "research/reductions/native_refresh_lottery_crossover.json"), reviewed = JSON.parse(fs.readFileSync(reviewedPath));
  check(R.status === "CROSSOVER_ALGEBRA_USEFUL_COMPOSED_ROUTE_SCOPE_FAILED_CONTROLS_CLASSICALLY_DOMINATED" && R.producer_sha256 === hash(path.join(ROOT, "theorems/native_refresh_crossover_scope_audit.py")) && R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_REFRESH_CROSSOVER_SCOPE_AUDIT.md")) && R.reviewed_artifact_sha256 === hash(reviewedPath), "current audit and untrusted reviewed artifact");
  const deps = ["native_basis_lottery.py", "native_classical_modulus_descent.py", "native_gaussian_quotient_completion.py", "native_small_multiple_completion.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py"];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));
  same(R.scaling_scope_audits, reviewed.composed_scaling_profiles.map(scope), "independent composed scope audit");
  check(R.original_baseline_controls.length === reviewed.actual_composed_pipeline_controls.length, "all controls compared");
  R.original_baseline_controls.forEach((c, i) => control(c, reviewed.actual_composed_pipeline_controls[i]));
  counter(R.dimension_counterprofile);
  check(R.reviewed_artifact_is_assumed_verified === false && R.accepted_speedup_candidate === false && R.new_active_negative_result_created === false && R.general_source_refresh_or_quantum_no_go_claimed === false && R.research_decision === "KEEP_CROSSOVER_LEMMA_REJECT_CURRENT_COMPOSITION_RETURN_TO_ACTUAL_QUANTUM_MECHANISM", "no promoted unproved quantum or general no-go claim");
  return {verified: true, scope_profiles: R.scaling_scope_audits.length, original_baseline_controls: R.original_baseline_controls.length,
    dimension_counterprofile_checked: true, independent_transcendental_certificate_supplied: false};
}
module.exports = {verify, scope, energy, counter};
if (require.main === module) console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT))), null, 2));

"use strict";
// Independent exact replay for Micciancio-Peikert prime-power Hensel probes and sample expansion ledgers.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const D = require("./native_gaussian_dither_sampler_crosscheck.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_mp12_prime_power_search_to_decision_audit.json");
const mod = (x, q) => (x % q + q) % q;
const enc = x => x <= 9007199254740991n && x >= -9007199254740991n ? Number(x) : String(x);
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a, b) => cmp(a, b) <= 0n ? a : b;
const max = (a, b) => cmp(a, b) >= 0n ? a : b;

function isqrt(n) {
  if (n < 2n) return n;
  let x = 1n << BigInt((n.toString(2).length + 1) >> 1);
  while (true) {
    const y = (x + n / x) >> 1n;
    if (y >= x) return x;
    x = y;
  }
}

function ceilLog2(m) {
  const v = BigInt(m);
  check(v >= 1n, "positive integer for ceilLog2");
  return v === 1n ? 0 : (v - 1n).toString(2).length;
}

function ceilSqrtRat(q) {
  if (q[0] === 0n) return zero;
  const prod = q[0] * q[1];
  let s = isqrt(prod);
  if (s * s < prod) s += 1n;
  return rat(s, q[1]);
}

function checkProbeBatch(raw, B) {
  const q = BigInt(B.modulus_q), n = B.dimension_n, m = B.batch_rows_m;
  const l = B.level_l, j = B.coordinate_j, d = BigInt(B.candidate_digit_d);
  const sLow = B.known_lower_prefix_s_low.map(BigInt);
  let qTmp = q, r = 0;
  while (qTmp % 3n === 0n) { qTmp /= 3n; r++; }
  check(qTmp === 1n && m === raw.length && B.probed_records.length === m && B.probe_receipts.length === m, "valid probe batch dimensions");
  B.probe_receipts.forEach((rc, idx) => {
    const orig = raw[idx];
    const u = BigInt(rc.probe_u), ew = BigInt(rc.widen_dither);
    const shiftA = mod(u * (3n ** BigInt(r - 1 - l)), q);
    const newLabel = orig.label.map((a, i) => enc(mod(BigInt(a) + (i === j ? shiftA : 0n), q)));
    const pDot = mod(orig.label.reduce((acc, a, i) => acc + BigInt(a) * sLow[i], 0n), q);
    const shiftY = mod(u * (3n ** BigInt(r - 1)) * d, q);
    const newVal = enc(mod(BigInt(orig.value) - pDot + shiftY + ew, q));
    const expectedRec = {
      label: newLabel,
      value: newVal,
      modulus: enc(q),
      source_id: `${orig.source_id}:mp12:l${l}:j${j}:d${d}:u${u}`,
    };
    same(rc.probed_record, expectedRec, "probed record in receipt");
    same(B.probed_records[idx], expectedRec, "probed record in batch");
  });
  check(B.original_records_paid_once === m && B.fresh_probe_randomness_is_a_fresh_original_sample === false, "probe batch honesty flags");
}

function checkSubgroupCensus(C) {
  const r = C.root_digits_r, l = C.hensel_level_l, q = 3 ** r;
  const topSub = [0, 3 ** (r - 1), 2 * (3 ** (r - 1))];
  same(C, {
    root_digits_r: r,
    modulus_q: q,
    hensel_level_l: l,
    order_3_top_subgroup: topSub,
    secrets_and_labels_pairs_checked: q * q,
    true_digit_zero_shift_invariance_checks: q * q,
    false_digit_subgroup_bijection_checks: 2 * q * q,
    false_lower_prefix_all_d_noninvariant_checks: l >= 1 ? q * q : 0,
    all_true_digits_preserve_error_law: true,
    all_false_digits_biject_onto_order3_subgroup: true,
    false_lower_prefix_invalidates_all_candidate_digits: l >= 1,
  }, "complete Hensel subgroup census");
}

function checkCoupledLedger(L) {
  const n = L.dimension_n, r = L.root_digits_r, q = 3n ** BigInt(r);
  const mDec = L.decision_rows_per_query_m_dec;
  const h = (n + 1).toString(2).length;
  const aDec = parse(L.decision_continuous_width_alpha_dec);
  const aSearch = div(aDec, rat(BigInt(h * h)));
  const added2 = sub(mul(aDec, aDec), mul(aSearch, aSearch));
  const tvSq = div(rat(11n * BigInt(mDec), 28n * q * q), added2);
  const tvRound = min(one, ceilSqrtRat(tvSq));
  const sigFloor = mul(mul(rat(q), aDec), sub(one, rat(1n, BigInt(h ** 4))));
  D.checkDrawParameters(L.certified_dither_sampler_draw_parameters);
  check(L.certified_dither_sampler_draw_parameters.sigma === str(sigFloor), "sigma_widen_floor matches draw parameters");
  const perDrawLoss = parse(L.certified_dither_sampler_draw_parameters.per_draw_coupling_loss_upper);
  const batchSamplerLoss = min(one, mul(rat(BigInt(mDec)), perDrawLoss));
  const gammaIdeal = parse(L.assumed_ideal_decision_advantage_EXTERNAL);
  const deltaTot = parse(L.total_recovery_failure_target);
  const gammaEff = max(zero, sub(sub(gammaIdeal, mul(rat(2n), tvRound)), mul(rat(2n), batchSamplerLoss)));
  const tests2nr = 2 * n * r;
  const ratioTarget = div(rat(BigInt(4 * n * r)), deltaTot);
  const invTarget = ceilLog2(ratioTarget[0] / ratioTarget[1] + 1n);
  let reps = null, totQueries = null, totSamples = null, mult = null;
  if (cmp(gammaEff, zero) > 0n) {
    const repFrac = div(rat(BigInt(2 * invTarget)), mul(gammaEff, gammaEff));
    let rVal = (repFrac[0] + repFrac[1] - 1n) / repFrac[1];
    if (rVal % 2n === 0n) rVal += 1n;
    reps = Number(rVal);
    totQueries = tests2nr * reps;
    totSamples = totQueries * mDec;
    mult = totQueries;
  }
  check(
    BigInt(L.modulus_q) === q &&
    L.smoothing_parameter_h === h &&
    L.search_continuous_width_alpha_search === str(aSearch) &&
    L.widening_width_squared_alpha_dec_sq_minus_alpha_search_sq === str(added2) &&
    L.rounded_input_widening_TV_squared_upper === str(tvSq) &&
    L.rounded_input_widening_TV_upper === str(tvRound) &&
    L.sigma_widen_rational_floor === str(sigFloor) &&
    L.per_query_dither_sampler_TV_loss_upper === str(batchSamplerLoss) &&
    L.effective_decision_advantage_lower_after_widening_and_sampler === str(gammaEff) &&
    L.total_coordinate_level_hypothesis_tests_2nr === tests2nr &&
    L.majority_repetitions_per_hypothesis_test === reps &&
    L.total_decision_oracle_queries === totQueries &&
    L.total_disjoint_original_search_samples_required === totSamples &&
    L.sample_expansion_multiplier_over_single_query_bank === mult &&
    L.fixed_single_query_bank_suffices === false &&
    L.actual_decision_algorithm_supplied === false,
    "coupled MP12 reduction ledger"
  );
}

function verify(R) {
  check(
    R.status === "MP12_PRIME_POWER_HENSEL_PROBE_AND_SAMPLE_EXPANSION_AUDIT_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/native_mp12_prime_power_search_to_decision_audit.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_MP12_PRIME_POWER_SEARCH_TO_DECISION_AUDIT.md")) &&
    R.contract_sha256 === hash(path.join(ROOT, "research/hypotheses/native_mp12_prime_power_search_to_decision_audit_contract.json")),
    "producer, derivation and contract hashes"
  );
  const deps = [
    "native_affine_fibre_relaxation.py",
    "native_basis_lottery.py",
    "native_gaussian_dither_sampler.py",
    "native_small_multiple_completion.py",
    "native_word_span_decision.py",
    "ternary_covariant_noise.py",
    "ternary_measured_lattice_decoder.py",
    "ternary_noise_degradation.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  const ctrl = R.hensel_probe_batch_control;
  checkProbeBatch(ctrl.original_records, ctrl.true_digit_probe_batch);
  checkProbeBatch(ctrl.original_records, ctrl.false_digit_probe_batch);

  check(R.complete_hensel_subgroup_censuses.length === 3, "3 Hensel subgroup censuses");
  R.complete_hensel_subgroup_censuses.forEach(checkSubgroupCensus);

  check(R.coupled_mp12_reduction_ledgers.length === 4, "4 coupled MP12 reduction ledgers");
  R.coupled_mp12_reduction_ledgers.forEach(checkCoupledLedger);

  check(
    R.actual_decision_algorithm_supplied === false &&
    R.fixed_single_query_bank_suffices === false &&
    R.worst_case_lattice_reduction_compatibility_established === false &&
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.novelty_claim === false,
    "honesty guardrails"
  );

  return {
    verified: true,
    subgroup_censuses: R.complete_hensel_subgroup_censuses.length,
    coupled_ledgers: R.coupled_mp12_reduction_ledgers.length,
    actual_decision_algorithm_supplied: false,
  };
}

module.exports = {
  verify,
  checkProbeBatch,
  checkSubgroupCensus,
  checkCoupledLedger,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}

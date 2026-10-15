"use strict";
// Independent exact replay for the certified rounded-Gaussian dither and sign/mask batch sampler.
// Transcendental Arb tail boxes remain trusted inputs replayed separately via --check-probabilities.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const S = require("./native_source_refresh_crosscheck.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_gaussian_dither_sampler.json");
const enc = x => x <= 9007199254740991n && x >= -9007199254740991n ? Number(x) : String(x);
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a, b) => cmp(a, b) <= 0n ? a : b;
const max = (a, b) => cmp(a, b) >= 0n ? a : b;

function exactInt(x) {
  check(typeof x === "number" ? Number.isSafeInteger(x) : typeof x === "string" && /^-?(0|[1-9][0-9]*)$/.test(x), "canonical exact integer");
  const y = BigInt(x);
  same(enc(y), x, "canonical large integer encoding");
  return y;
}

function ceilLog2(m) {
  const v = BigInt(m);
  check(v >= 1n, "positive integer for ceilLog2");
  return v === 1n ? 0 : (v - 1n).toString(2).length;
}

function ceilRat(q) {
  return (q[0] + q[1] - 1n) / q[1];
}

function floorDiv2(a) {
  return a >= 0n ? a / 2n : -((-a + 1n) / 2n);
}

function checkDrawParameters(P, kOverride = null) {
  const sig = parse(P.sigma), f = P.failure_bits_target;
  check(cmp(sig, zero) > 0n && Number.isSafeInteger(f) && f >= 1, "positive sigma and failure bits");
  const fSig = mul(rat(BigInt(f)), sig);
  const B = max([ceilRat(fSig), 1n], [1n, 1n])[0];
  const minK = f + ceilLog2(16n * (B + 1n));
  const K = kOverride !== null ? kOverride : P.active_dyadic_bits_K;
  if (kOverride === null) check(P.active_dyadic_bits_K === minK || P.using_uncertified_K_override === true, "certified K");
  const numThresh = 2n * B + 2n;
  const maxQueries = BigInt(ceilLog2(2n * B + 1n) + 2);
  const maxWidth = rat(2n, 2n ** BigInt(K));
  const adaptiveUnion = min(one, rat(4n * numThresh, 2n ** BigInt(K)));
  const naiveBound = min(one, rat(4n * maxQueries, 2n ** BigInt(K)));
  const ratio = rat(numThresh, maxQueries);
  const exp3f2 = Math.min(512, 3 * f * f);
  const tail3f2 = rat(1n, 2n ** BigInt(exp3f2));
  const tailf1 = rat(1n, 2n ** BigInt(f + 1));
  const perDraw = min(one, add(adaptiveUnion, tailf1));
  const target = rat(1n, 2n ** BigInt(f));
  same(P, {
    sigma: str(sig),
    failure_bits_target: f,
    truncation_bound_B: enc(B),
    minimum_certified_dyadic_bits_K: minK,
    active_dyadic_bits_K: K,
    using_uncertified_K_override: K < minK,
    total_binary_search_thresholds_2B_plus_2: enc(numThresh),
    max_single_path_queries_ceil_log2_2B_plus_1_plus_2: Number(maxQueries),
    required_cdf_enclosure_max_width: str(maxWidth),
    adaptive_all_threshold_precision_abort_upper: str(adaptiveUnion),
    naive_query_count_precision_bound_DO_NOT_USE: str(naiveBound),
    adaptive_over_naive_threshold_multiplier: str(ratio),
    adaptive_union_strictly_exceeds_naive_for_positive_B: numThresh > maxQueries,
    analytical_tail_abort_upper_2_pow_minus_3_f_sq: str(tail3f2),
    analytical_tail_abort_upper_2_pow_minus_f_minus_1: str(tailf1),
    per_draw_coupling_loss_upper: str(perDraw),
    per_draw_target_2_pow_minus_f: str(target),
    meets_per_draw_target: cmp(perDraw, target) <= 0n,
  }, "exact draw parameter ledger");
  if (!P.using_uncertified_K_override) {
    check(cmp(adaptiveUnion, tailf1) <= 0n && cmp(perDraw, target) <= 0n, "certified per-draw coupling loss <= 2^-f");
  }
}

function checkCdfBox(cdf, sigStr, tExpected, K) {
  const t = exactInt(cdf.threshold_t);
  check(t === BigInt(tExpected), "threshold t matches expected");
  const r = t >= 0n ? t : -t - 1n;
  const nonneg = t >= 0n;
  check(
    cdf.continuous_Gaussian_width === sigStr &&
    exactInt(cdf.radius_index) === r &&
    cdf.nonnegative_branch === nonneg &&
    Number.isSafeInteger(cdf.enclosure_bits) && cdf.enclosure_bits >= 4,
    "CDF box metadata"
  );
  const tail = cdf.underlying_tail_box;
  check(
    tail.continuous_Gaussian_width === sigStr &&
    exactInt(tail.integer_error_radius) === r &&
    tail.enclosure_bits === cdf.enclosure_bits,
    "underlying tail box metadata"
  );
  const tailLo = parse(tail.lower), tailHi = parse(tail.upper);
  check(cmp(tailLo, zero) >= 0n && cmp(tailLo, tailHi) <= 0n && cmp(tailHi, one) <= 0n, "valid tail probability box");
  const cdfLo = nonneg ? sub(one, div(tailHi, rat(2n))) : div(tailLo, rat(2n));
  const cdfHi = nonneg ? sub(one, div(tailLo, rat(2n))) : div(tailHi, rat(2n));
  const width = sub(cdfHi, cdfLo);
  const maxWidth = rat(2n, 2n ** BigInt(K));
  const ok = cmp(width, maxWidth) <= 0n;
  check(
    cdf.lower === str(cdfLo) &&
    cdf.upper === str(cdfHi) &&
    cdf.width === str(width) &&
    cdf.max_allowed_width === str(maxWidth) &&
    cdf.width_satisfies_bound === ok &&
    cdf.status === (ok ? "CERTIFIED_DIRECTED_CDF_BOX" : "NUMERICAL_PRECISION_CAP_ABORT") &&
    cdf.independent_transcendental_certificate_supplied === false,
    "directed CDF box derived from tail box"
  );
}

function replaySingleDraw(D) {
  checkDrawParameters(D.draw_parameters);
  const sigStr = D.draw_parameters.sigma;
  const B = exactInt(D.draw_parameters.truncation_bound_B);
  const K = D.draw_parameters.active_dyadic_bits_K;
  const allBits = D.dyadic_prefix_bits;
  check(Array.isArray(allBits) && allBits.length === D.bits_consumed && allBits.length <= K && allBits.every(b => b === 0 || b === 1), "valid lazy bit prefix");
  let fullPrefixInt = 0n;
  allBits.forEach(b => { fullPrefixInt = (fullPrefixInt << 1n) | BigInt(b); });
  check(exactInt(D.dyadic_prefix_integer) === fullPrefixInt, "dyadic prefix integer");

  const comps = D.threshold_comparisons;
  check(comps.length === D.thresholds_queried_count && comps.length >= 1, "nonempty threshold comparisons");

  let bitCursor = 0;
  let prefixInt = 0n;
  const seenBoxes = new Map();

  function replayStep(stepIdx, expectedT, expectedRole) {
    check(stepIdx < comps.length, "expected comparison step present");
    const step = comps[stepIdx];
    check(step.step_index === stepIdx && step.role === expectedRole && exactInt(step.threshold_t) === expectedT, "step index, role and threshold");
    checkCdfBox(step.cdf_box, sigStr, expectedT, K);
    seenBoxes.set(String(expectedT), step.cdf_box);
    if (step.cdf_box.status === "NUMERICAL_PRECISION_CAP_ABORT") {
      const denom = 2n ** BigInt(bitCursor);
      check(
        step.bits_read_after_step === bitCursor &&
        step.dyadic_interval_lower === str(rat(prefixInt, denom)) &&
        step.dyadic_interval_upper === str(rat(prefixInt + 1n, denom)) &&
        step.outcome === "NUMERICAL_PRECISION_CAP_ABORT",
        "numerical precision cap abort step"
      );
      return "NUMERICAL_PRECISION_CAP_ABORT";
    }
    const cdfLo = parse(step.cdf_box.lower), cdfHi = parse(step.cdf_box.upper);
    while (true) {
      const denom = 2n ** BigInt(bitCursor);
      const uLo = rat(prefixInt, denom), uHi = rat(prefixInt + 1n, denom);
      if (cmp(uHi, cdfLo) <= 0n) {
        check(
          step.bits_read_after_step === bitCursor &&
          JSON.stringify(step.dyadic_prefix_bits) === JSON.stringify(allBits.slice(0, bitCursor)) &&
          step.dyadic_interval_lower === str(uLo) &&
          step.dyadic_interval_upper === str(uHi) &&
          step.outcome === "U_LT_F",
          "lazy U_LT_F decision at minimal prefix"
        );
        return "U_LT_F";
      }
      if (cmp(uLo, cdfHi) >= 0n) {
        check(
          step.bits_read_after_step === bitCursor &&
          JSON.stringify(step.dyadic_prefix_bits) === JSON.stringify(allBits.slice(0, bitCursor)) &&
          step.dyadic_interval_lower === str(uLo) &&
          step.dyadic_interval_upper === str(uHi) &&
          step.outcome === "U_GE_F",
          "lazy U_GE_F decision at minimal prefix"
        );
        return "U_GE_F";
      }
      if (bitCursor >= K) {
        check(
          step.bits_read_after_step === K &&
          JSON.stringify(step.dyadic_prefix_bits) === JSON.stringify(allBits) &&
          step.dyadic_interval_lower === str(uLo) &&
          step.dyadic_interval_upper === str(uHi) &&
          step.outcome === "UNIFORM_PREFIX_PRECISION_ABORT",
          "K-bit precision abort step"
        );
        return "UNIFORM_PREFIX_PRECISION_ABORT";
      }
      check(bitCursor < allBits.length, "bit stream has next lazy bit");
      prefixInt = (prefixInt << 1n) | BigInt(allBits[bitCursor]);
      bitCursor++;
    }
  }

  let stepIdx = 0;
  const leftOut = replayStep(stepIdx++, -B - 1n, "LEFT_TAIL_CHECK");
  if (leftOut === "UNIFORM_PREFIX_PRECISION_ABORT" || leftOut === "NUMERICAL_PRECISION_CAP_ABORT") {
    check(D.status === leftOut && D.sampled_integer === null && D.abort_reason === leftOut && stepIdx === comps.length, "abort at left tail");
  } else if (leftOut === "U_LT_F") {
    check(D.status === "TAIL_TRUNCATION_ABORT" && D.tail_side === "LEFT_TAIL" && D.sampled_integer === null && stepIdx === comps.length, "left tail truncation abort");
  } else {
    const rightOut = replayStep(stepIdx++, B, "RIGHT_TAIL_CHECK");
    if (rightOut === "UNIFORM_PREFIX_PRECISION_ABORT" || rightOut === "NUMERICAL_PRECISION_CAP_ABORT") {
      check(D.status === rightOut && D.sampled_integer === null && D.abort_reason === rightOut && stepIdx === comps.length, "abort at right tail");
    } else if (rightOut === "U_GE_F") {
      check(D.status === "TAIL_TRUNCATION_ABORT" && D.tail_side === "RIGHT_TAIL" && D.sampled_integer === null && stepIdx === comps.length, "right tail truncation abort");
    } else {
      let low = -B, high = B, aborted = null;
      while (low < high) {
        const mid = floorDiv2(low + high);
        const out = replayStep(stepIdx++, mid, "BINARY_SEARCH_STEP");
        if (out === "UNIFORM_PREFIX_PRECISION_ABORT" || out === "NUMERICAL_PRECISION_CAP_ABORT") {
          aborted = out;
          break;
        }
        if (out === "U_LT_F") high = mid;
        else low = mid + 1n;
      }
      check(stepIdx === comps.length, "all threshold comparisons replayed");
      if (aborted !== null) {
        check(D.status === aborted && D.sampled_integer === null && D.abort_reason === aborted, "binary search abort");
      } else {
        check(
          D.status === "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE" &&
          exactInt(D.sampled_integer) === low &&
          D.abort_reason === null &&
          D.tail_side === null,
          "certified integer sample matches binary search convergence"
        );
        const denom = 2n ** BigInt(bitCursor);
        const uLo = rat(prefixInt, denom), uHi = rat(prefixInt + 1n, denom);
        const loBox = seenBoxes.get(String(low - 1n)), hiBox = seenBoxes.get(String(low));
        check(loBox !== undefined && hiBox !== undefined, "both bracketing thresholds queried");
        check(
          cmp(uLo, parse(loBox.upper)) >= 0n && cmp(uHi, parse(hiBox.lower)) <= 0n,
          "certified quantile bracket F_hi(t*-1) <= u_lo < u_hi <= F_lo(t*)"
        );
      }
    }
  }
  const finalDenom = 2n ** BigInt(bitCursor);
  check(
    bitCursor === D.bits_consumed &&
    D.final_dyadic_lower === str(rat(prefixInt, finalDenom)) &&
    D.final_dyadic_upper === str(rat(prefixInt + 1n, finalDenom)) &&
    D.midpoint_or_floating_fallback_used === false &&
    D.silent_resampling_used === false &&
    D.independent_transcendental_certificate_supplied === false,
    "final dyadic state and honesty flags"
  );
}

function checkCensus(C) {
  const sigStr = C.sigma, f = C.failure_bits_target, K = C.census_dyadic_bits;
  checkDrawParameters(C.draw_parameters, K);
  const B = Number(exactInt(C.truncation_bound_B));
  const totalCells = 2 ** K;
  check(C.total_dyadic_cells_censused === totalCells, "total dyadic cells");
  const boxes = C.threshold_cdf_boxes;
  check(Object.keys(boxes).length === 2 * B + 2, "complete 2B+2 threshold boxes");
  for (let t = -B - 1; t <= B; t++) {
    checkCdfBox(boxes[String(t)], sigStr, t, K);
  }

  const statusCounts = {}, intHist = {}, tailSides = {};
  let totalBits = 0;

  for (let cell = 0; cell < totalCells; cell++) {
    const bits = Array.from({length: K}, (_, j) => (cell >> (K - 1 - j)) & 1);
    let bitCursor = 0, prefixInt = 0n;
    function stepCompare(t) {
      const box = boxes[String(t)];
      const cdfLo = parse(box.lower), cdfHi = parse(box.upper);
      while (true) {
        const denom = 2n ** BigInt(bitCursor);
        const uLo = rat(prefixInt, denom), uHi = rat(prefixInt + 1n, denom);
        if (cmp(uHi, cdfLo) <= 0n) return "U_LT_F";
        if (cmp(uLo, cdfHi) >= 0n) return "U_GE_F";
        if (bitCursor >= K) return "UNIFORM_PREFIX_PRECISION_ABORT";
        prefixInt = (prefixInt << 1n) | BigInt(bits[bitCursor]);
        bitCursor++;
      }
    }
    let st = null, val = null, side = null;
    const lOut = stepCompare(-B - 1);
    if (lOut === "UNIFORM_PREFIX_PRECISION_ABORT") st = lOut;
    else if (lOut === "U_LT_F") { st = "TAIL_TRUNCATION_ABORT"; side = "LEFT_TAIL"; }
    else {
      const rOut = stepCompare(B);
      if (rOut === "UNIFORM_PREFIX_PRECISION_ABORT") st = rOut;
      else if (rOut === "U_GE_F") { st = "TAIL_TRUNCATION_ABORT"; side = "RIGHT_TAIL"; }
      else {
        let low = -B, high = B;
        while (low < high) {
          const mid = Math.floor((low + high) / 2);
          const out = stepCompare(mid);
          if (out === "UNIFORM_PREFIX_PRECISION_ABORT") { st = out; break; }
          if (out === "U_LT_F") high = mid;
          else low = mid + 1;
        }
        if (st === null) { st = "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE"; val = low; }
      }
    }
    totalBits += bitCursor;
    statusCounts[st] = (statusCounts[st] || 0) + 1;
    if (val !== null) intHist[String(val)] = (intHist[String(val)] || 0) + 1;
    if (side !== null) tailSides[side] = (tailSides[side] || 0) + 1;
  }

  same(C.status_counts, statusCounts, "census status counts");
  same(C.sampled_integer_histogram, intHist, "census sampled integer histogram");
  same(C.tail_abort_side_counts, tailSides, "census tail abort side counts");
  check(C.total_lazy_bits_consumed === totalBits, "census total lazy bits consumed");

  const accMass = rat(BigInt(statusCounts.CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE || 0), BigInt(totalCells));
  const precMass = rat(BigInt(statusCounts.UNIFORM_PREFIX_PRECISION_ABORT || 0), BigInt(totalCells));
  const tailMass = rat(BigInt(statusCounts.TAIL_TRUNCATION_ABORT || 0), BigInt(totalCells));
  check(
    C.exact_accepted_mass === str(accMass) &&
    C.exact_precision_abort_mass === str(precMass) &&
    C.exact_tail_abort_mass === str(tailMass) &&
    cmp(precMass, parse(C.draw_parameters.adaptive_all_threshold_precision_abort_upper)) <= 0n &&
    C.precision_abort_within_adaptive_union_bound === true &&
    C.every_accepted_cell_verified_against_directed_cdf_brackets === true &&
    C.finite_census_is_an_oracle_or_speedup_candidate === false,
    "census probability masses and adaptive union bound"
  );
}

function checkSignsAndMask(SM) {
  const n = SM.dimension, m = SM.parent_rows, k = SM.output_rows, g = exactInt(SM.modulus), fMask = SM.mask_failure_bits_target;
  check(SM.sign_rows.length === k && SM.sign_bits_consumed === k * m, "sign rows and bits");
  SM.sign_rows.forEach(row => check(row.length === m && row.every(t => t === -1 || t === 1), "valid sign row"));
  const bitsPerTrial = ceilLog2(g);
  const maxTrials = fMask + ceilLog2(Math.max(2, n));
  const singleRej = rat(2n ** BigInt(bitsPerTrial) - g, 2n ** BigInt(bitsPerTrial));
  let coordAbort = one;
  for (let i = 0; i < maxTrials; i++) coordAbort = mul(coordAbort, singleRej);
  const maskAbort = min(one, mul(rat(BigInt(n)), coordAbort));
  check(
    SM.bits_per_mask_trial === bitsPerTrial &&
    SM.max_trials_per_coordinate === maxTrials &&
    SM.single_trial_rejection_probability === str(singleRej) &&
    SM.mask_rejection_abort_probability_upper === str(maskAbort) &&
    cmp(maskAbort, rat(1n, 2n ** BigInt(fMask))) <= 0n,
    "mask rejection parameters and bound"
  );
  let maskBits = 0;
  const coords = [];
  let aborted = false;
  SM.mask_coordinate_receipts.forEach((cr, idx) => {
    check(cr.coordinate_index === idx && cr.trials_attempted === cr.trial_receipts.length && cr.trials_attempted <= maxTrials, "mask coordinate trials");
    let acceptedVal = null;
    cr.trial_receipts.forEach((tr, tIdx) => {
      check(tr.trial_index === tIdx && tr.bits.length === bitsPerTrial && tr.bits.every(b => b === 0 || b === 1), "mask trial bits");
      maskBits += bitsPerTrial;
      let val = 0n;
      tr.bits.forEach(b => { val = (val << 1n) | BigInt(b); });
      const acc = val < g;
      check(exactInt(tr.candidate_integer) === val && tr.accepted === acc, "mask trial candidate integer and acceptance");
      if (acc) acceptedVal = enc(val);
    });
    same(cr.accepted_value, acceptedVal, "coordinate accepted value");
    if (acceptedVal === null) aborted = true;
    else coords.push(acceptedVal);
  });
  check(
    SM.mask_bits_consumed === maskBits &&
    SM.total_sign_and_mask_bits_consumed === k * m + maskBits &&
    SM.status === (aborted ? "MASK_REJECTION_SAMPLING_ABORT" : "CERTIFIED_UNIFORM_SIGNS_AND_MASK") &&
    SM.signs_and_mask_from_paid_ideal_bits === true,
    "signs and mask totals"
  );
  if (aborted) check(SM.secret_mask === null, "aborted mask is null");
  else same(SM.secret_mask, coords, "accepted secret mask");
}

function checkBatchBudget(B) {
  const n = B.dimension, m = B.parent_rows, k = B.output_rows, g = exactInt(B.modulus);
  const fBatch = B.batch_dither_failure_bits_target, fMask = B.mask_failure_bits_target;
  const perDrawF = fBatch + ceilLog2(Math.max(2, k));
  check(B.per_draw_failure_bits_f === perDrawF, "per-draw failure bits f");
  checkDrawParameters(B.single_dither_draw_parameters);
  const perDrawLoss = parse(B.single_dither_draw_parameters.per_draw_coupling_loss_upper);
  const kLoss = min(one, mul(rat(BigInt(k)), perDrawLoss));
  const bitsPerTrial = ceilLog2(g);
  const maxTrials = fMask + ceilLog2(Math.max(2, n));
  const singleRej = rat(2n ** BigInt(bitsPerTrial) - g, 2n ** BigInt(bitsPerTrial));
  let coordAbort = one;
  for (let i = 0; i < maxTrials; i++) coordAbort = mul(coordAbort, singleRej);
  const maskLoss = min(one, mul(rat(BigInt(n)), coordAbort));
  const totalLoss = min(one, add(kLoss, maskLoss));
  const maxBits = k * m + n * maxTrials * bitsPerTrial + k * B.single_dither_draw_parameters.active_dyadic_bits_K;
  check(
    B.k_dither_draws_abort_union_upper === str(kLoss) &&
    B.mask_rejection_abort_union_upper === str(maskLoss) &&
    B.certified_complete_dither_sampler_TV_loss === str(totalLoss) &&
    B.worst_case_batch_random_bits_upper === maxBits &&
    B.shortened_partial_batch_allowed === false &&
    B.fresh_randomness_counts_as_new_original_samples === false,
    "complete batch sampler budget"
  );
}

function checkBatchResult(raw, BR) {
  checkBatchBudget(BR.batch_sampler_budget);
  checkSignsAndMask(BR.signs_and_mask_sampling);
  let ditherBits = 0;
  BR.dither_draw_receipts.forEach((d, idx) => {
    check(d.draw_index === idx, "dither draw index");
    replaySingleDraw(d);
    ditherBits += d.bits_consumed;
  });
  check(
    BR.total_random_bits_consumed === BR.signs_and_mask_sampling.total_sign_and_mask_bits_consumed + ditherBits &&
    BR.shortened_batch_emitted_as_valid_source === false &&
    BR.fresh_public_randomness_is_a_fresh_original_sample === false &&
    BR.actual_quantum_decision_or_multiple_producer_supplied === false,
    "batch bit consumption and honesty flags"
  );
  const allDithersOk =
    BR.signs_and_mask_sampling.status === "CERTIFIED_UNIFORM_SIGNS_AND_MASK" &&
    BR.dither_draw_receipts.length === BR.batch_sampler_budget.output_rows &&
    BR.dither_draw_receipts.every(d => d.status === "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE");
  if (!allDithersOk) {
    check(
      BR.status === "ABORTED_COMPLETE_REFRESH_BATCH_DIAGNOSTIC_ONLY" &&
      BR.refresh_transform === null &&
      BR.producer_input === null &&
      BR.completed_dither_draws < BR.batch_sampler_budget.output_rows,
      "complete batch abort suppresses producer_input and transform"
    );
  } else {
    check(
      BR.status === "CERTIFIED_COMPLETE_REFRESH_BATCH_READY_FOR_EXTERNAL_PRODUCER" &&
      BR.abort_reason === null &&
      BR.completed_dither_draws === BR.batch_sampler_budget.output_rows,
      "complete batch success status"
    );
    S.transform(raw, BR.refresh_transform);
    same(BR.refresh_transform.supplied_sign_rows, BR.signs_and_mask_sampling.sign_rows, "transform uses sampled signs");
    same(BR.refresh_transform.supplied_secret_mask, BR.signs_and_mask_sampling.secret_mask, "transform uses sampled mask");
    same(BR.refresh_transform.supplied_integer_dithers, BR.dither_draw_receipts.map(d => d.sampled_integer), "transform uses sampled dithers");
    same(BR.producer_input, BR.refresh_transform.producer_input, "producer input matches transform");
  }
}

function verify(R) {
  check(
    R.status === "CERTIFIED_ROUNDED_GAUSSIAN_DITHER_SAMPLER_AND_BATCH_COUPLING_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/native_gaussian_dither_sampler.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_GAUSSIAN_DITHER_SAMPLER.md")) &&
    R.contract_sha256 === hash(path.join(ROOT, "research/hypotheses/native_gaussian_dither_sampler_contract.json")),
    "current dither sampler producer, derivation, and contract hashes"
  );
  const deps = [
    "native_basis_lottery.py",
    "native_classical_modulus_descent.py",
    "native_gaussian_quotient_completion.py",
    "native_small_multiple_completion.py",
    "native_source_refresh.py",
    "ternary_covariant_noise.py",
    "ternary_measured_lattice_decoder.py",
    "ternary_noise_degradation.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  check(R.single_draw_controls.length === 4, "4 single-draw controls");
  R.single_draw_controls.forEach(c => replaySingleDraw(c.draw));
  check(
    exactInt(R.single_draw_controls[0].draw.sampled_integer) < 0n &&
    exactInt(R.single_draw_controls[1].draw.sampled_integer) === 0n &&
    exactInt(R.single_draw_controls[2].draw.sampled_integer) > 0n &&
    exactInt(R.single_draw_controls[3].draw.draw_parameters.truncation_bound_B) > 2n ** 53n,
    "negative, zero, positive, and giant-width (>2^53) controls"
  );

  check(R.bounded_dyadic_prefix_censuses.length === 2, "2 bounded dyadic prefix censuses");
  R.bounded_dyadic_prefix_censuses.forEach(checkCensus);

  const F = R.abort_and_trap_falsifiers;
  replaySingleDraw(F.forced_left_tail_abort);
  check(F.forced_left_tail_abort.status === "TAIL_TRUNCATION_ABORT" && F.forced_left_tail_abort.tail_side === "LEFT_TAIL", "forced left tail abort");
  replaySingleDraw(F.forced_right_tail_abort);
  check(F.forced_right_tail_abort.status === "TAIL_TRUNCATION_ABORT" && F.forced_right_tail_abort.tail_side === "RIGHT_TAIL", "forced right tail abort");
  replaySingleDraw(F.forced_uniform_prefix_precision_abort);
  check(F.forced_uniform_prefix_precision_abort.status === "UNIFORM_PREFIX_PRECISION_ABORT", "forced uniform prefix precision abort");
  replaySingleDraw(F.forced_numerical_precision_cap_abort);
  check(F.forced_numerical_precision_cap_abort.status === "NUMERICAL_PRECISION_CAP_ABORT", "forced numerical precision cap abort");

  check(F.adaptive_threshold_trap_regression.length === 4, "4 trap regression profiles");
  F.adaptive_threshold_trap_regression.forEach(tp => {
    const p = parse(tp.adaptive_all_threshold_union_upper), q = parse(tp.naive_query_count_bound_DO_NOT_USE);
    const mult = parse(tp.adaptive_over_naive_multiplier);
    check(cmp(p, q) > 0n && cmp(mult, one) > 0n, "adaptive threshold union strictly exceeds naive query-count bound");
  });

  const rawCtrl = R.integrated_source_refresh.complete_batch_control.original_records;
  checkBatchResult(rawCtrl, F.forced_complete_batch_abort_diagnostic);
  check(F.forced_complete_batch_abort_diagnostic.status === "ABORTED_COMPLETE_REFRESH_BATCH_DIAGNOSTIC_ONLY", "forced complete batch abort");

  const I = R.integrated_source_refresh;
  checkBatchResult(rawCtrl, I.complete_batch_control.batch_result);
  check(I.complete_batch_control.batch_result.status === "CERTIFIED_COMPLETE_REFRESH_BATCH_READY_FOR_EXTERNAL_PRODUCER", "complete batch control succeeded");

  check(I.coupled_source_refresh_profiles.length === 3, "3 coupled source-refresh profiles");
  I.coupled_source_refresh_profiles.forEach(cp => {
    checkBatchBudget(cp.batch_sampler_budget);
    S.source(cp.coupled_source_refresh_ledger);
    check(
      cp.coupled_source_refresh_ledger.certified_complete_dither_sampler_TV_loss_EXTERNAL === cp.batch_sampler_budget.certified_complete_dither_sampler_TV_loss &&
      cp.coupled_source_refresh_ledger.one_refresh_coverage_lower_IF_quality_and_external_contracts_hold !== null,
      "sampler TV loss wired into native_source_refresh.source_ledger"
    );
  });

  check(
    R.source_refresh_dither_sampler_implemented === true &&
    R.source_conditioned_producer_amplification_established === false &&
    R.actual_quantum_decision_or_multiple_producer_supplied === false &&
    R.independent_transcendental_certificate_supplied === false &&
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.novelty_claim === false,
    "honesty guardrails"
  );

  return {
    verified: true,
    single_draw_controls: R.single_draw_controls.length,
    censused_dyadic_cells: R.bounded_dyadic_prefix_censuses.reduce((s, c) => s + c.total_dyadic_cells_censused, 0),
    coupled_refresh_profiles: I.coupled_source_refresh_profiles.length,
    actual_quantum_producer_supplied: false,
  };
}

module.exports = {
  verify,
  checkDrawParameters,
  checkCdfBox,
  replaySingleDraw,
  checkCensus,
  checkSignsAndMask,
  checkBatchBudget,
  checkBatchResult,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}

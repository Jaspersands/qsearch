"use strict";
// Independent exact replay for refresh-to-clean-basis crossover and composed canonical DAG pipeline.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const M = require("./native_small_multiple_completion_crosscheck.js");
const B = require("./native_basis_lottery_crosscheck.js");
const P = require("./native_prefix_ambiguity_pruning_crosscheck.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_refresh_lottery_crossover.json");
const mod = (x, q) => (x % q + q) % q;
const enc = x => x <= 9007199254740991n && x >= -9007199254740991n ? Number(x) : String(x);
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const digest = x => crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a, b) => cmp(a, b) <= 0n ? a : b;
const max = (a, b) => cmp(a, b) >= 0n ? a : b;

function root(q) {
  check(q >= 3n, "positive ternary root");
  let d = 0;
  while (q % 3n === 0n) {
    q /= 3n;
    d++;
  }
  check(q === 1n, "actual ternary prime power");
  return d;
}

function canonicalNode(raw, scale0, prefix0) {
  const q0 = BigInt(raw[0].modulus), n = raw[0].label.length, scale = BigInt(scale0);
  check(scale >= 1n && q0 % scale === 0n, "scale divides original modulus");
  if (scale > 1n) root(scale);
  const g = q0 / scale;
  root(g);
  const prefix = prefix0.map(BigInt);
  if (scale === 1n) {
    check(prefix.length === n && prefix.every(x => x === 0n), "scale-1 zero prefix");
  } else {
    check(prefix.length === n && prefix.every(x => x >= 0n && x < scale), "canonical scale prefix");
  }
  const children = [], receipts = [];
  raw.forEach(origin => {
    const residual = mod(BigInt(origin.value) - origin.label.reduce((v, a, i) => v + BigInt(a) * prefix[i], 0n), q0);
    const val = mod((residual + scale / 2n) / scale, g);
    const child = {
      label: origin.label.map(a => enc(mod(BigInt(a), g))),
      value: enc(val),
      modulus: enc(g),
      source_id: origin.source_id,
    };
    children.push(child);
    receipts.push({
      source_id: origin.source_id,
      original_record_sha256: digest(origin),
      corrected_original_response: enc(residual),
      direct_original_derived_response: enc(val),
    });
  });
  const node = {
    original_records_sha256: digest(raw),
    original_modulus: enc(q0),
    modulus: enc(g),
    original_scale: enc(scale),
    known_original_lower_prefix_IF_path_true: prefix.map(enc),
  };
  return {
    status: "CANONICAL_ORIGINAL_QUOTIENT_NODE_FOR_REFRESH",
    canonical_node: node,
    canonical_node_sha256: digest(node),
    derived_records: children,
    record_receipts: receipts,
    original_records_paid_once: raw.length,
    canonical_rounding_evaluations: raw.length,
    canonical_node_from_originals_not_flooded_children: true,
    true_prefix_or_Gaussian_law_certified: false,
  };
}

function refreshBatch(raw, scale0, prefix0, signMatrix, secretMask, dithers) {
  const nodeReport = canonicalNode(raw, scale0, prefix0);
  const g = BigInt(nodeReport.canonical_node.modulus);
  const derived = nodeReport.derived_records;
  const m = derived.length, n = derived[0].label.length, k = signMatrix.length;
  check(k > 0 && dithers.length === k && secretMask.length === n, "valid refresh batch dimensions");
  const mask = secretMask.map(x => mod(BigInt(x), g));
  const nodeHash = nodeReport.canonical_node_sha256;
  const refreshed = [], receipts = [];
  for (let rIdx = 0; rIdx < k; rIdx++) {
    const tRow = signMatrix[rIdx], dither = BigInt(dithers[rIdx]);
    check(tRow.length === m && tRow.every(t => t === -1 || t === 1), "valid sign row");
    const label = Array.from({length: n}, (_, j) =>
      mod(derived.reduce((acc, row, i) => acc + BigInt(tRow[i]) * BigInt(row.label[j]), 0n), g)
    );
    const signedY = mod(derived.reduce((acc, row, i) => acc + BigInt(tRow[i]) * BigInt(row.value), 0n), g);
    const maskShift = mod(label.reduce((acc, a, j) => acc + a * mask[j], 0n), g);
    const value = mod(signedY + dither - maskShift, g);
    const rec = {
      label: label.map(enc),
      value: enc(value),
      modulus: enc(g),
      source_id: `refresh:${nodeHash.slice(0, 12)}:${rIdx}`,
    };
    refreshed.push(rec);
    receipts.push({
      row_index: rIdx,
      sign_row: tRow,
      dither: enc(dither),
      signed_canonical_response_mod_g: enc(signedY),
      mask_shift_mod_g: enc(maskShift),
      refreshed_record: rec,
    });
  }
  return {
    status: "CONDITIONAL_SIGN_MIX_MASKED_REFRESH_BATCH",
    canonical_node_report: nodeReport,
    refreshed_rows: k,
    parent_rows: m,
    dimension: n,
    modulus: enc(g),
    reduction_side_secret_mask: mask.map(enc),
    public_producer_input_records: refreshed,
    refresh_row_receipts: receipts,
    sign_sum_label_operations: k * m * n,
    sign_sum_response_operations: k * m,
    mask_shift_operations: k * n,
    sign_matrix_or_secret_mask_disclosed_to_producer: false,
    refreshed_records_are_independent_original_samples: false,
    already_flooded_children_rerandomized: false,
    dither_gaussian_law_or_parent_entropy_certified_by_algebra: false,
  };
}

function unmaskMultiple(coeff0, maskedMultiple, secretMask, g0) {
  const g = BigInt(g0), c = BigInt(coeff0);
  root(g);
  check(mod(c, g) !== 0n, "nonzero modulo-g coefficient");
  const mask = secretMask.map(x => mod(BigInt(x), g));
  const wMasked = maskedMultiple.map(x => mod(BigInt(x), g));
  const unmasked = wMasked.map((w, i) => enc(mod(w + c * mask[i], g)));
  return {
    modulus: enc(g),
    signed_coefficient: enc(c),
    masked_multiple: wMasked.map(enc),
    unmasked_multiple: unmasked,
    unmasking_multiply_add_operations: mask.length,
    coefficient_dependent_unmasking_is_free: false,
  };
}

function pruneNode(raw, scale0, prefix0, candidates, R0, requireNonWrapping = true) {
  const q0 = BigInt(raw[0].modulus), n = raw[0].label.length, L = BigInt(scale0), R = BigInt(R0);
  check(R >= 0n && 4n * R < q0 && candidates.length > 0, "valid node pruning inputs");
  const parentNode = canonicalNode(raw, L, prefix0), g = BigInt(parentNode.canonical_node.modulus);
  const evals = [], surviving = new Map(), terminals = [];
  let checksCount = 0;
  candidates.forEach(([c0, mult0], idx) => {
    const c = BigInt(c0), mult = mult0.map(x => enc(mod(BigInt(x), g)));
    const model = M.quotient(g, c, mult), entry = {candidate_index: idx, coefficient: c0, multiple: mult};
    if (model === null) {
      evals.push({...entry, status: "REJECTED_INCOMPATIBLE_RING_IMAGE"});
      return;
    }
    const x = model.known_quotient_IF_multiple_is_true.map(BigInt), Q = BigInt(model.remaining_modulus), gChild = BigInt(model.nonunit_factor);
    const nextP = parentNode.canonical_node.known_original_lower_prefix_IF_path_true.map((p, i) => enc(BigInt(p) + L * x[i]));
    const nextL = L * Q;
    Object.assign(entry, {quotient_model: model, candidate_next_scale: enc(nextL), candidate_next_prefix: nextP});
    if (gChild === 1n) {
      const F = B.complete(raw, 1n, nextP, R).unit_fit;
      checksCount += raw.length;
      if (F.fits_public_radius) {
        if (!terminals.some(t => JSON.stringify(t) === JSON.stringify(nextP))) terminals.push(nextP);
        evals.push({...entry, status: "SURVIVING_TERMINAL_ORIGINAL_FIT", original_fit: F});
      } else {
        evals.push({...entry, status: "PRUNED_BY_FULL_ORIGINAL_RADIUS", original_fit: F});
      }
      return;
    }
    const pfit = P.moduloScaleFit(raw, nextL, nextP, R);
    checksCount += raw.length;
    entry.modulo_scale_fit = pfit;
    if (requireNonWrapping && !pfit.non_wrapping_unique_decoding_regime_4R_lt_L) {
      evals.push({...entry, status: "UNPRUNED_WRAPPING_SCALE_4R_GE_L"});
      return;
    }
    if (!pfit.fits_modulo_scale_radius) {
      evals.push({...entry, status: "PRUNED_BY_MODULO_SCALE_ORIGINAL_RESIDUAL"});
      return;
    }
    const child = canonicalNode(raw, nextL, nextP), h = child.canonical_node_sha256, merged = surviving.has(h);
    if (!merged) surviving.set(h, child);
    evals.push({
      ...entry,
      status: merged ? "MERGED_INTO_EXISTING_CANONICAL_NODE" : "SURVIVING_NEW_CANONICAL_NODE",
      canonical_node_sha256: h,
    });
  });
  return {
    parent_canonical_node: parentNode.canonical_node,
    parent_canonical_node_sha256: parentNode.canonical_node_sha256,
    candidates_evaluated: candidates.length,
    original_modulo_distance_evaluations: checksCount,
    candidate_evaluations: evals,
    surviving_canonical_child_nodes: Array.from(surviving.values()),
    surviving_canonical_child_count: surviving.size,
    surviving_terminal_secrets: terminals,
    require_non_wrapping_4R_lt_L: requireNonWrapping,
    false_branch_null_assumption_used: false,
    multiple_producer_supplied: false,
  };
}

function checkRefreshLedger(R) {
  const n = R.dimension, r = R.original_root_digits, m = R.parent_rows, k = R.refreshed_rows;
  const aOrig = parse(R.alpha_original), aTarg = parse(R.alpha_target);
  const L = R.label_entropy_ledger, Eled = R.common_energy_ledger, D = R.dither_precision_ledger, A = R.conditional_amplification_and_branching_ledger;
  const etaL = parse(L.eta_label), etaN = parse(Eled.eta_noise);
  let labelSum = zero;
  L.per_root_budgets.forEach(b => {
    const g = 3n ** BigInt(b.root_digits);
    const expChi = rat(g ** BigInt(n) - 1n, 2n ** BigInt(m));
    const fail = min(one, div(mul(rat(BigInt(k * k)), expChi), mul(rat(4n), mul(etaL, etaL))));
    check(BigInt(b.modulus) === g && b.expected_chi2 === str(expChi) && b.markov_label_failure_upper === str(fail), "per-root label budget");
    labelSum = add(labelSum, fail);
  });
  const labelUnion = min(one, labelSum);
  check(L.all_reachable_roots_label_failure_union_upper === str(labelUnion), "label failure union");

  const dMin = Eled.minimum_reachable_root_digits, gMin = 3n ** BigInt(dMin);
  const reqE = div(mul(mul(etaN, etaN), mul(aTarg, aTarg)), rat(4n * BigInt(k)));
  const floor = rat(BigInt(m), 2n * gMin * gMin);
  const H = div(sub(reqE, floor), rat(2n));
  const expX2 = div(mul(rat(BigInt(m)), mul(aOrig, aOrig)), rat(6n));
  const eFail = cmp(H, zero) <= 0n ? one : min(one, div(expX2, H));
  check(
    BigInt(Eled.minimum_reachable_modulus) === gMin &&
    Eled.required_normalized_quotient_energy_upper === str(reqE) &&
    Eled.worst_case_rounding_floor_m_over_2_g_min_squared === str(floor) &&
    Eled.common_original_energy_threshold_H === str(H) &&
    Eled.expected_original_sum_X_squared_upper === str(expX2) &&
    Eled.common_energy_failure_upper === str(eFail) &&
    Eled.bound_is_nonvacuous === (cmp(H, zero) > 0n && cmp(eFail, one) < 0n && cmp(aTarg, one) < 0n),
    "common energy ledger"
  );

  const parentBad = min(one, add(labelUnion, eFail));
  check(R.good_parent_failure_union_upper === str(parentBad), "good parent failure union");
  const ditherAbort = parse(D.dither_abort_union_upper);
  const etaTotal = add(add(etaL, etaN), ditherAbort);
  check(R.per_call_total_TV_and_abort_loss === str(etaTotal), "per-call TV and abort loss");
  if (A !== null) {
    const pProd = parse(A.assumed_external_producer_average_success_at_alpha_target);
    const pEff = max(zero, sub(pProd, etaTotal));
    const Rcalls = A.refresh_calls_per_level, depth = A.recursion_depth;
    let miss = one;
    for (let i = 0; i < Rcalls; i++) miss = mul(miss, sub(one, pEff));
    const allMiss = min(one, mul(rat(BigInt(depth)), miss));
    const uncond = min(one, add(parentBad, allMiss));
    check(
      A.per_call_refresh_TV_and_abort_loss === str(etaTotal) &&
      A.conditional_single_call_success_lower_on_good_parent === str(pEff) &&
      A.conditional_per_level_miss_upper_on_good_parent === str(miss) &&
      A.conditional_all_levels_miss_union_upper_on_good_parent === str(allMiss) &&
      A.unconditional_good_parent_and_coverage_failure_upper_IF_producer_exists === str(uncond),
      "conditional amplification ledger"
    );
  }
}

function checkCrossover(C) {
  const m = BigInt(C.parent_rows), k = BigInt(C.refreshed_rows);
  const aOrig = parse(C.alpha_original), aTarg = parse(C.alpha_target), etaN = parse(C.eta_noise);
  const dMin = C.min_refresh_root_digits, dTerm = C.terminal_root_digits;
  check(dTerm >= 1 && dMin > dTerm, "valid crossover root digits");
  const gMin = 3n ** BigInt(dMin), gTerm = 3n ** BigInt(dTerm);
  const reqE = div(mul(mul(etaN, etaN), mul(aTarg, aTarg)), rat(4n * k));
  const floorMin = rat(m, 2n * gMin * gMin), floorTerm = rat(m, 2n * gTerm * gTerm);
  const Hmin = div(sub(reqE, floorMin), rat(2n)), Hterm = div(sub(reqE, floorTerm), rat(2n));
  check(cmp(Hmin, zero) > 0n, "positive H_min");
  const deltaRaw = div(mul(rat(m), mul(aOrig, aOrig)), mul(rat(6n), Hmin));
  const betaTerm = mul(aOrig, rat(gTerm)), betaSq = mul(betaTerm, betaTerm);
  const rhs = mul(mul(rat(6n), deltaRaw), mul(Hmin, rat(gTerm * gTerm, m)));
  const threeHalves = mul(rat(3n, 2n), deltaRaw), threeDelta = mul(rat(3n), deltaRaw);
  const nonpos = cmp(Hterm, zero) <= 0n;
  check(
    BigInt(C.min_refresh_modulus) === gMin &&
    BigInt(C.terminal_modulus) === gTerm &&
    C.H_at_min_refresh_root === str(Hmin) &&
    C.H_at_terminal_root === str(Hterm) &&
    C.unclamped_markov_delta_energy_at_g_min === str(deltaRaw) &&
    C.terminal_unflooded_derived_Gaussian_width_beta === str(betaTerm) &&
    C.terminal_beta_squared === str(betaSq) &&
    C.exact_identity_6_delta_H_min_g_term_sq_over_m === str(rhs) &&
    C.three_halves_delta_energy_upper === str(threeHalves) &&
    C.three_delta_energy_upper === str(threeDelta) &&
    C.terminal_H_is_nonpositive === nonpos &&
    C.parameter_cancellation_verified === true,
    "crossover width bound"
  );
  if (nonpos) {
    check(
      cmp(betaSq, threeHalves) < 0n &&
      C.beta_squared_strictly_below_three_halves_delta_when_H_nonpositive === true,
      "strict (3/2)*delta crossover inequality"
    );
  }
}

function checkProfile(prof) {
  checkRefreshLedger(prof.high_root_refresh_ledger);
  P.checkProfile(prof.modulo_scale_dag_pruning_ledger);
  checkCrossover(prof.refresh_to_lottery_crossover);
  B.probability(prof.terminal_clean_basis_lottery_ledger);

  const dagFail = parse(prof.modulo_scale_dag_pruning_ledger.total_local_pruning_and_radius_failure_upper);
  const refFail = parse(prof.high_root_refresh_ledger.good_parent_failure_union_upper);
  const lotFail = parse(prof.terminal_clean_basis_lottery_ledger.all_trials_fail_probability_upper);
  const localUnion = min(one, add(add(dagFail, refFail), lotFail));
  const ampMiss = parse(prof.high_root_refresh_ledger.conditional_amplification_and_branching_ledger.conditional_all_levels_miss_union_upper_on_good_parent);
  const compUnion = min(one, add(localUnion, ampMiss));
  const elim =
    prof.refresh_to_lottery_crossover.terminal_H_is_nonpositive === true &&
    prof.high_root_refresh_ledger.common_energy_ledger.bound_is_nonvacuous === true &&
    cmp(lotFail, rat(1n, 10n ** 15n)) < 0n;
  check(
    prof.unconditioned_local_source_failure_union_upper === str(localUnion) &&
    prof.composed_failure_upper_IF_external_producer_meets_average_contract === str(compUnion) &&
    prof.crossover_eliminates_small_root_refresh_vacuity === elim &&
    prof.actual_quantum_decision_or_multiple_producer_supplied === false,
    "composed crossover source ledger"
  );
}

function verify(R) {
  check(
    R.status === "REFRESH_TO_CLEAN_BASIS_CROSSOVER_AND_COMPOSED_DAG_PIPELINE_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/native_refresh_lottery_crossover.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_REFRESH_LOTTERY_CROSSOVER.md")),
    "current crossover producer and derivation"
  );
  const deps = [
    "native_affine_fibre_relaxation.py",
    "native_basis_lottery.py",
    "native_gaussian_quotient_completion.py",
    "native_prefix_ambiguity_pruning.py",
    "native_small_multiple_completion.py",
    "native_source_refresh.py",
    "ternary_covariant_noise.py",
    "ternary_measured_lattice_decoder.py",
    "ternary_noise_degradation.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  check(R.actual_composed_pipeline_controls.length === 2 && R.composed_scaling_profiles.length === 2, "declared live scope");
  let stagesReplayed = 0;
  R.actual_composed_pipeline_controls.forEach(ctrl => {
    const raw = ctrl.original_records, q0 = BigInt(raw[0].modulus), n = raw[0].label.length;
    const secret = ctrl.original_secret_FOR_CALIBRATION_ONLY.map(BigInt);
    const errN = BigInt(ctrl.original_error_at_index_n_FOR_CALIBRATION_ONLY);
    const radius = BigInt(ctrl.verification_radius);
    raw.forEach((rec, j) => {
      const e = j === n ? errN : 0n;
      check(mod(rec.label.reduce((v, a, i) => v + BigInt(a) * secret[i], 0n) + e, q0) === BigInt(rec.value), "calibration bank observation");
    });
    const pipe = ctrl.pipeline_result;
    let scale = 1n, prefix = Array(n).fill(0);
    pipe.refresh_pruning_stages.forEach(stage => {
      const g = q0 / scale;
      check(BigInt(stage.parent_modulus) === g && BigInt(stage.parent_scale) === scale, "stage parent modulus and scale");
      const signs = stage.refresh_batch.refresh_row_receipts.map(r => r.sign_row);
      const dithers = stage.refresh_batch.refresh_row_receipts.map(r => r.dither);
      const mask = stage.refresh_batch.reduction_side_secret_mask;
      const replayedRefresh = refreshBatch(raw, scale, prefix, signs, mask, dithers);
      same(stage.refresh_batch, replayedRefresh, "stage refresh batch replay");
      const unmaskedCands = [];
      stage.unmask_receipts.forEach(u => {
        const replayedU = unmaskMultiple(u.signed_coefficient, u.masked_multiple, mask, g);
        same(u, replayedU, "stage unmask receipt replay");
        unmaskedCands.push([u.signed_coefficient, replayedU.unmasked_multiple]);
      });
      const replayedPrune = pruneNode(raw, scale, prefix, unmaskedCands, radius, true);
      same(stage.modulo_scale_pruning, replayedPrune, "stage modulo-scale pruning replay");
      const chosen = replayedPrune.surviving_canonical_child_nodes.reduce((best, ch) =>
        BigInt(ch.canonical_node.modulus) < BigInt(best.canonical_node.modulus) ? ch : best
      );
      scale = BigInt(chosen.canonical_node.original_scale);
      prefix = chosen.canonical_node.known_original_lower_prefix_IF_path_true;
      stagesReplayed++;
    });
    const termStage = pipe.terminal_lottery_stage;
    const termNode = canonicalNode(raw, scale, prefix);
    const gTerm = BigInt(termNode.canonical_node.modulus);
    const pTerm = termNode.canonical_node.known_original_lower_prefix_IF_path_true;
    const effMult = pTerm.map(p => enc(mod(gTerm * BigInt(p), q0)));
    same(termStage.canonical_node, termNode.canonical_node, "terminal canonical node");
    check(termStage.canonical_node_sha256 === termNode.canonical_node_sha256, "terminal canonical node hash");
    check(BigInt(termStage.equivalent_original_coefficient) === gTerm, "terminal equivalent coefficient");
    same(termStage.equivalent_original_multiple, effMult, "terminal equivalent multiple");
    const replayedLottery = B.complete(raw, gTerm, effMult, radius);
    same(termStage.basis_lottery_completion, replayedLottery, "terminal clean-basis lottery completion");
    same(pipe.candidate_secret, replayedLottery.candidate_secret, "pipeline candidate secret");
    same(pipe.candidate_secret, ctrl.original_secret_FOR_CALIBRATION_ONLY, "pipeline recovers calibration secret");
    check(
      termStage.canonical_node_to_multiple_equivalence_verified === true &&
      termStage.further_source_refresh_used_at_terminal_node === false &&
      ctrl.matches_truth_after_solving === true &&
      ctrl.actual_multiple_producer_supplied === false,
      "terminal lottery honesty flags"
    );
  });

  R.composed_scaling_profiles.forEach(checkProfile);

  const F = R.falsifiers, prem = F.premature_high_root_lottery_falsifier, below = F.below_floor_refresh_vacuous_but_lottery_succeeds_control;
  B.probability(prem.high_root_lottery_ledger);
  check(
    cmp(parse(prem.high_root_lottery_ledger.no_correct_basis_probability_lower), rat(99n, 100n)) > 0n &&
    prem.no_correct_basis_probability_lower_exceeds_99_percent === true &&
    prem.skipping_refresh_descent_at_wide_root_works === false,
    "premature high-root lottery falsifier"
  );
  checkCrossover(below);

  check(
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.actual_quantum_decision_or_multiple_producer === false &&
    R.complete_recursive_search_to_decision_reduction_established === false &&
    R.novelty_claim === false,
    "promotion guardrails"
  );

  return {
    verified: true,
    composed_controls: R.actual_composed_pipeline_controls.length,
    stages_replayed: stagesReplayed,
    multiple_producer_supplied: false,
  };
}

module.exports = {
  verify,
  canonicalNode,
  refreshBatch,
  unmaskMultiple,
  pruneNode,
  checkRefreshLedger,
  checkCrossover,
  checkProfile,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}

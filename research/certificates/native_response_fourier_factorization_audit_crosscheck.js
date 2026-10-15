"use strict";
// Independent exact replay for response-phase Fourier factorization, 1-call autoregressive chain rule, and signed 2-call pinching.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one, field} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_response_fourier_factorization_audit.json");
const mod = (x, q) => (x % q + q) % q;
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const DIGITS = [[1, 0], [-1, 1], [0, -1]];

function poly(coeffs, q) {
  const K = field(q);
  return K.encode(coeffs.reduce((acc, c, i) => K.plus(acc, K.scale(K.powers[i], c)), K.F()));
}

function cycMul(a, b, root) {
  const out = Array.from({length: root}, () => zero);
  a.forEach((va, i) => {
    if (va[0] !== 0n) {
      b.forEach((vb, j) => {
        if (vb[0] !== 0n) {
          const idx = (i + j) % root;
          out[idx] = add(out[idx], mul(va, vb));
        }
      });
    }
  });
  return out;
}

function histProb(hist, root, denom) {
  const out = Array.from({length: root}, () => zero);
  for (const [a, ca] of hist.entries()) {
    for (const [b, cb] of hist.entries()) {
      const idx = mod(a - b, root);
      out[idx] = add(out[idx], rat(BigInt(ca * cb), BigInt(denom)));
    }
  }
  return out;
}

function tuples(q, n, prefix = []) {
  if (!n) return [prefix];
  const out = [];
  for (let x = 0; x < q; x++) out.push(...tuples(q, n - 1, [...prefix, x]));
  return out;
}

function buildRowsFromRecords(raw, mask) {
  const q = raw[0].modulus, n = raw[0].label.length, M = raw.length / 2;
  const words = tuples(3, M);
  return words.map(word => {
    const beta = word.flatMap(t => DIGITS[t]);
    const freq = Array.from({length: n}, (_, i) =>
      mod(beta.reduce((acc, b, idx) => acc + b * raw[idx].label[i], 0), q)
    );
    const phase = mod(
      beta.reduce((acc, b, idx) => acc + b * raw[idx].value, 0) +
      freq.reduce((acc, a, i) => acc + a * mask[i], 0),
      q
    );
    return {word, frequency: freq, known_phase: phase};
  });
}

function checkTensorControl(T, raw, mask) {
  const q = T.modulus_q, M = T.word_sites_M, D = T.word_dimension_D, sign2 = T.second_call_sign;
  check(D === 3 ** M && T.single_qutrit_site_marginals.length === M, "tensor control dimensions");
  const rows = buildRowsFromRecords(raw, mask);
  const f3Scale = q / 3;

  const siteRaw = [];
  T.single_qutrit_site_marginals.forEach((sm, j) => {
    const r0 = raw[2 * j], r1 = raw[2 * j + 1];
    const phases = [0, 1, 2].map(t => {
      const [b0, b1] = DIGITS[t];
      const f = r0.label.map((a0, i) => mod(b0 * a0 + b1 * r1.label[i], q));
      return mod(b0 * r0.value + b1 * r1.value + f.reduce((acc, a, i) => acc + a * mask[i], 0), q);
    });
    same(sm.digit_phases, phases, "site digit phases");
    const outRaw = [], outPolys = [];
    let sumSite = Array.from({length: q}, () => zero);
    for (let xj = 0; xj < 3; xj++) {
      const hist = new Map();
      for (let wj = 0; wj < 3; wj++) {
        for (let vj = 0; vj < 3; vj++) {
          const e = mod(phases[wj] + sign2 * phases[vj] + f3Scale * vj * (wj - xj), q);
          hist.set(e, (hist.get(e) || 0) + 1);
        }
      }
      const cVec = histProb(hist, q, 27);
      outRaw.push(cVec);
      outPolys.push(poly(cVec, q));
      sumSite = sumSite.map((a, i) => add(a, cVec[i]));
    }
    same(poly(sumSite, q), ["1"], "site marginal normalization");
    same(sm.marginal_outcome_probabilities, outPolys, "site marginal polynomials");
    siteRaw.push(outRaw);
  });

  const prodOutcomes = [], fullOutcomes = [];
  rows.forEach(rx => {
    let prodCoeffs = Array.from({length: q}, (_, i) => i === 0 ? one : zero);
    rx.word.forEach((xj, j) => {
      prodCoeffs = cycMul(prodCoeffs, siteRaw[j][xj], q);
    });
    prodOutcomes.push(poly(prodCoeffs, q));

    const hist = new Map();
    rows.forEach(rw => {
      rows.forEach(rv => {
        const f3Dot = mod(rw.word.reduce((acc, wj, j) => acc + rv.word[j] * (wj - rx.word[j]), 0), 3);
        const e = mod(rw.known_phase + sign2 * rv.known_phase + f3Scale * f3Dot, q);
        hist.set(e, (hist.get(e) || 0) + 1);
      });
    });
    fullOutcomes.push(poly(histProb(hist, q, D ** 3), q));
  });

  same(T.product_of_marginals_all_outcomes, prodOutcomes, "O(M) product outcomes");
  same(T.full_path_sum_all_outcomes, fullOutcomes, "full path sum outcomes");
  same(prodOutcomes, fullOutcomes, "product equals full path sum");
  check(
    T.product_matches_full_path_sum_identically === true &&
    T.single_qutrit_path_terms_evaluated_9_times_3_times_M === 27 * M &&
    T.full_dense_path_terms_3_pow_3M === D ** 3 &&
    T.tensor_qutrit_schedule_classically_tractable_in_O_M === true,
    "tensor factorization flags"
  );
}

function checkAutoregressiveControl(A, raw, mask) {
  const q = A.modulus_q, M = A.word_sites_M, D = A.word_dimension_D, root = A.root_order;
  check(D === 3 ** M && root === Math.max(q, D), "autoregressive dimensions");
  const rows = buildRowsFromRecords(raw, mask);
  const pScale = root / q, fScale = root / D;

  const full1Call = [];
  for (let v = 0; v < D; v++) {
    const hist = new Map();
    rows.forEach((rw, w) => {
      const e = mod(pScale * rw.known_phase + fScale * v * w, root);
      hist.set(e, (hist.get(e) || 0) + 1);
    });
    full1Call.push(poly(histProb(hist, root, D * D), root));
  }
  same(A.full_cyclic_dft_1call_all_outcomes, full1Call, "full 1-call cyclic DFT outcomes");

  const condLookup = new Map();
  check(A.autoregressive_conditional_tables.length === M, "M autoregressive tables");
  A.autoregressive_conditional_tables.forEach((tbl, k) => {
    const r0 = raw[2 * k], r1 = raw[2 * k + 1];
    const sitePhases = [0, 1, 2].map(t => {
      const [b0, b1] = DIGITS[t];
      const f = r0.label.map((a0, i) => mod(b0 * a0 + b1 * r1.label[i], q));
      return mod(b0 * r0.value + b1 * r1.value + f.reduce((acc, a, i) => acc + a * mask[i], 0), q);
    });
    const twScale = root / (3 ** (k + 1));
    check(tbl.step_k === k && tbl.prefix_modulus_3_pow_k === 3 ** k && tbl.prefix_conditionals.length === 3 ** k, "conditional table shape");
    tbl.prefix_conditionals.forEach((pe, vPref) => {
      check(pe.v_prefix_mod_3_pow_k === vPref && pe.parseval_sum_equals_one === true, "prefix entry");
      let sumBr = Array.from({length: root}, () => zero);
      const brPolys = [];
      for (let vk = 0; vk < 3; vk++) {
        const vLeK = vPref + (3 ** k) * vk;
        const hist = new Map();
        for (let t = 0; t < 3; t++) {
          const e = mod(pScale * sitePhases[t] + twScale * vLeK * t, root);
          hist.set(e, (hist.get(e) || 0) + 1);
        }
        const cVec = histProb(hist, root, 9);
        condLookup.set(`${k}:${vPref}:${vk}`, cVec);
        brPolys.push(poly(cVec, root));
        sumBr = sumBr.map((a, i) => add(a, cVec[i]));
      }
      same(poly(sumBr, root), ["1"], "Z_3 Parseval conditional sum equals 1");
      same(pe.conditional_probabilities_v_k_0_1_2, brPolys, "conditional branch polynomials");
    });
  });

  const chainOutcomes = [];
  for (let v = 0; v < D; v++) {
    let prodCoeffs = Array.from({length: root}, (_, i) => i === 0 ? one : zero);
    for (let k = 0; k < M; k++) {
      const vPref = v % (3 ** k);
      const vk = Math.floor(v / (3 ** k)) % 3;
      prodCoeffs = cycMul(prodCoeffs, condLookup.get(`${k}:${vPref}:${vk}`), root);
    }
    chainOutcomes.push(poly(prodCoeffs, root));
  }
  same(A.chain_rule_product_all_outcomes, chainOutcomes, "chain rule outcomes");
  same(chainOutcomes, full1Call, "chain rule matches full 1-call cyclic DFT");
  check(
    A.chain_rule_matches_full_cyclic_dft_identically === true &&
    A.per_sample_autoregressive_evaluation_steps === M &&
    A.one_call_cyclic_dft_classically_sampleable_in_O_M === true,
    "autoregressive flags"
  );
}

function checkSignedControl(S) {
  const raw = S.original_records, mask = S.public_mask, errors = S.calibration_only.original_errors;
  const q = S.modulus_q, D = S.word_dimension_D, root = S.root_order, n = raw[0].label.length;
  const rows = buildRowsFromRecords(raw, mask);
  const pScale = root / q, fScale = root / D;

  const obs = [];
  for (let x = 0; x < D; x++) {
    const hist = new Map();
    rows.forEach((rw, w) => {
      rows.forEach((rv, v) => {
        const e = mod(pScale * (rw.known_phase - rv.known_phase) + fScale * v * (w - x), root);
        hist.set(e, (hist.get(e) || 0) + 1);
      });
    });
    obs.push(poly(histProb(hist, root, D ** 3), root));
  }
  same(S.exact_observed_all_outcome_probabilities, obs, "observed signed 2-call outcomes");
  check(S.diagonal_w_eq_v_zero_phase_path_count === D, "all D diagonal paths w==v have zero phase");
  const diag = Array.from({length: D}, (_, x) => {
    const h = new Map();
    for (let w = 0; w < D; w++) {
      const e = mod(w * (w - x), D);
      h.set(e, (h.get(e) || 0) + 1);
    }
    return poly(histProb(h, D, D ** 3), D);
  });
  same(S.diagonal_fourier_component_weights, diag, "quadratic Fourier phase retained");
  check(S.diagonal_data_phase_cancels_only === true &&
    S.diagonal_component_is_probability_lower_bound === false, "no diagonal probability floor");

  const secrets = tuples(q, n);
  const errPh = rows.map(r =>
    mod(r.word.reduce((acc, t, j) => acc + DIGITS[t][0] * errors[2 * j] + DIGITS[t][1] * errors[2 * j + 1], 0), q)
  );

  const sweepOut = [], pinchedOut = [];
  for (let x = 0; x < D; x++) {
    let sweep = Array.from({length: root}, () => zero);
    secrets.forEach(s => {
      const hist = new Map();
      rows.forEach((rw, w) => {
        rows.forEach((rv, v) => {
          const ph = rw.frequency.reduce((acc, a, i) => acc + (a - rv.frequency[i]) * s[i], 0);
          const e = mod(pScale * (ph + errPh[w] - errPh[v]) + fScale * v * (w - x), root);
          hist.set(e, (hist.get(e) || 0) + 1);
        });
      });
      const term = histProb(hist, root, (D ** 3) * secrets.length);
      sweep = sweep.map((a, i) => add(a, term[i]));
    });

    const grouped = new Map();
    rows.forEach((rw, w) => {
      rows.forEach((rv, v) => {
        const df = JSON.stringify(rw.frequency.map((a, i) => mod(a - rv.frequency[i], q)));
        const e = mod(pScale * (errPh[w] - errPh[v]) + fScale * v * (w - x), root);
        if (!grouped.has(df)) grouped.set(df, new Map());
        const h = grouped.get(df);
        h.set(e, (h.get(e) || 0) + 1);
      });
    });
    let pinched = Array.from({length: root}, () => zero);
    for (const h of grouped.values()) {
      const term = histProb(h, root, D ** 3);
      pinched = pinched.map((a, i) => add(a, term[i]));
    }
    sweepOut.push(poly(sweep, root));
    pinchedOut.push(poly(pinched, root));
  }
  same(S.uniform_secret_mean_all_outcomes, sweepOut, "signed uniform-secret sweep outcomes");
  same(S.difference_relation_pinched_all_outcomes, pinchedOut, "signed difference-relation pinched outcomes");
  same(sweepOut, pinchedOut, "signed sweep equals difference pinching");
  check(
    S.signed_pinching_matches_secret_sweep_identically === true &&
    typeof S.signed_readout_differs_from_unsigned_readout === "boolean",
    "signed 2-call flags"
  );
}

function verify(R) {
  check(
    R.status === "RESPONSE_FOURIER_FACTORIZATION_AND_SIGNED_PATH_PINCHING_AUDIT_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/native_response_fourier_factorization_audit.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_RESPONSE_FOURIER_FACTORIZATION_AUDIT.md")) &&
    R.contract_sha256 === hash(path.join(ROOT, "research/hypotheses/native_response_fourier_factorization_audit_contract.json")),
    "producer, derivation, and contract hashes"
  );
  const deps = [
    "native_basis_lottery.py",
    "native_full_root_slice.py",
    "native_response_path_valuation.py",
    "native_word_span_decision.py",
    "ternary_measured_lattice_decoder.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  check(
    R.tensor_qutrit_factorization_controls.length === 3 &&
    R.one_call_cyclic_autoregressive_controls.length === 3 &&
    R.signed_two_call_cyclic_controls.length === 3,
    "3 controls per theorem family"
  );

  for (let i = 0; i < 3; i++) {
    const raw = R.signed_two_call_cyclic_controls[i].original_records;
    const mask = R.signed_two_call_cyclic_controls[i].public_mask;
    checkTensorControl(R.tensor_qutrit_factorization_controls[i], raw, mask);
    checkAutoregressiveControl(R.one_call_cyclic_autoregressive_controls[i], raw, mask);
    checkSignedControl(R.signed_two_call_cyclic_controls[i]);
  }
  const C = R.diagonal_floor_countercontrol, K9 = field(9);
  const phases = [8, 1, 0], h = new Map();
  for (let w = 0; w < 3; w++) for (let v = 0; v < 3; v++) {
    const e = mod(phases[w] - phases[v] + 3 * v * w, 9);
    h.set(e, (h.get(e) || 0) + 1);
  }
  same(C, {modulus_q: 9, word_dimension_D: 3, original_pair_values: [8, 0],
    digit_phases: phases, outcome_x: 0, exact_probability: poly(histProb(h, 9, 27), 9),
    diagonal_component_weight: "1/9", old_claimed_floor: "1/3",
    probability_floor_claim_refuted: true}, "valid paired-row countercontrol");
  check(E.sign(K9, K9.plus(K9.decode(C.exact_probability),
    K9.scale(K9.unit, rat(-1n, 9n)))) < 0, "full probability below diagonal component weight");
  check(
    R.tensor_qutrit_factorization_controls[2].differs_from_cyclic_F_D_when_M_ge_2 === true &&
    R.signed_two_call_cyclic_controls[0].signed_readout_differs_from_unsigned_readout === true &&
    R.signed_two_call_cyclic_controls[2].signed_readout_differs_from_unsigned_readout === true,
    "tensor F_3^M differs from cyclic F_{3^M} and signed differs from unsigned at q=9"
  );

  check(
    R.this_finite_audit_supplies_polynomial_two_call_sampler === false &&
    R.full_cyclic_approximate_sampling_has_separate_classical_baseline === true &&
    R.general_quantum_lower_bound_claimed === false &&
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.novelty_claim === false,
    "honesty guardrails"
  );

  return {
    verified: true,
    tensor_controls: R.tensor_qutrit_factorization_controls.length,
    autoregressive_controls: R.one_call_cyclic_autoregressive_controls.length,
    signed_two_call_controls: R.signed_two_call_cyclic_controls.length,
    accepted_speedup_candidate: false,
  };
}

module.exports = {
  verify,
  checkTensorControl,
  checkAutoregressiveControl,
  checkSignedControl,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}

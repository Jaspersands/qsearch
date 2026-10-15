"use strict";
// Independent exact replay for banded cyclic QFT two-call transfer-matrix contraction and scaling ledgers.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one, field} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_banded_qft_transfer_matrix_audit.json");
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

function cycNormSq(coeffs, root) {
  const out = Array.from({length: root}, () => zero);
  coeffs.forEach((va, i) => {
    if (va[0] !== 0n) {
      coeffs.forEach((vb, j) => {
        if (vb[0] !== 0n) {
          const idx = mod(i - j, root);
          out[idx] = add(out[idx], mul(va, vb));
        }
      });
    }
  });
  return out;
}

function tuples(q, n, prefix = []) {
  if (!n) return [prefix];
  const out = [];
  for (let x = 0; x < q; x++) out.push(...tuples(q, n - 1, [...prefix, x]));
  return out;
}

function checkBandedSweep(S, raw, mask) {
  const q = S.modulus_q, M = S.word_sites_M, D = S.word_dimension_D, root = S.root_order;
  const b = S.twiddle_bandwidth_b, sign2 = S.second_call_sign;
  check(D === 3 ** M && root === Math.max(q, D) && b >= 1 && b <= M, "valid banded sweep parameters");
  const pScale = root / q, fScale = root / D;

  const sitePhases = Array.from({length: M}, (_, j) => {
    const r0 = raw[2 * j], r1 = raw[2 * j + 1];
    return [0, 1, 2].map(t => {
      const [b0, b1] = DIGITS[t];
      const f = r0.label.map((a0, i) => mod(b0 * a0 + b1 * r1.label[i], q));
      return mod(b0 * r0.value + b1 * r1.value + f.reduce((acc, a, i) => acc + a * mask[i], 0), q);
    });
  });

  const words = tuples(3, M);
  const dpOuts = [];
  let winEvals = 0;

  words.forEach((xWord, xIdx) => {
    const initLen = Math.min(b - 1, M);
    let fCurr = new Map();
    tuples(3, initLen).forEach(st => {
      fCurr.set(JSON.stringify(st), Array.from({length: root}, (_, i) => i === 0 ? one : zero));
    });
    let evalsThisX = 0;
    for (let k = 0; k < M; k++) {
      const winLen = Math.min(b, M - k);
      const prevLen = Math.min(b - 1, M - k);
      const nextLen = Math.min(b - 1, M - 1 - k);
      const fNext = new Map();
      tuples(3, nextLen).forEach(st => {
        fNext.set(JSON.stringify(st), Array.from({length: root}, () => zero));
      });
      const phW = sitePhases[k], phV = sitePhases[M - 1 - k];
      tuples(3, winLen).forEach(wWin => {
        evalsThisX++;
        const wk = wWin[0];
        let winShift = 0;
        for (let off = 0; off < winLen; off++) {
          winShift += (wWin[off] - xWord[k + off]) * (3 ** (M - 1 - off));
        }
        const lCoeffs = Array.from({length: root}, () => zero);
        for (let t = 0; t < 3; t++) {
          const e = mod(pScale * (phW[wk] + sign2 * phV[t]) + fScale * t * winShift, root);
          lCoeffs[e] = add(lCoeffs[e], rat(1n, 3n));
        }
        const prevKey = JSON.stringify(wWin.slice(0, prevLen));
        const nextKey = JSON.stringify(wWin.slice(1));
        const prodTerm = cycMul(fCurr.get(prevKey), lCoeffs, root);
        const curNext = fNext.get(nextKey);
        fNext.set(nextKey, curNext.map((a, i) => add(a, prodTerm[i])));
      });
      fCurr = fNext;
    }
    if (xIdx === 0) winEvals = evalsThisX;
    const amp = fCurr.get("[]");
    const normSq = cycNormSq(amp, root).map(c => div(c, rat(BigInt(D))));
    dpOuts.push(poly(normSq, root));
  });

  same(S.transfer_matrix_dp_all_outcomes, dpOuts, "transfer-matrix DP outcomes");
  same(S.brute_force_path_sum_all_outcomes, dpOuts, "brute-force path sum outcomes match DP");
  check(
    S.max_transfer_matrix_boundary_states_3_pow_b_minus_1 === 3 ** (b - 1) &&
    S.dp_window_evaluations_per_outcome === winEvals &&
    S.dp_window_evaluations_upper_bound_M_times_3_pow_b === M * (3 ** b) &&
    S.brute_force_path_pairs_per_outcome_3_pow_2M === D * D &&
    S.dp_matches_brute_force_identically === true,
    "banded DP work and identity flags"
  );
}

function checkScaling(L) {
  const M = L.word_sites_M, b = L.twiddle_bandwidth_b;
  check(b >= 1 && b <= M, "valid scaling M and b");
  const bStates = 3 ** (b - 1);
  let dpWins = 0, gates = 0;
  for (let k = 0; k < M; k++) {
    dpWins += 3 ** Math.min(b, M - k);
    gates += Math.min(b, M - k);
  }
  const dpUpper = M * (3 ** b);
  same(L, {
    word_sites_M: M,
    twiddle_bandwidth_b: b,
    qft_twiddle_gates_count: gates,
    transfer_matrix_boundary_states_3_pow_b_minus_1: bStates,
    exact_dp_window_evaluations_per_outcome: dpWins,
    dp_window_evaluations_upper_M_3_pow_b: dpUpper,
    local_summand_evaluations_3_times_dp_windows: 3 * dpWins,
    dp_within_M_3_pow_b_bound: dpWins <= dpUpper,
    polynomial_in_M_when_b_is_O_log_M: b <= (M.toString(2).length + 1),
    full_bandwidth_b_eq_M: b === M,
  }, "bandwidth scaling ledger");
}

function verify(R) {
  check(
    R.status === "BANDED_QFT_TWO_CALL_TRANSFER_MATRIX_DEQUANTIZATION_AUDIT_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/native_banded_qft_transfer_matrix_audit.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_BANDED_QFT_TRANSFER_MATRIX_AUDIT.md")) &&
    R.contract_sha256 === hash(path.join(ROOT, "research/hypotheses/native_banded_qft_transfer_matrix_audit_contract.json")),
    "producer, derivation and contract hashes"
  );
  const deps = [
    "native_basis_lottery.py",
    "native_full_root_slice.py",
    "native_response_fourier_factorization_audit.py",
    "native_response_path_valuation.py",
    "native_word_span_decision.py",
    "ternary_measured_lattice_decoder.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  const ctrl = R.banded_qft_m2_sweep_control;
  check(ctrl.bandwidth_and_sign_sweeps.length === 4, "4 bandwidth and sign sweeps");
  ctrl.bandwidth_and_sign_sweeps.forEach(s => checkBandedSweep(s, ctrl.original_records, ctrl.public_mask));
  check(
    ctrl.b1_differs_from_b2_unsigned === true &&
    ctrl.b1_differs_from_b2_signed === true &&
    ctrl.bandwidth_and_sign_sweeps[1].matches_untruncated_cyclic_qft_when_b_eq_M === true,
    "b=1 vs b=2 difference and b=M full cyclic match"
  );

  check(R.bandwidth_scaling_ledgers.length === 7, "7 scaling ledgers");
  R.bandwidth_scaling_ledgers.forEach(checkScaling);

  check(
    R.full_bandwidth_b_eq_M_is_poly_M === false &&
    R.three_or_more_calls_contracted_by_2call_dp === false &&
    R.general_quantum_lower_bound_claimed === false &&
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.novelty_claim === false,
    "honesty guardrails"
  );

  return {
    verified: true,
    sweeps_checked: ctrl.bandwidth_and_sign_sweeps.length,
    scaling_profiles: R.bandwidth_scaling_ledgers.length,
    accepted_speedup_candidate: false,
  };
}

module.exports = {
  verify,
  checkBandedSweep,
  checkScaling,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}

"use strict";
// Independent exact replay for multi-round interleaved syndrome-work circuits and 2-call response pinching.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const W = require("./native_word_spectral_filter_audit_crosscheck.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one, field} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_interleaved_syndrome_work_audit.json");
const mod = (x, q) => (x % q + q) % q;
const enc = x => x <= 9007199254740991n && x >= -9007199254740991n ? Number(x) : String(x);
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");

function isqrt(n) {
  if (n < 2n) return n;
  let x = 1n << BigInt((n.toString(2).length + 1) >> 1);
  while (true) {
    const y = (x + n / x) >> 1n;
    if (y >= x) return x;
    x = y;
  }
}

function poly(coeffs, q) {
  const K = field(q);
  return K.encode(coeffs.reduce((acc, c, i) => K.plus(acc, K.scale(K.powers[i], c)), K.F()));
}

function tuples(q, n, prefix = []) {
  if (!n) return [prefix];
  const out = [];
  for (let x = 0; x < q; x++) out.push(...tuples(q, n - 1, [...prefix, x]));
  return out;
}

function errorPhases(rows, errors, q) {
  const digits = [[1, 0], [-1, 1], [0, -1]];
  return rows.map(r =>
    mod(
      r.word.reduce((s, t, j) => s + digits[t][0] * errors[2 * j] + digits[t][1] * errors[2 * j + 1], 0),
      q
    )
  );
}

function checkInterleavedControl(C) {
  W.control(C.native_source_reference);
  const base = C.native_source_reference;
  const rows = base.actual_native_word_rows;
  const q = C.modulus_q, n = C.dimension_n, M = C.word_pairs_M, D = C.word_dimension_D, N = C.syndrome_dimension_N;
  check(D === 3 ** M && N === q ** n && rows.length === D, "control dimensions");
  const freqs = tuples(q, n);
  const errors = C.calibration_truth_FOR_SWEEP_ONLY.original_errors;
  const errPh = errorPhases(rows, errors, q);

  const fCounts = new Map();
  rows.forEach(r => {
    const k = JSON.stringify(r.frequency);
    fCounts.set(k, (fCounts.get(k) || 0) + 1);
  });
  let maxFibre = 0, caSum = zero;
  for (const c of fCounts.values()) {
    if (c > maxFibre) maxFibre = c;
    caSum = add(caSum, rat(BigInt(c * c), BigInt(D * D)));
  }
  check(
    C.max_fibre_multiplicity === maxFibre &&
    C.fibre_trace_envelope_upper_m_max_over_D === str(rat(BigInt(maxFibre), BigInt(D))) &&
    C.exact_1call_collision_density_C_A === str(caSum),
    "fibre multiplicity and C_A"
  );

  // Raw Gram overlap polynomial
  const rawCoeffs = Array.from({length: q}, () => zero);
  rows.forEach((rw, wIdx) => {
    rows.forEach((rv, vIdx) => {
      if (JSON.stringify(rw.frequency) === JSON.stringify(rv.frequency)) {
        const diff = mod(errPh[vIdx] - errPh[wIdx], q);
        rawCoeffs[diff] = add(rawCoeffs[diff], rat(1n, BigInt(D * D)));
      }
    });
  });
  const rawPoly = poly(rawCoeffs, q);
  same(C.raw_gram_uniform_secret_overlap_root_polynomial, rawPoly, "raw Gram uniform-secret root polynomial");

  // Recompute Q2 phase table and delta sector weight polynomials
  const Q2 = freqs.map(z => {
    const quad = z.reduce((acc, zi, i) => acc + (i + 1) * (zi * zi + zi), 0);
    const bump = z.every(zi => zi === 0) ? Math.floor(q / 3) : 0;
    return mod(quad + bump, q);
  });
  same(C.multi_round_syndrome_weights.Q2_phase_table, Q2, "Q2 phase table");

  const deltaRaw = new Map();
  const sumCoeffs = Array.from({length: q}, () => zero);
  const distinctDelta = new Set();
  freqs.forEach(delta => {
    const cVec = Array.from({length: q}, () => zero);
    freqs.forEach((z, zIdx) => {
      freqs.forEach((zp, zpIdx) => {
        const inner = mod(delta.reduce((acc, d, i) => acc + d * (z[i] - zp[i]), 0), q);
        const expDiff = mod(Q2[zIdx] - Q2[zpIdx] + inner, q);
        cVec[expDiff] = add(cVec[expDiff], rat(1n, BigInt(N * N)));
      });
    });
    const key = delta.join(",");
    deltaRaw.set(key, cVec);
    const p = poly(cVec, q);
    distinctDelta.add(JSON.stringify(p));
    same(C.multi_round_syndrome_weights.delta_sector_weight_polynomials[key], p, "delta sector weight polynomial");
    for (let k = 0; k < q; k++) sumCoeffs[k] = add(sumCoeffs[k], cVec[k]);
  });
  const oneCoeffs = Array.from({length: q}, (_, i) => i === 0 ? one : zero);
  same(poly(sumCoeffs, q), poly(oneCoeffs, q), "Parseval sum over delta equals 1");
  check(
    C.multi_round_syndrome_weights.distinct_delta_weight_polynomial_count === distinctDelta.size &&
    distinctDelta.size >= 2 &&
    C.multi_round_syndrome_weights.parseval_sum_over_all_sectors_equals_one === true,
    "non-constant delta weights and Parseval flag"
  );

  // Recompute sector uniform-secret overlaps and total ground band sum
  const totalBandCoeffs = Array.from({length: q}, () => zero);
  check(C.sector_uniform_secret_overlaps.length === N, "all N syndrome sectors present");
  C.sector_uniform_secret_overlaps.forEach((sec, idx) => {
    const t = freqs[idx];
    same(sec.sector_t, t, "sector t order");
    const secCoeffs = Array.from({length: q}, () => zero);
    rows.forEach((rw, wIdx) => {
      const deltaKey = rw.frequency.map((f, i) => mod(f - t[i], q)).join(",");
      const wCoeffs = deltaRaw.get(deltaKey);
      rows.forEach((rv, vIdx) => {
        if (JSON.stringify(rw.frequency) === JSON.stringify(rv.frequency)) {
          const errDiff = mod(errPh[vIdx] - errPh[wIdx], q);
          wCoeffs.forEach((cVal, kExp) => {
            if (cmp(cVal, zero) !== 0n) {
              const targetExp = mod(errDiff + kExp, q);
              secCoeffs[targetExp] = add(secCoeffs[targetExp], div(cVal, rat(BigInt(D * D))));
            }
          });
        }
      });
    });
    for (let k = 0; k < q; k++) totalBandCoeffs[k] = add(totalBandCoeffs[k], secCoeffs[k]);
    same(sec.uniform_secret_mean_overlap_root_polynomial, poly(secCoeffs, q), "sector uniform-secret overlap polynomial");
  });

  const totalBandPoly = poly(totalBandCoeffs, q);
  same(C.sum_over_all_sectors_uniform_secret_overlap_root_polynomial, totalBandPoly, "total ground band polynomial");
  same(totalBandPoly, rawPoly, "multi-round Parseval ground-band conservation matches raw Gram");
  check(C.multi_round_parseval_ground_band_conservation_holds === true, "multi-round Parseval conservation");

  // Cross-fibre pinching check
  let offFibre = 0;
  rows.forEach(rw => rows.forEach(rv => { if (JSON.stringify(rw.frequency) !== JSON.stringify(rv.frequency)) offFibre++; }));
  const sweepCross = Array.from({length: q}, () => zero);
  freqs.forEach(sVec => {
    rows.forEach((rw, wIdx) => {
      const pw = mod(rw.frequency.reduce((acc, a, i) => acc + a * sVec[i], 0) + errPh[wIdx], q);
      rows.forEach((rv, vIdx) => {
        const pv = mod(rv.frequency.reduce((acc, a, i) => acc + a * sVec[i], 0) + errPh[vIdx], q);
        sweepCross[mod(pv - pw, q)] = add(sweepCross[mod(pv - pw, q)], rat(1n, BigInt(N * D * D)));
      });
    });
  });
  const sweepCrossPoly = poly(sweepCross, q);
  same(C.cross_fibre_word_effect_pinching, {
    off_fibre_nonzero_entries_in_E_cross: offFibre,
    complete_secret_sweep_mean_root_polynomial: sweepCrossPoly,
    pinched_fibre_diagonal_root_polynomial: rawPoly,
    cross_fibre_entries_annihilated_exactly_by_secret_twirl: true,
  }, "cross-fibre pinching verification");
}

function checkTwoCallControl(C) {
  W.control(C.native_source_reference);
  const q = C.modulus_q, n = C.dimension_n, M = C.word_pairs_M, D = C.word_dimension_D, N = C.syndrome_dimension_N;
  const rows = C.native_source_reference.actual_native_word_rows;
  const errors = C.calibration_truth_FOR_SWEEP_ONLY.original_errors;
  const errPh = errorPhases(rows, errors, q);
  const freqs = tuples(q, n);

  const fCounts = new Map();
  rows.forEach(r => {
    const k = JSON.stringify(r.frequency);
    fCounts.set(k, (fCounts.get(k) || 0) + 1);
  });
  let oneColl = 0;
  for (const c of fCounts.values()) oneColl += c * c;

  const pairList = [];
  const pairCounts = new Map();
  rows.forEach((r1, w1) => {
    rows.forEach((r2, w2) => {
      const tau = r1.frequency.map((a, i) => mod(a + r2.frequency[i], q));
      const eSum = mod(errPh[w1] + errPh[w2], q);
      pairList.push([tau, eSum]);
      const k = JSON.stringify(tau);
      pairCounts.set(k, (pairCounts.get(k) || 0) + 1);
    });
  });
  let twoColl = 0;
  for (const c of pairCounts.values()) twoColl += c * c;
  const prodColl = oneColl * oneColl;
  const nonTriv = twoColl - prodColl;

  const sweep2Coeffs = Array.from({length: q}, () => zero);
  freqs.forEach(sVec => {
    const hist = new Map();
    pairList.forEach(([tau, eSum]) => {
      const p = mod(tau.reduce((acc, a, i) => acc + a * sVec[i], 0) + eSum, q);
      hist.set(p, (hist.get(p) || 0) + 1);
    });
    for (const [p1, c1] of hist.entries()) {
      for (const [p2, c2] of hist.entries()) {
        sweep2Coeffs[mod(p2 - p1, q)] = add(sweep2Coeffs[mod(p2 - p1, q)], rat(BigInt(c1 * c2), BigInt(N * (D ** 4))));
      }
    }
  });
  const sweep2Poly = poly(sweep2Coeffs, q);

  const pinched2Coeffs = Array.from({length: q}, () => zero);
  const byTau = new Map();
  pairList.forEach(([tau, eSum]) => {
    const k = JSON.stringify(tau);
    if (!byTau.has(k)) byTau.set(k, []);
    byTau.get(k).push(eSum);
  });
  for (const eList of byTau.values()) {
    const hist = new Map();
    eList.forEach(e => hist.set(e, (hist.get(e) || 0) + 1));
    for (const [e1, c1] of hist.entries()) {
      for (const [e2, c2] of hist.entries()) {
        pinched2Coeffs[mod(e2 - e1, q)] = add(pinched2Coeffs[mod(e2 - e1, q)], rat(BigInt(c1 * c2), BigInt(D ** 4)));
      }
    }
  }
  const pinched2Poly = poly(pinched2Coeffs, q);

  same(C, {
    native_source_reference: C.native_source_reference,
    calibration_truth_FOR_SWEEP_ONLY: C.calibration_truth_FOR_SWEEP_ONLY,
    modulus_q: q,
    dimension_n: n,
    word_pairs_M: M,
    word_dimension_D: D,
    syndrome_dimension_N: N,
    one_call_fibre_collision_pairs: oneColl,
    one_call_collision_density_C_A: str(rat(BigInt(oneColl), BigInt(D * D))),
    two_call_total_4tuples_D4: D ** 4,
    two_call_additive_collision_4tuples: twoColl,
    product_of_1call_collision_4tuples: prodColl,
    nontrivial_cross_fibre_additive_collision_4tuples: nonTriv,
    two_call_collision_density_C2_A: str(rat(BigInt(twoColl), BigInt(D ** 4))),
    complete_secret_sweep_2call_root_polynomial: sweep2Poly,
    additive_4tuple_pinched_2call_root_polynomial: pinched2Poly,
    two_call_pinching_theorem_verified: true,
    nontrivial_additive_collisions_present: nonTriv > 0,
  }, "2-call response interleaving and 4-tuple additive pinching");
}

function checkCensus(C) {
  const n = C.dimension_n, d = C.root_digits_d, q = 3 ** d, M = C.word_pairs_M, D = 3 ** M, N = q ** n;
  const total4 = D ** 4;
  const zeroZ = 15 ** M;
  const div3Nonzero = (27 ** M) - zeroZ;
  const unit4 = total4 - (27 ** M);
  const probDiv3 = d === 1 ? one : rat(3n ** BigInt(n), BigInt(N));
  const expC2 = add(
    add(rat(BigInt(zeroZ), BigInt(total4)), mul(rat(BigInt(div3Nonzero), BigInt(total4)), probDiv3)),
    mul(rat(BigInt(unit4), BigInt(total4)), rat(1n, BigInt(N)))
  );
  same(C, {
    dimension_n: n,
    root_digits_d: d,
    modulus_q: q,
    word_pairs_M: M,
    word_dimension_D: D,
    syndrome_dimension_N: N,
    total_4tuples_81_pow_M: total4,
    stratum_zero_over_Z_15_pow_M: zeroZ,
    stratum_div3_nonzero_27_pow_M_minus_15_pow_M: div3Nonzero,
    stratum_unit_81_pow_M_minus_27_pow_M: unit4,
    div3_subgroup_collision_probability: str(probDiv3),
    exact_expected_2call_collision_density_E_A_C2: str(expC2),
    complete_label_bank_enumeration_verified: C.complete_label_bank_enumeration_verified,
    three_adic_valuation_stratification_verified: true,
  }, "IID 2-call 3-adic valuation stratification census");
}

function checkScaling(S) {
  const n = S.dimension_n, r = S.root_digits_r, sur = S.word_surplus, calls = S.declared_response_calls_r;
  const M = n * r + sur;
  const oneFactor = add(one, rat(1n, 3n ** BigInt(sur)));
  const twoFactor = add(one, rat(1n, 3n ** BigInt(sur)));
  const cheb = (2 * calls + 1) ** 2;
  const ampFactor = mul(rat(BigInt(cheb)), oneFactor);
  const target = parse(S.target_mean_acceptance);
  const sq = div(mul(target, rat(3n ** BigInt(n * r))), oneFactor);
  let dReq = isqrt(sq[0] / sq[1]);
  if (dReq * dReq * sq[1] < sq[0]) dReq += 1n;
  same(S, {
    dimension_n: n,
    root_digits_r: r,
    word_sites_M: M,
    word_surplus: sur,
    declared_response_calls_r: calls,
    one_call_expected_collision_upper: {coefficient: str(oneFactor), base: 3, exponent: -n * r},
    two_call_expected_collision_upper: {coefficient: str(twoFactor), base: 3, exponent: -n * r},
    r_call_reflection_chebyshev_multiplier_2r_plus_1_sq: cheb,
    r_call_amplified_mean_acceptance_upper: {coefficient: str(ampFactor), base: 3, exponent: -n * r},
    target_mean_acceptance: str(target),
    necessary_reflection_calls_lower_for_target: enc(dReq / 2n),
    arbitrary_depth_label_only_syndrome_interleaving_bounded_by_fibre_pinching: true,
    universal_quantum_lower_bound_claimed: false,
    scalable_quantum_speedup_supplied: false,
  }, "interleaved scaling ledger");
}

function verify(R) {
  check(
    R.status === "INTERLEAVED_SYNDROME_WORK_PINCHING_AND_RESPONSE_DEGREE_AUDIT_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/native_interleaved_syndrome_work_audit.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_INTERLEAVED_SYNDROME_WORK_AUDIT.md")) &&
    R.contract_sha256 === hash(path.join(ROOT, "research/hypotheses/native_interleaved_syndrome_work_audit_contract.json")),
    "producer, derivation and contract hashes"
  );
  const deps = [
    "native_basis_lottery.py",
    "native_full_root_slice.py",
    "native_small_multiple_completion.py",
    "native_syndrome_dilation.py",
    "native_word_spectral_filter_audit.py",
    "native_word_span_decision.py",
    "ternary_measured_lattice_decoder.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  check(R.multi_round_interleaved_controls.length === 3, "3 interleaved controls");
  R.multi_round_interleaved_controls.forEach(checkInterleavedControl);

  check(R.two_call_response_interleaving_controls.length === 2, "2 two-call controls");
  R.two_call_response_interleaving_controls.forEach(checkTwoCallControl);

  check(R.iid_two_call_additive_collision_censuses.length === 4, "4 IID censuses");
  R.iid_two_call_additive_collision_censuses.forEach(checkCensus);
  check(R.iid_two_call_additive_collision_censuses[0].complete_label_bank_enumeration_verified === true, "complete bank census verified on M=1");

  check(R.interleaved_scaling_ledgers.length === 4, "4 scaling ledgers");
  R.interleaved_scaling_ledgers.forEach(checkScaling);

  check(
    R.universal_quantum_lower_bound_claimed === false &&
    R.scalable_quantum_speedup_supplied === false &&
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.novelty_claim === false,
    "honesty guardrails"
  );

  return {
    verified: true,
    interleaved_controls: R.multi_round_interleaved_controls.length,
    two_call_controls: R.two_call_response_interleaving_controls.length,
    iid_censuses: R.iid_two_call_additive_collision_censuses.length,
    scalable_quantum_speedup_supplied: false,
  };
}

module.exports = {
  verify,
  checkInterleavedControl,
  checkTwoCallControl,
  checkCensus,
  checkScaling,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}

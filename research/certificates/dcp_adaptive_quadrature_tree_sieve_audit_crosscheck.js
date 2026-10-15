#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `dcp_adaptive_quadrature_tree_sieve_audit`.
 *
 * Recomputes from first principles:
 * 1. Exact modular phase identity for every k with v_2(k) = ell - 1 - r:
 *      (k * s) mod 2^ell === (k * s_{<r} + 2^(ell - 1) * s_r) mod 2^ell,
 *    and exact rational variance 1/2 - v^2 / 4.
 * 2. Complete census of equal-valuation CNOT label pairs (k_1, k_2) with v_2(k_1) = v_2(k_2) = h < ell - 1,
 *    verifying that min(v_2(k_1 + k_2), v_2(k_1 - k_2)) == h + 1 and
 *    max(v_2(k_1 + k_2), v_2(k_1 - k_2)) >= h + 2 for every pair.
 * 3. Exact rational visibility squaring v_d = (1 - p_bad)^(2^d) across sieve depths d = 0..6.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_adaptive_quadrature_tree_sieve_audit.json"
);

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function parseFrac(str) {
  const parts = String(str).split("/");
  if (parts.length === 1) {
    return { num: BigInt(parts[0]), den: 1n };
  }
  return { num: BigInt(parts[0]), den: BigInt(parts[1]) };
}

function formatFrac(num, den) {
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcd(num, den);
  return `${(num / g).toString()}/${(den / g).toString()}`;
}

function powBigInt(base, exp) {
  let res = 1n;
  let b = BigInt(base);
  let e = BigInt(exp);
  while (e > 0n) {
    if (e & 1n) res *= b;
    b *= b;
    e >>= 1n;
  }
  return res;
}

function twoAdicValuation(k, ell) {
  const N = 1 << ell;
  let km = ((k % N) + N) % N;
  if (km === 0) return ell;
  let v = 0;
  while ((km & 1) === 0) {
    km >>= 1;
    v += 1;
  }
  return v;
}

function main() {
  const report = JSON.parse(fs.readFileSync(process.argv[2] || ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "dcp_adaptive_quadrature_tree_sieve_audit") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let demodChecked = 0;
  for (const row of report.bitwise_dyadic_demodulation_audit) {
    const ell = row.ell;
    const N = 1 << ell;
    const halfN = 1 << (ell - 1);
    const v = parseFrac(row.visibility_v_fraction);
    const expMeanStr = formatFrac(v.num, 2n * v.den);
    const expVarStr = formatFrac(2n * v.den * v.den - v.num * v.num, 4n * v.den * v.den);
    if (
      expMeanStr !== row.expected_abs_demod_mean_fraction ||
      expVarStr !== row.expected_demod_variance_fraction
    ) {
      throw new Error(`Demodulation rational mean/var mismatch at ell=${ell}`);
    }

    let tuples = 0;
    for (let s = 0; s < N; s++) {
      for (let r = 0; r < ell; r++) {
        const h = ell - 1 - r;
        const sPrefix = s & ((1 << r) - 1);
        const sBit = (s >> r) & 1;
        for (let k = 1; k < N; k++) {
          if (twoAdicValuation(k, ell) !== h) continue;
          const lhs = (k * s) % N;
          const rhs = (k * sPrefix + halfN * sBit) % N;
          if (lhs !== rhs) {
            throw new Error(`Modular phase reduction mismatch at ell=${ell}, s=${s}, r=${r}, k=${k}`);
          }
          tuples += 1;
        }
      }
    }
    if (
      tuples !== row.tuples_checked ||
      !row.all_pointwise_signs_match_bit_s_r ||
      row.mean_identity_is_a_sampled_receiver !== false ||
      row.prescribed_labels_or_exact_expectations_available_to_solver !== false
    ) {
      throw new Error(`Demodulation census check failed at ell=${ell}`);
    }
    demodChecked += 1;
  }

  for (const row of report.raw_acquisition_profiles_NOT_executed) {
    const probability = parseFrac(row.stratum_probability);
    const expected = parseFrac(row.expected_original_preparations_without_sieve);
    if (probability.num * (1n << BigInt(row.ell)) !== probability.den * (1n << BigInt(row.stage)) ||
        expected.num * (1n << BigInt(row.stage)) !== expected.den * BigInt(row.useful_record_quota) * (1n << BigInt(row.ell)) ||
        row.sieved_acquisition_cost_is_supplied_by_this_bound !== false) throw new Error("Unpaid target acquisition");
  }
  if (report.end_to_end_shift_receiver_implemented !== false || report.sampled_shift_recovery_verified !== false) {
    throw new Error("Mean identities promoted into an implemented receiver");
  }
  require("./dcp_paid_tree_receiver_crosscheck.js").confidenceCounterexample(report.old_factor_two_confidence_claim_counterexample);

  let dichotomyChecked = 0;
  for (const row of report.equal_valuation_cnot_dichotomy_audit) {
    const ell = row.ell;
    const N = 1 << ell;
    const h = row.valuation_h;
    const labels = [];
    for (let k = 1; k < N; k++) {
      if (twoAdicValuation(k, ell) === h) labels.push(k);
    }
    if (labels.length !== row.stratum_size || labels.length !== 1 << (ell - 1 - h)) {
      throw new Error(`Stratum size mismatch at ell=${ell}, h=${h}`);
    }
    let exactCount = 0;
    let geCount = 0;
    for (const k1 of labels) {
      for (const k2 of labels) {
        const vp = twoAdicValuation(k1 + k2, ell);
        const vm = twoAdicValuation(k1 - k2, ell);
        if (Math.min(vp, vm) !== h + 1 || Math.max(vp, vm) < h + 2) {
          throw new Error(`Dichotomy violated for k1=${k1}, k2=${k2}`);
        }
        exactCount += 1;
        geCount += 1;
      }
    }
    if (
      exactCount !== row.exact_h_plus_1_branch_outcomes ||
      geCount !== row.ge_h_plus_2_branch_outcomes ||
      row.exact_h_plus_1_branch_fraction !== "1/2" ||
      row.ge_h_plus_2_branch_fraction !== "1/2"
    ) {
      throw new Error(`Dichotomy branch counts mismatch at ell=${ell}, h=${h}`);
    }
    dichotomyChecked += 1;
  }

  let visChecked = 0;
  for (const row of report.sieve_depth_visibility_threshold_audit) {
    const v0 = parseFrac(row.v0_fraction);
    for (const dp of row.depth_profiles) {
      const d = dp.sieve_depth_d;
      const leaves = 1 << d;
      const vdNum = powBigInt(v0.num, leaves);
      const vdDen = powBigInt(v0.den, leaves);
      const vdStr = formatFrac(vdNum, vdDen);
      if (vdStr !== dp.visibility_v_d_fraction || dp.min_guaranteed_2_adic_valuation !== d) {
        throw new Error(`Visibility profile mismatch at d=${d}`);
      }
    }
    visChecked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        demodulation_wire_sizes_verified: demodChecked,
        cnot_dichotomy_strata_verified: dichotomyChecked,
        sieve_visibility_profiles_verified: visChecked,
      },
      null,
      2
    )
  );
}

main();

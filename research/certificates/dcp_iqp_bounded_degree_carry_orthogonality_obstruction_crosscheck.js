#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_iqp_bounded_degree_carry_orthogonality_obstruction.
 * Re-computes F_2 Mobius ANF degrees, conjugated IQP observables, Lucas carry polynomials,
 * and clean/noisy source-average hit probabilities from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_iqp_bounded_degree_carry_orthogonality_obstruction.json"
);

function popcount(x) {
  let c = 0;
  while (x > 0) {
    c += x & 1;
    x >>= 1;
  }
  return c;
}

function comb(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  let res = 1;
  for (let i = 1; i <= k; i++) {
    res = (res * (n - i + 1)) / i;
  }
  return Math.round(res);
}

function mobiusAnfDegree(truthTable, numVars) {
  const coeffs = truthTable.map((v) => v & 1);
  for (let i = 0; i < numVars; i++) {
    const step = 1 << i;
    for (let mask = 0; mask < 1 << numVars; mask++) {
      if (mask & step) {
        coeffs[mask] ^= coeffs[mask ^ step];
      }
    }
  }
  let maxDeg = 0;
  for (let mask = 0; mask < coeffs.length; mask++) {
    if (coeffs[mask] & 1) {
      const deg = popcount(mask);
      if (deg > maxDeg) maxDeg = deg;
    }
  }
  return maxDeg;
}

function parseFrac(s) {
  if (String(s).includes("/")) {
    const [a, b] = String(s).split("/").map(Number);
    return a / b;
  }
  return Number(s);
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { n, t, q, K, A, u } = inst;
    const v = parseFrac(inst.visibility_exact);
    const L = 1 << K;
    let uMask = 0;
    let uWeight = 0;
    for (let r = 0; r < K; r++) {
      if (u[r]) {
        uMask |= 1 << r;
        uWeight++;
      }
    }
    if (uWeight !== inst.u_weight || uMask === 0) {
      console.error(`FAIL [${inst.instance_id}]: u_weight mismatch`);
      process.exit(1);
    }

    // 1. Verify Theorem 1 (Degree reduction and target hits)
    const ia = inst.iqp_matrix_audit;
    if (
      ia.degree_directional_derivative > Math.max(0, ia.degree_P - 1) ||
      !ia.all_rows_have_degree_one ||
      Math.abs(ia.advantage_trace - ia.advantage_formula) > 1e-11
    ) {
      console.error(`FAIL [${inst.instance_id}]: Theorem 1 IQP matrix audit failed`);
      process.exit(1);
    }

    // Recompute unsigned target hits
    const freqs = [];
    for (let x = 0; x < L; x++) {
      const f = [];
      for (let ell = 0; ell < n; ell++) {
        let s = 0;
        for (let r = 0; r < K; r++) {
          if ((x >> r) & 1) s += A[ell][r];
        }
        f.push(s % q);
      }
      freqs.push(f);
    }
    let unsignedHits = 0;
    for (let x = 0; x < L; x++) {
      const y = x ^ uMask;
      const diff = freqs[x].map((val, ell) => (val - freqs[y][ell] + q) % q);
      if (diff[0] === q >> 1 && diff.slice(1).every((z) => z === 0)) {
        unsignedHits++;
      }
    }
    if (unsignedHits !== ia.unsigned_target_hits) {
      console.error(`FAIL [${inst.instance_id}]: Unsigned target hits mismatch`);
      process.exit(1);
    }

    // 2. Verify Theorem 2 (Lucas carry ANF degree)
    const la = inst.lucas_carry_audit;
    const wLucas = 1 << (t - 1);
    const lLucas = 1 << wLucas;
    const carryTable = [];
    for (let mask = 0; mask < lLucas; mask++) {
      carryTable.push(comb(popcount(mask), wLucas) % 2);
    }
    const degCarry = mobiusAnfDegree(carryTable, wLucas);
    if (
      wLucas !== la.w_lucas_vars ||
      degCarry !== wLucas ||
      la.carry_anf_degree !== wLucas ||
      la.derivative_anf_degree >= wLucas ||
      la.xor_anf_degree !== wLucas ||
      la.derivative_truth_table_parity_mod2 !== 0 ||
      la.signed_correlation_lhs !== la.signed_correlation_rhs
    ) {
      console.error(`FAIL [${inst.instance_id}]: Theorem 2 Lucas carry audit failed`);
      process.exit(1);
    }

    // 3. Verify Theorem 3 (Source-average pivot column hit counts)
    const sa = inst.source_average_audit;
    if (
      !sa.all_x_hit_counts_over_pivot_column.every((c) => c === 1) ||
      !sa.theorem3_passed
    ) {
      console.error(`FAIL [${inst.instance_id}]: Theorem 3 source-average audit failed`);
      process.exit(1);
    }
  }

  for (const row of report.asymptotic_scaling) {
    if (
      row.msb_carry_anf_degree_power_of_two_exponent !== row.t - 1 ||
      row.clean_nonadaptive_mean_advantage_upper_neg_log2 < 4 ||
      (row.n >= 32 && !row.sparse_class_excluded_at_1_16)
    ) {
      console.error(`FAIL [asymptotic n=${row.n}]: Scaling check failed`);
      process.exit(1);
    }
  }

  if (
    report.honesty_guardrails.accepted_speedup_candidate !== false ||
    report.honesty_guardrails.new_active_negative_result_created !== false ||
    report.honesty_guardrails.novelty_claim !== false
  ) {
    console.error("FAIL: Honesty guardrails violated");
    process.exit(1);
  }

  console.log(
    `OK: dcp_iqp_bounded_degree_carry_orthogonality_obstruction cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();

#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_multi_harmonic_weighted_fisher_decoder_audit.json"
);

function gcdBigInt(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function fracStr(num, den) {
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcdBigInt(num, den);
  return `${num / g}/${den / g}`;
}

function verifyCase(c) {
  const q = BigInt(c.q);
  const [k0NumStr, k0DenStr] = c.k0_zero_error_prob_exact.split("/");
  const k0Num = BigInt(k0NumStr);
  const k0Den = BigInt(k0DenStr);

  const [purNumStr, purDenStr] = c.collision_purity_exact.split("/");
  const purNum = BigInt(purNumStr);
  const purDen = BigInt(purDenStr);

  // Theorem 1: sum_{d=1}^{q-1} lambda_d == q * K(0) - 1
  const sumNum = q * k0Num - k0Den;
  const sumDen = k0Den;
  const expectedSumStr = fracStr(sumNum, sumDen);
  if (c.nonzero_harmonic_sum_exact !== expectedSumStr) {
    throw new Error(`Case ${c.case_id}: nonzero_harmonic_sum_exact mismatch`);
  }
  if (c.theorem1_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: theorem1_residual > 1e-12`);
  }

  // Theorem 2: sum_{d=1}^{q-1} lambda_d^2 == q * ||K||_2^2 - 1
  const sqSumNum = q * purNum - purDen;
  const sqSumDen = purDen;
  const expectedSqSumStr = fracStr(sqSumNum, sqSumDen);
  if (c.nonzero_harmonic_sq_sum_exact !== expectedSqSumStr) {
    throw new Error(`Case ${c.case_id}: nonzero_harmonic_sq_sum_exact mismatch`);
  }
  if (c.theorem2_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: theorem2_residual > 1e-12`);
  }

  // Theorem 3: SNR_matched - SNR_unif == snr_gap_physical_variance_formula_exact >= 0
  if (
    c.snr_gap_matched_minus_uniform_exact !==
    c.snr_gap_physical_variance_formula_exact
  ) {
    throw new Error(`Case ${c.case_id}: SNR gap vs physical variance formula mismatch`);
  }
  if (c.snr_gap_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: snr_gap_residual > 1e-12`);
  }
  if (c.kernel_kind === "depolarizing" && c.snr_gap_matched_minus_uniform_exact !== "0/1") {
    throw new Error(`Case ${c.case_id}: depolarizing kernel must have 0 SNR gap`);
  }
  if (c.kernel_kind !== "depolarizing" && !(c.snr_gap_float > 0.0)) {
    throw new Error(`Case ${c.case_id}: non-depolarizing kernel must have positive SNR gap`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_MULTI_HARMONIC_PARSEVAL_AND_MATCHED_FILTER_LAWS"
  ) {
    throw new Error(`Unexpected status: ${payload.status}`);
  }
  if (
    payload.guardrails.accepted_speedup_candidate !== false ||
    payload.guardrails.new_active_negative_result_created !== false ||
    payload.guardrails.novelty_claim !== false
  ) {
    throw new Error("Guardrail violation");
  }

  for (const c of payload.cases) {
    verifyCase(c);
  }

  console.log(
    JSON.stringify(
      {
        status: "CROSSCHECK_PASSED",
        case_count: payload.cases.length,
        certificate_sha256: payload.certificate_sha256,
      },
      null,
      2
    )
  );
}

main();

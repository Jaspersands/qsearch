#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_kronecker_moment_rank_bridge.json"
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
  const g = gcdBigInt(num, den);
  return `${num / g}/${den / g}`;
}

function verifyCase(c) {
  const D = c.D;
  const k = c.k_calls;

  if (c.mean_vs_c0_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: mean_vs_c0_residual too large`);
  }
  if (c.var_vs_parseval_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: var_vs_parseval_residual too large`);
  }
  if (c.max_conjugate_symmetry_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: conjugate symmetry residual too large`);
  }
  if (c.max_nonzero_outcome_sum_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: non-zero outcome sum residual too large`);
  }

  let l2Sum = 0.0;
  for (let x = 0; x < D; x++) {
    if (Math.abs(c.empirical_var_probs[x] - c.parseval_var_probs[x]) > 1e-12) {
      throw new Error(`Case ${c.case_id}, x=${x}: empirical vs parseval var mismatch`);
    }
    l2Sum += c.parseval_var_probs[x];
  }
  if (Math.abs(l2Sum - c.total_l2_signal_energy) > 1e-12) {
    throw new Error(`Case ${c.case_id}: total_l2_signal_energy mismatch`);
  }

  const denom = BigInt(D) ** BigInt(2 * k + 1);
  const expectedBoundStr = fracStr(BigInt(c.off_zero_kronecker_4tuple_count), denom);
  if (c.kronecker_l2_upper_bound_exact !== expectedBoundStr) {
    throw new Error(`Case ${c.case_id}: kronecker_l2_upper_bound_exact mismatch`);
  }
  if (c.total_l2_signal_energy > c.kronecker_l2_upper_bound_float + 1e-12) {
    throw new Error(`Case ${c.case_id}: Theorem 3 Kronecker upper bound violated`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_KRONECKER_SECOND_MOMENT_PARSEVAL_IDENTITIES"
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

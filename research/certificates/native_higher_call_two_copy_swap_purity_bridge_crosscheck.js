#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_two_copy_swap_purity_bridge.json"
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

  if (Math.abs(c.swap_same_secret_expectation - 1.0) > 1e-12) {
    throw new Error(`Case ${c.case_id}: swap_same_secret_expectation != 1`);
  }
  if (Math.abs(c.swap_independent_secret_expectation - c.purity_rho_bar) > 1e-12) {
    throw new Error(`Case ${c.case_id}: swap_independent != purity_rho_bar`);
  }
  if (Math.abs(c.swap_expectation_excess - c.v_hs_operator_variance) > 1e-12) {
    throw new Error(`Case ${c.case_id}: swap_expectation_excess != v_hs`);
  }
  if (Math.abs(c.antisymmetric_independent_prob - 0.5 * c.v_hs_operator_variance) > 1e-12) {
    throw new Error(`Case ${c.case_id}: antisymmetric_independent_prob != v_hs/2`);
  }
  if (c.sigma_k_flip_purity_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: sigma_k_flip_purity_residual > 1e-12`);
  }

  if (k === 1) {
    const expectedK1Str = fracStr(BigInt(c.variety_size_V_epsilon), BigInt(D * D));
    if (c.k1_rational_purity_exact !== expectedK1Str) {
      throw new Error(`Case ${c.case_id}: k1_rational_purity_exact mismatch`);
    }
  }

  if (c.cnot_autocorrelation_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: cnot_autocorrelation_residual > 1e-12`);
  }
  if (c.coincidence_excess_vs_l2_energy_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: coincidence_excess_vs_l2_energy_residual > 1e-12`);
  }
  if (c.coincidence_excess_Delta0 > c.v_hs_operator_variance + 1e-12) {
    throw new Error(`Case ${c.case_id}: coincidence_excess_Delta0 > v_hs`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_TWO_COPY_SWAP_PURITY_AND_CNOT_COINCIDENCE_LAWS"
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

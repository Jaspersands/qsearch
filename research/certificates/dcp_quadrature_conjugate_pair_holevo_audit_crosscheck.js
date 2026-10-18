#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_quadrature_conjugate_pair_holevo_audit.json"
);

function binaryEntropyBits(p) {
  if (p <= 0.0 || p >= 1.0) return 0.0;
  return -(p * Math.log2(p) + (1.0 - p) * Math.log2(1.0 - p));
}

function verifyCase(c) {
  const q = c.q;
  const pErr = c.p_err;
  const dDiff = c.d_diff;

  const expectedLambdaD =
    1.0 - pErr + pErr * Math.cos((2.0 * Math.PI * dDiff) / q);
  if (Math.abs(c.lambda_d - expectedLambdaD) > 1e-12) {
    throw new Error(`Case ${c.case_id}: lambda_d mismatch`);
  }

  const pPlus = 0.5 * (1.0 + Math.abs(expectedLambdaD));
  const expectedHolevo = 1.0 - binaryEntropyBits(pPlus);
  if (Math.abs(c.holevo_capacity_empirical_bits - expectedHolevo) > 1e-12) {
    throw new Error(`Case ${c.case_id}: Holevo capacity mismatch`);
  }

  const lamSq = expectedLambdaD * expectedLambdaD;
  if (Math.abs(c.sld_quantum_fisher_info - lamSq) > 1e-12) {
    throw new Error(`Case ${c.case_id}: SLD QFI mismatch`);
  }

  const minXY = 0.5 * lamSq;
  const maxXY = lamSq / (2.0 - lamSq);
  if (Math.abs(c.min_conjugate_xy_fisher_info - minXY) > 1e-12) {
    throw new Error(`Case ${c.case_id}: min_conjugate_xy_fisher_info mismatch`);
  }
  if (Math.abs(c.max_conjugate_xy_fisher_info - maxXY) > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_conjugate_xy_fisher_info mismatch`);
  }

  const singProb = 0.25 * (1.0 - lamSq);
  const tripProb = 0.25 * (3.0 + lamSq);
  if (Math.abs(c.singlet_probability_constant - singProb) > 1e-12) {
    throw new Error(`Case ${c.case_id}: singlet_probability_constant mismatch`);
  }
  if (Math.abs(c.triplet_probability_constant - tripProb) > 1e-12) {
    throw new Error(`Case ${c.case_id}: triplet_probability_constant mismatch`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_BLOCH_DISK_HOLEVO_AND_CONJUGATE_FISHER_LAWS"
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

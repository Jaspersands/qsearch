#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_secret_subspace_restriction_audit.json"
);

function verifyCase(c) {
  if (c.projected_variety_size < c.full_variety_size) {
    throw new Error(
      `Case ${c.case_id}: projected_variety_size < full_variety_size`
    );
  }
  if (c.theorem1_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: theorem1_residual > 1e-12`);
  }
  if (c.theorem2_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: theorem2_residual > 1e-12`);
  }
  if (
    c.between_var_residual > 1e-12 ||
    c.within_var_residual > 1e-12 ||
    c.total_var_decomp_residual > 1e-12
  ) {
    throw new Error(`Case ${c.case_id}: Theorem 3 residual > 1e-12`);
  }

  const sumVar =
    c.between_coset_l2_variance + c.expected_within_coset_l2_variance;
  if (Math.abs(sumVar - c.total_l2_variance) > 1e-12) {
    throw new Error(
      `Case ${c.case_id}: between + within variance != total_l2_variance`
    );
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_SECRET_SUBSPACE_PINCHING_AND_TOTAL_VARIANCE_PARTITION"
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

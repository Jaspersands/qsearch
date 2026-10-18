#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_multiproduct_k_copy_dual_tensor_bridge.json"
);

function verifyCase(c) {
  const q = c.q;
  const dualDim = c.dual_dim_n_minus_d;
  const mDual = Math.pow(q, dualDim);

  if (c.num_cosets_q_pow_n_minus_d !== mDual) {
    throw new Error(`Case ${c.case_id}: num_cosets mismatch`);
  }
  if (c.theorem1_disentanglement_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: Theorem 1 residual > 1e-12`);
  }

  for (const row of c.k_rows) {
    const K = row.K_copies;
    const expectedDimK = Math.pow(mDual, K);
    const expectedFiberSize = Math.pow(mDual, K - 1);

    if (row.dual_tensor_dimension !== expectedDimK) {
      throw new Error(`Case ${c.case_id}, K=${K}: dual_tensor_dimension mismatch`);
    }
    if (
      row.distinct_sum_fibers !== mDual ||
      row.each_fiber_cardinality !== expectedFiberSize
    ) {
      throw new Error(`Case ${c.case_id}, K=${K}: fiber count/cardinality mismatch`);
    }
    if (row.observed_rank !== mDual) {
      throw new Error(`Case ${c.case_id}, K=${K}: observed_rank != q^(n-d)`);
    }
    if (row.purity_exact !== `1/${mDual}`) {
      throw new Error(`Case ${c.case_id}, K=${K}: purity_exact != 1/q^(n-d)`);
    }
    if (Math.abs(row.purity_empirical - 1.0 / mDual) > 1e-12) {
      throw new Error(`Case ${c.case_id}, K=${K}: purity_empirical mismatch`);
    }
    if (row.spectral_decomposition_residual > 1e-12) {
      throw new Error(`Case ${c.case_id}, K=${K}: spectral_decomposition_residual > 1e-12`);
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_K_COPY_DUAL_TENSOR_AND_PURITY_INVARIANCE_LAWS"
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

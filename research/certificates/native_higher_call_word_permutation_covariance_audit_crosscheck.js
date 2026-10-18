#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_word_permutation_covariance_audit.json"
);

function verifyCase(c) {
  const D = c.D;
  const k = c.k_calls;
  const m = c.m_unit;
  const mInv = c.m_inv;
  const isInv = (m * m) % D === 1;

  if ((m * mInv) % D !== 1) {
    throw new Error(`Case ${c.case_id}: m * m_inv !== 1 mod D`);
  }
  if (c.is_involutive_m_sq_eq_1 !== isInv) {
    throw new Error(`Case ${c.case_id}: involutive flag mismatch`);
  }
  if (
    c.variety_size_orig !== c.variety_size_dilated ||
    c.variety_size_orig !== c.variety_size_shifted
  ) {
    throw new Error(`Case ${c.case_id}: variety size not invariant under permutation`);
  }
  if (c.intertwine_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: intertwine_residual > 1e-12`);
  }
  if (c.max_alternating_intertwine_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_alternating_intertwine_residual > 1e-12`);
  }

  if (isInv || k === 1) {
    if (
      c.max_involutive_or_k1_dilation_residual > 1e-12 ||
      c.max_uniform_dilation_ordered_tv > 1e-12
    ) {
      throw new Error(`Case ${c.case_id}: involutive/k1 dilation invariance failed`);
    }
  } else {
    if (!(c.max_uniform_dilation_ordered_tv > 1e-4)) {
      throw new Error(`Case ${c.case_id}: expected non-involutive k>=2 symmetry breaking`);
    }
  }

  if (k === 1) {
    if (c.max_shift_born_tv > 1e-12) {
      throw new Error(`Case ${c.case_id}: k=1 shift Born invariance failed`);
    }
  } else if (c.shift_b % D !== 0) {
    if (!(c.max_shift_born_tv > 1e-4)) {
      throw new Error(`Case ${c.case_id}: expected k>=2 shift symmetry breaking`);
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_WORD_PERMUTATION_COVARIANCE_AND_ALTERNATING_RESCUE"
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

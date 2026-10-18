#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_subset_sum_modular_collision_entropy_audit.json"
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
  const q = BigInt(c.q);
  const m = BigInt(c.m);
  const twoPowM = 2n ** m;

  if (c.max_cosine_formula_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_cosine_formula_residual > 1e-12`);
  }
  if (c.max_single_coord_cos_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_single_coord_cos_residual > 1e-12`);
  }
  if (!c.pairwise_boolean_difference_surjective) {
    throw new Error(`Case ${c.case_id}: pairwise_boolean_difference_surjective is false`);
  }

  // Mean collision prob: 1/q + (1 - 1/q) * 2^{-m} = (2^m + q - 1) / (q * 2^m)
  const expectedCollStr = fracStr(twoPowM + q - 1n, q * twoPowM);
  if (c.mean_collision_probability_exact !== expectedCollStr) {
    throw new Error(
      `Case ${c.case_id}: mean_collision_probability_exact mismatch (${c.mean_collision_probability_exact} vs ${expectedCollStr})`
    );
  }

  // Mean off-diagonal collision prob: (2^m - 1) / (q * 2^m)
  const expectedOffStr = fracStr(twoPowM - 1n, q * twoPowM);
  if (c.mean_off_diagonal_collision_exact !== expectedOffStr) {
    throw new Error(`Case ${c.case_id}: mean_off_diagonal_collision_exact mismatch`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_SUBSET_SUM_COLLISION_AND_BOOLEAN_SURJECTIVITY_LAWS"
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

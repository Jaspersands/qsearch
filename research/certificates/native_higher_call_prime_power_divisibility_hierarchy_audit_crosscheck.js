#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_prime_power_divisibility_hierarchy_audit.json"
);

function verifyCase(c) {
  const D = c.D;
  const k = c.k_calls;
  const r = c.r;
  const numTraj = Math.pow(D, k);

  // Verify Theorem 1 residuals
  if (c.max_theorem1_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_theorem1_residual too large`);
  }

  // Verify Theorem 2 monotone filtration and telescoping counts
  const vSizes = c.variety_sizes_by_level;
  if (vSizes[0] !== numTraj * numTraj) {
    throw new Error(`Case ${c.case_id}: V^(0) size must be D^(2k)`);
  }
  for (let j = 0; j < r; j++) {
    if (vSizes[j] < vSizes[j + 1]) {
      throw new Error(`Case ${c.case_id}: non-monotone variety size at j=${j}`);
    }
  }
  if (vSizes[r] < numTraj) {
    throw new Error(`Case ${c.case_id}: V^(r) size < D^k`);
  }

  let shellSum = 0;
  for (let j = 0; j < r; j++) {
    const sRow = c.shell_rows[j];
    const expectedDiff = vSizes[j] - vSizes[j + 1];
    if (sRow.shell_pair_count !== expectedDiff) {
      throw new Error(`Case ${c.case_id}, j=${j}: shell pair count mismatch`);
    }
    if (sRow.diagonal_pairs_in_shell !== 0) {
      throw new Error(`Case ${c.case_id}, j=${j}: diagonal pairs in shell != 0`);
    }
    shellSum += sRow.shell_pair_count;

    // Verify Theorem 3 zero-sum shell increments and level difference match
    let sumOverX = 0.0;
    const pJ = c.level_rows[j].pinched_variety_probs;
    const pJ1 = c.level_rows[j + 1].pinched_variety_probs;
    for (let x = 0; x < D; x++) {
      const inc = sRow.shell_increment_probs[x];
      sumOverX += inc;
      if (Math.abs(inc - (pJ[x] - pJ1[x])) > 1e-12) {
        throw new Error(
          `Case ${c.case_id}, j=${j}, x=${x}: shell increment != P^(j) - P^(j+1)`
        );
      }
    }
    if (Math.abs(sumOverX) > 1e-12) {
      throw new Error(`Case ${c.case_id}, j=${j}: shell increment sum over x != 0`);
    }
  }

  if (vSizes[r] + shellSum !== numTraj * numTraj) {
    throw new Error(`Case ${c.case_id}: telescoping count sum mismatch`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_PRIME_POWER_DIVISIBILITY_PINCHING_HIERARCHY"
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

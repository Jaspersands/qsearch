#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_pgm_fidelity_window_threshold_audit.json"
);

function convolvePower(profile, K) {
  const q = profile.length;
  let cur = new Array(q).fill(0.0);
  cur[0] = 1.0;
  for (let s = 0; s < K; s++) {
    const nxt = new Array(q).fill(0.0);
    for (let a = 0; a < q; a++) {
      if (cur[a] === 0.0) continue;
      for (let b = 0; b < q; b++) {
        if (profile[b] === 0.0) continue;
        nxt[(a + b) % q] += cur[a] * profile[b];
      }
    }
    cur = nxt;
  }
  return cur;
}

function verifyCase(c) {
  const q = c.q;
  const R = c.R;
  const profile = c.base_profile;

  for (const row of c.k_rows) {
    const K = row.K_copies;
    const wK = convolvePower(profile, K);
    let sqrtSum = 0.0;
    let suppCount = 0;
    for (let m = 0; m < q; m++) {
      if (wK[m] > 1e-15) {
        suppCount++;
        sqrtSum += Math.sqrt(wK[m]);
      }
    }
    const pBhat = (sqrtSum * sqrtSum) / q;
    const expectedSupp = Math.min(q, K * (R - 1) + 1);
    const upperBound = expectedSupp / q;

    if (suppCount !== expectedSupp) {
      throw new Error(
        `Case ${c.case_id}, K=${K}: support count mismatch (${suppCount} vs ${expectedSupp})`
      );
    }
    if (Math.abs(pBhat - row.pgm_success_bhattacharyya_convolution) > 1e-12) {
      throw new Error(`Case ${c.case_id}, K=${K}: Bhattacharyya value mismatch`);
    }
    if (Math.abs(row.pgm_success_gram_operator - pBhat) > 1e-12) {
      throw new Error(`Case ${c.case_id}, K=${K}: Gram vs Bhattacharyya mismatch`);
    }
    if (pBhat > upperBound + 1e-12) {
      throw new Error(`Case ${c.case_id}, K=${K}: support upper bound violated`);
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_PGM_BHATTACHARYYA_WINDOW_THRESHOLD_LAWS"
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

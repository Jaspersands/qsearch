#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_noisy_tree_merge_error_propagation_audit.json"
);

function buildKernel(q, pErr) {
  const kernel = new Array(q).fill(0.0);
  kernel[0] = 1.0 - pErr;
  kernel[1 % q] += 0.5 * pErr;
  kernel[(q - 1) % q] += 0.5 * pErr;
  return kernel;
}

function convolvePower(kernel, kLeaves) {
  const q = kernel.length;
  let cur = new Array(q).fill(0.0);
  cur[0] = 1.0;
  for (let s = 0; s < kLeaves; s++) {
    const nxt = new Array(q).fill(0.0);
    for (let a = 0; a < q; a++) {
      if (cur[a] === 0.0) continue;
      for (let b = 0; b < q; b++) {
        if (kernel[b] === 0.0) continue;
        nxt[(a + b) % q] += cur[a] * kernel[b];
      }
    }
    cur = nxt;
  }
  return cur;
}

function firstHarmonic(dist) {
  const q = dist.length;
  let sum = 0.0;
  for (let e = 0; e < q; e++) {
    sum += dist[e] * Math.cos((2.0 * Math.PI * e) / q);
  }
  return sum;
}

function verifyCase(c) {
  const q = c.q;
  const pErr = c.p_err;
  const kernel = buildKernel(q, pErr);
  const lambda1 = firstHarmonic(kernel);

  if (Math.abs(lambda1 - c.single_leaf_lambda_1) > 1e-12) {
    throw new Error(`Case ${c.case_id}: single_leaf_lambda_1 mismatch`);
  }

  for (const row of c.depth_rows) {
    const L = row.depth_L;
    const K = 1 << L;
    if (row.k_leaves !== K) {
      throw new Error(`Case ${c.case_id}: k_leaves mismatch at L=${L}`);
    }
    const conv = convolvePower(kernel, K);
    const empVis = firstHarmonic(conv);
    const theoVis = Math.pow(lambda1, K);

    if (Math.abs(empVis - theoVis) > 1e-12) {
      throw new Error(`Case ${c.case_id}, L=${L}: convolution vs power mismatch`);
    }
    if (Math.abs(empVis - row.root_fundamental_visibility_empirical) > 1e-12) {
      throw new Error(`Case ${c.case_id}, L=${L}: empirical visibility mismatch`);
    }

    const snrLeaf = K * lambda1 * lambda1;
    const snrRoot = Math.pow(lambda1, 2 * K);
    const ratio = snrRoot / snrLeaf;
    const formulaRatio = Math.pow(2.0, -L) * Math.pow(lambda1, 2 * (K - 1));

    if (Math.abs(ratio - formulaRatio) > 1e-12) {
      throw new Error(`Case ${c.case_id}, L=${L}: SNR ratio formula mismatch`);
    }
    if (L >= 1 && !(ratio <= Math.pow(2.0, -L) + 1e-12 && ratio < 1.0)) {
      throw new Error(`Case ${c.case_id}, L=${L}: Theorem 3 SNR dominance violated`);
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_NOISY_TREE_MERGE_CONVOLUTION_AND_SNR_CROSSOVER"
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

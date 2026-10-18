#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_two_copy_cnot_difference_alignment_audit.json"
);

function verifyCase(c) {
  const q = c.q;
  const pErr = c.p_err;

  if (c.max_prob_half_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_prob_half_residual > 1e-12`);
  }
  if (c.max_branch_state_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_branch_state_residual > 1e-12`);
  }
  if (!c.diagonal_z1_annihilation_holds || !c.antidiagonal_z0_annihilation_holds) {
    throw new Error(`Case ${c.case_id}: Theorem 2 annihilation check failed`);
  }

  const lambdas = [];
  let sumSq = 0.0;
  let sumFourth = 0.0;
  for (let d = 1; d < q; d++) {
    const lam = 1.0 - pErr + pErr * Math.cos((2.0 * Math.PI * d) / q);
    lambdas.push(lam);
    sumSq += lam * lam;
    sumFourth += Math.pow(lam, 4);
  }

  const purity = Math.pow(1.0 - pErr, 2) + 0.5 * pErr * pErr;
  const parsevalSq = q * purity - 1.0;
  if (Math.abs(sumSq - parsevalSq) > 1e-12) {
    throw new Error(`Case ${c.case_id}: Parseval sumSq mismatch`);
  }

  const totalPairs = (q - 1) * (q - 1);
  const expectedYield = (parsevalSq * parsevalSq - sumFourth) / totalPairs;
  if (Math.abs(c.empirical_ensemble_active_yield - expectedYield) > 1e-12) {
    throw new Error(`Case ${c.case_id}: empirical_ensemble_active_yield mismatch`);
  }
  if (Math.abs(c.off_diagonal_pair_ensemble_yield - expectedYield) > 1e-12) {
    throw new Error(`Case ${c.case_id}: off_diagonal_pair_ensemble_yield mismatch`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_TWO_COPY_CNOT_BIFURCATION_AND_YIELD_LAWS"
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

#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_punctured_coordinate_projection_bridge.json"
);

function verifyCase(c) {
  const q = c.q;
  const d = c.d;
  const m = c.m_kept;
  const t = c.t_punctured;
  const dJ = c.punctured_rank_d_J;
  const dJBar = c.complement_rank_d_J_bar;
  const kJ = c.shortened_dim_k_J;

  if (kJ !== d - dJBar) {
    throw new Error(`Case ${c.case_id}: k_J != d - d_{J_bar}`);
  }

  const schmidtExp = dJ + dJBar - d;
  const expectedRank = Math.pow(q, schmidtExp);
  if (c.reduced_state_rank !== expectedRank) {
    throw new Error(`Case ${c.case_id}: reduced_state_rank mismatch`);
  }
  if (c.reduced_state_purity_exact !== `1/${expectedRank}`) {
    throw new Error(`Case ${c.case_id}: reduced_state_purity_exact mismatch`);
  }
  if (Math.abs(c.reduced_state_purity_float - 1.0 / expectedRank) > 1e-12) {
    throw new Error(`Case ${c.case_id}: reduced_state_purity_float mismatch`);
  }

  if (c.shortened_dual_size !== Math.pow(q, m - dJ)) {
    throw new Error(`Case ${c.case_id}: shortened_dual_size mismatch`);
  }
  if (c.punctured_dual_size !== Math.pow(q, m - kJ)) {
    throw new Error(`Case ${c.case_id}: punctured_dual_size mismatch`);
  }
  if (
    c.j_supported_probe_variance_exact !==
    c.theoretical_j_supported_variance_exact
  ) {
    throw new Error(`Case ${c.case_id}: j_supported_probe_variance_exact mismatch`);
  }

  if (t < c.primal_minimum_distance_d_min && dJ !== d) {
    throw new Error(`Case ${c.case_id}: d_min rank-locking violated`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_PUNCTURED_PROJECTION_AND_RANK_LOCKING_LAWS"
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

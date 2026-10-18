#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_error_table_gauge_invariance_audit.json"
);

function verifyCase(c) {
  const D = c.D;
  const k = c.k_calls;
  const numTraj = Math.pow(D, k);

  if (c.max_shift_covariance_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_shift_covariance_residual > 1e-12`);
  }
  if (c.gauge_rho_bar_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: gauge_rho_bar_residual > 1e-12`);
  }
  if (c.gauge_l2_energy_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: gauge_l2_energy_residual > 1e-12`);
  }
  if (c.gauge_v_hs_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: gauge_v_hs_residual > 1e-12`);
  }

  // Theorem 2: injective check
  if (c.tau_is_injective && c.max_injective_purity_deficit_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: injective purity deficit residual > 1e-12`);
  }

  // Theorem 3: subvariety inclusion and universal error-averaged distribution
  if (!c.subvariety_inclusion_W_subseteq_V) {
    throw new Error(`Case ${c.case_id}: W_epsilon not a subset of V_epsilon`);
  }
  if (
    c.word_multiplicity_variety_size_W_epsilon < numTraj ||
    c.word_multiplicity_variety_size_W_epsilon > c.frequency_collision_variety_size_V_f1 ||
    c.word_multiplicity_variety_size_W_epsilon > c.frequency_collision_variety_size_V_f2
  ) {
    throw new Error(`Case ${c.case_id}: variety cardinality inequality violated`);
  }

  for (let x = 0; x < D; x++) {
    const pw = c.universal_W_epsilon_probs[x];
    const pf1 = c.error_averaged_probs_f1[x];
    const pf2 = c.error_averaged_probs_f2[x];
    if (Math.abs(pw - pf1) > 1e-12 || Math.abs(pw - pf2) > 1e-12) {
      throw new Error(
        `Case ${c.case_id}, x=${x}: error-averaged probs do not match universal W_epsilon formula`
      );
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_ERROR_GAUGE_COVARIANCE_AND_WORD_MULTIPLICITY_PINCHING"
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

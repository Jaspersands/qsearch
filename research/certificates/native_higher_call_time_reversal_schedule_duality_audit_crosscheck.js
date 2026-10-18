#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_time_reversal_schedule_duality_audit.json"
);

function verifyCase(c) {
  const k = c.k_calls;
  const expectedTotal = Math.pow(4, k);
  const expectedOrbits = Math.pow(4, k - 1);

  if (c.total_schedules_4_pow_k !== expectedTotal) {
    throw new Error(`Case ${c.case_id}: total_schedules_4_pow_k mismatch`);
  }
  if (c.klein_four_orbit_count_4_pow_k_minus_1 !== expectedOrbits) {
    throw new Error(`Case ${c.case_id}: orbit count mismatch`);
  }
  if (c.max_conj_state_residual > 1e-12 || c.max_conj_born_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: Theorem 1 conjugation residual > 1e-12`);
  }
  if (
    c.max_reflection_born_residual > 1e-12 ||
    c.max_orbit_l2_energy_spread > 1e-12 ||
    c.max_orbit_v_hs_spread > 1e-12
  ) {
    throw new Error(`Case ${c.case_id}: Theorem 2 Klein four-group residual > 1e-12`);
  }
  if (
    c.max_time_reversal_amp0_residual > 1e-12 ||
    c.max_time_reversal_prob0_residual > 1e-12
  ) {
    throw new Error(`Case ${c.case_id}: Theorem 3 time-reversal residual > 1e-12`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_KLEIN_FOUR_AND_TIME_REVERSAL_SCHEDULE_DUALITIES"
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

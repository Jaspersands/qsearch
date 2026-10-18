#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_cyclic_subgroup_quotient_aliasing_audit.json"
);

function gcd(a, b) {
  while (b !== 0) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function eulerTotient(m) {
  let cnt = 0;
  for (let u = 1; u <= m; u++) {
    if (gcd(u, m) === 1) cnt++;
  }
  return cnt;
}

function verifyCase(c) {
  const q = c.q;

  if (c.totient_sum_q_minus_1 !== q - 1) {
    throw new Error(`Case ${c.case_id}: totient_sum != q - 1`);
  }
  if (c.max_coset_periodicity_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_coset_periodicity_residual > 1e-12`);
  }
  if (c.max_folded_visibility_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_folded_visibility_residual > 1e-12`);
  }
  if (c.max_ramanujan_stratum_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_ramanujan_stratum_residual > 1e-12`);
  }
  if (c.max_subgroup_parseval_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_subgroup_parseval_residual > 1e-12`);
  }
  if (!c.monotone_purity_holds) {
    throw new Error(`Case ${c.case_id}: monotone_purity_holds is false`);
  }

  let phiSum = 0;
  for (const row of c.divisor_rows) {
    const g = row.divisor_g;
    const m = row.quotient_order_m;
    if (g * m !== q) {
      throw new Error(`Case ${c.case_id}: g * m !== q`);
    }
    const expectedPhi = eulerTotient(m);
    if (row.stratum_size_phi_m !== expectedPhi) {
      throw new Error(`Case ${c.case_id}, g=${g}: stratum_size_phi_m mismatch`);
    }
    phiSum += expectedPhi;
    if (Math.abs(row.folded_purity_float - row.subgroup_parseval_float) > 1e-12) {
      throw new Error(`Case ${c.case_id}, g=${g}: folded purity vs subgroup Parseval mismatch`);
    }
    if (row.folded_purity_float + 1e-12 < c.base_purity_float) {
      throw new Error(`Case ${c.case_id}, g=${g}: folded purity < base purity`);
    }
  }
  if (phiSum !== q - 1) {
    throw new Error(`Case ${c.case_id}: phiSum !== q - 1`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_QUOTIENT_ALIASING_AND_RAMANUJAN_STRATUM_LAWS"
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

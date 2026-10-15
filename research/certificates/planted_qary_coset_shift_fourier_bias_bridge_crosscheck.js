#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_coset_shift_fourier_bias_bridge.json"
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
  const n = BigInt(c.n);
  const d = BigInt(c.d);
  const R = BigInt(c.R);
  const zeroInWindow = c.zero_in_window;
  const aInB = c.shift_a_in_B;

  if (c.max_qft_amplitude_formula_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: QFT amplitude formula residual too large`);
  }
  if (c.qft_born_tv_distance_coset_vs_subspace > 1e-12) {
    throw new Error(`Case ${c.case_id}: QFT Born TV distance > 1e-12`);
  }
  if (!c.off_dual_invariance_holds || !c.dual_collapse_holds) {
    throw new Error(`Case ${c.case_id}: Theorem 2 invariance/collapse failed`);
  }

  const expectedOffDualCount = Number((q ** (d - 1n)) * R);
  if (c.off_dual_expected_acceptance_count !== expectedOffDualCount) {
    throw new Error(`Case ${c.case_id}: off_dual_expected_acceptance_count mismatch`);
  }

  // Homogeneous first moment: 1_{0 in W} + (q^d - 1)*(R/q)
  const qPowD = q ** d;
  const homNum = (zeroInWindow ? q : 0n) + (qPowD - 1n) * R;
  const homStr = fracStr(homNum, q);
  if (c.homogeneous_first_moment_exact !== homStr) {
    throw new Error(
      `Case ${c.case_id}: homogeneous_first_moment_exact mismatch (${c.homogeneous_first_moment_exact} vs ${homStr})`
    );
  }

  // Coset first moment: equals homStr if a in B, else q^(d-1) * R
  const cosetStr = aInB ? homStr : fracStr((q ** (d - 1n)) * R, 1n);
  if (c.coset_first_moment_exact !== cosetStr) {
    throw new Error(
      `Case ${c.case_id}: coset_first_moment_exact mismatch (${c.coset_first_moment_exact} vs ${cosetStr})`
    );
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_COSET_SHIFT_FOURIER_AND_PROBE_INVARIANCE"
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

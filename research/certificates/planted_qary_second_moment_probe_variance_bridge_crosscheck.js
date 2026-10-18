#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_second_moment_probe_variance_bridge.json"
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
  const d = BigInt(c.d);
  const R = BigInt(c.R);
  const zeroInWindow = c.zero_in_window;

  const qPowD = q ** d;
  const expectedRays = Number((qPowD - 1n) / (q - 1n));
  if (c.projective_ray_count_L_d !== expectedRays) {
    throw new Error(`Case ${c.case_id}: projective_ray_count_L_d mismatch`);
  }

  // Theorem 1: Var_u[N_W(u; B)] = (q^d - 1) * (1_{0 in W} - R/q)^2
  const diffNum = (zeroInWindow ? q : 0n) - R;
  const varNum = (qPowD - 1n) * diffNum * diffNum;
  const varDen = q * q;
  const expectedVarStr = fracStr(varNum, varDen);
  if (c.subspace_variance_exact !== expectedVarStr) {
    throw new Error(
      `Case ${c.case_id}: subspace_variance_exact mismatch (${c.subspace_variance_exact} vs ${expectedVarStr})`
    );
  }

  // Theorem 2: sum of ray variances == subspace variance, max off-ray cov == 0
  if (c.sum_of_ray_variances_exact !== expectedVarStr) {
    throw new Error(`Case ${c.case_id}: sum_of_ray_variances_exact mismatch`);
  }
  if (c.max_off_ray_covariance_exact !== "0/1") {
    throw new Error(`Case ${c.case_id}: non-zero off-ray covariance`);
  }

  // Theorem 3: ray-free subset variance = (q^d - 1)*(R/q)*(1 - R/q)
  const sVarNum = (qPowD - 1n) * R * (q - R);
  const sVarStr = fracStr(sVarNum, varDen);
  if (c.ray_free_subset_variance_exact !== sVarStr) {
    throw new Error(`Case ${c.case_id}: ray_free_subset_variance_exact mismatch`);
  }
  if (!zeroInWindow) {
    const ratioStr = fracStr(R, q - R);
    if (c.variance_ratio_subspace_over_ray_free_exact !== ratioStr) {
      throw new Error(
        `Case ${c.case_id}: variance_ratio_subspace_over_ray_free_exact mismatch`
      );
    }
  }
  if (!c.off_dual_variance_is_zero) {
    throw new Error(`Case ${c.case_id}: off_dual_variance_is_zero must be true`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (payload.status !== "VERIFIED_EXACT_SECOND_MOMENT_PROBE_VARIANCE_LAWS") {
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

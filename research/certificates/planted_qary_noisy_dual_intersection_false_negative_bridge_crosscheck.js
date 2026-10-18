#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_noisy_dual_intersection_false_negative_bridge.json"
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
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcdBigInt(num, den);
  return `${num / g}/${den / g}`;
}

function verifyCase(c) {
  const q = BigInt(c.q);
  const n = BigInt(c.n);
  const d = BigInt(c.d);
  const m = BigInt(c.m_samples);
  const [gNumStr, gDenStr] = c.gamma_exact.split("/");
  const gNum = BigInt(gNumStr);
  const gDen = BigInt(gDenStr);

  const omgNum = gDen - gNum;
  const omgDen = gDen;
  const qPowM = q ** m;

  if (c.spurious_single_sample_survival_exact !== fracStr(1n, q)) {
    throw new Error(`Case ${c.case_id}: spurious_single_sample_survival_exact mismatch`);
  }
  if (c.spurious_m_sample_survival_exact !== fracStr(1n, qPowM)) {
    throw new Error(`Case ${c.case_id}: spurious_m_sample_survival_exact mismatch`);
  }

  const expectedSpuriousTotalStr = fracStr((q ** n) - (q ** d), qPowM);
  if (c.expected_spurious_survivors_exact !== expectedSpuriousTotalStr) {
    throw new Error(`Case ${c.case_id}: expected_spurious_survivors_exact mismatch`);
  }

  for (const s of c.planted_weight_strata) {
    const w = BigInt(s.hamming_weight);
    const charNum = omgNum ** w;
    const charDen = omgDen ** w;

    // Single-sample survival: 1/q + ((q-1)/q) * (1-gamma)^w = (charDen + (q-1)*charNum) / (q * charDen)
    const s1Num = charDen + (q - 1n) * charNum;
    const s1Den = q * charDen;
    if (s.single_sample_survival_exact !== fracStr(s1Num, s1Den)) {
      throw new Error(`Case ${c.case_id}, w=${w}: single_sample_survival_exact mismatch`);
    }

    const smNum = s1Num ** m;
    const smDen = s1Den ** m;
    if (s.m_sample_survival_exact !== fracStr(smNum, smDen)) {
      throw new Error(`Case ${c.case_id}, w=${w}: m_sample_survival_exact mismatch`);
    }

    const fnStr = fracStr(smDen - smNum, smDen);
    if (s.false_negative_prob_exact !== fnStr) {
      throw new Error(`Case ${c.case_id}, w=${w}: false_negative_prob_exact mismatch`);
    }

    const ssrNum = s1Num ** m;
    const ssrDen = charDen ** m;
    if (s.survival_to_spurious_ratio_exact !== fracStr(ssrNum, ssrDen)) {
      throw new Error(`Case ${c.case_id}, w=${w}: survival_to_spurious_ratio_exact mismatch`);
    }
  }

  const dMin = BigInt(c.primal_minimum_distance_d_min);
  const maxSsrNum = ((omgDen ** dMin) + (q - 1n) * (omgNum ** dMin)) ** m;
  const maxSsrDen = (omgDen ** dMin) ** m;
  if (c.max_nonzero_ssr_exact !== fracStr(maxSsrNum, maxSsrDen)) {
    throw new Error(`Case ${c.case_id}: max_nonzero_ssr_exact mismatch`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_NOISY_DUAL_INTERSECTION_FALSE_NEGATIVE_LAWS"
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

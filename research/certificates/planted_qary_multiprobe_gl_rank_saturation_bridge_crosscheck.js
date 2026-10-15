#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_multiprobe_gl_rank_saturation_bridge.json"
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

function qBinomialBigInt(d, r, q) {
  if (r < 0 || r > d) return 0n;
  if (r === 0 || r === d) return 1n;
  const qB = BigInt(q);
  let num = 1n;
  let den = 1n;
  for (let i = 0; i < r; i++) {
    num *= qB ** BigInt(d - i) - 1n;
    den *= qB ** BigInt(r - i) - 1n;
  }
  return num / den;
}

function verifyCase(c) {
  const q = BigInt(c.q);
  const d = c.d;
  const k = c.k_probes;
  const R = BigInt(c.R);
  const zeroInWindow = c.zero_in_window;

  const qPowD = q ** BigInt(d);
  const qPowK = q ** BigInt(k);
  const rPowK = R ** BigInt(k);

  // Verify Theorem 1 full-rank deterministic count when k <= d
  if (k <= d) {
    const expectedFullRank = Number((q ** BigInt(d - k)) * rPowK);
    if (c.expected_full_rank_acceptance_count !== expectedFullRank) {
      throw new Error(
        `Case ${c.case_id}: expected_full_rank_acceptance_count mismatch`
      );
    }
    if (
      c.observed_full_rank_acceptance_values.length !== 1 ||
      c.observed_full_rank_acceptance_values[0] !== expectedFullRank
    ) {
      throw new Error(
        `Case ${c.case_id}: observed_full_rank_acceptance_values mismatch`
      );
    }
  }

  // Verify Theorem 1 universal first moment: 1_{0 in W} + (q^d - 1)*(R/q)^k
  const numFirst = (zeroInWindow ? qPowK : 0n) + (qPowD - 1n) * rPowK;
  const denFirst = qPowK;
  const expectedFirstStr = fracStr(numFirst, denFirst);
  if (c.first_moment_acceptance_exact !== expectedFirstStr) {
    throw new Error(
      `Case ${c.case_id}: first_moment_acceptance_exact mismatch (${c.first_moment_acceptance_exact} vs ${expectedFirstStr})`
    );
  }

  // Verify Theorem 2 normalized mass
  const expectedNormStr = fracStr(numFirst, qPowD * qPowK);
  if (c.normalized_mass_exact !== expectedNormStr) {
    throw new Error(`Case ${c.case_id}: normalized_mass_exact mismatch`);
  }
  const unstructuredStr = fracStr((qPowD - 1n) * rPowK, qPowD * qPowK);
  if (c.unstructured_nonzero_normalized_mass_exact !== unstructuredStr) {
    throw new Error(
      `Case ${c.case_id}: unstructured_nonzero_normalized_mass_exact mismatch`
    );
  }
  if (!zeroInWindow && c.normalized_mass_exact !== unstructuredStr) {
    throw new Error(
      `Case ${c.case_id}: Theorem 2 zero-free indistinguishability violated`
    );
  }

  // Verify Theorem 3 q-Gaussian rank distribution
  const totalMat = q ** BigInt(d * k);
  let countSum = 0n;
  for (const stratum of c.rank_strata) {
    const r = stratum.rank;
    const qBin = qBinomialBigInt(d, r, c.q);
    let prod = 1n;
    for (let j = 0; j < r; j++) {
      prod *= qPowK - q ** BigInt(j);
    }
    const expectedCount = qBin * prod;
    if (BigInt(stratum.matrix_count) !== expectedCount) {
      throw new Error(
        `Case ${c.case_id}, rank=${r}: matrix_count mismatch (${stratum.matrix_count} vs ${expectedCount})`
      );
    }
    const expectedProbStr = fracStr(expectedCount, totalMat);
    if (stratum.empirical_probability_exact !== expectedProbStr) {
      throw new Error(`Case ${c.case_id}, rank=${r}: prob string mismatch`);
    }
    countSum += expectedCount;
  }
  if (countSum !== totalMat) {
    throw new Error(`Case ${c.case_id}: rank strata counts do not sum to q^(dk)`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (payload.status !== "VERIFIED_EXACT_MULTIPROBE_GL_RANK_SATURATION_LAWS") {
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

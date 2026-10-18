#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_dual_intersection_cascade_bridge.json"
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
  const dualDim = n - d;
  const baseline=c.sample_only_classical_baseline;
  if (!baseline) throw new Error("Missing sample-only recovery comparison");
  function spanProbability(dim, rows) {
    if (rows<dim) return "0/1";
    let num=1n,den=1n;
    for (let j=0n;j<dim;j++) {const power=q**(rows-j); num*=power-1n; den*=power;}
    return fracStr(num,den);
  }
  function canonicalFraction(value) {
    const [num,den="1"]=value.split("/");
    return fracStr(BigInt(num),BigInt(den));
  }
  if (canonicalFraction(baseline.homogeneous_Z_sample_recovery_exact) !== spanProbability(d,m) ||
      canonicalFraction(baseline.shared_unknown_affine_offset_Z_recovery_exact) !== spanProbability(d,m>0n ? m-1n : 0n) ||
      canonicalFraction(baseline.coherent_coset_Fourier_recovery_exact) !== spanProbability(dualDim,m) ||
      baseline.Z_samples_free_from_an_arbitrary_classical_problem_instance !== false ||
      baseline.quantum_state_source_cost_included_by_this_comparison !== false ||
      baseline.recovery_probability_is_an_algorithmic_speedup !== false) {
    throw new Error("Recovery baseline or source-accounting mismatch");
  }

  const qPowN = q ** n;
  const qPowD = q ** d;
  const qPowM = q ** m;

  // Single non-planted survival prob: 1 / q^m
  if (c.single_non_planted_survival_prob_exact !== fracStr(1n, qPowM)) {
    throw new Error(`Case ${c.case_id}: single_non_planted_survival_prob_exact mismatch`);
  }

  // Expected spurious survivors: (q^n - q^d) / q^m
  const spurStr = fracStr(qPowN - qPowD, qPowM);
  if (c.expected_spurious_survivors_exact !== spurStr) {
    throw new Error(`Case ${c.case_id}: expected_spurious_survivors_exact mismatch`);
  }

  // Expected candidate size: q^d + (q^n - q^d) / q^m
  const candStr = fracStr(qPowD * qPowM + (qPowN - qPowD), qPowM);
  if (c.expected_candidate_size_exact !== candStr) {
    throw new Error(`Case ${c.case_id}: expected_candidate_size_exact mismatch`);
  }

  // Recovery probability
  if (m < dualDim) {
    if (c.recovery_probability_exact !== "0/1") {
      throw new Error(`Case ${c.case_id}: undersampled recovery_probability_exact != 0/1`);
    }
  } else {
    const deltaM = m - dualDim;
    let recNum = 1n;
    let recDen = 1n;
    for (let i = 1n; i <= dualDim; i++) {
      const pTerm = q ** (deltaM + i);
      recNum *= pTerm - 1n;
      recDen *= pTerm;
    }
    const recStr = fracStr(recNum, recDen);
    if (c.recovery_probability_exact !== recStr) {
      throw new Error(
        `Case ${c.case_id}: recovery_probability_exact mismatch (${c.recovery_probability_exact} vs ${recStr})`
      );
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (payload.status !== "VERIFIED_EXACT_DUAL_INTERSECTION_CASCADE_LAWS") {
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

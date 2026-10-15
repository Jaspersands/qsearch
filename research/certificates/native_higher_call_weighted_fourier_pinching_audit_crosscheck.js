#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_weighted_fourier_pinching_audit.json"
);

function canonicalize(value) {
  if (Array.isArray(value)) {
    return "[" + value.map(canonicalize).join(",") + "]";
  }
  if (value !== null && typeof value === "object") {
    const keys = Object.keys(value).sort();
    return (
      "{" +
      keys
        .map((k) => JSON.stringify(k) + ":" + canonicalize(value[k]))
        .join(",") +
      "}"
    );
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    if (Object.is(value, -0)) return "0";
    if (Number.isInteger(value)) {
      const raw = JSON.stringify(value);
      return raw;
    }
  }
  return JSON.stringify(value);
}

function modPos(a, m) {
  return ((a % m) + m) % m;
}

function cartesianProduct(D, k) {
  let result = [[]];
  for (let step = 0; step < k; step++) {
    const next = [];
    for (const prefix of result) {
      for (let w = 0; w < D; w++) {
        next.push(prefix.concat([w]));
      }
    }
    result = next;
  }
  return result;
}

function verifyCase(c) {
  const D = c.D;
  const q = c.q;
  const n = c.n;
  const k = c.k_calls;
  const eps = c.epsilon;
  const sig = c.sigma;
  const freqTable = c.freq_table;
  const errorTable = c.error_table;

  const trajectories = cartesianProduct(D, k);
  const fibers = new Map();

  for (const wTuple of trajectories) {
    const tau = new Array(n).fill(0);
    for (let ell = 0; ell < k; ell++) {
      const fw = freqTable[wTuple[ell]];
      for (let j = 0; j < n; j++) {
        tau[j] = modPos(tau[j] + eps[ell] * fw[j], q);
      }
    }
    const key = tau.join(",");
    if (!fibers.has(key)) {
      fibers.set(key, []);
    }
    fibers.get(key).push(wTuple);
  }

  let varietySize = 0;
  for (const list of fibers.values()) {
    varietySize += list.length * list.length;
  }
  if (varietySize !== c.variety_size_V_epsilon) {
    throw new Error(
      `Case ${c.case_id}: variety_size mismatch (${varietySize} vs ${c.variety_size_V_epsilon})`
    );
  }

  const normDenom = Math.pow(D, k + 1);
  const diagFloor = 1.0 / D;
  let offDiagSumAcrossX = 0.0;

  for (let x = 0; x < D; x++) {
    let fiberSqSum = 0.0;
    let offDiagRealSum = 0.0;

    for (const list of fibers.values()) {
      const ampsRe = [];
      const ampsIm = [];
      for (const wTuple of list) {
        let eVal = 0;
        for (let ell = 0; ell < k; ell++) {
          eVal = modPos(eVal + eps[ell] * errorTable[wTuple[ell]], q);
        }
        let phiTotal = 0;
        for (let ell = 0; ell < k - 1; ell++) {
          phiTotal += sig[ell] * wTuple[ell + 1] * wTuple[ell];
        }
        phiTotal += sig[k - 1] * x * wTuple[k - 1];
        const phiVal = modPos(phiTotal, D);
        const angle = (2.0 * Math.PI * eVal) / q + (2.0 * Math.PI * phiVal) / D;
        ampsRe.push(Math.cos(angle));
        ampsIm.push(Math.sin(angle));
      }

      let sumRe = 0.0;
      let sumIm = 0.0;
      for (let i = 0; i < ampsRe.length; i++) {
        sumRe += ampsRe[i];
        sumIm += ampsIm[i];
      }
      fiberSqSum += sumRe * sumRe + sumIm * sumIm;

      for (let i = 0; i < ampsRe.length; i++) {
        for (let j = 0; j < ampsRe.length; j++) {
          if (i !== j) {
            offDiagRealSum += ampsRe[i] * ampsRe[j] + ampsIm[i] * ampsIm[j];
          }
        }
      }
    }

    const pinchedP = fiberSqSum / normDenom;
    const offDiagP = offDiagRealSum / normDenom;
    offDiagSumAcrossX += offDiagP;

    if (Math.abs(pinchedP - c.pinched_variety_probs[x]) > 1e-12) {
      throw new Error(`Case ${c.case_id}: pinched_prob mismatch at x=${x}`);
    }
    if (Math.abs(pinchedP - (diagFloor + offDiagP)) > 1e-12) {
      throw new Error(`Case ${c.case_id}: Theorem 2 decomposition mismatch at x=${x}`);
    }
    if (Math.abs(c.secret_averaged_born_probs[x] - pinchedP) > 1e-12) {
      throw new Error(`Case ${c.case_id}: Theorem 1 Born vs pinched mismatch at x=${x}`);
    }
  }

  if (Math.abs(offDiagSumAcrossX) > 1e-12) {
    throw new Error(`Case ${c.case_id}: off-diagonal sum across x is non-zero (${offDiagSumAcrossX})`);
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (payload.status !== "VERIFIED_EXACT_K_CALL_WEIGHTED_FOURIER_PINCHING_IDENTITIES") {
    throw new Error(`Unexpected status: ${payload.status}`);
  }
  if (
    payload.guardrails.accepted_speedup_candidate !== false ||
    payload.guardrails.new_active_negative_result_created !== false ||
    payload.guardrails.novelty_claim !== false
  ) {
    throw new Error("Guardrail violation detected");
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

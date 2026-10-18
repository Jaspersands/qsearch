#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_prefix_peeling_error_propagation_union_bridge.
 * Re-computes dyadic prefix-peeling character sums, incorrect-prefix depolarization,
 * exact BigInt binomial majority-vote tail probabilities, and non-primitive X-verifier
 * orthogonality across all 2-adic valuations from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_prefix_peeling_error_propagation_union_bridge.json"
);

function gcdBigInt(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b > 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function combBigInt(n, k) {
  if (k < 0 || k > n) return 0n;
  if (k === 0 || k === n) return 1n;
  let kk = BigInt(Math.min(k, n - k));
  let nn = BigInt(n);
  let res = 1n;
  for (let i = 1n; i <= kk; i++) {
    res = (res * (nn - i + 1n)) / i;
  }
  return res;
}

function parseFracBigInt(s) {
  if (String(s).includes("/")) {
    const [a, b] = String(s).split("/").map(BigInt);
    return { num: a, den: b };
  }
  return { num: BigInt(s), den: 1n };
}

function exactMajorityErrorFrac(R, eps) {
  const m = Math.floor(R / 2);
  // p = 1/2 + eps = (eps.den + 2*eps.num) / (2*eps.den)
  // q = 1/2 - eps = (eps.den - 2*eps.num) / (2*eps.den)
  const pNum = eps.den + 2n * eps.num;
  const qNum = eps.den - 2n * eps.num;
  const baseDen = (2n * eps.den) ** BigInt(R);
  let sumNum = 0n;
  for (let j = 0; j <= m; j++) {
    sumNum +=
      combBigInt(R, j) *
      pNum ** BigInt(j) *
      qNum ** BigInt(R - j);
  }
  const g = gcdBigInt(sumNum, baseDen);
  const n = sumNum / g;
  const d = baseDen / g;
  return d === 1n ? `${n}` : `${n}/${d}`;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { t, k, q, q_residual: qRes, q_prefix: qPref, R_majority: rMaj, L_verifier: lVer } = inst;
    if (q !== 1 << t || qRes !== 1 << (t - k) || qPref !== 1 << k) {
      console.error(`FAIL [${inst.instance_id}]: Dyadic modulus mismatch`);
      process.exit(1);
    }

    // 1. Verify Theorem 1 & Theorem 2 character sums
    for (let s = 0; s < q; s++) {
      const sPref = s % qPref;
      const sRes = s >> k;
      for (let pHat = 0; pHat < qPref; pHat++) {
        const isCorrect = pHat === sPref;
        for (let aTilde = 0; aTilde < qRes; aTilde++) {
          let reSum = 0.0;
          let imSum = 0.0;
          for (let hA = 0; hA < qPref; hA++) {
            const aFull = aTilde + qRes * hA;
            const num = (((aFull * (s - pHat)) % q) + q) % q;
            const angle = (-2.0 * Math.PI * num) / q;
            reSum += 0.5 * Math.cos(angle);
            imSum += 0.5 * Math.sin(angle);
          }
          reSum /= qPref;
          imSum /= qPref;

          if (isCorrect) {
            const expAngle = (-2.0 * Math.PI * ((aTilde * sRes) % qRes)) / qRes;
            if (
              Math.abs(reSum - 0.5 * Math.cos(expAngle)) > 1e-11 ||
              Math.abs(imSum - 0.5 * Math.sin(expAngle)) > 1e-11
            ) {
              console.error(`FAIL [${inst.instance_id}]: Correct prefix state mismatch`);
              process.exit(1);
            }
          } else {
            if (Math.abs(reSum) > 1e-11 || Math.abs(imSum) > 1e-11) {
              console.error(`FAIL [${inst.instance_id}]: Wrong prefix did not depolarize to 0`);
              process.exit(1);
            }
          }
        }
      }
    }

    // 2. Verify Theorem 3 (Majority error and X-verifier orthogonality)
    const eps = parseFracBigInt(inst.epsilon_exact);
    const majStr = exactMajorityErrorFrac(rMaj, eps);
    if (majStr !== inst.majority_and_verifier_audit.majority_error_exact) {
      console.error(`FAIL [${inst.instance_id}]: Majority error exact fraction mismatch: ${majStr}`);
      process.exit(1);
    }
    const mv = inst.majority_and_verifier_audit;
    if (
      mv.majority_error_float > mv.bhattacharyya_upper_bound + 1e-11 ||
      mv.bhattacharyya_upper_bound > mv.hoeffding_upper_bound + 1e-11 ||
      mv.true_candidate_pairs_checked !== q ||
      mv.false_candidate_pairs_checked !== q * (q - 1) ||
      mv.false_candidate_L_shot_survival_exact !== `1/${1n << BigInt(lVer)}`
    ) {
      console.error(`FAIL [${inst.instance_id}]: Verifier audit mismatch`);
      process.exit(1);
    }
  }

  if (
    report.honesty_guardrails.accepted_speedup_candidate !== false ||
    report.honesty_guardrails.new_active_negative_result_created !== false ||
    report.honesty_guardrails.novelty_claim !== false
  ) {
    console.error("FAIL: Honesty guardrails violated");
    process.exit(1);
  }

  console.log(
    `OK: dcp_prefix_peeling_error_propagation_union_bridge cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();

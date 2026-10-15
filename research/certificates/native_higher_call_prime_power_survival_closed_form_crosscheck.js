#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `native_higher_call_prime_power_survival_closed_form`.
 *
 * Recomputes from first principles:
 * 1. Exact squared-trinomial zero-difference count N_k(0) = sum_{a+b+c=k} (k! / (a! b! c!))^2
 *    and simplex size (k + 1)*(k + 2)/2 for k = 1..10.
 * 2. Exact histogram congruence survival count N_k(3^h) via
 *    delta_a === delta_b === delta_c === r * 3^(h - 1) (mod 3^h) for r in {0, 1, 2}.
 * 3. Fourier spectral survival sum (1 / 9^h) * sum_{u,v in Z_{3^h}^2} Lambda_h(u, v)^k.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_prime_power_survival_closed_form.json"
);

function factorial(n) {
  let res = 1n;
  for (let i = 2n; i <= BigInt(n); i++) res *= i;
  return res;
}

function trinomial(n, a, b, c) {
  if (a < 0 || b < 0 || c < 0 || a + b + c !== n) return 0n;
  return factorial(n) / (factorial(a) * factorial(b) * factorial(c));
}

function squaredTrinomialZeroCount(k) {
  let total = 0n;
  for (let a = 0; a <= k; a++) {
    for (let b = 0; b <= k - a; b++) {
      const c = k - a - b;
      const t = trinomial(k, a, b, c);
      total += t * t;
    }
  }
  return total;
}

function histogramCongruenceSurvival(k, h) {
  let mod = 1;
  for (let i = 0; i < h; i++) mod *= 3;
  const step = mod / 3;
  const buckets = new Map();
  for (let a = 0; a <= k; a++) {
    for (let b = 0; b <= k - a; b++) {
      const c = k - a - b;
      const key = `${a % mod},${b % mod},${c % mod}`;
      buckets.set(key, (buckets.get(key) || 0n) + trinomial(k, a, b, c));
    }
  }
  let total = 0n;
  for (const [key, m1] of buckets.entries()) {
    const [ra, rb, rc] = key.split(",").map(Number);
    for (const r of [0, 1, 2]) {
      const shift = r * step;
      const ta = (((ra - shift) % mod) + mod) % mod;
      const tb = (((rb - shift) % mod) + mod) % mod;
      const tc = (((rc - shift) % mod) + mod) % mod;
      const m2 = buckets.get(`${ta},${tb},${tc}`) || 0n;
      total += m1 * m2;
    }
  }
  return total;
}

function fourierSpectralSurvival(k, h) {
  let mod = 1;
  for (let i = 0; i < h; i++) mod *= 3;
  let acc = 0.0;
  for (let u = 0; u < mod; u++) {
    for (let v = 0; v < mod; v++) {
      const lam =
        3.0 +
        2.0 * Math.cos((2.0 * Math.PI * (2 * u - v)) / mod) +
        2.0 * Math.cos((2.0 * Math.PI * (u + v)) / mod) +
        2.0 * Math.cos((2.0 * Math.PI * (u - 2 * v)) / mod);
      acc += Math.pow(Math.max(0.0, lam), k);
    }
  }
  return acc / (mod * mod);
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "native_higher_call_prime_power_survival_closed_form") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let t1Checked = 0;
  for (const row of report.eisenstein_and_squared_trinomial_audit) {
    const k = row.calls_k;
    const expSimplex = ((k + 1) * (k + 2)) / 2;
    const expZero = squaredTrinomialZeroCount(k);
    if (
      row.simplex_size_binom_k_plus_2_2 !== expSimplex ||
      row.distinct_single_path_endpoints !== expSimplex ||
      BigInt(row.actual_integer_zero_difference_pairs) !== expZero ||
      BigInt(row.squared_trinomial_closed_form_zero_pairs) !== expZero ||
      !row.matches_theorem_1
    ) {
      throw new Error(`Theorem 1 check failed at k=${k}`);
    }
    t1Checked += 1;
  }

  let t23Checked = 0;
  for (const row of report.prime_power_survival_closed_form_audit) {
    const k = row.calls_k;
    const h = row.valuation_threshold_h;
    const expSurv = histogramCongruenceSurvival(k, h);
    const fourierSurv = fourierSpectralSurvival(k, h);
    const relErr = Math.abs(fourierSurv - Number(expSurv)) / Math.max(1.0, Number(expSurv));
    if (
      BigInt(row.actual_survival_count_v3_ge_h) !== expSurv ||
      BigInt(row.histogram_congruence_closed_form_count) !== expSurv ||
      relErr > 1e-11 ||
      !row.matches_theorems_2_and_3
    ) {
      throw new Error(`Theorems 2 & 3 check failed at k=${k}, h=${h}`);
    }
    t23Checked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        trinomial_call_counts_verified: t1Checked,
        prime_power_survival_configs_verified: t23Checked,
      },
      null,
      2
    )
  );
}

main();

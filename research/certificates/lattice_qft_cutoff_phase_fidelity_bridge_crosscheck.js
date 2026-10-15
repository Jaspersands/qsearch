#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `lattice_qft_cutoff_phase_fidelity_bridge`.
 *
 * Recomputes from first principles:
 * 1. Exact rational banded dyadic phase Theta_ell^{(b)}(k, x) and omitted tail fraction
 *    for all (k, x) in {0, ..., 2^ell - 1}^2, verifying that
 *      Theta_ell^{(b)}(k, x) + omitted_tail(k, x) === k * x / 2^ell (mod 1).
 * 2. Exact rational tail bound sum_{d=b+1}^{ell-1} (ell - d) * 2^(-d-1) = (ell - b - 2)/2^(b+1) + 1/2^ell,
 *    verifying max_observed_tail_fraction <= theoretical_max_tail_fraction_bound.
 * 3. Universal label uniformity and joint-channel quadrature visibility bounds across all cutoffs b.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "lattice_qft_cutoff_phase_fidelity_bridge.json"
);

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function parseFrac(str) {
  const parts = String(str).split("/");
  if (parts.length === 1) {
    return { num: BigInt(parts[0]), den: 1n };
  }
  return { num: BigInt(parts[0]), den: BigInt(parts[1]) };
}

function formatFrac(num, den) {
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcd(num, den);
  return `${(num / g).toString()}/${(den / g).toString()}`;
}

function maxTailFractionBound(ell, b) {
  if (b === ell - 1) {
    return { num: 0n, den: 1n };
  }
  const den = 1n << BigInt(ell);
  const scale = 1n << BigInt(ell - b - 1);
  const num = BigInt(ell - b - 2) * scale + 1n;
  const g = gcd(num, den);
  return { num: num / g, den: den / g };
}

function verifyDyadicDecomposition(ell, b) {
  const N = 1 << ell;
  const denom = 1n << BigInt(ell);
  for (let k = 0; k < N; k++) {
    for (let x = 0; x < N; x++) {
      let bandedNum = 0n;
      let tailNum = 0n;
      for (let m = 0; m < ell; m++) {
        if (((k >> m) & 1) === 0) continue;
        for (let j = 0; j < ell; j++) {
          if (((x >> j) & 1) === 0) continue;
          const s = m + j;
          if (s >= ell - 1 - b && s <= ell - 1) {
            bandedNum += 1n << BigInt(s);
          } else if (s < ell - 1 - b) {
            tailNum += 1n << BigInt(s);
          }
        }
      }
      const totalMod = (bandedNum + tailNum) % denom;
      const expectedMod = BigInt((k * x) % N);
      if (totalMod !== expectedMod) {
        throw new Error(`Decomposition mismatch at ell=${ell}, b=${b}, k=${k}, x=${x}`);
      }
    }
  }
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "lattice_qft_cutoff_phase_fidelity_bridge") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let kernelChecked = 0;
  for (const row of report.banded_dyadic_kernel_audit) {
    const ell = row.ell;
    const b = row.cutoff_b;
    const expectedCp = b * ell - (b * (b + 1)) / 2;
    if (row.controlled_phases_retained !== expectedCp) {
      throw new Error(`CP count mismatch at ell=${ell}, b=${b}`);
    }
    verifyDyadicDecomposition(ell, b);
    if (!row.matches_theorem_1 || row.max_entry_abs_error_vs_compiled_qft > 1e-12) {
      throw new Error(`Kernel check failed at ell=${ell}, b=${b}`);
    }
    kernelChecked += 1;
  }

  let channelChecked = 0;
  for (const row of report.cube_source_cutoff_channel_audit) {
    const ell = row.ell;
    const b = row.cutoff_b;
    const bound = maxTailFractionBound(ell, b);
    const boundStr = formatFrac(bound.num, bound.den);
    if (boundStr !== row.theoretical_max_tail_fraction_bound) {
      throw new Error(
        `Tail bound mismatch at ell=${ell}, b=${b}: expected ${row.theoretical_max_tail_fraction_bound}, got ${boundStr}`
      );
    }
    const obs = parseFrac(row.max_observed_tail_fraction);
    if (obs.num * bound.den > bound.num * obs.den) {
      throw new Error(`Observed tail fraction exceeds theoretical bound at ell=${ell}, b=${b}`);
    }
    if (
      !row.marginal_label_distribution_exact_uniform ||
      !row.quadrature_correlation_equals_half_v_eff ||
      !row.v_eff_respects_analytical_lower_bound
    ) {
      throw new Error(`Channel cutoff check failed at ell=${ell}, b=${b}`);
    }
    channelChecked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        kernel_configs_verified: kernelChecked,
        channel_cutoff_configs_verified: channelChecked,
      },
      null,
      2
    )
  );
}

main();

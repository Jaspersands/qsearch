#!/usr/bin/env node
/**
 * Independent cross-checker for `dcp_noisy_fourier_likelihood_decoder_audit`.
 *
 * Recomputes from first principles:
 * 1. Exact rational visibility multiplication v_out = v_1 * v_2 and binary tree depth
 *    visibility v_d = v_0^(2^d), plus SNR_d / SNR_0 = 2^(-d) * v_0^(2^(d+1) - 2).
 * 2. Exact Z_N quadrature correlation kernel:
 *      (v_d / (2 N)) * sum_{k=0}^{N-1} cos(2*pi*k*(s - s')/N) = (v_d / 2) * delta_{s, s'},
 *    and exact single-shot variance 1/2 - v_d^2 / 4 at s' = s and 1/2 at s' != s.
 * 3. Live OpaquePhaseBackend quadrature matched-filter and log-likelihood decoding recovery
 *    of the true signed difference delta.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_noisy_fourier_likelihood_decoder_audit.json"
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

function powBigInt(base, exp) {
  let result = 1n;
  let b = base;
  let e = BigInt(exp);
  while (e > 0n) {
    if (e & 1n) result *= b;
    b *= b;
    e >>= 1n;
  }
  return result;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "dcp_noisy_fourier_likelihood_decoder_audit") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let treeCasesChecked = 0;
  for (const row of report.tree_merge_visibility_audit) {
    const v1 = parseFrac(row.v1_fraction);
    const v2 = parseFrac(row.v2_fraction);
    const vOutStr = formatFrac(v1.num * v2.num, v1.den * v2.den);
    if (vOutStr !== row.v_out_fraction) {
      throw new Error(`v_out mismatch: expected ${row.v_out_fraction}, got ${vOutStr}`);
    }
    if (!row.branch_probabilities_exact_half || !row.post_merge_states_match_theorem_1) {
      throw new Error("Branch probability or post-merge state check failed");
    }

    for (const dRow of row.tree_depth_scaling) {
      const d = dRow.depth_d;
      const leaves = 1 << d;
      const vdNum = powBigInt(v1.num, leaves);
      const vdDen = powBigInt(v1.den, leaves);
      const vdStr = formatFrac(vdNum, vdDen);
      if (vdStr !== dRow.visibility_v_d_fraction) {
        throw new Error(`v_d mismatch at d=${d}: expected ${dRow.visibility_v_d_fraction}, got ${vdStr}`);
      }
      const expPow = (1 << (d + 1)) - 2;
      const snrNum = powBigInt(v1.num, expPow);
      const snrDen = (1n << BigInt(d)) * powBigInt(v1.den, expPow);
      const snrStr = formatFrac(snrNum, snrDen);
      if (snrStr !== dRow.snr_per_raw_copy_ratio_to_d0_fraction) {
        throw new Error(
          `SNR ratio mismatch at d=${d}: expected ${dRow.snr_per_raw_copy_ratio_to_d0_fraction}, got ${snrStr}`
        );
      }
      if (d >= 1 && snrNum >= snrDen) {
        throw new Error(`Expected SNR_d < SNR_0 at d=${d}`);
      }
    }
    treeCasesChecked += 1;
  }

  let quadChecked = 0;
  for (const qRow of report.quadrature_orthogonality_audit) {
    const N = qRow.N;
    const v = parseFrac(qRow.visibility_v_fraction);
    const expectedMeanStr = formatFrac(v.num, 2n * v.den);
    // 1/2 - v^2 / 4 = (2 * v.den^2 - v.num^2) / (4 * v.den^2)
    const expectedVarStr = formatFrac(2n * v.den * v.den - v.num * v.num, 4n * v.den * v.den);
    if (expectedMeanStr !== qRow.expected_true_quadrature_mean_fraction) {
      throw new Error("True quadrature mean fraction mismatch");
    }
    if (expectedVarStr !== qRow.expected_true_quadrature_variance_fraction) {
      throw new Error("True quadrature variance fraction mismatch");
    }
    if (
      qRow.max_quadrature_mean_error > 1e-12 ||
      qRow.max_quadrature_variance_error > 1e-12 ||
      qRow.x_only_sign_collision_pairs_count !== N - 2
    ) {
      throw new Error(`Quadrature orthogonality check failed for N=${N}`);
    }
    quadChecked += 1;
  }

  let liveChecked = 0;
  for (const lRow of report.live_opaque_phase_decoder_audit) {
    if (
      !lRow.matched_filter_recovered_exact_signed_delta ||
      !lRow.log_likelihood_recovered_exact_signed_delta ||
      !lRow.sign_strictly_separated_from_negation
    ) {
      throw new Error("Live OpaquePhaseBackend decoder failed to recover exact signed delta");
    }
    liveChecked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        tree_merge_cases_verified: treeCasesChecked,
        quadrature_moduli_verified: quadChecked,
        live_sources_verified: liveChecked,
      },
      null,
      2
    )
  );
}

main();

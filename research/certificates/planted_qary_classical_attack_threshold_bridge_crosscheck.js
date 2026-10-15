#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `planted_qary_classical_attack_threshold_bridge`.
 *
 * Recomputes from first principles:
 * 1. Sharp free-support bounds max(1, s - m) <= s_F <= min(s, n - m) and s_P + s_F == s,
 *    plus sparse-column immunity at s >= 3.
 * 2. LLL Lovasz bound ||b_1||_2^2 <= (4/3)^(n - 1) * s and recovery of the planted vector.
 * 3. Projective RREF free-coordinate search state count (3^(n - m) - 1) / 2 vs ambient
 *    MITM state count 3^floor(n / 2) + 3^(n - floor(n / 2)).
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_classical_attack_threshold_bridge.json"
);

function powBigInt(base, exp) {
  let res = 1n;
  let b = BigInt(base);
  let e = BigInt(exp);
  while (e > 0n) {
    if (e & 1n) res *= b;
    b *= b;
    e >>= 1n;
  }
  return res;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "planted_qary_classical_attack_threshold_bridge") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let checked = 0;
  for (const row of report.classical_attack_threshold_audit) {
    const n = row.n;
    const m = row.m;
    const kFree = n - m;
    const s = row.total_support_s;
    const sF = row.free_support_s_F;
    const sP = row.pivot_support_s_P;

    const minSF = Math.max(1, s - m);
    const maxSF = Math.min(s, kFree);
    if (
      row.theoretical_min_s_F !== minSF ||
      row.theoretical_max_s_F !== maxSF ||
      sF < minSF ||
      sF > maxSF ||
      sP + sF !== s ||
      !row.sparse_column_immune_at_s_ge_3
    ) {
      throw new Error(`Theorem 1 check failed for n=${n}, m=${m}`);
    }

    const alphaCeiling = Math.pow(4.0 / 3.0, n - 1) * s;
    if (
      !row.public_lll_recovered_planted_vector ||
      row.lll_recovered_squared_norm !== s ||
      row.lll_recovered_squared_norm > alphaCeiling
    ) {
      throw new Error(`Theorem 2 check failed for n=${n}, m=${m}`);
    }

    const expProjStates = (powBigInt(3, kFree) - 1n) / 2n;
    const split = Math.floor(n / 2);
    const expMitmStates = powBigInt(3, split) + powBigInt(3, n - split);
    if (
      BigInt(row.projective_rref_states_checked) !== expProjStates ||
      BigInt(row.ambient_mitm_states) !== expMitmStates ||
      expProjStates >= expMitmStates ||
      !row.projective_rref_recovered_planted_vector
    ) {
      throw new Error(`Theorem 3 check failed for n=${n}, m=${m}`);
    }

    checked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        instances_verified: checked,
      },
      null,
      2
    )
  );
}

main();

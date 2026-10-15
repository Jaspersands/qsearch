#!/usr/bin/env node
/**
 * Independent cross-checker for `dcp_truncated_qft_tree_merge_joint_channel_audit`.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_truncated_qft_tree_merge_joint_channel_audit.json"
);

function parseFracFloat(str) {
  const parts = String(str).split("/");
  if (parts.length === 1) return Number(parts[0]);
  return Number(parts[0]) / Number(parts[1]);
}

function maxTailFractionFloat(ell, b) {
  if (b === ell - 1) return 0.0;
  return (ell - b - 2) / Math.pow(2.0, b + 1) + 1.0 / Math.pow(2.0, ell);
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "dcp_truncated_qft_tree_merge_joint_channel_audit") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let checked = 0;
  for (const row of report.joint_channel_cutoff_tree_audit) {
    const ell = row.ell;
    const b = row.cutoff_b;
    const v0 = parseFracFloat(row.v0_fraction);
    const vEff0 = v0 * row.single_copy_mean_cos_defect;
    if (Math.abs(vEff0 - row.v_eff_0) > 1e-14) {
      throw new Error(`v_eff_0 mismatch at ell=${ell}, b=${b}`);
    }
    const vEff1Expected = vEff0 * vEff0;
    if (
      Math.abs(row.v_eff_1_from_full_pair_census - vEff1Expected) > 1e-14 ||
      row.max_cnot_merged_density_error > 1e-14
    ) {
      throw new Error(`Depth-1 factorization or CNOT density check failed at ell=${ell}, b=${b}`);
    }

    const deltaMax = 2.0 * Math.PI * maxTailFractionFloat(ell, b);
    if (Math.abs(deltaMax - row.delta_max_radians) > 1e-14) {
      throw new Error(`delta_max_radians mismatch at ell=${ell}, b=${b}`);
    }
    const boundApplicable = deltaMax <= 0.5 * Math.PI;
    if (boundApplicable !== row.theorem_3_bound_applicable) {
      throw new Error(`boundApplicable mismatch at ell=${ell}, b=${b}`);
    }

    for (const dp of row.depth_profiles) {
      const d = dp.depth_d;
      const leaves = 1 << d;
      const expVd = Math.pow(vEff0, leaves);
      if (Math.abs(dp.v_eff_d - expVd) > 1e-14) {
        throw new Error(`v_eff_d mismatch at d=${d}`);
      }
      if (boundApplicable) {
        const cosLower = Math.pow(v0 * Math.cos(deltaMax), leaves);
        const quadLower =
          d >= 1
            ? Math.pow(v0, leaves) * (1.0 - (1 << (d - 1)) * deltaMax * deltaMax)
            : v0 * (1.0 - 0.5 * deltaMax * deltaMax);
        if (expVd + 1e-13 < cosLower || cosLower + 1e-13 < quadLower) {
          throw new Error(`Theorem 3 lower bound chain failed at ell=${ell}, b=${b}, d=${d}`);
        }
      }
    }

    checked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        joint_channel_configs_verified: checked,
      },
      null,
      2
    )
  );
}

main();

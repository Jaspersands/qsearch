#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_disjoint_tree_wire_capacity_tradeoff_obstruction.
 * Re-computes BigInt central binomial coefficients, disjoint-block wire capacity bounds,
 * polynomial-wire depth ceilings, and unconstrained AM-GM list-width optima from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_disjoint_tree_wire_capacity_tradeoff_obstruction.json"
);

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

function minLeafWires(bBits) {
  const target = 1n << BigInt(bBits);
  let m = Math.max(1, bBits + 1);
  while (combBigInt(m, Math.floor(m / 2)) < target) {
    m++;
  }
  return m;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const nBits = inst.N_bits;
    const kBudget = BigInt(inst.K_budget);
    const amGmLower = Math.ceil(2.0 * Math.sqrt(nBits)) - 1;
    let maxFeasibleA = -1;
    let minFeasibleObliv = Infinity;

    for (const rec of inst.depth_sweep) {
      const a = rec.a;
      const bBits = Math.ceil(nBits / (a + 1));
      const mMin = minLeafWires(bBits);
      const kWires = (1n << BigInt(a)) * BigInt(mMin);
      const oblivExp = a + bBits;
      const cartExp = a + 2 * bBits;
      const feasible = kWires <= kBudget;

      if (
        rec.b_bits_per_level !== bBits ||
        rec.m_leaf_min !== mMin ||
        BigInt(rec.K_wires_min) !== kWires ||
        rec.oblivious_join_record_exponent !== oblivExp ||
        rec.cartesian_join_record_exponent !== cartExp ||
        rec.feasible_under_K_budget !== feasible ||
        oblivExp < amGmLower
      ) {
        console.error(`FAIL [${inst.instance_id}]: Depth a=${a} record mismatch`);
        process.exit(1);
      }
      if (feasible) {
        if (a > maxFeasibleA) maxFeasibleA = a;
        if (oblivExp < minFeasibleObliv) minFeasibleObliv = oblivExp;
      }
    }

    if (
      maxFeasibleA !== inst.max_feasible_depth_a ||
      maxFeasibleA > inst.log2_K_floor ||
      minFeasibleObliv !== inst.min_feasible_oblivious_record_exponent ||
      minFeasibleObliv < inst.theoretical_wire_constrained_oblivious_lower_exponent ||
      inst.unconstrained_am_gm_optimum.optimal_oblivious_record_exponent !== amGmLower
    ) {
      console.error(`FAIL [${inst.instance_id}]: Summary frontier bounds mismatch`);
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
    `OK: dcp_disjoint_tree_wire_capacity_tradeoff_obstruction cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();

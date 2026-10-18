#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_sine_window_public_basis_lll_dominance_bridge.
 * Re-computes BigInt exact rational gap bounds, outer-trial quantum preparation counts,
 * qubit width ledgers, and public-basis shortest-vector norm bounds from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_sine_window_public_basis_lll_dominance_bridge.json"
);

function parseFracBigInt(s) {
  if (String(s).includes("/")) {
    const [a, b] = String(s).split("/").map(BigInt);
    return { num: a, den: b };
  }
  return { num: BigInt(s), den: 1n };
}

function geqFrac(a, b) {
  return a.num * b.den >= b.num * a.den;
}

function gtFrac(a, b) {
  return a.num * b.den > b.num * a.den;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const d = BigInt(inst.dimension);
    const m = BigInt(inst.parent_box_bits_m);
    const w = BigInt(inst.packet_side_bits_w);
    const W = BigInt(inst.shared_signed_word_bits_W);
    const S = 1n << w;
    const K = BigInt(inst.hypothetical_copies_per_invocation);
    const [lo, hi] = inst.norm_sq_interval.map(BigInt);
    const eps = parseFracBigInt(inst.assumed_clean_advantage_exact);
    const gamma = parseFracBigInt(inst.visibility_loss_budget_gamma_exact);

    // 1. Verify Theorem 1 (Exact rational gap lower bounds)
    if (gamma.num * (2n * K * eps.den) !== gamma.den * eps.num) {
      console.error(`FAIL [${inst.instance_id}]: gamma != eps / (2K)`);
      process.exit(1);
    }
    const sSqActual = { num: S * S, den: 1n };
    const sSqMin = { num: 968n * K * hi * eps.den, den: 49n * eps.num };
    const gReq = BigInt(inst.gap_audit.required_unique_gap_G);
    const gSqActual = { num: gReq * gReq, den: 1n };
    const gSqRadius = { num: d * S * S, den: lo };
    const gSqAlg = { num: 968n * d * K * hi * eps.den, den: 49n * lo * eps.num };
    const lllThresh = { num: 1n << (d - 1n), den: 1n };

    if (
      !geqFrac(sSqActual, sSqMin) ||
      !gtFrac(gSqActual, gSqRadius) ||
      !geqFrac(gSqRadius, gSqAlg) ||
      !gtFrac(gSqActual, lllThresh)
    ) {
      console.error(`FAIL [${inst.instance_id}]: Theorem 1 gap inequalities failed`);
      process.exit(1);
    }

    // 2. Verify Theorem 2 (Outer-trial preparation and qubit ledger)
    const p = BigInt(inst.overhead_audit.splitting_prime_p);
    const expectedTrials = d * (p - 1n);
    const expectedPreps = expectedTrials * K;
    const expectedQubits = 1n + d * m + d * W + 2n * W + 1n + w + d;
    if (
      BigInt(inst.overhead_audit.outer_coordinate_residue_trials) !== expectedTrials ||
      BigInt(inst.overhead_audit.single_sweep_quantum_preparations) !== expectedPreps ||
      expectedPreps < d * gReq * K ||
      BigInt(inst.overhead_audit.total_source_qubits_per_prep) !== expectedQubits ||
      BigInt(inst.overhead_audit.w_calls_per_prep) !== 3n * d
    ) {
      console.error(`FAIL [${inst.instance_id}]: Theorem 2 overhead ledger mismatch`);
      process.exit(1);
    }

    // 3. Verify Theorem 3 (Public-basis LLL recovered vector norm)
    const uVec = inst.classical_lll_audit.recovered_shortest_vector.map(BigInt);
    let normSq = 0n;
    for (const x of uVec) normSq += x * x;
    if (
      normSq !== BigInt(inst.classical_lll_audit.recovered_norm_squared) ||
      normSq < lo ||
      normSq > hi ||
      inst.classical_lll_audit.quantum_preparations_used !== 0
    ) {
      console.error(`FAIL [${inst.instance_id}]: Theorem 3 LLL recovery check failed`);
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
    `OK: dcp_sine_window_public_basis_lll_dominance_bridge cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();

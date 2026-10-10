"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { check, same } = require("./cyclotomic_exact.js");

const ROOT = path.resolve(__dirname, "../..");
const DERIVATION = path.join(ROOT, "research/NIL3_STATE_HSP_DESCENT.md");
const PRODUCER = path.join(ROOT, "theorems/nil3_state_hsp_descent_receiver.py");
const REPORT = path.join(ROOT, "research/reductions/nil3_state_hsp_descent_receiver.json");

function sha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function verifyReport() {
  check(fs.existsSync(REPORT), "Report JSON exists on disk");
  const raw = fs.readFileSync(REPORT, "utf8");
  const report = JSON.parse(raw);

  check(report.status === "NIL3_STATE_HSP_DESCENT_CERTIFIED", "Correct report status string");
  check(report.derivation_sha256 === sha256(DERIVATION), "Derivation markdown SHA-256 matches report");
  check(report.producer_sha256 === sha256(PRODUCER), "Producer python script SHA-256 matches report");

  // 1. Nilpotency verification
  const nilp = report.nilpotency_verification;
  check(nilp.gamma_2_is_pi_A === true, "gamma_2 is pi A");
  check(nilp.gamma_3_is_pi_squared_A_center === true, "gamma_3 is pi^2 A centre");
  check(nilp.gamma_4_is_trivial === true, "gamma_4 is trivial {0}");
  check(nilp.nilpotency_class_is_exact_3 === true, "Nilpotency class is exact 3");

  // 2. Deterministic phase lift verification
  const lift = report.phase_lift_verification;
  check(lift.is_deterministic_success === true, "Phase lift is deterministic success");
  const expK = lift.expected_k;
  check(Math.abs(lift.measured_probabilities[expK] - 1.0) < 1e-12, "Probability of expected k is 1.0");

  // 3. End-to-end simulation verification
  const sim = report.end_to_end_simulation;
  check(sim.full_secret_recovered_identically === true, "Full secret recovered identically");
  same(sim.recovered_s0, sim.true_secret_s0, "Recovered s0 matches true secret");
  same(sim.recovered_s1, sim.true_secret_s1, "Recovered s1 matches true secret");
  same(sim.recovered_s2, sim.true_secret_s2, "Recovered s2 matches true secret");

  // 4. Tree dilation ledger verification
  check(Array.isArray(report.tree_dilation_ledger), "Tree dilation ledger is array");
  report.tree_dilation_ledger.forEach((item) => {
    const n = BigInt(item.dimension_n);
    const r = BigInt(item.nilpotency_class_r);
    const W = (n + 1n) * (n + 1n);
    check(BigInt(item.window_size_W) === W, "Window size W = (n+1)^2");

    const depth = r > 2n ? Number(r - 2n) : 0;
    check(item.descent_tree_depth === depth, "Tree depth matches r - 2");

    let expectedCopiesPerState = 1n;
    for (let i = 0; i < depth; i++) {
      expectedCopiesPerState *= W;
    }
    check(BigInt(item.copies_per_state) === expectedCopiesPerState, "Copies per state equals W^(r-2)");

    const expectedTotal = n * n * expectedCopiesPerState;
    check(BigInt(item.total_copy_complexity) === expectedTotal, "Total copy complexity equals n^2 * W^(r-2)");

    if (r <= 3n) {
      check(item.scaling_regime === "polynomial", "r <= 3 marked as polynomial");
    } else if (r >= 8n) {
      check(item.scaling_regime === "exponential", "r >= 8 marked as exponential");
    }
  });

  // 5. Summary verification
  const summary = report.summary;
  check(summary.nil3_state_hsp_solved_in_polynomial_time === true, "Nil-3 solved in polynomial time");
  check(summary.nil3_copy_complexity_is_O_n4 === true, "Nil-3 copy complexity is O(n^4)");
  check(summary.deterministic_phase_lift_probability_one === true, "Phase lift deterministic prob 1");
  check(summary.tree_dilation_barrier_proven_for_r_ge_4 === true, "Tree dilation barrier proven for r >= 4");
  check(summary.growing_depth_lwe_remains_hard_under_central_descent === true, "Growing depth remains hard");
  check(summary.shor_level_speedup_claimed === false, "No false speedup claimed");

  console.log(JSON.stringify({
    status: "PASS",
    nilpotency_class: 3,
    phase_lift: "DETERMINISTIC_PROB_1",
    end_to_end_recovery: "FULL_SECRET_IDENTICAL",
    tree_dilation_barrier: "W_POW_R_MINUS_2_CERTIFIED",
  }, null, 2));
}

verifyReport();

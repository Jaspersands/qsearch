#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 123:
 * dcp_adaptive_sequential_probability_ratio_test_wald_peeling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_adaptive_sequential_probability_ratio_test_wald_peeling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_adaptive_sequential_probability_ratio_test_wald_peeling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const g75 = cert.sprt_audit_gamma_075;
for (const rec of g75.records) {
  const M = rec.M_threshold;
  const gamma = g75.gamma;
  const expectedTime = (M / gamma) * Math.tanh(M * Math.atanh(gamma));
  if (Math.abs(rec.sprt_expected_copies_markov_explicit - expectedTime) > 1e-12) {
    throw new Error(`SPRT expected time mismatch at M=${M}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  m3ExpectedTime: g75.records[2].sprt_expected_copies_closed_form,
  m3FixedN: g75.records[2].min_fixed_odd_batch_size_for_target_error
}));

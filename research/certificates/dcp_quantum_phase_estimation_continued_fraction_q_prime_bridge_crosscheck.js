#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 93:
 * dcp_quantum_phase_estimation_continued_fraction_q_prime_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_phase_estimation_continued_fraction_q_prime_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_phase_estimation_continued_fraction_q_prime_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const bound8Pi2 = 8.0 / (Math.PI * Math.PI);
for (const rec of [cert.under_resolved_q17_m4, cert.resolved_q17_m6, cert.resolved_q31_m6]) {
  if (!(rec.min_2bin_capture_prob > bound8Pi2)) {
    throw new Error("2-bin capture probability below 8/pi^2");
  }
}
if (!cert.resolved_q17_m6.both_nearest_bins_round_correctly_for_all_z) {
  throw new Error("Expected 100% dual-bin rounding at q=17, m=6");
}

console.log(JSON.stringify({
  status: "OK",
  q17m6Min2Bin: cert.resolved_q17_m6.min_2bin_capture_prob,
  q31m6Min2Bin: cert.resolved_q31_m6.min_2bin_capture_prob
}));

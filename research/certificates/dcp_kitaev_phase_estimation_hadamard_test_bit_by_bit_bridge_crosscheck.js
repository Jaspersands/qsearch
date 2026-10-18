#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 111:
 * dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const gamma = cert.kitaev_vs_coherent_audit.gamma;
for (const rec of cert.kitaev_vs_coherent_audit.records) {
  const phi = rec.phi_over_pi * Math.PI;
  const cf = 0.5 * (1.0 - gamma * Math.max(Math.abs(Math.cos(phi)), Math.abs(Math.sin(phi))));
  if (Math.abs(rec.two_copy_kitaev_xy_error_explicit - cf) > 1e-12) {
    throw new Error("2-copy Kitaev error formula mismatch");
  }
}

console.log(JSON.stringify({
  status: "OK",
  kitaev2CopyPi4: cert.kitaev_vs_coherent_audit.records[2].two_copy_kitaev_xy_error_explicit,
  coherent1Copy: cert.kitaev_vs_coherent_audit.records[2].one_copy_coherent_feedforward_error
}));

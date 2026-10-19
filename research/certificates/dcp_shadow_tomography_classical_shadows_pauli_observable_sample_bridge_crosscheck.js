#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 140:
 * dcp_shadow_tomography_classical_shadows_pauli_observable_sample_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_shadow_tomography_classical_shadows_pauli_observable_sample_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_shadow_tomography_classical_shadows_pauli_observable_sample_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const mu = cert.shadow_vs_derandomized_sweep.true_expectation_mu;
for (const rec of cert.shadow_vs_derandomized_sweep.records) {
  const w = rec.weight_w;
  const expectedVar = Math.pow(3, w) - mu * mu;
  if (Math.abs(rec.shadow_variance_explicit - expectedVar) > 1e-11) {
    throw new Error(`Shadow variance mismatch at w=${w}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  w3Ratio: cert.shadow_vs_derandomized_sweep.records[2].sample_reduction_ratio_shadow_over_derand,
  w4Ratio: cert.shadow_vs_derandomized_sweep.records[3].sample_reduction_ratio_shadow_over_derand
}));

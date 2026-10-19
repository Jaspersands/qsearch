#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 121:
 * dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.twirling_carry_sweep.records) {
  const s = Math.abs(Math.sin(0.5 * rec.delta_rad));
  if (Math.abs(rec.coherent_trace_distance_explicit - s) > 1e-12 ||
      Math.abs(rec.twirled_trace_distance_explicit - s * s) > 1e-12) {
    throw new Error("Twirling squaring law mismatch");
  }
}

console.log(JSON.stringify({
  status: "OK",
  delta01Ratio: cert.twirling_carry_sweep.records[2].error_suppression_ratio_coh_over_twirl
}));

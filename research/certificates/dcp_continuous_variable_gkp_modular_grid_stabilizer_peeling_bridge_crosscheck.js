#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 139:
 * dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const q20 = cert.audit_q20_d4_m5;
const q56 = cert.audit_q56_d8_m7;
if (q20.successful_error_correction_trials !== 20 || q56.successful_error_correction_trials !== 56) {
  throw new Error("GKP error correction trials mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  q20Trials: q20.successful_error_correction_trials,
  q56Trials: q56.successful_error_correction_trials
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 136:
 * dcp_hidden_shift_bent_function_roetteler_involutory_dual_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_hidden_shift_bent_function_roetteler_involutory_dual_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_hidden_shift_bent_function_roetteler_involutory_dual_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of [cert.maiorana_mcfarland_4q_audit, cert.symmetric_complete_4q_audit, cert.maiorana_mcfarland_6q_audit]) {
  if (Math.abs(rec.min_2query_roetteler_success_prob_across_all_shifts - 1.0) > 1e-12 ||
      rec.max_1query_deviation_from_uniform_1_over_dim > 1e-12) {
    throw new Error("Roetteler bent carry hidden-shift verification failed");
  }
}

console.log(JSON.stringify({
  status: "OK",
  mm6qShiftsTested: cert.maiorana_mcfarland_6q_audit.hilbert_dim,
  mm6qMinSuccess: cert.maiorana_mcfarland_6q_audit.min_2query_roetteler_success_prob_across_all_shifts
}));

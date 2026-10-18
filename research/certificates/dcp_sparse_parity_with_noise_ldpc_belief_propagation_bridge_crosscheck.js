#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 92:
 * dcp_sparse_parity_with_noise_ldpc_belief_propagation_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_sparse_parity_with_noise_ldpc_belief_propagation.json"
);
// Handle exact filename
const actualPath = fs.existsSync(certPath)
  ? certPath
  : path.join(
      __dirname,
      "..",
      "reductions",
      "dcp_sparse_parity_with_noise_ldpc_belief_propagation_bridge.json"
    );
const cert = JSON.parse(fs.readFileSync(actualPath, "utf8"));

if (cert.theorem_id !== "dcp_sparse_parity_with_noise_ldpc_belief_propagation_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const sw = cert.ldpc_star_check_sweep;
for (const rec of sw) {
  const gExt = rec.gamma_partner * rec.gamma_check;
  const llrExt = 2.0 * Math.atanh(gExt);
  if (Math.abs(rec.single_check_extrinsic_llr - llrExt) > 1e-12) {
    throw new Error("Extrinsic LLR mismatch");
  }
  if (rec.max_bp_vs_exact_bayes_llr_error > 1e-12) {
    throw new Error("BP vs Bayes LLR error exceeded tolerance");
  }
}

console.log(JSON.stringify({
  status: "OK",
  errL0: sw[0].bp_map_error_prob,
  errL4: sw[4].bp_map_error_prob
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 135:
 * dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const tf = cert.tight_frame_3d_control;
const sf = cert.skewed_frame_3d_audit;
if (Math.abs(tf.anisotropy_inflation_factor - 1.0) > 1e-12 || sf.anisotropy_inflation_factor <= 1.40) {
  throw new Error("QFIM tight-frame vs skewed-frame check failed");
}

console.log(JSON.stringify({
  status: "OK",
  tightMSE: tf.trace_qfim_inverse_mse_bound,
  skewedMSE: sf.trace_qfim_inverse_mse_bound
}));

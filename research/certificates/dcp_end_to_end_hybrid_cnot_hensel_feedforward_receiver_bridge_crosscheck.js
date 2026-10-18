#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 100:
 * dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a2 = cert.audit_2d_mod16;
const a3 = cert.audit_3d_mod8;
if (a2.reconstruction_accuracy !== 1.0 || Math.abs(a2.min_stage_tv_bias_across_all_secrets_and_signs - a2.gamma) > 1e-12) {
  throw new Error("2D mod 16 end-to-end receiver check failed");
}
if (a3.reconstruction_accuracy !== 1.0 || Math.abs(a3.min_stage_tv_bias_across_all_secrets_and_signs - a3.gamma) > 1e-12) {
  throw new Error("3D mod 8 end-to-end receiver check failed");
}

console.log(JSON.stringify({
  status: "OK",
  secrets2D: a2.total_secrets_tested,
  secrets3D: a3.total_secrets_tested,
  acc2D: a2.reconstruction_accuracy,
  acc3D: a3.reconstruction_accuracy
}));

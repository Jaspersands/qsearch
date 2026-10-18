#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 113:
 * dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a6 = cert.iceberg_6_4_2_audit;
for (const rec of a6.records) {
  const p = rec.p_physical;
  const pAcc = 0.5 * (1.0 + Math.pow(1.0 - 2.0 * p, 6));
  if (Math.abs(rec.iceberg_accept_prob_explicit - pAcc) > 1e-12) {
    throw new Error("Iceberg [[6,4,2]] acceptance probability mismatch");
  }
}

console.log(JSON.stringify({
  status: "OK",
  p01Suppression: a6.records[2].error_suppression_factor
}));

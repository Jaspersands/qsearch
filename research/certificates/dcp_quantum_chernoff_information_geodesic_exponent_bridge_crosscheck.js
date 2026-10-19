#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 120:
 * dcp_quantum_chernoff_information_geodesic_exponent_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_chernoff_information_geodesic_exponent_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_chernoff_information_geodesic_exponent_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const gamma = cert.chernoff_exponent_sweep.gamma;
for (const rec of cert.chernoff_exponent_sweep.records) {
  const s2 = rec.sin_sq_half_delta_theta;
  const bQCB = 1.0 - (1.0 - Math.sqrt(1.0 - gamma * gamma)) * s2;
  if (Math.abs(rec.quantum_bhattacharyya_explicit - bQCB) > 1e-12) {
    throw new Error("Quantum Bhattacharyya formula mismatch");
  }
}

console.log(JSON.stringify({
  status: "OK",
  pi2Ratio: cert.chernoff_exponent_sweep.records[1].collective_exponent_ratio_qcb_over_sep,
  piRatio: cert.chernoff_exponent_sweep.records[3].collective_exponent_ratio_qcb_over_sep
}));

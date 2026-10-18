#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 101:
 * dcp_quantum_singular_value_transformation_pgm_chebyshev_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_singular_value_transformation_pgm_chebyshev_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_singular_value_transformation_pgm_chebyshev_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const c8 = cert.colliding_mod8_audit;
const p1 = c8.deg1_linear.conditional_qft_success;
const p3 = c8.deg3_qsvt.conditional_qft_success;
const p5 = c8.deg5_qsvt.conditional_qft_success;
const ceil = c8.rank_ceiling_R_over_Q;

if (!(p1 < p3 && p3 < p5 && p5 <= ceil + 1e-12)) {
  throw new Error("QSVT equalization hierarchy violated");
}
if (Math.abs(cert.flat_control_mod8.deg5_qsvt.conditional_qft_success - 1.0) > 1e-12) {
  throw new Error("Flat control QSVT mismatch");
}

console.log(JSON.stringify({ status: "OK", p1, p3, p5, ceil }));

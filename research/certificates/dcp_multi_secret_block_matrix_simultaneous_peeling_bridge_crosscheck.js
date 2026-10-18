#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 94:
 * dcp_multi_secret_block_matrix_simultaneous_peeling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_multi_secret_block_matrix_simultaneous_peeling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_multi_secret_block_matrix_simultaneous_peeling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const eq = cert.equal_secrets_control;
const piDiff = cert.pi_difference_control;
if (Math.abs(eq.x_expectation_b1_diff - Math.pow(eq.gamma, 2)) > 1e-12) {
  throw new Error("Equal secrets difference expectation mismatch");
}
if (Math.abs(piDiff.x_expectation_b1_diff - (-Math.pow(piDiff.gamma, 2))) > 1e-12) {
  throw new Error("Pi difference expectation mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  eqDiffX: eq.x_expectation_b1_diff,
  piDiffX: piDiff.x_expectation_b1_diff
}));

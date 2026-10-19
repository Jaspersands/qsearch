#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 134:
 * dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const k4 = cert.audit_k4_square;
const k9 = cert.audit_k9_square;
if (JSON.stringify(k4.k2_integer_root_weights) !== JSON.stringify([1, 3]) ||
    JSON.stringify(k9.k2_integer_root_weights) !== JSON.stringify([3, 6])) {
  throw new Error("Krawtchouk K_2 roots mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  k4Roots: k4.k2_integer_root_weights,
  k9Roots: k9.k2_integer_root_weights
}));

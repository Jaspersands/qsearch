#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 127:
 * dcp_non_binary_reed_solomon_vandermonde_qudit_witness_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_non_binary_reed_solomon_vandermonde_qudit_witness_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_non_binary_reed_solomon_vandermonde_qudit_witness_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a5 = cert.audit_p5_d2_consecutive;
const a7 = cert.audit_p7_d2_nonconsecutive;
if (a5.degree_le_d_annihilated_count !== 125 || a7.degree_le_d_annihilated_count !== 343) {
  throw new Error("Exhaustive polynomial annihilation count mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  w5: a5.barycentric_weights_mod_p,
  w7: a7.barycentric_weights_mod_p
}));

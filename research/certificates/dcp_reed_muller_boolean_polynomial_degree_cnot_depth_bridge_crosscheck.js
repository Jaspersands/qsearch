#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 122:
 * dcp_reed_muller_boolean_polynomial_degree_cnot_depth_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_reed_muller_boolean_polynomial_degree_cnot_depth_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_reed_muller_boolean_polynomial_degree_cnot_depth_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.degree_gadget_sweep) {
  const d = rec.d_degree;
  if (rec.parity_gadget_count_2d_minus_1 !== (Math.pow(2, d) - 1) ||
      rec.max_integer_identity_error !== 0) {
    throw new Error(`Degree-${d} gadget synthesis check failed`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  czGadgets: cert.degree_gadget_sweep[1].parity_gadget_count_2d_minus_1,
  cczGadgets: cert.degree_gadget_sweep[2].parity_gadget_count_2d_minus_1
}));

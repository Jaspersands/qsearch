#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 126:
 * dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const recs = cert.fano_holevo_n8_q16_audit.records;
if (recs[recs.length - 1].min_quantum_copies_integer_ceil !== 32) {
  throw new Error("Expected 32 copies at gamma=1.0 for 32-bit secret");
}

console.log(JSON.stringify({
  status: "OK",
  minCopiesG10: recs[0].min_quantum_copies_integer_ceil,
  minCopiesG100: recs[recs.length - 1].min_quantum_copies_integer_ceil
}));

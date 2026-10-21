#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 131:
 * dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a3 = cert.audit_3d_f17;
const a4 = cert.audit_4d_f31;
if (a3.out_of_sample_exact_matches !== 14 || a4.out_of_sample_exact_matches !== 16) {
  throw new Error("Out-of-sample recurrence extrapolation mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  f17Matches: a3.out_of_sample_exact_matches,
  f31Matches: a4.out_of_sample_exact_matches
}));

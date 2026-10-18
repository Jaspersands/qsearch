#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 102:
 * dcp_galois_frobenius_automorphism_prime_power_peeling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_galois_frobenius_automorphism_prime_power_peeling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_galois_frobenius_automorphism_prime_power_peeling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a4 = cert.audit_n4_q16;
const a8 = cert.audit_n8_q32;
if (!a4.midpoint_degree_n_over_2_annihilated || !a8.midpoint_degree_n_over_2_annihilated) {
  throw new Error("Midpoint degree n/2 annihilation failed");
}
if (a4.sum_with_conjugate[2] !== 0 || a8.sum_with_conjugate[4] !== 0) {
  throw new Error("Explicit midpoint coefficient non-zero");
}

console.log(JSON.stringify({
  status: "OK",
  sumConjN4: a4.sum_with_conjugate,
  sumConjN8Mid: a8.sum_with_conjugate[4]
}));

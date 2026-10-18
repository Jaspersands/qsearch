#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 108:
 * dcp_composite_crt_coprime_modulus_tensor_factorization_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_composite_crt_coprime_modulus_tensor_factorization_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_composite_crt_coprime_modulus_tensor_factorization_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of [cert.audit_q12_4x3, cert.audit_q24_8x3, cert.audit_q40_8x5]) {
  if ((rec.idempotent_e1 + rec.idempotent_e2) % rec.q_composite !== 1) {
    throw new Error("Bezout idempotent sum mismatch");
  }
  if (rec.max_s2_leakage_under_p_multiple_witness > 1e-12 ||
      rec.max_s1_leakage_under_2t_multiple_witness > 1e-12) {
    throw new Error("CRT factor annihilation leakage exceeded tolerance");
  }
}

console.log(JSON.stringify({
  status: "OK",
  q24_e1: cert.audit_q24_8x3.idempotent_e1,
  q24_e2: cert.audit_q24_8x3.idempotent_e2
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 109:
 * dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.carry_spectrum_sweep) {
  const m = rec.m_trees;
  const expectedH = (m % 2 === 0) ? m : (m - 1);
  if (Math.abs(rec.shannon_entropy_bits - expectedH) > 1e-12) {
    throw new Error(`Entropy mismatch at m=${m}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  m4Entropy: cert.carry_spectrum_sweep[2].shannon_entropy_bits,
  m5Entropy: cert.carry_spectrum_sweep[3].shannon_entropy_bits
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 117:
 * dcp_quantum_amplitude_amplification_grover_reflection_witness_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_amplitude_amplification_grover_reflection_witness_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_amplitude_amplification_grover_reflection_witness_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const w3 = cert.weight3_deterministic_k1;
const w4 = cert.weight4_boost_k1;
if (Math.abs(w3.amplified_syndrome_prob_explicit - 1.0) > 1e-12) {
  throw new Error("Weight-3 k=1 deterministic amplification failed");
}
if (Math.abs(w4.amplified_syndrome_prob_explicit - 25.0 / 32.0) > 1e-12) {
  throw new Error("Weight-4 k=1 amplification mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  w3ProbK1: w3.amplified_syndrome_prob_explicit,
  w4ProbK1: w4.amplified_syndrome_prob_explicit
}));

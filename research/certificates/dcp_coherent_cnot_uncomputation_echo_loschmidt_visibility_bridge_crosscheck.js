#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 106:
 * dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const gamma = cert.echo_vs_readout_sweep.gamma;
for (const rec of cert.echo_vs_readout_sweep.records) {
  const cf = Math.pow(gamma, 2) * Math.pow(Math.cos(rec.theta_0), 2);
  if (Math.abs(rec.x0_expectation_uncomputed_explicit - cf) > 1e-12) {
    throw new Error("Uncomputed echo formula mismatch");
  }
  if (Math.abs(rec.x0_expectation_given_d0_zero_sum - Math.pow(gamma, 2)) > 1e-12) {
    throw new Error("d_1=0 conditioned expectation mismatch");
  }
}

console.log(JSON.stringify({
  status: "OK",
  d0AtPiOver2: cert.echo_vs_readout_sweep.records[2].x0_expectation_given_d0_zero_sum,
  echoAtPiOver2: cert.echo_vs_readout_sweep.records[2].x0_expectation_uncomputed_explicit
}));

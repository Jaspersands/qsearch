#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 130:
 * dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const aIdle = cert.tree_vs_chain_sweep.alpha_idle;
for (const rec of cert.tree_vs_chain_sweep.records) {
  const h = rec.h_wires;
  const dLog = Math.round(Math.log2(h));
  const expectedGain = Math.exp(aIdle * h * (h - 1 - dLog));
  if (Math.abs(rec.visibility_gain_tree_over_chain - expectedGain) / expectedGain > 1e-12) {
    throw new Error(`Visibility gain mismatch at h=${h}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  h16Gain: cert.tree_vs_chain_sweep.records[3].visibility_gain_tree_over_chain
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 124:
 * dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.non_clifford_resource_sweep.records) {
  const m = rec.m_bits;
  if (rec.qft_fine_1q_rotations !== (m - 2) * (m - 1) ||
      rec.adaptive_peeling_fine_1q_rotations !== (m - 2)) {
    throw new Error(`Fine rotation count mismatch at m=${m}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  m32Reduction: cert.non_clifford_resource_sweep.records[4].fine_rotation_reduction_factor,
  m64Reduction: cert.non_clifford_resource_sweep.records[5].fine_rotation_reduction_factor
}));

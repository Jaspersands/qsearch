#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 137:
 * dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const recs = cert.ideal_wait_qram_sweep.records;
const d10 = recs.find(r => r.tree_depth_d === 10);
if (!d10 || d10.infidelity_reduction_ratio_fanout_over_bb <= 64.0) {
  throw new Error("Bucket-Brigade d=10 infidelity reduction check failed");
}

console.log(JSON.stringify({
  status: "OK",
  d10FidBB: d10.fidelity_bucket_brigade,
  d10FidFanout: d10.fidelity_fanout_decoder,
  d10Reduction: d10.infidelity_reduction_ratio_fanout_over_bb
}));

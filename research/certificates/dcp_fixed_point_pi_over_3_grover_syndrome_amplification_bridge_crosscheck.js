#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 118:
 * dcp_fixed_point_pi_over_3_grover_syndrome_amplification_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_fixed_point_pi_over_3_grover_syndrome_amplification_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_fixed_point_pi_over_3_grover_syndrome_amplification_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.pi_over_3_amplification_sweep.records) {
  const p0 = rec.p0;
  const expectedP1 = 1.0 - Math.pow(1.0 - p0, 3);
  if (Math.abs(rec.p1_pi_over_3_explicit - expectedP1) > 1e-12) {
    throw new Error(`pi/3 cubic law mismatch at p0=${p0}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  p1AtHalf: cert.pi_over_3_amplification_sweep.records[2].p1_pi_over_3_explicit,
  p2AtHalf: cert.pi_over_3_amplification_sweep.records[2].p2_recursive_pi_over_3
}));

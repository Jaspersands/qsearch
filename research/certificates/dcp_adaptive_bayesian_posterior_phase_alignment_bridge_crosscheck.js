#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 86:
 * dcp_adaptive_bayesian_posterior_phase_alignment_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_adaptive_bayesian_posterior_phase_alignment_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_adaptive_bayesian_posterior_phase_alignment_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const s1 = cert.stage1_mod8_audit;
if (s1.min_fixed_x_tv > 1e-12) {
  throw new Error("Expected fixed-X blind spot at s_low=1");
}
if (Math.abs(s1.min_adaptive_feedforward_tv - s1.gamma) > 1e-12) {
  throw new Error("Feedforward TV mismatch");
}
for (const rec of s1.prefix_records) {
  if (Math.abs(rec.sample_complexity_ratio_xy_over_feedforward - 2.0) > 1e-12) {
    throw new Error("Expected exact 2.0x sample complexity ratio");
  }
}

console.log(JSON.stringify({
  status: "OK",
  minFixedX: s1.min_fixed_x_tv,
  minFeedforward: s1.min_adaptive_feedforward_tv
}));

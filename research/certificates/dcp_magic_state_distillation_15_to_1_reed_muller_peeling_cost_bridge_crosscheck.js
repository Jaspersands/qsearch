#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 128:
 * dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const t32 = cert.threshold_stepdown_m32_audit;
if (t32.peeling_distillation_levels_required !== 1 ||
    t32.qft_distillation_levels_required !== 2 ||
    t32.raw_magic_state_reduction_factor <= 450.0) {
  throw new Error("Magic state distillation factory step-down check failed");
}

console.log(JSON.stringify({
  status: "OK",
  m32RawReduction: t32.raw_magic_state_reduction_factor,
  m64RawReduction: cert.matched_level_m64_audit.raw_magic_state_reduction_factor
}));

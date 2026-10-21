#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 129:
 * dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.bell_bitflip_immunity_sweep.records) {
  if (Math.abs(rec.xx_parity_expectation_explicit - 0.44) > 1e-12 ||
      Math.abs(rec.zz_detected_bitflip_rate - rec.eta_x) > 1e-12) {
    throw new Error(`Bell X-fault immunity check failed at eta_x=${rec.eta_x}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  xxAtEta05: cert.bell_bitflip_immunity_sweep.records[3].xx_parity_expectation_explicit
}));

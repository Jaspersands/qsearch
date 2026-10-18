#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 88:
 * dcp_noisy_syndrome_measurement_readout_bitflip_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_noisy_syndrome_measurement_readout_bitflip_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_noisy_syndrome_measurement_readout_bitflip_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const gamma = cert.readout_error_sweep.gamma;
for (const rec of cert.readout_error_sweep.records) {
  const eta = rec.eta;
  const visExp = (1.0 - 2.0 * eta) * gamma;
  if (Math.abs(rec.single_pair_visibility_unverified - visExp) > 1e-12) {
    throw new Error(`Single-pair visibility mismatch at eta=${eta}`);
  }
  const pAcc = Math.pow(1.0 - eta, 2) + Math.pow(eta, 2);
  const etaPost = Math.pow(eta, 2) / pAcc;
  if (Math.abs(rec.eta_post_selected - etaPost) > 1e-12) {
    throw new Error(`Post-selected eta mismatch at eta=${eta}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  eta05Post: cert.readout_error_sweep.records[2].eta_post_selected
}));

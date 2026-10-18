#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 114:
 * dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const u8 = cert.unit_drift_mod8_audit;
if (Math.abs(u8.static_time_averaged_x) > 1e-12 ||
    Math.abs(u8.velocity_tracked_time_averaged_x - u8.gamma) > 1e-12) {
  throw new Error("Drift tracking verification failed");
}

console.log(JSON.stringify({
  status: "OK",
  staticAvg: u8.static_time_averaged_x,
  trackedAvg: u8.velocity_tracked_time_averaged_x
}));

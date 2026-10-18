#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 98:
 * dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.rejection_sampling_sweep) {
  const P = rec.P_window_size;
  const lb = (P + 1.0) / (2.0 * P);
  if (rec.p_accept_sine_explicit < lb - 1e-12 || rec.p_accept_sine_explicit <= 0.5) {
    throw new Error(`Sine acceptance bound violated at P=${P}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  p31Accept: cert.rejection_sampling_sweep[4].p_accept_sine_explicit,
  p32Accept: cert.rejection_sampling_sweep[5].p_accept_sine_explicit
}));

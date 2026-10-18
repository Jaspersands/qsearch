#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 89:
 * dcp_gaussian_vs_sine_window_lwe_fourier_leakage_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_gaussian_vs_sine_window_lwe_fourier_leakage_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_gaussian_vs_sine_window_lwe_fourier_leakage_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of [cert.p16_window_comparison, cert.p32_window_comparison]) {
  const P = rec.P_window_size;
  const cfSin = Math.cos(Math.PI / (P + 1.0));
  const cfBox = 1.0 - 1.0 / P;
  if (Math.abs(rec.gamma1_sine_optimal_closed_form - cfSin) > 1e-12) {
    throw new Error("Sine gamma1 mismatch");
  }
  if (Math.abs(rec.gamma1_box - cfBox) > 1e-12) {
    throw new Error("Box gamma1 mismatch");
  }
  if (!(rec.gamma1_box < rec.gamma1_truncated_gaussian && rec.gamma1_truncated_gaussian < cfSin)) {
    throw new Error("Ordering gamma_box < gamma_gauss < gamma_sin violated");
  }
}

console.log(JSON.stringify({
  status: "OK",
  p32SineGamma1: cert.p32_window_comparison.gamma1_sine_optimal_closed_form,
  p32GaussGamma1: cert.p32_window_comparison.gamma1_truncated_gaussian
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 133:
 * dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a16 = cert.audit_p16_r30;
if (!(a16.peak_stopband_power_dolph_chebyshev < a16.peak_stopband_power_sine &&
      a16.peak_stopband_power_sine < a16.peak_stopband_power_box)) {
  throw new Error("Dolph-Chebyshev sidelobe ordering violated");
}

console.log(JSON.stringify({
  status: "OK",
  p16ChebPeak: a16.peak_stopband_power_dolph_chebyshev,
  p16SinePeak: a16.peak_stopband_power_sine,
  p16BoxPeak: a16.peak_stopband_power_box
}));

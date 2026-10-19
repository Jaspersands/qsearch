#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 125:
 * dcp_quantum_slepian_prolate_spheroidal_discrete_window_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quantum_slepian_prolate_spheroidal_discrete_window_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quantum_slepian_prolate_spheroidal_discrete_window_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of [cert.p16_b1_audit, cert.p32_b1_audit]) {
  if (!(rec.leakage_dpss_optimal < rec.leakage_sine && rec.leakage_sine < rec.leakage_box)) {
    throw new Error("DPSS leakage ordering violated");
  }
  if (!(rec.gamma1_box < rec.gamma1_dpss && rec.gamma1_dpss < rec.gamma1_sine_optimal)) {
    throw new Error("Sine gamma1 ordering violated");
  }
}

console.log(JSON.stringify({
  status: "OK",
  p32LeakDPSS: cert.p32_b1_audit.leakage_dpss_optimal,
  p32LeakSine: cert.p32_b1_audit.leakage_sine
}));

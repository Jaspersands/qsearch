#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 85:
 * dcp_coherent_multi_representative_amplitude_equalization_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_coherent_multi_representative_amplitude_equalization_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_coherent_multi_representative_amplitude_equalization_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.multiplicity_4_staircase_sweep) {
  const m = rec.M_representative_cap;
  const expected = Math.min(m, 4) / 4.0;
  if (Math.abs(rec.closed_form_m_rep_success - expected) > 1e-12) {
    throw new Error(`Staircase mismatch at M=${m}`);
  }
  if (Math.abs(rec.explicit_coherent_qft_success - expected) > 1e-12) {
    throw new Error(`Explicit QFT mismatch at M=${m}`);
  }
}

const vSweep = cert.variable_multiplicity_sweep;
const pM1 = 25.0 / 64.0;
const pM2 = Math.pow(2.0 + 3.0 * Math.sqrt(2.0), 2) / 64.0;
if (Math.abs(vSweep[0].closed_form_m_rep_success - pM1) > 1e-12) {
  throw new Error("M=1 variable multiplicity mismatch");
}
if (Math.abs(vSweep[1].closed_form_m_rep_success - pM2) > 1e-12) {
  throw new Error("M=2 variable multiplicity mismatch");
}

console.log(JSON.stringify({ status: "OK", pM1, pM2 }));

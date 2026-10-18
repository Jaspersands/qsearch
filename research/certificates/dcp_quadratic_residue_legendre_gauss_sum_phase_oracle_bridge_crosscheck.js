#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 104:
 * dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const p5 = cert.audit_p5_mod4_eq1;
const p7 = cert.audit_p7_mod4_eq3;
if (Math.abs(p5.residue_records[0].gauss_sum_real - Math.sqrt(5)) > 1e-11) {
  throw new Error("p=5 z=1 Gauss sum real part mismatch");
}
if (Math.abs(p7.residue_records[0].gauss_sum_imag - Math.sqrt(7)) > 1e-11) {
  throw new Error("p=7 z=1 Gauss sum imag part mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  g5_1: p5.residue_records[0].gauss_sum_real,
  g7_1_imag: p7.residue_records[0].gauss_sum_imag
}));

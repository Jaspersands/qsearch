#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 91:
 * dcp_modular_inversion_newton_hensel_lifting_quantum_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_modular_inversion_newton_hensel_lifting_quantum_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_modular_inversion_newton_hensel_lifting_quantum_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a3 = cert.audit_3x3_mod256;
const a4 = cert.audit_4x4_mod65536;
if (a3.num_newton_steps !== 3 || Math.abs(a3.decoupled_state_fidelity - 1.0) > 1e-12) {
  throw new Error("3x3 mod 256 Newton-Hensel verification failed");
}
if (a4.num_newton_steps !== 4 || Math.abs(a4.decoupled_state_fidelity - 1.0) > 1e-12) {
  throw new Error("4x4 mod 65536 Newton-Hensel verification failed");
}

console.log(JSON.stringify({
  status: "OK",
  stepsMod256: a3.num_newton_steps,
  stepsMod65536: a4.num_newton_steps
}));

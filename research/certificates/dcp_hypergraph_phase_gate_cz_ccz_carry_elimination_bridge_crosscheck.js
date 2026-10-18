#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 87:
 * dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const m4_2 = cert.mod4_m2_audit;
const m8_3 = cert.mod8_m3_audit;
if (Math.abs(m4_2.unrepaired_product_fidelity - 0.25) > 1e-12) {
  throw new Error("mod 4 m=2 unrepaired fidelity mismatch");
}
if (Math.abs(m4_2.deg2_only_repaired_product_fidelity - 1.0) > 1e-12) {
  throw new Error("mod 4 m=2 CZ-repaired fidelity mismatch");
}
if (Math.abs(m8_3.deg2_only_repaired_product_fidelity - 9.0 / 16.0) > 1e-12) {
  throw new Error("mod 8 m=3 deg2-only fidelity mismatch");
}
if (Math.abs(m8_3.full_hypergraph_repaired_product_fidelity - 1.0) > 1e-12) {
  throw new Error("mod 8 m=3 CCZ-repaired fidelity mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  mod4Unrepaired: m4_2.unrepaired_product_fidelity,
  mod8Deg2Only: m8_3.deg2_only_repaired_product_fidelity,
  mod8Full: m8_3.full_hypergraph_repaired_product_fidelity
}));

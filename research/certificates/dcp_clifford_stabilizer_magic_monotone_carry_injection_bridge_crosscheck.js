#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 95:
 * dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a3 = cert.audit_m3_qubits;
const m2T3 = Math.log2(4.0 / 3.0);
const m2CCZ = Math.log2(32.0 / 11.0);
if (a3.level_t1_mod2.stabilizer_renyi_2_magic_bits !== 0.0 ||
    a3.level_t2_mod4_cz_graph.stabilizer_renyi_2_magic_bits !== 0.0) {
  throw new Error("Expected zero magic at t=1 and t=2");
}
if (Math.abs(a3.level_t3_mod8_xor.stabilizer_renyi_2_magic_bits - m2T3) > 1e-12) {
  throw new Error("t=3 XOR magic mismatch");
}
if (Math.abs(a3.isolated_degree3_ccz_hypergraph.stabilizer_renyi_2_magic_bits - m2CCZ) > 1e-12) {
  throw new Error("CCZ magic mismatch");
}

console.log(JSON.stringify({ status: "OK", m2T3, m2CCZ }));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 105:
 * dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const d = cert.disjoint_tableau_audit;
for (const col of d.extracted_even_sublattice_columns) {
  for (const val of col) {
    if (val % 2 !== 0) {
      throw new Error("Extracted column entry is not even");
    }
  }
}

console.log(JSON.stringify({
  status: "OK",
  disjointCols: d.extracted_even_sublattice_columns
}));

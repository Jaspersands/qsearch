#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 97:
 * dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a = cert.audit_n4_q8;
if (!a.all_shifts_preserve_mod2_kernel || !a.all_shifts_equivariant_under_pauli_x_wrap_frame) {
  throw new Error("Shift orbit verification failed");
}

console.log(JSON.stringify({
  status: "OK",
  baseEvenVec: a.base_even_sublattice_vector,
  wrapShiftVec: a.shift_records[3].rectified_even_sublattice_vector
}));

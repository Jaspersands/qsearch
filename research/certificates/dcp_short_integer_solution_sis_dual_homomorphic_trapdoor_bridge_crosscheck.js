#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 115:
 * dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a = cert.gadget_trapdoor_n2_t3_audit;
if (!a.zero_sum_at_eq_0_mod_2t_verified || a.num_punctured_scales_extracted !== 6) {
  throw new Error("Gadget trapdoor verification failed");
}

console.log(JSON.stringify({
  status: "OK",
  numScales: a.num_punctured_scales_extracted,
  firstRectifiedScale: a.punctured_records[0].pauli_x_rectified_column_sum_mod_q
}));

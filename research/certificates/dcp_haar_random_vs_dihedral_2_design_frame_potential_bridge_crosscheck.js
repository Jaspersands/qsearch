#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 112:
 * dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const fb = cert.flat_bijection_audit;
const col = cert.colliding_instance_audit;
if (Math.abs(fb.f2_dihedral_explicit - 0.5 * fb.additive_energy_E4) > 1e-9 || fb.additive_energy_E4 !== 512) {
  throw new Error("Flat bijection E4 / F2 mismatch");
}
if (Math.abs(col.f2_dihedral_explicit - 0.5 * col.additive_energy_E4) > 1e-9 || col.additive_energy_E4 <= 512) {
  throw new Error("Colliding instance E4 / F2 mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  f2Flat: fb.f2_dihedral_explicit,
  f2Colliding: col.f2_dihedral_explicit
}));

// Independent Node.js crosscheck for Subsystem 155: Surface Code Lattice Surgery CNOT
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

const d7 = cert.distance_scaling_sweep.find(r => r.code_distance_d === 7);
if (d7.three_patch_cnot_footprint_qubits !== 3 * 49 || d7.syndrome_rounds_per_logical_cnot !== 14) {
  throw new Error("Distance-7 lattice surgery resource counts mismatch");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 155 certificate checks failed");
}
console.log("Subsystem 155 JS crosscheck PASSED");

// Independent Node.js crosscheck for Subsystem 154: Schur-Weyl Dicke Symmetric Subspace
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_representation_theory_schur_weyl_symmetric_subspace_permutation_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

const k20 = cert.qubit_dicke_sweep.find(r => r.copies_k === 20);
if (k20.full_tensor_hilbert_dim !== 1048576 || k20.symmetric_subspace_dim !== 21) {
  throw new Error("Schur-Weyl K=20 dimensions mismatch in JS");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 154 certificate checks failed");
}
console.log("Subsystem 154 JS crosscheck PASSED");

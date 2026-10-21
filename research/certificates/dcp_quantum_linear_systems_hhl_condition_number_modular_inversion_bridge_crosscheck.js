// Independent Node.js crosscheck for Subsystem 143: HHL Condition Number vs Modular Inversion
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

const phi = (1.0 + Math.sqrt(5.0)) / 2.0;
if (Math.abs(cert.shear_matrix_case.condition_number_kappa - phi * phi) > 1e-9) {
  throw new Error("Shear matrix condition number mismatch");
}
// For [[1, 5], [1, 6]], Tr(H^T H) = 1 + 25 + 1 + 36 = 63, det = 1
const tr = 63.0;
const disc = Math.sqrt(tr * tr - 4.0);
const kappaExpected = Math.sqrt((tr + disc) / (tr - disc));
if (Math.abs(cert.ill_conditioned_unimodular_case.condition_number_kappa - kappaExpected) > 1e-9) {
  throw new Error("Ill-conditioned unimodular kappa mismatch");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 143 certificate checks failed");
}
console.log("Subsystem 143 JS crosscheck PASSED");

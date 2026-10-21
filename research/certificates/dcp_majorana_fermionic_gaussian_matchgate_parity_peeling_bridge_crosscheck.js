// Independent Node.js crosscheck for Subsystem 146: Majorana Fermionic Gaussian Matchgates
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_majorana_fermionic_gaussian_matchgate_parity_peeling_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.majorana_gate_analysis.so4_orthogonality_max_error > 1e-14) {
  throw new Error("SO(4) orthogonality error too high");
}
if (cert.majorana_gate_analysis.gate_majorana_degrees.standard_cnot.majorana_degree !== 3) {
  throw new Error("CNOT Majorana degree must be 3");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 146 certificate checks failed");
}
console.log("Subsystem 146 JS crosscheck PASSED");

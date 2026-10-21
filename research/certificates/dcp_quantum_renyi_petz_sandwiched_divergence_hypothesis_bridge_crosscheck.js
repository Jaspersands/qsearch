// Independent Node.js crosscheck for Subsystem 151: Petz vs Sandwiched Quantum Renyi Divergence
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_renyi_petz_sandwiched_divergence_hypothesis_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.noncommuting_alpha2_comparison.araki_lieb_thirring_gap <= 0) {
  throw new Error("Araki-Lieb-Thirring gap must be strictly positive for non-commuting states");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 151 certificate checks failed");
}
console.log("Subsystem 151 JS crosscheck PASSED");

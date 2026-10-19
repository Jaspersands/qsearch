// Independent Node.js crosscheck for Subsystem 147: Quantum Wasserstein W_1 Cooling
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_wasserstein_ornstein_uhlenbeck_cooling_dissipative_peeling_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

for (const row of cert.cooling_trajectory) {
  const expectedW1 = 16.0 * 0.25 * Math.exp(-row.gamma_t);
  if (Math.abs(row.quantum_wasserstein_w1 - expectedW1) > 1e-12) {
    throw new Error("W_1 contraction mismatch in JS crosscheck");
  }
  if (row.quantum_wasserstein_w1 < row.trace_distance_t - 1e-12 || row.quantum_wasserstein_w1 > 16.0 * row.trace_distance_t + 1e-12) {
    throw new Error("De Palma sandwich inequality failed");
  }
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 147 certificate checks failed");
}
console.log("Subsystem 147 JS crosscheck PASSED");

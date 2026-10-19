// Independent Node.js crosscheck for Subsystem 149: Distributed Teleportation & BBPSSW CNOT Peeling
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_network_distributed_teleportation_bell_pair_cnot_peeling_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

function bbpssw(F) {
  const r = (1.0 - F) / 3.0;
  return (F * F + r * r) / (F * F + 2.0 * F * r + 5.0 * r * r);
}

if (Math.abs(cert.distillation_sweep[1].link_bell_fidelity - bbpssw(0.85)) > 1e-12) {
  throw new Error("BBPSSW 1-round fidelity mismatch in JS crosscheck");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 149 certificate checks failed");
}
console.log("Subsystem 149 JS crosscheck PASSED");

// Independent Node.js crosscheck for Subsystem 141: Quantum Ziv-Zakai Phase Lower Bound
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

function fid(h, v) {
  const s = Math.sin(0.5 * h);
  return 1.0 - v * v * s * s;
}

if (Math.abs(fid(Math.PI / 3.0, 1.0) - 0.75) > 1e-12) {
  throw new Error("Fidelity identity failed at h = pi/3");
}

const priorVar = (Math.PI * Math.PI) / 12.0;
if (Math.abs(cert.prior_variance_pi_sq_over_12 - priorVar) > 1e-12) {
  throw new Error("Prior variance mismatch");
}

// Recompute QZZB at K=4, v=0.85 with 400 midpoint bins
const N = 400;
const W = Math.PI;
const dh = W / N;
let integral = 0.0;
for (let i = 0; i < N; i++) {
  const h = (i + 0.5) * dh;
  const fK = Math.pow(fid(h, 0.85), 4);
  const pe = 0.5 * (1.0 - Math.sqrt(Math.max(0.0, 1.0 - fK)));
  integral += 0.5 * h * (1.0 - h / W) * (2.0 * pe) * dh;
}
const rowK4 = cert.dephased_v085_Info ? null : cert.dephased_v085_sweep.find(r => r.copies_k === 4);
if (!rowK4 || Math.abs(rowK4.qzzb_mse - integral) > 1e-9) {
  throw new Error("QZZB quadrature mismatch at K=4");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate checks did not all pass");
}
console.log("Subsystem 141 JS crosscheck PASSED");

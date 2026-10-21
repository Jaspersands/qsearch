// Independent Node.js crosscheck for Subsystem 145: Quantum Stein's Lemma & Umegaki Relative Entropy
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

function umegaki(v1, v0, theta) {
  const p1p = 0.5 * (1 + v1);
  const p1m = 0.5 * (1 - v1);
  const ent1 = p1p * Math.log(p1p) + p1m * Math.log(p1m);
  const cross = 0.5 * Math.log(0.25 * (1 - v0 * v0)) + 0.5 * v1 * Math.cos(theta) * Math.log((1 + v0) / (1 - v0));
  return ent1 - cross;
}

const r0 = cert.visibility_sweep[0];
if (Math.abs(r0.stein_exponent_d_rel - umegaki(0.92, 0.10, 0.0)) > 1e-12) {
  throw new Error("Umegaki relative entropy mismatch in JS crosscheck");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 145 certificate checks failed");
}
console.log("Subsystem 145 JS crosscheck PASSED");

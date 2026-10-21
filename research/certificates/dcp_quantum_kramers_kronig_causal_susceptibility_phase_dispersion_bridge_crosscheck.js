// Independent Node.js crosscheck for Subsystem 153: Kramers-Kronig Causal Susceptibility
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

for (const c of cert.kramers_kronig_quadrature_checks) {
  const exact = -c.detuning_delta / (c.detuning_delta * c.detuning_delta + c.gamma * c.gamma);
  if (Math.abs(c.chi_real_analytic - exact) > 1e-12 || c.absolute_error >= 2e-3) {
    throw new Error("Kramers-Kronig check failed in JS");
  }
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 153 certificate checks failed");
}
console.log("Subsystem 153 JS crosscheck PASSED");

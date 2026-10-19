// Independent Node.js crosscheck for Subsystem 156: Bernstein-Vazirani Carry Dilution
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (Math.abs(cert.peeled_zero_carry_case.target_bv_probability - 1.0) > 1e-14) {
  throw new Error("Peeled BV probability must equal 1.0");
}
if (Math.abs(cert.quadratic_and_carry_case.target_bv_probability - 0.25) > 1e-14) {
  throw new Error("Quadratic AND carry BV probability must equal 0.25");
}
if (Math.abs(cert.bent_cascade_carry_case.target_bv_probability - 0.0625) > 1e-14) {
  throw new Error("Bent carry BV probability must equal 1/16 = 0.0625");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 156 certificate checks failed");
}
console.log("Subsystem 156 JS crosscheck PASSED");

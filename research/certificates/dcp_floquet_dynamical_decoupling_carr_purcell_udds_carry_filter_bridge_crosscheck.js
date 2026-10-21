// Independent Node.js crosscheck for Subsystem 144: Dynamical Decoupling Filter Functions
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

function uddFilter(N, x) {
  let re = 1.0 + Math.pow(-1, N + 1) * Math.cos(x);
  let im = Math.pow(-1, N + 1) * Math.sin(x);
  for (let j = 1; j <= N; j++) {
    const tj = Math.pow(Math.sin((Math.PI * j) / (2 * N + 2)), 2);
    const sign = Math.pow(-1, j);
    re += 2.0 * sign * Math.cos(x * tj);
    im += 2.0 * sign * Math.sin(x * tj);
  }
  return re * re + im * im;
}

const row3 = cert.low_frequency_sweep.find(r => r.num_pulses_n === 3);
if (Math.abs(row3.udd_filter_value - uddFilter(3, 0.2)) > 1e-12) {
  throw new Error("UDD_3 filter value mismatch in JS crosscheck");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 144 certificate checks failed");
}
console.log("Subsystem 144 JS crosscheck PASSED");

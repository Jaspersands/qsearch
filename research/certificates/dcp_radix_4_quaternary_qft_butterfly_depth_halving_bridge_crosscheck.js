#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 119:
 * dcp_radix_4_quaternary_qft_butterfly_depth_halving_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_radix_4_quaternary_qft_butterfly_depth_halving_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_radix_4_quaternary_qft_butterfly_depth_halving_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const y4 = cert.quaternary_exact_y4_audit;
const y5 = cert.general_odd_y5_audit;
if (Math.abs(y4.prob_radix4_band1_local_qft4_blocks - 1.0) > 1e-12 ||
    Math.abs(y4.prob_radix2_band1_hadamard_only - 0.5) > 1e-12) {
  throw new Error("y=4 radix-4 vs radix-2 band-1 check failed");
}
if (!(y5.prob_radix4_band1_local_qft4_blocks > y5.prob_radix2_band1_hadamard_only)) {
  throw new Error("y=5 radix-4 band-1 dominance check failed");
}

console.log(JSON.stringify({
  status: "OK",
  y4Rad4: y4.prob_radix4_band1_local_qft4_blocks,
  y5Rad4: y5.prob_radix4_band1_local_qft4_blocks,
  y5Rad2: y5.prob_radix2_band1_hadamard_only
}));

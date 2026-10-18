#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 103:
 * dcp_multi_level_richardson_extrapolation_dephasing_mitigation_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_multi_level_richardson_extrapolation_dephasing_mitigation_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_multi_level_richardson_extrapolation_dephasing_mitigation_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const recs = cert.low_noise_audit.order_records;
for (let m = 0; m < recs.length; m++) {
  const expectedL1 = Math.pow(2, m + 1) - 1;
  if (Math.abs(recs[m].l1_weight_norm - expectedL1) > 1e-11) {
    throw new Error(`L1 norm mismatch at M=${m}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  biasM0: recs[0].absolute_bias,
  biasM2: recs[2].absolute_bias,
  biasM3: recs[3].absolute_bias
}));

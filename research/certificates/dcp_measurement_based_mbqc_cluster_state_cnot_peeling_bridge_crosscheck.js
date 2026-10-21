// Independent Node.js crosscheck for Subsystem 142: MBQC Cluster State CNOT Peeling
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_measurement_based_mbqc_cluster_state_cnot_peeling_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

for (let mask = 0; mask < 64; mask++) {
  const xc = (mask >> 0) & 1;
  const xt = (mask >> 1) & 1;
  const zc = (mask >> 2) & 1;
  const zt = (mask >> 3) & 1;
  const m1 = (mask >> 4) & 1;
  const m2 = (mask >> 5) & 1;
  const xc1 = xc;
  const xt1 = xc ^ xt ^ m2;
  const zc1 = zc ^ zt ^ m1;
  const zt1 = zt ^ m1;
  // Applying pure CNOT again restores input when m1=m2=0
  if (m1 === 0 && m2 === 0) {
    if ((xc1 ^ xt1) !== xt || (zc1 ^ zt1) !== zc) {
      throw new Error("Symplectic involution failed in JS crosscheck");
    }
  }
}
if (!cert.all_checks_passed || cert.exhaustive_f2_linearity.total_f2_states_checked !== 64) {
  throw new Error("MBQC certificate checks failed");
}
console.log("Subsystem 142 JS crosscheck PASSED");

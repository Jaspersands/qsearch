// Independent Node.js crosscheck for Subsystem 152: Expander Graph Ramanujan & Tanner Audit
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

const d10 = cert.ramanujan_degree_sweep.find(r => r.degree_d === 10);
if (Math.abs(d10.ramanujan_lambda2_bound - 6.0) > 1e-12) {
  throw new Error("Ramanujan bound at d=10 must equal 2*sqrt(9) = 6");
}
if (cert.peeling_decoding_threshold_certified !== false || cert.ramanujan_degree_sweep.some(r => r.guarantees_linear_time_peeling)) {
  throw new Error("Naive Tanner bound must not claim a linear-time peeling threshold");
}
if (!cert.all_checks_passed) {
  throw new Error("Subsystem 152 certificate checks failed");
}
console.log("Subsystem 152 JS crosscheck PASSED");

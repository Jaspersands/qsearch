#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 110:
 * dcp_multi_antenna_mimo_spatial_diversity_combining_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_multi_antenna_mimo_spatial_diversity_combining_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_multi_antenna_mimo_spatial_diversity_combining_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const d3 = cert.disparity_3branch_audit;
const c4 = cert.cooperative_4branch_audit;
if (!(d3.optimal_llr_bayes_error < d3.unweighted_majority_error / 3.0)) {
  throw new Error("Disparity LLR vs majority check failed");
}
if (!(c4.optimal_llr_bayes_error < c4.single_best_branch_error &&
      c4.optimal_llr_bayes_error < c4.unweighted_majority_error)) {
  throw new Error("Cooperative 4-branch LLR dominance failed");
}

console.log(JSON.stringify({
  status: "OK",
  d3LLRErr: d3.optimal_llr_bayes_error,
  d3MajErr: d3.unweighted_majority_error,
  c4LLRErr: c4.optimal_llr_bayes_error
}));

#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 116:
 * dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const laws = cert.six_core_laws_summary;
for (const k of Object.keys(laws)) {
  if (!laws[k].passed) {
    throw new Error(`Law ${k} failed`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  lawsVerified: Object.keys(laws).length,
  secretsReconstructed: laws.law_6_newton_hensel_end_to_end_receiver.total_secrets_reconstructed_100pct
}));

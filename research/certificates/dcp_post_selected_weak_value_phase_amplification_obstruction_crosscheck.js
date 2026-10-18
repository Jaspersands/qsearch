#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 96:
 * dcp_post_selected_weak_value_phase_amplification_obstruction
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_post_selected_weak_value_phase_amplification_obstruction.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_post_selected_weak_value_phase_amplification_obstruction") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const qfi = cert.weak_value_fisher_audit.quantum_fisher_info_bound;
for (const rec of cert.weak_value_fisher_audit.records) {
  if (rec.net_per_copy_post_selected_fisher_info > qfi + 1e-12) {
    throw new Error("Post-selected net Fisher info exceeded QFI bound");
  }
  if (Math.abs(rec.net_per_copy_post_selected_fisher_info + rec.discarded_accept_reject_fisher_info - rec.total_3outcome_fisher_info) > 1e-12) {
    throw new Error("Fisher chain rule violated");
  }
}

console.log(JSON.stringify({
  status: "OK",
  weakNetFisher: cert.weak_value_fisher_audit.records[0].net_per_copy_post_selected_fisher_info,
  qfiBound: qfi
}));

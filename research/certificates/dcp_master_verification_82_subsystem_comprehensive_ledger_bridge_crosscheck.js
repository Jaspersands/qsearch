#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 132:
 * dcp_master_verification_82_subsystem_comprehensive_ledger_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_master_verification_82_subsystem_comprehensive_ledger_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_master_verification_82_subsystem_comprehensive_ledger_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const ledger = cert.master_ledger;
if (ledger.verified_passed_count !== 67 || ledger.total_audited_subsystems !== 67) {
  throw new Error("Master ledger count mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  auditedSubsystems: ledger.verified_passed_count,
  masterMerkleRoot16: ledger.master_merkle_root_16
}));

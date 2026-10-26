// Independent Node.js crosscheck for Subsystem 150: Centennial 100-Subsystem Integration Audit
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_centennial_100_subsystem_master_audit_and_completeness_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));
const cpPath = path.join(__dirname, "..", "..", ".research_checkpoint.json");
const cp = JSON.parse(fs.readFileSync(cpPath, "utf8"));

if (cp.completed_subsystems.length < 100 || cert.total_verified_subsystems !== 100) {
  throw new Error("Expected 100-subsystem centennial slice in Centennial audit");
}
if (cert.independent_mathematical_review_certified_by_hashes !== false || cert.integration_audit_only_not_proof_verification !== true) {
  throw new Error("Centennial audit must separate integration counts from mathematical review");
}
const pillarSum = Object.values(cert.ten_pillar_taxonomy_counts).reduce((a, b) => a + b, 0);
if (pillarSum !== 100 || !cert.all_checks_passed) {
  throw new Error("Centennial audit checks failed in JS");
}
console.log("Subsystem 150 JS crosscheck PASSED");

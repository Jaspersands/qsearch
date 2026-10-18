#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 99:
 * dcp_bipartite_entanglement_entropy_syndrome_cut_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_bipartite_entanglement_entropy_syndrome_cut_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_bipartite_entanglement_entropy_syndrome_cut_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

if (Math.abs(cert.separable_control.purity_closed_form - 1.0) > 1e-12) {
  throw new Error("Separable control purity mismatch");
}
if (Math.abs(cert.maximal_bell_control.purity_closed_form - 0.5) > 1e-12) {
  throw new Error("Maximal Bell control purity mismatch");
}
if (Math.abs(cert.partial_entanglement_audit.purity_closed_form - 0.625) > 1e-12) {
  throw new Error("Partial entanglement purity mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  pSep: cert.separable_control.purity_closed_form,
  pBell: cert.maximal_bell_control.purity_closed_form,
  pPart: cert.partial_entanglement_audit.purity_closed_form
}));

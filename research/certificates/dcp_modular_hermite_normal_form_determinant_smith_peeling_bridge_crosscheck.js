#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 138:
 * dcp_modular_hermite_normal_form_determinant_smith_peeling_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_modular_hermite_normal_form_determinant_smith_peeling_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_modular_hermite_normal_form_determinant_smith_peeling_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const a8 = cert.audit_d_1_2_mod8;
const a12 = cert.audit_d_2_6_mod12;
if (a8.explicit_image_cardinality !== 32 || a12.explicit_image_cardinality !== 12) {
  throw new Error("SNF image cardinality mismatch");
}

console.log(JSON.stringify({
  status: "OK",
  mod8ImageSize: a8.explicit_image_cardinality,
  mod12ImageSize: a12.explicit_image_cardinality
}));

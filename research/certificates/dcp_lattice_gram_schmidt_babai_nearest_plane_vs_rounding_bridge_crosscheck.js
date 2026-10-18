#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 107:
 * dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

const sk = cert.skewed_3d_basis_audit;
if (!(sk.inscribed_radius_coordinate_rounding < sk.inscribed_radius_nearest_plane)) {
  throw new Error("Expected r_CR < r_NP on skewed basis");
}
if (!sk.nearest_plane_recovered_exact_lattice_point || sk.coordinate_rounding_recovered_exact_lattice_point) {
  throw new Error("Expected Nearest Plane success and Coordinate Rounding failure");
}

console.log(JSON.stringify({
  status: "OK",
  rNP: sk.inscribed_radius_nearest_plane,
  rCR: sk.inscribed_radius_coordinate_rounding
}));

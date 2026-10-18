#!/usr/bin/env node
/**
 * Independent Node.js cross-check for Subsystem 90:
 * dcp_non_abelian_wreath_product_pair_swap_commutant_bridge
 */
const fs = require("fs");
const path = require("path");

const certPath = path.join(
  __dirname,
  "..",
  "reductions",
  "dcp_non_abelian_wreath_product_pair_swap_commutant_bridge.json"
);
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

if (cert.theorem_id !== "dcp_non_abelian_wreath_product_pair_swap_commutant_bridge") {
  throw new Error("Invalid theorem_id");
}
if (!cert.all_checks_passed) {
  throw new Error("Certificate all_checks_passed is false");
}

for (const rec of cert.wreath_pair_sweep) {
  const M = rec.M_pairs;
  const sumDims = rec.wreath_sector_dimensions.reduce((a, b) => a + b, 0);
  if (sumDims !== Math.pow(4, M)) {
    throw new Error(`Dimension sum mismatch at M=${M}`);
  }
  if (!(rec.tv_global_sym2m > rec.tv_binomial_singlet + 1e-6)) {
    throw new Error(`Expected Sym^{2M} > Binomial singlet at M=${M}`);
  }
}

console.log(JSON.stringify({
  status: "OK",
  m3SingletTV: cert.wreath_pair_sweep[2].tv_binomial_singlet,
  m3Sym6TV: cert.wreath_pair_sweep[2].tv_global_sym2m
}));

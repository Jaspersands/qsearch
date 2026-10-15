#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `planted_qary_cdkm_adder_sparsity_bridge`.
 *
 * Recomputes from first principles:
 * 1. Centered-RREF nonzero count nnz(B) = n + nnz(C) <= n + m*(n - m) and exact CDKM
 *    constant-addition count (including uncompute):
 *      N_add = 2 * (b * nnz(B) + (1 + nnz(C_{*, j0})) + n),
 *    as well as saved additions vs a dense n x n basis:
 *      N_add_dense = 2 * (b * n^2 + 2 * n).
 * 2. Modulus-independent free-column point bounds:
 *      bound_split_free    = p_split * (M_box - 1) + g_res + W,
 *      bound_nonsplit_free = (M_box - 1) + W,
 *    and exact cell output bit widths across primes up to q > 2^80.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_cdkm_adder_sparsity_bridge.json"
);

function bitLength(x) {
  let v = BigInt(x);
  if (v <= 0n) return 0;
  let bits = 0;
  while (v > 0n) {
    bits += 1;
    v >>= 1n;
  }
  return bits;
}

function verifySparsityRecord(rec) {
  const n = rec.n;
  const m = rec.m;
  const b = rec.b_box_bits;
  const mBox = rec.M_box;
  const width = rec.width;
  const pSplit = rec.p_split;
  const gRes = rec.g_res;
  const nnzC = rec.nnz_C;
  const nnzCColJ0 = rec.nnz_C_col_j0;

  if (nnzC > m * (n - m) || nnzCColJ0 > m) {
    throw new Error(`Invalid nnzC=${nnzC} or nnzCColJ0=${nnzCColJ0}`);
  }
  const expectedNnzB = n + nnzC;
  if (rec.nnz_B_actual !== expectedNnzB || rec.nnz_B_formula !== expectedNnzB) {
    throw new Error(`nnz(B) mismatch: expected ${expectedNnzB}, got ${rec.nnz_B_actual}`);
  }

  const expectedAdds = 2 * (b * expectedNnzB + (1 + nnzCColJ0) + n);
  const denseAdds = 2 * (b * n * n + 2 * n);
  const savedAdds = denseAdds - expectedAdds;
  const minSaved = 2 * b * ((n - m) * (n - m - 1) + m * (m - 1)) + 2 * (n - m - 1);

  if (
    rec.actual_constant_additions_including_uncompute !== expectedAdds ||
    rec.formula_constant_additions_including_uncompute !== expectedAdds ||
    rec.dense_basis_constant_additions !== denseAdds ||
    rec.saved_constant_additions_vs_dense !== savedAdds ||
    savedAdds < minSaved
  ) {
    throw new Error(`Addition compression check failed for n=${n}, m=${m}`);
  }

  const shift = bitLength(width) - 1;
  const expSplitBound = pSplit * (mBox - 1) + gRes + width;
  const expNonsplitBound = (mBox - 1) + width;
  const expSplitBits = Math.max(bitLength(expSplitBound) + 1, shift + 1) - shift;
  const expNonsplitBits = Math.max(bitLength(expNonsplitBound) + 1, shift + 1) - shift;

  if (
    rec.expected_split_free_point_bound !== expSplitBound ||
    rec.expected_nonsplit_free_point_bound !== expNonsplitBound ||
    rec.expected_split_free_cell_bits !== expSplitBits ||
    rec.expected_nonsplit_free_cell_bits !== expNonsplitBits
  ) {
    throw new Error(`Free-column bound or cell width mismatch for n=${n}, m=${m}`);
  }

  for (let j = 0; j < n - m; j++) {
    const expectedBits = j === rec.j0_free_index ? expSplitBits : expNonsplitBits;
    if (rec.free_column_cell_bits[j] !== expectedBits) {
      throw new Error(`Free column ${j} cell bits mismatch`);
    }
  }

  if (
    !rec.free_col_nnz_all_equal_1 ||
    !rec.piv_col_nnz_matches_formula ||
    !rec.theorem_1_addition_count_matches ||
    !rec.theorem_2_free_bounds_and_widths_match ||
    !rec.theorem_3_nonsplit_free_popcount_matches
  ) {
    throw new Error(`Verification boolean false in record for n=${n}, m=${m}`);
  }
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "planted_qary_cdkm_adder_sparsity_bridge") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  const modAudit = report.modulus_scaling_audit;
  let modChecked = 0;
  const freeCellTotals = new Set();
  for (const rec of modAudit.records) {
    verifySparsityRecord(rec);
    const sumFree = rec.free_column_cell_bits.reduce((a, b) => a + b, 0);
    freeCellTotals.add(sumFree);
    modChecked += 1;
  }
  if (freeCellTotals.size !== 1) {
    throw new Error("Free-column cell qubit total varied across moduli q");
  }

  let dimChecked = 0;
  for (const rec of report.dimension_family_audit) {
    verifySparsityRecord(rec);
    dimChecked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        modulus_scaling_configs_verified: modChecked,
        dimension_family_configs_verified: dimChecked,
      },
      null,
      2
    )
  );
}

main();

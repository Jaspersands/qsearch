#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = process.argv[2] || path.join(
  ROOT,
  "research",
  "phase_workbench",
  "dcp_interleaved_tree_merge_syndrome_pruning_audit.json"
);

function gcdBigInt(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function fracStr(num, den) {
  const g = gcdBigInt(num, den);
  return `${num / g}/${den / g}`;
}

function verifyCase(c) {
  const [pNumStr, pDenStr] = c.p_err_exact.split("/");
  const pNum = BigInt(pNumStr);
  const pDen = BigInt(pDenStr);

  // K(0) = 1 - p = (pDen - pNum) / pDen, K(1) = K(q-1) = p / 2 = pNum / (2*pDen)
  const k0Num = pDen - pNum;
  const k0Den = pDen;
  const k1Num = pNum;
  const k1Den = 2n * pDen;

  // Step 1 acceptance: (1-p)^2 + p^2 / 2
  const acc1Num = 2n * k0Num * k0Num + pNum * pNum;
  const acc1Den = 2n * pDen * pDen;
  const acc1Str = fracStr(acc1Num, acc1Den);
  if (c.step1_acceptance_exact !== acc1Str) {
    throw new Error(
      `Case ${c.case_id}: step1_acceptance_exact mismatch (${c.step1_acceptance_exact} vs ${acc1Str})`
    );
  }

  // Verify regime
  if (pNum===0n || pNum===pDen) {
    if(c.expected_purification_regime!=="ENDPOINT_NEUTRAL" || Math.abs(c.step1_visibility_gain)>1e-12)throw new Error("endpoint must be neutral");
  } else if (3n * pNum < 2n * pDen && !(c.step1_visibility_gain > 0)) {
    throw new Error(`Case ${c.case_id}: expected purifying gain > 0`);
  }
  if (3n * pNum === 2n * pDen && Math.abs(c.step1_visibility_gain) > 1e-12) {
    throw new Error(`Case ${c.case_id}: expected neutral gain == 0 at p=2/3`);
  }
  if (pNum!==pDen && 3n * pNum > 2n * pDen && !(c.step1_visibility_gain < 0)) {
    throw new Error(`Case ${c.case_id}: expected degrading gain < 0`);
  }

  for (const row of c.depth_rows) {
    const L = row.depth_L;
    const K = BigInt(row.k_leaves);
    // Moment sum S_{2^L} = (1-p)^K + 2*(p/2)^K
    const sNum = (2n ** K) * (k0Num ** K) + 2n * (pNum ** K);
    const sDen = (2n ** K) * (pDen ** K);
    const sStr = fracStr(sNum, sDen);

    if (row.telescoping_product_survival_exact !== sStr) {
      throw new Error(
        `Case ${c.case_id}, L=${L}: telescoping_product_survival_exact mismatch`
      );
    }
    if (row.moment_sum_survival_exact !== sStr) {
      throw new Error(`Case ${c.case_id}, L=${L}: moment_sum_survival_exact mismatch`);
    }
    if(row.throughput_adjusted_pruned_snr>row.survival_probability_float+1e-12 || row.survival_probability_float>1+1e-12)throw new Error("conditional proxy upper bound violated");
    if(c.q===3 && 3n*pNum===2n*pDen){
      if(row.throughput_adjusted_pruned_snr!==0 || row.classical_k_leaf_snr!==0 || row.pruned_to_leaf_snr_ratio!==null || row.direct_leaf_comparison!=="EXACT_ZERO_TIE")throw new Error("zero visibility is an exact tie, not a strict dominance proof");
    }
  }
  if(c.analysis_model!=="CONDITIONAL_CLASSICAL_LATENT_ERROR_RETAIN_ONE_LEAF" || c.physical_equality_instrument_supplied!==false || c.CNOT_sum_merge_error_law_claimed!==false || c.direct_leaf_dominance_is_a_universal_theorem!==false)throw new Error("classical identities promoted to physical filter or universal comparison");
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "CONDITIONAL_CLASSICAL_IDENTITIES_PHYSICAL_ACCESS_NOT_SUPPLIED"
  ) {
    throw new Error(`Unexpected status: ${payload.status}`);
  }
  for(const flag of ["physical_equality_instrument_supplied","CNOT_sum_merge_error_law_claimed","universal_direct_leaf_dominance_claimed","external_theorem_review_complete"]){
    if(payload.guardrails[flag]!==false)throw new Error("physical access/theorem scope guardrail violated");
  }
  if (
    payload.guardrails.accepted_speedup_candidate !== false ||
    payload.guardrails.new_active_negative_result_created !== false ||
    payload.guardrails.novelty_claim !== false
  ) {
    throw new Error("Guardrail violation");
  }

  for (const c of payload.cases) {
    verifyCase(c);
  }

  console.log(
    JSON.stringify(
      {
        status: "CROSSCHECK_PASSED",
        case_count: payload.cases.length,
        certificate_sha256: payload.certificate_sha256,
      },
      null,
      2
    )
  );
}

main();

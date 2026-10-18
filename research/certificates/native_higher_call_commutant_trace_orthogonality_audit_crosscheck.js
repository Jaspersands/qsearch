#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_commutant_trace_orthogonality_audit.json"
);

function verifyCase(c) {
  const D = c.D;
  const maxPurityDeficit = 1.0 - 1.0 / D;

  if (c.max_fourier_inversion_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: Fourier inversion residual > 1e-12`);
  }
  if (c.max_adjoint_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: adjoint residual > 1e-12`);
  }
  if (c.max_nonzero_trace_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: non-zero trace residual > 1e-12`);
  }
  if (c.hs_vs_purity_deficit_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: HS vs purity deficit residual > 1e-12`);
  }
  if (c.hs_vs_parseval_rho_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: HS vs Parseval rho residual > 1e-12`);
  }

  const pDef = c.purity_deficit_1_minus_tr_rho_bar_sq;
  if (Math.abs(pDef - (1.0 - c.purity_rho_bar)) > 1e-12) {
    throw new Error(`Case ${c.case_id}: purity deficit identity mismatch`);
  }
  if (pDef > maxPurityDeficit + 1e-12) {
    throw new Error(`Case ${c.case_id}: purity deficit exceeds 1 - 1/D`);
  }

  for (const b of c.basis_evaluations) {
    const sumE = b.diagonal_l2_signal_energy + b.off_diagonal_coherence_energy;
    if (Math.abs(sumE - pDef) > 1e-12) {
      throw new Error(
        `Case ${c.case_id}, basis ${b.basis_name}: conservation mismatch`
      );
    }
    if (b.diagonal_l2_signal_energy > pDef + 1e-12) {
      throw new Error(
        `Case ${c.case_id}, basis ${b.basis_name}: diagonal L2 energy exceeds purity deficit`
      );
    }
  }
}

function main() {
  const raw = fs.readFileSync(ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);

  if (
    payload.status !==
    "VERIFIED_EXACT_OPERATOR_COMMUTANT_TRACE_AND_PURITY_DEFICIT_LAWS"
  ) {
    throw new Error(`Unexpected status: ${payload.status}`);
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

"""Rebuild the frozen central step and check the concrete Rees quotient chain."""

import argparse
import hashlib
import json
from pathlib import Path

import verify as base
import verify_group_bridge as bridge
import verify_cancellation as cancellation


ROOT = Path(__file__).resolve().parent
PREFIX = "QSearch.ReesQuotients."
THEOREMS = tuple(PREFIX+name for name in ["tailSpace_le","tailSpace_antitone","tailSpace_membership","monomial_tail","bracket_tail_raise","tailIdeal_antitone","tailIdeal_zero","tailIdeal_end","tailIdeal_raise","dilation_tail","quotientProjection_surjective","next_layer_central","truncate_mem","quotient_eq_iff_prefix","prefixRepresentative_same","hiddenLie_coefficients","stageHidden_prefix","first_stage_recovers_all_h","first_stage_surjective","first_stage_injective","first_stage_abelian","truncated_evaluation_impossible","stageDilation_projection","stageDilation_hidden","stageFactor_projection","stageFactor_surjective","stageFactor_hidden","stageFactor_comp","stageFactor_zero_iff","prefixRepresentative_eq","stageSection_right_inverse","next_layer_scalar","map_product","next_layer_group_central","first_stage_group_additive","stageGroupFactor_hidden","stageGroupDilation_hidden","step_kernel_central_and_scaled"])
DEFINITIONS = tuple(PREFIX+name for name in ["lowKernel","tailSpace","tailIdeal","quotientProjection","truncate","prefixRepresentative","hiddenLie","stageHidden","quotientMap","quotientEquiv","stageDilation","stageFactor","stageSection","imageGroup","imageLaw","subalgebraGroup","subalgebraLaw","polynomialGroupHom","polynomialGroupEquiv","coverGroup","coverLaw","stageGroup","stageLaw","stageGroupProjection","stageGroupFactor","stageGroupDilation"])
DECLARATIONS = THEOREMS+DEFINITIONS


def expected_audit():
    return "import ReesQuotients\n\n"+"".join(f"#print axioms {name}\n" for name in DECLARATIONS)


def scope_report():
    return {"actual_graded_tail_ideals_constructed": True,
            "quotient_group_laws_constructed_from_base": True,
            "central_scalar_kernels_checked": True,
            "hidden_images_and_public_sections_checked": True,
            "terminal_stage_retains_all_original_hidden_subspace": True,
            "truncated_nonzero_evaluation_shortcut_falsified": True,
            "base_polynomial_group_law_is_explicit_hypothesis": True,
            "base_lazard_bch_theorem_formalized": False,
            "recursive_quantum_instrument_composed": False,
            "fourier_recovery_formalized": False,
            "diagonal_solver_implemented": False,
            "formalizes_full_Rees_algorithm": False,
            "quantum_execution": False, "new_algorithm_or_novelty_claim": False,
            "independent_review_this_pass": False, "main_checkout_modified": False}


def verify():
    frozen = json.loads((ROOT/"cancellation_receipt.json").read_text())
    current = cancellation.verify()
    bridge.validate_base_record(current, frozen)
    if (ROOT/"AuditQuotients.lean").read_text() != expected_audit():
        raise ValueError("quotient audit differs from the full declaration set")
    compiled = base.lean("--json", "-o", ".lake/build/lib/lean/ReesQuotients.olean",
                         "ReesQuotients.lean")
    if compiled.strip():
        raise ValueError(f"quotient proof emitted diagnostics: {compiled}")
    axioms = base.parse_axioms(base.lean("--json", "AuditQuotients.lean"), DECLARATIONS)
    names = ("ReesQuotients.lean", "AuditQuotients.lean", "verify_quotients.py",
             "test_quotient_verifier.py", "REES_QUOTIENT_SCOPE.md", "QUOTIENT_HANDOFF.md")
    return {"status": "ACTUAL_REES_QUOTIENT_GROUP_CHAIN_CHECKED",
            "new_theorem_count": len(THEOREMS), "new_declaration_count": len(DECLARATIONS),
            "combined_theorem_count": len(THEOREMS)+current["combined_theorem_count"],
            "combined_declaration_count": len(DECLARATIONS)+current["combined_declaration_count"],
            "axioms_by_new_declaration": axioms, "compile_diagnostics": [],
            "lean_version": current["lean_version"], "mathlib_commit": current["mathlib_commit"],
            "cancellation_receipt_sha256": hashlib.sha256((ROOT/"cancellation_receipt.json").read_bytes()).hexdigest(),
            "cancellation_source_sha256": current["source_sha256"],
            "group_bridge_receipt_sha256": current["group_bridge_receipt_sha256"],
            "group_bridge_source_sha256": current["group_bridge_source_sha256"],
            "base_receipt_sha256": current["base_receipt_sha256"],
            "base_source_sha256": current["base_source_sha256"], **scope_report(),
            "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(f"Checked {result['combined_theorem_count']} theorems / "
          f"{result['combined_declaration_count']} declarations; actual quotient groups checked; "
          "full quantum composition NOT formalized.")

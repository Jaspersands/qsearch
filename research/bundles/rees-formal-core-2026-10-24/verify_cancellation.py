"""Rebuild the frozen Rees base and check the constructed cancellation step."""

import argparse
import hashlib
import json
from pathlib import Path

import verify as base
import verify_group_bridge as bridge


ROOT = Path(__file__).resolve().parent
PREFIX = "QSearch.ReesCancellation."
THEOREMS = tuple(PREFIX+name for name in (
    "decomposition_spec", "action_difference", "hiddenCenter_preserved",
    "central_range_normal", "hiddenCenter_quotient", "quotientRelation_iff",
    "zero_scale_discard", "character_sum", "moment_cancels", "mem_hiddenSubgroup",
    "highestEmbed_injective", "highestEmbed_central", "publicDilation_hidden",
    "publicDilation_center", "rees_instrument"))
DEFINITIONS = tuple(PREFIX+name for name in (
    "inHiddenCenter", "quotientRelation", "decomposition", "controlledAction",
    "centralAction", "automorphismCertificate", "linearCharacter", "scalarEquiv",
    "scaleEquiv", "hiddenSubgroup", "highestEmbed", "publicDilation", "reesCertificate"))
DECLARATIONS = THEOREMS+DEFINITIONS


def expected_audit():
    return "import ReesCancellation\n\n"+"".join(f"#print axioms {name}\n" for name in DECLARATIONS)


def scope_report():
    return {"cancellation_certificate_constructed": True,
            "actual_rees_top_grade_instantiated": True,
            "all_measurement_records_included": True,
            "arbitrary_address_reference_matrix": True,
            "nonzero_moment_witness_is_explicit_hypothesis": True,
            "complete_fourier_characters_are_explicit_hypothesis": True,
            "base_polynomial_group_law_is_explicit_hypothesis": True,
            "base_lazard_bch_theorem_formalized": False,
            "diagonal_solver_implemented": False,
            "graded_quotient_chain_formalized": False,
            "formalizes_full_Rees_algorithm": False,
            "quantum_execution": False, "new_algorithm_or_novelty_claim": False,
            "independent_review_this_pass": False, "main_checkout_modified": False}


def verify():
    frozen = json.loads((ROOT/"group_bridge_receipt.json").read_text())
    current = bridge.verify()
    bridge.validate_base_record(current, frozen)
    if (ROOT/"AuditCancellation.lean").read_text() != expected_audit():
        raise ValueError("cancellation audit differs from the full declaration set")
    compiled = base.lean("--json", "-o", ".lake/build/lib/lean/ReesCancellation.olean",
                         "ReesCancellation.lean")
    if compiled.strip():
        raise ValueError(f"cancellation proof emitted diagnostics: {compiled}")
    axioms = base.parse_axioms(base.lean("--json", "AuditCancellation.lean"), DECLARATIONS)
    names = ("ReesCancellation.lean", "AuditCancellation.lean", "verify_cancellation.py",
             "test_cancellation_verifier.py", "REES_CANCELLATION_SCOPE.md", "CANCELLATION_HANDOFF.md")
    return {"status": "CONSTRUCTED_REES_FIRST_CENTRAL_STEP_CHECKED",
            "new_theorem_count": len(THEOREMS), "new_declaration_count": len(DECLARATIONS),
            "combined_theorem_count": len(THEOREMS)+current["combined_theorem_count"],
            "combined_declaration_count": len(DECLARATIONS)+current["combined_declaration_count"],
            "axioms_by_new_declaration": axioms, "compile_diagnostics": [],
            "lean_version": current["lean_version"], "mathlib_commit": current["mathlib_commit"],
            "group_bridge_receipt_sha256": hashlib.sha256((ROOT/"group_bridge_receipt.json").read_bytes()).hexdigest(),
            "group_bridge_source_sha256": current["source_sha256"],
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
          f"{result['combined_declaration_count']} declarations; first central step constructed; "
          "full algorithm NOT formalized.")

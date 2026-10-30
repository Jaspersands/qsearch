"""Rebuild the frozen proof base and audit the explicit group bridge."""

import argparse
import hashlib
import json
from pathlib import Path

import verify as base


ROOT = Path(__file__).resolve().parent
PREFIX = "QSearch.ReesGroupBridge."
THEOREMS = tuple(PREFIX+name for name in (
    "map_interpret", "interpret_mem", "interpret_commuting", "interpret_split",
    "commuting_mul_add", "commuting_group", "toLie_mul", "interpret_pi",
    "dilationGroup_value", "group_hidden_membership", "dilationGroup_hidden",
    "actual_tuple_hides", "highestGroup_central", "highestGroup_scaled"))
DEFINITIONS = tuple(PREFIX+name for name in (
    "Expression", "interpret", "linearPart", "PolynomialGroupLaw", "subgroup", "toLie",
    "liftLieEquiv", "piLaw", "groupCover", "evaluationGroupHom", "dilationGroupEquiv",
    "highestGroupElement"))
DECLARATIONS = THEOREMS+DEFINITIONS


def expected_audit():
    return "import ReesGroupBridge\n\n"+"".join(f"#print axioms {name}\n" for name in DECLARATIONS)


def validate_base_record(current, frozen):
    if current != frozen:
        raise ValueError("fresh base verification differs from the frozen receipt")


def scope_report():
    return {"base_lazard_bch_theorem_formalized": False,
            "base_polynomial_group_law_is_explicit_hypothesis": True,
            "cover_group_maps_are_constructed_not_assumed": True,
            "graded_quotient_chain_formalized": False,
            "efficient_cancellation_implemented": False,
            "formalizes_full_Rees_algorithm": False,
            "quantum_execution": False, "new_algorithm_or_novelty_claim": False,
            "independent_review_this_pass": False, "main_checkout_modified": False}


def verify():
    frozen = json.loads((ROOT/"receipt.json").read_text())
    current = base.verify()
    validate_base_record(current, frozen)
    if (ROOT/"AuditGroupBridge.lean").read_text() != expected_audit():
        raise ValueError("group bridge audit differs from the full declaration set")
    compiled = base.lean("--json", "-o", ".lake/build/lib/lean/ReesGroupBridge.olean",
                         "ReesGroupBridge.lean")
    if compiled.strip():
        raise ValueError(f"group proof emitted diagnostics: {compiled}")
    axioms = base.parse_axioms(base.lean("--json", "AuditGroupBridge.lean"), DECLARATIONS)
    names = ("ReesGroupBridge.lean", "AuditGroupBridge.lean", "verify_group_bridge.py",
             "test_group_bridge_verifier.py", "REES_GROUP_BRIDGE_SCOPE.md", "GROUP_BRIDGE_HANDOFF.md")
    return {"status": "GROUP_BRIDGE_RELATIVE_TO_EXPLICIT_BASE_LAW_CHECKED",
            "new_theorem_count": len(THEOREMS), "new_declaration_count": len(DECLARATIONS),
            "combined_theorem_count": len(THEOREMS)+current["theorem_count"],
            "combined_declaration_count": len(DECLARATIONS)+current["declaration_count"],
            "axioms_by_new_declaration": axioms, "compile_diagnostics": [],
            "lean_version": current["lean_version"], "mathlib_commit": current["mathlib_commit"],
            "base_receipt_sha256": hashlib.sha256((ROOT/"receipt.json").read_bytes()).hexdigest(),
            "base_source_sha256": current["source_sha256"], **scope_report(),
            "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(f"Checked {result['combined_theorem_count']} theorems / "
          f"{result['combined_declaration_count']} declarations; "
          "base BCH law remains explicit; full algorithm NOT formalized.")

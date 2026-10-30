"""Check actual Rees stage instruments and fresh-source recursive composition."""

import argparse
import hashlib
import json
from pathlib import Path

import verify as base
import verify_group_bridge as bridge
import verify_quotients as quotients


ROOT = Path(__file__).resolve().parent
STAGE = "QSearch.ReesStageInstrument."
TREE = "QSearch.ReesRecursiveSource."
STAGE_THEOREMS = tuple(STAGE+name for name in (
    "kernelEmbed_central", "kernelEmbed_range", "hiddenCenter_projection", "step_relation",
    "actionDilation_center", "measuredState_scale", "record_source", "record_scaled_sources",
    "record_mass_complete", "prepareNext_source", "rees_hidden_image", "rees_prepareNext_source"))
TREE_THEOREMS = tuple(TREE+name for name in (
    "tree_source", "tree_record", "duplicate_children_pay_separately", "tree_stage_le_top",
    "leafCount_product", "plan_packet_nonempty", "rees_record_source", "rees_record_homogeneous",
    "rees_mass_complete", "rees_average_source", "rees_record_tree", "rees_average_tree",
    "rees_tree_leafCount"))
DEFINITIONS = tuple(STAGE+name for name in (
    "StepGeometry", "projectionGroup", "kernelEmbed", "actionDilation", "stepAction",
    "stepCertificate", "measuredState", "recordOutput", "recordMass", "prepareNext",
    "reesStep", "stageFintype")) + tuple(TREE+name for name in (
    "SourceTree", "evaluateTree", "treeWeight", "leafCount", "MeasurementPlan", "ReesPlan",
    "reesSource", "reesRecord", "reesMass", "reesAverage"))
THEOREMS = STAGE_THEOREMS + TREE_THEOREMS
DECLARATIONS = THEOREMS + DEFINITIONS


def expected_audit():
    return "import ReesRecursiveSource\n\n"+"".join(f"#print axioms {name}\n" for name in DECLARATIONS)


def scope_report():
    return {
        "actual_adjacent_Rees_instruments_instantiated": True,
        "all_records_unnormalized_source_identity_checked": True,
        "recursive_record_and_averaged_source_identity_checked": True,
        "fresh_leaf_cost_is_product_of_packet_arities": True,
        "identical_subtrees_still_charge_separate_leaves": True,
        "independent_tensor_input_required": True,
        "complete_characters_and_nonzero_moment_witnesses_required": True,
        "base_polynomial_group_law_is_explicit_hypothesis": True,
        "top_stage_source_preparation_is_explicit_input": True,
        "base_lazard_bch_theorem_formalized": False,
        "native_to_top_source_channel_formalized": False,
        "arbitrary_correlated_input_supported": False,
        "adaptive_cross_packet_source_reuse_supported": False,
        "final_fourier_recovery_formalized": False,
        "diagonal_solver_implemented": False,
        "end_to_end_complexity_formalized": False,
        "formalizes_full_Rees_algorithm": False,
        "quantum_execution": False,
        "new_algorithm_or_novelty_claim": False,
        "independent_review_this_pass": False,
        "main_checkout_modified": False,
    }


def verify():
    frozen = json.loads((ROOT/"quotient_receipt.json").read_text())
    current = quotients.verify()
    bridge.validate_base_record(current, frozen)
    if (ROOT/"AuditRecursiveSource.lean").read_text() != expected_audit():
        raise ValueError("recursive source audit differs from the full declaration set")
    for module in ("ReesStageInstrument", "ReesRecursiveSource"):
        compiled = base.lean("--json", "-o", f".lake/build/lib/lean/{module}.olean", f"{module}.lean")
        if compiled.strip():
            raise ValueError(f"recursive source proof emitted diagnostics: {compiled}")
    axioms = base.parse_axioms(base.lean("--json", "AuditRecursiveSource.lean"), DECLARATIONS)
    names = ("ReesStageInstrument.lean", "ReesRecursiveSource.lean", "AuditRecursiveSource.lean",
             "verify_recursive_source.py", "test_recursive_source.py", "REES_RECURSIVE_SCOPE.md",
             "RECURSIVE_HANDOFF.md")
    return {
        "status": "ACTUAL_REES_RECURSIVE_SOURCE_IDENTITIES_CHECKED",
        "new_theorem_count": len(THEOREMS), "new_declaration_count": len(DECLARATIONS),
        "combined_theorem_count": len(THEOREMS)+current["combined_theorem_count"],
        "combined_declaration_count": len(DECLARATIONS)+current["combined_declaration_count"],
        "axioms_by_new_declaration": axioms, "compile_diagnostics": [],
        "lean_version": current["lean_version"], "mathlib_commit": current["mathlib_commit"],
        "quotient_receipt_sha256": hashlib.sha256((ROOT/"quotient_receipt.json").read_bytes()).hexdigest(),
        "quotient_source_sha256": current["source_sha256"],
        **{key: value for key, value in current.items()
           if key.endswith("_receipt_sha256") or key.endswith("_source_sha256")},
        **scope_report(),
        "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(f"Checked {result['combined_theorem_count']} theorems / "
          f"{result['combined_declaration_count']} declarations; recursive source identities checked; "
          "full quantum algorithm NOT formalized.")

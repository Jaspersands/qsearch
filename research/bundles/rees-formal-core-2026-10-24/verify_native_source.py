"""Rebuild the frozen recursive chain and verify native copy-only acquisition."""

import argparse
import hashlib
import json
from pathlib import Path

import native_source_controls as controls
import verify as base
import verify_group_bridge as bridge
import verify_recursive_source as recursive


ROOT = Path(__file__).resolve().parent
PREFIX = "QSearch.ReesNativeSource."
THEOREMS = tuple(PREFIX+name for name in (
    "source_correlation", "indicator_product", "pullback_with_reference", "nativePullback_source",
    "source_relabel", "full_prefix", "topSection_left", "topSection_right", "top_hidden_image",
    "cover_hidden_pullback", "acquireTop_source", "native_average_tree", "native_record_tree"))
DEFINITIONS = tuple(PREFIX+name for name in (
    "pulledHidden", "nativePullback", "topSection", "topGroupEquiv", "coverEvaluation", "acquireTop"))
DECLARATIONS = THEOREMS+DEFINITIONS


def expected_audit():
    return "import ReesNativeSource\n\n"+"".join(f"#print axioms {name}\n" for name in DECLARATIONS)


def scope_report():
    return {
        "native_to_top_source_channel_formalized": True,
        "native_source_to_recursive_record_identity_checked": True,
        "native_source_to_recursive_average_identity_checked": True,
        "top_coordinate_equivalence_is_public_full_prefix": True,
        "noninjective_public_pullback_supported": True,
        "native_independent_mixed_coset_sources_required": True,
        "public_uniform_address_and_reversible_translation_required": True,
        "source_inverse_required": False,
        "hiding_function_oracle_required_by_copy_only_channel": False,
        "kernel_index_postselection_required": False,
        "correlated_target_bank_supported": False,
        "uniform_coherent_compiler_implemented": False,
        "final_fourier_recovery_formalized": False,
        "diagonal_solver_implemented": False,
        "base_lazard_bch_theorem_formalized": False,
        "end_to_end_complexity_formalized": False,
        "formalizes_full_Rees_algorithm": False,
        "quantum_execution": False, "new_algorithm_or_novelty_claim": False,
        "independent_review_this_pass": False, "main_checkout_modified": False,
    }


def verify():
    frozen = json.loads((ROOT/"recursive_source_receipt.json").read_text())
    current = recursive.verify()
    bridge.validate_base_record(current, frozen)
    if (ROOT/"AuditNativeSource.lean").read_text() != expected_audit():
        raise ValueError("native source audit differs from the full declaration set")
    compiled = base.lean("--json", "-o", ".lake/build/lib/lean/ReesNativeSource.olean", "ReesNativeSource.lean")
    if compiled.strip():
        raise ValueError(f"native source proof emitted diagnostics: {compiled}")
    axioms = base.parse_axioms(base.lean("--json", "AuditNativeSource.lean"), DECLARATIONS)
    names = ("ReesNativeSource.lean", "AuditNativeSource.lean", "verify_native_source.py",
             "native_source_controls.py", "test_native_source.py", "REES_NATIVE_SOURCE_SCOPE.md",
             "NATIVE_SOURCE_HANDOFF.md")
    return {
        "status": "NATIVE_COPY_ONLY_REES_SOURCE_CHAIN_CHECKED",
        "new_theorem_count": len(THEOREMS), "new_declaration_count": len(DECLARATIONS),
        "combined_theorem_count": len(THEOREMS)+current["combined_theorem_count"],
        "combined_declaration_count": len(DECLARATIONS)+current["combined_declaration_count"],
        "axioms_by_new_declaration": axioms, "compile_diagnostics": [],
        "lean_version": current["lean_version"], "mathlib_commit": current["mathlib_commit"],
        "recursive_source_receipt_sha256": hashlib.sha256((ROOT/"recursive_source_receipt.json").read_bytes()).hexdigest(),
        "recursive_source_sha256": current["source_sha256"],
        **{key: value for key, value in current.items()
           if key.endswith("_receipt_sha256") or key.endswith("_source_sha256")},
        **scope_report(), "finite_controls": controls.audit(),
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
          f"{result['combined_declaration_count']} declarations; native copy-only source chain checked; "
          "full quantum algorithm NOT formalized.")

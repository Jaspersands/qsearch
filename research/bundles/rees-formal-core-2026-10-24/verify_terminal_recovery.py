"""Rebuild the native Rees chain and audit the terminal Fourier receiver."""

import argparse
import hashlib
import json
from pathlib import Path
import re

import terminal_controls as controls
import verify as base
import verify_group_bridge as bridge
import verify_native_source as native


ROOT = Path(__file__).resolve().parent
PREFIX = "QSearch.ReesTerminalRecovery."
THEOREMS = tuple(PREFIX + name for name in (
    "character_unit_pair", "restriction_trivial_iff", "subgroup_character_sum", "fourier_source",
    "readout_smul", "dual_card", "evaluation_character_trivial", "complete_linear_characters",
    "fourier_columns", "readout_complete", "recovered_membership", "recovery_contains_hidden",
    "recovery_exact", "recovery_exact_iff", "standard_character_faithful", "standard_character_unitary",
    "terminal_source", "native_terminal_readout", "native_record_readout", "native_hidden_recovery"))
DEFINITIONS = tuple(PREFIX + name for name in ("additiveSource", "fourierReadout", "recovered"))
DECLARATIONS = THEOREMS + DEFINITIONS


def expected_audit():
    return "import ReesTerminalRecovery\n\n" + "".join(f"#print axioms {name}\n" for name in DECLARATIONS)


def validate_declarations(source):
    names = [PREFIX + name for name in re.findall(r"^(?:theorem|def)\s+(\w+)", source, re.MULTILINE)]
    if len(names) != len(set(names)) or set(names) != set(DECLARATIONS):
        raise ValueError("terminal declaration manifest differs from source")


def scope_report():
    return {
        "actual_native_tree_to_terminal_fourier_law_formalized": True,
        "retained_record_weights_preserved_without_conditioning": True,
        "prime_modulus_character_faithfulness_and_unitarity_checked": True,
        "complete_linear_character_family_checked": True,
        "recovery_exact_iff_annihilator_spanned_checked": True,
        "recovery_returns_all_original_hidden_lie_space": True,
        "independent_terminal_sources_required_for_sampling_bound": True,
        "finite_sample_rank_bound_is_written_not_lean_formalized": True,
        "basis_acquisition_and_kernel_algorithm_formalized": False,
        "diagonal_solver_implemented": False,
        "base_lazard_bch_theorem_formalized": False,
        "approximate_channel_and_runtime_bound_formalized": False,
        "uniform_coherent_compiler_implemented": False,
        "formalizes_full_Rees_algorithm": False,
        "quantum_execution": False,
        "new_algorithm_or_novelty_claim": False,
        "independent_review_this_pass": False,
        "main_checkout_modified": False,
    }


def verify():
    frozen = json.loads((ROOT / "native_source_receipt.json").read_text())
    current = native.verify()
    bridge.validate_base_record(current, frozen)
    validate_declarations((ROOT / "ReesTerminalRecovery.lean").read_text())
    if (ROOT / "AuditTerminalRecovery.lean").read_text() != expected_audit():
        raise ValueError("terminal audit differs from the complete declaration set")
    diagnostics = base.lean("--json", "-o", ".lake/build/lib/lean/ReesTerminalRecovery.olean",
                            "ReesTerminalRecovery.lean")
    if diagnostics.strip():
        raise ValueError(f"terminal proof emitted diagnostics: {diagnostics}")
    axioms = base.parse_axioms(base.lean("--json", "AuditTerminalRecovery.lean"), DECLARATIONS)
    names = ("ReesTerminalRecovery.lean", "AuditTerminalRecovery.lean", "verify_terminal_recovery.py",
             "terminal_controls.py", "test_terminal_recovery.py", "REES_TERMINAL_SCOPE.md",
             "TERMINAL_HANDOFF.md")
    return {
        "status": "NATIVE_REES_TERMINAL_MEASUREMENT_AND_RECOVERY_CONDITION_CHECKED",
        "new_theorem_count": len(THEOREMS), "new_declaration_count": len(DECLARATIONS),
        "combined_theorem_count": len(THEOREMS) + current["combined_theorem_count"],
        "combined_declaration_count": len(DECLARATIONS) + current["combined_declaration_count"],
        "axioms_by_new_declaration": axioms, "compile_diagnostics": [],
        "lean_version": current["lean_version"], "mathlib_commit": current["mathlib_commit"],
        "native_source_receipt_sha256": hashlib.sha256((ROOT / "native_source_receipt.json").read_bytes()).hexdigest(),
        "native_source_sha256": current["source_sha256"],
        **{key: value for key, value in current.items()
           if key.endswith("_receipt_sha256") or key.endswith("_source_sha256")},
        **scope_report(), "controls_and_symbolic_budgets": controls.audit(),
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Checked {result['combined_theorem_count']} theorems / "
          f"{result['combined_declaration_count']} declarations; terminal readout and exact "
          "spanning condition checked; full quantum algorithm NOT formalized.")

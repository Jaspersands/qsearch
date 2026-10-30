"""Emit a deterministic local receipt. No geometric or quantum execution."""

import hashlib
import json
from pathlib import Path

from sympy import zeros

from controls import frobenius_relation_fixture, word_fixture
from kernel_output import action, product_actions
from pullback import extract_kernel, mod, reconstruct_pullbacks


def run():
    rows = []
    for label, source in [("quadratic_word_completion", word_fixture())] + [
            (f"frobenius_relation_rank_{rank}", frobenius_relation_fixture(rank)) for rank in range(3)]:
        extracted = reconstruct_pullbacks(
            source.order, source.ell, source.characteristic, source.norms(), source.levels(),
            source.split, source.observe, max_auxiliary_prime=47)
        if extracted.coordinates != source.reference_pullbacks():
            raise AssertionError("CRT source recovery failed")
        output = extract_kernel(source.order, source.ell, source.split(source.ell), extracted.coordinates)
        phi = action(source.phi, product_actions(source.split(source.ell)))
        if mod(phi * output.known_subspace, source.ell) != zeros(4, output.known_subspace.cols):
            raise AssertionError("returned vector lies outside actual reference kernel")
        rows.append({
            "id": label, "characteristic": source.characteristic, "ell": source.ell,
            "gamma_coordinates": [[int(x) for x in gamma] for gamma in source.gammas],
            "pullback_coordinates": [[int(x) for x in a] for a in extracted.coordinates],
            "norm_squared_bounds": list(extracted.norm_bounds),
            "auxiliary_primes": list(extracted.primes), "crt_modulus": extracted.modulus,
            "maximum_pairing_bound": extracted.pairing_bound,
            "weak_action_packets_executed": len(source.calls),
            "geometric_point_evaluations_executed": 0,
            "point_access_requirements_not_executions": {
                "weak_source": extracted.weak_basis_points_required,
                "target_maps": extracted.target_basis_points_required,
                "source_basis_maps": extracted.source_basis_points_required},
            "rank_history": list(output.rank_history), "word_counts": list(output.word_counts),
            "known_kernel_columns": [[int(x) for x in output.known_subspace[:, i]]
                                     for i in range(output.known_subspace.cols)],
            "remaining_lagrangian_extensions_of_returned_subspace": output.remaining_lagrangian_extensions,
            "extension_count_is_not_a_hardness_claim": True,
            "status": output.status, "input_promises_certified_by_extraction": output.assumptions_verified,
            "reference_containment_verified": True,
        })
    root = Path(__file__).resolve().parent
    dependencies = [root / name for name in ("pullback.py", "controls.py", "test_pullback.py", "replay.py")]
    dependencies.append(root.parent / "kernel-output-2026-10-23" / "kernel_output.py")
    return {
        "scope": "source-side arithmetic controls for the existing weak-isogeny input",
        "new_quantum_algorithm": False, "natural_geometric_instance_executed": False,
        "independent_review": False, "novelty_claim": False,
        "target_order_supplied_to_extractor": False, "hidden_phi_supplied_to_extractor": False,
        "fixture_only_secret_usage": "reference callbacks and final correctness comparison",
        "abstract_source_ell_chart": "supplied public algebra splitting, no ell-torsion points",
        "maximum_auxiliary_prime_cap": 47,
        "records": rows,
        "sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in dependencies},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

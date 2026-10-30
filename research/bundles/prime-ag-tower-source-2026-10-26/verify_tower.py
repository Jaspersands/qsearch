"""Replay the actual prime-field source, full AG codes and classical witnesses."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform

import flint

from elementary_cover import BASELINE, control, one_point_control
from tower_seed import (asymptotic_quantum_certificate, default_seed,
                        persistent_section_bound, scan_consecutive_square_runs,
                        specialization, verify_certificate)


ROOT = Path(__file__).resolve().parent
FROZEN = {
    BASELINE: "d2ba9a0dc1d83a60f3210efec353b463897269bdc943abf728e2a642bc2129e3",
    ROOT.parent / "unambiguous-reduction-2026-10-26/receipt.json":
        "e6435c5275c7db6d593e5af002a82bf1e7f6e758beea3309af5dd30770949eeb",
    ROOT.parent / "schur-growth-classical-gate-2026-10-26/receipt.json":
        "778b6595a508c482fdfc9e8bb5001c6eb0967329bafbb54d128592fff32c6f64",
    ROOT.parent / "ag-affine-sampling-2026-10-26/receipt.json":
        "960726d49e2faaac7a8d427a370b04d4f90337262694c98cd6fa641062b742ce",
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def report():
    for path, expected in FROZEN.items():
        if digest(path) != expected:
            raise ValueError(f"frozen preceding result changed: {path}")
    certificate = default_seed().certificate()
    if not verify_certificate(certificate) or not certificate["schoof_sufficient_criterion"]:
        raise ArithmeticError("source certificate failed")
    problem, h, data = control()
    targets = [(0,)*problem.k, (1,)*problem.k, tuple(range(problem.k))]
    targets += [tuple(int(i == j) for i in range(problem.k)) for j in (0, 1, problem.k-1)]
    runs = []
    for target in targets:
        analytic = problem.from_annihilator(target, h, 2)
        matrix_only = problem.deterministic_attempt(target, 2)
        if not all(problem.verifies(item["witness"], target) for item in (analytic, matrix_only)):
            raise ArithmeticError("classical solver failed ORIGINAL relation")
        runs.append({"syndrome": target, "analytic_residue_run": analytic,
                     "original_matrix_only_run": matrix_only, "original_relation_verified": True})
    mutated, mutation = one_point_control()
    target = tuple(range(mutated.k))
    result = mutated.deterministic_attempt(target, 2)
    if not mutated.verifies(result["witness"], target):
        raise ArithmeticError("one-point mutation witness failed")
    sources = [ROOT / name for name in ("tower_seed.py", "elementary_cover.py",
               "test_tower_source.py", "verify_tower.py", "TOWER_SOURCE.md", "HANDOFF.md")]+list(FROZEN)
    return jsonable({
        "status": "CONCRETE_PRIME_TOWER_FAMILY_CLASSICALLY_SOLVED",
        "scope": {"relation": "original By=s and EVERY coordinate nonzero",
                  "classical_algorithm_is_prior_art": True,
                  "family_wide_claim_is_written_argument_not_scaling_experiment": True,
                  "all_ag_families_solved": False, "uniform_sampler_constructed": False,
                  "native_inverse_trace_solved": False, "usd_refinement_refuted": False,
                  "quantum_execution": False, "quantum_advantage_established": False,
                  "registry_admission": False},
        "source_seed": certificate, "source_discovery_replay": scan_consecutive_square_runs(),
        "actual_degree_eight_code": data, "native_witness_runs": runs,
        "one_point_mutation": {"data": mutation, "target": target, "result": result},
        "conditional_asymptotic_quantum_bound": asymptotic_quantum_certificate(),
        "bounded_effective_mutation_obstruction": persistent_section_bound(
            3, 0, full_kummer_inclusion_asserted=True),
        "uninstantiated_full_elementary_cover_parameters": specialization(4096),
        "runtime": {"python": platform.python_version(), "python_flint": flint.__version__},
        "sha256": {str(path.relative_to(ROOT.parent)): digest(path) for path in sources},
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    destination = ROOT / "receipt.json"
    if args.check:
        if json.loads(destination.read_text()) != data:
            raise SystemExit("FAIL: receipt differs from original-input replay")
        print(f"PASS: tower replay; {len(data['sha256'])} hashes; SHA256 {digest(destination)}")
    elif args.write:
        destination.write_text(json.dumps(data, indent=2)+"\n")
        print(f"Wrote {destination}; SHA256 {digest(destination)}")
    else:
        print(json.dumps(data, indent=2))

"""Replay sample-only controls; tiny group exhaustions are not a Luks backend."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import random

from diagonal_source import (apply_matrix, colored_points, lift_affine,
                             sample_source, sampling_plan)

ROOT = Path(__file__).resolve().parent


def tv_after_action(probabilities, action):
    moved = {action(x): value for x, value in probabilities.items()}
    return sum(abs(probabilities.get(x, 0)-moved.get(x, 0))
               for x in probabilities.keys() | moved.keys())/2


def ut3_action(g, point, p):
    a, b, c = g
    x, y, z = point
    return ((x+a*y+c*z) % p, (y+b*z) % p, z)


def ut3_product(g, h, p):
    return ((g[0]+h[0]) % p, (g[1]+h[1]) % p,
            (g[2]+h[2]+g[0]*h[1]) % p)


def nonnormal_sample_control():
    p, tiny, splitting = 5, F(1, 2**200), F(1, 2**180)
    probabilities = {(0, 0, 1): (1-tiny)/2+splitting, (0, 0, 2): (1-tiny)/2-splitting,
                     (0, 0, 0): tiny}
    rng = random.Random(261024)
    denominator = 2**201
    first_heavy_count = (denominator-2)//2 + int(denominator*splitting)
    calls = 0

    def sampler():
        nonlocal calls
        calls += 1
        value = rng.randrange(denominator)
        return (0, 0, 0 if value < 2 else 1 if value < 2+first_heavy_count else 2)

    plan = sampling_plan(3, F(3, 4), F(1, 8))
    result = sample_source(sampler, rank_cap=3, orbit_gap=F(3, 4),
        failure_probability=F(1, 8), dimension=3, field_prime=p,
        sample_budget=plan["sample_count"])
    group = tuple(product(range(p), repeat=3))  # Capped, classically easy reference.
    distances = {g: tv_after_action(probabilities, lambda x, g=g: ut3_action(g, x, p))
                 for g in group}
    original = {g for g in group if distances[g] == 0}
    coarse = {tuple(row["point"]): row["value"] for row in result["coarsening"]["rows"]}
    rounded = {g for g in group if tv_after_action(coarse, lambda x, g=g: ut3_action(g, x, p)) == 0}
    points = set(colored_points(result["coarsening"]))
    encoded = set()
    for g in group:
        a, b, c = g
        matrix = ((1, a, c), (0, 1, b), (0, 0, 1))
        lifted = lift_affine(matrix, (0, 0, 0), result["coarsening"]["color_count"], p)
        if {apply_matrix(lifted, x, p) for x in points} == points:
            encoded.add(g)
    core = set(original)
    for g in group:
        inv = ((-g[0]) % p, (-g[1]) % p, (g[0]*g[1]-g[2]) % p)
        core &= {ut3_product(ut3_product(g, h, p), inv, p) for h in original}
    empirical = {tuple(row["point"]): F(row["count"], calls) for row in result["histogram"]}
    frequency_error = max(abs(empirical.get(x, 0)-value) for x, value in probabilities.items())
    loss = sum(abs(value-coarse.get(x, 0)) for x, value in probabilities.items())
    return {"status": "SEEDED_CLASSICAL_SAMPLE_CONTROL_NOT_ASYMPTOTIC_PROOF",
            "sample_calls": calls, "planned_samples": plan["sample_count"],
            "histogram": result["histogram"], "minimum_true_weight_reference_only": tiny,
            "unequal_heavy_weight_difference_reference_only": 2*splitting,
            "uniform_frequency_event_verified_in_reference": frequency_error <= plan["frequency_error"],
            "observed_max_frequency_error_reference_only": frequency_error,
            "coarsening_trace_norm_loss": loss, "trace_norm_loss_bound": plan["trace_norm_loss_upper"],
            "group_order": len(group), "hidden_order": len(original), "normal_core_order": len(core),
            "minimum_outside_tv": min(v for v in distances.values() if v),
            "same_original_rounded_encoded_subgroup": original == rounded == encoded,
            "subgroup_labels_reference_only": sorted(original),
            "source_stage_group_backend_executed": result["coarsening"]["group_backend_executed"],
            "finite_group_enumeration_not_scalable_solver": True}


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def receipt():
    files = ["DIAGONAL_BASELINE.md", "diagonal_source.py", "test_diagonal_source.py",
             "HANDOFF.md", "run_audit.py"]
    dependencies = ["rees-coarse-spectrum-2026-10-24/COARSE_SPECTRUM.md",
                    "rees-coarse-spectrum-2026-10-24/receipt.json",
                    "hdqi-gap-baseline-2026-10-24/GAP_AND_BASELINE.md"]
    return {"status": "SCOPED_CLASSICAL_BASELINE_REVIEW_PENDING",
            "non_diagonal_quantum_source_dequantized": False,
            "classical_luks_backend_implemented": False, "quantum_algorithm_executed": False,
            "novelty_established": False, "accepted_speedup_candidate": False,
            "ordinary_samples_only": True,
            "classical_group_theorem_dependency": "Luks Theorem 3.2(6); defining-characteristic affine p-group",
            "source_sample_control": nonnormal_sample_control(),
            "large_rank_resource_ledger_not_execution": sampling_plan(128, F(1, 32), F(1, 1024)),
            "sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
            "dependency_sha256": {name: hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()
                                  for name in dependencies}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(receipt(), default=encode, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(rendered)
        print(args.output.resolve())
    else:
        print(rendered, end="")

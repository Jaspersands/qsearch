"""Freeze paid restrictions and bounded witness lifts, not quantum runs."""

import argparse
from dataclasses import asdict
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import numpy as np

import opi_reduction as o

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent/"orbit-norm-flat-2026-10-24/data"
NPZ_HASH = "f33a15681f41d581023812364c6c42587e571ac616fb11452cef7cd7325913cf"
PARENT_HASH = "7e805dda45ab9ce18f6e727135a30dda3beb8f21dfb2cb9acd9381ec935af51d"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded_digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "canonical_json_bytes": len(encoded)}


def native_input(K):
    if digest(DATA/"native.npz") != NPZ_HASH or digest(DATA/"cubic-parent.json") != PARENT_HASH:
        raise ValueError("frozen native provenance changed")
    parent = json.loads((DATA/"cubic-parent.json").read_text())["native"]
    domain = parent["domain"]
    g = o.Geometry(domain["p"], 3, domain["zeta"], tuple(row[0] for row in domain["orbits"]), K)
    if g.points != tuple(map(tuple, domain["orbits"])):
        raise ValueError("original ordered orbits changed")
    with np.load(DATA/"native.npz", allow_pickle=False) as data:
        if data["allowed"].shape != (2051, 2053) or data["allowed"].dtype != np.bool_:
            raise ValueError("frozen explicit input table changed shape/type")
        b = tuple(map(int, data["residual_coefficients"][:684]))
        if b != tuple(parent["multipliers"]):
            raise ValueError("native multipliers disagree with parent snapshot")
        halfsets = tuple(tuple(map(int, np.flatnonzero(row))) for row in data["allowed"][:684])
    return g, b, domain["eta_nonsquare"], halfsets


def compact_run(run):
    reduced = run["restriction"]
    if reduced is None:
        return run
    return {**run, "restriction": {key: value for key, value in reduced.items() if key != "lists"},
            "materialized_reduced_lists": {
                **encoded_digest(reduced["lists"]), "list_count": len(reduced["lists"]),
                "entries": sum(map(len, reduced["lists"])),
                "minimum_untrimmed_list_size": min(reduced["counts"]),
                "maximum_untrimmed_list_size": max(reduced["counts"]),
                "reconstruct": "restrict(original_g,b,nu,halfsets,saved_q1,saved_q2,saved_ell)['lists']"}}


def fixture(seed):
    g = o.geometry(13, 3, 3)
    rng = random.Random(seed)
    b = tuple(rng.randrange(1, 13) for _ in g.nodes)
    halfsets = tuple(tuple(sorted(rng.sample(range(13), 6))) for _ in g.nodes)
    return g, b, 2, halfsets


def small_lift(seed):
    g, b, nu, halfsets = fixture(seed)
    run = o.random_reduction(g, b, nu, halfsets, 3, seed=24, attempts=10)
    reduced = run["restriction"]
    if reduced is None:
        raise ArithmeticError("fixed small control exhausted restrictions; preserve input")
    for index, q0 in enumerate(product(range(13), repeat=3), start=1):
        if all(o.horner(q0, node, 13) in row for node, row in zip(g.nodes, reduced["lists"])):
            witness = o.lift_and_verify(g, b, nu, halfsets, reduced, q0)
            if witness["status"] != "VERIFIED_NATIVE_PERFECT":
                raise ArithmeticError("finite scalar solution failed native replay")
            return {"input_seed": seed, "geometry": asdict(g), "b": b, "nu": nu,
                    "halfsets": halfsets, "reduction": compact_run(run), "q0": q0,
                    "reference_search": "bounded_exhaustive_scalar_coefficients_NOT_scalable",
                    "scalar_candidates_examined": index, "witness": witness}
    raise ArithmeticError("small scalar control has no witness; do not reroll its input")


def frozen_trap():
    g = o.geometry(13, 3, 2)
    b, nu = (1, 2, 3, 4), 2
    halfsets = tuple(tuple(sorted(set(range(13))-{(v*(1-nu)*t*t+t) % 13 for t in range(13)})) for v in b)
    failed = o.restrict(g, b, nu, halfsets, (0, 0), (0, 0), 1)
    if failed["counts"] != (0, 0, 0, 0):
        raise ArithmeticError("deliberate frozen-restriction counterexample changed")
    repaired = o.random_reduction(g, b, nu, halfsets, 2, seed=241026, attempts=4)
    return {"geometry": asdict(g), "b": b, "nu": nu, "halfsets": halfsets,
            "zero_components": failed, "randomized_restriction": compact_run(repaired),
            "native_unsatisfiability_claimed": False}


def receipt():
    paths = ("opi_reduction.py", "test_opi_reduction.py", "make_receipt.py", "REDUCTION.md", "HANDOFF.md",
             "../orbit-residual-decoder-2026-10-24/orbit_decoder.py",
             "../orbit-norm-flat-2026-10-24/data/native.npz",
             "../orbit-norm-flat-2026-10-24/data/cubic-parent.json")
    before = {name: digest(ROOT/name) for name in paths}
    native = []
    for K in (68, 438):
        g, b, nu, halfsets = native_input(K)
        run = o.random_reduction(g, b, nu, halfsets, 769, seed=271026, attempts=4)
        native.append({"p": g.p, "M": len(g.nodes), "original_cubic_dimension": 204,
                       "dimension_in_this_run": g.dimension, "original_dimension_preserved": K == 68,
                       "same_original_halfsets_multipliers_nonsquare_ordered_orbits": True,
                       "native_npz_sha256": NPZ_HASH, "parent_snapshot_sha256": PARENT_HASH,
                       "result": compact_run(run), "native_polynomial_produced": False})
    result = {"status": "LOCAL_UNREVIEWED_REDUCTION_TO_KNOWN_SCALAR_OPI",
              "decision": "deprioritize_custom_cubic_capacity_backend_as_new_quantum_mechanism",
              "native_restrictions": native,
              "small_lifts": [small_lift(seed) for seed in (41, 42, 43, 44)],
              "frozen_restriction_counterexample": frozen_trap(),
              "external_theorem": {
                  "url": "https://arxiv.org/html/2610.12357v1#S1.SS2",
                  "statement": "Theorem1.8 and Section6.3; fixed-rate/density scalar OPI",
                  "dependency_not_project_discovery": True,
                  "finite_threshold_or_circuit_instantiated": False},
              "scope": {"large_native_problem_solved": False, "classical_dequantization": False,
                        "quantum_algorithm_executed": False, "new_candidate_admitted": False,
                        "novelty_or_independent_review_claimed": False, "uniform_output_sampler": False,
                        "main_checkout_modified": False},
              "source_sha256": before}
    if before != {name: digest(ROOT/name) for name in paths}:
        raise RuntimeError("source or frozen native input changed during the run")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = receipt()
    encoded = json.dumps(data, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")
    for run in data["native_restrictions"]:
        result = run["result"]
        print("Native dimension", run["dimension_in_this_run"], result["status"],
              "attempts", result["work"]["attempts_executed"], "; no native large witness")

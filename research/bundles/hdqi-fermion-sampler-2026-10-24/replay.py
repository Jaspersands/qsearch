"""Generate deterministic mathematical controls, not a speedup benchmark."""

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import random

import numpy as np

from fermion_sampler import (boundary, decode, perturbation_bound, prepare,
                             root, sample, word_phase)
from audit_controls import coherent_reference, dense_pilot, rational_law_control


def run():
    controls = []
    cases = [
        ("branching_tree", 6, [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)], 0.8),
        ("four_cycle", 4, [(0, 1), (1, 2), (2, 3), (3, 0)], 0.8),
        ("two_cycles", 4, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0)], 1.2),
        ("disconnected_with_isolate", 6, [(0, 1), (1, 2), (3, 4)], 0.8),
    ]
    for name, n, edges, beta in cases:
        model = root(n, edges)
        p = prepare(model, beta, bits=40)
        error = float(np.linalg.norm(coherent_reference(p) - dense_pilot(model, beta)))
        assert error < 1e-8
        control = rational_law_control(p)
        assert all(control[key] for key in (
            "target_normalized_exactly", "proposal_normalized_exactly",
            "envelope_holds_exactly", "all_dpp_branches_exact"))
        assert F(control["accepted_mass"]) == F(1, len(p.sectors))
        if name == "two_cycles":
            assert control["incoherent_shortcut_tv"] > 0.7
        controls.append({"name": name, "root_vertices": n, "root_edges": edges,
                         "native_generators": len(edges), "beta": beta,
                         "cycle_rank": model.cycle_rank, "flux_sectors": len(p.sectors),
                         "signed_state_l2_error_float_control": error,
                         "rational_backend": control,
                         "native_error_certified": p.native_error_certified})
    scalable = []
    for n in (32, 64, 128):
        model = root(n, [(i, (i - 1) // 2) for i in range(1, n)])
        p = prepare(model, 0.4, bits=16)
        rng = random.Random(7900 + n)
        draws = [sample(p, rng) for _ in range(3)]
        for draw in draws:
            y = draw["word"]
            assert draw["trials"] == 1 and decode(model, boundary(model, y), 0) == y
        scalable.append({"root_vertices": n, "native_generators": len(model.edges),
                         "cycle_rank": 0, "matrix_dimension": n,
                         "native_hilbert_dimension_not_constructed": str(1 << len(model.edges)),
                         "samples": draws, "quantization_bits": 16,
                         "exact_for_rational_surrogate": True,
                         "native_error_certified": False})
    cycle = root(4, cases[1][2])
    phase, x = word_phase(cycle, 15)
    assert phase == 2 and x == 0
    h, b = 1 << 20, 1 << 10
    m, d = h * b + h - 1, 2 * b + 2
    mass = F(m, 64 * (d + 1))
    here = Path(__file__).resolve().parent
    paths = [here / name for name in (
        "fermion_sampler.py", "audit_controls.py", "test_fermion_sampler.py",
        "replay.py", "FERMION_SAMPLER.md", "HANDOFF.md")]
    paths.append(here.parent / "hdqi-parent-gap-2026-10-23/parent_gap.py")
    return {
        "scope": "full canonical HDQI word sampling from a supplied line-graph root",
        "classical_algorithm": "exact rational DPP proposal with coherent-flux rejection",
        "algorithmic_cost": "exp(O(cycle_rank))*poly(root size, precision)",
        "forest_cost": "polynomial; all proposals accepted",
        "status": "LOCAL_UNREVIEWED_DERIVATION_AND_NUMERICAL_FRONTEND",
        "independent_review": False, "novelty_claim": False,
        "quantum_execution": False, "quantum_speedup_claim": False,
        "generic_degree_gap_resolved": False, "native_error_certified": False,
        "finite_controls": controls,
        "scalable_backend_runs": scalable,
        "single_sector_trace_falsifier": {
            "root": "four_cycle", "nonempty_native_word": 15,
            "native_trace": 0, "zero_flux_image_phase_power_of_i": phase,
            "zero_flux_image_majorana_subset": x, "zero_flux_trace": -1},
        "symbolic_nonmass_family_not_executed": {
            "root": "chain of hubs with private leaves", "hubs": h, "leaves_per_hub": b,
            "generators": m, "line_graph_max_degree_bound": d, "cycle_rank": 0,
            "beta_squared_times_d_plus_one": "1/64",
            "beta_squared_mass": str(mass),
            "beta_squared_mass_over_log_m": float(mass) / math.log(m)},
        "conditional_precision_bound_example": {
            "vertices": 8, "cycle_rank": 2,
            "assumed_certified_entry_and_scale_error": "1/1099511627776",
            "tv_bound": str(perturbation_bound(8, 2, F(1, 1 << 40), F(1, 1 << 40))),
            "assumption_certified_by_frontend": False},
        "next_blocker": "clean coherent flux amplitudes for extensive cycle rank; matched classical attacks",
        "source_hashes": {str(path.relative_to(here.parent)):
                          hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = run()
    payload = json.dumps(current, indent=2, sort_keys=True) + "\n"
    destination = Path(__file__).resolve().parent / "receipt.json"
    if args.write:
        destination.write_text(payload)
    elif args.check:
        if json.loads(destination.read_text()) != json.loads(payload):
            raise SystemExit("receipt replay mismatch")
        print("PASS: fresh replay matches receipt and all source hashes")
    else:
        print(payload, end="")

"""Live finite falsifiers and nonenumerating ledgers; no quantum execution."""

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

from flux_gap import (Interval, coherent_ledger, conditional, gap_certificate,
                      log_partition, sample_flux, source)
from flux_controls import (coherent_control, finite_control, flux_table,
                           trace_word_control, line_graph_positivity_falsifier,
                           gaussian_decomposition_control)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Interval):
        return {"lo": str(value.lo), "hi": str(value.hi), "width": str(value.width)}
    raise TypeError(type(value).__name__)


def run():
    cycle = source(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    two = source(4, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0)])
    k4 = source(4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
    cases = []
    for name, src in (("four_cycle", cycle), ("two_cycles", two), ("K4", k4)):
        for beta in (F(0), F(1, 32), F(1, 8)):
            control = finite_control(src, beta)
            assert control["gap"] >= control["analytic_gap_lower"] - 1e-12
            assert control["max_mixed_difference_column_sum"] <= control["analytic_influence_bound"] + 1e-12
            cases.append({"root": name, "beta": beta, **control})
    native = {
        "log_partition": log_partition(cycle, F(1, 8), 0, F(1, 1024)),
        "conditional": conditional(cycle, F(1, 8), 0, 0, F(1, 256)),
        "classical_flux_sample": sample_flux(cycle, F(1, 8), F(1, 2), seed=19),
        "full_pilot_sample": False, "floating_eigensolver_used": False,
    }
    ladder_size = 128
    edges = [(2*i, 2*i+1) for i in range(ladder_size)]
    edges += [(2*i+a, 2*i+a+2) for i in range(ladder_size-1) for a in (0, 1)]
    ladder = source(2*ladder_size, edges)
    logs = flux_table(cycle, F(1, 8))
    p = 1 / (1 + math.exp(float(logs[0] - logs[1])))
    delta = p - 0.5
    loss = 2 * delta * delta / (1 + math.sqrt(1 - 4 * delta * delta))
    copies = 10**9
    amplified = math.sqrt(-math.expm1(copies * math.log1p(-loss)))
    here = Path(__file__).resolve().parent
    paths = [here / name for name in (
        "flux_gap.py", "flux_controls.py", "test_flux_gap.py", "replay.py",
        "FLUX_GAP.md", "HANDOFF.md")]
    paths += [here.parent / "hdqi-fermion-sampler-2026-10-24" / name
              for name in ("fermion_sampler.py", "audit_controls.py", "FERMION_SAMPLER.md")]
    paths.append(here.parent / "hdqi-parent-gap-2026-10-23/parent_gap.py")
    paths.append(here.parent / "hdqi-paired-positivity-2026-10-24/paired_positivity.py")
    return {
        "status": "LOCAL_UNREVIEWED_LINE_GRAPH_FLUX_GAP_AND_IDEAL_CONSTRUCTION",
        "scope": "canonical independent HDQI words on a supplied simple line-graph root",
        "native_conditionals_interval_certified": True,
        "classical_flux_mixing_bound": "r exp[-t(1-3D beta^2)/r]",
        "regime": "0<=beta<=1/8, 3D beta^2<1; polynomial inverse gap required",
        "independent_review": False, "formal_proof": False,
        "quantum_execution": False, "compiled_quantum_circuit": False,
        "compiled_gaussian_stage": False, "novelty_claim": False,
        "quantum_speedup_claim": False, "generic_HDQi_gap_resolved": False,
        "finite_complete_flux_controls": cases,
        "common_resolvent_controls": [trace_word_control(k4, z, F(1, 16), 6)
                                      for z in range(8)],
        "certified_native_access_run": native,
        "dense_coherent_control": coherent_control(two, F(1, 8), time=32, slices=256),
        "gaussian_relative_phase_controls": [gaussian_decomposition_control(k4, F(1, 8), z)
                                             for z in range(8)],
        "same_output_classical_route_falsifier": line_graph_positivity_falsifier(),
        "uniform_flux_falsifier": {
            "single_four_cycle_bit_one_probability_float": p,
            "product_components_not_constructed": copies,
            "symbolic_product_trace_distance_float": amplified,
            "classically_factorable_not_hardness_example": True,
        },
        "extensive_rank_analytic_ledger_not_executed": {
            "vertices": 2*ladder_size, "edges": len(edges),
            "cycle_rank": ladder.r, "beta": F(1, 32),
            "certificate": gap_certificate(ladder, F(1, 32)),
            "coherent_resources": coherent_ledger(ladder, F(1, 32)),
            "finite_sector_enumeration": False, "quantum_execution": False,
            "hardness_example": False,
        },
        "remaining_blockers": [
            "independent proof review and prior-art comparison",
            "same-output classical sampling on connected high-rank roots",
            "useful native task and a justified classical complexity comparison",
            "compiled coherent arithmetic and relative-phase-safe Gaussian stage",
        ],
        "source_hashes": {str(path.relative_to(here.parent)):
                          hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
    }


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).with_name("receipt.json")
    data = json.loads(json.dumps(run(), default=encode))
    if args.write:
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {path}")
    elif args.check:
        if data != json.loads(path.read_text()):
            raise SystemExit("FAIL: fresh replay or source hash mismatch")
        print(f"PASS: fresh replay matches receipt and all {len(data['source_hashes'])} source hashes")
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

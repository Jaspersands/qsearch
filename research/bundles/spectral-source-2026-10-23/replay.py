"""Generate bounded physical controls, not an execution of the resource cap."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

from spectral_source import finite_qpe, source_budget, trace_distance


def run():
    root = Path(__file__).resolve().parent
    spectra = np.array([0.65, 0.25, 0.10])
    indices = np.arange(3)
    basis = np.exp(2j * np.pi * np.outer(indices, indices) / 3) / np.sqrt(3)
    rho = (basis * spectra) @ basis.conj().T
    top = np.outer(basis[:, 0], basis[:, 0].conj())
    grid = 8
    ideal = finite_qpe(rho, grid)
    controls = []
    for base in (32, 128, 512):
        counts = [base * (1 << j) for j in range(3)]
        actual = finite_qpe(rho, grid, counts)
        selected = sum(actual[y] for y in range(grid) if 4*y/grid-1 > 0.4)
        success = float(np.trace(selected).real)
        controls.append({
            "grid": grid,
            "program_copies_per_power": counts,
            "target_copies": 1,
            "program_copies": sum(counts),
            "complete_instrument_trace_distance": sum(
                trace_distance(a, b) for a, b in zip(actual, ideal)),
            "analytic_instrument_bound": min(1, sum(
                2 * (np.pi * (1 << j)/2)**2 / n for j, n in enumerate(counts))),
            "finite_selected_probability": success,
            "finite_conditional_top_error": trace_distance(selected/success, top),
            "unconditional_target_error": trace_distance(sum(actual), top),
            "protocol_gap_schedule_executed": False,
        })
    return {
        "status": "FINITE_CHANNEL_CHECKS_AND_PROPOSED_RESOURCE_ENVELOPE",
        "mechanism": "known density-matrix exponentiation and quantum PCA",
        "novel_algorithm_claim": False,
        "full_source_protocol_executed": False,
        "hsp_receiver_executed": False,
        "native_hard_application_identified": False,
        "source_contract": "fresh jointly IID mixed copies; supplied positive top gap",
        "controls": controls,
        "budget_examples": [source_budget(8, gap, Fraction(1, 100)).receipt()
                            for gap in (Fraction(1, 2), Fraction(1, 8), Fraction(1, 32))],
        "source_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in ("spectral_source.py", "test_spectral_source.py", "replay.py")
        },
        "numpy_version": np.__version__,
        "scope": "Small dense calculations are verifier controls, not the online input model.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="ascii")
        print(json.dumps({"artifact": str(args.output.resolve()),
                          "status": result["status"],
                          "instrument_distances": [x["complete_instrument_trace_distance"]
                                                   for x in result["controls"]]}))
    else:
        print(encoded)

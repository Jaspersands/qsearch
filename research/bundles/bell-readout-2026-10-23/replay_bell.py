"""Reproducible exact Bell-readout controls; no thermal sampler execution."""

import hashlib
import json
from pathlib import Path

import numpy as np

from bell_pushforward import (
    circuit_target_density, exact_chain_evidence, paired_readout_value,
)


def evidence():
    amplitudes = np.array([1, 1j, 2, -1j]) / np.sqrt(7)
    phases = np.array([1, 1, -1, 1j])
    decoder = [0, 1]
    density = circuit_target_density(amplitudes, [0, 1, 1, 0], decoder, phases)
    values = [paired_readout_value(u, amplitudes.__getitem__, (1, 1),
                                   decoder.__getitem__, phases.__getitem__, 1,
                                   lambda _: 1) for u in range(4)]
    mean = float(sum(abs(amplitudes[u])**2*values[u] for u in range(4)))
    exact = float(np.trace(density @ np.array([[0, 1], [1, 0]])).real)
    if abs(mean-exact) > 1e-12 or abs(exact + 4/7) > 1e-12:
        raise ArithmeticError("CT paired readout reference mismatch")
    return {
        "status": "exact_controls_pass_composition_review_pending",
        "speedup_admitted": False,
        "novelty_admitted": False,
        "general_coherent_simulation_admitted": False,
        "thermal_mpo_constructor_implemented": False,
        "source_mps_sampler_executed": False,
        "requires_decoder_for_classical_output": False,
        "decoder_free_output_scope": "Bell-label sampling only",
        "ct_pauli_extension_requires_efficient_decoder_and_amplitude_access": True,
        "requires_valid_target_approximation_promises": True,
        "ct_paired_readout_control": {
            "paired_mean": mean, "partial_trace_reference": exact,
            "analytic_reference": "-4/7",
            "maximum_absolute_estimator": max(map(abs, values)),
            "dense_calibration_only": True,
        },
        "in_window": exact_chain_evidence(5, 2),
        "out_of_window_counterexample": exact_chain_evidence(5, 3),
        "dependencies": [
            "https://arxiv.org/abs/2610.06667v2",
            "https://arxiv.org/html/2007.11174v2#S4.SS1",
            "https://arxiv.org/abs/1201.3974",
            "https://arxiv.org/html/0911.1624",
        ],
    }


def main():
    root = Path(__file__).resolve().parent
    record = evidence()
    names = ("bell_pushforward.py", "test_bell_pushforward.py", "replay_bell.py",
             "BELL_READOUT_DECISION.md")
    record["source_sha256"] = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names
    }
    path = root / "bell_receipt.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="ascii")
    print(json.dumps({"receipt": str(path), "status": record["status"],
                      "in_window_tv": record["in_window"]["bell_pushforward_tv"],
                      "counterexample_tv": record["out_of_window_counterexample"]["bell_pushforward_tv"]}))


if __name__ == "__main__":
    main()

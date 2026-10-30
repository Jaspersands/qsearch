"""Native nonlinear-decoder controls and conditional classical readout plans."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np

from decoder_margin import (arbitrary_pauli_plan, lift, recommended_cutoff,
                           short_word_plan, verify_ball)
from margin_controls import (complete_root_quotient, control, cycle_decoder,
                             cycle_model, hermitian_word, matrix, pullback)


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def run():
    model = cycle_model(5, F(1, 16), [1, -1, F(1, 2), 1, F(-1, 3)])
    decoder = cycle_decoder(model)
    small = []
    for word in (1, 2, 4, 8, 16, 3, 5):
        observable = hermitian_word(model, word)
        row = control(model, decoder, observable, word, 2-word.bit_count())
        assert row["good_column_error"] == 0
        small.append({"word": word, "observable": observable, **row})
    square = cycle_model(4, F(1, 16))
    dec4 = cycle_decoder(square)
    observable = hermitian_word(square, 5)
    actual = pullback(square, dec4, observable)
    guessed = matrix(lift(square, observable, 5), 4)
    state = np.zeros(16)
    state[[1, 2, 4, 8]] = 0.5
    actual_value = float(np.vdot(state, actual @ state).real)
    guessed_value = float(np.vdot(state, guessed @ state).real)
    assert actual_value == 1 and guessed_value == 0.5

    native = complete_root_quotient(32, F(1, 128))
    dec = cycle_decoder(native)
    radius = (native.pilot.m-1)//2
    precision = F(1, 4096)
    cutoff = recommended_cutoff(native, precision)
    plan = arbitrary_pauli_plan(native, dec, native.paulis[-1], radius, cutoff, precision)
    assert plan["classical_reduction_budget_met"]
    assert plan["canonical_plan"]["status"] == "marked_cluster_comparator"
    first = (1 << radius)-1
    second = first << radius
    nonlinear = (dec(native.label(first) ^ native.label(second))
                 != dec(native.label(first)) ^ dec(native.label(second)))
    assert nonlinear
    s = 1024
    v, m, degree = 2*s*s, s*s*(2*s*s-1), 4*s*s-4
    beta = F(1, 32*s)
    here = Path(__file__).resolve().parent
    paths = [here/name for name in (
        "decoder_margin.py", "margin_controls.py", "test_decoder_margin.py",
        "replay.py", "DECODER_MARGIN.md", "HANDOFF.md")]
    dependencies = [
        "hdqi-decoded-observables-2026-10-24/decoded_observables.py",
        "hdqi-coherent-sign-2026-10-24/coherent_sign.py",
        "hdqi-sign-sampler-2026-10-24/sign_sampler.py",
        "hdqi-defect-observables-2026-10-24/defect_observables.py",
        "hdqi-defect-observables-2026-10-24/DEFECT_OBSERVABLES.md",
        "hdqi-cluster-baseline-2026-10-24/cluster_baseline.py",
        "hdqi-cluster-baseline-2026-10-24/CLUSTER_BASELINE.md",
    ]
    paths += [here.parent/path for path in dependencies]
    return {
        "status": "LOCAL_UNREVIEWED_NONLINEAR_DECODER_MARGIN_REDUCTION",
        "target": "specified Pauli expectations of the ACTUAL decoded HDQI output",
        "gibbs_accuracy_assumed": False, "production_estimator_executed": False,
        "quantum_execution": False, "independent_review": False, "novelty_claim": False,
        "quantum_speedup_claim": False, "full_output_sampling": False,
        "finite_decoder_contract": verify_ball(model, decoder, 2),
        "signed_native_controls": small,
        "small_short_word_plan": short_word_plan(model, model.paulis[0], 1, 2),
        "missing_margin_counterexample": {
            "root": "four-cycle", "pilot": "normalized native degree-one filter H_hat|0>",
            "pilot_weight_cutoff": 1, "pilot_tail_mass": 0,
            "decoder_check": verify_ball(square, dec4, 1),
            "observable": observable, "actual_decoded_expectation": actual_value,
            "incorrect_single_lift_expectation": guessed_value,
            "admission": arbitrary_pauli_plan(square, dec4, observable, 1, cutoff=1),
        },
        "live_explicit_input_no_statevector": {
            "root_vertices": 32, "native_generators": native.pilot.m,
            "physical_qubits": native.n, "anticommutation_degree": native.pilot.degree,
            "beta": native.pilot.beta, "decoder_radius": radius, "pilot_cutoff": cutoff,
            "binary_decoder_nonlinearity_witness": nonlinear,
            "uniform_radius_provenance": "local all-size repetition-quotient algebra, not ball enumeration",
            "plan": plan,
        },
        "large_s_symbolic_family_not_constructed": {
            "s": s, "root_vertices": v, "generators": m, "degree": degree,
            "beta": beta, "degree_scale": (degree+1)*beta*beta,
            "beta_times_degree": beta*degree, "beta_squared_mass": beta*beta*m,
            "decoder_radius": (m-1)//2, "quantum_execution": False,
            "classical_hardness_claim": False,
        },
        "remaining_frontier": [
            "joint output sampling rather than specified additive Pauli readouts",
            "average-case decoders without a comparable uniform ball guarantee",
            "a useful non-Pauli or genuinely quantum downstream task",
            "independent review of this reduction and its cluster-estimator dependencies",
        ],
        "source_hashes": {str(p.relative_to(here.parent)):
                          hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).with_name("receipt.json")
    data = json.loads(json.dumps(run(), default=encode))
    if args.write:
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {path}")
    elif args.check:
        if data != json.loads(path.read_text()):
            raise SystemExit("FAIL: fresh replay or source hashes differ")
        print(f"PASS: fresh replay and all {len(data['source_hashes'])} source hashes match")
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

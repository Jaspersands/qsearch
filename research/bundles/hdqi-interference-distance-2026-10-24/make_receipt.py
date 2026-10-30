"""Run a bounded public distance certificate and physical reference controls."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random

import interference_distance as d

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt():
    paths = ("interference_distance.py", "test_interference_distance.py", "make_receipt.py",
             "INTERFERENCE_DISTANCE.md", "HANDOFF.md",
             "../hdqi-output-sampling-2026-10-24/output_sampling.py",
             "../hdqi-output-sampling-2026-10-24/OUTPUT_SAMPLING.md",
             "../hdqi-decoded-observables-2026-10-24/decoded_observables.py",
             "../hdqi-coherent-sign-2026-10-24/coherent_sign.py",
             "../hdqi-sign-sampler-2026-10-24/sign_sampler.py",
             "../central-rank-2026-10-23/central_rank.py")
    hashes = {name: digest(ROOT/name) for name in paths}
    model = d.scrambled_pairs()
    sampler = d.UniformSampler(model, 2, F(1, 1000))
    rng = random.Random(241025)
    controls = []
    for beta in (F(0), F(1, 16), F(1, 4), F(1)):
        small, decoder = d.nonlinear_fixture(beta)
        controls.append(d.dense_control(small, decoder, 1))
    result = {"status": "LOCAL_UNREVIEWED_RELATIVE_DISTANCE_CLASSICAL_COMPARATOR",
              "public_input": {"n": model.n, "paulis": model.paulis,
                               "couplings": [str(j) for j in model.pilot.couplings],
                               "beta": str(model.pilot.beta), "edges": model.pilot.edges,
                               "generator": "fixed_seeded_symplectic_transvections_NOT_uniform_Clifford",
                               "seed": 241024},
              "certificate": sampler.plan,
              "uniform_output_examples": [sampler.sample(rng) for _ in range(16)],
              "dense_physical_controls": controls,
              "scope": {"full_joint_law_claimed_uniform": False,
                        "arbitrary_basis_change_allowed": False,
                        "general_distance_algorithm": False,
                        "polynomial_sign_cost_required": False,
                        "general_HDQi_gap_resolved": False,
                        "new_quantum_algorithm": False,
                        "independent_review": False,
                        "main_checkout_changed": False},
              "source_sha256": hashes}
    if hashes != {name: digest(ROOT/name) for name in paths}:
        raise RuntimeError("a source changed during replay")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(receipt(), indent=2, sort_keys=True, allow_nan=False)+"\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")

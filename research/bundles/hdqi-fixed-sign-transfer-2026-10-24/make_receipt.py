"""Replay fixed-target transfer controls without building any large pilot."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import fixed_sign as f

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt():
    paths = ("fixed_sign.py", "test_fixed_sign.py", "make_receipt.py", "TRANSFER.md", "HANDOFF.md",
             "../hdqi-interference-distance-2026-10-24/interference_distance.py",
             "../hdqi-defect-observables-2026-10-24/DEFECT_OBSERVABLES.md",
             "../hdqi-output-sampling-2026-10-24/output_sampling.py",
             "../hdqi-decoded-observables-2026-10-24/decoded_observables.py",
             "../hdqi-coherent-sign-2026-10-24/coherent_sign.py",
             "../hdqi-sign-sampler-2026-10-24/sign_sampler.py",
             "../central-rank-2026-10-23/central_rank.py")
    hashes = {name: digest(ROOT/name) for name in paths}
    controls = []
    for k in (1, 2, 4, 8):
        controls.append({"actual_physical_decoder": f.dense_audit(f.repeated_model(k), lambda s: s >> 1),
                         "analytic_formula": f.repeated_formula(k)})
    signs = [f.dense_audit(f.repeated_model(5), lambda s: s >> 1, mask) for mask in range(32)]
    if abs(sum(row["coherent_bad_mass"] for row in signs)/32-signs[0]["pilot_decoding_failure"]) > 1e-12:
        raise ArithmeticError("random-sign identity failed")
    n = 32
    ps = [(1 << j, 0, 0) for j in range(n)]+[(0, 1 << j, 0) for j in range(n)]
    ps.append(((1 << n)-1, (1 << n)-1, n % 2))
    model = f.i.o.d.Physical.create(n, ps, [1]*len(ps), F(1, 128))
    _, positive = f.certify_transfer(model, 2, F(1, 10000))
    _, collision = f.certify_transfer(f.repeated_model(8), 1)
    _, budget = f.certify_transfer(f.repeated_model(8), 0, max_kernel_words=1)
    if positive["status"] != "CERTIFIED_IDEAL_PILOT_TRANSFER" or collision["status"] != "NO_CERTIFICATE":
        raise ArithmeticError("transfer certificate controls failed")
    result = {"status": "LOCAL_UNREVIEWED_FIXED_SIGN_TRANSFER_AUDIT",
              "negative_transfer_record": {"id": "NEG-HDQi-FIXED-SIGN-DILUTION-20261024",
                  "falsified_claim": "Small canonical decoding failure alone certifies a specified fixed-sign Gibbs target",
                  "native_target": "H=Z at beta=1; K duplicate coefficients 1/K; actual parity decoder",
                  "rational_certificate": f.repeated_certificate(65536),
                  "published_random_sign_theorem_falsified": False},
              "dense_repeated_controls": controls,
              "large_analytic_controls": [f.repeated_formula(k) for k in (16, 256, 65536, 2**32)],
              "random_sign_control": {"sign_choices_checked": len(signs),
                  "pilot_decoding_failure": signs[0]["pilot_decoding_failure"],
                  "average_coherent_bad_mass": sum(row["coherent_bad_mass"] for row in signs)/32,
                  "fixed_all_plus_bad_mass": signs[0]["coherent_bad_mass"],
                  "gauge_all_minus_bad_mass": signs[-1]["coherent_bad_mass"]},
              "correlated_sign_control": f.sign_structure_control(),
              "positive_input": {"n": model.n, "paulis": model.paulis,
                                 "couplings": [str(j) for j in model.pilot.couplings],
                                 "beta": str(model.pilot.beta)},
              "positive_ideal_transfer_certificate": positive,
              "collision_refusal": collision, "kernel_budget_refusal": budget,
              "scope": {"all_size_proofs_independently_reviewed": False,
                        "large_pilot_built": False, "quantum_algorithm_executed": False,
                        "new_quantum_algorithm_admitted": False, "general_pilot_gap_resolved": False,
                        "known_hard_Gibbs_family_instantiated": False,
                        "whole_repository_validated": False, "main_checkout_changed": False},
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

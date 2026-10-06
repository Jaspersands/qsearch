"""Finite original-source baseline; optional FLINT construction, exact audit."""

import argparse
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from theorems.native_rlwe_primal_babai import (
    exact_profile, nearest_plane, negacyclic, primal_rows, source_certificate)


def encoded(value):
    if isinstance(value, Fraction):
        return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}
    if isinstance(value, dict):
        return {k: encoded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [encoded(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dimension", type=int, choices=(64, 256, 1024), default=64)
    parser.add_argument("--seed", type=int, default=290960)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    from flint import fmpz_mat
    parameters = {64: (16777259, Fraction(25, 6)),
                  256: (4294967357, Fraction(45, 8)),
                  1024: (1099511627803, Fraction(7))}
    d = args.dimension
    q, log_upper = parameters[d]
    rng = random.Random(args.seed)
    a = [rng.randrange(q) for _ in range(d)]
    native = primal_rows(a, q)
    original = fmpz_mat(native)
    started = time.perf_counter()
    reduced, transform = original.lll(transform=True)
    lll_seconds = time.perf_counter()-started
    assert transform*original == reduced and abs(int(transform.det())) == 1
    rows = [[int(reduced[i, j]) for j in range(2*d)] for i in range(2*d)]
    profile = exact_profile(rows)
    assert profile["leading_gram_determinants"][-1] == q**(2*d)
    c = negacyclic(a)
    assert all((row[d+i]-sum(c[i][j]*row[j] for j in range(d))) % q == 0
               for row in rows for i in range(d))
    certificate = source_certificate(d, profile["gs_squared"], log_upper)
    print(json.dumps({"stage": "profile", "d": d, "q": q,
                      "lll_seconds": lll_seconds,
                      "min_gs_squared_reference": float(min(profile["gs_squared"])),
                      "spherical_failure_reference": float(certificate["spherical"]["failure_upper"]),
                      "elliptical_failure_reference": float(certificate["elliptical"]["total_failure_upper"])}),
          flush=True)
    # Within-promise algebra controls, NOT draws from either research source law.
    controls = []
    for radius in (1, 10, 50, 100, 1000, 5000):
        secret = [rng.randrange(-radius, radius+1) for _ in range(d)]
        error = [rng.randrange(-radius, radius+1) for _ in range(d)]
        b = [(sum(c[i][j]*secret[j] for j in range(d))+error[i]) % q
             for i in range(d)]
        centered_b = [(v+q//2) % q-q//2 for v in b]
        answer = nearest_plane(rows, [0]*d+centered_b, profile)
        controls.append({"radius": radius, "secret": secret, "error": error,
                         "b": b, "decoded_secret": answer["point"][:d],
                         "correct": answer["point"][:d] == secret})
    payload = {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
               "scope": "one_original_normal_form_public_label",
               "quantum_algorithm": False, "asymptotic_attack_proved": False,
               "independent_review": False, "source_distribution_samples": False,
               "seed": args.seed, "d": d, "q": q, "label": a,
               "log_dimension_upper": encoded(log_upper), "construction_backend": "python-flint-0.9.0",
               "lll_seconds": lll_seconds, "total_seconds": time.perf_counter()-started,
               "native_row_basis": native, "reduced_row_basis": rows,
               "unimodular_transform": [[int(transform[i, j]) for j in range(2*d)]
                                        for i in range(2*d)],
               "leading_gram_determinants_hex": [hex(x) for x in profile["leading_gram_determinants"]],
               "certificate": encoded(certificate), "controls": controls,
               "source_transfer_losses_paid": False, "held_out_verification_run": False}
    if args.save:
        path = Path(__file__).with_name(f"native_rlwe_primal_babai_d{d}_seed{args.seed}.json")
        path.write_text(json.dumps(payload, indent=2)+"\n")
        print(json.dumps({"saved": str(path), "total_seconds": payload["total_seconds"],
                          "controls_correct": [x["correct"] for x in controls]}), flush=True)


if __name__ == "__main__":
    main()

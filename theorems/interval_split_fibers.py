"""Divisor-free public kernel construction from two split polynomial fibers.

Greedy quadratic compositions can fail during PUBLIC setup; such a prefix is
never accepted as a frame. A positive exact Weil lower bound gives a uniform
setup guarantee in a restricted regime, not at arbitrary degree. The output
feeds the existing native translation-frame solver, not circuit search.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import random
import sys

from sympy.ntheory import sqrt_mod

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.interval_character_rounding import field, native_moments, parameters
from theorems.interval_subgroup_rounding import radius as torus_radius, round_frame, translation_frame
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import ring

REPORT = ROOT / "research/classical_baselines/interval_split_fibers.json"


def setup_bound(p, constraints):
    """Analytic bound only: never allocate an explicit length-p object here."""
    ring(p)
    integer(constraints, "distinct fiber constraints", 1, min(p - 1, 4096))
    M = constraints
    root = math.isqrt(p)
    root += int(root * root < p)
    coefficient = Fraction(M, 2) - 1 + Fraction(1, 1 << M)
    lower = Fraction(p, 1 << M) - coefficient * root - Fraction(M, 2)
    return {"prime_decimal": str(p), "distinct_constraints": M,
            "sqrt_p_outward_upper_integer": root,
            "squarefree_Weil_sum_coefficient_exact": rational(coefficient),
            "zero_value_correction_upper_exact": rational(Fraction(M, 2)),
            "legal_shifts_uniform_count_lower_exact": rational(lower),
            "every_distinct_constraint_set_has_a_legal_shift_certified": lower > 0,
            "full_field_table_or_quantum_state_materialized": False}


def degree_parameters(p, ell):
    field(p)
    integer(ell, "power-of-two fiber degree", 1, p // 2)
    if ell & (ell - 1):
        raise ValueError("this construction requires a power-of-two degree")


def construct(p, ell):
    """Target-independent, deterministic public setup; charge every shift test."""
    degree_parameters(p, ell)
    bound = setup_bound(p, ell)
    A, B, stages = {0}, {1}, []
    legendre_tests = roots_extracted = 0
    for _ in range(ell.bit_length() - 1):
        values = sorted(A | B)
        selected, rejected_zero, rejected_nonsquare = None, 0, 0
        for b in range(p):
            for v in values:
                difference = (v - b) % p
                legendre_tests += 1
                if pow(difference, (p - 1) // 2, p) != 1:
                    rejected_zero += int(difference == 0)
                    rejected_nonsquare += int(difference != 0)
                    break
            else:
                selected = b
                break
        stage = {"input_fiber_zero": sorted(A), "input_fiber_one": sorted(B),
                 "distinct_nonzero_square_constraints": len(values),
                 "selected_shift": selected, "candidate_shifts_tested": p if selected is None else selected + 1,
                 "rejected_zero_shifts": rejected_zero, "rejected_nonsquare_shifts": rejected_nonsquare}
        stages.append(stage)
        if selected is None:
            if bound["every_distinct_constraint_set_has_a_legal_shift_certified"]:
                raise ArithmeticError("exhausted setup contradicts the uniform Weil bound")
            return {"p": p, "ell": ell, "achieved_degree": len(A),
                    "status": "PUBLIC_FRAME_SETUP_EXHAUSTED_NOT_HARDNESS", "stages": stages,
                    "setup_Weil_certificate": bound, "waveform": None,
                    "original_problem_unsatisfiability_claimed": False,
                    "modular_character_tests_charged": legendre_tests,
                    "modular_square_roots_charged": roots_extracted,
                    "affine_target_used_to_select_setup": False}
        new = []
        for fiber in (A, B):
            image = set()
            for v in sorted(fiber):
                roots = tuple(map(int, sqrt_mod((v - selected) % p, p, all_roots=True)))
                roots_extracted += 1
                if len(roots) != 2 or roots[0] == roots[1] or any((r * r + selected) % p != v for r in roots):
                    raise ArithmeticError("verified nonzero square did not have two exact preimages")
                image.update(roots)
            new.append(image)
        if len(new[0]) != 2 * len(A) or len(new[1]) != 2 * len(B) or new[0] & new[1]:
            raise ArithmeticError("two polynomial fibers lost distinctness or multiplicity")
        A, B = new
    C, FA, FB = ring(p), ring(p)([1]), ring(p)([1])
    for a in sorted(A):
        FA *= C([-a, 1])
    for b in sorted(B):
        FB *= C([-b, 1])
    if len(A) != ell or len(B) != ell or FA - FB != C([1]):
        raise ArithmeticError("two fully split monic fibers do not differ by exactly1")
    w = [int(x in A) - int(x in B) for x in range(p)]
    if any(native_moments(p, ell, w)) or sum(pow(x, ell, p) * v for x, v in enumerate(w)) % p != (-ell) % p:
        raise ArithmeticError("Newton moment identities fail in original field")
    return {"p": p, "ell": ell, "achieved_degree": ell, "status": "VERIFIED_TWO_FULLY_SPLIT_FIBERS",
            "stages": stages, "setup_Weil_certificate": bound, "fiber_zero": sorted(A), "fiber_one": sorted(B),
            "fiber_zero_polynomial_coefficients": [int(FA[i]) for i in range(ell + 1)],
            "fiber_one_polynomial_coefficients": [int(FB[i]) for i in range(ell + 1)],
            "polynomial_difference_constant": 1, "waveform": w,
            "squared_waveform_norm": 2 * ell, "first_forbidden_moment": (-ell) % p,
            "modular_character_tests_charged": legendre_tests, "modular_square_roots_charged": roots_extracted,
            "affine_target_used_to_select_setup": False,
            "input_model": "original prime p, full support0..p-1, degree ell; no divisor hypothesis"}


@lru_cache(maxsize=8)
def public_frame(p, ell):
    setup = construct(p, ell)
    if setup["waveform"] is None:
        return setup, None
    model = translation_frame(p, ell, setup["waveform"], expected_first=(-ell) % p, expected_norm=2 * ell)
    return setup, model


def radius(p, ell):
    degree_parameters(p, ell)
    amount = (2 * ell + 1) * (4 * p - 1).bit_length()
    k = math.isqrt(amount // 2)
    while 2 * k * k < amount:
        k += 1
    return min(p // 2, k - 1)


def solve(p, d, ell, u, word, *, seed=4583, attempts=16, rounding="independent"):
    parameters(p, d, u)
    degree_parameters(p, ell)
    if d > ell:
        raise ValueError("completed public fiber degree must cover the native codimension")
    if len(word) != p or any(type(a) is not int or not 0 <= a < p for a in word):
        raise ValueError("canonical full public word required")
    setup, model = public_frame(p, ell)
    if model is None:
        return {"p": p, "d": d, "ell": ell, "u": u, "setup": setup, "solution": None,
                "status": setup["status"], "affine_target_admitted_to_rounding": False}
    row = round_frame(model, d, u, word, seed=seed, attempts=attempts, rounding=rounding)
    row["resource_model"]["setup"] = "deterministic full-prime scans for each quadratic layer plus exact modular square roots and polynomial fiber verification; actual counts saved"
    return row | {"setup": setup, "affine_target_admitted_to_rounding": True}


def run_controls():
    controls = []
    for p, ell in ((347, 8), (1019, 16)):
        rng = random.Random(4591 + p)
        candidates = [(min(e, torus_radius(p, e, torus=t)), e, t)
                      for t, order in (("split", p - 1), ("nonsplit", p + 1))
                      for e in range(ell, p // 2 + 1) if order % e == 0]
        prior_u, prior_ell, prior_kind = min(candidates)
        for label, y in (("uniform_public_word", [rng.randrange(p) for _ in range(p)]),
                         ("quarter_field_spike", [p // 4] + [0] * (p - 1))):
            u = min(ell, radius(p, ell))
            rounding = "nearest" if ell <= radius(p, ell) else "independent"
            L = 2 * u + 1
            score = Fraction(2 * L, 3 * p) + Fraction(1, 3 * p * L)
            controls.append({"input_source": label, "best_torus_certified_radius": prior_u,
                             "best_torus_order": prior_ell, "best_torus_type": prior_kind,
                             "uniform_interval_KV_score_exact": rational(score),
                             "quantum_uniform_interval_sufficient_condition_met": 4 * u <= p - 1 and Fraction(ell, p) < score,
                             **solve(p, ell, ell, u, y, rounding=rounding)})
    return {"schema_version": "interval-split-fibers-v1", "controls": controls,
            "setup_only_controls": [construct(1021, 4), construct(4093, 8)],
            "failed_public_setups": [construct(347, 16), construct(4093, 16)],
            "analytic_large_field_setup_only_no_state_materialized": setup_bound((1 << 61) - 1, 16),
            "all_declared_native_targets_verified": all(r["solution"] is not None for r in controls),
            "general_unconditional_setup_at_arbitrary_degree_claimed": False,
            "novelty_quantum_speedup_or_prescribed_sampling_claimed": False,
            "local_research_derivation_independent_review_pending": True,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("interval_subgroup_rounding.py", "interval_character_rounding.py", "prime_character_opi.py", "prime_character_capacity_source.py", "bpqm_gibbs_frontier.py")},
            "literature": ["https://doi.org/10.1073/pnas.34.5.204", "https://web.math.princeton.edu/~nmk/old/estcharsums.pdf",
                           "https://arxiv.org/abs/2411.12553"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"native": [{"p": r["p"], "ell": r["ell"], "u": r["u"],
                       "best_torus_radius": r["best_torus_certified_radius"],
                       "norm": r["attempts"][-1]["centered_infinity_norm"],
                       "denominator_bits": r["coordinate_denominator_bits"]} for r in report["controls"]],
                      "failed_setups": [{"p": r["p"], "requested_degree": r["ell"],
                          "achieved_degree": r["achieved_degree"], "last_candidates_tested": r["stages"][-1]["candidate_shifts_tested"]}
                          for r in report["failed_public_setups"]]}, indent=2))


if __name__ == "__main__":
    main()

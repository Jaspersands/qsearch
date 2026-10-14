"""Actual full-root classical decoding for explicit small signed error alphabets.

Integer carries are divided before F3 reduction. This is a bounded-noise
baseline, not a general Gaussian LWE solver, unknown-phase decoder or novelty claim.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random

from flint import nmod_mat

from native_affine_fibre_relaxation import canonical_vector, NonFreeRank
from native_small_multiple_completion import _records, _rational, PublicBasisCache
from native_classical_modulus_descent import digest
from nil3_state_hsp_descent_receiver import solve_full_rank_f3
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord
from ternary_phase_qubit_decoder import quadratic_equation, symmetric_basis

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_SMALL_ALPHABET_DECODER.md"
REPORT = ROOT / "research/classical_baselines/native_small_alphabet_decoder.json"
METHODS = ("cubic", "quadratic")


def feature_width(n, method="cubic"):
    integer(n, "positive original dimension", 1)
    if method not in METHODS: raise ValueError("explicit cubic or quadratic method required")
    return 3*n+comb(n, 2)+n*(n-1)+comb(n, 3) if method == "cubic" else n*(n+1)//2+n


def feature_layout(n, method="cubic"):
    feature_width(n, method)
    if method == "quadratic":
        return tuple(("quadratic", pair) for pair in symmetric_basis(n))+tuple(("u", (i,)) for i in range(n))
    return (tuple(("u", (i,)) for i in range(n))+tuple(("u2", (i,)) for i in range(n))+
        tuple(("uij", ij) for ij in combinations(range(n), 2))+
        tuple(("u2j", (i, j)) for i in range(n) for j in range(n) if i != j)+
        tuple(("uijk", ijk) for ijk in combinations(range(n), 3))+tuple(("v", (i,)) for i in range(n)))


def features(u, v=None, method="cubic"):
    u = tuple(u);canonical_vector(u, len(u), 3)
    if method == "cubic":
        if v is None: raise ValueError("explicit canonical next-trit vector required")
        v = canonical_vector(v, len(u), 3)
    out = []
    for kind, indices in feature_layout(len(u), method):
        if kind == "u": value = u[indices[0]]
        elif kind == "v": value = v[indices[0]]
        elif kind == "u2": value = u[indices[0]]**2
        elif kind == "u2j": value = u[indices[0]]**2*u[indices[1]]
        else:
            value = 1
            for i in indices: value *= u[i]
        out.append(value % 3)
    return tuple(out)


def cubic_equation(label, response):
    label = tuple(label);canonical_vector(label, len(label), 9)
    integer(response, "canonical low9 response")
    if not label or response >= 9: raise ValueError("nonempty canonical low9 input required")
    a, t, n = label, response, len(label)
    row = tuple(((x-x**3)//3-t*t*x+x**3) % 3 for x in a)
    row += tuple((t*x*x-x**3) % 3 for x in a)
    row += tuple(2*t*a[i]*a[j] % 3 for i, j in combinations(range(n), 2))
    row += tuple(-a[i]*a[i]*a[j] % 3 for i in range(n) for j in range(n) if i != j)
    row += tuple(-2*a[i]*a[j]*a[k] % 3 for i, j, k in combinations(range(n), 3))
    row += tuple(x % 3 for x in a)
    return row, -((t**3-t)//3) % 3


def compile_equations(records, method):
    if method == "cubic":
        pairs = tuple(cubic_equation(tuple(x % 9 for x in s.label), s.value % 9) for s in records)
    else:
        pairs = tuple(quadratic_equation(tuple(x % 3 for x in s.label), s.value % 3) for s in records)
    return tuple(a for a, _ in pairs), tuple(b for _, b in pairs)


def high_root_lift(records, lower, prefix):
    q, n = records[0].modulus, len(records[0].label)
    lower = canonical_vector(lower, n, prefix)
    H = q//prefix
    if H == 1:
        return lower, {"applied": False, "prefix_modulus": prefix, "remaining_modulus": 1,
                       "root_already_complete": True}
    cache = PublicBasisCache(records)
    try: basis = cache.inverse(H)
    except NonFreeRank:
        return None, {"applied": False, "prefix_modulus": prefix, "remaining_modulus": H,
                      "status": "ORIGINAL_LOW_LABEL_RANK_UNSUPPORTED"}
    transcript = []
    for s in records:
        residual = (s.value-sum(a*b for a, b in zip(s.label, lower))) % q
        rounded = ((residual+prefix//2)//prefix) % H
        transcript.append({"source_id": s.source_id, "corrected_original_response": residual,
                           "rounded_higher_equation": rounded})
    rhs = tuple(transcript[j]["rounded_higher_equation"] for j in cache.pivots)
    high = tuple(sum(a*b for a, b in zip(row, rhs)) % H for row in basis["inverse"])
    consistent = all(sum(a*b for a, b in zip(s.label, high)) % H == t["rounded_higher_equation"] for s, t in zip(records, transcript))
    candidate = tuple(a+prefix*b for a, b in zip(lower, high)) if consistent else None
    return candidate, {"applied": True, "prefix_modulus": prefix, "remaining_modulus": H,
        "public_basis_model": basis, "rounding_transcript": tuple(transcript),
        "higher_solution": high if consistent else None, "all_original_higher_equations_consistent": consistent,
        "new_independent_samples_created": False}


def decode(records, method="cubic", max_matrix_entries=2000000):
    records = _records(records);q, n, m = records[0].modulus, len(records[0].label), len(records)
    D = feature_width(n, method);r = root_digits(q)
    if method == "cubic" and r < 2: raise ValueError("divided-cubic source requires modulus at least9")
    integer(max_matrix_entries, "positive whole-matrix preflight cap", 1)
    entries = m*(D+1)
    base = {"original_modulus": q, "dimension": n, "method": method, "original_records_paid_once": m,
        "feature_dimension": D, "logical_augmented_matrix_entries": entries,
        "matrix_cap_includes_Python_and_FLINT_overhead": False,
        "candidate_secret": None, "fixed_instance_alphabet_uniqueness_certified": False,
        "actual_planted_secret_or_noise_law_certified": False,
        "required_canonical_original_error_alphabet": (-1, 0, 1) if method == "cubic" else (-1, 1),
        "original_data_without_secret_mask_errors_or_oracle_input": True,
        "new_quantum_algorithm_or_general_Gaussian_solver": False,
        "classical_secret_hypotheses_enumerated": 0,
        "matrix_and_original_record_work_are_free": False,
        "row_generation_order": "O(m*n^3)" if method == "cubic" else "O(m*n^2)",
        "field_elimination_order": "O(m*D^2)",
        "matrix_storage_order": "O(m*D)",
        "full_root_lift_arithmetic_order": "O(n^2*m+n^3*log(r+1)+m*n) on O(log(q))-bit operands"}
    if entries > max_matrix_entries:
        return {**base, "status": "WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION", "compiled_rows": 0,
                "field_elimination_calls": 0, "coefficient_rank": None}
    rows, rhs = compile_equations(records, method)
    system = {"basis": feature_layout(n, method), "rows": rows, "rhs": rhs}
    base.update({"compiled_rows": m, "compiled_system_sha256": digest(system),
        "original_records_sha256": digest(tuple(s.public() for s in records)),
        "field_elimination_calls": 1})
    try: solved = solve_full_rank_f3(rows, rhs, D)
    except ValueError as error:
        if str(error) != "inconsistent F3 equations": raise
        return {**base, "status": "INCONSISTENT_SMALL_ALPHABET_EQUATIONS", "coefficient_rank": None}
    if solved is None:
        return {**base, "status": "INSUFFICIENT_FEATURE_RANK_NOT_NO_SECRET", "coefficient_rank": int(nmod_mat(rows, 3).rank()),
                "field_elimination_calls": 2}
    base.update({"coefficient_rank": D, "linearized_solution": solved})
    if method == "cubic":
        u, v = solved[:n], solved[-n:]
        lower, prefix = tuple(a+3*b for a, b in zip(u, v)), 9
        expected = features(u, v)
    else:
        u, v = solved[-n:], None
        lower, prefix, expected = u, 3, features(u, method="quadratic")
    if solved != expected:
        return {**base, "status": "INVALID_NONLINEAR_FEATURE_LIFT", "low_secret": None}
    base.update({"low_secret": lower, "prefix_modulus": prefix, "nonlinear_features_verified": True})
    candidate, lift = high_root_lift(records, lower, prefix)
    base["full_root_lift"] = lift
    if candidate is None:
        return {**base, "status": "INCONSISTENT_OR_UNSUPPORTED_ORIGINAL_HIGHER_ROOT_LIFT"}
    residuals = tuple(((s.value-sum(a*b for a, b in zip(s.label, candidate))+q//2) % q)-q//2 for s in records)
    if any(e not in base["required_canonical_original_error_alphabet"] for e in residuals):
        return {**base, "status": "FULL_ROOT_ALPHABET_FIT_FAILED", "original_candidate_residuals": residuals}
    return {**base, "status": "UNIQUE_BOUNDED_ALPHABET_COMPATIBLE_FULL_ROOT_SECRET", "candidate_secret": candidate,
        "original_candidate_residuals": residuals, "fixed_instance_alphabet_uniqueness_certified": True,
        "planted_secret_recovery_requires_the_true_alphabet_promise": True}


def cubic_rank_ledger(n, m, probability_floor, supported_residues):
    D = feature_width(n);integer(m, "positive actual source row count", 1)
    support = tuple(supported_residues);p = _rational(probability_floor)
    if len(set(support)) != len(support) or len(support) not in (2, 3) or any(type(x) is not int or x not in (-1, 0, 1) for x in support):
        raise ValueError("at least two distinct signed noise residues required")
    if not 0 < p <= Fraction(1, len(support)):
        raise ValueError("true positive noise probability floor required")
    escape = 2*p/3 if len(support) == 3 else p/3
    capture = 1-escape
    power_block = 16
    # Do not expand exponentially long probability denominators in scaling histories.
    power = capture**power_block
    power_bits = (power.denominator//power.numerator).bit_length()-1
    exponent = 2*D-(m//power_block)*power_bits
    budget = Fraction(1, 2**min(64, max(0, -exponent)))
    short = m <= 512 and D <= 512
    exact = min(Fraction(1), Fraction(3**D-1, 2)*capture**m) if short else None
    if exact is not None: budget = min(budget, exact)
    return {"dimension": n, "original_rows": m, "feature_dimension": D,
        "supported_original_noise_residues": support, "true_noise_probability_floor": str(p),
        "row_escape_probability_lower": str(escape), "hyperplane_capture_probability_upper": str(capture),
        "projective_hyperplanes": {"base": 3, "exponent": D, "subtract": 1, "denominator": 2},
        "capture_power_block": power_block, "capture_power_at_block": str(power) if max(power.numerator.bit_length(), power.denominator.bit_length()) <= 12000 else None,
        "capture_power_negative_log2_floor": power_bits,
        "dyadic_rank_union_exponent": exponent, "exact_rank_union_upper_if_short": str(exact) if exact is not None else None,
        "rank_failure_upper_used": str(budget),
        "independent_uniform_original_labels_and_label_independent_noise_required": True,
        "actual_source_promise_or_probability_floor_established": False,
        "finite_matrix_rank_is_not_a_source_IID_certificate": True}


def coefficient_grid(n):
    D, count = feature_width(n), 3**(2*n+1)
    if count*D > 1000000: raise ValueError("whole public-coefficient grid cap exceeded")
    rows = []
    for params in product(range(3), repeat=2*n+1):
        a = tuple(params[i]+3*params[n+i] for i in range(n));t = params[-1]
        rows.append(cubic_equation(a, t)[0])
    return {"dimension": n, "full_public_parameter_grid_rows": count, "feature_dimension": D,
        "coefficient_rank_mod3": int(nmod_mat(rows, 3).rank()),
        "coefficient_grid_sha256": digest(rows), "these_rows_are_not_new_oracle_samples": True}


def scalar_escape_control(secret_low, alphabet):
    law = tuple((e, Fraction(1, len(alphabet))) for e in alphabet)
    rows = [(cubic_equation((a,), (a*secret_low+e) % 9)[0], p/9) for a in range(9) for e, p in law]
    probabilities = tuple(sum(p for row, p in rows if sum(a*b for a, b in zip(row, dual)) % 3)
                          for dual in product(range(3), repeat=3) if any(dual))
    ledger = cubic_rank_ledger(1, 32, Fraction(1, len(alphabet)), alphabet)
    return {"secret_low_fixture_only": secret_low, "noise_alphabet": alphabet, "public_label_noise_assignments": len(rows),
        "nonzero_duals_checked": len(probabilities), "minimum_actual_escape_probability": str(min(probabilities)),
        "claimed_escape_lower": ledger["row_escape_probability_lower"], "secret_enters_receiver": False}


def control(n, r, M, noise_kind, method, seed):
    from native_full_root_slice import source_data
    if noise_kind not in ("signed", "mixed"): raise ValueError("explicit forward calibration noise law required")
    records, mask, truth, errors = source_data(n, r, M, noise_kind == "signed", seed)
    secret = tuple((x-y) % (3**r) for x, y in zip(truth, mask))
    if noise_kind == "mixed":
        rng = random.Random(seed+1);errors = tuple(rng.choice((-1, 0, 1)) for _ in records)
        records = tuple(replace(s, value=(sum(a*b for a, b in zip(s.label, secret))+e) % s.modulus) for s, e in zip(records, errors))
    result = decode(records, method)
    support = (-1, 1) if noise_kind == "signed" else (-1, 0, 1)
    return {"original_records": tuple(s.public() for s in records),
        "declared_calibration_noise_alphabet": support,
        "truth_fixture_only": {"original_secret": secret, "original_errors": errors},
        "decoder": result, "matches_truth_fixture": result["candidate_secret"] == secret,
        "secret_or_errors_entered_decoder": False,
        "cubic_source_rank_budget": cubic_rank_ledger(n, len(records), Fraction(1, len(support)), support) if method == "cubic" else None,
        "unbounded_Gaussian_noise_is_represented_by_this_calibration": False}


def falsifiers():
    from native_full_root_slice import source_data
    records, mask, truth, errors = source_data(2, 3, 12, True, 97001)
    secret = tuple((x-y) % 27 for x, y in zip(truth, mask))
    changed = list(records);changed[-1] = replace(changed[-1], value=(changed[-1].value+3) % 27)
    bad_errors = tuple(e+(3 if j == len(records)-1 else 0) for j, e in enumerate(errors))
    aligned = tuple(replace(s, value=(s.value+9*s.label[0]) % 27) for s in records)
    aligned_errors = tuple(e+9*s.label[0] for e, s in zip(errors, records))
    rankless = tuple(replace(s, label=(0, 0), value=1) for s in records)
    nonphysical = tuple(NoisyLinearRecord((a,), t, 9, f"nonphysical-{j}") for j, (a, t) in enumerate(((3, 0), (1, 6), (1, 1), (3, 0))))
    cases = (("preflight_cap", records, secret, errors, 1),
        ("rankless_source", rankless, secret, (1,)*len(records), 2000000),
        ("corrupted_carry_equation", tuple(changed), secret, bad_errors, 2000000),
        ("wrong_planted_secret_with_unique_alphabet_fit", aligned, secret, aligned_errors, 2000000),
        ("full_rank_nonphysical_feature_lift", nonphysical, (0,), (0, 6, 1, 0), 2000000))
    output = []
    for kind, data, planted, error, cap in cases:
        result = decode(data, max_matrix_entries=cap)
        output.append({"kind": kind, "original_records": tuple(s.public() for s in data), "max_matrix_entries": cap,
            "truth_fixture_only": {"original_secret": planted, "original_errors": error},
            "decoder": result, "matches_planted_truth": result["candidate_secret"] == planted,
            "false_source_alphabet_promise_may_not_be_repaired_from_truth": True})
    return tuple(output)


def build_report():
    deps = ("native_affine_fibre_relaxation.py", "native_classical_modulus_descent.py", "native_small_multiple_completion.py",
        "native_full_root_slice.py", "nil3_state_hsp_descent_receiver.py", "ternary_covariant_noise.py",
        "ternary_measured_lattice_decoder.py", "ternary_phase_qubit_decoder.py")
    deps += ("ternary_noise_degradation.py",)
    return {"status": "POLYNOMIAL_FULL_ROOT_SMALL_ALPHABET_CLASSICAL_BASELINE_EXTERNAL_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "original_data_controls": [control(*args) for args in ((2, 3, 12, "signed", "cubic", 97001),
            (2, 6, 44, "signed", "quadratic", 97002), (4, 16, 200, "mixed", "cubic", 97003),
            (8, 64, 688, "mixed", "cubic", 97004))],
        "complete_coefficient_grids": [coefficient_grid(n) for n in (1, 2, 3)],
        "complete_scalar_escape_controls": [scalar_escape_control(u, support) for u in range(3) for support in ((-1, 1), (-1, 0, 1), (0, 1))],
        "falsifier_controls": falsifiers(),
        "scaling_rank_budgets": [cubic_rank_ledger(n, 8*(feature_width(n)+16), "1/3", (-1, 0, 1)) for n in (8, 32, 64, 128)],
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "general_Gaussian_LWE_solver_or_new_quantum_algorithm": False,
        "novelty_claim": False,
        "research_decision": "DO_NOT_COUNT_BOUNDED_SIGNED_ERROR_CALIBRATIONS_AS_HARD_QUANTUM_RECOVERY_EVIDENCE",
        "remaining_obligations": ["external carry/rank/uniqueness review", "full prior-art audit", "properly charged Gaussian quotient adapter",
            "robust corrupted-equation recovery or larger error alphabet", "production integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"],
        "controls": [{"n": c["decoder"]["dimension"], "root_digits": root_digits(c["decoder"]["original_modulus"]),
            "method": c["decoder"]["method"], "status": c["decoder"]["status"], "matches_truth": c["matches_truth_fixture"],
            "features": c["decoder"]["feature_dimension"]} for c in report["original_data_controls"]],
        "new_quantum_or_Gaussian_solver": False}, indent=2))


if __name__ == "__main__": main()

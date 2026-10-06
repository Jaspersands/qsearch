"""Terminal-lattice certificates for density-one subset-sum moments.

LOCAL DERIVATION / REVIEW PENDING. This bounds nonnegative nongeneric
tuple contributions, not witness complexity or quantum runtime. Catalogue
counting is an analysis device, not an efficient search algorithm.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "research/classical_baselines/dcp_subset_sum_terminal_catalogue.json"
STATUS = "LOCAL_DERIVATION_REVIEW_PENDING"


def hadamard_index_bound(rank: int) -> int:
    if rank < 1:
        raise ValueError("rank must be positive")
    return math.isqrt(rank**rank)


def data_generator_bound(rank: int) -> int:
    # The all-ones column is free. Reorder independent columns first, then
    # every additional necessary generator halves the saturation index.
    return rank - 1 + hadamard_index_bound(rank).bit_length() - 1


def saturation_index(matrix: Matrix) -> int:
    diagonal = smith_normal_form(matrix, domain=ZZ)
    return math.prod(
        abs(int(diagonal[i, i]))
        for i in range(min(diagonal.shape))
        if diagonal[i, i]
    )


def generator_certificate(patterns: list[tuple[int, ...]], order: int) -> dict:
    if order < 2 or any(
        len(p) != order or any(x not in (0, 1) for x in p) for p in patterns
    ):
        raise ValueError("order >= 2 and Boolean columns required")
    current = Matrix([1] * order)
    selected = []
    for i, pattern in enumerate(patterns):
        trial = current.row_join(Matrix(pattern))
        if trial.rank() > current.rank():
            current = trial
            selected.append(i)
    rank = current.rank()
    initial_index = saturation_index(current)
    current = hermite_normal_form(current)
    repair_indices = []
    index_drops = []
    for i, pattern in enumerate(patterns):
        trial = hermite_normal_form(current.row_join(Matrix(pattern)))
        if trial != current:
            old_index, new_index = saturation_index(current), saturation_index(trial)
            if old_index % new_index or old_index // new_index < 2:
                raise AssertionError("proper same-span enlargement did not divide index")
            current = trial
            selected.append(i)
            repair_indices.append(i)
            index_drops.append(old_index // new_index)
    target = hermite_normal_form(Matrix.hstack(Matrix([1] * order), *map(Matrix, patterns)))
    if current != target or len(selected) > data_generator_bound(rank):
        raise AssertionError("compressed generator certificate failed")
    if initial_index > hadamard_index_bound(rank):
        raise AssertionError("Boolean minor exceeded Hadamard bound")
    return {
        "rank": rank,
        "selected_data_indices": selected,
        "same_span_repair_indices": repair_indices,
        "same_span_index_drop_factors": index_drops,
        "initial_saturation_index": initial_index,
        "final_saturation_index": saturation_index(current),
        "data_generator_count": len(selected),
        "data_generator_bound": data_generator_bound(rank),
        "exact_original_lattice_preserved": current == target,
    }


def rank_terms(n_bits: int, order: int, offset: int = 0) -> list[dict]:
    if n_bits < 1 or order < 2 or n_bits + offset < 1:
        raise ValueError("positive n, m=n+c and order >= 2 required")
    m = n_bits + offset
    result = []
    for rank in range(2, min(order, m + 1) + 1):
        h = hadamard_index_bound(rank)
        g = data_generator_bound(rank)
        rho = Fraction(1, 2) if rank == order else Fraction(3, 4)
        # (3/4)^5 < 1/4 gives a deliberately coarse INTEGER exponent.
        decay = m if rank == order else 2 * (m // 5)
        exponent = (h - 1).bit_length() + order * g + rank * offset - decay
        result.append({
            "rank": rank,
            "hadamard_index_bound": h,
            "data_generator_bound": g,
            "catalogue_count_formula": f"2^({order}*{g})",
            "boolean_growth_ratio": str(rho),
            "certified_binary_exponent_upper_bound": exponent,
        })
    return result


def certified_binary_bound(n_bits: int, order: int, offset: int = 0) -> int:
    terms = rank_terms(n_bits, order, offset)
    return max(t["certified_binary_exponent_upper_bound"] for t in terms) + (
        len(terms) - 1
    ).bit_length()


def exact_catalogue_bound(n_bits: int, order: int, offset: int = 0) -> Fraction:
    m = n_bits + offset
    result = Fraction()
    for term in rank_terms(n_bits, order, offset):
        rank = term["rank"]
        exponent = order * term["data_generator_bound"] + rank * offset
        scale = Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)
        result += term["hadamard_index_bound"] * scale * Fraction(
            term["boolean_growth_ratio"]
        ) ** m
    return result


def fraction_record(value: Fraction) -> dict:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def falling(value: int, order: int) -> int:
    return math.prod(range(value - order + 1, value + 1)) if value >= order else 0


def gf2_rank(columns: list[int]) -> int:
    basis = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = column
                break
            column ^= basis[pivot]
    return len(basis)


def is_bad_tuple(assignments: tuple[int, ...], m: int) -> bool:
    k = len(assignments)
    columns = [(1 << k) - 1]
    columns.extend(
        sum(((b >> j) & 1) << i for i, b in enumerate(assignments))
        for j in range(m)
    )
    return gf2_rank(columns) < k


def exact_source_controls(n_bits: int, offset: int, orders=range(2, 7)) -> list[dict]:
    m, modulus = n_bits + offset, 1 << n_bits
    if m < 1 or modulus**m > 10000:
        raise ValueError("bounded exact source control exceeded")
    histogram = Counter()
    for labels in itertools.product(range(modulus), repeat=m):
        counts = [0] * modulus
        for assignment in range(1 << m):
            residue = sum(a for j, a in enumerate(labels) if assignment >> j & 1) % modulus
            counts[residue] += 1
        histogram.update(counts)
    denominator = modulus ** (m + 1)
    assert sum(histogram.values()) == denominator
    result = []
    for k in orders:
        observed = Fraction(sum(count * falling(c, k) for c, count in histogram.items()), denominator)
        independent = Fraction(falling(1 << m, k), modulus**k)
        excess = observed - independent
        bound = exact_catalogue_bound(n_bits, k, offset)
        if not 0 <= excess <= bound:
            raise AssertionError("terminal-catalogue bound failed exact source moment")
        result.append({
            "n_bits": n_bits, "register_offset": offset, "moment_order": k,
            "label_tuple_count": modulus**m, "joint_target_count": denominator,
            "exact_factorial_moment": fraction_record(observed),
            "independent_map_baseline": fraction_record(independent),
            "nonnegative_excess": fraction_record(excess),
            "exact_catalogue_bound": fraction_record(bound),
            "control_passed": True,
        })
    return result


def weighted_bad_tuple_controls(n_bits: int = 2, offset: int = 1) -> dict:
    m, modulus = n_bits + offset, 1 << n_bits
    if m > 4:
        raise ValueError("weighted tuple control limited to four assignment bits")
    totals = Counter()
    uniform_event_counts = Counter()
    per_label_event_probabilities = Counter()
    inverse_legal_fraction_sum = Fraction()
    lam = Fraction(1 << m, modulus)
    instances = 0
    for labels in itertools.product(range(modulus), repeat=m):
        fibers = [[] for _ in range(modulus)]
        for b in range(1 << m):
            fibers[sum(a for j, a in enumerate(labels) if b >> j & 1) % modulus].append(b)
        legal_count = sum(bool(fiber) for fiber in fibers)
        inverse_legal_fraction = Fraction(modulus, legal_count)
        second_moment = Fraction(sum(len(fiber)**2 for fiber in fibers), modulus)
        assert inverse_legal_fraction <= second_moment / lam**2
        inverse_legal_fraction_sum += inverse_legal_fraction
        for fiber in fibers:
            bad = {
                k: math.factorial(k) * sum(is_bad_tuple(t, m) for t in itertools.combinations(fiber, k))
                for k in range(2, 6)
            }
            for k in range(2, 5):
                if len(fiber) * bad[k] > k * bad[k] + bad[k + 1]:
                    raise AssertionError("planted-target bad-prefix inequality failed")
                totals[k] += bad[k]
                totals[(k, "weighted")] += len(fiber) * bad[k]
                if bad[k]:
                    uniform_event_counts[k] += 1
                    per_label_event_probabilities[k] += Fraction(1, legal_count)
                instances += 1
    denominator = modulus ** (m + 1)
    rows = []
    expected_inverse_legal_fraction = inverse_legal_fraction_sum / modulus**m
    assert expected_inverse_legal_fraction <= 1 + 1 / lam
    for k in range(2, 5):
        mean = Fraction(totals[k], denominator)
        weighted = Fraction(totals[(k, "weighted")], denominator)
        bound = exact_catalogue_bound(n_bits, k, offset)
        assert mean <= bound
        assert weighted <= k * bound + exact_catalogue_bound(n_bits, k + 1, offset)
        uniform_event = Fraction(uniform_event_counts[k], denominator)
        per_label_event = Fraction(per_label_event_probabilities[k]) / modulus**m
        assert per_label_event**2 <= expected_inverse_legal_fraction * uniform_event
        rows.append({"moment_order": k, "mean_bad_contribution": fraction_record(mean),
                     "mean_occupancy_weighted_bad_contribution": fraction_record(weighted),
                     "uniform_target_bad_event_probability": fraction_record(uniform_event),
                     "per_label_uniform_legal_bad_event_probability": fraction_record(per_label_event)})
    return {"per_instance_inequality_checks": instances, "rows": rows,
            "expected_inverse_legal_fraction": fraction_record(expected_inverse_legal_fraction),
            "per_label_legal_event_squared_bound_checked": True,
            "legal_target_law_is_joint_conditioning": True,
            "planted_target_change_of_measure_checked": True}


def terminal_lattice_controls(orders=range(2, 6)) -> list[dict]:
    from dcp_subset_sum_smith_transfer import (
        _matrix_from_key, _pattern_column, build_smith_transfer_system,
    )

    rows = []
    for k in orders:
        system = build_smith_transfer_system(k)
        checked = repairs = bad = 0
        for state, outgoing in system.transitions.items():
            matrix = _matrix_from_key(state)
            patterns = [
                tuple(int(x) for x in _pattern_column(k, mask))
                for mask in range(1 << k)
                if hermite_normal_form(matrix.row_join(_pattern_column(k, mask))) == matrix
            ]
            certificate = generator_certificate(patterns, k)
            checked += 1
            repairs += len(certificate["same_span_repair_indices"])
            profile = system.terminal_profiles.get(state)
            if profile is not None and not profile[3]:
                rank, _, base, _ = profile
                rho = Fraction(1, 2) if rank == k else Fraction(3, 4)
                assert Fraction(base, 1 << rank) <= rho
                bad += 1
        rows.append({"moment_order": k, "reachable_lattices_checked": checked,
                     "same_span_repairs_charged": repairs, "bad_distinct_row_lattices_checked": bad})
    return rows


def run_report() -> dict:
    adversarial = generator_certificate(
        [(1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (1, 0, 0, 0)], 4
    )
    assert adversarial["initial_saturation_index"] == 2
    assert adversarial["final_saturation_index"] == 1
    assert adversarial["same_span_index_drop_factors"] == [2]
    source_rows = [
        row for n, c in ((1, 0), (1, 1), (2, -1), (2, 0), (2, 1), (3, -1), (3, 0), (3, 1))
        for row in exact_source_controls(n, c)
    ]
    scaling = []
    for n in (1 << 12, 1 << 16, 1 << 20, 1 << 24):
        from sympy import integer_nthroot
        schedules = {"logarithmic": n.bit_length() - 1,
                     "cube_root": int(integer_nthroot(n, 3)[0]),
                     "two_fifths_power": int(integer_nthroot(n * n, 5)[0])}
        for schedule, k in schedules.items():
            exponent = certified_binary_bound(n, k, 2)
            scaling.append({"n_bits": n, "register_offset": 2, "moment_order": k,
                            "schedule": schedule, "certified_binary_exponent_upper_bound": exponent,
                            "bound_below_one": exponent < 0, "finite_row_is_asymptotic_proof": False})
    dependencies = ["theorems/dcp_subset_sum_cube_section_gap_theorem.py",
                    "theorems/dcp_subset_sum_smith_transfer.py"]
    return {
        "status": STATUS,
        "exact_fraction_encoding": "numerators and denominators are decimal strings; do not parse through floats",
        "source_contract": "a_i and S independent uniform in Z_(2^n); m=n+c; ordered distinct Boolean tuples",
        "definitions": {"D_k": "number of ordered distinct solutions with GF(2)-rank([tuple columns,1])<k",
                        "B_k": "sum_{r=2}^{min(k,m+1)} H_r 2^(k*g_r+r*c) rho_r^m",
                        "H_r": "floor(sqrt(r^r))", "g_r": "r-1+floor(log2 H_r)",
                        "rho_r": "1/2 for r=k, otherwise 3/4"},
        "derived_bounds": {"nonnegative_factorial_excess": "0<=E[(C)_k]-(2^m)_k/2^(n*k)<=E[D_k]<=B_k",
                           "vanishing_condition": "k^2 log k + k|c| = o(n)",
                           "fixed_offset_consequence": "k=o(sqrt(n/log n))",
                           "uniform_target_tail": "Pr[D_k>=tau]<=B_k/tau",
                           "joint_uniform_legal_target_tail": "Pr[D_k>=tau|C>0]<=(1+2^-c)*B_k/tau",
                           "per_label_uniform_legal_target_tail": "Pr_per_label_legal[D_k>=tau]^2<=(1+2^-c)*B_k/tau",
                           "planted_target_tail": "Pr_planted[D_k>=tau]<=(k*B_k+B_(k+1))/(2^c*tau)"},
        "adversarial_index_repair_control": adversarial,
        "terminal_lattice_controls": terminal_lattice_controls(),
        "exact_source_moment_controls": source_rows,
        "weighted_bad_tuple_controls": weighted_bad_tuple_controls(),
        "scaling_rows": scaling,
        "dependency_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
        "claim_gate": {"independent_theorem_review": False, "formal_proof": False,
                       "novelty_claim": False, "quantum_algorithm": False,
                       "witness_complexity_lower_bound": False, "all_signed_observables_excluded": False,
                       "all_conditioned_target_events_excluded": False,
                       "selected_label_distribution_preserved_by_joint_legal_conditioning": False,
                       "catalogue_enumeration_is_polynomial": False,
                       "max_occupancy_law_proved": False},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_report()
    if args.save:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"],
                      "reachable_lattices_checked": sum(r["reachable_lattices_checked"] for r in report["terminal_lattice_controls"]),
                      "exact_source_moment_controls": len(report["exact_source_moment_controls"]),
                      "weighted_inequality_checks": report["weighted_bad_tuple_controls"]["per_instance_inequality_checks"],
                      "scaling_rows": report["scaling_rows"]}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

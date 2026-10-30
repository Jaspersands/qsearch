"""Finite exact controls for the matched classical partition-source attack.

Reference enumeration is restricted to at most 27 ternary inputs. It is
not called by the recovery algorithm, which sees only f evaluations and
public promise bounds. No quantum or original-hidden-subgroup claim.
"""
from fractions import Fraction
from itertools import product


def reference_partition(width, evaluator):
    """Exact small-state Pauli losses, including mixed XZ labels."""
    if type(width) is not int or not 1 <= width <= 3:
        raise ValueError("finite ternary reference requires width 1..3")
    points = tuple(product(range(3), repeat=width))
    size = len(points)
    labels = [evaluator(x) for x in points]
    kernel = [[int(a == b) for b in labels] for a in labels]
    seen, fiber_sizes = set(), []
    for i in range(size):
        if i not in seen:
            members = {j for j in range(size) if kernel[i][j]}
            seen.update(members)
            fiber_sizes.append(len(members))
    mass = sum(map(sum, kernel))
    zero = (0,)*width
    span = {zero}
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            difference = tuple((a-b) % 3 for a, b in zip(x, y))
            if kernel[i][j] and difference not in span:
                span = {tuple((v[k]+c*difference[k]) % 3 for k in range(width))
                        for v in span for c in range(3)}
    phases = tuple(z for z in points if all(sum(a*b for a, b in zip(z, d)) % 3 == 0
                                           for d in span))
    indices = {x: i for i, x in enumerate(points)}
    translations, symmetries, losses = [], [], []
    for shift in points:
        shifted = [indices[tuple((a+b) % 3 for a, b in zip(x, shift))] for x in points]
        changed = sum(kernel[i][j] != kernel[shifted[i]][shifted[j]]
                      for i in range(size) for j in range(size))
        if changed == 0:
            translations.append(shift)
        for z in points:
            twice_overlap = 0
            for i, x in enumerate(points):
                for j, y in enumerate(points):
                    if kernel[i][j] and kernel[shifted[i]][shifted[j]]:
                        phase = sum(a*(b-c) for a, b, c in zip(z, x, y)) % 3
                        twice_overlap += 2 if phase == 0 else -1
            loss = Fraction(2*mass-twice_overlap, 2*size**2)
            losses.append((shift+z, loss))
            if loss == 0:
                symmetries.append(shift+z)
            if z == zero and loss != Fraction(changed, 2*size**2):
                raise ArithmeticError("translation mismatch identity failed")
    predicted = {t+z for t in translations for z in phases}
    if set(symmetries) != predicted:
        raise ArithmeticError("partition-source Pauli factorization failed")
    return {
        "finite_known_function_reference_only": True,
        "prime": 3, "width": width, "domain_size": size,
        "fiber_sizes": sorted(fiber_sizes),
        "purity": Fraction(mass, size**2),
        "collision_difference_span": tuple(sorted(span)),
        "translation_symmetries": tuple(translations),
        "phase_symmetries": phases,
        "pauli_symmetries": tuple(symmetries),
        "stabilizer_diagonal": span <= set(translations),
        "quotient_size": size//len(span),
        "minimum_positive_loss": min((d for _, d in losses if d > 0), default=None),
        "pauli_losses": tuple(losses),
    }


def nonuniform_layer(x):
    a, b = x
    return b, 0 if b == 0 else a


def repeated_nonuniform_layer(x):
    a, b, c = x
    return c, b, 0 if b == 0 else a


def singleton_partition(x):
    return int(not any(x))


def report():
    import hashlib
    from pathlib import Path
    import random

    from theorems.partition_source_attack import PartitionSourcePlan, recover_partition_symmetry

    root = Path(__file__).resolve().parents[1]
    cases = []
    for name, width, evaluator, R, gap in (
        ("nonuniform_layers", 2, nonuniform_layer, 6, Fraction(2, 27)),
        ("noncommuting_full_group", 3, repeated_nonuniform_layer, 17, Fraction(2, 81)),
    ):
        reference = reference_partition(width, evaluator)
        plan = PartitionSourcePlan(3, width, R, gap)
        recovery = recover_partition_symmetry(plan, evaluator, rng=random.Random(20261030))
        rows = recovery["pauli_generators"]
        generated = {tuple(sum(c*r[j] for c, r in zip(coefficients, rows)) % 3
                           for j in range(2*width))
                     for coefficients in product(range(3), repeat=len(rows))}
        matches = recovery["status"] == "SUCCESS" and generated == set(reference["pauli_symmetries"])
        if not matches:
            raise ArithmeticError("seeded classical recovery control failed")
        del reference["pauli_losses"]
        cases.append({"name": name, "reference": reference, "plan": plan.caps(),
                      "classical_run": recovery, "generators_match_exact_reference": matches})
    rejected = reference_partition(2, singleton_partition)
    del rejected["pauli_losses"]
    sources = (
        "theorems/partition_source_attack.py", "tests/test_partition_source_attack.py",
        "theorems/partition_source_filter.py", "tests/test_partition_source_filter.py",
        "research/PARTITION_SOURCE_CLASSICAL_FILTER.md", "qsearch_cli/commands/sde.py",
    )
    return {
        "status": "MATCHED_CLASSICAL_PARTITION_SOURCE_FILTER",
        "scope": "exact uniform query-and-discard equality kernel; stabilizer diagonal; supplied purity and gap",
        "controls": cases,
        "promise_violating_control": rejected,
        "classical_evaluator_queries_executed": True,
        "quantum_copies_consumed": 0,
        "general_quantum_input_dequantized": False,
        "arbitrary_quantum_preprocessing_covered": False,
        "original_subgroup_recovered_after_hashing": False,
        "new_speedup_claim_allowed": False,
        "source_sha256": {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources},
    }

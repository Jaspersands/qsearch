"""Exact finite controls for the sampler audit, not a curve implementation."""

from fractions import Fraction
from functools import cache
from itertools import product
import json
from pathlib import Path


def parity_law(rank):
    law = {x: Fraction(1, 2 ** (rank + 1)) for x in range(2**rank)}
    law[0] += Fraction(1, 2)
    return law


def extend_binary(space, x):
    return frozenset(space | {y ^ x for y in space})


def binary_failure(rank, rows):
    states = {frozenset({0}): Fraction(1)}
    for _ in range(rows):
        next_states = {}
        for space, mass in states.items():
            for x, probability in parity_law(rank).items():
                target = extend_binary(space, x)
                next_states[target] = next_states.get(target, Fraction(0)) + mass * probability
        states = next_states
    return sum(mass for space, mass in states.items() if len(space) < 2**rank)


def generation_control(moduli):
    rank = len(moduli)
    zero = (0,) * rank
    elements = set(product(*(range(m) for m in moduli)))
    law = {x: Fraction(1, 2 ** (rank + 1)) for x in product((0, 1), repeat=rank)}
    law[zero] += Fraction(1, 2)

    def add(x, y):
        return tuple((a + b) % m for a, b, m in zip(x, y, moduli))

    @cache
    def extend(subgroup, x):
        result = set(subgroup)
        multiple = x
        while multiple not in subgroup:
            result.update(add(y, multiple) for y in subgroup)
            multiple = add(multiple, x)
        return frozenset(result)

    escape_probabilities = []

    @cache
    def expectation(subgroup):
        if len(subgroup) == len(elements):
            return Fraction(0)
        stay = sum(probability for x, probability in law.items() if x in subgroup)
        escape_probabilities.append(1 - stay)
        tail = sum(
            probability * expectation(extend(subgroup, x))
            for x, probability in law.items()
            if x not in subgroup
        )
        return (1 + tail) / (1 - stay)

    biases = []
    for character in product((0, 1), repeat=rank):
        if any(character):
            biases.append(abs(sum(
                probability * (-1) ** (sum(a * b for a, b in zip(character, x)) % 2)
                for x, probability in law.items()
            )))
    expected = expectation(frozenset({zero}))
    s = len(elements).bit_length() - 1
    assert max(biases) == Fraction(1, 2)
    assert min(escape_probabilities) >= Fraction(1, 4)
    assert expected <= 4 * s
    total_variation = sum(abs(law.get(x, 0) - Fraction(1, len(elements))) for x in elements) / 2
    return {
        "moduli": moduli,
        "order": len(elements),
        "support": len(law),
        "total_variation_from_uniform": str(total_variation),
        "max_mod2_bias": str(max(biases)),
        "minimum_reachable_proper_subgroup_escape": str(min(escape_probabilities)),
        "expected_outer_proposals_exact": str(expected),
        "bound_4s": 4 * s,
        "reachable_subgroups": expectation.cache_info().currsize,
    }


def verification_control():
    # T=(e1,e2,e1+e2); relation space is {000,111}.
    torsion = (1, 2, 3)
    true_kernel = {0, 7}
    certified = rejected = 0
    for rows in product(range(4), repeat=2):
        kernel = []
        for coefficient in range(8):
            image = 0
            for j, t in enumerate(torsion):
                if coefficient >> j & 1:
                    image ^= t
            if all((image & row).bit_count() % 2 == 0 for row in rows):
                kernel.append((coefficient, image))
        # Choose a binary basis, then check only that basis in the group.
        span = frozenset({0})
        basis_images = []
        for coefficient, image in kernel:
            if coefficient not in span:
                span = extend_binary(span, coefficient)
                basis_images.append(image)
        if all(image == 0 for image in basis_images):
            assert {coefficient for coefficient, _ in kernel} == true_kernel
            certified += 1
        else:
            rejected += 1
    return {"row_sequences": 16, "exact_certificates": certified, "rejections": rejected}


def main():
    failures = []
    for rank in (1, 2, 3):
        rows = 4 * (rank + 1)
        actual = binary_failure(rank, rows)
        bound = (2**rank - 1) * Fraction(3, 4) ** rows
        assert actual <= bound < Fraction(1, 4)
        if rank == 1:
            assert actual == Fraction(3, 4) ** rows
        if rank == 2:
            assert actual == 3 * Fraction(3, 4) ** rows - 2 * Fraction(5, 8) ** rows
        failures.append({"rank": rank, "rows": rows, "exact_failure": str(actual), "union_bound": str(bound)})

    prime_degrees = []
    q = 100003
    for genus in (1, 6, 41, 81, 161, 321, 641, 10**4, 10**8, 10**16):
        n = 1
        while q**n < 16 * (genus + 1) ** 2 * (n + 6) ** 2:
            n += 1
        assert n <= genus + 1
        assert n <= 2 * (2 * genus + 2) - 2 * genus
        prime_degrees.append({"g": genus, "n": n})

    results = {
        "scope": "Exact finite-group/probability controls only; no curve sampler or pairing implementation.",
        "relation_batches": failures,
        "kernel_basis_verification": verification_control(),
        "generation": [generation_control(moduli) for moduli in ((16,), (8, 4), (8, 4, 2), (2, 2, 2))],
        "correlated_reuse_countercontrols": {
            "rank1_failure_reusing_one_half_atom_sample_any_positive_rows": "3/4",
            "rank2_failure_reusing_one_sample_any_positive_rows": "1",
            "independent_rank1_eight_row_failure": str(Fraction(3, 4) ** 8),
        },
        "prime_degree_inequality_checks": prime_degrees,
    }
    assert binary_failure(2, 1) == 1
    output = Path(__file__).resolve().parent / "sampler_control_results.json"
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

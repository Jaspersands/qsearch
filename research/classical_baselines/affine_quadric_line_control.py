"""Two prescribed exact affine-character line controls; run with Sage Python.

No birthday implementation or quantum simulation. Hidden values remain in
source harnesses; decoders receive signs and public coordinates only.
"""

import json

from sage.all import GF, matrix, vector


def padded(value):
    return 1 if value == 0 or value.is_square() else -1


def decode_line(field, values):
    """Recover a monic squarefree line and leading sign for p >= 11."""
    integer_sum = sum(values)
    if integer_sum not in (-1, 1, 3):
        return None
    moments = [
        sum(t**j * field(sign) for t, sign in zip(field, values))
        for j in range(5)
    ]
    h = moments[1] / field(integer_sum)
    second = moments[2] - h**2 * field(integer_sum)
    fourth = (
        moments[4] - 4 * h * moments[3] + 6 * h**2 * moments[2]
        - 3 * h**4 * field(integer_sum)
    )
    if second == 0:
        return None
    if integer_sum == -1:
        epsilon = 1
    elif integer_sum == 3:
        epsilon = -1
    else:
        negative = 2 * fourth == 3 * second**2
        positive = 18 * fourth == 13 * second**2
        if negative == positive:
            return None
        epsilon = -1 if negative else 1
    roots = integer_sum + epsilon
    d = second / (field(roots) - field(epsilon) / 2)
    return -2 * h, h**2 - d, epsilon


def decode_affine(field, dimension, oracle, translation, direction):
    basis = [
        vector(field, [int(i == j) for i in range(dimension)])
        for j in range(dimension)
    ]
    offsets = [vector(field, dimension)] + basis + [-e for e in basis]
    offsets += [
        basis[i] + basis[j]
        for i in range(dimension) for j in range(i + 1, dimension)
    ]
    constants = {}
    leading_signs = set()
    for offset in offsets:
        values = [oracle(translation + offset + t * direction) for t in field]
        decoded = decode_line(field, values)
        if decoded is None:
            return None
        constants[tuple(offset)] = decoded[1]
        leading_signs.add(decoded[2])
    constant_at_translation = constants[tuple(vector(field, dimension))]
    quadratic = matrix(field, dimension, dimension)
    linear_at_translation = vector(field, dimension)
    for i in range(dimension):
        plus = constants[tuple(basis[i])]
        minus = constants[tuple(-basis[i])]
        quadratic[i, i] = (plus + minus - 2 * constant_at_translation) / 2
        linear_at_translation[i] = (plus - minus) / 4
        for j in range(i + 1, dimension):
            quadratic[i, j] = quadratic[j, i] = (
                constants[tuple(basis[i] + basis[j])]
                - plus - constants[tuple(basis[j])] + constant_at_translation
            ) / 2
    linear = linear_at_translation - quadratic * translation
    constant = (
        constant_at_translation
        - (translation * quadratic).dot_product(translation)
        - 2 * linear.dot_product(translation)
    )
    return quadratic, linear, constant, sorted(leading_signs)


def main():
    field = GF(11)
    representatives = {
        1: field(1),
        -1: next(value for value in field if value and not value.is_square()),
    }
    cases = queries = ambiguous = 0
    failures = []
    for h in field:
        for d in field:
            if not d:
                continue
            for epsilon, leading in representatives.items():
                values = [padded(leading * ((t - h)**2 - d)) for t in field]
                decoded = decode_line(field, values)
                cases += 1
                queries += 11
                ambiguous += int(sum(values) == 1)
                if decoded != (-2 * h, h**2 - d, epsilon):
                    failures.append([int(h), int(d), epsilon])
    first = {
        "control": "all F11 squarefree quadratic and leading-sign pairs",
        "cases": cases, "native_sign_queries": queries,
        "integer_sum_one_cases": ambiguous, "failures": failures,
    }

    field = GF(101)
    quadratic = matrix(field, [[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    linear = vector(field, [4, 5, 6])
    constant = (linear * quadratic.inverse()).dot_product(linear)
    translation = vector(field, [2, 3, 5])
    direction = vector(field, [1, 4, 2])
    source_queries = 0

    def oracle(point):
        nonlocal source_queries
        source_queries += 1
        return padded(
            (point * quadratic).dot_product(point)
            + 2 * linear.dot_product(point) + constant
        )

    decoded = decode_affine(field, 3, oracle, translation, direction)
    leading = (direction * quadratic).dot_product(direction)
    matches = decoded is not None and decoded[:3] == (
        quadratic / leading, linear / leading, constant / leading
    )
    second = {
        "control": "one F101 affine n3 instance with zero critical value",
        "grid_size": 10, "native_sign_queries": source_queries,
        "correct_scaled_A_b_c": bool(matches),
        "leading_signs": decoded[3] if decoded is not None else None,
        "critical_value_zero": bool(
            constant == (linear * quadratic.inverse()).dot_product(linear)
        ),
        "below_probability_threshold": bool(101 < 16 * 3**2),
        "source_truth_harness_only": {
            "A_diagonal": [1, 2, 3], "b": [4, 5, 6], "c": int(constant)
        },
        "public_translation": [2, 3, 5], "public_direction": [1, 4, 2],
    }
    print(json.dumps({"controls": [first, second]}, indent=2))
    if failures or not matches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

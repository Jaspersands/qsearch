"""Exact structural controls, not HSP instances or an algorithm search.

Matrices are I+N over Z. The witnessed entries are 0 or 1, so the
inequalities persist modulo every prime. No hiding oracle is constructed.
"""

def add(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, 0) + value
        if out[key] == 0:
            del out[key]
    return out


def negative(a):
    return {key: -value for key, value in a.items()}


def matrix_product(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, ell), y in b.items():
            if j == k:
                key = (i, ell)
                out[key] = out.get(key, 0) + x * y
    return {key: value for key, value in out.items() if value != 0}


def group_product(a, b):
    return add(add(a, b), matrix_product(a, b))


def group_inverse(a):
    if any(i >= j for i, j in a):
        raise ValueError("Expected a strictly upper triangular nilpotent part")
    power, out, sign = dict(a), {}, -1
    while power:
        out = add(out, {key: sign * value for key, value in power.items()})
        power = matrix_product(power, a)
        sign = -sign
    return out


def group_commutator(a, b):
    return group_product(
        group_product(group_product(group_inverse(a), group_inverse(b)), a), b
    )


def lie_bracket(a, b):
    return add(matrix_product(a, b), negative(matrix_product(b, a)))


def unit(i, j):
    if not 0 <= i < j:
        raise ValueError("Expected an upper triangular matrix unit")
    return {(i, j): 1}


def block_support(block_size):
    if type(block_size) is not int or not 1 <= block_size <= 8:
        raise ValueError("Finite structural control requires 1 <= block_size <= 8")
    return {
        (i, j)
        for i in range(5 * block_size)
        for j in range(i + 1, 5 * block_size)
        if i // block_size < j // block_size
    }


def bracket_support(a, b):
    out = set()
    for i, j in a:
        for k, ell in b:
            if j == k:
                out.add((i, ell))
            if ell == i:
                out.add((k, j))
    return out


def series_dimensions(block_size):
    full = block_support(block_size)
    lower, derived = [len(full)], [len(full)]
    current = full
    while current:
        current = bracket_support(full, current)
        lower.append(len(current))
    current = full
    while current:
        current = bracket_support(current, current)
        derived.append(len(current))
    return {"lower_central": lower, "derived": derived}


def symbolic_witnesses():
    x, y, z, w = (unit(i, i + 1) for i in range(4))
    first = group_commutator(x, y)
    second = group_commutator(z, w)
    class_four = group_commutator(group_commutator(first, z), w)
    nonmetabelian = group_commutator(first, second)
    ab, ba = group_product(x, y), group_product(y, x)

    # The subalgebra is a conjugate of <E_13,E_35,E_15>.
    h_x, h_y, h_z = unit(0, 2), add(unit(2, 4), unit(1, 4)), unit(0, 4)
    outside = group_commutator(y, h_y)
    return {
        "class_four_commutator": class_four,
        "derived_noncommuting_commutator": nonmetabelian,
        "AB_product": ab,
        "BA_product": ba,
        "subalgebra_basis": [h_x, h_y, h_z],
        "subalgebra_nonzero_bracket": lie_bracket(h_x, h_y),
        "normality_obstruction": outside,
        "degree_two_projection": unit(2, 4),
    }


def in_h_span(matrix):
    """Membership in <E_13,E_35+E_25,E_15>, over Z or a field."""
    allowed = {(0, 2), (2, 4), (1, 4), (0, 4)}
    return set(matrix) <= allowed and matrix.get((2, 4), 0) == matrix.get((1, 4), 0)


def sparse_record(matrix):
    return [[i, j, value] for (i, j), value in sorted(matrix.items())]


def evidence():
    witness = symbolic_witnesses()
    return {
        "status": "STRUCTURAL_SCOPE_CONTROL_ONLY",
        "matrix_convention": "I+N; zero-based indices; integer identities",
        "parameter_family": "Five diagonal blocks of size m; prime p > 4",
        "general_lower_central_dimensions": ["10m^2", "6m^2", "3m^2", "m^2", "0"],
        "general_derived_dimensions": ["10m^2", "6m^2", "m^2", "0"],
        "checked_block_sizes": {
            str(m): series_dimensions(m) for m in (1, 2, 3, 5)
        },
        "integer_matrix_witnesses": {
            key: [sparse_record(x) for x in value]
            if key == "subalgebra_basis" else sparse_record(value)
            for key, value in witness.items()
        },
        "direct_scope_exclusions": [
            "Nilpotency-class-at-most-two theorem",
            "Abelian-by-cyclic ambient group theorems",
            "Quasi-Hamiltonian ambient group theorem",
            "Normal-subgroup-only recovery for the displayed nonnormal H",
        ],
        "regime_exclusion": "Bounded-prime result does not directly cover unbounded p",
        "does_not_exclude": [
            "A reduction to known algorithms",
            "Other literature not located in this audit",
            "An efficient classical algorithm for a supplied concrete source",
        ],
        "novelty_certified": False,
        "natural_hard_source_found": False,
        "quantum_algorithm_executed": False,
        "speedup_admitted": False,
    }

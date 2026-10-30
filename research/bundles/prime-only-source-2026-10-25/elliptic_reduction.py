"""Postprocess a SUPPLIED doubled elliptic kernel; no kernel recovery occurs."""

from sympy import isprime, zeros

from prime_source import ROOT
from kernel_output import (
    _preimage_lattice, adapted_basis, check_split, coordinate_map,
    integer_matrix, inverse_mod, mod,
)


def _line(vector, ell):
    vector = integer_matrix(vector)
    if type(ell) is not int or ell < 3 or not isprime(ell):
        raise ValueError("odd prime ell required")
    if vector.shape != (2, 1):
        raise ValueError("two by one line generator required")
    vector = mod(vector, ell)
    pivot = next((int(x) for x in vector if x), None)
    if pivot is None:
        raise ValueError("nonzero line required")
    return mod(pow(pivot, -1, ell)*vector, ell)


def line_from_doubled_kernel(kernel, ell):
    """Extract L only if the input plane is exactly L direct-sum L."""
    kernel = integer_matrix(kernel)
    if kernel.shape != (4, 2):
        raise ValueError("four by two doubled kernel required")
    adapted_basis(kernel, ell)
    top = mod(kernel[:2, :], ell)
    nonzero = next((top[:, j] for j in range(2) if top[:, j] != zeros(2, 1)), None)
    if nonzero is None:
        raise ValueError("kernel is not a doubled line")
    line = _line(nonzero, ell)
    for start in (0, 2):
        for j in range(2):
            column = mod(kernel[start:start+2, j], ell)
            if column != zeros(2, 1) and _line(column, ell) != line:
                raise ValueError("kernel is not a doubled line")
    return line


def annihilator_ideal(order, split, line, ell):
    """Column-HNF basis of the LEFT ideal {a in O: a L = 0 mod ell}."""
    line = _line(line, ell)
    check_split(order, split, ell)
    inverse = inverse_mod(adapted_basis(line, ell), ell)
    # In the basis (L, complement), the first column must vanish. This
    # is an annihilator condition, not image(a) contained in L.
    allowed = []
    for row in range(2):
        matrix = zeros(2)
        matrix[row, 1] = 1
        allowed.append(mod(matrix*inverse, ell))
    return _preimage_lattice(coordinate_map(split), allowed, ell)

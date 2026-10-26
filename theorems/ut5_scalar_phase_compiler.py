"""Public sparse coefficient maps after UT5 matrix-source jet alignment.

No hidden potential is evaluated. Unknown base coefficients and their pairwise
products remain symbolic. The standalone symbolic_scalar_phase_erasure adapter
consumes these maps; neither module implements a coherent quantum instrument.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import comb

from theorems.affine_phase_erasure import monomials
from theorems.ut5_matrix_phase_alignment import public_jet_maps, verify_alignment


def _add(target, source, scalar, p):
    scalar %= p
    if not scalar:
        return
    for key, value in source.items():
        coefficient = (target.get(key, 0)+scalar*value) % p
        if coefficient:
            target[key] = coefficient
        else:
            target.pop(key, None)


def _multiply(left, right, p):
    result = {}
    for (alpha, parameters), a in left.items():
        for (beta, others), b in right.items():
            exponent = tuple(x+y for x, y in zip(alpha, beta))
            lifted = tuple(sorted(parameters+others))
            if len(lifted) > 2:
                raise ArithmeticError("phase exceeded the quadratic parameter lift")
            key = (exponent, lifted)
            value = (result.get(key, 0)+a*b) % p
            if value:
                result[key] = value
            else:
                result.pop(key, None)
    return result


def _shifted_component(p, width, basis, coordinate, s, y):
    result = {}
    for index, (c, alpha) in enumerate(basis):
        if c != coordinate:
            continue
        for beta in product(*(range(a+1) for a in alpha)):
            coefficient = pow(s, sum(beta), p)
            for a, b, origin in zip(alpha, beta, y):
                coefficient = coefficient*comb(a, b)*pow(origin, a-b, p) % p
            if coefficient:
                result[(beta+(0,)*(width-len(beta)), (index,))] = coefficient
    return result


@dataclass
class SymbolicScalarPacket:
    p: int
    quotient_width: int
    jet_width: int
    parameter_basis: tuple[tuple[int, tuple[int, ...]], ...]
    terms: dict[tuple[tuple[int, ...], tuple[int, ...]], int]

    @property
    def width(self):
        return self.quotient_width+self.jet_width

    @property
    def degree(self):
        return max((sum(alpha) for alpha, _ in self.terms), default=0)

    @property
    def lifted_parameter_count(self):
        h = len(self.parameter_basis)
        return 1+h+h*(h+1)//2

    def evaluate_fixture(self, point, base_parameters):
        """Truth-based evaluation for reference tests ONLY, not a controller."""
        if len(point) != self.width or len(base_parameters) != len(self.parameter_basis):
            raise ValueError("matching diagnostic point and parameter dimensions required")
        result = 0
        for (alpha, parameters), coefficient in self.terms.items():
            value = coefficient
            for x, power in zip(point, alpha):
                value = value*pow(int(x), power, self.p) % self.p
            for index in parameters:
                value = value*base_parameters[index] % self.p
            result = (result+value) % self.p
        return result


def compile_scalar_packet(alignment, labels, scales, outcomes, central_characters,
                          spectator_outcome):
    """Return the public map Theta -> P(q,t), including harmless constants.

    Base parameter order is W=(b_1..b_r,a_1..a_r), degree<=2, followed by
    (c_1..c_r), degree<=4, and (d14,d24,d25) per factor, degrees (3,2,3).
    c is the Heisenberg LOG center, not the raw matrix n15. Quartic label
    cancellation also kills the scalar degree-four terms, leaving degree<=3.
    The descriptor ordering is fixed across independently prepared batches.
    """
    maps = alignment.maps
    p, r, m, R, D = maps.p, maps.factors, maps.quotient_width, maps.carrier_width, maps.jet_width
    if public_jet_maps(p, labels, scales, outcomes) != maps or not verify_alignment(alignment):
        raise ValueError("verified alignment compatible with these public inputs required")
    if len(central_characters) != len(labels) or any(
        len(mu) != 3*r or any(type(x) is not int or not 0 <= x < p for x in mu)
        for mu in central_characters
    ):
        raise ValueError("canonical extra central labels required for every source")
    if len(spectator_outcome) != R-D or any(type(x) is not int or not 0 <= x < p
                                          for x in spectator_outcome):
        raise ValueError("canonical spectator measurement outcome required")
    width = m+D
    degrees = [2]*(2*r)+[4]*r+[3, 2, 3]*r
    basis = tuple((coordinate, alpha) for coordinate, degree in enumerate(degrees)
                  for alpha in monomials(m, degree))
    x, z, psi = [], [], {}
    for source in maps.active_indices:
        s, y = scales[source], outcomes[source]
        for j in range(r):
            x.append(_shifted_component(p, width, basis, j, s, y))
            value = {}
            _add(value, _shifted_component(p, width, basis, r+j, s, y), labels[source][j], p)
            z.append(value)
        for j, character in enumerate(list(labels[source])+list(central_characters[source])):
            _add(psi, _shifted_component(p, width, basis, 2*r+j, s, y), character, p)
    displacement = x+z
    return _compile_weyl_phase(alignment, basis, displacement, psi, spectator_outcome)


def _compile_weyl_phase(alignment, basis, displacement, psi, spectator_outcome):
    """Shared symbolic Weyl kernel conversion; callers validate the source."""
    maps = alignment.maps
    p, m, R, D = maps.p, maps.quotient_width, maps.carrier_width, maps.jet_width
    width = m+D
    transformed = []
    for row in alignment.symplectic:
        value = {}
        for coefficient, component in zip(row, displacement):
            _add(value, component, coefficient, p)
        transformed.append(value)
    if any(sum(alpha) > 1 for component in transformed[:R] for alpha, _ in component):
        raise ArithmeticError("quadratic X displacements survived public alignment")
    phase = {}
    _add(phase, psi, -1, p)
    for j, (A, B) in enumerate(zip(transformed[:R], transformed[R:])):
        _add(phase, _multiply(A, B, p), -pow(2, -1, p), p)
        if j < D:
            exponent = [0]*width
            exponent[m+j] = 1
            _add(phase, _multiply(B, {(tuple(exponent), ()): 1}, p), -1, p)
        else:
            _add(phase, B, -spectator_outcome[j-D], p)
    result = SymbolicScalarPacket(p, m, D, basis, phase)
    if result.degree > 3:
        raise ArithmeticError("quartic scalar phase survived central-label cancellation")
    return result

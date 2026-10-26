"""Known logical-relation fibers and a Choi-gap falsifier.

No encoder, logical symmetry, hidden subgroup or quantum algorithm is learned
here. The fiber routine consumes an ALREADY LEARNED Lie subgroup. The marked
encoder is a lower-bound control, never an algorithm-search candidate.
"""
from dataclasses import dataclass
from fractions import Fraction

from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import (
    _fmpz_nullspace_basis, _fmpz_row_space_basis, _fmpz_solve_coordinates,
)
from theorems.ut5_matrix_phase_alignment import _canonical, _transpose


@dataclass(frozen=True)
class LogicalFiber:
    particular: tuple
    vertical_kernel: tuple


def known_logical_fiber(p, physical_width, logical_width, learned_basis, physical_log):
    """Solve (a,b) in an already known log H <= L_A direct-sum L_B.

    The returned affine set describes LOG coordinates, not multiplication
    of arbitrary logical gate representatives. H being the true symmetry
    subgroup is an external premise; linear independence does not prove it.
    """
    ring(p)
    if (type(physical_width) is not int or physical_width < 1 or
            type(logical_width) is not int or logical_width < 0):
        raise ValueError("positive physical and nonnegative logical widths required")
    _canonical(physical_log,physical_width,p)
    basis = tuple(map(tuple,learned_basis))
    width = physical_width+logical_width
    for row in basis:
        _canonical(row,width,p)
    if len(_fmpz_row_space_basis(basis,width,p)) != len(basis):
        raise ValueError("independent learned subgroup basis required")
    projected = tuple(row[:physical_width] for row in basis)
    coefficients = _fmpz_solve_coordinates(projected,physical_log,p)
    if coefficients is None:
        return None
    def logical_image(row):
        return tuple(sum(c*v[physical_width+j] for c,v in zip(row,basis)) % p
                     for j in range(logical_width))
    null = _fmpz_nullspace_basis(_transpose(projected),len(basis),p) if basis else []
    vertical = _fmpz_row_space_basis([logical_image(row) for row in null],logical_width,p)
    return LogicalFiber(logical_image(coefficients),tuple(vertical))


@dataclass(frozen=True)
class MarkedEncoderGap:
    """V_f|x>=|x,f(x)> with one unknown marked x; A=I tensor Z_p.

    gap_bounds concern the MINIMUM outside overlap gap of this group,
    not copy complexity. In particular its p^2 factor is not claimed
    to be necessary for distinguishing the two encoder Choi states.
    """
    p: int
    logical_dimension: int

    def __post_init__(self):
        ring(self.p)
        if self.p < 3:
            raise ValueError("odd prime required by this control")
        if type(self.logical_dimension) is not int or self.logical_dimension < 2:
            raise ValueError("logical dimension at least two required")

    @property
    def gap_bounds(self):
        d = self.logical_dimension
        population = Fraction(d-1,d*d)
        return (8*population/(self.p*self.p),
                min(Fraction(1),40*population/(self.p*self.p)))

    def choi_copy_lower_bound(self, success=Fraction(2,3)):
        """Necessary copies by Helstrom plus D_k^2 <= 2k/d.

        Only for IID normalized Choi copies, not arbitrary encoder queries.
        An integer return is a lower bound, not a sufficient sample count.
        """
        if not isinstance(success,Fraction) or not Fraction(1,2) < success < 1:
            raise ValueError("exact rational success in (1/2,1) required")
        bound = self.logical_dimension*(2*success-1)**2/2
        return -(-bound.numerator//bound.denominator)

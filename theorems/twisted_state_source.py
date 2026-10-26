"""Public algebra for character-twisted state-symmetry sources.

No state, hidden subgroup, character learner, SDE solver or quantum receiver
is implemented. K and its character must have been learned by a separately
costed procedure. See research/TWISTED_STATE_SYMMETRY_RECEIVER.md.
"""
from dataclasses import dataclass
from fractions import Fraction

from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import (
    _fmpz_nullspace_basis, _fmpz_solve_coordinates,
)
from theorems.ut5_matrix_phase_alignment import _canonical, _identity, _rank, _transpose
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket, _add, _shifted_component


@dataclass(frozen=True)
class CharacterNormalizer:
    kernel: tuple
    normalizer: tuple
    scalar_center_width: int


def character_normalizer(algebra, known_basis, character):
    """Compute M_chi={x:[x,K] <= ker chi}; never infer K or chi from data.

    A Lie character is linear and zero on [K,K]. This condition implies
    K <= M_chi and ker chi is an ideal of M_chi. If chi is nonzero,
    K/ker chi is one-dimensional central with faithful scalar character.
    """
    p,n = algebra.p,algebra.dimension
    basis = tuple(map(tuple,known_basis))
    _canonical(character,len(basis),p)
    for v in basis:
        _canonical(v,n,p)
    if _rank(basis,p) != len(basis):
        raise ValueError("independent known K basis required")
    for a in basis:
        for b in basis:
            coeff = _fmpz_solve_coordinates(basis,algebra.bracket(a,b),p)
            if coeff is None:
                raise ValueError("K must be a Lie subalgebra")
            if sum(c*x for c,x in zip(character,coeff)) % p:
                raise ValueError("character must vanish on [K,K]")
    coefficients = _fmpz_nullspace_basis([character],len(basis),p) if basis else []
    kernel = tuple(tuple(sum(c*v[j] for c,v in zip(row,basis)) % p for j in range(n))
                   for row in coefficients)
    annihilator = _fmpz_nullspace_basis(kernel,n,p)
    equations = []
    for k in basis:
        brackets = [algebra.bracket(e,k) for e in _identity(n)]
        for test in annihilator:
            equations.append(tuple(sum(a*b for a,b in zip(test,v)) % p for v in brackets))
    normalizer = tuple(_fmpz_nullspace_basis(equations,n,p))
    return CharacterNormalizer(kernel,normalizer,int(any(character)))


@dataclass(frozen=True)
class AffineCharacterSector:
    p: int
    particular: tuple
    directions: tuple
    central_constraints: tuple
    character: tuple

    @property
    def label_probability(self):
        """Ideal TWISTED source probability, not a conditional error bound."""
        return Fraction(1,self.p**len(self.directions))

    def contains(self, label):
        _canonical(label,len(self.particular),self.p)
        return tuple(sum(x*y for x,y in zip(row,label)) % self.p
                     for row in self.central_constraints) == self.character


def affine_character_sector(p, center_width, scalar_center_basis, character):
    """Describe lambda|Z=chi as an affine space without enumerating labels.

    For k tensor copies use k*chi mod p, NOT the unamplified character.
    The physical caller must establish that Z is central and acts by chi.
    """
    ring(p)
    if type(center_width) is not int or center_width < 1:
        raise ValueError("positive center width required")
    constraints = tuple(map(tuple,scalar_center_basis))
    _canonical(character,len(constraints),p)
    for row in constraints:
        _canonical(row,center_width,p)
    if _rank(constraints,p) != len(constraints):
        raise ValueError("independent scalar-center basis required")
    particular = (_fmpz_solve_coordinates(_transpose(constraints),character,p)
                  if constraints else (0,)*center_width)
    if particular is None:
        raise ArithmeticError("independent central constraints must be consistent")
    return AffineCharacterSector(p,tuple(particular),
        tuple(_fmpz_nullspace_basis(constraints,center_width,p)),constraints,tuple(character))


def attach_linear_character(packet, scales, outcomes, tensor_powers):
    """Append the UNKNOWN linear phase sum_i k_i*ell(Y_i+s_i*q).

    This is a public coefficient table, not evaluation of ell. Parameters
    are appended even if all k_i vanish modulo p, preserving a fixed schema
    across transcripts using this wrapper. Call once per matrix leaf.
    """
    p,m = packet.p,packet.quotient_width
    if not scales or len(scales) != len(outcomes) or len(scales) != len(tensor_powers):
        raise ValueError("matching nonempty shear/tensor transcript required")
    _canonical(scales,len(scales),p)
    if not all(scales):
        raise ValueError("nonzero shear scales required")
    _canonical(tensor_powers,len(scales),p)
    for y in outcomes:
        _canonical(y,m,p)
    if not packet.parameter_basis:
        raise ValueError("base parameter schema required")
    coordinate = 1+max(a for a,_ in packet.parameter_basis)
    basis = packet.parameter_basis+tuple((coordinate,tuple(int(i == j) for i in range(m)))
                                        for j in range(m))
    terms = dict(packet.terms)
    for scale,y,k in zip(scales,outcomes,tensor_powers):
        _add(terms,_shifted_component(p,packet.width,basis,coordinate,scale,y),k,p)
    return SymbolicScalarPacket(p,m,packet.jet_width,basis,terms)

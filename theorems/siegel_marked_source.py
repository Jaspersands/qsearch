"""Arithmetic budgets for proposed marked polarized-isogeny source lemmas.

This does not evaluate an isogeny, canonicalize a variety, or certify an HSP
oracle. Principal polarizations, genuine d-isogenies, full torsion bases,
and a SINGLE joint polarized, origin-preserving codomain isomorphism are
external proof obligations.
Projective mode permits one invertible scalar per entire torsion basis,
not a separate scalar for each point. See SIEGEL_MARKED_SOURCE_RIGIDITY.md.
"""

from dataclasses import dataclass
from math import gcd, isqrt, prod
from typing import Literal


@dataclass(frozen=True)
class SeparationBudget:
    level: int
    minimum_sufficient_level: int
    rosati_square_bound: int
    strict_separation: bool
    marked_basis_points: int
    mode: Literal["exact", "projective"]


def separation_budget(dimension: int, multiplier: int, orders: tuple[int, ...],
                      characteristic: int,
                      mode: Literal["exact", "projective"]) -> SeparationBudget:
    """Evaluate a sufficient rigidity inequality, NOT source feasibility.

    The multiplier d means phi^*lambda_B=d*lambda_A, so degree(phi)=d**g.
    The characteristic must be a supplied verified prime. Orders can be
    composite but must be pairwise coprime and coprime to d*characteristic.
    Neither their torsion availability nor their computation cost is assumed.
    """
    for name, value in (("dimension", dimension), ("multiplier", multiplier),
                        ("characteristic", characteristic)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if characteristic < 2:
        raise ValueError("Supply a verified positive characteristic prime")
    if mode not in ("exact", "projective"):
        raise ValueError("Mode must be exact or projective")
    if not orders:
        raise ValueError("At least one torsion order is required")
    for i, order in enumerate(orders):
        if not isinstance(order, int) or isinstance(order, bool) or order < 2:
            raise ValueError("Torsion orders must be integers at least two")
        if gcd(order, multiplier * characteristic) != 1:
            raise ValueError("Torsion orders must avoid the degree and characteristic")
        if any(gcd(order, previous) != 1 for previous in orders[:i]):
            raise ValueError("Torsion orders must be pairwise coprime; do not double-count")
    bound = (8 * dimension * multiplier if mode == "exact"
             else 8 * dimension**3 * multiplier**2)
    level = prod(orders)
    return SeparationBudget(level, isqrt(bound) + 1, bound, level * level > bound,
                            2 * dimension * len(orders), mode)

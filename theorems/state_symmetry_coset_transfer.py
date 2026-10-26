"""Paid-gap budget for orbit-state to quantum-hiding-set approximation.

This checks parameter arithmetic only. It neither certifies the overlap
promise nor prepares states, computes unknown cosets, or runs an HSP solver.
Conjugate access for the projective pure-state route must actually exist.
"""
from dataclasses import dataclass
from fractions import Fraction

from theorems.nil3_complete_budget import ceil_log


@dataclass(frozen=True)
class OrbitStateTransferPlan:
    group_order_bound: int
    effective_gap: Fraction
    oracle_uses: int
    error_budget: Fraction
    copies_per_label: int
    overlap_bits: int
    projective_pair: bool

    @property
    def hiding_set_deviation_bound(self):
        if self.effective_gap == 1:
            return Fraction(0)
        return Fraction(self.group_order_bound-1, 2**self.overlap_bits)

    @property
    def hybrid_error_bound(self):
        return self.oracle_uses*self.hiding_set_deviation_bound

    @property
    def preparations_per_label(self):
        return self.copies_per_label*(2 if self.projective_pair else 1)

    @property
    def total_preparation_uses_bound(self):
        # Inverse calls are included when the caller's workflow uses them.
        return self.oracle_uses*self.preparations_per_label


def plan_orbit_state_transfer(group_order_bound, effective_gap, oracle_uses,
                             error_budget=Fraction(1, 100), *,
                             projective_pair=False, conjugate_access=False):
    """Bound every forward/inverse use of a PURE quantum hiding procedure.

    For mixed-state copies the same budget bounds fresh reduced coset
    packets only; it does not grant purification or inverse access.
    In the projective route, the effective gap is for the conjugate pair.
    Passing the original absolute-overlap gap is conservative.
    """
    if (type(group_order_bound) is not int or group_order_bound < 1 or
            type(oracle_uses) is not int or oracle_uses < 1):
        raise ValueError("positive integer order bound and full oracle-use cap required")
    if not isinstance(effective_gap, Fraction) or not 0 < effective_gap <= 1:
        raise ValueError("a paid exact rational effective overlap gap in (0,1] is required")
    if not isinstance(error_budget, Fraction) or not 0 < error_budget < 1:
        raise ValueError("an exact rational error budget in (0,1) is required")
    if type(projective_pair) is not bool or type(conjugate_access) is not bool:
        raise ValueError("access flags must be booleans")
    if projective_pair and not conjugate_access:
        raise ValueError("projective pairing needs actual conjugate preparation AND action access")
    bits = group_order_bound.bit_length()+ceil_log(2, 4*oracle_uses/error_budget)
    ratio = Fraction(bits)/effective_gap
    copies = 1 if effective_gap == 1 else -(-ratio.numerator//ratio.denominator)
    result = OrbitStateTransferPlan(group_order_bound, effective_gap, oracle_uses,
                                   error_budget, copies, bits, projective_pair)
    if result.hybrid_error_bound > error_budget/4:
        raise ArithmeticError("transfer error allocation exceeded")
    return result

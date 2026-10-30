"""Public maps for learning polynomial phases under finite-support phase noise.

This is an adapter and conditional resource certificate, not an executed
antisymmetrizer/quantum learner. Hidden polynomial coefficients and error
labels never enter these APIs. See research/EXTERIOR_NOISY_PHASE_LEARNING.md.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from theorems.affine_phase_erasure import monomials
from theorems.polynomial_phase_copy_learning import (
    LearningFrame, _parameters, copy_envelope,
)
from theorems.rees_subspace_source import SubspacePlan
from theorems.ut5_matrix_phase_alignment import _canonical


def _offsets(p, width, degree, relative_offsets):
    _parameters(p, width, degree)
    offsets = tuple(tuple(u) for u in relative_offsets)
    for u in offsets:
        _canonical(u, width, p)
    rank = len(offsets) + 1
    if rank > p**width or rank % p == 0:
        raise ValueError("rank must fit the ambient space and be nonzero modulo p")
    return offsets + ((0,)*width,)


def translation_sum_matrix(p, width, degree, relative_offsets):
    """A_u = sum_i T_(u_i) modulo constants, with final u_r = 0.

    relative_offsets are observed measurement outcomes, NOT chosen queries.
    Rows are output coefficients; columns are input coefficients in the
    LearningFrame monomial order. No field-point enumeration is performed.
    """
    offsets = _offsets(p, width, degree, relative_offsets)
    indices = tuple(a for a in monomials(width, degree) if any(a))
    return tuple(tuple(
        0 if any(b > a for a, b in zip(alpha, beta)) else
        sum(prod(comb(a, b)*pow(u, a-b, p)
                 for a, b, u in zip(alpha, beta, offset))
            for offset in offsets) % p
        for alpha in indices) for beta in indices)


def _matvec(matrix, vector, p):
    return tuple(sum(a*b for a, b in zip(row, vector)) % p for row in matrix)


def translated_frame(frame, relative_offsets):
    """Express A_u J using the SAME unknown eta as the original frame J.

    A_u = r I + N, where N strictly lowers degree. Since p does not divide
    r, this is invertible, so the transformed public basis stays independent.
    """
    matrix = translation_sum_matrix(frame.p, frame.width, frame.degree, relative_offsets)
    return LearningFrame(
        frame.p, frame.width, frame.degree,
        _matvec(matrix, frame.known, frame.p),
        tuple(_matvec(matrix, row, frame.p) for row in frame.basis),
    )


def inverse_translation_sum(p, width, degree, relative_offsets, coefficients):
    """Invert a public translation sum modulo constants by a finite series.

    This is a coefficient-map control, not a measurement of an unknown
    state's polynomial. It must never be used as hidden-source access.
    """
    relative_offsets = tuple(tuple(u) for u in relative_offsets)
    matrix = translation_sum_matrix(p, width, degree, relative_offsets)
    _canonical(coefficients, len(matrix), p)
    rank_mod_p = (len(relative_offsets)+1) % p
    inv = pow(rank_mod_p, -1, p)
    term = tuple(coefficients)
    result = [0]*len(matrix)
    for _ in range(degree):
        result = [(x+inv*y) % p for x, y in zip(result, term)]
        mapped = _matvec(matrix, term, p)
        term = tuple((-inv*(a-rank_mod_p*b)) % p for a, b in zip(mapped, term))
    if any(term):
        raise ArithmeticError("translation remainder did not lower degree")
    return tuple(result)


def exterior_line_packet(frame, relative_offsets, axis, observed):
    """Public correction/packet for one independently prepared top wedge.

    Measure relative offsets, then the non-axis coordinates. Apply the
    returned known correction before phase elimination. Both measurements
    are outcomes, not requests for chosen coordinates or repeated errors.
    Keep frame and axis fixed throughout an elimination tree, even though
    each leaf has different offsets. Returned rows refer to the ORIGINAL
    frame's eta, and hence can be merged across leaves.
    """
    transformed = translated_frame(frame, relative_offsets)
    correction, packet = transformed.restrict(axis, observed)
    frame.check_coordinate_packet(axis, packet)
    return correction, packet


def noisy_copy_envelope(p, width, degree, rank, error=Fraction(1, 3)):
    """Uniform-error source cap, with explicit unresolved backend obligations.

    Uses the conservative public-map learner envelope, not the sharper
    fixed-axis bound. Four error accounts: learner exhaustion, wedge abort,
    bounded SDE abort, and COMPLETE quantum-instrument implementation error.
    Rank is supplied and exact; learning it is not included in this cap.
    """
    _parameters(p, width, degree)
    if type(rank) is not int or rank < 1 or rank > p**width or rank % p == 0:
        raise ValueError("positive feasible rank nonzero modulo p required")
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error fraction in (0,1) required")
    learner = copy_envelope(p, width, degree, error/2)
    wedge_cap = learner["original_copy_abort_cap"]
    plan = SubspacePlan(rank, wedge_cap, error/4)
    return {
        "prime": p, "variables": width, "degree": degree, "rank": rank,
        "rank_known_exactly": True,
        "source": "IID uniform mixture of distinct linear-phase errors",
        "recoverable_object": "nonlinear polynomial coefficients; affine terms are gauge",
        "learner": learner,
        "top_wedge_output_cap": wedge_cap,
        "raw_noisy_copy_cap": plan.raw_copy_cap,
        "growth_attempt_cap": plan.growth_attempt_cap,
        "multiplexed_register_swap_cap": plan.multiplexed_register_swap_cap,
        "source_register_bits": width*p.bit_length(),
        "relative_coordinate_subtraction_cap": wedge_cap*(rank-1)*width,
        "learner_abort_bound": error/4,
        "wedge_abort_bound": plan.abort_probability_bound,
        "sde_abort_budget": error/4,
        "sde_call_cap": wedge_cap,
        "required_sde_abort_per_call": error/(4*wedge_cap),
        "complete_instrument_error_budget": error/4,
        "total_error_upper_bound": 3*error/4+plan.abort_probability_bound,
        "full_quantum_backend_implemented": False,
        "sde_runtime_included": False,
        "source_promise_certified": False,
        "rees_receiver_required": False,
    }


def report():
    """Replay exact public-map controls, not a noisy-source learning run."""
    import hashlib
    from pathlib import Path

    frame = LearningFrame.initial(5, 2, 3)
    offsets = ((1, 2),)
    transformed = translated_frame(frame, offsets)
    basis_roundtrips = all(
        inverse_translation_sum(5, 2, 3, offsets, changed) == original
        for original, changed in zip(frame.basis, transformed.basis)
    )
    axis = frame.next_axis()
    packets = [exterior_line_packet(frame, offsets, axis, (y,))[1] for y in range(5)]
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/exterior_phase_learning.py",
        "theorems/polynomial_phase_copy_learning.py",
        "theorems/rees_subspace_source.py",
        "tests/test_exterior_phase_learning.py",
        "research/EXTERIOR_NOISY_PHASE_LEARNING.md",
        "research/NOISY_QUADRATIC_PHASE_FILTER.md",
        "qsearch_cli/commands/sde.py",
    )
    return {
        "status": "DIRECT_NOISY_PHASE_REDUCTION_WITH_PUBLIC_MAP_CONTROLS",
        "scope": "exact coefficient controls and conditional uniform-source budget",
        "public_map_basis_roundtrips": basis_roundtrips,
        "public_line_packets_checked": len(packets),
        "fixed_axis_filtration_checked": True,
        "quantum_source_prepared": False,
        "quantum_learning_run": False,
        "novelty_established": False,
        "classical_hardness_established": False,
        "standard_lwe_reduction": False,
        "rees_receiver_required": False,
        "affine_gauge_recoverable": False,
        "nonuniform_noise_budget_implemented": False,
        "quadratic_competitor": "four-copy cancellation with SWAP or classical symplectic verification",
        "quadratic_competitor_end_to_end_implemented": False,
        "counterexample": "rank divisible by p can erase nonlinear phase information",
        "budget": noisy_copy_envelope(101, 2, 3, 2),
        "remaining_obligations": [
            "independent human proof and prior-art review",
            "physical wedge and public-map learner integration",
            "bounded SDE solver and complete-instrument precision allocation",
            "useful native input reduction and matched-access competing learners",
        ],
        "source_sha256": {path: hashlib.sha256((root/path).read_bytes()).hexdigest()
                          for path in sources},
    }

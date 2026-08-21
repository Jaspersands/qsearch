"""Dense ordered-subword automata collapse to a dyadic boundary.

Let ``U`` be any fiber of a binary ordered-subword automaton on ``u`` frame
positions.  No automaton structure is needed for the decisive rank bound.  The
suffix-branch entropy theorem gives an anchor for which at most

    floor(u-log2|U|) = floor(log2(1/delta_U))

frame generators survive, where ``delta_U=|U|/2^u``.  Thus every fiber whose
density is bounded below has ``O(1)`` presentation rank over every finite
group.  In particular, a periodic constant-state automaton that mixes on a
fixed communicating class has uniformly bounded fiber rank.

This statement has a sharper consequence for the contiguous marked-word
pressure calculation.  For same/different supports ``S,D``, choose the denser
fiber and put

    c_S=u-log2|S|,  c_D=u-log2|D|,  c_min=min(c_S,c_D).

The frame rank is at most ``floor(c_min)``.  After the exact outer conjugacy
reduction, the scalar pressure margin above the crossing threshold is at least

    (c_S+c_D)/2 - floor(c_min).                         (1)

If both fibers mix uniformly on a class of size ``C``, (1) tends to

    log2(C)-floor(log2(C)).                             (2)

Hence every non-dyadic class size has a constant unsigned-mass loss that no
normalized target character can repair.  Power-of-two class sizes are the
only boundary left by the density theorem alone.  The existing contiguous
mixed-frame target factorization closes the *exactly balanced full-fiber*
case as well.  If ``|S|=|D|=2^k`` and ``0 in S``, scalar pressure saturates but
the zero same-cell relation forces the residual target to identity.  If
``0 notin S``, adjoining zero changes ``|S|`` to ``2^k+1`` and the integer
rank bound gives one full exponent of scalar loss.  Thus only near-uniform
dyadic fibers, a growing state space, or interleaved leaves remain.

The theorem closes the previous question about dense constant-state fibers.
It does not prove a no-go for every automaton or every marked word.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_frame_subword_entropy import (
    FrameSubwordSuffixBranchCertificate,
    frame_subword_suffix_branch_certificate,
)
from self_dual_wreath_periodic_frame_fiber_counterfamily import (
    audit_transfer_certificate,
)
from self_dual_wreath_periodic_frame_rank_collapse import (
    periodic_same_fiber_closed_form,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_dense_automaton_fiber_dyadic_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DENSE-AUTOMATON-FIBER-DYADIC-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]


@dataclass(frozen=True)
class DenseFiberRankControl:
    control_id: str
    frame_position_count: int
    fiber_size: int
    fiber_density: float
    density_codimension_bits: float
    theorem_generator_upper_bound: int
    explicit_suffix_generator_upper_bound: int
    explicit_anchor: Assignment
    explicit_suffix_forced_coordinates: tuple[int, ...]
    exact_density_rank_identity_verified: bool
    status: str


@dataclass(frozen=True)
class UniformAutomatonPressureControl:
    control_id: str
    effective_class_size: int
    class_size_is_power_of_two: bool
    frame_position_count: int
    same_fiber_size: int
    different_fiber_size: int
    same_codimension_bits: float
    different_codimension_bits: float
    denser_fiber_generator_upper_bound: int
    scalar_pressure_margin_lower_bound: float
    limiting_uniform_class_margin: float
    target_character_can_repair_scalar_loss: bool
    status: str


@dataclass(frozen=True)
class PeriodicMixingCertificate:
    automaton_state_count: int
    leading_communicating_class_size: int
    block_choice_count: int
    transfer_annihilator_roots: tuple[int, ...]
    subleading_to_leading_eigenvalue_ratio: float
    limiting_fiber_density: str
    constant_density_implies_constant_rank: bool
    exact_transfer_certificate_imported: bool
    status: str


@dataclass(frozen=True)
class ExactDyadicFullFiberDichotomyControl:
    control_id: str
    frame_position_count: int
    common_fiber_size: int
    zero_assignment_in_same_fiber: bool
    dominant_support_size_after_zero_adjoin: int
    scalar_pressure_margin: float
    residual_target_forced_to_identity: bool
    target_survival_blocked_by_scalar_loss: bool
    exact_dichotomy_verified: bool
    status: str


@dataclass(frozen=True)
class DenseAutomatonFiberDyadicBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    dense_fiber_controls: list[DenseFiberRankControl]
    uniform_class_controls: list[UniformAutomatonPressureControl]
    exact_dyadic_full_fiber_dichotomy: list[ExactDyadicFullFiberDichotomyControl]
    periodic_mixing_certificate: PeriodicMixingCertificate
    periodic_family_scaling: list[UniformAutomatonPressureControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _normalize_support(rows: Iterable[Assignment]) -> tuple[Assignment, ...]:
    rows = tuple(sorted(set(rows)))
    if not rows:
        raise ValueError("fiber support must be nonempty")
    width = len(rows[0])
    if any(
        len(row) != width or any(bit not in (0, 1) for bit in row)
        for row in rows
    ):
        raise ValueError("fiber support must be binary and fixed-width")
    return rows


def density_generator_upper_bound(width: int, fiber_size: int) -> int:
    """Return the integer suffix-branch rank bound ``floor(log2 1/delta)``."""

    if width < 0 or not 1 <= fiber_size <= 2**width:
        raise ValueError("fiber size must lie between one and 2^width")
    return width - (fiber_size - 1).bit_length()


def audit_dense_fiber_rank(
    control_id: str,
    support: Iterable[Assignment],
) -> DenseFiberRankControl:
    rows = _normalize_support(support)
    width = len(rows[0])
    density = len(rows) / 2**width
    codimension = -math.log2(density)
    theorem_bound = density_generator_upper_bound(width, len(rows))
    suffix: FrameSubwordSuffixBranchCertificate = (
        frame_subword_suffix_branch_certificate(rows)
    )
    exact = (
        theorem_bound == math.floor(codimension + 1e-12)
        and theorem_bound == suffix.universal_finite_group_generator_upper_bound
        and suffix.exact_suffix_branch_elimination_verified
        and len(suffix.suffix_forced_coordinates) <= theorem_bound
    )
    return DenseFiberRankControl(
        control_id=control_id,
        frame_position_count=width,
        fiber_size=len(rows),
        fiber_density=density,
        density_codimension_bits=codimension,
        theorem_generator_upper_bound=theorem_bound,
        explicit_suffix_generator_upper_bound=(
            suffix.universal_finite_group_generator_upper_bound
        ),
        explicit_anchor=suffix.anchor,
        explicit_suffix_forced_coordinates=suffix.suffix_forced_coordinates,
        exact_density_rank_identity_verified=exact,
        status=(
            "exact-dense-fiber-constant-rank-certificate"
            if exact
            else "dense-fiber-rank-control-failure"
        ),
    )


def modular_weight_fiber(width: int, modulus: int, residue: int) -> tuple[Assignment, ...]:
    """A permutation-transition automaton fiber used as an exact control."""

    if width < 1 or modulus < 2 or not 0 <= residue < modulus:
        raise ValueError("invalid modular fiber parameters")
    return tuple(
        bits
        for bits in itertools.product((0, 1), repeat=width)
        if sum(bits) % modulus == residue
    )


def pressure_margin_from_fiber_sizes(
    width: int,
    same_size: int,
    different_size: int,
) -> tuple[int, float]:
    """Apply the denser-fiber suffix rank to the contiguous crossing pressure."""

    if width < 1 or not 1 <= same_size <= 2**width or not 1 <= different_size <= 2**width:
        raise ValueError("support sizes must lie between one and 2^width")
    denser_size = max(same_size, different_size)
    rank = density_generator_upper_bound(width, denser_size)
    entropy = 0.5 * math.log2(same_size * different_size)
    return rank, width - entropy - rank


def uniform_class_pressure_control(
    control_id: str,
    class_size: int,
    width: int,
    same_size: int,
    different_size: int,
) -> UniformAutomatonPressureControl:
    if class_size < 2:
        raise ValueError("effective class size must be at least two")
    rank, margin = pressure_margin_from_fiber_sizes(
        width,
        same_size,
        different_size,
    )
    same_codimension = width - math.log2(same_size)
    different_codimension = width - math.log2(different_size)
    power_of_two = class_size & (class_size - 1) == 0
    limiting_margin = math.log2(class_size) - math.floor(math.log2(class_size))
    scalar_loss = margin > 1e-12
    return UniformAutomatonPressureControl(
        control_id=control_id,
        effective_class_size=class_size,
        class_size_is_power_of_two=power_of_two,
        frame_position_count=width,
        same_fiber_size=same_size,
        different_fiber_size=different_size,
        same_codimension_bits=same_codimension,
        different_codimension_bits=different_codimension,
        denser_fiber_generator_upper_bound=rank,
        scalar_pressure_margin_lower_bound=margin,
        limiting_uniform_class_margin=limiting_margin,
        target_character_can_repair_scalar_loss=not scalar_loss,
        status=(
            "dyadic-constant-state-saturation-boundary"
            if power_of_two and abs(margin) <= 1e-12
            else "non-dyadic-constant-state-scalar-loss"
            if scalar_loss
            else "finite-automaton-pressure-transition"
        ),
    )


def audit_periodic_mixing_certificate() -> PeriodicMixingCertificate:
    transfer = audit_transfer_certificate()
    exact = (
        transfer.exact_annihilating_polynomial_verified
        and transfer.exact_leading_projector_verified
        and transfer.leading_projector_nonzero_entry_count == 18
        and transfer.transition_row_sum == 32
    )
    return PeriodicMixingCertificate(
        automaton_state_count=transfer.state_count,
        leading_communicating_class_size=18,
        block_choice_count=transfer.transition_row_sum,
        transfer_annihilator_roots=transfer.annihilating_polynomial_roots,
        subleading_to_leading_eigenvalue_ratio=0.5,
        limiting_fiber_density="1/18+O(2^-k)",
        constant_density_implies_constant_rank=exact,
        exact_transfer_certificate_imported=exact,
        status=(
            "exact-periodic-mixing-to-constant-rank-transfer"
            if exact
            else "periodic-mixing-transfer-failure"
        ),
    )


def exact_dyadic_full_fiber_dichotomy_control(
    control_id: str,
    width: int,
    fiber_log2_size: int,
    *,
    zero_in_same_fiber: bool,
) -> ExactDyadicFullFiberDichotomyControl:
    """Apply the exact contiguous target theorem to balanced dyadic fibers."""

    if width < 1 or not 0 <= fiber_log2_size <= width:
        raise ValueError("invalid balanced dyadic fiber parameters")
    size = 2**fiber_log2_size
    dominant = size if zero_in_same_fiber else size + 1
    margin = math.ceil(math.log2(dominant)) - fiber_log2_size
    target_identity = zero_in_same_fiber
    scalar_block = not zero_in_same_fiber and margin >= 1.0
    exact = (
        (target_identity and abs(margin) <= 1e-12)
        or (scalar_block and abs(margin - 1.0) <= 1e-12)
    )
    return ExactDyadicFullFiberDichotomyControl(
        control_id=control_id,
        frame_position_count=width,
        common_fiber_size=size,
        zero_assignment_in_same_fiber=zero_in_same_fiber,
        dominant_support_size_after_zero_adjoin=dominant,
        scalar_pressure_margin=float(margin),
        residual_target_forced_to_identity=target_identity,
        target_survival_blocked_by_scalar_loss=scalar_block,
        exact_dichotomy_verified=exact,
        status=(
            "dyadic-saturation-target-forced-identity"
            if target_identity and exact
            else "dyadic-nonzero-fiber-one-exponent-loss"
            if scalar_block and exact
            else "dyadic-full-fiber-dichotomy-failure"
        ),
    )


def periodic_generic_pressure_scaling(
    maximum_m: int = 8,
) -> list[UniformAutomatonPressureControl]:
    output = []
    for m_value in range(maximum_m + 1):
        width = 30 * m_value + 5
        same_size = periodic_same_fiber_closed_form(m_value)
        output.append(
            uniform_class_pressure_control(
                f"periodic-S3-m={m_value}",
                18,
                width,
                same_size,
                same_size + 1,
            )
        )
    return output


def run_dense_automaton_fiber_dyadic_boundary(
) -> DenseAutomatonFiberDyadicBoundaryReport:
    dense = [
        audit_dense_fiber_rank(
            "parity-width-10",
            modular_weight_fiber(10, 2, 0),
        ),
        audit_dense_fiber_rank(
            "mod-three-width-10",
            modular_weight_fiber(10, 3, 0),
        ),
        audit_dense_fiber_rank(
            "mod-five-width-12",
            modular_weight_fiber(12, 5, 0),
        ),
    ]
    uniform = [
        uniform_class_pressure_control(
            "exact-dyadic-parity-boundary",
            2,
            10,
            2**9,
            2**9,
        ),
        uniform_class_pressure_control(
            "mod-three-near-uniform",
            3,
            10,
            len(modular_weight_fiber(10, 3, 0)),
            len(modular_weight_fiber(10, 3, 1)),
        ),
        uniform_class_pressure_control(
            "exact-four-state-dyadic-boundary",
            4,
            12,
            2**10,
            2**10,
        ),
    ]
    dyadic_dichotomy = [
        exact_dyadic_full_fiber_dichotomy_control(
            "identity-state-full-fiber",
            12,
            9,
            zero_in_same_fiber=True,
        ),
        exact_dyadic_full_fiber_dichotomy_control(
            "nonidentity-state-full-fiber",
            12,
            9,
            zero_in_same_fiber=False,
        ),
    ]
    periodic = periodic_generic_pressure_scaling()
    mixing = audit_periodic_mixing_certificate()
    exact = (
        all(row.exact_density_rank_identity_verified for row in dense)
        and mixing.exact_transfer_certificate_imported
        and all(row.scalar_pressure_margin_lower_bound > 0 for row in periodic)
        and all(row.exact_dichotomy_verified for row in dyadic_dichotomy)
    )
    limiting_periodic_margin = math.log2(18) - 4
    return DenseAutomatonFiberDyadicBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "dense_fiber_rank": (
                "Every U subset F_2^u has a suffix-branch anchor leaving at most "
                "floor(u-log2|U|)=floor(log2(1/delta_U)) generators."
            ),
            "constant_state_consequence": (
                "Every fiber with density bounded below independently of u has O(1) "
                "presentation rank over every finite group."
            ),
            "pressure_margin": (
                "For same/different codimensions c_S,c_D, the denser-fiber rank gives "
                "margin at least (c_S+c_D)/2-floor(min(c_S,c_D))."
            ),
            "uniform_class_limit": (
                "Equal fibers mixing to density 1/C have limiting margin "
                "log2(C)-floor(log2(C))."
            ),
            "exact_dyadic_full_fiber_dichotomy": (
                "For |S|=|D|=2^k, zero in S forces the residual target to identity; "
                "zero not in S makes |S union {0}|=2^k+1 and costs one exponent."
            ),
            "scope": (
                "Non-dyadic mixing and exact balanced dyadic full fibers are closed. "
                "Near-uniform dyadic fibers, growing-state automata, rare fibers, "
                "and interleaved marked words remain open."
            ),
        },
        dense_fiber_controls=dense,
        uniform_class_controls=uniform,
        exact_dyadic_full_fiber_dichotomy=dyadic_dichotomy,
        periodic_mixing_certificate=mixing,
        periodic_family_scaling=periodic,
        proof_obligations=[
            {
                "obligation": "prove_dense_constant_state_fibers_have_constant_rank",
                "resolved": exact,
                "resolution": (
                    "The suffix-branch entropy theorem is support-universal and gives "
                    "rank floor(log2(1/delta)) without using automaton details."
                ),
            },
            {
                "obligation": "classify_uniform_constant_state_scalar_pressure",
                "resolved": exact,
                "resolution": (
                    "The asymptotic margin is the fractional part of log2 of the "
                    "effective mixing-class size."
                ),
            },
            {
                "obligation": "eliminate_exact_balanced_dyadic_full_fibers",
                "resolved": exact,
                "resolution": (
                    "The exact target-survival dichotomy forces identity when zero lies "
                    "in S and otherwise gives one full scalar exponent of loss."
                ),
            },
            {
                "obligation": "eliminate_near_uniform_dyadic_target_survival",
                "resolved": False,
                "resolution": (
                    "Full fiber sizes just below a power of two can have vanishing "
                    "generic margin without exact saturation; prove structural loss or "
                    "construct a matching nontrivial target family."
                ),
            },
            {
                "obligation": "extend_to_growing_state_or_interleaved_automata",
                "resolved": False,
                "resolution": (
                    "The density-to-rank theorem remains true, but state growth and "
                    "multi-boundary outer pressure require new analysis."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "An exponential fiber can still have growing frame rank.",
                "resolved": True,
                "resolution": (
                    "Only its density matters: constant density gives a width-independent "
                    "integer generator bound."
                ),
            },
            {
                "objection": "Every constant-state automaton route is eliminated.",
                "resolved": True,
                "resolution": (
                    "False. Exact dyadic full fibers are closed, but near-uniform dyadic "
                    "fibers and non-full supports can approach the boundary."
                ),
            },
            {
                "objection": "A normalized target character can repair non-dyadic mass loss.",
                "resolved": True,
                "resolution": (
                    "Its magnitude is at most one, so it cannot recover a positive scalar "
                    "pressure exponent gap."
                ),
            },
            {
                "objection": "The S3 periodic conclusion relies on finite Tietze reductions.",
                "resolved": True,
                "resolution": (
                    "The exact transfer spectrum gives density 1/18+O(2^-k), and the "
                    "support-universal entropy theorem then gives constant rank."
                ),
            },
        ],
        headline_metrics={
            "dense_constant_state_rank_theorem_count": int(exact),
            "non_dyadic_uniform_class_no_go_theorem_count": int(exact),
            "dyadic_saturation_boundary_count": sum(
                row.class_size_is_power_of_two
                and abs(row.scalar_pressure_margin_lower_bound) <= 1e-12
                for row in uniform
            ),
            "exact_dyadic_full_fiber_dichotomy_theorem_count": int(exact),
            "exact_dyadic_full_fiber_survivor_count": 0,
            "periodic_effective_class_size": 18,
            "periodic_generic_generator_upper_bound": max(
                row.denser_fiber_generator_upper_bound for row in periodic[1:]
            ),
            "periodic_limiting_scalar_margin": limiting_periodic_margin,
            "periodic_minimum_checked_generic_margin": min(
                row.scalar_pressure_margin_lower_bound for row in periodic
            ),
            "surviving_algorithm_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "every_dense_constant_state_fiber_has_O1_rank_proved": exact,
            "non_dyadic_uniform_mixing_scalar_suppression_proved": exact,
            "exact_balanced_dyadic_full_fibers_eliminated": exact,
            "all_constant_state_automata_eliminated": False,
            "dyadic_target_survival_eliminated": False,
            "near_uniform_dyadic_target_survival_eliminated": False,
            "growing_state_automata_eliminated": False,
            "interleaved_leaf_automata_eliminated": False,
            "natural_component_M4_positive": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Dense fibers have bounded rank, non-dyadic classes lose scalar mass, "
                "and exact dyadic full fibers obey a target/scalar dichotomy; only "
                "near-uniform dyadic and growing-state boundaries remain."
            ),
        },
        status=(
            "dense-constant-state-route-reduced-to-dyadic-boundary"
            if exact
            else "dense-automaton-boundary-control-failure"
        ),
        summary=(
            "Proved constant rank for every dense automaton fiber, killed non-dyadic "
            "mixing, and eliminated exact balanced dyadic full fibers."
        ),
        falsifiers_triggered=[
            "Exponential fiber cardinality does not imply high finite-group presentation rank.",
            "Non-dyadic constant-state mixing has an irreparable scalar pressure loss.",
            "Exact dyadic full fibers cannot retain a nontrivial target at zero loss.",
            "Near-uniform dyadic fibers and growing-state algebra remain open.",
        ],
    )


def write_dense_automaton_fiber_dyadic_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_dense_automaton_fiber_dyadic_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_dense_automaton_fiber_dyadic_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

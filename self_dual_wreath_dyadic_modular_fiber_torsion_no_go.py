"""Cyclic-torsion no-go for dyadic modular automaton fibers.

The dense-automaton theorem leaves power-of-two mixing classes on the scalar
boundary.  The canonical dyadic example is the ``m``-state automaton that
records Hamming weight modulo ``m``.  Its zero fiber is

    U_(m,u)={v in F_2^u : |v|=0 mod m}.

For ``u>=m+1``, the ordered-subword presentation is exactly cyclic:

    P(U_(m,u)) = <x_1,...,x_u | w_v=1, v in U_(m,u)> ~= C_m.

Indeed every ``m``-subset is a relation.  For adjacent coordinates ``i,i+1``,
choose any other ``m-1`` coordinates.  The two corresponding ordered words
have identical prefix and suffix, so cancellation gives ``x_i=x_(i+1)``.
All generators are therefore one generator ``x``, and an ``m``-subset gives
``x^m=1``.  Conversely every fiber relation has length divisible by ``m``, so
it follows from ``x^m=1``.

The fiber density tends ``1/m`` by the roots-of-unity filter, with

    ||U|/2^u-1/m| <= (m-1)/m * cos(pi/m)^u.

The generic entropy bound would leave ``log2(m)`` generators when ``m`` is a
power of two and hence permits zero scalar margin.  The exact presentation
leaves a single torsion generator.  The number of permutations in ``S_n``
whose order divides ``m`` is

    |S_n|^(1-1/m+o(1)),

from the cycle-index sum over cycle lengths dividing ``m``.  Therefore the
true limiting scalar pressure margin for equal zero fibers is

    log2(m) - (1-1/m).

For every fixed dyadic ``m>=2`` this is positive.  A normalized target
character cannot repair the missing unsigned mass.  This kills cyclic dyadic
automata, not nonabelian dyadic automata, growing moduli, or interleaved words.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_dense_automaton_fiber_dyadic_boundary import (
    density_generator_upper_bound,
)
from self_dual_wreath_frame_subword_entropy import frame_subword_reduction


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_dyadic_modular_fiber_torsion_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DYADIC-MODULAR-FIBER-TORSION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]


@dataclass(frozen=True)
class ModularFiberPresentationControl:
    modulus: int
    frame_position_count: int
    fiber_size: int
    expected_weight_m_relation_count: int
    adjacent_pair_count: int
    adjacent_cancellation_witness_count: int
    tietze_remaining_generator_count: int
    tietze_residual_relations: tuple[tuple[int, ...], ...]
    expected_cyclic_relation_length: int
    exact_cyclic_presentation_verified: bool
    status: str


@dataclass(frozen=True)
class ModularFiberScalingRecord:
    modulus: int
    modulus_is_power_of_two: bool
    frame_position_count: int
    exact_fiber_size: int
    exact_fiber_density: float
    limiting_fiber_density: float
    density_deviation: float
    roots_of_unity_deviation_upper_bound: float
    density_codimension_bits: float
    generic_suffix_generator_upper_bound: int
    true_symmetric_group_frame_solution_exponent: float
    true_scalar_pressure_margin: float
    limiting_true_scalar_pressure_margin: float
    status: str


@dataclass(frozen=True)
class DyadicModularFiberTorsionNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    presentation_controls: list[ModularFiberPresentationControl]
    scaling_records: list[ModularFiberScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def modular_zero_fiber_size(width: int, modulus: int) -> int:
    if width < 0 or modulus < 2:
        raise ValueError("width must be nonnegative and modulus at least two")
    return sum(
        math.comb(width, weight)
        for weight in range(0, width + 1, modulus)
    )


def modular_zero_fiber(width: int, modulus: int) -> tuple[Assignment, ...]:
    if width < 1 or modulus < 2:
        raise ValueError("width must be positive and modulus at least two")
    return tuple(
        bits
        for bits in itertools.product((0, 1), repeat=width)
        if sum(bits) % modulus == 0
    )


def roots_of_unity_density_deviation_bound(width: int, modulus: int) -> float:
    if width < 0 or modulus < 2:
        raise ValueError("invalid roots-of-unity bound parameters")
    return (modulus - 1) / modulus * abs(math.cos(math.pi / modulus)) ** width


def audit_modular_fiber_presentation(
    modulus: int,
) -> ModularFiberPresentationControl:
    """Use width ``m+1`` as the finite Tietze fingerprint of the all-width proof."""

    if modulus < 2:
        raise ValueError("modulus must be at least two")
    width = modulus + 1
    support = modular_zero_fiber(width, modulus)
    reduction = frame_subword_reduction(support)
    expected_relation = tuple(-reduction.remaining_generators[0] for _ in range(modulus))
    adjacent_witnesses = 0
    universe = tuple(range(width))
    for left in range(width - 1):
        others = tuple(index for index in universe if index not in (left, left + 1))
        if len(others) >= modulus - 1:
            adjacent_witnesses += 1
    exact = (
        len(reduction.remaining_generators) == 1
        and reduction.residual_relations == (expected_relation,)
        and adjacent_witnesses == width - 1
        and len(support) == 1 + math.comb(width, modulus)
    )
    return ModularFiberPresentationControl(
        modulus=modulus,
        frame_position_count=width,
        fiber_size=len(support),
        expected_weight_m_relation_count=math.comb(width, modulus),
        adjacent_pair_count=width - 1,
        adjacent_cancellation_witness_count=adjacent_witnesses,
        tietze_remaining_generator_count=len(reduction.remaining_generators),
        tietze_residual_relations=reduction.residual_relations,
        expected_cyclic_relation_length=modulus,
        exact_cyclic_presentation_verified=exact,
        status=(
            "exact-modular-fiber-cyclic-presentation-control"
            if exact
            else "modular-fiber-presentation-control-failure"
        ),
    )


def modular_fiber_scaling_record(
    modulus: int,
    width: int,
) -> ModularFiberScalingRecord:
    if modulus < 2 or width < modulus + 1:
        raise ValueError("scaling requires modulus>=2 and width>=modulus+1")
    size = modular_zero_fiber_size(width, modulus)
    density = size / 2**width
    limit = 1.0 / modulus
    deviation = abs(density - limit)
    bound = roots_of_unity_density_deviation_bound(width, modulus)
    codimension = -math.log2(density)
    generic_rank = density_generator_upper_bound(width, size)
    true_exponent = 1.0 - 1.0 / modulus
    margin = codimension - true_exponent
    limiting_margin = math.log2(modulus) - true_exponent
    exact = deviation <= bound + 1e-15 and margin > 0
    return ModularFiberScalingRecord(
        modulus=modulus,
        modulus_is_power_of_two=modulus & (modulus - 1) == 0,
        frame_position_count=width,
        exact_fiber_size=size,
        exact_fiber_density=density,
        limiting_fiber_density=limit,
        density_deviation=deviation,
        roots_of_unity_deviation_upper_bound=bound,
        density_codimension_bits=codimension,
        generic_suffix_generator_upper_bound=generic_rank,
        true_symmetric_group_frame_solution_exponent=true_exponent,
        true_scalar_pressure_margin=margin,
        limiting_true_scalar_pressure_margin=limiting_margin,
        status=(
            "cyclic-torsion-gives-positive-scalar-gap"
            if exact
            else "modular-fiber-scaling-control-failure"
        ),
    )


def run_dyadic_modular_fiber_torsion_no_go(
) -> DyadicModularFiberTorsionNoGoReport:
    presentations = [audit_modular_fiber_presentation(m) for m in (2, 3, 4, 5)]
    scaling = [
        modular_fiber_scaling_record(modulus, multiple * modulus)
        for modulus in (2, 3, 4, 8, 16)
        for multiple in (2, 4, 8)
        if multiple * modulus >= modulus + 1
    ]
    exact = all(row.exact_cyclic_presentation_verified for row in presentations) and all(
        row.status == "cyclic-torsion-gives-positive-scalar-gap" for row in scaling
    )
    dyadic = [row for row in scaling if row.modulus_is_power_of_two]
    return DyadicModularFiberTorsionNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "fiber": "U_(m,u)={v in F_2^u: HammingWeight(v)=0 mod m}.",
            "presentation_isomorphism": (
                "For u>=m+1, adjacent m-subset relations identify all x_i and an "
                "m-subset gives x^m=1; every other relation follows. Thus P(U)=C_m."
            ),
            "density_bound": (
                "The roots-of-unity filter gives ||U|/2^u-1/m| <= "
                "((m-1)/m)cos(pi/m)^u."
            ),
            "symmetric_group_torsion_exponent": (
                "The cycle index for permutations with cycle lengths dividing m gives "
                "#Hom(C_m,S_n)=|S_n|^(1-1/m+o(1))."
            ),
            "dyadic_consequence": (
                "For fixed m=2^r, true limiting scalar margin is r-1+1/m>0."
            ),
            "scope": (
                "This kills cyclic Hamming-mod-m automata only. Nonabelian dyadic "
                "fibers, growing m, and interleaved leaves are not covered."
            ),
        },
        presentation_controls=presentations,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "classify_all_width_modular_zero_fiber_presentation",
                "resolved": exact,
                "resolution": (
                    "Adjacent m-subset cancellation proves P(U_(m,u))=C_m for every "
                    "u>=m+1; Tietze rows are finite fingerprints only."
                ),
            },
            {
                "obligation": "compute_modular_fiber_density",
                "resolved": exact,
                "resolution": (
                    "The roots-of-unity filter gives exponential convergence to 1/m."
                ),
            },
            {
                "obligation": "falsify_cyclic_dyadic_scalar_saturation",
                "resolved": exact,
                "resolution": (
                    "C_m homomorphisms into S_n have exponent 1-1/m, giving fixed "
                    "positive pressure loss even when m is a power of two."
                ),
            },
            {
                "obligation": "classify_nonabelian_dyadic_automaton_fibers",
                "resolved": False,
                "resolution": (
                    "Search fixed 2-group transition monoids for a free-rank saturation "
                    "with nontrivial target, or prove a bounded torsion/surface gap."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Density 1/2^r and suffix rank r imply scalar saturation.",
                "resolved": True,
                "resolution": (
                    "False for modular fibers: their exact presentation is C_(2^r), "
                    "not a free group of rank r."
                ),
            },
            {
                "objection": "Finite Tietze reductions are being extrapolated in width.",
                "resolved": True,
                "resolution": (
                    "False: the adjacent m-subset proof is symbolic for every u>=m+1."
                ),
            },
            {
                "objection": "A target character could restore the torsion loss.",
                "resolved": True,
                "resolution": (
                    "No normalized character exceeds one in magnitude, so it cannot "
                    "restore missing unsigned homomorphism mass."
                ),
            },
            {
                "objection": "The result eliminates all power-of-two automata.",
                "resolved": True,
                "resolution": (
                    "False: it covers the cyclic Hamming-weight automaton, not arbitrary "
                    "nonabelian 2-group or non-group transition monoids."
                ),
            },
        ],
        headline_metrics={
            "all_width_cyclic_presentation_theorem_count": int(exact),
            "dyadic_modular_no_go_theorem_count": int(exact),
            "checked_modulus_count": len({row.modulus for row in scaling}),
            "minimum_checked_dyadic_true_scalar_margin": min(
                row.true_scalar_pressure_margin for row in dyadic
            ),
            "minimum_limiting_dyadic_true_scalar_margin": min(
                row.limiting_true_scalar_pressure_margin for row in dyadic
            ),
            "nonabelian_dyadic_survivor_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "cyclic_modular_fiber_presentation_classified": exact,
            "cyclic_dyadic_scalar_saturation_falsified": exact,
            "all_dyadic_automata_eliminated": False,
            "nonabelian_dyadic_automata_eliminated": False,
            "growing_modulus_eliminated": False,
            "natural_component_M4_positive": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Fixed cyclic dyadic fibers collapse to C_m and lose scalar mass, but "
                "nonabelian and growing-state dyadic mechanisms remain open."
            ),
        },
        status=(
            "cyclic-dyadic-automaton-route-falsified"
            if exact
            else "cyclic-dyadic-control-failure"
        ),
        summary=(
            "Proved every fixed modular zero fiber is cyclic and used its torsion "
            "exponent to kill the simplest dyadic saturation route."
        ),
        falsifiers_triggered=[
            "The entropy generator count can be grossly loose on dyadic fibers.",
            "Cyclic power-of-two mixing incurs a fixed torsion exponent loss.",
            "Nonabelian dyadic transition structure remains the relevant boundary.",
        ],
    )


def write_dyadic_modular_fiber_torsion_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_dyadic_modular_fiber_torsion_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_dyadic_modular_fiber_torsion_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

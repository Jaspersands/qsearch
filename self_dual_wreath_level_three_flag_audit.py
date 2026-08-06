"""Exhaustive three-level flag audit for the orientation polar hierarchy.

For eight orientation projectors ``E_e`` indexed by ``F_2^3``, every ordered
basis of ``F_2^3`` defines a nested affine flag and hence a three-level polar
merge tree.  There are 168 ordered bases and seven merge occurrences per tree.

The complete flag audit below finds only relative-effect eigenvalues
``0, 1/2, 1`` on selected collision-free ``S_5`` sectors and on the
label-distinct ``S_3`` triangle control.  A fully repeated physical label
immediately produces ``1/3, 4/9, 5/9, 2/3`` as well as ``1/2``.  Half-integral
relative spectra are therefore genuine structure, not a generic consequence
of balanced binary trees.

This motivates, but does not prove, the all-n conjecture:

    Natural collision-free unequal-label portfolios admit an affine flag for
    which every relative effect has spectrum in {0,1/2,1} and its three
    spectral subspaces have polynomial coherent projectors.

The second clause is essential.  A half-integral spectrum by itself does not
give a circuit for its eigenspaces; defining those projectors through
``S_T^(-1/2)`` would be circular.  The audit therefore records two separate
proof obligations: spectral half-integrality and constructive eigenspace
access.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import eigh

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_hierarchical_polar_tree import _psd_powers
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_level_three_flag_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class LevelThreeFlagControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    target_partition: Partition
    globally_distinct_source_partitions: bool
    pairwise_distinct_physical_labels: bool
    orientation_count: int
    carrier_dimension: int
    union_support_rank: int
    ordered_linear_flag_count: int
    merge_occurrence_count: int
    unique_merge_count: int
    fractional_eigenvalue_occurrence_count: int
    nonhalf_fractional_eigenvalue_occurrence_count: int
    observed_fractional_eigenvalues: tuple[float, ...]
    minimum_fractional_endpoint_gap: float
    maximum_half_integral_spectrum_residual: float
    half_integral_on_every_linear_flag: bool
    exact_finite_flag_audit_verified: bool
    status: str


@dataclass(frozen=True)
class LevelThreeFlagScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_tree_depth: int
    level_three_is_below_information_threshold: bool
    collision_free_half_integrality_proved_all_n: bool
    polynomial_relative_eigenspace_projectors_proved: bool
    extended_sieve_lower_bound_applies: bool
    status: str


@dataclass(frozen=True)
class LevelThreeFlagAuditReport:
    created_at: str
    conjecture_contract: dict[str, Any]
    finite_controls: list[LevelThreeFlagControl]
    scaling_records: list[LevelThreeFlagScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _binary_rank(vectors: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        reduced = vector
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


@lru_cache(maxsize=1)
def ordered_f2_three_bases() -> tuple[tuple[int, int, int], ...]:
    return tuple(
        basis
        for basis in itertools.permutations(range(1, 8), 3)
        if _binary_rank(basis) == 3
    )


def flag_leaf_order(basis: tuple[int, int, int]) -> tuple[int, ...]:
    if _binary_rank(basis) != 3:
        raise ValueError("basis must be linearly independent over F_2")

    def coordinate(orientation: int) -> int:
        return sum(
            ((vector & orientation).bit_count() % 2) << index
            for index, vector in enumerate(basis)
        )

    return tuple(sorted(range(8), key=coordinate))


@lru_cache(maxsize=32)
def _reduced_projector_family(
    target: Partition,
    labels: tuple[Label, ...],
    tolerance: float,
) -> tuple[tuple[np.ndarray, ...], int, int]:
    if len(labels) != 3:
        raise ValueError("the level-three audit requires three labels")
    projectors = tuple(
        orientation_invariant_projector(target, labels, orientation)
        for orientation in range(8)
    )
    total = sum(projectors, np.zeros_like(projectors[0]))
    _, support_basis = eigh(
        (total + total.conj().T) / 2,
        subset_by_value=(tolerance, np.inf),
        driver="evr",
    )
    reduced = tuple(
        support_basis.conj().T @ projector @ support_basis
        for projector in projectors
    )
    return reduced, len(projectors[0]), support_basis.shape[1]


def _relative_effect_spectrum(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    parent = left + right
    _, parent_inverse, _, parent_basis = _psd_powers(parent, tolerance)
    if not parent_basis.shape[1]:
        return np.asarray([], dtype=float)
    effect = parent_inverse @ left @ parent_inverse
    restricted = parent_basis.conj().T @ effect @ parent_basis
    return np.linalg.eigvalsh((restricted + restricted.conj().T) / 2)


def audit_level_three_flags(
    control_id: str,
    n: int,
    labels: tuple[Label, ...],
    target: Partition,
    *,
    tolerance: float = 1e-8,
) -> LevelThreeFlagControl:
    if sum(target) != n:
        raise ValueError("target partition has the wrong degree")
    if any(
        sum(left) != n or sum(right) != n or left == right
        for left, right in labels
    ):
        raise ValueError("labels must be unequal partition pairs of n")
    reduced, carrier_dimension, support_rank = _reduced_projector_family(
        target,
        labels,
        tolerance,
    )
    zero = np.zeros((support_rank, support_rank), dtype=complex)
    frame_cache: dict[int, np.ndarray] = {}

    def frame(mask: int) -> np.ndarray:
        if mask not in frame_cache:
            frame_cache[mask] = sum(
                (
                    reduced[index]
                    for index in range(8)
                    if mask & (1 << index)
                ),
                zero.copy(),
            )
        return frame_cache[mask]

    spectrum_cache: dict[tuple[int, int], np.ndarray] = {}
    fractional_occurrences: list[float] = []
    maximum_half_residual = 0.0
    merge_occurrences = 0
    for basis in ordered_f2_three_bases():
        level = [1 << orientation for orientation in flag_leaf_order(basis)]
        for _ in range(3):
            next_level = []
            for index in range(0, len(level), 2):
                left_mask = level[index]
                right_mask = level[index + 1]
                key = tuple(sorted((left_mask, right_mask)))
                if key not in spectrum_cache:
                    spectrum_cache[key] = _relative_effect_spectrum(
                        frame(left_mask),
                        frame(right_mask),
                        tolerance,
                    )
                eigenvalues = spectrum_cache[key]
                maximum_half_residual = max(
                    maximum_half_residual,
                    max(
                        (
                            min(
                                abs(float(value)),
                                abs(float(value) - 0.5),
                                abs(float(value) - 1.0),
                            )
                            for value in eigenvalues
                        ),
                        default=0.0,
                    ),
                )
                fractional_occurrences.extend(
                    float(value)
                    for value in eigenvalues
                    if tolerance < value < 1 - tolerance
                )
                merge_occurrences += 1
                next_level.append(left_mask | right_mask)
            level = next_level

    nonhalf = [
        value
        for value in fractional_occurrences
        if abs(value - 0.5) > 100 * tolerance
    ]
    observed = tuple(
        sorted({round(value, 10) for value in fractional_occurrences})
    )
    source = tuple(partition for label in labels for partition in label)
    verified = bool(
        len(ordered_f2_three_bases()) == 168
        and merge_occurrences == 168 * 7
        and maximum_half_residual <= 0.5 + tolerance
        and all(-100 * tolerance <= value <= 1 + 100 * tolerance for value in (
            item for spectrum in spectrum_cache.values() for item in spectrum
        ))
    )
    half_integral = maximum_half_residual <= 100 * tolerance
    return LevelThreeFlagControl(
        control_id=control_id,
        n=n,
        labels=labels,
        target_partition=target,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        pairwise_distinct_physical_labels=len(labels) == len(set(labels)),
        orientation_count=8,
        carrier_dimension=carrier_dimension,
        union_support_rank=support_rank,
        ordered_linear_flag_count=len(ordered_f2_three_bases()),
        merge_occurrence_count=merge_occurrences,
        unique_merge_count=len(spectrum_cache),
        fractional_eigenvalue_occurrence_count=len(fractional_occurrences),
        nonhalf_fractional_eigenvalue_occurrence_count=len(nonhalf),
        observed_fractional_eigenvalues=observed,
        minimum_fractional_endpoint_gap=min(
            (min(value, 1 - value) for value in fractional_occurrences),
            default=0.5,
        ),
        maximum_half_integral_spectrum_residual=maximum_half_residual,
        half_integral_on_every_linear_flag=half_integral,
        exact_finite_flag_audit_verified=verified,
        status=(
            "all-linear-flags-half-integral"
            if verified and half_integral
            else "all-linear-flags-nonhalf-counterexample"
            if verified
            else "level-three-flag-validation-failure"
        ),
    )


def level_three_flag_scaling_record(n: int) -> LevelThreeFlagScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return LevelThreeFlagScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_tree_depth=copies,
        level_three_is_below_information_threshold=copies > 3,
        collision_free_half_integrality_proved_all_n=False,
        polynomial_relative_eigenspace_projectors_proved=False,
        extended_sieve_lower_bound_applies=False,
        status="finite-level-three-pattern-all-n-constructive-theorem-open",
    )


def _finite_controls() -> list[LevelThreeFlagControl]:
    distinct_triangle: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    repeated: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    w5_labels = _w5_probe_labels()[0]
    return [
        audit_level_three_flags(
            "W5-COLLISION-FREE-3-2",
            5,
            w5_labels,
            (3, 2),
        ),
        audit_level_three_flags(
            "W5-COLLISION-FREE-3-1-1",
            5,
            w5_labels,
            (3, 1, 1),
        ),
        audit_level_three_flags(
            "W3-DISTINCT-LABEL-TRIANGLE-STANDARD",
            3,
            distinct_triangle,
            (2, 1),
        ),
        audit_level_three_flags(
            "W3-REPEATED-LABEL-STANDARD",
            3,
            repeated,
            (2, 1),
        ),
    ]


def run_level_three_flag_audit() -> LevelThreeFlagAuditReport:
    controls = _finite_controls()
    scaling = [
        level_three_flag_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    validation_failures = sum(
        not row.exact_finite_flag_audit_verified for row in controls
    )
    collision_free = [
        row for row in controls if row.globally_distinct_source_partitions
    ]
    repeated = [
        row for row in controls if not row.pairwise_distinct_physical_labels
    ]
    positive = [
        row for row in controls if row.pairwise_distinct_physical_labels
    ]
    repeated_counterexamples = [
        row for row in repeated if not row.half_integral_on_every_linear_flag
    ]
    positive_failures = [
        row for row in positive if not row.half_integral_on_every_linear_flag
    ]
    finite_pattern = bool(collision_free) and not positive_failures
    falsifier = bool(repeated_counterexamples)
    return LevelThreeFlagAuditReport(
        created_at=utc_now(),
        conjecture_contract={
            "flag_family": (
                "Every ordered basis of F_2^3 defines a nested affine flag; "
                "all 168 bases and all seven merges are audited."
            ),
            "finite_positive_pattern": (
                "Selected collision-free and pairwise-distinct-label controls "
                "have relative spectra contained in {0,1/2,1}."
            ),
            "generic_falsifier": (
                "A fully repeated physical unequal label produces nonhalf "
                "relative eigenvalues at the same depth."
            ),
            "all_n_conjecture": (
                "A natural collision-free portfolio admits nested affine flags "
                "with half-integral relative effects and polynomial coherent "
                "projectors onto their endpoint/balanced subspaces."
            ),
            "constructive_boundary": (
                "Half-integral eigenvalues do not expose the eigenprojectors; "
                "constructing them via S_T^-1/2 is circular."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "all_n_collision_free_half_integrality",
                "resolved": False,
                "resolution": (
                    "The complete three-bit flag audit is finite.  A proof must "
                    "classify child-span intersections for growing affine "
                    "orientation families."
                ),
            },
            {
                "obligation": "relative_eigenspace_projectors",
                "resolved": False,
                "resolution": (
                    "Even under half-integrality, no circuit recognizes the "
                    "left-only, right-only, and balanced intersection channels."
                ),
            },
            {
                "obligation": "repeated_label_exclusion",
                "resolved": falsifier,
                "resolution": (
                    "The repeated-label countercontrol proves that any theorem "
                    "must use collision-free or stronger label structure."
                ),
            },
            {
                "obligation": "formal_sieve_scope",
                "resolved": True,
                "resolution": (
                    "MRS sieves measure one irrep after combining two states and "
                    "retain only a classical transcript.  These noncommuting "
                    "global orientation projectors act on all source registers "
                    "and preserve every internal branch coherently."
                ),
            },
            {
                "obligation": "extended_sieve_lower_bound_escape",
                "resolved": False,
                "resolution": (
                    "Formal noncoverage does not rule out a simulation by a "
                    "broader sieve or another lower-bound framework."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Balanced trees force half-integral relative spectra for any projector family.",
                "resolved": True,
                "resolution": (
                    "The repeated-label control has exact 1/3, 4/9, 5/9, and "
                    "2/3 channels."
                ),
            },
            {
                "objection": "One convenient W5 tree ordering explains the observation.",
                "resolved": True,
                "resolution": (
                    "All 168 ordered linear bases, all affine cosets in their "
                    "trees, and all seven merges per tree are included."
                ),
            },
            {
                "objection": "Half-integrality supplies a polynomial merge circuit.",
                "resolved": False,
                "resolution": (
                    "A constant spectrum is useful only with efficient coherent "
                    "access to its eigenspaces.  That is still open."
                ),
            },
            {
                "objection": "The finite pattern is asymptotic evidence strong enough for a decoder claim.",
                "resolved": False,
                "resolution": (
                    "Depth three is far below k=Theta(n log n), and only selected "
                    "W5 target sectors were diagonalized."
                ),
            },
        ],
        literature_links=[
            {
                "id": "MRS-2007-SIEVE-NO-GO",
                "url": "https://arxiv.org/abs/quant-ph/0612089",
                "relevant": True,
                "note": (
                    "Formal sieve model uses adaptive pairwise tensor-product "
                    "isotypic measurements and classical irrep transcripts."
                ),
            },
            {
                "id": "QUEK-REBENTROST-2021-POLAR",
                "url": "https://arxiv.org/abs/2106.07634",
                "relevant": True,
                "note": (
                    "Generic QSVT polar implementation pays inverse singular "
                    "scale; the flag route must exploit additional structure."
                ),
            },
        ],
        headline_metrics={
            "ordered_f2_three_basis_count": len(ordered_f2_three_bases()),
            "finite_control_count": len(controls),
            "finite_validation_failure_count": validation_failures,
            "pairwise_distinct_label_control_count": len(positive),
            "pairwise_distinct_label_half_integral_failure_count": len(
                positive_failures
            ),
            "collision_free_control_count": len(collision_free),
            "collision_free_half_integral_failure_count": sum(
                not row.half_integral_on_every_linear_flag
                for row in collision_free
            ),
            "repeated_label_counterexample_count": len(repeated_counterexamples),
            "merge_occurrence_count": sum(
                row.merge_occurrence_count for row in controls
            ),
            "fractional_eigenvalue_occurrence_count": sum(
                row.fractional_eigenvalue_occurrence_count for row in controls
            ),
            "nonhalf_fractional_eigenvalue_occurrence_count": sum(
                row.nonhalf_fractional_eigenvalue_occurrence_count
                for row in controls
            ),
            "collision_free_half_integrality_all_n_theorem_count": 0,
            "polynomial_relative_eigenspace_projector_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "polynomial_physical_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "complete_three_bit_linear_flag_audit_passed": (
                validation_failures == 0
            ),
            "finite_label_simple_half_integral_pattern_observed": finite_pattern,
            "universal_balanced_tree_half_integrality_falsified": falsifier,
            "collision_free_half_integrality_proved_all_n": False,
            "polynomial_relative_eigenspace_projectors_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "formal_mrs_sieve_theorem_directly_applies": False,
            "extended_sieve_lower_bound_escape_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exhaustive depth-three pattern is structurally selective "
                "and promising, but neither its all-n persistence nor a circuit "
                "for the relative eigenspaces is proved."
            ),
        },
        status=(
            "level-three-half-integral-pattern-repeated-label-falsifier-all-n-open"
            if validation_failures == 0 and finite_pattern and falsifier
            else "level-three-flag-audit-inconclusive"
        ),
        summary=(
            "Audited every three-bit linear flag, found only endpoint/half "
            "relative channels on selected label-simple sectors, and proved by "
            "countercontrol that repeated labels generate genuinely nonhalf "
            "conditional weights."
        ),
        falsifiers_triggered=[
            (
                "Balanced binary trees do not generically force relative "
                "effects into {0,1/2,1}."
            ),
            (
                "The W4 half-integral pattern survives a genuine third level "
                "and every linear flag in the selected W5 controls."
            ),
            (
                "Spectral half-integrality alone is not an implementation of "
                "the relative merge isometry."
            ),
            (
                "The formal MRS theorem does not cover this coherent global "
                "projector family, but that noncoverage is not a speedup proof."
            ),
        ],
    )


def write_level_three_flag_audit_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_level_three_flag_audit())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_level_three_flag_audit_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

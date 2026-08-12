"""Sharp nullity theorem for signed projective-Steiner incidence frames.

Let ``C`` be any real point-line incidence matrix of ``PG(K-1,2)`` whose
three nonzero entries in every line column are signs.  Such a column is the
most general scalar realization of a positive-holonomy line after line gauge.
For every ``K>=3``,

    dim ker(C^T) <= 2.                                    (1)

The proof is local and exact.  If a global kernel had dimension at least
three, its point evaluations would contain three independent vectors.  Their
binary labels cannot lie on one line, so they span an embedded Fano plane.
Every Fano line imposes a signed relation

    +/-p_x +/-p_y +/-p_(x+y) = 0.                         (2)

After naming independent vectors ``p_1,p_2,p_3``, write

    p_12=a p_1+b p_2,  p_13=c p_1+d p_3,
    p_23=e p_2+f p_3,                                    (3)

with all coefficients signs.  The line ``{12,13,23}`` forces

    c e f = -a b d.                                      (4)

Expressing ``p_123`` through the three lines
``{1,23,123}``, ``{2,13,123}``, and ``{3,12,123}`` instead forces

    c e f = a b d,                                       (5)

a contradiction.  Hence every Fano restriction has evaluation rank at most
two, and any three global point evaluations are dependent.  This proves (1).

The ``F_2^2`` quotient signing from the signed-incidence boundary has two
independent kernel vectors, so the bound is sharp at every depth.  Exhaustive
enumeration of all ``4^7`` positive-gauge Fano columns independently confirms
the theorem and gives nullity histogram ``{0:5632,1:8960,2:1792}``.

Consequently an equal-weight scalar full-line frame can lose at most
``2/(2^K-1)`` of its point rank to *exact* zero modes.  This does not bound
near-zero eigenvalues, the pattern-rich subfamily by itself, nonuniform line
weights, or matrix-valued multiplicity transports.  Those qualifications are
essential before drawing any conclusion about the physical PGM.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_random_steiner_gauge_edge import BALANCED_LINE_SIGNS
from self_dual_wreath_signed_steiner_incidence_boundary import (
    projective_points,
    projective_steiner_lines,
    signed_steiner_incidence_with_quotient_kernel,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_signed_steiner_nullity_theorem.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FanoSigningExhaustiveControl:
    signing_count: int
    gauge_class_upper_count: int
    nullity_histogram: dict[str, int]
    maximum_nullity: int
    minimum_third_eigenvalue: float
    maximum_nullity_bound_verified: bool
    sharp_two_dimensional_example_count: int
    status: str


@dataclass(frozen=True)
class SignedSteinerNullityScalingRecord:
    copy_count: int
    point_count: int
    line_count: int
    proved_maximum_nullity: int
    proved_maximum_exact_null_rank_fraction: float
    quotient_witness_rank: int
    quotient_signing_nullity: int
    upper_bound_attained: bool
    status: str


@dataclass(frozen=True)
class RandomSigningNullityControl:
    copy_count: int
    seed: int
    point_count: int
    line_count: int
    observed_rank: int
    observed_nullity: int
    theorem_bound_respected: bool
    status: str


@dataclass(frozen=True)
class SignedSteinerNullityTheoremReport:
    created_at: str
    theorem_contract: dict[str, Any]
    fano_exhaustive_control: FanoSigningExhaustiveControl
    scaling_records: list[SignedSteinerNullityScalingRecord]
    random_controls: list[RandomSigningNullityControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _signed_incidence_from_choices(
    copy_count: int,
    choices: tuple[int, ...],
) -> np.ndarray:
    points = projective_points(copy_count)
    lines = projective_steiner_lines(copy_count)
    if len(choices) != len(lines):
        raise ValueError("one sign choice is required per line")
    point_index = {point: index for index, point in enumerate(points)}
    incidence = np.zeros((len(points), len(lines)), dtype=float)
    for column, (line, choice) in enumerate(zip(lines, choices)):
        rows = [point_index[point] for point in line]
        incidence[rows, column] = BALANCED_LINE_SIGNS[choice]
    return incidence


def audit_all_fano_signings() -> FanoSigningExhaustiveControl:
    line_count = len(projective_steiner_lines(3))
    histogram: Counter[int] = Counter()
    minimum_third = math.inf
    for choices in itertools.product(range(4), repeat=line_count):
        incidence = _signed_incidence_from_choices(3, choices)
        values = np.linalg.eigvalsh(incidence @ incidence.T)
        nullity = int(np.sum(values < 1e-9))
        histogram[nullity] += 1
        minimum_third = min(minimum_third, float(values[2]))
    maximum = max(histogram)
    verified = bool(
        maximum == 2
        and histogram == Counter({0: 5632, 1: 8960, 2: 1792})
        and math.isclose(
            minimum_third,
            3 - math.sqrt(5),
            abs_tol=1e-9,
        )
    )
    return FanoSigningExhaustiveControl(
        signing_count=4**line_count,
        # The Fano incidence graph has cycle rank eight.
        gauge_class_upper_count=2**8,
        nullity_histogram={str(key): histogram[key] for key in sorted(histogram)},
        maximum_nullity=maximum,
        minimum_third_eigenvalue=minimum_third,
        maximum_nullity_bound_verified=verified,
        sharp_two_dimensional_example_count=histogram[2],
        status=(
            "fano-signed-nullity-at-most-two-exhausted"
            if verified
            else "fano-signed-nullity-control-failure"
        ),
    )


def signed_steiner_nullity_scaling_record(
    copy_count: int,
) -> SignedSteinerNullityScalingRecord:
    if copy_count < 3:
        raise ValueError("the Fano restriction theorem requires K>=3")
    incidence, witness = signed_steiner_incidence_with_quotient_kernel(
        copy_count
    )
    witness_rank = int(np.linalg.matrix_rank(witness, tol=1e-9))
    nullity = incidence.shape[0] - int(
        np.linalg.matrix_rank(incidence, tol=1e-9)
    )
    attained = witness_rank == 2 and nullity == 2
    return SignedSteinerNullityScalingRecord(
        copy_count=copy_count,
        point_count=incidence.shape[0],
        line_count=incidence.shape[1],
        proved_maximum_nullity=2,
        proved_maximum_exact_null_rank_fraction=2 / incidence.shape[0],
        quotient_witness_rank=witness_rank,
        quotient_signing_nullity=nullity,
        upper_bound_attained=attained,
        status=(
            "sharp-two-dimensional-nullity-bound-attained"
            if attained
            else "quotient-nullity-sharpness-control-failure"
        ),
    )


def audit_random_signing_nullity(
    copy_count: int,
    seed: int,
) -> RandomSigningNullityControl:
    line_count = len(projective_steiner_lines(copy_count))
    rng = np.random.default_rng(seed)
    choices = tuple(int(value) for value in rng.integers(4, size=line_count))
    incidence = _signed_incidence_from_choices(copy_count, choices)
    rank = int(np.linalg.matrix_rank(incidence, tol=1e-9))
    nullity = incidence.shape[0] - rank
    respected = nullity <= 2
    return RandomSigningNullityControl(
        copy_count=copy_count,
        seed=seed,
        point_count=incidence.shape[0],
        line_count=line_count,
        observed_rank=rank,
        observed_nullity=nullity,
        theorem_bound_respected=respected,
        status=(
            "random-signing-nullity-bound-respected"
            if respected
            else "signed-steiner-nullity-theorem-control-failure"
        ),
    )


def run_signed_steiner_nullity_theorem(
) -> SignedSteinerNullityTheoremReport:
    fano = audit_all_fano_signings()
    scaling = [
        signed_steiner_nullity_scaling_record(copy_count)
        for copy_count in range(3, 9)
    ]
    random_controls = [
        audit_random_signing_nullity(copy_count, seed)
        for copy_count, seed in ((4, 304), (5, 305), (6, 306), (7, 307))
    ]
    failures = int(not fano.maximum_nullity_bound_verified) + sum(
        not row.upper_bound_attained for row in scaling
    ) + sum(not row.theorem_bound_respected for row in random_controls)
    tail = scaling[-1]
    return SignedSteinerNullityTheoremReport(
        created_at=utc_now(),
        theorem_contract={
            "sharp_nullity_bound": (
                "Every real signed point-line incidence matrix of PG(K-1,2) "
                "has left nullity at most two for K>=3."
            ),
            "fano_local_proof": (
                "Three independent kernel evaluations would span a Fano plane; "
                "its seven signed line equations force simultaneously "
                "cef=-abd and cef=abd."
            ),
            "globalization": (
                "Any three binary labels are collinear or lie in a Fano "
                "subspace, so every three kernel evaluation vectors are real-"
                "dependent and the global evaluation rank is at most two."
            ),
            "sharpness": (
                "The first-two-bit quotient construction has an exact rank-two "
                "kernel at every depth."
            ),
            "rank_mass_consequence": (
                "For one equal-weight scalar full-line frame, exact null rank "
                "fraction is at most 2/(2^K-1)."
            ),
        },
        fano_exhaustive_control=fano,
        scaling_records=scaling,
        random_controls=random_controls,
        proof_obligations=[
            {
                "obligation": "classify_exact_scalar_nullity_all_depth",
                "resolved": failures == 0,
                "resolution": (
                    "The Fano sign contradiction proves the universal upper "
                    "bound and the F_2^2 quotient attains it."
                ),
            },
            {
                "obligation": "bound_exact_scalar_bad_rank_mass",
                "resolved": True,
                "resolution": (
                    "A single full-line scalar channel loses at most two of "
                    "2^K-1 point directions."
                ),
            },
            {
                "obligation": "bound_near_null_scalar_spectrum",
                "resolved": False,
                "resolution": (
                    "Rank rigidity does not exclude a growing collection of "
                    "small positive eigenvalues."
                ),
            },
            {
                "obligation": "sum_bad_rank_over_natural_carrier_channels",
                "resolved": False,
                "resolution": (
                    "Overlapping carrier sectors and nonuniform physical weights "
                    "prevent multiplying the per-channel bound naively."
                ),
            },
            {
                "obligation": "extend_nullity_rigidity_to_matrix_transport",
                "resolved": False,
                "resolution": (
                    "Orthogonal multiplicity transports can support higher-rank "
                    "flat sections not covered by the scalar Fano argument."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The signed quotient counterexample can have extensive scalar nullity.",
                "resolved": True,
                "resolution": (
                    "False for the full projective line family: two is the exact "
                    "maximum at every depth."
                ),
            },
            {
                "objection": "The theorem is only a K=3 enumeration.",
                "resolved": True,
                "resolution": (
                    "Every three global evaluation vectors lie in a line or an "
                    "embedded Fano plane, which globalizes the analytic contradiction."
                ),
            },
            {
                "objection": "Vanishing exact null fraction proves a spectral edge.",
                "resolved": False,
                "resolution": (
                    "It does not control near-zero eigenvalues or weighted PGM "
                    "mass and therefore is not a condition-number theorem."
                ),
            },
            {
                "objection": "The rich subfamily inherits the nullity-two bound.",
                "resolved": False,
                "resolution": (
                    "Deleting non-rich lines creates isolated points and removes "
                    "the embedded-Fano constraints used by the proof."
                ),
            },
        ],
        headline_metrics={
            "fano_signing_count": fano.signing_count,
            "fano_maximum_nullity": fano.maximum_nullity,
            "scaling_control_count": len(scaling),
            "random_control_count": len(random_controls),
            "finite_control_failure_count": failures,
            "tail_copy_count": tail.copy_count,
            "tail_maximum_exact_null_rank_fraction": (
                tail.proved_maximum_exact_null_rank_fraction
            ),
            "sharp_scalar_nullity_theorem_count": 1,
            "near_null_spectral_edge_theorem_count": 0,
            "matrix_transport_nullity_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "scalar_full_line_nullity_at_most_two": failures == 0,
            "scalar_nullity_bound_sharp": failures == 0,
            "exact_scalar_null_rank_fraction_vanishes": failures == 0,
            "near_null_scalar_mass_controlled": False,
            "natural_weighted_channel_sum_controlled": False,
            "matrix_valued_flat_sections_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact scalar kernels are rigid and negligible per channel, "
                "but near-kernel and matrix-valued weighted traffic remain open."
            ),
        },
        status="sharp-scalar-nullity-two-proved-near-kernel-open",
        summary=(
            "Proved that every positive-holonomy scalar signing of the full "
            "projective-Steiner frame has at most two exact null modes, with "
            "the quotient construction attaining the bound."
        ),
        falsifiers_triggered=[
            (
                "The adversarial scalar kernel cannot occupy a constant fraction "
                "of one full-line carrier channel."
            ),
            (
                "Exact scalar singularity is too low-rank by itself to establish "
                "a macroscopic PGM obstruction."
            ),
            (
                "The next obstruction must use near-zero spectral mass, omitted "
                "lines, nonuniform weights, or matrix-valued flat sections."
            ),
        ],
    )


def write_signed_steiner_nullity_theorem_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_signed_steiner_nullity_theorem())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_signed_steiner_nullity_theorem_report()
    print(json.dumps(report, indent=2, sort_keys=True))

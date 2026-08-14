"""Adaptive sign syndrome as variance of unsigned tetrahedral channels.

Fix a six-label sign-orbit tuple with no self-conjugate orbit and use the
physical coefficient-axis order ``(gk,ghk,hk,g,h,k)``.  For each input action
``a in {g,h,k}``, let ``P_a^0`` and ``P_a^1`` be its trivial and sign
isotypic projectors.  Define the eight unsigned tetrahedral amplitudes

    A_y = Tr(P_g^(y_g) P_h^(y_h) P_k^(y_k)),  y in F_2^3. (1)

Although a generic trace of three projections need not be nonnegative, these
particular traces are: expanding the projectors identifies

    A_y = (product_i d_i)/|S_n|^3 L_O(z_y),               (2)

where ``L_O(z_y)`` is one physical oriented likelihood with syndrome ``y``.
Thus ``A_y>=0``.

The signed traces from the companion projector reduction are exactly the
Walsh transform

    T_x = Tr(J_g(x_g)J_h(x_h)J_k(x_k))
        = sum_y (-1)^(x dot y) A_y.                       (3)

Since the coarse Plancherel factors cancel tuplewise,

    Q(O) F_x(O)^2 = T_x^2.                                (4)

When ``T_0>0``, the orbit-adaptive syndrome channel is simply

    Pr(Y=y|O)=A_y/T_0,       T_0=sum_y A_y.               (5)

Parseval now gives both the absolute and relative targets:

    sum_(x!=0) QF_x^2 = 8 sum_y (A_y-T_0/8)^2,            (6)

    chi^2(P_(Y|O)||U_3)
      =sum_(x!=0)(T_x/T_0)^2
      =8 sum_y(A_y/T_0-1/8)^2.                            (7)

This removes signed cancellation from the final formulation: adaptive
decoupling is equivalent to equidistribution of eight positive recoupling
channels on physical mass.

Marginal and pairwise data cannot prove that equidistribution.  On a
four-dimensional coordinate space indexed by the even-parity subset of
``F_2^3``, let ``P_a^b`` select coordinates whose ``a`` bit equals ``b``.
Every projector has rank two and every pair intersection has trace one,
exactly matching three independent fair bits.  Yet (1) is one on the four
even triples and zero on the four odd triples, so the conditional chi-square
is one and only the ``x=(1,1,1)`` Walsh mode survives.  This is an exact
three-way-synergy falsifier for every marginal-rank or pair-angle proof.

The remaining theorem must control a genuinely tetrahedral/6j three-projector
correlation, not ranks, pairwise angles, or local measured marginals.  No
canonical decay, survival, algorithm, or speedup is proved here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_projector_orbit_variance.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-PROJECTOR-ORBIT-VARIANCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

BitVector = tuple[int, int, int]
BITS = tuple(itertools.product((0, 1), repeat=3))


@dataclass(frozen=True)
class OrbitVarianceControl:
    control_id: str
    n: int
    orbit_indices: tuple[int, ...]
    orbit_representatives: tuple[tuple[int, ...], ...]
    dimensions: tuple[int, ...]
    unsigned_channel_amplitudes: tuple[float, ...]
    minimum_unsigned_amplitude: float
    total_unsigned_amplitude: float
    conditional_syndrome_probabilities: tuple[float, ...]
    probability_sum_residual: float
    signed_projector_traces: tuple[float, ...]
    maximum_walsh_reconstruction_residual: float
    conditional_chi_square_from_probabilities: float
    conditional_chi_square_from_signed_traces: float
    conditional_chi_square_residual: float
    absolute_nonzero_sector_energy: float
    absolute_variance_energy: float
    absolute_variance_residual: float
    exact_orbit_variance_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class PairwiseFlatSynergyControl:
    ambient_dimension: int
    projector_rank: int
    maximum_rank_residual: float
    target_pair_intersection_trace: float
    maximum_pair_intersection_residual: float
    unsigned_channel_amplitudes: tuple[float, ...]
    conditional_syndrome_probabilities: tuple[float, ...]
    surviving_nonzero_walsh_modes: tuple[BitVector, ...]
    conditional_chi_square: float
    all_marginals_uniform: bool
    all_pairs_uniform: bool
    triple_channel_uniform: bool
    exact_pairwise_flat_triple_synergy_verified: bool
    status: str


@dataclass(frozen=True)
class ParityProjectorOrbitVarianceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    orbit_controls: list[OrbitVarianceControl]
    synergy_counterexample: PairwiseFlatSynergyControl
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def walsh_transform(values: tuple[float, ...]) -> tuple[float, ...]:
    if len(values) != 8:
        raise ValueError("eight F_2^3 values are required")
    return tuple(
        sum(
            (-1) ** sum(left * right for left, right in zip(frequency, point))
            * value
            for point, value in zip(BITS, values)
        )
        for frequency in BITS
    )


def inverse_walsh_transform(values: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(value / 8.0 for value in walsh_transform(values))


def conditional_chi_square(probabilities: tuple[float, ...]) -> float:
    if len(probabilities) != 8:
        raise ValueError("eight probabilities are required")
    if min(probabilities) < -1e-12 or abs(sum(probabilities) - 1.0) > 1e-9:
        raise ValueError("values must form a probability distribution")
    return 8.0 * sum((value - 1.0 / 8.0) ** 2 for value in probabilities)


def audit_orbit_variance(
    control_id: str,
    n: int,
    orbit_indices: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> OrbitVarianceControl:
    if len(orbit_indices) != 6:
        raise ValueError("six orbit indices are required")
    orbits, arrays = parity_coset_word_likelihood_arrays(n)
    if any(index < 0 or index >= len(orbits) for index in orbit_indices):
        raise ValueError("orbit index is out of range")
    selected = tuple(orbits[index] for index in orbit_indices)
    if any(len(orbit) != 2 for orbit in selected):
        raise ValueError("the variance normal form requires non-self-conjugate orbits")
    dimensions = tuple(hook_length_dimension(orbit[0]) for orbit in selected)
    order = math.factorial(n)
    scale = math.prod(dimensions) / (order / 2.0) ** 3
    signed = tuple(float(arrays[frequency][orbit_indices]) * scale for frequency in BITS)
    unsigned = inverse_walsh_transform(signed)
    reconstructed = walsh_transform(unsigned)
    walsh_residual = max(
        abs(left - right) for left, right in zip(signed, reconstructed)
    )
    total = sum(unsigned)
    probabilities = (
        tuple(value / total for value in unsigned)
        if total > tolerance
        else (1.0 / 8.0,) * 8
    )
    probability_residual = abs(sum(probabilities) - 1.0)
    chi_probability = conditional_chi_square(probabilities)
    chi_signed = (
        sum(value * value for value in signed[1:]) / (signed[0] * signed[0])
        if abs(signed[0]) > tolerance
        else 0.0
    )
    chi_residual = abs(chi_probability - chi_signed)
    absolute_fourier = sum(value * value for value in signed[1:])
    mean = total / 8.0
    absolute_variance = 8.0 * sum((value - mean) ** 2 for value in unsigned)
    variance_residual = abs(absolute_fourier - absolute_variance)
    exact = bool(
        min(unsigned) >= -tolerance
        and probability_residual <= tolerance
        and walsh_residual <= tolerance
        and chi_residual <= tolerance
        and variance_residual <= tolerance
    )
    return OrbitVarianceControl(
        control_id=control_id,
        n=n,
        orbit_indices=orbit_indices,
        orbit_representatives=tuple(orbit[0] for orbit in selected),
        dimensions=dimensions,
        unsigned_channel_amplitudes=unsigned,
        minimum_unsigned_amplitude=min(unsigned),
        total_unsigned_amplitude=total,
        conditional_syndrome_probabilities=probabilities,
        probability_sum_residual=probability_residual,
        signed_projector_traces=signed,
        maximum_walsh_reconstruction_residual=walsh_residual,
        conditional_chi_square_from_probabilities=chi_probability,
        conditional_chi_square_from_signed_traces=chi_signed,
        conditional_chi_square_residual=chi_residual,
        absolute_nonzero_sector_energy=absolute_fourier,
        absolute_variance_energy=absolute_variance,
        absolute_variance_residual=variance_residual,
        exact_orbit_variance_normal_form_verified=exact,
        status=(
            "adaptive-syndrome-is-unsigned-projector-channel-variance"
            if exact
            else "orbit-projector-variance-control-failure"
        ),
    )


def pairwise_flat_synergy_counterexample(
    *,
    tolerance: float = 1e-10,
) -> PairwiseFlatSynergyControl:
    support = tuple(point for point in BITS if sum(point) % 2 == 0)
    projectors: dict[tuple[int, int], np.ndarray] = {}
    for coordinate in range(3):
        for bit in (0, 1):
            projectors[coordinate, bit] = np.diag(
                [float(point[coordinate] == bit) for point in support]
            )
    ranks = tuple(float(np.trace(projectors[key])) for key in sorted(projectors))
    rank_residual = max(abs(rank - 2.0) for rank in ranks)
    pair_residual = max(
        abs(
            float(np.trace(projectors[left, a] @ projectors[right, b]))
            - 1.0
        )
        for left in range(3)
        for right in range(left + 1, 3)
        for a in (0, 1)
        for b in (0, 1)
    )
    amplitudes = tuple(
        float(
            np.trace(
                projectors[0, point[0]]
                @ projectors[1, point[1]]
                @ projectors[2, point[2]]
            )
        )
        for point in BITS
    )
    total = sum(amplitudes)
    probabilities = tuple(value / total for value in amplitudes)
    signed = walsh_transform(amplitudes)
    surviving = tuple(
        frequency
        for frequency, value in zip(BITS[1:], signed[1:])
        if abs(value) > tolerance
    )
    chi = conditional_chi_square(probabilities)
    uniform_marginals = rank_residual <= tolerance
    uniform_pairs = pair_residual <= tolerance
    triple_uniform = max(probabilities) - min(probabilities) <= tolerance
    exact = bool(
        uniform_marginals
        and uniform_pairs
        and not triple_uniform
        and surviving == ((1, 1, 1),)
        and abs(chi - 1.0) <= tolerance
    )
    return PairwiseFlatSynergyControl(
        ambient_dimension=4,
        projector_rank=2,
        maximum_rank_residual=rank_residual,
        target_pair_intersection_trace=1.0,
        maximum_pair_intersection_residual=pair_residual,
        unsigned_channel_amplitudes=amplitudes,
        conditional_syndrome_probabilities=probabilities,
        surviving_nonzero_walsh_modes=surviving,
        conditional_chi_square=chi,
        all_marginals_uniform=uniform_marginals,
        all_pairs_uniform=uniform_pairs,
        triple_channel_uniform=triple_uniform,
        exact_pairwise_flat_triple_synergy_verified=exact,
        status=(
            "pairwise-flat-projectors-retain-pure-three-way-parity-synergy"
            if exact
            else "pairwise-flat-synergy-control-failure"
        ),
    )


def _default_orbit_controls() -> list[OrbitVarianceControl]:
    controls = []
    for n in (4, 5):
        orbits, _arrays = parity_coset_word_likelihood_arrays(n)
        retained = tuple(
            index
            for index, orbit in enumerate(orbits)
            if len(orbit) == 2 and hook_length_dimension(orbit[0]) > 1
        )
        if not retained:
            continue
        tuples = [
            (retained[0],) * 6,
            (retained[-1],) * 6,
        ]
        if len(retained) > 1:
            tuples.extend(
                [
                    tuple(retained[index % len(retained)] for index in range(6)),
                    tuple(retained[(index // 2) % len(retained)] for index in range(6)),
                ]
            )
        for index, orbit_tuple in enumerate(dict.fromkeys(tuples)):
            controls.append(
                audit_orbit_variance(f"S{n}-PAIRED-{index}", n, orbit_tuple)
            )
    return controls


def run_parity_projector_orbit_variance(
) -> ParityProjectorOrbitVarianceReport:
    controls = _default_orbit_controls()
    counterexample = pairwise_flat_synergy_counterexample()
    failures = sum(
        not control.exact_orbit_variance_normal_form_verified
        for control in controls
    ) + int(not counterexample.exact_pairwise_flat_triple_synergy_verified)
    verified = failures == 0
    positive_controls = sum(
        control.conditional_chi_square_from_probabilities > 1e-12
        for control in controls
    )
    return ParityProjectorOrbitVarianceReport(
        created_at=utc_now(),
        theorem_contract={
            "unsigned_channels": (
                "A_y=Tr(P_g^yg P_h^yh P_k^yk)>=0 and equals the physical "
                "oriented likelihood times product(d_i)/|S_n|^3."
            ),
            "walsh_relation": (
                "T_x=sum_y(-1)^(x dot y)A_y, with Q(O)F_x(O)^2=T_x^2."
            ),
            "conditional_channel": "P(Y=y|O)=A_y/sum_z A_z.",
            "variance_identity": (
                "sum_(x!=0)T_x^2=8sum_y(A_y-mean(A))^2."
            ),
            "relative_identity": (
                "chi2(P_(Y|O)||U3)=8sum_y(A_y/T0-1/8)^2."
            ),
            "pairwise_no_go": (
                "uniform ranks and every pair intersection do not control the "
                "eight triple overlaps; an even-parity coordinate model has chi2=1."
            ),
            "scope": (
                "This is a positive-channel normal form and proof-strategy no-go, "
                "not a canonical asymptotic estimate or algorithm."
            ),
        },
        orbit_controls=controls,
        synergy_counterexample=counterexample,
        proof_obligations=[
            {
                "obligation": "convert_signed_projector_traces_to_positive_channels",
                "resolved": verified,
                "resolution": (
                    "Inverse Walsh transform identifies the eight traces with scaled "
                    "physical oriented likelihoods."
                ),
            },
            {
                "obligation": "identify_adaptive_chi_square_with_channel_variance",
                "resolved": verified,
                "resolution": "Walsh Parseval gives the exact absolute and relative identities.",
            },
            {
                "obligation": "test_marginal_and_pairwise_projector_control",
                "resolved": verified,
                "resolution": (
                    "The even-parity four-atom construction has exactly flat one- and "
                    "two-coordinate data but pure three-way syndrome information."
                ),
            },
            {
                "obligation": "prove_canonical_eight_channel_equidistribution_or_survival",
                "resolved": False,
                "resolution": (
                    "Estimate a true tetrahedral/6j three-projector cumulant on the "
                    "canonical high-dimensional Plancherel sector."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A trace of three projections is automatically nonnegative.",
                "resolved": True,
                "resolution": (
                    "False in general; positivity here follows specifically from the "
                    "physical likelihood identity, not abstract projector algebra."
                ),
            },
            {
                "objection": "Asymptotically flat pairwise 6j marginals imply full mixing.",
                "resolved": True,
                "resolution": (
                    "The exact even-parity counterexample has every pair flat and a "
                    "unit conditional chi-square in the triple channel."
                ),
            },
            {
                "objection": "Positive S5 channel variance proves survival.",
                "resolved": False,
                "resolution": (
                    "It is a finite control only; both amplitudes and the source law "
                    "change with n."
                ),
            },
        ],
        headline_metrics={
            "positive_channel_variance_normal_form_theorem_count": int(verified),
            "pairwise_flat_triple_synergy_counterexample_count": int(verified),
            "finite_orbit_control_count": len(controls),
            "finite_positive_chi_square_control_count": positive_controls,
            "finite_control_failure_count": failures,
            "maximum_walsh_reconstruction_residual": max(
                control.maximum_walsh_reconstruction_residual for control in controls
            ),
            "maximum_variance_identity_residual": max(
                control.absolute_variance_residual for control in controls
            ),
            "counterexample_conditional_chi_square": counterexample.conditional_chi_square,
            "canonical_channel_equidistribution_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "adaptive_channel_is_positive_projector_trace_law": verified,
            "adaptive_chi_square_is_exact_channel_variance": verified,
            "marginal_rank_proof_strategy_sufficient": False,
            "pairwise_angle_proof_strategy_sufficient": False,
            "genuine_tetrahedral_cumulant_required": True,
            "canonical_adaptive_syndrome_decouples_proved": False,
            "canonical_adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The signed target is now positive eight-channel equidistribution, "
                "but pairwise data cannot control its genuine three-way cumulant."
            ),
        },
        status=(
            "adaptive-syndrome-is-positive-tetrahedral-channel-variance"
            if verified
            else "parity-projector-orbit-variance-control-failure"
        ),
        summary=(
            "Identified orbit-adaptive syndrome information with variance among "
            "eight positive projector channels and proved pairwise flatness insufficient."
        ),
        falsifiers_triggered=[
            "Triple-projection positivity is representation-specific, not a generic PSD fact.",
            "Uniform projector ranks cannot control adaptive syndrome information.",
            "Even complete pairwise overlap flatness cannot control the tetrahedral channel.",
            "The next bound must address a genuine three-way 6j cumulant.",
        ],
    )


def write_parity_projector_orbit_variance_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_projector_orbit_variance())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_projector_orbit_variance_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

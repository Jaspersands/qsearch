"""Split adaptive parity information into Racah rank and arithmetic terms.

The positive-channel reduction writes the eight orbit-adaptive syndrome
amplitudes as

    A_y = Tr(P_g^(y_g) P_h^(y_h) P_k^(y_k)).

In the physical coefficient-axis order

    (alpha,beta,gamma,mu,nu,lambda) = (gk,ghk,hk,g,h,k),

the physical recoupling law identifies these amplitudes with normalized
symmetric-group 6j block masses,

    A_y = ||R_(mu,nu)||_HS^2 / (d_mu d_nu).                 (1)

For the orientation selected by syndrome ``y``, define the row and column
multiplicities

    l_y = g(alpha,beta,mu) g(mu,gamma,lambda),
    r_y = g(beta,gamma,nu) g(alpha,nu,lambda),

and the common total multiplicity

    M_y = sum_eta g(alpha,beta,eta) g(eta,gamma,lambda)
        = sum_eta g(beta,gamma,eta) g(alpha,eta,lambda).

If the ``M_y`` dimensional recoupling matrix were Haar orthogonal, the mean
block mass would give the rank-profile benchmark

    H_y = l_y r_y / (M_y d_mu d_nu).                        (2)

Set ``E_y=A_y-H_y``.  For the centered seminorm

    N(v)^2 = 8 sum_y (v_y-mean(v))^2,

the exact adaptive energy decomposition is

    N(A)^2 = N(H)^2 + N(E)^2 + 16 <C H,C E>,                (3)

and Minkowski gives

    |N(H)-N(E)| <= N(A) <= N(H)+N(E).                       (4)

Equations (1)--(4) separate two asymptotic obligations that previous rank-only
arguments conflated: equidistribution of Kronecker multiplicity profiles and
control of deterministic non-Haar 6j arithmetic.  They also expose a third
issue, their centered alignment.  At ``S_4`` the natural channel can be exactly
flat while the rank profile and arithmetic residual are both nonflat and
perfectly anticorrelated.  At ``S_5`` there are controls in which the arithmetic
residual dominates the rank profile.  Therefore neither a nonuniform Haar mean
nor a flat Haar mean decides the natural channel.

For comparison only, a real Haar ``M x M`` orthogonal matrix has

    Var ||R_(mu,nu)||_HS^2
      = 2 l r (M-l)(M-r) / [M^2(M-1)(M+2)].                 (5)

This is a falsifiable null benchmark, not a stochastic model for natural
symmetric-group 6j symbols.  No canonical asymptotic bound, adaptive survival,
algorithm, or speedup is proved here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from self_dual_wreath_parity_projector_orbit_variance import (
    BITS,
    audit_orbit_variance,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    kronecker_multiplicity,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    orientation_syndrome,
    transpose_partition,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_racah_rank_residual_decomposition.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-RANK-RESIDUAL-DECOMPOSITION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Orientation = tuple[int, int, int, int, int, int]
Syndrome = tuple[int, int, int]
ORIENTATIONS: tuple[Orientation, ...] = tuple(
    itertools.product((0, 1), repeat=6)
)


@dataclass(frozen=True)
class AxisMappingSupportControl:
    n: int
    positive_likelihood_entry_count: int
    direct_mapping_unsupported_positive_count: int
    maximum_direct_mapping_unsupported_likelihood: float
    dual_geometric_mapping_unsupported_positive_count: int
    maximum_dual_geometric_mapping_unsupported_likelihood: float
    direct_coefficient_axis_mapping_verified: bool
    competing_dual_mapping_rejected: bool
    status: str


@dataclass(frozen=True)
class RacahChannelProfile:
    syndrome: Syndrome
    orientation_representative: Orientation
    left_block_rank: int
    right_block_rank: int
    total_multiplicity_dimension: int
    intermediate_dimensions: tuple[int, int]
    natural_normalized_block_mass: float
    haar_rank_profile_benchmark: float
    nonhaar_arithmetic_residual: float
    normalized_haar_block_variance: float
    orientation_fiber_profile_invariant: bool
    maximum_orientation_fiber_amplitude_residual: float
    forbidden_support_amplitude_residual: float


@dataclass(frozen=True)
class RacahRankResidualControl:
    control_id: str
    n: int
    orbit_indices: tuple[int, ...]
    orbit_representatives: tuple[Partition, ...]
    channels: tuple[RacahChannelProfile, ...]
    natural_centered_energy: float
    haar_rank_profile_centered_energy: float
    nonhaar_residual_centered_energy: float
    rank_residual_centered_cross_term: float
    variance_decomposition_residual: float
    centered_alignment_cosine: float
    minkowski_lower_bound: float
    minkowski_upper_bound: float
    minkowski_violation: float
    total_natural_amplitude: float
    conditional_syndrome_chi_square: float
    rank_profile_relative_scale: float
    nonhaar_residual_relative_scale: float
    independent_haar_null_energy_upper_benchmark: float
    maximum_forbidden_support_amplitude_residual: float
    maximum_orientation_fiber_amplitude_residual: float
    all_orientation_fusion_profiles_invariant: bool
    all_fusion_associativity_identities_verified: bool
    exact_rank_residual_decomposition_verified: bool
    finite_mechanism_diagnosis: str
    status: str


@dataclass(frozen=True)
class ParityRacahRankResidualReport:
    created_at: str
    theorem_contract: dict[str, Any]
    axis_mapping_controls: list[AxisMappingSupportControl]
    orbit_controls: list[RacahRankResidualControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def centered_energy(values: Iterable[float]) -> float:
    entries = tuple(float(value) for value in values)
    if len(entries) != 8:
        raise ValueError("eight syndrome-channel values are required")
    mean = sum(entries) / 8.0
    return 8.0 * sum((value - mean) ** 2 for value in entries)


def centered_cross_energy(
    left: Iterable[float],
    right: Iterable[float],
) -> float:
    first = tuple(float(value) for value in left)
    second = tuple(float(value) for value in right)
    if len(first) != 8 or len(second) != 8:
        raise ValueError("eight syndrome-channel values are required")
    first_mean = sum(first) / 8.0
    second_mean = sum(second) / 8.0
    return 8.0 * sum(
        (a - first_mean) * (b - second_mean)
        for a, b in zip(first, second)
    )


def haar_block_mass_variance(total: int, rows: int, columns: int) -> float:
    """Variance of an ``rows x columns`` block mass in Haar ``O(total)``."""

    if total < 0 or not 0 <= rows <= total or not 0 <= columns <= total:
        raise ValueError("block ranks must lie between zero and total")
    if total <= 1 or rows in (0, total) or columns in (0, total):
        return 0.0
    return (
        2.0
        * rows
        * columns
        * (total - rows)
        * (total - columns)
        / (total * total * (total - 1) * (total + 2))
    )


def _oriented_partitions(
    base: tuple[Partition, ...],
    orientation: Orientation,
) -> tuple[Partition, ...]:
    if len(base) != 6:
        raise ValueError("six base partitions are required")
    return tuple(
        transpose_partition(partition) if bit else partition
        for partition, bit in zip(base, orientation)
    )


def _fusion_profile(
    labels: tuple[Partition, ...],
) -> tuple[int, int, int, int, int, int]:
    """Return ``(l,r,M_left,M_right,d_mu,d_nu)`` in physical axis order."""

    if len(labels) != 6:
        raise ValueError("six physical labels are required")
    alpha, beta, gamma, mu, nu, lam = labels
    partitions = tuple(integer_partitions(sum(alpha)))
    left_rank = kronecker_multiplicity(
        alpha, beta, mu
    ) * kronecker_multiplicity(mu, gamma, lam)
    right_rank = kronecker_multiplicity(
        beta, gamma, nu
    ) * kronecker_multiplicity(alpha, nu, lam)
    left_total = sum(
        kronecker_multiplicity(alpha, beta, eta)
        * kronecker_multiplicity(eta, gamma, lam)
        for eta in partitions
    )
    right_total = sum(
        kronecker_multiplicity(beta, gamma, eta)
        * kronecker_multiplicity(alpha, eta, lam)
        for eta in partitions
    )
    return (
        left_rank,
        right_rank,
        left_total,
        right_total,
        hook_length_dimension(mu),
        hook_length_dimension(nu),
    )


def _mapping_is_supported(
    labels: tuple[Partition, ...],
    mapping: tuple[int, ...],
) -> bool:
    alpha, beta, gamma, mu, nu, lam = tuple(labels[index] for index in mapping)
    return bool(
        kronecker_multiplicity(alpha, beta, mu)
        and kronecker_multiplicity(mu, gamma, lam)
        and kronecker_multiplicity(beta, gamma, nu)
        and kronecker_multiplicity(alpha, nu, lam)
    )


def audit_axis_mapping_support(
    n: int,
    *,
    tolerance: float = 1e-9,
) -> AxisMappingSupportControl:
    """Check the implemented table convention against both tetrahedral duals."""

    partitions, likelihood, _product, _physical = finite_physical_likelihood_arrays(n)
    direct = (0, 1, 2, 3, 4, 5)
    competing_dual = (4, 5, 3, 2, 0, 1)
    direct_bad = 0
    direct_max = 0.0
    dual_bad = 0
    dual_max = 0.0
    positive_count = 0
    for indices in np.ndindex(likelihood.shape):
        value = float(likelihood[indices])
        if value <= tolerance:
            continue
        positive_count += 1
        labels = tuple(partitions[index] for index in indices)
        if not _mapping_is_supported(labels, direct):
            direct_bad += 1
            direct_max = max(direct_max, value)
        if not _mapping_is_supported(labels, competing_dual):
            dual_bad += 1
            dual_max = max(dual_max, value)
    direct_verified = direct_bad == 0
    dual_rejected = dual_bad > 0
    return AxisMappingSupportControl(
        n=n,
        positive_likelihood_entry_count=positive_count,
        direct_mapping_unsupported_positive_count=direct_bad,
        maximum_direct_mapping_unsupported_likelihood=direct_max,
        dual_geometric_mapping_unsupported_positive_count=dual_bad,
        maximum_dual_geometric_mapping_unsupported_likelihood=dual_max,
        direct_coefficient_axis_mapping_verified=direct_verified,
        competing_dual_mapping_rejected=dual_rejected,
        status=(
            "direct-physical-axis-order-verified-and-dual-rejected"
            if direct_verified and dual_rejected
            else "tetrahedral-axis-mapping-control-failure"
        ),
    )


def audit_racah_rank_residual(
    control_id: str,
    n: int,
    orbit_indices: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> RacahRankResidualControl:
    if len(orbit_indices) != 6:
        raise ValueError("six orbit indices are required")
    orbits, _arrays = parity_coset_word_likelihood_arrays(n)
    if any(index < 0 or index >= len(orbits) for index in orbit_indices):
        raise ValueError("orbit index is out of range")
    selected = tuple(orbits[index] for index in orbit_indices)
    if any(len(orbit) != 2 for orbit in selected):
        raise ValueError("rank-residual controls require non-self-conjugate orbits")
    base = tuple(orbit[0] for orbit in selected)
    dimensions = tuple(hook_length_dimension(partition) for partition in base)
    order = math.factorial(n)
    amplitude_scale = math.prod(dimensions) / order**3
    partitions, likelihood, _product, _physical = finite_physical_likelihood_arrays(n)
    partition_index = {partition: index for index, partition in enumerate(partitions)}
    natural = audit_orbit_variance(
        control_id,
        n,
        orbit_indices,
        tolerance=tolerance,
    ).unsigned_channel_amplitudes

    channels: list[RacahChannelProfile] = []
    associativity_verified = True
    for syndrome, natural_amplitude in zip(BITS, natural):
        fiber = tuple(
            orientation
            for orientation in ORIENTATIONS
            if orientation_syndrome(orientation) == syndrome
        )
        profiles = tuple(
            _fusion_profile(_oriented_partitions(base, orientation))
            for orientation in fiber
        )
        profile = profiles[0]
        profile_invariant = all(row == profile for row in profiles)
        left_rank, right_rank, left_total, right_total, d_mu, d_nu = profile
        associativity_verified &= left_total == right_total
        total = left_total
        benchmark = (
            left_rank * right_rank / (total * d_mu * d_nu)
            if total
            else 0.0
        )
        normalized_haar_variance = (
            haar_block_mass_variance(total, left_rank, right_rank)
            / (d_mu * d_nu) ** 2
            if total
            else 0.0
        )
        fiber_amplitudes = []
        for orientation in fiber:
            oriented = _oriented_partitions(base, orientation)
            indices = tuple(partition_index[label] for label in oriented)
            fiber_amplitudes.append(amplitude_scale * float(likelihood[indices]))
        fiber_residual = max(
            abs(value - natural_amplitude) for value in fiber_amplitudes
        )
        forbidden_residual = (
            abs(natural_amplitude) if left_rank * right_rank == 0 else 0.0
        )
        channels.append(
            RacahChannelProfile(
                syndrome=syndrome,
                orientation_representative=fiber[0],
                left_block_rank=left_rank,
                right_block_rank=right_rank,
                total_multiplicity_dimension=total,
                intermediate_dimensions=(d_mu, d_nu),
                natural_normalized_block_mass=natural_amplitude,
                haar_rank_profile_benchmark=benchmark,
                nonhaar_arithmetic_residual=natural_amplitude - benchmark,
                normalized_haar_block_variance=normalized_haar_variance,
                orientation_fiber_profile_invariant=profile_invariant,
                maximum_orientation_fiber_amplitude_residual=fiber_residual,
                forbidden_support_amplitude_residual=forbidden_residual,
            )
        )

    haar = tuple(row.haar_rank_profile_benchmark for row in channels)
    residual = tuple(row.nonhaar_arithmetic_residual for row in channels)
    natural_energy = centered_energy(natural)
    haar_energy = centered_energy(haar)
    residual_energy = centered_energy(residual)
    cross = centered_cross_energy(haar, residual)
    decomposition_residual = abs(
        natural_energy - (haar_energy + residual_energy + 2.0 * cross)
    )
    natural_norm = math.sqrt(max(0.0, natural_energy))
    haar_norm = math.sqrt(max(0.0, haar_energy))
    residual_norm = math.sqrt(max(0.0, residual_energy))
    lower = abs(haar_norm - residual_norm)
    upper = haar_norm + residual_norm
    minkowski_violation = max(0.0, lower - natural_norm, natural_norm - upper)
    alignment = (
        cross / math.sqrt(haar_energy * residual_energy)
        if haar_energy > tolerance and residual_energy > tolerance
        else 0.0
    )
    total_amplitude = sum(natural)
    chi_square = natural_energy / total_amplitude**2 if total_amplitude > tolerance else 0.0
    relative_haar = haar_norm / total_amplitude if total_amplitude > tolerance else 0.0
    relative_residual = (
        residual_norm / total_amplitude if total_amplitude > tolerance else 0.0
    )
    max_forbidden = max(row.forbidden_support_amplitude_residual for row in channels)
    max_fiber = max(row.maximum_orientation_fiber_amplitude_residual for row in channels)
    profile_invariant = all(
        row.orientation_fiber_profile_invariant for row in channels
    )
    exact = bool(
        profile_invariant
        and associativity_verified
        and max_forbidden <= tolerance
        and max_fiber <= tolerance
        and decomposition_residual <= tolerance
        and minkowski_violation <= tolerance
    )
    if natural_energy <= tolerance and haar_energy > tolerance and residual_energy > tolerance:
        diagnosis = "rank-profile-nonuniformity-exactly-cancelled-by-racah-arithmetic"
    elif residual_energy > 2.0 * max(haar_energy, tolerance):
        diagnosis = "nonhaar-racah-arithmetic-dominates-finite-centered-energy"
    elif haar_energy > 2.0 * max(residual_energy, tolerance):
        diagnosis = "kronecker-rank-profile-dominates-finite-centered-energy"
    else:
        diagnosis = "rank-profile-and-racah-arithmetic-both-material-at-finite-n"
    return RacahRankResidualControl(
        control_id=control_id,
        n=n,
        orbit_indices=orbit_indices,
        orbit_representatives=base,
        channels=tuple(channels),
        natural_centered_energy=natural_energy,
        haar_rank_profile_centered_energy=haar_energy,
        nonhaar_residual_centered_energy=residual_energy,
        rank_residual_centered_cross_term=cross,
        variance_decomposition_residual=decomposition_residual,
        centered_alignment_cosine=alignment,
        minkowski_lower_bound=lower,
        minkowski_upper_bound=upper,
        minkowski_violation=minkowski_violation,
        total_natural_amplitude=total_amplitude,
        conditional_syndrome_chi_square=chi_square,
        rank_profile_relative_scale=relative_haar,
        nonhaar_residual_relative_scale=relative_residual,
        independent_haar_null_energy_upper_benchmark=8.0
        * sum(row.normalized_haar_block_variance for row in channels),
        maximum_forbidden_support_amplitude_residual=max_forbidden,
        maximum_orientation_fiber_amplitude_residual=max_fiber,
        all_orientation_fusion_profiles_invariant=profile_invariant,
        all_fusion_associativity_identities_verified=associativity_verified,
        exact_rank_residual_decomposition_verified=exact,
        finite_mechanism_diagnosis=diagnosis,
        status=(
            "adaptive-channel-split-into-rank-profile-and-racah-arithmetic"
            if exact
            else "racah-rank-residual-control-failure"
        ),
    )


def _default_orbit_controls() -> list[RacahRankResidualControl]:
    controls: list[RacahRankResidualControl] = []
    for n in (4, 5):
        orbits, _arrays = parity_coset_word_likelihood_arrays(n)
        retained = tuple(
            index
            for index, orbit in enumerate(orbits)
            if len(orbit) == 2 and hook_length_dimension(orbit[0]) > 1
        )
        if not retained:
            continue
        tuples = [(retained[0],) * 6, (retained[-1],) * 6]
        if len(retained) > 1:
            tuples.append(tuple(retained[index % len(retained)] for index in range(6)))
        for index, orbit_tuple in enumerate(dict.fromkeys(tuples)):
            controls.append(
                audit_racah_rank_residual(f"S{n}-RACAH-{index}", n, orbit_tuple)
            )
    return controls


def run_parity_racah_rank_residual_decomposition(
) -> ParityRacahRankResidualReport:
    mapping_controls = [audit_axis_mapping_support(n) for n in (3, 4)]
    controls = _default_orbit_controls()
    failures = sum(
        not row.direct_coefficient_axis_mapping_verified
        or not row.competing_dual_mapping_rejected
        for row in mapping_controls
    ) + sum(not row.exact_rank_residual_decomposition_verified for row in controls)
    verified = failures == 0
    cancellation_controls = sum(
        row.finite_mechanism_diagnosis
        == "rank-profile-nonuniformity-exactly-cancelled-by-racah-arithmetic"
        for row in controls
    )
    arithmetic_dominated = sum(
        row.finite_mechanism_diagnosis
        == "nonhaar-racah-arithmetic-dominates-finite-centered-energy"
        for row in controls
    )
    return ParityRacahRankResidualReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_axis_order": (
                "(alpha,beta,gamma,mu,nu,lambda)=(gk,ghk,hk,g,h,k); "
                "the four fusion triples are (alpha,beta,mu), "
                "(mu,gamma,lambda), (beta,gamma,nu), and "
                "(alpha,nu,lambda)."
            ),
            "normalized_racah_mass": "A_y=||R_(mu,nu)||_HS^2/(d_mu d_nu).",
            "haar_rank_profile": (
                "H_y=l_y r_y/(M_y d_mu d_nu), the exact Haar-orthogonal "
                "mean for the corresponding recoupling block dimensions."
            ),
            "arithmetic_residual": "E_y=A_y-H_y isolates non-Haar 6j arithmetic.",
            "energy_decomposition": (
                "N(A)^2=N(H)^2+N(E)^2+2<C H,C E>_N, where "
                "N(v)^2=8||Cv||_2^2 and <.,.>_N=8<.,.>."
            ),
            "minkowski_boundary": "|N(H)-N(E)|<=N(A)<=N(H)+N(E).",
            "haar_null_variance": (
                "Var(||R_block||_HS^2)=2lr(M-l)(M-r)/[M^2(M-1)(M+2)] "
                "for a real Haar M-dimensional recoupling matrix."
            ),
            "scope": (
                "The Haar law is a null benchmark only. No natural random-matrix "
                "limit, canonical rank mixing, arithmetic decay, survival, algorithm, "
                "or speedup is proved."
            ),
        },
        axis_mapping_controls=mapping_controls,
        orbit_controls=controls,
        proof_obligations=[
            {
                "obligation": "fix_physical_coefficient_axis_to_racah_label_mapping",
                "resolved": verified,
                "resolution": (
                    "The direct mapping has no unsupported positive exact likelihoods; "
                    "the competing tetrahedral-dual mapping fails finite support tests."
                ),
            },
            {
                "obligation": "split_adaptive_energy_into_rank_arithmetic_and_alignment",
                "resolved": verified,
                "resolution": (
                    "The physical trace-mass law and centered Hilbert-space identity "
                    "give the exact decomposition and Minkowski bounds."
                ),
            },
            {
                "obligation": "bound_canonical_kronecker_rank_profile_variance",
                "resolved": False,
                "resolution": (
                    "Control the source-weighted relative norm N(H)/T0 on the "
                    "dimension-trimmed physical Plancherel sector."
                ),
            },
            {
                "obligation": "bound_canonical_nonhaar_racah_arithmetic_residual",
                "resolved": False,
                "resolution": (
                    "Prove or falsify a source-weighted estimate for N(E)/T0; Haar "
                    "entry moments do not apply to deterministic symmetric-group 6j blocks."
                ),
            },
            {
                "obligation": "control_rank_arithmetic_alignment_for_survival",
                "resolved": False,
                "resolution": (
                    "A survival lower bound requires preventing asymptotic cancellation "
                    "between the centered rank profile and arithmetic residual."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The geometric edge labeling is equivalent and harmless.",
                "resolved": True,
                "resolution": (
                    "It is the tetrahedral-dual incidence, not this table convention; "
                    "it assigns positive exact likelihoods to forbidden fusion blocks."
                ),
            },
            {
                "objection": "A nonuniform Kronecker rank profile proves syndrome survival.",
                "resolved": True,
                "resolution": (
                    "An S4 control has nonzero rank-profile variance cancelled exactly "
                    "by an antiparallel non-Haar residual, leaving a flat natural channel."
                ),
            },
            {
                "objection": "A flat Haar rank profile proves syndrome decoupling.",
                "resolved": True,
                "resolution": (
                    "Finite S5 controls have arithmetic-residual energy much larger than "
                    "their rank-profile energy."
                ),
            },
            {
                "objection": "The Haar variance formula models natural 6j symbols.",
                "resolved": True,
                "resolution": (
                    "No such distributional theorem is assumed; equation (5) is only a "
                    "calibrated null against which deterministic arithmetic can be tested."
                ),
            },
        ],
        headline_metrics={
            "rank_arithmetic_energy_decomposition_theorem_count": int(verified),
            "physical_axis_mapping_control_count": len(mapping_controls),
            "finite_orbit_control_count": len(controls),
            "finite_control_failure_count": failures,
            "exact_rank_arithmetic_cancellation_control_count": cancellation_controls,
            "finite_arithmetic_dominated_control_count": arithmetic_dominated,
            "maximum_axis_mapping_support_residual": max(
                row.maximum_direct_mapping_unsupported_likelihood
                for row in mapping_controls
            ),
            "maximum_orientation_fiber_amplitude_residual": max(
                row.maximum_orientation_fiber_amplitude_residual for row in controls
            ),
            "maximum_variance_decomposition_residual": max(
                row.variance_decomposition_residual for row in controls
            ),
            "canonical_rank_profile_bound_count": 0,
            "canonical_racah_residual_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_coefficient_axis_mapping_verified": verified,
            "positive_channels_are_normalized_racah_block_masses": verified,
            "rank_arithmetic_alignment_decomposition_proved": verified,
            "haar_rank_profile_alone_determines_natural_channel": False,
            "haar_null_is_natural_racah_distribution_theorem": False,
            "canonical_kronecker_rank_profile_mixes_proved": False,
            "canonical_nonhaar_racah_residual_vanishes_proved": False,
            "canonical_rank_arithmetic_alignment_controlled": False,
            "canonical_adaptive_syndrome_decouples_proved": False,
            "canonical_adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Adaptive information is now split into explicit multiplicity, "
                "deterministic 6j arithmetic, and alignment obligations, but none has "
                "the required canonical source-weighted asymptotic bound."
            ),
        },
        status=(
            "adaptive-parity-split-into-rank-profile-racah-arithmetic-and-alignment"
            if verified
            else "parity-racah-rank-residual-control-failure"
        ),
        summary=(
            "Separated adaptive parity variance into Kronecker rank-profile and "
            "non-Haar Racah arithmetic terms and exposed exact finite cancellation."
        ),
        falsifiers_triggered=[
            "The tetrahedral-dual geometric label mapping is incompatible with the implemented physical likelihood axes.",
            "Kronecker block ranks alone neither prove survival nor prove decoupling.",
            "Natural symmetric-group recoupling cannot be replaced by an unproved Haar ansatz.",
            "Rank and arithmetic components can cancel perfectly after centering.",
            "Canonical progress requires source-weighted asymptotics for both components and their alignment.",
        ],
    )


def write_parity_racah_rank_residual_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_racah_rank_residual_decomposition())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_racah_rank_residual_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

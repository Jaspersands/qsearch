"""Compressed finite probes of irreducible orientation-syndrome Racah CMI.

The pair-fiber compiler can evaluate the eight transpose-orientation syndrome
amplitudes of one six-label sign-orbit tuple beyond the old factorial
character-sum limit.  In physical coefficient order

    (alpha,beta,gamma,mu,nu,lambda),

choose one orientation representative for every syndrome
``y=A^T z in F_2^3``.  If ``x_y`` is the corresponding Racah block
Hilbert--Schmidt mass, then

    A_y=x_y/(d_mu d_nu).                                 (1)

Normalizing the eight ``A_y`` gives the adaptive syndrome channel.  Its
irreducible non-Haar information is exactly ``I(Y_g;Y_h|Y_k)``.  The physical
mass of the entire 64-orientation sign-orbit tuple is

    P_orbit = 8 (product_i d_i)/|S_n|^3 sum_y A_y.        (2)

Equation (2) is cross-checked against the exact ``S_5`` coarse physical law.

The repeated dimension-ten ``S_6`` orbit has a numerical two-syndrome channel
with almost one bit of conditional information, but physical mass only about
``1.07e-4``.  Repeated ``S_7`` sectors do not continue that pattern: their
source-weighted contributions are at most a few ``1e-7`` bits.  This is a
finite nonmonotonic falsifier, not evidence of decay.  The first repeated
dimension-70 ``S_8`` live attempt exceeded the current representation-space
resource envelope before one channel completed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
)
from self_dual_wreath_compressed_racah_block_probe import (
    compile_compressed_racah_block,
)
from self_dual_wreath_parity_racah_conditional_cumulant import (
    audit_conditional_cumulant,
)
from self_dual_wreath_parity_racah_toric_obstruction import (
    exact_natural_syndrome_amplitudes,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    orientation_syndrome,
    sign_orbits,
    transpose_partition,
)
from symmetric_character import kronecker_coefficient


Partition = tuple[int, ...]
Syndrome = tuple[int, int, int]
Orientation = tuple[int, int, int, int, int, int]
BITS: tuple[Syndrome, ...] = tuple(itertools.product((0, 1), repeat=3))
ORIENTATIONS: tuple[Orientation, ...] = tuple(itertools.product((0, 1), repeat=6))
SYNDROME_REPRESENTATIVES: dict[Syndrome, Orientation] = {
    syndrome: next(
        orientation
        for orientation in ORIENTATIONS
        if orientation_syndrome(orientation) == syndrome
    )
    for syndrome in BITS
}
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_compressed_orientation_racah_cumulant_probe.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-ORIENTATION-RACAH-CUMULANT-PROBE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrientationRacahBlockEntry:
    syndrome: Syndrome
    orientation_representative: Orientation
    oriented_partitions: tuple[Partition, ...]
    left_block_rank: int
    right_block_rank: int
    total_multiplicity_dimension: int
    block_hilbert_schmidt_square: float
    normalized_syndrome_amplitude: float
    haar_rank_profile_amplitude: float
    maximum_pair_embedding_isometry_residual: float
    numerically_zero_at_threshold: bool
    status: str


@dataclass(frozen=True)
class CompressedOrientationRacahControl:
    control_id: str
    n: int
    base_partitions: tuple[Partition, ...]
    base_dimensions: tuple[int, ...]
    all_base_partitions_equal: bool
    entries: tuple[OrientationRacahBlockEntry, ...]
    total_syndrome_amplitude: float
    conditional_syndrome_probabilities: tuple[float, ...]
    conditional_determinants: tuple[float, float]
    irreducible_racah_cmi_bits: float
    rank_profile_cmi_bits: float
    rank_profile_maximum_conditional_determinant: float
    physical_sign_orbit_tuple_mass: float
    physical_mass_weighted_irreducible_cmi_bits: float
    numerically_nonzero_syndrome_count: int
    exact_zero_pattern_proved: bool
    maximum_pair_embedding_isometry_residual: float
    compressed_orientation_channel_verified: bool
    finite_representation_space_probe_only: bool
    status: str


@dataclass(frozen=True)
class OrientationAmplitudeCrossCheck:
    n: int
    base_partitions: tuple[Partition, ...]
    exact_orbit_indices: tuple[int, ...]
    maximum_exact_amplitude_residual: float
    compressed_physical_orbit_mass: float
    exact_coarse_physical_orbit_mass: float
    physical_mass_formula_residual: float
    exact_amplitude_and_mass_formula_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationProbeResourceBoundary:
    n: int
    repeated_base_partition: Partition
    irrep_dimension: int
    pair_eigensolve_vector_dimension: int
    dense_three_copy_vector_dimension: int
    required_orientation_block_count: int
    completed_orientation_block_count: int
    live_attempt_exit_code: int
    asymptotic_inference_allowed: bool
    status: str


@dataclass(frozen=True)
class CompressedOrientationRacahReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_cross_check: OrientationAmplitudeCrossCheck
    controls: list[CompressedOrientationRacahControl]
    resource_boundary: OrientationProbeResourceBoundary
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _oriented_partitions(
    base: tuple[Partition, ...],
    orientation: Orientation,
) -> tuple[Partition, ...]:
    return tuple(
        transpose_partition(partition) if bit else partition
        for partition, bit in zip(base, orientation)
    )


def _rank_profile(
    labels: tuple[Partition, ...],
) -> tuple[int, int, int, float]:
    alpha, beta, gamma, mu, nu, final = labels
    n = sum(alpha)
    left = kronecker_coefficient(alpha, beta, mu) * kronecker_coefficient(
        mu, gamma, final
    )
    right = kronecker_coefficient(beta, gamma, nu) * kronecker_coefficient(
        alpha, nu, final
    )
    total = sum(
        kronecker_coefficient(alpha, beta, intermediate)
        * kronecker_coefficient(intermediate, gamma, final)
        for intermediate in integer_partitions(n)
    )
    amplitude = (
        left
        * right
        / (
            total
            * hook_length_dimension(mu)
            * hook_length_dimension(nu)
        )
        if total > 0
        else 0.0
    )
    return left, right, total, amplitude


def compile_orientation_racah_channel(
    control_id: str,
    base_partitions: tuple[Partition, ...],
    *,
    numerical_zero_threshold: float = 1e-20,
    tolerance: float = 3e-6,
) -> CompressedOrientationRacahControl:
    if len(base_partitions) != 6:
        raise ValueError("six base partitions are required")
    n = sum(base_partitions[0])
    if any(sum(partition) != n for partition in base_partitions):
        raise ValueError("base partitions must have common degree")
    if any(transpose_partition(partition) == partition for partition in base_partitions):
        raise ValueError("orientation probes require non-self-conjugate sign orbits")

    entries: list[OrientationRacahBlockEntry] = []
    amplitudes: list[float] = []
    rank_amplitudes: list[float] = []
    for syndrome in BITS:
        orientation = SYNDROME_REPRESENTATIVES[syndrome]
        labels = _oriented_partitions(base_partitions, orientation)
        alpha, beta, gamma, mu, nu, final = labels
        left, right, total, rank_amplitude = _rank_profile(labels)
        if left > 0 and right > 0 and total > 0:
            block = compile_compressed_racah_block(
                f"{control_id}-{''.join(map(str, syndrome))}",
                (alpha, beta, gamma, final),
                mu,
                nu,
                tolerance=tolerance,
            )
            hs_square = block.block_hilbert_schmidt_square
            amplitude = hs_square / (
                hook_length_dimension(mu) * hook_length_dimension(nu)
            )
            isometry = block.maximum_pair_embedding_isometry_residual
        else:
            hs_square = 0.0
            amplitude = 0.0
            isometry = 0.0
        amplitudes.append(amplitude)
        rank_amplitudes.append(rank_amplitude)
        entries.append(
            OrientationRacahBlockEntry(
                syndrome=syndrome,
                orientation_representative=orientation,
                oriented_partitions=labels,
                left_block_rank=left,
                right_block_rank=right,
                total_multiplicity_dimension=total,
                block_hilbert_schmidt_square=hs_square,
                normalized_syndrome_amplitude=amplitude,
                haar_rank_profile_amplitude=rank_amplitude,
                maximum_pair_embedding_isometry_residual=isometry,
                numerically_zero_at_threshold=amplitude <= numerical_zero_threshold,
                status=(
                    "compressed-orientation-racah-block-compiled"
                    if left > 0 and right > 0 and total > 0
                    else "orientation-channel-forbidden-by-fusion-support"
                ),
            )
        )
    total_amplitude = sum(amplitudes)
    if total_amplitude <= 0:
        raise ValueError("orientation channel has zero total amplitude")
    natural = audit_conditional_cumulant(control_id, amplitudes)
    if sum(rank_amplitudes) > 0:
        rank = audit_conditional_cumulant(f"{control_id}-RANK", rank_amplitudes)
        rank_cmi = rank.irreducible_racah_cmi_bits
        rank_minor = max(abs(value) for value in rank.direct_conditional_determinants)
    else:
        rank_cmi = 0.0
        rank_minor = 0.0
    dimensions = tuple(hook_length_dimension(partition) for partition in base_partitions)
    physical_mass = (
        8.0
        * math.prod(dimensions)
        * total_amplitude
        / math.factorial(n) ** 3
    )
    maximum_isometry = max(entry.maximum_pair_embedding_isometry_residual for entry in entries)
    verified = bool(
        natural.exact_conditional_cumulant_reduction_verified
        and rank_cmi <= tolerance
        and rank_minor <= tolerance
        and maximum_isometry <= tolerance
        and -tolerance <= physical_mass <= 1.0 + tolerance
    )
    return CompressedOrientationRacahControl(
        control_id=control_id,
        n=n,
        base_partitions=base_partitions,
        base_dimensions=dimensions,
        all_base_partitions_equal=len(set(base_partitions)) == 1,
        entries=tuple(entries),
        total_syndrome_amplitude=total_amplitude,
        conditional_syndrome_probabilities=natural.probabilities,
        conditional_determinants=natural.direct_conditional_determinants,
        irreducible_racah_cmi_bits=natural.irreducible_racah_cmi_bits,
        rank_profile_cmi_bits=rank_cmi,
        rank_profile_maximum_conditional_determinant=rank_minor,
        physical_sign_orbit_tuple_mass=physical_mass,
        physical_mass_weighted_irreducible_cmi_bits=(
            physical_mass * natural.irreducible_racah_cmi_bits
        ),
        numerically_nonzero_syndrome_count=sum(
            amplitude > numerical_zero_threshold for amplitude in amplitudes
        ),
        exact_zero_pattern_proved=False,
        maximum_pair_embedding_isometry_residual=maximum_isometry,
        compressed_orientation_channel_verified=verified,
        finite_representation_space_probe_only=True,
        status=(
            "compressed-orientation-racah-cumulant-probe-verified"
            if verified
            else "compressed-orientation-racah-control-failure"
        ),
    )


def audit_s5_exact_amplitude_cross_check(
    *,
    tolerance: float = 3e-8,
) -> tuple[OrientationAmplitudeCrossCheck, CompressedOrientationRacahControl]:
    n = 5
    orbit_indices = (1, 2, 1, 2, 2, 2)
    base = (
        (2, 1, 1, 1),
        (2, 2, 1),
        (2, 1, 1, 1),
        (2, 2, 1),
        (2, 2, 1),
        (2, 2, 1),
    )
    compressed = compile_orientation_racah_channel("S5-EXACT-CROSS-CHECK", base)
    exact = tuple(map(float, exact_natural_syndrome_amplitudes(n, orbit_indices)))
    amplitude_residual = max(
        abs(entry.normalized_syndrome_amplitude - target)
        for entry, target in zip(compressed.entries, exact)
    )
    exact_mass = float(aggregate_sign_orbit_law(n)[3][orbit_indices])
    mass_residual = abs(compressed.physical_sign_orbit_tuple_mass - exact_mass)
    verified = amplitude_residual <= tolerance and mass_residual <= tolerance
    return (
        OrientationAmplitudeCrossCheck(
            n=n,
            base_partitions=base,
            exact_orbit_indices=orbit_indices,
            maximum_exact_amplitude_residual=amplitude_residual,
            compressed_physical_orbit_mass=compressed.physical_sign_orbit_tuple_mass,
            exact_coarse_physical_orbit_mass=exact_mass,
            physical_mass_formula_residual=mass_residual,
            exact_amplitude_and_mass_formula_verified=verified,
            status=(
                "compressed-orientation-amplitudes-and-physical-mass-cross-checked"
                if verified
                else "compressed-orientation-exact-cross-check-failure"
            ),
        ),
        compressed,
    )


def run_compressed_orientation_racah_cumulant_probe(
) -> CompressedOrientationRacahReport:
    cross_check, s5 = audit_s5_exact_amplitude_cross_check()
    s6 = compile_orientation_racah_channel(
        "S6-REPEATED-DIMENSION-10", ((3, 1, 1, 1),) * 6
    )
    s7_controls = [
        compile_orientation_racah_channel(
            f"S7-REPEATED-ORBIT-{index}", (orbit[0],) * 6
        )
        for index, orbit in enumerate(sign_orbits(7)[0])
        if hook_length_dimension(orbit[0]) > 1
    ]
    controls = [s5, s6, *s7_controls]
    resource = OrientationProbeResourceBoundary(
        n=8,
        repeated_base_partition=(3, 2, 2, 1),
        irrep_dimension=70,
        pair_eigensolve_vector_dimension=4_900,
        dense_three_copy_vector_dimension=343_000,
        required_orientation_block_count=8,
        completed_orientation_block_count=0,
        live_attempt_exit_code=137,
        asymptotic_inference_allowed=False,
        status="current-compressed-compiler-exceeded-s8-repeated-orientation-resource-envelope",
    )
    failures = int(not cross_check.exact_amplitude_and_mass_formula_verified)
    failures += sum(not row.compressed_orientation_channel_verified for row in controls)
    verified = failures == 0
    repeated_s7 = [row for row in controls if row.control_id.startswith("S7-")]
    return CompressedOrientationRacahReport(
        created_at=utc_now(),
        theorem_contract={
            "syndrome_amplitude": "A_y=||R_y(mu,nu)||_HS^2/(d_mu d_nu)",
            "conditional_channel": "p_y=A_y/sum_z A_z",
            "irreducible_information": "I_p(Y_g;Y_h|Y_k)",
            "physical_orbit_mass": "8 product_i(d_i) sum_y(A_y)/|S_n|^3",
            "rank_null": "the Haar multiplicity-rank profile is G--K--H Markov",
            "scope": "selected finite sign-orbit tuples; no physical-average scaling theorem",
        },
        exact_cross_check=cross_check,
        controls=controls,
        resource_boundary=resource,
        proof_obligations=[
            {
                "obligation": "extend_orientation_racah_channels_beyond_factorial_character_enumeration",
                "resolved": verified,
                "resolution": "Eight gauge-invariant compressed pair-fiber block contractions produce one selected sign-orbit channel.",
            },
            {
                "obligation": "estimate_physical_average_orientation_cmi",
                "resolved": False,
                "resolution": "Need exact physical sampling of full six-label tuples, sign-orbit aggregation, duplicate caching, and confidence bounds.",
            },
            {
                "obligation": "prove_positive_mass_asymptotic_toric_violation",
                "resolved": False,
                "resolution": "The S6 spike collapses on tested repeated S7 sectors and gives no scalable family.",
            },
            {
                "obligation": "scale_compressed_orientation_channels_through_s8_and_beyond",
                "resolved": False,
                "resolution": "The first repeated dimension-70 S8 attempt exited 137 before a channel completed; require a character-sum or stochastic block estimator.",
            },
            {
                "obligation": "compare_classical_and_coherent_estimation_complexity",
                "resolved": False,
                "resolution": "Physical mass, normalized-character Monte Carlo variance, coherent preparation, and decoder costs must be compared on the same family.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "One bit at S6 is evidence of asymptotic survival.",
                "resolved": True,
                "resolution": "Its orbit mass is about 1.07e-4 and all tested repeated S7 weighted contributions are below 3.3e-7 bits.",
            },
            {
                "objection": "Numerically tiny S6 amplitudes are exact zeros.",
                "resolved": True,
                "resolution": "The report marks only a numerical two-support pattern; exact_zero_pattern_proved remains false.",
            },
            {
                "objection": "Repeated sign-orbit tuples represent the physical average.",
                "resolved": True,
                "resolution": "Mixed tuples may dominate both physical mass and CMI; repeated controls are deliberately nonexhaustive.",
            },
            {
                "objection": "A finite measured syndrome channel is a quantum algorithm.",
                "resolved": True,
                "resolution": "No coherent estimator, classical separation, decoder, or asymptotic source-mass theorem is supplied.",
            },
        ],
        headline_metrics={
            "compressed_orientation_channel_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_completed_n": max(row.n for row in controls),
            "S6_repeated_irreducible_cmi_bits": s6.irreducible_racah_cmi_bits,
            "S6_repeated_physical_mass": s6.physical_sign_orbit_tuple_mass,
            "S6_repeated_weighted_cmi_bits": s6.physical_mass_weighted_irreducible_cmi_bits,
            "S7_repeated_maximum_cmi_bits": max(
                row.irreducible_racah_cmi_bits for row in repeated_s7
            ),
            "S7_repeated_maximum_weighted_cmi_bits": max(
                row.physical_mass_weighted_irreducible_cmi_bits for row in repeated_s7
            ),
            "S7_repeated_total_physical_mass": sum(
                row.physical_sign_orbit_tuple_mass for row in repeated_s7
            ),
            "S8_completed_orientation_channel_count": 0,
            "physical_average_orientation_cmi_estimate_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "compressed_orientation_amplitude_formula_verified": verified,
            "physical_orbit_mass_formula_verified": cross_check.exact_amplitude_and_mass_formula_verified,
            "S6_numerical_two_syndrome_pattern_is_exact_proved": False,
            "repeated_orbit_sequence_supports_scaling_inference": False,
            "physical_average_orientation_cmi_positive_proved": False,
            "asymptotic_toric_violation_survives_proved": False,
            "coherent_extraction_implemented": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The finite S6 spike is low-mass and nonpersistent across repeated S7 sectors; mixed physical averaging and access complexity remain open.",
        },
        status=(
            "compressed-orientation-cmi-reaches-s7-with-nonmonotone-finite-signal"
            if verified
            else "compressed-orientation-racah-cumulant-control-failure"
        ),
        summary=(
            "Extended exact-orientation diagnostics to selected S7 sectors and "
            "falsified monotone extrapolation of the low-mass S6 one-bit spike."
        ),
        falsifiers_triggered=[
            "A large conditional CMI without physical source mass has little aggregate value.",
            "The repeated-orbit S6 signal does not persist uniformly at S7.",
            "Current pair-fiber embeddings do not provide a scalable S8 orientation workbench.",
        ],
    )


def write_compressed_orientation_racah_cumulant_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_compressed_orientation_racah_cumulant_probe())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_compressed_orientation_racah_cumulant_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

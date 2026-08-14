"""Kronecker rank profiles form a conditional-independence toric model.

For a symmetric-group Kronecker coefficient, transposing Young diagrams is
tensoring by the sign representation.  Hence

    g(a^u,b^v,c^w) = g_(u xor v xor w)(a,b,c),             (1)

where ``g_0(a,b,c)=g(a,b,c)`` and ``g_1(a,b,c)=g(a,b,c^t)``.

Apply (1) to the Haar rank-profile benchmark of the adaptive parity channel.
For one base six-label sign-orbit tuple, write ``a_t,b_t,c_t,d_t`` for the
two sign twists of the four tetrahedral fusion multiplicities and ``M_t`` for
the two final triple-product multiplicities.  In syndrome coordinates
``y=(g,h,k)``, the benchmark is exactly

    H_(g,h,k)
      = a_g b_(g xor k) c_h d_(h xor k) / (M_k d_mu d_nu). (2)

Thus ``H`` is a nonnegative pairwise factor graph with Markov structure

    G -- K -- H,       equivalently G independent of H given K.             (3)

Its two conditional-independence minors vanish:

    H_00k H_11k - H_01k H_10k = 0,  k=0,1,                 (4)

and therefore so does the no-three-factor-interaction cube binomial

    product_(g+h+k even) H_ghk - product_(g+h+k odd) H_ghk = 0. (5)

Equations (2)--(5) are exact, including on support boundaries; no logarithms
or positivity assumptions are needed.

The natural Racah channel does not obey this model.  At ``S_5``, orbit tuple
``(1,2,1,2,2,2)`` has the exact positive amplitudes

    (1/64,1/64,1/64,9/1600,1/64,9/1600,1/14400,1/64).

Its two minors are ``-7/28800`` and ``17/80000``, its cube defect is
``-61/1024000000``, and its normalized conditional mutual information
``I(G;H|K)`` is about 0.205 bits.  The corresponding rank benchmark has both
minors and the cube defect exactly zero.  This is a finite exact certificate
that deterministic non-Haar Racah arithmetic creates genuine tetrahedral
dependence unavailable to multiplicity ranks alone.

The witness is not asymptotic evidence, and measured-label conditional
dependence is neither an efficient coherent measurement nor a classical
complexity separation.  No algorithm or speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from self_dual_wreath_parity_projector_orbit_variance import BITS
from self_dual_wreath_parity_racah_rank_residual_decomposition import (
    audit_racah_rank_residual,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    kronecker_multiplicity,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    orientation_syndrome,
    transpose_partition,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    tetrahedral_class_signature_counts,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_racah_toric_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-TORIC-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Orientation = tuple[int, int, int, int, int, int]
ORIENTATIONS: tuple[Orientation, ...] = tuple(
    itertools.product((0, 1), repeat=6)
)
WORD_SIGNATURE_AXES = (3, 5, 4, 0, 1, 2)


@dataclass(frozen=True)
class KroneckerTransposeXorControl:
    n: int
    partition_count: int
    tested_oriented_triple_count: int
    mismatch_count: int
    transpose_xor_law_verified: bool
    status: str


@dataclass(frozen=True)
class RacahToricControl:
    control_id: str
    n: int
    orbit_indices: tuple[int, ...]
    orbit_representatives: tuple[Partition, ...]
    twisted_face_multiplicities: tuple[tuple[int, int], ...]
    twisted_total_multiplicities: tuple[int, int]
    exact_natural_amplitudes: tuple[str, ...]
    exact_rank_profile_amplitudes: tuple[str, ...]
    exact_natural_conditional_independence_minors: tuple[str, str]
    exact_rank_conditional_independence_minors: tuple[str, str]
    exact_natural_cube_binomial_defect: str
    exact_rank_cube_binomial_defect: str
    natural_conditional_mutual_information_bits: float
    rank_conditional_mutual_information_bits: float
    maximum_exact_to_projector_amplitude_residual: float
    maximum_rank_factorization_residual: float
    all_natural_amplitudes_positive: bool
    natural_channel_outside_rank_profile_toric_model: bool
    exact_rank_factorization_verified: bool
    exact_toric_obstruction_verified: bool
    status: str


@dataclass(frozen=True)
class ParityRacahToricObstructionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    transpose_xor_controls: list[KroneckerTransposeXorControl]
    toric_controls: list[RacahToricControl]
    primary_witness: RacahToricControl
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def twisted_kronecker_pair(
    left: Partition,
    right: Partition,
    target: Partition,
) -> tuple[int, int]:
    return (
        kronecker_multiplicity(left, right, target),
        kronecker_multiplicity(left, right, transpose_partition(target)),
    )


def audit_kronecker_transpose_xor(n: int) -> KroneckerTransposeXorControl:
    if not 2 <= n <= 7:
        raise ValueError("exact transpose-XOR controls require 2<=n<=7")
    partitions = tuple(integer_partitions(n))
    mismatches = 0
    tested = 0
    for left, right, target in itertools.product(partitions, repeat=3):
        pair = twisted_kronecker_pair(left, right, target)
        for bits in itertools.product((0, 1), repeat=3):
            oriented = tuple(
                transpose_partition(partition) if bit else partition
                for partition, bit in zip((left, right, target), bits)
            )
            observed = kronecker_multiplicity(*oriented)
            expected = pair[bits[0] ^ bits[1] ^ bits[2]]
            mismatches += observed != expected
            tested += 1
    verified = mismatches == 0
    return KroneckerTransposeXorControl(
        n=n,
        partition_count=len(partitions),
        tested_oriented_triple_count=tested,
        mismatch_count=mismatches,
        transpose_xor_law_verified=verified,
        status=(
            "kronecker-transpose-dependence-is-exactly-one-xor-bit"
            if verified
            else "kronecker-transpose-xor-control-failure"
        ),
    )


def exact_natural_syndrome_amplitudes(
    n: int,
    orbit_indices: tuple[int, ...],
) -> tuple[Fraction, ...]:
    """Evaluate ``A_y`` by exact character sums, without floating transforms."""

    if not 2 <= n <= 5:
        raise ValueError("exact character controls require 2<=n<=5")
    if len(orbit_indices) != 6:
        raise ValueError("six orbit indices are required")
    orbits, _arrays = parity_coset_word_likelihood_arrays(n)
    if any(index < 0 or index >= len(orbits) for index in orbit_indices):
        raise ValueError("orbit index is out of range")
    selected = tuple(orbits[index] for index in orbit_indices)
    if any(len(orbit) != 2 for orbit in selected):
        raise ValueError("toric controls require non-self-conjugate sign orbits")
    base = tuple(orbit[0] for orbit in selected)
    signatures = tetrahedral_class_signature_counts(n)
    denominator = math.factorial(n) ** 3
    amplitudes = []
    for syndrome in BITS:
        orientation = next(
            row for row in ORIENTATIONS if orientation_syndrome(row) == syndrome
        )
        labels = tuple(
            transpose_partition(partition) if bit else partition
            for partition, bit in zip(base, orientation)
        )
        numerator = sum(
            count
            * math.prod(
                symmetric_character(label, signature[axis])
                for label, axis in zip(labels, WORD_SIGNATURE_AXES)
            )
            for signature, count in signatures.items()
        )
        amplitude = Fraction(numerator, denominator)
        if amplitude < 0:
            raise ArithmeticError("exact physical amplitude became negative")
        amplitudes.append(amplitude)
    return tuple(amplitudes)


def exact_rank_profile_amplitudes(
    n: int,
    orbit_indices: tuple[int, ...],
) -> tuple[
    tuple[Fraction, ...],
    tuple[tuple[int, int], ...],
    tuple[int, int],
    tuple[Partition, ...],
]:
    orbits, _arrays = parity_coset_word_likelihood_arrays(n)
    selected = tuple(orbits[index] for index in orbit_indices)
    if len(selected) != 6 or any(len(orbit) != 2 for orbit in selected):
        raise ValueError("six non-self-conjugate sign orbits are required")
    alpha, beta, gamma, mu, nu, lam = tuple(orbit[0] for orbit in selected)
    face_pairs = (
        twisted_kronecker_pair(alpha, beta, mu),
        twisted_kronecker_pair(mu, gamma, lam),
        twisted_kronecker_pair(beta, gamma, nu),
        twisted_kronecker_pair(alpha, nu, lam),
    )
    partitions = tuple(integer_partitions(n))
    totals = tuple(
        sum(
            kronecker_multiplicity(alpha, beta, eta)
            * kronecker_multiplicity(
                eta,
                gamma,
                lam if twist == 0 else transpose_partition(lam),
            )
            for eta in partitions
        )
        for twist in (0, 1)
    )
    d_mu = hook_length_dimension(mu)
    d_nu = hook_length_dimension(nu)
    first, second, third, fourth = face_pairs
    amplitudes = tuple(
        Fraction(
            first[g] * second[g ^ k] * third[h] * fourth[h ^ k],
            totals[k] * d_mu * d_nu,
        )
        if totals[k]
        else Fraction()
        for g, h, k in BITS
    )
    return amplitudes, face_pairs, totals, (alpha, beta, gamma, mu, nu, lam)


def conditional_independence_minors(
    values: Iterable[Fraction],
) -> tuple[Fraction, Fraction]:
    entries = dict(zip(BITS, tuple(values)))
    if len(entries) != 8:
        raise ValueError("eight syndrome-channel values are required")
    return tuple(
        entries[0, 0, k] * entries[1, 1, k]
        - entries[0, 1, k] * entries[1, 0, k]
        for k in (0, 1)
    )


def cube_binomial_defect(values: Iterable[Fraction]) -> Fraction:
    entries = tuple(values)
    if len(entries) != 8:
        raise ValueError("eight syndrome-channel values are required")
    even = math.prod(
        value for point, value in zip(BITS, entries) if sum(point) % 2 == 0
    )
    odd = math.prod(
        value for point, value in zip(BITS, entries) if sum(point) % 2 == 1
    )
    return even - odd


def conditional_mutual_information_bits(values: Iterable[Fraction]) -> float:
    entries = tuple(values)
    if len(entries) != 8 or any(value < 0 for value in entries):
        raise ValueError("eight nonnegative syndrome-channel values are required")
    total = sum(entries, start=Fraction())
    if total == 0:
        return 0.0
    probabilities = {point: value / total for point, value in zip(BITS, entries)}
    result = 0.0
    for g, h, k in BITS:
        probability = probabilities[g, h, k]
        if probability == 0:
            continue
        p_k = sum(probabilities[a, b, k] for a in (0, 1) for b in (0, 1))
        p_gk = sum(probabilities[g, b, k] for b in (0, 1))
        p_hk = sum(probabilities[a, h, k] for a in (0, 1))
        result += float(probability) * math.log2(
            float(probability * p_k / (p_gk * p_hk))
        )
    return max(0.0, result)


def audit_racah_toric_control(
    control_id: str,
    n: int,
    orbit_indices: tuple[int, ...],
    *,
    tolerance: float = 1e-10,
) -> RacahToricControl:
    natural = exact_natural_syndrome_amplitudes(n, orbit_indices)
    rank, faces, totals, base = exact_rank_profile_amplitudes(n, orbit_indices)
    natural_minors = conditional_independence_minors(natural)
    rank_minors = conditional_independence_minors(rank)
    natural_cube = cube_binomial_defect(natural)
    rank_cube = cube_binomial_defect(rank)
    natural_cmi = conditional_mutual_information_bits(natural)
    rank_cmi = conditional_mutual_information_bits(rank)
    floating = audit_racah_rank_residual(control_id, n, orbit_indices)
    floating_rank = tuple(
        row.haar_rank_profile_benchmark for row in floating.channels
    )
    floating_natural = tuple(
        row.natural_normalized_block_mass for row in floating.channels
    )
    factorization_residual = max(
        abs(float(exact) - observed)
        for exact, observed in zip(rank, floating_rank)
    )
    natural_transform_residual = max(
        abs(float(exact) - observed)
        for exact, observed in zip(natural, floating_natural)
    )
    factorized = bool(
        rank_minors == (0, 0)
        and rank_cube == 0
        and rank_cmi <= tolerance
        and factorization_residual <= tolerance
        and natural_transform_residual <= tolerance
    )
    outside = natural_minors != (0, 0)
    obstruction = factorized and outside
    return RacahToricControl(
        control_id=control_id,
        n=n,
        orbit_indices=orbit_indices,
        orbit_representatives=base,
        twisted_face_multiplicities=faces,
        twisted_total_multiplicities=totals,
        exact_natural_amplitudes=tuple(map(str, natural)),
        exact_rank_profile_amplitudes=tuple(map(str, rank)),
        exact_natural_conditional_independence_minors=tuple(map(str, natural_minors)),
        exact_rank_conditional_independence_minors=tuple(map(str, rank_minors)),
        exact_natural_cube_binomial_defect=str(natural_cube),
        exact_rank_cube_binomial_defect=str(rank_cube),
        natural_conditional_mutual_information_bits=natural_cmi,
        rank_conditional_mutual_information_bits=rank_cmi,
        maximum_exact_to_projector_amplitude_residual=natural_transform_residual,
        maximum_rank_factorization_residual=factorization_residual,
        all_natural_amplitudes_positive=all(value > 0 for value in natural),
        natural_channel_outside_rank_profile_toric_model=outside,
        exact_rank_factorization_verified=factorized,
        exact_toric_obstruction_verified=obstruction,
        status=(
            "natural-racah-channel-violates-rank-profile-toric-model"
            if obstruction
            else "rank-profile-factorized-without-natural-toric-witness"
            if factorized
            else "racah-toric-control-failure"
        ),
    )


def run_parity_racah_toric_obstruction() -> ParityRacahToricObstructionReport:
    transpose_controls = [audit_kronecker_transpose_xor(n) for n in (3, 4, 5)]
    controls = [
        audit_racah_toric_control("S4-FLAT-NATURAL", 4, (1,) * 6),
        audit_racah_toric_control("S5-ALL-FIVE", 5, (2,) * 6),
        audit_racah_toric_control(
            "S5-EXACT-RACAH-TORIC-WITNESS",
            5,
            (1, 2, 1, 2, 2, 2),
        ),
    ]
    witness = controls[-1]
    failures = sum(not row.transpose_xor_law_verified for row in transpose_controls)
    failures += sum(not row.exact_rank_factorization_verified for row in controls)
    failures += int(not witness.exact_toric_obstruction_verified)
    verified = failures == 0
    return ParityRacahToricObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "transpose_xor_law": (
                "g(a^u,b^v,c^w)=g_(u xor v xor w)(a,b,c), because Young-diagram "
                "transpose tensors an irrep by sign."
            ),
            "rank_profile_factorization": (
                "H_ghk=a_g b_(g xor k)c_h d_(h xor k)/(M_k d_mu d_nu)."
            ),
            "conditional_independence": (
                "The normalized rank-profile channel obeys G independent of H "
                "conditional on K; both 2x2 conditional minors vanish exactly."
            ),
            "toric_cube_identity": (
                "product_(g+h+k even)H_ghk=product_(g+h+k odd)H_ghk."
            ),
            "natural_counterexample": (
                "The exact positive S5 orbit tuple (1,2,1,2,2,2) violates both "
                "conditional minors and the cube identity and has I(G;H|K)>0.2 bits."
            ),
            "scope": (
                "This isolates finite deterministic Racah synergy outside every "
                "rank-only Haar mean. It is not an asymptotic survival theorem, "
                "efficient measurement, classical separation, or algorithm."
            ),
        },
        transpose_xor_controls=transpose_controls,
        toric_controls=controls,
        primary_witness=witness,
        proof_obligations=[
            {
                "obligation": "characterize_all_sign_orientation_dependence_of_rank_profile",
                "resolved": verified,
                "resolution": (
                    "Sign twisting reduces every face and final multiplicity to one XOR "
                    "bit, yielding the exact three-node Markov factorization."
                ),
            },
            {
                "obligation": "exhibit_natural_dependence_impossible_for_rank_profile",
                "resolved": witness.exact_toric_obstruction_verified,
                "resolution": (
                    "An exact rational S5 channel violates both toric minors with a "
                    "strict margin and has positive conditional mutual information."
                ),
            },
            {
                "obligation": "find_asymptotic_positive_mass_toric_violation",
                "resolved": False,
                "resolution": (
                    "Construct a scalable Plancherel-typical family or prove a "
                    "source-weighted lower bound for natural conditional minors/CMI."
                ),
            },
            {
                "obligation": "test_classical_access_to_racah_toric_witness",
                "resolved": False,
                "resolution": (
                    "Compare estimation of the same conditional minors under classical "
                    "word-map samples, explicit representation access, and coherent coset access."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Transpose orientations create an arbitrary eight-channel rank model.",
                "resolved": True,
                "resolution": (
                    "They create only four binary face factors and one binary total factor, "
                    "forcing the G-K-H Markov variety."
                ),
            },
            {
                "objection": "The natural violation could be floating-point noise near zeros.",
                "resolved": True,
                "resolution": (
                    "All eight witness amplitudes are positive exact rationals; the two "
                    "minors and cube defect are nonzero exact fractions."
                ),
            },
            {
                "objection": "Positive conditional mutual information establishes a quantum speedup.",
                "resolved": True,
                "resolution": (
                    "It establishes only finite measured-label structure. Preparation, "
                    "estimation complexity, asymptotic mass, and classical hardness are open."
                ),
            },
            {
                "objection": "A Haar approximation can retain this tetrahedral signal.",
                "resolved": True,
                "resolution": (
                    "The block-rank Haar mean lies exactly on the toric variety; the "
                    "witness lies outside it, so the signal is deterministic 6j arithmetic."
                ),
            },
        ],
        headline_metrics={
            "kronecker_transpose_xor_theorem_count": int(verified),
            "rank_profile_conditional_independence_theorem_count": int(verified),
            "exact_natural_toric_counterexample_count": int(
                witness.exact_toric_obstruction_verified
            ),
            "transpose_xor_control_count": len(transpose_controls),
            "finite_toric_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_exact_to_projector_amplitude_residual": max(
                row.maximum_exact_to_projector_amplitude_residual
                for row in controls
            ),
            "maximum_rank_factorization_residual": max(
                row.maximum_rank_factorization_residual for row in controls
            ),
            "primary_witness_conditional_mutual_information_bits": (
                witness.natural_conditional_mutual_information_bits
            ),
            "primary_witness_minimum_amplitude": min(
                float(Fraction(value)) for value in witness.exact_natural_amplitudes
            ),
            "asymptotic_positive_mass_toric_witness_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "rank_profile_is_G_K_H_markov_channel_proved": verified,
            "rank_profile_has_zero_three_factor_log_interaction_proved": verified,
            "natural_racah_channel_can_escape_rank_toric_model_proved": (
                witness.exact_toric_obstruction_verified
            ),
            "finite_witness_is_strictly_positive": witness.all_natural_amplitudes_positive,
            "asymptotic_toric_violation_survives_proved": False,
            "canonical_source_mass_positive_proved": False,
            "coherent_extraction_implemented": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "An exact finite natural channel has genuine Racah conditional "
                "dependence impossible for rank profiles, but scaling, source mass, "
                "coherent access, and classical hardness remain open."
            ),
        },
        status=(
            "natural-racah-synergy-certified-outside-rank-profile-toric-variety"
            if verified
            else "parity-racah-toric-obstruction-control-failure"
        ),
        summary=(
            "Proved that all Kronecker rank-profile channels are G-K-H Markov and "
            "exhibited an exact positive natural Racah channel outside that variety."
        ),
        falsifiers_triggered=[
            "Transpose choices do not generate an unrestricted eight-channel multiplicity model.",
            "The Haar rank profile cannot reproduce genuine conditional G-H coupling at fixed K.",
            "The natural finite Racah channel contains exact arithmetic structure erased by Haar averaging.",
            "Finite conditional mutual information alone does not imply scalable or quantumly exclusive value.",
        ],
    )


def write_parity_racah_toric_obstruction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_racah_toric_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_racah_toric_obstruction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

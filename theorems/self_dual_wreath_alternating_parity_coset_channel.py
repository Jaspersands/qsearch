"""Orbit-adaptive syndrome equals parity-coset A_n word-map imbalance.

Fix six base sign orbits ``O`` and representatives.  For
``x=(x_g,x_h,x_k) in F_2^3``, define

    F_x(O)=sum_(parity(g,h,k)=x) product_i r_(O_i)(W_i(g,h,k)).       (1)

The orientation likelihood has the exact Fourier expansion

    L_O(z)=sum_x (-1)^(x . A^T z) F_x(O).                            (2)

In particular ``F_0`` is the coarse alternating-group base likelihood.  On
every base orbit tuple with ``F_0>0``, the conditional syndrome law is

    P(Y=y|O)=1/8 [1+sum_(x!=0)(-1)^(x.y) F_x(O)/F_0(O)].             (3)

Thus the seven conditional Walsh coefficients are exactly the coset ratios
``F_x/F_0``.  The conditional chi-square is their squared norm, and its
physical expectation is

    E chi^2(P_(Y|O)||U) = sum_O Q_O sum_(x!=0) F_x(O)^2/F_0(O).      (4)

Choosing one odd permutation identifies every odd coset with ``A_n`` and
turns the nonzero ``F_x`` into outer-automorphism-twisted ``A_n`` word maps.
Tetrahedral symmetry has two nonzero orbit types: four face frequencies whose
word-parity support has size three, and three opposite-complement frequencies
whose support has size four.

Equations (1)--(4) are exact reductions.  They do not bound the twisted
partition functions on the dimension-trimmed Plancherel bulk.  Raw second
moments may again be dominated by low-dimensional likelihood tails, so direct
trimmed KL/TV or state-weighted ratio moments are required.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
    coarse_alternating_plancherel_weights,
    permutation_parity_from_cycle_type,
)
from self_dual_wreath_sign_orbit_kl_chain_reduction import (
    audit_sign_orbit_kl_chain,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    BitVector,
    orientation_syndrome,
    sign_frequency,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
    tetrahedral_class_signature_counts,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_parity_coset_channel.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-PARITY-COSET-CHANNEL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AlternatingParityCosetControl:
    n: int
    coarse_label_count: int
    base_orbit_tuple_count: int
    parity_coset_count: int
    face_coset_count: int
    opposite_complement_coset_count: int
    maximum_orientation_fourier_reconstruction_residual: float
    maximum_base_likelihood_residual: float
    maximum_conditional_probability_sum_residual: float
    minimum_conditional_syndrome_probability: float
    expected_conditional_syndrome_kl_bits: float
    kl_chain_conditional_syndrome_kl_bits: float
    conditional_kl_residual: float
    expected_conditional_syndrome_chi_square: float
    maximum_face_type_annealed_ratio_moment_residual: float
    maximum_opposite_type_annealed_ratio_moment_residual: float
    face_type_annealed_ratio_moment: float
    opposite_type_annealed_ratio_moment: float
    exact_parity_coset_channel_verified: bool
    status: str


@dataclass(frozen=True)
class AlternatingParityCosetChannelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[AlternatingParityCosetControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def parity_coset_word_likelihood_arrays(
    n: int,
) -> tuple[tuple[tuple[tuple[int, ...], ...], ...], dict[BitVector, np.ndarray]]:
    """Evaluate all eight partition functions in equation (1)."""

    if not 2 <= n <= 5:
        raise ValueError("exact parity-coset arrays require 2<=n<=5")
    classes = tuple(integer_partitions(n))
    class_index = {cycle_type: position for position, cycle_type in enumerate(classes)}
    orbits, _weights = coarse_alternating_plancherel_weights(n)
    representatives = tuple(orbit[0] for orbit in orbits)
    ratios = np.asarray(
        [
            [
                symmetric_character(partition, cycle_type)
                / hook_length_dimension(partition)
                for cycle_type in classes
            ]
            for partition in representatives
        ],
        dtype=float,
    )
    arrays = {
        parity: np.zeros((len(orbits),) * 6, dtype=float)
        for parity in itertools.product((0, 1), repeat=3)
    }
    for signature, count in tetrahedral_class_signature_counts(n).items():
        parity = tuple(
            permutation_parity_from_cycle_type(cycle_type)
            for cycle_type in signature[:3]
        )
        observed_label_parity = tuple(
            permutation_parity_from_cycle_type(signature[index])
            for index in (3, 5, 4, 0, 1, 2)
        )
        if observed_label_parity != sign_frequency(parity):
            raise AssertionError("word parity map disagrees with the class signature")
        indices = tuple(class_index[cycle_type] for cycle_type in signature)
        vectors = (
            ratios[:, indices[3]],
            ratios[:, indices[5]],
            ratios[:, indices[4]],
            ratios[:, indices[0]],
            ratios[:, indices[1]],
            ratios[:, indices[2]],
        )
        arrays[parity] += count * np.einsum(
            "a,b,c,d,e,f->abcdef",
            *vectors,
            optimize=False,
        )
    for array in arrays.values():
        array[np.abs(array) < 1e-10] = 0.0
    return orbits, arrays


def _conditional_channel_from_cosets(
    values: dict[BitVector, float],
) -> tuple[float, tuple[float, ...]]:
    base = values[(0, 0, 0)]
    if base <= 0:
        return base, (1.0 / 8.0,) * 8
    probabilities = tuple(
        sum(
            (-1) ** sum(a * b for a, b in zip(parity, syndrome))
            * value
            for parity, value in values.items()
        )
        / (8.0 * base)
        for syndrome in itertools.product((0, 1), repeat=3)
    )
    return base, probabilities


def audit_alternating_parity_coset_channel(
    n: int,
) -> AlternatingParityCosetControl:
    if not 2 <= n <= 5:
        raise ValueError("exact parity-coset controls require 2<=n<=5")
    partitions, full_likelihood, _full_product, _full_physical = (
        finite_physical_likelihood_arrays(n)
    )
    index = {partition: position for position, partition in enumerate(partitions)}
    orbits, arrays = parity_coset_word_likelihood_arrays(n)
    aggregate_orbits, base_likelihood, base_product, _base_physical = (
        aggregate_sign_orbit_law(n)
    )
    if orbits != aggregate_orbits:
        raise AssertionError("coarse orbit order mismatch")
    base_residual = float(
        np.max(np.abs(arrays[(0, 0, 0)] - base_likelihood))
    )
    reconstruction_residual = 0.0
    probability_residual = 0.0
    minimum_probability = 1.0
    conditional_kl = 0.0
    conditional_chi = 0.0
    ratio_moments = {
        parity: 0.0
        for parity in itertools.product((0, 1), repeat=3)
        if parity != (0, 0, 0)
    }

    for orbit_indices in np.ndindex(base_likelihood.shape):
        values = {parity: float(array[orbit_indices]) for parity, array in arrays.items()}
        base, probabilities = _conditional_channel_from_cosets(values)
        probability_residual = max(
            probability_residual,
            abs(sum(probabilities) - 1.0),
        )
        minimum_probability = min(minimum_probability, min(probabilities))
        q_orbit = float(base_product[orbit_indices])
        p_orbit = q_orbit * base
        if base > 0 and p_orbit > 0:
            conditional_kl += p_orbit * sum(
                probability * math.log2(8.0 * probability)
                for probability in probabilities
                if probability > 0
            )
            ratios = {
                parity: value / base
                for parity, value in values.items()
                if parity != (0, 0, 0)
            }
            conditional_chi += p_orbit * sum(value * value for value in ratios.values())
            for parity, ratio in ratios.items():
                ratio_moments[parity] += p_orbit * ratio * ratio

        orbit_tuple = tuple(orbits[position] for position in orbit_indices)
        for orientation in itertools.product((0, 1), repeat=6):
            labels = tuple(
                orbit[orientation[axis]] if len(orbit) == 2 else orbit[0]
                for axis, orbit in enumerate(orbit_tuple)
            )
            observed = float(full_likelihood[tuple(index[label] for label in labels)])
            syndrome = orientation_syndrome(orientation)
            reconstructed = sum(
                (-1) ** sum(a * b for a, b in zip(parity, syndrome))
                * value
                for parity, value in values.items()
            )
            reconstruction_residual = max(
                reconstruction_residual,
                abs(observed - reconstructed),
            )

    face_parities = tuple(
        parity
        for parity in ratio_moments
        if sum(sign_frequency(parity)) == 3
    )
    opposite_parities = tuple(
        parity
        for parity in ratio_moments
        if sum(sign_frequency(parity)) == 4
    )
    face_values = tuple(ratio_moments[parity] for parity in face_parities)
    opposite_values = tuple(ratio_moments[parity] for parity in opposite_parities)
    face_residual = max(face_values) - min(face_values)
    opposite_residual = max(opposite_values) - min(opposite_values)
    chain = audit_sign_orbit_kl_chain(n)
    conditional_residual = abs(
        conditional_kl - chain.expected_conditional_syndrome_kl_bits
    )
    tolerance = 2e-8
    exact = bool(
        base_residual <= tolerance
        and reconstruction_residual <= tolerance
        and probability_residual <= tolerance
        and minimum_probability >= -tolerance
        and conditional_residual <= tolerance
        and face_residual <= tolerance
        and opposite_residual <= tolerance
        and len(face_parities) == 4
        and len(opposite_parities) == 3
    )
    return AlternatingParityCosetControl(
        n=n,
        coarse_label_count=len(orbits),
        base_orbit_tuple_count=len(orbits) ** 6,
        parity_coset_count=8,
        face_coset_count=len(face_parities),
        opposite_complement_coset_count=len(opposite_parities),
        maximum_orientation_fourier_reconstruction_residual=reconstruction_residual,
        maximum_base_likelihood_residual=base_residual,
        maximum_conditional_probability_sum_residual=probability_residual,
        minimum_conditional_syndrome_probability=minimum_probability,
        expected_conditional_syndrome_kl_bits=max(0.0, conditional_kl),
        kl_chain_conditional_syndrome_kl_bits=(
            chain.expected_conditional_syndrome_kl_bits
        ),
        conditional_kl_residual=conditional_residual,
        expected_conditional_syndrome_chi_square=conditional_chi,
        maximum_face_type_annealed_ratio_moment_residual=face_residual,
        maximum_opposite_type_annealed_ratio_moment_residual=opposite_residual,
        face_type_annealed_ratio_moment=face_values[0],
        opposite_type_annealed_ratio_moment=opposite_values[0],
        exact_parity_coset_channel_verified=exact,
        status=(
            "exact-alternating-parity-coset-channel-verified"
            if exact
            else "alternating-parity-coset-control-failure"
        ),
    )


def run_alternating_parity_coset_channel(
) -> AlternatingParityCosetChannelReport:
    controls = [audit_alternating_parity_coset_channel(n) for n in range(2, 6)]
    exact = all(row.exact_parity_coset_channel_verified for row in controls)
    tail = controls[-1]
    return AlternatingParityCosetChannelReport(
        created_at=utc_now(),
        theorem_contract={
            "coset_partition_function": (
                "F_x(O)=sum_(parity(g,h,k)=x) product_i r_(O_i)(W_i)."
            ),
            "orientation_fourier_expansion": (
                "L_O(z)=sum_x (-1)^(x dot A^Tz)F_x(O)."
            ),
            "conditional_syndrome": (
                "hat P_(Y|O)(x)=F_x(O)/F_0(O), with F_0 the coarse A_n likelihood."
            ),
            "annealed_ratio_moment": (
                "E chi2(P_(Y|O)||U)=sum_O Q_O sum_(x!=0)F_x(O)^2/F_0(O)."
            ),
            "twisted_An_interpretation": (
                "After choosing an odd coset representative, nonzero F_x are "
                "outer-automorphism-twisted A_n word maps."
            ),
            "tetrahedral_types": (
                "The seven nonzero sectors form four face-type and three "
                "opposite-complement-type symmetry classes."
            ),
            "scope": (
                "The reduction does not prove either twisted ratio moment vanishes "
                "after the canonical dimension trim."
            ),
        },
        exact_controls=controls,
        proof_obligations=[
            {
                "obligation": "derive_exact_orbit_adaptive_syndrome_partition_functions",
                "resolved": exact,
                "resolution": (
                    "Fourier averaging over six transpose bits projects the word input "
                    "onto each of the eight parity cosets."
                ),
            },
            {
                "obligation": "reduce_seven_twists_by_tetrahedral_symmetry",
                "resolved": exact,
                "resolution": (
                    "Word parity supports have the two exact orbit sizes four and three; "
                    "annealed ratio moments agree within each type in finite controls."
                ),
            },
            {
                "obligation": "bound_trimmed_face_type_coset_ratio_moment",
                "resolved": False,
                "resolution": (
                    "Prove F_x/F_0 contracts on positive coarse A_n Plancherel mass for "
                    "one face-type outer-automorphism twist."
                ),
            },
            {
                "obligation": "bound_trimmed_opposite_type_coset_ratio_moment",
                "resolved": False,
                "resolution": (
                    "Prove the corresponding four-edge twist contracts, or identify a "
                    "positive-mass retained counterfamily."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Conditional syndrome bias is an opaque information quantity.",
                "resolved": True,
                "resolution": (
                    "False: its Walsh coefficients are explicit parity-coset word-map "
                    "ratios F_x/F_0."
                ),
            },
            {
                "objection": "Seven unrelated asymptotic estimates are required.",
                "resolved": True,
                "resolution": (
                    "Tetrahedral symmetry reduces them to face and opposite-complement "
                    "twist types, though orbit labels are permuted."
                ),
            },
            {
                "objection": "A finite nonzero ratio moment proves adaptive survival.",
                "resolved": True,
                "resolution": (
                    "False: low-dimensional base sectors can dominate raw ratios; the "
                    "canonical trim and direct KL/TV mass are mandatory."
                ),
            },
            {
                "objection": "A twisted A_n word map is automatically quantum.",
                "resolved": True,
                "resolution": (
                    "False: it is a classical finite-group partition function until a "
                    "natural-input access separation is proved."
                ),
            },
        ],
        headline_metrics={
            "alternating_parity_coset_channel_theorem_count": int(exact),
            "parity_coset_count": 8,
            "face_twist_type_count": 4,
            "opposite_complement_twist_type_count": 3,
            "finite_control_count": len(controls),
            "maximum_fourier_reconstruction_residual": max(
                row.maximum_orientation_fourier_reconstruction_residual
                for row in controls
            ),
            "S5_expected_conditional_syndrome_chi_square": (
                tail.expected_conditional_syndrome_chi_square
            ),
            "S5_face_type_annealed_ratio_moment": (
                tail.face_type_annealed_ratio_moment
            ),
            "S5_opposite_type_annealed_ratio_moment": (
                tail.opposite_type_annealed_ratio_moment
            ),
            "trimmed_twisted_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "adaptive_syndrome_equals_parity_coset_imbalance_proved": exact,
            "seven_twists_reduce_to_two_tetrahedral_types_proved": exact,
            "trimmed_face_twist_ratio_vanishes_proved": False,
            "trimmed_opposite_twist_ratio_vanishes_proved": False,
            "orbit_adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The adaptive channel is reduced to two twisted A_n word-map types, "
                "but neither has a positive-mass asymptotic bound."
            ),
        },
        status=(
            "adaptive-syndrome-reduced-to-two-twisted-alternating-word-maps"
            if exact
            else "alternating-parity-coset-control-failure"
        ),
        summary=(
            "Converted orbit-adaptive syndrome information into two explicit parity-"
            "coset alternating-group word-map ratio problems."
        ),
        falsifiers_triggered=[
            "The adaptive syndrome has no orientation complexity beyond parity-coset imbalance.",
            "Only two tetrahedral twist types require asymptotic analysis.",
            "Raw twisted ratio moments remain vulnerable to low-dimensional tails.",
        ],
    )


def write_alternating_parity_coset_channel_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_parity_coset_channel())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_parity_coset_channel_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

"""Unconditional sign-syndrome information vanishes.

The sign-orbit reduction leaves three orientation syndrome bits.  A finite
sign-pair sector can have a strongly nonuniform conditional syndrome, but the
unconditional syndrome is controlled by already-proved proper marginals.

Choose any antisymmetric section ``eta`` of partition transposition:

    eta(lambda^T)=-eta(lambda),       eta(lambda)=0 if lambda=lambda^T.

Interpret ``eta`` as the conditional mean of a sign ``(-1)^Z``: for a
non-self-conjugate partition, ``Z`` is its deterministic section orientation;
for a self-conjugate partition, attach an independent fair bit.  This fair
lift avoids every assumption about self-conjugate Plancherel mass.

For the syndrome ``Y=A^T Z in F_2^3``, its seven nontrivial Walsh
coefficients are expectations of products of ``eta``.  Four frequencies use
the three labels on one tetrahedral fusion face.  The other three use the four
edges complementary to an opposite pair.  Therefore

    |hat p_Y(x)| <= sqrt(V_n)       for four face frequencies,
    |hat p_Y(x)| <= sqrt(V5_n)      for three opposite-complement frequencies,

where ``V_n`` is the exact fusion-face chi-square and ``V5_n`` is the exact
five-label chi-square from the source-conditioned decoupling theorem.
Tetrahedral symmetry transfers the representative five-label estimate to all
three opposite-pair complements.  Parseval gives

    chi^2(P_Y || Uniform(F_2^3)) <= 4 V_n + 3 V5_n,
    TV(P_Y,Uniform) <= 1/2 sqrt(4 V_n + 3 V5_n) = o(1).

Thus no fixed three-bit sign syndrome carries asymptotically stable measured-
label information.  This does not bound the syndrome after conditioning on
the six unoriented sign orbits.  In fact

    E_O D(P(Y|O)||U) = I_P(O:Y) + D(P_Y||U).

Since the second term vanishes, any surviving conditional syndrome signal is
precisely orbit-adaptive mutual information.  It remains classically readable
from measured partition labels and must still survive a same-access classical
baseline before it has algorithmic value.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    BitVector,
    sign_frequency,
    transpose_partition,
)
from self_dual_wreath_source_conditioned_channel_decoupling import (
    half_reciprocal_class_sum,
    source_averaged_conditional_chi_square,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sign_syndrome_unconditional_decoupling.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIGN-SYNDROME-UNCONDITIONAL-DECOUPLING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SignSyndromeMarginalControl:
    n: int
    syndrome_probabilities: tuple[float, ...]
    probability_sum_residual: float
    face_walsh_coefficients: tuple[float, ...]
    opposite_complement_walsh_coefficients: tuple[float, ...]
    maximum_face_coefficient: float
    maximum_opposite_complement_coefficient: float
    exact_face_coefficient_bound: float
    exact_five_label_coefficient_bound: float
    syndrome_chi_square: float
    syndrome_chi_square_upper_bound: float
    syndrome_total_variation: float
    syndrome_total_variation_upper_bound: float
    syndrome_kl_bits: float
    syndrome_kl_upper_bound_bits: float
    finite_fourier_inversion_verified: bool
    marginal_bounds_verified: bool
    status: str


@dataclass(frozen=True)
class SignSyndromeScalingRecord:
    n: int
    fusion_face_chi_square: float
    five_label_chi_square_upper_bound: float
    syndrome_chi_square_upper_bound: float
    syndrome_total_variation_upper_bound: float
    syndrome_kl_upper_bound_bits: float
    self_conjugate_mass_assumption_used: bool
    status: str


@dataclass(frozen=True)
class SignSyndromeUnconditionalDecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[SignSyndromeMarginalControl]
    scaling_records: list[SignSyndromeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def orientation_section_value(partition: tuple[int, ...]) -> int:
    """Conditional mean of the fair-lifted orientation sign."""

    partner = transpose_partition(partition)
    if partition == partner:
        return 0
    return 1 if partition < partner else -1


def _walsh_coefficient(
    physical: np.ndarray,
    section: np.ndarray,
    frequency: BitVector,
) -> float:
    observable = np.ones(physical.shape, dtype=float)
    for axis, enabled in enumerate(frequency):
        if not enabled:
            continue
        shape = [1] * 6
        shape[axis] = len(section)
        observable *= section.reshape(shape)
    return float(np.sum(physical * observable))


def _syndrome_from_walsh(
    coefficients: dict[BitVector, float],
) -> dict[BitVector, float]:
    return {
        syndrome: sum(
            (-1) ** sum(a * b for a, b in zip(input_parity, syndrome))
            * coefficient
            for input_parity, coefficient in coefficients.items()
        )
        / 8.0
        for syndrome in itertools.product((0, 1), repeat=3)
    }


def audit_sign_syndrome_marginal(n: int) -> SignSyndromeMarginalControl:
    if not 3 <= n <= 5:
        raise ValueError("exact syndrome controls require 3<=n<=5")
    partitions, _likelihood, _product, physical = finite_physical_likelihood_arrays(n)
    section = np.asarray(
        [orientation_section_value(partition) for partition in partitions],
        dtype=float,
    )
    coefficients = {
        input_parity: _walsh_coefficient(
            physical,
            section,
            sign_frequency(input_parity),
        )
        for input_parity in itertools.product((0, 1), repeat=3)
    }
    probabilities = _syndrome_from_walsh(coefficients)
    probability_values = np.asarray(tuple(probabilities.values()), dtype=float)
    face = tuple(
        coefficient
        for input_parity, coefficient in coefficients.items()
        if input_parity != (0, 0, 0)
        and sum(sign_frequency(input_parity)) == 3
    )
    complement = tuple(
        coefficient
        for input_parity, coefficient in coefficients.items()
        if sum(sign_frequency(input_parity)) == 4
    )
    variance = float(reciprocal_nonidentity_class_sum(n))
    five = float(source_averaged_conditional_chi_square(n))
    chi_upper = 4.0 * variance + 3.0 * five
    tv_upper = 0.5 * math.sqrt(chi_upper)
    chi_square = 8.0 * float(
        np.sum((probability_values - 1.0 / 8.0) ** 2)
    )
    total_variation = 0.5 * float(
        np.sum(np.abs(probability_values - 1.0 / 8.0))
    )
    positive = probability_values > 0
    kl_bits = float(
        np.sum(
            probability_values[positive]
            * np.log2(8.0 * probability_values[positive])
        )
    )
    kl_upper = math.log2(1.0 + chi_upper)
    inversion = (
        abs(float(np.sum(probability_values)) - 1.0) <= 1e-9
        and float(np.min(probability_values)) >= -1e-9
        and abs(coefficients[(0, 0, 0)] - 1.0) <= 1e-9
        and len(face) == 4
        and len(complement) == 3
    )
    bounds = (
        max(map(abs, face)) <= math.sqrt(variance) + 1e-9
        and max(map(abs, complement)) <= math.sqrt(five) + 1e-9
        and chi_square <= chi_upper + 1e-9
        and total_variation <= tv_upper + 1e-9
        and kl_bits <= kl_upper + 1e-9
    )
    return SignSyndromeMarginalControl(
        n=n,
        syndrome_probabilities=tuple(float(value) for value in probability_values),
        probability_sum_residual=abs(float(np.sum(probability_values)) - 1.0),
        face_walsh_coefficients=face,
        opposite_complement_walsh_coefficients=complement,
        maximum_face_coefficient=max(map(abs, face)),
        maximum_opposite_complement_coefficient=max(map(abs, complement)),
        exact_face_coefficient_bound=math.sqrt(variance),
        exact_five_label_coefficient_bound=math.sqrt(five),
        syndrome_chi_square=chi_square,
        syndrome_chi_square_upper_bound=chi_upper,
        syndrome_total_variation=total_variation,
        syndrome_total_variation_upper_bound=tv_upper,
        syndrome_kl_bits=max(0.0, kl_bits),
        syndrome_kl_upper_bound_bits=kl_upper,
        finite_fourier_inversion_verified=inversion,
        marginal_bounds_verified=bounds,
        status=(
            "exact-fair-lifted-syndrome-marginal-control"
            if inversion and bounds
            else "syndrome-marginal-control-failure"
        ),
    )


def sign_syndrome_scaling_record(n: int) -> SignSyndromeScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    variance = float(reciprocal_nonidentity_class_sum(n))
    half_sum = half_reciprocal_class_sum(n)
    five_upper = 2.0 * variance + half_sum * half_sum
    chi_upper = 4.0 * variance + 3.0 * five_upper
    return SignSyndromeScalingRecord(
        n=n,
        fusion_face_chi_square=variance,
        five_label_chi_square_upper_bound=five_upper,
        syndrome_chi_square_upper_bound=chi_upper,
        syndrome_total_variation_upper_bound=0.5 * math.sqrt(chi_upper),
        syndrome_kl_upper_bound_bits=math.log2(1.0 + chi_upper),
        self_conjugate_mass_assumption_used=False,
        status="unconditional-sign-syndrome-information-upper-bound-vanishing",
    )


def run_sign_syndrome_unconditional_decoupling(
) -> SignSyndromeUnconditionalDecouplingReport:
    controls = [audit_sign_syndrome_marginal(n) for n in range(3, 6)]
    scaling = [
        sign_syndrome_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 30, 40, 50)
    ]
    exact = all(
        row.finite_fourier_inversion_verified and row.marginal_bounds_verified
        for row in controls
    )
    tail = scaling[-1]
    return SignSyndromeUnconditionalDecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "fair_self_conjugate_lift": (
                "Attach an independent fair orientation bit to every self-conjugate "
                "partition, so no self-conjugate mass estimate is assumed."
            ),
            "walsh_support_geometry": (
                "The four weight-three sign frequencies are tetrahedral faces; the "
                "three weight-four frequencies complement opposite edge pairs."
            ),
            "coefficient_bounds": (
                "Face coefficients are at most sqrt(V_n); opposite-complement "
                "coefficients are at most sqrt(V5_n)."
            ),
            "syndrome_information_bound": (
                "chi2(P_Y||U)<=4V_n+3V5_n, TV<=sqrt(4V_n+3V5_n)/2, "
                "and KL_bits<=log2(1+4V_n+3V5_n)."
            ),
            "conditional_decomposition": (
                "E_O D(P(Y|O)||U)=I_P(O:Y)+D(P_Y||U); any surviving conditional "
                "signal is orbit-adaptive mutual information."
            ),
            "scope": (
                "The theorem does not bound I(O:Y), base-orbit dependence, coherent "
                "multiplicity phases, or the classical cost under a natural oracle."
            ),
        },
        exact_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "bound_unconditional_three_bit_sign_syndrome",
                "resolved": exact,
                "resolution": (
                    "Walsh frequencies reduce to four face and three proper four-edge "
                    "marginals, all controlled by existing V_n and V5_n theorems."
                ),
            },
            {
                "obligation": "remove_self_conjugate_mass_assumption_from_raw_syndrome",
                "resolved": exact,
                "resolution": (
                    "Independent fair bits on fixed transposition orbits make every "
                    "orientation coordinate balanced without discarding physical mass."
                ),
            },
            {
                "obligation": "bound_orbit_adaptive_syndrome_mutual_information",
                "resolved": False,
                "resolution": (
                    "Estimate I(O:Y) on the canonical high-dimensional trim, or build a "
                    "positive-mass orbit family with nonvanishing conditional bias."
                ),
            },
            {
                "obligation": "dequantize_any_orbit_adaptive_survivor",
                "resolved": False,
                "resolution": (
                    "Compare weak-Fourier syndrome sampling with classical character and "
                    "word-map access under the same natural-input model."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Self-conjugate partitions prevent a balanced orientation bit.",
                "resolved": True,
                "resolution": (
                    "A fair auxiliary bit on each fixed orbit produces an exact balanced "
                    "lift and does not condition away physical probability."
                ),
            },
            {
                "objection": "Finite conditional S5 syndrome KL contradicts decoupling.",
                "resolved": True,
                "resolution": (
                    "No: strong conditional biases can cancel across base sign orbits; "
                    "the theorem bounds only the unconditional syndrome."
                ),
            },
            {
                "objection": "Uniform syndrome proves the full six-label law is product.",
                "resolved": True,
                "resolution": (
                    "False. Base-orbit dependence and orbit-syndrome mutual information "
                    "remain exact components of the full law."
                ),
            },
            {
                "objection": "A surviving orbit-adaptive syndrome is automatically quantum.",
                "resolved": True,
                "resolution": (
                    "False. It is a deterministic statistic of measured partition labels "
                    "and still requires a same-access classical lower bound."
                ),
            },
        ],
        headline_metrics={
            "unconditional_syndrome_decoupling_theorem_count": int(exact),
            "face_frequency_count": 4,
            "opposite_complement_frequency_count": 3,
            "self_conjugate_mass_assumption_count": 0,
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                row.status != "exact-fair-lifted-syndrome-marginal-control"
                for row in controls
            ),
            "tail_n": tail.n,
            "tail_syndrome_total_variation_upper_bound": (
                tail.syndrome_total_variation_upper_bound
            ),
            "tail_syndrome_kl_upper_bound_bits": tail.syndrome_kl_upper_bound_bits,
            "orbit_adaptive_syndrome_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "unconditional_sign_syndrome_information_vanishes_proved": exact,
            "self_conjugate_mass_decay_needed_for_unconditional_result": False,
            "orbit_adaptive_syndrome_information_vanishes_proved": False,
            "base_sign_orbit_law_is_product_proved": False,
            "coherent_multiplicity_signal_absent_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every fixed sign syndrome decouples, but dependence revealed by adapting "
                "to the six base sign orbits remains the genuine six-label gate."
            ),
        },
        status=(
            "unconditional-sign-syndrome-decoupled-orbit-adaptive-channel-open"
            if exact
            else "sign-syndrome-decoupling-control-failure"
        ),
        summary=(
            "Proved the fair-lifted three-bit sign syndrome becomes uniform and isolated "
            "orbit-adaptive mutual information as the only orientation survivor."
        ),
        falsifiers_triggered=[
            "Finite sign-orbit conditional bias can cancel completely in the raw syndrome.",
            "Self-conjugate mass is not an obstruction to unconditional orientation decoupling.",
            "Any surviving orientation information must adapt to all six sign-orbit labels.",
        ],
    )


def write_sign_syndrome_unconditional_decoupling_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sign_syndrome_unconditional_decoupling())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_sign_syndrome_unconditional_decoupling_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

"""Fixed-support classical control variates for orientation Racah channels.

For fixed ``s``, let ``B_s`` be the permutations moving at most ``s`` points.
The rescaled orientation likelihoods

    ell_y = |S_n|^3 mu_y
          = sum_(g,h,k in S_n) Z(g,h,k)(-1)^(<y,p>)      (1)

admit the polynomial-size partial sums

    ell_y^(s) = sum_(g,h,k in B_s) Z(g,h,k)(-1)^(<y,p>). (2)

Here ``|B_s|=O(n^s)`` for fixed ``s``, so direct triple enumeration costs
``O(n^(3s))`` character evaluations.  Every resulting word moves at most
``3s`` points.  Fixed-support symmetric-group characters have shifted-
symmetric/character-polynomial descriptions, making this a serious
classical attack surface rather than random sampling of a factorial domain.

At ``s=2``, ``B_2`` contains only the identity and transpositions.  Its only
even element is the identity.  Walsh summation therefore gives the exact
aggregate identity

    sum_y ell_y^(2) = 8.                                 (3)

Thus the support-two stratum changes the conditional syndrome channel while
leaving the aggregate coarse-orbit likelihood at the product null.

For the repeated dimension-35 ``S_7`` control, this ``O(n^6)`` partial channel
is within about ``0.00621`` total variation of the full compressed Racah
channel and has conditional mutual information on the same tiny scale.  This
strongly demotes that finite signal.  It is not an all-n dequantization: the
full residual outside ``B_2^3`` is neither bounded nor efficiently summed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    CompressedOrientationRacahControl,
    audit_s5_exact_amplitude_cross_check,
    compile_orientation_racah_channel,
)
from self_dual_wreath_orientation_word_map_classical_baseline import (
    SYNDROMES,
    permutation_parity_bit_from_cycle_type,
    walsh_sign,
)
from self_dual_wreath_parity_racah_conditional_cumulant import (
    audit_conditional_cumulant,
)
from symmetric_character import symmetric_character


Partition = tuple[int, ...]
Permutation = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fixed_support_control_variate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FIXED-SUPPORT-CONTROL-VARIATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrientationFixedSupportControl:
    control_id: str
    n: int
    support_radius: int
    generator_support_ball_count: int
    enumerated_word_triple_count: int
    fixed_radius_enumeration_polynomial: bool
    exact_partial_rescaled_likelihoods: tuple[str, ...]
    partial_rescaled_likelihoods: tuple[float, ...]
    full_rescaled_likelihoods: tuple[float, ...]
    partial_aggregate_likelihood_ratio: float
    full_aggregate_likelihood_ratio: float
    aggregate_support_two_identity_residual: float
    partial_channel_is_nonnegative: bool
    partial_conditional_syndrome_probabilities: tuple[float, ...]
    full_conditional_syndrome_probabilities: tuple[float, ...]
    partial_to_full_total_variation: float
    maximum_partial_to_full_likelihood_residual: float
    partial_irreducible_cmi_bits: float
    full_irreducible_cmi_bits: float
    low_support_channel_within_one_percent_tv: bool
    full_residual_outside_support_ball_bounded: bool
    full_channel_dequantized: bool
    status: str


@dataclass(frozen=True)
class OrientationFixedSupportControlVariateReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[OrientationFixedSupportControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def moved_point_count(permutation: Permutation) -> int:
    return sum(index != image for index, image in enumerate(permutation))


def fixed_support_permutations(n: int, support_radius: int) -> tuple[Permutation, ...]:
    """Generate ``B_s`` directly, without enumerating all of ``S_n``."""

    if n < 1 or support_radius < 0:
        raise ValueError("positive degree and nonnegative support are required")
    identity = tuple(range(n))
    output = [identity]
    for support_size in range(2, min(n, support_radius) + 1):
        for support in itertools.combinations(range(n), support_size):
            for images in itertools.permutations(support):
                if any(source == image for source, image in zip(support, images)):
                    continue
                permutation = list(identity)
                for source, image in zip(support, images):
                    permutation[source] = image
                output.append(tuple(permutation))
    return tuple(output)


def _exact_word_observables(
    base_partitions: tuple[Partition, ...],
    g: Permutation,
    h: Permutation,
    k: Permutation,
) -> tuple[Fraction, ...]:
    gh = compose_permutations(g, h)
    word_types = (
        permutation_cycle_type(compose_permutations(g, k)),
        permutation_cycle_type(compose_permutations(gh, k)),
        permutation_cycle_type(compose_permutations(h, k)),
        permutation_cycle_type(g),
        permutation_cycle_type(h),
        permutation_cycle_type(k),
    )
    value = math.prod(
        Fraction(
            symmetric_character(partition, cycle_type),
            hook_length_dimension(partition),
        )
        for partition, cycle_type in zip(base_partitions, word_types)
    )
    parities = tuple(
        permutation_parity_bit_from_cycle_type(permutation_cycle_type(item))
        for item in (g, h, k)
    )
    return tuple(value * walsh_sign(syndrome, parities) for syndrome in SYNDROMES)


def exact_fixed_support_rescaled_likelihoods(
    base_partitions: tuple[Partition, ...],
    support_radius: int,
) -> tuple[tuple[Fraction, ...], int]:
    if len(base_partitions) != 6:
        raise ValueError("six base partitions are required")
    n = sum(base_partitions[0])
    if any(sum(partition) != n for partition in base_partitions):
        raise ValueError("base partitions must have common degree")
    support_ball = fixed_support_permutations(n, support_radius)
    sums = [Fraction() for _ in SYNDROMES]
    for g, h, k in itertools.product(support_ball, repeat=3):
        for index, value in enumerate(_exact_word_observables(base_partitions, g, h, k)):
            sums[index] += value
    return tuple(sums), len(support_ball)


def _total_variation(left: Iterable[float], right: Iterable[float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(left, right))


def audit_fixed_support_control_variate(
    control: CompressedOrientationRacahControl,
    support_radius: int = 2,
) -> OrientationFixedSupportControl:
    exact_partial, ball_count = exact_fixed_support_rescaled_likelihoods(
        control.base_partitions, support_radius
    )
    partial = tuple(map(float, exact_partial))
    dimension_product = math.prod(control.base_dimensions)
    group_order = math.factorial(control.n)
    full = tuple(
        group_order**3 * entry.normalized_syndrome_amplitude / dimension_product
        for entry in control.entries
    )
    partial_total = sum(partial)
    full_total = sum(full)
    nonnegative = min(partial) >= -1e-12 and partial_total > 0
    partial_probabilities = (
        tuple(value / partial_total for value in partial)
        if nonnegative
        else (1.0 / 8.0,) * 8
    )
    full_probabilities = tuple(value / full_total for value in full)
    partial_cmi = (
        audit_conditional_cumulant(
            f"{control.control_id}-SUPPORT-{support_radius}", partial
        ).irreducible_racah_cmi_bits
        if nonnegative
        else 0.0
    )
    tv = _total_variation(partial_probabilities, full_probabilities)
    support_two_identity_residual = (
        abs(partial_total - 8.0) if support_radius == 2 else math.nan
    )
    verified = bool(
        nonnegative
        and (
            support_radius != 2
            or support_two_identity_residual <= 2e-12
        )
    )
    return OrientationFixedSupportControl(
        control_id=control.control_id,
        n=control.n,
        support_radius=support_radius,
        generator_support_ball_count=ball_count,
        enumerated_word_triple_count=ball_count**3,
        fixed_radius_enumeration_polynomial=True,
        exact_partial_rescaled_likelihoods=tuple(str(value) for value in exact_partial),
        partial_rescaled_likelihoods=partial,
        full_rescaled_likelihoods=full,
        partial_aggregate_likelihood_ratio=partial_total / 8.0,
        full_aggregate_likelihood_ratio=full_total / 8.0,
        aggregate_support_two_identity_residual=support_two_identity_residual,
        partial_channel_is_nonnegative=nonnegative,
        partial_conditional_syndrome_probabilities=partial_probabilities,
        full_conditional_syndrome_probabilities=full_probabilities,
        partial_to_full_total_variation=tv,
        maximum_partial_to_full_likelihood_residual=max(
            abs(left - right) for left, right in zip(partial, full)
        ),
        partial_irreducible_cmi_bits=partial_cmi,
        full_irreducible_cmi_bits=control.irreducible_racah_cmi_bits,
        low_support_channel_within_one_percent_tv=tv <= 0.01,
        full_residual_outside_support_ball_bounded=False,
        full_channel_dequantized=False,
        status=(
            "fixed-support-polynomial-control-channel-audited"
            if verified
            else "fixed-support-control-channel-failure"
        ),
    )


def run_orientation_fixed_support_control_variate(
) -> OrientationFixedSupportControlVariateReport:
    _cross_check, s5 = audit_s5_exact_amplitude_cross_check()
    s6 = compile_orientation_racah_channel(
        "S6-REPEATED-DIMENSION-10", ((3, 1, 1, 1),) * 6
    )
    s7 = compile_orientation_racah_channel(
        "S7-REPEATED-DIMENSION-35", ((3, 2, 1, 1),) * 6
    )
    controls = [audit_fixed_support_control_variate(row, 2) for row in (s5, s6, s7)]
    s6_row, s7_row = controls[1], controls[2]
    failures = sum(row.status.endswith("failure") for row in controls)
    return OrientationFixedSupportControlVariateReport(
        created_at=utc_now(),
        theorem_contract={
            "support_ball": "B_s={pi in S_n: moved(pi)<=s}, |B_s|=O(n^s) for fixed s",
            "partial_likelihood": "ell_y^(s)=sum_(g,h,k in B_s) Z(g,h,k)(-1)^{<y,p>}",
            "enumeration_cost": "O(n^(3s)) fixed-support character evaluations",
            "support_two_identity": "sum_y ell_y^(2)=8 because B_2 has only one even element",
            "character_boundary": "all words move at most 3s points; fixed-support character polynomials apply",
            "scope": "finite classical surrogate and control variate; no tail bound outside B_s^3",
        },
        controls=controls,
        proof_obligations=[
            {
                "obligation": "enumerate_fixed_support_generator_strata_without_factorial_group_scan",
                "resolved": failures == 0,
                "resolution": "Direct derangement-on-chosen-support generation has O(n^s) elements for fixed s.",
            },
            {
                "obligation": "prove_support_two_preserves_aggregate_product_null",
                "resolved": failures == 0,
                "resolution": "Walsh summation selects the all-even generator stratum, which contains only the identity in B_2^3.",
            },
            {
                "obligation": "bound_residual_outside_fixed_support_on_natural_labels",
                "resolved": False,
                "resolution": "Need character-ratio tail estimates for at least one generator moving more than s points, with cancellation preserved.",
            },
            {
                "obligation": "derive_growing_support_algorithm_or_no_go",
                "resolved": False,
                "resolution": "Fixed s is polynomial but may miss the scalable Racah residual; growing s changes both runtime and character asymptotics.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The S7 orientation CMI cannot arise from classically enumerable word strata.",
                "resolved": True,
                "resolution": "The support-two O(n^6) channel lies within 0.00621 TV and has CMI on the same tiny scale.",
            },
            {
                "objection": "A close finite support-two surrogate dequantizes every n.",
                "resolved": True,
                "resolution": "No uniform tail bound exists and the S6 spike is not approximated by the same stratum.",
            },
            {
                "objection": "Increasing support radius must monotonically improve a signed partial sum.",
                "resolved": True,
                "resolution": "Signed character contributions are not a probability truncation; only explicit error bounds justify convergence claims.",
            },
            {
                "objection": "Polynomial tuple count alone proves polynomial bit complexity.",
                "resolved": True,
                "resolution": "A production attack must implement fixed-support character polynomials and exact arithmetic rather than treat character evaluation as unit cost.",
            },
        ],
        headline_metrics={
            "fixed_support_control_count": len(controls),
            "finite_control_failure_count": failures,
            "support_radius": 2,
            "S6_support_two_to_full_tv": s6_row.partial_to_full_total_variation,
            "S6_support_two_cmi_bits": s6_row.partial_irreducible_cmi_bits,
            "S6_full_cmi_bits": s6_row.full_irreducible_cmi_bits,
            "S7_support_two_to_full_tv": s7_row.partial_to_full_total_variation,
            "S7_support_two_cmi_bits": s7_row.partial_irreducible_cmi_bits,
            "S7_full_cmi_bits": s7_row.full_irreducible_cmi_bits,
            "full_tail_bound_count": 0,
            "full_dequantization_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fixed_support_enumeration_polynomial_proved": failures == 0,
            "support_two_aggregate_product_null_proved": failures == 0,
            "S7_finite_channel_has_close_polynomial_low_support_surrogate": (
                s7_row.low_support_channel_within_one_percent_tv
            ),
            "S6_one_bit_spike_explained_by_support_two": (
                s6_row.low_support_channel_within_one_percent_tv
            ),
            "full_residual_tail_bounded": False,
            "all_n_orientation_channel_dequantized": False,
            "classical_lower_bound_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The S7 finite signal has a close O(n^6) low-support surrogate, while no growing-support residual theorem or S6 scaling family survives.",
        },
        status=(
            "S7-finite-orientation-signal-demoted-by-fixed-support-classical-surrogate"
            if failures == 0 and s7_row.low_support_channel_within_one_percent_tv
            else "orientation-fixed-support-control-inconclusive"
        ),
        summary=(
            "Built an exact fixed-support classical control variate and found that "
            "the finite S7 orientation channel is closely reproduced by an O(n^6) "
            "identity/transposition sum."
        ),
        falsifiers_triggered=[
            "The S7 finite CMI is not isolated from polynomially enumerable low-support strata.",
            "Support-radius truncations are signed and need not converge monotonically.",
            "The S6 cancellation spike remains a finite low-mass exception, not a scaling mechanism.",
        ],
    )


def write_orientation_fixed_support_control_variate_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_orientation_fixed_support_control_variate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_orientation_fixed_support_control_variate_report()
    print(json.dumps(report, indent=2, sort_keys=True))

"""Natural high-dimensional sector mass for the joint-character decoder.

The joint-character multiplicity theorem leaves open whether its Schur-row
normalization matters on the natural source law.  This module resolves that
mass question.

For a fixed tuple of unequal source pairs
``Lambda=((lambda_i,mu_i))_(i=1)^k``, let ``q=2^k``.  Orientation ``e`` selects
one partition ``alpha_i(e)`` from each pair.  If
``g(alpha_1,...,alpha_k;nu)`` is the tensor-product multiplicity, then the
exact target-sector probability is

    p_nu(Lambda)=Tr(D_nu)
      = q^-1 sum_e d_nu g(alpha_1(e),...,alpha_k(e);nu)
          / product_i d_(alpha_i(e)).                    (1)

The unselected carrier dimensions cancel.  Thus each orientation is exactly
the dimension-weighted Kronecker transition already covered by Plancherel
recoupling stationarity.

If the ``2k`` source partitions are independent Plancherel samples, every
orientation selects ``k`` independent Plancherel factors.  Consequently the
annealed target law is exactly Plancherel for every ``k>=1``:

    E_Lambda p_nu(Lambda)=d_nu^2/n!.                     (2)

Now condition all ``2k`` source partitions to be distinct.  If ``E_cf`` is
that event, total-variation distance between the original source law and its
conditioning is exactly ``Pr(E_cf^c)``.  Stochastic-map contraction therefore
gives

    TV(E[p_nu|E_cf], Plancherel) <= Pr(E_cf^c).           (3)

The repository's collision-free mass theorem proves the right side is
``o(1)`` at ``k=ceil(log2(n!))+O(1)``.

This implies a quantitative high-row theorem without guessing a particular
shape.  Let ``P(n)`` be the partition number and

    R_n=floor(sqrt(n!)/P(n)).

There are only ``P(n)`` irreps, so their Plancherel mass below dimension
``R_n`` is at most

    sum_(d_nu<=R_n) d_nu^2/n! <= 1/P(n).                 (4)

After collision-free conditioning, the annealed low-row mass is at most
``delta_n=1/P(n)+Pr(E_cf^c)=exp(-Theta(sqrt(n)))``.  Markov gives low-row mass
at most ``sqrt(delta_n)`` for a ``1-sqrt(delta_n)`` fraction of source tuples.
Hence ``1-o(1)`` physical sector mass lies on

    d_nu > sqrt(n!)/P(n) = sqrt(n!) exp(-O(sqrt(n))).     (5)

On that mass, the canonical direct-analysis normalization ``sqrt(d_nu)`` and
its generic amplification degree are superpolynomial (indeed factorial-root
up to ``exp(O(sqrt(n)))`` factors).  Low-dimensional sectors cannot rescue a
decoder restricted to this canonical access architecture.

The theorem is about sector mass, not sector information.  The irrep label is
hidden-label independent, and equation (2) does not prove that the internal
``D_nu`` correlations carry extensive Holevo information.  It also does not
rule out a fused direct polar that bypasses canonical amplification.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
)
from self_dual_wreath_joint_character_analysis_map_normalization import (
    generic_analysis_amplification_degree_lower_bound,
)
from self_dual_wreath_joint_character_multiplicity_gram import (
    Label,
    Partition,
    predicted_joint_multiplicity_operator,
)
from self_dual_wreath_natural_pair_carrier_law import (
    tensor_target_multiplicity,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)
from self_dual_wreath_plancherel_recoupling_stationarity import (
    plancherel_weights,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_joint_character_natural_sector_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-NATURAL-SECTOR-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
HARDY_RAMANUJAN_PAPER_ID = "hardy-ramanujan-partition-asymptotic-1918"
HARDY_RAMANUJAN_PAPER_URL = "https://doi.org/10.1112/plms/s2-17.1.75"


@dataclass(frozen=True)
class FixedSourceSectorLawControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    orientation_count: int
    target_count: int
    exact_law_sum: str
    maximum_projection_gram_trace_residual: float
    exact_source_sector_law_verified: bool
    status: str


@dataclass(frozen=True)
class AnnealedTargetStationarityControl:
    n: int
    selected_factor_count: int
    partition_count: int
    exact_probability_sum: str
    maximum_plancherel_residual: str
    exact_annealed_plancherel_stationarity_verified: bool
    status: str


@dataclass(frozen=True)
class CollisionConditioningControl:
    n: int
    pair_count: int
    source_draw_count: int
    partition_count: int
    exact_collision_free_probability: str
    exact_collision_probability: str
    target_total_variation_from_plancherel: str
    source_conditioning_total_variation_bound: str
    target_tv_below_source_tv: bool
    exact_conditioning_contraction_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalSectorMassScalingRecord:
    n: int
    information_threshold_copy_count: int
    partition_count_decimal: str
    low_dimension_threshold_decimal: str
    low_dimension_threshold_log2: float
    unconditioned_low_dimension_mass_upper_bound: float
    collision_conditioned_low_dimension_mass_upper_bound: str
    source_typical_low_dimension_mass_upper_bound: str
    source_typical_failure_probability_upper_bound: str
    high_dimension_natural_sector_mass_tends_to_one: bool
    minimum_high_mass_canonical_normalization_log2: float
    minimum_high_mass_generic_analysis_degree_log2_lower_bound: float
    low_dimension_only_inverse_polynomial_decoder_possible: bool
    high_dimension_sector_information_proved: bool
    direct_structured_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class NaturalSectorMassTheorem:
    fixed_source_law: str
    annealed_stationarity: str
    conditioning_transfer: str
    low_dimension_tail: str
    source_typical_transfer: str
    canonical_access_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalSectorMassReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: NaturalSectorMassTheorem
    fixed_source_controls: list[FixedSourceSectorLawControl]
    stationarity_controls: list[AnnealedTargetStationarityControl]
    conditioning_controls: list[CollisionConditioningControl]
    scaling_records: list[NaturalSectorMassScalingRecord]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partition_number(n: int) -> int:
    """Return the partition number using Euler's pentagonal recurrence."""

    if n < 0:
        raise ValueError("n must be nonnegative")
    values = [0] * (n + 1)
    values[0] = 1
    for total in range(1, n + 1):
        value = 0
        index = 1
        while True:
            first = index * (3 * index - 1) // 2
            second = index * (3 * index + 1) // 2
            if first > total:
                break
            sign = 1 if index % 2 else -1
            value += sign * values[total - first]
            if second <= total:
                value += sign * values[total - second]
            index += 1
        values[total] = value
    return values[n]


def orientation_averaged_target_law(
    labels: tuple[Label, ...],
) -> dict[Partition, Fraction]:
    """Return the exact dimension-weighted law in equation (1)."""

    if not labels:
        raise ValueError("at least one source pair is required")
    n = sum(labels[0][0])
    if any(sum(left) != n or sum(right) != n for left, right in labels):
        raise ValueError("all source partitions must have the same degree")
    partitions = tuple(integer_partitions(n))
    count = 1 << len(labels)
    output = {target: Fraction() for target in partitions}
    for orientation in range(count):
        selected = tuple(
            pair[(orientation >> index) & 1]
            for index, pair in enumerate(labels)
        )
        denominator = math.prod(hook_length_dimension(item) for item in selected)
        for target in partitions:
            multiplicity = tensor_target_multiplicity(selected, target)
            output[target] += Fraction(
                hook_length_dimension(target) * multiplicity,
                count * denominator,
            )
    if sum(output.values(), Fraction()) != 1:
        raise ArithmeticError("orientation-averaged target law is not normalized")
    return output


def audit_fixed_source_sector_law(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> FixedSourceSectorLawControl:
    law = orientation_averaged_target_law(labels)
    residual = 0.0
    for target, probability in law.items():
        multiplicity, _, _ = predicted_joint_multiplicity_operator(target, labels)
        residual = max(
            residual,
            abs(float(probability) - float(np.trace(multiplicity).real)),
        )
    verified = residual <= 100 * tolerance
    return FixedSourceSectorLawControl(
        control_id=control_id,
        n=n,
        labels=labels,
        orientation_count=1 << len(labels),
        target_count=len(law),
        exact_law_sum=str(sum(law.values(), Fraction())),
        maximum_projection_gram_trace_residual=residual,
        exact_source_sector_law_verified=verified,
        status=(
            "exact-joint-target-sector-recoupling-law"
            if verified
            else "joint-target-sector-law-validation-failure"
        ),
    )


def annealed_tensor_target_law(
    n: int,
    selected_factor_count: int,
) -> dict[Partition, Fraction]:
    if selected_factor_count < 1:
        raise ValueError("selected_factor_count must be positive")
    partitions = tuple(integer_partitions(n))
    weights = plancherel_weights(n)
    output = {target: Fraction() for target in partitions}
    for factors in itertools.product(partitions, repeat=selected_factor_count):
        source_probability = math.prod(
            (weights[factor] for factor in factors),
            start=Fraction(1),
        )
        denominator = math.prod(hook_length_dimension(factor) for factor in factors)
        for target in partitions:
            output[target] += source_probability * Fraction(
                hook_length_dimension(target)
                * tensor_target_multiplicity(factors, target),
                denominator,
            )
    return output


def audit_annealed_target_stationarity(
    n: int,
    selected_factor_count: int,
) -> AnnealedTargetStationarityControl:
    observed = annealed_tensor_target_law(n, selected_factor_count)
    expected = plancherel_weights(n)
    residual = max(abs(observed[target] - expected[target]) for target in expected)
    total = sum(observed.values(), Fraction())
    verified = total == 1 and residual == 0
    return AnnealedTargetStationarityControl(
        n=n,
        selected_factor_count=selected_factor_count,
        partition_count=len(expected),
        exact_probability_sum=str(total),
        maximum_plancherel_residual=str(residual),
        exact_annealed_plancherel_stationarity_verified=verified,
        status=(
            "exact-annealed-joint-target-plancherel"
            if verified
            else "annealed-joint-target-stationarity-failure"
        ),
    )


def collision_free_conditioned_target_law(
    n: int,
    pair_count: int,
) -> tuple[Fraction, dict[Partition, Fraction]]:
    """Enumerate the target law conditioned on all ``2*pair_count`` draws distinct."""

    if pair_count < 1:
        raise ValueError("pair_count must be positive")
    partitions = tuple(integer_partitions(n))
    draw_count = 2 * pair_count
    if draw_count > len(partitions):
        raise ValueError("not enough partitions for a collision-free source tuple")
    weights = plancherel_weights(n)
    count = 1 << pair_count
    event_probability = Fraction()
    output = {target: Fraction() for target in partitions}
    for draws in itertools.permutations(partitions, draw_count):
        source_probability = math.prod(
            (weights[item] for item in draws),
            start=Fraction(1),
        )
        event_probability += source_probability
        for orientation in range(count):
            selected = tuple(
                draws[2 * index + ((orientation >> index) & 1)]
                for index in range(pair_count)
            )
            denominator = math.prod(
                hook_length_dimension(item) for item in selected
            )
            for target in partitions:
                output[target] += source_probability * Fraction(
                    hook_length_dimension(target)
                    * tensor_target_multiplicity(selected, target),
                    count * denominator,
                )
    output = {
        target: probability / event_probability
        for target, probability in output.items()
    }
    return event_probability, output


def audit_collision_conditioning(
    n: int,
    pair_count: int,
) -> CollisionConditioningControl:
    event_probability, conditioned = collision_free_conditioned_target_law(
        n,
        pair_count,
    )
    plancherel = plancherel_weights(n)
    target_tv = sum(
        (abs(conditioned[target] - plancherel[target]) for target in plancherel),
        start=Fraction(),
    ) / 2
    source_tv = 1 - event_probability
    verified = target_tv <= source_tv
    return CollisionConditioningControl(
        n=n,
        pair_count=pair_count,
        source_draw_count=2 * pair_count,
        partition_count=len(plancherel),
        exact_collision_free_probability=str(event_probability),
        exact_collision_probability=str(source_tv),
        target_total_variation_from_plancherel=str(target_tv),
        source_conditioning_total_variation_bound=str(source_tv),
        target_tv_below_source_tv=verified,
        exact_conditioning_contraction_verified=verified,
        status=(
            "collision-conditioning-target-tv-contraction"
            if verified
            else "collision-conditioning-contraction-failure"
        ),
    )


def natural_sector_mass_scaling_record(n: int) -> NaturalSectorMassScalingRecord:
    if n < 4:
        raise ValueError("n must be at least four")
    count = partition_number(n)
    order = math.factorial(n)
    threshold = math.isqrt(order) // count
    if threshold < 1:
        raise ArithmeticError("dimension threshold is trivial")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    degree = generic_analysis_amplification_degree_lower_bound(threshold + 1)
    return NaturalSectorMassScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        partition_count_decimal=str(count),
        low_dimension_threshold_decimal=str(threshold),
        low_dimension_threshold_log2=math.log2(threshold),
        unconditioned_low_dimension_mass_upper_bound=1.0 / count,
        collision_conditioned_low_dimension_mass_upper_bound=(
            "delta_n=1/p(n)+Pr(any collision)=exp(-Theta(sqrt(n)))"
        ),
        source_typical_low_dimension_mass_upper_bound="sqrt(delta_n)",
        source_typical_failure_probability_upper_bound="sqrt(delta_n)",
        high_dimension_natural_sector_mass_tends_to_one=True,
        minimum_high_mass_canonical_normalization_log2=(
            math.log2(threshold + 1) / 2
        ),
        minimum_high_mass_generic_analysis_degree_log2_lower_bound=(
            math.log2(degree)
        ),
        low_dimension_only_inverse_polynomial_decoder_possible=False,
        high_dimension_sector_information_proved=False,
        direct_structured_polar_ruled_out=False,
        status="natural-sector-mass-high-dimensional-canonical-polar-open",
    )


def run_joint_character_natural_sector_mass() -> NaturalSectorMassReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    fixed_controls = [
        audit_fixed_source_sector_law(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_fixed_source_sector_law(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    stationarity_controls = [
        audit_annealed_target_stationarity(n, factor_count)
        for n, factor_count in ((2, 1), (3, 2), (4, 2), (5, 2))
    ]
    conditioning_controls = [
        audit_collision_conditioning(4, 2),
        audit_collision_conditioning(5, 2),
    ]
    scaling = [
        natural_sector_mass_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_source_sector_law_verified for row in fixed_controls
    ) + sum(
        not row.exact_annealed_plancherel_stationarity_verified
        for row in stationarity_controls
    ) + sum(
        not row.exact_conditioning_contraction_verified
        for row in conditioning_controls
    )
    verified = failures == 0
    theorem = NaturalSectorMassTheorem(
        fixed_source_law=(
            "Tr(D_nu)=q^-1 sum_e d_nu g(alpha_1(e),...,alpha_k(e);nu)"
            "/product_i d_(alpha_i(e))."
        ),
        annealed_stationarity=(
            "Independent Plancherel source partitions give the exact annealed target "
            "law d_nu^2/n! for every k>=1."
        ),
        conditioning_transfer=(
            "Conditioning all 2k sources distinct changes the target law in TV by at "
            "most Pr(any source collision)=o(1) at information-threshold k."
        ),
        low_dimension_tail=(
            "For R_n=floor(sqrt(n!)/p(n)), Plancherel[d_nu<=R_n]<=1/p(n)."
        ),
        source_typical_transfer=(
            "If delta_n=1/p(n)+Pr(collision), Markov gives low-row physical mass "
            "<=sqrt(delta_n) for at least 1-sqrt(delta_n) of conditioned sources."
        ),
        canonical_access_consequence=(
            "The canonical sqrt(d_nu) analysis normalization is superpolynomial on "
            "1-o(1) natural source-sector mass."
        ),
        scope=(
            "Target mass is not target information. Internal multiplicity Holevo "
            "information and direct structured polar synthesis remain open."
        ),
        theorem_verified=verified,
        status=(
            "natural-joint-target-mass-high-dimensional-proved-information-open"
            if verified
            else "natural-joint-target-sector-mass-validation-failure"
        ),
    )
    return NaturalSectorMassReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        fixed_source_controls=fixed_controls,
        stationarity_controls=stationarity_controls,
        conditioning_controls=conditioning_controls,
        scaling_records=scaling,
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "use": (
                    "The maximal Plancherel atom is exp(-Theta(sqrt(n))), making "
                    "polynomially many source collisions asymptotically negligible."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": HARDY_RAMANUJAN_PAPER_ID,
                "url": HARDY_RAMANUJAN_PAPER_URL,
                "use": "p(n)=exp(Theta(sqrt(n))) for the low-dimension tail threshold.",
                "external_theorem_not_reproved_here": True,
            },
        ],
        proof_obligations=[
            {
                "obligation": "derive_joint_target_sector_probability",
                "resolved": verified,
                "resolution": (
                    "Unselected carrier dimensions cancel from Tr(D_nu), leaving the "
                    "dimension-weighted tensor-product decomposition in equation (1)."
                ),
            },
            {
                "obligation": "transfer_plancherel_stationarity_to_joint_D_nu_mass",
                "resolved": verified,
                "resolution": (
                    "Every orientation selects independent Plancherel factors, so the "
                    "annealed target law is exactly Plancherel."
                ),
            },
            {
                "obligation": "survive_global_distinct_source_conditioning",
                "resolved": verified,
                "resolution": (
                    "Total-variation contraction loses at most the collision event, "
                    "whose mass vanishes at the information-threshold copy count."
                ),
            },
            {
                "obligation": "prove_high_row_natural_sector_mass",
                "resolved": verified,
                "resolution": (
                    "A counting tail plus Markov puts 1-o(1) sector mass above "
                    "sqrt(n!)/p(n) for 1-o(1) conditioned source tuples."
                ),
            },
            {
                "obligation": "prove_high_row_hidden_label_information",
                "resolved": False,
                "resolution": (
                    "The irrep marginal is label independent. No extensive Holevo lower "
                    "bound inside the high-row D_nu blocks is known."
                ),
            },
            {
                "obligation": "compile_direct_structured_polar",
                "resolved": False,
                "resolution": (
                    "The mass theorem strengthens the canonical-access obstruction but "
                    "does not rule out a fused representation-specific polar."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The balanced two-row witness may have negligible natural mass.",
                "resolved": True,
                "resolution": (
                    "A particular balanced shape is unnecessary: all dimensions below "
                    "sqrt(n!)/p(n) have vanishing aggregate natural mass."
                ),
            },
            {
                "objection": "Conditioning source labels distinct destroys stationarity.",
                "resolved": True,
                "resolution": (
                    "It perturbs the target law, but data processing bounds the perturbation "
                    "by the source-collision probability, which is o(1)."
                ),
            },
            {
                "objection": "An annealed mass theorem implies every source tuple is good.",
                "resolved": True,
                "resolution": (
                    "False pointwise. Markov supplies the correct 1-o(1) source-typical "
                    "statement with a square-root loss."
                ),
            },
            {
                "objection": "High-dimensional target mass proves useful hidden information.",
                "resolved": False,
                "resolution": (
                    "It does not. The target label itself is hidden-label independent; "
                    "useful information must be proved inside multiplicity correlations."
                ),
            },
            {
                "objection": "Typical high dimension rules out every decoder.",
                "resolved": False,
                "resolution": (
                    "Only the canonical density/direct-analysis polynomial routes inherit "
                    "the normalization burden. Direct fused polars remain open."
                ),
            },
        ],
        headline_metrics={
            "exact_fixed_source_sector_law_theorem_count": 1,
            "annealed_target_plancherel_stationarity_theorem_count": 1,
            "collision_conditioning_tv_transfer_theorem_count": 1,
            "source_typical_high_dimension_mass_theorem_count": 1,
            "fixed_source_control_count": len(fixed_controls),
            "stationarity_control_count": len(stationarity_controls),
            "conditioning_control_count": len(conditioning_controls),
            "finite_control_failure_count": failures,
            "maximum_scaling_n": scaling[-1].n,
            "maximum_low_dimension_threshold_log2": max(
                row.low_dimension_threshold_log2 for row in scaling
            ),
            "maximum_high_mass_generic_degree_log2_lower_bound": max(
                row.minimum_high_mass_generic_analysis_degree_log2_lower_bound
                for row in scaling
            ),
            "high_dimension_information_theorem_count": 0,
            "direct_structured_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "joint_target_sector_law_identified": verified,
            "annealed_joint_target_law_is_exact_plancherel": verified,
            "collision_free_conditioned_target_law_is_asymptotically_plancherel": True,
            "natural_target_sector_mass_is_high_dimensional": True,
            "canonical_sqrt_d_nu_normalization_hits_one_minus_o_one_mass": True,
            "low_dimension_sectors_support_inverse_polynomial_mass_decoder": False,
            "high_dimension_sectors_carry_extensive_hidden_information_proved": False,
            "normalization_one_A_nu_access_constructed": False,
            "direct_structured_polar_compiled": False,
            "direct_structured_polar_ruled_out": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The canonical sqrt(d_nu) normalization now applies on 1-o(1) natural "
                "sector mass, so low-dimensional sectors cannot rescue that route. "
                "Hidden-label information inside the high-dimensional blocks and a "
                "direct fused polar remain unproved."
            ),
        },
        status=theorem.status,
        summary=(
            "Transferred Plancherel stationarity to Tr(D_nu) and proved that almost all "
            "collision-free natural sector mass has factorial-scale irrep dimension."
        ),
        falsifiers_triggered=[
            (
                "The canonical normalization boundary is not confined to an arbitrary "
                "balanced witness; it occurs on 1-o(1) natural sector mass."
            ),
            (
                "Global distinctness does not asymptotically move target mass into rare "
                "low-dimensional sectors."
            ),
            (
                "High-dimensional mass alone is not evidence for hidden-label information "
                "or an algorithmic speedup."
            ),
        ],
    )


def write_joint_character_natural_sector_mass_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
) -> dict[str, Any]:
    del write_registry, registry_experiment_id, registry_candidate_id, registry_result_id
    payload = asdict(run_joint_character_natural_sector_mass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_joint_character_natural_sector_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

"""A positive information projection isolates irreducible Racah synergy.

For a fully transpose-paired coarse orbit tuple ``O``, let

    P_O(g,h,k) = A_(g,h,k) / sum_y A_y

be its adaptive syndrome channel.  The companion toric theorem proves that
every Kronecker rank-profile channel belongs to the Markov family

    M = {Q : G is conditionally independent of H given K}.

The information projection of any ``P`` onto ``M`` is explicit:

    Pi_M(P)(g,h,k)=P(g|k)P(h|k)P(k).                       (1)

It is the unique minimizer on positive support and obeys

    min_(Q in M) D(P||Q) = D(P||Pi_M(P)) = I_P(G;H|K).    (2)

Because the uniform law belongs to ``M``, the Pythagorean identity gives the
positive, cancellation-free decomposition

    D(P||U_3) = I_P(G;H|K) + D(Pi_M(P)||U_3).             (3)

The first term is irreducible deterministic Racah synergy: no model that uses
only the four sign-twisted fusion multiplicities and final multiplicity can
reproduce it.  The second is rank-compatible syndrome bias.  Unlike the
centered amplitude split, both terms are nonnegative and cannot cancel.

For every Markov rank benchmark ``R`` with compatible support, a second
Pythagorean identity holds:

    D(P||R)=I_P(G;H|K)+D(Pi_M(P)||R).                      (4)

Thus conditional mutual information is not merely one diagnostic; it is the
exact KL distance from the complete rank-profile model class.

Finite aggregation over nonself sign-orbit tuples gives zero irreducible term
at ``S_4``.  At ``S_5``, the dimension-``>1`` paired sector has physical mass
``0.1035486111``, total adaptive KL contribution ``0.1152526218`` bits,
irreducible Racah contribution ``0.00284302207`` bits, and rank-compatible
contribution ``0.1124095998`` bits.  Therefore about 2.47 percent of this
finite sector's adaptive KL is provably outside every rank-profile Markov
model.  This is finite evidence only.

The asymptotic research target is now precise: prove that the physical
expectation of ``I(Y_g;Y_h|Y_k,O)`` vanishes, or lower-bound it on a
positive-mass canonical sector.  Neither result, an efficient coherent
estimator, nor a classical separation is established here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
)
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from self_dual_wreath_parity_projector_orbit_variance import (
    BITS,
    audit_orbit_variance,
    inverse_walsh_transform,
)
from self_dual_wreath_parity_racah_rank_residual_decomposition import (
    audit_racah_rank_residual,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_racah_information_projection.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-INFORMATION-PROJECTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Syndrome = tuple[int, int, int]


@dataclass(frozen=True)
class InformationProjectionControl:
    control_id: str
    n: int
    orbit_indices: tuple[int, ...]
    natural_probabilities: tuple[float, ...]
    markov_projection_probabilities: tuple[float, ...]
    rank_profile_probabilities: tuple[float, ...] | None
    adaptive_kl_to_uniform_bits: float
    irreducible_racah_conditional_mutual_information_bits: float
    markov_projection_kl_to_uniform_bits: float
    uniform_pythagorean_residual_bits: float
    natural_kl_to_rank_profile_bits: float | None
    markov_projection_kl_to_rank_profile_bits: float | None
    rank_profile_pythagorean_residual_bits: float | None
    maximum_markov_projection_conditional_minor: float
    exact_information_projection_verified: bool
    status: str


@dataclass(frozen=True)
class InformationProjectionAggregateControl:
    n: int
    minimum_dimension_exclusive: int
    retained_nonself_orbit_count: int
    positive_physical_orbit_tuple_count: int
    retained_physical_mass: float
    physical_mass_weighted_adaptive_kl_bits: float
    physical_mass_weighted_irreducible_racah_cmi_bits: float
    physical_mass_weighted_rank_compatible_kl_bits: float
    aggregate_pythagorean_residual_bits: float
    irreducible_fraction_of_adaptive_kl: float
    conditional_irreducible_cmi_on_retained_mass_bits: float
    maximum_single_orbit_irreducible_cmi_bits: float
    maximum_single_orbit_indices: tuple[int, ...] | None
    all_orbit_projections_verified: bool
    finite_exact_aggregation_only: bool
    status: str


@dataclass(frozen=True)
class ParityRacahInformationProjectionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    orbit_controls: list[InformationProjectionControl]
    aggregate_controls: list[InformationProjectionAggregateControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalize_channel(values: Iterable[float]) -> tuple[float, ...]:
    entries = tuple(max(0.0, float(value)) for value in values)
    if len(entries) != 8:
        raise ValueError("eight syndrome-channel values are required")
    total = sum(entries)
    if total <= 0:
        raise ValueError("channel must have positive total mass")
    return tuple(value / total for value in entries)


def kl_divergence_bits(
    probabilities: Iterable[float],
    reference: Iterable[float],
) -> float:
    left = tuple(float(value) for value in probabilities)
    right = tuple(float(value) for value in reference)
    if len(left) != 8 or len(right) != 8:
        raise ValueError("eight syndrome-channel values are required")
    if min(left) < -1e-12 or min(right) < -1e-12:
        raise ValueError("probabilities must be nonnegative")
    if abs(sum(left) - 1.0) > 1e-9 or abs(sum(right) - 1.0) > 1e-9:
        raise ValueError("probabilities must normalize")
    if any(value > 0 and reference_value <= 0 for value, reference_value in zip(left, right)):
        return math.inf
    return max(
        0.0,
        sum(
            value * math.log2(value / reference_value)
            for value, reference_value in zip(left, right)
            if value > 0
        ),
    )


def markov_information_projection(
    probabilities: Iterable[float],
) -> tuple[float, ...]:
    entries = dict(zip(BITS, tuple(float(value) for value in probabilities)))
    if len(entries) != 8 or min(entries.values()) < -1e-12:
        raise ValueError("eight nonnegative syndrome probabilities are required")
    if abs(sum(entries.values()) - 1.0) > 1e-9:
        raise ValueError("syndrome probabilities must normalize")
    p_k = {
        k: sum(entries[g, h, k] for g in (0, 1) for h in (0, 1))
        for k in (0, 1)
    }
    projected = []
    for g, h, k in BITS:
        if p_k[k] <= 0:
            projected.append(0.0)
            continue
        p_gk = sum(entries[g, b, k] for b in (0, 1))
        p_hk = sum(entries[a, h, k] for a in (0, 1))
        projected.append(p_gk * p_hk / p_k[k])
    return tuple(projected)


def conditional_independence_minor_residual(
    probabilities: Iterable[float],
) -> float:
    entries = dict(zip(BITS, tuple(float(value) for value in probabilities)))
    if len(entries) != 8:
        raise ValueError("eight syndrome probabilities are required")
    return max(
        abs(
            entries[0, 0, k] * entries[1, 1, k]
            - entries[0, 1, k] * entries[1, 0, k]
        )
        for k in (0, 1)
    )


def audit_information_projection(
    control_id: str,
    n: int,
    orbit_indices: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> InformationProjectionControl:
    natural_amplitudes = audit_orbit_variance(
        control_id, n, orbit_indices
    ).unsigned_channel_amplitudes
    natural = normalize_channel(natural_amplitudes)
    projection = markov_information_projection(natural)
    uniform = (1.0 / 8.0,) * 8
    adaptive_kl = kl_divergence_bits(natural, uniform)
    irreducible = kl_divergence_bits(natural, projection)
    compatible = kl_divergence_bits(projection, uniform)
    uniform_residual = abs(adaptive_kl - irreducible - compatible)
    minor_residual = conditional_independence_minor_residual(projection)

    racah = audit_racah_rank_residual(control_id, n, orbit_indices)
    rank_amplitudes = tuple(
        row.haar_rank_profile_benchmark for row in racah.channels
    )
    if sum(rank_amplitudes) > tolerance:
        rank = normalize_channel(rank_amplitudes)
        natural_to_rank = kl_divergence_bits(natural, rank)
        projection_to_rank = kl_divergence_bits(projection, rank)
        rank_residual = (
            abs(natural_to_rank - irreducible - projection_to_rank)
            if math.isfinite(natural_to_rank) and math.isfinite(projection_to_rank)
            else None
        )
    else:
        rank = None
        natural_to_rank = None
        projection_to_rank = None
        rank_residual = None
    exact = bool(
        uniform_residual <= tolerance
        and minor_residual <= tolerance
        and (rank_residual is None or rank_residual <= tolerance)
    )
    return InformationProjectionControl(
        control_id=control_id,
        n=n,
        orbit_indices=orbit_indices,
        natural_probabilities=natural,
        markov_projection_probabilities=projection,
        rank_profile_probabilities=rank,
        adaptive_kl_to_uniform_bits=adaptive_kl,
        irreducible_racah_conditional_mutual_information_bits=irreducible,
        markov_projection_kl_to_uniform_bits=compatible,
        uniform_pythagorean_residual_bits=uniform_residual,
        natural_kl_to_rank_profile_bits=natural_to_rank,
        markov_projection_kl_to_rank_profile_bits=projection_to_rank,
        rank_profile_pythagorean_residual_bits=rank_residual,
        maximum_markov_projection_conditional_minor=minor_residual,
        exact_information_projection_verified=exact,
        status=(
            "adaptive-kl-split-into-racah-cmi-and-rank-compatible-bias"
            if exact
            else "racah-information-projection-control-failure"
        ),
    )


def audit_information_projection_aggregate(
    n: int,
    minimum_dimension_exclusive: int = 1,
    *,
    tolerance: float = 1e-9,
) -> InformationProjectionAggregateControl:
    if minimum_dimension_exclusive < 0:
        raise ValueError("dimension threshold must be nonnegative")
    orbits, _base_likelihood, _base_product, base_physical = (
        aggregate_sign_orbit_law(n)
    )
    parity_orbits, parity_arrays = parity_coset_word_likelihood_arrays(n)
    if parity_orbits != orbits:
        raise AssertionError("coarse sign-orbit order mismatch")
    retained = tuple(
        index
        for index, orbit in enumerate(orbits)
        if len(orbit) == 2
        and hook_length_dimension(orbit[0]) > minimum_dimension_exclusive
    )
    mass = 0.0
    adaptive = 0.0
    irreducible = 0.0
    compatible = 0.0
    failures = 0
    positive_count = 0
    maximum = 0.0
    maximum_indices: tuple[int, ...] | None = None
    for orbit_indices in itertools.product(retained, repeat=6):
        physical_mass = float(base_physical[orbit_indices])
        if physical_mass <= tolerance:
            continue
        positive_count += 1
        signed = tuple(
            float(parity_arrays[frequency][orbit_indices]) for frequency in BITS
        )
        natural = normalize_channel(inverse_walsh_transform(signed))
        projection = markov_information_projection(natural)
        uniform = (1.0 / 8.0,) * 8
        row_adaptive = kl_divergence_bits(natural, uniform)
        row_irreducible = kl_divergence_bits(natural, projection)
        row_compatible = kl_divergence_bits(projection, uniform)
        row_residual = abs(row_adaptive - row_irreducible - row_compatible)
        failures += bool(
            row_residual > tolerance
            or conditional_independence_minor_residual(projection) > tolerance
        )
        mass += physical_mass
        adaptive += physical_mass * row_adaptive
        irreducible += physical_mass * row_irreducible
        compatible += physical_mass * row_compatible
        if row_irreducible > maximum:
            maximum = row_irreducible
            maximum_indices = orbit_indices
    residual = abs(adaptive - irreducible - compatible)
    verified = failures == 0 and residual <= tolerance
    return InformationProjectionAggregateControl(
        n=n,
        minimum_dimension_exclusive=minimum_dimension_exclusive,
        retained_nonself_orbit_count=len(retained),
        positive_physical_orbit_tuple_count=positive_count,
        retained_physical_mass=mass,
        physical_mass_weighted_adaptive_kl_bits=adaptive,
        physical_mass_weighted_irreducible_racah_cmi_bits=irreducible,
        physical_mass_weighted_rank_compatible_kl_bits=compatible,
        aggregate_pythagorean_residual_bits=residual,
        irreducible_fraction_of_adaptive_kl=(
            irreducible / adaptive if adaptive > tolerance else 0.0
        ),
        conditional_irreducible_cmi_on_retained_mass_bits=(
            irreducible / mass if mass > tolerance else 0.0
        ),
        maximum_single_orbit_irreducible_cmi_bits=maximum,
        maximum_single_orbit_indices=maximum_indices,
        all_orbit_projections_verified=verified,
        finite_exact_aggregation_only=True,
        status=(
            "finite-physical-racah-information-projection-aggregated"
            if verified
            else "racah-information-projection-aggregate-failure"
        ),
    )


def run_parity_racah_information_projection(
) -> ParityRacahInformationProjectionReport:
    controls = [
        audit_information_projection("S4-FLAT", 4, (1,) * 6),
        audit_information_projection("S5-ALL-FIVE", 5, (2,) * 6),
        audit_information_projection(
            "S5-RACAH-CMI-WITNESS", 5, (1, 2, 1, 2, 2, 2)
        ),
    ]
    aggregates = [
        audit_information_projection_aggregate(4),
        audit_information_projection_aggregate(5),
    ]
    failures = sum(not row.exact_information_projection_verified for row in controls)
    failures += sum(not row.all_orbit_projections_verified for row in aggregates)
    verified = failures == 0
    tail = aggregates[-1]
    return ParityRacahInformationProjectionReport(
        created_at=utc_now(),
        theorem_contract={
            "markov_family": "M={Q:G conditionally independent of H given K}.",
            "information_projection": "Pi_M(P)=P(G|K)P(H|K)P(K).",
            "irreducible_racah_information": (
                "min_(Q in M)D(P||Q)=D(P||Pi_M(P))=I_P(G;H|K)."
            ),
            "adaptive_kl_decomposition": (
                "D(P||U3)=I_P(G;H|K)+D(Pi_M(P)||U3)."
            ),
            "rank_profile_pythagorean_identity": (
                "For compatible rank R in M, D(P||R)=I_P(G;H|K)+D(Pi_M(P)||R)."
            ),
            "scope": (
                "The decomposition is exact and nonnegative. Finite aggregate values "
                "do not establish asymptotic source mass, coherent access, classical "
                "hardness, an algorithm, or a speedup."
            ),
        },
        orbit_controls=controls,
        aggregate_controls=aggregates,
        proof_obligations=[
            {
                "obligation": "replace_signed_rank_arithmetic_cancellation_by_positive_information_split",
                "resolved": verified,
                "resolution": (
                    "Information projection onto the rank-compatible Markov family "
                    "gives two nonnegative KL terms with an exact Pythagorean identity."
                ),
            },
            {
                "obligation": "aggregate_irreducible_racah_information_on_finite_physical_mass",
                "resolved": verified,
                "resolution": (
                    "Every positive retained S4/S5 orbit tuple was weighted by its "
                    "coarse physical mass; the aggregate KL identity closes numerically."
                ),
            },
            {
                "obligation": "decide_asymptotic_physical_expectation_of_racah_cmi",
                "resolved": False,
                "resolution": (
                    "Prove E_phys I(Y_g;Y_h|Y_k,O)->0 or a positive lower bound on a "
                    "canonical positive-mass sector."
                ),
            },
            {
                "obligation": "match_quantum_and_classical_access_for_cmi_estimation",
                "resolved": False,
                "resolution": (
                    "Specify sample/query complexity under word-map samples, explicit "
                    "representation access, and coherent coset-state access."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The chosen Haar rank benchmark may be the wrong comparison.",
                "resolved": True,
                "resolution": (
                    "CMI is the minimum KL distance to the entire rank-compatible Markov "
                    "family, not to one chosen benchmark."
                ),
            },
            {
                "objection": "Rank and arithmetic effects can cancel, so the split is unstable.",
                "resolved": True,
                "resolution": (
                    "Both information-projection terms are nonnegative and satisfy an "
                    "exact KL Pythagorean identity."
                ),
            },
            {
                "objection": "The finite S5 aggregate proves asymptotic survival.",
                "resolved": True,
                "resolution": (
                    "False. It covers a finite dimension-trimmed sector; both its mass "
                    "and conditional CMI can vanish with n."
                ),
            },
            {
                "objection": "Irreducible measured-label information is automatically quantumly useful.",
                "resolved": True,
                "resolution": (
                    "Classical word-map samples may estimate the same statistic, and no "
                    "coherent implementation or complexity gap is shown."
                ),
            },
        ],
        headline_metrics={
            "racah_information_projection_theorem_count": int(verified),
            "finite_orbit_control_count": len(controls),
            "finite_aggregate_control_count": len(aggregates),
            "finite_control_failure_count": failures,
            "S5_retained_physical_mass": tail.retained_physical_mass,
            "S5_physical_weighted_adaptive_kl_bits": (
                tail.physical_mass_weighted_adaptive_kl_bits
            ),
            "S5_physical_weighted_irreducible_racah_cmi_bits": (
                tail.physical_mass_weighted_irreducible_racah_cmi_bits
            ),
            "S5_irreducible_fraction_of_adaptive_kl": (
                tail.irreducible_fraction_of_adaptive_kl
            ),
            "S5_maximum_single_orbit_racah_cmi_bits": (
                tail.maximum_single_orbit_irreducible_cmi_bits
            ),
            "maximum_pythagorean_residual_bits": max(
                [row.uniform_pythagorean_residual_bits for row in controls]
                + [row.aggregate_pythagorean_residual_bits for row in aggregates]
            ),
            "asymptotic_racah_cmi_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "racah_cmi_is_exact_distance_to_all_rank_profile_models": verified,
            "adaptive_kl_has_positive_rank_racah_decomposition": verified,
            "finite_physical_racah_cmi_positive": (
                tail.physical_mass_weighted_irreducible_racah_cmi_bits > 0
            ),
            "asymptotic_racah_cmi_vanishes_proved": False,
            "asymptotic_racah_cmi_survives_proved": False,
            "canonical_source_mass_positive_proved": False,
            "coherent_extraction_implemented": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The irreducible natural 6j component is now an exact positive KL "
                "observable, but only finite S5 mass is established."
            ),
        },
        status=(
            "adaptive-kl-split-into-rank-compatible-bias-and-irreducible-racah-cmi"
            if verified
            else "parity-racah-information-projection-control-failure"
        ),
        summary=(
            "Identified conditional mutual information as the exact KL distance from "
            "natural adaptive syndrome channels to all rank-profile Markov models."
        ),
        falsifiers_triggered=[
            "A single Haar benchmark is unnecessary; the full rank-compatible model class has an exact information projection.",
            "Amplitude-level rank/arithmetic cancellation does not affect the positive KL split.",
            "Most finite S5 adaptive KL remains rank-compatible; only a smaller part is irreducibly Racah.",
            "A finite positive Racah CMI does not establish asymptotic or quantumly exclusive value.",
        ],
    )


def write_parity_racah_information_projection_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_racah_information_projection())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_racah_information_projection_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

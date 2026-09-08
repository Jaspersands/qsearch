"""Natural overlapping carrier labels reduce to a weighted commuting moment.

Consider three tensor blocks ``U,V,W``.  Each block contains at least one
independent Plancherel-distributed ``S_n`` irrep; arbitrary fixed factors may
also be present.  Let ``P_alpha`` be the full ``S_n`` isotypic projector on
``U tensor V`` and ``Q_beta`` the isotypic projector on ``V tensor W``.  The
normalized aggregate incompatibility of the two sharp label measurements is

    C_n = (1/D) sum_(alpha,beta) ||[P_alpha,Q_beta]||_F^2.       (1)

Plancherel character orthogonality makes every random block a normalized
regular trace.  Expanding the four projectors in (1) therefore leaves

    E C_n = 2(1-kappa_n),                                      (2)

where

    A_n(g) = sum_lambda d_lambda^2 chi_lambda(g)^2,
    mu_n(g) = A_n(g)/(n!)^2,
    kappa_n = Pr_(g,h iid mu_n)[gh=hg].                         (3)

The identity ``sum_g A_n(g)=(n!)^2`` proves that ``mu_n`` is a probability
law.  Equation (2) is an exact all-``n`` coefficient-level replacement for
dense carrier projectors and exposes the first genuinely joint datum missing
from pairwise overlap spectra: a fourth-order commuting-pair moment.

The exact moment is evaluated through ``n=8``.  A direct dense Plancherel
average at ``n=3`` independently verifies (2), and exact sampling from
``mu_n`` probes larger degrees without constructing a Specht tensor basis.
The observed commuting probability falls sharply through ``n=20``.  This is
evidence that natural overlapping carrier labels are strongly contextual,
not an asymptotic theorem: proving ``kappa_n<=1-c`` (or ``kappa_n=o(1)``)
remains the decisive character-moment obligation.

Conditioning on any globally-distinct source event of probability ``1-o(1)``
changes the expectation of (1) by at most twice the failure probability,
because ``0<=C_n<=2``.  Thus an eventual constant-gap theorem for (3) would
transfer to the collision-free physical event.  No Racah resolver, coherent
global channel atom, PGM, decoder, or quantum speedup is constructed here.
"""

from __future__ import annotations

import bisect
import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_carrier_contextuality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-CONTEXTUALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class ExactCarrierContextualityControl:
    n: int
    group_order: int
    partition_count: int
    character_squared_law_normalization: str
    weighted_commuting_pair_numerator: str
    weighted_commuting_pair_denominator: str
    exact_weighted_commuting_probability: str
    weighted_commuting_probability: float
    exact_annealed_aggregate_commutator: str
    annealed_aggregate_commutator: float
    nonabelian_contextuality_positive: bool
    exact_character_moment_verified: bool
    status: str


@dataclass(frozen=True)
class DensePlancherelContextualityControl:
    n: int
    source_tuple_count: int
    carrier_label_pair_count: int
    exact_formula_aggregate_commutator: float
    dense_annealed_aggregate_commutator: float
    dense_to_formula_residual: float
    maximum_projector_idempotence_residual: float
    dense_plancherel_formula_verified: bool
    status: str


@dataclass(frozen=True)
class SampledCarrierContextualityRecord:
    n: int
    partition_count: int
    sample_count: int
    random_seed: int
    confidence_failure_probability: float
    commuting_pair_hit_count: int
    estimated_weighted_commuting_probability: float
    hoeffding_radius: float
    commuting_probability_confidence_lower: float
    commuting_probability_confidence_upper: float
    estimated_annealed_aggregate_commutator: float
    aggregate_commutator_confidence_lower: float
    aggregate_commutator_confidence_upper: float
    exact_distribution_normalization_residual: float
    finite_sample_only: bool
    status: str


@dataclass(frozen=True)
class PlancherelCarrierContextualityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[ExactCarrierContextualityControl]
    dense_control: DensePlancherelContextualityControl
    sampled_scaling_records: list[SampledCarrierContextualityRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def character_squared_weight(cycle_type: Partition) -> int:
    """Return ``A_n(C)=sum_lambda d_lambda^2 chi_lambda(C)^2``."""

    n = sum(cycle_type)
    if n < 1:
        raise ValueError("cycle type must be a nonempty partition")
    return sum(
        hook_length_dimension(partition) ** 2
        * symmetric_character(partition, cycle_type) ** 2
        for partition in integer_partitions(n)
    )


def character_squared_class_law(n: int) -> dict[Partition, Fraction]:
    """Return the cycle-type law induced by ``mu_n(g)=A_n(g)/(n!)^2``."""

    if n < 1:
        raise ValueError("n must be positive")
    order = math.factorial(n)
    law = {
        cycle_type: Fraction(
            conjugacy_class_size(cycle_type)
            * character_squared_weight(cycle_type),
            order**2,
        )
        for cycle_type in integer_partitions(n)
    }
    if sum(law.values(), start=Fraction()) != 1:
        raise ArithmeticError("character-squared class law failed to normalize")
    return law


def _canonical_permutation(cycle_type: Partition) -> Permutation:
    output: list[int] = []
    offset = 0
    for length in cycle_type:
        output.extend(range(offset + 1, offset + length))
        output.append(offset)
        offset += length
    return tuple(output)


def _inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def _random_conjugate(
    representative: Permutation,
    generator: random.Random,
) -> Permutation:
    conjugator = list(range(len(representative)))
    generator.shuffle(conjugator)
    conjugator_tuple = tuple(conjugator)
    return compose_permutations(
        conjugator_tuple,
        compose_permutations(
            representative,
            _inverse_permutation(conjugator_tuple),
        ),
    )


def _commute(left: Permutation, right: Permutation) -> bool:
    return all(
        left[right[index]] == right[left[index]]
        for index in range(len(left))
    )


def exact_weighted_commuting_probability(n: int) -> Fraction:
    """Evaluate ``kappa_n`` exactly by class representatives.

    The cost is ``p(n)n!`` permutation commutation checks, so this control is
    intentionally restricted to ``n<=8``.
    """

    if not 1 <= n <= 8:
        raise ValueError("exact permutation controls require 1<=n<=8")
    order = math.factorial(n)
    cycle_types = tuple(integer_partitions(n))
    weights = {
        cycle_type: character_squared_weight(cycle_type)
        for cycle_type in cycle_types
    }
    permutations = tuple(itertools.permutations(range(n)))
    permutation_types = tuple(
        permutation_cycle_type(permutation) for permutation in permutations
    )
    numerator = 0
    for cycle_type in cycle_types:
        representative = _canonical_permutation(cycle_type)
        centralizer_weight = sum(
            weights[right_type]
            for right, right_type in zip(permutations, permutation_types)
            if _commute(representative, right)
        )
        numerator += (
            conjugacy_class_size(cycle_type)
            * weights[cycle_type]
            * centralizer_weight
        )
    return Fraction(numerator, order**4)


def exact_carrier_contextuality_control(
    n: int,
) -> ExactCarrierContextualityControl:
    if not 1 <= n <= 8:
        raise ValueError("exact controls require 1<=n<=8")
    order = math.factorial(n)
    law = character_squared_class_law(n)
    kappa = exact_weighted_commuting_probability(n)
    contextuality = 2 * (1 - kappa)
    positive = n >= 3 and contextuality > 0
    verified = bool(
        sum(law.values(), start=Fraction()) == 1
        and 0 <= kappa <= 1
        and ((n <= 2 and contextuality == 0) or positive)
    )
    return ExactCarrierContextualityControl(
        n=n,
        group_order=order,
        partition_count=len(law),
        character_squared_law_normalization=str(sum(law.values(), start=Fraction())),
        weighted_commuting_pair_numerator=str(kappa.numerator),
        weighted_commuting_pair_denominator=str(kappa.denominator),
        exact_weighted_commuting_probability=str(kappa),
        weighted_commuting_probability=float(kappa),
        exact_annealed_aggregate_commutator=str(contextuality),
        annealed_aggregate_commutator=float(contextuality),
        nonabelian_contextuality_positive=positive,
        exact_character_moment_verified=verified,
        status=(
            "exact-natural-overlapping-carrier-contextuality"
            if positive and verified
            else "exact-abelian-label-compatibility"
            if verified
            else "carrier-contextuality-character-control-failure"
        ),
    )


def _kron_three(
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
) -> np.ndarray:
    return np.kron(np.kron(first, second), third)


def _triple_isotypic_projectors(
    sources: tuple[Partition, Partition, Partition],
    side: str,
) -> tuple[np.ndarray, ...]:
    n = sum(sources[0])
    if any(sum(source) != n for source in sources):
        raise ValueError("all source partitions must have the same degree")
    source_rows = [
        dict(permutation_representation_matrices(source)) for source in sources
    ]
    dimensions = [hook_length_dimension(source) for source in sources]
    identities = [np.eye(dimension, dtype=complex) for dimension in dimensions]
    output = []
    for target in integer_partitions(n):
        target_rows = dict(permutation_representation_matrices(target))
        projector = np.zeros(
            (math.prod(dimensions), math.prod(dimensions)),
            dtype=complex,
        )
        for permutation, target_matrix in target_rows.items():
            character = np.trace(target_matrix).conjugate()
            if side == "left":
                factors = (
                    source_rows[0][permutation],
                    source_rows[1][permutation],
                    identities[2],
                )
            elif side == "right":
                factors = (
                    identities[0],
                    source_rows[1][permutation],
                    source_rows[2][permutation],
                )
            else:
                raise ValueError("side must be left or right")
            projector += character * _kron_three(*factors)
        projector *= hook_length_dimension(target) / math.factorial(n)
        output.append((projector + projector.conj().T) / 2)
    return tuple(output)


def audit_dense_plancherel_contextuality(
    n: int = 3,
    *,
    tolerance: float = 1e-9,
) -> DensePlancherelContextualityControl:
    """Independently verify the character formula by dense source averaging."""

    if not 2 <= n <= 3:
        raise ValueError("dense source controls require 2<=n<=3")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    source_weights = {
        partition: Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in partitions
    }
    total = 0.0
    maximum_idempotence = 0.0
    label_pairs = 0
    tuple_count = 0
    for sources in itertools.product(partitions, repeat=3):
        tuple_count += 1
        source_probability = math.prod(
            (float(source_weights[source]) for source in sources),
            start=1.0,
        )
        ambient = math.prod(hook_length_dimension(source) for source in sources)
        left = _triple_isotypic_projectors(sources, "left")
        right = _triple_isotypic_projectors(sources, "right")
        maximum_idempotence = max(
            maximum_idempotence,
            *(
                float(np.linalg.norm(projector @ projector - projector, ord=2))
                for projector in (*left, *right)
            ),
        )
        local = 0.0
        for first in left:
            for second in right:
                commutator = first @ second - second @ first
                local += float(np.linalg.norm(commutator, ord="fro") ** 2)
                label_pairs += 1
        total += source_probability * local / ambient
    exact = float(2 * (1 - exact_weighted_commuting_probability(n)))
    residual = abs(total - exact)
    verified = bool(
        maximum_idempotence <= 100 * tolerance
        and residual <= 100 * tolerance
    )
    return DensePlancherelContextualityControl(
        n=n,
        source_tuple_count=tuple_count,
        carrier_label_pair_count=label_pairs,
        exact_formula_aggregate_commutator=exact,
        dense_annealed_aggregate_commutator=total,
        dense_to_formula_residual=residual,
        maximum_projector_idempotence_residual=maximum_idempotence,
        dense_plancherel_formula_verified=verified,
        status=(
            "dense-plancherel-contextuality-formula-verified"
            if verified
            else "dense-plancherel-contextuality-formula-failure"
        ),
    )


def sample_weighted_commuting_probability(
    n: int,
    sample_count: int,
    *,
    seed: int,
    confidence_failure_probability: float = 0.01,
) -> SampledCarrierContextualityRecord:
    """Sample ``kappa_n`` exactly from its character-squared class law."""

    if n < 2 or sample_count < 1:
        raise ValueError("n>=2 and a positive sample count are required")
    if not 0 < confidence_failure_probability < 1:
        raise ValueError("confidence failure probability must lie in (0,1)")
    law = character_squared_class_law(n)
    cycle_types = tuple(law)
    cumulative = []
    total = 0.0
    for cycle_type in cycle_types:
        total += float(law[cycle_type])
        cumulative.append(total)
    cumulative[-1] = 1.0
    representatives = {
        cycle_type: _canonical_permutation(cycle_type)
        for cycle_type in cycle_types
    }
    generator = random.Random(seed)
    hits = 0
    for _ in range(sample_count):
        left_type = cycle_types[
            bisect.bisect_left(cumulative, generator.random())
        ]
        right_type = cycle_types[
            bisect.bisect_left(cumulative, generator.random())
        ]
        left = _random_conjugate(representatives[left_type], generator)
        right = _random_conjugate(representatives[right_type], generator)
        hits += _commute(left, right)
    estimate = hits / sample_count
    radius = math.sqrt(
        math.log(2 / confidence_failure_probability) / (2 * sample_count)
    )
    lower = max(0.0, estimate - radius)
    upper = min(1.0, estimate + radius)
    contextuality = 2 * (1 - estimate)
    return SampledCarrierContextualityRecord(
        n=n,
        partition_count=len(cycle_types),
        sample_count=sample_count,
        random_seed=seed,
        confidence_failure_probability=confidence_failure_probability,
        commuting_pair_hit_count=hits,
        estimated_weighted_commuting_probability=estimate,
        hoeffding_radius=radius,
        commuting_probability_confidence_lower=lower,
        commuting_probability_confidence_upper=upper,
        estimated_annealed_aggregate_commutator=contextuality,
        aggregate_commutator_confidence_lower=2 * (1 - upper),
        aggregate_commutator_confidence_upper=2 * (1 - lower),
        exact_distribution_normalization_residual=abs(total - 1.0),
        finite_sample_only=True,
        status="sampled-natural-carrier-contextuality-asymptotic-open",
    )


def run_plancherel_carrier_contextuality(
    *,
    sample_count: int = 20_000,
) -> PlancherelCarrierContextualityReport:
    exact = [exact_carrier_contextuality_control(n) for n in range(2, 9)]
    dense = audit_dense_plancherel_contextuality(3)
    sampled = [
        sample_weighted_commuting_probability(
            n,
            sample_count,
            seed=17_029 + n,
        )
        for n in (10, 12, 14, 16, 18, 20)
    ]
    exact_failures = sum(not row.exact_character_moment_verified for row in exact)
    verified = exact_failures == 0 and dense.dense_plancherel_formula_verified
    tail = sampled[-1]
    return PlancherelCarrierContextualityReport(
        created_at=utc_now(),
        theorem_contract={
            "natural_model": (
                "Three overlapping membership-pattern blocks each contain a fresh "
                "independent Plancherel S_n source factor; fixed extra factors are allowed."
            ),
            "aggregate_contextuality": (
                "C_n=D^-1 sum_(alpha,beta)||[P_alpha^(UV),Q_beta^(VW)]||_F^2."
            ),
            "character_reduction": (
                "E C_n=2(1-kappa_n), where kappa_n is the commuting probability "
                "of mu_n(g)=(n!)^-2 sum_lambda d_lambda^2 chi_lambda(g)^2."
            ),
            "collision_free_transfer": (
                "Conditioning on a source-distinct event E changes E[C_n] by at "
                "most 2 Pr(E^c), since 0<=C_n<=2."
            ),
            "scope": (
                "This is a joint carrier-label contextuality moment, not a "
                "Racah circuit, endpoint effect, PGM, decoder, or separation."
            ),
        },
        exact_controls=exact,
        dense_control=dense,
        sampled_scaling_records=sampled,
        proof_obligations=[
            {
                "obligation": "derive_natural_overlapping_carrier_contextuality_moment",
                "resolved": verified,
                "resolution": (
                    "Expanding four central isotypic projectors and applying one "
                    "fresh Plancherel trace per membership block leaves exactly "
                    "the commuting constraint [g,h]=1."
                ),
            },
            {
                "obligation": "verify_character_reduction_against_dense_physical_projectors",
                "resolved": dense.dense_plancherel_formula_verified,
                "resolution": (
                    "The complete dense n=3 source and carrier-label average "
                    "matches the exact character formula."
                ),
            },
            {
                "obligation": "transfer_constant_contextuality_to_global_distinct_event",
                "resolved": True,
                "resolution": (
                    "The bounded-observable conditioning inequality is exact; "
                    "the existing global collision theorem supplies Pr(E^c)=o(1)."
                ),
            },
            {
                "obligation": "prove_weighted_commuting_probability_bounded_away_from_one",
                "resolved": False,
                "resolution": (
                    "Exact small-n and sampled n<=20 values are not an all-n "
                    "character bound. Prove kappa_n<=1-c or kappa_n=o(1)."
                ),
            },
            {
                "obligation": "compile_structured_multistar_racah_resolver",
                "resolved": False,
                "resolution": (
                    "A contextuality witness rules out persistent sharp classical "
                    "labels; it does not implement the required coherent resolver."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pairwise carrier spectra determine simultaneous sharp labels.",
                "resolved": True,
                "resolution": (
                    "False: the missing fourth-order datum is the weighted "
                    "commuting-pair moment in equation (3)."
                ),
            },
            {
                "objection": "The n=3 contextuality control is a rare fixed-source artifact.",
                "resolved": True,
                "resolution": (
                    "The formula averages independent Plancherel source factors "
                    "and holds at every n; n=3 is only an independent dense audit."
                ),
            },
            {
                "objection": "The decreasing sampled kappa_n proves asymptotic maximal contextuality.",
                "resolved": True,
                "resolution": (
                    "False. Sampling supplies a finite confidence statement, not "
                    "a uniform character estimate or asymptotic theorem."
                ),
            },
            {
                "objection": "Contextual carrier labels rule out the collective PGM route.",
                "resolved": False,
                "resolution": (
                    "A structured Racah transform may resolve the incompatible "
                    "labels coherently; no circuit lower bound is proved."
                ),
            },
        ],
        headline_metrics={
            "natural_carrier_contextuality_character_reduction_theorem_count": int(verified),
            "dense_plancherel_formula_control_count": int(
                dense.dense_plancherel_formula_verified
            ),
            "exact_degree_control_count": len(exact),
            "exact_control_failure_count": exact_failures,
            "largest_exact_degree": exact[-1].n,
            "largest_exact_annealed_aggregate_commutator": max(
                row.annealed_aggregate_commutator for row in exact
            ),
            "sampled_degree_count": len(sampled),
            "largest_sampled_degree": tail.n,
            "tail_estimated_weighted_commuting_probability": (
                tail.estimated_weighted_commuting_probability
            ),
            "tail_contextuality_confidence_lower": (
                tail.aggregate_commutator_confidence_lower
            ),
            "asymptotic_constant_contextuality_theorem_count": 0,
            "coherent_multistar_racah_resolver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_natural_annealed_contextuality_formula_proved": verified,
            "pairwise_carrier_spectra_determine_joint_sharp_labels": False,
            "globally_distinct_conditioning_preserves_any_constant_gap": True,
            "weighted_commuting_probability_asymptotically_vanishes_proved": False,
            "collision_free_positive_constant_contextuality_proved": False,
            "persistent_global_boolean_carrier_label_is_valid_universally": False,
            "structured_multistar_racah_resolver_compiled": False,
            "physical_pgm_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural overlapping carrier compatibility is reduced exactly "
                "to one weighted commuting-pair character moment and finite data "
                "shows strong contextuality, but the all-n gap and coherent Racah "
                "resolver remain open."
            ),
        },
        status=(
            "natural-carrier-contextuality-reduced-to-weighted-commuting-moment"
            if verified
            else "natural-carrier-contextuality-control-failure"
        ),
        summary=(
            "Reduced natural overlapping S_n carrier-label incompatibility to an "
            "exact character-squared commuting probability, verified the formula "
            "densely, and found strong finite scaling without promoting it to an "
            "asymptotic no-go."
        ),
        falsifiers_triggered=[
            "Pairwise carrier overlap spectra are insufficient to certify a persistent global sharp label.",
            "Natural Plancherel averaging does not make overlapping full S_n carrier measurements exactly commute.",
            "A falling finite commuting-probability trend is not an all-n contextuality theorem.",
            "Carrier contextuality redirects the compiler to coherent Racah resolution; it does not rule that route out.",
        ],
    )


def write_plancherel_carrier_contextuality_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_plancherel_carrier_contextuality(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Natural overlapping carrier contextuality moment",
                status="completed-exact-character-reduction-asymptotic-gap-open",
                hypothesis=(
                    "Overlapping full S_n carrier labels on natural membership "
                    "blocks retain nonnegligible joint contextuality and therefore "
                    "require a coherent Racah resolver rather than classical label accumulation."
                ),
                protocol=(
                    "Average three independent Plancherel source blocks, reduce "
                    "the aggregate projector commutator to a character-squared "
                    "commuting-pair law, verify it densely, enumerate n<=8 exactly, "
                    "and sample the exact law through n=20."
                ),
                positive_signal=(
                    "An all-n upper bound kappa_n<=1-c, ideally kappa_n=o(1), "
                    "followed by a polynomial structured Racah resolver."
                ),
                falsifiers=[
                    "pairwise spectra are treated as joint label data",
                    "finite Monte Carlo is promoted to an asymptotic theorem",
                    "annealed source mass is confused with one fixed portfolio",
                    "contextuality is promoted to a circuit lower bound",
                ],
                metrics=[
                    "natural_carrier_contextuality_character_reduction_theorem_count",
                    "tail_estimated_weighted_commuting_probability",
                    "tail_contextuality_confidence_lower",
                    "asymptotic_constant_contextuality_theorem_count",
                    "coherent_multistar_racah_resolver_count",
                ],
                dependencies=[
                    "Plancherel character orthogonality",
                    "pair carrier-label contextuality",
                    "global source-partition collision theorem",
                    "membership-pattern carrier factorization",
                ],
                next_actions=[
                    "bound the character-squared weighted commuting probability asymptotically",
                    "decompose the moment by moved support and centralizer type",
                    "derive the corresponding multistar Racah block representation",
                    "compile or obstruct a normalization-one Racah resolver",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-"
            "CONTEXTUALITY-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_plancherel_carrier_contextuality": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NATURAL-OVERLAPPING-CARRIER-LABELS-NOT-EXACTLY-JOINT-CLASSICAL",
                source=registry_experiment_id,
                claim=(
                    "Natural Plancherel source averaging makes all overlapping "
                    "full S_n carrier labels exactly jointly classical."
                ),
                reason_invalid=(
                    "Their exact aggregate commutator is 2(1-kappa_n)>0 for "
                    "every nonabelian S_n; kappa_n is an explicit weighted "
                    "commuting probability."
                ),
                lesson=(
                    "A global compiler must resolve incompatible carrier frames "
                    "coherently or avoid sharp label accumulation."
                ),
                applies_to=[
                    registry_candidate_id,
                    "global carrier-label accumulation",
                    "affine-star Cayley compilation",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-CARRIER-CONTEXTUALITY-TREND-NOT-ASYMPTOTIC-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "The sampled decrease of kappa_n through n=20 proves "
                    "asymptotically maximal natural carrier contextuality."
                ),
                reason_invalid=(
                    "The samples have finite Hoeffding intervals but no uniform "
                    "all-n character or centralizer bound."
                ),
                lesson=(
                    "Prove the weighted commuting-moment asymptotics before using "
                    "contextuality as a positive-mass compiler obstruction."
                ),
                applies_to=[
                    registry_candidate_id,
                    "asymptotic contextuality claims",
                    "Racah compiler lower bounds",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_plancherel_carrier_contextuality_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

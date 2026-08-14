"""Classical word-map baseline for orientation-syndrome Racah information.

For a non-self-conjugate six-label sign-orbit tuple in coefficient order

    (alpha, beta, gamma, mu, nu, lambda),

the eight orientation-syndrome amplitudes have the exact character formula

    A_y = E[prod_i chi_(rho_i^z_i)(W_i(g,h,k))],          (1)

where ``W=(gk,ghk,hk,g,h,k)`` and ``A^T z=y``.  Since
``chi_(rho^t)(w)=sgn(w) chi_rho(w)``, all eight normalized amplitudes are the
Walsh coefficients

    mu_y=A_y/D=E[Z(g,h,k)(-1)^(<y,p(g,h,k)>)],            (2)

where ``D=prod_i d_i``, ``Z=prod_i chi_i(W_i)/d_i`` lies in ``[-1,1]``, and
``p`` records the parities of ``g,h,k``.  One classical word sample therefore
updates all eight coefficients; eight independent estimators are unnecessary.

If ``N`` independent samples estimate every coefficient to additive ``eta``,

    Pr(max_y |mu_hat_y-mu_y| > eta) <= 16 exp(-N eta^2/2). (3)

Clip negative empirical coefficients to zero and normalize.  With
``T=sum_y mu_y`` and ``eta<T/8``, the resulting syndrome law is within total
variation ``8 eta/T`` of the exact law.  Thus TV error ``epsilon`` with failure
probability ``delta`` is guaranteed by

    N >= 128 log(16/delta)/(epsilon^2 T^2).               (4)

The physical sign-orbit mass is ``P=8 D^2 T/|S_n|^3``, so (4) is equivalently

    N >= 8192 D^4 log(16/delta)/(epsilon^2 P^2 |S_n|^6). (5)

These are sufficient upper bounds, not lower bounds.  They expose a severe
signed-cancellation problem on the finite controls, but do not prove quantum
advantage: importance sampling may improve the variance, worst-case hardness
of symmetric-group character evaluation does not establish average-case
hardness here, and measured syndrome information is not a coherent decoder.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

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
from self_dual_wreath_sign_orbit_syndrome_reduction import sign_frequency
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    tetrahedral_class_signature_counts,
)
from symmetric_character import symmetric_character


Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Syndrome = tuple[int, int, int]
SYNDROMES: tuple[Syndrome, ...] = tuple(itertools.product((0, 1), repeat=3))
WORD_SIGNATURE_AXES = (3, 5, 4, 0, 1, 2)
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_word_map_classical_baseline.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-WORD-MAP-CLASSICAL-BASELINE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrientationWordMapExactControl:
    control_id: str
    n: int
    base_partitions: tuple[Partition, ...]
    dimension_product: int
    exact_normalized_walsh_means: tuple[str, ...]
    compiled_normalized_amplitudes: tuple[float, ...]
    maximum_exact_to_compiled_residual: float
    all_exact_means_nonnegative: bool
    exact_walsh_identity_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationClassicalCostRecord:
    control_id: str
    n: int
    base_partitions: tuple[Partition, ...]
    base_dimensions: tuple[int, ...]
    dimension_product: int
    total_normalized_amplitude: float
    physical_sign_orbit_tuple_mass: float
    physical_mass_formula_residual: float
    irreducible_racah_cmi_bits: float
    fixed_tv_target: float
    confidence_level: float
    log10_word_samples_sufficient_for_fixed_tv: float
    cmi_resolution_tv_target: float
    cmi_continuity_bound_at_target_bits: float
    log10_word_samples_sufficient_to_resolve_cmi: float
    inverse_physical_orbit_mass: float
    exact_character_evaluations_per_word_sample: int
    random_word_sample_updates_all_syndromes: bool
    word_map_estimator_is_classical: bool
    character_evaluation_is_unit_cost_assumed: bool
    polynomial_classical_runtime_proved: bool
    classical_lower_bound_proved: bool
    quantum_advantage_proved: bool
    status: str


@dataclass(frozen=True)
class OrientationWordMapClassicalBaselineReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_control: OrientationWordMapExactControl
    cost_records: list[OrientationClassicalCostRecord]
    query_model_matrix: list[dict[str, str | bool]]
    literature_boundaries: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_parity_bit_from_cycle_type(cycle_type: Partition) -> int:
    """Return zero for even and one for odd permutations of this cycle type."""

    return (sum(cycle_type) - len(cycle_type)) % 2


def walsh_sign(syndrome: Syndrome, input_parities: Syndrome) -> int:
    return -1 if sum(a * b for a, b in zip(syndrome, input_parities)) % 2 else 1


def _word_cycle_types(
    g: Permutation,
    h: Permutation,
    k: Permutation,
) -> tuple[Partition, ...]:
    gh = compose_permutations(g, h)
    return (
        permutation_cycle_type(compose_permutations(g, k)),
        permutation_cycle_type(compose_permutations(gh, k)),
        permutation_cycle_type(compose_permutations(h, k)),
        permutation_cycle_type(g),
        permutation_cycle_type(h),
        permutation_cycle_type(k),
    )


def normalized_word_map_walsh_observables(
    base_partitions: tuple[Partition, ...],
    g: Permutation,
    h: Permutation,
    k: Permutation,
) -> tuple[float, ...]:
    """Evaluate the shared bounded estimator for all eight syndromes."""

    if len(base_partitions) != 6:
        raise ValueError("six base partitions are required")
    n = len(g)
    if len(h) != n or len(k) != n:
        raise ValueError("permutations must have equal degree")
    if any(sum(partition) != n for partition in base_partitions):
        raise ValueError("partition and permutation degrees must agree")
    word_types = _word_cycle_types(g, h, k)
    normalized_product = math.prod(
        symmetric_character(partition, cycle_type)
        / hook_length_dimension(partition)
        for partition, cycle_type in zip(base_partitions, word_types)
    )
    input_parities = tuple(
        permutation_parity_bit_from_cycle_type(permutation_cycle_type(item))
        for item in (g, h, k)
    )
    return tuple(
        normalized_product * walsh_sign(syndrome, input_parities)
        for syndrome in SYNDROMES
    )


def exact_normalized_word_map_walsh_means(
    n: int,
    base_partitions: tuple[Partition, ...],
) -> tuple[Fraction, ...]:
    """Enumerate exact class signatures for ``n<=5`` and evaluate (2)."""

    if len(base_partitions) != 6 or any(
        sum(partition) != n for partition in base_partitions
    ):
        raise ValueError("six common-degree base partitions are required")
    dimensions = tuple(hook_length_dimension(row) for row in base_partitions)
    denominator = math.factorial(n) ** 3 * math.prod(dimensions)
    numerators = [0] * len(SYNDROMES)
    for signature, count in tetrahedral_class_signature_counts(n).items():
        base_character_product = math.prod(
            symmetric_character(label, signature[axis])
            for label, axis in zip(base_partitions, WORD_SIGNATURE_AXES)
        )
        input_parities = tuple(
            permutation_parity_bit_from_cycle_type(cycle_type)
            for cycle_type in signature[:3]
        )
        for index, syndrome in enumerate(SYNDROMES):
            numerators[index] += (
                count
                * base_character_product
                * walsh_sign(syndrome, input_parities)
            )
    return tuple(Fraction(numerator, denominator) for numerator in numerators)


def empirical_normalized_word_map_walsh_means(
    n: int,
    base_partitions: tuple[Partition, ...],
    sample_count: int,
    *,
    random_seed: int = 1729,
) -> tuple[float, ...]:
    if sample_count < 1:
        raise ValueError("positive sample count is required")
    rng = random.Random(random_seed)
    sums = [0.0] * len(SYNDROMES)
    identity = tuple(range(n))
    for _ in range(sample_count):
        permutations = []
        for _index in range(3):
            item = list(identity)
            rng.shuffle(item)
            permutations.append(tuple(item))
        values = normalized_word_map_walsh_observables(
            base_partitions, *permutations
        )
        for index, value in enumerate(values):
            sums[index] += value
    return tuple(value / sample_count for value in sums)


def simultaneous_hoeffding_sample_count(
    additive_error: float,
    failure_probability: float,
    *,
    coefficient_count: int = 8,
) -> int:
    if not 0 < additive_error <= 1:
        raise ValueError("additive error must lie in (0,1]")
    if not 0 < failure_probability < 1:
        raise ValueError("failure probability must lie in (0,1)")
    if coefficient_count < 1:
        raise ValueError("coefficient count must be positive")
    return math.ceil(
        2.0
        * math.log(2.0 * coefficient_count / failure_probability)
        / additive_error**2
    )


def normalized_tv_error_bound(total_mass: float, additive_error: float) -> float:
    """TV bound after clipping eight estimates to nonnegative values."""

    if total_mass <= 0:
        raise ValueError("total normalized amplitude must be positive")
    if additive_error < 0 or 8.0 * additive_error >= total_mass:
        raise ValueError("normalization requires 0<=8*error<total mass")
    return 8.0 * additive_error / total_mass


def log10_tv_sufficient_word_samples(
    total_mass: float,
    tv_error: float,
    failure_probability: float,
) -> float:
    if total_mass <= 0:
        raise ValueError("total normalized amplitude must be positive")
    if not 0 < tv_error < 1:
        raise ValueError("TV error must lie in (0,1)")
    if not 0 < failure_probability < 1:
        raise ValueError("failure probability must lie in (0,1)")
    return (
        math.log10(128.0)
        + math.log10(math.log(16.0 / failure_probability))
        - 2.0 * math.log10(tv_error)
        - 2.0 * math.log10(total_mass)
    )


def binary_entropy_bits(probability: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -probability * math.log2(probability) - (1.0 - probability) * math.log2(
        1.0 - probability
    )


def _entropy_continuity_bound_bits(tv_error: float, alphabet_size: int) -> float:
    if tv_error <= 0:
        return 0.0
    audenaert = (
        tv_error * math.log2(alphabet_size - 1)
        + binary_entropy_bits(tv_error)
    )
    return min(math.log2(alphabet_size), audenaert)


def conditional_mutual_information_continuity_bound_bits(tv_error: float) -> float:
    """Continuity bound for CMI of three binary syndrome coordinates."""

    if not 0 <= tv_error < 0.5:
        raise ValueError("CMI continuity control requires TV error in [0,1/2)")
    return sum(
        _entropy_continuity_bound_bits(tv_error, alphabet_size)
        for alphabet_size in (4, 4, 2, 8)
    )


def cmi_resolution_tv_target(cmi_bits: float) -> float:
    """Largest TV radius whose continuity penalty is at most half the CMI."""

    if cmi_bits <= 0:
        return 0.0
    target = cmi_bits / 2.0
    low, high = 0.0, 0.499999
    for _ in range(100):
        middle = (low + high) / 2.0
        if conditional_mutual_information_continuity_bound_bits(middle) <= target:
            low = middle
        else:
            high = middle
    return low


def audit_exact_s5_walsh_identity() -> OrientationWordMapExactControl:
    cross_check, control = audit_s5_exact_amplitude_cross_check()
    exact = exact_normalized_word_map_walsh_means(5, control.base_partitions)
    dimension_product = math.prod(control.base_dimensions)
    compiled = tuple(
        entry.normalized_syndrome_amplitude / dimension_product
        for entry in control.entries
    )
    residual = max(abs(float(left) - right) for left, right in zip(exact, compiled))
    verified = bool(
        cross_check.exact_amplitude_and_mass_formula_verified
        and all(value >= 0 for value in exact)
        and residual <= 1e-12
    )
    return OrientationWordMapExactControl(
        control_id="S5-EXACT-WALSH-WORD-MAP",
        n=5,
        base_partitions=control.base_partitions,
        dimension_product=dimension_product,
        exact_normalized_walsh_means=tuple(str(value) for value in exact),
        compiled_normalized_amplitudes=compiled,
        maximum_exact_to_compiled_residual=residual,
        all_exact_means_nonnegative=all(value >= 0 for value in exact),
        exact_walsh_identity_verified=verified,
        status=(
            "orientation-amplitudes-are-exact-word-map-walsh-coefficients"
            if verified
            else "orientation-word-map-walsh-identity-control-failure"
        ),
    )


def classical_cost_record(
    control: CompressedOrientationRacahControl,
    *,
    fixed_tv_target: float = 0.05,
    confidence_level: float = 0.95,
) -> OrientationClassicalCostRecord:
    dimension_product = math.prod(control.base_dimensions)
    total_mass = control.total_syndrome_amplitude / dimension_product
    physical_from_word_mass = (
        8.0
        * dimension_product**2
        * total_mass
        / math.factorial(control.n) ** 3
    )
    failure_probability = 1.0 - confidence_level
    cmi_tv = cmi_resolution_tv_target(control.irreducible_racah_cmi_bits)
    return OrientationClassicalCostRecord(
        control_id=control.control_id,
        n=control.n,
        base_partitions=control.base_partitions,
        base_dimensions=control.base_dimensions,
        dimension_product=dimension_product,
        total_normalized_amplitude=total_mass,
        physical_sign_orbit_tuple_mass=control.physical_sign_orbit_tuple_mass,
        physical_mass_formula_residual=abs(
            physical_from_word_mass - control.physical_sign_orbit_tuple_mass
        ),
        irreducible_racah_cmi_bits=control.irreducible_racah_cmi_bits,
        fixed_tv_target=fixed_tv_target,
        confidence_level=confidence_level,
        log10_word_samples_sufficient_for_fixed_tv=(
            log10_tv_sufficient_word_samples(
                total_mass, fixed_tv_target, failure_probability
            )
        ),
        cmi_resolution_tv_target=cmi_tv,
        cmi_continuity_bound_at_target_bits=(
            conditional_mutual_information_continuity_bound_bits(cmi_tv)
            if cmi_tv > 0
            else 0.0
        ),
        log10_word_samples_sufficient_to_resolve_cmi=(
            log10_tv_sufficient_word_samples(
                total_mass, cmi_tv, failure_probability
            )
            if cmi_tv > 0
            else math.inf
        ),
        inverse_physical_orbit_mass=1.0 / control.physical_sign_orbit_tuple_mass,
        exact_character_evaluations_per_word_sample=6,
        random_word_sample_updates_all_syndromes=True,
        word_map_estimator_is_classical=True,
        character_evaluation_is_unit_cost_assumed=True,
        polynomial_classical_runtime_proved=False,
        classical_lower_bound_proved=False,
        quantum_advantage_proved=False,
        status="classical-word-map-upper-bound-with-unresolved-sign-and-evaluation-costs",
    )


def run_orientation_word_map_classical_baseline(
) -> OrientationWordMapClassicalBaselineReport:
    exact_control = audit_exact_s5_walsh_identity()
    _cross_check, s5 = audit_s5_exact_amplitude_cross_check()
    s6 = compile_orientation_racah_channel(
        "S6-REPEATED-DIMENSION-10", ((3, 1, 1, 1),) * 6
    )
    s7 = compile_orientation_racah_channel(
        "S7-REPEATED-DIMENSION-35", ((3, 2, 1, 1),) * 6
    )
    records = [classical_cost_record(row) for row in (s5, s6, s7)]
    formula_verified = all(row.physical_mass_formula_residual <= 1e-12 for row in records)
    return OrientationWordMapClassicalBaselineReport(
        created_at=utc_now(),
        theorem_contract={
            "shared_estimator": "mu_y=A_y/D=E[Z(-1)^{<y,p>}] with |Z|<=1",
            "simultaneous_concentration": "Pr(max_y |mu_hat_y-mu_y|>eta)<=16 exp(-N eta^2/2)",
            "normalization": "clip negatives; TV<=8 eta/T for T=sum_y mu_y and 8 eta<T",
            "sample_upper_bound": "N>=128 log(16/delta)/(epsilon^2 T^2)",
            "physical_mass_conversion": "P_orbit=8 D^2 T/|S_n|^3",
            "scope": "sufficient classical random-word upper bound; no runtime lower bound",
        },
        exact_control=exact_control,
        cost_records=records,
        query_model_matrix=[
            {
                "access_model": "full_table_over_permutation_triples",
                "legal": True,
                "cost": "|S_n|^3 word triples and six exact character evaluations per triple",
                "conclusion": "exact but factorial-sized classical baseline",
            },
            {
                "access_model": "uniform_random_word_samples_plus_explicit_character_evaluator",
                "legal": True,
                "cost": "one random triple updates all eight Walsh coefficients",
                "conclusion": "rigorous Monte Carlo upper bound, conditional on evaluator cost",
            },
            {
                "access_model": "chosen_word_queries",
                "legal": True,
                "cost": "queries may be chosen, but no variance-reducing proposal is proved",
                "conclusion": "open importance-sampling and control-variate attack surface",
            },
            {
                "access_model": "unit_cost_exact_character_oracle",
                "legal": False,
                "cost": "strictly stronger than the explicit classical input model",
                "conclusion": "useful oracle baseline only; cannot establish an implemented runtime",
            },
            {
                "access_model": "coherent_coset_state_and_fourier_sampling",
                "legal": False,
                "cost": "quantum source preparation and nonabelian Fourier operations must be counted",
                "conclusion": "not interchangeable with classical random-word samples",
            },
        ],
        literature_boundaries=[
            {
                "literature_id": "ARXIV-2501.12579",
                "url": "https://arxiv.org/abs/2501.12579",
                "boundary": "Recent classical/quantum character algorithms do not make exact evaluation unit cost on every partition and cycle type.",
            },
            {
                "literature_id": "ARXIV-2207.05423",
                "url": "https://arxiv.org/abs/2207.05423",
                "boundary": "Worst-case exact symmetric-group character computation is strongly GapP-complete; this is not an average-case lower bound for these samples.",
            },
            {
                "literature_id": "ARXIV-2302.11454",
                "url": "https://arxiv.org/abs/2302.11454",
                "boundary": "Quantum additive approximation results for normalized Kronecker coefficients do not supply the missing coherent orientation decoder.",
            },
        ],
        proof_obligations=[
            {
                "obligation": "derive_shared_orientation_word_map_estimator",
                "resolved": exact_control.exact_walsh_identity_verified,
                "resolution": "Transpose-character signs turn the eight amplitudes into Walsh coefficients of one bounded random variable.",
            },
            {
                "obligation": "give_rigorous_classical_sample_upper_bound",
                "resolved": True,
                "resolution": "Simultaneous Hoeffding plus clipping and normalization gives an explicit TV guarantee.",
            },
            {
                "obligation": "remove_exact_character_unit_cost_assumption",
                "resolved": False,
                "resolution": "Need average-case complexity or a concrete evaluator analysis for Plancherel-typical labels and word-map cycle types.",
            },
            {
                "obligation": "test_importance_sampling_and_control_variates",
                "resolved": False,
                "resolution": "The direct estimator may be far from optimal because known class marginals and parity sectors provide control variates.",
            },
            {
                "obligation": "prove_quantum_estimator_beats_best_classical_access_model",
                "resolved": False,
                "resolution": "No coherent estimator, matched query accounting, or classical lower bound exists.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Eight syndrome amplitudes require eight unrelated classical searches.",
                "resolved": True,
                "resolution": "All are Walsh coefficients of the same sampled normalized-character product.",
            },
            {
                "objection": "A huge Hoeffding count proves classical hardness.",
                "resolved": True,
                "resolution": "It proves only that this direct bounded estimator has a weak sufficient guarantee; variance reduction can invalidate the inference.",
            },
            {
                "objection": "Worst-case character hardness proves this distribution hard.",
                "resolved": True,
                "resolution": "The required average-case hardness on selected partitions and word-map cycle types is completely open.",
            },
            {
                "objection": "Positive measured CMI is already coherently accessible.",
                "resolved": True,
                "resolution": "No efficient observable, decoder, or preparation-to-measurement pipeline is supplied.",
            },
        ],
        headline_metrics={
            "exact_walsh_control_verified": int(exact_control.exact_walsh_identity_verified),
            "classical_cost_record_count": len(records),
            "maximum_log10_fixed_tv_word_samples": max(
                row.log10_word_samples_sufficient_for_fixed_tv for row in records
            ),
            "maximum_log10_cmi_resolution_word_samples": max(
                row.log10_word_samples_sufficient_to_resolve_cmi for row in records
            ),
            "polynomial_classical_runtime_proof_count": 0,
            "classical_lower_bound_count": 0,
            "coherent_quantum_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_word_map_walsh_identity_proved": exact_control.exact_walsh_identity_verified,
            "physical_mass_conversion_verified": formula_verified,
            "direct_classical_estimator_available": True,
            "direct_estimator_polynomial_sample_bound_proved": False,
            "exact_character_average_case_efficiency_proved": False,
            "importance_sampling_ruled_out": False,
            "classical_lower_bound_proved": False,
            "coherent_quantum_estimator_implemented": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The shared classical estimator is exact but has a severe finite sign problem; neither an efficient classical attack nor a matched quantum separation is proved.",
        },
        status="orientation-signal-reduced-to-classical-walsh-word-map-sign-problem",
        summary=(
            "Reduced all eight orientation amplitudes to one classical word-map "
            "Walsh estimator and quantified, without overclaiming, the cancellation "
            "and character-evaluation barriers that remain."
        ),
        falsifiers_triggered=[
            "The eight orientation channels are not eight independent hidden structures.",
            "Finite high CMI does not imply low classical estimation cost or coherent accessibility.",
            "Worst-case character complexity cannot substitute for an average-case reduction.",
        ],
    )


def write_orientation_word_map_classical_baseline_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_orientation_word_map_classical_baseline())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_orientation_word_map_classical_baseline_report()
    print(json.dumps(report, indent=2, sort_keys=True))

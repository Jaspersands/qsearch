"""Untrimmed tetrahedral chi-square is dominated by a rare parity tail.

The physical six-label recoupling law has a useful exact classical dual.  Let
``g,h,k`` be independent uniform permutations in ``S_n`` and form the six
words

    W(g,h,k) = (g, h, k, gk, hk, ghk).                    (1)

Let ``P_word`` be their joint cycle-type law and let ``Q_word`` be the product
of six uniform-permutation cycle-type laws.  Plancherel character
orthogonality gives

    chi^2(P_physical || Plancherel^6)
      = chi^2(P_word || Q_word)
      = sum_C N_C^2 / product_i |C_i| - 1,                (2)

where ``N_C`` counts triples with six-class signature ``C``.  Thus the full
Racah-label second moment is exactly a classical word-map collision norm.

Expanding each class kernel into its identity and nonidentity parts leaves
only fifteen support masks.  Put

    V  = sum_(C!=e) |C|^-1,
    V4 = sum_(C!=e) |C|^-2,
    M2 = E_Pl[(sum_(C!=e) r_lambda(C)^2)^2].

Four masks contribute ``V``, three contribute ``V4``, six contribute
``M2-V4``, and the fully nonidentity mask contributes ``Z6``.  Hence

    chi^2 = 4 V + 6 M2 - 3 V4 + Z6.                      (3)

The previous source-conditioned theorem proves every displayed lower-support
term tends to zero.  The only unresolved class-word term is ``Z6``.

However, untrimmed chi-square can never vanish.  Restrict all six irrep labels
to the trivial/sign representations and encode them by bits
``a,b,c,m,u,l``.  Their likelihood is ``|S_n|^3`` exactly when

    a+b+m = b+c+u = a+b+c+l = 0 mod 2,                  (4)

and zero otherwise.  Eight of the 64 sign patterns satisfy (4).  This tiny
sector alone contributes

    8 - 16/|S_n|^3 + 64/|S_n|^6                         (5)

to chi-square, tending to eight.  Yet its physical probability is only
``8/|S_n|^3``; even the union of all sectors containing any one-dimensional
label has physical mass at most ``12/|S_n|`` by exact Plancherel marginals.

Therefore raw chi-square, fourth moments, and maximum likelihood ratios are
invalid decision metrics for positive-mass tetrahedral structure.  The
correct next observable is dimension-trimmed total variation or KL divergence
(and source/final-conditioned mutual information) with the removed physical
mass reported explicitly.  The parity tail is a metric no-go, not an
algorithmic signal and not proof that trimmed dependence vanishes.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)
from self_dual_wreath_shared_pair_recoupling_decoupling import (
    inverse_class_square_sum,
)
from self_dual_wreath_source_conditioned_channel_decoupling import (
    plancherel_character_energy_moments,
)
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_tetrahedral_chi_square_tail_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-CHI-SQUARE-TAIL-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Signature = tuple[Partition, Partition, Partition, Partition, Partition, Partition]

WORD_NAMES = ("g", "h", "k", "gk", "hk", "ghk")


@dataclass(frozen=True)
class TetrahedralClassSignatureControl:
    n: int
    group_order: int
    conjugacy_class_count: int
    occupied_signature_count: int
    exact_signature_probability_sum: str
    exact_full_second_moment: str
    exact_full_chi_square: str
    exact_low_support_contribution: str
    exact_fully_nonidentity_core: str
    exact_decomposition_residual: str
    support_mask_count: int
    size_three_mask_count: int
    size_four_mask_count: int
    size_five_mask_count: int
    exact_support_decomposition_verified: bool
    exact_class_signature_duality_verified: bool
    status: str


@dataclass(frozen=True)
class FinitePhysicalSixLabelControl:
    n: int
    partition_count: int
    label_tuple_count: int
    physical_probability_sum_residual: float
    minimum_likelihood: float
    maximum_likelihood: float
    total_variation_from_plancherel_product: float
    kl_divergence_bits: float
    chi_square_from_plancherel_product: float
    class_signature_chi_square: float
    chi_square_duality_residual: float
    physical_mass_with_any_one_dimensional_label: float
    union_bound_for_any_one_dimensional_label: float
    physical_mass_with_all_one_dimensional_labels: float
    exact_all_one_dimensional_mass: float
    all_one_dimensional_mass_residual: float
    status: str


@dataclass(frozen=True)
class ParityTailScalingRecord:
    n: int
    group_order_log2: float
    exact_restricted_chi_square_contribution: float
    exact_all_one_dimensional_physical_mass: float
    any_one_dimensional_physical_mass_upper_bound: float
    untrimmed_chi_square_vanishing_falsified: bool
    positive_mass_signal_certified: bool
    status: str


@dataclass(frozen=True)
class TetrahedralChiSquareTailNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_signature_controls: list[TetrahedralClassSignatureControl]
    finite_physical_controls: list[FinitePhysicalSixLabelControl]
    scaling_records: list[ParityTailScalingRecord]
    support_decomposition: dict[str, str | int | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def tetrahedral_class_signature_counts(n: int) -> dict[Signature, int]:
    if not 2 <= n <= 5:
        raise ValueError("exact class-signature enumeration requires 2<=n<=5")
    group = tuple(itertools.permutations(range(n)))
    cycle_type = {element: permutation_cycle_type(element) for element in group}
    counts: Counter[Signature] = Counter()
    for g in group:
        for h in group:
            gh = compose_permutations(g, h)
            for k in group:
                counts[
                    (
                        cycle_type[g],
                        cycle_type[h],
                        cycle_type[k],
                        cycle_type[compose_permutations(g, k)],
                        cycle_type[compose_permutations(h, k)],
                        cycle_type[compose_permutations(gh, k)],
                    )
                ] += 1
    return dict(counts)


def _signature_collision_contribution(signature: Signature, count: int) -> Fraction:
    return Fraction(
        count * count,
        math.prod(conjugacy_class_size(cycle_type) for cycle_type in signature),
    )


def tetrahedral_signature_second_moment(n: int) -> Fraction:
    return sum(
        (
            _signature_collision_contribution(signature, count)
            for signature, count in tetrahedral_class_signature_counts(n).items()
        ),
        start=Fraction(),
    )


def tetrahedral_support_contributions(n: int) -> dict[int, Fraction]:
    identity = (1,) * n
    rows: defaultdict[int, Fraction] = defaultdict(Fraction)
    for signature, count in tetrahedral_class_signature_counts(n).items():
        mask = sum(
            (cycle_type != identity) << index
            for index, cycle_type in enumerate(signature)
        )
        rows[mask] += _signature_collision_contribution(signature, count)
    return dict(rows)


def parity_tail_chi_square_contribution(n: int) -> Fraction:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    return Fraction(8) - Fraction(16, order**3) + Fraction(64, order**6)


def all_one_dimensional_physical_mass(n: int) -> Fraction:
    if n < 2:
        raise ValueError("n must be at least two")
    return Fraction(8, math.factorial(n) ** 3)


def audit_tetrahedral_class_signature(n: int) -> TetrahedralClassSignatureControl:
    if n < 3:
        raise ValueError("the fifteen-mask decomposition starts at n=3")
    counts = tetrahedral_class_signature_counts(n)
    order = math.factorial(n)
    second = tetrahedral_signature_second_moment(n)
    chi_square = second - 1
    supports = tetrahedral_support_contributions(n)
    variance = reciprocal_nonidentity_class_sum(n)
    inverse_square = inverse_class_square_sum(n)
    _, energy_second = plancherel_character_energy_moments(n)
    expected_by_size = {
        0: [Fraction(1)],
        3: [variance] * 4,
        4: [inverse_square] * 3,
        5: [energy_second - inverse_square] * 6,
    }
    grouped: defaultdict[int, list[Fraction]] = defaultdict(list)
    for mask, value in supports.items():
        grouped[mask.bit_count()].append(value)
    for values in grouped.values():
        values.sort()
    lower = 4 * variance + 6 * energy_second - 3 * inverse_square
    full_mask = (1 << len(WORD_NAMES)) - 1
    core = supports[full_mask]
    residual = chi_square - lower - core
    expected_masks = (
        len(supports) == 15
        and all(grouped[size] == sorted(values) for size, values in expected_by_size.items())
        and len(grouped[6]) == 1
    )
    probability_sum = Fraction(sum(counts.values()), order**3)
    verified = probability_sum == 1 and residual == 0 and expected_masks
    return TetrahedralClassSignatureControl(
        n=n,
        group_order=order,
        conjugacy_class_count=len(integer_partitions(n)),
        occupied_signature_count=len(counts),
        exact_signature_probability_sum=str(probability_sum),
        exact_full_second_moment=str(second),
        exact_full_chi_square=str(chi_square),
        exact_low_support_contribution=str(lower),
        exact_fully_nonidentity_core=str(core),
        exact_decomposition_residual=str(residual),
        support_mask_count=len(supports),
        size_three_mask_count=len(grouped[3]),
        size_four_mask_count=len(grouped[4]),
        size_five_mask_count=len(grouped[5]),
        exact_support_decomposition_verified=expected_masks and residual == 0,
        exact_class_signature_duality_verified=verified,
        status=(
            "exact-tetrahedral-class-signature-decomposition-verified"
            if verified
            else "tetrahedral-class-signature-control-failure"
        ),
    )


@lru_cache(maxsize=None)
def finite_physical_likelihood_arrays(
    n: int,
) -> tuple[tuple[Partition, ...], np.ndarray, np.ndarray, np.ndarray]:
    if not 2 <= n <= 5:
        raise ValueError("finite physical transforms require 2<=n<=5")
    partitions = tuple(integer_partitions(n))
    cycle_types = tuple(integer_partitions(n))
    cycle_index = {cycle_type: index for index, cycle_type in enumerate(cycle_types)}
    ratios = np.asarray(
        [
            [
                symmetric_character(partition, cycle_type)
                / hook_length_dimension(partition)
                for cycle_type in cycle_types
            ]
            for partition in partitions
        ],
        dtype=float,
    )
    shape = (len(partitions),) * 6
    likelihood = np.zeros(shape, dtype=float)
    for signature, count in tetrahedral_class_signature_counts(n).items():
        indices = tuple(cycle_index[cycle_type] for cycle_type in signature)
        # Label-axis order is alpha,beta,gamma,mu,nu,lambda.
        vectors = (
            ratios[:, indices[3]],
            ratios[:, indices[5]],
            ratios[:, indices[4]],
            ratios[:, indices[0]],
            ratios[:, indices[1]],
            ratios[:, indices[2]],
        )
        likelihood += count * np.einsum(
            "a,b,c,d,e,f->abcdef",
            *vectors,
            optimize=False,
        )
    likelihood[np.abs(likelihood) < 1e-10] = 0.0
    if float(likelihood.min()) < -1e-8:
        raise ArithmeticError("finite physical likelihood became negative")
    likelihood = np.maximum(likelihood, 0.0)
    weights = np.asarray(
        [float(weight) for weight in plancherel_weights(n)],
        dtype=float,
    )
    product = np.einsum(
        "a,b,c,d,e,f->abcdef",
        weights,
        weights,
        weights,
        weights,
        weights,
        weights,
        optimize=False,
    )
    physical = product * likelihood
    return partitions, likelihood, product, physical


@lru_cache(maxsize=None)
def finite_physical_six_label_control(n: int) -> FinitePhysicalSixLabelControl:
    partitions, likelihood, product, physical = finite_physical_likelihood_arrays(n)
    chi_square = float(np.sum(product * (likelihood - 1.0) ** 2))
    signature_chi = float(tetrahedral_signature_second_moment(n) - 1)
    total_variation = 0.5 * float(np.sum(np.abs(physical - product)))
    positive = physical > 0
    kl_bits = float(
        np.sum(physical[positive] * np.log2(likelihood[positive]))
    )
    dimensions = np.asarray(
        [hook_length_dimension(partition) for partition in partitions]
    )
    any_one_dimensional = np.zeros(shape, dtype=bool)
    all_one_dimensional = np.ones(shape, dtype=bool)
    for axis in range(6):
        axis_shape = [1] * 6
        axis_shape[axis] = len(partitions)
        axis_mask = (dimensions == 1).reshape(axis_shape)
        any_one_dimensional |= axis_mask
        all_one_dimensional &= axis_mask
    any_mass = float(np.sum(physical[any_one_dimensional]))
    all_mass = float(np.sum(physical[all_one_dimensional]))
    exact_all = float(all_one_dimensional_physical_mass(n))
    residual = abs(all_mass - exact_all)
    normalization = abs(float(np.sum(physical)) - 1.0)
    dual_residual = abs(chi_square - signature_chi)
    union_bound = min(1.0, 12.0 / math.factorial(n))
    verified = max(normalization, dual_residual, residual) <= 1e-8
    return FinitePhysicalSixLabelControl(
        n=n,
        partition_count=len(partitions),
        label_tuple_count=len(partitions) ** 6,
        physical_probability_sum_residual=normalization,
        minimum_likelihood=float(likelihood.min()),
        maximum_likelihood=float(likelihood.max()),
        total_variation_from_plancherel_product=total_variation,
        kl_divergence_bits=max(0.0, kl_bits),
        chi_square_from_plancherel_product=chi_square,
        class_signature_chi_square=signature_chi,
        chi_square_duality_residual=dual_residual,
        physical_mass_with_any_one_dimensional_label=any_mass,
        union_bound_for_any_one_dimensional_label=union_bound,
        physical_mass_with_all_one_dimensional_labels=all_mass,
        exact_all_one_dimensional_mass=exact_all,
        all_one_dimensional_mass_residual=residual,
        status=(
            "exact-physical-class-signature-chi-square-duality-verified"
            if verified
            else "physical-class-signature-duality-control-failure"
        ),
    )


def parity_tail_scaling_record(n: int) -> ParityTailScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    return ParityTailScalingRecord(
        n=n,
        group_order_log2=math.lgamma(n + 1) / math.log(2),
        exact_restricted_chi_square_contribution=float(
            parity_tail_chi_square_contribution(n)
        ),
        exact_all_one_dimensional_physical_mass=float(
            all_one_dimensional_physical_mass(n)
        ),
        any_one_dimensional_physical_mass_upper_bound=min(1.0, 12.0 / order),
        untrimmed_chi_square_vanishing_falsified=True,
        positive_mass_signal_certified=False,
        status="constant-chi-square-parity-tail-has-vanishing-physical-mass",
    )


def run_tetrahedral_chi_square_tail_no_go(
) -> TetrahedralChiSquareTailNoGoReport:
    signatures = [audit_tetrahedral_class_signature(n) for n in range(3, 6)]
    physical = [finite_physical_six_label_control(n) for n in range(2, 6)]
    scaling = [parity_tail_scaling_record(n) for n in (6, 8, 10, 20, 30, 50)]
    failures = sum(
        row.status != "exact-tetrahedral-class-signature-decomposition-verified"
        for row in signatures
    ) + sum(
        row.status != "exact-physical-class-signature-chi-square-duality-verified"
        for row in physical
    )
    verified = failures == 0
    tail = scaling[-1]
    return TetrahedralChiSquareTailNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "class_signature_duality": (
                "Physical six-label chi-square equals the cycle-type chi-square "
                "of (g,h,k,gk,hk,ghk)."
            ),
            "support_decomposition": (
                "chi^2=4V_n+6E_Pl[T_lambda^2]-3V4_n+Z6_n."
            ),
            "low_support_terms": (
                "All terms outside the fully nonidentity core Z6_n vanish."
            ),
            "one_dimensional_parity_likelihood": (
                "Eight trivial/sign patterns satisfying three parity equations "
                "have likelihood (n!)^3; the other 56 have likelihood zero."
            ),
            "chi_square_tail": (
                "The all-one-dimensional sector contributes "
                "8-16/(n!)^3+64/(n!)^6 to chi-square."
            ),
            "tail_mass": (
                "Its physical mass is 8/(n!)^3; any one-dimensional label has "
                "physical union mass at most 12/n!."
            ),
            "scope": (
                "Raw chi-square is invalidated, but dimension-trimmed TV/KL and "
                "coherent multiplicity-phase information remain open."
            ),
        },
        exact_signature_controls=signatures,
        finite_physical_controls=physical,
        scaling_records=scaling,
        support_decomposition={
            "allowed_support_mask_count": 15,
            "size_three_mask_count": 4,
            "each_size_three_contribution": "V_n",
            "size_four_mask_count": 3,
            "each_size_four_contribution": "V4_n",
            "size_five_mask_count": 6,
            "each_size_five_contribution": "E_Pl[T_lambda^2]-V4_n",
            "size_six_mask_count": 1,
            "size_six_contribution": "Z6_n",
            "all_lower_support_contributions_vanish": True,
            "fully_nonidentity_core_chi_square_vanishes": False,
            "fully_nonidentity_core_positive_mass_signal_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "derive_physical_class_signature_chi_square_duality",
                "resolved": True,
                "resolution": (
                    "Expand the six-character likelihood and apply Plancherel "
                    "column orthogonality independently on every edge."
                ),
            },
            {
                "obligation": "decide_untrimmed_six_label_chi_square_vanishing",
                "resolved": True,
                "resolution": (
                    "It is false: the trivial/sign parity sector contributes 8-o(1)."
                ),
            },
            {
                "obligation": "separate_tail_chi_square_from_positive_physical_mass",
                "resolved": True,
                "resolution": (
                    "The witness mass is 8/(n!)^3 and the entire one-dimensional "
                    "union has mass at most 12/n!."
                ),
            },
            {
                "obligation": "bound_dimension_trimmed_tetrahedral_tv_or_kl",
                "resolved": False,
                "resolution": (
                    "Choose an explicit Plancherel-typical dimension/shape trim, "
                    "bound removed physical mass, and estimate TV/KL on the retained law."
                ),
            },
            {
                "obligation": "bound_coherent_multiplicity_phase_information",
                "resolved": False,
                "resolution": "The class-signature dual sees label probabilities only.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A nonvanishing full chi-square proves a useful measured-label signal.",
                "resolved": True,
                "resolution": (
                    "False. A factorially rare sector has factorial likelihood and "
                    "alone supplies a constant second moment."
                ),
            },
            {
                "objection": "The parity equations give three bits on typical physical samples.",
                "resolved": True,
                "resolution": (
                    "They are exact only on the all-one-dimensional irrep sector, "
                    "whose physical mass is 8/(n!)^3."
                ),
            },
            {
                "objection": "Removing one-dimensional irreps proves the remaining law is flat.",
                "resolved": False,
                "resolution": (
                    "Other low-dimensional tails and a genuinely typical tetrahedral "
                    "core may remain; a scalable trim theorem is still required."
                ),
            },
            {
                "objection": "Classical word-map duality dequantizes coherent recoupling.",
                "resolved": False,
                "resolution": (
                    "It evaluates a dephased second moment, not a coherent Racah transform."
                ),
            },
        ],
        headline_metrics={
            "class_signature_duality_theorem_count": 1,
            "support_mask_decomposition_theorem_count": 1,
            "untrimmed_chi_square_metric_no_go_count": 1,
            "one_dimensional_parity_tail_theorem_count": 1,
            "exact_signature_control_count": len(signatures),
            "finite_physical_control_count": len(physical),
            "control_failure_count": failures,
            "maximum_exact_control_n": 5,
            "asymptotic_chi_square_lower_bound": 8.0,
            "n50_all_one_dimensional_physical_mass": (
                tail.exact_all_one_dimensional_physical_mass
            ),
            "dimension_trimmed_tv_kl_theorem_count": 0,
            "positive_mass_measured_signal_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_class_signature_chi_square_duality_proved": verified,
            "all_lower_support_class_word_terms_vanish_proved": verified,
            "untrimmed_six_label_chi_square_vanishing_falsified": verified,
            "constant_chi_square_witness_has_vanishing_physical_mass_proved": verified,
            "untrimmed_chi_square_valid_positive_mass_metric": False,
            "dimension_trimmed_total_variation_vanishes_proved": False,
            "dimension_trimmed_total_variation_survives_proved": False,
            "final_label_conditioned_mutual_information_vanishes_proved": False,
            "coherent_multiplicity_phase_signal_absent_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The only proved asymptotic six-label signal is an L2 tail on "
                "factorially rare trivial/sign sectors; typical-mass TV/KL is open."
            ),
        },
        status=(
            "tetrahedral-chi-square-tail-metric-rejected-trimmed-core-open"
            if verified
            else "tetrahedral-chi-square-tail-control-failure"
        ),
        summary=(
            "Reduced six-label chi-square to a classical six-word cycle-type "
            "collision norm and proved that its nonvanishing parity tail has "
            "factorially vanishing physical mass, forcing dimension-trimmed metrics."
        ),
        falsifiers_triggered=[
            "Raw six-label chi-square cannot vanish because of exact trivial/sign parity constraints.",
            "Constant chi-square does not imply positive-mass measured-label correlation.",
            "All lower-support word-map contributions vanish; only the fully nonidentity core remains after trimming.",
        ],
    )


def write_tetrahedral_chi_square_tail_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_tetrahedral_chi_square_tail_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_tetrahedral_chi_square_tail_no_go_report()
    print(json.dumps(report, indent=2))

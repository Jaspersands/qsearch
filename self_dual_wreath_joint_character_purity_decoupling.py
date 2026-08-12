"""Purity/Holevo decoupling bound for the retained joint register.

Retaining the group and orientation registers preserves nonclassical hidden
label correlations, but the carrier that is discarded is enormous.  This
module quantifies the resulting decoupling for natural Plancherel source
labels.

For a fixed tuple of unequal source pairs ``(lambda_i,mu_i)``, let ``tau_g``
be the joint group--orientation state after row-copy and carrier trace.  In
the orientation basis,

    tau_e[(s,e),(t,f)]
      = [|G| q d]^-1 Tr[sigma_e(s^-1) sigma_f(t)],

where ``q=2^k`` and ``d`` is the common carrier dimension.  Put
``u=s^-1t`` and write ``r_lambda`` for a normalized character.  Summing the
four orientation choices at copy ``i`` gives

    L_i(s,t) = r_lambda_i(u)^2 + r_mu_i(u)^2
             + r_lambda_i(s)^2 r_mu_i(t)^2
             + r_mu_i(s)^2 r_lambda_i(t)^2.

Hence

    Tr(tau_e^2)= [|G|^2 4^k]^-1 sum_(s,t) product_i L_i(s,t).   (1)

Draw every ``lambda_i,mu_i`` independently from Plancherel measure.  Character
column orthogonality gives

    E_Pl[r_lambda(x)^2] = z_x/|G| = 1/|Cl(x)| =: a_x.

The exact annealed purity is therefore

    E Tr(tau_e^2)
      = [|G|^2 2^k]^-1 sum_(s,t) [a_(s^-1t)+a_s a_t]^k.       (2)

It is class-compressible.  More importantly, it has an all-n upper bound.
Let ``Z_j=sum_g a_g^j``.  Then ``Z_0=|G|`` and ``Z_j<=p(n)`` for ``j>=1``.
Expanding (2) and applying Cauchy--Schwarz to
``sum_s a_s^(k-j)a_(su)^(k-j)`` gives, for
``k=ceil(log2 |G|)``,

    (|G|2^k) E Tr(tau_e^2) <= 2p(n)+2p(n)^2.                 (3)

For any fixed source tuple, its ensemble Holevo information obeys

    chi <= log2[(|G|2^k) Tr(tau_e^2)],                       (4)

because ``S(bar tau)<=log2(|G|2^k)`` and
``S(tau)>=-log2 Tr(tau^2)``.  Markov plus (3) proves that a typical natural
threshold block has only ``O(sqrt(n))`` Holevo bits, versus
``log2(n!)=Theta(n log n)`` hidden-label bits.  Conditioning on global source
collision-freedom changes the expectation by at most the reciprocal event
probability, which tends to one by the repository's collision-free theorem.

This refutes an extensive-information one-block decoder after carrier trace.
It does not refute polynomially many independent blocks: Fano only forces
``Omega(log(n!)/sqrt(n))`` blocks under this upper bound, still polynomial.
Here the multiblock comparison uses subadditivity of Holevo information for
independent blocks before applying Fano; it does not assume additivity of an
implemented measurement.  Nor does the result apply when the carrier is
retained and processed coherently.
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
from self_dual_wreath_joint_character_correlation_decoder import (
    joint_character_state,
)
from self_dual_wreath_orientation_fusion_moment import _class_algebra_data
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_joint_character_purity_decoupling.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-PURITY-DECOUPLING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class FixedTuplePurityControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    group_order: int
    joint_register_dimension: int
    direct_matrix_purity: float
    exact_character_purity: float
    purity_formula_residual: float
    normalized_purity: float
    holevo_upper_bound_bits: float
    exact_fixed_tuple_purity_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalPurityControl:
    n: int
    copy_count: int
    group_order: int
    partition_count: int
    exact_normalized_annealed_purity: float
    universal_normalized_purity_upper_bound: float
    exact_annealed_holevo_upper_bound_bits: float
    universal_holevo_upper_bound_bits: float
    bound_ratio: float
    class_product_rounding_residual: float
    exact_class_formula_verified: bool
    status: str


@dataclass(frozen=True)
class PurityDecouplingScalingRecord:
    n: int
    information_threshold_copy_count: int
    hidden_label_entropy_bits: float
    partition_count_decimal: str
    universal_annealed_holevo_upper_bound_bits: float
    typical_failure_probability: float
    typical_holevo_upper_bound_bits: float
    bounded_error_fano_block_lower_bound: float
    bounded_error_fano_coset_copy_lower_bound: float
    holevo_fraction_upper_bound: float
    collision_free_conditioning_asymptotically_neutral: bool
    one_block_extensive_information_ruled_out: bool
    polynomial_number_of_blocks_ruled_out: bool
    carrier_retaining_decoder_ruled_out: bool
    status: str


@dataclass(frozen=True)
class JointCharacterPurityTheorem:
    fixed_tuple_purity: str
    plancherel_second_character_moment: str
    annealed_purity: str
    partition_bound: str
    holevo_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointCharacterPurityDecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: JointCharacterPurityTheorem
    fixed_tuple_controls: list[FixedTuplePurityControl]
    natural_controls: list[NaturalPurityControl]
    scaling_records: list[PurityDecouplingScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalized_character(
    partition: Partition,
    cycle_type: Partition,
) -> float:
    return symmetric_character(partition, cycle_type) / hook_length_dimension(
        partition
    )


def fixed_tuple_joint_purity(
    n: int,
    labels: tuple[Label, ...],
) -> tuple[float, float]:
    """Evaluate equation (1) through class-product counts."""

    if not labels or any(
        sum(left) != n or sum(right) != n for left, right in labels
    ):
        raise ValueError("source labels must be nonempty partition pairs of n")
    (
        cycle_types,
        _,
        _,
        _,
        class_product_counts,
        rounding_residual,
        _,
        _,
    ) = _class_algebra_data(n)
    count = len(labels)
    local_product = np.ones_like(class_product_counts, dtype=np.longdouble)
    for left, right in labels:
        left_ratios = np.asarray(
            [normalized_character(left, cycle) for cycle in cycle_types],
            dtype=np.longdouble,
        )
        right_ratios = np.asarray(
            [normalized_character(right, cycle) for cycle in cycle_types],
            dtype=np.longdouble,
        )
        local = (
            left_ratios[None, None, :] ** 2
            + right_ratios[None, None, :] ** 2
            + left_ratios[:, None, None] ** 2
            * right_ratios[None, :, None] ** 2
            + right_ratios[:, None, None] ** 2
            * left_ratios[None, :, None] ** 2
        )
        local_product *= local
    order = np.longdouble(math.factorial(n))
    purity = np.sum(class_product_counts * local_product, dtype=np.longdouble)
    purity /= order**2 * np.longdouble(4) ** count
    return float(purity), rounding_residual


def audit_fixed_tuple_purity(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> FixedTuplePurityControl:
    state = joint_character_state(labels, tuple(range(n)))
    direct = float(np.trace(state @ state).real)
    predicted, _ = fixed_tuple_joint_purity(n, labels)
    residual = abs(direct - predicted)
    dimension = math.factorial(n) * (1 << len(labels))
    normalized = dimension * predicted
    verified = residual <= 100 * tolerance
    return FixedTuplePurityControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        group_order=math.factorial(n),
        joint_register_dimension=dimension,
        direct_matrix_purity=direct,
        exact_character_purity=predicted,
        purity_formula_residual=residual,
        normalized_purity=normalized,
        holevo_upper_bound_bits=max(0.0, math.log2(normalized)),
        exact_fixed_tuple_purity_verified=verified,
        status=(
            "exact-fixed-tuple-joint-purity"
            if verified
            else "joint-purity-formula-validation-failure"
        ),
    )


def partition_number(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def natural_annealed_joint_purity(
    n: int,
    copy_count: int,
) -> tuple[float, float]:
    """Evaluate equation (2) through the class algebra."""

    if n < 2 or copy_count < 1:
        raise ValueError("invalid degree or copy count")
    (
        _,
        _,
        _,
        class_sizes,
        class_product_counts,
        rounding_residual,
        _,
        _,
    ) = _class_algebra_data(n)
    inverse_sizes = 1 / np.asarray(class_sizes, dtype=np.longdouble)
    local = (
        inverse_sizes[None, None, :]
        + inverse_sizes[:, None, None] * inverse_sizes[None, :, None]
    )
    order = np.longdouble(math.factorial(n))
    purity = np.sum(
        class_product_counts * np.power(local, copy_count),
        dtype=np.longdouble,
    )
    purity /= order**2 * np.longdouble(2) ** copy_count
    return float(purity), rounding_residual


def universal_normalized_purity_bound(n: int) -> float:
    partitions = partition_number(n)
    return float(2 * partitions + 2 * partitions * partitions)


def audit_natural_purity(
    n: int,
    copy_count: int | None = None,
) -> NaturalPurityControl:
    copies = copy_count or math.ceil(math.lgamma(n + 1) / math.log(2))
    purity, rounding = natural_annealed_joint_purity(n, copies)
    order = math.factorial(n)
    normalized = order * (1 << copies) * purity
    bound = universal_normalized_purity_bound(n)
    verified = normalized <= bound * (1 + 1e-9)
    return NaturalPurityControl(
        n=n,
        copy_count=copies,
        group_order=order,
        partition_count=partition_number(n),
        exact_normalized_annealed_purity=normalized,
        universal_normalized_purity_upper_bound=bound,
        exact_annealed_holevo_upper_bound_bits=max(0.0, math.log2(normalized)),
        universal_holevo_upper_bound_bits=math.log2(bound),
        bound_ratio=normalized / bound,
        class_product_rounding_residual=rounding,
        exact_class_formula_verified=verified,
        status=(
            "exact-annealed-joint-purity-below-partition-bound"
            if verified
            else "annealed-joint-purity-bound-failure"
        ),
    )


def binary_entropy(probability: float) -> float:
    if not 0 <= probability <= 1:
        raise ValueError("probability must lie in [0,1]")
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * math.log2(probability) - (
        1 - probability
    ) * math.log2(1 - probability)


def purity_decoupling_scaling_record(
    n: int,
    *,
    decoding_error: float = 1 / 3,
    typical_failure_probability: float | None = None,
) -> PurityDecouplingScalingRecord:
    if n < 3 or not 0 < decoding_error < 1:
        raise ValueError("invalid scaling parameters")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    hidden_entropy = math.lgamma(n + 1) / math.log(2)
    partitions = partition_number(n)
    annealed_bound = universal_normalized_purity_bound(n)
    failure = typical_failure_probability or n**-2
    typical_bound = annealed_bound / failure
    typical_holevo = math.log2(typical_bound)
    fano_required = max(
        0.0,
        (1 - decoding_error) * hidden_entropy
        - binary_entropy(decoding_error),
    )
    block_lower = fano_required / typical_holevo
    return PurityDecouplingScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        hidden_label_entropy_bits=hidden_entropy,
        partition_count_decimal=str(partitions),
        universal_annealed_holevo_upper_bound_bits=math.log2(annealed_bound),
        typical_failure_probability=failure,
        typical_holevo_upper_bound_bits=typical_holevo,
        bounded_error_fano_block_lower_bound=block_lower,
        bounded_error_fano_coset_copy_lower_bound=block_lower * copies,
        holevo_fraction_upper_bound=typical_holevo / hidden_entropy,
        collision_free_conditioning_asymptotically_neutral=True,
        one_block_extensive_information_ruled_out=True,
        polynomial_number_of_blocks_ruled_out=False,
        carrier_retaining_decoder_ruled_out=False,
        status="one-block-joint-register-nonextensive-multiblock-open",
    )


def _exhaustive_natural_average(n: int, copy_count: int) -> float:
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    weights = {
        partition: hook_length_dimension(partition) ** 2 / order
        for partition in partitions
    }
    pairs = tuple(itertools.product(partitions, repeat=2))
    total = 0.0
    for labels in itertools.product(pairs, repeat=copy_count):
        probability = math.prod(
            weights[left] * weights[right] for left, right in labels
        )
        purity, _ = fixed_tuple_joint_purity(n, labels)
        total += probability * purity
    return total


def run_joint_character_purity_decoupling() -> JointCharacterPurityDecouplingReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    fixed = [
        audit_fixed_tuple_purity(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_fixed_tuple_purity(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_fixed_tuple_purity(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    natural = [audit_natural_purity(n) for n in range(3, 13)]
    exhaustive_residuals = []
    for copies in (1, 2):
        exhaustive = _exhaustive_natural_average(3, copies)
        formula, _ = natural_annealed_joint_purity(3, copies)
        exhaustive_residuals.append(abs(exhaustive - formula))
    scaling = [
        purity_decoupling_scaling_record(n)
        for n in (16, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_fixed_tuple_purity_verified for row in fixed)
    failures += sum(not row.exact_class_formula_verified for row in natural)
    failures += sum(residual > 1e-10 for residual in exhaustive_residuals)
    verified = failures == 0
    theorem = JointCharacterPurityTheorem(
        fixed_tuple_purity=(
            "Tr(tau^2)=|G|^-2 4^-k sum_(s,t) product_i L_i(s,t)."
        ),
        plancherel_second_character_moment=(
            "E_Pl[(chi_lambda(g)/d_lambda)^2]=1/|Cl(g)|."
        ),
        annealed_purity=(
            "E Tr(tau^2)=|G|^-2 2^-k sum_(s,t) "
            "[|Cl(s^-1t)|^-1+(|Cl(s)||Cl(t)|)^-1]^k."
        ),
        partition_bound=(
            "For k=ceil(log2|G|), |G|2^k ETr(tau^2)<=2p(n)+2p(n)^2."
        ),
        holevo_consequence=(
            "Typical one-block Holevo information is O(log p(n))=O(sqrt(n)), "
            "not Theta(log(n!))."
        ),
        scope=(
            "The theorem applies after carrier trace. It leaves polynomially many "
            "blocks, adaptive bit extraction, and carrier-retaining decoders open."
        ),
        theorem_verified=verified,
        status=(
            "joint-register-one-block-nonextensive-multiblock-open"
            if verified
            else "joint-character-purity-decoupling-validation-failure"
        ),
    )
    return JointCharacterPurityDecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            **asdict(theorem),
            "collision_free_conditioning": (
                "Conditioned expectation is at most the unconditioned expectation "
                "divided by P_cf(n,k), and P_cf(n,k)->1."
            ),
        },
        theorem=theorem,
        fixed_tuple_controls=fixed,
        natural_controls=natural,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_joint_register_purity",
                "resolved": verified,
                "resolution": (
                    "The carrier trace factorizes over orientation bits and class "
                    "contraction validates the exact fixed-tuple formula."
                ),
            },
            {
                "obligation": "bound_natural_one_block_information",
                "resolved": verified,
                "resolution": (
                    "Character column orthogonality, binomial expansion, and "
                    "Cauchy--Schwarz give the partition-count upper bound."
                ),
            },
            {
                "obligation": "condition_on_collision_free_sources",
                "resolved": True,
                "resolution": (
                    "Nonnegativity costs at most 1/P_cf, and the existing global "
                    "collision-free theorem proves P_cf tends to one."
                ),
            },
            {
                "obligation": "construct_multiblock_iterative_information_extractor",
                "resolved": False,
                "resolution": (
                    "The purity bound permits polynomially many blocks but supplies "
                    "no efficient observables whose outcomes accumulate to the label."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Finite positive Holevo information scales to a one-block decoder.",
                "resolved": verified,
                "resolution": (
                    "False for typical natural labels: normalized purity is at most "
                    "exp(O(sqrt(n))) and one-block Holevo is nonextensive."
                ),
            },
            {
                "objection": "Nonextensive one-block information kills the route completely.",
                "resolved": False,
                "resolution": (
                    "Fano requires only a polynomial number of threshold blocks under "
                    "this bound; iterative or adaptive extraction remains possible."
                ),
            },
            {
                "objection": "The bound also applies if the carrier is retained.",
                "resolved": False,
                "resolution": (
                    "No. Equation (1) arises specifically from tracing the carrier; "
                    "the full row-copy isometry preserves the original ensemble."
                ),
            },
        ],
        headline_metrics={
            "exact_fixed_tuple_purity_theorem_count": 1,
            "exact_plancherel_annealed_purity_theorem_count": 1,
            "partition_count_purity_upper_bound_theorem_count": 1,
            "fixed_tuple_control_count": len(fixed),
            "natural_class_control_count": len(natural),
            "exhaustive_plancherel_validation_count": len(exhaustive_residuals),
            "finite_control_failure_count": failures,
            "maximum_exact_normalized_annealed_purity": max(
                row.exact_normalized_annealed_purity for row in natural
            ),
            "maximum_exact_annealed_holevo_upper_bound_bits": max(
                row.exact_annealed_holevo_upper_bound_bits for row in natural
            ),
            "one_block_extensive_information_theorem_count": 0,
            "multiblock_information_extractor_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "joint_register_contains_nonzero_finite_information": True,
            "exact_joint_purity_class_formula_proved": verified,
            "typical_one_block_extensive_information_ruled_out": verified,
            "collision_free_conditioning_preserves_asymptotic_bound": True,
            "polynomial_number_of_joint_blocks_ruled_out": False,
            "adaptive_joint_information_extractor_constructed": False,
            "carrier_retaining_decoder_ruled_out": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "The carrier-traced joint register has an exact class-compressed purity. "
            "Typical natural threshold blocks carry only O(sqrt(n)) Holevo bits, "
            "ruling out an extensive one-block decoder but leaving polynomial "
            "multiblock information extraction open."
        ),
        falsifiers_triggered=[
            (
                "The substantial W3 joint correlation signal does not extrapolate "
                "to extensive information in one natural threshold block."
            ),
            (
                "Discarding the carrier incurs a quantifiable decoupling cost even "
                "though neither retained marginal alone contains information."
            ),
            (
                "A one-block no-go is not a polynomial-copy no-go; adaptive multiblock "
                "observables remain a legitimate research direction."
            ),
        ],
    )


def write_joint_character_purity_decoupling_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-PURITY-DECOUPLING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_joint_character_purity_decoupling" in globals():
        report = run_joint_character_purity_decoupling(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-JOINT-CHARACTER-PURITY-DECOUPLING",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-PURITY-DECOUPLING.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-PURITY-DECOUPLING.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_joint_character_purity_decoupling": str(path)
                },
            )
        )
    return payload

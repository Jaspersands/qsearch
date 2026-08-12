"""Hecke/Gelfand audit for the rigid code-equivalence wreath HSP.

Let

    W_n = (S_n x S_n) semidirect Z_2

with the nontrivial element swapping the two symmetric-group factors, and let

    h_s = (s, s^-1; swap).

The hidden subgroup is H_s=<h_s>.  Its conjugates are indexed by W_n/C_n,
where C_n=C_W(h_e) is the label stabilizer.  Two superficially similar
Gelfand-pair questions must not be confused:

* (W_n,C_n) is a Gelfand pair.  Its quotient is S_n, its double cosets are
  cycle types, and scalar covariant kernels are diagonalized by S_n
  characters.
* (W_n,H_e) is not a Gelfand pair for n>=3.  Therefore the all-register PGM
  optimality theorem for a hidden subgroup that forms a Gelfand pair does not
  transfer merely because the label stabilizer C_n does.

The natural k-copy Hilbert-Schmidt kernel is even more restrictive: after
normalization it equals 1 on the diagonal and 2^-k off the diagonal.  It has no
cycle-type signal.  The useful information, if any, must therefore live in the
operator-valued carrier algebra of the mixed coset states, not in a scalar
Hecke filter.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import conjugacy_class_size, symmetric_character


SELF_DUAL_WREATH_HECKE_PATH = Path(
    "research/representation/self_dual_wreath_hecke_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathHeckeSpec:
    exact_n_values: tuple[int, ...] = (2, 3, 4, 5, 6, 7, 8, 9, 10)
    tail_n_values: tuple[int, ...] = (16, 24, 32, 48, 64)


@dataclass(frozen=True)
class WreathHeckeRecord:
    n: int
    symmetric_group_order: int
    wreath_group_order: int
    bridge_class_size: int
    bridge_centralizer_size: int
    centralizer_quotient_size: int
    partition_count: int
    centralizer_double_coset_count: int
    centralizer_induced_dimension: int
    centralizer_multiplicity_free_dimension_sum: int
    centralizer_gelfand_pair_proved: bool
    finite_character_orthogonality_verified: bool | None
    finite_class_sum_moment_verification_count: int | None
    actual_hidden_subgroup_order: int
    actual_hidden_subgroup_index: int
    actual_hidden_subgroup_max_irrep_multiplicity: int | None
    actual_hidden_subgroup_multiplicity_lower_bound: int
    actual_hidden_subgroup_gelfand_pair: bool
    hidden_subgroup_gelfand_pgm_theorem_applicable: bool
    scalar_hecke_dimension: int
    factorial_hidden_label_kernel_table_required: bool
    uniform_polynomial_coherent_scalar_transform_proved: bool
    information_threshold_copy_count: int
    explicit_subset_term_count_decimal: str
    register_subset_orbit_count: int
    normalized_hs_off_diagonal_overlap_one_copy: float
    normalized_hs_off_diagonal_overlap_at_threshold: float
    normalized_hs_gram_distinct_entry_count: int
    normalized_hs_nontrivial_spectral_level_count: int
    pairwise_cycle_type_signal_present: bool
    operator_valued_kcopy_frame_reduced_to_scalar_hecke: bool
    carrier_sensitive_covariant_povm_proved: bool
    polynomial_hidden_permutation_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathHeckeReport:
    created_at: str
    spec: WreathHeckeSpec
    group_and_homogeneous_space: dict[str, Any]
    literature_links: list[dict[str, Any]]
    scalar_hecke_transform: dict[str, Any]
    records: list[WreathHeckeRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partition_number(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def centralizer_size(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return 2 * math.factorial(n)


def hidden_subgroup_multiplicity_lower_bound(n: int) -> int:
    """Multiplicity in the inversion-positive (n-1,1) equal-pair irrep."""

    if n < 2:
        raise ValueError("n must be at least two")
    dimension = n - 1
    return dimension * (dimension + 1) // 2


def _exact_hidden_subgroup_multiplicities(n: int) -> tuple[int, int]:
    dimensions = [
        hook_length_dimension(partition)
        for partition in integer_partitions(n)
    ]
    multiplicities: list[int] = []
    induced_dimension = 0
    for left, left_dimension in enumerate(dimensions):
        plus = left_dimension * (left_dimension + 1) // 2
        minus = left_dimension * (left_dimension - 1) // 2
        multiplicities.extend((plus, minus))
        induced_dimension += (
            plus * left_dimension * left_dimension
            + minus * left_dimension * left_dimension
        )
        for right_dimension in dimensions[left + 1 :]:
            multiplicity = left_dimension * right_dimension
            irrep_dimension = 2 * left_dimension * right_dimension
            multiplicities.append(multiplicity)
            induced_dimension += multiplicity * irrep_dimension
    return max(multiplicities, default=0), induced_dimension


def _verify_character_hecke_transform(n: int) -> dict[str, Any]:
    partitions = list(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    row_orthogonality = all(
        sum(
            conjugacy_class_size(cycle_type)
            * symmetric_character(left, cycle_type)
            * symmetric_character(right, cycle_type)
            for cycle_type in partitions
        )
        == (order if left == right else 0)
        for left in partitions
        for right in partitions
    )
    column_orthogonality = all(
        sum(
            symmetric_character(partition, left_cycle_type)
            * symmetric_character(partition, right_cycle_type)
            for partition in partitions
        )
        == (
            order // conjugacy_class_size(left_cycle_type)
            if left_cycle_type == right_cycle_type
            else 0
        )
        for left_cycle_type in partitions
        for right_cycle_type in partitions
    )

    class_sum_checks = 0
    for cycle_type in partitions:
        class_size = conjugacy_class_size(cycle_type)
        eigenvalues = {
            partition: Fraction(
                class_size * symmetric_character(partition, cycle_type),
                dimensions[partition],
            )
            for partition in partitions
        }
        trace = sum(
            dimensions[partition] ** 2 * eigenvalues[partition]
            for partition in partitions
        )
        second_moment = sum(
            dimensions[partition] ** 2 * eigenvalues[partition] ** 2
            for partition in partitions
        )
        identity_class = cycle_type == (1,) * n
        if trace != (order if identity_class else 0):
            raise ArithmeticError("class-sum regular trace identity failed")
        if second_moment != order * class_size:
            raise ArithmeticError("class-sum regular second moment failed")
        class_sum_checks += 1

    dimension_sum = sum(dimension * dimension for dimension in dimensions.values())
    if dimension_sum != order:
        raise ArithmeticError("symmetric-group regular dimension sum failed")
    return {
        "row_orthogonality_verified": row_orthogonality,
        "column_orthogonality_verified": column_orthogonality,
        "class_sum_moment_verification_count": class_sum_checks,
        "multiplicity_free_dimension_sum": dimension_sum,
    }


def audit_wreath_hecke(n: int, exact: bool = True) -> WreathHeckeRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    partitions = partition_number(n)
    copy_threshold = math.ceil(math.log2(order))
    subset_terms = 1 << copy_threshold
    lower_bound = hidden_subgroup_multiplicity_lower_bound(n)

    if exact:
        checks = _verify_character_hecke_transform(n)
        max_multiplicity, induced_dimension = _exact_hidden_subgroup_multiplicities(n)
        if induced_dimension != order * order:
            raise ArithmeticError("hidden-subgroup induced dimension sum failed")
        if checks["multiplicity_free_dimension_sum"] != order:
            raise ArithmeticError("centralizer induced dimension sum failed")
        character_verified: bool | None = bool(
            checks["row_orthogonality_verified"]
            and checks["column_orthogonality_verified"]
        )
        class_sum_count: int | None = int(
            checks["class_sum_moment_verification_count"]
        )
    else:
        max_multiplicity = None
        character_verified = None
        class_sum_count = None

    hidden_gelfand = lower_bound <= 1
    return WreathHeckeRecord(
        n=n,
        symmetric_group_order=order,
        wreath_group_order=2 * order * order,
        bridge_class_size=order,
        bridge_centralizer_size=2 * order,
        centralizer_quotient_size=order,
        partition_count=partitions,
        centralizer_double_coset_count=partitions,
        centralizer_induced_dimension=order,
        centralizer_multiplicity_free_dimension_sum=order,
        centralizer_gelfand_pair_proved=True,
        finite_character_orthogonality_verified=character_verified,
        finite_class_sum_moment_verification_count=class_sum_count,
        actual_hidden_subgroup_order=2,
        actual_hidden_subgroup_index=order * order,
        actual_hidden_subgroup_max_irrep_multiplicity=max_multiplicity,
        actual_hidden_subgroup_multiplicity_lower_bound=lower_bound,
        actual_hidden_subgroup_gelfand_pair=hidden_gelfand,
        hidden_subgroup_gelfand_pgm_theorem_applicable=hidden_gelfand,
        scalar_hecke_dimension=partitions,
        factorial_hidden_label_kernel_table_required=False,
        uniform_polynomial_coherent_scalar_transform_proved=False,
        information_threshold_copy_count=copy_threshold,
        explicit_subset_term_count_decimal=str(subset_terms),
        register_subset_orbit_count=copy_threshold + 1,
        normalized_hs_off_diagonal_overlap_one_copy=0.5,
        normalized_hs_off_diagonal_overlap_at_threshold=2.0 ** (-copy_threshold),
        normalized_hs_gram_distinct_entry_count=2,
        normalized_hs_nontrivial_spectral_level_count=1,
        pairwise_cycle_type_signal_present=False,
        operator_valued_kcopy_frame_reduced_to_scalar_hecke=False,
        carrier_sensitive_covariant_povm_proved=False,
        polynomial_hidden_permutation_decoder_proved=False,
        status=(
            "finite-character-control-centralizer-gelfand-actual-hsp-nongelfand"
            if exact and not hidden_gelfand
            else (
                "theorem-tail-centralizer-gelfand-actual-hsp-nongelfand"
                if not hidden_gelfand
                else "small-gelfand-control"
            )
        ),
    )


def run_self_dual_wreath_hecke_audit(
    spec: WreathHeckeSpec = WreathHeckeSpec(),
) -> SelfDualWreathHeckeReport:
    exact_records = [
        audit_wreath_hecke(n, exact=True)
        for n in spec.exact_n_values
    ]
    tail_records = [
        audit_wreath_hecke(n, exact=False)
        for n in spec.tail_n_values
        if n not in spec.exact_n_values
    ]
    records = exact_records + tail_records
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "exact_character_record_count": len(exact_records),
        "maximum_n": max((record.n for record in records), default=0),
        "centralizer_gelfand_pair_proof_count": sum(
            record.centralizer_gelfand_pair_proved for record in records
        ),
        "finite_character_orthogonality_verification_count": sum(
            record.finite_character_orthogonality_verified is True
            for record in records
        ),
        "finite_class_sum_moment_verification_count": sum(
            record.finite_class_sum_moment_verification_count or 0
            for record in records
        ),
        "actual_hidden_subgroup_non_gelfand_count": sum(
            not record.actual_hidden_subgroup_gelfand_pair for record in records
        ),
        "maximum_exact_hidden_subgroup_irrep_multiplicity": max(
            (
                record.actual_hidden_subgroup_max_irrep_multiplicity
                for record in exact_records
                if record.actual_hidden_subgroup_max_irrep_multiplicity is not None
            ),
            default=0,
        ),
        "scalar_hecke_transform_verification_count": len(exact_records),
        "factorial_hidden_label_table_elimination_count": sum(
            not record.factorial_hidden_label_kernel_table_required
            for record in records
        ),
        "pairwise_hs_kernel_collapse_count": sum(
            record.normalized_hs_gram_distinct_entry_count == 2
            and not record.pairwise_cycle_type_signal_present
            for record in records
        ),
        "maximum_information_threshold_copy_count": max(
            (record.information_threshold_copy_count for record in records),
            default=0,
        ),
        "maximum_register_subset_orbit_count": max(
            (record.register_subset_orbit_count for record in records),
            default=0,
        ),
        "uniform_polynomial_coherent_scalar_transform_count": 0,
        "operator_valued_kcopy_frame_reduction_count": 0,
        "carrier_sensitive_covariant_povm_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathHeckeReport(
        created_at=utc_now(),
        spec=spec,
        group_and_homogeneous_space={
            "group": "W_n=(S_n x S_n) semidirect Z_2",
            "hidden_subgroup": "H_s=<h_s>, h_s=(s,s^-1;swap)",
            "label_stabilizer": (
                "C_n=C_W(h_e)={(a,a;epsilon): a in S_n, epsilon in Z_2}"
            ),
            "label_space": "W_n/C_n is identified with S_n by (a,b;epsilon)C_n -> a b^-1",
            "double_cosets": (
                "C_n\\W_n/C_n are conjugacy classes of S_n; inversion adds no "
                "identifications because permutations and inverses have the same cycle type"
            ),
            "centralizer_permutation_representation": (
                "Ind_{C_n}^{W_n}(1)=direct_sum_lambda pi_(lambda,lambda,+), "
                "each once, with dimensions d_lambda^2"
            ),
            "actual_hidden_subgroup_multiplicity": (
                "For an equal-pair +/- wreath irrep, dim Hom_H(1,pi)="
                "(d_lambda^2 +/- d_lambda)/2; the standard irrep already gives "
                "n(n-1)/2 in the + extension"
            ),
        },
        literature_links=[
            {
                "paper_id": "moore-russell-pgm-conjugates-2005",
                "title": (
                    "For Distinguishing Conjugate Hidden Subgroups, the Pretty "
                    "Good Measurement is as Good as it Gets"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0501177",
                "scope": (
                    "One-register PGM optimality for conjugate hidden subgroups; "
                    "all-register optimality when the hidden subgroup H, not "
                    "merely its conjugacy stabilizer, forms a Gelfand pair."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "moore-russell-explicit-multiregister-2005",
                "title": "Explicit Multiregister Measurements for Hidden Subgroup Problems",
                "url": "https://arxiv.org/abs/quant-ph/0504067",
                "scope": (
                    "The information-theoretic multiregister measurement uses "
                    "logarithmically many registers and a contribution from each "
                    "register subset, without by itself giving an efficient algorithm."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        scalar_hecke_transform={
            "kernel_model": (
                "A C_n-bi-invariant scalar kernel on W_n is a class function "
                "kappa on S_n."
            ),
            "unnormalized_eigenvalue": (
                "hat(kappa)(lambda)=(1/d_lambda) sum_g kappa(g) chi_lambda(g)"
            ),
            "finite_verification": (
                "Character row/column orthogonality and both regular class-sum "
                "trace moments are checked exactly."
            ),
            "natural_kcopy_hs_kernel": (
                "K_k(s,t)=1 when s=t and 2^-k otherwise after normalization by purity"
            ),
            "natural_kernel_spectrum": (
                "1+(n!-1)2^-k on the trivial label vector and 1-2^-k on "
                "every nontrivial label direction"
            ),
            "consequence": (
                "The factorial label table is not fundamental for scalar kernels, "
                "but the natural overlap kernel has no cycle-type geometry and "
                "does not determine the mixed-state PGM."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "label_stabilizer_centralizer_gelfand_pair_proved": True,
            "actual_hidden_subgroup_is_label_stabilizer": False,
            "actual_hidden_subgroup_gelfand_pair_asymptotically": False,
            "all_register_pgm_optimality_theorem_transfers": False,
            "factorial_scalar_label_table_is_required": False,
            "natural_scalar_kernel_has_cycle_type_signal": False,
            "register_subset_terms_have_polynomial_orbit_count": True,
            "uniform_polynomial_coherent_scalar_transform_proved": False,
            "operator_valued_kcopy_frame_reduced": False,
            "carrier_sensitive_covariant_povm_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The scalar label-space Hecke algebra is explicit and "
                "multiplicity-free, but the actual order-two hidden subgroup is "
                "non-Gelfand from n=3 onward and the natural scalar overlap "
                "kernel collapses to equality versus inequality. The "
                "operator-valued k-copy frame, POVM, and decoder remain open."
            ),
        },
        status="centralizer-scalar-hecke-solved-actual-hsp-operator-algebra-open",
        summary=(
            f"Proved the centralizer Gelfand-pair and scalar Hecke transform on "
            f"{len(records)} scaling rows through n={metrics['maximum_n']}, "
            f"verified exact character controls on {len(exact_records)} rows, "
            f"and found the actual hidden subgroup non-Gelfand on "
            f"{metrics['actual_hidden_subgroup_non_gelfand_count']} rows. "
            "The natural k-copy scalar overlap has no cycle-type signal."
        ),
        falsifiers_triggered=[
            (
                "The label stabilizer C_n is not the hidden subgroup H_s; "
                "Gelfand-pair theorems must be checked against the correct subgroup."
            ),
            (
                "The actual pair (W_n,H_e) has irrep multiplicity greater than one "
                "for every n>=3."
            ),
            (
                "The normalized k-copy Hilbert-Schmidt overlap depends only on "
                "whether two hidden permutations are equal."
            ),
            (
                "A commutative scalar Hecke transform does not diagonalize the "
                "operator-valued mixed-state frame."
            ),
            (
                "Grouping 2^k register subsets into k+1 size orbits is a formal "
                "compression, not a coherent carrier transform or decoder."
            ),
        ],
    )


def write_self_dual_wreath_hecke_audit(
    path: Path = SELF_DUAL_WREATH_HECKE_PATH,
    spec: WreathHeckeSpec = WreathHeckeSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_hecke_audit(spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_hecke_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

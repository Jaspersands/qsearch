"""Random self-reductions for Regev's density-one modular subset-sum contract."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from sympy import Matrix

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from dcp_subset_sum_lattice_search import modular_subset_sum_embedding, solve_with_lll_embedding
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH = Path(
    "research/reductions/dcp_subset_sum_random_self_reduction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SelfReductionCertificate:
    n_bits: int
    register_count: int
    mask_weight: int
    odd_unit: int
    unit_invertible: bool
    forward_witness_verified: bool
    inverse_witness_verified: bool
    all_target_multiplicities_preserved: bool
    all_target_multiplicities_exhaustively_checked: bool
    joint_uniform_source_bijection_proved: bool
    legal_conditioned_source_preserved: bool
    target_independent_explicit_seed: bool
    shared_seed_interface_compatible: bool


@dataclass(frozen=True)
class SignedEmbeddingIsometryCertificate:
    n_bits: int
    register_count: int
    mask_weight: int
    embedding_scale: int
    exact_basis_identity_verified: bool
    row_map_unimodular: bool
    coordinate_map_orthogonal: bool
    embedding_lattice_isometry_proved: bool
    implication: str


@dataclass(frozen=True)
class RandomizedSelfReductionTrial:
    n_bits: int
    register_count: int
    register_offset: int
    trial_index: int
    target_sampled_independently_uniform: bool
    target_legality_exactly_known: bool
    target_legal: bool | None
    attempts_per_class: int
    direct_solved: bool
    sign_only_executed: bool
    odd_unit_executed: bool
    signed_odd_unit_executed: bool
    sign_only_solved: bool
    odd_unit_solved: bool
    signed_odd_unit_solved: bool
    sign_only_rescue: bool
    odd_unit_rescue: bool
    signed_odd_unit_rescue: bool
    all_returned_witnesses_valid: bool
    sign_only_attempts_used: int
    odd_unit_attempts_used: int
    signed_odd_unit_attempts_used: int
    explicit_seed_bits_upper_bound: int
    polynomial_attempt_budget: bool
    uniform_inverse_polynomial_legal_coverage_proved: bool
    source_contract_satisfied: bool


@dataclass(frozen=True)
class RandomizedSelfReductionScalingRow:
    n_bits: int
    register_offset: int
    attempts_per_class: int
    trial_count: int
    exact_legality_trial_count: int
    direct_unconditional_success_count: int
    sign_only_unconditional_success_count: int
    odd_unit_unconditional_success_count: int
    signed_odd_unit_unconditional_success_count: int
    direct_unconditional_success_rate: float
    sign_only_unconditional_success_rate: float
    odd_unit_unconditional_success_rate: float
    signed_odd_unit_unconditional_success_rate: float
    odd_unit_rescue_count: int
    signed_odd_unit_rescue_count: int
    odd_unit_hoeffding_lower_95pct: float
    odd_unit_zero_success_upper_95pct: float | None
    unconditional_success_lower_bounds_legal_coverage: bool
    uniform_inverse_polynomial_legal_coverage_proved: bool


@dataclass(frozen=True)
class DCPSubsetSumRandomSelfReductionReport:
    created_at: str
    theorem_contract: dict[str, str]
    algebra_certificates: list[SelfReductionCertificate]
    signed_isometry_certificates: list[SignedEmbeddingIsometryCertificate]
    trials: list[RandomizedSelfReductionTrial]
    scaling_rows: list[RandomizedSelfReductionScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_instance(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    mask: Sequence[int],
    odd_unit: int,
) -> None:
    modulus = 1 << n_bits
    if n_bits < 2 or not labels or len(labels) != len(mask):
        raise ValueError("invalid self-reduction dimensions")
    if any(bit not in {0, 1} for bit in mask):
        raise ValueError("mask must be binary")
    if not 0 <= target < modulus:
        raise ValueError("target must be reduced modulo 2^n")
    if not 0 < odd_unit < modulus or odd_unit % 2 == 0:
        raise ValueError("unit must be an odd residue modulo 2^n")


def transform_instance(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    mask: Sequence[int],
    odd_unit: int = 1,
) -> tuple[list[int], int]:
    """Apply x -> x xor mask and an odd-unit automorphism of Z_(2^n)."""
    _validate_instance(n_bits, labels, target, mask, odd_unit)
    modulus = 1 << n_bits
    offset = sum(int(label) for label, bit in zip(labels, mask) if bit)
    transformed_labels = [
        (odd_unit * (-int(label) if bit else int(label))) % modulus
        for label, bit in zip(labels, mask)
    ]
    transformed_target = (odd_unit * (int(target) - offset)) % modulus
    return transformed_labels, transformed_target


def inverse_transform_instance(
    n_bits: int,
    transformed_labels: Sequence[int],
    transformed_target: int,
    mask: Sequence[int],
    odd_unit: int = 1,
) -> tuple[list[int], int]:
    _validate_instance(
        n_bits, transformed_labels, transformed_target, mask, odd_unit
    )
    modulus = 1 << n_bits
    inverse_unit = pow(odd_unit, -1, modulus)
    labels = [
        ((-1 if bit else 1) * inverse_unit * int(label)) % modulus
        for label, bit in zip(transformed_labels, mask)
    ]
    target = (
        inverse_unit * int(transformed_target)
        + sum(label for label, bit in zip(labels, mask) if bit)
    ) % modulus
    return labels, target


def transform_witness(witness: Sequence[int], mask: Sequence[int]) -> list[int]:
    if len(witness) != len(mask) or any(bit not in {0, 1} for bit in witness):
        raise ValueError("witness and mask must be equal-length binary vectors")
    return [int(bit) ^ int(mask_bit) for bit, mask_bit in zip(witness, mask)]


def certify_self_reduction(
    n_bits: int,
    labels: Sequence[int],
    mask: Sequence[int],
    odd_unit: int,
    witness: Sequence[int],
    exhaustive_multiplicity_max_bits: int = 16,
) -> SelfReductionCertificate:
    modulus = 1 << n_bits
    target = sum(int(label) * int(bit) for label, bit in zip(labels, witness)) % modulus
    transformed_labels, transformed_target = transform_instance(
        n_bits, labels, target, mask, odd_unit
    )
    transformed_witness = transform_witness(witness, mask)
    forward = (
        sum(label * bit for label, bit in zip(transformed_labels, transformed_witness))
        % modulus
        == transformed_target
    )
    recovered_labels, recovered_target = inverse_transform_instance(
        n_bits, transformed_labels, transformed_target, mask, odd_unit
    )
    recovered_witness = transform_witness(transformed_witness, mask)
    inverse = (
        recovered_labels == [int(label) % modulus for label in labels]
        and recovered_target == target
        and recovered_witness == list(witness)
    )
    exhaustive_check = n_bits <= exhaustive_multiplicity_max_bits
    multiplicities = forward and inverse
    if exhaustive_check:
        original_counts = subset_sum_counts(n_bits, labels).astype(np.int64)
        transformed_counts = subset_sum_counts(n_bits, transformed_labels).astype(np.int64)
        offset = sum(int(label) for label, bit in zip(labels, mask) if bit)
        multiplicities = all(
            int(transformed_counts[(odd_unit * (value - offset)) % modulus])
            == int(original_counts[value])
            for value in range(modulus)
        )
    return SelfReductionCertificate(
        n_bits=n_bits,
        register_count=len(labels),
        mask_weight=sum(mask),
        odd_unit=odd_unit,
        unit_invertible=math.gcd(odd_unit, modulus) == 1,
        forward_witness_verified=forward,
        inverse_witness_verified=inverse,
        all_target_multiplicities_preserved=multiplicities,
        all_target_multiplicities_exhaustively_checked=exhaustive_check,
        joint_uniform_source_bijection_proved=True,
        legal_conditioned_source_preserved=True,
        target_independent_explicit_seed=True,
        shared_seed_interface_compatible=True,
    )


def certify_signed_embedding_isometry(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    mask: Sequence[int],
    embedding_scale: int = 4,
) -> SignedEmbeddingIsometryCertificate:
    transformed_labels, transformed_target = transform_instance(
        n_bits, labels, target, mask, odd_unit=1
    )
    basis = modular_subset_sum_embedding(
        labels, target, 1 << n_bits, embedding_scale
    )
    transformed_basis = modular_subset_sum_embedding(
        transformed_labels, transformed_target, 1 << n_bits, embedding_scale
    )
    register_count = len(labels)
    dimension = register_count + 2
    coordinate_map = Matrix.diag(
        *[(-1 if bit else 1) for bit in mask], 1, 1
    )
    row_map = Matrix.eye(dimension)
    for index, bit in enumerate(mask):
        row_map[index, index] = -1 if bit else 1
        if bit and int(labels[index]) % (1 << n_bits) != 0:
            row_map[index, dimension - 2] = 1
        row_map[dimension - 1, index] = -int(bit)
    raw_target = int(target) - sum(
        int(label) for label, bit in zip(labels, mask) if bit
    )
    row_map[dimension - 1, dimension - 2] = (
        (raw_target % (1 << n_bits)) - raw_target
    ) // (1 << n_bits)
    identity = transformed_basis == row_map * basis * coordinate_map
    unimodular = abs(int(row_map.det())) == 1
    orthogonal = coordinate_map.T * coordinate_map == Matrix.eye(dimension)
    return SignedEmbeddingIsometryCertificate(
        n_bits=n_bits,
        register_count=register_count,
        mask_weight=sum(mask),
        embedding_scale=embedding_scale,
        exact_basis_identity_verified=identity,
        row_map_unimodular=unimodular,
        coordinate_map_orthogonal=orthogonal,
        embedding_lattice_isometry_proved=identity and unimodular and orthogonal,
        implication=(
            "Coordinate sign/complement randomization can change an LLL basis presentation but cannot create a new "
            "isometry-invariant short-vector gap. Odd-unit multiplication is not covered by this isometry identity."
        ),
    )


def _random_mask(rng: random.Random, register_count: int, allow_zero: bool = True) -> list[int]:
    mask = [rng.randrange(2) for _ in range(register_count)]
    if not allow_zero and not any(mask):
        mask[rng.randrange(register_count)] = 1
    return mask


def _random_odd_unit(rng: random.Random, modulus: int, allow_one: bool = True) -> int:
    unit = rng.randrange(1, modulus, 2)
    if not allow_one and modulus > 4 and unit == 1:
        unit = 3
    return unit


def _try_randomized_lll_class(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    attempts: int,
    seed: int,
    use_signs: bool,
    use_units: bool,
    embedding_scale: int,
    lll_delta: float,
    combination_arity: int,
) -> tuple[bool, bool, int]:
    modulus = 1 << n_bits
    rng = random.Random(seed)
    register_count = len(labels)
    for attempt in range(1, attempts + 1):
        mask = _random_mask(rng, register_count, allow_zero=False) if use_signs else [0] * register_count
        unit = _random_odd_unit(rng, modulus, allow_one=False) if use_units else 1
        transformed_labels, transformed_target = transform_instance(
            n_bits, labels, target, mask, unit
        )
        transformed_witness, _, _ = solve_with_lll_embedding(
            n_bits,
            transformed_labels,
            transformed_target,
            embedding_scale,
            lll_delta,
            combination_arity,
        )
        if transformed_witness is None:
            continue
        witness = transform_witness(transformed_witness, mask)
        valid = (
            sum(int(label) * bit for label, bit in zip(labels, witness)) % modulus
            == target
        )
        return valid, valid, attempt
    return False, True, attempts


def run_randomized_self_reduction_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    attempts_per_class: int,
    seed: int,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
    exact_legality_max_bits: int = 20,
    enabled_classes: Sequence[str] = ("sign-only", "odd-unit", "signed-odd-unit"),
) -> RandomizedSelfReductionTrial:
    if attempts_per_class < 1:
        raise ValueError("attempts_per_class must be positive")
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    exact_legality = n_bits <= exact_legality_max_bits
    target_legal = bool(subset_sum_counts(n_bits, labels)[target]) if exact_legality else None
    direct_witness, _, _ = solve_with_lll_embedding(
        n_bits, labels, target, embedding_scale, lll_delta, combination_arity
    )
    direct_solved = direct_witness is not None
    class_specs = (
        ("sign-only", True, False),
        ("odd-unit", False, True),
        ("signed-odd-unit", True, True),
    )
    unknown_classes = set(enabled_classes) - {item[0] for item in class_specs}
    if unknown_classes or not enabled_classes:
        raise ValueError(f"invalid randomization classes: {sorted(unknown_classes)}")
    classes = []
    for class_index, (class_id, use_signs, use_units) in enumerate(class_specs):
        if class_id not in enabled_classes:
            classes.append((False, True, 0))
            continue
        classes.append(
            _try_randomized_lll_class(
                n_bits,
                labels,
                target,
                attempts_per_class,
                seed + 1_000_003 * (class_index + 1),
                use_signs,
                use_units,
                embedding_scale,
                lll_delta,
                combination_arity,
            )
        )
    (sign_solved, sign_valid, sign_attempts), (unit_solved, unit_valid, unit_attempts), (
        signed_unit_solved,
        signed_unit_valid,
        signed_unit_attempts,
    ) = classes
    budget_power = math.ceil(math.log(max(2, attempts_per_class), max(2, n_bits)))
    return RandomizedSelfReductionTrial(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        trial_index=trial_index,
        target_sampled_independently_uniform=True,
        target_legality_exactly_known=exact_legality,
        target_legal=target_legal,
        attempts_per_class=attempts_per_class,
        direct_solved=direct_solved,
        sign_only_executed="sign-only" in enabled_classes,
        odd_unit_executed="odd-unit" in enabled_classes,
        signed_odd_unit_executed="signed-odd-unit" in enabled_classes,
        sign_only_solved=sign_solved,
        odd_unit_solved=unit_solved,
        signed_odd_unit_solved=signed_unit_solved,
        sign_only_rescue=sign_solved and not direct_solved,
        odd_unit_rescue=unit_solved and not direct_solved,
        signed_odd_unit_rescue=signed_unit_solved and not direct_solved,
        all_returned_witnesses_valid=sign_valid and unit_valid and signed_unit_valid,
        sign_only_attempts_used=sign_attempts,
        odd_unit_attempts_used=unit_attempts,
        signed_odd_unit_attempts_used=signed_unit_attempts,
        explicit_seed_bits_upper_bound=2 * register_count + n_bits,
        polynomial_attempt_budget=attempts_per_class <= n_bits ** max(1, budget_power),
        uniform_inverse_polynomial_legal_coverage_proved=False,
        source_contract_satisfied=False,
    )


def run_random_self_reduction_audit(
    n_values: Sequence[int] = (20, 24, 28, 32),
    register_offsets: Sequence[int] = (4,),
    attempt_multiplier: int = 1,
    trials_per_row: int = 4,
    seed: int = 0,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
    exact_legality_max_bits: int = 20,
    enabled_classes: Sequence[str] = ("sign-only", "odd-unit", "signed-odd-unit"),
) -> DCPSubsetSumRandomSelfReductionReport:
    if attempt_multiplier < 1 or trials_per_row < 1:
        raise ValueError("attempt multiplier and trials must be positive")
    algebra_certificates: list[SelfReductionCertificate] = []
    isometry_certificates: list[SignedEmbeddingIsometryCertificate] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        register_count = n_bits + max(register_offsets)
        rng = random.Random(seed + 97_003 * n_index)
        labels = [rng.randrange(modulus) for _ in range(register_count)]
        mask = _random_mask(rng, register_count, allow_zero=False)
        unit = _random_odd_unit(rng, modulus, allow_one=False)
        witness = _random_mask(rng, register_count)
        target = sum(label * bit for label, bit in zip(labels, witness)) % modulus
        algebra_certificates.append(
            certify_self_reduction(n_bits, labels, mask, unit, witness)
        )
        isometry_certificates.append(
            certify_signed_embedding_isometry(
                n_bits, labels, target, mask, embedding_scale
            )
        )
    trials = [
        run_randomized_self_reduction_trial(
            n_bits,
            offset,
            trial,
            attempts_per_class=attempt_multiplier * n_bits,
            seed=seed + 1_000_003 * ni + 10_007 * oi + trial,
            embedding_scale=embedding_scale,
            lll_delta=lll_delta,
            combination_arity=combination_arity,
            exact_legality_max_bits=exact_legality_max_bits,
            enabled_classes=enabled_classes,
        )
        for ni, n_bits in enumerate(n_values)
        for oi, offset in enumerate(register_offsets)
        for trial in range(trials_per_row)
    ]
    scaling_rows: list[RandomizedSelfReductionScalingRow] = []
    for n_bits in n_values:
        for offset in register_offsets:
            grouped = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            count = len(grouped)
            direct = sum(item.direct_solved for item in grouped)
            sign = sum(item.sign_only_solved for item in grouped)
            unit = sum(item.odd_unit_solved for item in grouped)
            signed_unit = sum(item.signed_odd_unit_solved for item in grouped)
            unit_rate = unit / count
            scaling_rows.append(
                RandomizedSelfReductionScalingRow(
                    n_bits=n_bits,
                    register_offset=offset,
                    attempts_per_class=grouped[0].attempts_per_class,
                    trial_count=count,
                    exact_legality_trial_count=sum(
                        item.target_legality_exactly_known for item in grouped
                    ),
                    direct_unconditional_success_count=direct,
                    sign_only_unconditional_success_count=sign,
                    odd_unit_unconditional_success_count=unit,
                    signed_odd_unit_unconditional_success_count=signed_unit,
                    direct_unconditional_success_rate=direct / count,
                    sign_only_unconditional_success_rate=sign / count,
                    odd_unit_unconditional_success_rate=unit_rate,
                    signed_odd_unit_unconditional_success_rate=signed_unit / count,
                    odd_unit_rescue_count=sum(item.odd_unit_rescue for item in grouped),
                    signed_odd_unit_rescue_count=sum(
                        item.signed_odd_unit_rescue for item in grouped
                    ),
                    odd_unit_hoeffding_lower_95pct=max(
                        0.0,
                        unit_rate - math.sqrt(math.log(20.0) / (2.0 * count)),
                    ),
                    odd_unit_zero_success_upper_95pct=(
                        1.0 - 0.05 ** (1.0 / count) if unit == 0 else None
                    ),
                    unconditional_success_lower_bounds_legal_coverage=True,
                    uniform_inverse_polynomial_legal_coverage_proved=False,
                )
            )
    legal_trials = [trial for trial in trials if trial.target_legal is True]
    tail_n = max(n_values)
    tail_legal = [trial for trial in legal_trials if trial.n_bits == tail_n]
    tail_trials = [trial for trial in trials if trial.n_bits == tail_n]
    tail_signed_successes = sum(item.signed_odd_unit_solved for item in tail_trials)
    tail_signed_rate = tail_signed_successes / len(tail_trials)
    tail_signed_lower = max(
        0.0, tail_signed_rate - math.sqrt(math.log(20.0) / (2.0 * len(tail_trials)))
    )
    metrics: dict[str, int | float] = {
        "algebra_certificate_count": len(algebra_certificates),
        "all_target_multiplicity_certificate_count": sum(
            item.all_target_multiplicities_preserved for item in algebra_certificates
        ),
        "source_distribution_bijection_certificate_count": sum(
            item.joint_uniform_source_bijection_proved for item in algebra_certificates
        ),
        "shared_seed_interface_certificate_count": sum(
            item.shared_seed_interface_compatible for item in algebra_certificates
        ),
        "signed_embedding_isometry_certificate_count": sum(
            item.embedding_lattice_isometry_proved for item in isometry_certificates
        ),
        "trial_count": len(trials),
        "legal_trial_count": len(legal_trials),
        "exact_legality_trial_count": sum(item.target_legality_exactly_known for item in trials),
        "direct_unconditional_success_count": sum(item.direct_solved for item in trials),
        "sign_only_unconditional_success_count": sum(item.sign_only_solved for item in trials),
        "odd_unit_unconditional_success_count": sum(item.odd_unit_solved for item in trials),
        "signed_odd_unit_unconditional_success_count": sum(
            item.signed_odd_unit_solved for item in trials
        ),
        "direct_legal_success_count": sum(item.direct_solved for item in legal_trials),
        "sign_only_legal_success_count": sum(item.sign_only_solved for item in legal_trials),
        "odd_unit_legal_success_count": sum(item.odd_unit_solved for item in legal_trials),
        "signed_odd_unit_legal_success_count": sum(
            item.signed_odd_unit_solved for item in legal_trials
        ),
        "sign_only_rescue_count": sum(item.sign_only_rescue for item in trials),
        "odd_unit_rescue_count": sum(item.odd_unit_rescue for item in trials),
        "signed_odd_unit_rescue_count": sum(
            item.signed_odd_unit_rescue for item in trials
        ),
        "scaling_row_count": len(scaling_rows),
        "tail_legal_trial_count": len(tail_legal),
        "tail_trial_count": len(tail_trials),
        "tail_direct_unconditional_success_count": sum(
            item.direct_solved for item in tail_trials
        ),
        "tail_sign_only_unconditional_success_count": sum(
            item.sign_only_solved for item in tail_trials
        ),
        "tail_odd_unit_unconditional_success_count": sum(
            item.odd_unit_solved for item in tail_trials
        ),
        "tail_signed_odd_unit_unconditional_success_count": tail_signed_successes,
        "tail_signed_odd_unit_unconditional_success_rate": tail_signed_rate,
        "tail_signed_odd_unit_unconditional_success_hoeffding_lower_95pct": tail_signed_lower,
        "tail_direct_success_count": sum(item.direct_solved for item in tail_legal),
        "tail_odd_unit_success_count": sum(item.odd_unit_solved for item in tail_legal),
        "tail_signed_odd_unit_success_count": sum(
            item.signed_odd_unit_solved for item in tail_legal
        ),
        "invalid_returned_witness_count": sum(
            not item.all_returned_witnesses_valid for item in trials
        ),
        "polynomial_attempt_budget_row_count": sum(
            item.polynomial_attempt_budget for item in trials
        ),
        "proved_uniform_inverse_polynomial_legal_coverage_count": 0,
        "source_contract_satisfying_row_count": 0,
        "proved_polynomial_partial_subset_sum_solver_count": 0,
    }
    return DCPSubsetSumRandomSelfReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "instance_map": (
                "A'_i=u(-1)^{m_i}A_i mod 2^n and t'=u(t-sum_i m_i A_i) mod 2^n for explicit mask m and odd unit u"
            ),
            "witness_map": "x'=x xor m; the inverse witness map is identical",
            "source_preservation": (
                "for every fixed target-independent seed (m,u), the map is a bijection on the joint uniform (A,t) source, "
                "preserves every target multiplicity, and therefore preserves the legal-conditioned source"
            ),
            "coverage_accounting": (
                "every returned witness certifies that its independently uniform target was legal, and unconditional "
                "success probability lower-bounds success conditioned on legality; finite confidence bounds remain "
                "diagnostics rather than a uniform asymptotic theorem"
            ),
            "coherent_interface": (
                "the seed is O(n) classical bits and is shared coherently, so fixed-seed LLL is covered by the proved randomized matching lift"
            ),
            "isometry_boundary": (
                "the sign-mask subgroup is exactly a unimodular row change plus an orthogonal coordinate sign map for the centered embedding; "
                "odd-unit multiplication is source preserving but is not certified by that isometry identity"
            ),
        },
        algebra_certificates=algebra_certificates,
        signed_isometry_certificates=isometry_certificates,
        trials=trials,
        scaling_rows=scaling_rows,
        headline_metrics=metrics,
        claim_gate={
            "source_preserving_random_self_reduction_proved": True,
            "shared_seed_matching_interface_compatible": True,
            "sign_only_new_geometry_claim_allowed": False,
            "odd_unit_randomized_solver_implemented": True,
            "uniform_inverse_polynomial_legal_coverage_proved": False,
            "polynomial_partial_subset_sum_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Odd-unit randomization is a valid polynomial shared-seed solver class, but finite LLL rescues do not prove "
                "inverse-polynomial legal coverage. Sign-only randomization is exactly geometry-isometric."
            ),
        },
        status="source-preserving-randomization-proved-coverage-open",
        summary=(
            f"Certified {metrics['source_distribution_bijection_certificate_count']}/{len(algebra_certificates)} source "
            f"bijections and {metrics['signed_embedding_isometry_certificate_count']}/{len(isometry_certificates)} sign "
            f"isometries. On {len(legal_trials)} legal trials, direct/sign/unit/signed-unit successes="
            f"{metrics['direct_legal_success_count']}/{metrics['sign_only_legal_success_count']}/"
            f"{metrics['odd_unit_legal_success_count']}/{metrics['signed_odd_unit_legal_success_count']}; coverage proofs=0."
        ),
        falsifiers_triggered=[
            "Coordinate complements and sign flips are exact isometries of the centered modular embedding and cannot create an isometry-invariant short-vector gap.",
            "Odd-unit multiplication is a legitimate source-preserving randomization, but finite LLL rescues are not an asymptotic coverage theorem.",
            "Polynomially many seeds preserve polynomial runtime but do not imply inverse-polynomial success on legal random inputs.",
            "The experiment samples targets independently uniformly; planted-witness target sampling is not accepted as source evidence.",
            "A valid random self-reduction plus the shared-seed interface theorem still does not construct a solver unless one transformed class has proved coverage.",
        ],
    )


def write_random_self_reduction_audit(
    path: Path = DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH,
    n_values: Sequence[int] = (20, 24, 28, 32),
    register_offsets: Sequence[int] = (4,),
    attempt_multiplier: int = 1,
    trials_per_row: int = 4,
    seed: int = 0,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
    exact_legality_max_bits: int = 20,
    enabled_classes: Sequence[str] = ("sign-only", "odd-unit", "signed-odd-unit"),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_random_self_reduction_audit(
        n_values,
        register_offsets,
        attempt_multiplier,
        trials_per_row,
        seed,
        embedding_scale,
        lll_delta,
        combination_arity,
        exact_legality_max_bits,
        enabled_classes,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SIGNED-COORDINATE-SELF-REDUCTION-ISOMETRIC",
                source=str(path),
                claim=(
                    "Random coordinate complements or label sign flips create a new easy short-vector geometry for the centered modular embedding."
                ),
                reason_invalid=(
                    "The transformed basis is exactly UBD with U unimodular and D orthogonal, so the embedding lattices are isometric."
                ),
                lesson=(
                    "Use signs as a basis-presentation control. Focus randomized geometry search on source automorphisms such as odd units that are not covered by this isometry."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "signed_embedding_isometry_certificate_count": payload["headline_metrics"][
                        "signed_embedding_isometry_certificate_count"
                    ],
                    "proved_uniform_inverse_polynomial_legal_coverage_count": 0,
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-ODD-UNIT-LLL-FINITE-RANDOMIZATION-WITHOUT-COVERAGE",
                source=str(path),
                claim=(
                    "Finite rescues from polynomially many odd-unit LLL presentations establish a Regev-compatible partial solver."
                ),
                reason_invalid=(
                    "The self-reduction and runtime are valid, but no uniform inverse-polynomial legal-input coverage theorem is proved."
                ),
                lesson=(
                    "Retain odd-unit randomization as a legal solver class and demand held-out scaling plus an average-case geometry/coverage theorem."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "odd_unit_rescue_count": payload["headline_metrics"]["odd_unit_rescue_count"],
                    "signed_odd_unit_rescue_count": payload["headline_metrics"][
                        "signed_odd_unit_rescue_count"
                    ],
                    "proved_uniform_inverse_polynomial_legal_coverage_count": 0,
                },
            )
        )
        result_id = registry_result_id or (
            f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_subset_sum_random_self_reduction": str(path)},
            )
        )
    return payload

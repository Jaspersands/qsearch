"""Certificate and scaling gate for exact modular YJM contraction."""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import standard_young_tableaux
from representation_obstruction import conjugate_partition
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_modular_yjm_contraction import (
    characteristic_polynomial_mod,
    characteristic_polynomial_square_free_mod,
    content_penalty_spectrum,
    matrix_power_traces_mod,
    modular_inverse,
    modular_projected_fiber_parallel,
    modular_separator_block_from_fiber,
    modular_yjm_separator_block,
)
from symmetric_character import kronecker_coefficient


CERTIFICATE_PATH = Path(
    "research/certificates/coset_typical_modular_yjm_contraction_certificate.json"
)
N10_PRIME_CERTIFICATE_PATH = Path(
    "research/certificates/coset_typical_modular_yjm_n10_prime1009.json"
)
REPORT_PATH = Path(
    "research/representation/coset_typical_modular_yjm_contraction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-MODULAR-YJM-CONTRACTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PRIME = 1009
DEPENDENCY_PATHS = (
    Path("symmetric_modular_yjm_contraction.py"),
    Path("coset_jucys_murphy_label_transform.py"),
    Path("symmetric_character.py"),
)
CONTROL_SPECS = (
    ((3, 1, 1), (3, 2), 2, (Fraction(1, 30), Fraction(1, 36))),
    ((4, 2), (4, 2), 2, (Fraction(4, 45), Fraction(19, 1350))),
)
N10_SOURCE = (4, 3, 2, 1)
N10_TARGET = (5, 5)
N10_MULTIPLICITY = 6
N10_LADDER_TARGETS = (
    (5, 5),
    (2, 2, 2, 2, 2),
    (8, 2),
    (2, 2, 1, 1, 1, 1, 1, 1),
    (8, 1, 1),
    (3, 1, 1, 1, 1, 1, 1, 1),
    (6, 4),
    (2, 2, 2, 2, 1, 1),
    (7, 3),
    (2, 2, 2, 1, 1, 1, 1),
)
N10_LADDER_PRIMARY_TARGETS = (
    (5, 5),
    (8, 2),
    (8, 1, 1),
    (6, 4),
    (7, 3),
)


@dataclass(frozen=True)
class ModularControlRecord:
    n: int
    prime: int
    source_partition: list[int]
    target_partition: list[int]
    source_dimension: int
    tensor_dimension: int
    target_dimension: int
    multiplicity: int
    distinct_nonzero_penalty_count: int
    maximum_penalty_eigenvalue: int
    projected_trial_count: int
    projected_rank: int
    tableau_fiber_count: int
    separator_block_mod_prime: list[list[int]]
    power_traces_mod_prime: list[int]
    expected_power_traces_mod_prime: list[int]
    characteristic_polynomial_mod_prime: list[int]
    exact_trace_agreement_count: int
    pair_group_states_materialized: bool


@dataclass(frozen=True)
class ModularYJMContractionReport:
    created_at: str
    architecture_contract: dict[str, object]
    records: list[ModularControlRecord]
    n10_prime_certificates: list[dict[str, object]]
    n10_cost_model: dict[str, int | float]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _dependency_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    return {
        str(path): hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in DEPENDENCY_PATHS
    }


def _fraction_mod(value: Fraction, prime: int) -> int:
    return (
        value.numerator * modular_inverse(value.denominator, prime)
    ) % prime


def _control_record(
    source: tuple[int, ...],
    target: tuple[int, ...],
    multiplicity: int,
    expected_traces: tuple[Fraction, ...],
) -> ModularControlRecord:
    block, metrics = modular_yjm_separator_block(
        source,
        target,
        multiplicity,
        prime=PRIME,
    )
    traces = matrix_power_traces_mod(
        block,
        multiplicity,
        prime=PRIME,
    )
    expected = tuple(_fraction_mod(value, PRIME) for value in expected_traces)
    return ModularControlRecord(
        n=metrics.n,
        prime=metrics.prime,
        source_partition=list(source),
        target_partition=list(target),
        source_dimension=metrics.source_dimension,
        tensor_dimension=metrics.tensor_dimension,
        target_dimension=metrics.target_dimension,
        multiplicity=metrics.multiplicity,
        distinct_nonzero_penalty_count=(
            metrics.distinct_nonzero_penalty_count
        ),
        maximum_penalty_eigenvalue=metrics.maximum_penalty_eigenvalue,
        projected_trial_count=metrics.projected_trial_count,
        projected_rank=metrics.projected_rank,
        tableau_fiber_count=metrics.tableau_fiber_count,
        separator_block_mod_prime=block.tolist(),
        power_traces_mod_prime=list(traces),
        expected_power_traces_mod_prime=list(expected),
        characteristic_polynomial_mod_prime=list(
            characteristic_polynomial_mod(block, prime=PRIME)
        ),
        exact_trace_agreement_count=sum(
            int(observed == wanted)
            for observed, wanted in zip(traces, expected)
        ),
        pair_group_states_materialized=False,
    )


def write_modular_yjm_certificate(
    path: Path = CERTIFICATE_PATH,
) -> dict[str, object]:
    started = time.perf_counter()
    records = [
        _control_record(source, target, multiplicity, expected)
        for source, target, multiplicity, expected in CONTROL_SPECS
    ]
    payload = {
        "certificate_contract": {
            "dependency_sha256": _dependency_hashes(),
            "arithmetic": "exact Young rational-seminormal matrices over F_1009",
            "scope": (
                "Exact modular controls and n=10 cost model; no stored n=10 "
                "multiplicity-six residue yet."
            ),
            "elapsed_seconds": time.perf_counter() - started,
        },
        "records": [asdict(record) for record in records],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def _load_certificate(path: Path = CERTIFICATE_PATH) -> dict[str, object]:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    payload = json.loads(resolved.read_text())
    if payload.get("certificate_contract", {}).get(
        "dependency_sha256"
    ) != _dependency_hashes():
        raise ArithmeticError("modular-YJM dependency hash changed")
    return payload


def n10_target_certificate_path(
    target_partition: tuple[int, ...],
) -> Path:
    if target_partition == N10_TARGET:
        return N10_PRIME_CERTIFICATE_PATH
    slug = "-".join(str(value) for value in target_partition)
    return Path(
        "research/certificates/"
        f"coset_typical_modular_yjm_n10_target_{slug}_prime1009.json"
    )


def write_n10_target_prime_certificate(
    target_partition: tuple[int, ...],
    path: Path | None = None,
    *,
    workers: int = 6,
    seed: int = 0,
) -> dict[str, object]:
    """Compute one exact good-reduction certificate on the n=10 ladder."""

    started = time.perf_counter()
    if sum(target_partition) != 10:
        raise ValueError("target must partition n=10")
    multiplicity = kronecker_coefficient(
        N10_SOURCE,
        N10_SOURCE,
        target_partition,
    )
    if multiplicity < 2:
        raise ValueError("target must have nontrivial Kronecker multiplicity")
    spectrum = content_penalty_spectrum(N10_SOURCE, target_partition)
    if PRIME <= spectrum[-1]:
        raise ArithmeticError("certificate prime is not larger than all penalties")
    fiber, pivots, trials, seeds = modular_projected_fiber_parallel(
        N10_SOURCE,
        target_partition,
        multiplicity,
        prime=PRIME,
        seed=seed,
        workers=workers,
    )
    block, visited = modular_separator_block_from_fiber(
        N10_SOURCE,
        target_partition,
        fiber,
        prime=PRIME,
    )
    traces = matrix_power_traces_mod(
        block,
        multiplicity,
        prime=PRIME,
    )
    characteristic = characteristic_polynomial_mod(block, prime=PRIME)
    square_free = characteristic_polynomial_square_free_mod(
        characteristic,
        prime=PRIME,
    )
    source_dimension = len(standard_young_tableaux(N10_SOURCE))
    target_dimension = len(standard_young_tableaux(target_partition))
    good_reduction = {
        "prime_exceeds_maximum_penalty": PRIME > spectrum[-1],
        "prime_coprime_to_axial_denominators": all(
            math.gcd(PRIME, denominator) == 1
            for denominator in range(1, 10)
        ),
        "prime_coprime_to_target_dimension": PRIME % target_dimension != 0,
        "prime_coprime_to_newton_orders": all(
            math.gcd(PRIME, order) == 1
            for order in range(1, multiplicity + 1)
        ),
    }
    payload = {
        "certificate_contract": {
            "dependency_sha256": _dependency_hashes(),
            "arithmetic": "exact Young rational-seminormal contraction over F_1009",
            "scope": (
                "One good-prime square-free reduction proves the rational "
                f"multiplicity-{multiplicity} characteristic polynomial is "
                "square-free; "
                "it does not reconstruct its rational coefficients."
            ),
            "elapsed_seconds": time.perf_counter() - started,
            "workers": workers,
            "trial_seeds": list(seeds),
        },
        "record": {
            "n": 10,
            "prime": PRIME,
            "source_partition": list(N10_SOURCE),
            "target_partition": list(target_partition),
            "source_dimension": source_dimension,
            "tensor_dimension": source_dimension * source_dimension,
            "target_dimension": target_dimension,
            "multiplicity": multiplicity,
            "maximum_penalty_eigenvalue": spectrum[-1],
            "projector_polynomial_degree": len(spectrum) - 1,
            "projected_trial_count": trials,
            "projected_rank": len(fiber),
            "projected_basis_pivots": list(pivots),
            "tableau_fiber_count": visited,
            "separator_block_mod_prime": block.tolist(),
            "power_traces_mod_prime": list(traces),
            "characteristic_polynomial_mod_prime": list(characteristic),
            "characteristic_polynomial_square_free_mod_prime": square_free,
            "good_reduction_checks": good_reduction,
            "rational_characteristic_polynomial_square_free_consequence": (
                square_free and all(good_reduction.values())
            ),
        },
    }
    resolved_path = path or n10_target_certificate_path(target_partition)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def write_n10_prime_certificate(
    path: Path = N10_PRIME_CERTIFICATE_PATH,
    *,
    workers: int = 6,
) -> dict[str, object]:
    return write_n10_target_prime_certificate(
        N10_TARGET,
        path,
        workers=workers,
    )


def _load_n10_target_prime_certificate(
    target_partition: tuple[int, ...],
    path: Path | None = None,
) -> dict[str, object]:
    resolved = path or n10_target_certificate_path(target_partition)
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / resolved
    if not resolved.exists():
        return {}
    payload = json.loads(resolved.read_text())
    if payload.get("certificate_contract", {}).get(
        "dependency_sha256"
    ) != _dependency_hashes():
        raise ArithmeticError("n=10 modular-YJM dependency hash changed")
    record = payload.get("record", {})
    if record.get("prime") != PRIME:
        raise ArithmeticError("n=10 modular-YJM prime changed")
    if tuple(record.get("source_partition", [])) != N10_SOURCE:
        raise ArithmeticError("n=10 modular-YJM source changed")
    if tuple(record.get("target_partition", [])) != target_partition:
        raise ArithmeticError("n=10 modular-YJM target changed")
    multiplicity = kronecker_coefficient(
        N10_SOURCE,
        N10_SOURCE,
        target_partition,
    )
    if record.get("multiplicity") != multiplicity:
        raise ArithmeticError("n=10 modular-YJM multiplicity changed")
    block = np.array(record.get("separator_block_mod_prime", []), dtype=np.int64)
    if block.shape != (multiplicity, multiplicity):
        raise ArithmeticError("n=10 modular-YJM block shape changed")
    characteristic = characteristic_polynomial_mod(block, prime=PRIME)
    if list(characteristic) != record.get(
        "characteristic_polynomial_mod_prime"
    ):
        raise ArithmeticError("n=10 modular characteristic polynomial is inconsistent")
    square_free = characteristic_polynomial_square_free_mod(
        characteristic,
        prime=PRIME,
    )
    if square_free != record.get(
        "characteristic_polynomial_square_free_mod_prime"
    ):
        raise ArithmeticError("n=10 modular square-free result is inconsistent")
    checks = record.get("good_reduction_checks", {})
    expected_checks = {
        "prime_exceeds_maximum_penalty": (
            PRIME > int(record.get("maximum_penalty_eigenvalue", PRIME))
        ),
        "prime_coprime_to_axial_denominators": all(
            math.gcd(PRIME, denominator) == 1
            for denominator in range(1, 10)
        ),
        "prime_coprime_to_target_dimension": (
            PRIME % int(record.get("target_dimension", PRIME)) != 0
        ),
        "prime_coprime_to_newton_orders": all(
            math.gcd(PRIME, order) == 1
            for order in range(1, multiplicity + 1)
        ),
    }
    if checks != expected_checks:
        raise ArithmeticError("n=10 modular good-reduction checks are inconsistent")
    consequence = square_free and all(expected_checks.values())
    if consequence != record.get(
        "rational_characteristic_polynomial_square_free_consequence"
    ):
        raise ArithmeticError("n=10 modular rational consequence is inconsistent")
    return payload


def _load_n10_prime_certificate(
    path: Path = N10_PRIME_CERTIFICATE_PATH,
) -> dict[str, object]:
    return _load_n10_target_prime_certificate(N10_TARGET, path)


def _validated_records(
    payload: dict[str, object],
) -> list[ModularControlRecord]:
    records = [
        ModularControlRecord(**row)
        for row in payload.get("records", [])
    ]
    if len(records) != len(CONTROL_SPECS):
        raise ArithmeticError("modular-YJM control count changed")
    for record, (source, target, multiplicity, expected) in zip(
        records,
        CONTROL_SPECS,
    ):
        if tuple(record.source_partition) != source:
            raise ArithmeticError("modular-YJM source control changed")
        if tuple(record.target_partition) != target:
            raise ArithmeticError("modular-YJM target control changed")
        if record.multiplicity != multiplicity:
            raise ArithmeticError("modular-YJM multiplicity changed")
        expected_mod = [_fraction_mod(value, PRIME) for value in expected]
        if record.expected_power_traces_mod_prime != expected_mod:
            raise ArithmeticError("modular-YJM expected residues changed")
        if record.power_traces_mod_prime != expected_mod:
            raise ArithmeticError("modular-YJM control traces disagree")
        if record.projected_rank != multiplicity:
            raise ArithmeticError("modular YJM projector has wrong rank")
        if record.tableau_fiber_count != record.target_dimension:
            raise ArithmeticError("modular tableau propagation is incomplete")
    return records


def _n10_cost_model() -> dict[str, int | float]:
    source_dimension = len(standard_young_tableaux(N10_SOURCE))
    target_dimension = len(standard_young_tableaux(N10_TARGET))
    tensor_dimension = source_dimension * source_dimension
    spectrum = content_penalty_spectrum(N10_SOURCE, N10_TARGET)
    polynomial_degree = len(spectrum) - 1
    adjacent_diagonal_actions_per_penalty = 2 * (10 - 1) ** 2
    sparse_axis_actions_per_penalty = 2 * adjacent_diagonal_actions_per_penalty
    trial_count = N10_MULTIPLICITY + 3
    pair_group_space = math.factorial(10) ** 2
    return {
        "n": 10,
        "source_dimension": source_dimension,
        "tensor_dimension": tensor_dimension,
        "target_dimension": target_dimension,
        "multiplicity": N10_MULTIPLICITY,
        "distinct_nonzero_penalty_count": polynomial_degree,
        "maximum_penalty_eigenvalue": spectrum[-1],
        "projector_polynomial_degree": polynomial_degree,
        "adjacent_diagonal_actions_per_penalty": (
            adjacent_diagonal_actions_per_penalty
        ),
        "sparse_axis_actions_per_penalty": sparse_axis_actions_per_penalty,
        "projected_trial_count": trial_count,
        "sparse_axis_actions_for_all_trials": (
            trial_count * polynomial_degree * sparse_axis_actions_per_penalty
        ),
        "explicit_pair_group_state_space_size": pair_group_space,
        "pair_group_to_tensor_dimension_reduction_factor": (
            pair_group_space / tensor_dimension
        ),
    }


def build_modular_yjm_contraction_report() -> ModularYJMContractionReport:
    records = _validated_records(_load_certificate())
    n10_certificates = [
        certificate
        for target in N10_LADDER_TARGETS
        if (
            certificate := _load_n10_target_prime_certificate(target)
        )
    ]
    n10_certificate = next(
        (
            certificate
            for certificate in n10_certificates
            if tuple(
                certificate.get("record", {}).get("target_partition", [])
            )
            == N10_TARGET
        ),
        {},
    )
    n10_record = n10_certificate.get("record", {})
    rational_square_free = bool(
        n10_record.get(
            "rational_characteristic_polynomial_square_free_consequence",
            False,
        )
    )
    cost = _n10_cost_model()
    agreement_count = sum(
        record.exact_trace_agreement_count for record in records
    )
    exact_ladder_records = [
        certificate["record"] for certificate in n10_certificates
    ]
    square_free_ladder_records = [
        record
        for record in exact_ladder_records
        if record.get(
            "rational_characteristic_polynomial_square_free_consequence",
            False,
        )
    ]
    square_free_by_target = {
        tuple(record["target_partition"]): record
        for record in square_free_ladder_records
    }
    square_free_target_closure = set(square_free_by_target)
    square_free_target_closure.update(
        conjugate_partition(target) for target in square_free_by_target
    )
    conjugate_validation_pairs = 0
    for target, record in square_free_by_target.items():
        conjugate = conjugate_partition(target)
        if target >= conjugate or conjugate not in square_free_by_target:
            continue
        characteristic = record["characteristic_polynomial_mod_prime"]
        conjugate_characteristic = square_free_by_target[conjugate][
            "characteristic_polynomial_mod_prime"
        ]
        expected_conjugate = [
            coefficient if index % 2 == 0 else (-coefficient) % PRIME
            for index, coefficient in enumerate(characteristic)
        ]
        if conjugate_characteristic != expected_conjugate:
            raise ArithmeticError(
                "direct conjugate certificates violate sign-duality"
            )
        conjugate_validation_pairs += 1
    covered_primary_targets = {
        target
        for target in N10_LADDER_PRIMARY_TARGETS
        if target in square_free_target_closure
    }
    metrics: dict[str, int | float] = {
        "exact_modular_control_count": len(records),
        "exact_modular_power_trace_count": agreement_count,
        "exact_modular_trace_disagreement_count": (
            sum(record.multiplicity for record in records) - agreement_count
        ),
        "maximum_control_projected_rank": max(
            record.projected_rank for record in records
        ),
        "pair_group_states_materialized_count": 0,
        "n10_tensor_dimension": int(cost["tensor_dimension"]),
        "n10_pair_group_state_space_size": int(
            cost["explicit_pair_group_state_space_size"]
        ),
        "n10_pair_group_to_tensor_dimension_reduction_factor": float(
            cost["pair_group_to_tensor_dimension_reduction_factor"]
        ),
        "n10_projector_polynomial_degree": int(
            cost["projector_polynomial_degree"]
        ),
        "n10_sparse_axis_actions_for_all_trials": int(
            cost["sparse_axis_actions_for_all_trials"]
        ),
        "compiled_modular_projector_kernel_count": 0,
        "n10_modular_prime_residue_count": len(exact_ladder_records),
        "n10_modular_power_trace_residue_count": sum(
            len(record.get("power_traces_mod_prime", []))
            for record in exact_ladder_records
        ),
        "n10_direct_exact_square_free_target_count": len(
            square_free_ladder_records
        ),
        "n10_exact_square_free_target_count": len(
            square_free_target_closure
        ),
        "n10_inferred_by_conjugate_sign_duality_count": (
            len(square_free_target_closure)
            - len(square_free_ladder_records)
        ),
        "exact_conjugate_sign_duality_theorem_count": 1,
        "conjugate_sign_duality_validation_pair_count": (
            conjugate_validation_pairs
        ),
        "n10_exact_collision_target_count": sum(
            int(
                not record.get(
                    "characteristic_polynomial_square_free_mod_prime",
                    False,
                )
            )
            for record in exact_ladder_records
        ),
        "n10_maximum_exact_certified_multiplicity": max(
            (
                int(record.get("multiplicity", 0))
                for record in square_free_ladder_records
            ),
            default=0,
        ),
        "n10_nontrivial_multiplicity_target_count": 40,
        "n10_unaudited_target_count": (
            40 - len(square_free_target_closure)
        ),
        "n10_ladder_declared_target_count": len(
            N10_LADDER_PRIMARY_TARGETS
        ),
        "n10_ladder_remaining_declared_target_count": (
            len(N10_LADDER_PRIMARY_TARGETS)
            - len(covered_primary_targets)
        ),
        "exact_n10_multiplicity6_square_free_certificate_count": int(
            rational_square_free
        ),
        "exact_n10_multiplicity6_power_trace_count": 0,
        "exact_n10_multiplicity6_characteristic_polynomial_count": 0,
        "crt_rational_reconstruction_count": 0,
        "polynomial_in_n_state_dimension_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return ModularYJMContractionReport(
        created_at=utc_now(),
        architecture_contract={
            "representation": (
                "Young rational seminormal form removes all square roots and "
                "represents adjacent transpositions exactly over a prime field."
            ),
            "projector": (
                "The integer-valued diagonal content penalty has explicit "
                "spectrum; its finite-field spectral polynomial projects random "
                "vectors exactly onto one target-tableau multiplicity fiber."
            ),
            "restriction": (
                "Rational seminormal Gram weights and exact tableau propagation "
                "contract TT1+TC1 representatives into the multiplicity block."
            ),
            "conjugate_sign_duality": (
                "For self-conjugate source lambda, twisting the first source "
                "factor by the sign intertwiner maps target nu to its conjugate. "
                "Every TT1 and TC1 representative has an odd left transposition, "
                "so H_nu' is similar to -H_nu. Hence square-freeness and gap "
                "magnitudes transfer exactly for every n."
            ),
            "certification_route": (
                "Repeat over good primes, compute characteristic-polynomial "
                "residues, combine by CRT, and rationally reconstruct coefficients."
            ),
            "scaling_boundary": (
                "The state dimension is dim(lambda)^2 rather than (n!)^2, but "
                "remains exponential for typical lambda. The pure-Python n=10 "
                "projector also performs millions of full sparse-axis passes."
            ),
        },
        records=records,
        n10_prime_certificates=exact_ladder_records,
        n10_cost_model=cost,
        headline_metrics=metrics,
        claim_gate={
            "exact_finite_field_controls_reproduced": True,
            "factorial_pair_group_expansion_removed": True,
            "compiled_n10_projector_kernel_available": False,
            "n10_multiplicity6_residue_computed": bool(n10_record),
            "n10_multiplicity6_exactly_certified_square_free": (
                rational_square_free
            ),
            "all_declared_n10_ladder_targets_certified": (
                len(covered_primary_targets)
                == len(N10_LADDER_PRIMARY_TARGETS)
            ),
            "all_n10_nontrivial_targets_certified": (
                len(square_free_target_closure) == 40
            ),
            "conjugate_sign_duality_proved_all_n": True,
            "n10_rational_characteristic_coefficients_reconstructed": False,
            "state_dimension_scales_polynomially": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The modular architecture is exact and removes factorial group "
                "states. Even with a good-reduction square-free certificate, "
                "rational coefficient reconstruction, polynomial state compression, "
                "a coherent transform, and a decoder remain absent."
            ),
        },
        status=(
            "exact-n10-ladder-advancing-by-good-reduction-coefficients-and-scaling-open"
            if square_free_ladder_records
            else "exact-modular-controls-pass-n10-prime-certificate-required"
        ),
        summary=(
            (
                f"{len(square_free_ladder_records)} exact good-prime reduction(s) "
                "prove the corresponding n=10 separator polynomials are "
                "square-free; rational coefficients, full target coverage, "
                "asymptotic compression, and a decoder remain open."
            )
            if square_free_ladder_records
            else (
                "Exact finite-field YJM projection reproduces both rational trace "
                "controls without pair-group expansion and shrinks the n=10 finite "
                "ambient space by over twenty million-fold. A parallel prime "
                "certificate is now the concrete route to the sextic."
            )
        ),
        falsifiers_triggered=[
            "Removing factorial pair-group states does not remove the exponential typical-irrep tensor dimension.",
            (
                "The pure-Python n=10 projector still requires "
                f"{cost['sparse_axis_actions_for_all_trials']} full sparse-axis "
                "passes for nine trials after the exact Jucys-Murphy recurrence."
            ),
            (
                f"Only {len(exact_ladder_records)} of 40 nontrivial n=10 targets "
                "have good-prime certificates; rational coefficient reconstruction "
                "still requires height bounds and CRT."
                if exact_ladder_records
                else "No n=10 modular residue or CRT reconstruction has been produced yet."
            ),
            "Finite exact block certification is not an all-n transform or hidden-involution decoder.",
        ],
    )


def write_modular_yjm_contraction_report(
    output_path: Path = REPORT_PATH,
    *,
    recompute: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    if recompute:
        write_modular_yjm_certificate()
    payload = asdict(build_modular_yjm_contraction_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-PURE-PYTHON-MODULAR-YJM-N10-KERNEL",
                source=str(output_path),
                claim=(
                    "The exact modular YJM projector is ready for an n=10 "
                    "multi-prime run in the current pure-Python kernel."
                ),
                reason_invalid=(
                    "Nine projected trials require "
                    f"{payload['headline_metrics']['n10_sparse_axis_actions_for_all_trials']} "
                    "full sparse-axis passes over 589,824 coordinates before "
                    "CRT repetition."
                ),
                lesson=(
                    "Compile and parallelize the modular penalty/projector kernel, "
                    "stream independent projected vectors, then reconstruct the "
                    "sextic across independently validated good primes."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={
                    "coset_typical_modular_yjm_contraction": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_modular_yjm_contraction_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )

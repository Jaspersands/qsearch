"""Pair-carrier conditioning as a structured approximation to the natural PGM.

The natural multi-copy PGM has a substantial finite information advantage but
its covariance-compressed implementation requires a source-specific inverse on
large multiplicity spaces.  A pair-carrier measurement is polynomially
available and commutes with the global hidden-label action.  This module asks
whether branching on one such label makes the PGM meaningfully simpler while
retaining its discrimination power.

Let ``{C_alpha}`` be the left-pair carrier PVM and ``rho_h`` a source-
conditioned three-copy state.  The branch probability

    p_alpha = Tr(C_alpha rho_h)

is independent of ``h``.  The carrier-conditioned experiment therefore has
the covariant branch ensembles

    rho_(h|alpha) = C_alpha rho_h C_alpha / p_alpha.

The PGM of the classical-quantum output is exactly the direct sum of the
branch PGMs.  In a total-irrep block

    U = direct_sum_nu V_nu tensor M_nu,

write ``C_alpha=direct_sum_nu I tensor c_(nu,alpha)`` and the natural average
as ``I/d_nu tensor D_nu``.  Conditioning replaces the unresolved whitening
operator by

    (c_(nu,alpha) D_nu c_(nu,alpha))^(-1/2)

on the compressed multiplicity range.  It does not make this operator scalar:
the remaining Racah-path dimension contains
``K_(lambda_1,lambda_2)^alpha tensor K_(alpha,lambda_3)^nu``.

Exact natural ``S_5`` controls show a genuine tradeoff.  One pair label keeps
substantial Holevo and PGM information and improves average conditioning, but
discards much of the collective PGM gain and leaves source-specific matrix
whitening.  This is a structured approximation target, not a decoder.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_natural_multicopy_pgm_benchmark import (
    _channel_statistics,
    _source_data,
    _tensor_states,
    audit_natural_multicopy_pgm,
    pretty_good_measurement_channel,
)
from research_registry import utc_now
from self_dual_wreath_plancherel_carrier_contextuality import (
    _triple_isotypic_projectors,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_carrier_conditioned_pgm_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CARRIER-CONDITIONED-PGM-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CarrierConditionedPgmSourceControl:
    pair_partitions: tuple[Partition, Partition]
    third_partition: Partition
    natural_source_probability: float
    hidden_involution_count: int
    physical_dimension: int
    active_pair_carrier_count: int
    maximum_pair_carrier_branch_rank: int
    full_global_pgm_mutual_information_bits: float
    carrier_conditioned_pgm_mutual_information_bits: float
    full_global_pgm_bayes_success_probability: float
    carrier_conditioned_pgm_bayes_success_probability: float
    full_holevo_information_bits: float
    carrier_dephased_holevo_information_bits: float
    holevo_retention_fraction: float
    pgm_information_retention_fraction: float
    pgm_bayes_retention_fraction: float
    full_average_state_condition_number: float
    maximum_carrier_branch_condition_number: float
    carrier_dephasing_frobenius_fraction: float
    maximum_carrier_average_commutator_fraction: float
    maximum_hidden_branch_probability_residual: float
    conditioned_channel_normalization_residual: float
    maximum_branch_pgm_completeness_residual: float
    exact_branch_pgm_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierConditionedPgmAggregate:
    n: int
    transposition_count: int
    copy_count: int
    pair_source_type_count: int
    total_natural_source_probability: float
    full_global_pgm_mutual_information_bits: float
    carrier_conditioned_pgm_mutual_information_bits: float
    product_one_copy_pgm_mutual_information_bits: float
    separate_young_mutual_information_bits: float
    full_global_pgm_bayes_success_probability: float
    carrier_conditioned_pgm_bayes_success_probability: float
    product_one_copy_pgm_bayes_success_probability: float
    separate_young_bayes_success_probability: float
    full_holevo_information_bits: float
    carrier_dephased_holevo_information_bits: float
    holevo_retention_fraction: float
    pgm_information_retention_fraction: float
    pgm_bayes_retention_fraction: float
    retained_collective_information_gain_fraction_over_product_pgm: float
    retained_collective_bayes_gain_fraction_over_product_pgm: float
    average_full_condition_number: float
    average_maximum_carrier_branch_condition_number: float
    average_condition_number_reduction_factor: float
    average_carrier_dephasing_frobenius_fraction: float
    average_maximum_carrier_commutator_fraction: float
    average_active_pair_carrier_count: float
    natural_mass_with_at_least_80_percent_pgm_information_retention: float
    maximum_hidden_branch_probability_residual: float
    maximum_channel_normalization_residual: float
    maximum_branch_pgm_completeness_residual: float
    all_exact_controls_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierConditionedPgmTheorem:
    hidden_independent_branch_law: str
    direct_sum_pgm_factorization: str
    schur_multiplicity_compression: str
    residual_racah_path_space: str
    holevo_data_processing: str
    finite_tradeoff: str
    scope_limit: str
    hidden_independent_branch_law_proved: bool
    exact_branch_pgm_factorization_proved: bool
    multiplicity_whitening_compressed: bool
    multiplicity_whitening_eliminated: bool
    finite_collective_gain_retained: bool
    all_n_information_retention_proved: bool
    polynomial_branch_pgm_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierConditionedPgmBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    aggregate: CarrierConditionedPgmAggregate
    highest_weight_source_controls: list[CarrierConditionedPgmSourceControl]
    worst_information_retention_controls: list[CarrierConditionedPgmSourceControl]
    theorem: CarrierConditionedPgmTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _von_neumann_entropy_bits(state: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh((state + state.conj().T) / 2)
    positive = eigenvalues[eigenvalues > 1e-14]
    return -float(np.sum(positive * np.log2(positive)))


def _holevo_information(states: tuple[np.ndarray, ...]) -> float:
    average = sum(states) / len(states)
    return _von_neumann_entropy_bits(average) - sum(
        _von_neumann_entropy_bits(state) for state in states
    ) / len(states)


def _support_condition_number(
    state: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> float:
    eigenvalues = np.linalg.eigvalsh((state + state.conj().T) / 2)
    positive = eigenvalues[eigenvalues > tolerance]
    if not len(positive):
        return 1.0
    return float(positive[-1] / positive[0])


@lru_cache(maxsize=None)
def _global_source_pgm_metrics(
    n: int,
    transposition_count: int,
    source_indices: tuple[int, int, int],
) -> tuple[float, float]:
    _, _, state_families = _source_data(n, transposition_count)
    indices = tuple(sorted(source_indices))
    states = _tensor_states(tuple(state_families[index] for index in indices))
    channel, _, _ = pretty_good_measurement_channel(states)
    information, bayes, _ = _channel_statistics(channel)
    return information, bayes


def audit_carrier_conditioned_source(
    n: int,
    transposition_count: int,
    pair_indices: tuple[int, int],
    third_index: int,
    *,
    natural_source_probability: float,
    tolerance: float = 1e-10,
) -> CarrierConditionedPgmSourceControl:
    partitions, _, state_families = _source_data(n, transposition_count)
    first, second = pair_indices
    sources = (
        partitions[first],
        partitions[second],
        partitions[third_index],
    )
    states = _tensor_states(
        (
            state_families[first],
            state_families[second],
            state_families[third_index],
        )
    )
    hidden_count = len(states)
    average = sum(states) / hidden_count
    projectors = _triple_isotypic_projectors(sources, "left")
    dephased_states = tuple(
        sum(
            (projector @ state @ projector for projector in projectors),
            np.zeros_like(state, dtype=complex),
        )
        for state in states
    )
    dephased_average = sum(dephased_states) / hidden_count
    branch_channels = []
    branch_conditions = []
    active_ranks = []
    maximum_probability_residual = 0.0
    maximum_completeness = 0.0
    for projector in projectors:
        branch_states = tuple(projector @ state @ projector for state in states)
        probabilities = np.asarray(
            [float(np.trace(state).real) for state in branch_states]
        )
        branch_probability = float(probabilities.mean())
        maximum_probability_residual = max(
            maximum_probability_residual,
            float(np.max(np.abs(probabilities - branch_probability))),
        )
        if branch_probability <= tolerance:
            continue
        normalized_states = tuple(
            state / branch_probability for state in branch_states
        )
        branch_channel, _, completeness = pretty_good_measurement_channel(
            normalized_states
        )
        branch_channels.append(branch_probability * branch_channel)
        branch_average = sum(normalized_states) / hidden_count
        branch_conditions.append(_support_condition_number(branch_average))
        active_ranks.append(int(round(float(np.trace(projector).real))))
        maximum_completeness = max(maximum_completeness, completeness)
    if not branch_channels:
        raise ArithmeticError("carrier PVM has no active branch")
    conditioned_channel = np.hstack(branch_channels)
    conditioned_information, conditioned_bayes, channel_residual = (
        _channel_statistics(conditioned_channel)
    )
    global_information, global_bayes = _global_source_pgm_metrics(
        n,
        transposition_count,
        tuple(sorted((first, second, third_index))),
    )
    full_holevo = _holevo_information(states)
    dephased_holevo = _holevo_information(dephased_states)
    norm_average = max(float(np.linalg.norm(average, ord="fro")), tolerance)
    dephasing_fraction = float(
        np.linalg.norm(average - dephased_average, ord="fro") / norm_average
    )
    maximum_commutator = max(
        float(
            np.linalg.norm(projector @ average - average @ projector, ord="fro")
            / norm_average
        )
        for projector in projectors
    )
    verified = (
        maximum_probability_residual <= 1e-9
        and channel_residual <= 1e-9
        and maximum_completeness <= 1e-8
        and dephased_holevo <= full_holevo + 1e-9
    )
    return CarrierConditionedPgmSourceControl(
        pair_partitions=(partitions[first], partitions[second]),
        third_partition=partitions[third_index],
        natural_source_probability=natural_source_probability,
        hidden_involution_count=hidden_count,
        physical_dimension=states[0].shape[0],
        active_pair_carrier_count=len(branch_channels),
        maximum_pair_carrier_branch_rank=max(active_ranks),
        full_global_pgm_mutual_information_bits=global_information,
        carrier_conditioned_pgm_mutual_information_bits=conditioned_information,
        full_global_pgm_bayes_success_probability=global_bayes,
        carrier_conditioned_pgm_bayes_success_probability=conditioned_bayes,
        full_holevo_information_bits=full_holevo,
        carrier_dephased_holevo_information_bits=dephased_holevo,
        holevo_retention_fraction=(
            dephased_holevo / full_holevo if full_holevo > tolerance else 1.0
        ),
        pgm_information_retention_fraction=(
            conditioned_information / global_information
            if global_information > tolerance
            else 1.0
        ),
        pgm_bayes_retention_fraction=(
            conditioned_bayes / global_bayes if global_bayes > tolerance else 1.0
        ),
        full_average_state_condition_number=_support_condition_number(average),
        maximum_carrier_branch_condition_number=max(branch_conditions),
        carrier_dephasing_frobenius_fraction=dephasing_fraction,
        maximum_carrier_average_commutator_fraction=maximum_commutator,
        maximum_hidden_branch_probability_residual=maximum_probability_residual,
        conditioned_channel_normalization_residual=channel_residual,
        maximum_branch_pgm_completeness_residual=maximum_completeness,
        exact_branch_pgm_factorization_verified=verified,
        status=(
            "exact-carrier-conditioned-pgm-source-control"
            if verified
            else "carrier-conditioned-pgm-source-control-failure"
        ),
    )


@lru_cache(maxsize=None)
def audit_natural_carrier_conditioned_pgm(
    n: int = 5,
    transposition_count: int = 2,
) -> tuple[CarrierConditionedPgmAggregate, tuple[CarrierConditionedPgmSourceControl, ...]]:
    partitions, source_probabilities, _ = _source_data(n, transposition_count)
    controls = []
    for first, second in itertools.combinations_with_replacement(
        range(len(partitions)),
        2,
    ):
        pair_multiplicity = 1 if first == second else 2
        for third in range(len(partitions)):
            weight = (
                pair_multiplicity
                * source_probabilities[first]
                * source_probabilities[second]
                * source_probabilities[third]
            )
            controls.append(
                audit_carrier_conditioned_source(
                    n,
                    transposition_count,
                    (first, second),
                    third,
                    natural_source_probability=weight,
                )
            )
    total_mass = sum(control.natural_source_probability for control in controls)

    def average(field: str) -> float:
        return sum(
            control.natural_source_probability * float(getattr(control, field))
            for control in controls
        )

    benchmark = audit_natural_multicopy_pgm(n, transposition_count, 3)
    global_information = average("full_global_pgm_mutual_information_bits")
    conditioned_information = average(
        "carrier_conditioned_pgm_mutual_information_bits"
    )
    global_bayes = average("full_global_pgm_bayes_success_probability")
    conditioned_bayes = average(
        "carrier_conditioned_pgm_bayes_success_probability"
    )
    full_holevo = average("full_holevo_information_bits")
    dephased_holevo = average("carrier_dephased_holevo_information_bits")
    full_condition = average("full_average_state_condition_number")
    branch_condition = average("maximum_carrier_branch_condition_number")
    product_information = benchmark.product_one_copy_pgm_mutual_information_bits
    product_bayes = benchmark.product_one_copy_pgm_bayes_success_probability
    collective_information_gain = global_information - product_information
    collective_bayes_gain = global_bayes - product_bayes
    all_verified = (
        abs(total_mass - 1.0) <= 1e-9
        and all(control.exact_branch_pgm_factorization_verified for control in controls)
    )
    aggregate = CarrierConditionedPgmAggregate(
        n=n,
        transposition_count=transposition_count,
        copy_count=3,
        pair_source_type_count=len(controls),
        total_natural_source_probability=total_mass,
        full_global_pgm_mutual_information_bits=global_information,
        carrier_conditioned_pgm_mutual_information_bits=conditioned_information,
        product_one_copy_pgm_mutual_information_bits=product_information,
        separate_young_mutual_information_bits=(
            benchmark.separate_young_basis_mutual_information_bits
        ),
        full_global_pgm_bayes_success_probability=global_bayes,
        carrier_conditioned_pgm_bayes_success_probability=conditioned_bayes,
        product_one_copy_pgm_bayes_success_probability=product_bayes,
        separate_young_bayes_success_probability=(
            benchmark.separate_young_basis_bayes_success_probability
        ),
        full_holevo_information_bits=full_holevo,
        carrier_dephased_holevo_information_bits=dephased_holevo,
        holevo_retention_fraction=dephased_holevo / full_holevo,
        pgm_information_retention_fraction=conditioned_information / global_information,
        pgm_bayes_retention_fraction=conditioned_bayes / global_bayes,
        retained_collective_information_gain_fraction_over_product_pgm=(
            (conditioned_information - product_information)
            / collective_information_gain
        ),
        retained_collective_bayes_gain_fraction_over_product_pgm=(
            (conditioned_bayes - product_bayes) / collective_bayes_gain
        ),
        average_full_condition_number=full_condition,
        average_maximum_carrier_branch_condition_number=branch_condition,
        average_condition_number_reduction_factor=full_condition / branch_condition,
        average_carrier_dephasing_frobenius_fraction=average(
            "carrier_dephasing_frobenius_fraction"
        ),
        average_maximum_carrier_commutator_fraction=average(
            "maximum_carrier_average_commutator_fraction"
        ),
        average_active_pair_carrier_count=average("active_pair_carrier_count"),
        natural_mass_with_at_least_80_percent_pgm_information_retention=sum(
            control.natural_source_probability
            for control in controls
            if control.pgm_information_retention_fraction >= 0.8 - 1e-12
        ),
        maximum_hidden_branch_probability_residual=max(
            control.maximum_hidden_branch_probability_residual
            for control in controls
        ),
        maximum_channel_normalization_residual=max(
            control.conditioned_channel_normalization_residual
            for control in controls
        ),
        maximum_branch_pgm_completeness_residual=max(
            control.maximum_branch_pgm_completeness_residual
            for control in controls
        ),
        all_exact_controls_verified=all_verified,
        status=(
            "carrier-conditioning-retains-signal-compresses-not-eliminates-whitening"
            if all_verified
            else "carrier-conditioned-pgm-aggregate-control-failure"
        ),
    )
    return aggregate, tuple(controls)


def carrier_conditioned_pgm_theorem(
    aggregate: CarrierConditionedPgmAggregate,
) -> CarrierConditionedPgmTheorem:
    retained_gain = (
        aggregate.carrier_conditioned_pgm_mutual_information_bits
        > aggregate.product_one_copy_pgm_mutual_information_bits + 1e-10
        and aggregate.carrier_conditioned_pgm_bayes_success_probability
        > aggregate.product_one_copy_pgm_bayes_success_probability + 1e-10
    )
    return CarrierConditionedPgmTheorem(
        hidden_independent_branch_law=(
            "Because every C_alpha commutes with the global action, "
            "Tr(C_alpha rho_h) is constant on the hidden conjugacy class."
        ),
        direct_sum_pgm_factorization=(
            "For the classical carrier flag, the dephased ensemble average is "
            "block diagonal and its PGM is exactly the direct sum of the "
            "normalized branch PGMs."
        ),
        schur_multiplicity_compression=(
            "If B_nu=I/d_nu tensor D_nu and C_alpha=I tensor c_(nu,alpha), "
            "branch whitening is (c D_nu c)^(-1/2) on ran(c)."
        ),
        residual_racah_path_space=(
            "ran(c_(nu,alpha)) contains K_(lambda_1,lambda_2)^alpha tensor "
            "K_(alpha,lambda_3)^nu; one pair label need not make the "
            "multiplicity block one-dimensional or basis-accessible."
        ),
        holevo_data_processing=(
            "Carrier dephasing is a hidden-independent CPTP map, hence its "
            "Holevo information cannot exceed that of the original source branch."
        ),
        finite_tradeoff=(
            "The exact natural S_5 control retains substantial Holevo and PGM "
            "information and improves average conditioning, while losing most "
            "of the global PGM collective gain."
        ),
        scope_limit=(
            "No all-n retention theorem, coherent basis for c D_nu c, tightly "
            "normalized block encoding, branch polar circuit, outcome decoder, "
            "or classical separation is supplied."
        ),
        hidden_independent_branch_law_proved=True,
        exact_branch_pgm_factorization_proved=True,
        multiplicity_whitening_compressed=True,
        multiplicity_whitening_eliminated=False,
        finite_collective_gain_retained=retained_gain,
        all_n_information_retention_proved=False,
        polynomial_branch_pgm_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=aggregate.all_exact_controls_verified and retained_gain,
        status="pair-carrier-compresses-pgm-row-whitening-remains",
    )


def run_carrier_conditioned_pgm_boundary() -> CarrierConditionedPgmBoundaryReport:
    aggregate, controls = audit_natural_carrier_conditioned_pgm()
    theorem = carrier_conditioned_pgm_theorem(aggregate)
    highest_weight = sorted(
        controls,
        key=lambda control: control.natural_source_probability,
        reverse=True,
    )[:12]
    worst_retention = sorted(
        controls,
        key=lambda control: control.pgm_information_retention_fraction,
    )[:12]
    verified = theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "hidden_independent_carrier_branch_theorem_count": int(verified),
        "exact_carrier_branch_pgm_factorization_theorem_count": int(verified),
        "finite_collective_gain_retained_control_count": int(
            theorem.finite_collective_gain_retained
        ),
        "pair_source_type_count": aggregate.pair_source_type_count,
        "natural_source_mass_control_count": int(
            abs(aggregate.total_natural_source_probability - 1.0) <= 1e-9
        ),
        "carrier_conditioned_pgm_information_bits": (
            aggregate.carrier_conditioned_pgm_mutual_information_bits
        ),
        "carrier_conditioned_pgm_bayes_success": (
            aggregate.carrier_conditioned_pgm_bayes_success_probability
        ),
        "carrier_dephased_holevo_retention_fraction": (
            aggregate.holevo_retention_fraction
        ),
        "carrier_conditioned_pgm_information_retention_fraction": (
            aggregate.pgm_information_retention_fraction
        ),
        "retained_collective_information_gain_fraction": (
            aggregate.retained_collective_information_gain_fraction_over_product_pgm
        ),
        "average_condition_number_reduction_factor": (
            aggregate.average_condition_number_reduction_factor
        ),
        "multiplicity_whitening_elimination_theorem_count": 0,
        "polynomial_branch_pgm_compiler_count": 0,
        "hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CarrierConditionedPgmBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "input": "three natural same-hidden mixed S_5 coset states",
            "public_conditioning": (
                "one exact left-pair carrier label measured before discrimination"
            ),
            "measurement": (
                "exact source-specific PGM inside each carrier branch"
            ),
            "comparison": (
                "unconditioned global PGM, product one-copy PGM, separate Young "
                "measurement, Holevo information, and support condition number"
            ),
            "structural_target": (
                "compressed multiplicity inverse (c D_nu c)^(-1/2)"
            ),
        },
        aggregate=aggregate,
        highest_weight_source_controls=highest_weight,
        worst_information_retention_controls=worst_retention,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "factor_pgm_over_hidden_independent_carrier_flag",
                "resolved": verified,
                "resolution": (
                    "The flag is a direct-sum classical register and each branch "
                    "has hidden-independent prior weight."
                ),
            },
            {
                "obligation": "retain_nontrivial_collective_information",
                "resolved": theorem.finite_collective_gain_retained,
                "resolution": (
                    "The exact natural S_5 branch PGM beats the product one-copy "
                    "PGM in both mutual information and Bayes success."
                ),
            },
            {
                "obligation": "prove_all_n_constant_information_retention",
                "resolved": False,
                "resolution": (
                    "Only finite S_5 natural-source controls are available."
                ),
            },
            {
                "obligation": "eliminate_source_specific_multiplicity_whitening",
                "resolved": False,
                "resolution": (
                    "Conditioning changes D_nu to c D_nu c but does not make the "
                    "Racah path space scalar or expose its eigenbasis."
                ),
            },
            {
                "obligation": "compile_branch_pgm_and_decode_outcome",
                "resolved": False,
                "resolution": (
                    "The exact dense branch PGMs are evaluation controls, not "
                    "uniform circuits or polynomial hidden-label decoders."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Carrier conditioning creates information.",
                "survives": False,
                "response": (
                    "It is a hidden-independent CPTP instrument; Holevo data "
                    "processing proves it can only retain or discard information."
                ),
            },
            {
                "challenge": "One carrier label diagonalizes the PGM average.",
                "survives": False,
                "response": (
                    "The branch operator c D_nu c remains matrix-valued on the "
                    "two-stage Kronecker/Racah path multiplicity."
                ),
            },
            {
                "challenge": "Improved average condition number compiles the inverse.",
                "survives": False,
                "response": (
                    "A spectral condition number does not provide coherent SELECT, "
                    "a multiplicity basis, or normalization-controlled block access."
                ),
            },
            {
                "challenge": "The retained finite gain is negligible.",
                "survives": False,
                "response": (
                    "It remains above product PGM baselines in both information "
                    "and Bayes success, so it is a legitimate architecture target."
                ),
            },
            {
                "challenge": "Finite branch PGMs are an end-to-end algorithm.",
                "survives": False,
                "response": (
                    "They use dense eigendecomposition and direct hidden-labelled "
                    "effects; scalability and outcome decoding remain open."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "carrier_branch_probability_hidden_independent": verified,
            "carrier_conditioned_pgm_direct_sum_factorization_proved": verified,
            "finite_collective_information_gain_retained": (
                theorem.finite_collective_gain_retained
            ),
            "carrier_conditioning_improves_average_support_conditioning": (
                aggregate.average_condition_number_reduction_factor > 1.0
            ),
            "carrier_conditioning_eliminates_multiplicity_whitening": False,
            "all_n_constant_information_retention_proved": False,
            "polynomial_carrier_branch_pgm_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One carrier label gives a meaningful information/conditioning "
                "tradeoff but leaves a source-specific matrix inverse on a Racah "
                "multiplicity range."
            ),
        },
        status=(
            "carrier-conditioned-pgm-retains-gain-row-whitening-open"
            if verified
            else "carrier-conditioned-pgm-boundary-control-failure"
        ),
        summary=(
            "Factored the natural PGM over one hidden-independent pair-carrier "
            "flag. The exact S_5 control retains substantial Holevo information "
            "and finite collective gain while improving average conditioning, "
            "but the compressed multiplicity-row inverse remains unresolved."
        ),
        falsifiers_triggered=[
            "Carrier conditioning cannot create hidden information; its benefit can only be architectural.",
            "One pair-carrier label does not scalarize the source-specific PGM multiplicity inverse.",
            "The exact S_5 branch PGM retains only part of the global PGM collective gain.",
            "Improved finite conditioning does not imply coherent block access or a polar circuit.",
            "The surviving branch signal is real but has no all-n retention theorem or polynomial decoder.",
        ],
    )


def write_carrier_conditioned_pgm_boundary_report(
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
    payload = asdict(run_carrier_conditioned_pgm_boundary())
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
                title="Carrier-conditioned natural PGM boundary",
                status="completed-finite-gain-retained-row-whitening-open",
                hypothesis=(
                    "One efficiently measurable pair-carrier label may compress "
                    "the natural PGM enough to expose a structured implementation "
                    "while retaining collective hidden-involution information."
                ),
                protocol=(
                    "Factor the PGM over the hidden-independent carrier flag, "
                    "audit all exact natural S_5 pair-source types, and compare "
                    "information, Bayes success, Holevo loss, and conditioning."
                ),
                positive_signal=(
                    "An all-n carrier hierarchy retaining constant collective "
                    "gain whose compressed multiplicity inverses have a uniform "
                    "polynomial coherent implementation and decoder."
                ),
                falsifiers=[
                    "carrier conditioning is claimed to create information",
                    "one pair label is claimed to scalarize multiplicity whitening",
                    "finite condition numbers are treated as block-encoding circuits",
                    "dense branch PGMs are called an efficient decoder",
                ],
                metrics=[
                    "exact_carrier_branch_pgm_factorization_theorem_count",
                    "carrier_dephased_holevo_retention_fraction",
                    "carrier_conditioned_pgm_information_retention_fraction",
                    "retained_collective_information_gain_fraction",
                    "average_condition_number_reduction_factor",
                    "polynomial_branch_pgm_compiler_count",
                ],
                dependencies=[
                    "self_dual_wreath_covariant_pgm_factorization.py",
                    "self_dual_wreath_plancherel_carrier_racah_access_boundary.py",
                    "coset_natural_multicopy_pgm_benchmark.py",
                ],
                next_actions=[
                    "derive an all-n information-retention bound for a carrier hierarchy",
                    "classify c_(nu,alpha) D_nu c_(nu,alpha) using source-specific Racah paths",
                    "search for a recursive branch polar that avoids a dense multiplicity inverse",
                    "compare every branch architecture with tensor-network and arbitrary separable baselines",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-CARRIER-CONDITIONED-PGM-"
            "BOUNDARY-LATEST"
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
                    "self_dual_wreath_carrier_conditioned_pgm_boundary": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="ONE-CARRIER-LABEL-NOT-PGM-MULTIPLICITY-SCALARIZATION",
                source=registry_experiment_id,
                claim=(
                    "Resolving one pair-carrier label turns every natural PGM "
                    "Fourier block into a scalar whitening problem."
                ),
                reason_invalid=(
                    "The branch inverse remains (c D_nu c)^(-1/2) on a Racah "
                    "path space containing two Kronecker multiplicity factors."
                ),
                lesson=(
                    "Track the residual source-specific path multiplicity after "
                    "every proposed carrier hierarchy."
                ),
                applies_to=[
                    registry_candidate_id,
                    "carrier-conditioned PGM",
                    "multiplicity whitening",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-CARRIER-BRANCH-CONDITIONING-NOT-PGM-CIRCUIT",
                source=registry_experiment_id,
                claim=(
                    "A reduced finite support condition number supplies a "
                    "polynomial coherent implementation of the branch PGM."
                ),
                reason_invalid=(
                    "Conditioning improves the natural average but provides no "
                    "multiplicity basis, tightly normalized block encoding, "
                    "inverse implementation, or outcome decoder."
                ),
                lesson=(
                    "Require a typed access model and explicit polar compiler, "
                    "not only favorable finite spectra."
                ),
                applies_to=[
                    registry_candidate_id,
                    "PGM condition number",
                    "carrier hierarchy",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_carrier_conditioned_pgm_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

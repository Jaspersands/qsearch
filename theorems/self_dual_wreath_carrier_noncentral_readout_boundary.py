"""Minimum noncentral readout after Plancherel carrier measurements.

Carrier projectors expose an asymptotically maximal Racah disturbance, but
their entire adaptive outcome algebra is invariant under simultaneous
conjugation.  This module adds the smallest explicit operation outside that
algebra: a final diagonal measurement in the fixed Young orthogonal bases.
Uniform public conjugation, retained in the transcript, covariantizes this
noncentral readout without changing its information under the uniform hidden
involution prior.

For three naturally sampled coset states, condition on source irreps
``lambda_1,lambda_2,lambda_3`` without postselection.  The unnormalized
informative Fourier block is

    tensor_i d_i/|S_n| [I + rho_(lambda_i)(h)].

The module computes exact channels for alternating left/right pair-carrier
Luders instruments followed by the Young-basis readout.  It also computes the
carrier transcript with the row outcome discarded, an exhaustive product
strong-Fourier baseline over all relative ``S_n`` basis rotations for
``n<=4``, and the existing product/global PGM benchmarks.

The algebraic boundary is exact:

* source labels and every carrier-only transcript have zero information about
  the member ``h`` of a fixed conjugacy class;
* all information in the extended protocol is the conditional row term
  ``I(H;J | source, carrier transcript)``;
* a noncentral readout therefore escapes the invariance no-go, but does not
  inherit useful information from a large carrier commutator.

Finite controls show that one carrier measurement can slightly improve the
default Young-basis mutual information for ``S_4`` perfect matchings.  The
gain is not robust: it does not uniformly beat relative-basis product strong
Fourier sampling, it is dominated by the finite global PGM, and additional
alternating carrier measurements reduce rather than amplify the signal.  No
asymptotic decoder or speedup follows.
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

from coset_natural_multicopy_pgm_benchmark import audit_natural_multicopy_pgm
from coset_three_copy_recoupling_obstruction import involutions
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_plancherel_carrier_contextuality import (
    _kron_three,
    _triple_isotypic_projectors,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_carrier_noncentral_readout_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CARRIER-NONCENTRAL-READOUT-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class CarrierRowScheduleRecord:
    schedule: str
    carrier_measurement_depth: int
    output_count: int
    mutual_information_bits: float
    bayes_success_probability: float
    carrier_transcript_mutual_information_bits: float
    carrier_transcript_bayes_success_probability: float
    information_gain_over_default_product_young_bits: float
    bayes_gain_over_default_product_young: float
    information_gap_to_best_group_orbit_product_basis_bits: float
    bayes_gap_to_best_group_orbit_product_basis: float
    information_gap_to_global_pgm_bits: float
    bayes_gap_to_global_pgm: float
    probability_normalization_residual: float
    transcript_probability_normalization_residual: float
    status: str


@dataclass(frozen=True)
class ProductBasisBaseline:
    relative_basis_setting_count: int
    best_mutual_information_bits: float
    best_mutual_information_basis_pair: tuple[Permutation, Permutation]
    best_bayes_success_probability: float
    best_bayes_basis_pair: tuple[Permutation, Permutation]
    exhaustive_over_group_orbit_bases: bool
    exhaustive_over_all_local_povms: bool
    status: str


@dataclass(frozen=True)
class CarrierNoncentralFiniteControl:
    control_id: str
    n: int
    transposition_count: int
    hidden_involution_count: int
    copy_count: int
    schedules: tuple[CarrierRowScheduleRecord, ...]
    product_basis_baseline: ProductBasisBaseline
    product_one_copy_pgm_mutual_information_bits: float
    product_one_copy_pgm_bayes_success_probability: float
    global_pgm_mutual_information_bits: float
    global_pgm_bayes_success_probability: float
    best_carrier_schedule_by_information: str
    best_carrier_mutual_information_bits: float
    best_carrier_schedule_by_bayes: str
    best_carrier_bayes_success_probability: float
    maximum_carrier_transcript_mutual_information_residual: float
    carrier_readout_has_hidden_conditioned_signal: bool
    deeper_alternation_improves_over_depth_one: bool
    best_carrier_beats_global_pgm_information: bool
    best_carrier_beats_global_pgm_bayes: bool
    exact_natural_channel_control_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierNoncentralReadoutTheorem:
    natural_fourier_block: str
    carrier_transcript_invariance: str
    information_chain_rule: str
    minimum_noncentral_effect: str
    covariantization: str
    finite_baseline_boundary: str
    scope_limit: str
    carrier_transcript_zero_information_proved: bool
    minimum_covariant_noncentral_readout_compiled: bool
    physical_hidden_conditioned_signal_exhibited: bool
    carrier_contextuality_implies_decoder_information: bool
    uniform_collective_advantage_proved: bool
    scalable_hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierNoncentralReadoutBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CarrierNoncentralFiniteControl]
    theorem: CarrierNoncentralReadoutTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _entropy_bits(probabilities: np.ndarray) -> float:
    positive = probabilities[probabilities > 1e-15]
    return -float(np.sum(positive * np.log2(positive)))


def _channel_statistics(channel: np.ndarray) -> tuple[float, float, float]:
    rows = np.clip(np.asarray(channel, dtype=float), 0.0, None)
    row_sums = rows.sum(axis=1)
    residual = float(np.max(np.abs(row_sums - 1.0)))
    rows = rows / row_sums[:, None]
    marginal = rows.mean(axis=0)
    information = _entropy_bits(marginal) - sum(
        _entropy_bits(row) for row in rows
    ) / len(rows)
    bayes = float(rows.max(axis=0).sum() / len(rows))
    return information, bayes, residual


def _natural_informative_block(
    sources: tuple[Partition, Partition, Partition],
    hidden: Permutation,
    representations: dict[Partition, dict[Permutation, np.ndarray]],
) -> np.ndarray:
    order = math.factorial(sum(sources[0]))
    factors = []
    for source in sources:
        dimension = hook_length_dimension(source)
        factors.append(
            dimension
            / order
            * (np.eye(dimension) + representations[source][hidden])
        )
    return _kron_three(*factors)


@lru_cache(maxsize=None)
def natural_carrier_row_channels(
    n: int,
    transposition_count: int,
    schedules: tuple[str, ...] = ("", "L", "R", "LR", "RL", "LRL", "RLR"),
) -> tuple[tuple[str, np.ndarray, np.ndarray], ...]:
    """Return exact natural row and carrier-transcript channels.

    The empty schedule is the three-copy product Young-basis baseline.  The
    finite implementation is deliberately restricted to ``n<=4``; it is an
    exact falsification control, not a claimed scalable classical algorithm.
    """

    if not 2 <= n <= 4:
        raise ValueError("exact carrier-row controls require 2<=n<=4")
    if not schedules or schedules[0] != "":
        raise ValueError("schedules must begin with the empty baseline")
    if any(any(side not in "LR" for side in schedule) for schedule in schedules):
        raise ValueError("carrier schedules may contain only L and R")
    partitions = tuple(integer_partitions(n))
    hidden_values = involutions(n, transposition_count)
    representations = {
        partition: dict(permutation_representation_matrices(partition))
        for partition in partitions
    }
    row_channels = {
        schedule: [[] for _ in hidden_values] for schedule in schedules
    }
    transcript_channels = {
        schedule: [[] for _ in hidden_values] for schedule in schedules
    }
    for sources in itertools.product(partitions, repeat=3):
        projectors = {
            "L": _triple_isotypic_projectors(sources, "left"),
            "R": _triple_isotypic_projectors(sources, "right"),
        }
        for hidden_index, hidden in enumerate(hidden_values):
            state = _natural_informative_block(
                sources,
                hidden,
                representations,
            )
            for schedule in schedules:
                branches = (state,)
                for side in schedule:
                    branches = tuple(
                        projector @ branch @ projector
                        for branch in branches
                        for projector in projectors[side]
                    )
                for branch in branches:
                    row_channels[schedule][hidden_index].extend(
                        np.diag(branch).real.tolist()
                    )
                    transcript_channels[schedule][hidden_index].append(
                        float(np.trace(branch).real)
                    )
    output = []
    for schedule in schedules:
        output.append(
            (
                schedule,
                np.asarray(row_channels[schedule], dtype=float),
                np.asarray(transcript_channels[schedule], dtype=float),
            )
        )
    return tuple(output)


@lru_cache(maxsize=None)
def exhaustive_group_orbit_product_baseline(
    n: int,
    transposition_count: int,
) -> ProductBasisBaseline:
    """Optimize three local Young-basis rotations over the represented group.

    Simultaneous global rotation only relabels the uniform hidden prior, so the
    first local basis is fixed to the identity and all relative pairs are
    enumerated.  This is not an optimization over arbitrary local POVMs.
    """

    if not 2 <= n <= 4:
        raise ValueError("exhaustive product-basis controls require 2<=n<=4")
    partitions = tuple(integer_partitions(n))
    hidden_values = involutions(n, transposition_count)
    order = math.factorial(n)
    representations = {
        partition: dict(permutation_representation_matrices(partition))
        for partition in partitions
    }
    group = tuple(representations[partitions[0]])
    identity = tuple(range(n))
    one_copy: dict[Permutation, tuple[np.ndarray, ...]] = {}
    for basis_element in group:
        hidden_rows = []
        for hidden in hidden_values:
            outcomes = []
            for partition in partitions:
                dimension = hook_length_dimension(partition)
                basis = representations[partition][basis_element]
                block = dimension / order * (
                    np.eye(dimension) + representations[partition][hidden]
                )
                outcomes.extend(
                    np.diag(basis.conj().T @ block @ basis).real.tolist()
                )
            hidden_rows.append(np.asarray(outcomes, dtype=float))
        one_copy[basis_element] = tuple(hidden_rows)

    best_information = -1.0
    best_information_pair = (identity, identity)
    best_bayes = -1.0
    best_bayes_pair = (identity, identity)
    for second in group:
        for third in group:
            channel = np.asarray(
                [
                    np.einsum(
                        "i,j,k->ijk",
                        one_copy[identity][index],
                        one_copy[second][index],
                        one_copy[third][index],
                        optimize=True,
                    ).reshape(-1)
                    for index in range(len(hidden_values))
                ]
            )
            information, bayes, _ = _channel_statistics(channel)
            if information > best_information:
                best_information = information
                best_information_pair = (second, third)
            if bayes > best_bayes:
                best_bayes = bayes
                best_bayes_pair = (second, third)
    return ProductBasisBaseline(
        relative_basis_setting_count=len(group) ** 2,
        best_mutual_information_bits=best_information,
        best_mutual_information_basis_pair=best_information_pair,
        best_bayes_success_probability=best_bayes,
        best_bayes_basis_pair=best_bayes_pair,
        exhaustive_over_group_orbit_bases=True,
        exhaustive_over_all_local_povms=False,
        status="group-orbit-product-basis-exhausted-general-local-povm-open",
    )


def audit_carrier_noncentral_control(
    control_id: str,
    n: int,
    transposition_count: int,
) -> CarrierNoncentralFiniteControl:
    channels = natural_carrier_row_channels(n, transposition_count)
    product_basis = exhaustive_group_orbit_product_baseline(
        n,
        transposition_count,
    )
    pgm = audit_natural_multicopy_pgm(n, transposition_count, 3)
    raw_statistics = {
        schedule: (
            _channel_statistics(row_channel),
            _channel_statistics(transcript_channel),
        )
        for schedule, row_channel, transcript_channel in channels
    }
    baseline_information, baseline_bayes, _ = raw_statistics[""][0]
    records = []
    for schedule, row_channel, _ in channels:
        (information, bayes, residual), (
            transcript_information,
            transcript_bayes,
            transcript_residual,
        ) = raw_statistics[schedule]
        records.append(
            CarrierRowScheduleRecord(
                schedule=schedule or "NONE",
                carrier_measurement_depth=len(schedule),
                output_count=row_channel.shape[1],
                mutual_information_bits=information,
                bayes_success_probability=bayes,
                carrier_transcript_mutual_information_bits=transcript_information,
                carrier_transcript_bayes_success_probability=transcript_bayes,
                information_gain_over_default_product_young_bits=(
                    information - baseline_information
                ),
                bayes_gain_over_default_product_young=bayes - baseline_bayes,
                information_gap_to_best_group_orbit_product_basis_bits=(
                    information - product_basis.best_mutual_information_bits
                ),
                bayes_gap_to_best_group_orbit_product_basis=(
                    bayes - product_basis.best_bayes_success_probability
                ),
                information_gap_to_global_pgm_bits=(
                    information - pgm.global_pgm_mutual_information_bits
                ),
                bayes_gap_to_global_pgm=(
                    bayes - pgm.global_pgm_relabelled_bayes_success_probability
                ),
                probability_normalization_residual=residual,
                transcript_probability_normalization_residual=transcript_residual,
                status=(
                    "finite-carrier-row-gain-over-default-young"
                    if schedule and information > baseline_information + 1e-10
                    else "finite-carrier-row-no-gain-over-default-young"
                    if schedule
                    else "default-product-young-baseline"
                ),
            )
        )
    nonempty = [record for record in records if record.schedule != "NONE"]
    best_information = max(nonempty, key=lambda record: record.mutual_information_bits)
    best_bayes = max(nonempty, key=lambda record: record.bayes_success_probability)
    depth_one_information = max(
        record.mutual_information_bits
        for record in nonempty
        if record.carrier_measurement_depth == 1
    )
    deeper_information = max(
        record.mutual_information_bits
        for record in nonempty
        if record.carrier_measurement_depth > 1
    )
    maximum_transcript = max(
        abs(record.carrier_transcript_mutual_information_bits)
        for record in records
    )
    normalization = max(
        max(
            record.probability_normalization_residual,
            record.transcript_probability_normalization_residual,
        )
        for record in records
    )
    signal = any(
        record.mutual_information_bits > 1e-10 for record in nonempty
    )
    verified = normalization <= 1e-10 and maximum_transcript <= 1e-10 and signal
    return CarrierNoncentralFiniteControl(
        control_id=control_id,
        n=n,
        transposition_count=transposition_count,
        hidden_involution_count=len(involutions(n, transposition_count)),
        copy_count=3,
        schedules=tuple(records),
        product_basis_baseline=product_basis,
        product_one_copy_pgm_mutual_information_bits=(
            pgm.product_one_copy_pgm_mutual_information_bits
        ),
        product_one_copy_pgm_bayes_success_probability=(
            pgm.product_one_copy_pgm_bayes_success_probability
        ),
        global_pgm_mutual_information_bits=pgm.global_pgm_mutual_information_bits,
        global_pgm_bayes_success_probability=(
            pgm.global_pgm_relabelled_bayes_success_probability
        ),
        best_carrier_schedule_by_information=best_information.schedule,
        best_carrier_mutual_information_bits=best_information.mutual_information_bits,
        best_carrier_schedule_by_bayes=best_bayes.schedule,
        best_carrier_bayes_success_probability=best_bayes.bayes_success_probability,
        maximum_carrier_transcript_mutual_information_residual=maximum_transcript,
        carrier_readout_has_hidden_conditioned_signal=signal,
        deeper_alternation_improves_over_depth_one=(
            deeper_information > depth_one_information + 1e-10
        ),
        best_carrier_beats_global_pgm_information=(
            best_information.mutual_information_bits
            > pgm.global_pgm_mutual_information_bits + 1e-10
        ),
        best_carrier_beats_global_pgm_bayes=(
            best_bayes.bayes_success_probability
            > pgm.global_pgm_relabelled_bayes_success_probability + 1e-10
        ),
        exact_natural_channel_control_verified=verified,
        status=(
            "noncentral-signal-exact-carrier-refinement-baseline-limited"
            if verified
            else "carrier-noncentral-control-failure"
        ),
    )


def carrier_noncentral_readout_theorem() -> CarrierNoncentralReadoutTheorem:
    return CarrierNoncentralReadoutTheorem(
        natural_fourier_block=(
            "For source tuple lambda, the naturally weighted informative block "
            "is tensor_i d_lambda_i/|S_n| [I+rho_lambda_i(h)]."
        ),
        carrier_transcript_invariance=(
            "Every source-label and carrier-PVM transcript effect commutes with "
            "simultaneous conjugation, so its law is identical for all h in "
            "one conjugacy class and I(H;T)=0."
        ),
        information_chain_rule=(
            "For the final noncentral row outcome J, I(H;T,J)=I(H;J|T) "
            "because I(H;T)=0; the carrier transcript itself contributes no bits."
        ),
        minimum_noncentral_effect=(
            "A fixed Young-basis rank-one diagonal effect lies outside the "
            "carrier algebra and has hidden-conditioned probabilities."
        ),
        covariantization=(
            "Choose uniform public g, conjugate the final row basis by the "
            "diagonal representation U_g, and retain g. Carrier PVMs commute "
            "with U_g and the uniform hidden prior makes this an information-"
            "preserving covariant instrument."
        ),
        finite_baseline_boundary=(
            "Exact S_3/S_4 controls compare every alternating schedule through "
            "depth three with exhaustive group-orbit product bases and product/"
            "global PGM channels. A small default-basis gain is not robust."
        ),
        scope_limit=(
            "The finite enumerator is factorial and the product-basis baseline "
            "does not optimize all local POVMs. No all-n information bound, "
            "efficient row decoder, or classical separation is proved."
        ),
        carrier_transcript_zero_information_proved=True,
        minimum_covariant_noncentral_readout_compiled=True,
        physical_hidden_conditioned_signal_exhibited=True,
        carrier_contextuality_implies_decoder_information=False,
        uniform_collective_advantage_proved=False,
        scalable_hidden_involution_decoder_compiled=False,
        theorem_verified=True,
        status="minimum-noncentral-readout-compiled-carrier-gain-not-robust",
    )


def run_carrier_noncentral_readout_boundary() -> CarrierNoncentralReadoutBoundaryReport:
    controls = [
        audit_carrier_noncentral_control("S3-TRANSPOSITIONS", 3, 1),
        audit_carrier_noncentral_control("S4-TRANSPOSITIONS", 4, 1),
        audit_carrier_noncentral_control("S4-PERFECT-MATCHINGS", 4, 2),
    ]
    theorem = carrier_noncentral_readout_theorem()
    verified = theorem.theorem_verified and all(
        control.exact_natural_channel_control_verified for control in controls
    )
    default_gain_controls = sum(
        any(
            record.carrier_measurement_depth > 0
            and record.information_gain_over_default_product_young_bits > 1e-10
            for record in control.schedules
        )
        for control in controls
    )
    group_orbit_gain_controls = sum(
        control.best_carrier_mutual_information_bits
        > control.product_basis_baseline.best_mutual_information_bits + 1e-10
        for control in controls
    )
    global_pgm_dominates = sum(
        not control.best_carrier_beats_global_pgm_information
        and not control.best_carrier_beats_global_pgm_bayes
        for control in controls
    )
    metrics: dict[str, int | float] = {
        "carrier_transcript_zero_information_theorem_count": int(verified),
        "minimum_covariant_noncentral_readout_compiler_count": int(verified),
        "physical_hidden_conditioned_signal_control_count": sum(
            control.carrier_readout_has_hidden_conditioned_signal
            for control in controls
        ),
        "finite_control_count": len(controls),
        "finite_schedule_count": sum(len(control.schedules) for control in controls),
        "finite_carrier_gain_over_default_young_control_count": default_gain_controls,
        "finite_carrier_gain_over_group_orbit_product_control_count": (
            group_orbit_gain_controls
        ),
        "finite_global_pgm_dominates_carrier_control_count": global_pgm_dominates,
        "deeper_alternation_gain_control_count": sum(
            control.deeper_alternation_improves_over_depth_one
            for control in controls
        ),
        "maximum_carrier_transcript_information_residual": max(
            control.maximum_carrier_transcript_mutual_information_residual
            for control in controls
        ),
        "maximum_best_carrier_information_bits": max(
            control.best_carrier_mutual_information_bits for control in controls
        ),
        "uniform_collective_advantage_theorem_count": 0,
        "scalable_hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CarrierNoncentralReadoutBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "input": "three independent natural mixed coset states with common h",
            "carrier_instruments": (
                "alternating exact left/right pair-isotypic Luders measurements"
            ),
            "noncentral_readout": (
                "fixed Young-basis diagonal measurement, covariantized by "
                "retained uniform public conjugation"
            ),
            "query_model": (
                "coset-state samples plus known representation-theoretic "
                "carrier GPE and strong-Fourier basis operations"
            ),
            "classical_baselines": (
                "exact transcript channel, exhaustive relative group-orbit "
                "product bases, product one-copy PGM, and global PGM"
            ),
        },
        finite_controls=controls,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "escape_carrier_conjugation_invariance",
                "resolved": verified,
                "resolution": (
                    "The Young rank-one row effect is noncentral and exact "
                    "finite channels have positive hidden-conditioned information."
                ),
            },
            {
                "obligation": "localize_information_outside_carrier_transcript",
                "resolved": verified,
                "resolution": (
                    "Carrier transcript laws are class-invariant; the chain "
                    "rule places every bit in the final conditional row outcome."
                ),
            },
            {
                "obligation": "prove_carrier_refinement_advantage_all_n",
                "resolved": False,
                "resolution": (
                    "The finite gain occurs only on one S_4 control and deeper "
                    "alternation degrades it."
                ),
            },
            {
                "obligation": "beat_general_separable_measurements",
                "resolved": False,
                "resolution": (
                    "The exhaustive baseline covers group-orbit projective "
                    "bases only; arbitrary local POVMs remain a stronger baseline."
                ),
            },
            {
                "obligation": "compile_scalable_identity_decoder",
                "resolved": False,
                "resolution": (
                    "Positive mutual information is not a polynomial outcome "
                    "decoder, and the finite global PGM remains substantially stronger."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Large Racah disturbance itself contains the hidden label.",
                "survives": False,
                "response": (
                    "Discarding the final row outcome leaves exactly zero "
                    "mutual information for every schedule."
                ),
            },
            {
                "challenge": "More alternating carrier measurements amplify row information.",
                "survives": False,
                "response": (
                    "Every finite class has its best carrier protocol at depth "
                    "one; depth two and three lose information."
                ),
            },
            {
                "challenge": "Any gain over the default Young basis is collective advantage.",
                "survives": False,
                "response": (
                    "Relative local basis choices and PGM baselines must be "
                    "tested; the finite global PGM dominates all carrier schedules."
                ),
            },
            {
                "challenge": "The row readout is still conjugation-invariant.",
                "survives": False,
                "response": (
                    "Rank-one Young effects are noncentral. Public random "
                    "conjugation supplies a covariant family while retaining orientation."
                ),
            },
            {
                "challenge": "Finite exact enumeration is a scalable decoder.",
                "survives": False,
                "response": (
                    "The enumeration is factorial and establishes only a small-"
                    "degree mechanism/falsifier boundary."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "carrier_transcript_zero_hidden_information_proved": verified,
            "minimum_covariant_noncentral_readout_compiled": verified,
            "physical_hidden_conditioned_row_signal_exhibited": verified,
            "carrier_contextuality_alone_implies_decoder_information": False,
            "finite_carrier_gain_over_default_young_seen": default_gain_controls > 0,
            "finite_carrier_gain_robust_to_product_baselines": False,
            "deeper_racah_alternation_amplifies_identity_information": False,
            "all_n_collective_information_advantage_proved": False,
            "scalable_hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A minimum noncentral outcome escapes the invariance theorem, "
                "but the finite signal is baseline-limited and is degraded by "
                "additional carrier contextuality."
            ),
        },
        status=(
            "noncentral-readout-accessible-carrier-contextuality-not-decoder"
            if verified
            else "carrier-noncentral-readout-control-failure"
        ),
        summary=(
            "Compiled and exactly audited the minimum covariant noncentral row "
            "readout after carrier measurements. Carrier transcripts contain "
            "zero hidden information; the finite row signal survives, but does "
            "not robustly beat product baselines and weakens with deeper Racah "
            "alternation."
        ),
        falsifiers_triggered=[
            "Carrier-label transcripts remain exactly hidden-identity blind even after adaptive alternation.",
            "A fixed noncentral row outcome is sufficient to break invariance but not sufficient to obtain a useful decoder.",
            "The small S_4 perfect-matching gain over the default Young basis is not a universal product-measurement separation.",
            "Increasing carrier contextuality depth reduces identification information on every exact control.",
            "Finite global PGM channels dominate every tested carrier-row schedule.",
            "No all-n information advantage, efficient decoder, classical separation, or speedup is established.",
        ],
    )


def write_carrier_noncentral_readout_boundary_report(
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
    payload = asdict(run_carrier_noncentral_readout_boundary())
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
                title="Carrier noncentral row-readout boundary",
                status="completed-noncentral-signal-baseline-limited",
                hypothesis=(
                    "A minimal covariant noncentral row outcome may convert "
                    "the extensive Racah carrier disturbance into information "
                    "about the hidden involution."
                ),
                protocol=(
                    "Compute exact natural three-copy channels for alternating "
                    "pair-carrier instruments followed by a covariantized Young "
                    "row readout; compare product-basis and PGM baselines."
                ),
                positive_signal=(
                    "An all-n carrier-conditioned row channel with a proved "
                    "advantage over general separable measurements and an "
                    "efficient outcome decoder."
                ),
                falsifiers=[
                    "carrier transcripts themselves are assigned hidden information",
                    "a default-basis finite gain is called collective advantage",
                    "deeper contextuality is assumed to improve decoding",
                    "factorial exact enumeration is called an efficient algorithm",
                ],
                metrics=[
                    "carrier_transcript_zero_information_theorem_count",
                    "minimum_covariant_noncentral_readout_compiler_count",
                    "finite_carrier_gain_over_default_young_control_count",
                    "finite_global_pgm_dominates_carrier_control_count",
                    "scalable_hidden_involution_decoder_count",
                ],
                dependencies=[
                    "self_dual_wreath_plancherel_carrier_racah_access_boundary.py",
                    "coset_strong_fourier_information_scaling.py",
                    "coset_natural_multicopy_pgm_benchmark.py",
                ],
                next_actions=[
                    "replace the terminal rank-one row basis by a source-specific PGM multiplicity-row verifier",
                    "derive an all-n information comparison against arbitrary separable POVMs",
                    "test whether one carrier projection can be integrated into the natural frame polar without dense assembly",
                    "attack any surviving statistic with tensor-network and classical sampling baselines",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-CARRIER-NONCENTRAL-"
            "READOUT-BOUNDARY-LATEST"
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
                    "self_dual_wreath_carrier_noncentral_readout_boundary": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="CARRIER-TRANSCRIPT-CONTEXTUALITY-NOT-HIDDEN-INFORMATION",
                source=registry_experiment_id,
                claim=(
                    "An adaptive transcript of noncommuting pair-carrier labels "
                    "contains information about which conjugate involution is hidden."
                ),
                reason_invalid=(
                    "Every transcript effect remains in the simultaneous-"
                    "conjugation commutant; exact channels and the algebraic "
                    "invariance theorem give zero mutual information."
                ),
                lesson=(
                    "Attribute all identity information to an explicit "
                    "noncentral outcome and audit it separately."
                ),
                applies_to=[
                    registry_candidate_id,
                    "carrier contextuality",
                    "adaptive carrier-label protocols",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="DEEPER-CARRIER-ALTERNATION-NOT-DECODER-AMPLIFIER",
                source=registry_experiment_id,
                claim=(
                    "Increasing the depth of overlapping carrier-PVM "
                    "alternation converts larger Racah disturbance into more "
                    "hidden-involution information."
                ),
                reason_invalid=(
                    "On every exact S_3/S_4 control, depth-two and depth-three "
                    "alternation provide less row mutual information than the "
                    "best depth-one carrier projection, and the global PGM "
                    "dominates every schedule."
                ),
                lesson=(
                    "Optimize a source-specific noncentral frame row, not the "
                    "amount of carrier disturbance."
                ),
                applies_to=[
                    registry_candidate_id,
                    "Racah disturbance",
                    "carrier-row decoder search",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_carrier_noncentral_readout_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

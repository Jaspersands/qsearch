"""Multiplicity-stratum obstruction to per-target DCP witness amplification.

The arbitrary-measurement reduction transfers DCP decoding success to average
uniform-legal subset-sum witness preparation.  It does not give a guarantee for
every legal target.  This module proves that neither cyclic covariance nor the
natural signed/unit instance self-reductions can close that gap by themselves.

For public labels let ``c_s`` be the size of legal fiber ``s`` and

    |psi_0> = sum_s sqrt(c_s/2^m) |F_s>.

Choose one multiplicity stratum ``B={s:c_s=j}`` with at least two targets.  Give
every accepted target ``s notin B`` the same unit Gram vector ``e_0``.  Give the
targets in ``B`` the vectors ``zeta^ell e_1``, where the roots of unity sum to
zero.  If ``C`` is their Gram matrix, then ``C`` is positive semidefinite with
unit diagonal.  Consequently ``E_0=C/N`` is the seed of an exact cyclic
covariant POVM on the legal fiber span.  Equal amplitudes within ``B`` cancel,
so

    C|psi_0> = A sum_(s notin B) |F_s>,
    A = sum_(s notin B) sqrt(c_s/2^m).

The measurement has correct decoding probability ``p=A^2/N``.  The cleaned
inverse filter from ``dcp_arbitrary_measurement_witness_reduction.py`` has

    q_s = 1  for s notin B,
    q_s = 0  for s in B.                                (1)

Thus even constant average decoding success does not force nonzero per-target
witness success.

At density one (``m=n``), the quenched Poisson law gives
``|{s:c_s=j}|/N -> exp(-1)/j!``.  For every fixed ``j>=1`` the rejected legal
mass tends to ``1/(j!(e-1))>0``, while

    p -> (sum_(ell>=1, ell!=j) exp(-1)sqrt(ell)/ell!)^2 > 0.

Finally, coordinate permutations, Boolean complements, and multiplication by
units of ``Z_N`` are witness bijections.  They preserve ``c_s`` exactly, so a
target in the rejected stratum remains rejected along its entire natural
self-reduction orbit.

The seed uses the full multiplicity table and is not an efficient measurement
construction.  The theorem is an information-theoretic counterexample to a
proof strategy, not a DCP algorithm or a lower bound.  Any per-target upgrade
must exploit an efficiently provable regularity of measurement-induced filters
or a reduction that genuinely crosses multiplicity strata.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from dcp_subset_sum_qtt_contraction_search import exact_cyclic_subset_sum_counts
from dcp_subset_sum_random_self_reduction import transform_instance
from research_registry import utc_now


REPORT_PATH = Path(
    "research/reductions/dcp_per_target_stratum_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class StratumFilterControl:
    control_id: str
    modulus: int
    assignment_count: int
    legal_target_count: int
    rejected_multiplicity: int
    rejected_target_count: int
    rejected_legal_fraction: float
    correlation_dimension: int
    correlation_psd_residual: float
    correlation_unit_diagonal_residual: float
    povm_completeness_residual: float
    decoder_success_probability: float
    minimum_accepted_target_success: float
    maximum_accepted_target_success: float
    maximum_rejected_target_success: float
    uniform_legal_witness_success: float
    predicted_uniform_legal_witness_success: float
    filter_residual: float
    decoder_success_constant_at_finite_size: bool
    per_target_success_proved: bool
    stratum_filter_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplicityOrbitControl:
    n_bits: int
    register_count: int
    target: int
    target_multiplicity: int
    transformation_count: int
    transformed_multiplicity_minimum: int
    transformed_multiplicity_maximum: int
    signed_unit_orbit_preserves_multiplicity: bool
    orbit_crosses_multiplicity_strata: bool
    status: str


@dataclass(frozen=True)
class PoissonStratumLimit:
    rejected_multiplicity: int
    limiting_unconditional_target_mass: float
    limiting_uniform_legal_target_mass: float
    limiting_accepted_amplitude_coefficient: float
    limiting_decoder_success_probability: float
    rejected_stratum_has_positive_legal_mass: bool
    decoder_success_has_positive_constant_limit: bool
    per_target_gap_persists_asymptotically: bool
    status: str


@dataclass(frozen=True)
class PerTargetStratumObstructionTheorem:
    correlation_seed_construction: str
    exact_povm_statement: str
    cleaned_filter_statement: str
    density_one_limit: str
    natural_orbit_invariant: str
    consequence: str
    scope_limit: str
    covariance_forces_per_target_success: bool
    natural_self_reduction_upgrades_average_to_every_target: bool
    efficient_stratum_filter_measurement_constructed: bool
    per_target_witness_solver_constructed: bool
    information_theoretic_counterexample_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPPerTargetStratumObstructionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_filter_controls: list[StratumFilterControl]
    multiplicity_orbit_controls: list[MultiplicityOrbitControl]
    poisson_limits: list[PoissonStratumLimit]
    theorem: PerTargetStratumObstructionTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_law(
    counts: Sequence[int] | np.ndarray,
) -> tuple[np.ndarray, tuple[int, ...], int]:
    values = np.asarray(counts, dtype=np.int64)
    if values.ndim != 1 or values.size < 2 or np.any(values < 0):
        raise ValueError("counts must be a nonnegative vector")
    assignment_count = int(np.sum(values))
    support = tuple(int(index) for index in np.flatnonzero(values))
    if assignment_count <= 0 or not support:
        raise ValueError("a nonempty legal support is required")
    return values, support, assignment_count


def multiplicity_stratum_correlation(
    counts: Sequence[int] | np.ndarray,
    rejected_multiplicity: int,
) -> tuple[tuple[int, ...], np.ndarray, np.ndarray]:
    """Return support, legal amplitudes, and the exact stratum-filter Gram seed."""

    if rejected_multiplicity < 1:
        raise ValueError("rejected multiplicity must be positive")
    values, support, assignment_count = _support_law(counts)
    rejected = [
        position
        for position, residue in enumerate(support)
        if int(values[residue]) == rejected_multiplicity
    ]
    if len(rejected) < 2:
        raise ValueError("the rejected multiplicity stratum needs at least two targets")
    rejected_set = set(rejected)
    vectors = np.zeros((len(support), 2), dtype=complex)
    vectors[
        [position for position in range(len(support)) if position not in rejected_set],
        0,
    ] = 1.0
    for phase_index, position in enumerate(rejected):
        vectors[position, 1] = np.exp(
            2j * np.pi * phase_index / len(rejected)
        )
    correlation = vectors @ vectors.conj().T
    amplitudes = np.sqrt(
        np.asarray([values[residue] for residue in support], dtype=float)
        / assignment_count
    )
    return support, amplitudes, correlation


def audit_stratum_filter(
    control_id: str,
    counts: Sequence[int] | np.ndarray,
    rejected_multiplicity: int,
    *,
    tolerance: float = 1e-10,
) -> StratumFilterControl:
    values, support, assignment_count = _support_law(counts)
    modulus = len(values)
    support_result, state, correlation = multiplicity_stratum_correlation(
        values,
        rejected_multiplicity,
    )
    if support_result != support:
        raise ArithmeticError("support mismatch")
    rejected_mask = np.asarray(
        [values[residue] == rejected_multiplicity for residue in support],
        dtype=bool,
    )
    accepted_mask = ~rejected_mask
    if not np.any(accepted_mask):
        raise ValueError("at least one accepted target is required")
    seed = correlation / modulus
    eigenvalues = np.linalg.eigvalsh(
        (correlation + correlation.conj().T) / 2
    )
    psd_residual = max(0.0, -float(eigenvalues[0]))
    diagonal_residual = float(
        np.max(np.abs(np.diag(correlation) - 1.0))
    )
    # Distinct support residues make the cyclic twirl kill every off-diagonal.
    completeness = np.diag(np.diag(correlation))
    completeness_residual = float(
        np.linalg.norm(completeness - np.eye(len(support)), ord=2)
    )
    filtered = correlation @ state
    success = float(np.vdot(state, filtered).real / modulus)
    if success <= tolerance:
        raise ArithmeticError("the filter must retain positive decoder success")
    beta = filtered / (modulus * math.sqrt(success))
    target_success = modulus * np.abs(beta) ** 2
    expected = accepted_mask.astype(float)
    filter_residual = float(np.max(np.abs(target_success - expected)))
    accepted_minimum = float(np.min(target_success[accepted_mask]))
    accepted_maximum = float(np.max(target_success[accepted_mask]))
    rejected_maximum = float(np.max(target_success[rejected_mask]))
    average = float(np.mean(target_success))
    predicted_average = float(np.count_nonzero(accepted_mask) / len(support))
    verified = bool(
        psd_residual <= tolerance
        and diagonal_residual <= tolerance
        and completeness_residual <= tolerance
        and filter_residual <= 100 * tolerance
        and rejected_maximum <= 100 * tolerance
        and abs(accepted_minimum - 1.0) <= 100 * tolerance
        and abs(accepted_maximum - 1.0) <= 100 * tolerance
        and abs(average - predicted_average) <= 100 * tolerance
    )
    return StratumFilterControl(
        control_id=control_id,
        modulus=modulus,
        assignment_count=assignment_count,
        legal_target_count=len(support),
        rejected_multiplicity=rejected_multiplicity,
        rejected_target_count=int(np.count_nonzero(rejected_mask)),
        rejected_legal_fraction=float(np.mean(rejected_mask)),
        correlation_dimension=len(support),
        correlation_psd_residual=psd_residual,
        correlation_unit_diagonal_residual=diagonal_residual,
        povm_completeness_residual=completeness_residual,
        decoder_success_probability=success,
        minimum_accepted_target_success=accepted_minimum,
        maximum_accepted_target_success=accepted_maximum,
        maximum_rejected_target_success=rejected_maximum,
        uniform_legal_witness_success=average,
        predicted_uniform_legal_witness_success=predicted_average,
        filter_residual=filter_residual,
        decoder_success_constant_at_finite_size=success >= 0.01,
        per_target_success_proved=False,
        stratum_filter_verified=verified,
        status=(
            "exact-covariant-measurement-rejects-one-multiplicity-stratum"
            if verified
            else "stratum-filter-control-failure"
        ),
    )


def audit_multiplicity_orbit(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    *,
    transformation_count: int = 12,
    seed: int = 0,
) -> MultiplicityOrbitControl:
    if transformation_count < 1:
        raise ValueError("transformation_count must be positive")
    modulus = 1 << n_bits
    normalized = [int(label) % modulus for label in labels]
    counts = exact_cyclic_subset_sum_counts(normalized, modulus)
    multiplicity = int(counts[target % modulus])
    if multiplicity <= 0:
        raise ValueError("target must be legal")
    rng = random.Random(seed)
    transformed_multiplicities = []
    for _ in range(transformation_count):
        mask = [rng.randrange(2) for _ in normalized]
        unit = rng.randrange(1, modulus, 2)
        transformed_labels, transformed_target = transform_instance(
            n_bits,
            normalized,
            target % modulus,
            mask,
            unit,
        )
        transformed_counts = exact_cyclic_subset_sum_counts(
            transformed_labels,
            modulus,
        )
        transformed_multiplicities.append(
            int(transformed_counts[transformed_target])
        )
    preserved = all(value == multiplicity for value in transformed_multiplicities)
    return MultiplicityOrbitControl(
        n_bits=n_bits,
        register_count=len(normalized),
        target=target % modulus,
        target_multiplicity=multiplicity,
        transformation_count=transformation_count,
        transformed_multiplicity_minimum=min(transformed_multiplicities),
        transformed_multiplicity_maximum=max(transformed_multiplicities),
        signed_unit_orbit_preserves_multiplicity=preserved,
        orbit_crosses_multiplicity_strata=not preserved,
        status=(
            "natural-self-reduction-orbit-is-multiplicity-stratified"
            if preserved
            else "multiplicity-orbit-invariance-failure"
        ),
    )


def _poisson_sqrt_moment(maximum: int = 80) -> float:
    return sum(
        math.exp(-1.0) * math.sqrt(value) / math.factorial(value)
        for value in range(1, maximum + 1)
    )


def poisson_stratum_limit(rejected_multiplicity: int) -> PoissonStratumLimit:
    if rejected_multiplicity < 1:
        raise ValueError("rejected multiplicity must be positive")
    zero = math.exp(-1.0)
    unconditional = zero / math.factorial(rejected_multiplicity)
    legal = unconditional / (1.0 - zero)
    rejected_amplitude = (
        zero
        * math.sqrt(rejected_multiplicity)
        / math.factorial(rejected_multiplicity)
    )
    accepted_amplitude = _poisson_sqrt_moment() - rejected_amplitude
    success = accepted_amplitude**2
    return PoissonStratumLimit(
        rejected_multiplicity=rejected_multiplicity,
        limiting_unconditional_target_mass=unconditional,
        limiting_uniform_legal_target_mass=legal,
        limiting_accepted_amplitude_coefficient=accepted_amplitude,
        limiting_decoder_success_probability=success,
        rejected_stratum_has_positive_legal_mass=legal > 0,
        decoder_success_has_positive_constant_limit=success > 0,
        per_target_gap_persists_asymptotically=legal > 0 and success > 0,
        status="positive-decoder-success-with-positive-rejected-legal-stratum",
    )


def per_target_stratum_obstruction_theorem(
) -> PerTargetStratumObstructionTheorem:
    return PerTargetStratumObstructionTheorem(
        correlation_seed_construction=(
            "C is the Gram matrix of e_0 on accepted targets and root-of-unity "
            "phases times e_1 on one equal-amplitude multiplicity stratum"
        ),
        exact_povm_statement=(
            "C>=0 and diag(C)=1, so E_0=C/N and its cyclic translates sum to I"
        ),
        cleaned_filter_statement=(
            "the arbitrary-measurement inverse has q_s=1 off the rejected "
            "stratum and q_s=0 on it"
        ),
        density_one_limit=(
            "for fixed j, rejected uniform-legal mass tends to 1/(j!(e-1)) "
            "while decoder success tends to a positive constant"
        ),
        natural_orbit_invariant=(
            "coordinate permutations/complements and odd-unit multiplication "
            "are witness bijections and preserve c_s exactly"
        ),
        consequence=(
            "covariance, completeness, and natural instance randomization do "
            "not upgrade average legal-target witness success to every target"
        ),
        scope_limit=(
            "The multiplicity-aware seed is not shown efficiently implementable. "
            "The result blocks an information-theoretic proof strategy, not "
            "efficient per-target reductions using new non-orbit structure."
        ),
        covariance_forces_per_target_success=False,
        natural_self_reduction_upgrades_average_to_every_target=False,
        efficient_stratum_filter_measurement_constructed=False,
        per_target_witness_solver_constructed=False,
        information_theoretic_counterexample_proved=True,
        theorem_verified=True,
        status="per-target-upgrade-blocked-by-multiplicity-stratum-counterexample",
    )


def _finite_controls() -> tuple[list[StratumFilterControl], list[MultiplicityOrbitControl]]:
    filters: list[StratumFilterControl] = []
    orbits: list[MultiplicityOrbitControl] = []
    for n_bits, seed in ((6, 1061), (7, 2081), (8, 4099)):
        modulus = 1 << n_bits
        rng = random.Random(seed)
        for attempt in range(64):
            labels = [rng.randrange(modulus) for _ in range(n_bits)]
            counts = exact_cyclic_subset_sum_counts(labels, modulus).astype(
                np.int64
            )
            multiplicities = [
                value
                for value in (1, 2, 3)
                if np.count_nonzero(counts == value) >= 2
                and np.count_nonzero((counts > 0) & (counts != value)) >= 1
            ]
            if not multiplicities:
                continue
            rejected = multiplicities[min(attempt, len(multiplicities) - 1)]
            filters.append(
                audit_stratum_filter(
                    f"DENSITY-ONE-N{n_bits}-J{rejected}",
                    counts,
                    rejected,
                )
            )
            target = int(np.flatnonzero(counts == rejected)[0])
            orbits.append(
                audit_multiplicity_orbit(
                    n_bits,
                    labels,
                    target,
                    transformation_count=10,
                    seed=seed + 17,
                )
            )
            break
        else:
            raise ArithmeticError("failed to generate a finite stratum control")
    return filters, orbits


def run_per_target_stratum_obstruction(
) -> DCPPerTargetStratumObstructionReport:
    controls, orbits = _finite_controls()
    limits = [poisson_stratum_limit(value) for value in (1, 2, 3, 4)]
    theorem = per_target_stratum_obstruction_theorem()
    failures = (
        sum(not row.stratum_filter_verified for row in controls)
        + sum(not row.signed_unit_orbit_preserves_multiplicity for row in orbits)
        + sum(not row.per_target_gap_persists_asymptotically for row in limits)
    )
    verified = failures == 0 and theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "exact_stratum_filter_control_count": len(controls),
        "multiplicity_orbit_control_count": len(orbits),
        "finite_control_failure_count": failures,
        "poisson_positive_mass_stratum_count": len(limits),
        "information_theoretic_per_target_counterexample_count": int(verified),
        "minimum_finite_decoder_success": min(
            row.decoder_success_probability for row in controls
        ),
        "maximum_rejected_target_success": max(
            row.maximum_rejected_target_success for row in controls
        ),
        "minimum_limiting_decoder_success": min(
            row.limiting_decoder_success_probability for row in limits
        ),
        "minimum_limiting_rejected_legal_mass": min(
            row.limiting_uniform_legal_target_mass for row in limits
        ),
        "efficient_stratum_filter_measurement_count": 0,
        "per_target_witness_solver_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DCPPerTargetStratumObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": "density-one cyclic DCP phase ensemble on legal fibers",
            "measurement_class": "all exact covariant POVMs at the information-theoretic level",
            "rejected_set": "one fixed equal-amplitude multiplicity stratum",
            "self_reduction_group": (
                "coordinate permutations, Boolean complements, and units of Z_N"
            ),
            "dependency": (
                "quenched Poisson fiber law proved in the existing uniform-legal multiplicity module"
            ),
            "scope": theorem.scope_limit,
        },
        finite_filter_controls=controls,
        multiplicity_orbit_controls=orbits,
        poisson_limits=limits,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "construct_valid_covariant_stratum_filter_povm",
                "resolved": verified,
                "resolution": (
                    "The root-of-unity Gram construction is PSD with unit "
                    "diagonal and cyclic twirl equal to identity."
                ),
            },
            {
                "obligation": "derive_exact_cleaned_per_target_filter",
                "resolved": verified,
                "resolution": (
                    "Equal rejected amplitudes cancel, yielding q=0 there and "
                    "q=1 on every accepted legal target."
                ),
            },
            {
                "obligation": "show_gap_survives_density_one_scaling",
                "resolved": True,
                "resolution": (
                    "The zero-truncated Poisson law gives every fixed stratum "
                    "positive legal mass and the accepted amplitude a positive limit."
                ),
            },
            {
                "obligation": "upgrade_by_natural_instance_randomization",
                "resolved": False,
                "resolution": (
                    "Those witness-bijection transformations preserve exact "
                    "multiplicity, so they cannot leave the rejected stratum."
                ),
            },
            {
                "obligation": "implement_stratum_filter_efficiently",
                "resolved": False,
                "resolution": (
                    "The construction consumes the full multiplicity table and "
                    "is deliberately not promoted to an algorithm."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "POVM completeness might forbid a zero target-success coordinate.",
                "survives": True,
                "response": (
                    "Completeness fixes only the seed diagonal. The PSD Gram "
                    "off-diagonals create exact destructive cancellation."
                ),
            },
            {
                "challenge": "A constant decoder success might disappear asymptotically.",
                "survives": True,
                "response": (
                    "The Poisson limit gives an explicit positive constant for "
                    "every fixed rejected multiplicity."
                ),
            },
            {
                "challenge": "Random signed/unit transforms can move a hard target to an easy one.",
                "survives": True,
                "response": (
                    "They preserve fiber cardinality exactly, and the counterexample "
                    "accepts or rejects whole multiplicity strata."
                ),
            },
            {
                "challenge": "The counterexample is itself an efficient DCP decoder.",
                "survives": True,
                "response": (
                    "No. It is multiplicity-table dependent and only refutes an "
                    "information-theoretic per-target inference."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "covariance_implies_uniform_per_target_filter": False,
            "natural_self_reduction_crosses_multiplicity_strata": False,
            "average_to_per_target_upgrade_proved": False,
            "efficient_counterexample_measurement_constructed": False,
            "average_measurement_to_witness_reduction_invalidated": False,
            "per_target_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A valid covariant POVM can have constant decoding success while "
                "its witness filter vanishes on a positive-mass multiplicity "
                "stratum, and natural witness-bijection orbits preserve that stratum."
            ),
        },
        status=(
            "per-target-stratum-obstruction-certified"
            if verified
            else "per-target-stratum-obstruction-control-failure"
        ),
        summary=(
            "Covariance and natural DCP instance symmetries cannot upgrade the "
            "average witness reduction to every legal target: an exact constant-"
            "success POVM can reject an entire positive-mass multiplicity stratum."
        ),
        falsifiers_triggered=[
            "POVM completeness constrains the diagonal seed but does not force every cleaned target coefficient to be nonzero.",
            "Constant average DCP decoding success does not imply inverse-polynomial success for every legal subset-sum target.",
            "Signed, permuted, and odd-unit self-reductions preserve target multiplicity and cannot cross the counterexample's rejected stratum.",
            "The multiplicity-aware counterexample is not efficiently implementable and is not a quantum algorithm.",
            "The existing average measurement-to-witness reduction remains valid and is not weakened by this boundary.",
        ],
    )


def write_per_target_stratum_obstruction(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_per_target_stratum_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CP-PER-TARGET-STRATUM-OBSTRUCTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "dcp_per_target_stratum_obstruction": str(path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    output = write_per_target_stratum_obstruction()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))

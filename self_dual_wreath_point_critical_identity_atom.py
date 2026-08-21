"""The critical ambient point-energy spike is a factorially rare atom.

In the retained time--orientation-character state, diagonal measurement has

    Pr[s,z | g] = |G|^-1 p(z | s^-1 g),

where ``p`` is the branch-character law.  For every public source tuple,

    K_0(e)=I,       K_z(e)=0 for z!=0,

so ``p(0|e)=1``.  The event

    A_g = {s=g, z=0}

therefore has probability exactly ``1/N`` for ``N=|S_n|``.  In the point
quotient ``g(point)=j``, its subprobability distribution is

    r_j(s,0) = n/N^2  if s(point)=j,
               0      otherwise.                         (1)

Its average is ``1/N^2`` on every ``(s,0)``.  Consequently

    sum_(s,z) (r_j-r_bar)^2 = (n-1)/N^3,                 (2)

and on a retained register of dimension ``D=Nq``, ``q=2^k``,

    S_atom = D ||r_j-r_bar||_2^2 = (n-1)q/N^2.           (3)

The identity witness in the copy-threshold theorem is

    S_witness = (n-1)(q-1)/N^2,                           (4)

so (3) differs from it by only ``(n-1)/N^2``.  At
``k=ceil(2log_2 N)`` the existing upper and lower bounds imply

    |E S_total-S_atom| = o(1).                            (5)

Thus the entire known annealed critical ambient energy is asymptotically
explained by a source-independent rare atom.

Operationally, append a common failure outcome to (1).  On the atom, reading
``s(point)`` identifies ``j`` perfectly; off the atom one can only guess in
this isolated channel.  Its exact success is

    1/n + (n-1)/(nN),                                    (6)

and its relative collision is ``(n-1)/N``.  Both are factorially small.

This theorem kills the identity witness as evidence for a decoder.  It does
not prove that the full critical point state is useless: a residual with
``o(1)`` normalized Hilbert--Schmidt energy can still have large trace norm or
relative collision if spread over many average-state directions.  That
signal-weighted residual is the only remaining carrier-traced critical route.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_branch_character_decoder_boundary import (
    branch_character_distribution_from_cycle_type,
)
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    inverse_permutation,
)
from self_dual_wreath_point_copy_threshold import annealed_point_signal_bounds
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_point_critical_identity_atom.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-CRITICAL-IDENTITY-ATOM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class CriticalIdentityAtomControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    group_order: int
    orientation_count: int
    retained_dimension: int
    maximum_diagonal_channel_residual: float
    minimum_full_minus_atom_probability: float
    atom_total_mass: float
    predicted_atom_total_mass: float
    atom_normalized_hilbert_schmidt_energy: float
    predicted_atom_normalized_energy: float
    identity_witness_energy: float
    atom_minus_identity_witness_energy: float
    predicted_atom_minus_witness: float
    atom_relative_collision: float
    predicted_atom_relative_collision: float
    atom_completed_optimal_success: float
    predicted_atom_completed_optimal_success: float
    exact_identity_atom_channel_verified: bool
    status: str


@dataclass(frozen=True)
class CriticalIdentityAtomScalingRecord:
    n: int
    hidden_label_count_decimal: str
    critical_copy_count: int
    retained_dimension_log2: float
    atom_mass_log2: float
    atom_normalized_energy: float
    identity_witness_energy: float
    atom_minus_witness_energy_log2: float
    total_energy_distance_from_atom_upper_bound: float
    total_energy_distance_from_atom_log2_upper_bound: float
    atom_relative_collision_log2: float
    atom_operational_excess_log2: float
    atom_operational_excess_superpolynomially_small: bool
    annealed_critical_ambient_energy_atom_dominated: bool
    collision_free_residual_dominance_transfer_proved: bool
    residual_relative_collision_controlled: bool
    status: str


@dataclass(frozen=True)
class CriticalIdentityAtomTheorem:
    measured_channel: str
    identity_atom: str
    atom_energy: str
    copy_threshold_witness: str
    critical_dominance: str
    operational_value: str
    residual_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CriticalIdentityAtomReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CriticalIdentityAtomTheorem
    finite_controls: list[CriticalIdentityAtomControl]
    scaling_records: list[CriticalIdentityAtomScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _exp2(log2_value: float) -> float:
    if log2_value < -1074.0:
        return 0.0
    if log2_value > 1023.0:
        return math.inf
    return math.exp2(log2_value)


def measured_point_channel(
    labels: tuple[Label, ...],
    *,
    point: int | None = None,
) -> np.ndarray:
    if not labels:
        raise ValueError("at least one source label is required")
    n = sum(labels[0][0])
    if point is None:
        point = n - 1
    permutations = _permutations(n)
    order = len(permutations)
    subgroup_order = math.factorial(n - 1)
    orientation_count = 1 << len(labels)
    output = np.zeros((n, order * orientation_count), dtype=float)
    inverse = {permutation: inverse_permutation(permutation) for permutation in permutations}
    laws = {
        cycle: branch_character_distribution_from_cycle_type(labels, cycle)
        for cycle in {permutation_cycle_type(item) for item in permutations}
    }
    for image in range(n):
        hidden_fiber = tuple(
            hidden for hidden in permutations if hidden[point] == image
        )
        for source_index, source in enumerate(permutations):
            for hidden in hidden_fiber:
                relative = compose_permutations(inverse[source], hidden)
                cycle = permutation_cycle_type(relative)
                section = slice(
                    source_index * orientation_count,
                    (source_index + 1) * orientation_count,
                )
                output[image, section] += laws[cycle] / (order * subgroup_order)
    return output


def identity_atom_channel(
    n: int,
    copy_count: int,
    *,
    point: int | None = None,
) -> np.ndarray:
    if n < 2 or copy_count < 1:
        raise ValueError("require n>=2 and a positive copy count")
    if point is None:
        point = n - 1
    permutations = _permutations(n)
    order = len(permutations)
    orientation_count = 1 << copy_count
    output = np.zeros((n, order * orientation_count), dtype=float)
    atom_probability = n / (order * order)
    for image in range(n):
        for source_index, source in enumerate(permutations):
            if source[point] == image:
                output[image, source_index * orientation_count] = atom_probability
    return output


def _optimal_success(probabilities: np.ndarray) -> float:
    return float(np.sum(np.max(probabilities, axis=0)) / len(probabilities))


def audit_critical_identity_atom(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-10,
) -> CriticalIdentityAtomControl:
    measured = measured_point_channel(labels)
    atom = identity_atom_channel(n, len(labels))
    states = point_quotient_states(labels, point=n - 1)
    direct_diagonal = np.stack(tuple(np.diag(state).real for state in states))
    diagonal_residual = float(np.max(np.abs(measured - direct_diagonal)))
    minimum_remainder = float(np.min(measured - atom))

    order = math.factorial(n)
    orientation_count = 1 << len(labels)
    dimension = order * orientation_count
    atom_average = np.mean(atom, axis=0)
    centered = atom - atom_average
    energies = dimension * np.sum(centered * centered, axis=1)
    atom_energy = float(np.mean(energies))
    predicted_energy = (n - 1) * orientation_count / (order * order)
    witness = (n - 1) * (orientation_count - 1) / (order * order)
    difference = atom_energy - witness
    positive = atom_average > tolerance
    relative = np.sum(
        centered[:, positive] ** 2 / atom_average[positive],
        axis=1,
    )
    atom_relative = float(np.mean(relative))

    completed = np.pad(atom, ((0, 0), (0, 1)))
    completed[:, -1] = 1.0 - np.sum(atom, axis=1)
    optimal = _optimal_success(completed)
    predicted_optimal = 1.0 / n + (n - 1) / (n * order)
    mass = float(np.mean(np.sum(atom, axis=1)))
    predicted_relative = (n - 1) / order
    verified = bool(
        diagonal_residual <= 100 * tolerance
        and minimum_remainder >= -100 * tolerance
        and abs(mass - 1 / order) <= 100 * tolerance
        and np.max(np.abs(energies - predicted_energy)) <= 100 * tolerance
        and abs(atom_relative - predicted_relative) <= 100 * tolerance
        and abs(optimal - predicted_optimal) <= 100 * tolerance
        and abs(difference - (n - 1) / (order * order)) <= 100 * tolerance
    )
    return CriticalIdentityAtomControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        group_order=order,
        orientation_count=orientation_count,
        retained_dimension=dimension,
        maximum_diagonal_channel_residual=diagonal_residual,
        minimum_full_minus_atom_probability=minimum_remainder,
        atom_total_mass=mass,
        predicted_atom_total_mass=1 / order,
        atom_normalized_hilbert_schmidt_energy=atom_energy,
        predicted_atom_normalized_energy=predicted_energy,
        identity_witness_energy=witness,
        atom_minus_identity_witness_energy=difference,
        predicted_atom_minus_witness=(n - 1) / (order * order),
        atom_relative_collision=atom_relative,
        predicted_atom_relative_collision=predicted_relative,
        atom_completed_optimal_success=optimal,
        predicted_atom_completed_optimal_success=predicted_optimal,
        exact_identity_atom_channel_verified=verified,
        status=(
            "exact-factorially-rare-critical-identity-atom"
            if verified
            else "critical-identity-atom-validation-failure"
        ),
    )


def critical_identity_atom_scaling_record(
    n: int,
) -> CriticalIdentityAtomScalingRecord:
    if n < 5:
        raise ValueError("copy-threshold bounds require n>=5")
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(2.0 * log2_order)
    ratio = _exp2(copies - 2.0 * log2_order)
    atom_energy = (n - 1) * ratio
    witness_correction_log2 = math.log2(n - 1) - 2.0 * log2_order
    witness = atom_energy - _exp2(witness_correction_log2)
    bounds = annealed_point_signal_bounds(n, copies)
    residual = (
        bounds.identity_total_upper_bound
        - bounds.identity_witness_lower_bound
        + bounds.nonidentity_absolute_upper_bound
        + _exp2(witness_correction_log2)
    )
    residual_log2 = math.log2(residual) if residual > 0 else -math.inf
    operational_log2 = (
        math.log2(n - 1) - math.log2(n) - log2_order
    )
    relative_log2 = math.log2(n - 1) - log2_order
    return CriticalIdentityAtomScalingRecord(
        n=n,
        hidden_label_count_decimal=str(math.factorial(n)),
        critical_copy_count=copies,
        retained_dimension_log2=log2_order + copies,
        atom_mass_log2=-log2_order,
        atom_normalized_energy=atom_energy,
        identity_witness_energy=witness,
        atom_minus_witness_energy_log2=witness_correction_log2,
        total_energy_distance_from_atom_upper_bound=residual,
        total_energy_distance_from_atom_log2_upper_bound=residual_log2,
        atom_relative_collision_log2=relative_log2,
        atom_operational_excess_log2=operational_log2,
        atom_operational_excess_superpolynomially_small=(
            operational_log2 < -math.log2(n) ** 2
        ),
        annealed_critical_ambient_energy_atom_dominated=(
            residual < 1 / n
        ),
        collision_free_residual_dominance_transfer_proved=False,
        residual_relative_collision_controlled=False,
        status="critical-ambient-energy-rare-atom-dominated-residual-relative-open",
    )


def build_critical_identity_atom_report() -> CriticalIdentityAtomReport:
    controls = [
        audit_critical_identity_atom(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_critical_identity_atom(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        critical_identity_atom_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128)
    ]
    failures = sum(not row.exact_identity_atom_channel_verified for row in controls)
    verified = failures == 0 and all(
        row.annealed_critical_ambient_energy_atom_dominated
        for row in scaling[-3:]
    )
    theorem = CriticalIdentityAtomTheorem(
        measured_channel="Pr[s,z|g]=N^-1 p(z|s^-1g).",
        identity_atom=(
            "K_0(e)=I and K_z(e)=0 for z!=0, so (s=g,z=0) has exact mass 1/N."
        ),
        atom_energy="S_atom=(n-1)2^k/N^2.",
        copy_threshold_witness=(
            "S_witness=(n-1)(2^k-1)/N^2 differs from S_atom by (n-1)/N^2."
        ),
        critical_dominance=(
            "At k=ceil(2log2 N), the copy-threshold remainder bounds imply "
            "|E S_total-S_atom|=o(1)."
        ),
        operational_value=(
            "The atom has relative collision (n-1)/N and completed optimal "
            "success 1/n+(n-1)/(nN)."
        ),
        residual_boundary=(
            "Vanishing normalized-HS residual energy does not control residual "
            "trace norm or relative collision."
        ),
        theorem_verified=verified,
        status=(
            "critical-identity-energy-atomized-residual-relative-signal-open"
            if verified
            else "critical-identity-atom-validation-failure"
        ),
    )
    return CriticalIdentityAtomReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "independent natural public labels for annealed dominance; atom is source independent",
            "measurement": "time basis plus orientation Walsh character",
            "critical_width": "k=ceil(2log2(n!))",
            "dominance_scope": "unconditioned annealed normalized Hilbert--Schmidt energy",
            "claim_boundary": (
                "identity witness rejected as operational evidence; residual trace/relative signal open"
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "id": "PO-POINT-CRITICAL-IDENTITY-ATOM",
                "statement": "Identify the exact physical channel behind the critical identity witness.",
                "resolved": verified,
            },
            {
                "id": "PO-POINT-CRITICAL-ANNEALED-ATOM-DOMINANCE",
                "statement": "Prove the atom exhausts annealed critical ambient energy up to o(1).",
                "resolved": verified,
            },
            {
                "id": "PO-POINT-CRITICAL-RESIDUAL-RELATIVE-COLLISION",
                "statement": (
                    "Remove the identity atom and bound the signal-weighted relative "
                    "collision of the residual on typical globally distinct labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-CRITICAL-COLLISION-FREE-RESIDUAL-TRANSFER",
                "statement": (
                    "Transfer a residual, not merely total-energy, theorem through "
                    "global source distinctness conditioning."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The critical identity witness is diffuse collective information.",
                "answer": (
                    "False. It is asymptotically the energy of the explicit rare "
                    "event z=0,s=g with total mass 1/n!."
                ),
                "resolved": True,
            },
            {
                "challenge": "The rare atom gives an inverse-polynomial point decoder.",
                "answer": (
                    "False. Its exact excess is (n-1)/(n n!), factorially small."
                ),
                "resolved": True,
            },
            {
                "challenge": "Atom dominance proves the full point state is useless.",
                "answer": (
                    "Too strong. A diffuse residual can have o(1) normalized-HS "
                    "energy and still carry large trace or relative signal."
                ),
                "resolved": True,
            },
            {
                "challenge": "Annealed dominance automatically transfers to globally distinct labels.",
                "answer": (
                    "Not proved. The atom itself survives unchanged, but signed "
                    "residual control requires a separate conditional theorem."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_identity_atom_channel_theorem_count": int(verified),
            "annealed_critical_atom_dominance_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "tail_n": scaling[-1].n,
            "tail_atom_operational_excess_log2": scaling[-1].atom_operational_excess_log2,
            "tail_total_energy_distance_from_atom_log2_upper_bound": (
                scaling[-1].total_energy_distance_from_atom_log2_upper_bound
            ),
            "residual_relative_collision_theorem_count": 0,
            "collision_free_residual_transfer_theorem_count": 0,
            "harmonic_point_measurement_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "critical_identity_witness_physical_atom_identified": verified,
            "identity_atom_mass_is_one_over_factorial": verified,
            "identity_atom_operational_excess_factorially_small": verified,
            "annealed_critical_ambient_energy_atom_dominated": verified,
            "critical_identity_energy_is_algorithmic_evidence": False,
            "residual_relative_collision_controlled": False,
            "collision_free_residual_dominance_proved": False,
            "critical_harmonic_point_measurement_compiled": False,
            "full_hidden_permutation_decoder_constructed": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The entire known critical ambient-energy witness is explained by "
                "a factorially rare classical atom. Only the low-HS residual can "
                "still support a carrier-traced point mechanism."
            ),
        },
        status=theorem.status,
        summary=(
            "Identified the critical identity term as the exact z=0,s=g atom, "
            "proved it asymptotically exhausts annealed ambient energy, and showed "
            "its operational point excess is factorially small."
        ),
        falsifiers_triggered=[
            "The c=2 identity witness is not diffuse operational evidence.",
            "Theta(n) normalized Hilbert--Schmidt energy can come from total probability 1/n!.",
            "Critical point work must subtract the identity atom before evaluating relative signal.",
            "A residual o(1) ambient-energy bound is not a trace-distance or decoder no-go.",
        ],
    )


def write_critical_identity_atom_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(build_critical_identity_atom_report())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_critical_identity_atom_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

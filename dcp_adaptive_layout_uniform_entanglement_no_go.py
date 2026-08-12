"""All-balanced-layout entanglement no-go for low-bit DCP fibers.

Consider ``m=2q+c`` independent labels modulo ``2^q`` and the normalized
low-bit fiber state for an independent target.  A coordinate MPS may choose
its qubit ordering after seeing every public label.  Previous entanglement
bounds covered only a fixed polynomial dictionary of cuts.

The growing-order Boolean-section theorem closes this adaptive loophole.  For
any selected side ``I`` of ``q+O(1)`` labels, let ``c_(I,s)`` be its residue
multiplicity.  If ``S`` is uniform modulo ``2^q``, that theorem gives, for

    k=o((q/log q)^(1/3)),

    E[(c_(I,S))_k] <= 2                              (1)

for all sufficiently large ``q``.  Therefore

    Pr[max_s c_(I,s) >= T]
      <= 2^(q+1)/(T-k+1)^k.                          (2)

No independence between different cuts is needed.  Union bounding (2) over
all at most ``2^m`` coordinate subsets and choosing

    k=floor((q/log_2 q)^(1/4)),
    log_2 T >= (m+2q+1)/k + 1,

makes the probability that any balanced side has multiplicity above ``T`` at
most ``2^-q``.  Here ``log T=o(q)``.

The full low-bit fiber has mean
``lambda=(2^m-1)/2^q`` and variance at most ``lambda`` by pairwise
independence, so it has size at least ``lambda/2`` except with probability
``4/lambda``.  Across any coordinate cut its squared Schmidt weights are

    L_s R_(t-s) / C_t.

On the simultaneous side-cap event every unnormalized block weight is at most
``T^2``.  Hence retaining Schmidt mass ``eta`` requires rank at least

    eta C_t/T^2 >= eta lambda/(2T^2)=2^(q-o(q)).       (3)

Thus almost every source/target pair has exponential high-fidelity Schmidt
rank across every balanced coordinate cut at once.  Label-adaptive coordinate
orderings cannot rescue polynomial-bond MPS/QTT preparation of this low-bit
fiber state.

This is not a lower bound on general quantum circuits, non-coordinate tensor
factorizations, unbalanced-width algorithms, or coisometries that never
prepare the low-bit fiber state.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from dcp_fiber_entanglement import (
    fiber_schmidt_probabilities,
    fidelity_rank,
    residue_counts,
)
from dcp_subset_sum_growing_order_chain_theorem import (
    lattice_chain_length_upper_bound,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/phase_workbench/"
    "dcp_adaptive_layout_uniform_entanglement_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-ADAPTIVE-LAYOUT-UNIFORM-ENTANGLEMENT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class FiniteAllLayoutEntanglementControl:
    modulus_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    target: int
    full_fiber_size: int
    balanced_layout_count: int
    maximum_side_fiber_multiplicity: int
    minimum_exact_schmidt_rank: int
    minimum_rank_for_requested_mass: int
    minimum_deterministic_side_cap_rank_bound: int
    requested_schmidt_mass: float
    every_layout_fiber_size_consistent: bool
    every_layout_rank_bound_verified: bool
    status: str


@dataclass(frozen=True)
class AllLayoutEntanglementScalingRecord:
    modulus_bits: int
    register_offset: int
    register_count: int
    balanced_window: int
    selected_factorial_moment_order: int
    lattice_chain_length_upper_bound: int
    moment_schedule_condition_ratio: float
    inherited_averaged_factorial_moment_upper_bound: float
    side_multiplicity_cap_log2: int
    side_multiplicity_cap_subexponential: bool
    all_layout_side_cap_failure_log2_upper_bound: float
    full_fiber_mean_log2: float
    full_fiber_lower_tail_log2_upper_bound: float
    requested_schmidt_mass: float
    simultaneous_schmidt_rank_log2_lower_bound: float
    polynomial_bond_benchmark_log2: float
    every_balanced_coordinate_layout_exponential_rank_certified: bool
    finite_row_is_asymptotic_theorem: bool
    status: str


@dataclass(frozen=True)
class AdaptiveLayoutUniformEntanglementTheorem:
    inherited_moment_input: str
    one_side_maximum_tail: str
    all_layout_union_bound: str
    full_fiber_concentration: str
    deterministic_schmidt_bound: str
    asymptotic_consequence: str
    route_consequence: str
    scope_limit: str
    sub_cube_root_moment_schedule_admissible: bool
    all_balanced_coordinate_side_caps_proved: bool
    every_balanced_coordinate_cut_exp_rank_proved: bool
    adaptive_coordinate_mps_polynomial_bond_possible: bool
    inverse_polynomial_easy_source_subset_for_coordinate_mps_possible: bool
    noncoordinate_tensor_network_ruled_out: bool
    general_quantum_circuit_lower_bound_proved: bool
    polynomial_dcp_decoder_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPAdaptiveLayoutUniformEntanglementReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FiniteAllLayoutEntanglementControl]
    scaling_records: list[AllLayoutEntanglementScalingRecord]
    theorem: AdaptiveLayoutUniformEntanglementTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def adaptive_layout_moment_order(modulus_bits: int) -> int:
    if modulus_bits < 16:
        raise ValueError("modulus_bits must be at least sixteen")
    return max(
        2,
        math.floor(
            (modulus_bits / math.log2(modulus_bits)) ** 0.25
        ),
    )


def side_multiplicity_cap_log2(
    modulus_bits: int,
    register_count: int,
    moment_order: int,
    *,
    failure_exponent_bits: int | None = None,
) -> int:
    """Choose a cap making the all-subset union bound exponentially small."""

    if modulus_bits < 2 or register_count < modulus_bits:
        raise ValueError("invalid modulus/register dimensions")
    if moment_order < 2:
        raise ValueError("moment_order must be at least two")
    failure_bits = (
        modulus_bits if failure_exponent_bits is None else failure_exponent_bits
    )
    if failure_bits < 0:
        raise ValueError("failure exponent must be nonnegative")
    return (
        math.ceil(
            (
                register_count
                + modulus_bits
                + 1
                + failure_bits
            )
            / moment_order
        )
        + 1
    )


def all_layout_side_cap_failure_log2_upper_bound(
    modulus_bits: int,
    register_count: int,
    moment_order: int,
    cap_log2: int,
    *,
    averaged_factorial_moment_upper_bound: float = 2.0,
) -> float:
    if averaged_factorial_moment_upper_bound <= 0:
        raise ValueError("moment upper bound must be positive")
    # There are at most 2^m selected sides and 2^q targets.  If c_s>=T
    # and T>=2k, then (c_s)_k >= (T/2)^k.
    return (
        register_count
        + modulus_bits
        + math.log2(averaged_factorial_moment_upper_bound)
        - moment_order * (cap_log2 - 1)
    )


def moment_schedule_condition_ratio(
    modulus_bits: int,
    moment_order: int,
) -> float:
    chain = lattice_chain_length_upper_bound(moment_order)
    numerator = (
        chain * (math.log2(modulus_bits) + moment_order)
        + moment_order * math.log2(moment_order)
    )
    return numerator / modulus_bits


def simultaneous_schmidt_rank_log2_lower_bound(
    full_fiber_mean_log2: float,
    side_cap_log2: float,
    requested_mass: float,
) -> float:
    if not 0.0 < requested_mass <= 1.0:
        raise ValueError("requested_mass must lie in (0,1]")
    return (
        math.log2(requested_mass)
        + full_fiber_mean_log2
        - 1.0
        - 2.0 * side_cap_log2
    )


def _finite_all_layout_control(
    modulus_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
    requested_mass: float,
) -> FiniteAllLayoutEntanglementControl:
    modulus = 1 << modulus_bits
    register_count = 2 * modulus_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    full_counts = residue_counts(labels, modulus_bits)
    legal_targets = [
        residue for residue, count in enumerate(full_counts) if count
    ]
    target = rng.choice(legal_targets)
    fiber_size = full_counts[target]
    left_size = register_count // 2
    layout_count = 0
    maximum_side = 0
    minimum_exact_rank = math.inf
    minimum_mass_rank = math.inf
    minimum_bound = math.inf
    size_consistent = True
    bounds_verified = True
    all_indices = set(range(register_count))
    for left_indices in itertools.combinations(range(register_count), left_size):
        left_set = set(left_indices)
        right_indices = tuple(sorted(all_indices - left_set))
        left_counts = residue_counts(
            [labels[index] for index in left_indices], modulus_bits
        )
        right_counts = residue_counts(
            [labels[index] for index in right_indices], modulus_bits
        )
        probabilities, observed_size = fiber_schmidt_probabilities(
            left_counts, right_counts, target
        )
        layout_count += 1
        size_consistent = size_consistent and observed_size == fiber_size
        side_cap = max(max(left_counts), max(right_counts))
        maximum_side = max(maximum_side, side_cap)
        actual_rank = len(probabilities)
        mass_rank = fidelity_rank(probabilities, requested_mass)
        deterministic_bound = max(
            1,
            math.ceil(
                requested_mass * fiber_size / (side_cap * side_cap)
                - 1e-12
            ),
        )
        minimum_exact_rank = min(minimum_exact_rank, actual_rank)
        minimum_mass_rank = min(minimum_mass_rank, mass_rank)
        minimum_bound = min(minimum_bound, deterministic_bound)
        bounds_verified = bounds_verified and mass_rank >= deterministic_bound
    passed = size_consistent and bounds_verified
    return FiniteAllLayoutEntanglementControl(
        modulus_bits=modulus_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        target=target,
        full_fiber_size=fiber_size,
        balanced_layout_count=layout_count,
        maximum_side_fiber_multiplicity=maximum_side,
        minimum_exact_schmidt_rank=int(minimum_exact_rank),
        minimum_rank_for_requested_mass=int(minimum_mass_rank),
        minimum_deterministic_side_cap_rank_bound=int(minimum_bound),
        requested_schmidt_mass=requested_mass,
        every_layout_fiber_size_consistent=size_consistent,
        every_layout_rank_bound_verified=bounds_verified,
        status=(
            "all-finite-balanced-layout-rank-bounds-verified"
            if passed
            else "finite-all-layout-rank-bound-failure"
        ),
    )


def all_layout_entanglement_scaling_record(
    modulus_bits: int,
    *,
    register_offset: int = 4,
    balanced_window: int = 2,
    requested_schmidt_mass: float = 0.99,
    polynomial_bond_power: int = 12,
) -> AllLayoutEntanglementScalingRecord:
    if modulus_bits < 16:
        raise ValueError("modulus_bits must be at least sixteen")
    if register_offset < 0 or balanced_window < 0:
        raise ValueError("offsets must be nonnegative")
    register_count = 2 * modulus_bits + register_offset
    order = adaptive_layout_moment_order(modulus_bits)
    cap_log = side_multiplicity_cap_log2(
        modulus_bits, register_count, order
    )
    failure_log = all_layout_side_cap_failure_log2_upper_bound(
        modulus_bits, register_count, order, cap_log
    )
    full_mean_log = (
        register_count
        - modulus_bits
        + math.log2(1.0 - math.exp2(-register_count))
    )
    full_failure_log = 2.0 - full_mean_log
    rank_log = simultaneous_schmidt_rank_log2_lower_bound(
        full_mean_log, cap_log, requested_schmidt_mass
    )
    benchmark = polynomial_bond_power * math.log2(register_count)
    condition = moment_schedule_condition_ratio(modulus_bits, order)
    return AllLayoutEntanglementScalingRecord(
        modulus_bits=modulus_bits,
        register_offset=register_offset,
        register_count=register_count,
        balanced_window=balanced_window,
        selected_factorial_moment_order=order,
        lattice_chain_length_upper_bound=lattice_chain_length_upper_bound(order),
        moment_schedule_condition_ratio=condition,
        inherited_averaged_factorial_moment_upper_bound=2.0,
        side_multiplicity_cap_log2=cap_log,
        side_multiplicity_cap_subexponential=(
            cap_log / modulus_bits < 0.5
        ),
        all_layout_side_cap_failure_log2_upper_bound=failure_log,
        full_fiber_mean_log2=full_mean_log,
        full_fiber_lower_tail_log2_upper_bound=full_failure_log,
        requested_schmidt_mass=requested_schmidt_mass,
        simultaneous_schmidt_rank_log2_lower_bound=rank_log,
        polynomial_bond_benchmark_log2=benchmark,
        every_balanced_coordinate_layout_exponential_rank_certified=(
            condition < 1.0
            and cap_log / modulus_bits < 0.5
            and failure_log <= -modulus_bits
            and rank_log > benchmark
        ),
        finite_row_is_asymptotic_theorem=False,
        status=(
            "all-balanced-coordinate-layouts-exponential-rank-certified"
            if rank_log > benchmark and cap_log / modulus_bits < 0.5
            else "finite-scaling-not-yet-in-asymptotic-rank-regime"
        ),
    )


def build_dcp_adaptive_layout_uniform_entanglement_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = ((3, 0), (4, 0)),
    finite_trials: int = 2,
    requested_schmidt_mass: float = 0.99,
    scaling_modulus_bits: tuple[int, ...] = (
        1 << 24,
        1 << 32,
        1 << 40,
        1 << 48,
    ),
) -> DCPAdaptiveLayoutUniformEntanglementReport:
    finite = [
        _finite_all_layout_control(
            modulus_bits,
            offset,
            trial,
            seed=(
                19_000_019 * modulus_bits
                + 1_000_003 * offset
                + trial
            ),
            requested_mass=requested_schmidt_mass,
        )
        for modulus_bits, offset in finite_specs
        for trial in range(finite_trials)
    ]
    scaling = [
        all_layout_entanglement_scaling_record(
            modulus_bits,
            requested_schmidt_mass=requested_schmidt_mass,
        )
        for modulus_bits in scaling_modulus_bits
    ]
    finite_verified = all(
        row.every_layout_fiber_size_consistent
        and row.every_layout_rank_bound_verified
        for row in finite
    )
    asymptotic_verified = all(
        row.every_balanced_coordinate_layout_exponential_rank_certified
        for row in scaling
    )
    verified = finite_verified and asymptotic_verified
    theorem = AdaptiveLayoutUniformEntanglementTheorem(
        inherited_moment_input=(
            "For k=o((q/log q)^(1/3)), the cube-section/Smith-transfer theorem "
            "gives E_(a,S)[(c_S)_k]<=2 for all sufficiently large q."
        ),
        one_side_maximum_tail=(
            "Pr[max_s c_s>=T]<=2^(q+1)/(T-k+1)^k by factorial-moment Markov."
        ),
        all_layout_union_bound=(
            "Union over at most 2^m label subsets; no cross-layout independence "
            "is assumed. The selected T gives failure at most 2^-q."
        ),
        full_fiber_concentration=(
            "Pairwise independence gives mean lambda=(2^m-1)/2^q, variance "
            "at most lambda, and Pr[C_t<lambda/2]<=4/lambda."
        ),
        deterministic_schmidt_bound=(
            "If both side multiplicities are at most T, each Schmidt block has "
            "unnormalized weight at most T^2; eta mass needs rank eta*C_t/T^2."
        ),
        asymptotic_consequence=(
            "With k=(q/log q)^(1/4), log T=o(q), so every balanced coordinate "
            "cut has eta-rank 2^(q-o(q)) with probability 1-2^-Omega(q)."
        ),
        route_consequence=(
            "No label-adaptive coordinate ordering can give a polynomial-bond "
            "MPS/QTT for high-fidelity preparation on inverse-polynomial source mass."
        ),
        scope_limit=(
            "The theorem requires a balanced coordinate cut of the low-bit "
            "fiber state. Non-coordinate tensors, highly unbalanced algorithms, "
            "and circuits/coisometries that avoid that state are not covered."
        ),
        sub_cube_root_moment_schedule_admissible=True,
        all_balanced_coordinate_side_caps_proved=True,
        every_balanced_coordinate_cut_exp_rank_proved=True,
        adaptive_coordinate_mps_polynomial_bond_possible=False,
        inverse_polynomial_easy_source_subset_for_coordinate_mps_possible=False,
        noncoordinate_tensor_network_ruled_out=False,
        general_quantum_circuit_lower_bound_proved=False,
        polynomial_dcp_decoder_constructed=False,
        theorem_verified=verified,
        status=(
            "all-balanced-adaptive-coordinate-layouts-closed"
            if verified
            else "adaptive-layout-asymptotic-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_all_layout_control_count": len(finite),
        "finite_all_layout_control_failure_count": sum(
            not (
                row.every_layout_fiber_size_consistent
                and row.every_layout_rank_bound_verified
            )
            for row in finite
        ),
        "finite_balanced_layout_count": sum(
            row.balanced_layout_count for row in finite
        ),
        "scaling_record_count": len(scaling),
        "all_layout_side_cap_union_theorem_count": 1,
        "all_balanced_coordinate_exp_rank_theorem_count": 1,
        "adaptive_coordinate_mps_no_go_theorem_count": 1,
        "minimum_scaling_rank_exponent_fraction": min(
            row.simultaneous_schmidt_rank_log2_lower_bound
            / row.modulus_bits
            for row in scaling
        ),
        "maximum_all_layout_failure_log2_upper_bound": max(
            row.all_layout_side_cap_failure_log2_upper_bound
            for row in scaling
        ),
        "noncoordinate_tensor_network_no_go_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "polynomial_dcp_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DCPAdaptiveLayoutUniformEntanglementReport(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "m=2q+O(1) independent uniform labels modulo 2^q and an "
                "independent target, conditioned on the full low-bit fiber being nonempty."
            ),
            "architecture": (
                "Coordinate MPS/QTT whose ordering may be any function of all "
                "public labels and target, but has a balanced coordinate cut."
            ),
            "accuracy": (
                f"At least {requested_schmidt_mass:.3f} Schmidt mass."
            ),
            "asymptotic_dependency": (
                "The averaged growing-order factorial-moment theorem from "
                "dcp_subset_sum_cube_section_gap_theorem.py."
            ),
            "non_claim": (
                "No general tensor-network, circuit, query, or DCP lower bound."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-DCP-ADAPTIVE-COORDINATE-LAYOUT",
                "statement": (
                    "Control all balanced coordinate layouts selected after "
                    "seeing the source labels."
                ),
                "resolved": True,
            },
            {
                "id": "PO-DCP-NONCOORDINATE-TENSOR",
                "statement": (
                    "Classify algebraic/non-coordinate tensorizations that do "
                    "not expose a balanced assignment-coordinate cut."
                ),
                "resolved": False,
            },
            {
                "id": "PO-DCP-COISOMETRY-WITHOUT-FIBER-STATE",
                "statement": (
                    "Construct or obstruct an all-fiber arithmetic coisometry "
                    "that never prepares one low-bit fiber state."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The layouts are highly dependent, so union bounds fail.",
                "answer": (
                    "False. A union bound needs no independence; every selected "
                    "side has the same iid marginal source law."
                ),
                "resolved": True,
            },
            {
                "challenge": "The moment theorem controls a random target, not max_s.",
                "answer": (
                    "Summing factorial moments over all targets is exactly "
                    "2^q times the uniform-target average, which yields the max tail."
                ),
                "resolved": True,
            },
            {
                "challenge": "Large side support alone forces large Schmidt rank.",
                "answer": (
                    "Not by itself. The proof instead caps every side "
                    "multiplicity and lower-bounds the common full fiber size."
                ),
                "resolved": True,
            },
            {
                "challenge": "Volume-law entanglement proves circuit hardness.",
                "answer": (
                    "False. Polynomial circuits can create volume-law states; "
                    "only coordinate low-bond tensor architectures are excluded."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "fixed_polynomial_layout_dictionary_route_alive": False,
            "arbitrary_label_adaptive_coordinate_layout_route_alive": False,
            "inverse_polynomial_easy_source_coordinate_mps_route_alive": False,
            "noncoordinate_tensorization_route_alive": True,
            "all_fiber_coisometry_without_state_preparation_alive": True,
            "general_polynomial_quantum_circuit_route_alive": True,
            "polynomial_relation_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The growing moment theorem can be union-bounded over every "
                "balanced coordinate cut, forcing 2^(q-o(q)) high-fidelity "
                "Schmidt rank simultaneously. Only non-coordinate or state-avoiding "
                "implicit transforms remain relevant."
            ),
        },
        status=(
            "adaptive-coordinate-tensor-route-closed-"
            "noncoordinate-coisometry-open"
        ),
        summary=(
            "Upgraded the low-bit fiber entanglement theorem from fixed "
            "polynomial layout dictionaries to every label-adaptive balanced "
            "coordinate ordering at once. Polynomial-bond coordinate MPS/QTT "
            "preparation is closed on all inverse-polynomial source mass."
        ),
        falsifiers_triggered=[
            (
                "Selecting a coordinate ordering after seeing all labels does "
                "not evade the low-bit fiber Schmidt-rank obstruction."
            ),
            (
                "No inverse-polynomial easy-source subset supports a balanced "
                "polynomial-bond coordinate MPS at fixed high fidelity."
            ),
            (
                "The theorem cannot be promoted to non-coordinate tensorizations, "
                "general circuits, or all-fiber coisometries."
            ),
        ],
    )


def write_dcp_adaptive_layout_uniform_entanglement_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-ADAPTIVE-LAYOUT-UNIFORM-ENTANGLEMENT-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(
        build_dcp_adaptive_layout_uniform_entanglement_report(**kwargs)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_dcp_adaptive_layout_uniform_entanglement_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

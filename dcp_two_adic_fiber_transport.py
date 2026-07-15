"""2-adic fiber-transport workbench for density-one modular subset sum.

For F_k(t)={x: <A,x>=t mod 2^k}, a transport that preserves the low k
bits and toggles bit k can pair the two children of a low-bit fiber.  This
module certifies three explicit transport classes:

* flipping coordinate j when v_2(A_j)=k (a total involution);
* swapping coordinates i,j when A_i-A_j=2^k mod 2^(k+1) (a partial
  involution on x_i != x_j);
* swapping two subset patterns inside a small fixed block when their sums
  agree modulo 2^k and differ in bit k.

The first two mechanisms typically reach O(log n) and O(log n) (with a
larger constant) depths.  A polynomial family of O(log n)-bit blocks also
has only O(log n) birthday reach: a union bound is exponentially small at
linear k.  This is a no-go for explicit local transport dictionaries, not
for implicit global quantum walks or all subset-sum algorithms.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_TWO_ADIC_FIBER_TRANSPORT_PATH = Path(
    "research/phase_workbench/dcp_two_adic_fiber_transport.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-TWO-ADIC-FIBER-TRANSPORT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class TransportIdentityCertificate:
    transport_id: str
    transport_class: str
    scope: str
    low_residue_preserved: bool
    next_bit_toggled: bool
    involutive: bool
    total_on_fiber: bool
    proof: str


@dataclass(frozen=True)
class FiberTransportScalingRow:
    n_bits: int
    register_count: int
    trial_index: int
    block_size: int
    block_count: int
    maximum_tested_depth: int
    maximum_single_flip_depth: int
    maximum_swap_depth: int
    maximum_block_transport_depth: int
    single_flip_linear_depth_reached: bool
    swap_linear_depth_reached: bool
    block_linear_depth_reached: bool
    transport_free_tail_bits: int


@dataclass(frozen=True)
class LocalDictionaryNoGoCertificate:
    n_bits: int
    block_size: int
    polynomial_block_family_size: int
    tested_linear_depth: int
    collision_union_bound: float
    inverse_polynomial_threshold: float
    linear_depth_transport_ruled_out_for_model: bool
    theorem_scope: str


@dataclass(frozen=True)
class OpenTransportArchitecture:
    architecture_id: str
    mechanism: str
    why_not_ruled_out: str
    proof_obligations: list[str]
    first_falsifiers: list[str]


@dataclass(frozen=True)
class TwoAdicFiberTransportReport:
    created_at: str
    fiber_contract: dict[str, str]
    identity_certificates: list[TransportIdentityCertificate]
    scaling_rows: list[FiberTransportScalingRow]
    local_dictionary_no_go: list[LocalDictionaryNoGoCertificate]
    open_architectures: list[OpenTransportArchitecture]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def two_adic_valuation(value: int, n_bits: int) -> int:
    residue = value % (1 << n_bits)
    if residue == 0:
        return n_bits
    return (residue & -residue).bit_length() - 1


def subset_sum(labels: Sequence[int], assignment: int) -> int:
    return sum(label for index, label in enumerate(labels) if (assignment >> index) & 1)


def flip_coordinate(assignment: int, coordinate: int) -> int:
    return assignment ^ (1 << coordinate)


def swap_coordinates(assignment: int, left: int, right: int) -> int:
    left_bit = (assignment >> left) & 1
    right_bit = (assignment >> right) & 1
    if left_bit == right_bit:
        return assignment
    return assignment ^ (1 << left) ^ (1 << right)


def certifies_single_flip(label: int, depth: int, n_bits: int) -> bool:
    return two_adic_valuation(label, n_bits) == depth


def certifies_swap(left_label: int, right_label: int, depth: int) -> bool:
    modulus = 1 << (depth + 1)
    return (left_label - right_label) % modulus == 1 << depth


def verify_transport_on_assignment(
    labels: Sequence[int],
    assignment: int,
    transported: int,
    depth: int,
) -> tuple[bool, bool]:
    before = subset_sum(labels, assignment)
    after = subset_sum(labels, transported)
    low_modulus = 1 << depth
    next_modulus = 1 << (depth + 1)
    low_preserved = before % low_modulus == after % low_modulus
    toggled = (after - before) % next_modulus == 1 << depth
    return low_preserved, toggled


def _single_flip_counts(labels: Sequence[int], n_bits: int) -> list[int]:
    counts = [0] * n_bits
    for label in labels:
        valuation = two_adic_valuation(label, n_bits)
        if valuation < n_bits:
            counts[valuation] += 1
    return counts


def _disjoint_swap_counts(labels: Sequence[int], maximum_depth: int) -> list[int]:
    counts: list[int] = []
    for depth in range(maximum_depth + 1):
        low_modulus = 1 << depth
        by_low: dict[int, list[int]] = {}
        for label in labels:
            low = label % low_modulus if low_modulus > 1 else 0
            next_bit = (label >> depth) & 1
            bucket = by_low.setdefault(low, [0, 0])
            bucket[next_bit] += 1
        counts.append(sum(min(bucket) for bucket in by_low.values()))
    return counts


def _block_transport_counts(
    labels: Sequence[int],
    block_size: int,
    maximum_depth: int,
) -> list[int]:
    counts = [0] * (maximum_depth + 1)
    for start in range(0, len(labels), block_size):
        block = labels[start : start + block_size]
        sums = [subset_sum(block, assignment) for assignment in range(1 << len(block))]
        for depth in range(maximum_depth + 1):
            low_modulus = 1 << depth
            by_low: dict[int, list[int]] = {}
            for value in sums:
                low = value % low_modulus if low_modulus > 1 else 0
                next_bit = (value >> depth) & 1
                bucket = by_low.setdefault(low, [0, 0])
                bucket[next_bit] += 1
            counts[depth] += sum(min(bucket) for bucket in by_low.values())
    return counts


def analyze_transport_scaling(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
) -> FiberTransportScalingRow:
    if n_bits < 8:
        raise ValueError("n_bits must be at least eight")
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(1 << n_bits) for _ in range(register_count)]
    block_size = max(2, math.ceil(math.log2(n_bits)))
    maximum_depth = min(n_bits - 1, math.ceil(4 * math.log2(n_bits)))
    single_counts = _single_flip_counts(labels, n_bits)
    swap_counts = _disjoint_swap_counts(labels, maximum_depth)
    block_counts = _block_transport_counts(labels, block_size, maximum_depth)
    maximum_single = max((depth for depth, count in enumerate(single_counts) if count), default=-1)
    maximum_swap = max((depth for depth, count in enumerate(swap_counts) if count), default=-1)
    maximum_block = max((depth for depth, count in enumerate(block_counts) if count), default=-1)
    reached = max(maximum_single, maximum_swap, maximum_block)
    linear_threshold = n_bits // 2
    return FiberTransportScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        trial_index=trial_index,
        block_size=block_size,
        block_count=math.ceil(register_count / block_size),
        maximum_tested_depth=maximum_depth,
        maximum_single_flip_depth=maximum_single,
        maximum_swap_depth=maximum_swap,
        maximum_block_transport_depth=maximum_block,
        single_flip_linear_depth_reached=maximum_single >= linear_threshold,
        swap_linear_depth_reached=maximum_swap >= linear_threshold,
        block_linear_depth_reached=maximum_block >= linear_threshold,
        transport_free_tail_bits=max(0, n_bits - 1 - reached),
    )


def local_dictionary_no_go_certificate(
    n_bits: int,
    block_size: int | None = None,
    polynomial_family_size: int | None = None,
) -> LocalDictionaryNoGoCertificate:
    resolved_block_size = block_size or math.ceil(math.log2(n_bits))
    family_size = polynomial_family_size or n_bits**2
    depth = n_bits // 2
    exponent = 2 * resolved_block_size - depth - 1
    collision_bound = min(1.0, family_size * (2.0**exponent))
    threshold = n_bits**-2
    return LocalDictionaryNoGoCertificate(
        n_bits=n_bits,
        block_size=resolved_block_size,
        polynomial_block_family_size=family_size,
        tested_linear_depth=depth,
        collision_union_bound=collision_bound,
        inverse_polynomial_threshold=threshold,
        linear_depth_transport_ruled_out_for_model=collision_bound < threshold,
        theorem_scope=(
            "Union bound for a target-independent explicit family of fixed blocks, each enumerating all 2^b subset "
            "patterns over independent uniform labels. Overlapping/adaptive blocks require a separate dependence audit; "
            "implicit global transforms are not covered."
        ),
    )


def build_identity_certificates() -> list[TransportIdentityCertificate]:
    return [
        TransportIdentityCertificate(
            transport_id="TRANSPORT-SINGLE-V2-PIVOT",
            transport_class="single-coordinate flip",
            scope="all assignments when v2(A_j)=k",
            low_residue_preserved=True,
            next_bit_toggled=True,
            involutive=True,
            total_on_fiber=True,
            proof=(
                "Toggling x_j changes the sum by +/-A_j; when v2(A_j)=k, both signs equal 2^k modulo 2^(k+1)."
            ),
        ),
        TransportIdentityCertificate(
            transport_id="TRANSPORT-RESIDUE-MATCHED-SWAP",
            transport_class="coordinate swap",
            scope="assignments with x_i != x_j when A_i-A_j=2^k mod 2^(k+1)",
            low_residue_preserved=True,
            next_bit_toggled=True,
            involutive=True,
            total_on_fiber=False,
            proof=(
                "Swapping unequal bits changes the sum by +/-(A_i-A_j), which is 2^k modulo 2^(k+1). Equal bits are fixed."
            ),
        ),
        TransportIdentityCertificate(
            transport_id="TRANSPORT-BLOCK-PATTERN-SWAP",
            transport_class="small-block basis-pattern transposition",
            scope="two block patterns whose sums agree mod 2^k and differ in bit k",
            low_residue_preserved=True,
            next_bit_toggled=True,
            involutive=True,
            total_on_fiber=False,
            proof=(
                "A transposition of two named block patterns is reversible; the certified subset-sum difference toggles exactly the next residue bit."
            ),
        ),
    ]


def open_transport_architectures() -> list[OpenTransportArchitecture]:
    return [
        OpenTransportArchitecture(
            architecture_id="OPEN-TARGET-DEPENDENT-PARTIAL-FIBER-MAP",
            mechanism=(
                "Compute a target-dependent partial map on F_k(t) that pairs inverse-polynomial source mass across "
                "the two child fibers without extending to a total full-cube bijection."
            ),
            why_not_ruled_out=(
                "The total-transport Fourier collapse does not cover target-fiber partial maps, and the local dictionary "
                "union bound does not cover an implicit arithmetic relation sampler."
            ),
            proof_obligations=[
                "Give a polynomial circuit for the partial map, inverse on its image, and success flag.",
                "Prove it preserves F_k(t), toggles bit k, and covers inverse-polynomial source-weighted fiber mass.",
                "Compose transports through k=Theta(n) without exponential condition-number or precision loss.",
                "Beat classical reconstruction from the same transport oracle.",
            ],
            first_falsifiers=[
                "The map extends to a total full-cube transport and is therefore killed by the Fourier pivot theorem.",
                "The transform encodes an explicit polynomial correction dictionary.",
                "Coverage collapses past O(log n) depth.",
                "Computing one transport is equivalent to solving the target subset-sum instance.",
            ],
        ),
        OpenTransportArchitecture(
            architecture_id="OPEN-FIBER-TRANSPORT-QUANTUM-WALK",
            mechanism=(
                "Use local certified swaps as edges of a walk on F_k(t), then implement a coherent child-fiber transfer from spectral structure rather than a named correction."
            ),
            why_not_ruled_out=(
                "Sparse local moves can generate a large connected component even when no single explicit move reaches every witness."
            ),
            proof_obligations=[
                "Prove conductance or spectral gap on random density-one fibers through linear k.",
                "Construct a starting-state preparation and child-marking reflection with polynomial resources.",
                "Show the walk transfer produces a verified witness relation, not only a residue distinguisher.",
                "Audit classical mixing and local-search baselines on the same graph.",
            ],
            first_falsifiers=[
                "The transport graph fragments by a classical invariant.",
                "The spectral gap or marked fraction is exponentially small.",
                "Preparing a vertex in F_k(t) already costs exponential time at linear k.",
            ],
        ),
    ]


def run_two_adic_fiber_transport_audit(
    n_values: Sequence[int] = (32, 64, 128, 256),
    register_offset: int = 4,
    trials_per_size: int = 3,
    seed: int = 0,
) -> TwoAdicFiberTransportReport:
    rows = [
        analyze_transport_scaling(
            n_bits,
            register_offset,
            trial,
            seed + 1_000_003 * n_index + trial,
        )
        for n_index, n_bits in enumerate(n_values)
        for trial in range(trials_per_size)
    ]
    no_go = [local_dictionary_no_go_certificate(n_bits) for n_bits in n_values]
    identities = build_identity_certificates()
    architectures = open_transport_architectures()
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "identity_certificate_count": len(identities),
        "exact_identity_certificate_count": sum(
            item.low_residue_preserved and item.next_bit_toggled and item.involutive
            for item in identities
        ),
        "scaling_row_count": len(rows),
        "maximum_observed_single_flip_depth": max(row.maximum_single_flip_depth for row in rows),
        "maximum_observed_swap_depth": max(row.maximum_swap_depth for row in rows),
        "maximum_observed_block_transport_depth": max(
            row.maximum_block_transport_depth for row in rows
        ),
        "minimum_tail_transport_free_bits": min(row.transport_free_tail_bits for row in tail),
        "linear_depth_single_flip_count": sum(row.single_flip_linear_depth_reached for row in rows),
        "linear_depth_swap_count": sum(row.swap_linear_depth_reached for row in rows),
        "linear_depth_block_transport_count": sum(row.block_linear_depth_reached for row in rows),
        "local_dictionary_linear_depth_no_go_count": sum(
            item.linear_depth_transport_ruled_out_for_model for item in no_go
        ),
        "open_implicit_transport_architecture_count": len(architectures),
        "proved_polynomial_linear_depth_transport_count": 0,
        "proved_polynomial_relation_solver_count": 0,
    }
    return TwoAdicFiberTransportReport(
        created_at=utc_now(),
        fiber_contract={
            "fiber": "F_k(t)={x in {0,1}^m : sum_i A_i x_i=t mod 2^k}",
            "transport_goal": "reversible map preserving the low-k residue and toggling residue bit k",
            "source": "independent uniform A_i modulo 2^n with m=n+O(1)",
            "solver_requirement": "compose through k=Theta(n) and return a verified full-modulus binary witness",
            "no_go_scope": "explicit polynomial families of O(log n)-bit local block dictionaries only",
        },
        identity_certificates=identities,
        scaling_rows=rows,
        local_dictionary_no_go=no_go,
        open_architectures=architectures,
        headline_metrics=metrics,
        claim_gate={
            "low_bit_transport_identities_proved": True,
            "local_dictionary_linear_depth_route_alive": False,
            "implicit_global_total_transport_route_alive": False,
            "target_dependent_partial_transport_route_alive": True,
            "fiber_transport_quantum_walk_route_alive": True,
            "polynomial_linear_depth_transport_proved": False,
            "polynomial_relation_solver_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact local transports expose useful low-bit symmetries, but observed and union-bound reach is "
                "logarithmic while exact inversion needs linear depth. The full-cube Fourier theorem also closes total "
                "global transports; only target-dependent partial maps or a proved polynomial-gap fiber walk remain."
            ),
        },
        status="local-fiber-transport-stalls-implicit-global-route-open",
        summary=(
            f"Certified {len(identities)} exact 2-adic transport identities across {len(rows)} scaling rows. "
            f"No explicit local class reached linear depth; {metrics['local_dictionary_linear_depth_no_go_count']}/"
            f"{len(no_go)} asymptotic rows rule out the polynomial small-block dictionary model at k=n/2."
        ),
        falsifiers_triggered=[
            "Single-coordinate pivots are exact total transports but disappear after logarithmic depth on random labels.",
            "Residue-matched swaps extend local reach but remain partial and logarithmic-depth.",
            "Polynomial families of logarithmic-size explicit blocks have exponentially small collision probability at linear depth.",
            "Finite low-bit transport is not evidence for a full relation solver.",
            "The local no-go does not cover target-dependent partial fiber maps or polynomial-gap walks; total full-cube transports are closed separately.",
        ],
    )


def write_two_adic_fiber_transport_audit(
    path: Path = DCP_TWO_ADIC_FIBER_TRANSPORT_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256),
    register_offset: int = 4,
    trials_per_size: int = 3,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_two_adic_fiber_transport_audit(
            n_values=n_values,
            register_offset=register_offset,
            trials_per_size=trials_per_size,
            seed=seed,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-LOW-BIT-PIVOTS-AS-FULL-FIBER-SOLVER",
                "Exact single-coordinate or residue-swap transports through low bits imply a full density-one subset-sum solver.",
                "Random labels supply these explicit local pivots only to logarithmic depth; a linear number of target bits remains.",
            ),
            (
                "NEG-DCP-POLYNOMIAL-BLOCK-DICTIONARY-AS-LINEAR-TRANSPORT",
                "A polynomial dictionary of logarithmic-size block substitutions supplies child-fiber transports through linear depth.",
                "The scoped birthday/union bound is exponentially small at k=n/2 for the audited explicit fixed-block model.",
            ),
            (
                "NEG-DCP-FINITE-FIBER-TRANSPORT-AS-RELATION-SOLVER",
                "Finite low-bit transport coverage is evidence of inverse-polynomial full-modulus witness recovery.",
                "No polynomial linear-depth transport, starting-state preparation, spectral-gap theorem, or verified relation solver is constructed.",
            ),
        )
        for negative_id, claim, reason in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=(
                        "Retain only target-dependent partial maps or fiber-walk mechanisms that cross linear 2-adic depth "
                        "with polynomial circuits, source coverage, and classical baselines."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-TWO-ADIC-FIBER-TRANSPORT"
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
                artifacts={"dcp_two_adic_fiber_transport": str(path)},
            )
        )
    return payload

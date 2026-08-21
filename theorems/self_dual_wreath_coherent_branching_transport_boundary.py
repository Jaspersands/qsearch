"""Why coherent Racah branching does not prove independent tail smoothing.

The down-``k``/up-``k`` Plancherel chain has a second exact description.  Let
``Xi_k`` be the permutation representation of ``S_n`` on ordered distinct
``k``-tuples.  Its character is

    xi_k(g)=(fix(g))_k,

and tensoring an irrep ``lambda`` with ``Xi_k`` induces the transition

    J_k(lambda,mu)=d_mu/(d_lambda (n)_k)
                    <chi_mu, chi_lambda xi_k>.            (1)

This equals remove-``k``/regrow-``k`` branching exactly.

The projector-tail theorem needs ``J_k tensor J_k`` on the two intermediate
labels while the four outer labels are fixed.  Monoidal naturality instead
branches a Racah diagram coherently: the outer labels and both intermediate
channels share restriction data.  These are different operations.

The distinction cannot be repaired abstractly.  For uniform labels on a
cyclic set, the identity coupling is perfectly invariant when the same random
shift is applied to both labels, yet independent random shifts erase it.  Its
coherent Dirichlet energy is zero while its independent product-chain energy
is ``r-1`` and its mutual information is ``log2(r)``.

Therefore a useful Racah branching proof needs a new quantitative transport
inequality comparing coherent six-label branching with independent
intermediate-label noise.  Naturality alone supplies no such inequality.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_plancherel_down_up_racah_tail_reduction import (
    falling_factorial,
    plancherel_down_up_transition,
)
from symmetric_character import conjugacy_class_size, symmetric_character


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_coherent_branching_transport_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COHERENT-BRANCHING-TRANSPORT-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TensorBranchingIdentityControl:
    n: int
    boxes_removed: int
    partition_count: int
    permutation_module_dimension: int
    maximum_transition_formula_residual: float
    maximum_tensor_multiplicity_integrality_residual: float
    maximum_tensor_multiplicity_negativity: int
    exact_tensor_branching_identity_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentIndependentTransportCountermodel:
    label_count: int
    identity_coupling_mutual_information_bits: float
    coherent_shared_shift_dirichlet_energy: float
    independent_shift_dirichlet_energy: float
    expected_independent_energy: float
    independent_energy_residual: float
    independent_smoothed_likelihood_residual_to_one: float
    exact_coherent_independent_separation_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentBranchingTransportTheorem:
    tensor_product_chain_identity: str
    coherent_operation: str
    projector_tail_operation: str
    abstract_transport_implication_valid: bool
    natural_racah_transport_inequality_proved: bool
    status: str


@dataclass(frozen=True)
class CoherentBranchingTransportReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CoherentBranchingTransportTheorem
    tensor_branching_controls: list[TensorBranchingIdentityControl]
    countermodels: list[CoherentIndependentTransportCountermodel]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def ordered_tuple_permutation_character(
    cycle_type: Partition,
    tuple_length: int,
) -> int:
    fixed_points = cycle_type.count(1)
    return falling_factorial(fixed_points, tuple_length)


def tensor_branching_transition(
    n: int,
    boxes_removed: int,
) -> tuple[tuple[Partition, ...], np.ndarray, np.ndarray]:
    if n < 2 or not 1 <= boxes_removed < n:
        raise ValueError("require n>=2 and 1<=k<n")
    partitions = tuple(integer_partitions(n))
    dimensions = [hook_length_dimension(partition) for partition in partitions]
    module_dimension = falling_factorial(n, boxes_removed)
    transition = np.zeros((len(partitions), len(partitions)), dtype=float)
    multiplicities = np.zeros_like(transition)
    for left_index, left in enumerate(partitions):
        for right_index, right in enumerate(partitions):
            numerator = sum(
                conjugacy_class_size(cycle_type)
                * symmetric_character(left, cycle_type)
                * symmetric_character(right, cycle_type)
                * ordered_tuple_permutation_character(cycle_type, boxes_removed)
                for cycle_type in partitions
            )
            order = math.factorial(n)
            if numerator % order:
                raise ArithmeticError("tensor branching multiplicity is not integral")
            multiplicity = numerator // order
            multiplicities[left_index, right_index] = multiplicity
            transition[left_index, right_index] = (
                dimensions[right_index]
                * multiplicity
                / (dimensions[left_index] * module_dimension)
            )
    return partitions, multiplicities, transition


def audit_tensor_branching_identity(
    n: int,
    boxes_removed: int,
    *,
    tolerance: float = 3e-12,
) -> TensorBranchingIdentityControl:
    if not 3 <= n <= 10:
        raise ValueError("finite tensor-branching controls require 3<=n<=10")
    partitions, multiplicities, tensor_transition = tensor_branching_transition(
        n, boxes_removed
    )
    branching_partitions, _q, branching_transition = plancherel_down_up_transition(
        n, boxes_removed
    )
    if partitions != branching_partitions:
        raise AssertionError("partition order mismatch")
    formula_residual = float(np.max(np.abs(tensor_transition - branching_transition)))
    integrality_residual = float(
        np.max(np.abs(multiplicities - np.rint(multiplicities)))
    )
    negativity = int(max(0.0, -float(np.min(multiplicities))))
    verified = bool(
        formula_residual <= tolerance
        and integrality_residual <= tolerance
        and negativity == 0
    )
    return TensorBranchingIdentityControl(
        n=n,
        boxes_removed=boxes_removed,
        partition_count=len(partitions),
        permutation_module_dimension=falling_factorial(n, boxes_removed),
        maximum_transition_formula_residual=formula_residual,
        maximum_tensor_multiplicity_integrality_residual=integrality_residual,
        maximum_tensor_multiplicity_negativity=negativity,
        exact_tensor_branching_identity_verified=verified,
        status=(
            "down-up-chain-equals-ordered-tuple-tensor-chain"
            if verified
            else "tensor-branching-identity-control-failure"
        ),
    )


def coherent_independent_transport_countermodel(
    label_count: int,
    *,
    tolerance: float = 1e-12,
) -> CoherentIndependentTransportCountermodel:
    r = label_count
    if r < 2:
        raise ValueError("countermodel requires at least two labels")
    q = np.full(r, 1.0 / r)
    reference = q[:, None] * q[None, :]
    likelihood = np.zeros((r, r), dtype=float)
    np.fill_diagonal(likelihood, r)

    coherent = np.zeros_like(likelihood)
    for x in range(r):
        for y in range(r):
            coherent[x, y] = sum(
                likelihood[(x + shift) % r, (y + shift) % r]
                for shift in range(r)
            ) / r
    refresh = np.full((r, r), 1.0 / r)
    independent = refresh @ likelihood @ refresh.T
    coherent_energy = float(np.sum(reference * likelihood * (likelihood - coherent)))
    independent_energy = float(
        np.sum(reference * likelihood * (likelihood - independent))
    )
    expected = float(r - 1)
    independent_residual = abs(independent_energy - expected)
    smoothed_residual = float(np.max(np.abs(independent - 1.0)))
    verified = bool(
        abs(coherent_energy) <= tolerance
        and independent_residual <= tolerance
        and smoothed_residual <= tolerance
    )
    return CoherentIndependentTransportCountermodel(
        label_count=r,
        identity_coupling_mutual_information_bits=math.log2(r),
        coherent_shared_shift_dirichlet_energy=coherent_energy,
        independent_shift_dirichlet_energy=independent_energy,
        expected_independent_energy=expected,
        independent_energy_residual=independent_residual,
        independent_smoothed_likelihood_residual_to_one=smoothed_residual,
        exact_coherent_independent_separation_verified=verified,
        status=(
            "coherent-naturality-does-not-imply-independent-smoothing"
            if verified
            else "coherent-independent-transport-control-failure"
        ),
    )


def run_coherent_branching_transport_boundary(
) -> CoherentBranchingTransportReport:
    tensor_controls = [
        audit_tensor_branching_identity(n, boxes)
        for n in (4, 5, 6, 8)
        for boxes in (1, 2)
    ]
    countermodels = [
        coherent_independent_transport_countermodel(r) for r in (2, 4, 8, 16, 32)
    ]
    failures = sum(
        not row.exact_tensor_branching_identity_verified for row in tensor_controls
    )
    failures += sum(
        not row.exact_coherent_independent_separation_verified
        for row in countermodels
    )
    verified = failures == 0
    theorem = CoherentBranchingTransportTheorem(
        tensor_product_chain_identity=(
            "J_k(lambda,mu)=d_mu/(d_lambda(n)_k)<chi_mu,chi_lambda Ind_(S_(n-k))^(S_n)1>"
        ),
        coherent_operation=(
            "restrict/regrow the full Racah diagram with shared branching data and changing outer labels"
        ),
        projector_tail_operation=(
            "apply independent J_k chains to mu and nu while conditioning on fixed outer labels"
        ),
        abstract_transport_implication_valid=False,
        natural_racah_transport_inequality_proved=False,
        status=(
            "coherent-branching-shortcut-falsified-independent-transport-open"
            if verified
            else "coherent-branching-transport-control-failure"
        ),
    )
    return CoherentBranchingTransportReport(
        created_at=utc_now(),
        theorem_contract={
            "permutation_module": "ordered injective k-tuples, dimension (n)_k",
            "character": "xi_k(g)=(number of fixed points of g)_k",
            "tensor_chain": "dimension-weighted irrep sampled from lambda tensor Xi_k",
            "coherent_branching": "one shared restriction/regrowth environment for the whole diagram",
            "independent_branching": "separate environments on the two intermediate labels",
            "scope": "logical transport boundary; no natural Racah instability lower bound",
        },
        theorem=theorem,
        tensor_branching_controls=tensor_controls,
        countermodels=countermodels,
        proof_obligations=[
            {
                "obligation": "identify_down_up_chain_as_tensor_product_chain",
                "resolved": verified,
                "resolution": "Frobenius reciprocity equates Ind-Res multiplicity with tensoring by the ordered-tuple permutation character.",
            },
            {
                "obligation": "derive_coherent_to_independent_racah_transport_inequality",
                "resolved": False,
                "resolution": "Must compare shared six-label branching against fixed-outer independent intermediate-label branching quantitatively.",
            },
            {
                "obligation": "bound_transport_defect_under_physical_outer_average",
                "resolved": False,
                "resolution": "Any useful defect bound must hold on nonnegligible physical mass at k=Theta(n/log^2 n).",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Functoriality of the associator proves down-up stability.",
                "resolved": True,
                "resolution": "Functoriality is coherent and changes all labels; the Fourier tail uses independent noise at fixed outer labels.",
            },
            {
                "objection": "Shared and independent branching are asymptotically interchangeable by symmetry.",
                "resolved": True,
                "resolution": "The cyclic identity-coupling family has zero shared-noise energy and independent energy r-1 for every r.",
            },
            {
                "objection": "The countermodel proves natural Racah branching is unstable.",
                "resolved": True,
                "resolution": "It proves only that no abstract implication exists; natural representation structure may still yield a transport bound.",
            },
        ],
        headline_metrics={
            "exact_tensor_branching_identity_count": int(verified),
            "finite_tensor_branching_control_count": len(tensor_controls),
            "coherent_independent_countermodel_count": len(countermodels),
            "finite_control_failure_count": failures,
            "natural_racah_transport_inequality_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "down_up_tensor_product_identity_proved": verified,
            "coherent_branching_implies_independent_smoothing": False,
            "natural_racah_transport_inequality_proved": False,
            "natural_racah_branching_stability_proved": False,
            "natural_racah_mutual_information_sublogarithmic_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The only automatic branching identity is coherent; the independent fixed-outer transport defect remains unbounded.",
        },
        status=(
            "branching-naturality-shortcut-closed-transport-theorem-required"
            if verified
            else "coherent-branching-transport-control-failure"
        ),
        summary=(
            "Identified the down/up chain as ordered-tuple tensoring and proved "
            "that coherent Racah naturality cannot supply independent tail smoothing abstractly."
        ),
        falsifiers_triggered=[
            "Coherent restriction is not the product-chain operation in the projector-tail theorem.",
            "Shared-noise invariance can coexist with maximal independent-noise sensitivity.",
        ],
    )


def write_coherent_branching_transport_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_coherent_branching_transport_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_coherent_branching_transport_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

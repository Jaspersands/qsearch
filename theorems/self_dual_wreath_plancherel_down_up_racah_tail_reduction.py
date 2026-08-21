"""Reduce the Racah projector tail to Plancherel branching stability.

Let ``J_k`` be the Markov chain on partitions of ``n`` that removes ``k``
boxes through the Young graph and then adds ``k`` boxes.  It is reversible
for Plancherel measure.  Fulman's exact diagonalization says that the
Plancherel character mode

    phi_C(lambda)=sqrt(|C|)chi_lambda(C)/d_lambda

has eigenvalue

    beta_k(C)=(n-m(C))_k/(n)_k,                           (1)

where ``m(C)`` is the number of moved points.  Therefore, for a two-label
likelihood ``L`` with Fourier coefficients ``a_(C,D)``, the product-chain
Dirichlet form is

    D_k(L)=<L,(I-J_k tensor J_k)L>
          =sum_(C,D)(1-beta_k(C)beta_k(D))a_(C,D)^2.      (2)

If ``Tail_s`` is the energy with ``max(m(C),m(D))>s``, then

    Tail_s(L) <= D_k(L) /
       (1-(n-s-1)_k/(n)_k).                              (3)

Choosing ``k=ceil(n/(s+1))`` makes the denominator at least ``1-e^-1``.
Thus the full projector tail can be killed by proving that the natural Racah
likelihood is stable under deleting and regrowing about ``n/log^2(n)`` boxes,
after separately controlling the low-support Fourier sector.

This is an exact L2 reduction, not the missing stability theorem.  A
one-box chain pays a factor of order ``n/s`` and is generally too weak.  L2
also remains vulnerable to rare spikes, so an entropy or fractional analogue
may still be necessary.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_compressed_racah_coupling_probe import (
    CompleteCompressedRacahCoupling,
    compile_complete_racah_coupling,
)
from self_dual_wreath_plancherel_character_racah_fourier_reduction import (
    plancherel_character_basis_matrix,
)


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_down_up_racah_tail_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-DOWN-UP-RACAH-TAIL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PlancherelDownUpSpectrumControl:
    n: int
    boxes_removed: int
    partition_count: int
    maximum_row_sum_residual: float
    maximum_detailed_balance_residual: float
    maximum_character_eigenfunction_residual: float
    largest_nonconstant_eigenvalue: float
    smallest_nonzero_moved_support: int
    exact_down_up_spectrum_verified: bool
    status: str


@dataclass(frozen=True)
class RacahFourierTailControl:
    model: str
    n: int
    boxes_removed: int
    maximum_retained_moved_support: int
    total_nonconstant_fourier_energy: float
    retained_fourier_energy: float
    omitted_fourier_tail_energy: float
    product_chain_dirichlet_energy: float
    exact_cutoff_spectral_gap: float
    dirichlet_tail_upper: float
    tail_bound_slack: float
    direct_parseval_residual: float
    cutoff_bound_verified: bool
    status: str


@dataclass(frozen=True)
class DownUpRacahTailScalingRecord:
    n: int
    maximum_retained_moved_support: int
    boxes_removed: int
    exact_cutoff_spectral_gap: float
    exponential_gap_lower: float
    one_box_tail_amplification: float
    mesoscopic_tail_amplification: float
    constant_gap_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelDownUpRacahTailTheorem:
    character_mode_eigenvalue: str
    joint_dirichlet_parseval: str
    support_tail_bound: str
    mesoscopic_box_choice: str
    natural_racah_branching_stability_proved: bool
    entropy_stability_analogue_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelDownUpRacahTailReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PlancherelDownUpRacahTailTheorem
    spectrum_controls: list[PlancherelDownUpSpectrumControl]
    tail_controls: list[RacahFourierTailControl]
    scaling_records: list[DownUpRacahTailScalingRecord]
    literature_basis: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def falling_factorial(value: int, length: int) -> int:
    if length < 0:
        raise ValueError("falling-factorial length must be nonnegative")
    if value < length:
        return 0
    return math.prod(range(value - length + 1, value + 1))


def moved_support(cycle_type: Partition) -> int:
    return sum(cycle_type) - cycle_type.count(1)


def down_up_character_eigenvalue(
    cycle_type: Partition,
    boxes_removed: int,
) -> float:
    n = sum(cycle_type)
    if not 1 <= boxes_removed <= n:
        raise ValueError("require 1<=k<=n")
    fixed_points = cycle_type.count(1)
    return falling_factorial(fixed_points, boxes_removed) / falling_factorial(
        n, boxes_removed
    )


def removable_corner_partitions(partition: Partition) -> tuple[Partition, ...]:
    output: list[Partition] = []
    for row, length in enumerate(partition):
        next_length = partition[row + 1] if row + 1 < len(partition) else 0
        if length <= next_length:
            continue
        reduced = list(partition)
        reduced[row] -= 1
        output.append(tuple(value for value in reduced if value > 0))
    return tuple(output)


@lru_cache(maxsize=None)
def down_path_counts(partition: Partition, boxes_removed: int) -> tuple[tuple[Partition, int], ...]:
    if boxes_removed < 0 or boxes_removed > sum(partition):
        return ()
    counts: Counter[Partition] = Counter({partition: 1})
    for _ in range(boxes_removed):
        next_counts: Counter[Partition] = Counter()
        for current, multiplicity in counts.items():
            for reduced in removable_corner_partitions(current):
                next_counts[reduced] += multiplicity
        counts = next_counts
    return tuple(sorted(counts.items(), reverse=True))


def plancherel_down_up_transition(
    n: int,
    boxes_removed: int,
) -> tuple[tuple[Partition, ...], np.ndarray, np.ndarray]:
    if n < 2 or not 1 <= boxes_removed < n:
        raise ValueError("require n>=2 and 1<=k<n")
    partitions = tuple(integer_partitions(n))
    dimensions = np.asarray(
        [hook_length_dimension(partition) for partition in partitions], dtype=float
    )
    q = dimensions**2 / math.factorial(n)
    paths = [dict(down_path_counts(partition, boxes_removed)) for partition in partitions]
    denominator = falling_factorial(n, boxes_removed)
    transition = np.zeros((len(partitions), len(partitions)), dtype=float)
    for left, left_paths in enumerate(paths):
        for right, right_paths in enumerate(paths):
            common = sum(
                multiplicity * right_paths.get(lower, 0)
                for lower, multiplicity in left_paths.items()
            )
            transition[left, right] = (
                common * dimensions[right] / (denominator * dimensions[left])
            )
    return partitions, q, transition


def audit_plancherel_down_up_spectrum(
    n: int,
    boxes_removed: int,
    *,
    tolerance: float = 3e-11,
) -> PlancherelDownUpSpectrumControl:
    if not 3 <= n <= 10:
        raise ValueError("finite spectrum controls require 3<=n<=10")
    partitions, q, transition = plancherel_down_up_transition(n, boxes_removed)
    basis_partitions, basis = plancherel_character_basis_matrix(n)
    if basis_partitions != partitions:
        raise AssertionError("partition order mismatch")
    predicted = np.asarray(
        [down_up_character_eigenvalue(cycle, boxes_removed) for cycle in partitions]
    )
    eigen_residual = float(
        np.max(np.abs(transition @ basis - basis * predicted[None, :]))
    )
    row_residual = float(np.max(np.abs(np.sum(transition, axis=1) - 1.0)))
    balance = q[:, None] * transition
    balance_residual = float(np.max(np.abs(balance - balance.T)))
    identity_index = partitions.index((1,) * n)
    nonconstant = np.delete(predicted, identity_index)
    supports = [moved_support(cycle) for cycle in partitions if cycle != (1,) * n]
    verified = bool(
        row_residual <= tolerance
        and balance_residual <= tolerance
        and eigen_residual <= tolerance
    )
    return PlancherelDownUpSpectrumControl(
        n=n,
        boxes_removed=boxes_removed,
        partition_count=len(partitions),
        maximum_row_sum_residual=row_residual,
        maximum_detailed_balance_residual=balance_residual,
        maximum_character_eigenfunction_residual=eigen_residual,
        largest_nonconstant_eigenvalue=float(np.max(nonconstant)),
        smallest_nonzero_moved_support=min(supports),
        exact_down_up_spectrum_verified=verified,
        status=(
            "plancherel-down-up-character-spectrum-verified"
            if verified
            else "plancherel-down-up-spectrum-control-failure"
        ),
    )


def _coupling_probability_matrix(
    coupling: CompleteCompressedRacahCoupling,
    partitions: tuple[Partition, ...],
) -> np.ndarray:
    index = {partition: position for position, partition in enumerate(partitions)}
    probability = np.zeros((len(partitions), len(partitions)), dtype=float)
    for entry in coupling.coupling_entries:
        probability[
            index[entry.left_intermediate_partition],
            index[entry.right_intermediate_partition],
        ] = entry.physical_block_probability
    return probability


def audit_racah_fourier_tail(
    n: int,
    boxes_removed: int,
    maximum_support: int,
    *,
    coupling: CompleteCompressedRacahCoupling | None = None,
    tolerance: float = 5e-9,
) -> RacahFourierTailControl:
    if not 2 <= maximum_support < n:
        raise ValueError("require 2<=support<n")
    partitions, basis = plancherel_character_basis_matrix(n)
    order = math.factorial(n)
    q = np.asarray(
        [hook_length_dimension(partition) ** 2 / order for partition in partitions]
    )
    if coupling is None:
        probability = np.diag(q)
        model = "plancherel-identity-coupling"
    else:
        if coupling.n != n:
            raise ValueError("coupling degree mismatch")
        probability = _coupling_probability_matrix(coupling, partitions)
        model = "selected-natural-racah-coupling"
    coefficients = basis.T @ probability @ basis
    identity_index = partitions.index((1,) * n)
    coefficient_energy = coefficients**2
    total = float(np.sum(coefficient_energy) - coefficient_energy[identity_index, identity_index])
    supports = np.asarray([moved_support(cycle) for cycle in partitions], dtype=int)
    retained_mask = np.maximum(supports[:, None], supports[None, :]) <= maximum_support
    retained_mask[identity_index, identity_index] = False
    retained = float(np.sum(coefficient_energy[retained_mask]))
    tail = total - retained
    eigenvalues = np.asarray(
        [down_up_character_eigenvalue(cycle, boxes_removed) for cycle in partitions]
    )
    dirichlet = float(
        np.sum((1.0 - eigenvalues[:, None] * eigenvalues[None, :]) * coefficient_energy)
    )
    first_omitted_fixed_points = n - maximum_support - 1
    cutoff_eigenvalue = falling_factorial(
        first_omitted_fixed_points, boxes_removed
    ) / falling_factorial(n, boxes_removed)
    gap = 1.0 - cutoff_eigenvalue
    upper = dirichlet / gap
    likelihood = probability / (q[:, None] * q[None, :])
    direct_chi_square = float(
        np.sum(q[:, None] * q[None, :] * (likelihood - 1.0) ** 2)
    )
    parseval_residual = abs(total - direct_chi_square)
    slack = upper - tail
    verified = bool(parseval_residual <= tolerance and slack >= -tolerance and gap > 0)
    return RacahFourierTailControl(
        model=model,
        n=n,
        boxes_removed=boxes_removed,
        maximum_retained_moved_support=maximum_support,
        total_nonconstant_fourier_energy=total,
        retained_fourier_energy=retained,
        omitted_fourier_tail_energy=tail,
        product_chain_dirichlet_energy=dirichlet,
        exact_cutoff_spectral_gap=gap,
        dirichlet_tail_upper=upper,
        tail_bound_slack=slack,
        direct_parseval_residual=parseval_residual,
        cutoff_bound_verified=verified,
        status=(
            "branching-dirichlet-controls-fourier-projector-tail"
            if verified
            else "plancherel-down-up-tail-control-failure"
        ),
    )


def down_up_tail_scaling_record(
    n: int,
    maximum_support: int,
) -> DownUpRacahTailScalingRecord:
    if n < 20 or not 2 <= maximum_support < n:
        raise ValueError("scaling controls require n>=20 and 2<=support<n")
    boxes = min(n - 1, math.ceil(n / (maximum_support + 1)))
    beta = falling_factorial(n - maximum_support - 1, boxes) / falling_factorial(n, boxes)
    gap = 1.0 - beta
    exponential_lower = 1.0 - math.exp(-boxes * (maximum_support + 1) / n)
    one_box_gap = (maximum_support + 1) / n
    verified = gap + 1e-15 >= exponential_lower and gap >= 1.0 - math.exp(-1.0)
    return DownUpRacahTailScalingRecord(
        n=n,
        maximum_retained_moved_support=maximum_support,
        boxes_removed=boxes,
        exact_cutoff_spectral_gap=gap,
        exponential_gap_lower=exponential_lower,
        one_box_tail_amplification=1.0 / one_box_gap,
        mesoscopic_tail_amplification=1.0 / gap,
        constant_gap_verified=verified,
        status=(
            "mesoscopic-down-up-chain-has-constant-projector-tail-gap"
            if verified
            else "down-up-tail-scaling-control-failure"
        ),
    )


def run_plancherel_down_up_racah_tail_reduction(
) -> PlancherelDownUpRacahTailReport:
    spectra = [
        audit_plancherel_down_up_spectrum(n, boxes)
        for n in (4, 5, 6, 8)
        for boxes in (1, 2)
    ]
    identity_tails = [
        audit_racah_fourier_tail(n, boxes, support)
        for n in (5, 6, 8)
        for boxes, support in ((1, 2), (2, 3))
    ]
    source = (3, 2, 1)
    coupling = compile_complete_racah_coupling((source,) * 4)
    natural_tails = [
        audit_racah_fourier_tail(6, boxes, support, coupling=coupling)
        for boxes, support in ((1, 2), (2, 3))
    ]
    tails = [*identity_tails, *natural_tails]
    scaling = [
        down_up_tail_scaling_record(n, support)
        for n in (100, 1_000, 10_000)
        for support in (
            max(2, math.ceil(math.log(n) ** 2 / 50)),
            max(3, math.ceil(math.log(n) ** 2 / 25)),
        )
    ]
    failures = sum(not row.exact_down_up_spectrum_verified for row in spectra)
    failures += sum(not row.cutoff_bound_verified for row in tails)
    failures += sum(not row.constant_gap_verified for row in scaling)
    verified = failures == 0
    theorem = PlancherelDownUpRacahTailTheorem(
        character_mode_eigenvalue="J_k phi_C=((n-m(C))_k/(n)_k)phi_C",
        joint_dirichlet_parseval=(
            "D_k(L)=sum_(C,D)(1-beta_k(C)beta_k(D)) hat L(C,D)^2"
        ),
        support_tail_bound=(
            "Tail_s(L)<=D_k(L)/(1-(n-s-1)_k/(n)_k)"
        ),
        mesoscopic_box_choice=(
            "k=ceil(n/(s+1)) gives denominator >=1-e^-1"
        ),
        natural_racah_branching_stability_proved=False,
        entropy_stability_analogue_proved=False,
        status=(
            "racah-projector-tail-reduced-to-mesoscopic-branching-stability"
            if verified
            else "plancherel-down-up-racah-tail-control-failure"
        ),
    )
    return PlancherelDownUpRacahTailReport(
        created_at=utc_now(),
        theorem_contract={
            "chain": "remove k boxes through Plancherel down transitions, then regrow k",
            "stationary_measure": "Plancherel(S_n)",
            "joint_operator": "J_k tensor J_k on the two intermediate labels",
            "tail": "class-pair Fourier modes with max moved support greater than s",
            "target_scale": "s at least logarithmic-squared, k approximately n/s",
            "scope": "L2 projector-tail certificate; no natural stability estimate",
        },
        theorem=theorem,
        spectrum_controls=spectra,
        tail_controls=tails,
        scaling_records=scaling,
        literature_basis=[
            {
                "id": "fulman-stein-plancherel-2003",
                "url": "https://arxiv.org/abs/math/0305423",
                "primary_source": True,
                "use": "Proposition 5.2 gives the exact J_k eigenvalues and normalized character eigenfunctions.",
            }
        ],
        proof_obligations=[
            {
                "obligation": "derive_exact_support_tail_dirichlet_bound",
                "resolved": verified,
                "resolution": "Apply Parseval in the exact J_k tensor J_k eigenbasis and use the minimum tail spectral gap.",
            },
            {
                "obligation": "prove_physical_average_natural_racah_branching_stability",
                "resolved": False,
                "resolution": "Need E_outer D_k(L_o)=n^o(1) or a stronger decaying bound at k approximately n/log^2(n).",
            },
            {
                "obligation": "control_low_support_character_pair_sector",
                "resolved": False,
                "resolution": "Growing-support character sums through at least the log-squared scale remain unbounded.",
            },
            {
                "obligation": "derive_entropy_or_fractional_down_up_stability",
                "resolved": False,
                "resolution": "Needed if rare likelihood spikes make the L2 Dirichlet form factorially large.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The known spectral gap automatically controls the natural Racah tail.",
                "resolved": True,
                "resolution": "Only functions with a proved small Dirichlet form benefit; natural Racah branching stability is open.",
            },
            {
                "objection": "The one-box down-up chain is sufficient.",
                "resolved": True,
                "resolution": "Its tail inequality loses n/(s+1), which is nearly linear at logarithmic-squared support.",
            },
            {
                "objection": "Taking k approximately n/s is a local perturbation.",
                "resolved": True,
                "resolution": "It changes a mesoscopic number of boxes; compatibility of Racah couplings under that branching is the hard theorem.",
            },
            {
                "objection": "L2 stability settles the entropy target in every regime.",
                "resolved": True,
                "resolution": "Rare spikes can keep L2 energy huge while contributing little KL; a fractional or entropy form may be necessary.",
            },
        ],
        headline_metrics={
            "exact_down_up_spectrum_theorem_count": int(verified),
            "exact_fourier_tail_dirichlet_theorem_count": int(verified),
            "finite_spectrum_control_count": len(spectra),
            "finite_tail_control_count": len(tails),
            "finite_control_failure_count": failures,
            "natural_branching_stability_theorem_count": 0,
            "entropy_stability_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "plancherel_down_up_spectrum_verified": verified,
            "projector_tail_dirichlet_reduction_proved": verified,
            "natural_racah_mesoscopic_branching_stability_proved": False,
            "low_support_racah_fourier_sector_controlled": False,
            "natural_racah_collision_subpolynomial_proved": False,
            "natural_racah_mutual_information_sublogarithmic_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The spectral reduction is exact, but both natural branching stability and the growing low-support sector remain open.",
        },
        status=(
            "projector-tail-has-concrete-mesoscopic-branching-falsifier"
            if verified
            else "plancherel-down-up-racah-tail-control-failure"
        ),
        summary=(
            "Converted the uncontrolled character-projector tail into an exact "
            "mesoscopic Young-graph noise-sensitivity obligation."
        ),
        falsifiers_triggered=[
            "Fixed-support moment estimates cannot substitute for a Fourier tail bound.",
            "The one-box spectral gap is too lossy at the required support scale.",
            "Known down-up diagonalization supplies no natural Racah smoothness estimate.",
        ],
    )


def write_plancherel_down_up_racah_tail_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_plancherel_down_up_racah_tail_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_plancherel_down_up_racah_tail_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

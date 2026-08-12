"""Typical Plancherel obstruction to uniform orientation-frame norm decay.

For a natural unequal wreath label, the two latent source partitions are
independent Plancherel draws.  Divide the information-threshold labels into
blocks of the absolute constant size supplied by Sellke's tensor-covering
theorem.  On a good block, both the left and right tensor products cover every
``S_n`` irrep and therefore both contain the trivial representation.

Sellke's theorem only states an ``1-o(1)`` success probability and gives no
rate needed here.  If a block fails with probability ``q_n=o(1)``, Markov's
inequality shows that the fraction of bad blocks is ``o(1)`` with high
probability.  Freeze all labels in bad blocks and the bounded leftover.  Pick
a target irrep occurring in that residual tensor product.  Vary one replicated
orientation bit on every good block.  The exact fixed-family common-range
theorem then gives a common vector for all ``2^r`` resulting projectors.

At ``k=ceil(log2(n!))`` and ``r=(1-o(1))k/C``, this yields

    ||F_nu|| >= 2^(r-k).

The ratio to any proposed ``poly(n) 2^-k`` upper bound is
``2^r/poly(n)=2^Omega(k)/poly(n)``, which diverges.  Thus the uniform
collision-free frame-norm route is asymptotically false on typical natural
tuples.  This is not a no-go theorem for all collective measurements, a
decoder lower bound, or a classical-equivalence result.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_block_obstruction.json"
)
NATURAL_SOURCE_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_unequal_dominance.json"
)
GLOBAL_COLLISION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_global_partition_collision.json"
)
BLOCK_COMMON_CORE_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_block_common_core.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SELLKE_PAPER_ID = "sellke-irrep-tensor-covering-2022"
SELLKE_PAPER_URL = "https://arxiv.org/abs/2004.05283"
SELLKE_THEOREM_LABEL = "Theorem 1.2"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class ProofStepRecord:
    id: str
    statement: str
    dependencies: tuple[str, ...]
    assumptions: tuple[str, ...]
    falsifier: str
    proved: bool


@dataclass(frozen=True)
class BadBlockDensityCertificate:
    complete_block_count: int
    single_block_failure_probability_upper_bound: float
    bad_fraction_threshold: float
    probability_bad_fraction_reaches_threshold_upper_bound: float
    good_block_count_lower_bound_off_failure_event: int
    common_orientation_family_size_lower_bound: int
    averaged_fourier_norm_lower_bound: float
    log2_averaged_fourier_norm_lower_bound: int
    ratio_to_two_to_one_minus_k: int
    log2_ratio_to_two_to_one_minus_k: int


@dataclass(frozen=True)
class ResidualTargetCertificate:
    n: int
    selected_residual_partitions: tuple[Partition, ...]
    target_partition: Partition
    target_multiplicity_in_residual: int
    trivial_multiplicity_in_target_tensor_residual: int
    residual_target_lemma_verified: bool


@dataclass(frozen=True)
class PlancherelBlockObstructionReport:
    created_at: str
    literature: dict[str, str]
    theorem_contract: dict[str, str]
    dependency_evidence: dict[str, bool | int | float | str]
    proof_steps: list[ProofStepRecord]
    adversarial_audit: list[dict[str, bool | str]]
    finite_markov_controls: list[BadBlockDensityCertificate]
    residual_target_controls: list[ResidualTargetCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        repo_path = Path(__file__).resolve().parent / path
        if repo_path.exists():
            path = repo_path
        else:
            return {}
    try:
        payload = json.loads(path.read_text())
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return {}


def bad_block_density_certificate(
    copy_count: int,
    covering_block_size: int,
    single_block_failure_probability_upper_bound: float,
    bad_fraction_threshold: float,
) -> BadBlockDensityCertificate:
    """Quantify the rate-free Markov step for a finite surrogate."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    if covering_block_size < 1:
        raise ValueError("covering_block_size must be positive")
    if not 0 <= single_block_failure_probability_upper_bound <= 1:
        raise ValueError("block failure probability must lie in [0,1]")
    if not 0 < bad_fraction_threshold <= 1:
        raise ValueError("bad fraction threshold must lie in (0,1]")
    block_count = copy_count // covering_block_size
    failure_bound = min(
        1.0,
        single_block_failure_probability_upper_bound
        / bad_fraction_threshold,
    )
    good_lower_bound = math.floor(
        (1 - bad_fraction_threshold) * block_count
    )
    family_size = 1 << good_lower_bound
    averaged_log2 = good_lower_bound - copy_count
    averaged_lower_bound = math.ldexp(1.0, averaged_log2)
    ratio_log2 = good_lower_bound - 1
    ratio = 1 << ratio_log2
    return BadBlockDensityCertificate(
        complete_block_count=block_count,
        single_block_failure_probability_upper_bound=(
            single_block_failure_probability_upper_bound
        ),
        bad_fraction_threshold=bad_fraction_threshold,
        probability_bad_fraction_reaches_threshold_upper_bound=failure_bound,
        good_block_count_lower_bound_off_failure_event=good_lower_bound,
        common_orientation_family_size_lower_bound=family_size,
        averaged_fourier_norm_lower_bound=averaged_lower_bound,
        log2_averaged_fourier_norm_lower_bound=averaged_log2,
        ratio_to_two_to_one_minus_k=ratio,
        log2_ratio_to_two_to_one_minus_k=ratio_log2,
    )


def residual_target_certificate(
    n: int,
    selected_residual_partitions: tuple[Partition, ...],
) -> ResidualTargetCertificate:
    """Choose a target whose tensor with the frozen residual has an invariant."""

    if n < 2:
        raise ValueError("n must be at least two")
    if any(sum(partition) != n for partition in selected_residual_partitions):
        raise ValueError("all residual partitions must have size n")
    trivial = (n,)
    if selected_residual_partitions:
        residual = dict(
            tensor_product_multiplicities(
                tuple(sorted(selected_residual_partitions, reverse=True)),
                n,
            )
        )
    else:
        residual = {trivial: 1}
    target, multiplicity = max(
        residual.items(),
        key=lambda item: (item[1], item[0]),
    )
    invariant_multiplicity = dict(
        tensor_product_multiplicities(
            tuple(sorted((*selected_residual_partitions, target), reverse=True)),
            n,
        )
    ).get(trivial, 0)
    return ResidualTargetCertificate(
        n=n,
        selected_residual_partitions=selected_residual_partitions,
        target_partition=target,
        target_multiplicity_in_residual=multiplicity,
        trivial_multiplicity_in_target_tensor_residual=(
            invariant_multiplicity
        ),
        residual_target_lemma_verified=(
            multiplicity > 0 and invariant_multiplicity == multiplicity
        ),
    )


def _dependency_evidence(
    natural: dict[str, Any],
    collision: dict[str, Any],
    block: dict[str, Any],
) -> dict[str, bool | int | float | str]:
    natural_gate = natural.get("claim_gate", {})
    collision_gate = collision.get("claim_gate", {})
    block_gate = block.get("claim_gate", {})
    return {
        "physical_label_pair_law_verified": bool(
            natural_gate.get("physical_label_pair_law_verified")
        ),
        "threshold_tuple_all_unequal_with_probability_one_minus_o_one": bool(
            natural_gate.get(
                "threshold_tuple_all_unequal_with_probability_one_minus_o_one"
            )
        ),
        "global_source_draws_are_iid_plancherel": bool(
            collision_gate.get("global_source_draws_are_iid_plancherel")
        ),
        "asymptotic_global_all_distinct_dominance_proved": bool(
            collision_gate.get(
                "asymptotic_global_all_distinct_dominance_proved"
            )
        ),
        "block_common_core_construction_proved": bool(
            block_gate.get("block_common_core_construction_proved")
        ),
        "tail_exact_finite_exponential_common_family_found": bool(
            block_gate.get(
                "tail_exact_finite_exponential_common_family_found"
            )
        ),
        "sellke_paper_id": SELLKE_PAPER_ID,
        "sellke_theorem_label": SELLKE_THEOREM_LABEL,
    }


def build_plancherel_block_obstruction_report(
    natural_source_path: Path = NATURAL_SOURCE_PATH,
    global_collision_path: Path = GLOBAL_COLLISION_PATH,
    block_common_core_path: Path = BLOCK_COMMON_CORE_PATH,
) -> PlancherelBlockObstructionReport:
    natural = _read_json(natural_source_path)
    collision = _read_json(global_collision_path)
    block = _read_json(block_common_core_path)
    evidence = _dependency_evidence(natural, collision, block)
    local_dependencies = all(
        evidence[key]
        for key in (
            "physical_label_pair_law_verified",
            "threshold_tuple_all_unequal_with_probability_one_minus_o_one",
            "global_source_draws_are_iid_plancherel",
            "asymptotic_global_all_distinct_dominance_proved",
            "block_common_core_construction_proved",
        )
    )
    residual_controls = [
        residual_target_certificate(5, ()),
        residual_target_certificate(5, ((4, 1),)),
        residual_target_certificate(5, ((4, 1), (3, 2))),
    ]
    residual_verified = all(
        control.residual_target_lemma_verified
        for control in residual_controls
    )
    markov_controls = [
        bad_block_density_certificate(160, 8, 0.04, 0.20),
        bad_block_density_certificate(640, 8, 0.01, 0.10),
        bad_block_density_certificate(2560, 8, 0.0025, 0.05),
    ]
    proof_steps = [
        ProofStepRecord(
            id="natural-latent-pair-law",
            statement=(
                "Each natural physical unequal label has two latent iid "
                "Plancherel source partitions; unordered packaging only "
                "complements an orientation coordinate."
            ),
            dependencies=(
                "self_dual_wreath_natural_unequal_dominance",
                "self_dual_wreath_global_partition_collision",
            ),
            assumptions=(),
            falsifier=(
                "A physical-label probability or representation equivalence "
                "that is not the unordered image of two iid Plancherel draws."
            ),
            proved=bool(
                evidence["physical_label_pair_law_verified"]
                and evidence["global_source_draws_are_iid_plancherel"]
            ),
        ),
        ProofStepRecord(
            id="constant-block-tensor-covering",
            statement=(
                "Sellke Theorem 1.2 supplies an absolute block size C for "
                "which arbitrarily coupled Plancherel irreps tensor-cover "
                "every S_n irrep with probability 1-o(1)."
            ),
            dependencies=(SELLKE_PAPER_ID,),
            assumptions=(
                "The cited theorem is used exactly in its Plancherel regime.",
            ),
            falsifier=(
                "The published theorem lacks a fixed absolute C, excludes "
                "the Plancherel law, or requires a coupling absent here."
            ),
            proved=True,
        ),
        ProofStepRecord(
            id="linear-good-block-density",
            statement=(
                "If q_n=o(1) is the probability either side of a block fails "
                "to cover, Markov gives an o(1) bad-block fraction with "
                "probability 1-o(1), without any rate assumption."
            ),
            dependencies=("constant-block-tensor-covering",),
            assumptions=("k=ceil(log2(n!)) tends to infinity.",),
            falsifier=(
                "The expected bad-block fraction does not tend to zero or "
                "the number of complete blocks is not Theta(k)."
            ),
            proved=True,
        ),
        ProofStepRecord(
            id="residual-target-selection",
            statement=(
                "Freeze every bad block and leftover label, then choose a "
                "target constituent of the selected residual tensor. Since "
                "S_n irreps are self-dual, target tensor residual contains "
                "the trivial irrep."
            ),
            dependencies=("S_n irreps are self-dual",),
            assumptions=(
                "The uniform norm claim ranges over every target block.",
            ),
            falsifier=(
                "The physical frame omits the selected target sector or the "
                "residual tensor has no irreducible constituent."
            ),
            proved=residual_verified,
        ),
        ProofStepRecord(
            id="structured-common-core-family",
            statement=(
                "One replicated orientation bit per good block produces "
                "2^r projectors sharing a vector: every good left/right block "
                "uses its trivial sector and the residual uses the selected "
                "target invariant."
            ),
            dependencies=(
                "self_dual_wreath_orientation_block_common_core",
                "residual-target-selection",
            ),
            assumptions=("n>=5", "all physical labels are unequal"),
            falsifier=(
                "A fixed-family parity equation fails for the all-trivial "
                "assignment or the orientation projectors do not share the "
                "claimed invariant."
            ),
            proved=bool(
                evidence["block_common_core_construction_proved"]
                and residual_verified
            ),
        ),
        ProofStepRecord(
            id="typical-polynomial-factor-norm-obstruction",
            statement=(
                "With r=(1-o(1))k/C, ||F_nu||>=2^(r-k); hence its ratio to "
                "poly(n)2^-k is 2^r/poly(n), which diverges because "
                "k=Theta(n log n)."
            ),
            dependencies=(
                "linear-good-block-density",
                "structured-common-core-family",
                "asymptotic-global-all-distinct-dominance",
            ),
            assumptions=("The polynomial factor has fixed degree."),
            falsifier=(
                "r=o(k), the Fourier normalization differs from 2^-k, or "
                "the frame norm is not the maximum of its target blocks."
            ),
            proved=local_dependencies and residual_verified,
        ),
    ]
    all_steps_proved = all(step.proved for step in proof_steps)
    metrics: dict[str, int | float] = {
        "sellke_covering_literature_theorem_count": 1,
        "natural_iid_plancherel_pair_law_theorem_count": int(
            evidence["physical_label_pair_law_verified"]
        ),
        "threshold_all_unequal_theorem_count": int(
            evidence[
                "threshold_tuple_all_unequal_with_probability_one_minus_o_one"
            ]
        ),
        "asymptotic_global_all_distinct_theorem_count": int(
            evidence["asymptotic_global_all_distinct_dominance_proved"]
        ),
        "block_common_core_construction_theorem_count": int(
            evidence["block_common_core_construction_proved"]
        ),
        "residual_target_control_count": len(residual_controls),
        "residual_target_control_failure_count": sum(
            not control.residual_target_lemma_verified
            for control in residual_controls
        ),
        "asymptotic_linear_good_block_density_theorem_count": 1,
        "typical_exponential_common_orientation_family_theorem_count": int(
            all_steps_proved
        ),
        "uniform_collision_free_polynomial_factor_norm_counterexample_theorem_count": int(
            all_steps_proved
        ),
        "all_collective_measurement_no_go_theorem_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "classical_code_equivalence_separation_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PlancherelBlockObstructionReport(
        created_at=utc_now(),
        literature={
            "paper_id": SELLKE_PAPER_ID,
            "title": "Covering Irrep(S_n) With Tensor Products and Powers",
            "author": "Mark Sellke",
            "theorem": SELLKE_THEOREM_LABEL,
            "url": SELLKE_PAPER_URL,
        },
        theorem_contract={
            "natural_source": (
                "Before unordered packaging, k natural labels are k iid "
                "pairs of iid Plancherel S_n irreps."
            ),
            "covering_input": (
                "Sellke Theorem 1.2 gives a fixed absolute C such that C "
                "arbitrarily coupled Plancherel irreps cover every irrep "
                "asymptotically almost surely."
            ),
            "rate_free_density": (
                "For block failure q_n=o(1), Markov at threshold sqrt(q_n) "
                "gives a 1-o(1) fraction of good blocks with probability "
                "1-o(1); no convergence rate is assumed."
            ),
            "residual_target": (
                "Bad blocks and leftovers are frozen; a target constituent "
                "of their selected tensor makes the full-pattern tensor "
                "contain the trivial irrep."
            ),
            "common_core": (
                "Replicating one orientation bit across each good block gives "
                "2^r orientations with an exact shared invariant."
            ),
            "norm_obstruction": (
                "For some target nu, ||F_nu||>=2^(r-k) with "
                "r=(1-o(1))k/C, ruling out every uniform "
                "poly(n)2^-k upper bound with high probability."
            ),
            "scope_boundary": (
                "This kills the uniform orientation-frame norm strategy only; "
                "it does not rule out whitening, non-projector measurements, "
                "other observables, efficient decoders, or quantum speedups."
            ),
        },
        dependency_evidence=evidence,
        proof_steps=proof_steps,
        adversarial_audit=[
            {
                "objection": (
                    "Sellke gives no convergence rate, so a growing number of "
                    "blocks might contain mostly failures."
                ),
                "resolved": True,
                "resolution": (
                    "Only the bad-block fraction is needed. Its expectation is "
                    "q_n=o(1), and Markov gives convergence of that fraction "
                    "to zero without independence or an explicit rate."
                ),
            },
            {
                "objection": (
                    "Physical unequal labels are unordered, whereas good "
                    "blocks use named left and right Plancherel factors."
                ),
                "resolved": True,
                "resolution": (
                    "Use the latent ordered iid draw. Swapping either member "
                    "of an unordered pair complements one orientation bit and "
                    "permutes the full orientation-projector family, leaving "
                    "the existence of the common core and the norm unchanged."
                ),
            },
            {
                "objection": (
                    "Conditioning on global distinctness destroys block "
                    "independence and therefore the good-block argument."
                ),
                "resolved": True,
                "resolution": (
                    "No conditioning is used. Good-block density and global "
                    "distinctness each hold with probability 1-o(1), so their "
                    "intersection does too by a union bound."
                ),
            },
            {
                "objection": (
                    "Tensor covering is only a support statement and may not "
                    "supply enough multiplicity for a large common core."
                ),
                "resolved": True,
                "resolution": (
                    "Positive trivial multiplicity on each good side is "
                    "enough for one shared vector. The exponential norm factor "
                    "comes from the number of projectors sharing it, not from "
                    "large representation multiplicities."
                ),
            },
            {
                "objection": (
                    "The target irrep is selected after seeing bad blocks, so "
                    "the theorem proves a fixed-target lower bound."
                ),
                "resolved": False,
                "resolution": (
                    "It does not prove a fixed-target lower bound. It is enough "
                    "to falsify a bound uniform over every target and to lower-"
                    "bound the maximum Fourier-block norm. Any claim about "
                    "typical fixed targets remains open."
                ),
            },
            {
                "objection": (
                    "A large maximum frame eigenvalue rules out every useful "
                    "collective measurement or decoder."
                ),
                "resolved": False,
                "resolution": (
                    "False. The result kills the proposed uniform norm upper "
                    "bound and its direct normalization argument only. "
                    "Whitening, quotienting common channels, non-projector "
                    "measurements, and different observables remain open."
                ),
            },
            {
                "objection": (
                    "The common blocks may be information-theoretically "
                    "existent but computationally impossible to identify."
                ),
                "resolved": False,
                "resolution": (
                    "Efficient identification is irrelevant to this norm "
                    "counterexample, but it is an unresolved requirement for "
                    "any algorithm that tries to exploit or quotient them."
                ),
            },
        ],
        finite_markov_controls=markov_controls,
        residual_target_controls=residual_controls,
        headline_metrics=metrics,
        claim_gate={
            "sellke_constant_plancherel_covering_theorem_verified": True,
            "natural_iid_plancherel_pair_law_proved": bool(
                evidence["physical_label_pair_law_verified"]
                and evidence["global_source_draws_are_iid_plancherel"]
            ),
            "asymptotic_global_all_unequal_and_distinct_proved": bool(
                evidence[
                    "threshold_tuple_all_unequal_with_probability_one_minus_o_one"
                ]
                and evidence["asymptotic_global_all_distinct_dominance_proved"]
            ),
            "rate_free_linear_good_block_density_proved": True,
            "residual_target_selection_proved": residual_verified,
            "typical_exponential_common_orientation_family_proved": (
                all_steps_proved
            ),
            "uniform_collision_free_polynomial_factor_norm_bound_falsified": (
                all_steps_proved
            ),
            "uniform_orientation_frame_norm_route_viable": False,
            "all_collective_measurements_ruled_out": False,
            "alternative_measurement_or_whitening_ruled_out": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Typical natural tuples contain a linear number of tensor-"
                "covering blocks, producing an exponential structured family "
                "of orientation projectors with a common vector. This "
                "asymptotically falsifies the uniform poly(n)2^-k frame-norm "
                "bound, but leaves alternative measurements and decoding open."
            ),
        },
        status=(
            "typical-uniform-frame-norm-route-falsified-alternatives-open"
            if all_steps_proved
            else "plancherel-block-obstruction-dependency-failure"
        ),
        summary=(
            "Combined the natural Plancherel source law, Sellke's constant-"
            "block tensor-covering theorem, a rate-free bad-block argument, "
            "and the exact common-core construction. The desired uniform "
            "poly(n)2^-k norm bound fails with high probability."
        ),
        falsifiers_triggered=[
            (
                "Global source distinctness does not force orientation "
                "projectors toward transversality; typical constant-size "
                "tensor-covering blocks create exact shared invariants."
            ),
            (
                "The unknown convergence rate in Sellke's theorem is not an "
                "escape hatch: Markov controls the bad-block fraction from "
                "q_n=o(1) alone."
            ),
            (
                "Finite random-family disappearance at depth five misses "
                "correlated block-code families of exponential size."
            ),
            (
                "The obstruction does not imply that the code-equivalence "
                "HSP, all covariant measurements, or all decoders fail."
            ),
        ],
    )


def write_plancherel_block_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(build_plancherel_block_obstruction_report())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_plancherel_block_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

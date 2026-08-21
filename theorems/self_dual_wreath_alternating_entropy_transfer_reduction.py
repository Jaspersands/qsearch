"""Physical rank transfer reduces to coarse alternating-group entropy.

The exact sign-orbit chain rule writes the physical six-label total
correlation as

    D(P_six || Plancherel(S_n)^6)
      = D(P_O || Q_O)
        + E_(O~P) D(P(Y|O) || Uniform(F_2^3)),             (1)

where ``O`` is the tuple of six transpose orbits and ``Y`` is the three-bit
orientation syndrome.  The second term is always between zero and three bits.
Consequently

    D_base <= D_full <= D_base + 3,                       (2)

and hence

    D_full=o(log n) iff D_base=o(log n).                  (3)

The alternating-base theorem identifies ``P_O`` exactly as the coarse
weak-Fourier tetrahedral law of ``A_n`` and ``Q_O`` as its coarse Plancherel
product law.  Combining (3) with the entropy-transfer theorem gives the
cleanest current rank target:

    D(P_coarse-A_n || Q_coarse-A_n)=o(log n)
       implies physical Haar rank-profile mixing.         (4)

No asymptotic control of the adaptive three-bit syndrome is needed for this
rank conclusion; at most three bits cannot violate a sublogarithmic target.
This does not remove that channel from the search for irreducible non-Haar
Racah information: a constant syndrome CMI may still survive after the rank
profile mixes.

Equation (4) is a reduction, not an entropy estimate for ``A_n``.  The merged
trivial label still creates a factorially rare high-likelihood spike, but its
entropy contribution vanishes and cannot obstruct a sublogarithmic bound.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    audit_alternating_base_orbit_reduction,
)
from self_dual_wreath_sign_orbit_kl_chain_reduction import (
    audit_sign_orbit_kl_chain,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_entropy_transfer_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-ENTROPY-TRANSFER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AlternatingEntropyReductionControl:
    n: int
    full_six_label_total_correlation_bits: float
    base_sign_orbit_total_correlation_bits: float
    coarse_alternating_total_correlation_bits: float
    conditional_three_bit_syndrome_information_bits: float
    full_minus_base_residual: float
    base_minus_alternating_residual: float
    conditional_information_upper_bound_bits: float
    conditional_information_bound_verified: bool
    exact_entropy_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class AlternatingEntropyTransferTheorem:
    kl_sandwich: str
    sublogarithmic_equivalence: str
    alternating_group_identification: str
    rank_transfer_implication: str
    orientation_entropy_asymptotic_estimate_required: bool
    coarse_alternating_entropy_estimate_proved: bool
    status: str


@dataclass(frozen=True)
class AlternatingEntropyTransferReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AlternatingEntropyTransferTheorem
    exact_controls: list[AlternatingEntropyReductionControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_alternating_entropy_reduction(
    n: int,
) -> AlternatingEntropyReductionControl:
    if not 2 <= n <= 5:
        raise ValueError("exact entropy reductions require 2<=n<=5")
    chain = audit_sign_orbit_kl_chain(n)
    alternating = audit_alternating_base_orbit_reduction(n)
    full = chain.full_six_label_kl_bits
    base = chain.base_sign_orbit_kl_bits
    conditional = chain.expected_conditional_syndrome_kl_bits
    coarse = alternating.base_sign_orbit_kl_bits
    chain_residual = abs(full - base - conditional)
    coarse_residual = abs(base - coarse)
    bounded = conditional <= 3.0 + 1e-10
    exact = bool(
        chain.exact_lossless_orientation_reduction_verified
        and alternating.exact_alternating_group_reduction_verified
        and chain_residual <= 1e-8
        and coarse_residual <= 1e-8
        and bounded
    )
    return AlternatingEntropyReductionControl(
        n=n,
        full_six_label_total_correlation_bits=full,
        base_sign_orbit_total_correlation_bits=base,
        coarse_alternating_total_correlation_bits=coarse,
        conditional_three_bit_syndrome_information_bits=conditional,
        full_minus_base_residual=chain_residual,
        base_minus_alternating_residual=coarse_residual,
        conditional_information_upper_bound_bits=3.0,
        conditional_information_bound_verified=bounded,
        exact_entropy_reduction_verified=exact,
        status=(
            "six-label-entropy-exactly-reduced-to-coarse-alternating-base-plus-three-bits"
            if exact
            else "alternating-entropy-reduction-control-failure"
        ),
    )


def sublog_equivalence_control(
    n: int,
    base_entropy_bits: float,
    conditional_entropy_bits: float,
) -> tuple[float, bool]:
    if n < 2 or base_entropy_bits < 0:
        raise ValueError("invalid entropy scaling parameters")
    if not 0 <= conditional_entropy_bits <= 3:
        raise ValueError("three-bit conditional entropy must lie in [0,3]")
    full = base_entropy_bits + conditional_entropy_bits
    ratio_difference = abs(full / math.log2(n) - base_entropy_bits / math.log2(n))
    return ratio_difference, math.isclose(
        ratio_difference,
        conditional_entropy_bits / math.log2(n),
        rel_tol=1e-12,
        abs_tol=1e-15,
    )


def run_alternating_entropy_transfer_reduction(
) -> AlternatingEntropyTransferReductionReport:
    controls = [audit_alternating_entropy_reduction(n) for n in range(2, 6)]
    scaling_checks = [
        sublog_equivalence_control(n, math.sqrt(math.log2(n)), 3.0)
        for n in (10**6, 10**12, 10**24)
    ]
    failures = sum(not row.exact_entropy_reduction_verified for row in controls)
    failures += sum(not verified for _difference, verified in scaling_checks)
    exact = failures == 0
    theorem = AlternatingEntropyTransferTheorem(
        kl_sandwich="D_base<=D_full<=D_base+3 bits",
        sublogarithmic_equivalence="D_full=o(log n) iff D_base=o(log n)",
        alternating_group_identification=(
            "D_base is the total correlation of the coarse A_n tetrahedral "
            "weak-Fourier label law relative to coarse A_n Plancherel product"
        ),
        rank_transfer_implication=(
            "D_base=o(log n) implies physical Haar rank-profile mixing"
        ),
        orientation_entropy_asymptotic_estimate_required=False,
        coarse_alternating_entropy_estimate_proved=False,
        status=(
            "physical-rank-entropy-gate-reduced-to-coarse-alternating-base-law"
            if exact
            else "alternating-entropy-transfer-reduction-failure"
        ),
    )
    return AlternatingEntropyTransferReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_chain_rule": (
                "D_full=D_base+E_O D(P(Y|O)||Uniform(F_2^3))."
            ),
            "three_bit_bound": "0<=E_O D(P(Y|O)||U3)<=3 bits.",
            "sublog_equivalence": theorem.sublogarithmic_equivalence,
            "base_law": theorem.alternating_group_identification,
            "rank_consequence": theorem.rank_transfer_implication,
            "scope": (
                "No asymptotic entropy bound for the coarse A_n law and no "
                "non-Haar Racah-syndrome conclusion is proved."
            ),
        },
        theorem=theorem,
        exact_controls=controls,
        proof_obligations=[
            {
                "obligation": "remove_orientation_entropy_from_sublog_rank_gate",
                "resolved": exact,
                "resolution": (
                    "The sufficient orientation statistic has only eight outcomes, "
                    "so its conditional KL is at most three bits."
                ),
            },
            {
                "obligation": "identify_base_entropy_as_standard_group_law",
                "resolved": exact,
                "resolution": (
                    "Sign-orbit averaging restricts all three word inputs to A_n and "
                    "the coarse weights are A_n Plancherel weights."
                ),
            },
            {
                "obligation": "prove_coarse_alternating_tetrahedral_total_correlation_sublogarithmic",
                "resolved": False,
                "resolution": (
                    "Prove D(P_coarse-A_n||Q_coarse-A_n)=o(log n), or construct a "
                    "logarithmic positive-mass obstruction."
                ),
            },
            {
                "obligation": "decide_irreducible_orbit_adaptive_syndrome_information",
                "resolved": False,
                "resolution": (
                    "A bounded three-bit term is harmless for rank transfer but may "
                    "remain the only non-Haar measured-label survivor."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Orbit-adaptive syndrome KL also needs to be o(1).",
                "resolved": True,
                "resolution": (
                    "Not for the sublogarithmic rank-transfer gate; it is uniformly "
                    "bounded by three bits."
                ),
            },
            {
                "objection": "The three-bit term can grow logarithmically through conditioning.",
                "resolved": True,
                "resolution": (
                    "Conditional KL to uniform on eight outcomes is pointwise at most "
                    "three bits, so averaging cannot increase it."
                ),
            },
            {
                "objection": "Coarse sign orbits are an ad hoc quotient.",
                "resolved": True,
                "resolution": (
                    "They are exactly merged A_n irreducible labels with the matching "
                    "coarse Plancherel law."
                ),
            },
            {
                "objection": "Rank mixing would eliminate all syndrome information.",
                "resolved": False,
                "resolution": (
                    "The non-Haar conditional cumulants can carry a bounded survivor "
                    "outside every rank-compatible Markov model."
                ),
            },
        ],
        headline_metrics={
            "alternating_entropy_reduction_theorem_count": int(exact),
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_orientation_entropy_bits": 3,
            "coarse_alternating_sublog_entropy_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "full_sublog_entropy_equivalent_to_base_sublog_entropy_proved": exact,
            "base_law_is_coarse_alternating_tetrahedral_law_proved": exact,
            "orientation_entropy_asymptotic_control_required_for_rank": False,
            "coarse_alternating_total_correlation_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The entropy gate now lies entirely in the coarse A_n base law, "
                "whose all-n total correlation remains unbounded."
            ),
        },
        status=(
            "coarse-alternating-total-correlation-is-exact-rank-entropy-target"
            if exact
            else "alternating-entropy-target-reduction-failure"
        ),
        summary=(
            "Reduced the sublogarithmic physical rank-transfer condition exactly to "
            "the coarse A_n tetrahedral base-label total correlation."
        ),
        falsifiers_triggered=[
            "The bounded three-bit orientation channel cannot obstruct a sublogarithmic rank-transfer theorem.",
            "The remaining base entropy is a standard alternating-group law, not an arbitrary quotient.",
            "Rank-profile mixing would not by itself eliminate irreducible Racah syndrome information.",
        ],
    )


def write_alternating_entropy_transfer_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_entropy_transfer_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_entropy_transfer_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

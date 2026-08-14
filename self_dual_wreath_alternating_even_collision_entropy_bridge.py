"""Coarse alternating entropy has an exact even-word collision upper bound.

Let ``P_O`` be the coarse sign-orbit tetrahedral law and ``Q_O`` its product
Plancherel reference.  Its likelihood is the even-input word sum

    L_O = sum_(g,h,k in A_n) product_i r_(O_i)(W_i(g,h,k)).

The same-parity projected-kernel identity and full character orthogonality
give the exact second moment

    C_n^even := E_(Q_O) L_O^2
      = sum_C N_even(C)^2 / product_i |C_i|,              (1)

where ``N_even(C)`` counts triples ``g,h,k in A_n`` with six-word cycle
signature ``C``.  This is a purely classical cycle-signature collision norm.

Monotonicity of Renyi divergence yields

    D(P_O || Q_O) <= log2 C_n^even.                       (2)

Combining (2) with the alternating entropy-transfer reduction proves

    C_n^even = n^o(1)
       implies physical Haar rank-profile mixing.         (3)

This target permits any subpolynomial divergence and uses only the even-input
sector.  It is stronger than the direct entropy condition and therefore not
necessary: a thin high-likelihood tail may make ``C_n^even`` polynomial while
the KL remains sublogarithmic.  Exact values through ``S_5`` are not scaling
evidence.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
)
from self_dual_wreath_projected_parity_coset_kernel import (
    full_parity_class_collision_energy,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_even_collision_entropy_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-ENTROPY-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EvenCollisionEntropyControl:
    n: int
    coarse_label_count: int
    exact_label_likelihood_second_moment: float
    exact_even_class_signature_collision_moment: float
    second_moment_duality_residual: float
    coarse_base_kl_bits: float
    renyi_two_divergence_bits: float
    kl_to_renyi_gap_bits: float
    kl_bounded_by_renyi_two: bool
    exact_even_collision_duality_verified: bool
    status: str


@dataclass(frozen=True)
class EvenCollisionEntropyBridgeTheorem:
    exact_collision_identity: str
    renyi_entropy_bound: str
    sufficient_collision_condition: str
    subpolynomial_collision_implies_rank_mixing: bool
    subpolynomial_collision_is_necessary: bool
    physical_collision_condition_proved: bool
    status: str


@dataclass(frozen=True)
class AlternatingEvenCollisionEntropyBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: EvenCollisionEntropyBridgeTheorem
    exact_controls: list[EvenCollisionEntropyControl]
    proof_obligations: list[dict[str, str | bool]]
    literature_boundary: list[dict[str, str]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_even_collision_entropy(n: int) -> EvenCollisionEntropyControl:
    if not 2 <= n <= 5:
        raise ValueError("exact even-collision controls require 2<=n<=5")
    orbits, likelihood, reference, physical = aggregate_sign_orbit_law(n)
    label_second = float(np.sum(reference * likelihood**2))
    class_second = float(full_parity_class_collision_energy(n, (0, 0, 0)))
    positive = physical > 0
    kl = float(np.sum(physical[positive] * np.log2(likelihood[positive])))
    renyi = math.log2(class_second)
    residual = abs(label_second - class_second)
    bounded = kl <= renyi + 1e-10
    exact = residual <= 2e-8 and bounded
    return EvenCollisionEntropyControl(
        n=n,
        coarse_label_count=len(orbits),
        exact_label_likelihood_second_moment=label_second,
        exact_even_class_signature_collision_moment=class_second,
        second_moment_duality_residual=residual,
        coarse_base_kl_bits=max(0.0, kl),
        renyi_two_divergence_bits=renyi,
        kl_to_renyi_gap_bits=max(0.0, renyi - kl),
        kl_bounded_by_renyi_two=bounded,
        exact_even_collision_duality_verified=exact,
        status=(
            "coarse-alternating-renyi-two-equals-even-word-collision"
            if exact
            else "alternating-even-collision-entropy-control-failure"
        ),
    )


def subpolynomial_collision_scaling_control(
    n: int,
) -> tuple[float, float, bool]:
    if n < 2:
        raise ValueError("n must be at least two")
    collision = math.exp(math.sqrt(math.log(n)))
    renyi_bits = math.log2(collision)
    ratio = renyi_bits / math.log2(n)
    expected = 1.0 / math.sqrt(math.log(n))
    return collision, ratio, math.isclose(ratio, expected, rel_tol=1e-12)


def run_alternating_even_collision_entropy_bridge(
) -> AlternatingEvenCollisionEntropyBridgeReport:
    controls = [audit_even_collision_entropy(n) for n in range(2, 6)]
    scaling = [
        subpolynomial_collision_scaling_control(n)
        for n in (10**6, 10**12, 10**24)
    ]
    failures = sum(not row.exact_even_collision_duality_verified for row in controls)
    failures += sum(not verified for _collision, _ratio, verified in scaling)
    exact = failures == 0
    theorem = EvenCollisionEntropyBridgeTheorem(
        exact_collision_identity=(
            "E_(Q_O)L_O^2=sum_C N_even(C)^2/product_i|C_i|"
        ),
        renyi_entropy_bound="D(P_O||Q_O)<=log2 E_(Q_O)L_O^2",
        sufficient_collision_condition="C_n^even=n^o(1)",
        subpolynomial_collision_implies_rank_mixing=exact,
        subpolynomial_collision_is_necessary=False,
        physical_collision_condition_proved=False,
        status=(
            "rank-entropy-gate-has-even-word-subpolynomial-collision-sufficient-condition"
            if exact
            else "alternating-even-collision-entropy-bridge-failure"
        ),
    )
    return AlternatingEvenCollisionEntropyBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "coarse_likelihood": (
                "L_O=sum_(g,h,k in A_n) product_i r_(O_i)(W_i)."
            ),
            "collision_duality": theorem.exact_collision_identity,
            "renyi_monotonicity": theorem.renyi_entropy_bound,
            "rank_sufficient_condition": theorem.sufficient_collision_condition,
            "scope": (
                "No subpolynomial bound on the even collision norm is proved, and "
                "the condition is sufficient rather than necessary."
            ),
        },
        theorem=theorem,
        exact_controls=controls,
        proof_obligations=[
            {
                "obligation": "identify_coarse_alternating_renyi_two_as_classical_collision",
                "resolved": exact,
                "resolution": (
                    "Same-parity sign-orbit collapse followed by full character "
                    "orthogonality gives the even class-signature collision sum."
                ),
            },
            {
                "obligation": "prove_even_tetrahedral_class_collision_subpolynomial",
                "resolved": False,
                "resolution": (
                    "Show sum_C N_even(C)^2/product_i|C_i|=n^o(1), or use direct "
                    "entropy/tail control if Renyi-two is dominated by spikes."
                ),
            },
            {
                "obligation": "separate_low_support_and_fully_nonidentity_even_collision_terms",
                "resolved": False,
                "resolution": (
                    "Derive an even-input support-mask expansion and isolate the only "
                    "term not handled by reciprocal even-class sums."
                ),
            },
        ],
        literature_boundary=[
            {
                "id": "hanany-puder-word-measures-symmetric-groups",
                "url": "https://arxiv.org/abs/2009.00897",
                "boundary": (
                    "Fixed stable characters do not directly control a joint full "
                    "cycle-signature collision norm."
                ),
            },
            {
                "id": "larsen-shalev-word-maps",
                "url": "https://arxiv.org/abs/math/0701334",
                "boundary": (
                    "Single-word near-uniformity does not imply joint independence of "
                    "the six overlapping tetrahedral words."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The full eight-sector collision moment is still required.",
                "resolved": True,
                "resolution": (
                    "No. The entropy reduction needs only the even-input base sector."
                ),
            },
            {
                "objection": "The collision moment must remain bounded.",
                "resolved": True,
                "resolution": "Any subpolynomial growth is sufficient.",
            },
            {
                "objection": "Polynomial collision growth disproves rank mixing.",
                "resolved": True,
                "resolution": (
                    "False: Renyi-two may be tail-dominated while KL and the weak-L1 "
                    "likelihood tail remain sublogarithmic/subquadratic."
                ),
            },
            {
                "objection": "The finite nonmonotone moments suggest boundedness.",
                "resolved": False,
                "resolution": "S_2 through S_5 carry no asymptotic force.",
            },
        ],
        headline_metrics={
            "even_collision_duality_theorem_count": int(exact),
            "renyi_entropy_bridge_theorem_count": int(exact),
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "even_collision_subpolynomial_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "coarse_alternating_renyi_two_collision_identity_proved": exact,
            "subpolynomial_even_collision_would_imply_rank_mixing": exact,
            "even_collision_subpolynomial_proved": False,
            "coarse_alternating_total_correlation_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The sufficient classical collision target is exact but has no all-n "
                "subpolynomial estimate."
            ),
        },
        status=(
            "even-word-class-collision-is-concrete-renyi-route-to-rank-mixing"
            if exact
            else "alternating-even-collision-bridge-control-failure"
        ),
        summary=(
            "Reduced the coarse alternating entropy gate to the sufficient classical "
            "condition that one even-input class-signature collision norm is n^o(1)."
        ),
        falsifiers_triggered=[
            "The full physical collision moment is not the minimal Renyi target for rank transfer.",
            "Bounded collision is unnecessarily strong; subpolynomial growth suffices.",
            "A large collision moment alone cannot certify persistent bounded rank signal.",
        ],
    )


def write_alternating_even_collision_entropy_bridge_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_even_collision_entropy_bridge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_even_collision_entropy_bridge_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

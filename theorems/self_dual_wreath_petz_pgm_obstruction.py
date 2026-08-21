"""Generic Petz/PGM implementation obstruction and the covariance escape hatch.

Gilyen, Lloyd, Marvian, Quek, and Wilde implement the pretty-good instrument
as a Petz recovery channel.  Their generic complexity contains a prefactor

    sqrt(d_E * kappa_(N(sigma))),

where ``d_E`` is at least the Kraus rank of the forward channel.  For an
``N``-hypothesis PGM, the standard reduction uses

    sigma_XB = N^-1 sum_s |s><s| tensor rho_s,
    N_(XB->B) = Tr_X.

The Stinespring environment stores ``X``, hence ``d_E=N``.  The paper's
complementary-state-rank variant also sees rank ``N`` because the uniform
classical hypothesis marginal has full support.  With ``N=n!``, the generic
Petz implementation therefore carries a ``sqrt(n!)`` dimension charge before
any condition-number cost.

This is a baseline obstruction, not a lower bound for the structured wreath
ensemble.  The label ``s`` occupies only ``O(n log n)`` qubits, and the
separate covariant-factorization theorem uses a Beals Fourier transform to
cancel the explicit ``sqrt(n!)`` normalization algebraically.  The surviving
algorithmic target is a polynomial implementation of that factorization's
controlled multiplicity inverse, not the generic Petz circuit.

Primary source:
https://doi.org/10.1103/PhysRevLett.128.220502
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_petz_pgm_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PETZ_PGM_PAPER_URL = "https://doi.org/10.1103/PhysRevLett.128.220502"


@dataclass(frozen=True)
class PetzPgmObstructionRecord:
    n: int
    hidden_hypothesis_count_decimal: str
    hidden_label_qubit_count: int
    generic_environment_dimension_decimal: str
    complementary_state_rank_decimal: str
    log2_generic_environment_sqrt_charge: float
    generic_environment_charge_superpolynomial: bool
    condition_number_charge_included: bool
    efficient_symmetric_group_qft_available: bool
    algebraic_covariance_compressed_factorization_proved: bool
    polynomial_covariance_compressed_stinespring_circuit_proved: bool
    structured_multiplicity_whitening_proved: bool
    status: str


@dataclass(frozen=True)
class PetzPgmObstructionReport:
    created_at: str
    reduction_contract: dict[str, Any]
    literature_theorem: dict[str, Any]
    scaling_records: list[PetzPgmObstructionRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def petz_pgm_obstruction_record(n: int) -> PetzPgmObstructionRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    hypotheses = math.factorial(n)
    log_hypotheses = math.lgamma(n + 1) / math.log(2)
    return PetzPgmObstructionRecord(
        n=n,
        hidden_hypothesis_count_decimal=str(hypotheses),
        hidden_label_qubit_count=math.ceil(log_hypotheses),
        generic_environment_dimension_decimal=str(hypotheses),
        complementary_state_rank_decimal=str(hypotheses),
        log2_generic_environment_sqrt_charge=log_hypotheses / 2,
        generic_environment_charge_superpolynomial=(
            log_hypotheses / 2 > math.log2(n) ** 2
        ),
        condition_number_charge_included=False,
        efficient_symmetric_group_qft_available=True,
        algebraic_covariance_compressed_factorization_proved=True,
        polynomial_covariance_compressed_stinespring_circuit_proved=False,
        structured_multiplicity_whitening_proved=False,
        status="generic-petz-factorial-dimension-charge-covariant-factorization-open",
    )


def run_petz_pgm_obstruction() -> PetzPgmObstructionReport:
    records = [
        petz_pgm_obstruction_record(n)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 64, 128, 256, 512)
    ]
    separated = [row for row in records if row.generic_environment_charge_superpolynomial]
    return PetzPgmObstructionReport(
        created_at=utc_now(),
        reduction_contract={
            "ensemble_state": (
                "sigma_XB=N^-1 sum_s |s><s| tensor rho_s."
            ),
            "forward_channel": "N_(XB->B)=Tr_X.",
            "pgm_as_petz": (
                "The Petz recovery channel outputs the PGM label X and a quantum "
                "post-measurement register."
            ),
            "environment_dimension": (
                "The standard Stinespring extension of Tr_X stores X, so d_E=N."
            ),
            "complementary_rank": (
                "For uniform hypotheses, the complementary classical X marginal "
                "has rank N; replacing d_E by complementary rank does not help."
            ),
            "wreath_specialization": "N=n! hidden bridge permutations.",
        },
        literature_theorem={
            "paper_id": "gilyen-lloyd-marvian-quek-wilde-petz-pgm-2022",
            "title": "Quantum Algorithm for Petz Recovery Channels and Pretty Good Measurements",
            "url": PETZ_PGM_PAPER_URL,
            "statement_used": (
                "The generic Petz implementation complexity has prefactor "
                "sqrt(d_E kappa_(N(sigma))); d_E is no smaller than channel "
                "Kraus rank, with a complementary-state-rank variant."
            ),
            "specific_wreath_lower_bound_claimed": False,
            "external_theorem_not_reproved_here": True,
        },
        scaling_records=records,
        proof_obligations=[
            {
                "obligation": "generic_pgm_to_petz_mapping",
                "resolved": True,
                "resolution": (
                    "The cq ensemble and partial-trace channel are exactly the PGM "
                    "specialization in the primary paper."
                ),
            },
            {
                "obligation": "wreath_environment_dimension_charge",
                "resolved": True,
                "resolution": (
                    "The hypothesis register has dimension and full uniform rank n!, "
                    "giving a sqrt(n!) generic prefactor before conditioning costs."
                ),
            },
            {
                "obligation": "specific_covariant_lower_bound",
                "resolved": False,
                "resolution": (
                    "The paper's oracle lower bound is generic and does not rule out "
                    "a representation-specific S_n-covariant implementation."
                ),
            },
            {
                "obligation": "algebraic_covariance_compressed_factorization",
                "resolved": True,
                "resolution": (
                    "The separate Fourier-factorization theorem cancels the explicit "
                    "sqrt(n!) environment normalization exactly."
                ),
            },
            {
                "obligation": "polynomial_covariance_compressed_stinespring_circuit",
                "resolved": False,
                "resolution": (
                    "The algebraic factorization still requires coherent controlled "
                    "multiplicity inverse square roots D_nu^-1/2."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The label needs n! qubits.",
                "resolved": True,
                "resolution": (
                    "False: a permutation label needs ceil(log2 n!)=O(n log n) qubits. "
                    "The obstruction is generic amplitude normalization, not storage."
                ),
            },
            {
                "objection": "The Petz theorem proves this structured PGM is hard.",
                "resolved": False,
                "resolution": (
                    "It does not. Its lower bound concerns generally applicable oracle "
                    "implementations; group covariance could evade the generic d_E charge."
                ),
            },
            {
                "objection": "Improving the inverse-square-root polynomial is enough.",
                "resolved": True,
                "resolution": (
                    "Even ideal conditioning leaves the generic sqrt(d_E)=sqrt(n!) "
                    "environment factor in this reduction."
                ),
            },
            {
                "objection": "A group QFT automatically removes the environment cost.",
                "resolved": False,
                "resolution": (
                    "The QFT handles label basis changes but does not construct the "
                    "mixed multiplicity tight frame or its coherent whitening."
                ),
            },
        ],
        headline_metrics={
            "generic_pgm_to_petz_reduction_count": 1,
            "generic_environment_dimension_obstruction_count": 1,
            "complementary_rank_bypass_failure_count": 1,
            "scaling_record_count": len(records),
            "superpolynomial_generic_charge_record_count": len(separated),
            "maximum_n": records[-1].n,
            "maximum_log2_generic_environment_sqrt_charge": (
                records[-1].log2_generic_environment_sqrt_charge
            ),
            "algebraic_covariance_compressed_factorization_count": 1,
            "polynomial_covariance_compressed_stinespring_circuit_count": 0,
            "structured_multiplicity_whitening_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "generic_petz_pgm_baseline_mapped": True,
            "generic_petz_implementation_is_polynomial_for_wreath_ensemble": False,
            "generic_complementary_rank_variant_removes_factorial_charge": False,
            "specific_covariant_pgm_lower_bound_proved": False,
            "algebraic_covariance_compressed_factorization_proved": True,
            "polynomial_covariance_compressed_stinespring_circuit_proved": False,
            "structured_multiplicity_whitening_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The general Petz/PGM algorithm pays sqrt(n!) through its label "
                "environment even before condition number. The symmetry-specific "
                "factorization now cancels that explicit charge algebraically, but its "
                "multiplicity inverse has no polynomial implementation."
            ),
        },
        status="generic-petz-baseline-evaded-algebraically-multiplicity-circuit-open",
        summary=(
            "Mapped the standard PGM-to-Petz implementation to the wreath ensemble "
            "and isolated its independent sqrt(n!) environment-dimension charge."
        ),
        falsifiers_triggered=[
            (
                "A generic Petz implementation does not turn constant PGM success "
                "into a polynomial algorithm for n! hypotheses."
            ),
            (
                "The factorial charge is not caused by label storage: it arises from "
                "generic Stinespring normalization/amplification."
            ),
            (
                "The primary theorem leaves group-covariant factorization open, so it "
                "cannot be cited as a structured impossibility result."
            ),
        ],
    )


def write_petz_pgm_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_petz_pgm_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_petz_pgm_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

"""Primary-source theorem contracts for natural-problem reductions.

A citation label is not enough to compose reductions.  Each record below states
the exact source variant, target solver interface, parameter regime, success
condition, and limitations that downstream candidate-specific edges must
preserve.  The catalog is intentionally small: unsupported folklore is proof
debt, not an accepted edge.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now


THEOREM_CATALOG_PATH = Path("research/reductions/theorem_contracts.json")


@dataclass(frozen=True)
class ReductionTheoremContract:
    id: str
    title: str
    literature_id: str
    primary_url: str
    theorem_locator: str
    provenance_status: str
    source_problem: str
    source_promise: str
    target_problem: str
    target_group_or_domain: str
    target_instances_supplied: str
    target_access_supplied: list[str]
    target_solver_contract: str
    source_solution_recovered: str
    parameter_map: str
    reduction_resources: str
    success_requirement: str
    uniformity_and_advice: str
    quantifier_scope: str
    limitations: list[str]


REQUIRED_TEXT_FIELDS = (
    "title",
    "literature_id",
    "primary_url",
    "theorem_locator",
    "provenance_status",
    "source_problem",
    "source_promise",
    "target_problem",
    "target_group_or_domain",
    "target_instances_supplied",
    "target_solver_contract",
    "source_solution_recovered",
    "parameter_map",
    "reduction_resources",
    "success_requirement",
    "uniformity_and_advice",
    "quantifier_scope",
)


def seed_theorem_contracts() -> list[ReductionTheoremContract]:
    return [
        ReductionTheoremContract(
            id="THM-REGEV-USVP-TO-DCP-2003",
            title="Approximate unique-SVP from dihedral coset sampling",
            literature_id="regev-lattice-dhsp-2003",
            primary_url="https://arxiv.org/abs/cs/0304005",
            theorem_locator=(
                "arXiv source quantum_average.tex: theorem_svp near line 125; formal DCP definition near line 255; "
                "n_dimensional_2pp near line 285; improved_main_lattice_lemma near line 602"
            ),
            provenance_status="primary-source-latex-theorem-and-definition-verified",
            source_problem="theta-n-2.5-unique-svp",
            source_promise=(
                "The f=1 specialization of the paper's theorem: an n-dimensional lattice with a "
                "Theta(n^(1/2+2f))=Theta(n^2.5) unique-shortest-vector gap."
            ),
            target_problem="dihedral-coset-problem",
            target_group_or_domain="Dihedral groups D_N with log N polynomially related to the lattice input size.",
            target_instances_supplied=(
                "poly(log N) tensor-product registers with a common hidden slope d. Each register is a valid dihedral "
                "coset state with probability at least 1-1/(log N)^f and otherwise may be an arbitrary basis state |b,x|."
            ),
            target_access_supplied=[
                "independent-coset-state-samples",
                "quantum-state-input",
                "adversarial-bad-registers-at-rate-1-over-logN-to-f",
            ],
            target_solver_contract=(
                "For f=1, output the common hidden slope d with probability poly(1/log N) in time poly(log N), despite "
                "per-register bad probability at most 1/log N. A perfect-state or restricted-family solver is insufficient."
            ),
            source_solution_recovered="A vector satisfying the paper's unique-SVP approximation promise.",
            parameter_map=(
                "In the improved proof choose prime p>n^(2+2f), M=2^(4n), and map the n-dimensional two-point instance "
                "to DCP modulus N=(2M)^n, hence log N=Theta(n^2). The f=1 approximation factor is Theta(n^2.5); "
                "the DCP input uses poly(log N) registers."
            ),
            reduction_resources="Quantum polynomial-time reduction with polynomially many target coset samples.",
            success_requirement=(
                "Output d with probability poly(1/log N) and time poly(log N) under the DCP failure-parameter promise; "
                "the lattice routine then succeeds with inverse-polynomial probability and polynomial repetition."
            ),
            uniformity_and_advice="Uniform construction from the lattice instance; no family-specific nonuniform advice.",
            quantifier_scope="Worst-case promised lattice instances in the stated approximation regime.",
            limitations=[
                "This is not a reduction from exact SVP or arbitrary approximation factors.",
                "It supplies coset-state samples, not automatically a public reversible evaluator for a phase family.",
                "The f=1 theorem permits arbitrary bad basis-state registers at probability up to 1/log N; a perfect-state sieve does not cover the theorem input.",
                "Hardness does not transfer to a restricted easy dihedral or hidden-shift subfamily without another reduction.",
            ],
        ),
        ReductionTheoremContract(
            id="CONSTRUCTION-GI-TO-HIDDEN-INVOLUTION-HSP",
            title="Graph isomorphism as a hidden-involution subgroup problem",
            literature_id="symmetric-defies-fourier-2005",
            primary_url="https://arxiv.org/abs/quant-ph/0501056",
            theorem_locator="Graph-isomorphism-relevant hidden subgroup construction discussed in the paper",
            provenance_status="primary-source-described-standard-reduction",
            source_problem="graph-isomorphism-search",
            source_promise="Two explicitly represented n-vertex graphs, with search output required on isomorphic inputs.",
            target_problem="graph-isomorphism-hidden-involution-hsp",
            target_group_or_domain="The graph-isomorphism wreath-product/embedded symmetric-group construction.",
            target_instances_supplied=(
                "A coherently evaluable hiding function whose hidden subgroup encodes an isomorphism as an involution."
            ),
            target_access_supplied=["coherent-hiding-function-evaluation", "coset-state-preparation"],
            target_solver_contract=(
                "Recover enough of the hidden subgroup on every encoded graph pair to output and verify an isomorphism."
            ),
            source_solution_recovered="A vertex permutation mapping one input graph to the other.",
            parameter_map="The target permutation degree and oracle evaluation cost are polynomial in graph size.",
            reduction_resources="Uniform polynomial-time classical/quantum oracle construction and classical verification.",
            success_requirement="Bounded-error recovery on the full encoded graph-isomorphism promise.",
            uniformity_and_advice="Uniformly constructed from the two input graphs with no graph-family advice.",
            quantifier_scope="All explicitly represented graph pairs, not only CFI, regular, or cospectral subfamilies.",
            limitations=[
                "Strong Fourier sampling is insufficient on the relevant hidden subgroups.",
                "Solving a restricted graph family does not solve general graph isomorphism.",
                "A separating observable must be implementable and decoded, not merely information-theoretically existent.",
            ],
        ),
        ReductionTheoremContract(
            id="CONSTRUCTION-CODE-EQUIVALENCE-TO-NONABELIAN-HSP",
            title="Search code equivalence as a nonabelian hidden subgroup problem",
            literature_id="code-equivalence-fourier-2011",
            primary_url="https://arxiv.org/abs/1111.4382",
            theorem_locator="Introduction and the search code-equivalence hidden-subgroup formulation",
            provenance_status="primary-source-construction",
            source_problem="linear-code-equivalence-search",
            source_promise=(
                "Two full-rank generator matrices M and M' for equivalent q-ary linear codes, with M'=SMP."
            ),
            target_problem="code-equivalence-nonabelian-hsp",
            target_group_or_domain=(
                "The row-operation and coordinate-permutation group action, converted to its standard hidden-subgroup form."
            ),
            target_instances_supplied=(
                "A coherently evaluable group-action hiding function derived from both generator matrices."
            ),
            target_access_supplied=["coherent-hiding-function-evaluation", "coset-state-preparation"],
            target_solver_contract=(
                "Recover the hidden subgroup/action element sufficiently to output the coordinate permutation P."
            ),
            source_solution_recovered="A permutation P, and then S by polynomial-time linear algebra.",
            parameter_map="Group representation and oracle evaluation are polynomial in n, k, and log q.",
            reduction_resources="Uniform polynomial-time group-action oracle construction plus linear-algebraic decoding.",
            success_requirement="Bounded-error recovery on every promised equivalent code pair in the claimed scope.",
            uniformity_and_advice="Uniform construction from M and M'; no private code-family advice.",
            quantifier_scope="The stated search code-equivalence problem, not only a selected algebraic code family.",
            limitations=[
                "Many structured families are classically resolved by support splitting or stronger invariants.",
                "Hardness of measuring a coset state is not evidence that the underlying code family is classically hard.",
                "A solver for a restricted code family does not establish a route from general code equivalence.",
            ],
        ),
    ]


def validate_theorem_contract(contract: ReductionTheoremContract) -> list[str]:
    issues: list[str] = []
    for field in REQUIRED_TEXT_FIELDS:
        if len(str(getattr(contract, field)).strip()) < 12:
            issues.append(f"{field}: missing or too vague")
    if not contract.primary_url.startswith("https://arxiv.org/"):
        issues.append("primary_url: expected a primary arXiv record")
    if not contract.target_access_supplied:
        issues.append("target_access_supplied: at least one explicit access capability is required")
    if not contract.limitations:
        issues.append("limitations: at least one non-transfer limitation is required")
    return issues


def theorem_contract_index() -> dict[str, ReductionTheoremContract]:
    contracts = seed_theorem_contracts()
    ids = [contract.id for contract in contracts]
    if len(ids) != len(set(ids)):
        raise ValueError("reduction theorem contract IDs must be unique")
    invalid = {contract.id: validate_theorem_contract(contract) for contract in contracts}
    invalid = {key: value for key, value in invalid.items() if value}
    if invalid:
        raise ValueError(f"invalid theorem contracts: {invalid}")
    return {contract.id: contract for contract in contracts}


def build_theorem_catalog() -> dict[str, Any]:
    contracts = list(theorem_contract_index().values())
    return {
        "created_at": utc_now(),
        "kind": "primary-source-reduction-theorem-contract-catalog",
        "contract_count": len(contracts),
        "status": "contracts-validated",
        "contracts": [asdict(contract) for contract in contracts],
        "interpretation": (
            "These contracts certify only the listed upstream reductions. Candidate-specific family and access-model "
            "bridges remain separate proof obligations."
        ),
    }


def write_theorem_catalog(output_path: Path = THEOREM_CATALOG_PATH) -> dict[str, Any]:
    payload = build_theorem_catalog()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload

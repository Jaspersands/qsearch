"""Replay exact classical witnesses, comparison controls and source hashes."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform

import flint

from finite_controls import annihilator_control, curve_control
from schur_gate import FullSupportProblem, rows


ROOT = Path(__file__).resolve().parent
FROZEN = {
    ROOT.parent / "inverse-trace-local-list-2026-10-26/receipt.json":
        "c75052e06a71e2afde22c776c7711d114b0cea8f964327d29f09beeb494556bb",
    ROOT.parent / "inverse-trace-modular-norm-2026-10-25/receipt.json":
        "ca9170b9b06fc50c7454080837841cfb6681e71b6cc0430df889c654186c9fab",
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def report():
    for path, expected in FROZEN.items():
        if digest(path) != expected:
            raise ValueError(f"unrelated frozen receipt changed: {path}")
    finite = []
    for genus in (1, 2, 3):
        problem, metadata = curve_control(genus)
        syndrome = tuple(range(1, problem.k+1))
        result = problem.deterministic_attempt(syndrome, 2)
        exhaustive = annihilator_control(problem)
        if (result["witness"] is None or exhaustive["rank_failures"] != 1
                or exhaustive["nonzero_rank_failures"] != 0):
            raise ArithmeticError("AG control contradicts the claimed classical completion")
        union = Fraction(problem.p**problem.k-1,
                         (problem.p-1)*exhaustive["annihilators_enumerated"])
        exact = problem.exact_bounds() if problem.p**problem.k <= 4096 else None
        if exact is not None and exact["classical_failure_bound"] != union:
            raise ArithmeticError("AG union-bound formula failed exact enumeration")
        finite.append(dict(metadata, original_parity=rows(problem.B), syndrome=syndrome,
                           supplied_verified_nonsquare=2, result=result,
                           comparison=problem.dominance(), exhaustive_control=exhaustive,
                           quantum_expression_floor=problem.quantum_bound_floor(),
                           actual_uniform_annihilator_failure=Fraction(
                               1, exhaustive["annihilators_enumerated"]),
                           classical_union_bound_from_geometric_proof=union,
                           exact_codeword_enumeration=exact))
    rs = FullSupportProblem(11, [[1]*10, list(range(10))], relation="full_support")
    rs_exact = rs.exact_bounds()
    if not rs_exact["quantum_failure_expression"] < 1:
        raise ArithmeticError("nonvacuous quantum-bound comparison control lost")
    control = {"comparison": rs.dominance(), "exact_bounds": rs_exact,
               "quantum_expression_floor": rs.quantum_bound_floor(),
               "original_parity": rows(rs.B), "syndrome": [3, 7],
               "result": rs.deterministic_attempt((3, 7), 2)}
    sources = [ROOT / name for name in ("schur_gate.py", "finite_controls.py",
               "test_schur_gate.py", "verify_schur_gate.py", "SCHUR_AG_CLASSICAL.md",
               "HANDOFF.md")]
    sources.extend(FROZEN)
    return jsonable({
        "status": "STANDARD_HIGH_DEGREE_AG_EXTENSION_CLASSICALLY_COVERED",
        "proof_status": "WRITTEN_DEDUCTION_WITH_EXACT_CONTROLS_NOT_INDEPENDENTLY_REVIEWED",
        "scope": {"relation": "By=s and every y_i nonzero",
                  "standard_ag_degrees": "2g+1 <= degree(G) < m",
                  "quantum_criterion": "Ragavan-Shutty 2610.00502v1 Theorem 5.4, Q<1",
                  "algorithm_is_prior_art": True,
                  "universal_quantum_lower_bound": False,
                  "native_inverse_trace_dequantized": False,
                  "quantum_advantage_established": False, "quantum_execution": False,
                  "uniform_witness_sampling": False, "independent_review": False,
                  "repository_registry_admission": False},
        "ag_finite_controls": finite,
        "reed_solomon_nonvacuous_comparison_control": control,
        "primary_sources": ["https://arxiv.org/html/2610.00502v1#S5.SS3",
                            "https://arxiv.org/html/2610.00502v1#S6.SS2",
                            "https://arxiv.org/html/1401.6025v3#S2.SS2"],
        "runtime": {"python": platform.python_version(), "python_flint": flint.__version__},
        "sha256": {str(path.relative_to(ROOT.parent)): digest(path) for path in sources},
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    destination = ROOT / "receipt.json"
    if args.check:
        if json.loads(destination.read_text()) != data:
            raise SystemExit("FAIL: receipt differs from exact replay")
        print(f"PASS: exact replay; {len(data['sha256'])} hashes; SHA256 {digest(destination)}")
    elif args.write:
        destination.write_text(json.dumps(data, indent=2)+"\n")
        print(f"Wrote {destination}; SHA256 {digest(destination)}")
    else:
        print(json.dumps(data, indent=2))

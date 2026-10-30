"""Recompile scoped Rees proofs and inspect every declared axiom dependency."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
LAKE = str(Path.home()/".elan/bin/lake")
MATHLIB = "56a005855ea17e0b0958f73ec801ae140b0a1679"
ORIGINAL = "ded56af5166e119d7dbc912c01e365b63d6d7dcba102a1de84f07b1cd509ffed"
PREFIX = "QSearch.ReesHomogenization."
CORE_THEOREMS = tuple(PREFIX+name for name in (
    "applyRows_mul", "applyRows_one", "evaluationMatrix_apply", "evaluation_det_ne_zero",
    "rows_mem", "coefficientwise_iff", "dilation_membership_iff", "zero_dilation_erases",
    "tuple_hides", "coefficient_translate", "coefficient_allowed", "intersection_card_pos",
    "coefficient_outside", "coefficient_forbidden", "zero_evaluation_loses_coefficient",
    "repeated_evaluation_loses_coefficient"))
LIE_PREFIX = "QSearch.ReesLie."
LIE_THEOREMS = tuple(LIE_PREFIX+name for name in (
    "lowerCentral_bracket", "monomial_bracket", "evaluate_eq_rows", "evaluate_single",
    "monomial_mem", "evaluate_eq_sum", "evaluationSpace_bracket", "cover_nilpotent", "evaluate_injective",
    "recover_evaluate", "recover_mem", "evaluate_recover", "cover_membership_iff",
    "recover_gradeOne", "gradeOne_membership_iff"))
LIE_DEFINITIONS = tuple(LIE_PREFIX+name for name in (
    "evaluationLieRing", "evaluationLieAlgebra", "monomial", "coefficientSpace",
    "evaluate", "evaluationSpace", "cover", "evaluationHom", "recover", "gradeOne"))
DILATION_PREFIX = "QSearch.ReesDilation."
DILATION_THEOREMS = tuple(DILATION_PREFIX+name for name in (
    "dilation_evaluate", "scale_single", "dilation_monomial", "dilation_mem", "dilation_lie",
    "recover_dilation", "dilation_mul", "dilation_one", "dilation_hidden_membership_iff",
    "dilation_zero", "highest_monomial_central", "dilation_highest_grade", "uniform_scaling_obstruction"))
DILATION_DEFINITIONS = tuple(DILATION_PREFIX+name for name in (
    "recoverLinear", "scaleCoefficients", "dilationLinear", "dilationHom", "dilationEquiv"))
CENTRAL_PREFIX = "QSearch.ReesCentralInstrument."
CENTRAL_THEOREMS = tuple(CENTRAL_PREFIX+name for name in (
    "character_star", "character_pair_sum", "fourier_gram", "central_source_shift",
    "measurement_eq_projected", "projected_coefficient", "projected_correlation",
    "intersectionSize_ne_zero", "allowed_branch_mass", "normalized_correlation",
    "normalized_trace", "normalized_at", "normalized_outside", "branch_factorization",
    "forbidden_zero", "complete_branches", "complete_mass", "measurement_complete",
    "controlledDiscard_eq", "tensor_correlation", "supported_product", "descent_with_reference",
    "scaled_source", "zero_actions_identity", "all_record_factorization", "complete_instrument",
    "central_record_descent", "forbidden_record_zero", "packet_mass_complete",
    "central_cq_record", "central_instrument"))
CENTRAL_DEFINITIONS = tuple(CENTRAL_PREFIX+name for name in (
    "sourceEntry", "projectedEntry", "measuredEntry", "correlation", "intersectionSize",
    "normalizedEntry", "spectralAction", "controlledDiscard", "CancellationCertificate"))
THEOREMS = CORE_THEOREMS + LIE_THEOREMS + DILATION_THEOREMS + CENTRAL_THEOREMS
DECLARATIONS = THEOREMS + LIE_DEFINITIONS + DILATION_DEFINITIONS + CENTRAL_DEFINITIONS
FOUNDATIONS = {"propext", "Classical.choice", "Quot.sound"}


def parse_axioms(output, expected=DECLARATIONS):
    records = {}
    for line in output.splitlines():
        if not line.strip():
            continue
        message = json.loads(line)
        if message.get("severity") != "information":
            raise ValueError("Lean audit emitted an error or warning")
        data = message["data"].strip()
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[([^]]*)\]", data, re.DOTALL)
        empty = re.fullmatch(r"'([^']+)' does not depend on any axioms", data)
        if match:
            name = match[1]
            axioms = [x.strip() for x in match[2].split(",") if x.strip()]
        elif empty:
            name, axioms = empty[1], []
        else:
            raise ValueError("unexpected axiom diagnostic")
        if name not in expected or name in records or not set(axioms) <= FOUNDATIONS:
            raise ValueError("unexpected/duplicate declaration or unapproved axiom")
        records[name] = axioms
    if set(records) != set(expected):
        raise ValueError("incomplete axiom audit")
    return records


def command(args, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {args}\n{result.stdout}{result.stderr}")
    if result.stderr.strip():
        raise RuntimeError(f"unexpected stderr: {result.stderr}")
    return result.stdout


def lean(*args):
    # The path dependency's published cache lands in the root build folder.
    # Put that complete cache before a partial dependency-local build tree.
    return command([LAKE, "env", "/bin/sh", "-c",
                    'exec env LEAN_PATH="$PWD/.lake/build/lib/lean:$LEAN_PATH" lean "$@"',
                    "lean", *args])


def verify():
    if command(["git", "rev-parse", "HEAD"], ROOT/"mathlib").strip() != MATHLIB:
        raise ValueError("wrong mathlib revision")
    if command(["git", "status", "--porcelain"], ROOT/"mathlib").strip():
        raise ValueError("mathlib source checkout is modified")
    if hashlib.sha256((ROOT/"source/ReesHomogenization.lean").read_bytes()).hexdigest() != ORIGINAL:
        raise ValueError("original draft snapshot changed")
    expected_audit = "import ReesDilation\nimport ReesCentralInstrument\n\n"+"".join(f"#print axioms {x}\n" for x in DECLARATIONS)
    if (ROOT/"Audit.lean").read_text() != expected_audit:
        raise ValueError("audit commands differ from the declared proof/definition set")
    (ROOT/".lake/build/lib/lean").mkdir(parents=True, exist_ok=True)
    for module in ("ReesHomogenization", "ReesLie", "ReesDilation", "ReesCentralInstrument"):
        compiled = lean("--json", "-o", f".lake/build/lib/lean/{module}.olean", f"{module}.lean")
        if compiled.strip():
            raise ValueError(f"proof compilation emitted diagnostics: {compiled}")
    report = lean("--json", "Audit.lean")
    records = parse_axioms(report)
    files = ("ReesHomogenization.lean", "ReesLie.lean", "ReesDilation.lean", "ReesCentralInstrument.lean", "Audit.lean", "source/ReesHomogenization.lean",
             "lakefile.toml", "lean-toolchain", "lake-manifest.json", "verify.py",
             "test_verify.py", "README.md", "REES_LIE_SCOPE.md", "REES_DILATION_SCOPE.md",
             "REES_CENTRAL_SCOPE.md", "central_controls.py", "test_central_controls.py", "CENTRAL_HANDOFF.md")
    return {"status": "SCOPED_LEAN_KERNEL_CHECK_PASSED", "theorem_count": len(THEOREMS),
            "declaration_count": len(records), "axioms_by_declaration": records,
            "lean_version": lean("--version").strip(),
            "mathlib_commit": MATHLIB, "original_draft_sha256": ORIGINAL,
            "compile_diagnostics": [], "formalizes_full_Rees_algorithm": False,
            "central_instrument_requires_cancellation_certificate": True,
            "bch_group_bridge_formalized": False,
            "new_algorithm_or_novelty_claim": False, "independent_review_this_pass": False,
            "quantum_execution": False, "main_checkout_modified": False,
            "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    record = verify()
    if args.output:
        args.output.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    print(f"Checked {record['theorem_count']} theorems and {record['declaration_count']-record['theorem_count']} definitions/instances/structures; standard foundations only; full algorithm NOT formalized.")

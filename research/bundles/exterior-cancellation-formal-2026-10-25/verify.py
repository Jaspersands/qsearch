"""Recompile exterior compression and audit its precise algebraic proof scope."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT.parent / "rees-formal-core-2026-10-24"
ARITHMETIC = ROOT.parent / "exterior-cancellation-2026-10-25"
LAKE = str(Path.home() / ".elan/bin/lake")
MATHLIB = "56a005855ea17e0b0958f73ec801ae140b0a1679"
TOOLCHAIN = "leanprover/lean4:v4.35.0"
ARITHMETIC_RECEIPT = "8e2f31784c0642fbac6a9370b43ba130533f6daecd379730da0a4bf7de9bec55"
PREFIX = "QSearch.ExteriorCompression."
THEOREMS = tuple(PREFIX + name for name in (
    "shear_apply", "contraction_square", "contraction_right_wedge", "wedge_update_closed",
    "shear_formula", "shear_fixes_closed", "shear_is_closed", "contraction_map_zero",
    "lift_fst", "covector_lift", "fst_comp_lift", "lift_comp_fst", "recover_closed",
    "projection_injective_on_closed", "projected_relation_is_full", "closed_dimension",
    "closed_top_zero", "closed_rows_dimension", "closed_rows_relation",
    "degenerate_projection_counterexample", "nonclosed_projection_counterexample"))
DEFINITIONS = tuple(PREFIX + name for name in (
    "contraction", "shear", "closedDegree", "covector", "lift", "closedProjection",
    "closedLift", "closedEquiv"))
DECLARATIONS = THEOREMS + DEFINITIONS
FOUNDATIONS = {"propext", "Classical.choice", "Quot.sound"}
SOURCES = ("ExteriorCompression.lean", "Audit.lean", "verify.py", "test_verify.py",
           "FORMAL_SCOPE.md", "HANDOFF.md")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def hashes(root, names):
    return {name: sha((root / name).read_bytes()) for name in names}


def expected_audit():
    return "import ExteriorCompression\n\n" + "".join(
        f"#print axioms {name}\n" for name in DECLARATIONS)


def validate_declarations(source):
    names = [PREFIX + name for name in re.findall(
        r"^\s*(?:(?:private|protected|noncomputable)\s+)?"
        r"(?:theorem|lemma|def|abbrev|axiom|constant|opaque|structure|class|inductive)\s+(\w+)",
        source, re.MULTILINE)]
    if len(names) != len(set(names)) or set(names) != set(DECLARATIONS):
        raise ValueError("declaration manifest differs from source")
    if re.search(r"\b(?:sorry|admit|axiom|unsafe|implemented_by)\b", source):
        raise ValueError("unsupported proof/source declaration")
    if re.search(r"^\s*(?:instance|example)\b", source, re.MULTILINE):
        raise ValueError("anonymous declarations are not in this audit format")


def parse_axioms(output):
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
            name, axioms = match[1], [a.strip() for a in match[2].split(",") if a.strip()]
        elif empty:
            name, axioms = empty[1], []
        else:
            raise ValueError("unexpected axiom diagnostic")
        if name not in DECLARATIONS or name in records or not set(axioms) <= FOUNDATIONS:
            raise ValueError("unexpected/duplicate declaration or unapproved axiom")
        records[name] = axioms
    if set(records) != set(DECLARATIONS):
        raise ValueError("incomplete axiom audit")
    return records


def command(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=180)
    if result.returncode or result.stderr.strip():
        raise RuntimeError(f"command failed: {args}\n{result.stdout}{result.stderr}")
    return result.stdout


def lean(runtime, *args):
    # Reuse the pinned cache, but compile only into this new bundle.
    return command([LAKE, "env", "/bin/sh", "-c",
                    'build="$1"; shift; exec env LEAN_PATH="$build:$PWD/.lake/build/lib/lean:$LEAN_PATH" lean "$@"',
                    "lean", str(ROOT / ".build"), *args], runtime)


def verify(runtime=RUNTIME):
    before = hashes(ROOT, SOURCES)
    validate_declarations((ROOT / "ExteriorCompression.lean").read_text())
    if (ROOT / "Audit.lean").read_text() != expected_audit():
        raise ValueError("audit commands differ from the complete declaration set")
    if (runtime / "lean-toolchain").read_text().strip() != TOOLCHAIN:
        raise ValueError("wrong Lean toolchain")
    if command(["git", "rev-parse", "HEAD"], runtime / "mathlib").strip() != MATHLIB:
        raise ValueError("wrong mathlib revision")
    if command(["git", "status", "--porcelain"], runtime / "mathlib").strip():
        raise ValueError("mathlib source checkout is modified")
    frozen = (ARITHMETIC / "receipt.json").read_bytes()
    if sha(frozen) != ARITHMETIC_RECEIPT:
        raise ValueError("prior arithmetic receipt changed")
    original = json.loads(frozen)["source_hashes"]
    if hashes(ARITHMETIC, original) != original:
        raise ValueError("prior arithmetic source changed")
    (ROOT / ".build").mkdir(exist_ok=True)
    diagnostics = lean(runtime, "--json", "-R", str(ROOT), "-o",
                       str(ROOT / ".build/ExteriorCompression.olean"),
                       str(ROOT / "ExteriorCompression.lean"))
    if diagnostics.strip():
        raise ValueError(f"proof compilation emitted diagnostics: {diagnostics}")
    axioms = parse_axioms(lean(runtime, "--json", "-R", str(ROOT), str(ROOT / "Audit.lean")))
    if before != hashes(ROOT, SOURCES):
        raise ValueError("source changed during verification")
    return {
        "status": "SCOPED_EXTERIOR_COMPRESSION_KERNEL_CHECK_PASSED",
        "theorem_count": len(THEOREMS), "declaration_count": len(DECLARATIONS),
        "axioms_by_declaration": axioms, "compile_diagnostics": [],
        "lean_version": lean(runtime, "--version").strip(), "mathlib_commit": MATHLIB,
        "source_sha256": before,
        "runtime_config_sha256": hashes(runtime, ("lean-toolchain", "lakefile.toml", "lake-manifest.json")),
        "prior_arithmetic_receipt_sha256": ARITHMETIC_RECEIPT,
        "prior_arithmetic_source_sha256": original,
        "algebraic_coordinate_recovery_formalized": True,
        "right_wedge_update_formalized": True,
        "row_dimension_and_nontrivial_relation_formalized": True,
        "top_degree_vanishing_formalized": True,
        "two_missing_assumption_counterexamples_formalized": True,
        "python_equivalence_formalized": False,
        "recursive_nonempty_support_formalized": False,
        "full_sde_solver_formalized": False,
        "runtime_and_probability_bounds_formalized": False,
        "new_quantum_algorithm_or_novelty_claim": False,
        "independent_review_this_pass": False,
        "main_checkout_modified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    parser.add_argument("--runtime", type=Path, default=RUNTIME)
    args = parser.parse_args()
    value = json.dumps(verify(args.runtime.resolve()), indent=2, sort_keys=True) + "\n"
    target = ROOT / "receipt.json"
    if args.write:
        target.write_text(value, encoding="ascii")
    elif target.read_text(encoding="ascii") != value:
        raise SystemExit("receipt mismatch")
    print(f"{len(THEOREMS)} theorems, {len(DECLARATIONS)} declarations; "
          f"scoped algebra only; SHA256 {sha(value.encode('ascii'))}")


if __name__ == "__main__":
    main()

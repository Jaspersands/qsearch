"""Global native square-completion probe using a real finite-field solver.

Both the polynomial and square-root coordinates live over the ORIGINAL F_p.
Boolean block selection models the score objective, not a promised subset.
SAT models need independent native verification. All other outcomes remain
unresolved; no solver timeout/UNSAT flag becomes a research negative.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.folded_norm_attacks import Problem, REPORT as INPUT_REPORT
from theorems.folded_norm_source import character, extension_model

REPORT = ROOT / "research/classical_baselines/folded_norm_mq.json"


def file_sha256(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def square_coordinates(model, root):
    """Independent polynomial-basis squaring, without an extension solver sort."""
    p, m = model["p"], model["m"]
    if len(root) != m or any(type(a) is not int or not 0 <= a < p for a in root):
        raise ValueError("canonical ORIGINAL base-field root coordinates required")
    raw = [0]*(2*m - 1)
    for i in range(m):
        for j in range(i, m):
            raw[i + j] = (raw[i + j] + (1 if i == j else 2)*root[i]*root[j]) % p
    modulus = model["record"]["modulus_coefficients"]
    for j in range(2*m - 2, m - 1, -1):
        for r in range(m):
            raw[j - m + r] = (raw[j - m + r] - modulus[r]*raw[j]) % p
    return raw[:m]


def nonsquare_scale(problem):
    value = next(a for a in range(2, problem.p) if pow(a, (problem.p - 1)//2, problem.p) == problem.p - 1)
    model = extension_model(problem.p, problem.m)
    if character(model, model["field"](value)) != -1:
        raise ArithmeticError("base-field nonsquare did not remain nonsquare in odd extension")
    return value


def emit_smt(problem, target, path):
    """Stream a typed SMT-LIB AST. No known polynomial/root witness is input."""
    try:
        import sexpdata as sx
    except ImportError as exc:
        raise RuntimeError("install requirements-research-mq.txt for SMT-LIB serialization") from exc
    integer(target, "accepted block target", 0, problem.n)
    p, n, m, K = problem.p, problem.n, problem.m, problem.K
    model, scale = extension_model(p, m), nonsquare_scale(problem)
    E, S = model["field"], sx.Symbol
    def field(value):
        return [S("as"), S("ff" + str(value % p)), S("F")]
    def add(terms):
        return field(0) if not terms else terms[0] if len(terms) == 1 else [S("ff.add"), *terms]
    def mul(coefficient, term):
        return term if coefficient % p == 1 else [S("ff.mul"), field(coefficient), term]
    powers, power = [], E(1)
    for _ in range(2*m - 1):
        powers.append(list(map(int, power.to_list())))
        power *= E.gen()
    linear_products, root_products, reduction_products, inverse_products = 0, 0, 0, 0
    with Path(path).open("w") as output:
        def emit(expression):
            output.write(sx.dumps(expression) + "\n")
        def define(name, expression):
            emit([S("define-fun"), S(name), [], S("F"), expression])
        def assert_equal(left, right):
            emit([S("assert"), [S("="), left, right]])
        emit([S("set-logic"), S("QF_FF")])
        emit([S("set-option"), S(":produce-models"), S("true")])
        emit([S("define-sort"), S("F"), [], [S("_"), S("FiniteField"), p]])
        coefficients = [S(f"c_{j}") for j in range(K)]
        selected = [S(f"b_{i}") for i in range(n)]
        roots = [[S(f"w_{i}_{j}") for j in range(m)] for i in range(n)]
        squares = [[S(f"sq_{i}_{j}") for j in range(m)] for i in range(n)]
        inverses = [[S(f"inv_{i}_{j}") for j in range(m)] for i in range(n)] if not problem.include_zero else []
        slack = [S(f"slack_{j}") for j in range(n - target)]
        for name in (coefficients + selected + slack
                     + [a for row in roots + squares + inverses for a in row]):
            emit([S("declare-const"), name, S("F")])
        # Native field idempotents are Boolean because F_p is a field. The
        # integer slack equation has NO modular wrap: p>n from nm<=p-1.
        for bit in selected + slack:
            assert_equal([S("ff.mul"), bit, bit], bit)
        assert_equal(add(selected + [mul(-1, bit) for bit in slack]), field(target))
        if target == n:
            # An exact consequence of p>n and idempotence, not a guessed subset.
            for bit in selected:
                assert_equal(bit, field(1))
        for i in range(n):
            for degree in range(2*m - 1):
                terms = []
                for a in range(m):
                    b = degree - a
                    if a <= b < m:
                        terms.append(mul(1 if a == b else 2, [S("ff.mul"), roots[i][a], roots[i][b]]))
                        root_products += 1
                define(f"raw_{i}_{degree}", add(terms))
            if inverses:
                for degree in range(2*m - 1):
                    terms = []
                    for a in range(m):
                        b = degree - a
                        if 0 <= b < m:
                            terms.append([S("ff.mul"), roots[i][a], inverses[i][b]])
                            inverse_products += 1
                    define(f"inverse_raw_{i}_{degree}", add(terms))
            for r in range(m):
                x, power = problem.points[i*m + r], 1
                terms = []
                for j in range(K):
                    terms.append(mul(power, coefficients[j]))
                    linear_products += int(power != 1)
                    power = power*x % p
                define(f"eval_{i}_{r}", add(terms))
                factor = 1 if problem.signs[i] == 1 else scale
                terms, inverse_terms = [], []
                for j, values in enumerate(powers):
                    value = values[r]
                    if value:
                        terms.append(mul(value, S(f"raw_{i}_{j}")))
                        reduction_products += int(value != 1)*(1 + bool(inverses))
                        if inverses:
                            inverse_terms.append(mul(value, S(f"inverse_raw_{i}_{j}")))
                assert_equal(squares[i][r], add(terms))
                residual = add([S(f"eval_{i}_{r}"), field(-problem.shifts[i][r]), mul(-factor, squares[i][r])])
                assert_equal([S("ff.mul"), selected[i], residual], field(0))
                if inverses:
                    # w_i*inv_i=b_i in E: selected roots are nonzero; for an
                    # unselected block inv_i=0 always permits any root.
                    assert_equal(add(inverse_terms), selected[i] if r == 0 else field(0))
        emit([S("check-sat")])
        emit([S("get-value"), coefficients + selected + [a for row in roots for a in row]])
    spec = problem.specification()
    binding = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"input_sha256": binding, "target": target,
            "scalar_polynomial_variables": K, "base_field_root_variables": n*m,
            "Boolean_block_selectors": n, "native_coordinate_equations": n*m,
            "selector_representation": "PRIME_FIELD_IDEMPOTENTS",
            "square_coordinate_auxiliary_variables": n*m, "cardinality_slack_bits": n - target,
            "strict_inverse_auxiliary_variables": 0 if problem.include_zero else n*m,
            "pure_prime_field_system_maximum_total_degree": 2,
            "native_linear_constant_products": linear_products,
            "frontend_Vandermonde_power_products": n*m*K,
            "public_folding_point_products_recorded": n*m,
            "root_quadratic_products": root_products,
            "strict_inverse_quadratic_products": inverse_products,
            "root_offdiagonal_constant_products": n*m*(m - 1)//2,
            "selector_idempotent_products": 2*n - target,
            "selector_gate_products": n*m,
            "gate_residual_constant_products": m*sum((-(1 if sign == 1 else scale)) % p != 1 for sign in problem.signs),
            "cardinality_slack_negation_products": n - target,
            "extension_reduction_constant_products": reduction_products,
            "public_nonsquare_tests_charged": scale - 1,
            "square_reduction_basis_products_charged": 2*m - 1,
            "cardinality_no_wrap_because_prime_exceeds_block_count": p > n,
            "operation_counters_are_expression_counts_not_complete_bit_complexity": True,
            "SMT_bytes": Path(path).stat().st_size,
            "SMT_sha256": file_sha256(path),
            "known_polynomial_or_root_witness_supplied": False,
            "selected_subset_fixed_or_promised_satisfiable": False,
            "extension_field_unknown_or_coefficient_relaxation_used": False,
            "public_field": model["record"]}


def parse_model(text, p):
    import sexpdata as sx
    try:
        parsed = sx.loads(text, true="true", false="false")
    except Exception as exc:
        raise ValueError("solver output is not a complete SMT-LIB assignment list") from exc
    if not isinstance(parsed, list):
        raise ValueError("get-value assignment list required")
    result = {}
    for pair in parsed:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("malformed solver assignment")
        name, value = str(pair[0]), pair[1]
        if name in result:
            raise ValueError("duplicate solver variable")
        if type(value) is bool:
            result[name] = value
            continue
        token = str(value)
        if not token.startswith("#f"):
            raise ValueError("native finite-field model literal required")
        pieces = token[2:].split("m")
        if len(pieces) != 2 or int(pieces[1]) != p:
            raise ValueError("solver model changed the ORIGINAL prime field")
        result[name] = int(pieces[0]) % p
    return result


def verify_model(problem, target, assignments):
    """Check every selected root equation and the original score, not SAT flags."""
    p, n, m, K = problem.p, problem.n, problem.m, problem.K
    integer(target, "accepted block target", 0, n)
    coefficients = [assignments[f"c_{j}"] for j in range(K)]
    values, flags = problem.evaluate(coefficients)
    point = 1
    for value in values:
        direct = 0
        for coefficient in reversed(coefficients):
            direct = (direct*point + coefficient) % p
        if direct != value:
            raise ValueError("native multipoint evaluation disagrees with independent original Horner replay")
        point = point*problem.gamma % p
    scale, model = nonsquare_scale(problem), extension_model(p, m)
    selected, witnesses = [], []
    for i in range(n):
        bit = assignments[f"b_{i}"]
        if type(bit) is not int or bit not in (0, 1):
            raise ValueError("solver block selector is not a native field Boolean")
        if bit:
            root = [assignments[f"w_{i}_{r}"] for r in range(m)]
            square = square_coordinates(model, root)
            factor = 1 if problem.signs[i] == 1 else scale
            expected = [(problem.shifts[i][r] + factor*square[r]) % p for r in range(m)]
            if (expected != values[i*m:(i + 1)*m] or not flags[i]
                    or (not problem.include_zero and not any(root))):
                raise ValueError("SAT model fails the ORIGINAL native square/predicate equations")
            selected.append(i)
            witnesses.append({"block": i, "root_base_field_coordinates": root})
    if len(selected) < target or sum(flags) < target:
        raise ValueError("SAT model misses the actual optimization target")
    return {"polynomial_coefficients": coefficients, "native_score": sum(flags),
            "native_accepted_blocks": [i for i, yes in enumerate(flags) if yes],
            "selected_blocks": selected, "selected_square_root_witnesses": witnesses,
            "verification_costs": {"independent_original_Horner_products": n*m*K,
                                   "native_extension_norm_character_evaluations": n,
                                   "selected_root_quadratic_products": len(selected)*m*(m + 1)//2,
                                   "selected_root_modulus_reduction_products": len(selected)*m*(m - 1)},
            "all_selected_native_equations_independently_verified": True}


def run_solver(binary, script, *, seconds=60, memory_mb=3072):
    """Own-child budgets: an intentional solver limit is never UNSAT evidence."""
    integer(seconds, "external solver wall-clock budget", 1, 3600)
    integer(memory_mb, "sampled child RSS budget MiB", 128, 8192)
    stdout_path, stderr_path = Path(str(script) + ".stdout"), Path(str(script) + ".stderr")
    command = [str(binary), "--lang=smt2", f"--tlimit={seconds*1000}", str(script)]
    start, peak_rss, terminated = time.monotonic(), None, None
    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
        while process.poll() is None:
            if time.monotonic() - start > seconds + 5:
                terminated = "WALL_CLOCK_BUDGET"
            try:
                measured = subprocess.run(["ps", "-o", "rss=", "-p", str(process.pid)],
                                          capture_output=True, text=True, timeout=2)
                if measured.stdout.strip():
                    peak_rss = max(peak_rss or 0, int(measured.stdout.strip()))
                    if peak_rss > memory_mb*1024:
                        terminated = "SAMPLED_CHILD_RSS_BUDGET"
            except (OSError, ValueError, subprocess.TimeoutExpired):
                pass
            if terminated:
                process.kill()
                process.wait()
                break
            try:
                process.wait(timeout=.25)
            except subprocess.TimeoutExpired:
                pass
    stdout = stdout_path.read_text(errors="replace")
    stderr = stderr_path.read_text(errors="replace")
    return {"process_returncode": process.returncode, "elapsed_seconds": time.monotonic() - start,
            "requested_solver_time_budget_seconds": seconds,
            "sampled_child_RSS_budget_MiB": memory_mb, "sampled_peak_RSS_KiB": peak_rss,
            "memory_monitor_is_sampled_not_a_hard_OS_limit": True,
            "terminated_by_declared_experiment_budget": terminated,
            "stdout": stdout, "stderr": stderr}


def probe(problem, target, binary, directory, *, seconds=60, memory_mb=3072):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    script = directory / f"n{problem.n}-K{problem.K}-target{target}.smt2"
    start = time.monotonic()
    encoding = emit_smt(problem, target, script)
    encoding["frontend_elapsed_seconds"] = time.monotonic() - start
    execution = run_solver(binary, script, seconds=seconds, memory_mb=memory_mb)
    stdout, stderr = execution.pop("stdout"), execution.pop("stderr")
    first, _, remainder = stdout.strip().partition("\n")
    first = first.strip()
    status, witness, verification_error = "UNKNOWN_BACKEND_ERROR", None, None
    if first == "sat":
        try:
            witness = verify_model(problem, target, parse_model(remainder.strip(), problem.p))
            status = "SAT_NATIVE_WITNESS_VERIFIED"
        except (ValueError, KeyError, TypeError) as exc:
            status, verification_error = "UNKNOWN_INVALID_SAT_MODEL", str(exc)
            if execution["terminated_by_declared_experiment_budget"]:
                status = "UNKNOWN_" + execution["terminated_by_declared_experiment_budget"]
    elif execution["terminated_by_declared_experiment_budget"]:
        status = "UNKNOWN_" + execution["terminated_by_declared_experiment_budget"]
    elif first == "unsat":
        status = "SOLVER_UNSAT_NOT_INDEPENDENTLY_CERTIFIED"
    elif first == "unknown":
        status = "UNKNOWN_SOLVER_RESULT"
    elif "interrupted by timeout" in stderr:
        status = "UNKNOWN_SOLVER_REPORTED_TIME_BUDGET"
    return {"status": status, "specification": problem.specification(), "encoding": encoding,
            "execution": execution, "witness": witness, "verification_error": verification_error,
            "backend_diagnostic_prefix": (stderr or remainder)[:2000] if first != "sat" else stderr[:2000],
            "raw_stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
            "source_rerolls": 0, "native_optimization_target_not_a_prescribed_subset": True,
            "solver_UNSAT_or_budget_failure_is_a_hardness_certificate": False,
            "accepted_speedup_or_general_dequantization_claim": False}


def run_controls(binary, directory, *, seconds=60, memory_mb=3072):
    from theorems.folded_norm_attacks import instance
    input_bytes = INPUT_REPORT.read_bytes()
    inputs = json.loads(input_bytes)
    dependencies = ("folded_norm_attacks.py", "folded_norm_source.py", "prime_character_opi.py", "bpqm_gibbs_frontier.py")
    source_hash = file_sha256(__file__)
    dependency_hashes = {name: file_sha256(ROOT/"theorems"/name) for name in dependencies}
    input_hash, binary_hash = hashlib.sha256(input_bytes).hexdigest(), file_sha256(binary)
    del input_bytes
    calibration = probe(instance(7, 3, 1, 1, 3, 20, include_zero=False), 2, binary,
                        Path(directory)/"calibration-three", seconds=5, memory_mb=512)
    if calibration["status"] != "SAT_NATIVE_WITNESS_VERIFIED":
        raise RuntimeError("solver failed a native calibration; no main outcomes were recorded")
    six_block = probe(instance(7, 6, 1, 1, 3, 2, include_zero=False), 4, binary,
                      Path(directory)/"calibration-six", seconds=2, memory_mb=512)
    if six_block["status"].startswith("SOLVER_UNSAT"):
        raise ArithmeticError("solver/encoding contradicted exhaustively verified six-block feasibility")
    controls = []
    for control in inputs["controls"]:
        spec = control["classical"]["specification"]
        n = spec["n_blocks"]
        problem = Problem(int(spec["p_decimal"]), n, spec["m_fold"], spec["ORIGINAL_scalar_dimension_K"],
                          spec["gamma"], tuple(map(tuple, spec["shifts"])), tuple(spec["signs"]), spec["include_zero"])
        if problem.specification() != spec:
            raise ArithmeticError("input record's public field or native problem changed")
        target = {25: 25, 65: 58, 127: 114}[n]
        result = probe(problem, target, binary, directory, seconds=seconds, memory_mb=memory_mb)
        if result["encoding"]["input_sha256"] != control["classical"]["input_sha256"]:
            raise ArithmeticError("global solver did not use the same fixed public input")
        controls.append(result)
        print(json.dumps({"n": n, "target": target, "status": result["status"],
                          "score": None if result["witness"] is None else result["witness"]["native_score"],
                          "SMT_bytes": result["encoding"]["SMT_bytes"],
                          "execution": result["execution"]}), flush=True)
    version = subprocess.run([str(binary), "--version"], capture_output=True, text=True, timeout=10)
    if (file_sha256(__file__) != source_hash or file_sha256(INPUT_REPORT) != input_hash
            or file_sha256(binary) != binary_hash
            or any(file_sha256(ROOT/"theorems"/name) != digest for name, digest in dependency_hashes.items())):
        raise RuntimeError("a producer, dependency, input report or binary changed during the run; refusing misleading provenance")
    return {"schema_version": "folded-norm-native-mq-v1", "controls": controls,
            "backend_calibrations": [calibration, six_block],
            "backend_version_first_line": version.stdout.splitlines()[0],
            "backend_binary_sha256": binary_hash,
            "input_report_sha256": input_hash, "source_sha256": source_hash,
            "dependency_sha256": dependency_hashes,
            "no_central_registry_admission_or_automatic_negative_result": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default=os.environ.get("QSEARCH_CVC5") or shutil.which("cvc5"))
    parser.add_argument("--directory", type=Path, default=ROOT/"tmp/folded_norm_mq")
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--memory-mb", type=int, default=3072)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.solver:
        parser.error("a cvc5 binary BUILT WITH CoCoA is required; the standard Python wheel lacks it")
    report = run_controls(Path(args.solver).resolve(), args.directory, seconds=args.seconds, memory_mb=args.memory_mb)
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()

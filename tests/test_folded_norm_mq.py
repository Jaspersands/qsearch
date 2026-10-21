"""Native prime-field encoding, optimization semantics and verified witnesses."""

from itertools import product
import json
import os
from pathlib import Path

import pytest

import theorems.folded_norm_mq as module
from theorems.folded_norm_attacks import Problem, instance
from theorems.folded_norm_source import extension_model

BINARY = os.environ.get("QSEARCH_CVC5")
native_solver = pytest.mark.skipif(not BINARY, reason="requires a cvc5 executable built WITH CoCoA")


def assignments_for_word(problem, coefficients):
    values, flags = problem.evaluate(coefficients)
    model, scale = extension_model(problem.p, problem.m), module.nonsquare_scale(problem)
    E = model["field"]
    assignments = {f"c_{j}": c for j, c in enumerate(coefficients)}
    for i, flag in enumerate(flags):
        assignments[f"b_{i}"] = int(flag)
        root = E(0)
        if flag:
            z = E(values[i*problem.m:(i + 1)*problem.m]) - E(list(problem.shifts[i]))
            factor = 1 if problem.signs[i] == 1 else scale
            root = (z*E(pow(factor, -1, problem.p))) ** ((model["Q"] + 1)//4)
            assert factor*root*root == z
        for r, value in enumerate(root.to_list()):
            assignments[f"w_{i}_{r}"] = int(value)
    return assignments, sum(flags)


def test_full_small_root_space_squares_match_independent_extension_arithmetic():
    model = extension_model(7, 3)
    E = model["field"]
    for coordinates in product(range(7), repeat=3):
        assert module.square_coordinates(model, coordinates) == list(map(int, (E(list(coordinates)) ** 2).to_list()))
    with pytest.raises(ValueError, match="ORIGINAL"):
        module.square_coordinates(model, (True, 0, 0))


def test_native_model_verifier_checks_each_selected_equation_and_target_not_just_total_flags():
    problem = instance(127, 6, 3, 10, 3, 5211)
    coefficients = list(range(10))
    assignments, count = assignments_for_word(problem, coefficients)
    witness = module.verify_model(problem, count, assignments)
    assert witness["native_score"] == count
    assert witness["polynomial_coefficients"] == coefficients
    selected = witness["selected_blocks"]
    assert selected
    bad = dict(assignments)
    bad[f"w_{selected[0]}_0"] = (bad[f"w_{selected[0]}_0"] + 1) % problem.p
    with pytest.raises(ValueError, match="ORIGINAL"):
        module.verify_model(problem, count, bad)
    with pytest.raises(ValueError, match="target"):
        module.verify_model(problem, count + 1, assignments)
    bad = dict(assignments)
    bad["c_0"] = True
    with pytest.raises(ValueError, match="canonical polynomial"):
        module.verify_model(problem, count, bad)


def test_solver_model_parser_rejects_prime_changes_duplicates_and_incomplete_outputs():
    pytest.importorskip("sexpdata")
    assert module.parse_model("((c_0 #f3m7) (b_0 true) (w_0_0 #f-1m7))", 7) == {
        "c_0": 3, "b_0": True, "w_0_0": 6}
    for text in ("((c_0 #f3m5))", "((c_0 #f3m7) (c_0 #f4m7))", "((c_0 3))", "((c_0 #f3m7)"):
        with pytest.raises(ValueError):
            module.parse_model(text, 7)


@native_solver
def test_global_selectable_blocks_succeed_when_first_target_subset_is_infeasible(tmp_path):
    pytest.importorskip("sexpdata")
    problem = instance(7, 3, 1, 1, 3, 20, include_zero=False)
    # Exhaust ALL native polynomials independently. No source or witness is
    # supplied to the solver. A fixed first-two-block solve would be UNSAT.
    scores = [problem.evaluate([c])[1] for c in range(7)]
    assert max(map(sum, scores)) == 2
    assert not any(all(row[:2]) for row in scores)
    result = module.probe(problem, 2, BINARY, tmp_path, seconds=5, memory_mb=512)
    assert result["status"] == "SAT_NATIVE_WITNESS_VERIFIED", result
    assert result["witness"]["native_score"] == 2
    assert result["witness"]["selected_blocks"] != [0, 1]
    assert not result["encoding"]["selected_subset_fixed_or_promised_satisfiable"]
    assert not result["encoding"]["known_polynomial_or_root_witness_supplied"]
    assert not result["encoding"]["extension_field_unknown_or_coefficient_relaxation_used"]
    assert result["encoding"]["cardinality_no_wrap_because_prime_exceeds_block_count"]
    assert result["encoding"]["pure_prime_field_system_maximum_total_degree"] == 2


@native_solver
@pytest.mark.parametrize("include_zero,target,expected", [(True, 6, "SAT_NATIVE_WITNESS_VERIFIED"),
                                                        (False, 4, "SOLVER_UNSAT_NOT_INDEPENDENTLY_CERTIFIED")])
def test_zero_policy_and_UNSAT_scope_match_full_native_enumeration(tmp_path, include_zero, target, expected):
    pytest.importorskip("sexpdata")
    problem = Problem(7, 6, 1, 1, 3, ((0,),)*6, (1, -1, 1, -1, 1, -1), include_zero)
    maximum = max(sum(problem.evaluate([c])[1]) for c in range(7))
    assert maximum == (6 if include_zero else 3)
    result = module.probe(problem, target, BINARY, tmp_path, seconds=2, memory_mb=512)
    # Bounded solving is not promised complete, even on a known tiny input.
    # Keep the independently known truth; a timeout never becomes UNSAT.
    if include_zero:
        assert result["status"] == expected, result
    else:
        assert result["status"] == expected or result["status"].startswith("UNKNOWN_SOLVER"), result
    assert not result["solver_UNSAT_or_budget_failure_is_a_hardness_certificate"]
    if result["witness"]:
        assert result["witness"]["polynomial_coefficients"] == [0]


def test_native_idempotent_cardinality_is_exact_for_every_small_selection_without_wrap():
    for p, n in ((7, 6), (11, 8)):
        assert [x for x in range(p) if (x*x - x) % p == 0] == [0, 1]
        for target in range(n + 1):
            possible_slack = {sum(bits) for bits in product((0, 1), repeat=n - target)}
            for selected in product((0, 1), repeat=n):
                possible = any((sum(selected) - slack - target) % p == 0 for slack in possible_slack)
                assert possible == (sum(selected) >= target)


@native_solver
def test_known_feasible_six_block_budget_failure_is_retained_not_reported_as_UNSAT(tmp_path):
    pytest.importorskip("sexpdata")
    problem = instance(7, 6, 1, 1, 3, 2, include_zero=False)
    assert max(sum(problem.evaluate([c])[1]) for c in range(7)) == 4
    result = module.probe(problem, 4, BINARY, tmp_path, seconds=1, memory_mb=512)
    assert result["status"] == "SAT_NATIVE_WITNESS_VERIFIED" or result["status"].startswith("UNKNOWN_SOLVER"), result
    assert not result["solver_UNSAT_or_budget_failure_is_a_hardness_certificate"]


@native_solver
def test_actual_extension_square_reduction_in_SMT_matches_native_pinned_polynomials(tmp_path):
    sx = pytest.importorskip("sexpdata")
    problem = instance(7, 2, 3, 4, 3, 5213)
    original = tmp_path/"extension.smt2"
    metadata = module.emit_smt(problem, 2, original)
    assert metadata["base_field_root_variables"] == 6
    assert metadata["root_quadratic_products"] == 12
    commands = sx.loads("(" + original.read_text() + ")")
    for index, coefficients in enumerate(([0, 0, 0, 0], [1, 2, 3, 4], [6, 1, 0, 2], [3, 0, 1, 6])):
        pinned = [[sx.Symbol("assert"), [sx.Symbol("="), sx.Symbol(f"c_{j}"),
                                        [sx.Symbol("as"), sx.Symbol(f"ff{value}"), sx.Symbol("F")]]]
                  for j, value in enumerate(coefficients)]
        path = tmp_path/f"pinned{index}.smt2"
        path.write_text("\n".join(sx.dumps(c) for c in commands[:-2] + pinned + commands[-2:]) + "\n")
        result = module.run_solver(BINARY, path, seconds=10, memory_mb=512)
        status, _, rest = result["stdout"].strip().partition("\n")
        expected = all(problem.evaluate(coefficients)[1])
        assert status == ("sat" if expected else "unsat"), result
        if expected:
            verified = module.verify_model(problem, 2, module.parse_model(rest, problem.p))
            assert verified["polynomial_coefficients"] == coefficients


def test_UNKNOWN_and_unverified_UNSAT_results_never_create_research_negatives(tmp_path, monkeypatch):
    pytest.importorskip("sexpdata")
    problem = instance(7, 6, 1, 1, 3, 2)
    for answer, status in (("unknown\n", "UNKNOWN_SOLVER_RESULT"),
                           ("unsat\n", "SOLVER_UNSAT_NOT_INDEPENDENTLY_CERTIFIED"),
                           ("sat\n((c_0 #f1m5))", "UNKNOWN_INVALID_SAT_MODEL")):
        monkeypatch.setattr(module, "run_solver", lambda *args, **kwargs: {
            "stdout": answer, "stderr": "", "terminated_by_declared_experiment_budget": None,
            "process_returncode": 0})
        result = module.probe(problem, 4, "not-executed", tmp_path)
        assert result["status"] == status
        assert result["witness"] is None
        assert not result["accepted_speedup_or_general_dequantization_claim"]
        assert not result["solver_UNSAT_or_budget_failure_is_a_hardness_certificate"]


def test_complete_valid_witness_is_kept_even_if_solver_was_later_budget_terminated(tmp_path, monkeypatch):
    sx = pytest.importorskip("sexpdata")
    problem = instance(7, 3, 1, 1, 3, 20, include_zero=False)
    assignments, target = assignments_for_word(problem, [2])
    body = sx.dumps([[sx.Symbol(name), sx.Symbol(f"#f{value}m7")] for name, value in assignments.items()])
    monkeypatch.setattr(module, "run_solver", lambda *args, **kwargs: {
        "stdout": "sat\n" + body, "stderr": "", "process_returncode": -9,
        "terminated_by_declared_experiment_budget": "WALL_CLOCK_BUDGET"})
    result = module.probe(problem, target, "not-executed", tmp_path)
    assert result["status"] == "SAT_NATIVE_WITNESS_VERIFIED"
    assert result["witness"]["native_score"] == target == 2
    assert result["execution"]["terminated_by_declared_experiment_budget"] == "WALL_CLOCK_BUDGET"


def test_own_child_solver_budget_kills_and_waits_instead_of_reporting_UNSAT(tmp_path):
    # A deliberately slow executable exercises the process lifecycle, not any
    # research outcome. It is killed by the declared experiment wall budget.
    binary = tmp_path/"slow-solver"
    binary.write_text("#!/usr/bin/env python3\nimport time\ntime.sleep(30)\n")
    binary.chmod(0o700)
    script = tmp_path/"empty.smt2"
    script.write_text("")
    result = module.run_solver(binary, script, seconds=1, memory_mb=512)
    assert result["terminated_by_declared_experiment_budget"] == "WALL_CLOCK_BUDGET"
    assert result["process_returncode"] is not None and result["process_returncode"] < 0
    assert result["elapsed_seconds"] < 12


def test_live_global_report_keeps_input_provenance_and_all_failures_unresolved():
    if not module.REPORT.exists():
        pytest.skip("global live workflow not yet recorded")
    report = json.loads(module.REPORT.read_text())
    assert report["source_sha256"] == module.file_sha256(module.__file__)
    assert report["input_report_sha256"] == module.file_sha256(module.INPUT_REPORT)
    for name, digest in report["dependency_sha256"].items():
        assert digest == module.file_sha256(module.ROOT/"theorems"/name)
    assert [row["encoding"]["target"] for row in report["controls"]] == [25, 58, 114]
    for row in report["controls"]:
        assert not row["encoding"]["known_polynomial_or_root_witness_supplied"]
        assert not row["solver_UNSAT_or_budget_failure_is_a_hardness_certificate"]
        assert not row["accepted_speedup_or_general_dequantization_claim"]
        assert row["source_rerolls"] == 0
        if row["witness"]:
            spec = row["specification"]
            problem = Problem(int(spec["p_decimal"]), spec["n_blocks"], spec["m_fold"],
                              spec["ORIGINAL_scalar_dimension_K"], spec["gamma"],
                              tuple(map(tuple, spec["shifts"])), tuple(spec["signs"]), spec["include_zero"])
            assert sum(problem.evaluate(row["witness"]["polynomial_coefficients"])[1]) == row["witness"]["native_score"]
        else:
            assert row["status"].startswith(("UNKNOWN_", "SOLVER_UNSAT_"))

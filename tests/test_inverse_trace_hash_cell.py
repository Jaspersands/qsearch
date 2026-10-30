"""Exact tiny native fibers and bounded-probe controls, not sampling evidence."""

from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from itertools import product
import json

import pytest
import z3
from z3.z3util import get_vars

from theorems.explicit_quadratic_opi import field
import theorems.inverse_trace_hash_cell as cell


def instance(bits=4, mode="mixed"):
    length = bits*bits if bits >= 4 else 4
    return {"bits": bits, "checks": length//8 if bits >= 4 else 1,
            "points": [(5*i+3) % (1 << bits) for i in range(length)],
            "targets": [i % 2 if mode == "mixed" else int(mode) for i in range(length)],
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}


@lru_cache(None)
def arithmetic(bits, coefficients):
    """Independent integer polynomial arithmetic in the SUPPLIED field."""
    q = 1 << bits
    modulus = sum(c << j for j, c in enumerate(coefficients))

    def multiply(a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            if a & q:
                a ^= modulus
            b >>= 1
        return result

    table = tuple(tuple(multiply(a, b) for b in range(q)) for a in range(q))
    inverse = (0,) + tuple(next(b for b in range(1, q) if table[a][b] == 1)
                           for a in range(1, q))
    traces = []
    for a in range(q):
        t, power = 0, a
        for _ in range(bits):
            t ^= power
            power = table[power][power]
        assert t in (0, 1)
        traces.append(t)
    return table, inverse, tuple(traces)


def hash_value(rows, u):
    return sum(((row & u).bit_count() % 2) << j for j, row in enumerate(rows))


def direct_fibers(problem, indices):
    """Enumerate accepted WORDS, without SAT or Vandermonde elimination."""
    bits, checks = problem["bits"], problem["checks"]
    mul, inverse, traces = arithmetic(bits, tuple(problem["field_modulus_coefficients"]))
    pivot = next(j for j in range(bits) if traces[1 << j])
    local_positions = [j for j in range(bits) if j != pivot]
    alphabets = [[x for x in range(1 << bits) if traces[inverse[x]] == problem["targets"][i]]
                 for i in indices]
    fibers = defaultdict(dict)
    for word in product(*alphabets):
        h = [0]*checks
        for index, x in zip(indices, word):
            power = 1
            for j in range(checks):
                h[j] ^= mul[power][x]
                power = mul[power][problem["points"][index]]
        u = sum(((inverse[x] >> j) & 1) << (s*(bits-1)+l)
                for s, x in enumerate(word[checks:]) for l, j in enumerate(local_positions))
        assert u not in fibers[tuple(h)]
        by_index = dict(zip(indices, word))
        fibers[tuple(h)][u] = tuple(by_index[i] for i in sorted(indices))
    return fibers


def actual_solutions(report):
    result = {entry["u"]: tuple(entry["residual_word"]) for entry in report["solutions"]}
    assert len(result) == len(report["solutions"]) == report["model_count"]
    return result


def assert_receipt(report):
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert not report["uniform_sampler"]
    assert not report["hardness_evidence"]
    assert not report["polynomial_enumeration_established"]
    assert not report["whole_workflow_wall_clock_cap_enforced"]
    assert not report["completeness_independently_certified"]
    assert report["unsat_proof_artifact"] is None
    assert "selected_sample" not in report
    calls = report["solver_calls"]
    for status in ("SAT", "UNSAT", "UNKNOWN"):
        assert report["solver_call_counts"][status] == sum(c["status"] == status for c in calls)
    assert report["solver_check_errors"] == sum(c["status"] == "ERROR" for c in calls)
    assert report["check_seconds"] == sum(c["check_seconds"] for c in calls)
    assert report["model_count"] == report["seed_model_count"] + report["solver_model_count"]
    assert report["seed_model_count"] == sum(s["origin"] == "external_seed" for s in report["solutions"])
    assert report["solver_model_count"] == sum(s["origin"] == "solver" for s in report["solutions"])
    assert report["solver_model_count"] <= report["solver_call_counts"]["SAT"]
    for call in calls:
        assert isinstance(call["solver_statistics"], dict)
        assert 0 < call["timeout_ms"] <= report["timeout_ms"]
        assert call["check_seconds"] >= 0
    assert all(v >= 0 for k, v in report.items() if k.endswith("_seconds") and v is not None)
    assert report["total_seconds"] >= report["setup_seconds"] + report["check_seconds"]
    first = report["first_verified_model_seconds"]
    if report["solutions"]:
        assert 0 <= first <= report["total_seconds"]
        if not report["seed_model_count"]:
            assert report["setup_seconds"] <= first
    else:
        assert first is None
    first_solver = report["first_solver_model_seconds"]
    if report["solver_model_count"]:
        assert first <= first_solver <= report["total_seconds"]
        assert report["setup_seconds"] <= first_solver
        if not report["seed_model_count"]:
            assert first_solver == first
    else:
        assert first_solver is None
    if report["complete"]:
        assert report["status"] == "COMPLETE"
        assert report["stop_reason"] == "final_unsat"
        assert calls[-1]["status"] == report["final_solver_status"] == "UNSAT"
        assert report["cell_cardinality"] == report["model_count"]
        assert len(calls) == report["solver_model_count"] + 1
        assert report["projected_blocks"] == report["model_count"]
        assert report["setup_seconds"] <= report["completion_seconds"] <= report["total_seconds"]
        if first is not None:
            assert first <= report["completion_seconds"]
    else:
        assert report["status"] in ("PARTIAL", "UNKNOWN")
        assert report["cell_cardinality"] is None
        assert report["completion_seconds"] is None


@pytest.mark.parametrize("mode", ["0", "1", "mixed"])
@pytest.mark.parametrize("h", [(0, 0), (3, 7), (12, 4)])
def test_complete_native_gf16_cells_match_direct_accepted_words(mode, h):
    problem = instance(mode=mode)
    indices = (12, 2, 9, 0)
    fiber = direct_fibers(problem, indices)[h]
    hashes = [((), 0), ((0, 0, 0, 0), 0), ((0, 0, 0, 0), 1),
              ((1, 1, 0, 8), 0), ((1, 1, 0, 8), 3), ((1, 1, 0, 8), 1),
              ((3, 6, 12, 24), 5)]
    for rows, rhs in hashes:
        report = cell.enumerate_cell(problem, indices, h, rows, rhs, timeout_ms=5000)
        expected = {u: word for u, word in fiber.items() if hash_value(rows, u) == rhs}
        assert report["complete"]
        assert actual_solutions(report) == expected
        assert report["hash_rows"] == list(rows) and report["hash_rhs"] == rhs
        assert report["pivot_indices"] == [12, 2]
        assert report["free_indices"] == [9, 0]
        assert report["residual_word_indices"] == [0, 2, 9, 12]
        assert_receipt(report)


def test_every_tiny_hash_including_zero_deficient_overdetermined_and_inconsistent():
    problem = instance(2, "0")
    indices, h = (0, 1, 2), (0,)
    fiber = direct_fibers(problem, indices)[h]
    assert len(fiber) == 4
    for rows in product(range(4), repeat=3):
        for rhs in range(8):
            report = cell.enumerate_cell(problem, indices, h, rows, rhs, timeout_ms=5000)
            expected = {u: word for u, word in fiber.items() if hash_value(rows, u) == rhs}
            assert report["complete"]
            assert actual_solutions(report) == expected
            assert report["hash_rank"] == report["hash_system"]["rank"]
            assert report["hash_free_bits"] == 2-report["hash_rank"]
            assert report["hash_system"]["consistent"] == bool(expected)
            if expected:
                assert len(expected) == 1 << report["hash_free_bits"]
            assert_receipt(report)


@pytest.mark.parametrize("targets", list(product((0, 1), repeat=3)))
def test_every_small_target_and_nonzero_syndrome(targets):
    problem = instance(2)
    indices = (2, 0, 3)
    for i, b in zip(indices, targets):
        problem["targets"][i] = b
    fibers = direct_fibers(problem, indices)
    for h in range(4):
        report = cell.enumerate_cell(problem, indices, (h,), (), 0, timeout_ms=5000)
        assert report["complete"]
        assert actual_solutions(report) == fibers[(h,)]
        assert_receipt(report)


@pytest.mark.parametrize("bits", [2, 3, 4, 5])
def test_trace_coordinates_are_canonical_bijective_and_zero_complete(bits):
    problem = instance(bits, "0")
    indices = tuple(range(problem["checks"]+1))
    report = cell.enumerate_cell(problem, indices, [0]*problem["checks"], (), 0,
                                 max_models=0)
    _, inverse, traces = arithmetic(bits, tuple(problem["field_modulus_coefficients"]))
    mask = sum(traces[1 << j] << j for j in range(bits))
    c = mask & -mask
    positions = [j for j in range(bits) if 1 << j != c]
    basis = [(1 << j) ^ (c if (mask >> j) & 1 else 0) for j in positions]
    assert report["trace_mask"] == mask
    assert report["trace_one"] == c
    assert report["trace_kernel_basis"] == basis
    assert report["trace_free_bit_positions"] == positions
    assert report["u_bit_order"] == [[indices[-1], j] for j in range(bits-1)]
    for b in (0, 1):
        alphabet = []
        for u in range(1 << (bits-1)):
            y = b*c
            for j, v in enumerate(basis):
                if (u >> j) & 1:
                    y ^= v
            alphabet.append(inverse[y])
        assert len(set(alphabet)) == 1 << (bits-1)
        assert set(alphabet) == {x for x in range(1 << bits) if traces[inverse[x]] == b}
        assert (0 in alphabet) == (b == 0)


def test_full_rank_hash_has_no_symbolic_binary_free_bits_and_final_unsat():
    problem = instance(4, "0")
    indices, h, rows = (1, 8, 3, 12), (0, 0), (1, 2, 4, 8, 16, 32)
    fiber = direct_fibers(problem, indices)[h]
    for u in range(64):
        report = cell.enumerate_cell(problem, indices, h, rows, u, timeout_ms=5000)
        assert report["hash_rank"] == report["B"] == 6
        assert report["hash_free_bits"] == report["symbolic_hash_free_bits"] == 0
        assert report["complete"]
        assert actual_solutions(report) == ({u: fiber[u]} if u in fiber else {})
        assert_receipt(report)
    zero = cell.enumerate_cell(problem, indices, h, rows, 0)
    assert actual_solutions(zero) == {0: (0, 0, 0, 0)}


@pytest.mark.parametrize("rows,rhs", [((), 0), ((0, 0), 0), ((0, 0), 1)])
def test_zero_width_projection_never_builds_bitvec_zero(rows, rhs):
    problem = instance(2, "0")
    report = cell.enumerate_cell(problem, (3,), (0,), rows, rhs)
    assert report["complete"]
    assert report["B"] == report["hash_rank"] == report["hash_free_bits"] == 0
    assert actual_solutions(report) == ({0: (0,)} if rhs == 0 else {})
    assert_receipt(report)


def test_native_empty_fiber_is_complete_even_with_consistent_hash():
    problem = instance(2, "0")
    problem["targets"][1] = 1
    report = cell.enumerate_cell(problem, (0, 1), (0,), (), 0)
    assert report["hash_system"]["consistent"]
    assert report["complete"] and report["solutions"] == []
    assert report["solver_call_counts"] == {"SAT": 0, "UNSAT": 1, "UNKNOWN": 0}
    assert_receipt(report)


@pytest.mark.parametrize("cap", [0, 1, 4])
def test_model_cap_is_partial_even_when_the_list_happens_to_be_exhaustive(cap):
    problem = instance(2, "0")
    report = cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0, max_models=cap)
    expected = direct_fibers(problem, (0, 1, 2))[(0,)]
    assert not report["complete"] and report["status"] == "PARTIAL"
    assert report["stop_reason"] == "max_models"
    assert report["model_count"] == cap
    assert actual_solutions(report).items() <= expected.items()
    assert report["solver_call_counts"] == {"SAT": cap, "UNSAT": 0, "UNKNOWN": 0}
    assert_receipt(report)


def test_real_resource_limit_unknown_never_becomes_empty_complete():
    problem = instance(5, "1")
    report = cell.enumerate_cell(problem, tuple(range(5)), (0, 0, 0), (), 0,
                                 timeout_ms=1000, resource_limit=1)
    assert report["status"] == "UNKNOWN" and not report["complete"]
    assert report["stop_reason"] == "solver_unknown" and report["reason_unknown"]
    assert report["solutions"] == []
    assert report["solver_call_counts"] == {"SAT": 0, "UNSAT": 0, "UNKNOWN": 1}
    assert report["solver_calls"][-1]["solver_statistics"]
    assert_receipt(report)


class SolverProxy:
    def __init__(self, solver):
        self.solver = solver

    def __getattr__(self, name):
        return getattr(self.solver, name)


def install_proxy(monkeypatch, cls):
    original = cell._make_solver
    proxies = []

    def make(*args):
        proxy = cls(original(*args))
        proxies.append(proxy)
        return proxy

    monkeypatch.setattr(cell, "_make_solver", make)
    return proxies


def test_unknown_after_a_model_retains_only_a_verified_partial_subset(monkeypatch):
    class UnknownSecond(SolverProxy):
        calls = 0

        def check(self):
            self.calls += 1
            return self.solver.check() if self.calls == 1 else z3.unknown

        def reason_unknown(self):
            return "controlled timeout"

    install_proxy(monkeypatch, UnknownSecond)
    problem = instance(2, "0")
    report = cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["model_count"] == 1
    assert report["reason_unknown"] == "controlled timeout"
    assert actual_solutions(report).items() <= direct_fibers(problem, (0, 1, 2))[(0,)].items()
    assert [call["status"] for call in report["solver_calls"]] == ["SAT", "UNKNOWN"]
    assert_receipt(report)


def test_one_deadline_decreases_and_includes_verification_not_setup(monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(cell, "perf_counter", lambda: clock[0])
    verify = cell._verify_projection
    eliminate = cell.vandermonde_eliminate_residual

    def costly_setup(*args):
        clock[0] += 1.0
        return eliminate(*args)

    def costly_verify(*args):
        clock[0] += 0.003
        return verify(*args)

    class Timed(SolverProxy):
        def set(self, **kwargs):
            # Simulated clock tests budget allocation, not machine-speed timing.
            self.solver.set(timeout=5000)

        def check(self):
            clock[0] += 0.004
            return self.solver.check()

    install_proxy(monkeypatch, Timed)
    monkeypatch.setattr(cell, "vandermonde_eliminate_residual", costly_setup)
    monkeypatch.setattr(cell, "_verify_projection", costly_verify)
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0, timeout_ms=10)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["stop_reason"] == "enumeration_deadline"
    assert report["model_count"] == 2
    calls = report["solver_calls"]
    assert 1 <= calls[1]["timeout_ms"] < calls[0]["timeout_ms"] <= 10
    assert report["setup_seconds"] == 1.0
    assert report["check_seconds"] == pytest.approx(0.008)
    assert report["verification_seconds"] == pytest.approx(0.006)
    assert report["first_verified_model_seconds"] == pytest.approx(1.007)
    assert_receipt(report)


def test_completion_timestamp_includes_setup_and_empty_cells_have_no_first_model(monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(cell, "perf_counter", lambda: clock[0])
    encode = cell._encode

    def timed_encode(*args):
        clock[0] += 2.0
        return encode(*args)

    class Timed(SolverProxy):
        def check(self):
            clock[0] += 0.1
            return self.solver.check()

    install_proxy(monkeypatch, Timed)
    monkeypatch.setattr(cell, "_encode", timed_encode)
    problem = instance(2, "0")
    complete = cell.enumerate_cell(problem, (0, 1, 2), (0,), (1, 2), 0)
    assert complete["first_verified_model_seconds"] == pytest.approx(2.1)
    assert complete["completion_seconds"] == pytest.approx(2.2)
    assert_receipt(complete)
    empty = cell.enumerate_cell(problem, (0, 1, 2), (0,), (0,), 1)
    assert empty["first_verified_model_seconds"] is None
    assert empty["completion_seconds"] == pytest.approx(2.1)
    assert_receipt(empty)


@pytest.mark.parametrize("stage", [
    "check", "statistics", "model_extraction", "projected_blocking", "set_timeout", "reason_unknown",
])
def test_backend_exceptions_keep_verified_partial_records_visible(monkeypatch, stage):
    class Broken(SolverProxy):
        calls = 0

        def set(self, **kwargs):
            if stage == "set_timeout" and self.calls:
                raise RuntimeError("controlled set_timeout failure")
            self.solver.set(**kwargs)

        def check(self):
            self.calls += 1
            if self.calls == 2:
                if stage == "check":
                    raise RuntimeError("controlled check failure")
                if stage == "reason_unknown":
                    return z3.unknown
            return self.solver.check()

        def statistics(self):
            if stage == "statistics" and self.calls == 2:
                raise RuntimeError("controlled statistics failure")
            return self.solver.statistics()

        def model(self):
            if stage == "model_extraction" and self.calls == 2:
                raise RuntimeError("controlled model_extraction failure")
            return self.solver.model()

        def add(self, *constraints):
            if stage == "projected_blocking" and self.calls:
                raise RuntimeError("controlled projected_blocking failure")
            self.solver.add(*constraints)

        def reason_unknown(self):
            raise RuntimeError("controlled reason_unknown failure")

    install_proxy(monkeypatch, Broken)
    problem = instance(2, "0")
    report = cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0)
    assert not report["complete"] and report["status"] == "PARTIAL"
    assert report["stop_reason"] == "backend_error"
    assert report["backend_errors"] == [
        {"stage": stage, "type": "RuntimeError", "message": f"controlled {stage} failure"}]
    assert report["model_count"] == 1
    assert actual_solutions(report).items() <= direct_fibers(problem, (0, 1, 2))[(0,)].items()
    assert report["solver_check_errors"] == int(stage == "check")
    assert_receipt(report)


@pytest.mark.parametrize("stage", ["solver_setup", "encoding", "check"])
def test_backend_exceptions_before_any_model_are_unknown_not_unsat(monkeypatch, stage):
    def fail(*args):
        raise RuntimeError("controlled initial failure")

    if stage == "solver_setup":
        monkeypatch.setattr(cell, "_make_solver", fail)
    elif stage == "encoding":
        monkeypatch.setattr(cell, "_encode", fail)
    else:
        class Broken(SolverProxy):
            def check(self):
                fail()

        install_proxy(monkeypatch, Broken)
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0)
    assert report["status"] == "UNKNOWN" and not report["complete"]
    assert report["stop_reason"] == "backend_error"
    assert report["backend_errors"] == [
        {"stage": stage, "type": "RuntimeError", "message": "controlled initial failure"}]
    assert report["solutions"] == []
    assert report["first_verified_model_seconds"] is report["completion_seconds"] is None
    assert_receipt(report)


def test_blocking_mentions_only_projected_u_and_duplicate_models_fail_closed(monkeypatch):
    class Recorder(SolverProxy):
        def __init__(self, solver):
            super().__init__(solver)
            self.additions = []

        def add(self, *constraints):
            self.additions.extend(constraints)
            self.solver.add(*constraints)

    proxies = install_proxy(monkeypatch, Recorder)
    problem = instance(2, "0")
    report = cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0)
    assert report["complete"] and report["model_count"] == 4
    for block in proxies[0].additions[-4:]:
        assert z3.is_or(block)
        assert {str(v) for v in get_vars(block)} == {"hash_free_0", "hash_free_1"}

    class RepeatModel(SolverProxy):
        cached_model = None

        def check(self):
            if self.cached_model is None:
                outcome = self.solver.check()
                self.cached_model = self.solver.model()
                return outcome
            return z3.sat

        def model(self):
            return self.cached_model

    install_proxy(monkeypatch, RepeatModel)
    duplicate = cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0)
    assert not duplicate["complete"] and duplicate["status"] == "PARTIAL"
    assert duplicate["stop_reason"] == "duplicate_projected_model"
    assert duplicate["duplicate_models"] == 1 and duplicate["model_count"] == 1
    assert_receipt(duplicate)


def test_independent_field_verification_rejects_wrong_elimination(monkeypatch):
    original = cell.vandermonde_eliminate_residual

    def incorrect(*args):
        pivots, free, constants, coefficients = original(*args)
        return pivots, free, (constants[0] ^ 1,), coefficients

    monkeypatch.setattr(cell, "vandermonde_eliminate_residual", incorrect)
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0)
    assert not report["complete"] and report["status"] == "UNKNOWN"
    assert report["stop_reason"] == "invalid_model" and report["invalid_models"] == 1
    assert report["solutions"] == []
    assert "original_residual_syndrome_failed" in report["solver_calls"][0]["verification_errors"]
    assert_receipt(report)


def test_independent_verifier_checks_original_hash_and_symbolic_word():
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (1, 2), 0)
    assert actual_solutions(report) == {0: (0, 0, 0)}
    _, errors = cell._verify_projection(report, 1, [0, 0, 0])
    assert "original_hash_failed" in errors
    assert "symbolic_model_disagrees_with_field_decode" in errors


@pytest.mark.parametrize("argument,value", [
    ("indices", (0, 0, 2)), ("indices", ()), ("indices", (0, 4)),
    ("indices", (0, -1)), ("indices", (True, 1)), ("indices", (0, 1.0)),
    ("indices", {0, 1}), ("indices", "012"), ("indices", None),
    ("target_syndrome", ()), ("target_syndrome", (0, 0)),
    ("target_syndrome", (-1,)), ("target_syndrome", (4,)),
    ("target_syndrome", (True,)), ("target_syndrome", (0.0,)),
    ("target_syndrome", "0"), ("target_syndrome", None),
    ("hash_rows", (4,)), ("hash_rows", (-1,)), ("hash_rows", (True,)),
    ("hash_rows", (1.0,)), ("hash_rows", {1}), ("hash_rows", "1"),
    ("hash_rhs", 2), ("hash_rhs", -1), ("hash_rhs", True), ("hash_rhs", 0.0),
])
def test_reject_malformed_indices_syndrome_and_noncanonical_hashes(argument, value):
    args = {"indices": (0, 1, 2), "target_syndrome": (0,), "hash_rows": (1,), "hash_rhs": 0}
    args[argument] = value
    with pytest.raises(ValueError):
        cell.enumerate_cell(instance(2), **args)


@pytest.mark.parametrize("key,value", [
    ("timeout_ms", 0), ("timeout_ms", True), ("resource_limit", 0),
    ("resource_limit", True), ("max_models", -1), ("max_models", True),
    ("solver_seed", -1), ("solver_seed", True),
])
def test_invalid_limits_fail_closed(key, value):
    with pytest.raises(ValueError):
        cell.enumerate_cell(instance(2), (0, 1, 2), (0,), (), 0, **{key: value})


@pytest.mark.parametrize("change", [
    {"points": [0, 0, 2, 3]}, {"targets": [0, True, 0, 0]},
    {"field_modulus_coefficients": [1, 0, 1]}, {"checks": 0},
])
def test_reuses_public_instance_validation(change):
    problem = instance(2)
    problem.update(change)
    with pytest.raises(ValueError):
        cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0)


def test_inputs_are_preserved_and_report_snapshot_is_detached():
    problem = instance(4)
    indices, h, rows = [12, 2, 9, 0], [3, 7], [1, 1, 0, 8]
    before = deepcopy((problem, indices, h, rows))
    report = cell.enumerate_cell(problem, indices, h, rows, 3)
    assert (problem, indices, h, rows) == before
    assert report["instance"] == problem
    assert report["residual_indices"] == indices and report["residual_syndrome"] == h
    assert report["hash_rows"] == rows
    assert len(report["instance_sha256"]) == 64
    report["instance"]["points"][0] ^= 1
    report["instance"]["targets"][0] ^= 1
    report["instance"]["field_modulus_coefficients"][0] ^= 1
    report["residual_indices"].reverse()
    report["residual_syndrome"][0] ^= 1
    report["hash_rows"][0] ^= 1
    assert (problem, indices, h, rows) == before


@pytest.mark.parametrize("mode", ["0", "1", "mixed"])
@pytest.mark.parametrize("h", [(0, 0), (3, 7)])
def test_known_seed_complete_native_hash_slices_match_direct_words(mode, h):
    problem, indices = instance(4, mode), (12, 2, 9, 0)
    before = deepcopy(problem)
    fiber = direct_fibers(problem, indices)[h]
    assert fiber
    for known_u in (min(fiber), max(fiber)):
        for rows in ((), (0, 0), (3, 3, 0, 24), (1, 2, 4, 8, 16, 32)):
            rhs = hash_value(rows, known_u)
            report = cell.enumerate_cell(problem, indices, h, rows, rhs, known_u=known_u)
            expected = {u: word for u, word in fiber.items() if hash_value(rows, u) == rhs}
            assert report["complete"]
            assert actual_solutions(report) == expected
            assert report["seed_model_count"] == 1
            assert report["solver_model_count"] == len(expected)-1
            assert report["solutions"][0] == {
                "u": known_u, "residual_word": list(fiber[known_u]),
                "independently_verified": True, "origin": "external_seed"}
            assert all(call.get("projected_u") != known_u for call in report["solver_calls"])
            assert_receipt(report)
    assert problem == before


@pytest.mark.parametrize("known_u", [-1, 4, True, False, 0.0, "0", [], {}])
def test_known_seed_must_be_a_canonical_coordinate(known_u):
    with pytest.raises(ValueError, match="known_u"):
        cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0, known_u=known_u)


@pytest.mark.parametrize("bad_relation", ["native", "hash", "inconsistent_hash"])
def test_known_seed_must_satisfy_original_native_and_hash_relations(monkeypatch, bad_relation):
    def no_solver(*args):
        pytest.fail("invalid seed reached solver setup")

    monkeypatch.setattr(cell, "_make_solver", no_solver)
    problem = instance(2, "0")
    if bad_relation == "native":
        problem["targets"][0] = 1
        rows, rhs, known_u, error = (), 0, 0, "original_inverse_trace_failed"
    elif bad_relation == "hash":
        rows, rhs, known_u, error = (1,), 0, 1, "original_hash_failed"
    else:
        rows, rhs, known_u, error = (1, 1), 1, 0, "original_hash_failed"
    with pytest.raises(ValueError, match=error):
        cell.enumerate_cell(problem, (0, 1, 2), (0,), rows, rhs, known_u=known_u)


def test_known_seed_is_checked_against_original_syndrome_not_only_elimination(monkeypatch):
    original = cell.vandermonde_eliminate_residual

    def incorrect(*args):
        pivots, free, constants, coefficients = original(*args)
        return pivots, free, (constants[0] ^ 1,), coefficients

    monkeypatch.setattr(cell, "vandermonde_eliminate_residual", incorrect)
    with pytest.raises(ValueError, match="original_residual_syndrome_failed"):
        cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0, known_u=0)


@pytest.mark.parametrize("indices,rows,known_u", [((0, 1, 2), (1, 2), 2), ((3,), (), 0)])
def test_seed_is_preblocked_and_singleton_completes_on_first_unsat(indices, rows, known_u):
    report = cell.enumerate_cell(instance(2, "0"), indices, (0,), rows,
                                 hash_value(rows, known_u), known_u=known_u)
    assert report["complete"] and report["model_count"] == 1
    assert report["seed_model_count"] == 1 and report["solver_model_count"] == 0
    assert report["solver_call_counts"] == {"SAT": 0, "UNSAT": 1, "UNKNOWN": 0}
    assert report["projected_blocks"] == 1
    assert report["first_solver_model_seconds"] is None
    assert report["completion_seconds"] is not None
    assert_receipt(report)


@pytest.mark.parametrize("cap", [1, 2, 4])
def test_seed_counts_toward_model_cap_without_claiming_completion(cap):
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0,
                                 known_u=2, max_models=cap)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["stop_reason"] == "max_models"
    assert report["model_count"] == cap and report["seed_model_count"] == 1
    assert report["solver_model_count"] == cap-1
    assert report["solver_call_counts"] == {"SAT": cap-1, "UNSAT": 0, "UNKNOWN": 0}
    assert report["solutions"][0]["u"] == 2
    assert_receipt(report)


def test_seed_rejects_zero_model_cap_and_singleton_cap_stays_partial():
    problem = instance(2, "0")
    with pytest.raises(ValueError, match="known_u requires max_models"):
        cell.enumerate_cell(problem, (0, 1, 2), (0,), (), 0, known_u=0, max_models=0)
    report = cell.enumerate_cell(problem, (0, 1, 2), (0,), (1, 2), 0,
                                 known_u=0, max_models=1)
    assert report["status"] == "PARTIAL" and report["stop_reason"] == "max_models"
    assert report["solver_calls"] == [] and not report["complete"]
    assert report["first_solver_model_seconds"] is report["completion_seconds"] is None
    assert_receipt(report)


def test_seed_survives_real_resource_limit_unknown_without_solver_found_credit():
    problem = instance(5, "0")
    report = cell.enumerate_cell(problem, tuple(range(5)), (0, 0, 0), (), 0,
                                 known_u=0, resource_limit=1)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["stop_reason"] == "solver_unknown" and report["reason_unknown"]
    assert actual_solutions(report) == {0: (0, 0, 0, 0, 0)}
    assert report["seed_model_count"] == 1 and report["solver_model_count"] == 0
    assert report["solver_call_counts"] == {"SAT": 0, "UNSAT": 0, "UNKNOWN": 1}
    assert report["first_solver_model_seconds"] is report["completion_seconds"] is None
    assert_receipt(report)


def test_backend_returning_seed_again_never_counts_it_as_solver_found(monkeypatch):
    # Simulate a backend failing to honor the supplied projected block.
    monkeypatch.setattr(cell, "_block_projection", lambda *args: None)
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (1, 2), 2, known_u=2)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["stop_reason"] == "duplicate_projected_model"
    assert report["duplicate_models"] == 1
    assert report["seed_model_count"] == 1 and report["solver_model_count"] == 0
    assert report["model_count"] == 1 and report["first_solver_model_seconds"] is None
    assert report["solver_call_counts"] == {"SAT": 1, "UNSAT": 0, "UNKNOWN": 0}
    assert report["solver_calls"][0]["projected_u"] == 2
    assert_receipt(report)


def test_seed_and_solver_model_survive_later_unknown_with_distinct_timings(monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(cell, "perf_counter", lambda: clock[0])
    verify = cell._verify_projection
    encode = cell._encode

    def timed_verify(*args):
        clock[0] += 0.1
        return verify(*args)

    def timed_encode(*args):
        clock[0] += 1.0
        return encode(*args)

    class UnknownSecond(SolverProxy):
        calls = 0

        def check(self):
            self.calls += 1
            clock[0] += 0.2
            return self.solver.check() if self.calls == 1 else z3.unknown

        def reason_unknown(self):
            return "controlled timeout"

    install_proxy(monkeypatch, UnknownSecond)
    monkeypatch.setattr(cell, "_verify_projection", timed_verify)
    monkeypatch.setattr(cell, "_encode", timed_encode)
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0, known_u=0)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["seed_model_count"] == report["solver_model_count"] == 1
    assert report["first_verified_model_seconds"] == pytest.approx(0.1)
    assert report["first_solver_model_seconds"] == pytest.approx(1.4)
    assert report["verification_seconds"] == pytest.approx(0.2)
    assert report["seed_verification_seconds"] == pytest.approx(0.1)
    assert report["stop_reason"] == "solver_unknown"
    assert [s["origin"] for s in report["solutions"]] == ["external_seed", "solver"]
    assert_receipt(report)


@pytest.mark.parametrize("stage", ["solver_setup", "seed_projected_blocking"])
def test_seed_survives_backend_setup_or_preblocking_exception(monkeypatch, stage):
    def fail(*args):
        raise RuntimeError("controlled seed failure")

    if stage == "solver_setup":
        monkeypatch.setattr(cell, "_make_solver", fail)
    else:
        monkeypatch.setattr(cell, "_block_projection", fail)
    report = cell.enumerate_cell(instance(2, "0"), (0, 1, 2), (0,), (), 0, known_u=1)
    assert report["status"] == "PARTIAL" and not report["complete"]
    assert report["stop_reason"] == "backend_error"
    assert report["backend_errors"][0]["stage"] == stage
    assert report["seed_model_count"] == 1 and report["solver_model_count"] == 0
    assert report["model_count"] == 1 and report["solver_calls"] == []
    assert_receipt(report)

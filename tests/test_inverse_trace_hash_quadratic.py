"""Bounded exact field and certificate controls for the degree-two sidecar."""

from copy import deepcopy
from itertools import product
import json
from random import Random

import pytest
from flint import nmod_mat

from theorems.explicit_quadratic_opi import element, encoded, field
import theorems.inverse_trace_hash_quadratic as quadratic


def instance(bits=2, targets=(0, 1, 0, 0), checks=1):
    return {"bits": bits, "points": list(range(len(targets))), "targets": list(targets),
            "checks": checks,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}


def affine_value(mask, assignment):
    return (mask & 1) ^ (((mask >> 1) & assignment).bit_count() & 1)


def model_from_report(report):
    maps = report["affine_maps"]
    return {"x": [[int(a, 16) for a in word] for word in maps["x_bits_hex"]],
            "y": [[int(a, 16) for a in word] for word in maps["y_bits_hex"]],
            "u": [int(a, 16) for a in maps["u_bits_hex"]], "variable_order": maps["variable_order"]}


def model_values(model, assignment):
    values = []
    for name in ("x", "y"):
        values.append([sum(affine_value(a, assignment) << j for j, a in enumerate(word))
                       for word in model[name]])
    u = sum(affine_value(a, assignment) << j for j, a in enumerate(model["u"]))
    return *values, u


def lift(assignment, variables):
    result, column = 1 | (assignment << 1), 1+variables
    for i in range(variables):
        for j in range(i+1, variables):
            result |= (((assignment >> i) & (assignment >> j)) & 1) << column
            column += 1
    return result


def independent_syndrome(problem, indices, word):
    bits = problem["bits"]
    return tuple(encoded(sum((element(bits, problem["points"][i])**j*element(bits, x)
                              for i, x in zip(indices, word)), field(bits).zero()))
                 for j in range(problem["checks"]))


def hash_value(rows, u):
    return sum(((row & u).bit_count() % 2) << j for j, row in enumerate(rows))


def direct_cell(problem, indices, h, rows, rhs):
    """Tiny actual-field word enumeration, independent of all affine maps."""
    bits, checks = problem["bits"], problem["checks"]
    assert bits <= 3 and len(indices) <= 3
    inverse = [encoded(element(bits, x)**-1) if x else 0 for x in range(1 << bits)]
    traces = [int(element(bits, y).trace()) for y in range(1 << bits)]
    pivot = next(j for j in range(bits) if traces[1 << j])
    positions = [j for j in range(bits) if j != pivot]
    alphabets = [[x for x in range(1 << bits) if traces[inverse[x]] == problem["targets"][i]]
                 for i in indices]
    result = set()
    for word in product(*alphabets):
        if independent_syndrome(problem, indices, word) != tuple(h):
            continue
        u = sum(((inverse[x] >> j) & 1) << (s*(bits-1)+l)
                for s, x in enumerate(word[checks:]) for l, j in enumerate(positions))
        if hash_value(rows, u) == rhs:
            result.add((u, word))
    return result


def assert_receipt(report):
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert report["processed_row_count"] <= report["compiled_row_count"] <= report["expected_row_count"]
    assert report["row_rank"] <= min(report["processed_row_count"], report["row_span_columns"])
    assert len(report["row_ids"]) == report["compiled_row_count"]
    assert len(report["rows_sha256"]) == len(report["cell_sha256"]) == 64
    assert len(report["source_sha256"]) == 64
    assert not report["field_enumerated"]
    assert not report["groebner_basis_computed"] and not report["degree_growth_performed"]
    assert not report["hardness_evidence"] and not report["polynomial_enumeration_established"]
    assert not report["uniform_sampler"] and not report["whole_workflow_wall_clock_cap_enforced"]
    assert all(value >= 0 for key, value in report.items() if key.endswith("_seconds"))
    assert "solutions" not in report and "witness" not in report and "cell_cardinality" not in report
    if report["native_cell_empty_certified"]:
        assert report["certificate_verified"] and report["unit_in_row_span"] is True
        assert quadratic.verify_certificate(report)
        assert report["status"] in ("CERTIFIED_AFFINE_CONTRADICTION", "CERTIFIED_QUADRATIC_CONTRADICTION")
        assert not report["quadratic_relaxation_feasible_certified"]
        assert report["relaxation_certificate"] is None
        assert not quadratic.verify_relaxation_certificate(report)
    else:
        assert report["certificate"] is None and not report["certificate_verified"]
        assert not quadratic.verify_certificate(report)
        if report["row_span_complete"]:
            assert report["status"] == "INCONCLUSIVE_QUADRATIC_RELAXATION"
            assert report["unit_in_row_span"] is False
            assert report["quadratic_relaxation_feasible_certified"]
            assert quadratic.verify_relaxation_certificate(report)
        else:
            assert report["status"] == "UNKNOWN_CAP"
            assert report["unit_in_row_span"] is None
            assert not report["quadratic_relaxation_feasible_certified"]
            assert report["relaxation_certificate"] is None
            assert not quadratic.verify_relaxation_certificate(report)


@pytest.mark.parametrize("variables", [0, 1, 2, 3])
def test_affine_product_uses_boolean_diagonal_and_exact_pair_order(variables):
    for a, b in product(range(1 << (variables+1)), repeat=2):
        row = quadratic._affine_product(a, b, variables)
        for assignment in range(1 << variables):
            assert ((row & lift(assignment, variables)).bit_count() & 1) == (
                affine_value(a, assignment)*affine_value(b, assignment))


@pytest.mark.parametrize("bits,indices,h,rows,rhs", [
    (2, (2, 0, 3), (3,), (1, 1, 0), 3),
    (3, (3, 0, 2), (5,), (3, 12), 2),
    (4, (6, 1, 4, 0), (3, 7), (3, 6, 12, 24), 5),
])
@pytest.mark.parametrize("strengthen", [False, True])
def test_every_substituted_component_matches_independent_field_evaluation(
        bits, indices, h, rows, rhs, strengthen):
    problem = instance(bits, tuple(i % 2 for i in range(max(indices)+1)), len(h))
    report = quadratic.analyze_cell(problem, indices, h, rows, rhs, strengthen_target_one=strengthen)
    assert report["row_span_complete"]
    model = model_from_report(report)
    compiled = list(quadratic._quadratic_rows(report, model, strengthen, lambda stage: None))
    assert len(compiled) == report["polynomial_rows_raw"]
    rng = Random(1029)
    for _ in range(32):
        assignment = rng.getrandbits(report["variable_count"])
        x_words, y_words, u = model_values(model, assignment)
        assert independent_syndrome(problem, indices, x_words) == h
        assert hash_value(rows, u) == rhs
        residuals = {}
        for i, x_word, y_word in zip(indices, x_words, y_words):
            x, y = element(bits, x_word), element(bits, y_word)
            assert int(y.trace()) == problem["targets"][i]
            values = (x*x*y+x, x*y*y+y, x**4*y+x**3, x*y**4+y**3, (x*y)**2+x*y, x*y+1)
            for name, value in zip((*quadratic.IDENTITIES, "xy_plus_one"), values):
                residuals[i, name] = encoded(value)
        lifted = lift(assignment, report["variable_count"])
        for identifier, row in compiled:
            wanted = (residuals[identifier["coordinate"], identifier["identity"]] >> identifier["component"]) & 1
            assert (row & lifted).bit_count() % 2 == wanted
    assert_receipt(report)


@pytest.mark.parametrize("targets", list(product((0, 1), repeat=3)))
@pytest.mark.parametrize("h", [0, 1, 3])
def test_exact_tiny_solution_sets_including_zero_and_nonzero_syndromes(targets, h):
    problem, indices = instance(2, targets+(0,)), (0, 1, 2)
    for rows, rhs in (((), 0), ((1, 1, 0), 0), ((1, 1, 0), 3), ((1, 2), 2)):
        report = quadratic.analyze_cell(problem, indices, (h,), rows, rhs)
        model = model_from_report(report)
        compiled = [row for _, row in quadratic._quadratic_rows(report, model, True, lambda stage: None)]
        actual = set()
        for assignment in range(1 << report["variable_count"]):
            lifted = lift(assignment, report["variable_count"])
            if all((row & lifted).bit_count() % 2 == 0 for row in compiled):
                x, _, u = model_values(model, assignment)
                actual.add((u, tuple(x)))
        expected = direct_cell(problem, indices, (h,), rows, rhs)
        assert actual == expected
        if expected:
            assert not report["native_cell_empty_certified"]
        assert_receipt(report)


def test_zero_branch_is_retained_and_target_one_product_is_not_added_there():
    problem = instance(3, (0, 0, 0, 0))
    report = quadratic.analyze_cell(problem, (0, 1, 2), (0,), (1, 1, 0), 0)
    assert report["status"] == "INCONCLUSIVE_QUADRATIC_RELAXATION"
    assert report["polynomial_rows_raw"] == 5*3*3
    assert all(row["identity"] != "xy_plus_one" for row in report["row_ids"])
    model = model_from_report(report)
    assert model_values(model, 0) == ([0, 0, 0], [0, 0, 0], 0)
    assert all(row & 1 == 0 for _, row in quadratic._quadratic_rows(report, model, True, lambda stage: None))
    assert_receipt(report)


def test_explicit_empty_native_fixture_has_independently_replayable_unit():
    problem = instance()
    report = quadratic.analyze_cell(problem, (0, 1), (0,), (), 0)
    assert direct_cell(problem, (0, 1), (0,), (), 0) == set()
    assert report["status"] == "CERTIFIED_QUADRATIC_CONTRADICTION"
    model = model_from_report(report)
    rows = list(quadratic._quadratic_rows(report, model, True, lambda stage: None))
    value = 0
    for position, identifier in zip(report["certificate"]["row_indices"], report["certificate"]["row_ids"]):
        assert rows[position][0] == identifier
        value ^= rows[position][1]
    assert value == 1
    # Replay is independent of the Gaussian basis and its claimed rank.
    copy = deepcopy(report)
    copy["row_rank"] = 0
    assert quadratic.verify_certificate(copy)
    assert_receipt(report)


@pytest.mark.parametrize("strengthen", [False, True])
def test_row_rank_matches_independent_flint_matrix_rank(strengthen):
    report = quadratic.analyze_cell(instance(), (0, 1, 2), (3,), (1, 1), 3,
                                    strengthen_target_one=strengthen)
    model = model_from_report(report)
    rows = [row for _, row in quadratic._quadratic_rows(report, model, strengthen, lambda stage: None)]
    matrix = nmod_mat([[(row >> j) & 1 for j in range(report["monomial_columns"])] for row in rows], 2)
    assert matrix.rank() == report["row_rank"]


def test_known_nonzero_native_solution_cannot_yield_unit_on_induced_nonzero_syndrome():
    problem, indices = instance(5, (1,)*25, 3), (9, 3, 17, 1)
    word = (1,)*4
    h = independent_syndrome(problem, indices, word)
    assert any(h)
    report = quadratic.analyze_cell(problem, indices, h, (3,), 0)
    assert report["status"] == "INCONCLUSIVE_QUADRATIC_RELAXATION"
    model = model_from_report(report)
    # In odd degree Tr(1)=1; the canonical accepted-root coordinates of y=1 are zero.
    assignment = sum(1 << j for j, v in enumerate(model["variable_order"])
                     if v["kind"] == "x_free" and v["bit"] == 0)
    assert model_values(model, assignment) == ([1]*4, [1]*4, 0)
    lifted = lift(assignment, report["variable_count"])
    assert all((row & lifted).bit_count() % 2 == 0
               for _, row in quadratic._quadratic_rows(report, model, True, lambda stage: None))
    assert_receipt(report)


@pytest.mark.parametrize("change", ["combination", "duplicate", "boolean", "identity", "component",
                                         "coordinate", "cell", "xor", "rows_digest", "map", "syndrome"])
def test_tampered_certificates_and_source_rows_are_rejected(change):
    report = quadratic.analyze_cell(instance(), (0, 1), (0,), (), 0)
    cert = report["certificate"]
    if change == "combination":
        cert["row_indices"].pop()
    elif change == "duplicate":
        cert["row_indices"].append(cert["row_indices"][-1])
    elif change == "boolean":
        cert["row_indices"][0] = True
    elif change in ("identity", "component", "coordinate"):
        cert["row_ids"][0][change] = "wrong" if change == "identity" else 99
    elif change == "cell":
        cert["cell_sha256"] = "0"*64
    elif change == "xor":
        cert["xor_hex"] = "0x0"
    elif change == "rows_digest":
        report["rows_sha256"] = "0"*64
    elif change == "map":
        report["affine_maps"]["x_bits_hex"][0][0] = "0x0"
    else:
        report["residual_syndrome"][0] = 1
    assert not quadratic.verify_certificate(report)


@pytest.mark.parametrize("rows,rhs", [((1, 1, 0), 1), ((0,), 1)])
def test_raw_hash_inconsistency_has_separate_original_row_certificate(monkeypatch, rows, rhs):
    def forbidden(*args):
        pytest.fail("contradictory raw hash must not compile field identities")

    monkeypatch.setattr(quadratic, "compiled_relations", forbidden)
    report = quadratic.analyze_cell(instance(), (0, 1), (0,), rows, rhs, max_monomials=1)
    assert report["status"] == "CERTIFIED_AFFINE_CONTRADICTION"
    assert not report["hash_consistent"] and report["affine_maps"] is None
    assert report["polynomial_rows_processed"] == 0
    mask, value = 0, 0
    for identifier in report["certificate"]["row_ids"]:
        j = identifier["hash_row"]
        mask ^= rows[j]
        value ^= (rhs >> j) & 1
    assert (mask, value) == (0, 1)
    assert_receipt(report)


def test_n17_dimension_cap_reports_680_variables_and_231541_columns_without_compiling(monkeypatch):
    problem = instance(17, (1,)*289, 36)
    def forbidden(*args):
        pytest.fail("monomial cap must precede affine-map/field-row construction")

    monkeypatch.setattr(quadratic, "_build_maps", forbidden)
    report = quadratic.analyze_cell(problem, tuple(range(40)), (0,)*36,
                                    tuple(1 << j for j in range(28)), 0, max_monomials=231540)
    assert report["variable_count"] == 680
    assert report["monomial_columns"] == 231541
    assert report["polynomial_rows_raw"] == 6*17*40
    assert report["hash_rank"] == 28
    assert report["status"] == "UNKNOWN_CAP" and report["stop_reason"] == "monomial_column_cap"
    assert report["compiled_row_count"] == report["processed_row_count"] == 0
    assert_receipt(report)


@pytest.mark.parametrize("rows,variables", [((), 7), ((1, 1), 6), ((1, 2), 5)])
def test_variable_formula_uses_actual_hash_rank_not_forced_rank(rows, variables):
    report = quadratic.analyze_cell(instance(), (0, 1, 2), (0,), rows, 0)
    assert report["variable_count"] == variables
    assert report["hash_rows"] == list(rows)
    assert_receipt(report)


@pytest.mark.parametrize("indices,rows,rhs", [((0,), (), 0), ((0,), (0,), 1)])
def test_zero_width_hash_coordinates(indices, rows, rhs):
    report = quadratic.analyze_cell(instance(2, (0, 0, 0, 0)), indices, (0,), rows, rhs)
    assert report["B"] == 0 and report["variable_count"] == 1
    assert report["native_cell_empty_certified"] == bool(rhs)
    assert_receipt(report)


@pytest.mark.parametrize("cap,certified", [(1, False), (14, True)])
def test_row_cap_preserves_any_already_found_unit_certificate(cap, certified):
    report = quadratic.analyze_cell(instance(), (0, 1), (0,), (), 0, max_rows=cap)
    assert report["compiled_row_count"] == report["processed_row_count"] == cap
    assert not report["row_span_complete"] and report["stop_reason"] == "row_cap"
    assert report["native_cell_empty_certified"] == certified
    assert_receipt(report)


@pytest.mark.parametrize("stage", ["compilation", "elimination", "after_unit"])
def test_cooperative_timeout_never_promotes_incomplete_absence_of_unit(monkeypatch, stage):
    clock = [0.0]
    monkeypatch.setattr(quadratic, "perf_counter", lambda: clock[0])
    if stage == "compilation":
        original = quadratic.compiled_relations

        def delayed(bits):
            clock[0] += 1
            return original(bits)

        monkeypatch.setattr(quadratic, "compiled_relations", delayed)
    else:
        original = quadratic._insert

        def delayed(row, index, basis, metrics, tick):
            if stage == "elimination":
                clock[0] += 1
                tick("elimination")
            original(row, index, basis, metrics, tick)
            if stage == "after_unit" and 0 in basis:
                clock[0] += 1

        monkeypatch.setattr(quadratic, "_insert", delayed)
    report = quadratic.analyze_cell(instance(), (0, 1), (0,), (), 0, timeout_ms=1)
    assert not report["row_span_complete"]
    assert report["stop_reason"].startswith("timeout_")
    assert report["native_cell_empty_certified"] == (stage == "after_unit")
    assert report["setup_seconds"] == 0
    assert_receipt(report)


@pytest.mark.parametrize("key,value", [
    ("indices", (0, 0)), ("indices", (True, 1)), ("indices", (-1, 1)),
    ("indices", (0, 4)), ("indices", {0, 1}), ("target_syndrome", ()),
    ("target_syndrome", (0, 1)), ("target_syndrome", (True,)), ("target_syndrome", (4,)),
    ("hash_rows", (2,)), ("hash_rows", (True,)), ("hash_rows", (-1,)),
    ("hash_rhs", True), ("hash_rhs", 1), ("timeout_ms", 0), ("timeout_ms", True),
    ("max_monomials", 0), ("max_monomials", True), ("max_rows", 0),
    ("strengthen_target_one", 1),
])
def test_malformed_inputs_fail_closed(key, value):
    args = {"indices": (0, 1), "target_syndrome": (0,), "hash_rows": (), "hash_rhs": 0}
    args[key] = value
    with pytest.raises(ValueError):
        quadratic.analyze_cell(instance(), **args)


def test_input_preservation_and_detached_report():
    problem = instance(3, (0, 1, 0, 1))
    indices, h, rows = [3, 0, 2], [5], [3, 3, 0]
    original = deepcopy((problem, indices, h, rows))
    report = quadratic.analyze_cell(problem, indices, h, rows, 3)
    assert (problem, indices, h, rows) == original
    assert report["instance"] == problem and report["hash_rows"] == rows
    report["instance"]["points"][0] = 7
    report["instance"]["targets"][0] = 1
    report["instance"]["field_modulus_coefficients"][0] = 0
    report["residual_indices"].reverse()
    report["residual_syndrome"][0] = 0
    report["hash_rows"].clear()
    assert (problem, indices, h, rows) == original


def relaxation_report():
    problem = instance(3, (0, 0, 0, 0))
    return quadratic.analyze_cell(problem, (0, 1, 2), (0,), (1, 1, 0), 0)


def test_dual_certificate_replays_every_row_without_using_rank_or_basis():
    report = relaxation_report()
    cert = report["relaxation_certificate"]
    assert report["quadratic_relaxation_feasible_certified"]
    assert cert["kind"] == "quadratic_dual_relaxation"
    assert cert["width"] == report["monomial_columns"]
    assert cert["row_count"] == report["expected_row_count"]
    assert cert["formal_monomial_assignment_only"] is True
    w = int(cert["w_hex"], 16)
    assert w & 1 and w < 1 << cert["width"] and hex(w) == cert["w_hex"]
    model = model_from_report(report)
    rows = list(quadratic._quadratic_rows(report, model, True, lambda stage: None))
    assert len(rows) == cert["row_count"]
    assert all((row & w).bit_count() % 2 == 0 for _, row in rows)
    report["row_rank"] = -1  # The independently replayed witness does not trust this claim.
    assert quadratic.verify_relaxation_certificate(report)
    assert not report["native_cell_empty_certified"]


@pytest.mark.parametrize("change", ["zero", "constant_zero", "violated_row", "width", "boolean_width",
                                         "high_bit", "noncanonical_hex", "cell", "row_count", "rows_digest",
                                         "row_ids", "map", "kind", "scope"])
def test_dual_certificate_tampering_is_rejected(change):
    report = relaxation_report()
    cert = report["relaxation_certificate"]
    w = int(cert["w_hex"], 16)
    if change == "zero":
        cert["w_hex"] = "0x0"
    elif change == "constant_zero":
        cert["w_hex"] = hex(w & ~1)
    elif change == "violated_row":
        model = model_from_report(report)
        row = next(row for _, row in quadratic._quadratic_rows(report, model, True, lambda stage: None) if row >> 1)
        bit = (row & ~1) & -(row & ~1)
        cert["w_hex"] = hex(w ^ bit)
    elif change == "width":
        cert["width"] += 1
    elif change == "boolean_width":
        cert["width"] = True
    elif change == "high_bit":
        cert["w_hex"] = hex(w | (1 << cert["width"]))
    elif change == "noncanonical_hex":
        cert["w_hex"] = "0x0" + cert["w_hex"][2:]
    elif change == "cell":
        cert["cell_sha256"] = "0"*64
    elif change == "row_count":
        cert["row_count"] -= 1
    elif change == "rows_digest":
        report["rows_sha256"] = "0"*64
    elif change == "row_ids":
        report["row_ids"].pop()
    elif change == "map":
        report["affine_maps"]["x_bits_hex"][0][0] = "0x0"
    elif change == "kind":
        cert["kind"] = "native_assignment"
    else:
        cert["formal_monomial_assignment_only"] = False
    assert not quadratic.verify_relaxation_certificate(report)


def test_dual_verifier_recomputes_full_count_rejecting_self_consistent_subset_receipt():
    report = relaxation_report()
    model = model_from_report(report)
    rows = list(quadratic._quadratic_rows(report, model, True, lambda stage: None))[:-1]
    # Even a matching hash, ID list, and all forged counters cannot hide an omitted row.
    for key in ("expected_row_count", "compiled_row_count", "processed_row_count",
                "polynomial_rows_raw", "polynomial_rows_processed"):
        report[key] = len(rows)
    report["relaxation_certificate"]["row_count"] = len(rows)
    report["row_ids"] = [identifier for identifier, _ in rows]
    digest = quadratic._row_digest(report["monomial_columns"])
    for _, row in rows:
        digest.update(row.to_bytes((report["monomial_columns"]+7)//8, "little"))
    report["rows_sha256"] = digest.hexdigest()
    assert report["row_span_complete"]
    assert not quadratic.verify_relaxation_certificate(report)


@pytest.mark.parametrize("change", ["row_cap", "column_cap", "incomplete", "timeout"])
def test_dual_verifier_rejects_cap_or_incomplete_receipts(change):
    report = relaxation_report()
    if change == "row_cap":
        report["max_rows"] = report["expected_row_count"]-1
    elif change == "column_cap":
        report["max_monomials"] = report["monomial_columns"]-1
    elif change == "incomplete":
        report["row_span_complete"] = False
    else:
        report["stop_reason"] = "timeout_elimination"
    assert not quadratic.verify_relaxation_certificate(report)


@pytest.mark.parametrize("change", ["omit", "extra"])
def test_dual_verifier_checks_actual_generator_coverage_not_only_report_counters(monkeypatch, change):
    report = relaxation_report()
    original = quadratic._quadratic_rows

    def incorrect(*args):
        rows = list(original(*args))
        yield from rows[:-1] if change == "omit" else rows+[rows[-1]]

    monkeypatch.setattr(quadratic, "_quadratic_rows", incorrect)
    assert not quadratic.verify_relaxation_certificate(report)


def test_dual_replay_time_is_charged_and_bad_replay_fails_closed(monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(quadratic, "perf_counter", lambda: clock[0])
    original = quadratic.verify_relaxation_certificate

    def delayed(*args):
        clock[0] += 0.25
        return original(*args)

    monkeypatch.setattr(quadratic, "verify_relaxation_certificate", delayed)
    report = relaxation_report()
    assert report["quadratic_relaxation_feasible_certified"]
    assert report["relaxation_verification_seconds"] == 0.25
    assert report["verification_seconds"] == report["total_seconds"] == 0.25
    monkeypatch.setattr(quadratic, "verify_relaxation_certificate", lambda *args: False)
    with pytest.raises(ArithmeticError, match="dual relaxation certificate"):
        relaxation_report()

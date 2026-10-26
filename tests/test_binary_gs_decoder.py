import ast
import hashlib
from itertools import product
import json

from flint import fq_default_poly_ctx
import pytest

from theorems.balanced_codeword_filter import filter_budget
from theorems.binary_gs_decoder import (
    REPORT, ROOT, _child, _terms, decode, exhaustive_decoder_control, gs_layout,
    large_field_control, linear_roots, polynomial_roots, report,
)
from theorems.explicit_quadratic_opi import element, encoded, field


def test_all_small_monic_polynomials_have_complete_distinct_root_lists():
    ring = fq_default_poly_ctx(field(2))
    for degree in (1, 2, 3):
        for coefficients in product(range(4), repeat=degree):
            f = ring([element(2, c) for c in coefficients+(1,)])
            expected = [x for x in range(4) if f(element(2, x)) == 0]
            roots, work = linear_roots(2, coefficients+(1,))
            assert roots == expected
            assert work["basis_cuts"] <= 2
            assert work["modular_squarings"] <= 2+2*(2-1)


@pytest.mark.parametrize("bits", [2, 3, 17, 31, 61])
def test_repeated_zero_roots_and_nonbasefield_factors_do_not_require_factorization(bits):
    ring = fq_default_poly_ctx(field(bits))
    y = ring.gen()
    trace_one = next(element(bits, 1 << j) for j in range(bits)
                     if element(bits, 1 << j).trace() != 0)
    a = element(bits, (1 << (bits-1))+1)
    no_roots = y*y+y+trace_one
    f = y**4*(y+a)**2*no_roots
    roots, work = linear_roots(bits, map(encoded, f.coeffs()))
    assert roots == [0, encoded(a)]
    assert work["basis_cuts"] <= bits
    assert work["modular_squarings"] <= bits+bits*(bits-1)
    assert linear_roots(bits, map(encoded, no_roots.coeffs()))[0] == []


def test_constant_and_zero_polynomial_have_different_contracts():
    assert linear_roots(31, [7])[0] == []
    with pytest.raises(ValueError, match="zero polynomial"):
        linear_roots(31, [0, 0])


def test_no_random_factorization_or_builtin_root_backend_is_called():
    source = (ROOT / "theorems/binary_gs_decoder.py").read_text()
    names = [node.func.attr for node in ast.walk(ast.parse(source))
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)]
    assert not set(names) & {"roots", "factor", "factor_squarefree", "random_element"}


@pytest.mark.parametrize("degree", [1, 2, 5])
def test_early_zero_root_must_not_discard_other_roots_with_same_prefix(degree):
    # Y(Y+X^degree), including a root already visible at the first node.
    terms = {(0, 2): 1, (degree, 1): 1}
    roots, ledger = polynomial_roots(3, terms, degree+1)
    expected = [(0,)*(degree+1), (0,)*degree+(1,)]
    assert roots == expected
    assert max(ledger["level_widths"]) <= 2
    assert ledger["visited_nodes"] <= ledger["node_cap"]


@pytest.mark.parametrize("coefficient_count", [1, 2, 5])
def test_truncated_prefix_is_not_a_formal_polynomial_root(coefficient_count):
    roots, _ = polynomial_roots(3, {(0, 1): 1, (coefficient_count, 0): 1}, coefficient_count)
    assert roots == []


def test_repeated_polynomial_root_and_initial_x_content_are_preserved():
    # X^3 * (Y + 2 + 3X + X^2)^4 in characteristic two.
    terms = {(3, 4): 1, (3, 0): encoded(element(3, 2)**4),
             (7, 0): encoded(element(3, 3)**4), (11, 0): 1}
    roots, ledger = polynomial_roots(3, terms, 3)
    assert roots == [(2, 3, 1)]
    assert max(ledger["specialization_degree_budgets"]) <= 4


def test_x_content_normalization_and_lucas_expansion_are_exact():
    bits = 3
    terms = _terms(bits, {(2, 0): 3, (0, 3): 4, (1, 2): 5, (0, 1): 6})
    gamma = element(bits, 5)
    child, valuation = _child(bits, terms, 5)
    for u, v in product(range(8), repeat=2):
        x, y = element(bits, u), element(bits, v)
        before = sum((c*x**i*(gamma+x*y)**j for (i, j), c in terms.items()), field(bits).zero())
        after = x**valuation*sum((c*x**i*y**j for (i, j), c in child.items()), field(bits).zero())
        assert before == after


@pytest.mark.parametrize("terms", [
    {(0, 2): 1, (1, 1): 1},
    {(0, 2): 2, (1, 1): 3, (2, 0): 1, (0, 0): 2},
    {(0, 3): 1, (3, 1): 2, (2, 0): 3},
    {(0, 0): 1, (2, 0): 1},
])
def test_rr_completeness_against_all_small_polynomial_messages(terms):
    ring = fq_default_poly_ctx(field(2))
    x = ring.gen()
    expected = []
    for coefficients in product(range(4), repeat=3):
        f = ring([element(2, c) for c in coefficients])
        value = sum((element(2, c)*x**i*f**j for (i, j), c in terms.items()), ring.zero())
        if value.is_zero():
            expected.append(coefficients)
    roots, ledger = polynomial_roots(2, terms, 3)
    assert roots == expected
    assert ledger["visited_nodes"] <= ledger["node_cap"]


@pytest.mark.parametrize("params", [(2, 3, 1, 1), (2, 3, 2, 1), (2, 4, 2, 1)])
def test_complete_decoder_and_singleton_erasure_for_every_received_word(params):
    row = exhaustive_decoder_control(*params)
    assert sum(row["list_size_histogram"].values()) == (1 << params[0])**params[1]
    assert row["retained_pairs_erased_exactly"] == row["list_size_histogram"].get("1", 0)
    if params == (2, 3, 2, 1):
        assert row["list_size_histogram"] == {"1": 16, "3": 48}


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_large_field_small_code_closes_root_backend_not_native_quantum_experiment(bits):
    row = large_field_control(bits)
    assert row["planted_message"] in row["decoded_messages"]
    assert not row["ledger"]["field_table_enumerated"]
    assert not row["ledger"]["random_factorization_used"]
    assert not row["ledger"]["coherent_receiver_executed"]
    assert not row["native_large_code_executed"]
    assert row["planted_decoder_regression_only"]


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_native_layout_agrees_with_existing_filter_and_has_bounded_tree(bits):
    n, k, w = bits*bits, bits*bits//8, 3*bits*bits//5
    row, old = gs_layout(n, k, w), filter_budget(bits, n, k, w)
    assert row["interpolation_rows"] == old["gs_interpolation_constraints"]
    assert row["interpolation_columns"] == old["gs_interpolation_monomials"]
    assert row["multiplicity"] == old["gs_multiplicity"] == 4
    assert row["rr_node_cap"] == 1+k*row["Y_degree_cap"]


@pytest.mark.parametrize("callback", [
    lambda: linear_roots(3, [True, 1]),
    lambda: linear_roots(3, [8, 1]),
    lambda: polynomial_roots(3, {}, 2),
    lambda: polynomial_roots(3, {(0, 1): 1}, 0),
    lambda: gs_layout(4, 2, 2),
    lambda: decode(3, [0, 0, 1], 1, [1, 1, 1], 1),
    lambda: decode(3, [0, 1, 2], 1, [1], 1),
    lambda: decode(17, range(289), 36, [0]*289, 173),
    lambda: exhaustive_decoder_control(17, 289, 36, 173),
])
def test_input_contracts_and_reference_caps(callback):
    with pytest.raises(ValueError):
        callback()


def test_live_artifact_binds_proof_source_and_replays_all_controls():
    data = json.loads(REPORT.read_text())
    assert data == report()
    assert data["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/binary_gs_decoder.py").read_bytes()).hexdigest()
    assert data["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/BINARY_GS_DECODER.md").read_bytes()).hexdigest()
    assert not data["random_factorization_required"]
    assert not data["coherent_receiver_implemented"]
    assert not data["quantum_speedup_established"]

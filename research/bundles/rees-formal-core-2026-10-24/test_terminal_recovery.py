from fractions import Fraction
from itertools import product
import json

import pytest

import terminal_controls as c
import verify as base
import verify_terminal_recovery as terminal


def diagnostics(names, axiom="propext"):
    return "\n".join(json.dumps({"severity": "information",
                                "data": f"'{name}' depends on axioms: [{axiom}]"}) for name in names)


def test_complete_manifest_and_audit():
    assert len(terminal.THEOREMS) == 20
    assert len(set(terminal.DECLARATIONS)) == 23
    terminal.validate_declarations((terminal.ROOT / "ReesTerminalRecovery.lean").read_text())
    assert (terminal.ROOT / "AuditTerminalRecovery.lean").read_text() == terminal.expected_audit()
    assert len(base.parse_axioms(diagnostics(terminal.DECLARATIONS), terminal.DECLARATIONS)) == 23


@pytest.mark.parametrize("missing", ["fourier_source", "readout_complete", "standard_character_faithful",
                                     "native_terminal_readout", "native_record_readout", "native_hidden_recovery"])
def test_missing_proof_rejected(missing):
    with pytest.raises(ValueError, match="incomplete"):
        base.parse_axioms(diagnostics([name for name in terminal.DECLARATIONS
                                      if name != terminal.PREFIX + missing]), terminal.DECLARATIONS)


@pytest.mark.parametrize("axiom", ["sorryAx", "AssumeCorrectFourierReadout", "AssumeSamplesSpan"])
def test_unproved_assumptions_rejected(axiom):
    with pytest.raises(ValueError, match="unapproved axiom"):
        base.parse_axioms(diagnostics(terminal.DECLARATIONS, axiom), terminal.DECLARATIONS)


def test_unlisted_source_declaration_rejected():
    source = (terminal.ROOT / "ReesTerminalRecovery.lean").read_text()
    with pytest.raises(ValueError, match="manifest"):
        terminal.validate_declarations(source + "\ndef unlisted : Nat := 0\n")


def test_claims_remain_scoped():
    report = terminal.scope_report()
    assert report["actual_native_tree_to_terminal_fourier_law_formalized"]
    assert report["finite_sample_rank_bound_is_written_not_lean_formalized"]
    for key in ("formalizes_full_Rees_algorithm", "quantum_execution", "new_algorithm_or_novelty_claim",
                "diagonal_solver_implemented", "base_lazard_bch_theorem_formalized",
                "approximate_channel_and_runtime_bound_formalized", "independent_review_this_pass"):
        assert not report[key]


@pytest.mark.parametrize("p,r,k", [(2, 0, 0), (2, 0, 3), (2, 1, 0), (2, 2, 1),
                                    (2, 2, 4), (3, 1, 4), (3, 2, 3), (5, 2, 2)])
def test_exact_spanning_law(p, r, k):
    result = c.exhaustive_rank_check(p, r, k)
    assert Fraction(result["spanning_probability"]) == c.spanning_probability(p, r, k)


@pytest.mark.parametrize("q", [2, 3, 4, 7, 65537])
def test_hyperplane_union_bound_dominates_exact_failure(q):
    for r in range(5):
        for k in range(8):
            assert 1 - c.spanning_probability(q, r, k) <= c.hyperplane_failure_bound(q, r, k)


@pytest.mark.parametrize("q,n,arities", [(2, 1, ()), (3, 5, (2,)), (7, 5, (16, 531441)),
                                        (65537, 1000, (1001**2, 1001))])
def test_charged_budget_includes_final_readout_and_precision(q, n, arities):
    epsilon = Fraction(1, 10**9)
    b = c.terminal_budget(q, n, arities, epsilon)
    assert Fraction(b["rank_failure_upper_bound"]) <= epsilon / 3
    assert b["final_readout_instruments"] == b["terminal_samples"]
    assert b["complete_instruments"] == b["fresh_lifted_leaves"] + b["conversion_nodes"] + b["terminal_samples"]
    assert Fraction(b["per_instrument_half_diamond_error"]) * b["complete_instruments"] == epsilon / 3
    assert b["original_source_copies"] == (len(arities) + 1) * b["fresh_lifted_leaves"]
    assert not b["gate_or_solver_runtime_certified"]


def test_source_tree_counts_not_sum_or_memoized():
    b = c.terminal_budget(7, 5, (3, 5, 7), Fraction(1, 100))
    m = b["terminal_samples"]
    assert b["fresh_lifted_leaves"] == m * 105
    assert b["conversion_nodes"] == m * (1 + 3 + 15)


def test_literal_density_fourier_readout_and_falsifiers():
    result = c.audit()
    assert len(result["exact_density_controls"]) == 6
    assert result["degenerate_character_total_mass"] == "9"
    assert result["iid_rank_two_four_sample_success"] == "2080/2187"
    assert result["same_marginal_correlated_four_sample_success"] == "0"
    assert not result["quantum_execution"]


def test_correct_samples_without_span_return_wrong_larger_space():
    original = {(0, 0)}
    samples = [(1, 0)] * 10
    assert all(sum(a * b for a, b in zip(row, x)) % 3 == 0 for row in samples for x in original)
    assert c.nullspace_points(samples, 3, 2) > original


def test_discarded_coherence_changes_output_law():
    domain = tuple(product(range(3), repeat=2))
    ideal = c.literal_fourier_diagonal(c.source_fixture(domain, 3, 2), 3, 2)
    dephased = tuple(tuple(Fraction(int(i == j), 9) for j in range(9)) for i in range(9))
    wrong = c.literal_fourier_diagonal(dephased, 3, 2)
    assert sum(abs(ideal[x][0] - wrong[x][0]) for x in domain) / 2 == Fraction(8, 9)


@pytest.mark.parametrize("q,r,k", [(1, 1, 2), (2, -1, 2), (2, 1, -1), (True, 1, 2)])
def test_rank_formula_domain_validation(q, r, k):
    with pytest.raises(ValueError):
        c.spanning_probability(q, r, k)


@pytest.mark.parametrize("n,arities,error", [(0, (), Fraction(1, 2)), (1, (0,), Fraction(1, 2)),
                                           (1, (True,), Fraction(1, 2)), (1, (), 0), (1, (), 1)])
def test_invalid_budgets_rejected(n, arities, error):
    with pytest.raises(ValueError):
        c.terminal_budget(3, n, arities, error)


@pytest.mark.parametrize("prime,dimension", [(4, 2), (37, 1), (3, 8)])
def test_finite_allocation_or_nonfield_controls_rejected(prime, dimension):
    with pytest.raises(ValueError):
        c.literal_fourier_diagonal([], prime, dimension)


def test_finite_rank_census_is_capped():
    with pytest.raises(ValueError, match="census cap"):
        c.exhaustive_rank_check(3, 3, 4)


def test_wrong_density_dimension_rejected():
    with pytest.raises(ValueError, match="incorrect dimension"):
        c.literal_fourier_diagonal([[1]], 3, 2)

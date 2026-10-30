from fractions import Fraction
from itertools import product

import pytest

from flint import nmod_mat

from schur_gate import FullSupportProblem, rows, selected
from finite_controls import annihilator_control, curve_control


def rs_control(scaled=False):
    # An exact algebra control, NOT an alleged hard problem or quantum experiment.
    v = [i+1 if scaled else 1 for i in range(10)]
    return FullSupportProblem(11, [v, [i*v[i] % 11 for i in range(10)]],
                              relation="full_support")


def test_rs_dimensions_and_whole_sum_dominance():
    p = rs_control()
    gate, exact = p.dominance(), p.exact_bounds()
    assert (gate["square_dimension"], gate["cube_dimension"]) == (3, 4)
    assert gate["status"] == "CLASSICAL_COVERS_THIS_QUANTUM_CRITERION"
    assert gate["classical_bound_over_quantum_bound_upper"] == Fraction(1, 220)
    assert exact["minimum_distance"] == 9
    assert exact["quantum_failure_expression"] < 1
    assert exact["classical_failure_bound"] <= exact["quantum_failure_expression"]/220
    assert p.quantum_bound_floor() <= exact["quantum_failure_expression"]


def test_nonconstant_public_unit_is_not_silently_assumed():
    p = rs_control(scaled=True)
    assert not p.dominance()["public_unit_verified"]
    gate = p.dominance(tuple(range(1, 11)))
    assert gate["public_unit_verified"]
    exact = p.exact_bounds()
    assert exact["classical_failure_bound"] <= (
        gate["classical_bound_over_quantum_bound_upper"]*exact["quantum_failure_expression"])
    assert not p.dominance((0,)*10)["public_unit_verified"]


def test_every_shortening_respects_the_growth_bound():
    p = rs_control(scaled=True)
    delta = len(p.U)-len(p.W)
    for mask in range(1 << p.m):
        zero_positions = [i for i in range(p.m) if mask >> i & 1]
        assert p.shortened_dimension(p.U, zero_positions) - p.shortened_dimension(
            p.W, zero_positions) <= delta


def test_constructive_solver_all_original_syndromes():
    p = rs_control()
    # Fourth finite differences annihilate every cubic on these ORIGINAL columns.
    h = (1, 7, 6, 7, 1, 0, 0, 0, 0, 0)
    for syndrome in product(range(11), repeat=2):
        result = p.from_annihilator(syndrome, h, 2)
        assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
        assert result["algorithm_is_prior_art"]
        assert not result["uniform_witness_sampling"]
        assert result["witness"][5:] == [1]*5
        assert all(result["witness"])
        assert all(sum(int(p.B[r, i])*result["witness"][i] for i in range(10)) % 11 == syndrome[r]
                   for r in range(2))


def test_random_annihilator_sampling_charges_attempts_and_draws():
    p = rs_control()
    result = p.solve((3, 7), 2, seed=26)
    assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
    assert result["field_draws"] == 6*result["attempts"]
    assert p.verifies(result["witness"], (3, 7))


def test_exact_classical_failure_bound_matches_all_729_annihilators():
    p = FullSupportProblem(3, [[1]*7], relation="full_support")
    failures = 0
    for prefix in product(range(3), repeat=6):
        h = prefix+((-sum(prefix)) % 3,)
        result = p.from_annihilator((2,), h, 2)
        if result["witness"] is None:
            failures += 1
        else:
            assert p.verifies(result["witness"], (2,))
    assert failures == 1
    exact = p.exact_bounds()
    assert exact["classical_failure_bound"] == Fraction(1, 729)
    assert exact["quantum_failure_expression"] < 1


def test_cube_growth_gate_can_fail_without_claiming_advantage():
    # Punctured first-order RM arithmetic control; not a speedup benchmark.
    points = list(product(range(3), repeat=3))[1:]
    p = FullSupportProblem(3, [[1]*len(points)]+
                           [[point[i] for point in points] for i in range(3)],
                           relation="full_support")
    gate = p.dominance()
    assert gate["public_unit_verified"]
    assert (gate["square_dimension"], gate["cube_dimension"], gate["rank"]) == (10, 17, 4)
    assert gate["status"] == "NO_DOMINANCE_CERTIFICATE_NOT_ADVANTAGE"
    assert gate["quantum_advantage_established"] is False


@pytest.mark.parametrize("genus,dimensions", [(1, (3, 6, 9, 12)),
                                            (2, (4, 9, 14, 15)),
                                            (3, (5, 12, 19, 22))])
def test_smooth_ag_schur_products_and_every_annihilator(genus, dimensions):
    p, metadata = curve_control(genus)
    assert (p.k, len(p.W), len(p.U), p.m) == dimensions
    assert metadata["schur_and_rr_rowspaces_equal"]
    assert p.m > 3*metadata["divisor_degree"]-genus+1
    control = annihilator_control(p)
    assert control["rank_failures"] == 1
    assert control["nonzero_rank_failures"] == 0
    assert control["annihilators_enumerated"] == p.p**len(p.annihilator)
    assert control["minimum_nonzero_support"] >= 3*metadata["divisor_degree"]-2*genus+2
    result = p.deterministic_attempt(tuple(range(1, p.k+1)), 2)
    assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
    assert result["field_draws"] == 0


def test_exact_growth_factor_includes_delta_equal_rank_plus_one():
    p, _ = curve_control(2)
    gate = p.dominance()
    assert gate["multiplication_growth"] == p.k+1
    assert gate["classical_bound_over_quantum_bound_upper"] == Fraction(19, 36)
    assert gate["status"] == "CLASSICAL_COVERS_THIS_QUANTUM_CRITERION"


def test_geometric_solver_beyond_growth_gate_and_vacuous_union_bound():
    p, _ = curve_control(3)
    gate = p.dominance()
    assert gate["status"] == "NO_DOMINANCE_CERTIFICATE_NOT_ADVANTAGE"
    assert gate["classical_bound_over_quantum_bound_upper"] == Fraction(361, 36)
    # Geometric proof makes every projective bad event the SAME zero h.
    union = Fraction(p.p**p.k-1, (p.p-1)*p.p**len(p.annihilator))
    assert union > 1
    assert p.quantum_bound_floor() > 1
    assert p.deterministic_attempt((7, 0, 3, 18, 12), 2)["witness"] is not None


def test_elliptic_shortening_and_bound_are_not_failure_probability():
    p, metadata = curve_control(1)
    d = metadata["divisor_degree"]
    for coefficients in product(range(p.p), repeat=p.k):
        if not any(coefficients):
            continue
        word = [sum(a*v[i] for a, v in zip(coefficients, p.V)) % p.p
                for i in range(p.m)]
        zeros = [i for i, x in enumerate(word) if not x]
        assert len(zeros) <= d
        if zeros:
            assert selected(nmod_mat(p.U, p.p), zeros).rank() == len(zeros)
        assert p.shortened_dimension(p.W, zeros) == len(p.W)-len(zeros)
    exact = p.exact_bounds()
    assert exact["classical_failure_bound"] == Fraction(133, 1331)
    assert exact["classical_failure_bound"] > Fraction(1, 1331)
    assert p.quantum_bound_floor() <= exact["quantum_failure_expression"]
    assert p.quantum_bound_floor() > 1


def test_original_equations_survive_monomial_scaling_and_row_basis_change():
    original, _ = curve_control(3)
    multipliers = [i % (original.p-1)+1 for i in range(original.m)]
    B = rows(original.B)
    B = [[row[i]*multipliers[i] % original.p for i in reversed(range(original.m))]
         for row in B]
    B[0] = [(x+3*y) % original.p for x, y in zip(B[0], B[1])]
    B[1], B[-1] = B[-1], B[1]
    p = FullSupportProblem(original.p, B, relation="full_support")
    for a, b in product(range(p.p), repeat=2):
        syndrome = (a, b, (a+b) % p.p, (a*b) % p.p, (a+3*b) % p.p)
        result = p.deterministic_attempt(syndrome, 2)
        assert p.verifies(result["witness"], syndrome)
        assert all(sum(row[i]*result["witness"][i] for i in range(p.m)) % p.p == s
                   for row, s in zip(B, syndrome))


def test_no_annihilator_and_bad_first_choice_do_not_certify_hardness():
    p = FullSupportProblem(3, [[1, 0], [0, 1]], relation="full_support")
    result = p.deterministic_attempt((0, 0), 2)
    assert result["status"] == "UNKNOWN_FIRST_ANNIHILATOR"
    assert result["hardness_evidence"] is False
    # Direct sum forces first kernel vector to miss a nontrivial row block.
    p = FullSupportProblem(3, [[1, 1, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 1, 1, 1, 1]], relation="full_support")
    assert p.deterministic_attempt((1, 2), 2)["status"] == "UNKNOWN_FIRST_ANNIHILATOR"
    assert p.solve((1, 2), 2, seed=0, attempts=32)["witness"] is not None


@pytest.mark.parametrize("genus", [0, 4, True])
def test_curve_controls_cannot_be_mistaken_for_an_unbounded_generator(genus):
    with pytest.raises(ValueError):
        curve_control(genus)


def test_rank_failure_and_cap_are_unknown_not_unsat():
    p = FullSupportProblem(3, [[1, 0], [0, 1]], relation="full_support")
    result = p.solve((0, 0), 2, seed=26, attempts=3)
    assert result == {"status": "UNKNOWN_ATTEMPT_CAP", "witness": None,
                      "attempts": 3, "field_draws": 0, "hardness_evidence": False}
    # A bad particular annihilator does not imply failure on the original input.
    rs = rs_control()
    assert rs.from_annihilator((3, 7), (0,)*10, 2)["status"] == "RETRY_RANK"
    assert rs.solve((3, 7), 2, seed=26)["witness"] is not None


@pytest.mark.parametrize("relation", ["inverse_trace", "halfsets", "cubic_orbit", None])
def test_no_silent_native_problem_replacement(relation):
    with pytest.raises(ValueError, match="only By=s"):
        FullSupportProblem(3, [[1, 1]], relation=relation)


@pytest.mark.parametrize("prime", [2, 9, True, 11.0, 2**67-1])
def test_prime_backend_guards(prime):
    with pytest.raises(ValueError):
        FullSupportProblem(prime, [[1, 1]], relation="full_support")


@pytest.mark.parametrize("data", [[], [[]], [[0, 0]], [[1, 1], [2, 2]],
                                   [[1], [1, 2]], [[True, 1]], [[1, 3]]])
def test_parity_input_guards(data):
    with pytest.raises(ValueError):
        FullSupportProblem(3, data, relation="full_support")


def test_witness_and_resource_guards():
    p = rs_control()
    for nu in (0, 1, 11, True):
        with pytest.raises(ValueError):
            p.from_annihilator((0, 0), (0,)*10, nu)
    with pytest.raises(ValueError, match="full Schur cube"):
        p.from_annihilator((0, 0), (1,)+(0,)*9, 2)
    for syndrome in ((0,), (0, 11), (True, 0)):
        with pytest.raises(ValueError):
            p.solve(syndrome, 2, seed=0)
    for attempts in (0, -1, True, 2.0):
        with pytest.raises(ValueError):
            p.solve((0, 0), 2, seed=0, attempts=attempts)
    big = FullSupportProblem(101, [[1]*10, list(range(10))], relation="full_support")
    assert big.dominance()["public_unit_verified"]
    with pytest.raises(ValueError, match="enumeration cap"):
        big.exact_bounds()

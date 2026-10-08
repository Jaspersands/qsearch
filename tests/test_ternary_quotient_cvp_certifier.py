from itertools import product
import json
import subprocess

import pytest

from ternary_covariant_noise import CovariantRecord
from ternary_measured_lattice_decoder import compile_code_lattice
from ternary_quotient_cvp import compile_quotient, conditional_point
from ternary_quotient_cvp_certifier import REPORT, point_active_coefficients, sphere_search


def compiled():
    records = (CovariantRecord((1,), (1,), (0, 1), 3),
               CovariantRecord((1,), (1,), (1, 1), 3))
    model = compile_code_lattice(records)
    return compile_quotient(model, ((0, 3, 0, 0), (0, 0, 3, 0), (0, 0, 0, 3), (1, 1, 1, 1)))


def test_complete_search_finds_exact_optima_not_merely_local_babai_for_all_small_targets():
    c = compiled()
    for target in product(range(3), repeat=4):
        result = sphere_search(c, target, node_cap=1000)
        best = min(conditional_point(c, target, (a,))["supplied_Euclidean_cost"] for a in range(-3, 6))
        assert result["CVP_optimality_certified"]
        assert result["final_squared_radius"] == best
        assert result["status"] == "EXACT_FINITE_CVP_OPTIMUM_CERTIFIED"
    result = sphere_search(c, (0, 1, 1, 1), node_cap=1000)
    assert result["initial_squared_radius"] == 3 and result["final_squared_radius"] == 1
    assert result["best_point"]["candidate"] == (1,)


@pytest.mark.parametrize("cap", (0, 1))
def test_cap_exhaustion_cannot_certify_optimality_or_hardness_even_on_easy_input(cap):
    result = sphere_search(compiled(), (0, 1, 1, 1), node_cap=cap)
    assert result["status"] == "UNKNOWN_NODE_CAP_EXHAUSTED"
    assert not result["CVP_optimality_certified"]
    assert not result["all_live_branches_within_radius_exhausted"]
    assert result["search_counters"]["tested_coefficient_extensions"] == cap
    assert not result["cap_exhaustion_certifies_approximation_or_hardness"]


def test_complete_search_includes_coefficients_outside_fixed_plus_minus_one_menu():
    c = compiled()
    # A poor valid public incumbent may be far from the target; radius search
    # must reach distant integer values without secret or root enumeration.
    result = sphere_search(c, (40, 40, 40, 40), node_cap=1000, incumbent_active=(-100,))
    assert result["CVP_optimality_certified"] and result["final_squared_radius"] == 0
    assert result["best_point"]["active_coefficients"] == (40,)
    assert result["unbounded_integer_coefficients_handled_by_exact_radius"]


def test_exact_search_reproducible_and_every_improvement_is_a_valid_full_point():
    c, target = compiled(), (0, 1, 1, 1)
    result = sphere_search(c, target, incumbent_active=(3,))
    assert result == sphere_search(c, target, incumbent_active=(3,))
    old = result["initial_squared_radius"]
    for item in result["strict_improvement_trace"]:
        cost = conditional_point(c, target, item["active_coefficients"])["supplied_Euclidean_cost"]
        assert cost == item["supplied_Euclidean_cost"] < old
        old = cost
    assert old == result["final_squared_radius"]


def test_exact_inverse_basis_recovers_active_coordinates_of_all_valid_points():
    c, target = compiled(), (0, 1, 1, 1)
    for active in range(-10, 11):
        path = conditional_point(c, target, (active,))
        assert point_active_coefficients(c, path["point"]) == (active,)
    with pytest.raises(ValueError):
        point_active_coefficients(c, (1, 0, 0, 0))


def test_fractional_centers_and_coupled_live_coefficients_match_direct_integer_enumeration():
    model = compile_code_lattice((CovariantRecord((1,), (1,), (0, 0), 3),))
    rows = ((1, 1), (0, 3))
    c = compile_quotient(model, rows)
    assert c["certificate"]["live_positions"] == (0, 1)
    assert str(c["profile"]["mu"][1][0]) == "3/2"
    for target in product(range(3), repeat=2):
        expected = min(sum((target[j]-a*rows[0][j]-b*rows[1][j])**2 for j in range(2))
                       for a, b in product(range(-4, 5), repeat=2))
        result = sphere_search(c, target, node_cap=1000)
        assert result["CVP_optimality_certified"] and result["final_squared_radius"] == expected


def test_independent_live_certifier_replays_complete_and_capped_searches():
    checker = REPORT.parents[1]/"certificates/ternary_quotient_cvp_certifier_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    verified = json.loads(result.stdout)
    assert verified["status"] == "PASS" and verified["full_cohorts"] == 8
    assert verified["certified_finite_optima"] == 1
    assert verified["explicitly_unknown_capped_controls"] == 7
    assert verified["exact_tested_extensions"] == 31758
    assert not verified["efficient_population_solver"]


@pytest.mark.parametrize("mutation", ("false_optimality", "wrong_radius"))
def test_independent_checker_rejects_optimality_from_cap_or_false_distance(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    result = report["controls"][1]["result"]
    if mutation == "false_optimality":
        result["CVP_optimality_certified"] = True
        result["status"] = "EXACT_FINITE_CVP_OPTIMUM_CERTIFIED"
    else:
        result["final_squared_radius"] += 1
    file = tmp_path/"false.json"
    file.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_quotient_cvp_certifier_crosscheck.js"
    assert subprocess.run(["node", str(checker), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("cap", (-1, True, 1.5))
def test_invalid_caps_rejected(cap):
    with pytest.raises(ValueError):
        sphere_search(compiled(), (0, 1, 1, 1), node_cap=cap)

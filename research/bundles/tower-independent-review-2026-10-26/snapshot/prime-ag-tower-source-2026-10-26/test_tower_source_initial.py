from copy import deepcopy
from fractions import Fraction
from itertools import product
from math import prod
import random

import pytest

from elementary_cover import (LOW_MASKS, MASKS, PRIME, control, evaluate,
                              local_coefficient, monomials, sqrt_series)
from tower_seed import (BRANCHES, SPLITTING_X, TowerSeed, asymptotic_quantum_certificate,
                        default_seed, exact_small_quantum_bounds, kummer_quotient_rank,
                        persistent_section_bound, scan_consecutive_square_runs,
                        specialization, verify_certificate)


@pytest.fixture(scope="module")
def built():
    return control()


def test_actual_seed_and_discovery_replay():
    certificate = default_seed().certificate()
    assert verify_certificate(certificate)
    assert certificate["genus"] == 6
    assert certificate["splitting_places"] == 23
    assert certificate["kummer_rank_over_base"] == 12
    assert certificate["schoof_squared_margin"] == 4
    assert certificate["schoof_sufficient_criterion"]
    replay = scan_consecutive_square_runs()
    assert replay == {"x_values": list(SPLITTING_X), "legendre_tests": 51887, "status": "FOUND"}
    for pair in certificate["affine_splitting_pairs"]:
        x = pair["x"]
        assert all(r*r % PRIME == (x-a) % PRIME for r, a in zip(pair["square_roots"], BRANCHES))
        assert len(set(pair["y_pair"])) == 2
        assert all(y*y % PRIME == prod(x-a for a in BRANCHES) % PRIME for y in pair["y_pair"])


@pytest.mark.parametrize("mutation", ["root", "y", "rank", "margin", "admission", "prime"])
def test_forged_certificates_rejected(mutation):
    data = deepcopy(default_seed().certificate())
    if mutation == "root":
        data["affine_splitting_pairs"][0]["square_roots"][0] ^= 1
    elif mutation == "y":
        data["affine_splitting_pairs"][0]["y_pair"][0] ^= 1
    elif mutation == "rank":
        data["kummer_rank_over_base"] = 13
    elif mutation == "margin":
        data["schoof_squared_margin"] = 5
    elif mutation == "admission":
        data["registry_admission"] = True
    else:
        data["prime"] = 100005
    assert not verify_certificate(data)


@pytest.mark.parametrize("args", [
    (100005, BRANCHES, SPLITTING_X), (PRIME, (0, 0, 1, 2, 3), SPLITTING_X),
    (PRIME, BRANCHES[:-1], SPLITTING_X), (PRIME, BRANCHES, (0,)),
    (PRIME, BRANCHES, (18501, 18501)), (PRIME, BRANCHES, (True,)),
])
def test_invalid_seed_rejected(args):
    with pytest.raises(ValueError):
        TowerSeed(*args)


def test_additional_split_pair_invalidates_this_gs_certificate_not_the_tower():
    data = TowerSeed(PRIME, BRANCHES, SPLITTING_X+(51888,)).certificate()
    assert data["schoof_squared_margin"] == -4
    assert not data["schoof_sufficient_criterion"]
    assert verify_certificate(data)


def test_kummer_relation_and_infinity_character_count():
    assert kummer_quotient_rank(13) == 12
    assert len(LOW_MASKS) == 8 and len(MASKS) == 16
    assert all(mask.bit_count() % 2 == 0 for mask in LOW_MASKS)
    assert len(monomials(2)) == 8
    assert len(monomials(10)) == 41
    assert len(monomials(13)) == 64
    full_low_pole_count = sum((2-mask.bit_count())//2+1 for mask in range(1 << 13)
                             if mask.bit_count() <= 2)
    assert full_low_pole_count == 93


def test_exact_series_square_identity():
    for mask in MASKS:
        root = sqrt_series(mask, 8)
        poly = [1]+[0]*8
        for i in range(13):
            if mask & (1 << i):
                for j in range(8, 0, -1):
                    poly[j] = (poly[j]-i*poly[j-1]) % PRIME
        assert [sum(root[i]*root[j-i] for i in range(j+1)) % PRIME for j in range(9)] == poly


def test_original_matrix_is_full_rr_code_not_pullback_subcode(built):
    problem, _, data = built
    assert (problem.k, problem.m, len(problem.W), len(problem.U)) == (43, 176, 126, 173)
    assert data["infinity_constraint_rank"] == 21
    assert len(problem.annihilator) == 3
    assert len({(pt["x"], pt["y"], *pt["w"]) for pt in data["points"]}) == 176
    for pt in data["points"]:
        assert pt["y"]**2 % PRIME == prod(pt["x"]-i for i in range(13)) % PRIME
        assert all(w*w % PRIME == pt["x"]*(pt["x"]-i) % PRIME
                   for i, w in enumerate(pt["w"], 1))


def test_explicit_function_cancellation_and_residues(built):
    _, h, data = built
    certificate = data["analytic_annihilator"]
    coefficients = [-66, 62, -36, 18, -45, 1, 0, 0]
    assert certificate["coefficients"] == [x % PRIME for x in coefficients]
    assert certificate["order_at_distinguished_infinity"] == 8
    assert certificate["function_space_dimension"] == 3
    functions = monomials(2)
    for exponent in range(-2, 8):
        assert sum(c*local_coefficient(f, -exponent) for c, f in zip(coefficients, functions)) % PRIME == 0
    assert sum(c*local_coefficient(f, -8) for c, f in zip(coefficients, functions)) % PRIME == -27*pow(32, -1, PRIME) % PRIME
    assert all(h)
    for point in data["points"]:
        assert sum(c*evaluate(f, point) for c, f in zip(coefficients, functions)) % PRIME


def test_all_original_basis_syndromes_and_seeded_targets(built):
    problem, h, _ = built
    targets = [(0,)*problem.k, (1,)*problem.k, tuple(range(problem.k))]
    targets += [tuple(int(i == j) for i in range(problem.k)) for j in range(problem.k)]
    rng = random.Random(260261)
    targets += [tuple(rng.randrange(PRIME) for _ in range(problem.k)) for _ in range(8)]
    for target in targets:
        result = problem.from_annihilator(target, h, 2)
        assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
        assert problem.verifies(result["witness"], target)
        assert not result["uniform_witness_sampling"]
    assert len(targets) == 54


def test_original_matrix_only_solver_and_tampered_h(built):
    problem, h, _ = built
    result = problem.deterministic_attempt(tuple(range(problem.k)), 2)
    assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
    assert result["field_draws"] == 0
    assert problem.verifies(result["witness"], tuple(range(problem.k)))
    broken = list(h)
    broken[0] = (broken[0]+1) % PRIME
    with pytest.raises(ValueError, match="Schur cube"):
        problem.from_annihilator((0,)*problem.k, broken, 2)


def test_cubic_nonzero_is_stronger_than_old_length_guarantee(built):
    _, _, data = built
    assert not data["parameters"]["cubic_completion_sufficient"]
    assert data["analytic_support_parity_rank"] == 43
    assert data["analytic_support_size"] == 176
    quantum = exact_small_quantum_bounds(8)
    assert 0 < quantum["E_upper"] < Fraction(1, 10**34)
    assert quantum["ideal_success_lower"] > Fraction(999, 1000)
    assert exact_small_quantum_bounds(4)["ideal_success_lower"] == 0
    for e in (8, 16, 32):
        bound = exact_small_quantum_bounds(e)["E_upper"]
        assert bound < PRIME**9*Fraction(2, PRIME**2)**e
    assert asymptotic_quantum_certificate()["all_dyadic_e_ge_8_bound_nonvacuous"]


@pytest.mark.parametrize("e", [0, 3, True, -8])
def test_bad_parameter_degree_rejected(e):
    with pytest.raises(ValueError):
        specialization(e)


def test_large_formulas_never_claim_constructed_levels():
    data = specialization(4096)
    assert (data["genus"], data["length"], data["dimension"]) == (20481, 90112, 20483)
    assert not data["efficient_uniform_generator_proved"]
    assert not data["quantum_advantage_established"]
    with pytest.raises(ValueError):
        exact_small_quantum_bounds(64)


def test_bounded_divisor_mutations_do_not_escape_without_new_premises():
    assert persistent_section_bound(3, 0, full_kummer_inclusion_asserted=True)["annihilator_dimension_lower"] == 84
    assert persistent_section_bound(3, 83, full_kummer_inclusion_asserted=True)["annihilator_dimension_lower"] == 1
    boundary = persistent_section_bound(3, 84, full_kummer_inclusion_asserted=True)
    assert boundary["annihilator_dimension_lower"] == 0
    assert boundary["status"] == "NO_CERTIFICATE_NOT_HARDNESS"
    no_inclusion = persistent_section_bound(3, 0, full_kummer_inclusion_asserted=False)
    assert no_inclusion["annihilator_dimension_lower"] is None
    assert not no_inclusion["inclusion_premise_verified_by_this_helper"]

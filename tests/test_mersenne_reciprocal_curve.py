from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from math import comb, gcd, isqrt
from pathlib import Path

import pytest
from flint import nmod_mat

from theorems import mersenne_reciprocal_curve as mersenne
from theorems.balanced_codeword_filter import reciprocal_trace as legacy_predicate
from theorems.balanced_filter_channel_audit import projection_size
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import mds_character_bound, reciprocal_bound
from theorems.inverse_trace_smt import verify_word as legacy_verify_word


def instance(bits=5, s=2, points=(0, 1, 2), targets=(0, 0, 0), checks=1):
    return mersenne.make_instance(bits, s, points, targets, checks)


@pytest.mark.parametrize("bits,s", [(5, 1), (5, 2), (5, 3), (5, 4), (7, 2), (7, 3)])
@pytest.mark.parametrize("target", [0, 1])
def test_root_bijection_both_bits_and_zero(bits, s, target):
    q, d = 1 << bits, (1 << s)-1
    hyperplane = {u for u in range(q) if int(element(bits, u).trace()) == target}
    accepted = {x for x in range(q)
                if (int(((element(bits, x)**-1)**d).trace()) if x else 0) == target}
    roots = {mersenne.root_from_trace(bits, s, u, target) for u in hyperplane}
    seeded = [mersenne.root_from_seed(bits, s, target, seed) for seed in range(q//2)]
    assert gcd(d, q-1) == 1
    assert len(roots) == len(hyperplane) == len(accepted) == q//2
    assert set(seeded) == roots == accepted
    assert len(set(seeded)) == q//2
    assert (0 in roots) == (target == 0)
    exponent = (-pow(d, -1, q-1)) % (q-1)
    for u in hyperplane:
        x = mersenne.root_from_trace(bits, s, u, target)
        assert x == (encoded(element(bits, u)**exponent) if u else 0)
        assert mersenne.reciprocal_value(bits, s, x) == u
        assert mersenne.reciprocal_trace(bits, s, x) == target
    for seed, x in enumerate(seeded):
        assert mersenne.reciprocal_value(bits, s, x) >> 1 == seed
    if target == 0:
        assert mersenne.root_from_trace(bits, s, 0, 0) == 0
        assert mersenne.root_from_seed(bits, s, 0, 0) == 0
    with pytest.raises(ValueError, match="hyperplane"):
        mersenne.root_from_trace(bits, s, 0 if target else 1, target)


@pytest.mark.parametrize("bits,s", [(17, 3), (17, 4), (31, 7), (61, 14), (127, 31)])
def test_large_root_maps_need_no_field_enumeration(bits, s):
    for target in (0, 1):
        for seed in (0, 1, (1 << (bits-1))-1):
            x = mersenne.root_from_seed(bits, s, target, seed)
            assert mersenne.reciprocal_trace(bits, s, x) == target
            assert mersenne.reciprocal_value(bits, s, x) >> 1 == seed


@pytest.mark.parametrize("bits,s,weight", [(17, 3, 11), (31, 7, 22), (61, 14, 13)])
def test_canonical_native_constructor_and_root_weight(bits, s, weight):
    problem = mersenne.native_instance(bits)
    assert problem["s"] == (bits-3)//4 == s
    assert problem["points"] == list(range(bits*bits))
    assert problem["targets"] == [1]*(bits*bits)
    assert problem["checks"] == bits*bits//8
    row = mersenne.ideal_budget(instance(bits, s), 1)
    assert row["canonical_growing_s"] == s
    assert row["canonical_research_parameters"] and row["matches_growing_s_formula"]
    assert row["parameter_role"] == "CANONICAL_GROWING_GENUS_CANDIDATE"
    assert row["root_power_binary_weight"] == weight
    assert row["root_map_degree_label"] == f"BOOLEAN_VECTOR_DEGREE_{weight}"
    assert row["predicate_degree"] == bits-s


def test_old_floor_n_over_four_is_labeled_low_degree_not_rejected():
    canonical = mersenne.native_instance()
    control = mersenne.native_instance(17, s=17//4)
    assert canonical["s"] == 3 and control["s"] == 4
    assert canonical["problem_family"] == control["problem_family"]
    row = mersenne.ideal_budget(control, 173)
    assert row["parameter_role"] == "LOW_DEGREE_ROOT_CONTROL_N17_S4"
    assert row["root_power_binary_weight"] == 4
    assert row["root_map_degree_label"] == "BOOLEAN_VECTOR_DEGREE_4"
    assert row["predicate_degree"] == 13
    assert not row["canonical_research_parameters"] and not row["matches_growing_s_formula"]


@pytest.mark.parametrize("bits", [3, 5, 7, 9, 17, 31, 61])
def test_telescoping_inverse_exponent_identity_and_actual_binary_weight(bits):
    order = (1 << bits)-1
    for s in range(1, bits):
        if gcd(s, bits) != 1:
            continue
        row = mersenne.ideal_budget(instance(bits, s), 1)
        k, d = pow(s, -1, bits), (1 << s)-1
        inverse = sum(1 << ((j*s) % bits) for j in range(k))
        assert d*inverse % order == 1
        assert inverse == pow(d, -1, order) == row["d_inverse"]
        assert row["s_inverse_mod_n"] == k
        assert row["d_inverse_binary_weight"] == inverse.bit_count() == k
        assert row["root_power"] == order-inverse == (-inverse) % order
        assert row["root_power_binary_weight"] == (order-inverse).bit_count() == bits-k
        assert row["predicate_degree"] == bits-s


@pytest.mark.parametrize("bits", [3, 5, 7])
def test_root_vector_degree_and_predicate_degree_against_exhaustive_anf(bits):
    for s in range(1, bits):
        coefficients = [mersenne.root_from_trace(bits, s, u, int(element(bits, u).trace()))
                        for u in range(1 << bits)]
        for bit in range(bits):
            for mask in range(1 << bits):
                if mask & (1 << bit):
                    coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
        measured = max(mask.bit_count() for mask, coefficient in enumerate(coefficients)
                       if coefficient)
        row = mersenne.functional_degree_control(bits, s)
        assert measured == row["root_power_binary_weight"] == bits-pow(s, -1, bits)
        assert row["algebraic_degree"] == row["predicate_degree"] == bits-s


@pytest.mark.parametrize("bits,s", [(2, 1), (4, 1), (6, 1), (128, 1),
                                       (9, 3), (15, 5), (5, 0), (5, 5), (5, 6)])
def test_invalid_degree_or_nonpermutation_is_rejected_everywhere(bits, s):
    operations = [
        lambda: mersenne.make_instance(bits, s, [0, 1], [0, 0], 1),
        lambda: mersenne.reciprocal_trace(bits, s, 0),
        lambda: mersenne.reciprocal_value(bits, s, 0),
        lambda: mersenne.root_from_trace(bits, s, 0, 0),
        lambda: mersenne.root_from_seed(bits, s, 0, 0),
        lambda: mersenne.finite_curve_count(bits, s, 1),
        lambda: mersenne.finite_walsh_control(bits, s),
        lambda: mersenne.functional_degree_control(bits, s),
    ]
    for operation in operations:
        with pytest.raises(ValueError):
            operation()


def test_odd_composite_degree_is_allowed_when_coprime():
    problem = instance(9, 2)
    assert mersenne.validate_instance(problem)[:2] == (9, 2)
    assert mersenne.verify_word(problem, [0, 0, 0])
    problem["s"] = 3
    for operation in (lambda: mersenne.validate_instance(problem),
                      lambda: mersenne.verify_word(problem, [0, 0, 0]),
                      lambda: mersenne.ideal_budget(problem, 1)):
        with pytest.raises(ValueError, match="gcd"):
            operation()


@pytest.mark.parametrize("bits", [3, 5, 7])
def test_s1_is_exactly_the_old_predicate_but_requires_new_schema(bits):
    for x in range(1 << bits):
        assert mersenne.reciprocal_trace(bits, 1, x) == legacy_predicate(bits, x)
    problem = instance(bits, 1)
    legacy = {k: v for k, v in problem.items() if k not in ("problem_family", "schema_version", "s")}
    assert mersenne.verify_word(problem, [0, 0, 0]) == legacy_verify_word(legacy, [0, 0, 0])
    with pytest.raises(ValueError, match="schema"):
        mersenne.verify_word(legacy, [0, 0, 0])
    assert mersenne.ideal_budget(problem, 1)["beta"] == reciprocal_bound(bits, 3, 1)[0]


def test_s2_cross_predicate_counterexample_and_s_binding():
    # Equal symbols meet the sole parity row, independently of either predicate.
    x = next(x for x in range(32)
             if mersenne.reciprocal_trace(5, 2, x) != legacy_predicate(5, x))
    cubic_bit, old_bit = mersenne.reciprocal_trace(5, 2, x), legacy_predicate(5, x)
    problem = instance(points=(0, 1), targets=(cubic_bit, cubic_bit))
    legacy = {k: v for k, v in problem.items() if k not in ("problem_family", "schema_version", "s")}
    assert mersenne.verify_word(problem, [x, x])
    assert not legacy_verify_word(legacy, [x, x])
    assert not mersenne.verify_word(dict(problem, s=1), [x, x])
    legacy["targets"] = [old_bit, old_bit]
    assert legacy_verify_word(legacy, [x, x])
    assert not mersenne.verify_word(dict(problem, targets=legacy["targets"]), [x, x])


def test_verifier_checks_all_vandermonde_rows_and_zero_convention():
    problem = instance(checks=2)
    assert mersenne.verify_word(problem, [0, 0, 0])
    assert not mersenne.verify_word(dict(problem, targets=[1, 0, 0]), [0, 0, 0])
    word = [1, 1, 0]  # j=0 cancels; j=1 does not.
    targets = [mersenne.reciprocal_trace(5, 2, x) for x in word]
    assert mersenne.verify_word(instance(targets=targets), word)
    assert not mersenne.verify_word(instance(targets=targets, checks=2), word)
    assert not mersenne.verify_word(problem, [0, 0])


def test_small_verifier_matches_independent_direct_equations():
    points, checks = (0, 2, 5), 2
    for word in product(range(8), repeat=3):
        expected_targets = [int((element(3, x)**4).trace()) for x in word]
        expected_parity = all(sum(
            (element(3, a)**j*element(3, x) for a, x in zip(points, word)),
            field(3).zero()) == 0 for j in range(checks))
        problem = instance(3, 2, points, expected_targets, checks)
        assert mersenne.verify_word(problem, word) == expected_parity
        problem["targets"][0] ^= 1
        assert not mersenne.verify_word(problem, word)


@pytest.mark.parametrize("bits,s", [(3, 1), (3, 2), (5, 1), (5, 2), (5, 3), (5, 4)])
def test_finite_walsh_parseval_and_independent_smooth_curve_count(bits, s):
    row, q, d = mersenne.finite_walsh_control(bits, s), 1 << bits, (1 << s)-1
    walsh = row["walsh"]
    assert row["problem_family"] == mersenne.PROBLEM_FAMILY
    assert row["bits"] == bits and row["s"] == s and row["exponent"] == d
    assert row["predicate"] == f"Tr(inv0(x)^{d})" and row["inv0_at_zero"] == 0
    assert walsh[0] == 0
    assert row["parseval_sum"] == q*q
    assert sum(walsh) == q  # Fourier inversion at f_s(0)=0.
    assert row["genus"] == 1 << (s-1) and row["pole_orders"] == (d, 1)
    assert set(row["curve_counts"]) == set(range(1, q))
    assert row["curve_identity_checked"] and row["hasse_weil_checked"]
    for u, count in row["curve_counts"].items():
        affine_via_trace = sum(2 for x in range(1, q) if int(
            (element(bits, x)**(-d)+element(bits, u)*element(bits, x)).trace()) == 0)
        assert count == affine_via_trace+2 == q+walsh[u]
        assert (count-q-1)**2 <= (1 << (2*s))*q
        assert max(0, abs(walsh[u])-1)**2 <= (1 << (2*s))*q
    with pytest.raises(ValueError, match="nonzero"):
        mersenne.finite_curve_count(bits, s, 0)
    assert row["exponential_control"] and not row["formal_curve_materialized"]
    assert not row["classical_hardness_claimed"]


@pytest.mark.parametrize("bits,s,degree", [(3, 1, 2), (3, 2, 1), (5, 2, 3),
                                           (7, 2, 5), (5, 4, 1), (7, 6, 1)])
def test_functional_degree_controls_include_zero_and_bind_s(bits, s, degree):
    row = mersenne.functional_degree_control(bits, s)
    assert row["s"] == s and row["exponent"] == (1 << s)-1
    assert row["algebraic_degree"] == degree
    assert row["predicate_degree"] == degree == bits-s
    assert row["coupled_problem_binary_linear"] == (degree == 1)
    for x in range(1 << bits):
        reconstructed = sum((x & mask) == mask for mask in row["anf_support"]) % 2
        assert reconstructed == mersenne.reciprocal_trace(bits, s, x)
        if s == bits-1:
            assert reconstructed == int(element(bits, x).trace())
    if (bits, s) == (3, 2):
        assert row["classification"] == "LINEAR_DEQUANTIZED_N3_S2"
    assert row["exponential_control"]
    assert not row["novelty_claimed"] and not row["quantum_advantage_claimed"]


def test_finite_controls_cannot_expand_to_native_field():
    for operation in (lambda: mersenne.finite_walsh_control(7, 2),
                      lambda: mersenne.finite_curve_count(7, 2, 1),
                      lambda: mersenne.functional_degree_control(9, 2),
                      lambda: mersenne.finite_walsh_control(17, 4),
                      lambda: mersenne.finite_curve_count(31, 7, 1)):
        with pytest.raises(ValueError, match="control bits"):
            operation()


@pytest.mark.parametrize("bits,s", [(17, 2), (17, 3), (17, 4), (31, 7), (61, 14)])
def test_native_budgets_use_s_bound_genus_beta_and_exact_binomial(bits, s):
    length, checks, radius = bits*bits, bits*bits//8, 3*bits*bits//5
    problem = instance(bits, s, list(range(length)), [1]*length, checks)
    before = deepcopy(problem)
    row = mersenne.ideal_budget(problem, radius)
    q = 1 << bits
    expected_beta = Fraction(1+(1 << s)*(isqrt(q)+1), q)
    assert row["beta"] == expected_beta
    assert row["beta"] != reciprocal_bound(bits, length, checks)[0]
    if s != 2:
        assert row["beta"] != Fraction(1+4*(isqrt(q)+1), q)
    assert row["eta"] == mds_character_bound(bits, length, checks, expected_beta)
    assert row["eta"] < Fraction(1, 1000)
    tau = Fraction(sum(comb(length, j) for j in range(radius+1)), 1 << length)
    assert row["tau"] == tau and row["tail"] == 1-tau
    assert row["padding"] == projection_size(length, checks, radius, q**checks) == 8
    assert row["native_success_per_attempt_lower"] == (1-row["eta"])*tau**2/8
    assert Fraction(1, 9) < row["native_success_per_attempt_lower"] < Fraction(1, 8)
    assert row["johnson_gap"] == (length-radius)**2-length*(checks-1) > 0
    assert row["problem_family"] == mersenne.PROBLEM_FAMILY
    assert row["s"] == s and row["exponent"] == (1 << s)-1
    assert row["predicate"] == f"Tr(inv0(x)^{(1 << s)-1})"
    assert row["genus"] == 1 << (s-1)
    assert row["canonical_research_parameters"] == (s == (bits-3)//4)
    assert row["predicate_degree"] == bits-s
    assert row["root_power_binary_weight"] == bits-pow(s, -1, bits)
    assert row["proof_scope"] == "CONDITIONAL_IDEAL_BOUND_NOT_QUANTUM_IMPLEMENTATION"
    for key in ("requires_paid_known_source_preparation", "requires_complete_reversible_list_decoder",
                "requires_clean_fixed_padding_projection", "requires_final_native_verification",
                "conditional_uniformity_requires_positive_native_success"):
        assert row[key] is True
    for key in ("quantum_premises_verified", "full_quantum_algorithm_implemented",
                "field_tables_materialized", "curves_materialized", "novelty_claimed",
                "quantum_advantage_claimed", "classical_hardness_claimed",
                "polynomial_classical_walsh_access_established",
                "polynomial_classical_source_access_claimed"):
        assert row[key] is False
    assert "polynomial in n" in row["field_operation_bit_cost"]
    assert "exponential in s" in row["generic_classical_point_count_cost"]
    assert problem == before


def test_native_budget_never_calls_exponential_controls_or_root_tables(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("analytic budget called an enumerative primitive")

    problem = instance(17, 3, list(range(289)), [i % 2 for i in range(289)], 36)
    for name in ("finite_walsh_control", "finite_curve_count", "functional_degree_control",
                 "reciprocal_trace", "element", "root_from_trace", "root_from_seed"):
        monkeypatch.setattr(mersenne, name, forbidden)
    assert mersenne.ideal_budget(problem, 173)["native_success_per_attempt_lower"] > 0


def test_vacuous_beta_and_strict_johnson_equality_are_not_positive_claims():
    for bits, s in ((3, 2), (5, 4)):
        row = mersenne.ideal_budget(instance(bits, s), 1)
        assert row["beta"] == 1 and row["eta"] >= 1
        assert row["native_success_per_attempt_lower"] == 0
        assert row["predicate_binary_linear"]
        assert row["n3_s2_linear_dequantized"] == ((bits, s) == (3, 2))
    assert not mersenne.ideal_budget(instance(3, 1), 1)["predicate_binary_linear"]
    problem = instance(points=(0, 1, 2, 3), targets=(0, 0, 0, 0), checks=2)
    for radius in (2, 3):  # Equality and failure of strict Johnson.
        with pytest.raises(ValueError, match="strict Johnson"):
            mersenne.ideal_budget(problem, radius)


@pytest.mark.parametrize("key,value", [
    ("problem_family", "inverse_trace"), ("problem_family", "inverse_cubic_trace_v1"),
    ("problem_family", None), ("schema_version", True), ("schema_version", 2),
    ("schema_version", 1.0), ("bits", True), ("bits", 4), ("bits", 5.0),
    ("s", True), ("s", 2.0), ("s", 0), ("s", 5),
    ("checks", True), ("checks", 3),
    ("points", [0, 1, 1]), ("points", [False, 1, 2]), ("points", [0, 1, 32]),
    ("points", [0, 1, []]), ("points", "012"),
    ("targets", [0, True, 0]), ("targets", [0, 0]), ("targets", [0, 0, 2]),
    ("targets", [0, 0, 0.0]), ("targets", None),
    ("field_modulus_coefficients", [1, 0, 0, 0, 0, 1]),
])
def test_strict_schema_rejects_wrong_modulus_bools_duplicates_and_shape(key, value):
    problem = instance()
    problem[key] = value
    with pytest.raises(ValueError):
        mersenne.validate_instance(problem)
    with pytest.raises(ValueError):
        mersenne.verify_word(problem, [0, 0, 0])
    with pytest.raises(ValueError):
        mersenne.ideal_budget(problem, 1)


def test_strict_schema_rejects_extra_missing_fields_and_boolean_modulus():
    original = instance()
    bad = [dict(original, predicate="legacy"), dict(original, exponent=1)]
    for key in original:
        problem = deepcopy(original)
        del problem[key]
        bad.append(problem)
    problem = deepcopy(original)
    problem["field_modulus_coefficients"][0] = bool(problem["field_modulus_coefficients"][0])
    bad.append(problem)  # List equality alone would silently accept this.
    for problem in bad:
        with pytest.raises(ValueError):
            mersenne.validate_instance(problem)


@pytest.mark.parametrize("word", [[False, 0, 0], [-1, 0, 0], [32, 0, 0], [0.0, 0, 0]])
def test_malformed_witnesses_are_not_coerced(word):
    with pytest.raises(ValueError):
        mersenne.verify_word(instance(), word)


def test_scalar_contracts_reject_bool_and_out_of_range_without_coercion():
    for operation in (
        lambda: mersenne.reciprocal_trace(True, 2, 0),
        lambda: mersenne.reciprocal_trace(5, True, 0),
        lambda: mersenne.reciprocal_value(5, 2, True),
        lambda: mersenne.root_from_trace(5, 2, False, 0),
        lambda: mersenne.root_from_trace(5, 2, 0, False),
        lambda: mersenne.root_from_seed(5, 2, True, 0),
        lambda: mersenne.root_from_seed(5, 2, 0, True),
        lambda: mersenne.root_from_seed(5, 2, 0, 16),
        lambda: mersenne.finite_curve_count(5, 2, True),
        lambda: mersenne.ideal_budget(instance(), True),
    ):
        with pytest.raises(ValueError):
            operation()


@pytest.mark.parametrize("bits,s", [(3, 1), (3, 2), (5, 1), (5, 2), (5, 3), (5, 4)])
def test_quadratic_lift_equivalence_counts_and_false_zero_branch(bits, s):
    h, q = 1 << (s-1), 1 << bits
    for target in (0, 1):
        for word in range(q):
            x = element(bits, word)
            lifts = [v for label in range(q) if (
                (v := element(bits, label))**2+x**h*v+target*x**(2*h) == x)]
            accepted = mersenne.reciprocal_trace(bits, s, word) == target
            if word:
                assert len(lifts) == (2 if accepted else 0)
                for v in lifts:
                    y = v/(x**h)
                    assert y*y+y+target == x**(-((1 << s)-1))
            else:
                assert lifts == [field(bits).zero()]
                assert accepted == (target == 0)
            # An unguarded quadratic solver would falsely admit zero at b=1.
            guarded = bool(lifts) and (word != 0 or target == 0)
            assert guarded == accepted


def test_predicate_power_transfer_can_break_the_same_parity_problem():
    points, values = list(range(25)), [0]*25
    for index, value in zip((0, 1, 2, 4), (22, 13, 30, 5)):
        values[index] = value
    targets = [legacy_predicate(5, x) for x in values]
    problem = mersenne.make_instance(5, 2, points, targets, 3)
    legacy = {k: v for k, v in problem.items()
              if k not in ("problem_family", "schema_version", "s")}
    assert legacy_verify_word(legacy, values)
    transferred = [encoded(element(5, x)**21) for x in values]
    assert all(mersenne.reciprocal_trace(5, 2, x) == b
               for x, b in zip(transferred, targets))
    assert not mersenne.verify_word(problem, transferred)
    syndrome = [encoded(sum((element(5, a)**j*element(5, x)
                             for a, x in zip(points, transferred)), field(5).zero()))
                for j in range(3)]
    assert syndrome == [13, 27, 22]


def test_projected_affine_flat_can_exceed_the_lifted_affine_bound():
    # Halley's native-field countercontrol: x-only flats need not lift affinely.
    assert list(map(int, field(17).modulus().coeffs())) == [1, 0, 0, 1]+[0]*13+[1]
    points = [0x9579]
    for direction in (0x3377, 0x3451, 0x87b1, 0x136af):
        points += [point ^ direction for point in points]
    assert len(set(points)) == 16 and 0 not in points
    assert all(mersenne.reciprocal_trace(17, 3, point) == 1 for point in points)
    # Dimension four exceeds s=3. This is one local set, not an Hx=0 witness.
    assert len(points).bit_length()-1 > 3


def test_analytic_report_outward_rounding_and_saved_replay():
    root = Path(__file__).resolve().parents[1]
    report = mersenne.analytic_report()
    saved = json.loads((root/"research/reductions/mersenne_reciprocal_curve.json").read_text())
    assert saved == report
    assert report["changed_predicate_not_original_inverse_trace"]
    for key in ("classical_hardness_established", "quantum_advantage_established",
                "novelty_established", "compiled_quantum_algorithm",
                "independent_human_peer_review_complete"):
        assert report[key] is False
    for row in report["native_budgets"]:
        live = mersenne.ideal_budget(mersenne.native_instance(row["bits"]), row["radius"])
        assert Fraction(*row["beta"]) == live["beta"]
        for quantity, key in (("eta", "eta_power2_upper"), ("tail", "tail_power2_upper")):
            upper = Fraction(2)**row[key]
            assert upper/2 < live[quantity] <= upper
        lower = Fraction(*row["ideal_native_success_lower"])
        assert lower <= live["native_success_per_attempt_lower"] < lower+Fraction(1, 1 << 128)
        assert lower > Fraction(1, 9)
        assert not row["native_quantum_execution"]
        assert not row["native_classical_search_execution"]
        q, n, length = 1 << row["bits"], row["bits"], row["length"]
        oil = (1+live["eta"])*Fraction(q, q-1)**length/q**row["checks"]
        upper = Fraction(2)**row["independent_uniform_oil_success_power2_upper"]
        assert upper/2 < oil <= upper == Fraction(2)**(1-n*row["checks"])
        assert row["lifted_affine_dimension_upper"] == min(row["s"], n-4*row["s"]+4)
        assert not row["partial_norm_preserves_original_linear_parity"]


@pytest.mark.parametrize("bits,s", [(7, 1), (21, 4), (33, 7)])
def test_native_degree_contract_does_not_promote_general_controls(bits, s):
    with pytest.raises(ValueError):
        mersenne.native_instance(bits, s=s)
    control = mersenne.make_instance(bits, s, [0, 1, 2], [0, 0, 0], 1)
    row = mersenne.ideal_budget(control, 1)
    assert row["matches_growing_s_formula"]
    assert not row["canonical_research_parameters"]
    assert row["parameter_role"] != "CANONICAL_GROWING_GENUS_CANDIDATE"
    assert mersenne.verify_word(control, [0, 0, 0])


def test_target_length_rejected_before_element_validation(monkeypatch):
    original = instance()
    original["targets"] = [object()]*200_000

    def forbidden(*args, **kwargs):
        raise AssertionError("length mismatch reached backend validation")

    monkeypatch.setattr(mersenne, "_validate_arithmetic_shape", forbidden)
    for operation in (lambda: mersenne.validate_instance(original),
                      lambda: mersenne.make_instance(5, 2, [0, 1], original["targets"], 1)):
        with pytest.raises(ValueError, match="target length"):
            operation()


def test_binomial_recurrence_is_exact_at_every_small_cutoff():
    for length in range(2, 70):
        for radius in range(length+1):
            assert mersenne._binomial_prefix(length, radius) == sum(
                comb(length, j) for j in range(radius+1))


@pytest.mark.parametrize("bits", [17, 31, 61, 127])
def test_partial_norm_and_constant_degree_graph_identities(bits):
    s, remainder = (bits-3)//4, bits-4*((bits-3)//4)
    order, d = (1 << bits)-1, (1 << s)-1
    exponent = (1 << remainder)*sum(1 << (j*s) for j in range(4)) % order
    root_exponent = -pow(d, -1, order) % order
    assert exponent.bit_count() == 4 and gcd(exponent, order) == 1
    assert (-d*exponent) % order == (1 << remainder)-1
    assert ((1 << remainder)-1)*root_exponent % order == exponent
    for word in (0, 1, 2, 17, (1 << bits)-1):
        value = mersenne.partial_norm_value(bits, word)
        t = element(bits, word)
        assert value == encoded(t**exponent)
        assert mersenne.reciprocal_trace(bits, s, value) == int(
            (t**((1 << remainder)-1)).trace())
        target = int(t.trace())
        root = element(bits, mersenne.root_from_trace(bits, s, word, target))
        assert encoded(root**((1 << remainder)-1)) == value


@pytest.mark.parametrize("bits", [17, 31, 61, 127])
def test_linearized_adjoint_rank_and_constant_kernel_bound(bits):
    s, remainder = (bits-3)//4, bits-4*((bits-3)//4)
    samples = (0, 1, 17, (1 << bits)-1)
    for a, c in product(samples, repeat=2):
        A, C = element(bits, a), element(bits, c)
        basis = [element(bits, 1 << bit) for bit in range(bits)]
        columns = [encoded(A*x**(1 << s)+C*x**(1 << (s-1))+x) for x in basis]
        adjoint_columns = [encoded(x**(1 << s)+C*C*x*x+A*x) for x in basis]
        ranks = [nmod_mat([[column >> row & 1 for column in col]
                          for row in range(bits)], 2).rank()
                 for col in (columns, adjoint_columns)]
        assert ranks[0] == ranks[1]
        assert bits-ranks[0] <= min(s, remainder+4)


def test_partial_norm_rejects_out_of_regime_and_malformed_words():
    for bits in (True, 7, 21, 33, 129):
        with pytest.raises(ValueError):
            mersenne.partial_norm_value(bits, 1)
    for word in (True, -1, 1 << 17, 1.0):
        with pytest.raises(ValueError):
            mersenne.partial_norm_value(17, word)


def test_common_auxiliary_exclusion_is_not_native_unsatisfiability():
    bits, s, length = 5, 2, 5
    h = 1 << (s-1)
    for label in range(1 << bits):
        v = element(bits, label)
        roots = [word for word in range(1, 1 << bits) if (
            (x := element(bits, word))**(2*h)+v*x**h+x == v*v)]
        reachable = {0}
        for _ in range(length):
            reachable = {a ^ b for a in reachable for b in roots}
        assert 0 not in reachable

    # Native solutions still exist with coordinated, nonconstant auxiliaries.
    accepted = [x for x in range(1 << bits) if mersenne.reciprocal_trace(bits, s, x)]
    paths = {0: []}
    for _ in range(length):
        paths = {syndrome ^ x: path+[x] for syndrome, path in paths.items() for x in accepted}
    problem = mersenne.make_instance(bits, s, list(range(length)), [1]*length, 1)
    assert 0 in paths and mersenne.verify_word(problem, paths[0])

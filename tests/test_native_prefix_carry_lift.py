"""Actual mod9 carry equations, independent ANF and scoped prefix/filter means."""
from fractions import Fraction
from itertools import product
import json
import math
import subprocess

from flint import nmod_mat
import pytest

from theorems import native_prefix_carry_lift as C
from native_affine_fibre_relaxation import matrix_product
from native_short_preimage_reduction import PublicWordFamily


def evaluate_polys(polys, free):
    return tuple(sum(m["coefficient"]*math.prod(u**p for u, p in zip(free, m["powers"])) for m in poly) % 3 for poly in polys)


def canonical_ANF(values, k):
    """Independent full evaluation-basis interpolation over F3."""
    powers = tuple(product(range(3), repeat=k))
    free = powers
    matrix = [[math.prod(u**p for u, p in zip(point, exponent)) % 3 for exponent in powers] for point in free]
    answer = nmod_mat(matrix, 3).inv()*nmod_mat([[v] for v in values], 3)
    return tuple((exponent, int(answer[i, 0])) for i, exponent in enumerate(powers) if int(answer[i, 0]))


def small_family(q=9):
    pairs = (((1, 0), (0, 0)), ((0, 1), (0, 0)), ((1, 1), (1, 0)), ((2, 1), (1, 2)))
    return PublicWordFamily(q, 2, 1, 4, (pairs,))


def test_canonical_trit_lift_identity_holds_for_all_integer_residues_including_negative():
    for T in range(-200, 201):
        assert (T**3-3*T*(T-1)) % 9 == T % 3
    for t in range(3): assert t**3 % 9 == (t+3*t*(t-1)) % 9


def test_mod9_local_polynomial_is_the_actual_selector_not_a_linear_extension():
    for a, c, T in product(range(9), range(9), range(9)):
        t = T % 3
        actual = (a, c-a, -c)[t] % 9
        assert (a+(c-2*a)*T**3+3*a*T*(T-1)) % 9 == actual
    assert (1+(0-2)*2) % 9 != -0 % 9


@pytest.mark.parametrize("r", (2, 3, 16, 64))
def test_compact_carry_matches_actual_first_two_digits_but_not_a_full_root_claim(r):
    family = small_family(3**r)
    for target in ((0, 0), (7, 8)):
        circuit = C.compile_carry(family, 0, target)
        poly = circuit.expanded_polynomial()
        for free in product(range(3), repeat=2):
            word = circuit.word(free);actual = family.frequency(0, word)
            residual = tuple((x-y) % 9 for x, y in zip(actual, target))
            assert all(x % 3 == 0 for x in residual)
            assert circuit.evaluate(free) == tuple(x//3 for x in residual) == evaluate_polys(poly, free)
        assert circuit.record()["matching_mod9_implies_full_root_matching"] == (r == 2)


def test_zero_free_variable_prefix_still_has_an_honest_constant_carry_equation():
    pairs = (((1, 0), (0, 0)), ((0, 1), (0, 0)))
    family = PublicWordFamily(9, 2, 1, 2, (pairs,))
    circuit = C.compile_carry(family, 0, (7, 8))
    actual = family.frequency(0, circuit.word(()))
    assert circuit.evaluate(()) == tuple(((x-y) % 9)//3 for x, y in zip(actual, (7, 8)))
    assert evaluate_polys(circuit.expanded_polynomial(), ()) == circuit.evaluate(())


def test_divided_cube_is_not_an_ordinary_cube_in_characteristic3():
    # The ordinary F3 cube has no mixed terms; the divided integer cube does.
    u, v = 1, 1
    divided = ((u+v)**3-u**3-v**3)//3 % 3
    ordinary_mixed = ((u+v)**3-u**3-v**3) % 3
    assert divided == 2 and ordinary_mixed == 0


def test_carry_polynomial_is_unique_canonical_ANF_and_has_genuine_cubic_controls():
    p = json.loads(C.REPORT.read_text());has_cubic = False
    for c in p["bounded_carry_controls"]:
        for cohort in c.get("cohort_controls", []):
            k = cohort["compact_circuit"]["free_trits"]
            rows = cohort["complete_prefix_word_rows"]
            for i, poly in enumerate(cohort["canonical_polynomials"]):
                values = [row["next_digit_residual"][i] for row in rows]
                independent = canonical_ANF(values, k)
                assert independent == tuple((tuple(m["powers"]), m["coefficient"]) for m in poly)
                assert all(sum(power) <= 3 for power, _ in independent)
                has_cubic |= any(sum(power) == 3 for power, _ in independent)
    assert has_cubic


def test_compact_compiler_does_not_materialize_a_cubic_tensor_at_large_free_width():
    k = 1000
    pairs = (((1, 0), (0, 0)), ((0, 1), (0, 0)))+(((1, 1), (1, 0)),)*k
    family = PublicWordFamily(9, 2, 1, k+2, (pairs,))
    circuit = C.compile_carry(family, 0, (7, 8))
    assert len(circuit.pivot_forms) == 2
    assert all(len(form["coefficients"]) == k for form in circuit.pivot_forms)
    assert not circuit.record()["expanded_cubic_tensor_materialized"]
    free = tuple(i % 3 for i in range(k))
    sigma = family.frequency(0, circuit.word(free))
    assert circuit.evaluate(free) == tuple(((x-y) % 9)//3 for x, y in zip(sigma, (7, 8)))
    with pytest.raises(ValueError, match="expansion exceeds cap"):
        circuit.expanded_polynomial(cap=10000)


def test_output_minor_normalizes_cubic_forms_but_does_not_decouple_the_variables():
    pairs = small_family().paired_labels[0][:-1]+(((1, 0), (1, 1)),)
    family = PublicWordFamily(9, 2, 1, 4, (pairs,))
    circuit = C.compile_carry(family, 0, (7, 8))
    recipe = circuit.prefix_recipe
    cubic = tuple(tuple(circuit.pivot_weights[j][i]["cube"] for j in range(2)) for i in range(2))
    actual_minor = tuple(tuple(row[j] for j in recipe.pivot_columns) for row in recipe.matrix)
    assert cubic == actual_minor
    assert matrix_product(recipe.pivot_inverse, cubic, 3) == ((1, 0), (0, 1))
    for free in product(range(3), repeat=2):
        residual = circuit.evaluate(free)
        transformed = tuple(sum(a*b for a, b in zip(row, residual)) % 3 for row in recipe.pivot_inverse)
        assert all(x == 0 for x in transformed) == all(x == 0 for x in residual)
    # Dense forms share free variables; the invertible output change is not independent solving.
    assert any(sum(x != 0 for x in form["coefficients"]) > 1 for form in circuit.pivot_forms)


def test_nonfree_prefix_is_unsupported_not_no_native_words():
    family = PublicWordFamily(9, 1, 1, 1, ((((1,), (2,)),),))
    with pytest.raises(C.NonFreeRank): C.compile_carry(family, 0, (1,))
    assert family.frequency(0, (0,)) == (1,)


def test_many_free_variables_do_not_prove_an_inhomogeneous_target_is_solvable():
    # Full prefix rank, more free variables than the degree sum, yet no mod9 lift.
    pairs = (((1,), (0,)),)+(((0,), (0,)),)*10
    family = PublicWordFamily(9, 1, 1, 11, (pairs,))
    circuit = C.compile_carry(family, 0, (4,))
    polynomial = circuit.expanded_polynomial()
    assert polynomial == (({"powers": (0,)*10, "coefficient": 2},),)
    assert circuit.evaluate((0,)*10) == circuit.evaluate((2,)*10) == (2,)


def test_literature_gate_preserves_withdrawal_and_no_automatic_diagonal_transfer():
    p = json.loads((C.ROOT/"research/literature_audits/native_prefix_carry_sources.json").read_text())
    diagonal, withdrawn = p["records"]
    assert not diagonal["automatic_native_carry_solver_transfer_proved"]
    assert withdrawn["publication_status"] == "WITHDRAWN"
    assert not withdrawn["quantum_advantage_supporting_evidence_allowed"]
    assert not p["speedup_claim_allowed"]


@pytest.mark.parametrize("family,b,target", ((small_family(3), 0, (0, 0)), (small_family(), 1, (0, 0)),
                                            (small_family(), 0, (9, 0)), (small_family(), 0, (True, 0))))
def test_invalid_carry_requests_are_not_repaired(family, b, target):
    with pytest.raises(ValueError): C.compile_carry(family, b, target)


def test_fixed_label_uniform_higher_target_mean_is_exact_not_a_selected_target_promise():
    family = small_family()
    for low in product(range(3), repeat=2):
        acceptance = Fraction(0)
        for high in product(range(3), repeat=2):
            target = tuple(a+3*b for a, b in zip(low, high))
            circuit = C.compile_carry(family, 0, target)
            hits = sum(all(x == 0 for x in circuit.evaluate(free)) for free in product(range(3), repeat=2))
            acceptance += Fraction(hits, 9)
        assert acceptance/9 == Fraction(1, 9)


def test_prescribed_target_mean_requires_uniform_high_original_labels():
    # Exhaust the conditional actual original higher digits with low labels fixed.
    low_pairs = (((1,), (1,)), ((0,), (1,)))
    total = Fraction(0)
    for high in product(range(3), repeat=4):
        pairs = tuple(tuple(tuple(a+3*high[2*j+t] for a in label) for t, label in enumerate(pair))
                      for j, pair in enumerate(low_pairs))
        family = PublicWordFamily(9, 1, 1, 2, (pairs,))
        circuit = C.compile_carry(family, 0, (7,))
        total += Fraction(sum(circuit.evaluate((u,)) == (0,) for u in range(3)), 3)
    assert total/81 == Fraction(1, 3)
    # A single fixed higher-label assignment need not have this acceptance.
    fixed_pairs = (((4,), (4,)), ((0,), (1,)))
    fixed = C.compile_carry(PublicWordFamily(9, 1, 1, 2, (fixed_pairs,)), 0, (7,))
    assert Fraction(sum(fixed.evaluate((u,)) == (0,) for u in range(3)), 3) != Fraction(1, 3)


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_growing_prefix_filter_ledger_preserves_its_source_model_and_scope(n):
    L = C.prefix_filter_ledger(n, n, 1, n*n+24)
    assert L["free_native_word_trits_per_cohort"] == n*n+24-n
    assert L["uniform_higher_target_mean_acceptance"]["negative_exponent"] == n*(n-1)
    assert L["IID_uniform_higher_original_labels_conditioned_on_low_labels_required_for_prescribed_target_mean"]
    assert L["prescribed_target_fixed_conditioned_on_low_labels_before_higher_labels_required"]
    assert L["prefix_basis_and_cohort_weights_depend_only_on_low_labels_required"]
    assert not L["uniform_target_mean_is_a_per_dataset_prescribed_target_promise"]
    assert not L["later_digit_equations_proved_degree3"]
    assert not L["generic_carry_solvers_excluded"]


def test_live_report_keeps_zero_acceptance_and_mod9_full_root_difference():
    p = json.loads(C.REPORT.read_text());mismatch = False
    assert not p["accepted_speedup_candidate"] and not p["polynomial_cubic_solver_or_full_root_row_circuit"]
    for c in p["bounded_carry_controls"]:
        for control in c.get("cohort_controls", []):
            for row in control["complete_prefix_word_rows"]:
                mismatch |= row["matches_mod9_target"] and not row["matches_entire_root_target"]
    assert mismatch
    assert any(control["mod9_filter_acceptance"] == "0" for c in p["bounded_carry_controls"] for control in c.get("cohort_controls", []))


def test_independent_checker_replays_compact_and_canonical_carry_systems():
    checker = C.ROOT/"research/certificates/native_prefix_carry_crosscheck.js"
    p = subprocess.run(["node", str(checker)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


@pytest.mark.parametrize("mutation", ("constant", "form", "cubic", "word", "full_root", "law", "rank_one", "scope"))
def test_independent_checker_rejects_false_carry_or_prefix_claims(mutation, tmp_path):
    p = json.loads(C.REPORT.read_text());c = p["bounded_carry_controls"][1]["cohort_controls"][0]
    if mutation == "constant": c["compact_circuit"]["F3_constants"][0] = (c["compact_circuit"]["F3_constants"][0]+1) % 3
    if mutation == "form": c["compact_circuit"]["pivot_affine_forms"][0]["offset"] = (c["compact_circuit"]["pivot_affine_forms"][0]["offset"]+1) % 3
    if mutation == "cubic": c["canonical_polynomials"][0].append({"powers": [2, 2], "coefficient": 1})
    if mutation == "word": c["complete_prefix_word_rows"][0]["native_word"][0] = (c["complete_prefix_word_rows"][0]["native_word"][0]+1) % 3
    if mutation == "full_root": p["bounded_carry_controls"][2]["cohort_controls"][0]["compact_circuit"]["matching_mod9_implies_full_root_matching"] = True
    if mutation == "law": p["growing_prefix_filter_ledgers"][0]["uniform_target_mean_is_a_per_dataset_prescribed_target_promise"] = True
    if mutation == "rank_one": c["compact_circuit"]["divided_cubes_are_ordinary_rank_one_F3_cubes"] = True
    if mutation == "scope": p["accepted_speedup_candidate"] = True
    target = tmp_path/"forged.json";target.write_text(json.dumps(p))
    checker = C.ROOT/"research/certificates/native_prefix_carry_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert result.returncode != 0, mutation

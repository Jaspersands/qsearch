from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from theorems import ternary_sparse_reduction as reduction
from theorems.ternary_classical_sampling import valid


def problem(forms, offsets):
    return {"spins": len(forms[0]), "forms": forms, "offsets": offsets}


@pytest.mark.parametrize("coefficients", list(product((1, 2), repeat=4)))
def test_every_sign_and_offset_has_exactly_one_auxiliary_extension(coefficients):
    for offset in range(3):
        source = problem((coefficients,), (offset,))
        mapped = reduction.sparsify(source)
        assert len(mapped.additions) == 1
        counts = Counter()
        for x in product(range(3), repeat=4):
            extended = mapped.lift(x)
            assert valid(mapped.target, extended) == reduction.dense_valid(source, x)
            for auxiliary in range(3):
                if valid(mapped.target, (*x, auxiliary)):
                    counts[x] += 1
                    assert (*x, auxiliary) == extended
        assert counts == Counter({x: 1 for x in product(range(3), repeat=4) if reduction.dense_valid(source, x)})


def test_multi_gadget_projection_preserves_uniformity_gauge_and_dependent_forms():
    source = problem(((1, 1, 2, 1, 2, 0), (2, 2, 1, 2, 1, 0), (0, 0, 0, 0, 0, 0)), (0, 1, 2))
    mapped = reduction.sparsify(source)
    assert len(mapped.additions) == 4
    assert mapped.target["spins"] == 10
    assert len(mapped.target["forms"]) == 11
    # A native SAT census is independent of lift(); auxiliaries are not free advice.
    import pycosat
    from theorems.ternary_classical_sampling import decode, encode
    clauses, support = encode(mapped.target)
    support = set(support)
    counts = Counter()
    for model in pycosat.itersolve(clauses):
        word = decode(mapped.target, [lit for lit in model if abs(lit) in support])
        assert word == mapped.lift(word[:6])
        counts[word[:6]] += 1
    expected = {x for x in product(range(3), repeat=6) if reduction.dense_valid(source, x)}
    assert counts == Counter({x: 1 for x in expected})
    assert {x[-1] for x in expected} == {0, 1, 2}


@pytest.mark.parametrize("offset", (0, 1, 2))
def test_zero_constraints_and_no_gadget_case_are_not_dropped(offset):
    source = problem(((0, 0), (1, 2)), (offset, 0))
    mapped = reduction.sparsify(source)
    assert not mapped.additions and not mapped.pairs
    for x in product(range(3), repeat=2):
        assert mapped.lift(x) == x
        assert valid(mapped.target, x) == reduction.dense_valid(source, x)
    if not offset:
        assert not any(valid(mapped.target, x) for x in product(range(3), repeat=2))


def test_disjoint_short_words_annihilate_matrix_and_are_independent():
    mapped = reduction.sparsify(problem(((1, 2, 1, 2, 1),), (1,)))
    report = reduction.short_subcode(mapped.target, mapped.pairs)
    assert report["independent_short_subcode_dimension"] == 2
    assert report["all_ordered_offset_differences_are_1"]
    H = np.array(mapped.target["forms"], dtype=np.int64).T
    seen = set()
    for symbols in product(range(3), repeat=2):
        word = np.zeros(H.shape[1], dtype=np.int64)
        for (p, q), symbol in zip(mapped.pairs, symbols):
            word[p], word[q] = symbol, -symbol % 3
        assert np.all(H@word % 3 == 0)
        seen.add(tuple(word))
    assert len(seen) == 9


def test_code_quotient_recovers_original_dense_code_with_exact_gadget_multiplicity():
    source = problem(((1, 2, 1, 2), (2, 1, 2, 1)), (1, 2))
    mapped = reduction.sparsify(source)
    old = []
    for word in product(range(3), repeat=2):
        try:
            reduction.codeword(source, word)
            old.append(word)
        except ValueError:
            pass
    lifted = {mapped.lift_codeword(word, coins) for word in old for coins in product(range(3), repeat=2)}
    brute = set()
    for word in product(range(3), repeat=6):
        if all(sum(row[i]*x for row, x in zip(mapped.target["forms"], word)) % 3 == 0 for i in range(6)):
            brute.add(word)
    assert lifted == brute
    assert len(lifted) == len(old)*9 == 27
    assert Counter(mapped.project_codeword(word) for word in lifted) == Counter({word: 9 for word in old})
    with pytest.raises(ValueError):
        mapped.lift_codeword((1, 0), (0, 0))
    with pytest.raises(ValueError):
        mapped.project_codeword((1, 0, 0, 0, 0, 0))


def test_local_physical_ensemble_matches_primal_dual_certificate():
    report = reduction.pair_certificate()
    assert report["physical_vs_compressed_Gram_residual"] < 2e-15
    assert report["measurement_completeness_residual"] < 2e-15
    assert report["primal_dual_gap"] < 2e-15
    assert report["dual_slack_minimum_eigenvalue"] > -2e-15
    assert report["optimal_success_numeric_NOT_certificate"] == pytest.approx((3+2*np.sqrt(2))/6)


def optimum(H):
    words = [x for x in product(range(3), repeat=len(H[0])) if all(sum(a*v for a, v in zip(row, x)) % 3 == 0 for row in H)]
    gram = np.array([[(-.5)**sum(x != y for x, y in zip(a, b)) for a in words] for b in words])
    eigenvalues = np.linalg.eigvalsh(gram)
    assert min(eigenvalues) > -1e-12
    return float((sum(np.sqrt(np.maximum(0, eigenvalues)))/len(words))**2)


@pytest.mark.parametrize("H,tight", [(((1, 1),), True),
    (((1, 1, 0, 0), (0, 0, 1, 1)), True), (((1, 1, 1, 1),), False),
    (((1, 1, 0),), False)])
def test_full_code_genie_bound_against_independent_complete_Gram(H, tight):
    pairs = ((0, 1), (2, 3)) if len(H[0]) == 4 else ((0, 1),)
    p = problem(tuple(zip(*H)), [0]*len(H[0]))
    reduction.short_subcode(p, pairs)
    bound = ((3+2*np.sqrt(2))/6)**len(pairs)
    actual = optimum(H)
    assert actual <= bound+1e-12
    assert (abs(actual-bound) < 1e-12) == tight


@pytest.mark.parametrize("gadgets", (0, 1, 10, 100, 1000))
def test_outward_product_success_and_offset_distance_bounds(gadgets):
    report = reduction.success_bound(gadgets)
    lo, hi = map(Fraction, report["product_subcode_optimal_success_interval"])
    with localcontext() as ctx:
        ctx.prec = 120
        exact = ((Decimal(3)+2*Decimal(2).sqrt())/6)**gadgets
        assert Decimal(lo.numerator)/Decimal(lo.denominator) <= exact <= Decimal(hi.numerator)/Decimal(hi.denominator)
    assert hi-lo < Fraction(1, 1 << 110)
    assert Fraction(report["offset_source_TV_lower_if_all_ordered_differences_1"]) == 1-Fraction(1, 3**gadgets)
    assert not report["all_sampling_or_sparsification_algorithms_ruled_out"]


def test_correlated_gadget_offsets_break_character_orthogonality():
    omega = np.exp(2j*np.pi/3)
    independent = sum(omega**((a-b) % 3) for a, b in product(range(3), repeat=2))/9
    paired = sum(omega**((a-(a+1)) % 3) for a in range(3))/3
    assert abs(independent) < 1e-15
    assert abs(paired) == pytest.approx(1)
    # Positive decoding error does not imply hard sampling: this target is {0}.
    p = problem(((1,), (1,)), (1, 2))
    assert [x for x in product(range(3), repeat=1) if valid(p, x)] == [(0,)]
    assert optimum(((1, 1),)) < 1


def test_public_basis_change_preserves_solutions_and_exact_decoding_code():
    p = problem(((1, 1, 0, 0), (0, 1, 2, 0), (1, 0, 0, 1)), (0, 1, 2))
    dense, T = reduction.scramble(p, 7191)
    array = np.array([[int(T[r, c]) for c in range(4)] for r in range(4)])
    for z in product(range(3), repeat=4):
        x = tuple(map(int, array@np.array(z) % 3))
        assert valid(p, x) == reduction.dense_valid(dense, z)
    for d in product(range(3), repeat=3):
        old = np.array(p["forms"]).T@np.array(d) % 3
        new = np.array(dense["forms"]).T@np.array(d) % 3
        assert np.all(old == 0) == np.all(new == 0)


def test_overlap_and_wrong_column_witnesses_fail_closed():
    p = problem(((1, 0), (1, 0), (1, 0), (0, 1)), (1, 2, 0, 0))
    for pairs in (((0, 1), (1, 2)), ((0, 3),), ((0, 0),), ((-1, 2),), ((0, True),)):
        with pytest.raises(ValueError):
            reduction.short_subcode(p, pairs)
    with pytest.raises(ValueError):
        reduction.sparsify(problem(((True, 0),), (1,)))
    with pytest.raises(ValueError):
        reduction.sparsify(problem(((3, 0),), (1,)))
    with pytest.raises(ValueError):
        reduction.success_bound(-1)
    mapped = reduction.sparsify(problem(((1, 1, 1, 1),), (0,)))
    with pytest.raises(ValueError):
        mapped.lift((0, 1, 2))

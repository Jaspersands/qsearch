from dataclasses import replace
from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest

import affine_converse as a


def all_spaces(n):
    spaces = {(0,)}
    pending = [(0,)]
    while pending:
        v = pending.pop()
        for x in range(n):
            w = tuple(sorted(set(v) | {x ^ y for y in v}))
            if w not in spaces:
                spaces.add(w)
                pending.append(w)
    return sorted(spaces)


@pytest.mark.parametrize("c", [F(0), F(1, 3), F(1, 2), F(13, 20), F(1)])
def test_four_message_all_covariant_affine_optimum(c):
    q, effects = a.four_message(c)
    result = a.audit(q, effects)
    assert result["mean_unresolved_bits"] == 4*c*c-c**4
    z = (F(3), F(1), F(1), -F(7, 3), F(1), -F(7, 3), -F(7, 3), F(1))
    spaces = [coset for v in all_spaces(8) for coset in a.cosets(v, 8)]
    assert len(spaces) == 51
    for coset in spaces:
        assert sum(z[y] for y in coset)/len(coset) <= 3-(len(coset).bit_length()-1)
    assert sum(x*y for x, y in zip(q, z)) == result["mean_unresolved_bits"]
    assert result["fixed_instance_Gibbs_sampler_certified"] is False
    assert result["efficient_for_growing_blocks_certified"] is False


def test_negative_overlaps_require_affine_offsets_not_negative_probabilities():
    q = (F(1, 10), F(3, 10), F(3, 10), F(3, 10))
    mixtures = [((0, 1, 2, 3), F(2, 5))]
    mixtures += [(pair, F(1, 5)) for pair in ((1, 2), (1, 3), (2, 3))]
    result = a.audit(q, a.mixture_effects(q, mixtures))
    assert result["mean_unresolved_bits"] == F(3, 5)
    assert a.gram_from_q(q)[0][1:] == (-F(1, 5),)*3
    assert any(0 not in b.frequency_coset for b in result["branches"])
    z = (-3, 1, 1, 1)
    for v in all_spaces(4):
        for coset in a.cosets(v, 4):
            assert F(sum(z[y] for y in coset), len(coset)) <= 2-(len(coset).bit_length()-1)
    assert sum(x*y for x, y in zip(q, z)) == F(3, 5)


@pytest.mark.parametrize("n", [2, 4, 8])
def test_all_local_directions_and_cosets_with_independent_physical_povm(n):
    mixtures = [(coset, F(1)) for v in all_spaces(n) for coset in a.cosets(v, n)]
    mixtures = [(coset, weight/len(mixtures)) for coset, weight in mixtures]
    q = tuple(sum(weight/len(coset) for coset, weight in mixtures if y in coset)
              for y in range(n))
    effects = a.mixture_effects(q, mixtures)
    result = a.audit(q, effects)
    actual = {}
    # Construct effects directly in the physical character basis, using
    # inverse square roots of q, not contribution Gram entries.
    for coset, weight in mixtures:
        if len(coset) == 1:
            continue
        direction = tuple(sorted(y ^ coset[0] for y in coset))
        v = a.annihilator(direction, n)
        for labels in a.cosets(v, n):
            s = labels[0]
            vector = np.array([a.character(s, y)/np.sqrt(float(q[y]))
                               if y in coset else 0. for y in range(n)])
            key = (v, s)
            actual.setdefault(key, np.zeros((n, n)))
            actual[key] += float(weight)/(len(coset)**2)*np.outer(vector, vector)
    states = np.array([[np.sqrt(float(q[y]))*a.character(y, d)
                        for d in range(n)] for y in range(n)])
    for effect in effects:
        operator = actual[(effect.label_direction, effect.label_coset_representative)]
        assert np.linalg.eigvalsh(operator).min() >= -1e-12
        assert np.allclose(states.T@operator@states, np.array(effect.gram, dtype=float), atol=1e-12)
    residual = np.eye(n)-sum(actual.values())
    assert np.linalg.eigvalsh(residual).min() >= -1e-12
    q_residual = np.array(result["residual_spectrum"], dtype=float)
    assert np.allclose(np.diag(residual)*np.array(q, dtype=float), q_residual, atol=1e-12)


@pytest.mark.parametrize("q,coset", [((F(0), F(1)), (1,)),
                                    ((F(0), F(1, 2), F(1, 2), F(0)), (1, 2)),
                                    ((F(1, 2), F(0), F(1, 2), F(0)), (0, 2))])
def test_singular_spectra_need_no_inverse_or_regularization(q, coset):
    result = a.audit(q, a.mixture_effects(q, [(coset, F(1))]))
    assert result["source_reconstructed_exactly"] is True
    assert all(q[y] > 0 for branch in result["branches"] for y in branch.frequency_coset)
    assert result["mean_unresolved_bits"] == (len(q)//len(coset)).bit_length()-1


def test_empty_information_measurement_is_not_a_decoder():
    result = a.audit((F(1, 4),)*4, [])
    assert result["mean_unresolved_bits"] == 2
    assert len(result["branches"]) == 4


def test_non_covariant_usd_is_not_accepted_as_independent_branch_law():
    q = (F(3, 4), F(1, 4))
    effects = [a.Effect((0,), 0, ((F(1, 2), 0), (0, 0))),
               a.Effect((0,), 1, ((0, 0), (0, F(1, 4))))]
    # A physical but asymmetric USD: the residual Gram remains positive.
    assert a.psd(((F(1, 2), F(1, 2)), (F(1, 2), F(3, 4))))
    with pytest.raises(ValueError, match="covariant"):
        a.audit(q, effects)
    twirled = [a.Effect((0,), 0, ((F(3, 8), 0), (0, 0))),
               a.Effect((0,), 1, ((0, 0), (0, F(3, 8))))]
    result = a.audit(q, twirled)
    assert result["mean_unresolved_bits"] == F(5, 8)


def test_minimum_error_measurement_is_outside_unambiguous_class():
    q = (F(9, 25), F(16, 25))
    k0 = ((F(49, 50), -F(7, 50)), (-F(7, 50), F(1, 50)))
    k1 = ((F(1, 50), -F(7, 50)), (-F(7, 50), F(49, 50)))
    assert a.psd(k0) and a.psd(k1)
    assert tuple(tuple(k0[i][j]+k1[i][j] for j in range(2)) for i in range(2)) == a.gram_from_q(q)
    with pytest.raises(ValueError, match="unambiguous"):
        a.audit(q, [a.Effect((0,), 0, k0), a.Effect((0,), 1, k1)])


def test_codeword_probability_is_not_coherent_superposition_probability():
    q, w = (F(3, 4), F(1, 4)), F(1, 2)
    result = a.audit(q, a.mixture_effects(q, [((0, 1), w), ((0,), 1-w)]))
    p_codeword = sum(b.weight for b in result["branches"] if len(b.frequency_coset) == 2)
    # The normalized sum of the two nonorthogonal states is frequency |0>.
    p_superposition = w/(2*q[0])
    assert p_codeword == F(1, 2) and p_superposition == F(1, 3)


def test_fixed_sign_counterexample_and_full_sign_average():
    result = a.fixed_sign_countercontrol()
    first = result["cases"][0]
    assert F(first["target_zero"]) == F(79, 142)
    assert F(first["proposal_zero"]) == F(65, 128)
    assert F(first["tv"]) == F(441, 9088) > F(3, 64)
    assert len(result["cases"]) == 16
    assert result["fixed_zero_sign_exceeds_average_bound"] is True
    assert result["all_sign_average_obeys_bound"] is True
    assert F(result["all_sign_mean_tv"]) <= F(3, 64)


@pytest.mark.parametrize("matrix,expected", [(((0, 1), (1, 0)), False),
                                            (((0, 0), (0, 1)), True),
                                            (((1, 1), (1, 1)), True),
                                            (((1, 2), (2, 1)), False),
                                            (((1, 1), (0, 1)), False)])
def test_psd_singular_and_adversarial_pivots(matrix, expected):
    assert a.psd(matrix) is expected


def test_residual_budget_and_duplicate_validation():
    effects = a.mixture_effects((F(3, 4), F(1, 4)), [((0, 1), F(3, 4))])
    with pytest.raises(ValueError, match="budget"):
        a.audit((F(3, 4), F(1, 4)), effects)
    valid = a.mixture_effects((F(1, 2),)*2, [((0, 1), F(1, 2))])
    with pytest.raises(ValueError, match="duplicate"):
        a.audit((F(1, 2),)*2, valid+[valid[0]])
    with pytest.raises(ValueError, match="PSD"):
        a.audit((F(1, 2),)*2, [replace(valid[0], gram=((-F(1), 0), (0, 0)))])


@pytest.mark.parametrize("q", [(0.5, 0.5), (1, 1), (F(-1, 4), F(5, 4)),
                              (F(1, 3),)*3, (F(1, 32),)*32])
def test_bad_inputs_and_exponential_caps_fail_closed(q):
    with pytest.raises(ValueError):
        a.audit(q, [])


def test_every_three_bit_affine_direction_has_transposed_rank_condition():
    def rank(vectors):
        span = {0}
        for x in vectors:
            span |= {x ^ y for y in tuple(span)}
        return len(span).bit_length()-1
    # Independent exhaustive row and column ranks for every 3x3 binary map
    # and every canonical residual subspace. No random-rank assumption.
    for rows in product(range(8), repeat=3):
        for v in all_spaces(8):
            basis, span = [], {0}
            for x in v:
                if x not in span:
                    basis.append(x)
                    span |= {x ^ y for y in tuple(span)}
            constraints = []
            for u in basis:
                row = 0
                for j in range(3):
                    if (u >> j) & 1:
                        row ^= rows[j]
                constraints.append(row)
            columns = [sum(((row >> j) & 1) << i for i, row in enumerate(constraints))
                       for j in range(3)]
            assert rank(constraints) == rank(columns)

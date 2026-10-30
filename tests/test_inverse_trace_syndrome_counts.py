from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import product
from operator import xor as xor_pair

import pytest

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_syndrome_counts import syndrome_count_error, partial_transcript_error


@pytest.mark.parametrize("bits,points,targets,K", [
    (2, [0, 1, 2, 3], [0, 1, 0, 1], 1),
    (2, [3, 1, 2, 0], [1, 1, 0, 0], 2),
    (3, [7, 0, 2, 4, 1], [0, 1, 1, 0, 1], 2),
])
def test_every_syndrome_count_matches_full_fourier_expansion(bits, points, targets, K):
    q, m = 1 << bits, len(points)
    values = [element(bits, i) for i in range(q)]
    sign = lambda v: 1-2*int(v.trace())
    kl = {encoded(t): sum(sign(z+t/z) for z in values[1:]) for t in values}
    alphabets = [[x for x in range(q) if reciprocal_trace(bits, x) == b] for b in targets]
    counts = Counter()
    for word in product(*alphabets):
        h = tuple(encoded(sum((element(bits, x)*element(bits, a)**j
                               for a, x in zip(points, word)), field(bits).zero())) for j in range(K))
        counts[h] += 1
    frequencies = []
    for coefficients in product(values, repeat=K):
        transform = 1
        for a, b in zip(points, targets):
            p = sum((c*element(bits, a)**j for j, c in enumerate(coefficients)), field(bits).zero())
            transform *= q*int(p == 0)+(1-2*b)*(1+kl[encoded(p)])
        frequencies.append((coefficients, transform))
    for h in product(range(q), repeat=K):
        raw = sum(sign(sum((c*element(bits, v) for c, v in zip(coefficients, h)),
                           field(bits).zero()))*transform for coefficients, transform in frequencies)
        assert Fraction(raw, q**m) == Fraction(q**K*counts[h], (q//2)**m)


def test_complete_twisted_kloosterman_transform_including_zero():
    bits, q = 3, 8
    values = [element(bits, i) for i in range(q)]
    sign = lambda v: 1-2*int(v.trace())
    kl = {encoded(t): sum(sign(z+t/z) for z in values[1:]) for t in values}
    for a in values[1:]:
        for lam in values:
            actual = sum(kl[encoded(a*x)]*sign(lam*x) for x in values)
            assert actual == (0 if lam == 0 else q*sign(a/lam))


@pytest.mark.parametrize("bits,first_surplus", [(17, 45), (31, 52), (61, 84)])
def test_pointwise_bound_threshold_is_not_the_old_average_residual(bits, first_surplus):
    K = bits*bits//8
    assert syndrome_count_error(bits, K+first_surplus, K) < 1
    assert syndrome_count_error(bits, K+first_surplus-1, K) >= 1
    old_surplus = (4*K+bits-1)//bits
    assert syndrome_count_error(bits, K+old_surplus, K) > 1


def test_partial_observation_bound_is_not_full_native_sampling():
    n, N, K = 61, 61*61, 61*61//8
    assert partial_transcript_error(n, N, K, N-560) < Fraction(1, 2**299)
    assert partial_transcript_error(n, N, K, N-K) is None
    assert partial_transcript_error(n, N, K, N) is None
    assert partial_transcript_error(n, N, K, 0) == 0
    assert syndrome_count_error(3, 5, 0) == 0
    assert partial_transcript_error(3, 5, 0, 5) == 0


def test_even_empty_observation_needs_a_certified_nonempty_initial_fiber():
    accepted = [x for x in range(4) if reciprocal_trace(2, x) == 0]
    assert accepted == [0, 1]
    assert all(x ^ y != 2 for x, y in product(accepted, repeat=2))
    assert partial_transcript_error(2, 2, 1, 0) is None


def test_adaptive_variable_length_transcript_has_the_same_count_likelihood_ratio():
    bits, q, N, K = 3, 8, 6, 1
    targets = [0, 1, 0, 1, 1, 0]
    alphabets = [[x for x in range(q) if reciprocal_trace(bits, x) == b] for b in targets]
    words = list(product(*alphabets))
    xor = lambda values: reduce(xor_pair, values, 0)
    native = [w for w in words if xor(w) == 0]

    def transcript(word):
        if word[0] == 0:
            return ((0, 0),)
        second = 1 if word[0] == 3 else 2
        return ((0, word[0]), (second, word[second]))

    proposed, target = Counter(map(transcript, words)), Counter(map(transcript, native))
    assert {record[-1][0] for record in proposed} == {0, 1, 2}
    full_g = Fraction(q*len(native), (q//2)**N)
    residual_errors = []
    for record, frequency in proposed.items():
        observed = dict(record)
        hidden = [i for i in range(N) if i not in observed]
        rhs = xor(observed.values())
        count = sum(xor(rest) == rhs for rest in product(*(alphabets[i] for i in hidden)))
        g = Fraction(q*count, (q//2)**len(hidden))
        actual_ratio = Fraction(target[record], len(native))/Fraction(frequency, len(words))
        assert actual_ratio == g/full_g
        residual_errors.append(abs(g-1))
    tv = sum(abs(Fraction(target[t], len(native))-Fraction(proposed[t], len(words)))
             for t in proposed)/2
    full_error = abs(full_g-1)
    assert full_error < 1
    assert tv <= (max(residual_errors)+full_error)/(2*(1-full_error))

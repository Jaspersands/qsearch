from fractions import Fraction as F
import math
import random

import numpy as np
import pytest

from fermion_sampler import (acceptance, amplitudes, boundary, chord_word, coin,
    condition, decode, determinant, matrix_function, minor, perturbation_bound,
    pfaffian, prepare, probability, root, sample, word_phase)
from audit_controls import (coherent_reference, dense_pilot, dpp_branch_law,
                            rational_law_control)


CASES = [
    (2, [(0, 1)]),
    (5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
    (5, [(0, 1), (0, 2), (0, 3), (0, 4)]),
    (6, [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)]),
    (6, [(0, 1), (1, 2), (3, 4)]),
    (3, [(0, 1), (1, 2), (2, 0)]),
    (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    (4, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0)]),
    (4, [(i, j) for i in range(4) for j in range(i + 1, 4)]),
    (6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]),
]


@pytest.mark.parametrize("n,edges", CASES)
def test_incidence_phase_and_fiber_bijection(n, edges):
    model = root(n, edges)
    pairs = set()
    for y in range(1 << len(edges)):
        x, c = boundary(model, y), chord_word(model, y)
        assert decode(model, x, c) == y
        assert word_phase(model, y)[1] == x
        pairs.add((x, c))
    assert len(pairs) == 1 << len(edges)
    assert model.cycle_rank == len(edges) - n + len(set(model.components))


@pytest.mark.parametrize("n,edges", CASES)
@pytest.mark.parametrize("beta", [0.0, 0.19, 0.8, 3.0])
def test_full_probability_and_signed_coherent_transform(n, edges, beta):
    js = [(-1 if j % 2 else 1) * (0.3 + j / (2 * len(edges)))
          for j in range(len(edges))]
    model = root(n, edges, js)
    prepared = prepare(model, beta, bits=40)
    exact = dense_pilot(model, beta)
    reconstructed = coherent_reference(prepared)
    assert np.linalg.norm(reconstructed - exact) < 2e-9
    law = np.array([float(probability(prepared, y)) for y in range(len(exact))])
    assert np.max(np.abs(law - exact ** 2)) < 2e-9
    assert not prepared.native_error_certified


@pytest.mark.parametrize("n,edges", CASES)
def test_rational_backend_all_branches_and_exact_rejection_envelope(n, edges):
    p = prepare(root(n, edges), 0.7, bits=12)
    report = rational_law_control(p)
    for name in ("target_normalized_exactly", "proposal_normalized_exactly",
                 "envelope_holds_exactly", "all_dpp_branches_exact"):
        assert report[name]
    assert F(report["accepted_mass"]) == F(1, 1 << p.model.cycle_rank)


@pytest.mark.parametrize("size", range(9))
def test_pfaffian_square_equals_determinant_exactly(size):
    rng = random.Random(size)
    a = [[F(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            a[i][j] = F(rng.randrange(-8, 9), 7)
            a[j][i] = -a[i][j]
    assert pfaffian(a) ** 2 == determinant(a)


def test_cycle_sector_mixture_is_not_native_pilot():
    p = prepare(root(4, CASES[7][1]), 1.2)
    report = rational_law_control(p)
    assert report["incoherent_shortcut_tv"] > 0.7
    assert np.linalg.norm(coherent_reference(p) - dense_pilot(p.model, 1.2)) < 1e-8


def test_fixed_flux_quotient_collapses_nonempty_canonical_word():
    model = root(4, CASES[6][1])
    cycle = (1 << len(model.edges)) - 1
    assert boundary(model, cycle) == 0
    assert word_phase(model, cycle) == (2, 0)
    assert decode(model, 0, 0) != decode(model, 0, 1)


def test_singular_zero_temperature_and_zero_couplings():
    for beta, js in [(0, [1, 1, 1]), (5, [0, 0, 0])]:
        p = prepare(root(3, CASES[5][1], js), beta)
        assert probability(p, 0) == 1
        assert all(probability(p, y) == 0 for y in range(1, 8))
        assert sample(p, random.Random(13))["word"] == 0


def test_zero_probability_dpp_branches_are_not_conditioned_on():
    p = prepare(root(3, [(0, 1)]), 0)
    assert dpp_branch_law(p.sectors[0].marginal) == {0: F(1)}
    with pytest.raises(ValueError, match="zero-probability"):
        condition(((F(0),),), True)
    with pytest.raises(ValueError, match="zero-probability"):
        condition(((F(1),),), False)


def test_disconnected_components_require_separate_parity():
    model = root(5, [(0, 1), (2, 3)])
    with pytest.raises(ValueError, match="EACH"):
        decode(model, (1 << 0) | (1 << 2), 0)
    with pytest.raises(ValueError, match="EACH"):
        decode(model, 1 << 4, 0)


def test_no_dense_hilbert_space_in_large_forest(monkeypatch):
    import scipy.linalg
    monkeypatch.setattr(scipy.linalg, "expm", lambda *_: pytest.fail("dense exponential"))
    model = root(64, [(i, (i - 1) // 2) for i in range(1, 64)])
    p = prepare(model, 0.4, bits=16)
    rng = random.Random(781)
    for _ in range(3):
        draw = sample(p, rng)
        assert draw["trials"] == 1
        assert decode(model, boundary(model, draw["word"]), 0) == draw["word"]
    assert len(p.sectors[0].k) == 64


def test_nonhermitian_kernel_is_retained():
    p = prepare(root(2, [(0, 1)]), 0.9)
    k = p.sectors[0].marginal
    assert k[0][1] == -k[1][0] != 0
    assert dpp_branch_law(k)[3] > 0


def test_conditional_error_bound_is_not_a_front_end_certificate():
    assert perturbation_bound(8, 2, F(1, 1 << 40), F(1, 1 << 40)) < F(1, 10**6)
    assert perturbation_bound(8, 2, F(0), F(0)) == 0
    assert perturbation_bound(8, 2, F(1, 8), F(1)) == 1
    with pytest.raises(ValueError):
        perturbation_bound(8, 2, F(1), F(0))


def test_rejection_cap_fails_explicitly():
    class RejectingRng:
        def randrange(self, stop):
            return stop - 1
    p = prepare(root(3, CASES[5][1]), 0)
    with pytest.raises(RuntimeError, match="INCONCLUSIVE"):
        sample(p, RejectingRng(), max_trials=1)


@pytest.mark.parametrize("n,edges,js", [
    (True, [], None), (0, [], None), (2, [(0, 0)], None),
    (2, [(0, 2)], None), (2, [(0, 1), (1, 0)], None),
    (2, [(0, 1)], []), (2, [(0, 1)], [math.inf]),
    (2, [(0, 1)], [1.1]), (2, [(0, 1)], [True]),
])
def test_invalid_native_inputs(n, edges, js):
    with pytest.raises(ValueError):
        root(n, edges, js)


@pytest.mark.parametrize("beta", [-1, float("inf"), float("nan"), True])
def test_invalid_beta(beta):
    with pytest.raises(ValueError):
        matrix_function(root(2, [(0, 1)]), beta)


def test_work_cap_and_invalid_probability():
    model = root(4, CASES[7][1])
    with pytest.raises(ValueError, match="cycle-rank cap"):
        prepare(model, 0.1, max_cycle_rank=1)
    with pytest.raises(ValueError):
        prepare(model, 0.1, bits=100)
    with pytest.raises(ValueError):
        acceptance((F(0), F(0)), 0)
    with pytest.raises(ValueError):
        coin(F(3, 2), random.Random(1))
    with pytest.raises(ArithmeticError, match="never clip"):
        condition(((F(-1),),), False)


def test_nonstandard_generator_order_keeps_clifford_phases():
    edges = [CASES[8][1][i] for i in (4, 1, 5, 0, 3, 2)]
    model = root(4, edges, [1, -0.5, 0, 0.25, -1, 0.7])
    p = prepare(model, 2, bits=40)
    assert np.linalg.norm(coherent_reference(p) - dense_pilot(model, 2)) < 1e-8


def test_empty_hamiltonian_keeps_all_native_labels_empty():
    model = root(3, [])
    p = prepare(model, 20)
    assert probability(p, 0) == 1
    assert sample(p, random.Random(7)) == {"word": 0, "trials": 1}

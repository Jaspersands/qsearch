"""Physical finite-density checks, not scalable-source or learner tests."""

from itertools import product

import numpy as np
import pytest

from theorems import skew_bell_mixed_reference as reference


CASES = [(3, 1, 1), (3, 1, 2), (3, 2, 1), (3, 2, 2),
         (5, 2, 0), (5, 0, 2), (5, 3, 0), (5, 0, 3)]


def generic_mixed(p, seed):
    rng = np.random.default_rng(seed)
    matrix = rng.normal(size=(p, p)) + 1j * rng.normal(size=(p, p))
    rho = matrix @ matrix.conj().T + np.eye(p)
    return rho / np.trace(rho)


def projector(vector):
    vector = np.asarray(vector, dtype=complex)
    vector /= np.linalg.norm(vector)
    return np.outer(vector, vector.conj())


def assert_law(law):
    assert law.min() >= -2e-12
    assert law.sum() == pytest.approx(1, abs=2e-12)


@pytest.mark.parametrize("p", [3, 5])
def test_weyl_bell_labels_and_elementary_bell_measurement(p):
    bell = reference.bell_basis(p)
    np.testing.assert_allclose(bell.conj().T @ bell, np.eye(p * p), atol=2e-14)
    omega = np.exp(2j * np.pi / p)
    fourier = omega ** np.outer(np.arange(p), np.arange(p)) / np.sqrt(p)
    # |r,s> -> |r-s,s>, then inverse Fourier on the second register.
    subtract = np.zeros((p * p, p * p))
    for r, s in product(range(p), repeat=2):
        subtract[((r - s) % p) * p + s, r * p + s] = 1
    analyzer = np.kron(np.eye(p), fourier.conj().T) @ subtract
    for z, x in product(range(p), repeat=2):
        weyl = reference.weyl_operator(p, z, x)
        np.testing.assert_allclose(bell[:, z * p + x], weyl.reshape(-1) / np.sqrt(p))
        probability = abs(analyzer @ bell[:, z * p + x]) ** 2
        expected = np.zeros(p * p)
        expected[x * p + z] = 1  # computational outputs (shift, phase)
        np.testing.assert_allclose(probability, expected, atol=2e-14)


@pytest.mark.parametrize("p,a,b", CASES)
def test_public_skew_is_inverse_on_even_registers(p, a, b):
    permutation = reference.skew_permutation(p, a, b)
    np.testing.assert_array_equal(np.sort(permutation), np.arange(p**4))
    matrix = np.array([[a, b], [b, -a]]) % p
    np.testing.assert_array_equal(matrix.T @ matrix % p, -np.eye(2, dtype=int) % p)
    for source, (r, s, t, u) in enumerate(product(range(p), repeat=4)):
        output = np.unravel_index(permutation[source], (p,) * 4)
        assert output[0] == r and output[2] == t
        np.testing.assert_array_equal(np.array([output[1], output[3]]) @ matrix % p, [s, u])


@pytest.mark.parametrize("p,a,b", CASES)
@pytest.mark.parametrize("seed", [123, 987])
def test_generic_mixed_physical_marginal_matches_independent_fourier(p, a, b, seed):
    rho = generic_mixed(p, seed)
    original = rho.copy()
    # These fixtures are neither computational-diagonal nor stabilizer-diagonal:
    # every nonidentity Pauli coefficient is nonzero, so the weak group is trivial.
    assert np.linalg.norm(rho - np.diag(np.diag(rho))) > 0.01
    assert min(abs(np.trace(rho @ reference.weyl_operator(p, z, x)))
               for z, x in product(range(p), repeat=2) if (z, x) != (0, 0)) > 1e-5
    result = reference.simulate_skew_bell_mixed(rho, p, a, b)
    for law in [result.four_copy_joint, result.eight_copy_joint,
                result.four_copy_first_marginal, result.eight_copy_first_marginal]:
        assert_law(law)
    expected = reference.fourier_marginal(rho, p, a, b)
    np.testing.assert_allclose(result.eight_copy_first_marginal, expected, atol=2e-12, rtol=0)
    assert result.four_copy_source_copies == 4
    assert result.difference_source_copies == 8
    assert result.dense_dimension == p**4 <= reference.MAX_FOUR_COPY_DIM
    assert not result.physical_quantum_backend
    np.testing.assert_array_equal(rho, original)


def test_born_table_matches_elementary_analyzer_without_fourier_shortcut(monkeypatch):
    p = 3
    rho = generic_mixed(p, 17)
    def forbidden(*args, **kwargs):
        raise AssertionError("physical branch must not call coefficient/Fourier helpers")
    monkeypatch.setattr(reference, "fourier_marginal", forbidden)
    monkeypatch.setattr(reference, "_characteristic_squared", forbidden)
    monkeypatch.setattr(reference, "weyl_operator", forbidden)
    actual = reference.four_copy_bell_law(rho, p, 1, 1)
    omega = np.exp(2j * np.pi / p)
    f_dagger = omega ** (-np.outer(np.arange(p), np.arange(p))) / np.sqrt(p)
    subtract = np.zeros((p * p, p * p))
    for r, s in product(range(p), repeat=2):
        subtract[((r - s) % p) * p + s, r * p + s] = 1
    pair_analyzer = np.kron(np.eye(p), f_dagger) @ subtract
    # Independent dense permutation construction, including tensor ordering.
    skew = np.zeros((p**4, p**4))
    for digits in product(range(p), repeat=4):
        r, s, t, u = digits
        out = (r, (-s - u) % p, t, (-s + u) % p)
        skew[np.ravel_multi_index(out, (p,) * 4), np.ravel_multi_index(digits, (p,) * 4)] = 1
    circuit = np.kron(pair_analyzer, pair_analyzer) @ skew
    density = np.kron(np.kron(np.kron(rho, rho), rho), rho)
    measured = np.diag(circuit @ density @ circuit.conj().T).real
    # Analyzer outputs (x1,z1,x2,z2); the reference reports (z1,x1,z2,x2).
    expected = measured.reshape((p,) * 4).transpose(1, 0, 3, 2)
    np.testing.assert_allclose(actual, expected, atol=2e-14)


@pytest.mark.parametrize("p,a,b", [(3, 1, 1), (5, 0, 2)])
def test_difference_is_of_independent_batches_with_within_batch_control(p, a, b):
    result = reference.simulate_skew_bell_mixed(generic_mixed(p, 741), p, a, b)
    first = result.four_copy_first_marginal
    expected = np.zeros((p, p))
    for z, x, v, w in product(range(p), repeat=4):
        expected[(v - z) % p, (w - x) % p] += first[z, x] * first[v, w]
    np.testing.assert_allclose(result.eight_copy_first_marginal, expected, atol=2e-14)
    within_batch = np.zeros((p, p))
    for z, x, v, w in product(range(p), repeat=4):
        within_batch[(v - z) % p, (w - x) % p] += result.four_copy_joint[z, x, v, w]
    if p == 3:
        assert np.max(abs(within_batch - expected)) > 1e-5
    else:
        # Here a=0: the skew only swaps/scales the even registers. Both Bell
        # pairs are independent with the same law, so this shortcut coincides.
        np.testing.assert_allclose(within_batch, expected, atol=2e-14)


@pytest.mark.parametrize("p,a,b", [(3, 1, 2), (5, 2, 0), (5, 0, 2)])
def test_entire_difference_table_matches_operator_fourier_identity(p, a, b):
    rho = generic_mixed(p, 397)
    labels = np.array(list(product(range(p), repeat=2)))
    c = np.array([abs(np.trace(rho @ reference.weyl_operator(p, z, x))) ** 2
                  for z, x in labels]).reshape(p, p)
    weights = np.empty((p * p, p * p))
    for i, u in enumerate(labels):
        for j, v in enumerate(labels):
            weights[i, j] = (c[tuple(u)] * c[tuple(v)]
                             * c[tuple((a * u + b * v) % p)]
                             * c[tuple((b * u - a * v) % p)])
    symplectic = np.outer(labels[:, 0], labels[:, 1]) - np.outer(labels[:, 1], labels[:, 0])
    characters = np.exp(2j * np.pi * (symplectic % p) / p)
    expected = (characters @ weights @ characters.T / p**4).reshape((p,) * 4)
    result = reference.simulate_skew_bell_mixed(rho, p, a, b)
    np.testing.assert_allclose(result.eight_copy_joint, expected, atol=2e-13, rtol=0)


@pytest.mark.parametrize("p,a,b", [(3, 1, 1), (5, 2, 0), (5, 0, 2)])
@pytest.mark.parametrize("kind", ["computational", "quadratic"])
def test_pure_stabilizer_uniform_on_its_line(p, a, b, kind):
    if kind == "computational":
        rho = projector(np.eye(p)[1])
        line = [(z, 0) for z in range(p)]
    else:
        q = np.arange(p)
        rho = projector(np.exp(2j * np.pi * (q * q + q) / p))
        line = [(2 * x % p, x) for x in range(p)]
    expected = np.zeros((p, p))
    for label in line:
        expected[label] = 1 / p
    result = reference.simulate_skew_bell_mixed(rho, p, a, b)
    np.testing.assert_allclose(result.eight_copy_first_marginal, expected, atol=2e-13)
    np.testing.assert_allclose(result.eight_copy_joint, np.einsum("ij,kl->ijkl", expected, expected), atol=2e-13)
    np.testing.assert_allclose(reference.pure_convolution_marginal_control(rho, p, a, b), expected, atol=2e-13)


@pytest.mark.parametrize("p,a,b", [(3, 1, 1), (5, 0, 2)])
def test_maximally_mixed_is_normalized_uniform_not_pure_convolution(p, a, b):
    rho = np.eye(p) / p
    result = reference.simulate_skew_bell_mixed(rho, p, a, b)
    np.testing.assert_allclose(result.four_copy_joint, 1 / p**4, atol=2e-14)
    np.testing.assert_allclose(result.eight_copy_joint, 1 / p**4, atol=2e-14)
    np.testing.assert_allclose(result.eight_copy_first_marginal, 1 / p**2, atol=2e-14)
    wrong = reference.pure_convolution_marginal_control(rho, p, a, b)
    expected_wrong = np.zeros((p, p))
    expected_wrong[0, 0] = p**-4
    np.testing.assert_allclose(wrong, expected_wrong, atol=2e-14)
    assert np.max(abs(wrong / wrong.sum() - result.eight_copy_first_marginal)) > 0.8


@pytest.mark.parametrize("p,a,b", [(3, 1, 1), (5, 2, 0), (5, 0, 2)])
def test_pure_convolution_fails_generic_mixed_even_after_renormalizing(p, a, b):
    rho = generic_mixed(p, 931)
    actual = reference.simulate_skew_bell_mixed(rho, p, a, b).eight_copy_first_marginal
    wrong = reference.pure_convolution_marginal_control(rho, p, a, b)
    purity = np.trace(rho @ rho).real
    assert wrong.sum() == pytest.approx(purity**4, abs=2e-13)
    assert np.max(abs(wrong / wrong.sum() - actual)) > 1e-3


def rank_mod_prime(rows, prime):
    matrix = np.asarray(rows, dtype=int).copy() % prime
    rank = 0
    for column in range(matrix.shape[1]):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i, column]), None)
        if pivot is None:
            continue
        matrix[[rank, pivot]] = matrix[[pivot, rank]]
        matrix[rank] = matrix[rank] * pow(int(matrix[rank, column]), -1, prime) % prime
        for i in range(len(matrix)):
            if i != rank:
                matrix[i] = (matrix[i] - matrix[i, column] * matrix[rank]) % prime
        rank += 1
    return rank


def test_factorized_two_qutrit_noncommuting_full_symmetry():
    first_rho, second_rho = np.eye(3) / 3, np.diag([1 / 2, 1 / 3, 1 / 6])
    first = reference.simulate_skew_bell_mixed(first_rho, 3, 1, 1)
    second = reference.simulate_skew_bell_mixed(second_rho, 3, 1, 1)
    # The skew and Bell circuits factor across qudit coordinates. This remains
    # eight copies of a two-qudit state, not sixteen, without a 6561-square matrix.
    law = np.einsum("ij,kl->ijkl", first.eight_copy_first_marginal,
                    second.eight_copy_first_marginal)
    assert_law(law)
    rho = np.kron(first_rho, second_rho)  # Only 9 by 9 for membership checks.
    purity = np.trace(rho @ rho).real
    assert purity == pytest.approx(7 / 54)
    accepted = []
    outside_losses = []
    for z1, x1, z2, x2 in product(range(3), repeat=4):
        weyl = np.kron(reference.weyl_operator(3, z1, x1), reference.weyl_operator(3, z2, x2))
        loss = purity - np.trace(rho @ weyl @ rho @ weyl.conj().T).real
        if abs(loss) < 1e-12:
            accepted.append((z1, x1, z2, x2))
        else:
            outside_losses.append(loss)
    assert set(accepted) == {(z1, x1, z2, 0) for z1, x1, z2 in product(range(3), repeat=3)}
    assert len(accepted) == 27
    assert len(outside_losses) == 54
    np.testing.assert_allclose(outside_losses, 1 / 36, atol=2e-14)
    masses = np.array([law[label] for label in accepted])
    assert masses.min() > 0
    np.testing.assert_allclose(masses, masses[0], atol=2e-14)
    assert masses.sum() >= purity**3
    assert rank_mod_prime(accepted, 3) == 3  # Do not truncate to isotropic rank 2.
    x1, z1 = reference.weyl_operator(3, 0, 1), reference.weyl_operator(3, 1, 0)
    assert np.linalg.norm(x1 @ z1 - z1 @ x1) > 1


@pytest.mark.parametrize("p", [True, np.bool_(False), 3.0, "3", 0, 2, 7, 9])
def test_prime_and_dense_cap_rejected_before_allocation(p):
    with pytest.raises(ValueError):
        reference.simulate_skew_bell_mixed(np.eye(3) / 3, p, 1, 1)


@pytest.mark.parametrize("a,b", [(0, 0), (0, 1), (True, 1), (1.0, 1), (-1, 1), (3, 1)])
def test_invalid_skew_parameters(a, b):
    with pytest.raises(ValueError):
        reference.simulate_skew_bell_mixed(np.eye(3) / 3, 3, a, b)


@pytest.mark.parametrize("entry", [reference.four_copy_bell_law, reference.fourier_marginal,
                                   reference.pure_convolution_marginal_control])
@pytest.mark.parametrize("bad", ["shape", "trace", "negative", "nonhermitian", "nan", "inf"])
def test_density_validation(entry, bad):
    rho = np.eye(3, dtype=complex) / 3
    if bad == "shape":
        rho = np.eye(9) / 9
    elif bad == "trace":
        rho *= 2
    elif bad == "negative":
        rho[0, 0], rho[1, 1] = -0.1, 1.1 - rho[2, 2]
    elif bad == "nonhermitian":
        rho[0, 1] = 0.1j
    else:
        rho[0, 0] = float(bad)
    with pytest.raises(ValueError):
        entry(rho, 3, 1, 1)


@pytest.mark.parametrize("bad", [np.ones((3, 3)), np.ones((3, 3, 3, 5)),
                                 np.ones((3,) * 4), np.full((3,) * 4, np.nan),
                                 np.full((3,) * 4, 1 / 81 + 0.01j),
                                 np.full((3,) * 4, -1 / 81)])
def test_difference_rejects_nonprobability_tables(bad):
    with pytest.raises(ValueError):
        reference.independent_difference_law(bad)

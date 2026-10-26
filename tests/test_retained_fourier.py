"""Complete retained-frequency and ordinary-source composition controls.

Finite diagnostic instances, not hidden-oracle candidates or speedup evidence.
"""

from itertools import product

import numpy as np
import pytest

from theorems.class_three_monomial_jet import ClassThreeStructure


@pytest.mark.parametrize("p,width", [(5, 0), (5, 1), (5, 2), (7, 2)])
def test_all_linear_frequencies_form_complete_negative_fourier_basis(p, width):
    vectors = np.array(list(product(range(p), repeat=width)), dtype=int)
    phases = vectors @ vectors.T % p
    transform = np.exp(-2j*np.pi*phases/p)/np.sqrt(len(vectors))
    np.testing.assert_allclose(transform.conj().T @ transform, np.eye(len(vectors)), atol=2e-13)
    np.testing.assert_allclose(transform @ transform.conj().T, np.eye(len(vectors)), atol=2e-13)
    if width:
        without_zero = transform[1:, :]
        assert np.linalg.norm(without_zero.conj().T @ without_zero-np.eye(len(vectors))) > 0.9


def test_trivial_base_character_collapses_the_transform():
    p = 5
    collapsed = np.ones((p, p))/np.sqrt(p)
    assert np.linalg.matrix_rank(collapsed) == 1
    assert not np.allclose(collapsed.conj().T @ collapsed, np.eye(p))
    # This is a bad Fourier base character, NOT permission to discard
    # a zero central label. That valid case occurs in the source test.


@pytest.mark.parametrize("center_width", [1, 2])
def test_actual_cosets_through_central_and_retained_b_fourier(center_width):
    p = 5
    gamma = (((0, 1), (4, 0)),)+(((0, 0), (0, 0)),)*(center_width-1)
    delta = (((1,), (0,)),)+(((0,), (0,)),)*(center_width-1)
    structure = ClassThreeStructure(p, (((0, 1), (4, 0)),), gamma, delta)
    normal = list(product(range(p), repeat=3+center_width))
    carriers = list(product(range(p), repeat=3))
    carrier_index = {x: i for i, x in enumerate(carriers)}
    identity = (0,)*(3+center_width)

    def multiply(x, y):
        blocks = structure.multiply_fixture((x[:2], x[2:3], x[3:]),
                                            (y[:2], y[2:3], y[3:]))
        return blocks[0]+blocks[1]+blocks[2]

    def inverse(x):
        return tuple(-v % p for v in x)

    def powers(x):
        result = [identity]
        for _ in range(p-1):
            result.append(multiply(result[-1], x))
        assert multiply(result[-1], x) == identity
        return result

    hidden = powers((1, 1, 2)+(1,)*center_width)
    section = powers((0, 1, 1)+(0,)*center_width)
    assert all(multiply(hidden[u], hidden[v]) == hidden[(u+v) % p]
               for u, v in product(range(p), repeat=2))

    # Genuine G=F_p x N, H={(u,h^u)}. Only the explicit public section
    # enters the chart. The output label is assigned by actual right H action.
    labels = {}
    for q, n in product(range(p), normal):
        if (q, n) in labels:
            continue
        label = len(labels)//p
        for u in range(p):
            key = ((q+u) % p, multiply(n, hidden[u]))
            assert key not in labels
            labels[key] = label
    rows = [[labels[(q, multiply(n, section[q]))] for n in normal] for q in range(p)]
    assert all(len(set(row)) == len(normal) for row in rows)
    assert all(set(row) == set(rows[0]) for row in rows)

    potential = [multiply(hidden[q], inverse(section[q])) for q in range(p)]
    omega = np.exp(2j*np.pi/p)
    character_labels = [(0,)*center_width, (1,)*center_width]
    if center_width == 2:
        character_labels += [(0, 1), (1, 0)]
    observed_coherence = False
    observed_wrong_frequency = False
    for label in character_labels:
        # Direct physical amplitudes: normal inversion, positive C Fourier,
        # negative B Fourier. No group potential is used to construct K.
        kraus = np.zeros((len(carriers), len(normal)), dtype=complex)
        for j, n in enumerate(normal):
            inv = inverse(n)
            central_phase = sum(a*b for a, b in zip(label, inv[3:]))
            for mu in range(p):
                i = carrier_index[inv[:2]+(mu,)]
                kraus[i, j] = omega**((central_phase-mu*inv[2]) % p)/np.sqrt(p**(center_width+1))
        np.testing.assert_allclose(kraus @ kraus.conj().T, np.eye(len(carriers)), atol=2e-13)

        def action(g, wrong_frequency=False):
            result = np.zeros((len(carriers), len(carriers)), dtype=complex)
            for j, x in enumerate(carriers):
                out, phase = structure.fourier_action_fixture(label, (g[:2], g[2:3], g[3:]), x)
                if wrong_frequency:
                    # Mutation: use the old mu instead of mu+ell in -nu(d).
                    d = multiply(g, x[:2]+(0,)+(0,)*center_width)[2]
                    phase = (phase+(out[2]-x[2])*d) % p
                result[carrier_index[out], j] = omega**phase
            return result

        for q, r in [(0, 0), (0, 1), (1, 3)]:
            # Each row is a bijection of the actual oracle labels. Matching
            # them contracts the equality kernel without a dense |N|^2 table.
            lookup = {value: j for j, value in enumerate(rows[r])}
            matching = [lookup[value] for value in rows[q]]
            actual = kraus @ kraus[:, matching].conj().T/(p*len(normal))
            expected = action(potential[q]).conj().T @ action(potential[r])/(p*len(normal))
            np.testing.assert_allclose(actual, expected, atol=2e-13)
            if q == r:
                mass = p*np.trace(actual).real
                assert mass == pytest.approx(p**(-center_width))
                scalar_image_dimension = int(any(label))
                if scalar_image_dimension != center_width:
                    assert mass != pytest.approx(p**(-scalar_image_dimension))
            else:
                dephased = actual.copy()
                for i, x in enumerate(carriers):
                    for j, y in enumerate(carriers):
                        if x[2] != y[2]:
                            dephased[i, j] = 0
                observed_coherence |= np.linalg.norm(actual-dephased) > 1e-6
                wrong = action(potential[q], True).conj().T @ action(potential[r], True)/(p*len(normal))
                observed_wrong_frequency |= np.linalg.norm(actual-wrong) > 1e-6
    assert observed_coherence, "Measuring mu must change at least one genuine source block"
    assert observed_wrong_frequency, "The shifted-frequency phase is load-bearing"

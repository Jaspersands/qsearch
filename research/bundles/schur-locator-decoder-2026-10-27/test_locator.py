from itertools import combinations, product
from pathlib import Path
import random
import sys

import pytest

from locator import SchurLocator, native_bounds

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "small-prime-tower-2026-10-27"))
from small_prime import build_control


def reed_solomon(p, k, m):
    return [[pow(x, i, p) for x in range(m)] for i in range(k)]


def test_all_f5_degree_one_codewords_and_one_symbol_errors():
    decoder = SchurLocator(5, reed_solomon(5, 2, 5))
    for message in product(range(5), repeat=2):
        word = decoder.encode(message)
        assert decoder.decode(word, 1)["word"] == word
        for position in range(5):
            for value in range(1, 5):
                received = word.copy()
                received[position] = (received[position]+value) % 5
                result = decoder.decode(received, 1)
                assert result["word"] == word
                assert result["locator"][position] == 0
                assert result["message_in_original_basis"] == list(message)


@pytest.mark.parametrize("weight", [0, 1, 2])
def test_two_errors_without_geometry(weight):
    decoder = SchurLocator(11, reed_solomon(11, 3, 8))
    word = decoder.encode([4, 7, 2])
    for support in combinations(range(8), weight):
        for values in product((1, 10), repeat=weight):
            received = word.copy()
            for i, v in zip(support, values):
                received[i] = (received[i]+v) % 11
            assert decoder.decode(received, 2)["word"] == word


@pytest.mark.parametrize("mode", ["original", "permuted_scaled_row_changed"])
def test_actual_native_matrix_nine_errors(mode):
    _, _, native = build_control()
    matrix = [row[:] for row in native["original_parity"]]
    rng = random.Random(7919)
    if mode != "original":
        permutation = list(range(176))
        rng.shuffle(permutation)
        scales = [rng.randrange(1, 1019) for _ in range(176)]
        matrix = [[row[j]*scales[i] % 1019 for i, j in enumerate(permutation)] for row in matrix]
        matrix[0] = [(a+7*b) % 1019 for a, b in zip(matrix[0], matrix[1])]
    decoder = SchurLocator(1019, matrix)
    assert (decoder.k, decoder.m, len(decoder.W)) == (43, 176, 126)
    for weight in (0, 1, 8, 9):
        message = [rng.randrange(1019) for _ in range(43)]
        word = decoder.encode(message)
        received = word.copy()
        support = rng.sample(range(176), weight)
        for i in support:
            received[i] = (received[i]+rng.randrange(1, 1019)) % 1019
        result = decoder.decode(received, 9)
        assert result["word"] == word
        assert result["message_in_original_basis"] == message
        assert all(result["locator"][i] == 0 for i in support)


def test_full_square_is_not_a_distance_certificate():
    decoder = SchurLocator(5, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    result = decoder.decode([1, 2, 3], 0)
    assert result["status"] == "FAIL_NONUNIQUE_ERASURES"
    assert result["word"] is None


def test_outside_radius_never_silently_accepts():
    decoder = SchurLocator(5, reed_solomon(5, 2, 5))
    for r in product(range(5), repeat=5):
        result = decoder.decode(r, 0)
        if result["word"] is not None:
            assert result["word"] == list(r)


@pytest.mark.parametrize("e", [8, 128, 256, 512, 1024])
def test_native_analytic_decoder_radius_and_tail(e):
    bound = native_bounds(e)
    assert bound["classical_decode_radius"] == 2*e-7
    assert bound["classical_decode_radius"] < bound["W_distance_lower"]
    assert bound["classical_decode_radius"] < bound["k"]
    assert 2*bound["V_distance_lower"] > bound["m"]
    assert bound["ordinary_DQI_raw_verified_success_lower"] > 99/100
    assert not bound["higher_input_generated"]
    assert not bound["classical_full_support_solver_claimed"]


@pytest.mark.parametrize("p,matrix", [(6, [[1]]), (3, []), (3, [[3]]), (3, [[1], [1]])])
def test_invalid_generator(p, matrix):
    with pytest.raises(ValueError):
        SchurLocator(p, matrix)

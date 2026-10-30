from itertools import product

import numpy as np
import pytest

from walsh_attack import (
    block_basis, certified_score, dyadic_partition, exact_translation_control,
    load_resident_functions, shortest_scalar_move, walsh_rows,
)


def test_native_partition_is_exact_and_basis_is_invertible_over_composite_order():
    assert dyadic_partition(6000, 6420) == [(6000, 16), (6016, 128), (6144, 256), (6400, 16), (6416, 4)]
    basis, blocks = block_basis(8, 20, 15)
    inverse = basis.copy()
    for offset, size in blocks:
        i = offset-8
        inverse[i:i+size, i:i+size] = basis[i:i+size, i:i+size]*pow(size, -1, 15) % 15
    assert np.array_equal((basis @ inverse) % 15, np.eye(12, dtype=np.int64))


@pytest.mark.parametrize('start,stop', [(0, 17), (3, 19), (8, 16), (9, 10)])
def test_partition_has_no_gaps_and_aligned_binary_blocks(start, stop):
    blocks = dyadic_partition(start, stop)
    assert [v for offset, size in blocks for v in range(offset, offset+size)] == list(range(start, stop))
    assert all(size & (size-1) == 0 and offset % size == 0 for offset, size in blocks)


@pytest.mark.parametrize('order', [7, 15, 31])
def test_covariance_with_independent_direct_sums(order):
    kernel = np.array([(i*i+3*i+2) % order for i in range(32)], dtype=np.int64)
    phases, count = exact_translation_control(kernel, 8, 8, order)
    assert count == 32*8*3
    for row, mode in product(range(32), range(8)):
        expected = sum(int(kernel[row ^ (8+u)]) * (-1 if (u&mode).bit_count() % 2 else 1)
                       for u in range(8)) % order
        assert phases[row, mode] == expected
    disjoint = [i for i in range(32) if not 8 <= i < 16]
    for mode in range(8):
        column = phases[disjoint, mode]
        assert len(np.unique(np.minimum(column, (-column) % order))) <= 3


def test_walsh_transform_not_float_approximation():
    matrix = np.array([[0, 1, 2, 3], [65530, -3, 20, 7]], dtype=np.int64)
    transformed = walsh_rows(matrix, 65535)
    assert np.array_equal(walsh_rows(transformed, 65535), 4*matrix % 65535)


def test_short_scalar_diagnostic_matches_independent_python():
    phases = np.array([0, 3, 4, 11, 12, 3], dtype=np.int64)
    result = shortest_scalar_move(phases, 15)
    expected = min((max(min((int(v)*d) % 15, (-int(v)*d) % 15) for v in phases), d)
                   for d in range(1, 15))
    assert (result['min_max_centered_residue'], result['displacement']) == expected
    assert result['distinct_frequencies_up_to_sign'] == 3


def test_unchanged_line_solver_works_with_composite_walsh_basis():
    functions, hashes = load_resident_functions()
    assert len(hashes) == 2
    order = 15
    matrix = np.array([[1, 3], [2, 5], [7, 4]], dtype=np.int64)
    centers = np.array([1, 6, 8], dtype=np.int64)
    basis, _ = block_basis(0, 2, order)
    result = functions['fft_line_search'](matrix, centers, np.zeros(2, dtype=np.int64), order,
                                        basis_inv=basis, sweeps=1)
    current = np.zeros(2, dtype=np.int64)
    for j in range(2):
        scores = [float(np.cos(2*np.pi*((matrix @ ((current+d*basis[:,j]) % order)-centers) % order)/order).mean())
                  for d in range(order)]
        best = int(np.argmax(scores))
        if scores[best] > scores[0]+1e-12:
            current = (current+best*basis[:,j]) % order
    assert np.array_equal(current, result['assignment'])
    score = np.cos(2*np.pi*((matrix @ current-centers) % order)/order).mean()
    assert abs(score-result['final_mean_cosine']) < 1e-12


def test_interval_verifier_does_not_claim_nearby_thresholds():
    assert certified_score(np.array([0, 0]), 15)['score_at_least_0_3_certified']
    assert certified_score(np.array([5, 5]), 15)['score_below_0_3_certified']


@pytest.mark.parametrize('start,stop', [(0, 0), (-1, 3), (True, 2), (2, 1)])
def test_invalid_partition_fails(start, stop):
    with pytest.raises(ValueError):
        dyadic_partition(start, stop)


def test_invalid_transform_contracts():
    for matrix, modulus in [(np.zeros((2,3), dtype=np.int64),15),
                            (np.zeros((2,4), dtype=float),15),
                            (np.zeros((2,4), dtype=np.int64),16)]:
        with pytest.raises(ValueError):
            walsh_rows(matrix, modulus)
    with pytest.raises(ValueError):
        exact_translation_control(np.arange(16), 3, 4, 15)
    with pytest.raises(ValueError):
        block_basis(0, 4, 14)

"""Independent, fixed-S3 native-state/QFT controls; no producer imports or writes."""

from fractions import Fraction
from itertools import permutations, product
import math

import numpy as np
import pytest
from numpy.testing import assert_allclose


_G = tuple(permutations(range(3)))
_W = tuple(product(_G, _G, (0, 1)))
_DIMS = (1, 1, 2)
_N = 6
_M = 72
_ATOL = 2e-12


def _compose(a, b):
    return tuple(a[b[i]] for i in range(3))


def _inverse(a):
    return tuple(a.index(i) for i in range(3))


def _multiply(x, y):
    a, b, s = x
    c, d, t = y
    if s:
        c, d = d, c
    return _compose(a, c), _compose(b, d), s ^ t


def _act(w, point):
    a, b, s = w
    return _compose(_compose(b, _inverse(point) if s else point), _inverse(a))


def _block_diagonal(a, b):
    result = np.zeros((len(a) + len(b), len(a) + len(b)))
    result[:len(a), :len(a)] = a
    result[len(a):, len(a):] = b
    return result


@pytest.fixture(scope="module")
def model():
    # Enumerate stabilizers and actual left cosets, independently of the producer.
    assert len(_G) == _N and len(_W) == _M
    index = {w: i for i, w in enumerate(_W)}
    table = np.array([[index[_multiply(x, y)] for y in _W] for x in _W])
    subgroups, incidences, adjacencies, raw = [], [], [], []
    for tau in _G:
        subgroup = {index[w] for w in _W if _act(w, tau) == tau}
        unseen = set(range(_M))
        cosets = []
        while unseen:
            coset = set(table[min(unseen), sorted(subgroup)])
            assert coset <= unseen and len(coset) == 12
            unseen -= coset
            column = np.zeros(_M, dtype=np.int64)
            column[sorted(coset)] = 1
            cosets.append(column)
        incidence = np.column_stack(cosets)
        assert incidence.shape == (_M, _N)
        vectors = incidence / math.sqrt(12)
        subgroups.append(subgroup)
        incidences.append(incidence)
        adjacencies.append(incidence @ incidence.T)
        raw.append(vectors @ vectors.T / _N)

    helmert = np.array([[1 / math.sqrt(2), 1 / math.sqrt(6)],
                        [-1 / math.sqrt(2), 1 / math.sqrt(6)],
                        [0, -2 / math.sqrt(6)]])
    base = [dict() for _ in _DIMS]
    for g in _G:
        permutation = np.zeros((3, 3))
        permutation[list(g), np.arange(3)] = 1
        sign = (-1) ** sum(g[i] > g[j] for i in range(3) for j in range(i + 1, 3))
        base[0][g] = np.ones((1, 1))
        base[1][g] = np.array([[sign]], dtype=float)
        base[2][g] = helmert.T @ permutation @ helmert

    irreps = []
    for lam, d in enumerate(_DIMS):
        swap = np.zeros((d * d, d * d))
        for i, j in product(range(d), repeat=2):
            swap[j * d + i, i * d + j] = 1
        for sign in (1, -1):
            # Reversing a,b makes the fixed column vector row-major vec(U(tau)).
            matrices = np.array([
                np.kron(base[lam][b], base[lam][a])
                @ (sign * swap if s else np.eye(d * d))
                for a, b, s in _W
            ])
            irreps.append({"label": (lam, sign), "degree": d * d,
                           "lam": lam, "plus": sign == 1, "matrices": matrices})
    for lam in range(3):
        for mu in range(lam + 1, 3):
            d = _DIMS[lam] * _DIMS[mu]
            swap = np.block([[np.zeros((d, d)), np.eye(d)],
                             [np.eye(d), np.zeros((d, d))]])
            matrices = np.array([
                _block_diagonal(np.kron(base[lam][b], base[mu][a]),
                                np.kron(base[lam][a], base[mu][b]))
                @ (swap if s else np.eye(2 * d))
                for a, b, s in _W
            ])
            irreps.append({"label": (lam, mu, "mixed"), "degree": 2 * d,
                           "lam": None, "plus": False, "matrices": matrices})

    offset = compressed_offset = 0
    fourier_rows = []
    for irrep in irreps:
        d = irrep["degree"]
        irrep["sector"] = slice(offset, offset + d * d)
        offset += d * d
        fourier_rows.append(math.sqrt(d / _M) * irrep["matrices"].reshape(_M, d * d).T)
        if irrep["plus"]:
            irrep["compressed_sector"] = slice(compressed_offset, compressed_offset + d)
            compressed_offset += d
    assert offset == _M and compressed_offset == _N
    return {"index": index, "table": table, "subgroups": subgroups,
            "incidences": incidences, "adjacencies": adjacencies, "raw": raw,
            "base": base, "irreps": irreps, "qft": np.vstack(fourier_rows)}


def _compress(state, model):
    fourier = model["qft"] @ state @ model["qft"].T
    result = np.zeros((_N, _N))
    for irrep in model["irreps"]:
        if irrep["plus"]:
            d, sector = irrep["degree"], irrep["sector"]
            block = fourier[sector, sector].reshape(d, d, d, d)
            target = irrep["compressed_sector"]
            result[target, target] = np.einsum("ijil->jl", block)
    return result


def _lift(state, model, normalize_rows=True):
    result = np.zeros((_M, _M))
    for irrep in model["irreps"]:
        if irrep["plus"]:
            d, sector = irrep["degree"], irrep["sector"]
            source = irrep["compressed_sector"]
            row = np.eye(d) / (d if normalize_rows else 1)
            result[sector, sector] = np.kron(row, state[source, source])
    return model["qft"].T @ result @ model["qft"]


def _entropy(state):
    values = np.linalg.eigvalsh(state)
    assert values.min() >= -_ATOL
    assert_allclose(values.sum(), 1, atol=_ATOL, rtol=0)
    positive = values[values > _ATOL]
    return -float(np.sum(positive * np.log2(positive)))


@pytest.mark.parametrize("irrep_index", range(9))
def test_all_wreath_irreps_obey_every_group_product(model, irrep_index):
    irrep = model["irreps"][irrep_index]
    matrices = irrep["matrices"]
    assert_allclose(matrices[model["table"]],
                    matrices[:, None] @ matrices[None, :], atol=_ATOL, rtol=0)
    assert_allclose(matrices @ matrices.transpose(0, 2, 1),
                    np.broadcast_to(np.eye(irrep["degree"]), matrices.shape),
                    atol=_ATOL, rtol=0)


def test_full_qft_is_unitary_and_irrep_list_is_complete(model):
    assert len(model["irreps"]) == 9
    assert sum(irrep["degree"] ** 2 for irrep in model["irreps"]) == _M
    characters = np.array([np.trace(irrep["matrices"], axis1=1, axis2=2)
                           for irrep in model["irreps"]])
    assert_allclose(characters @ characters.T / _M, np.eye(9), atol=_ATOL, rtol=0)
    qft = model["qft"]
    assert qft.shape == (_M, _M)
    assert_allclose(qft @ qft.T, np.eye(_M), atol=_ATOL, rtol=0)
    assert_allclose(qft.T @ qft, np.eye(_M), atol=_ATOL, rtol=0)


@pytest.mark.parametrize("tau_index", range(_N), ids=[str(tau) for tau in _G])
def test_native_coset_state_fourier_blocks_and_both_channels(model, tau_index):
    tau, e = _G[tau_index], _G[0]
    subgroup = model["subgroups"][tau_index]
    explicit = {(p, _compose(_compose(tau, p), _inverse(tau)), 0) for p in _G}
    explicit |= {(_compose(p, _inverse(tau)), _compose(tau, p), 1) for p in _G}
    assert subgroup == {model["index"][h] for h in explicit}
    base = {(p, p, s) for p, s in product(_G, (0, 1))}
    conjugated = {_multiply(_multiply((e, tau, 0), h), (e, _inverse(tau), 0)) for h in base}
    assert explicit == conjugated and len(subgroup) == 12
    assert set(model["table"][np.ix_(sorted(subgroup), sorted(subgroup))].flat) <= subgroup

    incidence = model["incidences"][tau_index]
    assert np.array_equal(incidence.T @ incidence, 12 * np.eye(_N, dtype=np.int64))
    adjacency = model["adjacencies"][tau_index]
    regular_sum = np.zeros((_M, _M), dtype=np.int64)
    for h in subgroup:
        regular_sum[model["table"][:, h], np.arange(_M)] += 1
    assert np.array_equal(adjacency, regular_sum)
    assert np.array_equal(adjacency @ adjacency, 12 * adjacency)
    raw = model["raw"][tau_index]
    assert_allclose(raw, regular_sum / _M, atol=_ATOL, rtol=0)

    expected_fourier = np.zeros((_M, _M))
    expected_compressed = np.zeros((_N, _N))
    for irrep in model["irreps"]:
        fixed = irrep["matrices"][sorted(subgroup)].mean(axis=0)
        if irrep["plus"]:
            lam, d = irrep["lam"], irrep["degree"]
            vector = model["base"][lam][tau].reshape(-1) / math.sqrt(_DIMS[lam])
            projector = np.outer(vector, vector)
            assert_allclose(fixed, projector, atol=_ATOL, rtol=0)
            sector, target = irrep["sector"], irrep["compressed_sector"]
            expected_fourier[sector, sector] = np.kron(np.eye(d), projector) / _N
            expected_compressed[target, target] = (d / _N) * projector
        else:
            assert_allclose(fixed, 0, atol=_ATOL, rtol=0)
    assert_allclose(model["qft"] @ raw @ model["qft"].T,
                    expected_fourier, atol=_ATOL, rtol=0)
    compressed = _compress(raw, model)
    assert_allclose(compressed, expected_compressed, atol=_ATOL, rtol=0)
    assert_allclose(_lift(compressed, model), raw, atol=_ATOL, rtol=0)
    assert_allclose(_compress(_lift(compressed, model), model), compressed, atol=_ATOL, rtol=0)


def test_channels_have_kraus_certificates_on_the_occupied_sectors(model):
    forward, reverse = [], []
    for irrep in model["irreps"]:
        if not irrep["plus"]:
            continue
        d, sector, target = irrep["degree"], irrep["sector"], irrep["compressed_sector"]
        for row in range(d):
            selector = np.zeros((_N, _M))
            selector[target, sector.start + row * d:sector.start + (row + 1) * d] = np.eye(d)
            kraus = selector @ model["qft"]
            forward.append(kraus)
            reverse.append(kraus.T / math.sqrt(d))
    support = sum(k.T @ k for k in forward)
    assert_allclose(support @ support, support, atol=_ATOL, rtol=0)
    assert_allclose(np.trace(support), 18, atol=_ATOL, rtol=0)
    assert_allclose(sum(k.T @ k for k in reverse), np.eye(_N), atol=_ATOL, rtol=0)
    for raw in model["raw"]:
        assert_allclose(support @ raw @ support, raw, atol=_ATOL, rtol=0)
        compressed = _compress(raw, model)
        assert_allclose(sum(k @ raw @ k.T for k in forward), compressed, atol=_ATOL, rtol=0)
        assert_allclose(sum(k @ compressed @ k.T for k in reverse), raw, atol=_ATOL, rtol=0)


def test_all_36_pairwise_overlaps_and_squared_direct_sum_weights(model):
    compressed = [_compress(raw, model) for raw in model["raw"]]
    weights = [Fraction(d * d, _N) for d in _DIMS]
    for i, tau in enumerate(_G):
        for j, sigma in enumerate(_G):
            delta = _compose(_inverse(tau), sigma)
            centralizer = sum(_compose(g, delta) == _compose(delta, g) for g in _G)
            intersection = len(model["subgroups"][i] & model["subgroups"][j])
            assert intersection == 2 * centralizer
            exact_raw = Fraction(int(np.sum(model["adjacencies"][i]
                                            * model["adjacencies"][j].T)), _M * _M)
            assert exact_raw == Fraction(intersection, _M) == Fraction(centralizer, _N * _N)
            assert_allclose(np.trace(model["raw"][i] @ model["raw"][j]),
                            float(exact_raw), atol=_ATOL, rtol=0)
            conditional = [np.trace(base[delta]) ** 2 / (d * d)
                           for base, d in zip(model["base"], _DIMS)]
            squared = sum(float(p * p) * overlap for p, overlap in zip(weights, conditional))
            assert_allclose(np.trace(compressed[i] @ compressed[j]), squared, atol=_ATOL, rtol=0)
    assert sum(p * p for p in weights) == Fraction(1, 2)
    # The old unsquared-weight expression would instead give identity overlap 1.
    assert_allclose(np.trace(compressed[0] @ compressed[0]), 1 / 2, atol=_ATOL, rtol=0)
    assert not np.isclose(np.trace(compressed[0] @ compressed[0]), float(sum(weights)))


def test_actual_spectra_purities_average_states_and_holevo(model):
    raw = model["raw"]
    compressed = [_compress(state, model) for state in raw]
    for r, s in zip(raw, compressed):
        assert_allclose(np.linalg.eigvalsh(r), [0] * 66 + [1 / 6] * 6, atol=_ATOL, rtol=0)
        assert_allclose(np.linalg.eigvalsh(s), [0] * 3 + [1 / 6] * 2 + [2 / 3], atol=_ATOL, rtol=0)
        assert_allclose(np.trace(r @ r), 1 / 6, atol=_ATOL, rtol=0)
        assert_allclose(np.trace(s @ s), 1 / 2, atol=_ATOL, rtol=0)
    mean_raw, mean_compressed = sum(raw) / _N, sum(compressed) / _N
    assert_allclose(np.linalg.eigvalsh(mean_raw),
                    [0] * 54 + [1 / 24] * 16 + [1 / 6] * 2, atol=_ATOL, rtol=0)
    assert_allclose(mean_compressed, np.eye(_N) / _N, atol=_ATOL, rtol=0)
    assert_allclose(np.trace(mean_raw @ mean_raw), 1 / 12, atol=_ATOL, rtol=0)
    assert_allclose(np.trace(mean_compressed @ mean_compressed), 1 / 6, atol=_ATOL, rtol=0)
    assert_allclose(_entropy(mean_raw), math.log2(_N) + 4 / 3, atol=_ATOL, rtol=0)
    assert_allclose(_entropy(mean_compressed), math.log2(_N), atol=_ATOL, rtol=0)
    assert_allclose(_entropy(mean_raw) - sum(map(_entropy, raw)) / _N, 4 / 3, atol=_ATOL, rtol=0)
    assert_allclose(_entropy(mean_compressed) - sum(map(_entropy, compressed)) / _N,
                    4 / 3, atol=_ATOL, rtol=0)


def test_trace_distance_is_preserved_and_does_not_collapse(model):
    raw = model["raw"]
    compressed = [_compress(state, model) for state in raw]
    for ensemble in (raw, compressed):
        mean = sum(ensemble) / _N
        for state in ensemble:
            distance = np.abs(np.linalg.eigvalsh(state - mean)).sum() / 2
            assert_allclose(distance, 1 / 2, atol=_ATOL, rtol=0)


def test_optimal_povm_and_dual_certificates_for_both_ensembles(model):
    raw = model["raw"]
    compressed = [_compress(state, model) for state in raw]
    effects = compressed
    assert_allclose(sum(effects), np.eye(_N), atol=_ATOL, rtol=0)
    dual = np.zeros((_N, _N))
    for irrep in model["irreps"]:
        if irrep["plus"]:
            target, d = irrep["compressed_sector"], irrep["degree"]
            weight = np.trace(compressed[0][target, target])
            dual[target, target] = (weight / _N) * np.eye(d)
    raw_effects = [_lift(effect, model, normalize_rows=False) for effect in effects]
    # Complete the POVM outside all occupied sectors without changing its statistics.
    remainder = np.eye(_M) - sum(raw_effects)
    raw_effects = [effect + remainder / _N for effect in raw_effects]
    assert_allclose(sum(raw_effects), np.eye(_M), atol=_ATOL, rtol=0)
    for ensemble, povm, certificate in ((compressed, effects, dual),
                                        (raw, raw_effects, _lift(dual, model))):
        for state, effect in zip(ensemble, povm):
            assert np.linalg.eigvalsh(effect).min() >= -_ATOL
            assert np.linalg.eigvalsh(certificate - state / _N).min() >= -_ATOL
        success = sum(np.trace(state @ effect) for state, effect in zip(ensemble, povm)) / _N
        assert_allclose(success, 1 / 2, atol=_ATOL, rtol=0)
        assert_allclose(success, np.trace(certificate), atol=_ATOL, rtol=0)

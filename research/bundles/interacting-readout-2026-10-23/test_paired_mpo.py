from fractions import Fraction as Q
import itertools
import math

import numpy as np
import pytest

from controls import direct_tfd_expectation, exact_ising_mpo, sector_filter, word_matrix

from paired_mpo import (
    MPO, PAULI, dense_to_mpo, error_budget, log_norm_squared,
    overlap, paired_value, sector_value,
)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_general_complex_mpo_contraction(n):
    rng = np.random.default_rng(100+n)
    x = rng.normal(size=(2**n, 2**n)) + 1j*rng.normal(size=(2**n, 2**n))
    y = rng.normal(size=x.shape) + 1j*rng.normal(size=x.shape)
    a, b = "Y" + "X"*(n-1), "Y" + "Z"*(n-1)
    phase, mag = overlap(dense_to_mpo(x, n), dense_to_mpo(y, n), a, b)
    expected = np.trace(x.conj().T @ word_matrix(a) @ y @ word_matrix(b).T)
    assert phase * np.exp(mag) == pytest.approx(expected, abs=1e-10)


def test_y_transpose_is_essential():
    ident = dense_to_mpo(np.eye(2), 1)
    assert paired_value(ident, ident, "Y", "Y") == pytest.approx(-1)
    wrong = np.trace(PAULI["Y"] @ PAULI["Y"]) / 2
    assert wrong == 1


@pytest.mark.parametrize("cl,cr,a,b", [
    ("II", "II", "XZI", "YXI"),
    ("XI", "XI", "III", "III"),
    ("YI", "XI", "YII", "III"),
    ("XY", "YX", "YZI", "IZY"),
    ("ZI", "IZ", "ZZI", "IXI"),
    ("XI", "II", "III", "III"),
])
def test_interacting_thermal_paired_expectation(cl, cr, a, b):
    filters = [sector_filter(z) for z in range(4)]
    mpos = [dense_to_mpo(f, 3) for f in filters]
    weights = np.array([np.vdot(f, f).real for f in filters])
    values = [sector_value(z, mpos.__getitem__, cl, cr, a, b) for z in range(4)]
    actual = float(weights @ values / weights.sum())
    assert actual == pytest.approx(direct_tfd_expectation(filters, cl, cr, a, b), abs=2e-12)
    assert max(abs(v) for v in values) <= 1 + 1e-12


def test_scalar_offsets_cannot_be_dropped_by_sector_normalization():
    f = [sector_filter(z) for z in range(4)]
    target = direct_tfd_expectation(f, "XI", "XI", "III", "III")
    normalized = [x/np.linalg.norm(x) for x in f]
    wrong = direct_tfd_expectation(normalized, "XI", "XI", "III", "III")
    assert abs(target - wrong) > 0.02


def test_product_backend_is_not_the_interacting_answer():
    full = [sector_filter(z) for z in range(4)]
    product = [sector_filter(z, False) for z in range(4)]
    a = direct_tfd_expectation(full, "II", "II", "ZZI", "III")
    b = direct_tfd_expectation(product, "II", "II", "ZZI", "III")
    assert abs(a - b) > 0.15


@pytest.mark.parametrize("eta", [1e-5, 0.01, 0.3])
def test_relative_frobenius_error_is_uniform_over_weight_imbalance(eta):
    rng = np.random.default_rng(612)
    for scale in (1e-50, 1.0, 1e50):
        x, y = sector_filter(0), scale * sector_filter(1)
        ex = rng.normal(size=x.shape) + 1j*rng.normal(size=x.shape)
        ey = rng.normal(size=y.shape) + 1j*rng.normal(size=y.shape)
        ex *= eta * np.linalg.norm(x) / np.linalg.norm(ex)
        ey *= eta * np.linalg.norm(y) / np.linalg.norm(ey)
        ref = paired_value(dense_to_mpo(x, 3), dense_to_mpo(y, 3), "YXI", "IZY")
        val = paired_value(dense_to_mpo(x+ex, 3), dense_to_mpo(y+ey, 3), "YXI", "IZY")
        assert abs(val-ref) <= 4*eta + 2*eta**2 + 1e-12


def test_log_scaling_does_not_allocate_huge_normalization():
    base = dense_to_mpo(np.eye(2), 1)
    a, b = MPO(base.tensors, 10000), MPO(base.tensors, 10001)
    assert math.isfinite(log_norm_squared(a))
    assert paired_value(a, b, "I", "I") == pytest.approx(1 / math.cosh(1), abs=2e-12)


def test_only_two_central_sectors_are_requested():
    called = []
    base = dense_to_mpo(np.eye(2), 1)
    def get(z):
        called.append(z)
        return base
    r = 100
    assert sector_value(17, get, "X"+"I"*(r-1), "X"+"I"*(r-1), "I", "I") == 1
    assert called == [17, 16]


def test_all_central_pauli_pairs_with_complex_nonhermitian_filters():
    rng = np.random.default_rng(17)
    f = [rng.normal(size=(4, 4)) + 1j*rng.normal(size=(4, 4)) for _ in range(4)]
    mpos = [dense_to_mpo(x, 2) for x in f]
    w = np.array([np.vdot(x, x).real for x in f])
    words = ["".join(s) for s in itertools.product("IXYZ", repeat=2)]
    for cl, cr in itertools.product(words, repeat=2):
        values = [sector_value(z, mpos.__getitem__, cl, cr, "YX", "ZY") for z in range(4)]
        actual = w @ values / w.sum()
        assert actual == pytest.approx(
            direct_tfd_expectation(f, cl, cr, "YX", "ZY"), abs=2e-12)


def test_interacting_long_chain_without_dense_allocation():
    n, coupling = 192, 0.3
    mpo = exact_ising_mpo(n, coupling)
    assert max(t.shape[3] for t in mpo.tensors) == 2
    expected_log_norm = math.log(2) + (n-1)*math.log(2*math.cosh(2*coupling))
    assert log_norm_squared(mpo) == pytest.approx(expected_log_norm, abs=1e-10)
    assert paired_value(mpo, mpo, "ZZ" + "I"*(n-2), "I"*n) == pytest.approx(
        math.tanh(2*coupling), abs=1e-11)


def test_unmatched_masks_do_not_request_sectors():
    def forbidden(_):
        raise AssertionError("No sector access needed")
    assert sector_value(0, forbidden, "X", "I", "I", "I") == 0


def test_zero_overlap_and_zero_norm_are_distinguished():
    ident = dense_to_mpo(np.eye(2), 1)
    assert overlap(ident, ident, "X", "I") == (0j, -math.inf)
    assert paired_value(ident, ident, "X", "I") == 0
    with pytest.raises(ArithmeticError):
        paired_value(ident, dense_to_mpo(np.zeros((2, 2)), 1), "I", "I")


def test_error_ledger_and_invalid_promises():
    b = error_budget(Q(1, 100), Q(1, 200), Q(1, 1000))
    assert b["total_bias"] == Q(256, 5000)
    with pytest.raises(ValueError):
        error_budget(1, 0)
    with pytest.raises(ValueError):
        error_budget(0, -1)
    with pytest.raises(ValueError):
        dense_to_mpo(np.eye(2), 10)
    with pytest.raises(ValueError):
        MPO((np.zeros((1, 2, 2, 2)),))


def test_receipt_does_not_promote_diagnostics_to_a_solver():
    from replay import evidence
    row = evidence()
    for key in ("speedup_admitted", "novelty_admitted", "general_tfd_simulation_admitted",
                "scalable_thermal_constructor_implemented", "end_to_end_sampler_executed",
                "arithmetic_interval_certified"):
        assert row[key] is False
    assert row["illustrative_error_contract_only"]["total_bias"] == "32/625"
    assert not row["bounded_dense_control"]["distance_window_claimed"]

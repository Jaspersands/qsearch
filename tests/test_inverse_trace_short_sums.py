from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path

from flint import fq_default_poly_ctx
import pytest

from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_short_sums import _q_half_power_upper, short_sum_certificate


@pytest.mark.parametrize("q", [4, 8, 16, 32])
def test_half_power_upper_bound_handles_negative_and_positive_exponents(q):
    for exponent in range(-7, 8):
        bound = _q_half_power_upper(q, exponent)
        exact_square = Fraction(q**exponent) if exponent >= 0 else Fraction(1, q**(-exponent))
        assert bound*bound >= exact_square
        if exponent % 2 == 0 or q in (4, 16):
            assert bound*bound == exact_square


@pytest.mark.parametrize("bits", [61, 63])
def test_balanced_native_endpoints_have_exact_iid_certificates(bits):
    N, K = bits*bits, bits*bits//8
    for M in ((N-bits)//2, (N+bits)//2):
        certificate = short_sum_certificate(bits, M, K, M)
        assert certificate["status"] == "CERTIFIED_IID_SHORT_SUM_TRIAL_BOUND"
        assert certificate["first_moment_error_power2_upper"] <= -N
        assert certificate["first_moment_greater_than_half"]
        assert certificate["second_moment_less_than_twice_binomial"]
        assert certificate["expected_iid_trials_upper"] <= 8*comb(2*(M-K-1)+4, 3)
        assert certificate["uniform_factor_allocation_required"]
        assert certificate["published_theorem_import_not_formally_verified"]
        assert not certificate["uniform_native_sampler"]


def test_small_parameter_failure_is_not_promoted_or_clipped():
    certificate = short_sum_certificate(17, 139, 36, 130)
    assert certificate["status"] == "BOUND_INCONCLUSIVE"
    assert certificate["first_moment_error_power2_upper"] > 0
    assert certificate["iid_trial_success_lower_bound"] is None
    assert short_sum_certificate(5, 6, 3, 2)["status"] == "OUTSIDE_CERTIFICATE_SCOPE"


@pytest.mark.parametrize("M,c,d0", [(3, 1, 0), (4, 2, 1), (4, 3, 2)])
def test_full_normalized_first_moment_matches_coefficient_enumeration(M, c, d0):
    bits, q, K = 2, 4, 1
    values = [element(bits, i) for i in range(q)]
    ring = fq_default_poly_ctx(field(bits))
    X, P = ring.gen(), ring.one()
    points = values[:M]
    for a in points:
        P *= X+a
    D = P.derivative()
    Cs = [element(bits, c)*a+element(bits, d0) for a in points]
    targets = [int(C.trace()) for C in Cs]
    sign = lambda a: 1-2*int(a.trace())
    kappa = (element(bits, c)**(-1))**(q//2)
    r, s = M-K-1, M-2*K-1
    good = 0
    for uc in product(values, repeat=r+1):
        U = ring(list(uc))
        for ac in product(values, repeat=r):
            A = ring(list(ac)+[kappa])
            local = [(A(a)/D(a), U(a)/D(a), C, b)
                     for a, C, b in zip(points, Cs, targets)]
            good += all(v*v+a*v+C*a*a == 1 and not (b and a == 0)
                        for a, v, C, b in local)
    kl = {encoded(t): sum(sign(z+t/z) for z in values[1:]) for t in values}
    total = 0
    for pc in product(values, repeat=K+1):
        p = ring(list(pc))
        for gc in product(values, repeat=K):
            g = ring(list(gc))
            term = sign(kappa*pc[K])
            for a, C, b in zip(points, Cs, targets):
                xi, zeta = p(a), g(a)
                term *= (q*int(xi == 0 and zeta == 0)
                         +sign(C)*kl[encoded(xi*xi+xi*zeta+C*zeta*zeta)]-b*sign(zeta))
            total += term
    assert Fraction(total, q**M) == Fraction(good, q**s)


def test_exceptional_expansion_exponents_fit_without_short_sum_import():
    for K in range(1, 10):
        for M in range(2*K+1, 4*K+5):
            for t in range(K+1):
                k = K-t
                for ell in range(M-t+1):
                    if k == 0 or ell < k:
                        assert 2*t+4*k+2+ell-2*M <= 3*K+3-M
                    else:
                        assert 3*K-t+ell+3-2*M <= 3*K+3-M


def test_bound_artifact_replays_without_claiming_large_field_execution():
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root/"research/classical_baselines/inverse_trace_general_search_bounds.json").read_text())
    for path, digest in record["sources"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == digest
    for row in record["rows"]:
        assert row == short_sum_certificate(row["bits"], row["length"], row["checks"], row["zeros"])
    assert not record["field_factorization_executed"]
    assert not record["native_word_search_executed"]
    assert not record["new_quantum_speedup"]

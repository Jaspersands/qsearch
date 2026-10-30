from itertools import product
import hashlib
import json
from math import comb
from pathlib import Path
from random import Random

from flint import fq_default_poly_ctx
import pytest

from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_genus_zero import (
    run_experiment, split_norm, success_certificate, trace_bit_instance, word_from_norm,
)
from theorems.inverse_trace_smt import verify_word


def test_sparse_native_target_is_public_and_outside_dense_support_guard():
    instance, c, d0 = trace_bit_instance()
    assert (instance["bits"], len(instance["points"]), instance["checks"]) == (17, 289, 36)
    assert sum(instance["targets"]) == 33 < instance["checks"]
    assert c and d0 == 0
    assert all(int((element(17, c)*element(17, a)).trace()) == b
               for a, b in zip(instance["points"], instance["targets"]))


@pytest.mark.parametrize("bits", [15, 17, 19, 23])
def test_exact_success_certificate_native_sequence(bits):
    N, K = bits*bits, bits*bits//8
    bound = success_certificate(bits, N, K, N)
    assert bound["status"] == "CERTIFIED_IID_GENUS_ZERO_TRIAL_BOUND"
    assert bound["uniform_factor_allocation_required"]
    assert bound["published_theorem_import_not_formally_verified"]
    assert bound["first_moment_error_power2_upper"] < -100
    if bits == 17:
        assert bound["iid_trial_success_lower_bound"] == [1, 21864708]
        assert bound["divisor_error_power2_upper"] <= -551


def test_inconclusive_and_outside_scope_are_not_certificates():
    assert success_certificate(3, 4, 1, 2)["status"] == "BOUND_INCONCLUSIVE"
    assert success_certificate(5, 5, 3, 1)["status"] == "OUTSIDE_CERTIFICATE_SCOPE"


def test_conic_fourier_formula_and_deleted_one_site_exactly():
    bits, q = 3, 8
    F = field(bits)
    values = [element(bits, x) for x in range(q)]
    sign = lambda x: 1-2*int(x.trace())
    kl = {encoded(t): sum(sign(x+t/x) for x in values[1:]) for t in values}
    for C in values:
        conic = [(u, a) for u, a in product(values, repeat=2) if u*u+u*a+C*a*a == 1]
        eps = sign(C)
        assert len(conic) == q-eps
        good = [(u, a) for u, a in conic if not (eps == -1 and a == F.zero())]
        assert len(good) == (q-1 if eps == 1 else q)
        for v, w in product(values, repeat=2):
            # The character is v*A+w*U; this order matters in the dual form.
            observed = sum(sign(v*a+w*u) for u, a in conic)
            expected = q*int(v == 0 and w == 0)+eps*kl[encoded(v*v+v*w+C*w*w)]
            assert observed == expected
            if v != 0 or w != 0:
                transformed = sum(sign(v*a+w*u) for u, a in good)
                assert transformed*transformed <= (2*q**0.5+1)**2


def test_all_repeated_split_allocations_and_nonmonic_scalar():
    bits, c, d0 = 5, 11, 7
    ring = fq_default_poly_ctx(field(bits))
    slope, offset, X = element(bits, c), element(bits, d0), ring.gen()
    a = next(element(bits, k) for k in range(32) if (slope*element(bits, k)+offset).trace() == 0)
    polynomial = element(bits, 19)*(X+a)**3
    seen = set()

    class Allocation:
        def __init__(self, j):
            self.j = j

        def randrange(self, stop):
            assert stop == 4
            return self.j

    for j in range(4):
        U, A, record = split_norm(bits, polynomial, c, d0, Allocation(j))
        assert record["allocation_count"] == 4 and record["norm_identity_verified"]
        assert U*U+U*A+(X*slope+offset)*A*A == polynomial
        seen.add((tuple(map(encoded, U.coeffs())), tuple(map(encoded, A.coeffs()))))
    assert len(seen) == 4


def test_inert_odd_exponents_reject_but_even_exponents_split():
    bits, ring = 3, fq_default_poly_ctx(field(3))
    a = next(element(bits, k) for k in range(8) if element(bits, k).trace() == 1)
    F = ring.gen()+a
    U, A, record = split_norm(bits, F, 1, 0, Random(3))
    assert U is A is None and not record["is_norm"]
    U, A, record = split_norm(bits, F*F, 1, 0, Random(3))
    assert record["is_norm"] and record["allocation_count"] == 1
    assert U*U+U*A+ring.gen()*A*A == F*F


def test_word_certificate_rejects_zero_at_one_and_bad_degree_or_norm():
    bits, ring = 3, fq_default_poly_ctx(field(3))
    points = list(range(4))
    targets = [int(element(bits, a).trace()) for a in points]
    assert any(targets)
    instance = {"bits": bits, "points": points, "targets": targets, "checks": 1,
                "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}
    P = ring.one()
    for a in points:
        P *= ring.gen()+element(bits, a)
    assert P.derivative().degree() == 0
    assert word_from_norm(instance, 1, 0, P.derivative(), ring.zero()) is None
    with pytest.raises(ValueError, match="degree"):
        word_from_norm(instance, 1, 0, ring.gen()**4, ring.one())
    with pytest.raises(ValueError, match="residues"):
        word_from_norm(instance, 1, 0, P.derivative()+1, ring.zero())


def test_frozen_small_native_witness_and_full_certificate_replay():
    instance, c, d0 = trace_bit_instance(5, 4)
    result = run_experiment(instance, c, d0, max_trials=16)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["instance"] == instance and verify_word(instance, result["witness"])
    cert = result["certificate"]
    ring = fq_default_poly_ctx(field(5))
    polys = {k: ring([element(5, a) for a in cert[k]]) for k in ("P", "D", "T", "F", "U", "A")}
    expected_P = ring.one()
    for a in instance["points"]:
        expected_P *= ring.gen()+element(5, a)
    assert polys["P"] == expected_P
    assert polys["D"] == polys["P"].derivative()
    assert polys["F"] == polys["D"]**2 % polys["P"]+polys["P"]*polys["T"]
    norm = polys["U"]**2+polys["U"]*polys["A"]+(ring.gen()*element(5, c)+element(5, d0))*polys["A"]**2
    assert norm == polys["F"]
    # Congruence alone accepts a jointly tampered T,F with the same residues.
    assert (norm-(polys["F"]+polys["P"])) % polys["P"] == 0
    assert norm != polys["F"]+polys["P"]
    assert word_from_norm(instance, c, d0, polys["U"], polys["A"]) == result["witness"]
    for flag in ("hardness_evidence", "uniform_sampler", "unrestricted_target_solver_established",
                 "whole_workflow_wall_clock_cap_enforced", "factorization_subroutine_randomness_capped"):
        assert result[flag] is False


def test_zero_trials_and_wrong_trace_model_do_not_promote():
    instance, c, d0 = trace_bit_instance(5, 4)
    result = run_experiment(instance, c, d0, max_trials=0)
    assert result["status"] == "UNKNOWN_TRIAL_LIMIT" and result["witness"] is None
    changed = dict(instance, targets=[1-instance["targets"][0]]+instance["targets"][1:])
    with pytest.raises(ValueError, match="trace-affine"):
        run_experiment(changed, c, d0)
    with pytest.raises(ValueError, match="nonzero trace slope"):
        run_experiment(instance, 0, d0)


def test_factor_count_equals_exhaustive_normalized_lifts():
    ring, bits = fq_default_poly_ctx(field(3)), 3
    X, values = ring.gen(), [element(bits, i) for i in range(8)]
    P = X*(X+1)*(X+element(bits, 2))
    F = P.derivative()**2 % P+P
    for offset in range(8):
        count = 0
        for u0, u1, a0 in product(values, repeat=3):
            U, A = u0+X*u1, a0+X
            count += int(U*U+U*A+(X+element(bits, offset))*A*A == F)
        _, _, record = split_norm(bits, F, 1, offset, Random(3))
        assert record["allocation_count"] == count
    for multiplicity in range(50):
        assert (multiplicity+1)**2 <= comb(multiplicity+3, 3)


def test_small_mds_dual_support_and_singleton_trace_obstruction():
    bits, values = 3, [element(3, i) for i in range(8)]
    points = values[:4]
    for dimension, expected in [(2, 3), (3, 4)]:
        minimum = 5
        for word in product(values, repeat=4):
            if all(v == 0 for v in word):
                continue
            if all(sum((v*a**j for v, a in zip(word, points)), field(bits).zero()) == 0
                   for j in range(dimension)):
                minimum = min(minimum, sum(v != 0 for v in word))
        assert minimum == expected
    # A basis subspace has zero sums of every monomial below size-1.
    for j in range(3):
        assert sum((a**j for a in points), field(bits).zero()) == 0
    for coeffs in product(values, repeat=3):
        traces = [int(sum((c*a**j for j, c in enumerate(coeffs)), field(bits).zero()).trace())
                  for a in points]
        assert sum(traces) % 2 == 0


def test_unweighted_reciprocal_shortcut_has_missing_power_sum():
    bits, points, pole = 3, [0, 1, 2], element(3, 4)
    S0 = sum(((element(bits, a)+pole)**-1 for a in points), field(bits).zero())
    S1 = sum((element(bits, a)/(element(bits, a)+pole) for a in points), field(bits).zero())
    assert S1 == 1+pole*S0
    assert S1 != pole*S0


def test_native_artifact_with_independent_binary_field_arithmetic():
    path = Path(__file__).resolve().parents[1]/"research/classical_baselines/inverse_trace_genus_zero_n17.json"
    record = json.loads(path.read_text())
    instance, word = record["instance"], record["witness"]
    assert instance["points"] == list(range(289))
    assert instance["targets"] == [0]*256+[1]*33
    assert record["status"] == "VERIFIED_NATIVE_WITNESS"
    assert record["instance_sha256"] == hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest()
    rng = Random(record["seed"])
    for index, trial in enumerate(record["trials"]):
        raw_T = [rng.getrandbits(17) for _ in range(216)]+[1]
        assert trial["trial"] == index
        assert trial["T_sha256"] == hashlib.sha256(json.dumps(raw_T).encode()).hexdigest()
    assert raw_T == record["certificate"]["T"]
    bits = instance["bits"]
    modulus = sum(c << j for j, c in enumerate(instance["field_modulus_coefficients"]))
    assert bits == 17 and modulus == (1 << 17)+(1 << 3)+1
    ring = fq_default_poly_ctx(field(bits))
    polys = {k: ring([element(bits, a) for a in record["certificate"][k]])
             for k in ("P", "D", "T", "F", "U", "A")}
    P = ring.one()
    for a in instance["points"]:
        P *= ring.gen()+element(bits, a)
    assert polys["P"] == P and polys["D"] == P.derivative()
    assert polys["F"] == polys["D"]**2 % P+P*polys["T"]
    C = ring.gen()*element(bits, record["c"])+element(bits, record["d0"])
    assert polys["U"]**2+polys["U"]*polys["A"]+C*polys["A"]**2 == polys["F"]
    assert word_from_norm(instance, record["c"], record["d0"], polys["U"], polys["A"]) == word

    def mul(a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a >> bits:
                a ^= modulus
        return out

    def power(a, exponent):
        out = 1
        while exponent:
            if exponent & 1:
                out = mul(out, a)
            a = mul(a, a)
            exponent >>= 1
        return out

    syndromes = [0]*instance["checks"]
    assert len(word) == len(instance["points"])
    for a, x, target in zip(instance["points"], word, instance["targets"], strict=True):
        assert type(x) is int and 0 <= x < 1 << bits
        term = 1
        for j in range(len(syndromes)):
            syndromes[j] ^= mul(term, x)
            term = mul(term, a)
        reciprocal, trace = power(x, (1 << bits)-2) if x else 0, 0
        for _ in range(bits):
            trace ^= reciprocal
            reciprocal = mul(reciprocal, reciprocal)
        assert trace == target
    assert not any(syndromes)

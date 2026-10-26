from fractions import Fraction as Q
import hashlib
import json
from math import gcd
from pathlib import Path

import pytest

from theorems import integer_character_interpolation as integer


@pytest.mark.parametrize("exponent", [2, 3, 4, 5])
def test_lifting_exhausts_small_unit_group(exponent):
    modulus, order, _ = integer.lifting_data(exponent)
    for label in range(order):
        value = pow(2, label, modulus)
        recovered, cost = integer.lifted_log(value, exponent)
        assert recovered == label
        assert cost["ternary_digits_processed"] == exponent-1


@pytest.mark.parametrize("primes", [(2, 3, 5), (2, 4, 5), (2, 2, 5), (), (1, 5)])
def test_prime_independence_and_units_are_required(primes):
    with pytest.raises(ValueError, match="distinct primes"):
        integer.construct(primes, 1)


def test_lifting_rejects_nonunits():
    with pytest.raises(ValueError, match="unit"):
        integer.lifted_log(3, 5)


def test_public_labels_are_verified():
    public = integer.construct((2, 5, 7), 1)
    integer.validate_public_labels(public["primes"], public["labels"], public["exponent"])
    assert public["labels"][0] == 1
    bad = public["labels"].copy()
    bad[1] = (bad[1]+1) % public["order"]
    with pytest.raises(ValueError, match="logarithm"):
        integer.validate_public_labels(public["primes"], bad, public["exponent"])
    assert not public["preprocessing"]["full_group_table_used"]
    assert not public["preprocessing"]["quantum_discrete_log_preprocessing_used"]


def test_integer_rational_reconstruction_signed_and_composite_modulus():
    modulus = 3**6
    for numerator in range(-10, 11):
        for denominator in range(1, 11):
            if gcd(numerator, denominator) == gcd(denominator, modulus) == 1:
                residue = numerator*pow(denominator, -1, modulus) % modulus
                assert integer.rational_reconstruct(residue, modulus) == Q(numerator, denominator)


@pytest.mark.parametrize("length", [3, 4])
def test_all_small_source_words_and_observables(length):
    result = integer.small_control(length)
    assert result["target_norm"] == pytest.approx(1, abs=3e-13)
    mean = result["target_mean_cosine"]
    assert float(Q(result["source_mean"]["mean_cosine_lower"]))-3e-13 <= mean
    assert mean <= float(Q(result["source_mean"]["mean_cosine_upper"]))+3e-13
    assert result["observable_images_checked"] == result["patterns_decoded"]*length*2


def test_magnitude_and_count_limits_are_enforced():
    public = integer.construct((2, 5, 7), 2)
    labels, order, exponent = public["labels"], public["order"], public["exponent"]
    assert integer.decode((2, 5, 7), 2, exponent, 2*labels[0] % order) is None
    public = integer.construct((2, 5, 7), 1)
    assert integer.decode((2, 5, 7), 1, public["exponent"],
                          sum(public["labels"][:2]) % public["order"]) is None
    assert integer.decode((2, 5, 7), 1, public["exponent"], 0) == (0, 0, 0)


def test_norm_injectivity_does_not_certify_score_readout():
    counter = integer.readout_alias_control()
    assert counter["box_injective"]
    assert not counter["readout_license_valid"]
    assert counter["shifted"] == [-2, 0, 0]
    with pytest.raises(ValueError, match="height/readout"):
        integer.height_license((2, 5, 7), 1, 3)


def test_native_public_input_and_syndrome_replay():
    result = json.loads(integer.REPORT.read_text())
    assert result["producer_sha256"] == hashlib.sha256(
        Path(integer.__file__).read_bytes()).hexdigest()
    native = result["native"]
    primes = native["public_primes"]
    labels = list(map(int, native["public_labels_decimal"]))
    exponent = native["modulus_exponent"]
    modulus, order, _ = integer.lifting_data(exponent)
    assert modulus == int(native["modulus_decimal"])
    assert order == int(native["cyclic_order_decimal"])
    assert order.bit_length() == 924
    integer.validate_public_labels(primes, labels, exponent)
    assert [integer.lifted_log(p, exponent)[0] for p in primes] == labels
    error = [0]*len(primes)
    for position in native["positive_positions"]:
        error[position] = 1
    for position in native["negative_positions"]:
        error[position] = -1
    observed = int(native["observed_syndrome_decimal"])
    assert sum(a*e for a, e in zip(labels, error)) % order == observed
    assert integer.decode(primes, 35, exponent, observed) == tuple(error)
    assert error.count(1) == error.count(-1) == 35
    assert native["source_mean"] == integer.source_mean(1024, 35, Q(1, 20))
    assert Q(native["source_mean"]["mean_cosine_lower"]) > Q(304, 1000)
    assert native["preprocessing"]["ternary_digits_processed"] == 1024*(exponent-1)
    assert not native["full_group_enumerated"]
    assert not native["quantum_optimizer_executed"]
    assert not native["native_classical_optimizer_executed"]
    assert not result["classical_hardness_or_quantum_speedup_proved"]

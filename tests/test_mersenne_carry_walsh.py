from itertools import product
from hashlib import sha256
import json
from pathlib import Path

import pytest

from theorems import mersenne_carry_walsh as carry
from theorems import mersenne_reciprocal_access as access
from theorems import mersenne_reciprocal_curve as curve
from theorems.explicit_quadratic_opi import element


@pytest.mark.parametrize("precision", range(1, 9))
def test_parity_polynomial_all_residue_classes(precision):
    coefficients = carry.parity_polynomial(precision)
    modulus = 1 << precision
    assert len(coefficients) == precision
    for value in range(-modulus, modulus):
        observed = sum(coefficient*pow(value, k, modulus)
                       for k, coefficient in enumerate(coefficients)) % modulus
        assert observed == (1 if value % 2 == 0 else modulus-1)


@pytest.mark.parametrize("bits,precision", [(3, 5), (5, 7), (17, 19), (61, 63)])
def test_teichmuller_reduction_multiplicativity_and_base_trace(bits, precision):
    ring = carry.UnramifiedBinaryRing(bits, precision)
    for x, y in ((0, 1), (1, 7), (3, 5), ((1 << bits)-1, 2)):
        tx, ty = ring.teichmuller(x), ring.teichmuller(y)
        assert sum((int(tx[i]) & 1) << i for i in range(bits)) == x
        # Polynomial coefficient encoding, not an integer coercion of field elements.
        coefficients = (element(bits, x)*element(bits, y)).to_list()
        field_product = sum(int(coefficient) << i for i, coefficient in enumerate(coefficients))
        assert ring.multiply(tx, ty) == ring.teichmuller(field_product)
        total, conjugate = ring.zero, tx
        for _ in range(bits):
            total += conjugate
            conjugate = ring.multiply(conjugate, conjugate)
        assert ring.scalar(total) % 2 == int(element(bits, x).trace())


@pytest.mark.parametrize("bits,s", [(3, 1), (5, 2), (17, 3), (61, 14)])
def test_lifted_trace_parity_at_actual_inputs(bits, s):
    precision = min(bits+2, 9)
    ring = carry.UnramifiedBinaryRing(bits, precision)
    coefficients = carry.parity_polynomial(precision)
    q, order = 1 << bits, (1 << bits)-1
    for a, x in ((0, 1), (1, 3), (7, q-1)):
        ta, tx = ring.teichmuller(a), ring.teichmuller(x)
        first = tx.pow_mod((1-(1 << s)) % order, ring.polynomial)
        second = ring.multiply(ta, tx)
        trace = ring.zero
        for _ in range(bits):
            trace += first+second
            first, second = ring.multiply(first, first), ring.multiply(second, second)
        scalar = ring.scalar(trace)
        sign = 1-2*(curve.reciprocal_trace(bits, s, x)
                    ^ int((element(bits, a)*element(bits, x)).trace()))
        assert sum(h*pow(scalar, j, ring.modulus)
                   for j, h in enumerate(coefficients)) % ring.modulus == sign % ring.modulus


@pytest.mark.parametrize("bits,s,degree", [(3, 1, 2), (5, 2, 1)])
def test_cyclic_carry_equivalence_unique_and_bounded(bits, s, degree):
    order = (1 << bits)-1
    for choices in product(range(degree+1), repeat=2*bits):
        if sum(choices) > degree:
            continue
        u, v = choices[:bits], choices[bits:]
        digits = [u[i]+v[i]-u[(i-s) % bits] for i in range(bits)]
        total = sum(digit*(1 << i) for i, digit in enumerate(digits))
        roots = []
        for last in range(-degree, degree+1):
            previous, observed = last, []
            for digit in digits:
                if (digit+previous) % 2:
                    break
                previous = (digit+previous)//2
                observed.append(previous)
            else:
                if previous == last:
                    roots.append(observed)
        assert bool(roots) == (total % order == 0)
        if roots:
            assert len(roots) == 1 and roots[0][-1] == total//order
            assert all(abs(value) <= sum(choices) for value in roots[0])


@pytest.mark.parametrize("frequency", range(8))
def test_completed_signed_walsh_matches_all_small_field_frequencies(frequency):
    reference = access.finite_walsh_spectrum(3, 1)[frequency]
    result = carry.carry_walsh(3, 1, frequency)
    assert result["status"] == "EXACT_WALSH"
    assert result["walsh_value"] == reference
    assert result["walsh_residue"] == reference % 32
    assert result["full_precision"]
    assert not result["field_table_materialized"]


@pytest.mark.parametrize("frequency", [0, 1, 2, 7])
def test_nontrivial_extension_field_coefficients_at_full_precision(frequency):
    result = carry.carry_walsh(5, 1, frequency, max_transitions=3_000_000)
    assert result["status"] == "EXACT_WALSH"
    assert result["walsh_value"] == access.finite_walsh_spectrum(5, 1)[frequency]


def test_reordered_factors_and_overlapping_boundary_are_not_double_counted(monkeypatch):
    original_layout = carry.carry_layout
    reverse = {"multiplier": 4, "width": 1, "center_offset": -1,
               "previous_offset": 0, "shift_offset": 0,
               "canonical_constant_width": False}
    monkeypatch.setattr(carry, "carry_layout", lambda n, s: reverse)
    reversed_result = carry.carry_walsh(5, 1, 7, max_transitions=3_000_000)
    assert reversed_result["status"] == "EXACT_WALSH"
    assert reversed_result["walsh_value"] == access.finite_walsh_spectrum(5, 1)[7]
    overlap = original_layout(3, 1) | {"width": 2}
    monkeypatch.setattr(carry, "carry_layout", lambda n, s: overlap)
    overlap_result = carry.carry_walsh(3, 1, 1, precision=3)
    assert overlap_result["status"] == "EXACT_CONGRUENCE"
    assert overlap_result["walsh_residue"] == 4
    assert overlap_result["walsh_value"] is None


@pytest.mark.parametrize("bits,s", [(17, 3), (31, 7), (61, 14), (127, 31)])
def test_canonical_layout_binds_every_original_factor(bits, s):
    layout = carry.carry_layout(bits, s)
    assert layout["canonical_constant_width"] and layout["width"] <= 9
    multiplier = layout["multiplier"]
    for i in range(bits):
        center = multiplier*i % bits
        endpoint = (center-layout["center_offset"]) % bits
        assert (endpoint+layout["previous_offset"]) % bits == multiplier*(i-1) % bits
        assert (endpoint+layout["shift_offset"]) % bits == multiplier*(i-s) % bits


def test_cap_never_returns_a_partial_coefficient_or_falls_back_to_table(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("carry backend used full-field Fourier table")
    monkeypatch.setattr(access, "finite_walsh_spectrum", forbidden)
    monkeypatch.setattr(curve, "finite_walsh_control", forbidden)
    result = carry.carry_walsh(61, 14, 12345, max_transitions=100)
    assert result["status"] == "WORK_CAP"
    assert result["transitions"] == 100
    assert result["walsh_residue"] is result["walsh_value"] is None
    assert result["layout"]["multiplier"] == 4
    assert not result["field_table_materialized"]


def test_uncapped_is_explicit_and_low_precision_is_only_a_congruence():
    for precision in range(1, 6):
        result = carry.carry_walsh(3, 1, 1, precision=precision, max_transitions=None)
        assert result["walsh_residue"] == -4 % (1 << precision)
        assert result["transition_cap"] is None
        assert result["walsh_value"] == (-4 if precision >= 5 else None)


@pytest.mark.parametrize("bits,s,a", [(True, 1, 0), (4, 1, 0), (9, 3, 0),
                                     (5, 0, 0), (5, 2, True), (5, 2, -1), (5, 2, 32)])
def test_family_and_frequency_guards(bits, s, a):
    with pytest.raises(ValueError):
        carry.carry_walsh(bits, s, a)


@pytest.mark.parametrize("value", [True, False, 0, -1, 2.0, "3"])
def test_precision_and_cap_guards(value):
    with pytest.raises(ValueError):
        carry.carry_walsh(3, 1, 1, precision=value)
    with pytest.raises(ValueError):
        carry.parity_polynomial(value)
    with pytest.raises(ValueError):
        carry.carry_walsh(3, 1, 1, max_transitions=value)


def test_exact_oracle_returns_only_completed_signed_values():
    assert carry.exact_walsh_oracle(3, 1, 1) == -4
    with pytest.raises(carry.CarryWorkCap, match="transition cap"):
        carry.exact_walsh_oracle(17, 3, 1, max_transitions=1)


def test_sampler_does_not_confuse_oracle_work_cap_with_probabilistic_abort():
    def bounded_oracle(bits, s, frequency):
        return carry.exact_walsh_oracle(bits, s, frequency, max_transitions=1)
    with pytest.raises(carry.CarryWorkCap):
        access.sample_clipped_fourier(17, bounded_oracle)


def test_report_cli_replays_controls_and_source_hashes(tmp_path, capsys):
    output = tmp_path/"carry.json"
    carry.main(["--output", str(output)])
    carry.main([])
    assert capsys.readouterr().out == output.read_text()
    report = json.loads(output.read_text())
    root = Path(carry.__file__).resolve().parents[1]
    for name, digest in report["source_hashes_sha256"].items():
        assert sha256((root/name).read_bytes()).hexdigest() == digest
    for control in report["controls"]:
        if control["status"] == "EXACT_WALSH":
            assert control["walsh_value"] == access.finite_walsh_spectrum(
                control["bits"], control["s"])[control["frequency"]]
        else:
            assert control["status"] == "WORK_CAP"
            assert control["walsh_value"] is control["walsh_residue"] is None
    for key in ("full_precision_native_execution_completed",
                "canonical_reordered_execution_completed", "native_completion_solver",
                "practical_runtime_claimed", "quantum_advantage_claimed",
                "novelty_established", "field_table_materialized"):
        assert report[key] is False


def test_optional_native_congruence_report_never_upgrades_to_signed_value(monkeypatch):
    real_carry = carry.carry_walsh
    calls = []
    def capped_control(bits, s, frequency, **kwargs):
        if bits == 17:
            calls.append(kwargs)
            return real_carry(bits, s, frequency, precision=kwargs["precision"], max_transitions=1)
        return real_carry(bits, s, frequency, **kwargs)
    monkeypatch.setattr(carry, "carry_walsh", capped_control)
    report = carry.build_carry_walsh_report(native_mod32=True)
    assert calls == [{"precision": 5, "max_transitions": 8_000_000}]
    assert report["controls"][-1]["status"] == "WORK_CAP"
    assert not report["full_precision_native_execution_completed"]

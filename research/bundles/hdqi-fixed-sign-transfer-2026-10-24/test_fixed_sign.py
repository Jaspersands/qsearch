from fractions import Fraction as F
import math

import numpy as np
import pytest

import fixed_sign as f


@pytest.mark.parametrize("k", [1, 2, 3, 4, 6, 8])
@pytest.mark.parametrize("beta", [F(0), F(1, 4), F(1)])
def test_repeated_term_formulas_against_actual_physical_decoder(k, beta):
    model = f.repeated_model(k, beta)
    actual = f.dense_audit(model, lambda s: s >> 1)
    formula = f.repeated_formula(k, float(beta))
    for key in ("pilot_decoding_failure", "coherent_bad_mass", "target_norm_ratio", "actual_physical_trace_distance"):
        assert actual[key] == pytest.approx(formula[key], abs=1e-10)
    assert max(actual["identity_errors"].values()) < 1e-10


def test_random_sign_average_restores_the_published_error_identity():
    model = f.repeated_model(5)
    rows = [f.dense_audit(model, lambda s: s >> 1, mask) for mask in range(32)]
    r = rows[0]["pilot_decoding_failure"]
    assert sum(row["coherent_bad_mass"] for row in rows)/32 == pytest.approx(r, abs=1e-12)
    assert rows[0]["coherent_bad_mass"] > 3*r
    assert all(row["pilot_decoding_failure"] == pytest.approx(r) for row in rows)


def test_strict_rational_large_countercertificate():
    row = f.repeated_certificate(65536)
    assert F(row["pilot_failure_upper"]) < F(1, 250000)
    assert F(row["physical_trace_distance_strict_lower"]) > F(374, 1000)
    assert row["small_failure_does_not_certify_fixed_sign_Gibbs"]
    assert not row["random_sign_theorem_falsified"] and not row["large_pilot_built"]


def test_small_certificate_can_be_inconclusive():
    assert not f.repeated_certificate(2)["small_failure_does_not_certify_fixed_sign_Gibbs"]


def test_failure_vanishes_while_fixed_target_error_persists():
    rows = [f.repeated_formula(k) for k in (16, 256, 65536, 2**32)]
    assert all(b["pilot_decoding_failure"] < a["pilot_decoding_failure"] for a, b in zip(rows, rows[1:]))
    assert rows[-1]["pilot_decoding_failure"] < 1e-10
    assert rows[-1]["actual_physical_trace_distance"] > .38
    assert rows[-1]["coherent_bad_mass"] > .28
    assert math.isclose(rows[-1]["target_norm_ratio"], math.cosh(1), rel_tol=1e-9)


def test_injective_noncommuting_input_is_a_positive_exact_transfer_control():
    model = f.i.o.d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [F(3, 5), F(-4, 5)], F(1))
    row = f.dense_audit(model, lambda syndrome: syndrome)
    assert row["pilot_decoding_failure"] == 0 and row["coherent_bad_mass"] == 0
    assert row["actual_physical_trace_distance"] < 1e-12


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_general_noncommuting_redundant_input_and_bad_decoders(seed):
    model = f.i.o.d.Physical.create(2, [(1, 0, 0), (0, 1, 0), (1, 1, 1), (0, 2, 0)],
                                  [1, F(-1, 2), F(3, 4), F(1, 4)], F(1, 2))
    table = np.random.default_rng(seed).integers(0, 16, size=16)
    row = f.dense_audit(model, lambda syndrome: int(table[syndrome]))
    assert max(row["identity_errors"].values()) < 1e-10
    assert row["actual_TFD_infidelity"] <= row["fixed_sign_infidelity_upper"]+1e-10
    assert row["coherent_bad_mass"] <= row["pilot_decoding_failure"]+float(F(f.weighted_kernel(model)["weighted_sum"]))+1e-10


def test_independent_signs_do_not_preserve_grouped_circuit_parent_structure():
    row = f.sign_structure_control()
    assert row["original_grouped_terms_commute"]
    assert row["one_independent_Pauli_sign_flip_breaks_commutation"]
    assert row["changed_commutator_coefficient_on_X1X2Z1Z2"] == ["0", "-48/25"]


@pytest.mark.parametrize("k,beta", [(0, 1), (True, 1), (4, -1), (4, math.nan), (4, True)])
def test_invalid_formula_inputs(k, beta):
    with pytest.raises(ValueError):
        f.repeated_formula(k, beta)


def test_dense_and_sign_guards():
    with pytest.raises(ValueError):
        f.repeated_model(9)
    with pytest.raises(ValueError):
        f.dense_audit(f.repeated_model(2), lambda s: s >> 1, 4)


def long_relation_model(n=3, beta=F(1, 16)):
    ps = [(1 << j, 0, 0) for j in range(n)]+[(0, 1 << j, 0) for j in range(n)]
    ps.append(((1 << n)-1, (1 << n)-1, n % 2))
    return f.i.o.d.Physical.create(n, ps, [1]*len(ps), beta)


@pytest.mark.parametrize("seed", range(8))
def test_exact_kernel_enumerator_matches_exhaustive_physical_labels(seed):
    rng = np.random.default_rng(seed)
    ps = []
    for _ in range(7):
        x, z = map(int, rng.integers(0, 4, size=2))
        ps.append((x, z, (x & z).bit_count() % 2))
    js = [F(int(j), 4) for j in rng.integers(-4, 5, size=7)]
    model = f.i.o.d.Physical.create(2, ps, js, F(3, 4))
    result = f.weighted_kernel(model)
    expected, counts = F(0), {}
    for y in range(1, 128):
        if model.label(y) == 0:
            size = str(y.bit_count())
            counts[size] = counts.get(size, 0)+1
            expected += math.prod((min(F(1), model.pilot.beta*abs(j)) for k, j in enumerate(js) if y >> k & 1), start=F(1))
    assert F(result["weighted_sum"]) == expected
    assert result["weight_counts"] == counts


@pytest.mark.parametrize("beta", [F(0), F(1, 16), F(1, 4), F(1)])
def test_constructive_fixed_sign_transfer_bound_against_dense_output(beta):
    model = long_relation_model(beta=beta)
    decoder, report = f.certify_transfer(model, 2)
    row = f.dense_audit(model, decoder)
    r = row["pilot_decoding_failure"]
    weight = F(report["kernel"]["weighted_sum"])
    assert row["coherent_bad_mass"] <= r+float(weight)+1e-12
    assert r <= float(F(report["decoder"]["failure_upper"]))+1e-12
    assert row["actual_pair_trace_distance"]**2 <= float(F(report["trace_distance_squared_upper"]))+1e-12
    assert (report["status"] == "CERTIFIED_IDEAL_PILOT_TRANSFER") == (beta <= F(1, 16))
    assert not report["quantum_advantage_claimed"]
    for y in range(128):
        assert model.label(decoder(model.label(y))) == model.label(y)
        if y.bit_count() <= 2:
            assert decoder(model.label(y)) == y


def test_large_low_kernel_rank_certificate_without_dense_pilot():
    model = long_relation_model(32, F(1, 128))
    _, result = f.certify_transfer(model, 2, F(1, 10000))
    assert result["status"] == "CERTIFIED_IDEAL_PILOT_TRANSFER"
    assert result["kernel"]["checked_words"] == 1
    assert result["kernel"]["weight_counts"] == {"65": 1}
    assert result["decoder"]["checked_words"] == 2146


def test_injective_decoder_certifies_exact_transfer_without_enumeration():
    model = f.i.o.d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, 1], 1)
    decoder, report = f.certify_transfer(model, 2, max_kernel_words=0, max_decoder_words=0)
    assert report["status"] == "CERTIFIED_IDEAL_PILOT_TRANSFER"
    assert report["trace_distance_squared_upper"] == "0"
    assert all(decoder(model.label(y)) == y for y in range(4))


def test_duplicate_terms_fail_low_weight_and_kernel_budget_gates():
    model = f.repeated_model(8)
    decoder, report = f.certify_transfer(model, 1)
    assert decoder is None
    assert report["decoder"]["status"] == "LOW_WEIGHT_COLLISION"
    witness = report["decoder"]["collision"]
    assert witness["first"] != witness["second"]
    assert model.label(witness["first"]) == model.label(witness["second"])
    assert report["status"] == "NO_CERTIFICATE"
    _, report = f.certify_transfer(model, 0, max_kernel_words=1)
    assert report["kernel"]["status"] == "UNKNOWN_BUDGET"
    assert report["kernel"]["weighted_sum"] is None
    assert report["trace_distance_squared_upper"] is None


def test_decoder_budget_refuses_before_enumeration():
    _, result = f.certify_transfer(long_relation_model(), 2, max_decoder_words=28)
    assert result["decoder"]["checked_words"] == 0
    assert result["decoder"]["status"] == "UNKNOWN_BUDGET"
    assert result["status"] == "NO_CERTIFICATE"


@pytest.mark.parametrize("kwargs", [{"t": -1}, {"t": True}, {"t": 8}, {"t": 2, "epsilon": 0},
                                    {"t": 2, "max_kernel_words": -1}, {"t": 2, "max_decoder_words": True}])
def test_certificate_argument_guards(kwargs):
    with pytest.raises(ValueError):
        f.certify_transfer(long_relation_model(), **kwargs)


def test_physical_pauli_sign_gauges_cannot_remove_bad_coherence():
    model = f.repeated_model(5)
    gauge_masks = {sum(((a & model.label(1 << j)).bit_count() % 2) << j for j in range(5))
                   for a in range(4)}
    assert gauge_masks == {0, 31}
    rows = [f.dense_audit(model, lambda s: s >> 1, mask) for mask in sorted(gauge_masks)]
    assert rows[0]["coherent_bad_mass"] == pytest.approx(rows[1]["coherent_bad_mass"], abs=1e-12)
    assert rows[0]["coherent_bad_mass"] > 3*rows[0]["pilot_decoding_failure"]


def test_kernel_bound_includes_identity_and_zero_couplings():
    model = f.i.o.d.Physical.create(1, [(0, 0, 0), (1, 0, 0), (1, 0, 0)], [F(1, 2), 1, 0], F(1))
    weight = f.weighted_kernel(model)
    assert F(weight["weighted_sum"]) == F(1, 2)
    for decoder in (lambda s: 0, lambda s: 7, lambda s: 2*s):
        row = f.dense_audit(model, decoder)
        assert row["coherent_bad_mass"] <= row["pilot_decoding_failure"]+.5+1e-12


def test_kernel_certificate_is_useful_but_is_not_necessary():
    model = long_relation_model()
    _, report = f.certify_transfer(model, 2)
    r = F(report["decoder"]["failure_upper"])
    assert F(report["trace_distance_squared_upper"]) < 3*r
    _, refused = f.certify_transfer(model, 2, F(1, 10**10))
    assert refused["status"] == "NO_CERTIFICATE" and not refused["hardness_from_refusal"]


@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_noncommuting_representation_dilution_for_multiple_decoders(k):
    model = f.i.o.d.Physical.create(1, [(1, 0, 0), (0, 1, 0)]*k,
                                  [F(3, 5*k), F(-4, 5*k)]*k, F(1))
    section, _ = f.low_weight_section(model, 0)
    for decoder in (section, lambda s: 0, lambda s: (1 << (2*k))-1):
        row = f.dense_audit(model, decoder)
        assert row["actual_physical_distance_to_maximally_mixed"]**2 <= 1/(4*k)+1e-12


def test_total_decoder_and_kernel_budget_input_checks():
    decoder, _ = f.low_weight_section(long_relation_model(), 2)
    for syndrome in (-1, 64, True, .5):
        with pytest.raises(ValueError):
            decoder(syndrome)
    with pytest.raises(ValueError):
        f.weighted_kernel(long_relation_model(), True)

from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from math import comb, isqrt
from pathlib import Path

import pytest

from theorems import balanced_signed_mpi
from theorems import mersenne_reciprocal_access as access
from theorems import mersenne_reciprocal_curve as curve
from theorems.balanced_filter_channel_audit import projection_size
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import mds_character_bound


SMALL_PARAMETERS = [(3, 1), (3, 2), (5, 1), (5, 2), (5, 3), (5, 4)]


def small_instance():
    return curve.make_instance(5, 2, [0, 1, 2], [0, 1, 0], 1)


@pytest.mark.parametrize("bits,s", SMALL_PARAMETERS)
def test_differential_counts_exhaustive_and_native_output_relabeling(bits, s):
    q = 1 << bits
    exponent = (1 << (bits-s))-1
    vector = [encoded(element(bits, x)**exponent) for x in range(q)]
    native = [curve.reciprocal_value(bits, s, x) for x in range(q)]
    counts = Counter(vector[x ^ 1] ^ vector[x] for x in range(q))
    native_counts = Counter(native[x ^ 1] ^ native[x] for x in range(q))
    actual = [access.differential_count(bits, s, c) for c in range(q)]
    assert actual == [counts[c] for c in range(q)]
    assert sum(actual) == q
    for c in range(q):
        relabeled = encoded(element(bits, c)**(1 << (bits-s)))
        assert actual[relabeled] == native_counts[c]
    assert actual[0] == 0


@pytest.mark.parametrize("bits,s", SMALL_PARAMETERS)
def test_gauss_blocks_against_every_quadratic_character_sum(bits, s):
    q, h = 1 << bits, 1 << (s-1)
    elements = [element(bits, word) for word in range(q)]
    characters = [[1-2*int((t*x).trace()) for x in elements] for t in elements]
    for b in (0, 1):
        # Enumerate the actual unguarded lift, not the reduced Gauss formula.
        residuals = [[encoded(v*v+x**h*v+x+b*x**(2*h)) for v in elements]
                     for x in elements]
        for t in range(q):
            inner = [sum(characters[t][value] for value in row) for row in residuals]
            for a in range(q):
                expected = sum(inner[x]*characters[a][x] for x in range(q))
                assert access.gauss_block(bits, s, t, a, b) == expected
                if t == 0:
                    assert expected == q*q*int(a == 0)
                else:
                    assert abs(expected) == q


@pytest.mark.parametrize("bits,s", SMALL_PARAMETERS)
def test_walsh_matches_curve_control_in_field_frequency_order(bits, s):
    actual = access.finite_walsh_spectrum(bits, s)
    control = curve.finite_walsh_control(bits, s)
    assert actual == control["walsh"]
    assert actual[0] == 0
    assert sum(w*w for w in actual) == 1 << (2*bits)
    if s == bits-1:
        assert actual[1] == 1 << bits
        assert sum(w != 0 for w in actual) == 1


def test_transform_modulus_centering_and_trace_index_conversion(monkeypatch):
    bits, s, q = 5, 2, 32
    calls = []
    original_walsh, original_indices = access.walsh, access.trace_indices

    def checked_walsh(vector, modulus):
        assert modulus == 2*q+1
        assert vector == [1-2*curve.reciprocal_trace(bits, s, x) for x in range(q)]
        calls.append("walsh")
        return original_walsh(vector, modulus)

    def checked_indices(n):
        assert n == bits
        calls.append("trace_indices")
        return original_indices(n)

    monkeypatch.setattr(access, "walsh", checked_walsh)
    monkeypatch.setattr(access, "trace_indices", checked_indices)
    spectrum = access.finite_walsh_spectrum(bits, s)
    assert calls == ["walsh", "trace_indices"]
    assert min(spectrum) < 0
    raw = original_walsh([1-2*curve.reciprocal_trace(bits, s, x) for x in range(q)], 2*q+1)
    centered = tuple(w if w <= q else w-(2*q+1) for w in raw)
    assert spectrum == tuple(centered[i] for i in original_indices(bits))
    assert spectrum != centered


@pytest.mark.parametrize("bits,s", [(3, 2), (5, 2), (17, 3)])
def test_compact_fourier_report_hash_histogram_and_exact_tv(bits, s, monkeypatch):
    spectrum = access.finite_walsh_spectrum(bits, s)
    monkeypatch.setattr(access, "finite_walsh_spectrum", lambda n, k: spectrum)
    report = access.finite_fourier_report(bits, s)
    q = 1 << bits
    assert "walsh" not in report and "spectrum" not in report
    assert report["field_modulus_coefficients"] == list(map(int, field(bits).modulus().coeffs()))
    assert report["field_basis"] and report["frequency_order"]
    assert report["transform_modulus"] == 2*q+1
    assert report["walsh_at_zero"] == spectrum[0] == 0
    assert report["walsh_at_one"] == spectrum[1]
    assert report["parseval_sum"] == q*q and report["parseval_checked"]
    assert report["histogram"] == dict(Counter(spectrum))
    assert sum(report["histogram"].values()) == q
    assert report["distinct_values"] == len(set(spectrum))
    expected_tv = sum((abs(Fraction(w*w, q*q)-Fraction(1, q)) for w in spectrum), Fraction(0))/2
    assert type(report["tv_from_uniform"]) is Fraction
    assert report["tv_from_uniform"] == expected_tv
    assert report["spectrum_sha256"] == hashlib.sha256(
        json.dumps(list(spectrum), separators=(",", ":")).encode("ascii")
    ).hexdigest()
    assert report["full_field_entries"] == q
    assert report["exponential_control"] and report["field_tables_materialized"]
    for key in ("classical_hardness_claimed", "quantum_advantage_claimed",
                "full_quantum_algorithm_implemented",
                "polynomial_classical_walsh_access_established",
                "polynomial_classical_source_access_claimed"):
        assert report[key] is False
    if (bits, s) == (17, 3):
        assert report["walsh_at_one"] == -848
        assert report["distinct_values"] == 145
        assert report["tv_from_uniform"] == Fraction(32345987, 67108864)
        assert len(json.dumps(report, default=str)) < 10_000


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_half_boundary_exact_guarantees_and_inverse_length_success(bits):
    problem = curve.native_instance(bits)
    before = deepcopy(problem)
    n, k, q = len(problem["points"]), problem["checks"], 1 << bits
    t, m = n-4*k, 4*k
    report = access.partial_completion_budget(problem, t)
    beta = min(Fraction(1), Fraction(1+(1 << problem["s"])*(isqrt(q)+1), q))
    assert report["beta"] == beta
    assert report["eta_N"] == mds_character_bound(bits, n, k, beta)
    assert report["eta_M"] == mds_character_bound(bits, m, k, beta)
    assert report["eta_N"] <= report["eta_M"] < Fraction(1, 2)
    remainder = bits-4*problem["s"]
    assert report["eta_M"] < Fraction(1, 1 << ((remainder-1)*k))
    assert report["all_accepted_fixed_assignments_extend"]
    assert report["native_fiber_nonempty_guaranteed"]
    assert report["fixed_marginal_tv_upper"] == report["eta_M"]/(1-report["eta_N"])
    assert report["fixed_count"] == t and report["remaining"] == m
    assert report["radius"] == 2*k
    assert report["strict_johnson"] and report["johnson_gap"] == m
    tau = Fraction(sum(comb(m, j) for j in range(2*k+1)), 1 << m)
    assert report["tau"] == tau == Fraction(1, 2)+Fraction(comb(m, m//2), 1 << (m+1))
    padding = 1 << k.bit_length()
    assert report["padding"] == projection_size(m, k, m//2, q**k) == padding
    assert k+1 <= padding < 2*(k+1)
    success = report["native_success_per_attempt_lower"]
    assert type(success) is Fraction
    assert success == (1-report["eta_M"])*tau*tau/padding
    # Matched constant multiples of 1/N at each requested boundary fixture.
    assert Fraction(1, 2*n) < success < Fraction(8, n)
    assert problem == before
    for key in ("requires_paid_syndrome_offset_source", "requires_paid_known_source_preparation",
                "requires_complete_reversible_list_decoder", "requires_clean_fixed_padding_projection",
                "requires_final_native_verification", "tv_requires_nonempty_native_fiber"):
        assert report[key] is True
    assert report["syndrome_scope"] == "PUBLIC_SYNDROME_FROM_ACCEPTED_FIXED_COORDINATES"
    for key in ("unknown_syndrome_algorithm", "completion_solver_implemented",
                "field_tables_materialized", "quantum_premises_verified",
                "full_quantum_algorithm_implemented", "classical_hardness_claimed",
                "quantum_advantage_claimed"):
        assert report[key] is False


def test_budget_uses_generic_helpers_without_any_large_control(monkeypatch):
    problem = curve.native_instance(61)

    def forbidden(*args, **kwargs):
        raise AssertionError("budget called a spectral, field-element or solver control")

    for name in ("finite_walsh_spectrum", "finite_fourier_report", "differential_count",
                 "gauss_block", "element", "walsh", "trace_indices"):
        monkeypatch.setattr(access, name, forbidden)
    for name in ("finite_walsh_control", "finite_curve_count", "functional_degree_control",
                 "reciprocal_trace", "reciprocal_value", "root_from_seed", "root_from_trace", "element"):
        monkeypatch.setattr(curve, name, forbidden)
    monkeypatch.setattr(balanced_signed_mpi, "presentation", forbidden)
    calls = []

    def generic_bound(bits, length, checks, beta):
        calls.append((bits, length, checks, beta))
        return mds_character_bound(bits, length, checks, beta)

    monkeypatch.setattr(access, "mds_character_bound", generic_bound)
    n, k = len(problem["points"]), problem["checks"]
    report = access.partial_completion_budget(problem, n-4*k)
    assert [row[1] for row in calls] == [n, 4*k]
    assert report["native_success_per_attempt_lower"] > 0


def test_vacuous_bounds_and_johnson_failure_are_not_positive_claims(monkeypatch):
    report = access.partial_completion_budget(small_instance(), 0)
    assert report["beta"] == Fraction(25, 32)
    assert report["eta_N"] >= 1 and report["eta_M"] >= 1
    assert not report["all_accepted_fixed_assignments_extend"]
    assert not report["native_fiber_nonempty_guaranteed"]
    assert report["fixed_marginal_tv_upper"] == 1
    assert report["native_success_per_attempt_lower"] == 0
    linear = curve.make_instance(5, 4, [0, 1, 2], [0, 1, 0], 1)
    assert access.partial_completion_budget(linear, 0)["beta"] == 1

    def forbidden(*args, **kwargs):
        raise AssertionError("failed Johnson gate reached binomial or padding work")

    monkeypatch.setattr(access, "projection_size", forbidden)
    monkeypatch.setattr(access, "_binomial_prefix", forbidden)
    for k, gap in ((2, 0), (3, -4)):
        problem = curve.make_instance(5, 2, list(range(4)), [0]*4, k)
        report = access.partial_completion_budget(problem, 0)
        assert not report["strict_johnson"] and report["johnson_gap"] == gap
        assert report["tau"] is report["padding"] is report["native_success_per_attempt_lower"] is None


def test_budget_is_uniform_over_public_points_and_targets_but_s_bound():
    problem = curve.native_instance(17)
    fixed = len(problem["points"])-4*problem["checks"]
    original = access.partial_completion_budget(problem, fixed)
    changed = deepcopy(problem)
    changed["points"] = [point+1000 for point in reversed(problem["points"])]
    changed["targets"] = [i % 2 for i in range(len(problem["points"]))]
    assert access.partial_completion_budget(changed, fixed) == original
    changed["s"] = 4
    other = access.partial_completion_budget(changed, fixed)
    assert other["s"] == 4
    assert other["beta"] == Fraction(1+16*(isqrt(1 << 17)+1), 1 << 17)
    assert other["beta"] != original["beta"]
    assert not other["canonical_research_parameters"]


def test_tv_clipping_and_strict_positivity_threshold(monkeypatch):
    for eta_n, eta_m, tv in ((Fraction(1, 2), Fraction(3, 4), Fraction(1)),
                             (Fraction(0), Fraction(1), Fraction(1)),
                             (Fraction(1), Fraction(2), Fraction(1))):
        bounds = iter((eta_n, eta_m))
        monkeypatch.setattr(access, "mds_character_bound", lambda *args: next(bounds))
        report = access.partial_completion_budget(small_instance(), 1)
        assert report["fixed_marginal_tv_upper"] == tv
        assert report["all_accepted_fixed_assignments_extend"] == (eta_m < 1)
        assert report["native_success_per_attempt_lower"] == max(Fraction(0), 1-eta_m)*report["tau"]**2/report["padding"]


@pytest.mark.parametrize("bits,s", [(True, 1), (5.0, 2), (5, True), (5, 2.0),
                                       (2, 1), (4, 1), (129, 1), (9, 3), (5, 0), (5, 5)])
def test_strict_parameter_guards_for_every_access_primitive(bits, s):
    for call in (lambda: access.differential_count(bits, s, 0),
                 lambda: access.gauss_block(bits, s, 0, 0, 0),
                 lambda: access.finite_walsh_spectrum(bits, s),
                 lambda: access.finite_fourier_report(bits, s)):
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize("bad", [True, False, -1, 32, 1.0, "1", None])
def test_field_word_guards_even_on_zero_gauss_branch(bad):
    for call in (lambda: access.differential_count(5, 2, bad),
                 lambda: access.gauss_block(5, 2, bad, 0, 0),
                 lambda: access.gauss_block(5, 2, 0, bad, 0),
                 lambda: access.gauss_block(5, 2, 0, 0, bad)):
        with pytest.raises(ValueError):
            call()
    with pytest.raises(ValueError):
        access.gauss_block(5, 2, 0, 0, 2)


@pytest.mark.parametrize("bits,s", [(19, 4), (31, 7), (61, 14), (127, 31)])
def test_full_table_cap_precedes_field_access(bits, s, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("oversized control accessed the field")

    monkeypatch.setattr(access, "element", forbidden)
    monkeypatch.setattr(access, "trace_indices", forbidden)
    for function in (access.finite_walsh_spectrum, access.finite_fourier_report):
        with pytest.raises(ValueError, match="finite Walsh control bits"):
            function(bits, s)


def test_polynomial_queries_do_not_build_field_tables(monkeypatch):
    calls = []
    original_element = access.element

    def counted(bits, word):
        calls.append(word)
        return original_element(bits, word)

    def forbidden(*args, **kwargs):
        raise AssertionError("polynomial query requested an exponential control")

    monkeypatch.setattr(access, "element", counted)
    for name in ("walsh", "trace_indices", "finite_walsh_spectrum"):
        monkeypatch.setattr(access, name, forbidden)
    count = access.differential_count(127, 31, 7)
    assert 0 <= count <= 1 << 127 and count % 2 == 0
    assert len(calls) == 128
    calls.clear()
    assert abs(access.gauss_block(127, 31, 7, 3, 1)) == 1 << 127
    assert len(calls) <= 3


@pytest.mark.parametrize("fixed", [True, False, -1, 2, 3, 1.0, None])
def test_fixed_coordinate_count_guard(fixed):
    with pytest.raises(ValueError):
        access.partial_completion_budget(small_instance(), fixed)


@pytest.mark.parametrize("key,value", [
    ("problem_family", "inverse_trace"), ("schema_version", True), ("schema_version", 2),
    ("bits", True), ("bits", 4), ("s", True), ("s", 0), ("checks", True),
    ("points", [0, 1, 1]), ("points", [0, True, 2]), ("points", [0, 1, 32]),
    ("targets", [0, 1]), ("targets", [0, True, 0]), ("targets", [0, 2, 0]),
    ("field_modulus_coefficients", [1, 0, 0, 0, 0, 1]),
])
def test_budget_reuses_canonical_instance_validation(key, value):
    problem = small_instance()
    problem[key] = value
    with pytest.raises(ValueError):
        access.partial_completion_budget(problem, 0)


def test_budget_rejects_noncanonical_modulus_container_bools_and_schema():
    original = small_instance()
    bad = [dict(original, extra=0), None, []]
    for key in original:
        problem = deepcopy(original)
        del problem[key]
        bad.append(problem)
    for modulus in (tuple(original["field_modulus_coefficients"]),
                    [bool(c) for c in original["field_modulus_coefficients"]]):
        bad.append(dict(original, field_modulus_coefficients=modulus))
    for problem in bad:
        with pytest.raises(ValueError):
            access.partial_completion_budget(problem, 0)


@pytest.mark.parametrize("bits,s,t,expected_x", [(5, 2, 2, 12),
                                                   (17, 3, 6, 39667),
                                                   (31, 7, 2, 1533916894)])
def test_old_accepted_conic_does_not_transfer_to_new_predicate(bits, s, t, expected_x):
    parameter = element(bits, t)
    denominator = parameter*parameter+parameter+field(bits).one()
    assert denominator != 0
    x = encoded(denominator**-1)
    assert x == expected_x
    assert int(denominator.trace()) == 1
    assert curve.reciprocal_trace(bits, 1, x) == 1
    assert curve.reciprocal_trace(bits, s, x) == 0


@pytest.fixture(scope="module")
def replayed_report():
    return access.access_report()


def _json_normalize(report):
    def fraction_pair(value):
        assert type(value) is Fraction
        return [value.numerator, value.denominator]
    return json.loads(json.dumps(report, default=fraction_pair))


def test_saved_report_replays_all_claims_and_source_hashes(replayed_report):
    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root/"research/classical_baselines/mersenne_reciprocal_access.json").read_text())
    assert saved == _json_normalize(replayed_report)
    for name, digest in saved["source_sha256"].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest
    assert saved["status"] == "LOCAL_ACCESS_CONSTRUCTED_NATIVE_COMPLETION_UNRESOLVED"
    assert saved["polynomial_classical_walsh_access_established"] is True
    assert saved["polynomial_approximate_local_sampling_construction"] is True
    assert "capped reference" in saved["walsh_access_scope"]
    for key in ("compiled_quantum_algorithm", "native_classical_solver",
                "practical_classical_runtime_established", "exact_local_fourier_sampler_established",
                "quantum_advantage_established",
                "classical_hardness_established", "standard_problem_reduction_established",
                "novelty_established"):
        assert saved[key] is False


def test_serialized_bounds_round_outward_and_keep_original_checks(replayed_report):
    for row in replayed_report["native_parameter_bounds"]:
        problem = curve.native_instance(row["bits"])
        n, k = len(problem["points"]), problem["checks"]
        report = access.partial_completion_budget(problem, n-4*k)
        assert row["checks"] == k and row["remaining"] == 4*k
        assert row["fixed_count"] == (n+1)//2
        for original, key in (("eta_N", "eta_N_power2_upper"),
                              ("eta_M", "eta_M_power2_upper"),
                              ("fixed_marginal_tv_upper", "marginal_tv_power2_upper")):
            upper = Fraction(2)**row[key]
            assert upper/2 < report[original] <= upper
        lower = Fraction(*row["conditional_quantum_success_lower"])
        exact = report["native_success_per_attempt_lower"]
        assert lower <= exact < lower+Fraction(1, 1 << 128)
        assert row["quantum_success_above_one_over_twice_N"]
        assert not row["full_quantum_algorithm_implemented"]
        assert not row["completion_solver_implemented"]
        assert row["clipped_sampler"]["walsh_oracle_required"]
        assert not row["clipped_sampler"]["polynomial_classical_walsh_access_established"]


def test_access_report_cli_exact_json_and_output_file(replayed_report, monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(access, "access_report", lambda: replayed_report)
    access.main([])
    stdout = capsys.readouterr().out
    assert json.loads(stdout) == _json_normalize(replayed_report)
    destination = tmp_path/"report.json"
    access.main(["--output", str(destination)])
    assert capsys.readouterr().out == ""
    assert destination.read_text() == stdout

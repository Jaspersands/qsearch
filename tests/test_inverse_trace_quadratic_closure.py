import hashlib
import json
from random import Random

import pytest

from theorems.balanced_codeword_filter import reciprocal_trace, trace_mask
from theorems.cubic_rs_affine_flats import solve_binary
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_quadratic_closure import (
    REPORT, ROOT, conditioned_lift, dense_countercontrol, native_linear_rows,
    slice_hull_certificate, support_word, verify_moments,
)


@pytest.mark.parametrize("bits", [5, 6, 7])
@pytest.mark.parametrize("target", [0, 1])
def test_all_small_native_slice_points_have_exactly_the_claimed_affine_hull(bits, target):
    points = []
    for y in range(1 << bits):
        if int(element(bits, y).trace()) == target:
            x = encoded(element(bits, y)**-1) if y else 0
            points.append((1 | (x << 1) | (y << (bits+1)), 0))
    assert solve_binary(points, 2*bits+1)["rank"] == 2*bits
    certificate = slice_hull_certificate(bits)
    assert certificate["character_sum_upper"] < certificate["slice_size"]


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_large_slice_lift_is_target_conditioned_and_not_a_native_pair(bits):
    trace = trace_mask(bits, 1)
    row = conditioned_lift(bits, 1, 0, trace & -trace)
    assert row["status"] == "VERIFIED_TARGET_CONDITIONED_AFFINE_LIFT"
    assert row["rank"] == 2*bits
    mean = 0
    for x, y in row["selected_graph_points"]:
        assert x != 0
        assert int(element(bits, y).trace()) == 1
        assert encoded(element(bits, x)*element(bits, y)) == 1
        mean ^= x | (y << bits)
    assert mean == (trace & -trace) << bits


def test_failed_local_span_stays_unknown():
    class ZeroRng:
        def getrandbits(self, bits):
            return 0

    row = conditioned_lift(17, 1, 0, 1, rng=ZeroRng())
    assert row["status"] == "UNKNOWN_SLICE_SPAN_BUDGET"
    assert row["rank"] == 1


@pytest.mark.parametrize("checks", [1, 2, 3])
def test_two_native_minimum_support_words_intersect_only_at_the_pivot(checks):
    points = tuple(range(2*checks+1))
    u = support_word(5, points, checks, tuple(range(checks+1)), 0)
    v = support_word(5, points, checks, (0, *range(checks+1, 2*checks+1)), 0)
    assert u[0] == v[0] == 1
    assert [i for i in range(len(points)) if u[i] and v[i]] == [0]
    for word in (u, v):
        assert sum(x != 0 for x in word) == checks+1
        for degree in range(checks):
            assert sum((element(5, a)**degree*element(5, x) for a, x in zip(points, word)),
                       field(5).zero()) == 0


@pytest.mark.parametrize("bits,length,checks", [(5, 3, 1), (5, 5, 2), (7, 7, 3)])
def test_coupled_relaxation_passes_every_check_but_projected_zero_is_false(bits, length, checks):
    row = dense_countercontrol(bits, tuple(range(length)), checks, tuple(i % 2 for i in range(length)))
    assert row["verification"]["valid"]
    assert not row["native_witness"]
    assert row["verification"]["checked_linear_and_multiplied_equations"] == (bits*checks+length)*(2*bits*length+1)
    assert not row["higher_degree_or_general_classical_attack_excluded"]


def test_extension_also_works_for_nonzero_code_projections_and_arbitrary_trace_means():
    n, points, k = 5, (0, 3, 5, 11, 17), 2
    x = support_word(n, points, k, (0, 2, 4), 2)
    rng = Random(1022)
    y = tuple(rng.getrandbits(n) for _ in points)
    targets = tuple(int(element(n, value).trace()) for value in y)
    row = dense_countercontrol(n, points, k, targets, x_means=x, y_means=y)
    assert row["verification"]["valid"]
    assert any(row["projected_x"])


def test_verifier_detects_native_outer_product_and_cross_block_tampering():
    row = dense_countercontrol(5, (0, 1, 2), 1, (1, 0, 1))
    mean = int(row["means_hex"], 16)
    original = list(map(lambda x: int(x, 16), row["moment_rows_hex"]))
    args = (5, row["points"], 1, row["targets"], mean)
    genuine = [mean if (mean >> j) & 1 else 0 for j in range(30)]
    check = verify_moments(*args, genuine, row["local_lifts"])
    assert not check["valid"]
    assert check["failures"]["local_quadratic"] > 0
    # Alter only an inter-block xy product, preserving symmetry and the diagonal.
    original[0] ^= 1 << 20
    original[20] ^= 1
    check = verify_moments(*args, original, row["local_lifts"])
    assert not check["valid"]
    assert check["failures"]["symmetry"] == 0
    assert check["failures"]["local_quadratic"] == 0
    assert check["failures"]["linear_times_variable"] > 0


def test_degree_two_certificate_remains_valid_under_affine_linear_elimination():
    row = dense_countercontrol(5, (0, 1, 2, 3, 4), 2, (0, 1, 1, 0, 1))
    mean = int(row["means_hex"], 16)
    moments = [int(x, 16) for x in row["moment_rows_hex"]]
    covariance = [m ^ (mean if (mean >> i) & 1 else 0) for i, m in enumerate(moments)]
    for linear, _ in native_linear_rows(5, row["points"], 2, row["targets"]):
        assert all((linear & column).bit_count() % 2 == 0 for column in covariance)
    assert all((c >> i) & 1 == 0 for i, c in enumerate(covariance))


@pytest.mark.parametrize("args", [(4, (0, 1, 2), 1, (0, 1, 0)),
                                  (5, (0, 1, 2, 3), 2, (0, 1, 0, 1)),
                                  (17, tuple(range(9)), 1, (0,)*9),
                                  (5, (0, 1, 1), 1, (0, 1, 0))])
def test_scope_and_dense_caps_are_not_silently_relaxed(args):
    with pytest.raises(ValueError):
        dense_countercontrol(*args)


def test_illegal_first_moments_and_certificate_width_are_rejected():
    with pytest.raises(ValueError, match="linear constraints"):
        dense_countercontrol(5, (0, 1, 2), 1, (1, 0, 1), x_means=(1, 0, 0))
    with pytest.raises(ValueError, match="trace"):
        conditioned_lift(5, 1, 0, 0)
    row = dense_countercontrol(5, (0, 1, 2), 1, (1, 0, 1))
    with pytest.raises(ValueError, match="projected binary"):
        verify_moments(5, row["points"], 1, row["targets"], 1 << 30,
                       [int(x, 16) for x in row["moment_rows_hex"]], row["local_lifts"])


def test_live_artifact_replays_real_tables_and_source_proof_hashes():
    data = json.loads(REPORT.read_text())
    assert data["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/inverse_trace_quadratic_closure.py").read_bytes()).hexdigest()
    assert data["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/INVERSE_TRACE_QUADRATIC_CLOSURE.md").read_bytes()).hexdigest()
    for row in data["dense_coupled_controls"]:
        check = verify_moments(row["bits"], row["points"], row["checks"], row["targets"],
                               int(row["means_hex"], 16), [int(x, 16) for x in row["moment_rows_hex"]], row["local_lifts"])
        assert check["valid"]
        assert row["native_witness"] == all(reciprocal_trace(row["bits"], x) == b
                                             for x, b in zip(row["projected_x"], row["targets"]))
        assert not row["native_witness"]
        modulus = sum(int(c) << j for j, c in enumerate(field(row["bits"]).modulus().coeffs()))
        assert all(local["field_modulus"] == modulus for local in row["local_lifts"])
    for local in data["large_field_local_lifts_only"]:
        bits, mean, moments = local["bits"], 0, [0]*(2*local["bits"])
        assert len(local["selected_graph_points"]) % 2 == 1
        for x, y in local["selected_graph_points"]:
            assert x != 0 and encoded(element(bits, x)*element(bits, y)) == 1
            assert int(element(bits, y).trace()) == local["target"]
            word = x | (y << bits)
            mean ^= word
            for j in range(2*bits):
                if (word >> j) & 1:
                    moments[j] ^= word
        assert mean == local["projected_pair"][0] | (local["projected_pair"][1] << bits)
        assert moments == local["moment_rows"]

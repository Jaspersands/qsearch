from __future__ import annotations

import json
import math
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from tools.dqi_screen import prange as P
from tools.dqi_screen import rules as R
from tools.dqi_screen import screen as S

REPO = Path(__file__).resolve().parents[2]
EXAMPLES = REPO / "tools/dqi_screen/examples"


def test_objective_and_threshold_hand_values() -> None:
    a = 39 / 127
    assert R.q_prange(a, 0.5) == pytest.approx(0.654, abs=5e-4)
    assert R.q_dqi(19 / 127, 0.5) == pytest.approx(0.857, abs=5e-4)
    assert R.q_dqi(0.9, 0.5) == 1.0
    assert R.lambda_crit(a, 0.5) == pytest.approx(0.024, abs=5e-4)
    assert R.lambda_crit(0.5, 0.5) == pytest.approx(0.067, abs=5e-4)
    assert R.rho_crit(0.5) == pytest.approx(0.092, abs=5e-4)
    assert R.lambda_crit(0.5, R.rho_crit(0.5)) == pytest.approx(0.25)  # rho_crit: lambda_crit meets alpha/2
    for bad in ((0.0, 0.5), (0.3, 1.0), (1.2, 0.5)):
        with pytest.raises(ValueError):
            R.q_prange(*bad)


A = 39 / 127


def test_reach_bounds_caps_and_cosine() -> None:
    a = A
    assert R.licensed_radius(40) == 19
    assert R.singleton_reach(a) == pytest.approx(0.154, abs=5e-4)
    assert R.distance_reach(40 / 127) == pytest.approx(20 / 127)
    assert R.sphere_packing_reach(a, 2**61 - 1) == pytest.approx(0.293, abs=5e-4)
    assert R.q_ary_entropy(R.q_ary_entropy_inverse(0.3, 7), 7) == pytest.approx(0.3, abs=1e-9)
    assert R.plotkin_reach(0.5, 2) == pytest.approx(0.125)
    assert R.margin_cap(a) == pytest.approx(0.207, abs=5e-4)
    assert R.margin_cap(0.5) == pytest.approx(0.183, abs=5e-4)
    assert R.margin_cap(1 - 1 / 2**0.5) == pytest.approx(R.UNIVERSAL_CAP, abs=1e-9)
    # Proposition 13(ii) of arXiv:2610.06753: sqrt(2 lam(1-lam)), not 2 sqrt(lam(1-lam)) (the plan's 0.367).
    assert R.cosine_objective(209 / 6000) == pytest.approx(0.259, abs=5e-4)
    assert R.lambda_crit_cos(0.07) == pytest.approx(0.00246, abs=5e-6)
    assert R.lambda_crit_cos(0.8) is None
    for alpha in (0.01, 0.07, 0.3, 0.7):  # the value meets Prange's alpha exactly at the threshold
        assert R.cosine_objective(R.lambda_crit_cos(alpha)) == pytest.approx(alpha, rel=1e-9)
    assert R.cosine_objective(0.5) == R.cosine_objective(0.8) == pytest.approx(2**-0.5)  # max over t <= lam


def test_restarts_and_subfield_hand_values() -> None:
    a = A
    assert R.restart_length(a, 0.816830 - R.q_prange(a, 0.5), 1) == pytest.approx(399.2, abs=0.1)
    # The paper's Table 3: MPI at m = 6000, alpha = 0.07, finite DQI 0.2518, cosine range R = 2 -> 1729.
    assert R.restart_length(0.07, 0.2518 - 0.07, 2) == pytest.approx(1729, abs=0.5)
    assert R.existential_line(0.5, 0.5, 2**61 - 1) == 1.0
    assert R.existential_line(0.2, 0.5, 7) == pytest.approx(0.909, abs=5e-4)
    assert R.subfield_rate(0.3, 2, 1) == pytest.approx(0.6)
    assert R.subfield_baseline(0.5, 0.6, 100) == pytest.approx(0.8)
    assert R.subfield_blocks_at_half(0.5, 2, 1) is True and R.subfield_blocks_at_half(0.3, 2, 1) is False


def _run(example: str, **changes) -> tuple[S.Screen, dict[str, S.Check]]:
    cand = S.load_candidate(EXAMPLES / example)
    result = S.screen(replace(cand, **changes))
    return result, {check.rule: check for check in result.checks}


def test_example_a_radius_19_numbers() -> None:
    s, checks = _run("opi_prime_character_r19.json")
    qn = s.quantities
    assert qn["q_prange"] == pytest.approx(0.654, abs=5e-4)
    assert qn["lambda_crit"] == pytest.approx(0.024, abs=5e-4)
    assert qn["radius_crit"] == pytest.approx(3.07, abs=5e-3)
    assert qn["licensed_radius"] == 19
    assert qn["kappa"] == pytest.approx(0.207, abs=5e-4)
    assert qn["q_cap"] == pytest.approx(0.861, abs=5e-4)
    assert qn["restart_length"] == pytest.approx(399.2, abs=0.1)
    assert checks["R1"].passed is True
    assert checks["reach"].passed is True
    assert checks["witness"].passed is False and "0.01" in checks["witness"].detail
    assert s.verdict == "unknown"
    assert list(qn) == [
        "alpha", "lam", "delta", "q_prange", "q_dqi", "q_dqi_finite", "margin", "margin_finite", "lambda_crit",
        "radius_crit", "licensed_radius", "singleton_radius", "plotkin_radius", "hamming_radius",
        "signed_packing_radius", "singleton_reach", "distance_reach",
        "sphere_packing_reach", "plotkin_reach", "signed_packing_reach", "kappa", "q_cap", "cosine_objective",
        "lambda_crit_cos", "restart_length",
        "existential_line", "rho_crit", "alpha_sub", "subfield_baseline",
    ]
    assert list(checks) == ["R1", "reach", "R2", "R3", "R3-encoder", "R4", "cap", "witness", "restarts"]


def test_example_a_radius_32_is_outside_licensed_reach() -> None:
    s, checks = _run("opi_prime_character_r32.json")
    assert checks["reach"].passed is False
    assert "outside licensed Hamming reach" in checks["reach"].detail
    assert s.verdict == "not viable"


def test_finite_reach_bounds_hand_values() -> None:
    assert R.plotkin_distance(15, 11, 2) == 8  # simplex [15, 4, 8] meets the finite Plotkin bound
    assert R.plotkin_distance(16, 11, 2) == 8  # RM(1, 4) [16, 5, 8]
    assert R.plotkin_distance(1000, 900, 2) == 500
    assert R.plotkin_distance(127, 39, 2**61 - 1) == 126  # m (1 - 1/q), rounded down
    assert R.plotkin_distance(3, 1, 7) == 2  # [3, 2] over F_7: 3 * 6 * 7 / 48 = 2.625
    assert R.packing_radius(23, 11, 2, 1) == 3  # the perfect Golay [23, 12, 7]: its radius-3 ball is 2^11 exactly


def _ball_radius(m: int, n: int, q: int, letters: int) -> int:
    """The largest l with sum_{i <= l} C(m, i) letters^i <= q^n, by exact integers."""
    total, cap, term = 0, q**n, 1  # term = C(m, radius) letters^radius
    for radius in range(m + 1):
        total += term
        if total > cap:
            return radius - 1
        term = term * (m - radius) * letters // (radius + 1)
    return m


def test_packing_radius_counts_the_whole_ball_not_one_weight() -> None:
    # Every pattern of weight <= l needs its own syndrome: the ball, not the patterns of weight exactly l.
    assert R.packing_radius(24, 11, 2, 1) == 2  # 1 + 24 + 276 + 2024 = 2325 > 2^11: binary [24, 13] cannot reach 3
    assert R.packing_radius(15, 11, 2, 1) == 4 and R.packing_radius(10, 1, 2, 1) == 0
    assert R.packing_radius(2000, 779, 3, 2) == 224
    assert R.packing_radius(1000, 681, 5, 2) == 644  # one weight alone would allow every radius
    assert R.packing_radius(20, 19, 3, 2) == 11
    assert R.packing_radius(6000, 420, 8191, 2) == 1178  # MPI: the README's signed packing radius
    assert R.packing_radius(1000, 680, 2**61 - 1, 2) == 1000  # 3^1000 < q^680: every pattern fits
    for q in (2, 3, 4, 5, 7):
        for m in range(1, 31):
            for n in range(m + 1):
                for letters in sorted({q - 1, 2}):
                    assert R.packing_radius(m, n, q, letters) == _ball_radius(m, n, q, letters), (m, n, q, letters)


@pytest.mark.parametrize("m, n, q, letters", [
    (1000, 600, 2**61 - 1, 2**61 - 2),  # count over a huge field: the ball is its last term
    (30000, 779, 2**61 - 1, 2),  # signed patterns: the radius sits just below the mode, 20000
    (20677, 14114, 5, 2),  # q^n tops the half of 3^m up to the mode: the radius is past the mode
    (60000, 40000, 2, 1),  # binary, far below the mode
])
def test_packing_radius_beyond_exact_integers_matches_the_ball(m: int, n: int, q: int, letters: int) -> None:
    assert n * math.log2(q) > R._EXACT_BITS  # the floating-point ball
    assert R.packing_radius(m, n, q, letters) == _ball_radius(m, n, q, letters)


def test_floating_point_ball_matches_exact_integers() -> None:
    for q in (2, 3, 5, 7):
        for m in range(1, 31):
            for n in range(m + 1):
                for letters in sorted({q - 1, 2}):
                    assert R._packing_radius_float(m, n, q, letters) == _ball_radius(m, n, q, letters), (m, n, q)


def test_reach_fails_one_past_the_ball_radius() -> None:
    # sum_{i <= 225} C(2000, i) 2^i > 3^779: radius 225 is impossible for a ternary [2000, 1221] code.
    third = {"q": 3, "m": 2000, "n": 779, "rho": 1 / 3, "min_distance": None}
    s, checks = _run("hermite_half_rate.json", **third, radius=225)
    assert s.quantities["hamming_radius"] == 224
    assert checks["reach"].passed is False and "sphere-packing 224" in checks["reach"].detail
    assert s.verdict == "not viable"
    assert _run("hermite_half_rate.json", **third, radius=224)[1]["reach"].passed is True
    s, checks = _run("hermite_half_rate.json", q=2, m=24, n=11, radius=3, min_distance=None)  # binary [24, 13]
    assert checks["reach"].passed is False and "sphere-packing 2" in checks["reach"].detail
    # The cosine: radius 1178 is the largest whose signed ball fits 8191^420 (MPI).
    s, checks = _run("mpi_signed_cosine.json", radius=1178)
    assert s.quantities["signed_packing_radius"] == 1178 and checks["reach"].passed is True
    s, checks = _run("mpi_signed_cosine.json", radius=1179)
    assert checks["reach"].passed is False and "signed packing radius 1178" in checks["reach"].detail
    assert s.verdict == "not viable"


@pytest.mark.parametrize("m, n", [(15, 11), (16, 11), (24, 12)])  # simplex, RM(1, 4), extended Golay; d = 8
def test_licensed_radii_of_real_codes_pass_reach(m: int, n: int) -> None:
    # Corollary 7's Plotkin and sphere-packing forms are asymptotic: these codes beat them at l = 3 = (d - 2) // 2.
    s, checks = _run("hermite_half_rate.json", q=2, m=m, n=n, radius=3, min_distance=8)
    assert checks["reach"].passed is True, checks["reach"].detail
    assert s.verdict != "not viable", s.reasons


def test_reach_uses_finite_singleton_plotkin_and_packing_radii() -> None:
    # Without d, radius n/2 still cannot be licensed: d <= n + 1 gives l <= (n - 1) // 2.
    s, checks = _run("hermite_half_rate.json", q=2**61 - 1, m=128, n=40, radius=20, min_distance=None)
    assert s.quantities["singleton_radius"] == 19
    assert checks["reach"].passed is False and "Singleton 19" in checks["reach"].detail
    assert _run("hermite_half_rate.json", q=2**61 - 1, m=128, n=40, radius=19, min_distance=None)[1]["reach"].passed
    # Binary [1000, 100]: no such code has d > 500 (Plotkin), though sphere packing and Singleton allow l = 300.
    s, checks = _run("hermite_half_rate.json", q=2, n=900, radius=300, min_distance=None)
    assert (s.quantities["plotkin_radius"], s.quantities["singleton_radius"], s.quantities["hamming_radius"]) == \
        (249, 449, 319)
    assert checks["reach"].passed is False and "Plotkin 249" in checks["reach"].detail
    # Binary [1000, 500] at l = 200: C(1000, 200) > 2^500, though Singleton and Plotkin allow 249.
    s, checks = _run("hermite_half_rate.json", q=2, radius=200, min_distance=None)
    assert s.quantities["hamming_radius"] == 111 and s.quantities["plotkin_radius"] == 249
    assert checks["reach"].passed is False and "sphere-packing" in checks["reach"].detail


def test_example_b_cosine_is_viable() -> None:
    s, checks = _run("mpi_signed_cosine.json")
    assert s.quantities["lambda_crit_cos"] == pytest.approx(0.00246, abs=5e-6)
    assert s.quantities["cosine_objective"] == pytest.approx(0.259, abs=5e-4)
    assert s.quantities["restart_length"] == pytest.approx(1594.5, abs=0.1)
    assert checks["R1"].passed is True
    assert s.verdict == "viable", s.reasons
    s, checks = _run("mpi_signed_cosine.json", decoder_known=False)
    assert checks["reach"].passed is None and s.verdict == "unknown"


def test_signed_packing_reach_hand_values() -> None:
    # Proposition 13(i) and Table 3 of arXiv:2610.06753: "Signed-pattern packing bound permits reach 0.196" for MPI.
    assert R.signed_packing_reach(0.07, 8191) == pytest.approx(0.196, abs=5e-4)
    assert R.signed_packing_reach(0.68, 2**61 - 1) == 0.5  # alpha log2 q >= 3/2: every lam <= 1/2 fits
    lam = R.signed_packing_reach(0.3, 5)
    assert (R.binary_entropy(lam) + lam) / R.math.log2(5) == pytest.approx(0.3, abs=1e-9)
    # Finite length: sum_{i <= l} C(m, i) 2^i <= q^n, the patterns of weight <= l need distinct syndromes.
    assert R.packing_radius(6000, 420, 8191, 2) == 1178


def test_cosine_reach_uses_signed_packing_not_hamming_bounds() -> None:
    # Proposition 13: the Hamming-based Singleton, sphere-packing, Plotkin and distance bounds do not
    # limit a decoder licensed for {+-1} patterns.
    s, checks = _run("mpi_signed_cosine.json", radius=300)  # lam = 0.05 > alpha/2 = 0.035
    assert checks["reach"].passed is True and "signed" in checks["reach"].detail
    assert s.verdict != "not viable", s.reasons
    for d in (2, 300):  # a Hamming licence below the radius is not an upper bound on signed reach
        s, checks = _run("mpi_signed_cosine.json", min_distance=d)
        assert checks["reach"].passed is True and s.verdict != "not viable", (d, s.reasons)
    s, checks = _run("mpi_signed_cosine.json", min_distance=420)
    assert "(d - 2) // 2 = 209" in checks["reach"].detail  # radius 209 inside the Hamming licence
    s, checks = _run("mpi_signed_cosine.json", q=2**61 - 1, m=1000, n=680, radius=400)
    assert s.quantities["signed_packing_reach"] == 0.5
    assert checks["R1"].passed is True and "signed packing" in checks["R1"].detail
    s, checks = _run("mpi_signed_cosine.json", radius=1500)  # C(6000, 1500) 2^1500 > 8191^420
    assert checks["reach"].passed is False and "signed packing radius" in checks["reach"].detail
    assert s.verdict == "not viable"
    assert "signed" in S.render(s).splitlines()[-1]


def test_cosine_existential_line() -> None:
    # Proposition 13(iii) and Table 3 of arXiv:2610.06753: Q* ~= 0.726 for MPI (alpha = 0.07, q = 8191).
    assert R.cosine_existential_line(0.07, 8191) == pytest.approx(0.726, abs=5e-4)
    # Exact sum over F_q up to 2^16, the von Mises limit beyond: the two agree across the switch.
    for alpha in (0.01, 0.07, 0.3):
        assert R.cosine_existential_line(alpha, 65521) == pytest.approx(R.cosine_existential_line(alpha, 65537), abs=1e-4)
    values = [R.cosine_existential_line(a, 2**61 - 1) for a in (0.001, 0.01, 0.05, 0.1)]
    assert values == sorted(set(values)) and 0 < values[0] and values[-1] < 1
    assert R.cosine_existential_line(0.9, 2**61 - 1) == pytest.approx(1)  # 1 - O(q^(-2 alpha)) rounds to 1
    s, checks = _run("mpi_signed_cosine.json")
    assert s.quantities["existential_line"] == pytest.approx(0.726, abs=5e-4)
    assert checks["R3"].passed is True and s.verdict == "viable"
    for finite in (0.80, 0.99):  # above Q*: no assignment of a typical instance is that good
        s, checks = _run("mpi_signed_cosine.json", finite_dqi_mean=finite)
        assert checks["R3"].passed is False and s.verdict == "unknown"


def test_cosine_r2_passes_exactly_when_the_margin_is_positive() -> None:
    for n in (6, 70, 420, 2000, 4000):
        for radius in (0, 1, 5, 10, 15, 30, 100, 209, 1000, 2999, 3000, 3500):
            s, checks = _run("mpi_signed_cosine.json", n=n, radius=radius)
            if s.quantities["lambda_crit_cos"] is None:
                continue
            assert checks["R2"].passed is (s.quantities["margin"] > 0), (n, radius, s.quantities["margin"])
    # The restart rule uses the same value: at m = 1000, l = 34 the length is 1646.4 > m.
    s, checks = _run("mpi_signed_cosine.json", m=1000, n=70, radius=34)
    assert s.quantities["restart_length"] == pytest.approx(1646.4, abs=0.1)
    assert checks["restarts"].passed is False and s.verdict == "unknown"


def test_example_c_half_rate() -> None:
    s, checks = _run("hermite_half_rate.json")
    assert s.quantities["lambda_crit"] == pytest.approx(0.067, abs=5e-4)
    assert s.quantities["singleton_reach"] == 0.25
    assert s.quantities["kappa"] == pytest.approx(0.183, abs=5e-4)
    assert checks["R4"].passed is None and "prime field" in checks["R4"].detail
    assert checks["restarts"].passed is False and s.verdict == "unknown"  # restarts need m >= 1212.7


def test_witness_is_compared_with_the_claimed_dqi_value() -> None:
    longer = {"m": 2000, "radius": 248, "min_distance": 500}  # Q_DQI 0.8296, q_cap - 0.01 = 0.923
    s, checks = _run("hermite_half_rate.json", **longer, classical_witness=0.90)
    assert checks["witness"].passed is False and "Q_DQI" in checks["witness"].detail
    assert s.verdict == "unknown"
    s, checks = _run("hermite_half_rate.json", **longer, classical_witness=0.80)
    assert checks["witness"].passed is True and s.verdict == "viable"
    s, checks = _run("hermite_half_rate.json", **longer, classical_witness=0.80, finite_dqi_mean=0.79)
    assert checks["witness"].passed is False and "finite DQI mean" in checks["witness"].detail
    # The cosine has no cap, but its witness still has to stay below DQI's value 0.259.
    for witness, finite, passed in ((0.30, None, False), (1.0, None, False), (0.20, None, True), (0.20, 0.19, False)):
        s, checks = _run("mpi_signed_cosine.json", classical_witness=witness, finite_dqi_mean=finite)
        assert checks["witness"].passed is passed, (witness, finite, checks["witness"].detail)
        assert s.verdict == ("viable" if passed else "unknown")
    s, checks = _run("mpi_signed_cosine.json", classical_witness=0.20, radius=None)
    assert checks["witness"].passed is None and "give radius or finite_dqi_mean" in checks["witness"].detail


def test_encoder_known_caps_margin_at_zero() -> None:
    s, checks = _run("mpi_signed_cosine.json", encoder_known=True)
    assert checks["R3-encoder"].passed is False
    assert s.verdict == "not viable"


def test_encoder_known_is_documented_as_a_polynomial_time_encoder_attaining_q_star(capsys) -> None:
    # Proposition 9 (R3): a polynomial-time encoder for im(B) attaining Q*, not "the planted encoder".
    s, checks = _run("mpi_signed_cosine.json", encoder_known=True)
    assert "polynomial-time encoder" in checks["R3-encoder"].detail and "Q*" in checks["R3-encoder"].detail
    assert "polynomial-time encoder" in _run("mpi_signed_cosine.json")[1]["R3-encoder"].detail
    with pytest.raises(SystemExit):
        S.main(["--help"])
    help_text = " ".join(capsys.readouterr().out.split())
    assert "planted encoder is known" not in help_text and "polynomial-time encoder" in help_text and "Q*" in help_text
    readme = (REPO / "tools/dqi_screen/README.md").read_text(encoding="utf-8")
    row = next(line for line in readme.splitlines() if line.startswith("| `encoder_known`"))
    assert "planted encoder is known" not in row and "polynomial-time" in row and "Q*" in row


def test_r3_encoder_pass_says_the_rule_stays_unresolved() -> None:
    # arXiv:2610.06753: without a known encoder attaining Q*, (R3) "stays unresolved" (Table 3: MPI unresolved).
    s, checks = _run("mpi_signed_cosine.json")
    encoder = checks["R3-encoder"]
    assert encoder.passed is True and s.verdict == "viable"  # not violated: the verdict logic is unchanged
    assert encoder.detail.startswith("not violated (unresolved: ") and "Proposition 9" in encoder.detail
    readme = (REPO / "tools/dqi_screen/README.md").read_text(encoding="utf-8")
    viable = readme.split("- **viable**", 1)[1].split("\n\n", 1)[0]  # the verdict's bullet
    assert "(R3)" in viable and "unresolved" in viable
    row = next(line for line in readme.splitlines() if line.startswith("| R3-encoder | hard"))
    assert "unresolved" in row
    source = (REPO / "tools/corpus/mcp_server.py").read_text(encoding="utf-8")
    assert "unresolved" in source.split("def screen_dqi_candidate", 1)[1].split('"""')[1]  # the tool's docstring


def test_prime_power_q_without_subfield_inputs_is_unknown_not_na() -> None:
    # Example (c) at twice the length is viable over the prime field F_8191.
    longer = {"m": 2000, "radius": 248, "min_distance": 500}
    assert _run("hermite_half_rate.json", **longer)[0].verdict == "viable"
    s, checks = _run("hermite_half_rate.json", q=4096, **longer)
    assert checks["R4"].passed is None and "give p, b, c" in checks["R4"].detail
    assert s.verdict == "unknown"
    s, checks = _run("hermite_half_rate.json", q=4096, p=2, b=12, c=1, **longer)
    assert checks["R4"].passed is False and s.quantities["subfield_baseline"] == 1.0
    assert s.verdict == "not viable"


def test_subfield_inputs_must_match_q() -> None:
    longer = {"m": 2000, "radius": 248, "min_distance": 500, "q": 4096}
    for p, b, c in ((2, 1, 12), (3, 2, 1), (4, 6, 1), (2, 12, 13), (2, 12, 0), (2, 6, 3)):
        with pytest.raises(ValueError, match="q = 4096"):
            _run("hermite_half_rate.json", p=p, b=b, c=c, **longer)
    # c is an F_p-affine codimension (Proposition 9, R4): any 1 <= c <= b, not only a divisor of b.
    for p, b, c in ((2, 12, 1), (2, 12, 4), (2, 12, 5), (2, 12, 12)):
        assert _run("hermite_half_rate.json", p=p, b=b, c=c, **longer)[1]["R4"].passed is not None
    for q, b, c in ((32, 5, 3), (8, 3, 2)):  # the paper's A.6 example: a half-density set in F_32, c <= 3
        s, checks = _run("hermite_half_rate.json", p=2, b=b, c=c, n=1000, **{**longer, "q": q})  # alpha = 1/2
        assert s.quantities["alpha_sub"] == pytest.approx(min(1, b * 0.5 / c))
        assert checks["R4"].passed is False  # Q_DQI 0.83 <= the subfield baseline 0.92 or 0.875
    # Rounding c = 3 up to the only divisor c = 5 would understate the subfield baseline and pass R4.
    assert _run("hermite_half_rate.json", p=2, b=5, c=5, n=1000, **{**longer, "q": 32})[1]["R4"].passed is True
    with pytest.raises(ValueError, match="p = 3"):
        _run("hermite_half_rate.json", p=3, **longer)  # checked even when b and c are absent
    assert _run("hermite_half_rate.json", p=8191, b=1, c=1)[1]["R4"].detail == "not applicable (prime field)"


def test_subfield_codimension_must_fit_the_density() -> None:
    # Appendix A.6: a set of density rho contains a codimension-c coset only if p^(b-c) <= rho p^b.
    sparse = {"q": 4096, "m": 2000, "n": 200, "rho": 0.1, "radius": 90, "min_distance": None, "p": 2, "b": 12}
    for c in (1, 2, 3):
        with pytest.raises(ValueError, match=r"log_p\(1/rho\)"):
            _run("hermite_half_rate.json", c=c, **sparse)
    assert _run("hermite_half_rate.json", c=4, **sparse)[1]["R4"].passed is not None
    assert _run("hermite_half_rate.json", q=4096, p=2, b=12, c=1, m=2000, radius=248, min_distance=500)[0].verdict \
        == "not viable"  # rho = 1/2 = 2^-1 fits exactly


# Each rule's decisive branch, one candidate apiece (a mutant that always passes or never passes a
# rule, or drops one bound, fails at least one of these).
LONGER = {"m": 2000, "radius": 248, "min_distance": 500}  # hermite_half_rate at twice the length: viable


def test_r1_fails_on_each_asymptotic_reach_bound_alone() -> None:
    no_radius = {"radius": None, "min_distance": None}
    cases = (
        ("Plotkin", {"q": 2, "n": 900, **no_radius}),  # Plotkin 0.225 <= 0.282 < H_2^-1(0.9) = 0.316
        ("distance", {"min_distance": 100, "radius": None}),  # delta/2 = 0.05 <= 0.067 < 0.25
    )
    for bound, changes in cases:
        s, checks = _run("hermite_half_rate.json", **changes)
        r1 = checks["R1"]
        assert r1.passed is False and r1.detail.startswith(f"reach bound {bound} "), (bound, r1.detail)
        assert s.verdict == "not viable"
    assert _run("hermite_half_rate.json", radius=None)[1]["R1"].passed is True
    # Sphere packing binds alone only at a density no field has (q = 2, rho = 0.1: H_2^-1(0.1) = 0.013 <= 0.0166
    # < Plotkin; no k/q with q <= 32 does it), so the screen rejects the input, but R1 itself names the bound.
    cand = replace(S.load_candidate(EXAMPLES / "hermite_half_rate.json"), q=2, n=100, rho=0.1, **no_radius)
    with pytest.raises(ValueError, match="rho"):
        S.screen(cand)
    r1 = S._check_r1(cand, S._quantities(cand))
    assert r1.passed is False and r1.detail.startswith("reach bound sphere-packing "), r1.detail


def test_cosine_without_a_threshold_is_not_viable_even_without_a_radius() -> None:
    for radius in (None, 400):  # alpha = 0.71 >= 1/sqrt(2)
        s, checks = _run("mpi_signed_cosine.json", m=1000, n=710, radius=radius)
        assert checks["R1"].passed is False and "1/sqrt(2)" in checks["R1"].detail
        assert s.verdict == "not viable"
    assert _run("mpi_signed_cosine.json", m=1000, n=710, radius=400)[1]["R2"].passed is False


def test_reach_fails_just_past_the_licensed_radius_alone() -> None:
    s, checks = _run("hermite_half_rate.json", radius=125)  # (250 - 2) // 2 = 124; every other bound allows 249
    assert checks["reach"].passed is False and "licensed radius 124" in checks["reach"].detail
    assert "finite-length radius bound" not in checks["reach"].detail and s.verdict == "not viable"


def test_r3_cap_and_restarts_fail_paths() -> None:
    small = {"q": 7, "m": 2000, "n": 400, "rho": 3 / 7, "radius": 100, "min_distance": None}  # Q* = 0.854, Q_DQI 0.651
    s, checks = _run("hermite_half_rate.json", **small)
    assert checks["R3"].passed is True and s.verdict == "viable", s.reasons
    s, checks = _run("hermite_half_rate.json", **small, finite_dqi_mean=0.95)
    assert checks["R3"].passed is False and "existential line" in checks["R3"].detail and s.verdict == "unknown"
    s, checks = _run("hermite_half_rate.json", **LONGER)
    assert checks["cap"].passed is True and checks["restarts"].passed is True and s.verdict == "viable"
    assert _run("hermite_half_rate.json", radius=300)[1]["cap"].passed is False  # lam = 0.3 > alpha/2
    s, checks = _run("hermite_half_rate.json", **LONGER, finite_dqi_mean=0.6)  # below Q_Pr = 0.625
    assert checks["restarts"].passed is False and "no length" in checks["restarts"].detail
    assert s.verdict == "unknown"


def test_r4_passes_and_blocks_at_half() -> None:
    subfield = {**LONGER, "q": 4096, "p": 2, "b": 12}
    s, checks = _run("hermite_half_rate.json", **subfield, c=12)  # alpha_sub = 0.25: baseline 0.625 < 0.83
    assert checks["R4"].passed is True and s.verdict == "viable", s.reasons
    # c = 4: alpha = 0.25 >= 2c^2/(b^2+c^2) = 0.2 blocks every licensed radius, even when a finite
    # mean 0.9 tops the baseline 0.875.
    s, checks = _run("hermite_half_rate.json", **subfield, c=4, finite_dqi_mean=0.9)
    assert s.quantities["subfield_baseline"] == pytest.approx(0.875)
    assert checks["R4"].passed is False and "blocks every licensed radius" in checks["R4"].detail
    assert R.subfield_baseline(0.5, 1 / 3, 10) == pytest.approx(0.65)  # floor(10/3) = 3 rows, not 3.33


def test_r4_fails_without_a_radius_when_no_radius_can_pass() -> None:
    no_radius = {"q": 4096, "p": 2, "b": 12, "m": 2000, "radius": None}
    # alpha = 1/2 >= 2c^2/(b^2+c^2) at rho = 1/2: Proposition 9 blocks every licensed radius.
    s, checks = _run("hermite_half_rate.json", **no_radius, c=1)
    assert checks["R4"].passed is False and "blocks every licensed radius" in checks["R4"].detail
    assert s.verdict == "not viable"
    # rho = 1/4: the subfield baseline is 1 (alpha_sub = 1), which no claimed value can beat.
    s, checks = _run("hermite_half_rate.json", **no_radius, c=2, rho=0.25)
    assert s.quantities["subfield_baseline"] == 1.0 and checks["R4"].passed is False
    assert "subfield baseline 1" in checks["R4"].detail and s.verdict == "not viable"
    s, checks = _run("hermite_half_rate.json", **no_radius, c=12)  # baseline 0.625: the radius decides
    assert checks["R4"].passed is None and "give radius or finite_dqi_mean" in checks["R4"].detail


def test_saturated_reach_is_flagged_not_viable() -> None:
    s, checks = _run("hermite_half_rate.json", radius=600)  # lam = 0.6 > 1 - rho
    assert s.quantities["q_dqi"] == 1.0
    assert s.verdict == "not viable"
    assert any("saturated" in check.detail for check in checks.values())
    assert checks["reach"].passed is False and "saturated" in checks["reach"].detail


def test_saturation_alone_fails_reach_inside_every_reach_bound() -> None:
    # alpha = 0.9: lam = 0.35 is below Singleton 0.45 and every other bound, but above 1 - rho = 0.3.
    s, checks = _run("hermite_half_rate.json", n=900, rho=0.7, radius=350, min_distance=None)
    assert s.quantities["q_dqi"] == 1.0
    assert all(s.quantities["lam"] <= bound for bound in (s.quantities["singleton_reach"], s.quantities["plotkin_reach"],
                                                           s.quantities["sphere_packing_reach"]))
    assert checks["R1"].passed is True and checks["R2"].passed is True
    reach = checks["reach"]
    assert reach.passed is False and "saturated" in reach.detail
    assert "outside licensed Hamming reach" not in reach.detail and "exceeds the reach bound" not in reach.detail
    assert s.verdict == "not viable"
    s, checks = _run("hermite_half_rate.json", n=900, rho=0.7, radius=290, min_distance=None)  # lam = 0.29 <= 0.3
    assert checks["reach"].passed is True


@pytest.mark.parametrize("rho", [0.6, 0.7, 0.75, 0.8, 0.9])
def test_saturation_starts_strictly_past_one_minus_rho(rho: float) -> None:
    # 1 - 0.9 rounds to 0.09999999999999998: radius (1 - rho) m itself is not saturated.
    edge = round((1 - rho) * 1000)
    s, checks = _run("hermite_half_rate.json", q=101, n=900, rho=rho, radius=edge, min_distance=None)
    assert checks["reach"].passed is True and s.quantities["q_dqi"] == pytest.approx(1.0)
    s, checks = _run("hermite_half_rate.json", q=101, n=900, rho=rho, radius=edge + 1, min_distance=None)
    detail = checks["reach"].detail
    assert checks["reach"].passed is False and "saturated" in detail
    # Eq. (1) does give Q_DQI = 1 there; the detail says so and names the radius to screen instead.
    assert "says nothing" not in detail and "Q_DQI = 1" in detail and f"radius {edge} " in detail


def test_candidate_from_dict_rejects_unknown_keys_and_objectives() -> None:
    base = {"name": "x", "objective": "count", "q": 7, "m": 100, "n": 30, "rho": 3 / 7}
    assert S.candidate_from_dict(base).q == 7
    for bad in ({**base, "radiuss": 3}, {**base, "objective": "max"}, {"objective": "count"}, {**base, "q": 12}):
        with pytest.raises(ValueError):
            S.screen(S.candidate_from_dict(bad))
    for key in ("name", "objective", "q", "m", "n", "rho"):  # null required fields name the field
        with pytest.raises(ValueError, match=f"^{key} "):
            S.candidate_from_dict({**base, key: None})
    assert S.candidate_from_dict({**base, "q": 7.0}).q == 7
    with pytest.raises(ValueError, match="exact integer"):  # float(2^61 - 1) rounds to 2^61
        S.candidate_from_dict({**base, "q": float(2**61 - 1)})


def test_cosine_objective_needs_a_prime_above_three() -> None:
    # Proposition 13 assumes q > 3 prime: over F_2 cos(pi v) = +-1 has variance 1, over F_3 skewness 1/sqrt(2).
    base = {"name": "x", "objective": "cosine", "m": 1000, "n": 300, "rho": 0.5, "radius": 30, "decoder_known": True}
    for q in (2, 3, 4, 9, 4096):
        with pytest.raises(ValueError, match="prime q > 3"):
            S.screen(S.candidate_from_dict({**base, "q": q}))
    assert S.screen(S.candidate_from_dict({**base, "q": 5})).quantities["cosine_objective"] is not None
    assert S.main(["--objective", "cosine", "--q", "2", "--m", "1000", "--n", "300", "--rho", "0.5"]) == 2


def test_densities_and_distances_no_instance_can_have_are_bad_input() -> None:
    base = {"name": "x", "objective": "count", "q": 2, "m": 100, "n": 30, "rho": 0.5, "radius": 10,
            "decoder_known": True}
    # rho = |F_i| / q for a whole number 1 <= |F_i| <= q - 1, up to 1% rounding.
    for q, rho in ((2, 0.3), (7, 0.5), (7, 0.45), (2, 0.1), (3, 0.1), (7, 0.9999), (2**61 - 1, 1e-30)):
        with pytest.raises(ValueError, match=r"rho = .* \|F_i\|"):
            S.screen(S.candidate_from_dict({**base, "q": q, "rho": rho}))
    for q, rho in ((7, 3 / 7), (7, 0.4286), (3, 0.333), (101, 0.6), (8191, 0.5), (2**61 - 1, 0.5)):
        assert S.screen(S.candidate_from_dict({**base, "q": q, "rho": rho})).verdict
    cosine = {**base, "objective": "cosine", "q": 7, "rho": 0.5}  # the cosine objective ignores rho
    assert S.screen(S.candidate_from_dict(cosine)).quantities["q_prange"] is None
    # d <= n + 1 (Singleton) and d <= the finite Plotkin bound of the dual [m, m - n] code.
    for changes in ({"min_distance": 90}, {"min_distance": 32}, {"m": 15, "n": 11, "min_distance": 9, "radius": 3}):
        with pytest.raises(ValueError, match="min_distance"):
            S.screen(S.candidate_from_dict({**base, **changes}))
    for changes in ({"min_distance": 31}, {"m": 15, "n": 11, "min_distance": 8, "radius": 3}):
        assert S.screen(S.candidate_from_dict({**base, **changes})).verdict
    # The README's example uses a density the field has.
    readme = (REPO / "tools/dqi_screen/README.md").read_text(encoding="utf-8")
    assert "--q 7 --m 100 --n 30 --rho 0.5 " not in readme and "--rho 0.5 " not in S.__doc__
    assert S.main(["--objective", "count", "--q", "7", "--m", "100", "--n", "30", "--rho", "0.5"]) == 2


def test_docs_say_n_is_the_rank_of_b_and_the_cosine_ignores_rho() -> None:
    readme = (REPO / "tools/dqi_screen/README.md").read_text(encoding="utf-8")
    rows = {line.split("|")[1].strip(): line for line in readme.splitlines() if line.startswith("| `")}
    assert "rank(B)" in rows["`q`, `m`, `n`"] and "variables; alpha" not in rows["`q`, `m`, `n`"]
    assert "cosine objective ignores" in rows["`rho`"] and "Plotkin" in rows["`min_distance`"]
    source = (REPO / "tools/corpus/mcp_server.py").read_text(encoding="utf-8")
    doc = source.split("def screen_dqi_candidate", 1)[1].split('"""')[1]
    assert "rank(B)" in doc and "ignores" in doc


def test_claimed_values_must_be_finite_and_in_the_objective_range() -> None:
    base = {"name": "x", "objective": "count", "q": 7, "m": 100, "n": 30, "rho": 3 / 7, "radius": 5}
    for key in ("finite_dqi_mean", "classical_witness"):
        for value in (float("nan"), float("inf"), -0.1, 1.5):
            with pytest.raises(ValueError, match=key):
                S.screen(S.candidate_from_dict({**base, key: value}))
        assert S.screen(S.candidate_from_dict({**base, key: 0.0})).quantities is not None
        cosine = {**base, "objective": "cosine", key: -0.5}
        assert S.screen(S.candidate_from_dict(cosine)).quantities is not None
        with pytest.raises(ValueError, match=key):
            S.screen(S.candidate_from_dict({**cosine, key: -1.5}))


def test_cli_json_and_markdown(capsys, tmp_path) -> None:
    main = S.main
    assert main(["--params", str(EXAMPLES / "mpi_signed_cosine.json"), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["verdict"] == "viable" and payload["quantities"]["cosine_objective"] == pytest.approx(0.259, abs=5e-4)
    out = tmp_path / "s.md"
    assert main(["--params", str(EXAMPLES / "opi_prime_character_r32.json"), "--out", str(out)]) == 1
    assert "outside licensed Hamming reach" in out.read_text() and "# DQI screen: opi-prime-character-r32" in out.read_text()
    assert capsys.readouterr().out == f"not viable: {out}\n"
    assert main(["--objective", "count", "--q", "7", "--m", "100", "--n", "30", "--rho", "0.4286", "--radius", "5", "--min-distance", "20", "--decoder-known"]) == 0
    text = capsys.readouterr().out
    assert text.startswith("# DQI screen: candidate") and "| q_prange |" in text and "Verdict:" in text
    assert main(["--objective", "count", "--q", "12", "--m", "100", "--n", "30", "--rho", "0.5"]) == 2
    assert "prime power" in capsys.readouterr().err
    qnull = tmp_path / "qnull.json"
    qnull.write_text(json.dumps({"name": "x", "objective": "count", "q": None, "m": 100, "n": 30, "rho": 0.5}))
    assert main(["--params", str(qnull)]) == 2  # bad input, not "not viable"
    assert capsys.readouterr().err.startswith("error: q ")


def test_huge_inputs_are_bad_input_not_a_verdict(capsys, tmp_path) -> None:
    base = {"name": "x", "objective": "count", "q": 7, "m": 100, "n": 30, "rho": 3 / 7}
    for key in ("rho", "classical_witness", "finite_dqi_mean"):
        with pytest.raises(ValueError, match=key) as error:
            S.candidate_from_dict({**base, key: 10**400})
        assert len(str(error.value)) < 100  # names the field, does not echo 400 digits
    huge = {**base, "m": 10**400, "n": 10**400 // 2}
    with pytest.raises(ValueError, match="too large"):
        S.screen(S.candidate_from_dict(huge))  # the MCP tool turns this ValueError into {"error": ...}
    for data in (huge, {**base, "rho": 10**400}):
        path = tmp_path / "huge.json"
        path.write_text(json.dumps(data))
        assert S.main(["--params", str(path)]) == 2
        assert capsys.readouterr().err.startswith("error: ")


def _mcp_screen(root: Path, params: dict) -> dict:
    import anyio

    from tools.corpus.mcp_server import create_server

    server = create_server(root, dense="off")

    async def go():
        return await server.call_tool("screen_dqi_candidate", {"params": params})

    result = anyio.run(go)
    if isinstance(result, tuple):  # FastMCP: (content blocks, structured result)
        return result[1].get("result", result[1])
    return json.loads(result[0].text)


def test_degenerate_inputs_never_crash_into_exit_1(capsys, tmp_path, fake_repo) -> None:
    # Exit 1 means "not viable": a traceback must never look like a verdict, nor the MCP tool raise.
    import sympy

    big = int(sympy.nextprime(10**400))
    huge_field = {"name": "x", "objective": "count", "q": big, "m": 100, "n": 30, "rho": 0.5, "p": big, "b": 1, "c": 1}
    s = S.screen(S.candidate_from_dict(huge_field))  # p^-c is compared in log space: no float overflow
    assert s.verdict == "unknown" and s.checks[5].detail == "not applicable (prime field)"
    path = tmp_path / "x.json"
    path.write_text(json.dumps(huge_field))
    assert S.main(["--params", str(path)]) == 0
    assert _mcp_screen(fake_repo, huge_field)["verdict"] == "unknown"
    capsys.readouterr()
    cosine = {"name": "x", "objective": "cosine", "q": 8191, "m": 10**220, "n": 10, "rho": 0.5}
    for mean in (2e-200, 1e-160):  # mu^2 underflows to 0; the restart length overflows to inf
        data = {**cosine, "finite_dqi_mean": mean}
        with pytest.raises(ValueError, match="floating point"):
            S.screen(S.candidate_from_dict(data))
        path.write_text(json.dumps(data))
        assert S.main(["--params", str(path), "--json"]) == 2
        captured = capsys.readouterr()
        assert captured.err.startswith("error: ") and "Infinity" not in captured.out
        assert "floating point" in _mcp_screen(fake_repo, data)["error"]
    with pytest.raises(OverflowError):
        R.restart_length(0.5, 1e-160, 2)
    path.write_text("[" * 200000 + "]" * 200000)  # nested too deeply for the JSON decoder
    assert S.main(["--params", str(path)]) == 2
    assert capsys.readouterr().err.startswith("error: ")


def test_cli_write_errors_exit_2_not_1(capsys, tmp_path) -> None:
    args = ["--params", str(EXAMPLES / "hermite_half_rate.json"), "--out"]
    blocker = tmp_path / "file"
    blocker.write_text("x")
    for out in (tmp_path, blocker / "x.md"):  # a directory; a path under a regular file
        assert S.main([*args, str(out)]) == 2
        assert capsys.readouterr().err.startswith("error: ")


def test_cli_zero_valued_flags_override_the_params_file(capsys) -> None:
    main = S.main
    args = ["--params", str(EXAMPLES / "opi_prime_character_r19.json"), "--json"]
    assert main([*args, "--radius", "0", "--classical-witness", "0", "--finite-dqi-mean", "0"]) == 1
    candidate = json.loads(capsys.readouterr().out)["candidate"]
    assert (candidate["radius"], candidate["classical_witness"], candidate["finite_dqi_mean"]) == (0, 0.0, 0.0)
    assert candidate["decoder_known"] is True  # an absent boolean flag keeps the file's value
    flags = ["--objective", "count", "--q", "7", "--m", "100", "--n", "30", "--rho", "0.4286", "--min-distance", "20"]
    assert main([*flags, "--radius", "0", "--decoder-known"]) == 1  # lam = 0 cannot beat Prange
    assert "R2 (hard): FAIL" in capsys.readouterr().out


def test_readme_maps_each_check_to_the_papers_rules() -> None:
    # The screen's "R2" is Theorem 6's threshold; the paper's (R2) decoder rule lives in "reach".
    readme = (REPO / "tools/dqi_screen/README.md").read_text(encoding="utf-8")
    table = readme.split("| Screen check | Paper (arXiv:2610.06753) |", 1)[1].split("\n\n", 1)[0]
    rows = {line.split("|")[1].strip(): line.split("|")[2] for line in table.splitlines() if line.startswith("| ")}
    assert set(rows) == {"R1", "reach", "R2", "R3", "R3-encoder", "R4", "cap", "witness", "restarts"}
    assert "(R2) decoder" in rows["reach"] and "Theorem 6" in rows["R2"] and "(R3) encoder" in rows["R3-encoder"]


def test_baseline_catalog_says_where_the_best_of_n_score_comes_from() -> None:
    # screen.py computes the Prange line and the Theorem 10 length; only prange_restarts runs best-of-N.
    from tools.corpus.baselines import load_catalog

    entry = next(e for e in load_catalog() if e["id"] == "prange-restarts-opi")
    assert "computes both" not in entry["summary"]
    assert "prange_restarts" in entry["summary"] and "restart length" in entry["summary"]
    assert entry["runnable"]["entry"] == "tools/dqi_screen/prange.py:prange_restarts"


def test_corpus_mcp_docs_list_the_screen_tool() -> None:
    from tools.corpus import mcp_server

    tools = next(par for par in mcp_server.__doc__.split("\n\n") if par.startswith("Tools:"))
    assert "screen_dqi_candidate(params)" in tools
    readme = (REPO / "tools/corpus/README.md").read_text(encoding="utf-8")
    agents = readme.split("## For the research agents (MCP)", 1)[1].split("\n\n")[1]
    assert "`screen_dqi_candidate`" in agents


def test_prange_full_field_scores_one() -> None:
    B = np.random.default_rng(3).integers(0, 5, size=(6, 3))
    result = P.prange_restarts(B, [range(5)] * 6, 5, restarts=2, seed=0)
    assert result["best"] == 1.0
    assert (result["m"], result["n"], result["q"], result["restarts"], result["rank"]) == (6, 3, 5, 2, 3)
    B[:, 2] = 0  # rank 2 < n: Prange runs on the image of B, every row still accepted
    rank_deficient = P.prange_restarts(B, [range(5)] * 6, 5, restarts=2, seed=0)
    assert rank_deficient["best"] == 1.0 and rank_deficient["rank"] == 2
    with pytest.raises(ValueError):
        P.prange_restarts(B, [range(4)] * 6, 4)


def test_prange_rank_deficient_b_runs_on_its_image() -> None:
    # Duplicated columns (rank 1 of 2), and a 40 x 10 matrix with a repeated column: never the old 0.0.
    tiny = P.prange_restarts(np.array([[1, 2], [2, 4], [3, 6], [1, 2]]), [{0, 1}] * 4, 7, restarts=5, seed=0)
    assert tiny["rank"] == 1 and all(score >= 1 / 4 for score in tiny["scores"])
    B = np.random.default_rng(11).integers(0, 7, size=(40, 10))
    B[:, 9] = B[:, 0]
    result = P.prange_restarts(B, [{0, 1, 2}] * 40, 7, restarts=50, seed=0)
    assert result["rank"] == 9 and all(score >= 9 / 40 for score in result["scores"])  # the 9 chosen rows hold
    assert result["best"] > 0.5
    wide = P.prange_restarts(np.random.default_rng(2).integers(1, 5, size=(2, 3)), [{1}] * 2, 5, restarts=3, seed=0)
    assert wide["rank"] == 2 and wide["best"] == 1.0  # m < n: both rows are chosen and hold
    for empty in (np.zeros((0, 2), dtype=int), np.zeros((3, 0), dtype=int)):
        with pytest.raises(ValueError, match="at least one"):
            P.prange_restarts(empty, [{0}] * len(empty), 5)


def test_prange_more_restarts_never_lower_best() -> None:
    B = np.random.default_rng(5).integers(0, 7, size=(12, 4))
    accepted = [{0, 1, 2}] * 12
    three = P.prange_restarts(B, accepted, 7, restarts=3, seed=1)
    twelve = P.prange_restarts(B, accepted, 7, restarts=12, seed=1)
    assert three["best"] <= twelve["best"]
    assert twelve["scores"][:3] == three["scores"]
    assert all(score >= 4 / 12 for score in twelve["scores"])  # the n targeted rows always hold


def test_prange_reduces_range_accepted_sets_mod_q() -> None:
    one_row = np.array([[1], [1]])
    shifted = P.prange_restarts(one_row, [range(5, 7)] * 2, 5, restarts=3, seed=0)["scores"]
    assert shifted == P.prange_restarts(one_row, [{5, 6}] * 2, 5, restarts=3, seed=0)["scores"] == [1.0] * 3
    B = np.random.default_rng(5).integers(0, 7, size=(12, 4))
    for arc, residues in ((range(-1, 2), {6, 0, 1}), (range(5, 9), {5, 6, 0, 1}), (range(7), set(range(7)))):
        by_range = P.prange_restarts(B, [arc] * 12, 7, restarts=8, seed=2)["scores"]
        assert by_range == P.prange_restarts(B, [residues] * 12, 7, restarts=8, seed=2)["scores"], arc
        assert all(score >= 4 / 12 for score in by_range)  # the n targeted rows always hold
    with pytest.raises(ValueError, match="longer than q"):
        P.prange_restarts(B, [range(-1, 7)] * 12, 7)


def test_prange_rejects_non_integer_entries() -> None:
    B = np.ones((5, 1), dtype=int)
    for accepted in ([{0.5, 1}] * 5, [{2.9}] * 5, ["01"] * 5, [b"01"] * 5):
        with pytest.raises(ValueError, match="integer"):
            P.prange_restarts(B, accepted, 3)
    for entry in (1.7, "1"):
        bad = np.array([[entry], [1], [1], [1], [1]], dtype=object)
        with pytest.raises(ValueError, match="integer"):
            P.prange_restarts(bad, [{0, 1}] * 5, 3)
    ok = np.array([[np.int64(1)], [1], [2], [1], [1]], dtype=object)
    assert P.prange_restarts(ok, [{np.int64(0), 1}] * 5, 3)["rank"] == 1


def test_prange_large_prime_field() -> None:
    q = 2**61 - 1
    rng = np.random.default_rng(7)
    B = rng.integers(1, q, size=(4, 2))  # int64 entries; int64 products would overflow
    x = [int(v) for v in rng.integers(1, q, size=2)]
    targets = [(int(B[i, 0]) * x[0] + int(B[i, 1]) * x[1]) % q for i in range(4)]
    result = P.prange_restarts(B, [{t} for t in targets], q, restarts=3, seed=0)
    assert result["best"] == 1.0 and result["rank"] == 2

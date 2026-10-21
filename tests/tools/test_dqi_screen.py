from __future__ import annotations

import json
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
    assert R.packing_radius(23, 11, 2, 1) >= 3  # the perfect Golay [23, 12, 7] decodes 3 errors


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
    assert (s.quantities["plotkin_radius"], s.quantities["singleton_radius"]) == (249, 449)
    assert s.quantities["hamming_radius"] >= 300
    assert checks["reach"].passed is False and "Plotkin 249" in checks["reach"].detail
    # Binary [1000, 500] at l = 200: C(1000, 200) > 2^500, though Singleton and Plotkin allow 249.
    s, checks = _run("hermite_half_rate.json", q=2, radius=200, min_distance=None)
    assert s.quantities["hamming_radius"] < 200 <= s.quantities["plotkin_radius"]
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
    # Finite length: C(m, l) 2^l <= q^n, the patterns of weight l need distinct syndromes.
    assert R.packing_radius(6000, 420, 8191, 2) >= 300
    assert R.packing_radius(15, 11, 2, 1) >= 3 and R.packing_radius(10, 1, 2, 1) == 0


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


def test_candidate_from_dict_rejects_unknown_keys_and_objectives() -> None:
    base = {"name": "x", "objective": "count", "q": 7, "m": 100, "n": 30, "rho": 0.5}
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


def test_claimed_values_must_be_finite_and_in_the_objective_range() -> None:
    base = {"name": "x", "objective": "count", "q": 7, "m": 100, "n": 30, "rho": 0.5, "radius": 5}
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
    assert main(["--objective", "count", "--q", "7", "--m", "100", "--n", "30", "--rho", "0.5", "--radius", "5", "--min-distance", "20", "--decoder-known"]) == 0
    text = capsys.readouterr().out
    assert text.startswith("# DQI screen: candidate") and "| q_prange |" in text and "Verdict:" in text
    assert main(["--objective", "count", "--q", "12", "--m", "100", "--n", "30", "--rho", "0.5"]) == 2
    assert "prime power" in capsys.readouterr().err
    qnull = tmp_path / "qnull.json"
    qnull.write_text(json.dumps({"name": "x", "objective": "count", "q": None, "m": 100, "n": 30, "rho": 0.5}))
    assert main(["--params", str(qnull)]) == 2  # bad input, not "not viable"
    assert capsys.readouterr().err.startswith("error: q ")


def test_cli_zero_valued_flags_override_the_params_file(capsys) -> None:
    main = S.main
    args = ["--params", str(EXAMPLES / "opi_prime_character_r19.json"), "--json"]
    assert main([*args, "--radius", "0", "--classical-witness", "0", "--finite-dqi-mean", "0"]) == 1
    candidate = json.loads(capsys.readouterr().out)["candidate"]
    assert (candidate["radius"], candidate["classical_witness"], candidate["finite_dqi_mean"]) == (0, 0.0, 0.0)
    assert candidate["decoder_known"] is True  # an absent boolean flag keeps the file's value
    flags = ["--objective", "count", "--q", "7", "--m", "100", "--n", "30", "--rho", "0.5", "--min-distance", "20"]
    assert main([*flags, "--radius", "0", "--decoder-known"]) == 1  # lam = 0 cannot beat Prange
    assert "R2 (hard): FAIL" in capsys.readouterr().out


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
    assert (result["m"], result["n"], result["q"], result["restarts"], result["singular"]) == (6, 3, 5, 2, 0)
    B[:, 2] = 0  # rank 2 < n: every draw is singular and scores 0
    rank_deficient = P.prange_restarts(B, [range(5)] * 6, 5, restarts=2, seed=0)
    assert rank_deficient["best"] == 0.0 and rank_deficient["singular"] == 2
    with pytest.raises(ValueError):
        P.prange_restarts(B, [range(4)] * 6, 4)


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


def test_prange_large_prime_field() -> None:
    q = 2**61 - 1
    rng = np.random.default_rng(7)
    B = rng.integers(1, q, size=(4, 2))  # int64 entries; int64 products would overflow
    x = [int(v) for v in rng.integers(1, q, size=2)]
    targets = [(int(B[i, 0]) * x[0] + int(B[i, 1]) * x[1]) % q for i in range(4)]
    result = P.prange_restarts(B, [{t} for t in targets], q, restarts=3, seed=0)
    assert result["best"] == 1.0 and result["singular"] == 0

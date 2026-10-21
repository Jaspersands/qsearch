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
        "radius_crit", "licensed_radius", "singleton_reach", "distance_reach", "sphere_packing_reach",
        "plotkin_reach", "kappa", "q_cap", "cosine_objective", "lambda_crit_cos", "restart_length",
        "existential_line", "rho_crit", "alpha_sub", "subfield_baseline",
    ]
    assert list(checks) == ["R1", "reach", "R2", "R3", "R3-encoder", "R4", "cap", "witness", "restarts"]


def test_example_a_radius_32_is_outside_licensed_reach() -> None:
    s, checks = _run("opi_prime_character_r32.json")
    assert checks["reach"].passed is False
    assert "outside licensed Hamming reach" in checks["reach"].detail
    assert s.verdict == "not viable"


def test_example_b_cosine_is_viable() -> None:
    s, checks = _run("mpi_signed_cosine.json")
    assert s.quantities["lambda_crit_cos"] == pytest.approx(0.00246, abs=5e-6)
    assert s.quantities["cosine_objective"] == pytest.approx(0.259, abs=5e-4)
    assert s.quantities["restart_length"] == pytest.approx(1594.5, abs=0.1)
    assert checks["R1"].passed is True
    assert s.verdict == "viable", s.reasons
    s, checks = _run("mpi_signed_cosine.json", decoder_known=False)
    assert checks["reach"].passed is None and s.verdict == "unknown"


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
    for p, b, c in ((2, 1, 12), (3, 2, 1), (4, 6, 1), (2, 12, 5), (2, 12, 0), (2, 6, 3)):
        with pytest.raises(ValueError, match="q = 4096"):
            _run("hermite_half_rate.json", p=p, b=b, c=c, **longer)
    for p, b, c in ((2, 12, 1), (2, 12, 4), (2, 12, 12)):
        assert _run("hermite_half_rate.json", p=p, b=b, c=c, **longer)[1]["R4"].passed is not None
    with pytest.raises(ValueError, match="p = 3"):
        _run("hermite_half_rate.json", p=3, **longer)  # checked even when b and c are absent
    assert _run("hermite_half_rate.json", p=8191, b=1, c=1)[1]["R4"].detail == "not applicable (prime field)"


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

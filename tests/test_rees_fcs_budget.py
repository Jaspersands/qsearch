"""tab:fcs-budget of the Rees paper against its JSON artifact and the paper's formulas."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from theorems import rees_fcs_budget as fb

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "docs" / "papers" / "rees-hsp" / "main.tex"
ARTIFACT = fb.DEFAULT_OUT

# The table as printed in main.tex (None marks a dash).
PRINTED = {
    "11": ("202.1", None, None, "42.3", "28.3", "47.0", "103.5"),
    "1031": ("167.3", None, None, "36.6", "33.4", "50.8", "93.0"),
    "5281": ("852.3", "50.3", "128.2", "39.1", "33.8", "52.2", "119.9"),
    "2^31-1": ("940.3", "50.9", "121.6", "35.9", "31.0", "49.8", "127.1"),
    "2^61-1": ("533.4", "52.9", "128.3", "34.1", "33.5", "51.0", "150.8"),
    "2^127-1": ("41.4", "49.9", "115.2", "34.0", "31.0", "49.5", "142.0"),
}


def _cell(text: str):
    text = text.strip()
    if text in ("--", "---"):
        return None
    m = re.fullmatch(r"\$(.+)\$", text)
    assert m, text
    return m.group(1)


def _table_from_main() -> dict:
    src = MAIN.read_text(encoding="utf-8")
    start = src.index(r"\midrule", src.index(r"\label{tab:fcs-budget}"))
    body = src[start:src.index(r"\bottomrule", start)]
    rows = {}
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("$") or not line.endswith(r"\\"):
            continue
        cells = [c for c in line[:-2].split("&")]
        label = _cell(cells[0]).replace("{", "").replace("}", "")
        rows[label] = tuple(_cell(c) for c in cells[1:])
    return rows


@pytest.fixture(scope="module")
def artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def _row_values(row: dict) -> tuple:
    return tuple(row["table"][c] for c in fb.COLUMNS)


def test_artifact_matches_printed_table(artifact):
    got = {r["label"]: _row_values(r) for r in artifact["rows"]}
    assert got == PRINTED
    wc = {r["label"]: r["table"]["combined_worst_case_Q"] for r in artifact["rows"]}
    assert (wc["2^31-1"], wc["2^61-1"], wc["2^127-1"]) == ("944.9", "555.4", "61.5")


@pytest.mark.skipif(not MAIN.exists(), reason="paper source not present")
def test_printed_table_is_the_live_main_tex_table():
    assert _table_from_main() == PRINTED


def test_artifact_is_current():
    fresh = json.loads(json.dumps(fb.build()))
    assert fresh == json.loads(ARTIFACT.read_text(encoding="utf-8")), \
        "run: /opt/anaconda3/bin/python -m theorems.rees_fcs_budget"


def test_rounding_is_not_borderline(artifact):
    for r in artifact["rows"]:
        for col, margin in r["rounding_margin"].items():
            assert margin is None or margin > 1e-3, (r["label"], col, margin)


def test_appendix_claims_at_the_six_primes(artifact):
    """Appendix app:fc-numbers(a): least public arities, one FCS node per Gamma_F grade, linear at
    kappa_d = 1, Gamma_0 empty, no Schedule 2, and the min-with-combined variant never used."""
    worst = max((r["iii"]["grades"][str(r["iii"]["argmax_cap_grade"])]["log2_trial_cap"], r["label"],
                 r["iii"]["argmax_cap_grade"], r["iii"]["B"]) for r in artifact["rows"])
    assert worst[1:] == ("5281", 4, 40) and abs(worst[0] - 33.78) < 0.005
    assert max(float(r["table"]["iii_total"]) for r in artifact["rows"]) == 52.2
    for r in artifact["rows"]:
        iii = r["iii"]
        assert iii["S"] == 20 and iii["t"] == 1
        assert iii["Gamma0_empty"] and not iii["schedule2_used"]
        assert iii["error_budget"]["within_eps"] and iii["explicit_choice"]["within_eps"]
        for d, gr in iii["grades"].items():
            if gr["kappa"] == 1:
                assert gr["schedule"] == "lin" and int(gr["M"]) == fb.PROFILE[int(d) - 1] + 1
            else:
                assert gr["schedule"] == "FCS" and gr["fcs_not_above_combined"]
                assert 1 <= int(gr["explicit_M"]) - int(gr["M"]) <= 2
        assert 0.2 <= iii["explicit_choice"]["log2_Q_increase"] <= 1.35
        assert round(iii["explicit_choice"]["max_trial_cap_log2"], 1) <= 33.8


def test_least_arity_is_least():
    """At every FCS grade, M_d - 1 columns admit no n0 with beta <= tau_d."""
    for _, p in fb.PRIMES:
        res = fb.free_coordinate_iii(p)
        for d, gr in res["grades"].items():
            if gr["cls"] != "F":
                continue
            M, k, g = gr["M"], gr["kappa"], fb.PROFILE[d - 1]
            assert fb.beta(p, k, M, gr["n0"], g) <= gr["tau"]
            assert all(fb.beta(p, k, M - 1, n0, g) > gr["tau"] for n0 in range(1, M))


def test_uniform_kernel_rule_is_flagged_and_robust(artifact):
    for r in artifact["rows"]:
        uk = r["uniform_kernel"]
        if r["table"]["uniform_kernel_Q"] is None:
            assert uk is None
            continue
        assert "not stated in main.tex" in uk["rule"]
        assert uk["tree_abort_le_1_16"] and uk["column_bumps"] == 0
        assert uk["main_tex_literal_rank_term"]["same_as_table"]


def test_proposed_macro_entries(artifact):
    entries = artifact["proposed_numbers_map_entries"]
    assert len(entries) == 38
    names = [e["macro"] for e in entries]
    assert len(set(names)) == len(names) and all(re.fullmatch(r"[A-Za-z]+", n) for n in names)
    for e in entries:
        node = artifact
        for part in e["path"].split("."):
            node = node[int(part)] if isinstance(node, list) else node[part]
        assert isinstance(node, str) and re.fullmatch(r"\d+\.\d", node)


def test_independent_spot_values():
    """Hand-checkable entries: the combined rule at p = 11 and B_d(a) at small arguments."""
    assert fb.B_IS(2, 1) == (2 * 4) ** 2
    assert fb.B_IS(4, 1) == (4 ** 6 * 2 ** 4) ** 3
    comb = fb.combined_rule(11)
    # p = 11: kappa = (2,1,2,5,2,1,2,1) at d = 2..9; p < 16*2^6, so Schedule 1 at degree kappa_d.
    expected = [fb.B_IS(2, 17), 17, fb.B_IS(2, 14), fb.B_IS(5, 12), fb.B_IS(2, 9), 7, fb.B_IS(2, 3), 2]
    assert [comb["sch"][d][1] for d in range(2, 10)] == expected
    assert comb["Q"] == 9 * 20 * __import__("math").prod(expected)

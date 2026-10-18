from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
PAPER = REPO / "docs" / "papers" / "classical-competitors"


def _numbers():
    spec = importlib.util.spec_from_file_location("paper_numbers", PAPER / "make_numbers.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_resolve_walks_keys_and_indices() -> None:
    data = {"a": [{"b": 1}, {"b": {"c": 0.123456}}]}
    nb = _numbers()
    assert nb.resolve(data, "a.1.b.c") == 0.123456
    with pytest.raises(KeyError, match="a.2"):
        nb.resolve(data, "a.2.b")


def test_render_formats_and_rejects_bad_macro_names(tmp_path: Path) -> None:
    (tmp_path / "r.json").write_text(json.dumps({"x": 0.7745042850823902, "n": 127, "s": "13/20"}))
    entries = [
        {"macro": "DcpX", "source": "r.json", "path": "x", "format": "{:.4f}"},
        {"macro": "Count", "source": "r.json", "path": "n", "format": "{}"},
        {"macro": "Ratio", "source": "r.json", "path": "s", "format": "{}"},
    ]
    text = _numbers().render(entries, tmp_path)
    assert "\\newcommand{\\DcpX}{0.7745}" in text and "\\newcommand{\\Count}{127}" in text
    with pytest.raises(ValueError, match="macro"):
        _numbers().render([{"macro": "Bad1", "source": "r.json", "path": "n", "format": "{}"}], tmp_path)


def test_convert_rounds_in_the_stated_direction() -> None:
    nb = _numbers()
    assert nb.convert("424553765284920852120940002337825/41538374868278621028243970633760768", "up:6") == "0.010221"
    assert nb.convert("1/3", "down:4") == "0.3333" and nb.convert("1/3", "up:4") == "0.3334"
    assert nb.convert("2/5", "up:4") == "0.4000" and nb.convert(0, "down:4") == "0.0000"


def test_convert_bits_pi_and_sci() -> None:
    nb = _numbers()
    assert nb.convert("2305843009213693951", "bits") == "61" and nb.convert(2**1279 - 1, "bits") == "1279"
    assert nb.convert(1.0471975511965976, "pi") == "\\pi/3" and nb.convert(2.0943951023931953, "pi") == "2\\pi/3"
    assert nb.convert(1.6689710972195777, "pi") == "17\\pi/32" and nb.convert(1.5707963267948966, "pi") == "\\pi/2"
    assert nb.convert(4.06e-06, "sci") == "4.1\\times 10^{-6}" and nb.convert(4.0e-06, "sci") == "4.0\\times 10^{-6}"
    with pytest.raises(ValueError):
        nb.convert(1.0, "pi")  # not a small rational multiple of pi


def test_render_applies_kind_before_format(tmp_path: Path) -> None:
    (tmp_path / "r.json").write_text(json.dumps({"tv": "1/3"}))
    text = _numbers().render([{"macro": "TV", "source": "r.json", "path": "tv", "kind": "up:3", "format": "{}"}], tmp_path)
    assert "\\newcommand{\\TV}{0.334}" in text


def test_used_macros_must_be_defined() -> None:
    nb = _numbers()
    tex = "We get \\DcpX{} and \\Missing{} and \\section{x} \\cite{a}."
    assert nb.undefined(tex, {"DcpX"}, known_commands={"section", "cite"}) == ["Missing"]


def test_compare_reports_matches_mismatches_and_missing(tmp_path: Path) -> None:
    committed, fresh = tmp_path / "repo", tmp_path / "fresh"
    for root, value in ((committed, 0.77450), (fresh, 0.77452)):
        (root / "a").mkdir(parents=True)
        (root / "a" / "r.json").write_text(json.dumps({"x": value, "n": 127}))
    (committed / "a" / "only.json").write_text(json.dumps({"y": 1}))
    entries = [
        {"macro": "X", "source": "a/r.json", "path": "x", "format": "{:.4f}"},
        {"macro": "N", "source": "a/r.json", "path": "n", "format": "{}"},
        {"macro": "Y", "source": "a/only.json", "path": "y", "format": "{}"},
    ]
    rows = {r["macro"]: r["status"] for r in _numbers().compare(entries, committed, fresh)}
    assert rows == {"X": "same", "N": "same", "Y": "not regenerated"}
    (fresh / "a" / "r.json").write_text(json.dumps({"x": 0.9, "n": 127}))
    rows = {r["macro"]: r["status"] for r in _numbers().compare(entries, committed, fresh)}
    assert rows["X"] == "DIFFERENT"


@pytest.mark.skipif(not (PAPER / "numbers_map.json").exists(), reason="paper not drafted yet")
def test_committed_numbers_match_the_reports() -> None:
    nb = _numbers()
    entries = json.loads((PAPER / "numbers_map.json").read_text())["numbers"]
    assert (PAPER / "numbers.tex").read_text() == nb.render(entries, REPO)

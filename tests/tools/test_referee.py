from __future__ import annotations

import hashlib
import json
import os
import textwrap
from pathlib import Path

import pytest

from tools.referee import extract as X
from tools.referee import referee as R


FIXTURE_NOTE = textwrap.dedent(
    """\
    # Fixture Radial Bound

    2026-10-18. LOCAL APPLICATION REVIEW PENDING. No speedup is claimed. Not a new algorithm.
    Producer: `python theorems/fixture_radial.py --write --seed 3`.
    Output: `research/classical_baselines/fixture_radial.json`.

    ## Question And Result

    Does the radial bound hold for every saved input? It holds for all twelve
    saved inputs, with margin at least 0.031.

    ## 1. Lemma: Radial Bound

    For every radius r at least 1 the weight enumerator is bounded by the
    radial sum, by the triangle inequality applied term by term.

    ## Decisive Controls

    The Prange completion baseline reaches 0.654 on the same inputs.

    ## Try To Kill It

    We searched 10000 random inputs for a counterexample to the radial bound
    and found none.

    ## Decision And Next

    Keep the bound; next test the 32-radius inputs.
    """
)


def _write(root: Path, stem: str, text: str | bytes) -> Path:
    path = root / "research" / f"{stem}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")
    return path


def test_parse_note_reads_every_field(tmp_path: Path) -> None:
    path = _write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE)
    packet = X.parse_note(path)
    assert (packet.stem, packet.status, packet.date) == ("FIXTURE_NOTE", "review-pending", "2026-10-18")
    assert packet.path == "research/FIXTURE_NOTE.md"
    assert packet.title == "Fixture Radial Bound"
    assert packet.producer == {
        "command": "python theorems/fixture_radial.py --write --seed 3",
        "script": "theorems/fixture_radial.py",
        "flags": "--write --seed 3",
        "artifact": "research/classical_baselines/fixture_radial.json",
    }
    assert "No speedup is claimed." in packet.not_claimed
    assert "Not a new algorithm." in packet.not_claimed
    assert "##" not in packet.result and "twelve" in packet.result
    assert [d["heading"] for d in packet.derivations] == ["1. Lemma: Radial Bound"]
    assert "triangle inequality" in packet.derivations[0]["text"]
    assert [c["heading"] for c in packet.controls] == ["Decisive Controls"]
    assert packet.self_check is not None and "counterexample" in packet.self_check
    assert packet.decision is not None and "32-radius" in packet.decision
    assert packet.content_sha == hashlib.sha256(path.read_bytes()).hexdigest()
    assert isinstance(packet.flags, list)
    assert X.to_dict(packet)["stem"] == "FIXTURE_NOTE"


def test_parse_note_flags_only_what_the_claim_checker_raises_on_the_result(tmp_path: Path) -> None:
    text = textwrap.dedent(
        """\
        # Flagged

        2026-10-17. REVIEW PENDING.

        ## Result

        The sampler reads the table through QRAM. No membership oracle is supplied.

        ## Discussion

        This is an oracle separation heuristic.
        """
    )
    assert X.parse_note(_write(tmp_path, "FLAGGED", text)).flags == ["input_loading"]
    assert X.parse_note(_write(tmp_path, "PLAIN", FIXTURE_NOTE)).flags == []


def test_parse_note_falls_back_to_the_first_section_for_result(tmp_path: Path) -> None:
    text = textwrap.dedent(
        """\
        # Fallback

        2026-10-12. Review pending.

        ## Setup And Inputs

        The saved inputs are the N127 instances.

        ## Discussion

        Later text.
        """
    )
    packet = X.parse_note(_write(tmp_path, "FALLBACK", text))
    assert "N127 instances" in packet.result
    assert "Later text" not in packet.result
    assert packet.derivations == [] and packet.controls == []
    assert packet.self_check is None and packet.decision is None
    assert packet.producer is None


def test_parse_note_reads_producer_from_the_reproduce_block_at_the_end(tmp_path: Path) -> None:
    (tmp_path / "theorems").mkdir()
    (tmp_path / "theorems" / "end_block.py").write_text(
        'ROOT = None\nREPORT = ROOT / "research/classical_baselines/end_block.json"\n', encoding="utf-8"
    )
    text = textwrap.dedent(
        """\
        # End Block

        2026-10-14. REVIEW PENDING.

        ## Claim

        A claim with no artifact path in the text.

        ## Reproduce

        ```text
        python theorems/end_block.py --write
        ```
        """
    )
    packet = X.parse_note(_write(tmp_path, "END_BLOCK", text))
    assert packet.producer == {
        "command": "python theorems/end_block.py --write",
        "script": "theorems/end_block.py",
        "flags": "--write",
        "artifact": "research/classical_baselines/end_block.json",
    }


def test_parse_note_prefers_the_notes_own_producer_and_its_artifact(tmp_path: Path) -> None:
    (tmp_path / "theorems").mkdir()
    for stem in ("own_design", "own_simulation", "report_only"):
        (tmp_path / "theorems" / f"{stem}.py").write_text(f'REPORT = ROOT / "research/classical_baselines/{stem}.json"\n', encoding="utf-8")
    (tmp_path / "research" / "classical_baselines").mkdir(parents=True)
    for stem in ("own_design", "report_only"):
        (tmp_path / "research" / "classical_baselines" / f"{stem}.json").write_text("{}", encoding="utf-8")
    own_design = textwrap.dedent(
        """\
        # Own Design

        2026-10-14. REVIEW PENDING.

        ## Result

        The sampler from `research/classical_baselines/sampler.json` is reused.

        ## Reproduce

        ```text
        python theorems/sampler.py --write
        python theorems/own_design.py --write
        python theorems/own_design.py --length 32768 --write
        ```
        """
    )
    packet = X.parse_note(_write(tmp_path, "OWN_DESIGN", own_design))
    assert packet.producer == {"command": "python theorems/own_design.py --write", "script": "theorems/own_design.py",
                               "flags": "--write", "artifact": "research/classical_baselines/own_design.json"}

    own_simulation = textwrap.dedent(
        """\
        # Own Simulation

        2026-10-14. REVIEW PENDING.

        ## Result

        Sources are in `research/literature_audits/instrument_sources.json`.

        ```text
        python theorems/own_simulation.py
        ```

        Report: `research/classical_baselines/own_simulation.json`.
        """
    )
    packet = X.parse_note(_write(tmp_path, "OWN_SIMULATION", own_simulation))
    assert packet.producer["artifact"] == "research/classical_baselines/own_simulation.json"

    report_only = own_simulation.replace("own_simulation.py", "report_only.py").replace(
        "Report: `research/classical_baselines/own_simulation.json`.", "")
    packet = X.parse_note(_write(tmp_path, "REPORT_ONLY_NOTE", report_only))
    assert packet.producer["artifact"] == "research/classical_baselines/report_only.json"
    unresolved = own_simulation.replace("Report: `research/classical_baselines/own_simulation.json`.", "")
    packet = X.parse_note(_write(tmp_path, "UNRESOLVED_NOTE", unresolved))
    assert packet.producer["artifact"] == "research/literature_audits/instrument_sources.json"


def test_parse_note_keeps_fenced_headings_inside_their_section(tmp_path: Path) -> None:
    text = textwrap.dedent(
        """\
        # Fenced

        2026-10-15. Review pending.

        ## 2. Derivation

        The exact table is

        ```text
        ## not a heading
        k = 3
        ```

        and the bound follows.

        ## Decision

        Stop here.
        """
    )
    packet = X.parse_note(_write(tmp_path, "FENCED", text))
    assert [d["heading"] for d in packet.derivations] == ["2. Derivation"]
    body = packet.derivations[0]["text"]
    assert "## not a heading" in body and "the bound follows" in body
    assert packet.decision == "Stop here."


def test_parse_note_reads_replacement_bytes_and_long_producer_flags(tmp_path: Path) -> None:
    raw = (
        b"# Bytes \xff Note\n\n2026-10-16. REVIEW PENDING. No hardness claim.\n\n"
        b"## Result\n\nThe sampler matches the target law \xfe within 0.01.\n\n## Execute\n\n"
        b"```\npython theorems/polar_source_design.py --length 32768 --grid 256 --power 3 --write\n```\n"
    )
    path = _write(tmp_path, "BYTES_NOTE", raw)
    packet = X.parse_note(path)
    assert packet.content_sha == hashlib.sha256(raw).hexdigest()
    assert "�" in packet.title
    assert packet.producer is not None
    assert packet.producer["flags"] == "--length 32768 --grid 256 --power 3 --write"
    assert packet.producer["artifact"] is None
    assert "within 0.01" in packet.result


def _with_artifact(root: Path, artifact: str, payload: str) -> X.NotePacket:
    path = root / artifact
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    text = FIXTURE_NOTE.replace("research/classical_baselines/fixture_radial.json", artifact.removeprefix("research/"))
    return X.parse_note(_write(root, "FIXTURE_NOTE", text))


def test_artifact_excerpt_lists_keys_and_numeric_leaves(tmp_path: Path) -> None:
    data = {"status": "ok", "mean": 0.9028, "flag": True, "tail": {"k110": 0.3145, "runs": [1, 2, 3, 4, 5, 6, 7]}}
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", json.dumps(data))
    assert packet.producer["artifact"] == "classical_baselines/fixture_radial.json"
    excerpt = X.artifact_excerpt(tmp_path, packet)
    assert excerpt is not None
    assert excerpt.startswith("keys: flag, mean, status, tail")
    assert "mean = 0.9028" in excerpt and "tail.k110 = 0.3145" in excerpt
    assert not any(line.startswith("flag") for line in excerpt.splitlines()[1:])  # booleans are not leaves
    assert "tail.runs[4] = 5" in excerpt and "tail.runs[5]" not in excerpt and "(+2)" in excerpt
    assert len(excerpt) <= 4000
    big = {f"key{i:04d}": i / 7 for i in range(2000)}
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", json.dumps(big))
    short = X.artifact_excerpt(tmp_path, packet, max_chars=500)
    assert short is not None and len(short) <= 500 and short.endswith("[truncated]")


def test_artifact_excerpt_shares_the_budget_across_top_level_keys(tmp_path: Path) -> None:
    data = {"a_large": {f"k{i:03d}": i / 7 for i in range(300)}, "b_small": {"x": 1.5}, "c_list": [7, 8], "d_flag": True}
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", json.dumps(data))
    excerpt = X.artifact_excerpt(tmp_path, packet, max_chars=600)
    assert excerpt is not None and len(excerpt) <= 600 and excerpt.endswith("[truncated]")
    lines = excerpt.splitlines()
    assert lines[0] == "keys: a_large, b_small, c_list, d_flag"
    assert "b_small.x = 1.5" in lines and "c_list[0] = 7" in lines and "c_list[1] = 8" in lines
    body = lines[1:-1]
    assert body[0] == "a_large.k000 = 0.0" and sum(line.startswith("a_large.") for line in body) > 5
    keys = [line.split(".")[0].split("[")[0] for line in body]
    assert keys == sorted(keys)  # grouped by key, in key order


def test_artifact_excerpt_is_none_when_missing_or_invalid(tmp_path: Path) -> None:
    packet = X.parse_note(_write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE))
    assert X.artifact_excerpt(tmp_path, packet) is None
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", "{not json")
    assert X.artifact_excerpt(tmp_path, packet) is None
    fallback = X.parse_note(_write(tmp_path, "FALLBACK", "# F\n\n2026-10-01. Review pending.\n\n## Result\n\nNo producer.\n"))
    assert fallback.producer is None and X.artifact_excerpt(tmp_path, fallback) is None
    assert X._resolve_artifact(tmp_path, "classical_baselines/fixture_radial.json") == (
        tmp_path / "research/classical_baselines/fixture_radial.json"
    )
    assert X._resolve_artifact(tmp_path, "classical_baselines/absent.json") is None


def _dated_note(root: Path, stem: str, status_line: str, mtime: int) -> Path:
    path = _write(root, stem, f"# {stem}\n\n{status_line}\n\n## Result\n\nA result about the {stem.lower()} inputs.\n")
    os.utime(path, (mtime, mtime))
    return path


def test_select_notes_orders_by_status_date_then_mtime_and_skips_current_reviews(tmp_path: Path) -> None:
    _dated_note(tmp_path, "PRIME_OLD", "2026-10-10. REVIEW PENDING.", 4000)
    _dated_note(tmp_path, "PRIME_NEW", "2026-10-18. REVIEW PENDING.", 1000)
    _dated_note(tmp_path, "POLAR_UNDATED", "Local derivation, review pending.", 3000)
    _dated_note(tmp_path, "POLAR_UNDATED_OLDER", "Review pending.", 2000)
    _dated_note(tmp_path, "SUPERSEDED_ONE", "2026-10-19. SUPERSEDED by the newer note; review pending.", 5000)
    (tmp_path / "research" / "AGENT_HANDOFF.md").write_text("# Handoff\n\n2026-10-20. Review pending.\n", encoding="utf-8")
    everything = ["PRIME_NEW", "PRIME_OLD", "POLAR_UNDATED", "POLAR_UNDATED_OLDER"]
    assert [p.stem for p in R.select_notes(tmp_path)] == everything
    assert R.load_reviews(tmp_path) == {"notes": {}}

    current = R.note_sha(tmp_path / "research" / "PRIME_NEW.md")
    reviews = {"notes": {"PRIME_NEW": {"content_sha": current}, "PRIME_OLD": {"content_sha": "0" * 64}}}
    assert [p.stem for p in R.select_notes(tmp_path, reviews=reviews)] == everything[1:]
    assert [p.stem for p in R.select_notes(tmp_path, reviews=reviews, exclude_reviewed=False)] == everything
    store = tmp_path / R.REVIEWS
    store.parent.mkdir(parents=True)
    store.write_text(json.dumps(reviews), encoding="utf-8")
    assert R.load_reviews(tmp_path) == reviews
    assert [p.stem for p in R.select_notes(tmp_path)] == everything[1:]

    assert [p.stem for p in R.select_notes(tmp_path, prefixes=("PRIME",), exclude_reviewed=False)] == ["PRIME_NEW", "PRIME_OLD"]
    assert [p.stem for p in R.select_notes(tmp_path, limit=2, exclude_reviewed=False)] == everything[:2]
    assert [p.stem for p in R.select_notes(tmp_path, statuses=("superseded",))] == ["SUPERSEDED_ONE"]


def _export_fixture(root: Path) -> list[Path]:
    artifact = root / "research" / "classical_baselines" / "fixture_radial.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps({"mean": 0.9028, "status": "certificate verified for every saved input"}), encoding="utf-8")
    notes = [_write(root, "FIXTURE_NOTE", FIXTURE_NOTE)]
    for i in range(5):
        notes.append(_dated_note(root, f"OTHER_{i}", f"2026-10-0{5 - i}. REVIEW PENDING.", 1000 + i))
    return notes


def test_export_writes_instructions_and_batches_with_artifact_excerpts(tmp_path: Path) -> None:
    notes = _export_fixture(tmp_path)
    out = tmp_path / "out"
    paths = R.export_batches(tmp_path, out, notes)
    assert [p.name for p in paths] == ["batch_01.json", "batch_02.json"]
    first, second = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
    assert (first["batch"], len(first["notes"]), second["batch"], len(second["notes"])) == (1, 5, 2, 1)
    assert [n["stem"] for n in first["notes"] + second["notes"]] == [p.stem for p in notes]
    assert first["claim_verdicts"] == list(R.CLAIM_VERDICTS) and first["overall_verdicts"] == list(R.OVERALL)
    assert '"claims"' in first["output_format"]
    packet = first["notes"][0]
    assert "mean = 0.9028" in packet["artifact_excerpt"]
    assert packet["text"] == FIXTURE_NOTE and packet["content_sha"] == R.note_sha(notes[0])
    assert all(n["artifact_excerpt"] is None for n in first["notes"][1:] + second["notes"])
    instructions = (out / "INSTRUCTIONS.md").read_text(encoding="utf-8")
    for word in R.CLAIM_VERDICTS + R.OVERALL:
        assert f"`{word}`" in instructions
    assert "verbatim" in instructions and "must not propose" in instructions


def _claim(quote: str, verdict: str = "gap", **extra) -> dict:
    return {"quote": quote, "verdict": verdict, "step": "Question And Result", "finding": "The margin needs a uniform bound.", **extra}


def _row(root: Path, stem: str = "FIXTURE_NOTE", overall: str = "needs-work", claims: list[dict] | None = None, **extra) -> dict:
    sha = R.note_sha(root / "research" / f"{stem}.md")
    claims = claims if claims is not None else [_claim("It holds for all twelve saved inputs, with margin at least 0.031")]
    return {"stem": stem, "content_sha": sha, "overall": overall, "summary": "One gap in the margin.", "claims": claims, **extra}


def _jsonl(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def test_import_rejects_bad_verdicts_and_non_verbatim_quotes_and_marks_stale(tmp_path: Path) -> None:
    _write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE)
    _dated_note(tmp_path, "OTHER", "2026-10-11. REVIEW PENDING.", 1000)
    out = tmp_path / "out"
    bad_rows = [
        _row(tmp_path, claims=[_claim("It holds for all twelve saved inputs", verdict="maybe")]),
        _row(tmp_path, overall="fine"),
        _row(tmp_path, claims=[_claim("the radial bound holds")]),
        _row(tmp_path, claims=[_claim("It holds for all thirteen saved inputs")]),
        _row(tmp_path, claims=[_claim("olds for all twelve saved inputs")]),
        _row(tmp_path, stem="OTHER") | {"stem": "MISSING_NOTE"},
    ]
    for index, row in enumerate(bad_rows):
        with pytest.raises(ValueError):
            R.import_reviews(tmp_path, [_jsonl(out / f"bad_{index}.jsonl", [_row(tmp_path, stem="OTHER", claims=[]), row])], "j")
    assert not (tmp_path / R.REVIEWS).exists()

    many = [_claim("It holds for all twelve saved inputs, with margin at least 0.031", finding="x" * 900)] * 8
    good = _row(tmp_path, claims=many, summary="s" * 2000)
    stale = _row(tmp_path, stem="OTHER", overall="sound", claims=[]) | {"content_sha": "0" * 64}
    result = R.import_reviews(tmp_path, [_jsonl(out / "good.jsonl", [good, stale])], "test-judge", today="2026-10-21")
    assert result == {"imported": ["FIXTURE_NOTE", "OTHER"], "stale": ["OTHER"]}
    data = json.loads((tmp_path / R.REVIEWS).read_text(encoding="utf-8"))
    entry = data["notes"]["FIXTURE_NOTE"]
    assert (entry["judge"], entry["reviewed_on"], entry["overall"], entry["stale"]) == ("test-judge", "2026-10-21", "needs-work", False)
    assert len(entry["claims"]) == 6 and len(entry["claims"][0]["finding"]) == 600 and len(entry["summary"]) == 1500
    assert entry["claims"][0]["covered_by_self_check"] is False
    assert data["notes"]["OTHER"]["stale"] is True

    again = _row(tmp_path, overall="unsound", claims=[_claim("It holds for all twelve saved inputs", verdict="wrong")])
    R.import_reviews(tmp_path, [_jsonl(out / "again.jsonl", [again])], "second-judge", today="2026-10-22")
    data = json.loads((tmp_path / R.REVIEWS).read_text(encoding="utf-8"))
    assert data["notes"]["FIXTURE_NOTE"]["overall"] == "unsound" and data["notes"]["FIXTURE_NOTE"]["judge"] == "second-judge"
    assert len(data["notes"]["FIXTURE_NOTE"]["claims"]) == 1 and "OTHER" in data["notes"]


@pytest.mark.parametrize("overall, verdicts, accepted", [
    ("sound", ["wrong"], False),
    ("sound", ["holds", "gap"], False),
    ("needs-work", ["gap", "wrong"], False),
    ("unclear", ["wrong"], False),
    ("unclear", ["gap"], False),
    ("unsound", ["gap", "holds"], False),
    ("unsound", [], False),
    ("unsound", ["gap", "wrong"], True),
    ("needs-work", ["holds", "gap"], True),
    ("needs-work", [], True),
    ("sound", ["holds", "unclear"], True),
    ("sound", [], True),
    ("unclear", ["unclear", "holds"], True),
])
def test_import_rejects_an_overall_verdict_that_contradicts_the_claims(tmp_path: Path, overall, verdicts, accepted) -> None:
    _write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE)
    quote = "It holds for all twelve saved inputs, with margin at least 0.031"
    row = _row(tmp_path, overall=overall, claims=[_claim(quote, verdict=verdict) for verdict in verdicts])
    answer = _jsonl(tmp_path / "out" / "rows.jsonl", [row])
    if accepted:
        assert R.import_reviews(tmp_path, [answer], "j")["imported"] == ["FIXTURE_NOTE"]
    else:
        with pytest.raises(ValueError, match="contradicts"):
            R.import_reviews(tmp_path, [answer], "j")


def test_import_rejects_malformed_rows_and_stems_that_are_paths(tmp_path: Path) -> None:
    _write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE)
    (tmp_path / "README.md").write_text("Some words here for a long enough quote to pass the check.\n", encoding="utf-8")
    quote = "It holds for all twelve saved inputs, with margin at least 0.031"
    out = tmp_path / "out"
    malformed = {
        "list": '[["a"]]\n',
        "scalar": "5\n",
        "claims_object": json.dumps(_row(tmp_path) | {"claims": {"quote": quote}}) + "\n",
        "claim_string": json.dumps(_row(tmp_path) | {"claims": [quote]}) + "\n",
        "traversal": json.dumps({"stem": "../README", "content_sha": "x", "overall": "unsound", "claims": [
            {"quote": "Some words here for a long enough quote", "verdict": "wrong"}]}) + "\n",
        "bad_json": '{"stem": \n',
    }
    for name, text in malformed.items():
        path = out / f"{name}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        with pytest.raises(ValueError):
            R.import_reviews(tmp_path, [path], "j")
    with pytest.raises(ValueError, match="cannot read"):
        R.import_reviews(tmp_path, [out / "absent" / "*.jsonl"], "j")
    assert not (tmp_path / R.REVIEWS).exists()

    store = tmp_path / R.REVIEWS
    store.parent.mkdir(parents=True)
    store.write_text(json.dumps({"notes": {"../README": {"overall": "unsound", "content_sha": "x", "claims": []}}}), encoding="utf-8")
    R.render(tmp_path, today="2026-10-21")
    assert not (tmp_path / "research/audits/README.md").exists()
    assert sorted(p.name for p in (tmp_path / "research/audits/reviews").iterdir()) == ["reviews.json"]


def test_cli_rejects_bad_numbers_and_reports_import_errors_without_a_traceback(tmp_path: Path, capsys) -> None:
    _export_fixture(tmp_path)
    root = str(tmp_path)
    for argv in (["export", "--root", root, "--out-dir", str(tmp_path / "o"), "--batch-size", "0"],
                 ["select", "--root", root, "--limit", "-1"]):
        with pytest.raises(SystemExit) as exit_info:
            R.main(argv)
        assert exit_info.value.code == 2
    assert R.main(["export", "--root", root, "--out-dir", str(tmp_path / "o"), "--note", "research/OTHER_3.md"]) == 0
    assert [n["stem"] for n in json.loads((tmp_path / "o" / "batch_01.json").read_text(encoding="utf-8"))["notes"]] == ["OTHER_3"]
    with pytest.raises(SystemExit):
        R.main(["export", "--root", root, "--out-dir", str(tmp_path / "o"), "--note", "../README"])
    capsys.readouterr()
    rows = _jsonl(tmp_path / "rows.jsonl", [_row(tmp_path) | {"claims": {"quote": "x"}}])
    for files in ([str(tmp_path / "nonexistent" / "*.jsonl")], [str(rows)]):
        assert R.main(["import", *files, "--root", root, "--judge", "j"]) == 2
        assert "nothing imported" in capsys.readouterr().err


def test_import_checks_a_note_edited_after_export_against_the_exported_text(tmp_path: Path) -> None:
    notes = _export_fixture(tmp_path)
    R.export_batches(tmp_path, tmp_path / "pass", notes[:2])
    quote = "It holds for all twelve saved inputs, with margin at least 0.031"
    rows = [_row(tmp_path, claims=[_claim(quote)]),
            _row(tmp_path, stem="OTHER_0", overall="sound", claims=[_claim("A result about the other_0 inputs", verdict="holds")])]
    answer = _jsonl(tmp_path / "pass" / "out" / "batch_01.jsonl", rows)
    note = notes[0]
    note.write_text(note.read_text(encoding="utf-8").replace("It holds for all twelve", "It holds for eleven of twelve"), encoding="utf-8")

    result = R.import_reviews(tmp_path, [answer], "j", today="2026-10-21")
    assert result == {"imported": ["FIXTURE_NOTE", "OTHER_0"], "stale": ["FIXTURE_NOTE"]}
    claim = R.load_reviews(tmp_path)["notes"]["FIXTURE_NOTE"]["claims"][0]
    assert claim["verified"] is True and claim["quote"] == "It holds for all twelve\nsaved inputs, with margin at least 0.031"

    invented = _row(tmp_path, claims=[_claim("It holds for all thirteen saved inputs, with margin")]) | {"content_sha": rows[0]["content_sha"]}
    with pytest.raises(ValueError, match="not verbatim"):
        R.import_reviews(tmp_path, [_jsonl(tmp_path / "pass" / "out" / "invented.jsonl", [invented])], "j")

    elsewhere = _jsonl(tmp_path / "moved" / "batch_01.jsonl", rows)
    result = R.import_reviews(tmp_path, [elsewhere], "j", today="2026-10-22")
    assert result["stale"] == ["FIXTURE_NOTE"]
    claim = R.load_reviews(tmp_path)["notes"]["FIXTURE_NOTE"]["claims"][0]
    assert claim["verified"] is False and claim["quote"] == quote

    batch = tmp_path / "pass" / "batch_01.json"
    tampered = json.loads(batch.read_text(encoding="utf-8"))
    tampered["notes"][0]["text"] = tampered["notes"][0]["text"].replace("twelve", "thirteen")
    batch.write_text(json.dumps(tampered), encoding="utf-8")
    R.import_reviews(tmp_path, [_jsonl(tmp_path / "pass" / "out" / "invented.jsonl", [invented])], "j")
    assert R.load_reviews(tmp_path)["notes"]["FIXTURE_NOTE"]["claims"][0]["verified"] is False

    R.render(tmp_path, today="2026-10-22")
    review = (tmp_path / "research/audits/reviews/FIXTURE_NOTE.md").read_text(encoding="utf-8")
    assert "not found in the current note" in review


def test_import_rejects_a_quote_from_the_artifact_excerpt(tmp_path: Path) -> None:
    notes = _export_fixture(tmp_path)
    batch = json.loads(R.export_batches(tmp_path, tmp_path / "out", notes[:1])[0].read_text(encoding="utf-8"))
    lifted = "certificate verified for every saved input"
    assert lifted in batch["notes"][0]["artifact_excerpt"]
    row = _row(tmp_path, claims=[_claim(lifted, verdict="holds")])
    with pytest.raises(ValueError, match="not verbatim"):
        R.import_reviews(tmp_path, [_jsonl(tmp_path / "out" / "lifted.jsonl", [row])], "j")


MATH_NOTE = textwrap.dedent(
    """\
    # Radial Readout

    2026-10-19. REVIEW PENDING.

    ## Result

    For any unit radial superposition u, its bad mass b<=epsilon. Unique-good
    radial vectors give

        1-epsilon <= ||A u||^2 <= 1+(M-1)*epsilon.

    When 2ell+1<=K, the older exact RS-moment argument already determines every
    coefficient, with margin 0.031 on all **twelve** inputs.

    - the first listed item holds for every input
    - the second listed item has a gap of 0.5
    """
)


def test_import_rejects_quotes_whose_symbols_differ_from_the_note(tmp_path: Path) -> None:
    _write(tmp_path, "MATH_NOTE", MATH_NOTE)
    flipped = [
        "For any unit radial superposition u, its bad mass b>=epsilon.",
        "When 2ell+1>K, the older exact RS-moment argument already determines every",
        "1+epsilon >= ||A u||^2 >= 1-(M+1)/epsilon.",
        "the older exact RS moment argument already determines",
        "coefficient, with margin 0,031 on all twelve inputs",
    ]
    for index, quote in enumerate(flipped):
        row = _row(tmp_path, stem="MATH_NOTE", overall="unsound", claims=[_claim(quote, verdict="wrong")])
        with pytest.raises(ValueError, match="symbols"):
            R.import_reviews(tmp_path, [_jsonl(tmp_path / "out" / f"flip_{index}.jsonl", [row])], "j")
    assert not (tmp_path / R.REVIEWS).exists()


def test_import_stores_the_note_wording_of_each_quote(tmp_path: Path) -> None:
    _write(tmp_path, "MATH_NOTE", MATH_NOTE)
    loose = {
        "For any unit radial superposition u its bad mass b <= epsilon":
            "For any unit radial superposition u, its bad mass b<=epsilon",
        "1 - epsilon ≤ ||A u||^2 ≤ 1 + (M−1)*epsilon": "1-epsilon <= ||A u||^2 <= 1+(M-1)*epsilon",
        "with margin 0.031 on all twelve inputs": "with margin 0.031 on all **twelve** inputs",
        "the first listed item holds for every input the second listed item":
            "the first listed item holds for every input\n- the second listed item",
        "holds for every input - the second listed item has": "holds for every input\n- the second listed item has",
    }
    row = _row(tmp_path, stem="MATH_NOTE", overall="needs-work", claims=[_claim(quote) for quote in loose])
    R.import_reviews(tmp_path, [_jsonl(tmp_path / "out" / "loose.jsonl", [row])], "j")
    stored = R.load_reviews(tmp_path)["notes"]["MATH_NOTE"]["claims"]
    assert [claim["quote"] for claim in stored] == list(loose.values())


def _reviewed_repo(root: Path) -> None:
    """FIXTURE_NOTE unsound, EDITED needs-work then edited, SOUND_NOTE sound, OTHER_n unreviewed."""
    _write(root, "FIXTURE_NOTE", FIXTURE_NOTE)
    edited = _dated_note(root, "EDITED", "2026-10-12. REVIEW PENDING.", 1000)
    _dated_note(root, "SOUND_NOTE", "2026-10-13. REVIEW PENDING.", 1000)
    for i in range(3):
        _dated_note(root, f"OTHER_{i}", f"2026-10-0{i + 1}. REVIEW PENDING.", 1000)
    quote = "A result about the edited inputs"
    rows = [
        _row(root, overall="unsound", claims=[
            _claim("We searched 10000 random inputs for a counterexample", verdict="holds"),
            _claim("It holds for all twelve saved inputs, with margin at least 0.031", verdict="wrong",
                   finding="Input 7 has margin -0.002 in the excerpt."),
        ]),
        _row(root, stem="EDITED", claims=[_claim(quote + ".")]),
        _row(root, stem="SOUND_NOTE", overall="sound", claims=[]),
    ]
    R.import_reviews(root, [_jsonl(root / "out" / "rows.jsonl", rows)], "test-judge", today="2026-10-21")
    edited.write_text(edited.read_text(encoding="utf-8") + "\nAn added paragraph.\n", encoding="utf-8")


def test_render_writes_a_note_review_and_the_queue(tmp_path: Path) -> None:
    _reviewed_repo(tmp_path)
    R.render(tmp_path, today="2026-10-21")
    review = (tmp_path / "research/audits/reviews/FIXTURE_NOTE.md").read_text(encoding="utf-8")
    assert review.startswith("# Referee review: FIXTURE_NOTE")
    for needle in ("**unsound**", "It holds for all twelve saved inputs", "wrong", "Question And Result", "Input 7 has margin"):
        assert needle in review
    assert "Stale" in (tmp_path / "research/audits/reviews/EDITED.md").read_text(encoding="utf-8")
    queue = (tmp_path / R.QUEUE).read_text(encoding="utf-8")
    assert "| unsound | 1 |" in queue and "| sound | 1 |" in queue and "| stale | 1 |" in queue
    flagged, rest = queue.split("## Flagged", 1)[1].split("## Stale", 1)
    assert "FIXTURE_NOTE" in flagged and "wrong" in flagged and "EDITED" not in flagged
    stale, upcoming = rest.split("## Next 30", 1)
    assert "EDITED" in stale
    assert [s for s in ("OTHER_0", "OTHER_1", "OTHER_2", "EDITED", "FIXTURE_NOTE", "SOUND_NOTE") if s in upcoming] == [
        "OTHER_0", "OTHER_1", "OTHER_2", "EDITED"]


def test_status_returns_only_flagged_non_stale_reviews(tmp_path: Path) -> None:
    assert R.status(tmp_path)["available"] is False
    _reviewed_repo(tmp_path)
    result = R.status(tmp_path)
    assert result["available"] is True and result["reviewed"] == 3
    assert [f["stem"] for f in result["flagged"]] == ["FIXTURE_NOTE"]
    flagged = result["flagged"][0]
    assert (flagged["overall"], flagged["reviewed_on"]) == ("unsound", "2026-10-21")
    assert flagged["worst_claim"]["verdict"] == "wrong"
    assert result["stale"] == ["EDITED"]
    entry = R.load_reviews(tmp_path)["notes"]["EDITED"]
    assert R.is_stale(tmp_path, "EDITED", entry) is True
    assert R.worst_claim({"claims": []}) is None


def test_cli_round_trip(tmp_path: Path, capsys) -> None:
    _export_fixture(tmp_path)
    root = str(tmp_path)
    assert R.main(["select", "--root", root, "--json"]) == 0
    selected = json.loads(capsys.readouterr().out)
    assert isinstance(selected, list) and [s["stem"] for s in selected][:2] == ["FIXTURE_NOTE", "OTHER_0"]
    assert selected[0] == {"stem": "FIXTURE_NOTE", "path": "research/FIXTURE_NOTE.md", "date": "2026-10-18"}

    out = tmp_path / "batches"
    assert R.main(["export", "--root", root, "--out-dir", str(out), "--limit", "2"]) == 0
    assert str(out / "INSTRUCTIONS.md") in capsys.readouterr().out
    batch = json.loads((out / "batch_01.json").read_text(encoding="utf-8"))
    assert [n["stem"] for n in batch["notes"]] == ["FIXTURE_NOTE", "OTHER_0"]

    answer = _jsonl(out / "out" / "batch_01.jsonl", [_row(tmp_path, overall="unsound", claims=[
        _claim("It holds for all twelve saved inputs, with margin at least 0.031", verdict="wrong")])])
    assert R.main(["import", str(answer), "--root", root, "--judge", "test-judge"]) == 0
    assert "imported 1" in capsys.readouterr().out
    assert R.main(["render", "--root", root]) == 0
    assert (tmp_path / R.QUEUE).exists() and (tmp_path / "research/audits/reviews/FIXTURE_NOTE.md").exists()
    capsys.readouterr()
    assert R.main(["status", "--root", root, "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [f["stem"] for f in payload["flagged"]] == ["FIXTURE_NOTE"]

    assert R.main(["select", "--root", root, "--json"]) == 0
    assert "FIXTURE_NOTE" not in [s["stem"] for s in json.loads(capsys.readouterr().out)]
    assert R.main(["select", "--root", root, "--json", "--include-reviewed", "--prefix", "FIX"]) == 0
    assert [s["stem"] for s in json.loads(capsys.readouterr().out)] == ["FIXTURE_NOTE"]

    _write(tmp_path, "UNLABELLED", "# U\n\n2026-10-20. Local derivations require review.\n\n## Result\n\nSomething.\n")
    cal = tmp_path / "calibration"
    assert R.main(["export", "--root", root, "--out-dir", str(cal), "--note", "UNLABELLED", "--note", "OTHER_3"]) == 0
    batch = json.loads((cal / "batch_01.json").read_text(encoding="utf-8"))
    assert [(n["stem"], n["status"]) for n in batch["notes"]] == [("UNLABELLED", "unlabelled"), ("OTHER_3", "review-pending")]

    bad = _jsonl(out / "out" / "bad.jsonl", [_row(tmp_path, overall="fine")])
    capsys.readouterr()
    assert R.main(["import", str(bad), "--root", root, "--judge", "test-judge"]) == 2
    assert "bad overall verdict" in capsys.readouterr().err

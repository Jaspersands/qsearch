from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.arxiv_watch.judge import export_batches, import_judgements, main, pending
from tools.arxiv_watch.tracks import TRACKS
from tools.arxiv_watch.verdicts import VERDICTS, VERDICTS_FILE, load_verdicts, set_verdict
from tools.arxiv_watch.watch import _load_state, run
from tools.corpus.api import Corpus
from tools.corpus.sources.arxiv import Paper


def _paper(arxiv_id: str, title: str, abstract: str, published: str = "2026-10-15") -> Paper:
    return Paper(arxiv_id, "v1", title, abstract, ["A. Author"], published, published, ["quant-ph"], f"https://arxiv.org/abs/{arxiv_id}")


class FakeClient:
    def __init__(self, papers: list[Paper]) -> None:
        self.papers = papers

    def search(self, query: str, max_results: int = 50, start: int = 0) -> list[Paper]:
        return list(self.papers)


KILL = _paper(
    "2610.11111",
    "Dequantizing Helstrom readout of dihedral coset packets",
    "A classical algorithm for quantum product readout of dihedral coset packets beats every local measurement we tried.",
)
REVIEWED = _paper("2610.33333", "Dequantizing the dihedral coset problem", "An efficient classical algorithm for quantum coset states.")


@pytest.fixture
def watched(fake_repo: Path) -> tuple[Path, Corpus]:
    """A fake checkout whose watch stored two possible kills, one of them with a human verdict."""
    corpus = Corpus(fake_repo)
    corpus.refresh()
    run(fake_repo, FakeClient([KILL, REVIEWED]), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    set_verdict(fake_repo, "2610.33333", "should-cite", "cite it", "human", today="2026-10-20")
    return fake_repo, corpus


def test_export_lists_unreviewed_flags_with_excerpts(watched: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = watched
    state = _load_state(root)
    assert [arxiv_id for arxiv_id, _ in pending(state)] == ["2610.11111", "2610.33333"]  # the verdict is not attached yet
    paths = export_batches(root, tmp_path / "judge", corpus=corpus)
    assert [path.name for path in paths] == ["batch_01.json"]  # three batches asked for, empty ones not written
    batch = json.loads(paths[0].read_text(encoding="utf-8"))
    assert batch["batch"] == 1 and set(batch["verdicts"]) == set(VERDICTS)
    [paper] = batch["papers"]
    assert (paper["arxiv_id"], paper["label"], paper["abstract"]) == ("2610.11111", "possible-kill", KILL.abstract)
    assert set(paper) == {"arxiv_id", "title", "abstract", "label", "cues", "tracks", "nearest"}
    assert set(paper["nearest"][0]) == {"doc_id", "title", "excerpt"}
    assert "Helstrom" in paper["nearest"][0]["excerpt"] and all(len(n["excerpt"]) <= 600 for n in paper["nearest"])
    instructions = (tmp_path / "judge" / "INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert all(f"`{verdict}`" in instructions for verdict in VERDICTS)


def _jsonl(path: Path, rows: list[dict]) -> Path:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def _row(arxiv_id: str, quote: str, quote_from: str = "abstract", verdict: str = "false-alarm") -> dict:
    return {"arxiv_id": arxiv_id, "verdict": verdict, "reason": "the cue is spurious", "quote": quote,
            "quote_from": quote_from, "action": None, "confidence": 0.7}


def test_import_rejects_unknown_verdict_and_non_verbatim_quote(watched: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = watched
    quote = "A classical algorithm for quantum product readout"
    with pytest.raises(ValueError, match="unknown verdict"):
        import_judgements(root, [_jsonl(tmp_path / "a.jsonl", [_row("2610.11111", quote, verdict="maybe")])], "test", corpus=corpus)
    for arxiv_id in ("", "2610.99999"):
        with pytest.raises(ValueError, match="arxiv_id"):
            import_judgements(root, [_jsonl(tmp_path / "b.jsonl", [_row(arxiv_id, quote)])], "test", corpus=corpus)
    assert set(load_verdicts(root)["verdicts"]) == {"2610.33333"}  # a failed import writes nothing

    paraphrase = _row("2610.11111", "a classical algorithm that beats every local measurement")
    short = _row("2610.11111", "classical algorithm for quantum")  # verbatim, but under six words
    for row in (paraphrase, short):
        result = import_judgements(root, [_jsonl(tmp_path / "c.jsonl", [row])], "test", corpus=corpus)
        assert result == {"imported": [], "rejected": [{"arxiv_id": "2610.11111", "why": "quote not found"}]}
    assert set(load_verdicts(root)["verdicts"]) == {"2610.33333"}

    result = import_judgements(root, [_jsonl(tmp_path / "d.jsonl", [_row("2610.11111", quote)])], "test", corpus=corpus, today="2026-10-22")
    assert result == {"imported": ["2610.11111"], "rejected": []}
    entry = load_verdicts(root)["verdicts"]["2610.11111"]
    assert (entry["verdict"], entry["by"], entry["reviewed_on"]) == ("false-alarm", "judge:test", "2026-10-22")
    assert (entry["quote"], entry["quote_from"], entry["confidence"]) == (quote, "abstract", 0.7)
    assert _load_state(root)["papers"]["2610.11111"]["verdict"]["by"] == "judge:test"
    digest = (root / "research" / "audits" / "ARXIV_WATCH.md").read_text(encoding="utf-8")
    assert "| 2610.11111 |" in digest and "judge:test" in digest


def test_judge_never_overwrites_a_human_verdict(watched: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = watched
    kill = _row("2610.33333", "An efficient classical algorithm for quantum coset states", verdict="kill")
    result = import_judgements(root, [_jsonl(tmp_path / "a.jsonl", [kill])], "test", corpus=corpus)
    assert result == {"imported": [], "rejected": [{"arxiv_id": "2610.33333", "why": "human verdict exists"}]}
    entry = load_verdicts(root)["verdicts"]["2610.33333"]
    assert (entry["verdict"], entry["by"]) == ("should-cite", "human")

    # A judge may replace a judge's verdict, but not one recorded under any other name.
    first = _row("2610.11111", "A classical algorithm for quantum product readout", verdict="should-cite")
    import_judgements(root, [_jsonl(tmp_path / "b.jsonl", [first])], "one", corpus=corpus)
    import_judgements(root, [_jsonl(tmp_path / "c.jsonl", [dict(first, verdict="related-only")])], "two", corpus=corpus)
    entry = load_verdicts(root)["verdicts"]["2610.11111"]
    assert (entry["verdict"], entry["by"]) == ("related-only", "judge:two")
    set_verdict(root, "2610.11111", "false-alarm", "read it", "jsands")
    result = import_judgements(root, [_jsonl(tmp_path / "d.jsonl", [first])], "three", corpus=corpus)
    assert result["rejected"] == [{"arxiv_id": "2610.11111", "why": "human verdict exists"}]

    # An entry written by hand without `by` is a human's, not a judge's.
    hand = {"verdict": "false-alarm", "reason": "read it by hand", "action": None, "reviewed_on": "2026-10-21"}
    (root / VERDICTS_FILE).write_text(json.dumps({"verdicts": {"2610.11111": hand}}), encoding="utf-8")
    result = import_judgements(root, [_jsonl(tmp_path / "e.jsonl", [dict(first, verdict="kill")])], "four", corpus=corpus)
    assert result == {"imported": [], "rejected": [{"arxiv_id": "2610.11111", "why": "human verdict exists"}]}
    assert load_verdicts(root)["verdicts"]["2610.11111"] == hand


def test_quote_crossing_a_chunk_boundary_is_rejected(watched: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = watched
    record = _load_state(root)["papers"]["2610.11111"]
    first, second = (near["doc_id"] for near in record["nearest"][:2])
    words_1, words_2 = (corpus.get(doc_id).text[:600].split() for doc_id in (first, second))
    abstract = KILL.abstract.split()
    crossings = [
        (" ".join(abstract[-3:] + words_1[:3]), "abstract"),
        (" ".join(abstract[-3:] + words_1[:3]), first),
        (" ".join(words_1[-3:] + words_2[:3]), first),
        (" ".join(words_1[-3:] + words_2[:3]), second),
    ]
    nearest = {near["doc_id"] for near in record["nearest"]}
    outsider = next(d for d in corpus.doc_ids() if d not in nearest and len(corpus.get(d).text.split()) >= 6)
    crossings.append((" ".join(corpus.get(outsider).text.split()[:6]), outsider))  # verbatim, but not shown to the judge
    for index, (quote, source) in enumerate(crossings):
        result = import_judgements(root, [_jsonl(tmp_path / f"x{index}.jsonl", [_row("2610.11111", quote, source)])], "test", corpus=corpus)
        assert result["rejected"] == [{"arxiv_id": "2610.11111", "why": "quote not found"}], (quote, source)

    inside = _row("2610.11111", " ".join(words_1[2:9]), first)
    assert import_judgements(root, [_jsonl(tmp_path / "ok.jsonl", [inside])], "test", corpus=corpus)["imported"] == ["2610.11111"]


def test_cli_exports_then_imports(watched: tuple[Path, Corpus], tmp_path: Path, capsys) -> None:
    root, _ = watched
    out = tmp_path / "judge"
    assert main(["--root", str(root), "--export", str(out), "--batches", "2"]) == 0
    assert "exported 1 unreviewed flags in 1 batches" in capsys.readouterr().out
    assert (out / "INSTRUCTIONS.md").exists() and (out / "batch_01.json").exists()
    answer = _jsonl(tmp_path / "answer.jsonl", [_row("2610.11111", "A classical algorithm for quantum product readout")])
    assert main(["--root", str(root), "--import", str(answer), "--judge", "cli"]) == 0
    assert "imported 1 verdicts; rejected 0" in capsys.readouterr().out
    assert load_verdicts(root)["verdicts"]["2610.11111"]["by"] == "judge:cli"
    bad = _jsonl(tmp_path / "bad.jsonl", [_row("2610.11111", "x", verdict="maybe")])
    assert main(["--root", str(root), "--import", str(bad), "--judge", "cli"]) == 2

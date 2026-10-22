from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools.arxiv_watch.judge import _confidence, _verbatim, export_batches, import_judgements, main, pending
from tools.arxiv_watch.tracks import TRACKS
from tools.arxiv_watch.verdicts import VERDICTS, VERDICTS_FILE, load_verdicts, set_verdict
from tools.arxiv_watch.watch import _load_state, attach_verdicts, render_digest, run
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


def _flagged_rows(root: Path, heading: str = "Possible kills") -> list[str]:
    digest = (root / "research" / "audits" / "ARXIV_WATCH.md").read_text(encoding="utf-8")
    section = digest.split(f"## {heading}\n")[1].split("\n## ")[0]
    return [line for line in section.splitlines() if line.startswith("| 2")]


def test_a_judge_verdict_leaves_the_flag_listed_until_a_person_decides(watched: tuple[Path, Corpus], tmp_path: Path) -> None:
    from tools.arxiv_watch import watch

    root, corpus = watched
    dismissal = _row("2610.11111", "A classical algorithm for quantum product readout", verdict="false-alarm")
    assert import_judgements(root, [_jsonl(tmp_path / "a.jsonl", [dismissal])], "test", corpus=corpus)["imported"] == ["2610.11111"]
    [row] = [line for line in _flagged_rows(root) if "2610.11111" in line]
    assert "judge: false-alarm" in row
    digest = (root / "research" / "audits" / "ARXIV_WATCH.md").read_text(encoding="utf-8")
    assert "| 2610.11111 |" in digest.split("## Reviewed")[1]  # and the Reviewed table shows who decided
    assert not any("2610.33333" in line for line in _flagged_rows(root))  # a person's verdict moves the flag out

    assert watch.main(["--root", str(root), "--verdict", "2610.11111", "false-alarm", "--reason", "checked it"]) == 0
    assert not any("2610.11111" in line for line in _flagged_rows(root))


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

    # An entry written by hand without `by` is a human's, not a judge's, and so is one written by
    # hand under a versioned or prefixed id.
    hand = {"verdict": "false-alarm", "reason": "read it by hand", "action": None, "reviewed_on": "2026-10-21"}
    for key in ("2610.11111", "arXiv:2610.11111v1", "2610.11111v2"):
        (root / VERDICTS_FILE).write_text(json.dumps({"verdicts": {key: hand}}), encoding="utf-8")
        assert "2610.11111" not in [arxiv_id for arxiv_id, _ in pending(_attached(root))], key
        result = import_judgements(root, [_jsonl(tmp_path / "e.jsonl", [dict(first, verdict="kill")])], "four", corpus=corpus)
        assert result == {"imported": [], "rejected": [{"arxiv_id": "2610.11111", "why": "human verdict exists"}]}, key
        assert load_verdicts(root)["verdicts"] == {"2610.11111": hand}
        digest = render_digest(_attached(root), verdicts=load_verdicts(root)["verdicts"])
        assert "| not stored |" not in digest and "2610.11111" not in digest.split("## Possible kills")[1].split("## ")[0], key


def _attached(root: Path) -> dict:
    state = _load_state(root)
    attach_verdicts(state, load_verdicts(root)["verdicts"])
    return state


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


MATH = _paper(
    "2610.44444",
    "Dequantizing Helstrom readout of dihedral coset packets",
    "A classical algorithm for quantum product readout: we prove the margin satisfies κ ≤ 0.207 against the bound "
    "Ω(n) for every local measurement we tried.",
)


@pytest.fixture
def math_flag(fake_repo: Path) -> tuple[Path, Corpus]:
    """A fake checkout whose watch stored one possible kill with Greek letters and math symbols in its abstract."""
    corpus = Corpus(fake_repo)
    corpus.refresh()
    run(fake_repo, FakeClient([MATH]), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    assert _load_state(fake_repo)["papers"]["2610.44444"]["label"] == "possible-kill"
    return fake_repo, corpus


def test_quote_must_keep_greek_letters_and_math_symbols(math_flag: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = math_flag
    altered = [
        "we prove the margin satisfies κ ≥ 0.207 against the bound",  # inequality flipped
        "we prove the margin satisfies ≤ 0.207 against the bound Ω(n)",  # κ dropped
        "the margin satisfies κ ≤ 0.207 against the bound Θ(n)",  # Ω swapped for Θ
        "the margin satisfies κ ≤ 0.207 against the bound ω(n)",  # big Omega made little omega
        "the margin satisfies κ < 0.207 against the bound Ω(n)",  # ≤ made <
    ]
    for index, quote in enumerate(altered):
        result = import_judgements(root, [_jsonl(tmp_path / f"a{index}.jsonl", [_row("2610.44444", quote)])], "test", corpus=corpus)
        assert result == {"imported": [], "rejected": [{"arxiv_id": "2610.44444", "why": "quote not found"}]}, quote
    assert load_verdicts(root)["verdicts"] == {}

    # Latin letter case, punctuation and spacing may still differ.
    loose = _row("2610.44444", "We prove the margin satisfies κ≤0.207, against the bound Ω( n )")
    assert import_judgements(root, [_jsonl(tmp_path / "ok.jsonl", [loose])], "test", corpus=corpus)["imported"] == ["2610.44444"]


PRE, POST = "we prove that the error of the estimator ", " for every instance in the family"

# (source, quote): the quote changes the maths of the source, so it must not count as verbatim.
CHANGED_MATHS = [
    ("decays as n^{-1/2}", "decays as n^{1/2}"),  # exponent sign dropped
    ("is 10^{-3}", "is 10^{3}"),
    ("is -0.207", "is 0.207"),  # sign dropped
    ("is $2^{-n}$", "is $2^{n}$"),
    ("is $\\Omega(n)$", "is $\\omega(n)$"),  # TeX big Omega made little omega
    ("is Omega(sqrt(n))", "is omega(sqrt(n))"),  # spelled-out Omega made omega
    ("is $\\Theta(n)$", "is $\\Omega(n)$"),
    ("is 2ⁿ", "is 2n"),  # a superscript is an exponent, not a digit pair
    ("is n²", "is n2"),
    ("is 2/3", "is 2.3"),  # slash dropped
    ("needs n! queries", "needs n queries"),  # factorial dropped
    ("is #P-hard", "is P-hard"),
    ("is O(n/\\log n)", "is O(n log n)"),
    ("is O(n log n)", "is O(n) log n"),
    ("is 50%", "is 50"),
    ("is 0.207", "is 0"),  # a decimal is one number
    ("is x_{ij}", "is x{ij}"),
    ("is $2^{n-1}$", "is $2^n - 1$"),  # braces group
    # A one-letter symbol keeps its case (only the word "a" does not).
    ("uses O(n) queries", "uses o(n) queries"),
    ("is N = 2^n", "is n = 2^n"),
    ("is $\\log N$", "is $\\log n$"),
    ("is $\\mathbb{N}$", "is $\\mathbb{n}$"),
    ("has d = 3", "has D = 3"),
    ("is $I - P$", "is $i - P$"),
    # A prime is maths: dropped, added or moved, it changes the formula.
    ("is $W'$", "is $W$"),
    ("is f'(x)", "is f(x)"),
    ("is H' of G", "is H of G"),
    ("is n' >= n", "is n >= n'"),
    ("is f''(x)", "is f'(x)"),
    ("is $\\alpha'$", "is $\\alpha$"),
    ("is (x+y)' here", "is (x+y) here"),
    # A decimal point is part of its number, and a ratio's colon is maths.
    ("is 2.5x", "is 2, 5x"),
    ("is .5", "is 5"),
    ("is 1:2", "is 1 2"),
]

# (source, quote): spacing, Latin letter case in words, sentence punctuation, TeX's math delimiters and
# the spelling of a superscript or a minus sign may differ.
SAME_MATHS = [
    ("is κ ≤ 0.207", "is κ≤0.207,"),
    ("is 2ⁿ", "is 2^n"),
    ("is 2⁻ⁿ", "is 2^{-n}"),
    ("is n¹⁰", "is n^{10}"),
    ("is −0.207", "is -0.207"),
    ("is $\\Omega(n)$", "is \\(\\Omega(n)\\)"),
    ("is $O(n\\,\\log n)$", "is $O(n \\log n)$"),
    ("is “hard” here", 'is "hard" here'),
    ("is **hard** here", "is hard here"),
    ("is ‘hard’ here", "is 'hard' here"),
    ("is ``hard'' here", 'is "hard" here'),
    ("is A hard one", "is a hard one"),  # the word a, not a symbol
    ("is $(I-O(\\log n))$ bits", "is (I-O(\\log n)) bits"),  # with or without TeX's $
    ("is $O(n)$ bits", "is O(n)$ bits"),  # or from inside a formula
    ("is Shor's and the players' choice", "is Shor’s and the players’ choice"),  # apostrophes are not primes
    ("is Bayes' rule", "is Bayes rule"),
    ("is O'Donnell's bound", "is O Donnell's bound"),  # nor is one after a one-letter word inside a name
    ("is ``P'' here", 'is "P" here'),  # a quoted letter keeps no prime
    ("is f′(x)", "is f'(x)"),  # an ASCII prime is a prime
    ("is 2.9x", "is 2.9 x"),
    ("is $a \\quad b \\qquad c$", "is $a b c$"),  # TeX spacing commands
    ("is $a\\hspace{1em}b$", "is $a b$"),
    ("is fast—so", "is fast, so"),  # an em dash between clauses is punctuation
    ("is fast---so", "is fast so"),
    ("is fast -- so", "is fast so"),
    ("is Erdős--Rényi", "is Erdős–Rényi"),  # a range or name-pair dash is one dash however it is typed
]


@pytest.mark.parametrize(("source", "quote"), CHANGED_MATHS, ids=[quote for _, quote in CHANGED_MATHS])
def test_quote_that_changes_the_maths_is_not_verbatim(source: str, quote: str) -> None:
    assert _verbatim(PRE + source + POST, PRE + source + POST)
    assert not _verbatim(PRE + quote + POST, PRE + source + POST)


@pytest.mark.parametrize(("source", "quote"), SAME_MATHS, ids=[quote for _, quote in SAME_MATHS])
def test_quote_may_differ_in_spacing_case_and_sentence_punctuation(source: str, quote: str) -> None:
    assert _verbatim(PRE.upper() + quote + POST, PRE + source + POST)


def test_quote_may_not_start_or_end_inside_a_formula() -> None:
    source = "we find the margin is -0.207 for every instance and it decays as n^{-1/2} in the family"
    assert _verbatim("the margin is -0.207 for every instance", source)
    assert not _verbatim("0.207 for every instance and it decays", source)  # the sign is cut off
    assert not _verbatim("for every instance and it decays as n", source)  # the exponent is cut off
    assert _verbatim("for every instance and it decays as n^{-1/2}", source)


# (source, quote): the quote appears verbatim in the source but starts or ends inside a formula.
FORMULA_CUTS = [
    ("so the bound is -n log n for every instance", "n log n for every instance"),  # a sign before a letter
    ("we show that the algorithm needs n! queries", "we show that the algorithm needs n"),  # a factorial
    ("we show that the algorithm needs 5! queries", "we show that the algorithm needs 5"),
    ("we show that the algorithm needs n/2 queries", "we show that the algorithm needs n"),  # a fraction bar
    ("we prove that it fails on 2/3 of the instances", "we prove that it fails on 2"),
    ("it fails on 2/3 of the instances in the family", "3 of the instances in the family"),
    ("we prove that it fails on 50% of the instances", "we prove that it fails on 50"),  # a percent sign
    ("we prove that the ratio is 1 - 1/e here", "we prove that the ratio is 1"),  # a minus between terms
    ("we show that it gains a factor of 3 × 10^5 here", "we show that it gains a factor of 3"),  # a product
    ("we show that it gains a factor of 3 \\times 10^5 here", "we show that it gains a factor of 3"),
    ("we show that it gains a factor of 3 \\cdot 10^5 here", "we show that it gains a factor of 3"),
    ("we prove the claim when n = 5 for all instances", "we prove the claim when n"),  # an equation
    ("only √n queries suffice for every instance here", "n queries suffice for every instance here"),  # a root
    ("only \\sqrt n queries suffice for every instance here", "n queries suffice for every instance here"),
    ("about n \\log n queries suffice for every instance here", "n queries suffice for every instance here"),  # a function
    ("a ratio of $(1-1/e)$ for every instance in the family", "e)$ for every instance in the family"),
    ("we find that only .5 of the instances are hard", "5 of the instances are hard"),  # a leading decimal point
    ("we find a ratio of 1:2 of the instances are hard", "2 of the instances are hard"),  # a ratio
    ("we prove that the subgroup H' of G is normal", "we prove that the subgroup H"),  # a prime
    ("here we give a new quantum-inspired algorithm", "here we give a new quantum"),  # half a hyphenated word
]


@pytest.mark.parametrize(("source", "quote"), FORMULA_CUTS, ids=[quote for _, quote in FORMULA_CUTS])
def test_quote_that_cuts_a_formula_is_not_verbatim(source: str, quote: str) -> None:
    assert quote.replace("$", "") in source.replace("$", "") or quote in source
    assert not _verbatim(quote, source)


def test_quote_may_start_after_a_clause_dash_and_end_before_an_exclamation() -> None:
    source = "it is fast—5 times faster than belief propagation on every instance, and it works!"
    assert _verbatim("5 times faster than belief propagation on every instance", source)
    assert _verbatim("on every instance, and it works", source)


def test_quote_must_match_whole_words_and_count_six_of_them() -> None:
    source = "it is impossible to efficiently simulate the circuit family, so the margin satisfies κ ≤ 0.207 here"
    assert _verbatim("impossible to efficiently simulate the circuit family", source)
    assert not _verbatim("possible to efficiently simulate the circuit family", source)  # inside "impossible"
    assert not _verbatim("the margin satisfies κ ≤ 0.207", source)  # five words; "≤" is not a word
    assert _verbatim("so the margin satisfies κ ≤ 0.207", source)


def test_batch_shows_symbols_as_stored_so_a_copied_quote_is_accepted(math_flag: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = math_flag
    [path] = export_batches(root, tmp_path / "judge", corpus=corpus)
    raw = path.read_text(encoding="utf-8")
    assert "κ ≤ 0.207" in raw and "\\u03ba" not in raw
    quote = re.search(r"we prove the margin satisfies [^\"]*? against the bound", raw).group(0)
    result = import_judgements(root, [_jsonl(tmp_path / "copied.jsonl", [_row("2610.44444", quote)])], "test", corpus=corpus)
    assert result == {"imported": ["2610.44444"], "rejected": []}


@pytest.mark.parametrize(
    ("value", "stored"),
    [(0.7, 0.7), ("0.3", 0.3), (1.5, 1.0), (-0.2, 0.0), (1, 1.0), ("nan", None), (float("nan"), None), ("inf", None),
     (float("-inf"), None), (True, None), (False, None), ("sure", None), (None, None), (10**400, None), (-(10**400), None)],
)
def test_confidence_is_a_clamped_finite_number_or_null(value, stored) -> None:
    assert _confidence(value) == stored


def test_a_huge_integer_confidence_is_stored_as_null(watched: tuple[Path, Corpus], tmp_path: Path, capsys) -> None:
    root, _ = watched
    row = json.dumps(_row("2610.11111", "A classical algorithm for quantum product readout")).replace("0.7", "1" + "0" * 400)
    (tmp_path / "huge.jsonl").write_text(row + "\n", encoding="utf-8")
    assert main(["--root", str(root), "--import", str(tmp_path / "huge.jsonl"), "--judge", "t"]) == 0
    assert "imported 1 verdicts" in capsys.readouterr().out
    assert load_verdicts(root)["verdicts"]["2610.11111"]["confidence"] is None


def test_bare_nan_confidence_is_stored_as_null(watched: tuple[Path, Corpus], tmp_path: Path) -> None:
    root, corpus = watched
    row = json.dumps(_row("2610.11111", "A classical algorithm for quantum product readout")).replace("0.7", "NaN")
    (tmp_path / "nan.jsonl").write_text(row + "\n", encoding="utf-8")
    assert import_judgements(root, [tmp_path / "nan.jsonl"], "test", corpus=corpus)["imported"] == ["2610.11111"]
    assert load_verdicts(root)["verdicts"]["2610.11111"]["confidence"] is None


def _excerpt_row(root: Path, corpus: Corpus, arxiv_id: str = "2610.11111") -> dict:
    """A row whose quote comes from the first nearest record's excerpt, so checking it needs the corpus."""
    doc_id = _load_state(root)["papers"][arxiv_id]["nearest"][0]["doc_id"]
    return _row(arxiv_id, " ".join(corpus.get(doc_id).text[:600].split()[2:9]), doc_id)


def test_excerpt_quotes_are_checked_against_the_excerpt_the_judge_was_shown(
    watched: tuple[Path, Corpus], tmp_path: Path, monkeypatch
) -> None:
    from tools.arxiv_watch import judge

    root, corpus = watched
    out = tmp_path / "judge"
    [batch] = export_batches(root, out, corpus=corpus)
    shown = json.loads(batch.read_text(encoding="utf-8"))["papers"][0]["nearest"][0]
    faithful = _row("2610.11111", " ".join(shown["excerpt"].split()[2:9]), shown["doc_id"])
    later = "This record was rewritten after the export and says something else entirely now."
    monkeypatch.setattr(judge, "_excerpt", lambda corpus, doc_id: later)  # the record changes before the import
    (out / "out").mkdir()
    rows = _jsonl(out / "out" / "batch_01.jsonl", [faithful])
    assert import_judgements(root, [rows], "test", corpus=corpus)["imported"] == ["2610.11111"]
    unseen = _row("2610.11111", later, shown["doc_id"])  # verbatim in today's text, which the judge never saw
    rows = _jsonl(out / "out" / "batch_01.jsonl", [unseen])
    assert import_judgements(root, [rows], "test", corpus=corpus)["rejected"] == [{"arxiv_id": "2610.11111", "why": "quote not found"}]
    other = json.loads(batch.read_text(encoding="utf-8"))["papers"][0]["nearest"][1]["doc_id"]
    misnamed = {**faithful, "quote_from": other}  # the right words credited to the next record shown
    rows = _jsonl(out / "out" / "batch_01.jsonl", [misnamed])
    assert import_judgements(root, [rows], "test", corpus=corpus)["rejected"] == [{"arxiv_id": "2610.11111", "why": "quote not found"}]
    # Without its batch file beside the output, a row is checked against today's text.
    assert import_judgements(root, [_jsonl(tmp_path / "loose.jsonl", [unseen])], "test", corpus=corpus)["imported"] == ["2610.11111"]


def test_abstract_quotes_are_checked_against_the_stored_abstract(
    watched: tuple[Path, Corpus], tmp_path: Path
) -> None:
    root, corpus = watched
    out = tmp_path / "judge"
    export_batches(root, out, corpus=corpus)
    state = _load_state(root)
    state["papers"]["2610.11111"]["abstract"] = "A second version replaced the abstract with entirely different words after the export."
    (root / "research" / "audits" / "arxiv_collisions.json").write_text(json.dumps(state), encoding="utf-8")
    (out / "out").mkdir()
    shown = _row("2610.11111", "A classical algorithm for quantum product readout")
    assert import_judgements(root, [_jsonl(out / "out" / "batch_01.jsonl", [shown])], "test", corpus=corpus)["rejected"] == [{"arxiv_id": "2610.11111", "why": "quote not found"}]
    unseen = _row("2610.11111", "replaced the abstract with entirely different words")
    result = import_judgements(root, [_jsonl(out / "out" / "batch_01.jsonl", [unseen])], "test", corpus=corpus)
    assert result["imported"] == ["2610.11111"]


def test_only_a_batch_named_like_the_output_is_read_and_a_broken_one_stops_the_import(
    watched: tuple[Path, Corpus], tmp_path: Path
) -> None:
    root, corpus = watched
    row = _row("2610.11111", "A classical algorithm for quantum product readout")
    (tmp_path / "results.json").write_text("[1, 2]", encoding="utf-8")  # not a batch, and not named like one
    (tmp_path / "out").mkdir()
    assert import_judgements(root, [_jsonl(tmp_path / "out" / "results.jsonl", [row])], "test", corpus=corpus)["imported"] == ["2610.11111"]
    before = (root / VERDICTS_FILE).read_bytes()
    (tmp_path / "batch_02.json").write_text('{"batch": 2}', encoding="utf-8")
    with pytest.raises(ValueError, match="not a batch file"):
        import_judgements(root, [_jsonl(tmp_path / "out" / "batch_02.jsonl", [row])], "test", corpus=corpus)
    (tmp_path / "batch_02.json").write_text('{"papers": [', encoding="utf-8")
    with pytest.raises(ValueError):
        import_judgements(root, [_jsonl(tmp_path / "out" / "batch_02.jsonl", [row])], "test", corpus=corpus)
    assert (root / VERDICTS_FILE).read_bytes() == before


def test_import_writes_nothing_when_a_later_row_fails(watched: tuple[Path, Corpus], tmp_path: Path, monkeypatch, capsys) -> None:
    import sqlite3

    from tools.arxiv_watch import judge

    root, corpus = watched
    verdicts, collisions = (root / VERDICTS_FILE).read_bytes(), (root / "research/audits/arxiv_collisions.json").read_bytes()
    good = _row("2610.11111", "A classical algorithm for quantum product readout")

    # A bad second row stops the import before the first is written.
    rows = _jsonl(tmp_path / "bad.jsonl", [good, _row("2610.11111", "x", verdict="maybe")])
    with pytest.raises(ValueError, match="unknown verdict"):
        import_judgements(root, [rows], "test", corpus=corpus)

    # So does a corpus that cannot be opened while the second row's excerpt quote is checked.
    def locked(root):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr(judge, "_corpus", locked)
    rows = _jsonl(tmp_path / "locked.jsonl", [good, _excerpt_row(root, corpus)])
    with pytest.raises(sqlite3.OperationalError):
        import_judgements(root, [rows], "test")
    assert main(["--root", str(root), "--import", str(rows), "--judge", "test"]) == 2
    assert capsys.readouterr().err == "error: database is locked\n"
    assert (root / VERDICTS_FILE).read_bytes() == verdicts
    assert (root / "research/audits/arxiv_collisions.json").read_bytes() == collisions


def test_import_keeps_what_was_written_while_it_ran(watched: tuple[Path, Corpus], tmp_path: Path, monkeypatch) -> None:
    from tools.arxiv_watch import judge

    root, corpus = watched
    path = root / "research/audits/arxiv_collisions.json"
    gap = {"track": "dcp", "since": "2026-09-01", "until": "2026-09-10", "found_on": "2026-10-23"}

    def busy_corpus(root):  # another writer records a person's verdict and a gap while the rows are checked
        set_verdict(root, "2610.11111", "false-alarm", "read it", "human", today="2026-10-23")
        state = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps({**state, "gaps": [gap]}), encoding="utf-8")
        return corpus

    monkeypatch.setattr(judge, "_corpus", busy_corpus)
    rows = _jsonl(tmp_path / "rows.jsonl", [_excerpt_row(root, corpus)])
    result = import_judgements(root, [rows], "test")
    assert result == {"imported": [], "rejected": [{"arxiv_id": "2610.11111", "why": "human verdict exists"}]}
    assert load_verdicts(root)["verdicts"]["2610.11111"]["by"] == "human"
    assert json.loads(path.read_text(encoding="utf-8"))["gaps"] == [gap]

    path.write_text(json.dumps({**json.loads(path.read_text(encoding="utf-8")), "gaps": []}), encoding="utf-8")
    monkeypatch.setattr(judge, "_corpus", lambda root: (path.write_text(
        json.dumps({**json.loads(path.read_text(encoding="utf-8")), "gaps": [gap]}), encoding="utf-8"), corpus)[1])
    set_verdict(root, "2610.11111", "related-only", "a judge's", "judge:old")
    result = import_judgements(root, [rows], "test")
    assert result == {"imported": ["2610.11111"], "rejected": []}
    stored = _load_state(root)
    assert stored["gaps"] == [gap] and stored["papers"]["2610.11111"]["verdict"]["by"] == "judge:test"


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


def test_cli_exits_2_on_unusable_input(watched: tuple[Path, Corpus], tmp_path: Path, capsys) -> None:
    root, _ = watched
    texts = {"string.jsonl": '"just a string"\n', "list_id.jsonl": '{"arxiv_id": ["x"], "verdict": "kill"}\n',
             "broken.jsonl": "{not json\n"}
    for name, text in texts.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    for name in [*texts, "no_such_file.jsonl"]:  # an unmatched shell glob passes its pattern through
        assert main(["--root", str(root), "--import", str(tmp_path / name), "--judge", "t"]) == 2, name
        assert capsys.readouterr().err.startswith("error: "), name
    (tmp_path / "a_file").write_text("", encoding="utf-8")
    assert main(["--root", str(root), "--export", str(tmp_path / "a_file")]) == 2
    assert capsys.readouterr().err.startswith("error: ")
    with pytest.raises(SystemExit) as stop:
        main(["--root", str(root), "--export", str(tmp_path / "out"), "--batches", "0"])
    assert stop.value.code == 2 and "--batches" in capsys.readouterr().err
    assert set(load_verdicts(root)["verdicts"]) == {"2610.33333"}

@pytest.mark.parametrize('source,quote', [('O(kN)','O(kn)'),('O(Nd)','O(nd)'),('Ω(nT)','Ω(Nt)'),('O(εN)','O(εn)'),('N2','n2'),('$Wd$','$wD$'),('SU(2)','su(2)'),('O(Log n)','O(log n)')])
def test_glued_symbol_case_is_not_prose(source, quote) -> None:
    assert not _verbatim(PRE + quote + POST, PRE + source + POST)


@pytest.mark.parametrize('source,quote', [('2n qubits suffice for every input in this family','n qubits suffice for every input in this family'),('3k queries suffice for every input in this family','k queries suffice for every input in this family'),('we prove the error is below 1e-6 for every input','we prove the error is below 1'),('2D<d is equivalent for every instance in this family','D<d is equivalent for every instance in this family')])
def test_glued_product_or_number_cannot_be_cut(source, quote) -> None:
    assert not _verbatim(quote, source)


@pytest.mark.parametrize('prefix', ['Quantum walks are powerful - ', 'Results: - ', 'Results:\n* ', '### ', 'Earlier result. ### '])
def test_prose_bullet_or_heading_is_not_a_formula(prefix) -> None:
    quote = 'we show the map is unitary for every input'
    assert _verbatim(quote, prefix + quote + '.')
    assert not _verbatim('y is enough for every input in the family', 'x - y is enough for every input in the family')


def test_code_backticks_do_not_consume_the_next_prime() -> None:
    source = "Checked by `theorems/coset_pgm.py`. The map W' is unitary and the bound holds for all inputs."
    assert _verbatim("The map W' is unitary and the bound holds for all inputs", source)
    assert not _verbatim('The map W is unitary and the bound holds for all inputs', source)


def test_reused_export_directory_is_rejected_without_overwriting(watched, tmp_path) -> None:
    root, corpus = watched
    out = tmp_path/'judge'
    paths = export_batches(root,out,corpus=corpus)
    before = paths[0].read_bytes()
    with pytest.raises(ValueError, match='fresh|empty|already|reuse'):
        export_batches(root,out,n_batches=1,corpus=corpus)
    assert paths[0].read_bytes() == before


def test_relative_output_uses_exported_excerpt(watched,tmp_path,monkeypatch) -> None:
    from tools.arxiv_watch import judge
    root, corpus = watched
    out = tmp_path/'judge'
    [batch] = export_batches(root,out,corpus=corpus)
    near = json.loads(batch.read_text())['papers'][0]['nearest'][0]
    row = _row('2610.11111',' '.join(near['excerpt'].split()[2:9]),near['doc_id'])
    (out/'out').mkdir()
    _jsonl(out/'out/batch_01.jsonl',[row])
    monkeypatch.setattr(judge,'_excerpt',lambda *args:'different content now')
    monkeypatch.chdir(out/'out')
    assert import_judgements(root,[Path('batch_01.jsonl')],'test',corpus=corpus)['imported'] == ['2610.11111']


def test_tampered_batch_cannot_supply_quote_evidence(watched,tmp_path) -> None:
    root, corpus = watched
    out = tmp_path/'judge'
    [batch] = export_batches(root,out,corpus=corpus)
    data = json.loads(batch.read_text())
    fabricated = 'This invented sentence refutes all the project claims entirely.'
    data['papers'][0]['abstract'] = fabricated
    batch.write_text(json.dumps(data))
    (out/'out').mkdir()
    row = _row('2610.11111',fabricated)
    with pytest.raises(ValueError, match='changed|integrity|hash'):
        import_judgements(root,[_jsonl(out/'out/batch_01.jsonl',[row])],'test',corpus=corpus)


def test_truncated_text_is_marked_and_quote_cannot_end_at_cut(watched,tmp_path) -> None:
    from tools.arxiv_watch import judge
    root, corpus = watched
    state = _load_state(root)
    prefix = ' '.join(f'uniqueword{i}' for i in range(300))
    state['papers']['2610.11111']['abstract'] = prefix[:1500]
    state['papers']['2610.11111'].pop('abstract_complete',None)
    (root/'research/audits/arxiv_collisions.json').write_text(json.dumps(state))
    [batch] = export_batches(root,tmp_path/'judge',corpus=corpus)
    item = json.loads(batch.read_text())['papers'][0]
    assert item['abstract'].endswith('[truncated]')
    quote = ' '.join(prefix[:1500].split()[-10:])
    assert not _verbatim(quote,item['abstract'])
    class Doc:
        text = prefix
    class CorpusStub:
        def get(self, _): return Doc()
    excerpt = judge._excerpt(CorpusStub(),'id')
    assert excerpt.endswith('[truncated]')
    assert not _verbatim(' '.join(excerpt.removesuffix(' [truncated]').split()[-10:]),excerpt)

@pytest.mark.parametrize('source,quote', [('is $WE$ here','is $we$ here'),('uses O(ABC) queries','uses O(abc) queries'),('is $Alpha$ here','is $alpha$ here'),('has x - delta here','has x delta here')])
def test_adversarial_math_case_and_named_operand(source,quote) -> None:
    assert not _verbatim(PRE + quote + POST, PRE + source + POST)

@pytest.mark.parametrize('formula', ['$AB - CD$', 'AB - CD', '$alpha - beta$'])
def test_subtraction_is_never_clause_punctuation(formula) -> None:
    source = 'We prove ' + formula + ' is the exact bound today.'
    assert not _verbatim(source.replace(' - ', ' '),source)

@pytest.mark.parametrize('left,right', [('$','$'),('$$','$$'),(r'\[',r'\]'),(r'\(',r'\)')])
@pytest.mark.parametrize('dash', ['-', '–', '—', '--', '---', '―'])
def test_explicit_math_never_drops_clause_style_dashes(left,right,dash) -> None:
    source = f'We prove {left}ab {dash} cd{right} is the exact bound today.'
    quote = f'We prove {left}ab cd{right} is the exact bound today.'
    assert _verbatim(source,source)
    assert not _verbatim(quote,source)

@pytest.mark.parametrize('operands', [('AB','CD'),('x','y'),('α','β'),('2','3'),('ab','cd')])
@pytest.mark.parametrize('dash', ['-', '–', '—', '--', '---'])
def test_bare_symbol_operands_keep_their_dash(operands,dash) -> None:
    left,right=operands
    source=f'We prove {left} {dash} {right} is the exact bound today.'
    assert _verbatim(source,source)
    assert not _verbatim(source.replace(f' {dash} ',' '),source)


@pytest.mark.parametrize('formula,changed', [('$$\n- x + y\n$$','$$\nx + y\n$$'),(r'$AB ** CD$',r'$AB CD$'),('$$\n# P\n$$','$$\nP\n$$')])
def test_explicit_math_is_not_markdown(formula,changed) -> None:
    source=f'We prove {formula} is the exact bound today.'
    assert _verbatim(source,source)
    assert not _verbatim(f'We prove {changed} is the exact bound today.',source)

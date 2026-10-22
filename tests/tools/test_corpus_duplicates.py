from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse as sp

from tests.tools.conftest import HANDOFF, NEGATIVES, NOTE, QUARANTINED
from tests.tools.test_corpus_mcp import _call
from tools.corpus.api import Corpus
from tools.corpus.cli import main
from tools.corpus.duplicates import (
    DraftError,
    check_claim,
    claim_report,
    draft_claim,
    draft_claims,
    near_duplicates,
    pair_report,
)
from tools.corpus.mcp_server import create_server

HELSTROM = "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"
PLATYPUS = "negative:NEG-NEW-PLATYPUS-SIEVE"
UNIQUE = {
    "id": "NEG-NEW-PLATYPUS-SIEVE",
    "applies_to": ["HSP"],
    "claim": "A platypus sieve over echidna coset states recovers the hidden shift in polynomial time.",
    "reason_invalid": "The platypus sieve collapses to Kuperberg merging, whose cost is subexponential.",
    "lesson": "Charge the merging cost of every sieve.",
}
# The Helstrom record's claim with two words changed ("readout" -> "measurement", "dominates" -> "beats").
NEAR_CLAIM = "Local Helstrom measurement of each dihedral coset packet beats every product X-basis readout."

DUP_A = {
    "id": "NEG-DUP-A",
    "applies_to": ["HSP"],
    "claim": "A wombat sieve over abelian coset states recovers the hidden shift in polynomial time.",
    "reason_invalid": "The wombat sieve collapses to Kuperberg merging, whose cost is subexponential.",
    "lesson": "Charge the merging cost of every sieve.",
}
DUP_B = {
    "id": "NEG-DUP-B",
    "applies_to": ["HSP"],
    "claim": "A wombat sieve over abelian coset states recovers the hidden shift in quasi-polynomial time.",
    "reason_invalid": "The wombat sieve collapses to Kuperberg merging, whose cost is subexponential.",
    "lesson": "Charge the merging cost of every sieve.",
}

# Three parameter sweeps of ten records each: identical text, ids differing in a trailing number.
SWEEPS = {
    "NEG-GOPPA-SCALE-M6-T3-N48-0": "Goppa syndrome decoding at scale stays above the information set decoding baseline.",
    "NEG-POLAR-SHAPING-N32": "Polar successive cancellation shaping matches the quantum Gibbs sampler on every frozen set.",
    "NEG-LATTICE-BABAI-DIM": "Babai nearest plane rounding recovers the planted lattice vector below the radius bound.",
}
RESTATEMENT = [
    {
        "id": "NEG-ECHIDNA-READOUT-BOUND",
        "claim": "Echidna collective readout of platypus packets beats every adaptive product readout.",
        "reason_invalid": "A certified semidefinite bound caps echidna collective readout at the adaptive value.",
        "lesson": "Bound collective platypus readout before claiming a gap.",
    },
    {
        "id": "NEG-ECHIDNA-COLLECTIVE-LIMIT",
        "claim": "Collective echidna readout of platypus packets beats adaptive product readout.",
        "reason_invalid": "A certified semidefinite bound caps collective echidna readout at the adaptive value.",
        "lesson": "Bound collective platypus readout before claiming any gap.",
    },
]


# The closest record to WOMBAT_DRAFT is padded with stop words: TF-IDF ignores them, but BM25
# ranks the long record below thirty short siblings, so the fused search's top ten leave it out.
WOMBAT_CLAIM = "A wombat sieve over abelian coset states recovers the hidden shift in polynomial time."
WOMBAT_REASON = "The wombat sieve collapses to Kuperberg merging, whose cost is subexponential."
WOMBAT_DRAFT = f"{WOMBAT_CLAIM.replace('polynomial', 'quasi-polynomial')} {WOMBAT_REASON}"
WOMBAT_TARGET = {
    "id": "NEG-WOMBAT-TARGET",
    "claim": WOMBAT_CLAIM,
    "reason_invalid": f"{WOMBAT_REASON} " + " ".join(["the of and to in is it that for on with as by at from"] * 200),
    "lesson": "Charge merging.",
}
WOMBAT_CROWD = [
    {
        "id": f"NEG-WOMBAT-SWEEP-{i}",
        "claim": f"A wombat sieve over abelian coset states at size {i} recovers the hidden shift.",
        "reason_invalid": "The wombat sieve collapses to Kuperberg merging.",
        "lesson": "Sweep.",
    }
    for i in range(30)
] + [
    {
        "id": f"NEG-FILLER-{i}",
        "claim": f"Filler record {i} about lattice zebra {i} and platypus graphs.",
        "reason_invalid": f"Unrelated filler reason {i} with echidna lemmas.",
        "lesson": "Filler.",
    }
    for i in range(80)
]


def _corpus_with(fake_repo: Path, extra: list[dict]) -> Corpus:
    path = fake_repo / "research" / "registry" / "negative_results.json"
    path.write_text(json.dumps(NEGATIVES + extra, indent=2), encoding="utf-8")
    corpus = Corpus(fake_repo)
    corpus.refresh()
    return corpus


def _sweep_records() -> list[dict]:
    return [
        {"id": f"{family}-{i}", "claim": claim, "reason_invalid": "Sweep point.", "lesson": "Sweep."}
        for family, claim in SWEEPS.items()
        for i in range(1, 11)
    ]


def test_near_duplicates_finds_the_planted_pair(fake_repo: Path) -> None:
    corpus = _corpus_with(fake_repo, [DUP_A, DUP_B])
    pairs = near_duplicates(corpus)
    assert (pairs[0].a, pairs[0].b) == ("negative:NEG-DUP-A", "negative:NEG-DUP-B")
    assert pairs[0].score >= 0.8
    assert pairs[0].title_a == DUP_A["claim"]
    assert not any(HELSTROM in (pair.a, pair.b) for pair in pairs)
    assert near_duplicates(corpus, threshold=1.01) == []


def test_per_family_cap_keeps_a_true_restatement_visible(fake_repo: Path) -> None:
    corpus = _corpus_with(fake_repo, _sweep_records() + RESTATEMENT)
    restatement = ("negative:NEG-ECHIDNA-COLLECTIVE-LIMIT", "negative:NEG-ECHIDNA-READOUT-BOUND")
    crowded = near_duplicates(corpus, limit=10)
    assert restatement not in [(pair.a, pair.b) for pair in crowded]  # siblings fill the top 10
    capped = near_duplicates(corpus, limit=10, per_family=2)
    assert restatement in [(pair.a, pair.b) for pair in capped]
    assert len(capped) == 3 * 2 + 1


def test_pair_report_counts_the_pairs_cut_by_the_limit(fake_repo: Path) -> None:
    corpus = _corpus_with(fake_repo, _sweep_records() + RESTATEMENT)
    report = pair_report(corpus, limit=10)
    assert len(report.pairs) == 10
    assert report.total == 3 * 45 + 1  # every sibling pair of three ten-record sweeps, plus the restatement
    assert report.documents == len(NEGATIVES) + 1 + 30 + 2  # retained, quarantined, sweeps, restatement
    assert pair_report(corpus, limit=10, per_family=2).total == 3 * 2 + 1
    assert pair_report(corpus, limit=-1).pairs == []
    assert pair_report(corpus, kind="nosuchkind").documents == 0


def test_pair_report_orders_ties_by_id_so_the_family_cap_keeps_the_lowest_ids(fake_repo: Path) -> None:
    # Ids -1 to -9 differ in one digit, which TF-IDF ignores, so their texts score 1.000 together.
    # They are filed in reverse, so the index order is not the id order.
    corpus = _corpus_with(fake_repo, [r for r in _sweep_records() if not r["id"].endswith("-10")][::-1])
    report = pair_report(corpus, threshold=0.99, limit=1000)
    assert report.total == 3 * 36 and {pair.score for pair in report.pairs} == {1.0}
    assert [(p.a, p.b) for p in report.pairs] == sorted((p.a, p.b) for p in report.pairs)
    capped = pair_report(corpus, threshold=0.99, limit=1000, per_family=2)
    expected = [(f"negative:{family}-1", f"negative:{family}-{n}") for family in sorted(SWEEPS) for n in (2, 3)]
    assert [(p.a, p.b) for p in capped.pairs] == expected


def _fixed_matrix(corpus: Corpus, monkeypatch, ids: list[str], dense: list[list[float]]) -> None:
    sims = sp.csr_matrix(np.array(dense, dtype=np.float32))
    monkeypatch.setattr(corpus, "matrix", lambda kind="negative": (ids, sims))


def test_pair_report_rounds_scores_to_four_places_before_ordering(corpus: Corpus, monkeypatch) -> None:
    # 0.99999 and 0.99996 both show as 1.000, so the pairs tie and go by id, not by the raw score.
    ids = ["negative:NEG-C", "negative:NEG-A", "negative:NEG-B"]
    _fixed_matrix(corpus, monkeypatch, ids, [[1, 0.99999, 0.5], [0.99999, 1, 0.99996], [0.5, 0.99996, 1]])
    pairs = [(p.a, p.b, p.score) for p in pair_report(corpus, threshold=0.9).pairs]
    assert pairs == [("negative:NEG-A", "negative:NEG-B", 1.0), ("negative:NEG-A", "negative:NEG-C", 1.0)]


def test_a_pair_shown_as_1_000_counts_at_threshold_1(corpus: Corpus, monkeypatch) -> None:
    # float32 cosines of identical texts can be 0.9999997: shown as 1.000, they were missed at --threshold 1.
    ids = ["negative:NEG-A", "negative:NEG-B", "negative:NEG-C"]
    _fixed_matrix(corpus, monkeypatch, ids, [[1, 0.9999997, 0.99994], [0.9999997, 1, 0.5], [0.99994, 0.5, 1]])
    assert [(p.a, p.b, p.score) for p in pair_report(corpus, threshold=1).pairs] == [
        ("negative:NEG-A", "negative:NEG-B", 1.0)
    ]
    assert [p.score for p in pair_report(corpus, threshold=0.9999).pairs] == [1.0, 0.9999]


def test_a_claim_shown_as_1_000_matches_at_threshold_1(corpus: Corpus, monkeypatch) -> None:
    doc = corpus.get(HELSTROM)
    text = f"{doc.title} {doc.text}"
    state = corpus._state()
    exact = state.scores
    monkeypatch.setattr(state, "scores", lambda query: exact(query) * np.float32(1 - 3e-7))
    assert float(state.scores(text)[np.flatnonzero(state.rowids == corpus.store.row_of(HELSTROM))[0]]) < 1
    shown = claim_report(corpus, text, threshold=0.99).matches
    assert (shown[0].doc_id, shown[0].score) == (HELSTROM, 1.0)
    assert [hit.doc_id for hit in claim_report(corpus, text, threshold=1).matches] == [HELSTROM]


@pytest.fixture
def corpus(fake_repo: Path) -> Corpus:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    return corpus


def test_check_claim_returns_cosine_scored_negatives_above_threshold(corpus: Corpus) -> None:
    hits = check_claim(corpus, NEAR_CLAIM)
    assert hits[0].doc_id == HELSTROM
    assert 0.6 <= hits[0].score <= 1.0
    assert all(hit.kind == "negative" and hit.score >= 0.6 for hit in hits)
    assert check_claim(corpus, "zebrafish migration") == []


def test_check_claim_scores_every_negative_not_only_the_fused_top_ten(fake_repo: Path) -> None:
    corpus = _corpus_with(fake_repo, [WOMBAT_TARGET, *WOMBAT_CROWD])
    target = "negative:NEG-WOMBAT-TARGET"
    assert target not in [hit.doc_id for hit in corpus.search(WOMBAT_DRAFT, kinds=("negative",), k=10)]
    cosine = corpus.cosine(WOMBAT_DRAFT, [target])[target]
    assert cosine > 0.9
    hits = check_claim(corpus, WOMBAT_DRAFT)
    assert hits[0].doc_id == target and hits[0].score == round(cosine, 4)
    assert [hit.doc_id for hit in check_claim(corpus, WOMBAT_DRAFT, threshold=0.9)] == [target]
    report = claim_report(corpus, WOMBAT_DRAFT)
    assert report.total == 31 and len(report.matches) == 5  # the target and its thirty siblings
    assert report.documents == len(NEGATIVES) + 1 + 1 + 110  # retained, quarantined, target, crowd
    assert [hit.score for hit in report.matches] == sorted((hit.score for hit in report.matches), reverse=True)


def test_check_claim_does_not_depend_on_the_search_ranking(corpus: Corpus, monkeypatch) -> None:
    monkeypatch.setattr(corpus, "search", lambda *args, **kwargs: [])
    assert check_claim(corpus, NEAR_CLAIM)[0].doc_id == HELSTROM


def test_cli_check_new_header_counts_every_match(fake_repo: Path, capsys) -> None:
    _corpus_with(fake_repo, [WOMBAT_TARGET, *WOMBAT_CROWD])
    root = ["--root", str(fake_repo), "check-new", "--text", WOMBAT_DRAFT]
    assert main(root) == 2
    out = capsys.readouterr().out
    assert out.startswith("POSSIBLE DUPLICATE: 31 negative record(s) at TF-IDF cosine >= 0.6; the closest 5 are shown.")
    assert "NEG-WOMBAT-TARGET" in out
    assert main([*root, "--json"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["total"] == 31 and len(payload["matches"]) == 5


def test_cosine_of_a_doc_with_itself_is_one(corpus: Corpus) -> None:
    doc = corpus.get(HELSTROM)
    assert corpus.cosine(f"{doc.title} {doc.text}", [HELSTROM])[HELSTROM] == pytest.approx(1.0, abs=1e-5)


def test_cli_near_duplicates_writes_json_and_markdown(fake_repo: Path, tmp_path: Path, capsys) -> None:
    _corpus_with(fake_repo, [DUP_A, DUP_B])
    out = tmp_path / "dups.json"
    assert main(["--root", str(fake_repo), "near-duplicates", "--threshold", "0.8", "--out", str(out)]) == 0
    payload = json.loads(out.read_text())
    assert set(payload) == {
        "kind", "threshold", "per_family", "limit", "total", "pairs", "generated_on",
        "documents", "changed_since_fit", "index_incomplete", "index_issues",
    }  # fmt: skip
    assert (payload["kind"], payload["threshold"], payload["per_family"], payload["limit"]) == ("negative", 0.8, None, 200)
    assert payload["documents"] == len(NEGATIVES) + 1 + 2 and payload["index_incomplete"] is False
    assert payload["changed_since_fit"] == 0  # --out refits first
    assert payload["total"] == len(payload["pairs"])
    assert (payload["pairs"][0]["a"], payload["pairs"][0]["b"]) == ("negative:NEG-DUP-A", "negative:NEG-DUP-B")
    markdown = (tmp_path / "DUPS.md").read_text()
    assert "| 1.000 | NEG-DUP-A | NEG-DUP-B |" in markdown
    assert "(retained and quarantined negatives)" in markdown
    capsys.readouterr()
    assert main(["--root", str(fake_repo), "near-duplicates", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["pairs"][0]["b"] == "negative:NEG-DUP-B"


def test_cli_near_duplicates_out_refits_so_the_report_does_not_depend_on_patches(
    fake_repo: Path, tmp_path: Path
) -> None:
    corpus = _corpus_with(fake_repo, RESTATEMENT)
    # One more record is under 5 % of the documents, so the shared TF-IDF state is patched,
    # keeping the old vocabulary and IDF; a refit weighs "echidna" and "collective" anew.
    path = fake_repo / "research" / "registry" / "negative_results.json"
    extra = {"id": "NEG-ECHIDNA-ECHO", "claim": "Echidna collective readout.", "reason_invalid": "Echidna."}
    path.write_text(json.dumps(NEGATIVES + RESTATEMENT + [extra], indent=2), encoding="utf-8")
    assert corpus.refresh().refit is False and corpus.changed_since_fit() > 0
    patched = pair_report(corpus, threshold=0.5).pairs[0].score
    fresh = Corpus(fake_repo, index_dir=tmp_path / "fresh_index")
    fresh.refresh()
    refit = pair_report(fresh, threshold=0.5).pairs[0].score
    assert patched != refit
    out = tmp_path / "dups.json"
    assert main(["--root", str(fake_repo), "near-duplicates", "--threshold", "0.5", "--out", str(out)]) == 0
    payload = json.loads(out.read_text())
    assert payload["pairs"][0]["score"] == refit and payload["changed_since_fit"] == 0


def test_cli_near_duplicates_refuses_to_write_from_an_incomplete_index(fake_repo: Path, tmp_path: Path, capsys) -> None:
    negatives = fake_repo / "research" / "registry" / "negative_results.json"
    text = json.dumps(NEGATIVES + [DUP_A, DUP_B], indent=2)
    negatives.write_text(text[: len(text) // 2])  # caught half-way through a rewrite
    out = tmp_path / "dups.json"
    root = ["--root", str(fake_repo), "near-duplicates", "--threshold", "0.8"]
    assert main([*root, "--out", str(out)]) == 2
    assert "INDEX INCOMPLETE" in capsys.readouterr().err
    assert not out.exists() and not (tmp_path / "DUPS.md").exists()
    assert main([*root, "--json"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["index_incomplete"] is True and payload["documents"] == 1  # only the quarantined record
    assert any(issue["path"].endswith("negative_results.json") for issue in payload["index_issues"])
    assert main(root) == 2
    assert "INDEX INCOMPLETE" in capsys.readouterr().out


@pytest.mark.parametrize("name", ["dups.md", "DUPS.md", "dups.txt", "dups"])
def test_cli_near_duplicates_out_must_be_a_json_file(fake_repo: Path, tmp_path: Path, capsys, name: str) -> None:
    folder = tmp_path / "reports"
    folder.mkdir()
    assert main(["--root", str(fake_repo), "near-duplicates", "--out", str(folder / name)]) == 1
    assert "--out must name a .json file" in capsys.readouterr().err
    assert list(folder.iterdir()) == []


def test_cli_near_duplicates_out_reports_an_unwritable_path(fake_repo: Path, tmp_path: Path, capsys) -> None:
    out = tmp_path / "dups.json"
    out.mkdir()
    assert main(["--root", str(fake_repo), "near-duplicates", "--out", str(out)]) == 1
    assert f"error: cannot write {out}" in capsys.readouterr().err
    assert not (tmp_path / "DUPS.md").exists()


def test_cli_near_duplicates_says_how_many_pairs_the_limit_cut(fake_repo: Path, tmp_path: Path, capsys) -> None:
    _corpus_with(fake_repo, _sweep_records() + RESTATEMENT)
    root = ["--root", str(fake_repo), "near-duplicates", "--threshold", "0.8"]
    assert main([*root, "--limit", "5"]) == 0
    assert "\n5 of 136 pairs at TF-IDF cosine >= 0.8 (raise --limit to see the rest)." in capsys.readouterr().out
    assert main([*root, "--limit", "5", "--per-family", "2", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert (len(payload["pairs"]), payload["total"]) == (5, 7)
    out = tmp_path / "dups.json"
    assert main([*root, "--limit", "5", "--out", str(out)]) == 0
    assert capsys.readouterr().out.startswith("5 of 136 pairs at cosine >= 0.8")
    assert "highest first: the first 5 of 136 pairs (`--limit 5`)." in (tmp_path / "DUPS.md").read_text()
    assert main([*root, "--limit", "500"]) == 0
    assert "\n136 pairs at TF-IDF cosine >= 0.8. A pair" in capsys.readouterr().out


def test_cli_near_duplicates_labels_follow_the_kind(fake_repo: Path, tmp_path: Path, capsys) -> None:
    root = ["--root", str(fake_repo), "near-duplicates"]
    out = tmp_path / "notes.json"
    assert main([*root, "--kind", "note", "--threshold", "0.95", "--out", str(out)]) == 0
    markdown = (tmp_path / "NOTES.md").read_text()
    assert markdown.startswith("# Near-duplicate `note` documents\n")
    assert "`note` documents whose TF-IDF cosine" in markdown and "negatives" not in markdown.split("\n\n")[1]
    capsys.readouterr()
    assert main([*root, "--kind", "nosuchkind"]) == 1
    captured = capsys.readouterr()
    assert "the index has no `nosuchkind` documents" in captured.err and captured.out == ""


def test_check_claim_leaves_out_excluded_ids(corpus: Corpus) -> None:
    assert check_claim(corpus, NEAR_CLAIM)[0].doc_id == HELSTROM
    assert check_claim(corpus, NEAR_CLAIM, exclude=(HELSTROM,)) == []


def test_draft_claim_reads_claim_and_reason_of_a_record() -> None:
    record = dict(NEGATIVES[0], id="NEG-DRAFT-HELSTROM")
    expected = f"{record['claim']} {record['reason_invalid']}"
    assert draft_claim(json.dumps(record, indent=2)) == (expected, "NEG-DRAFT-HELSTROM")
    assert draft_claim(json.dumps({"claim": "Only a claim."})) == ("Only a claim.", None)
    assert draft_claim("A plain draft claim.\n") == ("A plain draft claim.\n", None)
    assert draft_claim("[1, 2]") == ("[1, 2]", None)  # not a record list: plain text


def test_draft_claim_reads_a_quarantined_record_as_filed() -> None:
    entry = QUARANTINED[0]
    original = entry["original_record"]
    expected = (f"{original['claim']} {original['reason_invalid']}", entry["id"])
    assert draft_claim(json.dumps(entry, indent=2)) == expected


def test_draft_claim_normalises_bom_list_and_id() -> None:
    record = NEGATIVES[0]
    expected = (f"{record['claim']} {record['reason_invalid']}", record["id"])
    raw = json.dumps(record, indent=2)
    assert draft_claim("﻿" + raw) == expected
    assert draft_claim(json.dumps([record])) == expected
    assert draft_claim(json.dumps(dict(record, id=f"negative:{record['id']}"))) == expected
    assert draft_claim(json.dumps(dict(record, id=f"  {record['id']} "))) == expected
    pair = json.dumps([record, NEGATIVES[1]], indent=2)
    assert [record_id for _, record_id in draft_claims(pair)] == [record["id"], NEGATIVES[1]["id"]]
    with pytest.raises(DraftError, match="2 records"):
        draft_claim(pair)


@pytest.mark.parametrize(
    "raw",
    [
        json.dumps(NEGATIVES[0], indent=2)[:-40],  # truncated
        '{"id": "NEG-NO-CLAIM"}',
        json.dumps(dict(NEGATIVES[0], claim=["a", "b"])),
        json.dumps(NEGATIVES[0]).replace(json.dumps(NEGATIVES[0]["claim"]), "NaN"),
        json.dumps(dict(NEGATIVES[0], claim="   ")),
        json.dumps(dict(NEGATIVES[0], reason_invalid=["x"])),
        json.dumps([NEGATIVES[0], "not a record"]),
        "[]",
    ],
)
def test_draft_claim_rejects_json_that_is_not_a_record(raw: str) -> None:
    with pytest.raises(DraftError):
        draft_claims(raw)


def test_cli_check_new_exit_code_gates_on_a_match(fake_repo: Path, tmp_path: Path, capsys) -> None:
    root = ["--root", str(fake_repo)]
    assert main([*root, "check-new", "--text", NEAR_CLAIM]) == 2
    assert "NEG-DCP-LOCAL-HELSTROM-HIERARCHY" in capsys.readouterr().out
    assert main([*root, "check-new", "--text", "zebrafish migration", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["matches"] == [] and payload["duplicate"] is False and "index_incomplete" in payload
    assert main([*root, "check-new", "--text", "zebrafish migration"]) == 0
    assert capsys.readouterr().out.startswith("No negative record (retained or quarantined) has TF-IDF cosine")
    record = tmp_path / "record.json"
    record.write_text(json.dumps(dict(NEGATIVES[0], id="NEG-DRAFT-HELSTROM"), indent=2))
    assert main([*root, "check-new", "--file", str(record)]) == 2
    plain = tmp_path / "claim.txt"
    plain.write_text(NEAR_CLAIM + "\n")
    assert main([*root, "check-new", "--file", str(plain)]) == 2


def test_cli_check_new_file_checks_claim_and_reason_not_the_raw_json(
    fake_repo: Path, tmp_path: Path, corpus: Corpus
) -> None:
    # Padded with a note and a handoff, the raw JSON is too diluted to match; its claim and reason are not.
    padded = dict(NEGATIVES[0], id="NEG-DRAFT-HELSTROM-PADDED", context=[NOTE, HANDOFF])
    raw = json.dumps(padded, indent=2)
    assert check_claim(corpus, raw) == []
    assert check_claim(corpus, draft_claim(raw)[0])[0].doc_id == HELSTROM
    record = tmp_path / "padded.json"
    record.write_text(raw)
    assert main(["--root", str(fake_repo), "check-new", "--file", str(record)]) == 2


def test_cli_check_new_file_does_not_match_the_record_with_itself(fake_repo: Path, tmp_path: Path, capsys) -> None:
    root = ["--root", str(fake_repo), "check-new", "--json", "--file"]
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps(UNIQUE, indent=2))
    assert main([*root, str(draft)]) == 0  # before it is filed
    capsys.readouterr()
    corpus = _corpus_with(fake_repo, [UNIQUE])  # after: a hook on registry edits sees the record filed
    assert check_claim(corpus, f"{UNIQUE['claim']} {UNIQUE['reason_invalid']}")[0].doc_id == PLATYPUS
    assert main([*root, str(draft)]) == 0
    assert json.loads(capsys.readouterr().out)["matches"] == []
    twin = tmp_path / "twin.json"
    twin.write_text(json.dumps(dict(UNIQUE, id="NEG-NEW-PLATYPUS-SIEVE-TWIN")))
    assert main([*root, str(twin)]) == 2
    assert [match["doc_id"] for match in json.loads(capsys.readouterr().out)["matches"]] == [PLATYPUS]
    filed = tmp_path / "filed.json"
    filed.write_text(json.dumps(NEGATIVES[0]))
    assert main([*root, str(filed)]) == 0
    quarantined = tmp_path / "quarantined.json"
    quarantined.write_text(json.dumps({"id": QUARANTINED[0]["id"], **QUARANTINED[0]["original_record"]}))
    assert main([*root, str(quarantined)]) == 0
    capsys.readouterr()
    as_filed = tmp_path / "quarantined_as_filed.json"  # the claim sits under original_record
    as_filed.write_text(json.dumps(QUARANTINED[0], indent=2))
    assert main([*root, str(as_filed)]) == 0
    assert json.loads(capsys.readouterr().out)["matches"] == []


def test_cli_check_new_reads_a_record_saved_with_a_bom_or_in_a_list(fake_repo: Path, tmp_path: Path, capsys) -> None:
    root = ["--root", str(fake_repo), "check-new", "--json", "--file"]
    bom = tmp_path / "bom.json"
    bom.write_bytes(b"\xef\xbb\xbf" + json.dumps(NEGATIVES[0], indent=2).encode())
    assert main([*root, str(bom)]) == 0  # filed: its own id is left out
    listed = tmp_path / "listed.json"
    listed.write_text(json.dumps([NEGATIVES[0]], indent=2))
    assert main([*root, str(listed)]) == 0
    capsys.readouterr()


def test_cli_check_new_checks_a_list_of_records_one_by_one(fake_repo: Path, tmp_path: Path, capsys) -> None:
    root = ["--root", str(fake_repo), "check-new", "--file"]
    filed = tmp_path / "filed.json"
    filed.write_text(json.dumps(NEGATIVES, indent=2))  # both filed: each leaves out both ids
    assert main([*root, str(filed)]) == 0
    capsys.readouterr()
    batch = tmp_path / "batch.json"
    batch.write_text(json.dumps([UNIQUE, dict(NEGATIVES[0], id="NEG-DRAFT-HELSTROM")], indent=2))
    assert main([*root, str(batch), "--json"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert [(m["draft_id"], m["doc_id"]) for m in payload["matches"]] == [("NEG-DRAFT-HELSTROM", HELSTROM)]
    assert payload["total"] == 1 and payload["drafts"] == 2
    assert main([*root, str(batch)]) == 2
    out = capsys.readouterr().out
    assert "NEG-NEW-PLATYPUS-SIEVE: no negative record" in out
    assert "NEG-DRAFT-HELSTROM: POSSIBLE DUPLICATE: 1 negative record(s)" in out


def test_cli_check_new_compares_a_new_record_with_a_filed_one_listed_beside_it(
    fake_repo: Path, tmp_path: Path, capsys
) -> None:
    # A registry hunk with context: the filed Helstrom record, then a verbatim copy under a new id.
    # Leaving out every listed id hid the original from its copy, so the copy passed with exit 0.
    hunk = tmp_path / "hunk.json"
    hunk.write_text(json.dumps([NEGATIVES[0], dict(NEGATIVES[0], id="NEG-HELSTROM-RESTATED")], indent=2))
    root = ["--root", str(fake_repo), "check-new", "--file", str(hunk)]
    assert main([*root, "--json"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert [(m["draft_id"], m["doc_id"]) for m in payload["matches"]] == [("NEG-HELSTROM-RESTATED", HELSTROM)]
    assert payload["filed"] == 1
    assert main(root) == 2
    captured = capsys.readouterr()
    assert "NEG-DCP-LOCAL-HELSTROM-HIERARCHY: no negative record (retained or quarantined) has" in captured.out
    assert "NEG-HELSTROM-RESTATED: POSSIBLE DUPLICATE: 1 negative record(s)" in captured.out
    assert "already in the index" not in captured.err  # one filed record hides nothing


def test_cli_check_new_warns_when_filed_records_of_a_list_hide_each_other(fake_repo: Path, tmp_path: Path, capsys) -> None:
    listed = tmp_path / "registry_copy.json"  # say a hook given the whole registry file
    listed.write_text(json.dumps(NEGATIVES, indent=2))
    root = ["--root", str(fake_repo), "check-new", "--file", str(listed)]
    assert main(root) == 0
    captured = capsys.readouterr()
    assert "warning: 2 of 2 listed records are already in the index" in captured.err
    assert "NEG-DCP-LOCAL-HELSTROM-HIERARCHY: no negative record outside the list has TF-IDF cosine >= 0.6." in captured.out
    assert main([*root, "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["filed"] == 2


def test_cli_check_new_gives_a_batch_the_same_answer_before_and_after_it_is_filed(
    fake_repo: Path, tmp_path: Path, capsys
) -> None:
    batch = tmp_path / "batch.json"
    batch.write_text(json.dumps([DUP_A, DUP_B], indent=2))
    root = ["--root", str(fake_repo), "check-new", "--json", "--file"]
    assert main([*root, str(batch)]) == 0  # not yet filed: records of one list are not compared with each other
    assert json.loads(capsys.readouterr().out)["filed"] == 0
    _corpus_with(fake_repo, [DUP_A, DUP_B])
    assert main([*root, str(batch)]) == 0  # filed: each leaves out the other's id too
    assert json.loads(capsys.readouterr().out)["filed"] == 2
    alone = tmp_path / "alone.json"
    alone.write_text(json.dumps(DUP_A, indent=2))
    assert main([*root, str(alone)]) == 2  # on its own, the filed record still meets its twin
    assert [m["doc_id"] for m in json.loads(capsys.readouterr().out)["matches"]] == ["negative:NEG-DUP-B"]


@pytest.mark.parametrize(
    "content",
    [json.dumps(NEGATIVES[0], indent=2)[:-40], json.dumps(dict(NEGATIVES[0], claim=["a", "b"])), '{"id": "X"}'],
)
def test_cli_check_new_rejects_a_record_it_cannot_read(fake_repo: Path, tmp_path: Path, capsys, content: str) -> None:
    draft = tmp_path / "draft.json"
    draft.write_text(content)
    assert main(["--root", str(fake_repo), "check-new", "--file", str(draft)]) == 1
    captured = capsys.readouterr()
    assert captured.err.startswith(f"error: {draft}: ") and captured.out == ""


@pytest.mark.parametrize("draft", ["", "   \n", "the of and", json.dumps(dict(UNIQUE, claim="the of", reason_invalid=""))])
def test_cli_check_new_rejects_a_draft_with_no_words(fake_repo: Path, tmp_path: Path, capsys, draft: str) -> None:
    root = ["--root", str(fake_repo), "check-new"]
    path = tmp_path / "draft.txt"
    path.write_text(draft)
    assert main([*root, "--file", str(path)]) == 1
    assert "no words to compare" in capsys.readouterr().err
    if not draft.startswith("{"):
        assert main([*root, "--text", draft]) == 1
        assert "no words to compare" in capsys.readouterr().err


def test_cli_check_new_threshold_flag_moves_the_gate(fake_repo: Path, corpus: Corpus, capsys) -> None:
    cosine = check_claim(corpus, NEAR_CLAIM)[0].score
    assert 0.6 <= cosine < 0.99
    root = ["--root", str(fake_repo), "check-new", "--text", NEAR_CLAIM]
    assert main([*root, "--threshold", "0.99"]) == 0
    assert "TF-IDF cosine >= 0.99 with this claim." in capsys.readouterr().out
    assert main([*root, "--threshold", str(cosine - 0.01)]) == 2
    capsys.readouterr()


def test_check_duplicate_negative_tool_passes_its_threshold(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "check_duplicate_negative", {"claim": NEAR_CLAIM, "threshold": 0.99})
    assert payload["duplicate"] is False and payload["matches"] == [] and payload["threshold"] == 0.99
    assert _call(server, "check_duplicate_negative", {"claim": NEAR_CLAIM, "threshold": 0.5})["duplicate"] is True


@pytest.mark.parametrize("value", ["nan", "inf", "1e309", "1.5", "0", "-1", "60"])
def test_cli_rejects_a_threshold_outside_0_1(fake_repo: Path, capsys, value: str) -> None:
    for command in (["check-new", "--text", NEAR_CLAIM], ["near-duplicates"]):
        with pytest.raises(SystemExit) as raised:
            main(["--root", str(fake_repo), *command, "--threshold", value])
        assert raised.value.code == 2
        assert "threshold must be a number in (0, 1]" in capsys.readouterr().err


@pytest.mark.parametrize("flag", ["--limit", "--per-family"])
@pytest.mark.parametrize("value", ["-3", "-1", "2.5", "many"])
def test_cli_near_duplicates_rejects_a_negative_limit_or_per_family(fake_repo: Path, capsys, flag: str, value: str) -> None:
    # --limit -3 printed "0 of 57 pairs ... (raise --limit to see the rest)" and stored "limit": -3;
    # --per-family -1 silently dropped every sibling pair, as 0 does.
    with pytest.raises(SystemExit) as raised:
        main(["--root", str(fake_repo), "near-duplicates", flag, value])
    assert raised.value.code == 2
    assert f"argument {flag}: {flag} must be a whole number of at least 0, got {value}" in capsys.readouterr().err
    assert not (fake_repo / "research" / "corpus_index").exists()  # rejected before the index is touched


def test_cli_near_duplicates_accepts_a_zero_limit_and_per_family(fake_repo: Path, capsys) -> None:
    _corpus_with(fake_repo, _sweep_records() + RESTATEMENT)
    root = ["--root", str(fake_repo), "near-duplicates", "--threshold", "0.8", "--json"]
    assert main([*root, "--limit", "0"]) == 0  # the count alone
    payload = json.loads(capsys.readouterr().out)
    assert (payload["limit"], payload["pairs"], payload["total"]) == (0, [], 136)
    assert main([*root, "--per-family", "0"]) == 0  # no sweep siblings, only the restatement
    payload = json.loads(capsys.readouterr().out)
    assert (payload["per_family"], payload["total"]) == (0, 1)


@pytest.mark.parametrize("value", [float("nan"), 1.5, 0.0, -1.0, 60.0])
def test_check_duplicate_negative_tool_rejects_a_threshold_outside_0_1(fake_repo: Path, value: float) -> None:
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "check_duplicate_negative", {"claim": NEAR_CLAIM, "threshold": value})
    assert "threshold must be a number in (0, 1]" in payload["error"] and "duplicate" not in payload


def test_cli_check_new_says_index_incomplete_on_a_half_written_registry(fake_repo: Path, capsys) -> None:
    negatives = fake_repo / "research" / "registry" / "negative_results.json"
    text = negatives.read_text()
    negatives.write_text(text[: len(text) // 2])
    root = ["--root", str(fake_repo), "check-new", "--text", NEAR_CLAIM]
    assert main(root) == 0  # the Helstrom record cannot be read, so nothing matches
    captured = capsys.readouterr()
    assert "INDEX INCOMPLETE: a registry could not be read" in captured.out
    assert "INDEX INCOMPLETE" in captured.err
    assert main([*root, "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["index_incomplete"] is True


def test_check_new_with_no_negative_records_is_an_error(fake_repo: Path, capsys) -> None:
    registry = fake_repo / "research" / "registry"
    (registry / "negative_results.json").write_text("[]")
    (registry / "quarantined_campaign_negatives.json").write_text("[]")
    assert main(["--root", str(fake_repo), "check-new", "--text", NEAR_CLAIM]) == 1
    captured = capsys.readouterr()
    assert "the index has no negative records" in captured.err and "No negative record" not in captured.out
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "check_duplicate_negative", {"claim": NEAR_CLAIM})
    assert "the index has no negative records" in payload["error"] and "duplicate" not in payload


def test_check_duplicate_negative_tool_sees_a_record_filed_since_its_last_refresh(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")  # refreshes other tools at most every 30 s
    claim = f"{UNIQUE['claim']} {UNIQUE['reason_invalid']}"
    assert _call(server, "check_duplicate_negative", {"claim": claim})["duplicate"] is False
    _corpus_with(fake_repo, [UNIQUE])  # another agent files the record and indexes it
    payload = _call(server, "check_duplicate_negative", {"claim": claim})
    assert payload["duplicate"] is True and payload["matches"][0]["doc_id"] == PLATYPUS


GOPPA_SIBLING = {
    "id": "NEG-GOPPA-SCALE-M6-T3-N48-0-11",
    "claim": SWEEPS["NEG-GOPPA-SCALE-M6-T3-N48-0"],
    "reason_invalid": "Sweep point.",
    "lesson": "Sweep.",
}


def test_cli_check_new_allow_accepts_known_siblings(fake_repo: Path, tmp_path: Path, capsys) -> None:
    corpus = _corpus_with(fake_repo, _sweep_records())
    draft = tmp_path / "sibling.json"
    draft.write_text(json.dumps(GOPPA_SIBLING))
    cosine = claim_report(corpus, draft_claim(draft.read_text())[0]).matches[0].score
    root = ["--root", str(fake_repo), "check-new", "--file", str(draft)]
    assert main(root) == 2
    assert capsys.readouterr().out.startswith("POSSIBLE DUPLICATE: 10 negative record(s)")
    assert main([*root, "--allow", "NEG-GOPPA-SCALE-M6-T3-N48-0-1"]) == 2  # one sibling allowed, nine left
    out = capsys.readouterr().out
    assert out.startswith("POSSIBLE DUPLICATE: 9 negative record(s)")
    allowed_one = f"NEG-GOPPA-SCALE-M6-T3-N48-0-1 ({cosine:.3f})"
    assert f"\nNot counted: 1 matching record(s) allowed by --allow: {allowed_one}.\n" in out
    assert main([*root, "--allow", "NEG-GOPPA-SCALE-M6-T3-N48-0-*"]) == 0
    out = capsys.readouterr().out
    # Every match allowed: the header must not say that no record reaches the threshold.
    assert out.startswith(
        "No negative record outside --allow has TF-IDF cosine >= 0.6 with this claim (10 allowed matches, listed below).\n"
    )
    assert f"\nNot counted: 10 matching record(s) allowed by --allow: {allowed_one}," in out
    assert main([*root, "--allow", "negative:NEG-GOPPA-SCALE-M6-T3-N48-0-*", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["duplicate"] is False and payload["matches"] == [] and len(payload["allowed"]) == 10
    with pytest.raises(SystemExit):
        main([*root, "--allow", "*"])
    assert "--allow" in capsys.readouterr().err


def test_cli_check_new_allowed_list_counts_what_it_cuts_and_names_the_draft(
    fake_repo: Path, tmp_path: Path, capsys
) -> None:
    _corpus_with(fake_repo, _sweep_records() + [dict(GOPPA_SIBLING, id="NEG-GOPPA-SCALE-M6-T3-N48-0-12")])
    draft = tmp_path / "sibling.json"
    draft.write_text(json.dumps(GOPPA_SIBLING))
    root = ["--root", str(fake_repo), "check-new", "--file", str(draft), "--allow", "NEG-GOPPA-SCALE-M6-T3-N48-0-*"]
    assert main(root) == 0
    line = next(line for line in capsys.readouterr().out.splitlines() if line.startswith("Not counted:"))
    assert line.startswith("Not counted: 11 matching record(s) allowed by --allow: ")
    assert line.endswith(", and 1 more.") and line.count(" (") == 10  # ten named with their cosines
    assert main([*root, "--json"]) == 0
    allowed = json.loads(capsys.readouterr().out)["allowed"]
    assert len(allowed) == 11 and {entry["draft_id"] for entry in allowed} == {GOPPA_SIBLING["id"]}


def test_allow_accepts_a_quarantined_record(fake_repo: Path, capsys) -> None:
    original = QUARANTINED[0]["original_record"]
    root = ["--root", str(fake_repo), "check-new", "--text", f"{original['claim']} {original['reason_invalid']}", "--json"]
    quarantined = f"quarantined:{QUARANTINED[0]['id']}"
    for pattern in (QUARANTINED[0]["id"], quarantined, "NEG-ANNEALING-*"):
        assert main([*root, "--allow", pattern]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["matches"] == [] and [entry["doc_id"] for entry in payload["allowed"]] == [quarantined]


def test_check_duplicate_negative_tool_allow(fake_repo: Path) -> None:
    _corpus_with(fake_repo, _sweep_records())
    server = create_server(fake_repo, dense="off")
    claim = f"{GOPPA_SIBLING['claim']} {GOPPA_SIBLING['reason_invalid']}"
    payload = _call(server, "check_duplicate_negative", {"claim": claim})
    assert payload["duplicate"] is True
    assert payload["total"] == 10 and len(payload["matches"]) == 5  # the closest five; total counts them all
    payload = _call(server, "check_duplicate_negative", {"claim": claim, "allow": ["NEG-GOPPA-SCALE-M6-T3-N48-0-*"]})
    assert payload["duplicate"] is False and len(payload["allowed"]) == 10
    assert "error" in _call(server, "check_duplicate_negative", {"claim": claim, "allow": ["*"]})


def test_check_duplicate_negative_tool_rejects_an_empty_claim(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")
    for claim in ("", "the of and"):
        payload = _call(server, "check_duplicate_negative", {"claim": claim})
        assert "no words to compare" in payload["error"] and "duplicate" not in payload


def test_cli_check_new_unreadable_file_exits_1_before_indexing(fake_repo: Path, tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.json"
    assert main(["--root", str(fake_repo), "check-new", "--file", str(missing)]) == 1
    assert f"error: cannot read {missing}" in capsys.readouterr().err
    assert not (fake_repo / "research" / "corpus_index").exists()


def test_cli_check_new_marks_a_quarantined_match(fake_repo: Path, capsys) -> None:
    original = QUARANTINED[0]["original_record"]
    assert main(["--root", str(fake_repo), "check-new", "--text", f"{original['claim']} {original['reason_invalid']}"]) == 2
    out = capsys.readouterr().out
    assert out.startswith("POSSIBLE DUPLICATE: 1 negative record(s), 1 of them quarantined, at TF-IDF cosine >= 0.6.")
    assert "NEG-ANNEALING-GAP-BARRIER (quarantined)" in out
    assert "retained" not in out


def test_check_duplicate_negative_tool(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "check_duplicate_negative", {"claim": NEAR_CLAIM})
    assert payload["duplicate"] is True and payload["threshold"] == 0.6 and payload["claim"] == NEAR_CLAIM
    assert payload["matches"][0]["doc_id"] == HELSTROM and "index_incomplete" in payload
    assert _call(server, "check_duplicate_negative", {"claim": "zebrafish migration"})["duplicate"] is False

from __future__ import annotations

import json
from pathlib import Path

import pytest

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
    assert set(payload) == {"kind", "threshold", "per_family", "limit", "total", "pairs", "generated_on"}
    assert (payload["kind"], payload["threshold"], payload["per_family"], payload["limit"]) == ("negative", 0.8, None, 200)
    assert payload["total"] == len(payload["pairs"])
    assert (payload["pairs"][0]["a"], payload["pairs"][0]["b"]) == ("negative:NEG-DUP-A", "negative:NEG-DUP-B")
    markdown = (tmp_path / "DUPS.md").read_text()
    assert "| 1.000 | NEG-DUP-A | NEG-DUP-B |" in markdown
    assert "(retained and quarantined negatives)" in markdown
    capsys.readouterr()
    assert main(["--root", str(fake_repo), "near-duplicates", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["pairs"][0]["b"] == "negative:NEG-DUP-B"


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

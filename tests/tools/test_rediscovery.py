from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from tools.audit import rediscovery as rd
from tools.corpus.sources.arxiv import Client, query_url

FIXTURE = Path(__file__).parent / "fixtures" / "arxiv_atom_sample.xml"


def _neg(record_id: str, claim: str, reason: str, lesson: str = "", source: str = "theorems/x.py") -> dict:
    return {"id": record_id, "claim": claim, "reason_invalid": reason, "lesson": lesson, "applies_to": [], "evidence": {}, "source": source}


TOPICS = {
    "barren": ("Variational circuits train at scale", "Gradient variance vanishes exponentially: barren plateaus from Haar concentration."),
    "code": ("Generated code pair is hard for code equivalence", "Support splitting and hull dimension invariants separate the code pair classically."),
    "dcp": ("Dihedral coset sieve beats Kuperberg", "The Kuperberg collimation sieve needs subexponential dihedral coset samples."),
}


def _topic_records() -> list[dict]:
    records = []
    for topic, (claim, reason) in TOPICS.items():
        for i in range(4):
            records.append(_neg(f"NEG-{topic.upper()}-{i}", f"{claim} variant {i}.", f"{reason} Case {i}."))
    return records


def test_strip_citations_removes_arxiv_identifiers() -> None:
    text = (
        "Bound by arXiv:2605.25995 and arxiv:1607.01842; see https://arxiv.org/abs/2408.08292v2 "
        "and quant-ph/0501044 for details."
    )
    stripped = rd.strip_citations(text)
    for needle in ("2605.25995", "1607.01842", "2408.08292", "0501044", "arxiv.org"):
        assert needle not in stripped
    assert "Bound by" in stripped and "for details" in stripped


def test_cited_ids_reads_text_and_evidence() -> None:
    record = _neg("A", "c", "Atom bound by arXiv:2605.25995.")
    record["evidence"] = {"literature_ids": ["arxiv:1607.01842"]}
    assert rd.cited_ids(record) == ["1607.01842", "2605.25995"]


def test_query_url_supports_relevance_sort() -> None:
    query = parse_qs(urlparse(query_url("abs:x", 10, sort_by="relevance")).query)
    assert query["sortBy"] == ["relevance"]
    default = parse_qs(urlparse(query_url("abs:x", 10)).query)
    assert default["sortBy"] == ["submittedDate"]


def test_cluster_negatives_groups_topics() -> None:
    clusters = rd.cluster_negatives(_topic_records(), n_clusters=3)
    assert len(clusters) == 3
    groups = sorted(sorted({m.split("-")[1] for m in c.members}) for c in clusters)
    assert groups == [["BARREN"], ["CODE"], ["DCP"]]
    for cluster in clusters:
        assert cluster.terms and len(cluster.similarity) == len(cluster.members)


def test_packets_strip_citations_and_include_required_members() -> None:
    records = _topic_records()
    records[0]["reason_invalid"] += " Known since arXiv:1803.11173."
    clusters = rd.cluster_negatives(records, n_clusters=3)
    packets = rd.build_packets(clusters, records, corpus=None, max_members=2, must_include={"NEG-BARREN-3"})
    barren = next(p for p in packets if any(m["id"].startswith("NEG-BARREN") for m in p["members"]))
    assert "NEG-BARREN-3" in [m["id"] for m in barren["members"]]
    assert 2 <= len(barren["members"]) <= 3
    assert "1803.11173" not in json.dumps(packets)


def test_paced_opener_spaces_calls_across_instances(tmp_path: Path) -> None:
    clock = {"t": 100.0}
    sleeps: list[float] = []

    def fake_open(request, timeout=0):
        return request

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        clock["t"] += seconds

    first = rd.PacedOpener(tmp_path, delay=3.0, opener=fake_open, now=lambda: clock["t"], sleep=sleep)
    second = rd.PacedOpener(tmp_path, delay=3.0, opener=fake_open, now=lambda: clock["t"], sleep=sleep)
    first("a")
    clock["t"] += 1.0
    second("b")
    assert sleeps == [pytest.approx(2.0)]


def test_known_papers_reads_cached_responses(tmp_path: Path) -> None:
    (tmp_path / "x.xml").write_bytes(FIXTURE.read_bytes())
    papers = rd.known_papers(tmp_path)
    assert len(papers) == 5
    some = next(iter(papers.values()))
    assert some.abstract


def test_search_records_query_log(tmp_path: Path) -> None:
    class Response:
        def read(self) -> bytes:
            return FIXTURE.read_bytes()

        def __enter__(self):
            return self

        def __exit__(self, *exc) -> None:
            return None

    client = Client(opener=lambda request, timeout=0: Response(), sleep=lambda s: None, cache_dir=tmp_path)
    rows = rd.search(client, 'abs:"hidden subgroup"', max_results=5, log=tmp_path / "queries.jsonl", who="t")
    assert len(rows) == 5 and {"arxiv_id", "title", "abstract", "published"} <= set(rows[0])
    logged = [json.loads(line) for line in (tmp_path / "queries.jsonl").read_text().splitlines()]
    assert logged[0]["query"] == 'abs:"hidden subgroup"' and logged[0]["who"] == "t"


def _papers() -> dict:
    from tools.corpus.sources.arxiv import parse_atom

    return {p.arxiv_id: p for p in parse_atom(FIXTURE.read_bytes())}


def test_import_verifies_citations_against_abstracts(tmp_path: Path) -> None:
    papers = _papers()
    pid, paper = next(iter(papers.items()))
    quote = " ".join(paper.abstract.split()[3:12])
    out = tmp_path / "j.jsonl"
    rows = [
        {"cluster": "C01", "label": "published", "confidence": 0.8,
         "citations": [{"arxiv_id": pid, "quote": quote}], "member_overrides": {}, "queries": ["q"]},
        {"cluster": "C02", "label": "published", "confidence": 0.9,
         "citations": [{"arxiv_id": pid, "quote": "words that are not in the abstract at all"}], "member_overrides": {}, "queries": []},
        {"cluster": "C03", "label": "not-found", "confidence": 0.6, "citations": [],
         "member_overrides": {"NEG-X": {"label": "adjacent", "note": "technique known"}}, "queries": []},
    ]
    out.write_text("\n".join(json.dumps(r) for r in rows))
    judged = rd.import_judgements([out], papers, local={})
    assert judged["C01"]["label"] == "published" and judged["C01"]["citations"][0]["verified"] is True
    assert judged["C02"]["label"] == "unclear"
    assert judged["C02"]["downgraded_from"] == "published"
    assert judged["C03"]["member_overrides"]["NEG-X"]["label"] == "adjacent"
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({"cluster": "C04", "label": "novel!", "confidence": 1, "citations": []}))
    with pytest.raises(ValueError):
        rd.import_judgements([bad], papers, local={})


def test_published_override_needs_its_own_verified_citation(tmp_path: Path) -> None:
    papers = _papers()
    (pid, paper), (other, other_paper) = list(papers.items())[:2]
    quote = " ".join(paper.abstract.split()[3:12])
    other_quote = " ".join(other_paper.abstract.split()[2:11])
    out = tmp_path / "j.jsonl"
    out.write_text(json.dumps({
        "cluster": "C01", "label": "unclear", "confidence": 0.6,
        "citations": [{"arxiv_id": pid, "quote": quote}],
        "member_overrides": {
            "NEG-A": {"label": "published", "note": f"arXiv:{pid} states it."},
            "NEG-B": {"label": "published", "note": "arXiv:2208.11060 states it."},
            "NEG-C": {"label": "published", "note": "own quote", "citations": [{"arxiv_id": other, "quote": other_quote}]},
            "NEG-D": {"label": "adjacent", "note": "no citation needed"},
        },
        "queries": [],
    }))
    overrides = rd.import_judgements([out], papers, local={})["C01"]["member_overrides"]
    assert overrides["NEG-A"]["label"] == "published" and overrides["NEG-A"]["citations"][0]["arxiv_id"] == pid
    assert overrides["NEG-B"]["label"] == "unclear" and overrides["NEG-B"]["downgraded_from"] == "published"
    assert overrides["NEG-C"]["label"] == "published" and overrides["NEG-C"]["citations"][0]["arxiv_id"] == other
    assert overrides["NEG-D"]["label"] == "adjacent"


def test_ground_truth_shows_the_members_own_citation() -> None:
    records = _topic_records()
    clusters = rd.cluster_negatives(records, n_clusters=3)
    barren = next(c for c in clusters if c.members[0].startswith("NEG-BARREN"))
    own = {"arxiv_id": "2208.11060", "quote": "q", "verified": True}
    judgements = {barren.cluster_id: {
        "label": "unclear", "confidence": 0.6,
        "citations": [{"arxiv_id": "2408.02778", "quote": "q", "verified": True}],
        "member_overrides": {"NEG-BARREN-1": {"label": "published", "note": "n", "citations": [own]}},
    }}
    analysis = rd.analyse(records, clusters, judgements, {"NEG-BARREN-1": "kernels", "NEG-BARREN-0": "x"}, shown=set())
    rows = {r["id"]: r for r in analysis["ground_truth"]["rows"]}
    assert [c["arxiv_id"] for c in rows["NEG-BARREN-1"]["citations"]] == ["2208.11060"]
    assert rows["NEG-BARREN-0"]["citations"] == []


def test_spot_check_section_lists_disagreements_by_basis() -> None:
    records = _topic_records()
    clusters = rd.cluster_negatives(records, n_clusters=3)
    barren = next(c for c in clusters if c.members[0].startswith("NEG-BARREN"))
    judgements = {barren.cluster_id: {"label": "published", "confidence": 0.9,
                                      "citations": [{"arxiv_id": "1803.11173", "quote": "q", "verified": True}], "member_overrides": {}}}
    spot = {"NEG-BARREN-0": {"agree": True, "note": "label=published; fine"},
            "NEG-BARREN-1": {"agree": False, "note": "label=adjacent; different setting"}}
    analysis = rd.analyse(records, clusters, judgements, {}, shown={"NEG-BARREN-0"}, spot_check=spot)
    assert analysis["spot_check"]["by_basis"] == {"shown": [1, 1], "propagated": [0, 1]}
    text = rd.render(analysis)
    assert "## Spot check" in text and "NEG-BARREN-1" in text and "different setting" in text


def test_spot_check_verdict_on_a_label_that_has_since_changed_is_stale() -> None:
    records = [_neg(f"NEG-BARREN-{i}", f"Barren claim {i}.", "Gradients vanish.") for i in range(6)]
    cluster = rd.Cluster("C01", [r["id"] for r in records], [])
    overrides = {f"NEG-BARREN-{i}": {"label": "adjacent", "note": "different setting"} for i in (1, 2)}
    spot = {"NEG-BARREN-0": {"agree": True, "note": "label=published; fine", "seen_label": "published"},
            "NEG-BARREN-4": {"agree": True, "note": "label=published; fine", "seen_label": "published"}}
    analysis = rd.analyse(records, [cluster], _published("C01", overrides), {},
                          shown={"NEG-BARREN-0", "NEG-BARREN-1", "NEG-BARREN-2"}, spot_check=spot)
    check = analysis["spot_check"]
    assert (check["sampled"], check["n"], check["agree"]) == (2, 1, 1)
    assert check["stale"] == {"n": 1, "agreed_with_seen_label": 1, "ids": ["NEG-BARREN-4"]}
    text = rd.render(analysis)
    assert "re-read 2 randomly chosen judged records" in text and "On the 1 whose label has not changed" in text
    assert "1 sampled record's label changed after the review" in text


def test_import_keeps_the_label_the_spot_reviewer_saw(fake_repo: Path, tmp_path: Path) -> None:
    review = tmp_path / "review.jsonl"
    review.write_text(json.dumps({"id": "NEG-BARREN-0", "agree": True, "note": "ok", "assigned_label": "published"}) + "\n")
    assert rd.main(["--root", str(fake_repo), "import", "--spot-check", str(review)]) == 0
    stored = json.loads((fake_repo / rd.JUDGEMENTS_FILE).read_text())["spot_check"]["NEG-BARREN-0"]
    assert stored["seen_label"] == "published"


def test_analyse_propagates_labels_and_scores_ground_truth() -> None:
    records = _topic_records()
    clusters = rd.cluster_negatives(records, n_clusters=3)
    barren = next(c for c in clusters if c.members[0].startswith("NEG-BARREN"))
    code = next(c for c in clusters if c.members[0].startswith("NEG-CODE"))
    judgements = {
        barren.cluster_id: {"label": "published", "confidence": 0.9, "citations": [{"arxiv_id": "1803.11173", "quote": "q", "verified": True}], "member_overrides": {}},
        code.cluster_id: {"label": "adjacent", "confidence": 0.5, "citations": [], "member_overrides": {"NEG-CODE-2": {"label": "not-found", "note": "n"}}},
    }
    truth = {"NEG-BARREN-1": "barren plateaus", "NEG-CODE-0": "support splitting"}
    analysis = rd.analyse(records, clusters, judgements, truth, shown={"NEG-BARREN-1", "NEG-CODE-2"})
    rows = {row["id"]: row for row in analysis["records"]}
    assert rows["NEG-BARREN-1"]["label"] == "published" and rows["NEG-BARREN-1"]["basis"] == "shown"
    assert rows["NEG-BARREN-0"]["basis"] == "propagated"
    assert rows["NEG-CODE-2"]["label"] == "not-found"
    assert rows["NEG-DCP-0"]["label"] == "unjudged"
    assert analysis["counts"]["published"] == 4
    gt = analysis["ground_truth"]
    assert gt["n"] == 2 and gt["published"] == 1
    report = rd.render(analysis)
    for heading in ("## Headline", "## By track", "## Ground truth", "## Review queue"):
        assert heading in report


def _published(cluster: str, overrides: dict | None = None) -> dict:
    return {cluster: {"label": "published", "confidence": 0.9, "member_overrides": overrides or {},
                      "citations": [{"arxiv_id": "1803.11173", "quote": "q", "verified": True}]}}


def test_unread_members_are_withheld_when_the_judge_mostly_overrode_the_cluster_label() -> None:
    records = [_neg(f"NEG-BARREN-{i}", f"Barren claim {i}.", "Gradients vanish.") for i in range(6)]
    cluster = rd.Cluster("C01", [r["id"] for r in records], [])
    overrides = {f"NEG-BARREN-{i}": {"label": "adjacent", "note": "different setting"} for i in (1, 2)}
    analysis = rd.analyse(records, [cluster], _published("C01", overrides), {}, shown={"NEG-BARREN-0", "NEG-BARREN-1", "NEG-BARREN-2"})
    rows = {row["id"]: row for row in analysis["records"]}
    assert rows["NEG-BARREN-0"]["label"] == "published" and rows["NEG-BARREN-0"]["basis"] == "shown"
    for i in (3, 4, 5):
        assert (rows[f"NEG-BARREN-{i}"]["label"], rows[f"NEG-BARREN-{i}"]["basis"]) == ("unclear", "withheld")
    assert analysis["read"]["published"] == 1 and analysis["read"]["n"] == 3


def test_unread_member_on_another_track_does_not_inherit_the_label() -> None:
    records = [_neg(f"NEG-BARREN-{i}", f"Barren claim {i}.", "Gradients vanish.") for i in range(3)]
    records.append(_neg("NEG-DCP-SIEVE-0", "Dihedral sieve claim.", "Gradients vanish."))
    cluster = rd.Cluster("C01", [r["id"] for r in records], [])
    analysis = rd.analyse(records, [cluster], _published("C01"), {}, shown={"NEG-BARREN-0"})
    rows = {row["id"]: row for row in analysis["records"]}
    assert (rows["NEG-BARREN-2"]["label"], rows["NEG-BARREN-2"]["basis"]) == ("published", "propagated")
    assert (rows["NEG-DCP-SIEVE-0"]["label"], rows["NEG-DCP-SIEVE-0"]["basis"]) == ("unclear", "withheld")
    report = rd.render(analysis)
    assert "withheld" in report and "read by a judge" in report


def test_cli_export_and_report_on_fake_repo(fake_repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "packets"
    assert rd.main(["--root", str(fake_repo), "export", "--out", str(out), "--clusters", "2", "--batches", "1"]) == 0
    batch = json.loads((out / "batch_01.json").read_text())
    assert batch["clusters"] and batch["labels"]
    assert rd.main(["--root", str(fake_repo), "report"]) == 0
    audit = json.loads((fake_repo / "research" / "audits" / "rediscovery_audit.json").read_text())
    assert audit["total"] == 2
    assert (fake_repo / "research" / "audits" / "REDISCOVERY_AUDIT.md").exists()

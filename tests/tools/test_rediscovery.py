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


def test_cli_export_and_report_on_fake_repo(fake_repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "packets"
    assert rd.main(["--root", str(fake_repo), "export", "--out", str(out), "--clusters", "2", "--batches", "1"]) == 0
    batch = json.loads((out / "batch_01.json").read_text())
    assert batch["clusters"] and batch["labels"]
    assert rd.main(["--root", str(fake_repo), "report"]) == 0
    audit = json.loads((fake_repo / "research" / "audits" / "rediscovery_audit.json").read_text())
    assert audit["total"] == 2
    assert (fake_repo / "research" / "audits" / "REDISCOVERY_AUDIT.md").exists()

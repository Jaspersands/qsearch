from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from tools.arxiv_watch.tracks import TRACKS, classify
from tools.arxiv_watch.watch import label_for, replay_seeds, run
from tools.corpus.api import Corpus
from tools.corpus.sources.arxiv import Client, Paper, parse_atom

FIXTURE = Path(__file__).parent / "fixtures" / "arxiv_atom_sample.xml"


def _paper(arxiv_id: str, title: str, abstract: str, published: str = "2026-10-15") -> Paper:
    return Paper(arxiv_id, "v1", title, abstract, ["A. Author"], published, published, ["quant-ph"], f"https://arxiv.org/abs/{arxiv_id}")


def test_parse_atom_reads_real_api_response() -> None:
    papers = parse_atom(FIXTURE.read_bytes())
    assert len(papers) == 5
    first = papers[0]
    assert first.title.startswith("Cyclotomic Cosets: Hidden Subgroup")
    assert first.arxiv_id.count(".") == 1 and "v" not in first.arxiv_id
    assert first.version.startswith("v")
    assert first.published == "2026-09-28"
    assert first.abstract and first.authors and first.categories
    assert first.url == f"https://arxiv.org/abs/{first.arxiv_id}"


def test_parse_atom_handles_old_style_ids() -> None:
    xml = FIXTURE.read_text()
    entry_id = xml.split("<entry>")[1].split("<id>")[1].split("</id>")[0]
    xml = xml.replace(entry_id, "http://arxiv.org/abs/quant-ph/0501044v2", 1)
    assert parse_atom(xml.encode())[0].arxiv_id == "quant-ph/0501044"


def test_client_builds_query_and_waits_between_calls() -> None:
    urls: list[str] = []
    sleeps: list[float] = []

    class Response:
        def __init__(self, body: bytes) -> None:
            self.body = body

        def read(self) -> bytes:
            return self.body

        def __enter__(self):
            return self

        def __exit__(self, *exc) -> None:
            return None

    def opener(request, timeout=0):
        urls.append(request.full_url)
        return Response(FIXTURE.read_bytes())

    client = Client(opener=opener, sleep=sleeps.append, delay=3.0)
    client.search('abs:"dihedral"', max_results=7)
    client.search('abs:"hidden shift"', max_results=7)
    query = parse_qs(urlparse(urls[0]).query)
    assert query["search_query"] == ['abs:"dihedral"']
    assert query["max_results"] == ["7"] and query["sortBy"] == ["submittedDate"]
    assert sleeps == [3.0]


def test_client_cache_replays_without_network(tmp_path: Path) -> None:
    calls: list[str] = []

    class Response:
        def read(self) -> bytes:
            return FIXTURE.read_bytes()

        def __enter__(self):
            return self

        def __exit__(self, *exc) -> None:
            return None

    def opener(request, timeout=0):
        calls.append(request.full_url)
        return Response()

    Client(opener=opener, sleep=lambda s: None, cache_dir=tmp_path).search("abs:x", max_results=5)
    papers = Client(opener=None, sleep=lambda s: None, cache_dir=tmp_path).search("abs:x", max_results=5)
    assert len(calls) == 1 and len(papers) == 5


@pytest.mark.parametrize(
    ("text", "track"),
    [
        ("A subexponential algorithm for the dihedral hidden subgroup problem", "dcp"),
        ("Optimization by decoded quantum interferometry", "dqi_opi"),
        ("Belief propagation with quantum messages for polar codes", "bpqm_gibbs"),
        ("Regev's multidimensional factoring algorithm made space efficient", "number_theory"),
        ("Permutation code equivalence and the Goppa code distinguisher", "code_equivalence"),
        ("Quantum Fourier transform over the symmetric group", "representation"),
        ("Learning with errors is hard for quantum lattice algorithms", "lattice"),
        ("Group QFT primitives for wreath products", "representation"),
        ("Quantum algorithms for representation-theoretic multiplicities", "representation"),
        ("Diameters of finite simple groups", "representation"),
        ("Locking classical information in a small subsystem", "state_discrimination"),
        ("Solving shift problems and the hidden coset problem", "hidden_shift"),
        ("The syzygy distinguisher for shortened dual codes", "code_equivalence"),
        ("Attacks on subcodes of algebraic geometry codes", "code_equivalence"),
    ],
)
def test_classify_assigns_tracks(text: str, track: str) -> None:
    assert track in classify(text)


def test_classify_unrelated_text_has_no_track() -> None:
    assert classify("A survey of superconducting qubit fabrication yields") == []


def test_every_track_has_a_category_limited_query() -> None:
    for track in TRACKS.values():
        assert "cat:quant-ph" in track.arxiv_query()


def test_label_rules() -> None:
    kill = _paper("2610.00001", "Dequantizing decoded quantum interferometry", "We give a classical algorithm matching DQI.")
    scoop = _paper("2610.00002", "An exponential quantum speedup for dihedral cosets", "A polynomial-time quantum algorithm.")
    plain = _paper("2610.00003", "Notes on dihedral coset states", "We study coset states.")
    off = _paper("2610.00004", "Superconducting fabrication", "Qubit yields.")
    assert label_for(kill, classify(kill.title + kill.abstract), cited=False)[0] == "possible-kill"
    assert label_for(scoop, classify(scoop.title + scoop.abstract), cited=False)[0] == "possible-scoop"
    assert label_for(plain, classify(plain.title + plain.abstract), cited=False)[0] == "related"
    assert label_for(off, [], cited=False)[0] == "unrelated"
    assert label_for(plain, ["dcp"], cited=True)[0] == "already-cited"


def test_peripheral_tracks_and_non_quantum_papers_stay_related() -> None:
    query = _paper("2610.00005", "Quantum query complexity of maximum degree", "We prove a tight lower bound.")
    assert classify(query.title) == ["query_and_fourier"]
    assert label_for(query, ["query_and_fourier"], cited=False)[0] == "related"
    math = _paper("2610.00006", "Imaginary quadratic fields of class number at most 2000", "A lower bound on class numbers.")
    assert label_for(math, classify(math.title + math.abstract), cited=False)[0] == "related"


def test_relabel_recomputes_labels_without_fetching(fake_repo: Path) -> None:
    from tools.arxiv_watch.watch import relabel

    corpus = Corpus(fake_repo)
    corpus.refresh()
    papers = [_paper("2610.22222", "Quantum query complexity of maximum degree", "A tight lower bound.")]
    run(fake_repo, FakeClient(papers), corpus, since="2026-10-01", tracks={"q": TRACKS["query_and_fourier"]})
    path = fake_repo / "research" / "audits" / "arxiv_collisions.json"
    state = json.loads(path.read_text())
    state["papers"]["2610.22222"]["label"] = "possible-kill"
    path.write_text(json.dumps(state))
    changed = relabel(fake_repo, corpus)
    assert changed == 1
    assert json.loads(path.read_text())["papers"]["2610.22222"]["label"] == "related"


class FakeClient:
    def __init__(self, papers: list[Paper]) -> None:
        self.papers = papers
        self.queries: list[str] = []

    def search(self, query: str, max_results: int = 50, start: int = 0) -> list[Paper]:
        self.queries.append(query)
        return list(self.papers)


def test_run_writes_collisions_and_digest_then_dedupes(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    papers = [
        _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout."),
        _paper("2408.08292", "Optimization by Decoded Quantum Interferometry", "Decoding.", published="2026-10-14"),
        _paper("2601.00001", "Old dihedral paper", "Dihedral coset states.", published="2026-01-01"),
    ]
    client = FakeClient(papers)
    report = run(fake_repo, client, corpus, since="2026-10-01", tracks={"dcp": TRACKS["dcp"], "dqi_opi": TRACKS["dqi_opi"]})
    assert report.new == 2
    state = json.loads((fake_repo / "research" / "audits" / "arxiv_collisions.json").read_text())
    record = state["papers"]["2610.11111"]
    assert record["label"] == "possible-kill"
    assert record["nearest"][0]["doc_id"] == "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"
    assert state["papers"]["2408.08292"]["label"] == "already-cited"
    assert "2601.00001" not in state["papers"]
    digest = (fake_repo / "research" / "audits" / "ARXIV_WATCH.md").read_text()
    assert "Possible kills" in digest and "2610.11111" in digest
    again = run(fake_repo, FakeClient(papers), corpus, since="2026-10-01", tracks={"dcp": TRACKS["dcp"]})
    assert again.new == 0


def test_replay_seeds_reports_track_accuracy(fake_repo: Path) -> None:
    result = replay_seeds(fake_repo)
    assert result["checked"] == 1
    assert result["matched"] == 1

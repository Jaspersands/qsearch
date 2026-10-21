from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from tools.arxiv_watch.tracks import CATEGORIES, TRACKS, classify
from tools.arxiv_watch.verdicts import VERDICTS_FILE, load_verdicts, set_verdict
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


def test_client_fetches_papers_by_id() -> None:
    urls: list[str] = []

    class Response:
        def read(self) -> bytes:
            return FIXTURE.read_bytes()

        def __enter__(self):
            return self

        def __exit__(self, *exc) -> None:
            return None

    def opener(request, timeout=0):
        urls.append(request.full_url)
        return Response()

    papers = Client(opener=opener, sleep=lambda s: None).get(["2408.08292", "quant-ph/9508027"])
    query = parse_qs(urlparse(urls[0]).query)
    assert query["id_list"] == ["2408.08292,quant-ph/9508027"]
    assert len(papers) == 5


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


def test_every_track_query_ands_its_phrases_with_the_category_filter() -> None:
    categories = re.fullmatch(r"\((cat:[\w.-]+)( OR cat:[\w.-]+)*\)", CATEGORIES)
    assert categories is not None and "cat:quant-ph" in CATEGORIES
    for name, track in TRACKS.items():
        query = track.arxiv_query()
        phrases, sep, tail = query.rpartition(" AND ")
        assert sep and tail == CATEGORIES, name  # the category filter restricts every phrase
        assert phrases.startswith("(") and phrases.endswith(")"), name
        terms = phrases[1:-1].split(" OR ")
        assert terms == [f'abs:"{phrase}"' for phrase in track.phrases], name
        assert all('"' not in phrase and " AND " not in phrase for phrase in track.phrases), name


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


# --- paging, overlap and idempotent runs --------------------------------------------------------


class PagedClient:
    """Serves a newest-first result list in pages, like the arXiv API with sortBy=submittedDate."""

    def __init__(self, papers: list[Paper]) -> None:
        self.papers = sorted(papers, key=lambda p: p.published, reverse=True)
        self.calls: list[tuple[int, int]] = []

    def search(self, query: str, max_results: int = 50, start: int = 0) -> list[Paper]:
        self.calls.append((start, max_results))
        return self.papers[start : start + max_results]


def _daily(count: int, newest: str = "2026-10-18", per_day: int = 2) -> list[Paper]:
    day0 = dt.date.fromisoformat(newest)
    return [
        _paper(f"2610.{50000 + i:05d}", f"Dihedral coset note {i}", "Coset states.", (day0 - dt.timedelta(days=i // per_day)).isoformat())
        for i in range(count)
    ]


def _state(root: Path) -> dict:
    return json.loads((root / "research" / "audits" / "arxiv_collisions.json").read_text())


def test_run_pages_until_results_are_older_than_since(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    papers = _daily(250)
    since = "2026-07-20"
    client = PagedClient(papers)
    report = run(fake_repo, client, corpus, since=since, tracks={"dcp": TRACKS["dcp"]}, page_size=100, today="2026-10-19")
    assert client.calls == [(0, 100), (100, 100)]  # the second page reaches past `since`, so no third
    in_range = {p.arxiv_id for p in papers if p.published >= since}
    assert len(in_range) == 182 and set(_state(fake_repo)["papers"]) == in_range
    assert report.truncated == {}


def test_hitting_the_page_cap_is_recorded_and_reported(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    papers = _daily(250)
    since = "2026-07-20"
    report = run(fake_repo, PagedClient(papers), corpus, since=since, tracks={"dcp": TRACKS["dcp"]},
                 page_size=50, max_pages=2, today="2026-10-19")
    oldest = min(p.published for p in papers[:100])
    assert report.truncated["dcp"]["oldest_seen"] == oldest
    gaps = _state(fake_repo)["gaps"]
    assert gaps == [{"track": "dcp", "since": since, "until": oldest, "found_on": "2026-10-19"}]
    digest = (fake_repo / "research" / "audits" / "ARXIV_WATCH.md").read_text()
    assert "Incomplete coverage" in digest and f"| dcp | {since} to {oldest} |" in digest
    # A backfill that is not cut short closes the gap.
    again = run(fake_repo, PagedClient(papers), corpus, since=since, tracks={"dcp": TRACKS["dcp"]},
                page_size=100, max_pages=5, today="2026-10-20")
    assert again.truncated == {} and again.new == 82
    assert _state(fake_repo)["gaps"] == []
    assert "Incomplete coverage" not in (fake_repo / "research" / "audits" / "ARXIV_WATCH.md").read_text()


def test_paging_goes_through_the_paced_client(fake_repo: Path) -> None:
    urls: list[str] = []
    sleeps: list[float] = []
    empty = b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>'

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
        start = parse_qs(urlparse(request.full_url).query)["start"][0]
        return Response(FIXTURE.read_bytes() if start == "0" else empty)

    corpus = Corpus(fake_repo)
    corpus.refresh()
    client = Client(opener=opener, sleep=sleeps.append, delay=3.0)
    # The fixture's five entries reach back to 2025-12-01, so a full page asks for the next one.
    run(fake_repo, client, corpus, since="2025-06-01", tracks={"dcp": TRACKS["dcp"]}, page_size=5, today="2026-10-19")
    assert [parse_qs(urlparse(u).query)["start"] for u in urls] == [["0"], ["5"]]
    assert sleeps == [3.0]


def test_paper_announced_after_the_last_run_is_still_recorded(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    tracks = {"dcp": TRACKS["dcp"]}
    early = _paper("2610.00001", "Dequantizing the dihedral coset problem", "An efficient classical algorithm.", "2026-10-14")
    run(fake_repo, FakeClient([early]), corpus, tracks=tracks, today="2026-10-19")
    # Submitted Friday 2026-10-16 after the cutoff, so first listed after the Monday run.
    friday = _paper("2610.99999", "Dequantizing dihedral cosets again", "An efficient classical algorithm.", "2026-10-16")
    report = run(fake_repo, FakeClient([early, friday]), corpus, tracks=tracks, today="2026-10-26")
    assert report.new == 1
    state = _state(fake_repo)
    assert "2610.99999" in state["papers"]
    assert state["papers"]["2610.00001"]["first_seen"] == "2026-10-19"  # seen papers are not re-reported


def test_run_without_new_papers_leaves_the_outputs_untouched(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    papers = [_paper("2610.11111", "Dihedral coset note", "Coset states.", "2026-10-15")]
    run(fake_repo, FakeClient(papers), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    paths = [fake_repo / "research" / "audits" / name for name in ("arxiv_collisions.json", "ARXIV_WATCH.md")]
    before = [path.read_bytes() for path in paths]
    report = run(fake_repo, FakeClient(papers), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-26")
    assert report.new == 0
    assert [path.read_bytes() for path in paths] == before  # so the weekly job opens no pull request


# --- labels ---------------------------------------------------------------------------------------

# Titles and sentences from papers in research/audits/arxiv_collisions.json (2026-10-18 run).
LABEL_CASES = [
    # Positive quantum results whose wording tripped the old kill cues ("lower bound", "limitation", ...).
    ("2609.35656", "The power of oracle access: Optimal sample and query complexity of the abelian state hidden subgroup problem",
     "In the query model, we give a time-efficient quantum algorithm using O(log(|G/H|)/sqrt(eps)) forward and inverse "
     "queries, and prove a matching lower bound which holds even in the stronger conjugate-query setting.",
     ["nonabelian_hsp"], "possible-scoop"),
    ("2609.38060", "Classical Verification of Quantum Computation with Quasilinear Resources, from Compiled Nonlocal Games",
     "This is achieved by constructing a new computational self-test for certifying the prover's quantum state and using "
     "it to dequantize the efficient verification protocol of Broadbent (ToC 2018).",
     ["lattice"], "related"),
    ("2610.00502", "Quantum Algorithms for OPI Variants Beyond Locality and Classical Decodability",
     "To date, applications that have not been dequantized have relied on efficient classical decoders. We also give an "
     "efficient classical algorithm under a stronger three-fold multiplication property, leaving intermediate regimes "
     "as candidates for quantum advantage.",
     ["dqi_opi"], "possible-scoop"),
    ("2610.03566", "Gibbs state preparation through quantum decoding",
     "We propose a Gibbs state preparation algorithm that exploits algebraic structure in the Hamiltonian. However, we "
     '"dequantize" this strategy for commuting Hamiltonians, contributing a classical rejection sampler.',
     ["dqi_opi", "bpqm_gibbs"], "possible-scoop"),
    ("2610.03645", "Exponential quantum space advantage in random data streams",
     "We show two unconditional quantum space advantages in the random-order streaming model. Our lower bound is shown "
     "using density-restoring partitions.",
     ["dqi_opi"], "possible-scoop"),
    ("2610.04597", "Efficient Quantum State Identity Testing",
     "We present two quantum algorithms with complementary guarantees on circuit depth and sample complexity. We also "
     "prove a matching sample complexity lower bound for any quantum algorithm with failure probability at most delta.",
     ["representation"], "possible-scoop"),
    ("2610.16827", "The Quantum Character Transform",
     "I give complementary quantum algorithms for class convolution based on direct class-sum block encoding, as well as "
     "characterizing the central information used in hidden-subgroup problems, including its limitations for graph isomorphism.",
     ["nonabelian_hsp"], "possible-scoop"),
    # A cap on DQI's margin over classical completion is kill-like even though it mentions quantum advantage.
    ("2610.06753", "Discovering New Problems for Decoded Quantum Interferometry",
     "It is hard to tell which problems could give it a quantum advantage. We prove that under worst-case Hamming decoding "
     "DQI's guarantee can exceed Prange completion by at most (sqrt(2)-1)/2, so no candidate in this setting can exceed "
     "OPI's margin.",
     ["dqi_opi"], "possible-kill"),
    # Kills: a classical algorithm framed in the title, or a stated no-advantage result.
    ("2609.40250", "An (almost) efficient classical algorithm for sampling from typical Gibbs states",
     "Gibbs state preparation has emerged as a potential avenue for quantum advantage. Here, we give strong evidence "
     "against an exponential quantum advantage in Gibbs sampling.",
     ["bpqm_gibbs"], "possible-kill"),
    ("2609.40302", "Solving Sparse SDPs in Sublinear Time: A Classical Algorithm Inspired by the Quantum OR Lemma",
     "We give the first sublinear-time classical solvers for sparse semidefinite programs. This suggests a quartic "
     "quantum speedup when m is close to n.",
     ["bpqm_gibbs"], "possible-kill"),
    ("2609.40036", "Cycle Codes and Decoded Quantum Interferometry",
     "However, these no-go results rely on minimum distance assumptions that underestimate actual DQI performance. "
     "These bounds rule out quantum advantage in the regimes we analyze.",
     ["dqi_opi"], "possible-kill"),
    # Scoops that should stay scoops.
    ("2609.40260", "Quantum Algorithms for Minimum Generating Set",
     "In this paper, we present a polynomial-time quantum algorithm for computing a minimum-sized generating set.",
     ["representation"], "possible-scoop"),
    ("2610.01902", "Exponential quantum advantages for decoded quantum interferometry in the streaming setting",
     "Any classical algorithm that produces an answer satisfying just 76% of the constraints requires polynomial space.",
     ["dqi_opi"], "possible-scoop"),
    ("2609.35101", "From Simple Sources to Quantum Advantage: Homomorphic Polynomial Transduction via Relative Decoding",
     "We recast this approach as quantum state transduction through algebra homomorphisms.",
     ["dqi_opi"], "possible-scoop"),
    # Classical hardness is not a classical win.
    ("2609.40310", "Planted Cliques and Quantum Symmetry-Adapted Measurements",
     "Detection is statistically possible but conjectured hard for polynomial-time classical algorithms.",
     ["representation"], "related"),
    # Generic negative results for quantum algorithms.
    ("2610.90001", "Query lower bounds for the dihedral coset problem",
     "We prove that any quantum algorithm requires exponentially many coset states.", ["dcp"], "possible-kill"),
    ("2610.90002", "No quantum speedup for hidden shifts of bent functions",
     "We study hidden shift problems for quantum computers.", ["hidden_shift"], "possible-kill"),
    ("2610.90003", "Notes on dihedral coset states",
     "Quantum algorithms with superpolynomial speed-ups motivate this survey of coset states.", ["dcp"], "related"),
]


@pytest.mark.parametrize(("arxiv_id", "title", "abstract", "tracks", "expected"), LABEL_CASES, ids=[c[0] for c in LABEL_CASES])
def test_labels_on_committed_papers(arxiv_id: str, title: str, abstract: str, tracks: list[str], expected: str) -> None:
    assert label_for(_paper(arxiv_id, title, abstract), tracks, cited=False)[0] == expected


# --- verdicts -------------------------------------------------------------------------------------


def test_verdict_round_trip(tmp_path: Path) -> None:
    assert load_verdicts(tmp_path) == {"verdicts": {}}
    entry = set_verdict(tmp_path, "2610.11111", "false-alarm", "cue spurious", "human", today="2026-10-21")
    expected = {"verdict": "false-alarm", "reason": "cue spurious", "action": None, "by": "human", "reviewed_on": "2026-10-21"}
    assert entry == expected
    assert load_verdicts(tmp_path) == {"verdicts": {"2610.11111": expected}}
    text = (tmp_path / VERDICTS_FILE).read_text(encoding="utf-8")
    assert text.endswith("}\n") and json.loads(text) == {"verdicts": {"2610.11111": expected}}


def test_set_verdict_rejects_unknown_value(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        set_verdict(tmp_path, "2610.11111", "maybe", "unsure", "human")
    assert not (tmp_path / VERDICTS_FILE).exists()

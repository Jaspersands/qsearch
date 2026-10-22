from __future__ import annotations

import datetime as dt
import json
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from tools.arxiv_watch.tracks import CATEGORIES, TRACKS, classify
from tools.arxiv_watch.verdicts import VERDICTS_FILE, load_verdicts, normalize_id, set_verdict
from tools.arxiv_watch.watch import label_for, recheck_cited, relabel, render_digest, replay_seeds, run
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
    # A weekly run that is not cut short but starts after the gap, and a run of another track,
    # leave it listed; so does a backfill that is cut short again.
    weekly = run(fake_repo, PagedClient(papers), corpus, tracks={"dcp": TRACKS["dcp"]}, page_size=100, max_pages=5, today="2026-10-26")
    assert weekly.truncated == {} and _state(fake_repo)["gaps"] == gaps
    other = [_paper("2610.70000", "Decoded quantum interferometry note", "DQI.", "2026-10-25")]
    assert run(fake_repo, FakeClient(other), corpus, tracks={"dqi_opi": TRACKS["dqi_opi"]}, today="2026-10-26").saved
    assert _state(fake_repo)["gaps"] == gaps
    cut = run(fake_repo, PagedClient(papers), corpus, since="2026-07-10", tracks={"dcp": TRACKS["dcp"]},
              page_size=50, max_pages=2, today="2026-10-27")
    assert cut.truncated and gaps[0] in _state(fake_repo)["gaps"]
    # A backfill that is not cut short closes the gap.
    again = run(fake_repo, PagedClient(papers), corpus, since="2026-07-10", tracks={"dcp": TRACKS["dcp"]},
                page_size=100, max_pages=5, today="2026-10-28")
    assert again.truncated == {} and again.new == 102
    assert _state(fake_repo)["gaps"] == []
    assert "Incomplete coverage" not in (fake_repo / "research" / "audits" / "ARXIV_WATCH.md").read_text()


def test_each_track_window_starts_a_week_before_its_own_last_fetch(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    path = fake_repo / "research" / "audits" / "arxiv_collisions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"updated": "2026-10-12", "papers": {}}), encoding="utf-8")  # every track ran 10-12
    dcp, dqi = {"dcp": TRACKS["dcp"]}, {"dqi_opi": TRACKS["dqi_opi"]}
    assert run(fake_repo, FakeClient([_paper("2610.00001", "Dihedral coset note", "Coset states.", "2026-10-18")]), corpus,
               tracks=dcp, today="2026-10-19").saved
    state = _state(fake_repo)
    assert state["updated"] == "2026-10-19" and state["tracks_updated"]["dcp"] == "2026-10-19"
    assert state["tracks_updated"]["dqi_opi"] == "2026-10-12"  # recorded before `updated` moved
    # A --since that starts after a track's usual window leaves its date, so the skipped days come next time.
    narrow = [_paper("2610.00002", "Decoded quantum interferometry note", "DQI.", "2026-10-20")]
    assert run(fake_repo, FakeClient(narrow), corpus, since="2026-10-19", tracks=dqi, today="2026-10-21").saved
    assert _state(fake_repo)["tracks_updated"]["dqi_opi"] == "2026-10-12"
    # So dqi_opi's next window still starts 2026-10-05, and a paper submitted 10-06 but listed late is found.
    late = [_paper("2610.00003", "Decoded quantum interferometry again", "DQI.", "2026-10-06")]
    assert run(fake_repo, FakeClient(late), corpus, tracks=dqi, today="2026-10-26").new == 1
    assert _state(fake_repo)["tracks_updated"]["dqi_opi"] == "2026-10-26"


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

    set_verdict(tmp_path, "arXiv:2610.22222v3", "kill", "versioned", "human", today="2026-10-21")
    assert set(json.loads((tmp_path / VERDICTS_FILE).read_text(encoding="utf-8"))["verdicts"]) == {"2610.11111", "2610.22222"}


def test_reviewed_table_is_ordered_by_verdict_then_id_and_marks_done_actions(tmp_path: Path) -> None:
    def entry(verdict: str, action: str | None = None, done: bool = False) -> dict:
        base = {"verdict": verdict, "reason": "r", "action": action, "by": "human", "reviewed_on": "2026-10-21"}
        return {**base, "action_done": True} if done else base

    verdicts = {
        "2610.55555": entry("false-alarm"),
        "2610.22222": entry("should-cite", "Cite it in X.", done=True),
        "2610.44444": entry("kill", "Narrow note Y."),
        "2610.11111": entry("should-cite", "Cite it in Z."),
        "2610.33333": entry("related-only"),
    }
    digest = render_digest({"updated": "2026-10-21", "papers": {}}, verdicts=verdicts)
    rows = [line for line in _section(digest, "Reviewed").splitlines() if line.startswith("| 2610.")]
    assert [row.split(" | ")[0][2:] for row in rows] == ["2610.44444", "2610.11111", "2610.22222", "2610.33333", "2610.55555"]
    assert rows[1].endswith("| Cite it in Z. |") and rows[2].endswith("| Cite it in X. (done) |")


def test_set_verdict_rejects_unknown_value(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        set_verdict(tmp_path, "2610.11111", "maybe", "unsure", "human")
    assert not (tmp_path / VERDICTS_FILE).exists()


@pytest.mark.parametrize(
    ("raw", "bare"),
    [("0704.0001", "0704.0001"), ("1412.9999v2", "1412.9999"), ("1501.00001", "1501.00001"),
     ("arXiv:2610.06753v2", "2610.06753"), ("quant-ph/0501044v2", "quant-ph/0501044"), ("math.NT/0601001", "math.NT/0601001")],
)
def test_normalize_id_accepts_real_ids(raw: str, bare: str) -> None:
    assert normalize_id(raw) == bare


# A dropped or extra digit (four digits after the dot from 1501 on, five before), month 00 or 13,
# or a new-style id before 0704.
@pytest.mark.parametrize("raw", ["2610.0675", "1501.1234", "1412.12345", "0704.12345", "2613.06753", "2600.06753", "0612.1234"])
def test_normalize_id_rejects_impossible_new_style_ids(raw: str) -> None:
    with pytest.raises(ValueError, match="not an arXiv id"):
        normalize_id(raw)


def _write_verdicts(root: Path, data) -> None:
    (root / VERDICTS_FILE).parent.mkdir(parents=True, exist_ok=True)
    (root / VERDICTS_FILE).write_text(json.dumps(data), encoding="utf-8")


def _hand(verdict: str = "false-alarm", by: str | None = "human") -> dict:
    entry = {"verdict": verdict, "reason": "read it by hand", "action": None, "reviewed_on": "2026-10-21"}
    return {**entry, "by": by} if by else entry


def test_hand_written_keys_are_read_as_bare_ids(tmp_path: Path) -> None:
    for key in ("arXiv:2610.11111v1", "2610.11111v2", "https://arxiv.org/abs/2610.11111v3", "quant-ph/0501044v2"):
        _write_verdicts(tmp_path, {"verdicts": {key: _hand()}})
        assert set(load_verdicts(tmp_path)["verdicts"]) == {"2610.11111" if "2610" in key else "quant-ph/0501044"}, key

    # Two keys for one paper: a person's verdict outranks a judge's, and two of a kind are ambiguous.
    judge = _hand("kill", by="judge:x")
    _write_verdicts(tmp_path, {"verdicts": {"2610.11111": judge, "arXiv:2610.11111v1": _hand()}})
    assert load_verdicts(tmp_path)["verdicts"] == {"2610.11111": _hand()}
    _write_verdicts(tmp_path, {"verdicts": {"arXiv:2610.11111v1": _hand(by=None), "2610.11111": judge}})
    assert load_verdicts(tmp_path)["verdicts"] == {"2610.11111": _hand(by=None)}
    _write_verdicts(tmp_path, {"verdicts": {"2610.11111": _hand(), "2610.11111v1": _hand("kill")}})
    with pytest.raises(ValueError, match="2610.11111"):
        load_verdicts(tmp_path)


@pytest.mark.parametrize(
    "data",
    [[], {"verdicts": None}, {"verdicts": []}, {"verdicts": {"2610.11111": "false-alarm"}},
     {"verdicts": {"2610.11111": {"verdict": "maybe"}}}, {"verdicts": {"see 2610.11111": {"verdict": "kill"}}}],
    ids=["list", "null", "verdicts-list", "string-entry", "unknown-verdict", "bad-key"],
)
def test_malformed_verdicts_file_is_a_clean_error(fake_repo: Path, monkeypatch, capsys, data) -> None:
    from tools.arxiv_watch import judge, watch

    def refuse(*args, **kwargs):
        raise AssertionError("a malformed verdicts file must stop the watch before it fetches")

    monkeypatch.setattr(watch, "Client", refuse)
    monkeypatch.setattr(watch, "Corpus", refuse)
    _write_verdicts(fake_repo, data)
    with pytest.raises(ValueError, match="arxiv_verdicts.json"):
        load_verdicts(fake_repo)
    written = (fake_repo / VERDICTS_FILE).read_bytes()
    for argv in ([], ["--relabel"], ["--verdict", "2610.22222", "related-only", "--reason", "x"]):
        assert watch.main(["--root", str(fake_repo), *argv]) == 2, argv
        assert capsys.readouterr().err.startswith("error: research/audits/arxiv_verdicts.json: "), argv
    assert (fake_repo / VERDICTS_FILE).read_bytes() == written
    assert not (fake_repo / "research" / "audits" / "ARXIV_WATCH.md").exists()
    assert judge.main(["--root", str(fake_repo), "--export", str(fake_repo / "judge")]) == 2
    assert capsys.readouterr().err.startswith("error: research/audits/arxiv_verdicts.json: ")


def _section(digest: str, heading: str) -> str:
    """One `## heading` section of the digest, up to the next section."""
    start = digest.index(f"## {heading}\n")
    end = digest.find("\n## ", start)
    return digest[start:] if end == -1 else digest[start:end]


def test_paper_with_a_verdict_leaves_the_flagged_list(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    tracks = {"dcp": TRACKS["dcp"]}
    kill = _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout.")
    client = FakeClient([kill])
    run(fake_repo, client, corpus, tracks=tracks, today="2026-10-19")
    digest_path = fake_repo / "research" / "audits" / "ARXIV_WATCH.md"
    assert "2610.11111" in _section(digest_path.read_text(), "Possible kills")

    set_verdict(fake_repo, "2610.11111", "false-alarm", "cue spurious", "human", today="2026-10-21")
    set_verdict(fake_repo, "2610.99999", "related-only", "never fetched", "human", today="2026-10-21")
    report = run(fake_repo, client, corpus, tracks=tracks, today="2026-10-26")
    assert report.new == 0 and report.saved  # the verdict alone rewrites the outputs
    record = _state(fake_repo)["papers"]["2610.11111"]
    assert record["verdict"]["verdict"] == "false-alarm" and record["label"] == "possible-kill"
    digest = digest_path.read_text()
    assert "2610.11111" not in _section(digest, "Possible kills")
    reviewed = _section(digest, "Reviewed")
    assert "| 2610.11111 |" in reviewed and "false-alarm" in reviewed
    assert "| 2610.99999 | not stored |" in reviewed

    paths = [fake_repo / "research" / "audits" / name for name in ("arxiv_collisions.json", "ARXIV_WATCH.md")]
    before = [path.read_bytes() for path in paths]
    assert not run(fake_repo, client, corpus, tracks=tracks, today="2026-11-02").saved
    assert [path.read_bytes() for path in paths] == before

    (fake_repo / VERDICTS_FILE).write_text(json.dumps({"verdicts": {}}), encoding="utf-8")
    assert run(fake_repo, client, corpus, tracks=tracks, today="2026-11-09").saved  # a withdrawn verdict is dropped
    assert "verdict" not in _state(fake_repo)["papers"]["2610.11111"]
    assert "2610.11111" in _section(digest_path.read_text(), "Possible kills")


def test_verdict_added_by_hand_for_an_unstored_paper_reaches_the_digest(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    tracks = {"dcp": TRACKS["dcp"]}
    client = FakeClient([_paper("2610.11111", "Dihedral coset note", "Coset states.")])
    run(fake_repo, client, corpus, tracks=tracks, today="2026-10-19")
    collisions, digest = (fake_repo / "research" / "audits" / name for name in ("arxiv_collisions.json", "ARXIV_WATCH.md"))
    assert not run(fake_repo, client, corpus, tracks=tracks, today="2026-10-20").saved
    stored = collisions.read_bytes()

    entry = {"verdict": "related-only", "reason": "hand", "action": None, "by": "human", "reviewed_on": "2026-10-21"}
    (fake_repo / VERDICTS_FILE).write_text(json.dumps({"verdicts": {"2610.77777": entry}}), encoding="utf-8")
    report = run(fake_repo, client, corpus, tracks=tracks, today="2026-10-26")
    assert report.saved and report.new == 0
    assert "| 2610.77777 | not stored |" in _section(digest.read_text(), "Reviewed")
    assert collisions.read_bytes() == stored  # no stored record changed, so only the digest is re-rendered

    rendered = digest.read_bytes()
    assert not run(fake_repo, client, corpus, tracks=tracks, today="2026-11-02").saved
    assert digest.read_bytes() == rendered


def test_flagged_paper_becomes_already_cited_once_a_note_cites_it(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    tracks = {"dcp": TRACKS["dcp"]}
    client = FakeClient([
        _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout."),
        _paper("2610.33333", "Dequantizing the dihedral coset problem", "An efficient classical algorithm for quantum coset states."),
    ])
    assert run(fake_repo, client, corpus, tracks=tracks, today="2026-10-19").relabelled == 0
    assert {record["label"] for record in _state(fake_repo)["papers"].values()} == {"possible-kill"}

    set_verdict(fake_repo, "2610.33333", "should-cite", "cite it", "human", today="2026-10-20")
    note = "# Cites Kill\n\nThis note builds on arXiv:2610.11111v1 and on arXiv:2610.33333.\n"
    (fake_repo / "research" / "CITES_KILL.md").write_text(note, encoding="utf-8")
    corpus.refresh()
    report = run(fake_repo, client, corpus, tracks=tracks, today="2026-10-26")
    assert report.relabelled == 1 and report.new == 0 and report.saved
    state = _state(fake_repo)
    cited = state["papers"]["2610.11111"]
    assert (cited["label"], cited["relabelled_on"], cited["relabelled_from"]) == ("already-cited", "2026-10-26", "possible-kill")
    reviewed = state["papers"]["2610.33333"]
    assert reviewed["label"] == "possible-kill" and "relabelled_on" not in reviewed  # a verdict-bearing paper is untouched
    assert run(fake_repo, client, corpus, tracks=tracks, today="2026-10-27").relabelled == 0

    # --relabel keeps the demotion record while the paper is cited and drops it once it is flagged again.
    relabel(fake_repo, corpus)
    cited = _state(fake_repo)["papers"]["2610.11111"]
    assert (cited["label"], cited["relabelled_on"], cited["relabelled_from"]) == ("already-cited", "2026-10-26", "possible-kill")
    (fake_repo / "research" / "CITES_KILL.md").unlink()
    corpus.refresh()
    assert relabel(fake_repo, corpus) == 2
    flagged = _state(fake_repo)["papers"]["2610.11111"]
    assert flagged["label"] == "possible-kill" and "relabelled_on" not in flagged and "relabelled_from" not in flagged


def test_recheck_cited_demotes_only_flagged_papers(fake_repo: Path) -> None:
    (fake_repo / "research" / "CITES_ALL.md").write_text(
        "# Cites All\n\nSee arXiv:2610.11111, arXiv:2610.22222, arXiv:2610.33333 and arXiv:2610.44444.\n", encoding="utf-8"
    )
    corpus = Corpus(fake_repo)
    corpus.refresh()
    labels = {"2610.11111": "possible-kill", "2610.22222": "possible-scoop", "2610.33333": "related", "2610.44444": "unrelated"}
    state = {"papers": {arxiv_id: {"arxiv_id": arxiv_id, "label": label} for arxiv_id, label in labels.items()}}
    assert recheck_cited(state, corpus, "2026-10-26") == 2
    assert {arxiv_id: record["label"] for arxiv_id, record in state["papers"].items()} == {
        "2610.11111": "already-cited", "2610.22222": "already-cited", "2610.33333": "related", "2610.44444": "unrelated"}
    assert "relabelled_from" not in state["papers"]["2610.33333"]


def test_relabel_copies_verdicts_onto_the_records(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    kill = _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout.")
    run(fake_repo, FakeClient([kill]), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    set_verdict(fake_repo, "2610.11111", "false-alarm", "cue spurious", "human", today="2026-10-21")  # by hand, no run since
    assert "verdict" not in _state(fake_repo)["papers"]["2610.11111"]
    relabel(fake_repo, corpus)
    assert _state(fake_repo)["papers"]["2610.11111"]["verdict"]["verdict"] == "false-alarm"


def test_recheck_cited_is_fast_for_many_flags_sharing_a_trailing_token(fake_repo: Path) -> None:
    ids = [f"{24 + i // 12}{i % 12 + 1:02d}.11111" for i in range(30)]
    (fake_repo / "research" / "CITES_ONE.md").write_text("# Cites One\n\nSee arXiv:2605.11111 for the bound.\n", encoding="utf-8")
    corpus = Corpus(fake_repo)
    corpus.refresh()
    state = {"papers": {arxiv_id: {"arxiv_id": arxiv_id, "label": "possible-kill"} for arxiv_id in ids}}
    start = time.perf_counter()
    assert recheck_cited(state, corpus, "2026-10-26") == 1
    assert time.perf_counter() - start < 1.0
    assert state["papers"]["2605.11111"]["label"] == "already-cited"


def test_verdict_flag_records_and_rerenders_without_fetching(fake_repo: Path, monkeypatch, capsys) -> None:
    from tools.arxiv_watch import watch

    corpus = Corpus(fake_repo)
    corpus.refresh()
    kill = _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout.")
    run(fake_repo, FakeClient([kill]), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")

    def refuse(*args, **kwargs):
        raise AssertionError("--verdict must not fetch or build the corpus")

    monkeypatch.setattr(watch, "Client", refuse)
    monkeypatch.setattr(watch, "Corpus", refuse)
    argv = ["--root", str(fake_repo), "--verdict", "2610.11111", "false-alarm", "--reason", "cue spurious", "--action", "none"]
    assert watch.main(argv) == 0
    entry = load_verdicts(fake_repo)["verdicts"]["2610.11111"]
    assert (entry["verdict"], entry["reason"], entry["action"], entry["by"]) == ("false-alarm", "cue spurious", "none", "human")
    digest = (fake_repo / "research" / "audits" / "ARXIV_WATCH.md").read_text()
    assert "| 2610.11111 |" in _section(digest, "Reviewed") and "2610.11111" not in _section(digest, "Possible kills")
    assert _state(fake_repo)["papers"]["2610.11111"]["verdict"]["verdict"] == "false-alarm"

    assert watch.main(["--root", str(fake_repo), "--verdict", "2610.11111", "maybe"]) == 2
    assert "unknown verdict" in capsys.readouterr().err
    assert load_verdicts(fake_repo)["verdicts"]["2610.11111"]["verdict"] == "false-alarm"


def test_verdict_flag_keeps_an_earlier_action_and_action_done_marks_it(fake_repo: Path, capsys) -> None:
    from tools.arxiv_watch import watch

    corpus = Corpus(fake_repo)
    corpus.refresh()
    kill = _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout.")
    run(fake_repo, FakeClient([kill]), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    digest = fake_repo / "research" / "audits" / "ARXIV_WATCH.md"

    def verdict(*argv: str) -> dict:
        assert watch.main(["--root", str(fake_repo), "--verdict", "2610.11111", *argv]) == 0, argv
        return load_verdicts(fake_repo)["verdicts"]["2610.11111"]

    entry = verdict("should-cite", "--reason", "r", "--action", "Cite it in X.")
    assert entry["action"] == "Cite it in X." and "action_done" not in entry
    capsys.readouterr()
    assert watch.main(["--root", str(fake_repo), "--action-done", "arXiv:2610.11111v1"]) == 0
    assert capsys.readouterr().out == "2610.11111: action marked done; digest re-rendered\n"
    assert load_verdicts(fake_repo)["verdicts"]["2610.11111"]["action_done"] is True
    assert "Cite it in X. (done) |" in _section(digest.read_text(), "Reviewed")

    # Re-recording without --action keeps the action and whether it was done, and says so.
    entry = verdict("kill", "--reason", "read the full text")
    assert (entry["verdict"], entry["action"], entry["action_done"]) == ("kill", "Cite it in X.", True)
    assert "kept the earlier action" in capsys.readouterr().out
    entry = verdict("kill", "--reason", "again", "--action", "Cite it in X.")
    assert entry["action_done"] is True
    entry = verdict("kill", "--reason", "again", "--action", "Cite it in Y.")  # a new action is not done yet
    assert entry["action"] == "Cite it in Y." and "action_done" not in entry
    entry = verdict("kill", "--reason", "again", "--action", "")  # an empty --action clears it
    assert entry["action"] is None and "action_done" not in entry

    capsys.readouterr()
    for ident, why in (("2610.11111", "no action"), ("2610.22222", "no verdict"), ("2610.0675", "not an arXiv id")):
        assert watch.main(["--root", str(fake_repo), "--action-done", ident]) == 2, ident
        assert why in capsys.readouterr().err, ident


def test_verdict_flag_stores_the_bare_id(fake_repo: Path, capsys) -> None:
    from tools.arxiv_watch import watch

    corpus = Corpus(fake_repo)
    corpus.refresh()
    kill = _paper("2610.11111", "Dequantizing Helstrom readout of dihedral coset packets", "A classical algorithm for quantum product readout.")
    run(fake_repo, FakeClient([kill]), corpus, tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    for ident in ("2610.11111v2", "arXiv:2610.11111", "https://arxiv.org/abs/2610.11111v1"):
        assert watch.main(["--root", str(fake_repo), "--verdict", ident, "false-alarm", "--reason", "x"]) == 0
        assert capsys.readouterr().out == "2610.11111: false-alarm; digest re-rendered\n", ident
        assert set(load_verdicts(fake_repo)["verdicts"]) == {"2610.11111"}
        assert _state(fake_repo)["papers"]["2610.11111"]["verdict"]["verdict"] == "false-alarm"
    assert "2610.11111" not in _section((fake_repo / "research" / "audits" / "ARXIV_WATCH.md").read_text(), "Possible kills")

    assert watch.main(["--root", str(fake_repo), "--verdict", "quant-ph/0501044v2", "related-only"]) == 0
    assert capsys.readouterr().out == "quant-ph/0501044: related-only (not in the collisions file yet); digest re-rendered\n"
    for bad in ("2610.111", "see 2610.11111", "", "2610.0675"):
        assert watch.main(["--root", str(fake_repo), "--verdict", bad, "kill"]) == 2
        assert "not an arXiv id" in capsys.readouterr().err
    assert set(load_verdicts(fake_repo)["verdicts"]) == {"2610.11111", "quant-ph/0501044"}


def test_a_root_that_is_not_a_checkout_is_refused_before_anything_is_written(tmp_path: Path, monkeypatch, capsys) -> None:
    from tools.arxiv_watch import judge, watch

    def refuse(*args, **kwargs):
        raise AssertionError("a wrong --root must be refused before fetching")

    monkeypatch.setattr(watch, "Client", refuse)
    monkeypatch.setattr(watch, "Corpus", refuse)
    a_file = tmp_path / "a_file"
    a_file.write_text("", encoding="utf-8")
    for root in (tmp_path / "nope" / "typo", a_file, tmp_path):
        for argv in (["--verdict", "2610.06753", "should-cite", "--reason", "x"], [], ["--relabel"]):
            assert watch.main(["--root", str(root), *argv]) == 2, (root, argv)
            assert "is not a Q-Search checkout" in capsys.readouterr().err
        assert judge.main(["--root", str(root), "--export", str(tmp_path / "judge")]) == 2
        assert "is not a Q-Search checkout" in capsys.readouterr().err
    assert sorted(path.name for path in tmp_path.iterdir()) == ["a_file"]


def test_verdict_flag_writes_nothing_when_the_collisions_file_is_unreadable(fake_repo: Path, capsys) -> None:
    from tools.arxiv_watch import watch

    corpus = Corpus(fake_repo)
    corpus.refresh()
    run(fake_repo, FakeClient([_paper("2610.11111", "Dihedral coset note", "Coset states.")]), corpus,
        tracks={"dcp": TRACKS["dcp"]}, today="2026-10-19")
    collisions = fake_repo / "research" / "audits" / "arxiv_collisions.json"
    text = collisions.read_text(encoding="utf-8")
    for broken in (text[: len(text) // 2], "[]", "directory"):
        if broken == "directory":
            collisions.unlink()
            collisions.mkdir()
        else:
            collisions.write_text(broken, encoding="utf-8")
        assert watch.main(["--root", str(fake_repo), "--verdict", "2610.11111", "false-alarm", "--reason", "x"]) == 2, broken
        assert capsys.readouterr().err.startswith("error: "), broken
        assert not (fake_repo / VERDICTS_FILE).exists(), broken


REPO = Path(__file__).resolve().parents[2]
REVIEW =REPO / "research" / "audits" / "ARXIV_TRIAGE_REVIEWED.md"


def _review_verdicts(text: str) -> dict[str, str]:
    """arXiv id -> verdict from the review's table rows and its "### id, ..." sections."""
    found = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and re.fullmatch(r"\d{4}\.\d{5}", cells[0]):
            found[cells[0]] = cells[3].replace(" ", "-")
    for arxiv_id, verdict in re.findall(r"^### (\d{4}\.\d{5}),[^\n]*\n\nFlagged \w+\. Verdict: \*\*([a-z ]+)\*\*", text, re.M):
        found[arxiv_id] = verdict.replace(" ", "-")
    return found


SEED_DAY = "2026-10-21"


def _review_sources(text: str) -> dict[str, tuple[str, bool]]:
    """arXiv id -> (the review's "Reason and action" cell, True) or (its "### id, ..." section, False)."""
    found = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and re.fullmatch(r"\d{4}\.\d{5}", cells[0]):
            found[cells[0]] = (cells[4], True)
    for match in re.finditer(r"^### (\d{4}\.\d{5}),", text, re.M):
        end = re.compile(r"^##", re.M).search(text, match.end())
        found[match.group(1)] = (text[match.start() : end.start() if end else len(text)], False)
    return found


def _flat(text: str) -> str:
    return " ".join(text.split())


def _words(text: str) -> set[str]:
    """Words of three letters or more; a file path may gain its research/ prefix."""
    return {word for word in re.findall(r"[^\W_]+", text.lower()) if len(word) > 2} - {"research"}


def _assert_seed_text_follows_review(entry: dict, source: str, cell: bool) -> None:
    """A table row's reason is a phrase of its cell, and its action uses only the cell's words (the
    action may name the note's path where the cell says "that note"). A section entry's reason and
    action are the section's own sentences and clauses."""
    reason, action = entry["reason"], entry.get("action") or ""
    if cell:
        assert _flat(reason) in _flat(source), reason
        assert _words(action) <= _words(source), action
        return
    for piece in re.split(r"(?<=[.;:])\s+", f"{reason} {action}".strip()):
        assert piece in _flat(source), piece


def _assert_seed_matches_review(verdicts: dict, text: str) -> None:
    """The 22 seeded entries still say what the review says.

    Only the seed is checked: later verdicts for other papers, an action marked done since, or a
    seeded paper re-recorded on a later day (its entry is no longer the review's) all pass.
    """
    reviewed = set(re.findall(r"\b\d{4}\.\d{5}\b", text))
    expected = _review_verdicts(text)
    assert len(reviewed) == 22 and set(expected) == reviewed and reviewed <= set(verdicts)
    counts: dict[str, int] = {}
    for verdict in expected.values():
        counts[verdict] = counts.get(verdict, 0) + 1
    assert counts == {"should-cite": 9, "related-only": 8, "false-alarm": 5}
    seed = {arxiv_id: verdicts[arxiv_id] for arxiv_id in reviewed if verdicts[arxiv_id].get("reviewed_on") == SEED_DAY}
    assert {arxiv_id: entry["verdict"] for arxiv_id, entry in seed.items()} == {arxiv_id: expected[arxiv_id] for arxiv_id in seed}
    assert all(entry["by"] == "human" and entry["reason"] for entry in seed.values())
    assert {"2610.06753", "2610.03566"} & set(seed) <= {arxiv_id for arxiv_id, entry in seed.items() if entry.get("action_done")}
    sources = _review_sources(text)
    for arxiv_id, entry in seed.items():
        _assert_seed_text_follows_review(entry, *sources[arxiv_id])


@pytest.mark.skipif(not REVIEW.exists(), reason="the reviewed triage is not in this checkout")
def test_seeded_verdicts_match_the_reviewed_triage() -> None:
    _assert_seed_matches_review(load_verdicts(REPO)["verdicts"], REVIEW.read_text(encoding="utf-8"))


@pytest.mark.skipif(not REVIEW.exists(), reason="the reviewed triage is not in this checkout")
def test_seed_check_allows_later_verdicts_but_not_a_drifted_seed() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    seeded = load_verdicts(REPO)["verdicts"]
    later = {
        "2609.23818": {"verdict": "related-only", "reason": "read it", "action": None, "by": "human", "reviewed_on": "2026-10-27"},
        "2610.99999": {"verdict": "kill", "reason": "r", "action": "a", "by": "judge:x", "reviewed_on": "2026-10-27",
                       "quote": "q", "quote_from": "abstract", "confidence": 0.5},
        "2610.00502": {**seeded["2610.00502"], "action_done": True},  # an agent carried out a seeded action
        "2610.01141": {**seeded["2610.01141"], "verdict": "kill", "reviewed_on": "2026-11-02"},  # re-recorded since
    }
    _assert_seed_matches_review({**seeded, **later}, text)
    for drift in ({"verdict": "kill"}, {"by": "judge:x"}, {"action_done": False}):
        changed = {**seeded, "2610.06753": {**seeded["2610.06753"], **drift}}
        with pytest.raises(AssertionError):
            _assert_seed_matches_review(changed, text)
    with pytest.raises(AssertionError):
        _assert_seed_matches_review({k: v for k, v in seeded.items() if k != "2610.01902"}, text)


@pytest.mark.skipif(not REVIEW.exists(), reason="the reviewed triage is not in this checkout")
def test_seed_check_catches_a_reworded_reason_or_action() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    seeded = load_verdicts(REPO)["verdicts"]
    for arxiv_id, field, value in (
        ("2610.00502", "reason", "WRONG " + seeded["2610.00502"]["reason"]),
        ("2610.00502", "action", "Do nothing."),
        ("2609.40036", "reason", seeded["2610.06812"]["reason"]),  # another row's reason
        ("2610.03566", "reason", "Its rejection sampler is per-symbol USD plus Prange, so the negative result stands."),
        ("2610.06753", "action", "Preprint: cite the cap and reword question 2."),
    ):
        changed = {**seeded, arxiv_id: {**seeded[arxiv_id], field: value}}
        with pytest.raises(AssertionError):
            _assert_seed_matches_review(changed, text)

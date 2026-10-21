from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.arxiv_watch.judge import export_batches, pending
from tools.arxiv_watch.tracks import TRACKS
from tools.arxiv_watch.verdicts import VERDICTS, set_verdict
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

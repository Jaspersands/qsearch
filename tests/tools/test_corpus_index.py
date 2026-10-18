from __future__ import annotations

import os
import time
from pathlib import Path

import numpy as np
import pytest

from tools.corpus.api import Corpus
from tools.corpus.ranking import rrf, snippet


@pytest.fixture
def corpus(fake_repo: Path) -> Corpus:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    return corpus


def _bump(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    later = time.time() + 5
    os.utime(path, (later, later))


def test_first_build_indexes_every_file_and_ignores_itself_in_git(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo)
    stats = corpus.refresh()
    assert stats.files_changed == stats.files_scanned > 5
    assert stats.docs_total == len(corpus.doc_ids())
    assert (fake_repo / "research" / "corpus_index" / ".gitignore").read_text().strip() == "*"


def test_second_refresh_without_changes_touches_nothing(corpus: Corpus) -> None:
    stats = corpus.refresh()
    assert stats.files_changed == 0
    assert stats.docs_added == stats.docs_removed == 0


def test_edited_note_replaces_its_chunks_only(fake_repo: Path, corpus: Corpus) -> None:
    before = set(corpus.doc_ids())
    note = fake_repo / "research" / "OLD_HIERARCHY.md"
    _bump(note, "# Old Hierarchy Claim\n\nSUPERSEDED.\n\n## Replacement\n\nZebrafish permutation sieve idea.\n")
    stats = corpus.refresh()
    assert stats.files_changed == 1
    after = set(corpus.doc_ids())
    assert "note:OLD_HIERARCHY#claim" in before - after
    assert "note:OLD_HIERARCHY#replacement" in after - before
    assert corpus.search("zebrafish sieve")[0].doc_id == "note:OLD_HIERARCHY#replacement"


def test_touched_but_identical_file_is_not_reparsed(fake_repo: Path, corpus: Corpus) -> None:
    note = fake_repo / "research" / "OLD_HIERARCHY.md"
    _bump(note, note.read_text())
    assert corpus.refresh().files_changed == 0


def test_deleted_file_removes_its_docs(fake_repo: Path, corpus: Corpus) -> None:
    (fake_repo / "research" / "OLD_HIERARCHY.md").unlink()
    stats = corpus.refresh()
    assert stats.docs_removed >= 1
    assert not any(doc_id.startswith("note:OLD_HIERARCHY") for doc_id in corpus.doc_ids())


def test_search_ranks_the_matching_negative_first_with_location(corpus: Corpus) -> None:
    hits = corpus.search("does a local Helstrom measurement beat product X basis readout?")
    top = hits[0]
    assert top.doc_id == "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"
    assert top.kind == "negative"
    assert top.path == "research/registry/negative_results.json"
    assert top.line > 0
    assert "Helstrom" in top.snippet


def test_search_stems_word_variants(corpus: Corpus) -> None:
    hits = corpus.search("decoders for the dual code", kinds=("literature",))
    assert hits[0].doc_id == "literature:jordan-dqi-2024"


def test_kind_filter_only_returns_that_kind(corpus: Corpus) -> None:
    hits = corpus.search("exterior characters cycle indicator", kinds=("note",))
    assert hits and {hit.kind for hit in hits} == {"note"}


def test_tag_filter(corpus: Corpus) -> None:
    hits = corpus.search("classical solver", tags=("OPI",))
    assert [hit.doc_id for hit in hits] == ["negative:NEG-OPI-MIXED-COSET-HARDNESS"]


def test_new_docs_are_searchable_after_incremental_refresh(fake_repo: Path, corpus: Corpus) -> None:
    theorem = fake_repo / "theorems" / "quokka_walk.py"
    _bump(theorem, '"""Quokka continuous-time quantum walk on glued trees."""\n')
    corpus.refresh()
    assert corpus.search("quokka glued trees walk")[0].doc_id == "theorem:quokka_walk"


def test_similar_excludes_the_doc_itself(corpus: Corpus) -> None:
    hits = corpus.similar("negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY")
    assert hits
    assert "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY" not in [hit.doc_id for hit in hits]


def test_get_returns_full_doc(corpus: Corpus) -> None:
    doc = corpus.get("dequant:DEQ-POLAR-GIBBS-SOURCE")
    assert doc.meta["severity"] == "high"
    assert "Gibbs" in doc.text


def test_matrix_gives_cosine_similarities_for_one_kind(corpus: Corpus) -> None:
    ids, sims = corpus.matrix("negative")
    assert set(ids) == {
        "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY",
        "negative:NEG-OPI-MIXED-COSET-HARDNESS",
        "quarantined:NEG-ANNEALING-GAP-BARRIER",
    }
    dense = sims.toarray()
    assert dense.shape == (3, 3)
    assert np.allclose(np.diag(dense), 1.0, atol=1e-5)


def test_been_tried_groups_hits(corpus: Corpus) -> None:
    groups = corpus.been_tried("Use a quadratic extension norm to solve mixed coset OPI classically", k=3)
    assert list(groups) == [
        "Killed before",
        "Dequantization checks",
        "Notes and handoff",
        "Code and experiments",
        "Literature",
    ]
    assert all(hit.kind == "negative" for hit in groups["Killed before"])
    assert groups["Killed before"][0].doc_id == "negative:NEG-OPI-MIXED-COSET-HARDNESS"


def test_dense_ranker_uses_injected_embedder_and_caches_by_content(fake_repo: Path) -> None:
    calls: list[int] = []

    def embed(texts: list[str]) -> np.ndarray:
        calls.append(len(texts))
        vectors = np.array([[t.lower().count("gibbs"), t.lower().count("helstrom"), 1.0] for t in texts], dtype=np.float32)
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    corpus = Corpus(fake_repo, embedder=embed)
    corpus.refresh(dense=True)
    first = sum(calls)
    assert first == len(corpus.doc_ids())
    corpus.refresh(dense=True)
    assert sum(calls) == first  # nothing re-embedded
    hits = corpus.search("sampling a thermal state", dense=True)
    assert hits[0].doc_id in {"dequant:DEQ-POLAR-GIBBS-SOURCE", "hypothesis:bpqm_gibbs_frontier_contract"} or any(
        "Gibbs" in hit.title or "Gibbs" in hit.snippet for hit in hits[:3]
    )


def test_rrf_merges_rankings() -> None:
    fused = rrf([["a", "b", "c"], ["b", "a"], []])
    assert fused[0][0] in {"a", "b"}
    assert [key for key, _ in fused] [:2] == sorted(["a", "b"], key=lambda key: -dict(fused)[key])
    assert dict(fused)["c"] < dict(fused)["a"]


def test_snippet_picks_the_sentence_sharing_most_query_terms() -> None:
    text = "Intro sentence about nothing. The Helstrom readout loses to X basis. Closing remark."
    assert snippet(text, "Helstrom readout") == "The Helstrom readout loses to X basis."


def test_mentions_finds_documents_citing_an_arxiv_id(corpus: Corpus) -> None:
    assert corpus.mentions("2408.08292") == ["literature:jordan-dqi-2024"]
    assert corpus.mentions("quant-ph/0501044") == ["literature:dihedral_sources:ARXIV-quant-ph-0501044-v2"]
    assert corpus.mentions("9999.99999") == []


def test_index_version_change_forces_full_reparse(fake_repo: Path, corpus: Corpus, monkeypatch) -> None:
    import tools.corpus.api as api

    monkeypatch.setattr(api, "INDEX_VERSION", "test-bump")
    stats = Corpus(fake_repo).refresh()
    assert stats.files_changed == stats.files_scanned


def test_templated_records_rank_below_specific_ones(fake_repo: Path) -> None:
    import json

    path = fake_repo / "research" / "registry" / "dequantization_checks.json"
    template = "Experiment result supports the candidate without triggering kill criteria."
    records = [
        {
            "id": f"DEQ-T-{i}",
            "claim_under_test": template,
            "target_id": f"EXP-{i}",
            "required_action": "Resolve.",
            "evidence": "Platypus decoder falsifier triggered.",
            "severity": "medium",
        }
        for i in range(4)
    ]
    records.append(
        {
            "id": "DEQ-SPECIFIC",
            "claim_under_test": "Platypus decoder gives an advantage.",
            "target_id": "EXP-9",
            "required_action": "Charge the platypus decoder.",
            "evidence": "x",
            "severity": "high",
        }
    )
    path.write_text(json.dumps(records, indent=2))
    corpus = Corpus(fake_repo)
    corpus.refresh()
    hits = corpus.search("platypus decoder falsifier", kinds=("dequant",))
    assert hits[0].doc_id == "dequant:DEQ-SPECIFIC"

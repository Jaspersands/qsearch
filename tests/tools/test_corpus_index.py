from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path

import numpy as np
import pytest

from tests.tools.conftest import NEGATIVES, QUARANTINED
from tools.corpus.api import Corpus
from tools.corpus.ranking import rrf, snippet
from tools.corpus.store import Store


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
    assert np.allclose(dense, dense.T, atol=1e-6)
    assert len(ids) == sum(doc_id.startswith(("negative:", "quarantined:")) for doc_id in corpus.doc_ids())


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


def _gibbs_embedder(calls: list[int] | None = None):
    """A toy embedder that knows 'thermal' means 'Gibbs', which no lexical ranker can know."""

    def embed(texts: list[str]) -> np.ndarray:
        if calls is not None:
            calls.append(len(texts))
        rows = [[t.lower().count("gibbs") + t.lower().count("thermal"), t.lower().count("helstrom"), 0.05] for t in texts]
        vectors = np.array(rows, dtype=np.float32)
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    return embed


GIBBS_DOCS = {"dequant:DEQ-POLAR-GIBBS-SOURCE", "hypothesis:bpqm_gibbs_frontier_contract"}


def test_dense_ranker_uses_injected_embedder_and_caches_by_content(fake_repo: Path) -> None:
    calls: list[int] = []
    corpus = Corpus(fake_repo, embedder=_gibbs_embedder(calls))
    corpus.refresh(dense=True)
    first = sum(calls)
    assert first == len(corpus.doc_ids())
    corpus.refresh(dense=True)
    assert sum(calls) == first  # nothing re-embedded
    query = "thermal equilibrium"  # shares no word with any Gibbs document
    lexical = [hit.doc_id for hit in corpus.search(query, k=3)]
    dense = [hit.doc_id for hit in corpus.search(query, k=3, dense=True)]
    assert not GIBBS_DOCS & set(lexical)  # so only the dense ranker can surface them
    assert set(dense[:2]) == GIBBS_DOCS


def test_rrf_merges_rankings() -> None:
    fused = rrf([["a", "b", "c"], ["b", "c"], []])
    assert [key for key, _ in fused] == ["b", "c", "a"]
    scores = dict(fused)
    assert scores["b"] == pytest.approx(1 / 62 + 1 / 61)
    assert scores["c"] == pytest.approx(1 / 63 + 1 / 62)
    assert scores["a"] == pytest.approx(1 / 61)


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


# --- robustness: malformed input, interrupted refreshes, concurrent agents ----------------------


def _db(fake_repo: Path) -> Path:
    return fake_repo / "research" / "corpus_index" / "corpus.sqlite"


def _can_write(db: Path) -> bool:
    other = sqlite3.connect(db, timeout=0.2, isolation_level=None)
    try:
        other.execute("BEGIN IMMEDIATE")
        other.execute("INSERT OR REPLACE INTO info VALUES ('probe', 'x')")
        other.execute("ROLLBACK")
        return True
    except sqlite3.OperationalError:
        return False
    finally:
        other.close()


def test_malformed_registry_records_do_not_break_the_index(fake_repo: Path, corpus: Corpus) -> None:
    registry = fake_repo / "research" / "registry"
    kangaroo = {"id": "NEG-KANGAROO-SIEVE", "claim": "Kangaroo sieve for dihedral cosets.", "reason_invalid": "x",
                "lesson": "y", "applies_to": ["DCP"]}
    broken = {"id": "NEG-BROKEN-TAGS", "claim": "Broken tags.", "applies_to": 5}
    _bump(registry / "negative_results.json", json.dumps(NEGATIVES + [kangaroo, broken], indent=2))
    stringy = {"id": "NEG-Q2", "original_record": "see NEG-KANGAROO-SIEVE wombat", "status": "QUARANTINED"}
    _bump(registry / "quarantined_campaign_negatives.json", json.dumps(QUARANTINED + [stringy], indent=2))
    corpus.refresh()
    assert corpus.search("kangaroo sieve", kinds=("negative",))[0].doc_id == "negative:NEG-KANGAROO-SIEVE"
    assert corpus.get("quarantined:NEG-ANNEALING-GAP-BARRIER") is not None
    assert "wombat" in corpus.get("quarantined:NEG-Q2").text  # a string original_record is kept as text
    assert corpus.get("negative:NEG-BROKEN-TAGS") is None  # skipped, and counted:
    issues = corpus.issues()
    assert any(i["path"].endswith("negative_results.json") and "NEG-BROKEN-TAGS" in i["message"] for i in issues)


def test_any_exception_during_refresh_rolls_back_and_releases_the_write_lock(
    fake_repo: Path, corpus: Corpus, monkeypatch
) -> None:
    _bump(fake_repo / "research" / "OLD_HIERARCHY.md", "# Old\n\n## New\n\nPlatypus sieve on wreath products.\n")
    _bump(fake_repo / "theorems" / "quokka_walk.py", '"""Quokka walk."""\n')
    calls = []
    real = Store.set_file_state

    def flaky(self, *args):
        calls.append(args)
        if len(calls) == 2:
            raise RuntimeError("disk on fire")
        return real(self, *args)

    monkeypatch.setattr(Store, "set_file_state", flaky)
    with pytest.raises(RuntimeError):
        corpus.refresh()
    assert not corpus.store.conn.in_transaction
    assert _can_write(_db(fake_repo))  # another agent's refresh is not locked out
    monkeypatch.setattr(Store, "set_file_state", real)
    corpus.refresh()
    assert corpus.search("platypus sieve wreath")[0].doc_id == "note:OLD_HIERARCHY#new"


def test_noop_refresh_does_not_take_the_write_lock(fake_repo: Path, corpus: Corpus) -> None:
    holder = sqlite3.connect(_db(fake_repo), isolation_level=None)
    holder.execute("BEGIN IMMEDIATE")  # another agent is mid-build
    holder.execute("INSERT OR REPLACE INTO info VALUES ('holder', 'x')")
    try:
        corpus.store.conn.execute("PRAGMA busy_timeout = 200")
        stats = corpus.refresh()
        assert stats.files_changed == 0
        assert corpus.search("Helstrom")
    finally:
        holder.execute("ROLLBACK")
        holder.close()


def test_interrupted_refit_is_repaired_by_the_next_refresh(fake_repo: Path, corpus: Corpus, monkeypatch) -> None:
    from tools.corpus import ranking

    _bump(fake_repo / "theorems" / "quokka_walk.py", '"""Quokka continuous-time quantum walk on glued trees."""\n')
    (fake_repo / "research" / "OLD_HIERARCHY.md").unlink()

    def interrupted(cls, items):
        raise KeyboardInterrupt("Ctrl-C during the refit")

    monkeypatch.setattr(ranking.TfidfState, "fit", classmethod(interrupted))
    with pytest.raises(KeyboardInterrupt):
        corpus.refresh()
    monkeypatch.undo()

    fresh = Corpus(fake_repo)  # the next CLI call
    fresh.refresh()
    live = {rowid for rowid, _ in fresh.store.texts()}
    assert set(fresh._state().rowids.tolist()) == live
    assert fresh.search("quokka glued trees")[0].doc_id == "theorem:quokka_walk"

    # A query with --no-refresh repairs a pickle that does not match the database, too.
    fresh.store.set_info("epoch", "written-by-another-agent")
    fresh.store.commit()
    other = Corpus(fake_repo)
    assert other._state().epoch == "written-by-another-agent"
    assert set(other._state().rowids.tolist()) == live


def test_editing_one_record_keeps_the_other_docs_and_patches_tfidf(fake_repo: Path) -> None:
    path = fake_repo / "research" / "registry" / "negative_results.json"
    extra = [
        {"id": f"NEG-FILLER-{i}", "claim": f"Filler claim number {i} about sieve variant {i}.", "reason_invalid": "x",
         "lesson": "y", "applies_to": ["DCP"]}
        for i in range(80)
    ]
    path.write_text(json.dumps(NEGATIVES + extra, indent=2))
    corpus = Corpus(fake_repo)
    corpus.refresh()
    before = {doc_id: corpus.store.row_of(doc_id) for doc_id in corpus.doc_ids()}
    extra[40]["claim"] = "Echidna sieve replaces filler forty."
    extra.insert(0, {"id": "NEG-NEW-TOP", "claim": "Numbat readout.", "reason_invalid": "x", "lesson": "y"})
    _bump(path, json.dumps(NEGATIVES + extra, indent=2))
    stats = corpus.refresh()
    assert (stats.docs_added, stats.docs_removed) == (2, 1)
    assert stats.refit is False
    after = {doc_id: corpus.store.row_of(doc_id) for doc_id in corpus.doc_ids()}
    assert all(after[d] == before[d] for d in before if d != "negative:NEG-FILLER-40")
    moved = corpus.get("negative:NEG-FILLER-41")  # unchanged text, new line number
    assert '"id": "NEG-FILLER-41"' in path.read_text().splitlines()[moved.line - 1]
    assert corpus.search("echidna sieve")[0].doc_id == "negative:NEG-FILLER-40"
    assert corpus.search("numbat readout")[0].doc_id == "negative:NEG-NEW-TOP"


def test_fts_rows_stay_in_step_with_docs_when_heading_ids_collide(fake_repo: Path) -> None:
    long = " ".join(f"w{i}" for i in range(450))
    (fake_repo / "research" / "DUP.md").write_text(
        f"# Dup\n\n## Results\n\n{long}\n\n## Results\n\nsecond results section about echidna.\n\n"
        "## Results 2\n\nthird section about numbat.\n"
    )
    corpus = Corpus(fake_repo)
    corpus.refresh()
    dup = [doc_id for doc_id in corpus.doc_ids() if doc_id.startswith("note:DUP")]
    assert len(dup) == len(set(dup)) == 4
    db = sqlite3.connect(_db(fake_repo))
    assert db.execute("SELECT COUNT(*) FROM docs_fts").fetchone() == db.execute("SELECT COUNT(*) FROM docs").fetchone()
    assert "echidna" in corpus.get(corpus.search("echidna second results")[0].doc_id).text
    assert "numbat" in corpus.get(corpus.search("numbat third section")[0].doc_id).text


def test_mentions_matches_versioned_and_prefixed_arxiv_ids(fake_repo: Path) -> None:
    (fake_repo / "research" / "CITES.md").write_text(
        "# Cites\n\n## One\n\nWe follow 2609.35656v1 closely here.\n\n"
        "## Two\n\nSee arXiv:2609.40250v2 for the sampler details.\n\n"
        "## Three\n\nThe arXiv2609.31111v3 preprint has the bound.\n\n"
        "## Four\n\nUnrelated numbers 2609.356567 and 12609.40250 and 2609.31111x9.\n"
    )
    corpus = Corpus(fake_repo)
    corpus.refresh()
    assert corpus.mentions("2609.35656") == ["note:CITES#one"]
    assert corpus.mentions("2609.40250") == ["note:CITES#two"]
    assert corpus.mentions("2609.31111") == ["note:CITES#three"]
    assert corpus.mentions("2609.3565") == []


def test_partial_dense_vectors_are_not_auto_used_and_new_docs_score_neutrally(fake_repo: Path) -> None:
    corpus = Corpus(fake_repo, embedder=_gibbs_embedder())
    corpus.refresh(dense=True)
    assert corpus.has_dense()
    new = {"id": "NEG-KANGAROO-HELSTROM", "claim": "Kangaroo Helstrom readout of coset packets beats Helstrom product readout.",
           "reason_invalid": "Kangaroo readout is a Helstrom test in disguise.", "lesson": "Helstrom.", "applies_to": ["DCP"]}
    _bump(fake_repo / "research" / "registry" / "negative_results.json", json.dumps(NEGATIVES + [new], indent=2))
    corpus.refresh()  # what every query does: no embedding
    assert not corpus.has_dense()  # so dense=auto does not fuse a ranker that cannot see the new record
    hits = corpus.search("kangaroo helstrom readout", kinds=("negative",), dense=True)
    assert hits[0].doc_id == "negative:NEG-KANGAROO-HELSTROM"  # and an explicit --dense does not bury it

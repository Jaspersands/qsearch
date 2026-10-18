"""The Corpus API: incremental refresh plus fused lexical (and optional dense) search."""

from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from tools.corpus.docs import Doc
from tools.corpus.ranking import (
    Embedder,
    TfidfState,
    fts_match,
    rrf,
    sentence_transformer_embedder,
    snippet,
    top_rows,
)
from tools.corpus.sources import discover, parse_file
from tools.corpus.store import Store

REPO_ROOT = Path(__file__).resolve().parents[2]
# Bump when parsers change what they emit, so existing indexes re-parse every file.
INDEX_VERSION = "2"
REFIT_FRACTION = 0.05
POOL = 200

GROUPS: dict[str, tuple[str, ...]] = {
    "Killed before": ("negative",),
    "Dequantization checks": ("dequant",),
    "Notes and handoff": ("note", "handoff"),
    "Code and experiments": ("theorem", "hypothesis", "experiment", "result", "proof", "candidate"),
    "Literature": ("literature",),
}


def default_root() -> Path:
    return Path(os.environ.get("QSEARCH_ROOT", REPO_ROOT)).resolve()


@dataclass
class Hit:
    doc_id: str
    kind: str
    path: str
    line: int
    title: str
    score: float
    snippet: str
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def location(self) -> str:
        return f"{self.path}:{self.line}" if self.line else self.path


@dataclass
class BuildStats:
    files_scanned: int = 0
    files_changed: int = 0
    docs_added: int = 0
    docs_removed: int = 0
    docs_total: int = 0
    refit: bool = False
    vectors_added: int = 0
    seconds: float = 0.0


class Corpus:
    def __init__(self, root: Path | None = None, index_dir: Path | None = None, embedder: Embedder | None = None):
        self.root = Path(root).resolve() if root else default_root()
        self.index_dir = index_dir or self.root / "research" / "corpus_index"
        self.index_dir.mkdir(parents=True, exist_ok=True)
        ignore = self.index_dir / ".gitignore"
        if not ignore.exists():
            ignore.write_text("*\n", encoding="utf-8")
        self.store = Store(self.index_dir / "corpus.sqlite")
        self.tfidf_path = self.index_dir / "tfidf.pkl"
        self._tfidf: TfidfState | None = None
        self._kinds: np.ndarray | None = None
        self._embedder = embedder
        self._dense: tuple[np.ndarray, np.ndarray] | None = None

    # building -----------------------------------------------------------------
    def refresh(self, full: bool = False, dense: bool = False) -> BuildStats:
        start = time.time()
        stats = BuildStats()
        if self.store.info("version") != INDEX_VERSION:
            full = True
        states = self.store.file_states()
        files = discover(self.root)
        stats.files_scanned = len(files)
        added: list[int] = []
        removed: list[int] = []
        for rel in files:
            path = self.root / rel
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            known = states.get(rel)
            if known and known[0] == stat.st_mtime and known[1] == stat.st_size and not full:
                continue
            sha = hashlib.sha1(path.read_bytes()).hexdigest()
            if known and known[2] == sha and not full:
                self.store.set_file_state(rel, stat.st_mtime, stat.st_size, sha)
                continue
            new_ids, old_ids = self.store.replace_file(rel, parse_file(self.root, rel))
            self.store.set_file_state(rel, stat.st_mtime, stat.st_size, sha)
            added.extend(new_ids)
            removed.extend(old_ids)
            stats.files_changed += 1
        for rel in set(states) - set(files):
            removed.extend(self.store.remove_file(rel))
            stats.files_changed += 1
        self.store.set_info("version", INDEX_VERSION)
        self.store.commit()

        stats.docs_total = self.store.count()
        stats.docs_added, stats.docs_removed = len(added), len(removed)
        tfidf = None if full else TfidfState.load(self.tfidf_path)
        if tfidf is None or tfidf.changed_since_fit + len(added) + len(removed) > REFIT_FRACTION * max(stats.docs_total, 1):
            tfidf = TfidfState.fit(self.store.texts())
            stats.refit = True
            tfidf.save(self.tfidf_path)
        elif added or removed:
            tfidf.patch(set(removed), self.store.texts(added))
            tfidf.save(self.tfidf_path)
        self._tfidf, self._kinds, self._dense = tfidf, None, None

        if dense:
            stats.vectors_added = self._embed_missing()
        stats.seconds = round(time.time() - start, 3)
        return stats

    def _embedder_or_default(self) -> Embedder:
        if self._embedder is None:
            self._embedder = sentence_transformer_embedder()
        return self._embedder

    def _embed_missing(self, batch: int = 512) -> int:
        missing = self.store.missing_vector_rows()
        embed = self._embedder_or_default()
        for start in range(0, len(missing), batch):
            chunk = missing[start : start + batch]
            vectors = embed([text for _, text in chunk]).astype(np.float32)
            self.store.put_vectors((sha, vector.tobytes()) for (sha, _), vector in zip(chunk, vectors))
            self.store.commit()
        return len(missing)

    def has_dense(self) -> bool:
        return self.store.has_vectors()

    # lookup ---------------------------------------------------------------------
    def doc_ids(self) -> list[str]:
        return self.store.doc_ids()

    def get(self, doc_id: str) -> Doc | None:
        return self.store.get(doc_id)

    def _state(self) -> TfidfState:
        if self._tfidf is None:
            self._tfidf = TfidfState.load(self.tfidf_path)
            if self._tfidf is None:
                self.refresh()
        assert self._tfidf is not None
        return self._tfidf

    def _row_kinds(self) -> np.ndarray:
        if self._kinds is None:
            kinds = self.store.kinds_by_row()
            self._kinds = np.array([kinds.get(int(r), "") for r in self._state().rowids], dtype=object)
        return self._kinds

    def _dense_matrix(self) -> tuple[np.ndarray, np.ndarray]:
        if self._dense is None:
            rows = list(self.store.vector_rows())
            ids = np.array([rowid for rowid, _ in rows], dtype=np.int64)
            matrix = np.vstack([np.frombuffer(blob, dtype=np.float32) for _, blob in rows]) if rows else np.zeros((0, 1))
            self._dense = (ids, matrix)
        return self._dense

    # search -----------------------------------------------------------------------
    def search(
        self,
        query: str,
        *,
        kinds: tuple[str, ...] = (),
        tags: tuple[str, ...] = (),
        k: int = 10,
        dense: bool = False,
        exclude: tuple[str, ...] = (),
    ) -> list[Hit]:
        state = self._state()
        pool = POOL * (5 if tags else 1)
        rankings: list[list[int]] = [self.store.fts(fts_match(query), tuple(kinds), pool)]
        allowed = np.isin(self._row_kinds(), list(kinds)) if kinds else None
        rankings.append(top_rows(state.scores(query), state.rowids, allowed, pool))
        if dense and self.has_dense():
            ids, matrix = self._dense_matrix()
            qvec = self._embedder_or_default()([query])[0]
            kinds_by_row = self.store.kinds_by_row() if kinds else {}
            dense_allowed = np.array([kinds_by_row.get(int(i)) in kinds for i in ids]) if kinds else None
            rankings.append(top_rows(matrix @ qvec, ids, dense_allowed, pool))

        fused = rrf(rankings)
        rows = self.store.rows([rowid for rowid, _ in fused[: pool * 2]])
        wanted_tags = {tag.lower() for tag in tags}
        hits: list[Hit] = []
        for rowid, score in fused:
            doc = rows.get(rowid)
            if doc is None or doc.doc_id in exclude:
                continue
            if wanted_tags and not wanted_tags & {str(t).lower() for t in doc.meta.get("tags", [])}:
                continue
            hits.append(Hit(doc.doc_id, doc.kind, doc.path, doc.line, doc.title, round(score, 6), snippet(doc.text, query), doc.meta))
            if len(hits) >= k:
                break
        return hits

    def similar(self, doc_id: str, k: int = 10, dense: bool = False) -> list[Hit]:
        doc = self.get(doc_id)
        if doc is None:
            raise KeyError(doc_id)
        return self.search(f"{doc.title} {doc.text[:3000]}", k=k, dense=dense, exclude=(doc.doc_id,))

    def been_tried(self, idea: str, k: int = 5, dense: bool = False) -> dict[str, list[Hit]]:
        return {name: self.search(idea, kinds=kinds, k=k, dense=dense) for name, kinds in GROUPS.items()}

    def matrix(self, kind: str = "negative") -> tuple[list[str], Any]:
        """Doc ids of one kind and their pairwise TF-IDF cosine similarities (sparse)."""
        state = self._state()
        mask = self._row_kinds() == kind
        rows = self.store.rows(int(r) for r in state.rowids[mask])
        ids = [rows[int(r)].doc_id for r in state.rowids[mask]]
        sub = state.matrix[np.flatnonzero(mask)]
        return ids, (sub @ sub.T).tocsr()

"""The Corpus API: incremental refresh plus fused lexical (and optional dense) search."""

from __future__ import annotations

import hashlib
import os
import re
import time
import uuid
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
from tools.corpus.sources import GLOBS, _parser_for, discover, parse_source
from tools.corpus.store import Store

REPO_ROOT = Path(__file__).resolve().parents[2]
# Bump when parsers change what they emit, so existing indexes re-parse every file.
INDEX_VERSION = "4"
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


class CorpusRootError(ValueError):
    """The root has nothing to index: it is missing, not a Q-Search checkout, or holds no documents."""


def checkout_root(root: Path | None = None) -> Path:
    """`root` (default: QSEARCH_ROOT or this repository), resolved, once it is known to be a checkout.

    Raises CorpusRootError before anything is written when the path is not a directory, has
    no research/ directory or holds no file the corpus indexes, so a mistyped --root never
    leaves an index tree behind and the MCP server does not start on it.
    """
    path = Path(root).resolve() if root else default_root()
    if not path.is_dir():
        raise CorpusRootError(f"{path} is not a directory")
    if not (path / "research").is_dir():
        raise CorpusRootError(f"{path} is not a Q-Search checkout: it has no research/ directory")
    if not _has_sources(path):
        raise CorpusRootError(f"nothing to index under {path}: no registry, note, code or literature file")
    return path


def _has_sources(root: Path) -> bool:
    """Whether `root` holds a file `discover` would return; stops at the first, so it costs far less."""
    for pattern in GLOBS:
        for path in root.glob(pattern):
            if path.is_file() and _parser_for(path.relative_to(root).as_posix()) is not None:
                return True
    return False


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
        """Re-parse changed files, then bring the TF-IDF pickle in step with the database.

        Files are stat'ed, hashed and parsed before any write, so an unchanged index is never
        locked: a no-op refresh only reads. Changes are applied in one write transaction that is
        rolled back on any exception. Each committed change stores a fresh `epoch` token in the
        database; the TF-IDF pickle records the epoch it reflects, and a pickle whose epoch does
        not match (a crash between commit and save, or another agent's write) is refit.
        """
        start = time.time()
        stats = BuildStats()
        version_ok = self.store.info("version") == INDEX_VERSION
        full = full or not version_ok
        states = self.store.file_states()
        files = discover(self.root)
        stats.files_scanned = len(files)
        touched: list[tuple[str, float, int, str]] = []
        parsed: list[tuple[str, float, int, str, list[Doc], list[str]]] = []
        for rel in files:
            path = self.root / rel
            try:
                stat = path.stat()
                known = states.get(rel)
                if known and known[0] == stat.st_mtime and known[1] == stat.st_size and not full:
                    continue
                sha = hashlib.sha1(path.read_bytes()).hexdigest()
            except FileNotFoundError:
                continue
            if known and known[2] == sha and not full:
                touched.append((rel, stat.st_mtime, stat.st_size, sha))
                continue
            docs, issues = parse_source(self.root, rel)
            parsed.append((rel, stat.st_mtime, stat.st_size, sha, docs, issues))
        gone = sorted(set(states) - set(files))

        added: list[int] = []
        removed: list[int] = []
        base_epoch = self.store.info("epoch") or ""
        new_epoch = base_epoch
        if touched or parsed or gone or not version_ok:
            with self.store.write():
                base_epoch = new_epoch = self.store.info("epoch") or ""
                for rel, mtime, size, sha in touched:
                    self.store.set_file_state(rel, mtime, size, sha)
                for rel, mtime, size, sha, docs, issues in parsed:
                    new_ids, old_ids = self.store.replace_file(rel, docs)
                    self.store.set_issues(rel, issues)
                    self.store.set_file_state(rel, mtime, size, sha)
                    added.extend(new_ids)
                    removed.extend(old_ids)
                for rel in gone:
                    removed.extend(self.store.remove_file(rel))
                if not version_ok:
                    self.store.drop_orphan_fts_rows()
                    self.store.set_info("version", INDEX_VERSION)
                if added or removed:
                    new_epoch = uuid.uuid4().hex
                    self.store.set_info("epoch", new_epoch)
        stats.files_changed = len(parsed) + len(gone)
        stats.docs_total = self.store.count()
        stats.docs_added, stats.docs_removed = len(added), len(removed)
        stats.refit = self._sync_tfidf(base_epoch, new_epoch, added, removed, force_refit=full)

        if dense:
            stats.vectors_added = self._embed_missing()
        stats.seconds = round(time.time() - start, 3)
        return stats

    def _sync_tfidf(self, base: str, ours: str, added: list[int], removed: list[int], force_refit: bool = False) -> bool:
        """Make the TF-IDF state match the database epoch; returns True when it was refit.

        A state is patched only when it reflects exactly the epoch our changes started from and
        nobody committed after us; anything else is refit from the stored texts. The epoch is
        read before the texts, so a saved state never claims to be newer than its content.
        """
        current = self.store.info("epoch") or ""
        tfidf = None
        if not force_refit:
            if self._tfidf is not None and self._tfidf.epoch in {base, current}:
                tfidf = self._tfidf
            else:
                tfidf = TfidfState.load(self.tfidf_path)
        if tfidf is not None and tfidf.epoch == current and not force_refit:
            if tfidf is not self._tfidf:  # another agent refreshed: drop caches built on the old rows
                self._tfidf, self._kinds, self._dense = tfidf, None, None
            return False
        patchable = (
            tfidf is not None
            and tfidf.epoch == base
            and current == ours
            and tfidf.changed_since_fit + len(added) + len(removed) <= REFIT_FRACTION * max(self.store.count(), 1)
        )
        if patchable:
            assert tfidf is not None
            tfidf.patch(set(removed), self.store.texts(added))
        else:
            if not self.store.count():
                raise CorpusRootError(f"nothing to index under {self.root}: no registry, note, code or literature file")
            tfidf = TfidfState.fit(self.store.texts())
        tfidf.epoch = current
        tfidf.save(self.tfidf_path)
        self._tfidf, self._kinds, self._dense = tfidf, None, None
        return not patchable

    def refit(self) -> None:
        """Refit TF-IDF from every stored text now, and save it.

        Between refits, changed documents are patched in with the vocabulary and IDF of the
        last fit, so cosines depend on that history (by up to a few hundredths). A refit
        makes them a function of the current documents alone.
        """
        self._state()
        self._sync_tfidf("", "", [], [], force_refit=True)

    def changed_since_fit(self) -> int:
        """Documents patched into the TF-IDF state since it was last fit (0 right after a refit)."""
        return self._state().changed_since_fit

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
        if missing:
            self._dense = None
        return len(missing)

    def has_dense(self) -> bool:
        """True when every document has a stored vector, so a dense ranking can see all of them."""
        return self.store.has_vectors() and self.store.docs_without_vectors() == 0

    def issues(self) -> list[dict[str, str]]:
        """Parse problems recorded for indexed files (skipped records, files indexed as raw text)."""
        return [{"path": path, "message": message} for path, message in self.store.issues()]

    def incomplete(self) -> bool:
        """True when a registry file or record could not be read, so negatives may be missing."""
        return any(path.startswith("research/registry/") for path, _ in self.store.issues())

    # lookup ---------------------------------------------------------------------
    def doc_ids(self) -> list[str]:
        return self.store.doc_ids()

    def get(self, doc_id: str) -> Doc | None:
        return self.store.get(doc_id)

    def _state(self) -> TfidfState:
        if self._tfidf is None:
            loaded = TfidfState.load(self.tfidf_path)
            if loaded is None and not self.store.count():
                self.refresh()  # first use: build the index
            elif loaded is None or loaded.epoch != (self.store.info("epoch") or ""):
                self._sync_tfidf("", "", [], [], force_refit=True)  # pickle missing or out of step
            else:
                self._tfidf = loaded
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
        covered: set[int] | None = None
        if dense and self.store.has_vectors():
            ids, matrix = self._dense_matrix()
            qvec = self._embedder_or_default()([query])[0]
            kinds_by_row = self.store.kinds_by_row() if kinds else {}
            dense_allowed = np.array([kinds_by_row.get(int(i)) in kinds for i in ids]) if kinds else None
            rankings.append(top_rows(matrix @ qvec, ids, dense_allowed, pool))
            if len(ids) < self.store.count():
                covered = set(ids.tolist())

        fused = rrf(rankings)
        if covered is not None:
            # Docs added since the last `build --dense` have no vector. Score them on the other
            # rankings alone, scaled up to the same number of rankers, so they are neither buried
            # nor favoured by a ranker that cannot see them.
            scale = len(rankings) / (len(rankings) - 1)
            fused = sorted(
                ((key, score if key in covered else score * scale) for key, score in fused), key=lambda item: -item[1]
            )
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

    def mentions(self, phrase: str, limit: int = 50) -> list[str]:
        """Doc ids whose text contains the phrase as consecutive tokens, e.g. an arXiv id.

        A version suffix or a glued prefix is allowed: "2609.35656" also matches "2609.35656v1",
        "arXiv:2609.35656v2" and "arXiv2609.35656". FTS5 keeps "35656v1" as one token, so the
        last token is searched as a prefix and every candidate is checked with a regex.
        """
        tokens = re.findall(r"[A-Za-z0-9]+", phrase)
        if not tokens:
            return []
        self._state()
        first = r"(?<![0-9])" if tokens[0][0].isdigit() else r"(?<![A-Za-z0-9])"
        pattern = re.compile(
            first + r"[^A-Za-z0-9]{1,2}".join(re.escape(t) for t in tokens) + r"(?:v[0-9]+)?(?![A-Za-z0-9])", re.I
        )
        candidates = self.store.fts(f'"{tokens[-1]}" *', (), max(limit * 20, 1000))
        found = self.store.rows(candidates)
        hits = [found[r].doc_id for r in candidates if r in found and pattern.search(f"{found[r].title}\n{found[r].text}")]
        return hits[:limit]

    def similar(self, doc_id: str, k: int = 10, dense: bool = False) -> list[Hit]:
        doc = self.get(doc_id)
        if doc is None:
            raise KeyError(doc_id)
        return self.search(f"{doc.title} {doc.text[:3000]}", k=k, dense=dense, exclude=(doc.doc_id,))

    def been_tried(self, idea: str, k: int = 5, dense: bool = False) -> dict[str, list[Hit]]:
        return {name: self.search(idea, kinds=kinds, k=k, dense=dense) for name, kinds in GROUPS.items()}

    def cosine(self, text: str, doc_ids: list[str]) -> dict[str, float]:
        """TF-IDF cosine between `text` and each listed document; ids not in the index are left out.

        Unlike `Hit.score` (a reciprocal-rank fusion score), this is a true cosine in [0, 1].
        """
        state = self._state()
        scores = state.scores(text)
        found: dict[str, float] = {}
        for doc_id in doc_ids:
            rowid = self.store.row_of(doc_id)
            position = np.flatnonzero(state.rowids == rowid) if rowid is not None else ()
            if len(position):
                found[doc_id] = float(scores[position[0]])
        return found

    def cosine_hits(
        self, text: str, kinds: tuple[str, ...], minimum: float, exclude: tuple[str, ...] = ()
    ) -> list[Hit]:
        """Every document of `kinds` whose TF-IDF cosine with `text` is at least `minimum`, highest first.

        Exhaustive: each document of those kinds is scored, unlike `search`, whose rank fusion
        can leave a close document out of its top k. A hit's `score` is the cosine rounded to
        four places, and that rounded score is what is compared with `minimum`, so a float32
        cosine of 0.9999997, shown as 1.0, matches a minimum of 1. Ties are ordered by doc id.
        Doc ids in `exclude` are left out.
        """
        state = self._state()
        scores = state.scores(text)
        near = np.flatnonzero(np.isin(self._row_kinds(), list(kinds)) & (scores >= minimum - 1e-4))
        rounded = {int(i): round(float(scores[i]), 4) for i in near}
        keep = [i for i, score in rounded.items() if score >= minimum]
        rows = self.store.rows(int(state.rowids[i]) for i in keep)
        hits: list[Hit] = []
        for i in keep:
            doc = rows.get(int(state.rowids[i]))
            if doc is None or doc.doc_id in exclude:
                continue
            score = rounded[i]
            hits.append(Hit(doc.doc_id, doc.kind, doc.path, doc.line, doc.title, score, snippet(doc.text, text), doc.meta))
        hits.sort(key=lambda hit: (-hit.score, hit.doc_id))
        return hits

    def kind_count(self, kinds: tuple[str, ...]) -> int:
        """How many indexed documents are of these kinds."""
        return int(np.isin(self._row_kinds(), list(kinds)).sum())

    def matrix(self, kind: str = "negative") -> tuple[list[str], Any]:
        """Doc ids of one kind and their pairwise TF-IDF cosine similarities (sparse)."""
        state = self._state()
        mask = self._row_kinds() == kind
        rows = self.store.rows(int(r) for r in state.rowids[mask])
        ids = [rows[int(r)].doc_id for r in state.rowids[mask]]
        sub = state.matrix[np.flatnonzero(mask)]
        return ids, (sub @ sub.T).tocsr()

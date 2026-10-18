"""Rankers (BM25 query building, TF-IDF cosine, optional dense) and reciprocal rank fusion."""

from __future__ import annotations

import os
import pickle
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np

STOP = None  # filled lazily from scikit-learn

Embedder = Callable[[list[str]], np.ndarray]


def _stopwords() -> frozenset[str]:
    global STOP
    if STOP is None:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

        STOP = frozenset(ENGLISH_STOP_WORDS)
    return STOP


def query_terms(text: str, cap: int = 64) -> list[str]:
    terms: list[str] = []
    seen = set()
    stop = _stopwords()
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if len(token) < 2 or token in stop or token in seen:
            continue
        seen.add(token)
        terms.append(token)
        if len(terms) >= cap:
            break
    return terms


def fts_match(text: str) -> str:
    """An FTS5 MATCH expression that ORs the query's content words."""
    return " OR ".join(f'"{term}"' for term in query_terms(text))


def preprocess(text: str) -> str:
    return re.sub(r"[-_/]+", " ", text.lower())


def rrf(rankings: Sequence[Sequence], k0: int = 60) -> list[tuple[object, float]]:
    """Reciprocal rank fusion: sum of 1/(k0 + rank) over the rankings that contain each key."""
    scores: dict[object, float] = {}
    for ranking in rankings:
        for rank, key in enumerate(ranking, start=1):
            scores[key] = scores.get(key, 0.0) + 1.0 / (k0 + rank)
    return sorted(scores.items(), key=lambda item: -item[1])


def snippet(text: str, query: str, width: int = 300) -> str:
    """The sentence of `text` sharing the most 5-letter word prefixes with the query."""
    wanted = {term[:5] for term in query_terms(query)}
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return ""

    def overlap(sentence: str) -> int:
        return len(wanted & {word[:5] for word in re.findall(r"[a-z0-9]+", sentence.lower())})

    best = max(sentences, key=overlap)
    return best if len(best) <= width else best[: width - 1].rstrip() + "…"


@dataclass
class TfidfState:
    vectorizer: object
    matrix: object  # scipy.sparse.csr_matrix, rows L2-normalized
    rowids: np.ndarray
    changed_since_fit: int = 0

    @classmethod
    def fit(cls, items: Iterable[tuple[int, str]]) -> "TfidfState":
        from sklearn.feature_extraction.text import TfidfVectorizer

        rowids, texts = [], []
        for rowid, text in items:
            rowids.append(rowid)
            texts.append(text)
        n = len(texts)
        vectorizer = TfidfVectorizer(
            preprocessor=preprocess,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2 if n >= 20 else 1,
            max_df=0.4 if n >= 50 else 1.0,
            sublinear_tf=True,
            max_features=300_000,
            dtype=np.float32,
        )
        matrix = vectorizer.fit_transform(texts).tocsr()
        vectorizer.stop_words_ = None  # pruned-term set is large and unused at query time
        return cls(vectorizer, matrix, np.asarray(rowids, dtype=np.int64))

    def patch(self, removed: set[int], added: Iterable[tuple[int, str]]) -> None:
        import scipy.sparse as sp

        keep = ~np.isin(self.rowids, np.fromiter(removed, dtype=np.int64, count=len(removed)))
        matrix, rowids = self.matrix[keep], self.rowids[keep]
        added = list(added)
        if added:
            extra = self.vectorizer.transform([text for _, text in added]).astype(np.float32)
            matrix = sp.vstack([matrix, extra]).tocsr()
            rowids = np.concatenate([rowids, np.asarray([rowid for rowid, _ in added], dtype=np.int64)])
        self.matrix, self.rowids = matrix, rowids
        self.changed_since_fit += len(removed) + len(added)

    def scores(self, text: str) -> np.ndarray:
        vector = self.vectorizer.transform([text])
        return np.asarray((self.matrix @ vector.T).todense()).ravel()

    def save(self, path: Path) -> None:
        tmp = path.with_suffix(".tmp")
        with tmp.open("wb") as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, path)

    @staticmethod
    def load(path: Path) -> "TfidfState | None":
        if not path.exists():
            return None
        with path.open("rb") as handle:
            return pickle.load(handle)


def top_rows(scores: np.ndarray, rowids: np.ndarray, allowed: np.ndarray | None, limit: int) -> list[int]:
    if allowed is not None:
        scores = np.where(allowed, scores, -np.inf)
    count = min(limit, int(np.isfinite(scores).sum()))
    if count <= 0:
        return []
    order = np.argpartition(-scores, count - 1)[:count]
    order = order[np.argsort(-scores[order], kind="stable")]
    return [int(rowids[i]) for i in order if scores[i] > 0]


def sentence_transformer_embedder(model: str = "sentence-transformers/all-MiniLM-L6-v2") -> Embedder:
    """A local sentence-transformers embedder; stays offline when the model is already cached."""
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    loaded: list[object] = []

    def embed(texts: list[str]) -> np.ndarray:
        if not loaded:
            from sentence_transformers import SentenceTransformer

            loaded.append(SentenceTransformer(model))
        encoder = loaded[0]
        return np.asarray(
            encoder.encode(texts, batch_size=64, normalize_embeddings=True, show_progress_bar=False), dtype=np.float32
        )

    return embed

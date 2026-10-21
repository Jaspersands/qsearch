"""Near-duplicate retained negatives, and a duplicate check for a draft claim, by TF-IDF cosine.

    from tools.corpus.duplicates import check_claim, near_duplicates
    pairs = near_duplicates(Corpus(), threshold=0.9, per_family=3)
    hits = check_claim(Corpus(), "Local Helstrom readout of each coset packet ...")

A score is the cosine of two documents' word unigram and bigram TF-IDF vectors (the
index's own vectorizer: sublinear tf, English stop words, rows L2-normalized), so 1.0 means
the same words in the same proportions. Many top pairs are parameter-sweep siblings whose
ids differ only in a trailing number (`...-N48-0-1` and `...-N48-0-2`); `per_family` caps
how many pairs of one such family are kept, so they do not crowd true restatements out.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

import scipy.sparse as sp

from tools.corpus.api import Corpus, Hit

_LAST_NUMBER = re.compile(r"-\d+$")


@dataclass(frozen=True)
class Pair:
    a: str
    b: str
    score: float
    title_a: str
    title_b: str


def _family(doc_id: str) -> str:
    """The id without its last `-<number>` segment; sweep siblings share it."""
    return _LAST_NUMBER.sub("", doc_id)


def near_duplicates(
    corpus: Corpus, kind: str = "negative", threshold: float = 0.8, limit: int = 200, per_family: int | None = None
) -> list[Pair]:
    """Pairs of documents of one kind whose cosine is at least `threshold`, highest first.

    Within a pair `a < b`. Ties are ordered by id, on scores rounded to four places, so a
    report is stable across runs. With `per_family`, at most that many pairs whose two ids
    share a family (the id before its last `-<number>`) are kept; other pairs are not capped.
    """
    ids, sims = corpus.matrix(kind)
    upper = sp.triu(sims, k=1).tocoo()
    keep = upper.data >= threshold
    found = sorted(
        (round(float(score), 4), *sorted((ids[i], ids[j])))
        for i, j, score in zip(upper.row[keep], upper.col[keep], upper.data[keep])
    )
    found.sort(key=lambda item: -item[0])  # stable: ids stay ascending within a score
    per: dict[str, int] = {}
    chosen: list[tuple[float, str, str]] = []
    for score, a, b in found:
        if len(chosen) >= limit:
            break
        if per_family is not None and _family(a) == _family(b):
            key = _family(a)
            if per.get(key, 0) >= per_family:
                continue
            per[key] = per.get(key, 0) + 1
        chosen.append((score, a, b))
    titles: dict[str, str] = {}
    for doc_id in {doc_id for _, a, b in chosen for doc_id in (a, b)}:
        doc = corpus.get(doc_id)
        titles[doc_id] = doc.title if doc is not None else ""
    return [Pair(a, b, score, titles[a], titles[b]) for score, a, b in chosen]


def check_claim(corpus: Corpus, text: str, threshold: float = 0.6, k: int = 5) -> list[Hit]:
    """Retained negatives whose TF-IDF cosine with a draft claim is at least `threshold`.

    The fused search finds candidates; each is re-scored with `Corpus.cosine`, so a hit's
    `score` here is a cosine in [0, 1], not the search's rank-fusion score.
    """
    hits = corpus.search(text, kinds=("negative",), k=max(2 * k, 10))
    cosines = corpus.cosine(text, [hit.doc_id for hit in hits])
    scored = [
        replace(hit, score=round(cosines[hit.doc_id], 4))
        for hit in hits
        if cosines.get(hit.doc_id, 0.0) >= threshold
    ]
    scored.sort(key=lambda hit: (-hit.score, hit.doc_id))
    return scored[:k]

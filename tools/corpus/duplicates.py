"""Near-duplicate retained negatives, and a duplicate check for a draft claim, by TF-IDF cosine.

    from tools.corpus.duplicates import check_claim, near_duplicates, pair_report
    pairs = near_duplicates(Corpus(), threshold=0.9, per_family=3)
    report = pair_report(Corpus(), threshold=0.8, limit=200)   # report.total: pairs before the limit
    hits = check_claim(Corpus(), "Local Helstrom readout of each coset packet ...")

A score is the cosine of two documents' word unigram and bigram TF-IDF vectors (the
index's own vectorizer: sublinear tf, English stop words, rows L2-normalized), so 1.0 means
the same words in the same proportions. Many top pairs are parameter-sweep siblings whose
ids differ only in a trailing number (`...-N48-0-1` and `...-N48-0-2`); `per_family` caps
how many pairs of one such family are kept, so they do not crowd true restatements out.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

import scipy.sparse as sp

from tools.corpus.api import Corpus, Hit

_LAST_NUMBER = re.compile(r"-\d+$")

# Default for the committed report (`cli.py near-duplicates`); calibrated in README.md, "Duplicates".
REPORT_THRESHOLD = 0.9


@dataclass(frozen=True)
class Pair:
    a: str
    b: str
    score: float
    title_a: str
    title_b: str


@dataclass(frozen=True)
class PairReport:
    pairs: list[Pair]  # the first `limit` pairs, highest first
    total: int  # pairs at or above the threshold after the per-family cap, before `limit`
    documents: int  # documents of the kind that were compared


def _family(doc_id: str) -> str:
    """The id without its last `-<number>` segment; sweep siblings share it."""
    return _LAST_NUMBER.sub("", doc_id)


def pair_report(
    corpus: Corpus, kind: str = "negative", threshold: float = 0.8, limit: int = 200, per_family: int | None = None
) -> PairReport:
    """Pairs of documents of one kind whose cosine is at least `threshold`, highest first.

    Within a pair `a < b`. Ties are ordered by id, on scores rounded to four places, so a
    report is stable across runs. With `per_family`, at most that many pairs whose two ids
    share a family (the id before its last `-<number>`) are kept; other pairs are not capped.
    `total` counts the pairs left after that cap, so a caller can say how many `limit` cut.
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
    capped: list[tuple[float, str, str]] = []
    for score, a, b in found:
        if per_family is not None and _family(a) == _family(b):
            key = _family(a)
            if per.get(key, 0) >= per_family:
                continue
            per[key] = per.get(key, 0) + 1
        capped.append((score, a, b))
    chosen = capped[: max(limit, 0)]
    titles: dict[str, str] = {}
    for doc_id in {doc_id for _, a, b in chosen for doc_id in (a, b)}:
        doc = corpus.get(doc_id)
        titles[doc_id] = doc.title if doc is not None else ""
    pairs = [Pair(a, b, score, titles[a], titles[b]) for score, a, b in chosen]
    return PairReport(pairs, len(capped), len(ids))


def near_duplicates(
    corpus: Corpus, kind: str = "negative", threshold: float = 0.8, limit: int = 200, per_family: int | None = None
) -> list[Pair]:
    """The pairs of `pair_report`, without the counts."""
    return pair_report(corpus, kind=kind, threshold=threshold, limit=limit, per_family=per_family).pairs


def draft_claim(raw: str) -> tuple[str, str | None]:
    """The text to check for a draft, and the draft's record id when it has one.

    A JSON object with a `claim` is a registry record: its claim and reason_invalid are
    checked, and its `id` is returned so the record is not matched with itself once filed.
    Anything else (plain text, other JSON) is checked as it is, with no id.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw, None
    if not (isinstance(data, dict) and data.get("claim")):
        return raw, None
    record_id = data.get("id")
    text = f"{data['claim']} {data.get('reason_invalid') or ''}".strip()
    return text, str(record_id) if record_id else None


def own_ids(record_id: str | None) -> tuple[str, ...]:
    """The doc ids a registry record with this id has in the index (retained or quarantined)."""
    return (f"negative:{record_id}", f"quarantined:{record_id}") if record_id else ()


@dataclass(frozen=True)
class ClaimReport:
    matches: list[Hit]  # the first `k` matches, highest first
    total: int  # every negative record at or above the threshold, before `k`
    quarantined: int  # how many of the `total` are quarantined records
    documents: int  # negative-kind documents compared


def claim_report(
    corpus: Corpus, text: str, threshold: float = 0.6, k: int = 5, exclude: tuple[str, ...] = ()
) -> ClaimReport:
    """Negative records (retained or quarantined) whose TF-IDF cosine with a draft claim is at least `threshold`.

    Every negative-kind document is scored (`Corpus.cosine_hits`), so no record at or above
    the threshold is missed and the closest comes first. A hit's `score` is a cosine in
    [0, 1], not the search's rank-fusion score. Doc ids in `exclude` (say the draft's own
    record, already filed) are never returned or counted.
    """
    found = corpus.cosine_hits(text, ("negative",), threshold, exclude=exclude)
    quarantined = sum(hit.doc_id.startswith("quarantined:") for hit in found)
    return ClaimReport(found[: max(k, 0)], len(found), quarantined, corpus.kind_count(("negative",)))


def check_claim(
    corpus: Corpus, text: str, threshold: float = 0.6, k: int = 5, exclude: tuple[str, ...] = ()
) -> list[Hit]:
    """The matches of `claim_report`, without the counts."""
    return claim_report(corpus, text, threshold=threshold, k=k, exclude=exclude).matches

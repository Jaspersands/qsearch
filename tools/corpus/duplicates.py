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
import math
import re
from dataclasses import dataclass

import scipy.sparse as sp

from tools.corpus.api import Corpus, Hit

_LAST_NUMBER = re.compile(r"-\d+$")

# Default for the committed report (`cli.py near-duplicates`); calibrated in README.md, "Duplicates".
REPORT_THRESHOLD = 0.9
# With no negative-kind document every claim would look new, so the gate refuses to answer.
NO_NEGATIVES = "the index has no negative records (retained or quarantined), so no claim can be checked"


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

    Within a pair `a < b`. Scores are rounded to four places, and a pair is kept when its
    rounded score is at least `threshold` (so a float32 cosine of 0.9999997, reported as 1.0,
    counts at a threshold of 1). Ties are ordered by id, so a report is stable across runs on
    one TF-IDF fit and the per-family cap keeps a family's lowest ids. Documents changed
    since the last fit are patched in with that fit's IDF, which can move a score by a few hundredths; call
    `corpus.refit()` first for a report that depends only on the current documents (the
    CLI does for `--out`). With `per_family`, at most that many pairs whose two ids
    share a family (the id before its last `-<number>`) are kept; other pairs are not capped.
    `total` counts the pairs left after that cap, so a caller can say how many `limit` cut.
    """
    ids, sims = corpus.matrix(kind)
    upper = sp.triu(sims, k=1).tocoo()
    near = upper.data >= threshold - 1e-4  # a loose cut; the threshold applies to the rounded score
    found: list[tuple[float, str, str]] = []
    for i, j, raw in zip(upper.row[near], upper.col[near], upper.data[near]):
        score = round(float(raw), 4)
        if score >= threshold:
            a, b = sorted((ids[i], ids[j]))
            found.append((score, a, b))
    found.sort(key=lambda item: (-item[0], item[1], item[2]))
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


class DraftError(ValueError):
    """A draft that looks like a JSON registry record (or a list of them) but is not one."""


# An object, or a list that is empty or starts with an object: text a user meant as records.
_RECORDS = re.compile(r"\s*(?:\{|\[\s*[{\]])")
_ID_PREFIXES = ("negative", "quarantined")


def _record_id(value: object) -> str | None:
    """A record id as filed: stripped, without a `negative:` or `quarantined:` doc-id prefix."""
    if value is None:
        return None
    text = str(value).strip()
    prefix, colon, rest = text.partition(":")
    if colon and prefix.strip() in _ID_PREFIXES:
        text = rest.strip()
    return text or None


def _record_draft(data: object, label: str) -> tuple[str, str | None]:
    if not isinstance(data, dict):
        raise DraftError(f"{label} is not a JSON object")
    body = data
    if "claim" not in data and isinstance(data.get("original_record"), dict):
        body = data["original_record"]  # a quarantined record keeps its claim here, its id on top
    claim, reason = body.get("claim"), body.get("reason_invalid")
    if not isinstance(claim, str) or not claim.strip():
        raise DraftError(f"{label} has no claim string")
    if reason is not None and not isinstance(reason, str):
        raise DraftError(f"{label} has a reason_invalid that is not a string")
    record_id = data.get("id") if data.get("id") is not None else body.get("id")
    return f"{claim} {reason or ''}".strip(), _record_id(record_id)


def draft_claims(raw: str) -> list[tuple[str, str | None]]:
    """The texts to check for a draft file, each with its record id when it has one.

    A JSON object is a registry record: its claim and reason_invalid are checked (a
    quarantined record's, under `original_record`, too) and its id is returned, stripped
    and without a `negative:` or `quarantined:` prefix, so the record is not matched with
    itself once filed. A JSON list of records gives one draft per record. A leading BOM is
    ignored. Text that starts like an object or a list of objects but is not one (bad
    JSON, a truncated file, no string claim) raises DraftError rather than being checked
    as raw text. Anything else is plain text, checked as it is, with no id.
    """
    raw = raw.lstrip("﻿")
    if not _RECORDS.match(raw):
        return [(raw, None)]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DraftError(f"looks like a JSON record but does not parse ({exc})") from None
    if isinstance(data, list):
        if not data:
            raise DraftError("the JSON list holds no record")
        return [_record_draft(item, f"record {index}") for index, item in enumerate(data, start=1)]
    return [_record_draft(data, "the record")]


def draft_claim(raw: str) -> tuple[str, str | None]:
    """The single draft of `draft_claims`; DraftError when the text holds several records."""
    drafts = draft_claims(raw)
    if len(drafts) != 1:
        raise DraftError(f"holds {len(drafts)} records; check them with draft_claims")
    return drafts[0]


def own_ids(record_id: str | None) -> tuple[str, ...]:
    """The doc ids a registry record with this id has in the index (retained or quarantined)."""
    return (f"negative:{record_id}", f"quarantined:{record_id}") if record_id else ()


def valid_threshold(value: float) -> float:
    """A cosine threshold as a float; ValueError unless it is a finite number in (0, 1].

    NaN, an infinity or a value above 1 would match nothing, and 0 or less would match every
    record, so a gate given one would always pass or always block.
    """
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = math.nan
    if not (math.isfinite(number) and 0 < number <= 1):
        raise ValueError(f"threshold must be a number in (0, 1], got {value}")
    return number


def allow_patterns(values: list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    """Record ids, or id prefixes ending in `*`, of records a draft is known to differ from.

    Each is stripped and loses a `negative:` or `quarantined:` prefix. ValueError for an empty
    pattern or a bare `*`, which would allow every record.
    """
    patterns: list[str] = []
    for value in values or ():
        pattern = _record_id(value) or ""
        if not pattern.rstrip("*"):
            raise ValueError(f"--allow needs a record id or an id prefix ending in *, got {value!r}")
        patterns.append(pattern)
    return tuple(patterns)


def _is_allowed(doc_id: str, patterns: tuple[str, ...]) -> bool:
    record = doc_id.partition(":")[2]
    return any(record.startswith(p[:-1]) if p.endswith("*") else record == p for p in patterns)


@dataclass(frozen=True)
class ClaimReport:
    matches: list[Hit]  # the first `k` matches, highest first
    total: int  # every negative record at or above the threshold, before `k`
    quarantined: int  # how many of the `total` are quarantined records
    documents: int  # negative-kind documents compared
    allowed: tuple[Hit, ...] = ()  # matches left out of `total` by `allow`, highest first


def claim_report(
    corpus: Corpus,
    text: str,
    threshold: float = 0.6,
    k: int = 5,
    exclude: tuple[str, ...] = (),
    allow: tuple[str, ...] = (),
) -> ClaimReport:
    """Negative records (retained or quarantined) whose TF-IDF cosine with a draft claim is at least `threshold`.

    Every negative-kind document is scored (`Corpus.cosine_hits`), so no record at or above
    the threshold is missed and the closest comes first. A hit's `score` is a cosine in
    [0, 1], not the search's rank-fusion score. Doc ids in `exclude` (say the draft's own
    record, already filed) are never returned or counted. A match whose record id is in
    `allow` (see `allow_patterns`; a sweep sibling the author has read) is reported under
    `allowed` instead of counting as a match. ValueError for a threshold outside (0, 1]
    (`valid_threshold`).
    """
    found = corpus.cosine_hits(text, ("negative",), valid_threshold(threshold), exclude=exclude)
    allowed = tuple(hit for hit in found if _is_allowed(hit.doc_id, allow))
    found = [hit for hit in found if not _is_allowed(hit.doc_id, allow)]
    quarantined = sum(hit.doc_id.startswith("quarantined:") for hit in found)
    return ClaimReport(found[: max(k, 0)], len(found), quarantined, corpus.kind_count(("negative",)), allowed)


def check_claim(
    corpus: Corpus, text: str, threshold: float = 0.6, k: int = 5, exclude: tuple[str, ...] = ()
) -> list[Hit]:
    """The matches of `claim_report`, without the counts."""
    return claim_report(corpus, text, threshold=threshold, k=k, exclude=exclude).matches


PARAPHRASE_LIMITATION = (
    "TF-IDF cosine is a near-copy check, not a novelty verdict: paraphrases can pass. "
    "Read the nearest negative records or run been-tried before filing."
)


def nearest_negatives(corpus: Corpus, text: str, exclude: tuple[str, ...] = (), k: int = 3) -> list[dict]:
    """Advisory fused-search leads, with independent cosines; these never set duplicate."""
    hits = corpus.search(text, kinds=("negative",), k=k, exclude=exclude)
    cosines = corpus.cosine(text, [hit.doc_id for hit in hits])
    return [
        {"doc_id": hit.doc_id, "title": hit.title, "location": hit.location,
         "search_rank": rank, "cosine": round(cosines[hit.doc_id], 4)}
        for rank, hit in enumerate(hits, start=1)
    ]

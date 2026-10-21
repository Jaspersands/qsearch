"""The classical baselines a quantum proposal should be compared against, and a recommender.

    from tools.corpus.baselines import recommend, validate_catalog, load_catalog
    recs = recommend(Corpus(), "sampling the Gibbs law of a signed parity-check code")
    problems = validate_catalog(load_catalog())

The catalog (`baselines.json`, next to this module) lists named classical algorithms: the
problem each solves, three to six lowercase mechanism keywords, references (arXiv ids and
research notes by stem) and, when the repository has one, a command that runs it.

A baseline's score is the fraction of its keywords found in the idea, plus a tenth for each
note or negative among the ten documents nearest the idea that names it (its name or an
alias, on word boundaries; a note counts once however many of its sections are near). The
score ranks leads to run; it is not a judgement that the baseline wins.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from tools.corpus.api import Corpus, Hit

NEARBY = 10  # note sections and negatives searched for citations; each citing note or negative adds 1 / NEARBY
CATALOG = Path(__file__).with_name("baselines.json")
FIELDS = ("id", "name", "aliases", "problem", "mechanisms", "summary", "references", "runnable")
_TEXT_FIELDS = ("id", "name", "problem", "summary")
_LIST_FIELDS = ("aliases", "mechanisms", "references")
_ARXIV = re.compile(r"\d{4}\.\d{4,5}")
_STEM = re.compile(r"[A-Z0-9_]+")


def load_catalog(path: Path = CATALOG) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["baselines"]


def _reference_ok(ref: object) -> bool:
    """{"arxiv": "2609.40036"} or {"note": "PRIME_CHARACTER_OPI"} (a research/<STEM>.md file)."""
    if not isinstance(ref, dict) or len(ref) != 1:
        return False
    (key, value), = ref.items()
    pattern = {"arxiv": _ARXIV, "note": _STEM}.get(key)
    return pattern is not None and isinstance(value, str) and pattern.fullmatch(value) is not None


def validate_catalog(entries: list[dict]) -> list[str]:
    """Problems with catalog entries, one line each; an empty list means the catalog is usable."""
    problems: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"entry {index + 1}: must be an object")
            continue
        label = str(entry.get("id") or f"entry {index + 1}")
        missing = [name for name in FIELDS if name not in entry]
        if missing:
            problems.append(f"{label}: missing field {', '.join(missing)}")
        for name in _TEXT_FIELDS:
            if name in entry and not (isinstance(entry[name], str) and entry[name].strip()):
                problems.append(f"{label}: {name} must be a non-empty string")
        for name in _LIST_FIELDS:
            if name in entry and not isinstance(entry[name], list):
                problems.append(f"{label}: {name} must be a list")
        if label in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(label)
        mechanisms = entry.get("mechanisms")
        if isinstance(mechanisms, list) and not (
            3 <= len(mechanisms) <= 6 and all(isinstance(m, str) and m.strip() for m in mechanisms)
        ):
            problems.append(f"{label}: mechanisms must be 3 to 6 keywords, found {len(mechanisms)}")
        if isinstance(entry.get("aliases"), list) and not all(isinstance(a, str) and a.strip() for a in entry["aliases"]):
            problems.append(f"{label}: aliases must be non-empty strings")
        for ref in entry.get("references") if isinstance(entry.get("references"), list) else ():
            if not _reference_ok(ref):
                problems.append(f"{label}: malformed reference {json.dumps(ref)}")
        runnable = entry.get("runnable")
        if runnable is not None and not (
            isinstance(runnable, dict)
            and isinstance(runnable.get("command"), str)
            and set(runnable) <= {"command", "entry"}
        ):
            problems.append(f"{label}: runnable must be null or {{command, entry?}}")
    return problems


@dataclass
class Recommendation:
    baseline: dict
    score: float
    matched: list[str]
    evidence: list[Hit]


def _singular(word: str) -> str:
    """'glasses' -> 'glass', 'codes' -> 'code', 'gibbs' -> 'gibb'; 'glass' and words of three letters stay."""
    if word.endswith("sses"):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


# German umlauts as their usual transcription, so "Gröbner" is "Groebner"; other accents are dropped.
_UMLAUTS = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
# One spelling per word on both sides of a match: British spellings, accent-free "Grobner",
# and the run-together "MaxCut".
_SPELLINGS = {
    "colouring": "coloring",
    "colour": "color",
    "coloured": "colored",
    "grobner": "groebner",
    "maxcut": "max cut",
}
# In a keyword, `k` stands for a number: "max k cut" matches "max-3-cut", "Max-q-Cut" and "max-k-cut".
PLACEHOLDER = "k"


def tokens(text: str) -> list[str]:
    """Lowercase alphanumeric words, singular: "sses" becomes "ss", and a final single "s" is
    dropped from words longer than three letters. Umlauts become ae/oe/ue and other accents
    are dropped ("Gröbner" is `groebner`), and a few spelling variants are folded into one
    (`_SPELLINGS`: "colouring" is `coloring`, "MaxCut" is `max cut`)."""
    folded = unicodedata.normalize("NFKD", text.lower().translate(_UMLAUTS))
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    words = [_singular(w) for w in re.findall(r"[a-z0-9]+", folded)]
    return [part for word in words for part in _SPELLINGS.get(word, word).split()]


def _number_like(word: str) -> bool:
    return word.isdigit() or word in {PLACEHOLDER, "q"}


def keyword_matches(keyword: list[str], idea: list[str]) -> bool:
    """Whether a keyword's tokens occur in an idea's tokens.

    In any order, unless the keyword has the `k` placeholder: then its tokens must occur in a
    row, with a number, k or q in the placeholder's place ("max k cut" matches "max-3-cut"
    but not "max cut at depth 3").
    """
    if PLACEHOLDER not in keyword:
        return set(keyword) <= set(idea)
    width = len(keyword)

    def fits(window: list[str]) -> bool:
        return all(word == token or (token == PLACEHOLDER and _number_like(word)) for token, word in zip(keyword, window))

    return any(fits(idea[i : i + width]) for i in range(len(idea) - width + 1))


def _name_pattern(baseline: dict) -> re.Pattern[str]:
    names = [baseline["name"], *baseline.get("aliases", [])]
    return re.compile(r"(?<!\w)(?:" + "|".join(re.escape(name) for name in names) + r")(?!\w)", re.I)


def _source(hit: Hit) -> str:
    """What a citation counts as: a note file once, however many of its sections are near; each registry record."""
    return hit.path if hit.kind == "note" else hit.doc_id


def _citing(hits: list[Hit], texts: dict[str, str], pattern: re.Pattern[str]) -> list[Hit]:
    """The nearest hit of each source that names the baseline."""
    seen: set[str] = set()
    found: list[Hit] = []
    for hit in hits:
        if _source(hit) not in seen and pattern.search(texts[hit.doc_id]):
            seen.add(_source(hit))
            found.append(hit)
    return found


def recommend(corpus: Corpus, idea: str, k: int = 5, catalog: list[dict] | None = None) -> list[Recommendation]:
    """Catalog baselines for an idea, best first: keyword overlap plus nearby notes that name them.

    A keyword matches when every one of its tokens occurs among the idea's tokens. The ten
    note sections and negatives the corpus ranks nearest the idea are read in full; each note
    or negative among them that names a baseline adds 0.1 to its score (a note once, however
    many of its sections are near) and its nearest hit is returned as evidence. Baselines
    scoring 0 are left out.
    """
    entries = load_catalog() if catalog is None else catalog
    words = tokens(idea)
    hits = corpus.search(idea, kinds=("note", "negative"), k=NEARBY)
    texts: dict[str, str] = {}
    for hit in hits:
        doc = corpus.get(hit.doc_id)
        texts[hit.doc_id] = f"{doc.title}\n{doc.text}" if doc is not None else f"{hit.title}\n{hit.snippet}"
    found: list[Recommendation] = []
    for baseline in entries:
        mechanisms = baseline["mechanisms"]
        matched = [m for m in mechanisms if keyword_matches(tokens(m), words)]
        citing = _citing(hits, texts, _name_pattern(baseline))
        score = round(len(matched) / len(mechanisms) + len(citing) / NEARBY, 4)
        if score > 0:
            found.append(Recommendation(baseline, score, matched, citing))
    found.sort(key=lambda rec: (-rec.score, rec.baseline["name"]))
    return found[: max(k, 0)]

"""Rediscovery audit: which retained negatives restate barriers already in the literature?

    python tools/audit/rediscovery.py export --out DIR --clusters 60 --batches 6
    python tools/audit/rediscovery.py search 'abs:"barren plateau" AND abs:gradient' --who batch-01
    python tools/audit/rediscovery.py import DIR/out/*.jsonl
    python tools/audit/rediscovery.py spot-export --out FILE --n 30
    python tools/audit/rediscovery.py import --spot-check FILE.jsonl
    python tools/audit/rediscovery.py report

Negatives are clustered by their reasoning. A judge (in-session subagents) states each
cluster's shared barrier in standard terms, searches arXiv through the `search` command
(paced to one request per 3 s across processes and cached), and labels the cluster
published / adjacent / not-found / unclear. A "published" label needs a citation whose
abstract contains the judge's quote verbatim; otherwise it is downgraded to unclear.
Labels propagate from the shown members to the rest of the cluster.

Outputs: research/audits/rediscovery_audit.json and REDISCOVERY_AUDIT.md. Inputs that
make the report reproducible are committed next to them: the cluster assignment, the
judgements and the query log. The raw arXiv responses stay in the git-ignored cache.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import random
import re
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.audit import failure_modes as fm  # noqa: E402
from tools.corpus.docs import read_json  # noqa: E402
from tools.corpus.sources.arxiv import Client, Paper, parse_atom  # noqa: E402

CACHE_DIR = "research/corpus_index/arxiv_cache"
AUDITS = "research/audits"
CLUSTERS_FILE = f"{AUDITS}/rediscovery_clusters.json"
JUDGEMENTS_FILE = f"{AUDITS}/rediscovery_judgements.json"
QUERY_LOG = f"{AUDITS}/rediscovery_queries.jsonl"

LABELS = {
    "published": "A retrieved abstract states the same barrier for the same problem setting; the records add at most instances.",
    "adjacent": "The technique or barrier is known, but in a different setting, or the literature only implies it.",
    "not-found": "No retrieved abstract states the barrier after a reasonable search.",
    "unclear": "The cluster is too heterogeneous or its records too terse to judge.",
}
UNJUDGED = "unjudged"

# Records whose barrier is textbook-known, fixed before any judging. Each must come back "published".
GROUND_TRUTH = {
    "NEG-BARREN-PLATEAUS-VARIATIONAL-QUANTUM-HORIZON": "Barren plateaus in parameterized circuits (McClean et al. 2018) and the Lie-algebraic variance theory.",
    "NEG-QUANTUM-ERROR-MITIGATION-EXPONENTIAL-SAMPLING-BARRIER": "Universal sampling-cost bounds for error mitigation (Takagi, Endo, Minagawa, Gu 2022; Quek et al. 2022).",
    "NEG-QUANTUM-MACHINE-LEARNING-KERNEL-CONCENTRATION-BARRIER": "Exponential concentration in quantum kernel methods (Thanasilp, Wang, Cerezo, Holmes 2022).",
    "NEG-QUANTUM-SUPREMACY-RCS-ANTICONCENTRATION-BARRIER": "Polynomial-time classical simulation of noisy random circuit sampling (Aharonov, Gao, Landau, Liu, Vazirani 2022).",
    "NEG-QAOA-BOUNDED-DEPTH-OPTIMIZATION-BARRIER": "Locality limits of bounded-depth QAOA (Farhi, Gamarnik, Gutmann 2020; Bravyi, Kliesch, Koenig, Tang 2019).",
    "NEG-BOSON-SAMPLING-PHOTONIC-LOSS-DEQUANTIZATION-BARRIER": "Classical simulation of lossy boson sampling (Oszmaniec and Brod 2018; Garcia-Patron, Renema, Shchesnovich 2019).",
    "NEG-CONTINUOUS-VARIABLE-GKP-NON-GAUSSIAN-BARRIER": "Efficient classical simulation of Gaussian and positive-Wigner circuits (Bartlett et al. 2002; Mari and Eisert 2012).",
    "NEG-SYMMETRIC-GROUP-KRONECKER-RACAH-BARRIER": "Limits of Fourier sampling over S_n for graph isomorphism (Moore, Russell, Schulman 2005; Hallgren et al. 2006).",
    "NEG-STRONGLY-COSPECTRAL-QUANTUM-WALK-BLINDNESS": "Quantum walks fail to distinguish strongly regular graphs (Smith 2010; Gamble et al. 2010).",
    "NEG-LINEAR-CODE-EQUIVALENCE-WREATH-BARRIER": "Quantum Fourier sampling resists the code-equivalence HSP behind McEliece (Dinh, Moore, Russell 2011).",
}

_NEW_ID = r"\d{4}\.\d{4,5}"
_OLD_ID = r"[a-z-]+(?:\.[A-Z]{2})?/\d{7}"
_ID = rf"(?:{_NEW_ID}|{_OLD_ID})"
_CITE_PATTERNS = (
    re.compile(rf"arxiv\.org/(?:abs|pdf)/({_ID})(?:v\d+)?", re.I),
    re.compile(rf"arxiv\s*:\s*({_ID})(?:v\d+)?", re.I),
)
_STRIP = (
    re.compile(r"https?://(?:export\.)?arxiv\.org/\S+", re.I),
    re.compile(rf"arxiv\s*:\s*{_ID}(?:v\d+)?", re.I),
    re.compile(rf"\b{_OLD_ID}(?:v\d+)?\b"),
    re.compile(rf"\b{_NEW_ID}(?:v\d+)?\b"),
)


def strip_citations(text: str) -> str:
    for pattern in _STRIP:
        text = pattern.sub("[ref]", text)
    return text


def cited_ids(record: dict) -> list[str]:
    blob = json.dumps(record, default=str)
    return sorted({m.group(1) for pattern in _CITE_PATTERNS for m in pattern.finditer(blob)})


@dataclass
class Cluster:
    cluster_id: str
    members: list[str]
    terms: list[str]
    similarity: dict[str, float] = field(default_factory=dict)


def _record_text(record: dict) -> str:
    return strip_citations(fm.record_text(record))


def cluster_negatives(records: list[dict], n_clusters: int = 60, seed: int = 0) -> list[Cluster]:
    """Spherical k-means on TF-IDF (via SVD) of claim + reason + lesson."""
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize

    ids = [record["id"] for record in records]
    texts = [_record_text(record) for record in records]
    n = len(texts)
    k = max(1, min(n_clusters, n))
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2 if n >= 50 else 1,
        max_df=0.5 if n >= 50 else 1.0,
        sublinear_tf=True,
        token_pattern=r"(?u)\b[A-Za-z][A-Za-z0-9_]+\b",
    )
    tfidf = vectorizer.fit_transform(texts)
    components = max(1, min(100, n - 1, tfidf.shape[1] - 1))
    if k == 1 or components < 2:
        labels = np.zeros(n, dtype=int)
    else:
        reduced = normalize(TruncatedSVD(n_components=components, random_state=seed).fit_transform(tfidf))
        labels = KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(reduced)
    terms = np.asarray(vectorizer.get_feature_names_out())
    clusters = []
    for label in sorted(set(labels)):
        rows = np.flatnonzero(labels == label)
        centroid = np.asarray(tfidf[rows].mean(axis=0)).ravel()
        norm = np.linalg.norm(centroid) or 1.0
        sims = np.asarray(tfidf[rows] @ (centroid / norm)).ravel()
        order = rows[np.argsort(-sims)]
        similarity = {ids[r]: round(float(s), 4) for r, s in zip(rows, sims)}
        clusters.append(Cluster("", [ids[r] for r in order], [str(t) for t in terms[np.argsort(-centroid)[:8]]], similarity))
    clusters.sort(key=lambda c: (-len(c.members), c.members[0]))
    for index, cluster in enumerate(clusters, start=1):
        cluster.cluster_id = f"C{index:02d}"
    return clusters


def _member(record: dict, similarity: float) -> dict:
    return {
        "id": record["id"],
        "claim": strip_citations(str(record.get("claim", "")))[:700],
        "reason_invalid": strip_citations(str(record.get("reason_invalid", "")))[:900],
        "lesson": strip_citations(str(record.get("lesson", "")))[:500],
        "evidence_keys": sorted(record.get("evidence", {}))[:20] if fm.is_templated(record) else [],
        "similarity": similarity,
    }


def build_packets(
    clusters: list[Cluster], records: list[dict], corpus=None, max_members: int = 6, must_include: set[str] = frozenset()
) -> list[dict]:
    by_id = {record["id"]: record for record in records}
    packets = []
    for cluster in clusters:
        shown = cluster.members[:max_members]
        shown += [m for m in cluster.members if m in must_include and m not in shown]
        literature = []
        if corpus is not None:
            query = " ".join(cluster.terms) + " " + " ".join(by_id[m].get("claim", "") for m in shown[:3])
            for hit in corpus.search(query, kinds=("literature",), k=8):
                literature.append({"doc_id": hit.doc_id, "title": hit.title, "url": hit.meta.get("url"), "snippet": hit.snippet})
        packets.append({
            "cluster": cluster.cluster_id,
            "size": len(cluster.members),
            "terms": cluster.terms,
            "members": [_member(by_id[m], cluster.similarity.get(m, 0.0)) for m in shown],
            "local_literature": literature,
        })
    return packets


JUDGE_INSTRUCTIONS = """\
# Rediscovery judging

You are auditing a quantum-algorithm research registry. Each cluster groups retained
negative results that share their reasoning. Decide whether the cluster's shared
barrier, the general reason these proposals fail, is already in the published literature.

For each cluster in your batch:

1. Read the members and write one sentence, `barrier`, that states the shared barrier in
   standard terminology (no internal jargon or record ids).
2. Search arXiv with the repository's search command, run from the repository root:

       /opt/anaconda3/bin/python3 tools/audit/rediscovery.py search 'QUERY' --who BATCH

   QUERY uses arXiv API syntax, e.g. `abs:"barren plateau" AND abs:gradient` or
   `ti:"graph isomorphism" AND abs:"coset states"`. Run 2 to 5 queries per cluster, using
   standard names of problems and techniques. Results are cached; a new query waits up to
   a few seconds for arXiv's rate limit. Also read the packet's `local_literature`.
   Do not use any other web or search tool, so the audit is reproducible from the cache.
3. Pick a label:
   - `published`: a retrieved abstract states the same barrier for the same problem
     setting; the cluster adds at most specific instances.
   - `adjacent`: the technique or barrier is known, but in a different setting, or the
     literature only implies it.
   - `not-found`: no retrieved abstract states it after a reasonable search.
   - `unclear`: the cluster is too heterogeneous or its records too terse.
4. Cite up to 3 papers that appeared in your search results (`arxiv_id`) or in
   `local_literature` (`doc_id`), each with a quote of at least 6 words copied verbatim
   from that paper's abstract or snippet. Quotes are checked automatically; a citation
   whose quote is not found is discarded, and a `published` label with no surviving
   citation becomes `unclear`.
5. If a shown member clearly deserves a different label from the cluster, add it to
   `member_overrides`.

Write one JSON object per line (JSONL), one line per cluster, to your output path:

{"cluster": "C07", "barrier": "...", "label": "published", "confidence": 0.8, "citations": [{"arxiv_id": "1803.11173", "quote": "..."}], "member_overrides": {"RECORD-ID": {"label": "adjacent", "note": "..."}}, "queries": ["..."]}

`confidence` is your probability (0 to 1) that the label is right. Do not skip clusters.
"""


def export_batches(packets: list[dict], out_dir: Path, n_batches: int, seed: int = 0) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INSTRUCTIONS.md").write_text(JUDGE_INSTRUCTIONS, encoding="utf-8")
    order = list(packets)
    random.Random(seed).shuffle(order)
    paths = []
    for index in range(n_batches):
        path = out_dir / f"batch_{index + 1:02d}.json"
        path.write_text(json.dumps({"batch": index + 1, "labels": LABELS, "clusters": order[index::n_batches]}, indent=1), encoding="utf-8")
        paths.append(path)
    return paths


class PacedOpener:
    """URL opener that keeps arXiv requests 3 s apart across processes (lock file + timestamp)."""

    def __init__(
        self,
        state_dir: Path,
        delay: float = 3.0,
        opener: Callable = urllib.request.urlopen,
        now: Callable[[], float] = time.time,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.state_dir, self.delay, self.opener, self.now, self.sleep = Path(state_dir), delay, opener, now, sleep

    def __call__(self, request, timeout: int = 30):
        self.state_dir.mkdir(parents=True, exist_ok=True)
        stamp = self.state_dir / ".arxiv_pace"
        with open(self.state_dir / ".arxiv_pace.lock", "a+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                last = float(stamp.read_text() or 0) if stamp.exists() else 0.0
                wait = last + self.delay - self.now()
                if wait > 0:
                    self.sleep(wait)
                try:
                    return self.opener(request, timeout=timeout)
                finally:
                    stamp.write_text(repr(self.now()))
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)


def search(client: Client, query: str, max_results: int = 15, log: Path | None = None, who: str = "") -> list[dict]:
    papers = client.search(query, max_results=max_results, sort_by="relevance")
    rows = [
        {"arxiv_id": p.arxiv_id, "published": p.published, "title": p.title, "authors": p.authors[:4], "abstract": p.abstract}
        for p in papers
    ]
    if log is not None:
        log.parent.mkdir(parents=True, exist_ok=True)
        entry = {"query": query, "who": who, "results": [r["arxiv_id"] for r in rows], "at": dt.datetime.now().isoformat(timespec="seconds")}
        with log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
    return rows


def known_papers(cache_dir: Path) -> dict[str, Paper]:
    papers: dict[str, Paper] = {}
    if not cache_dir.exists():
        return papers
    for path in sorted(cache_dir.glob("*.xml")):
        try:
            for paper in parse_atom(path.read_bytes()):
                papers.setdefault(paper.arxiv_id, paper)
        except Exception:  # noqa: BLE001 - a truncated cache file should not stop the report
            continue
    return papers


def _norm(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def _verify(citation: dict, papers: dict[str, Paper], local: dict[str, str]) -> dict:
    arxiv_id, doc_id = citation.get("arxiv_id"), citation.get("doc_id")
    source = papers[arxiv_id].abstract if arxiv_id in papers else local.get(doc_id or "", "")
    title = papers[arxiv_id].title if arxiv_id in papers else doc_id or ""
    quote = str(citation.get("quote", ""))
    verified = bool(source) and len(_norm(quote).split()) >= 6 and _norm(quote) in _norm(source)
    return {"arxiv_id": arxiv_id, "doc_id": doc_id, "title": title, "quote": quote[:400], "verified": verified}


def _rows(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return json.loads(text) if text.startswith("[") else [json.loads(line) for line in text.splitlines() if line.strip()]


def import_judgements(paths: list[Path], papers: dict[str, Paper], local: dict[str, str]) -> dict[str, dict]:
    judged: dict[str, dict] = {}
    for path in paths:
        for row in _rows(path):
            cluster, label = row.get("cluster"), row.get("label")
            if not cluster or label not in LABELS:
                raise ValueError(f"{path}: bad cluster/label {cluster!r}/{label!r}")
            overrides = {}
            for record_id, override in (row.get("member_overrides") or {}).items():
                if override.get("label") not in LABELS:
                    raise ValueError(f"{path}: bad override label for {record_id}")
                overrides[record_id] = {"label": override["label"], "note": str(override.get("note", ""))[:300]}
            citations = [_verify(c, papers, local) for c in (row.get("citations") or [])[:3]]
            entry = {
                "label": label,
                "barrier": str(row.get("barrier", ""))[:500],
                "confidence": max(0.0, min(1.0, float(row.get("confidence", 0.5)))),
                "citations": citations,
                "member_overrides": overrides,
                "queries": [str(q) for q in row.get("queries", [])][:10],
            }
            if label == "published" and not any(c["verified"] for c in citations):
                entry["label"], entry["downgraded_from"] = "unclear", "published"
            judged[cluster] = entry
    return judged


def analyse(
    records: list[dict],
    clusters: list[Cluster],
    judgements: dict[str, dict],
    truth: dict[str, str],
    shown: set[str],
    retrieved: set[str] = frozenset(),
    spot_check: dict[str, dict] | None = None,
) -> dict:
    cluster_of = {m: c for c in clusters for m in c.members}
    rows = []
    for record in records:
        cluster = cluster_of.get(record["id"])
        judgement = judgements.get(cluster.cluster_id) if cluster else None
        if judgement is None:
            label, basis = UNJUDGED, "none"
        else:
            override = judgement["member_overrides"].get(record["id"])
            label = override["label"] if override else judgement["label"]
            basis = "shown" if record["id"] in shown else "propagated"
        rows.append({
            "id": record["id"],
            "cluster": cluster.cluster_id if cluster else None,
            "similarity": cluster.similarity.get(record["id"]) if cluster else None,
            "track": fm.track_for(record),
            "label": label,
            "basis": basis,
            "cited_ids": cited_ids(record),
        })
    by_id = {row["id"]: row for row in rows}
    counts = Counter(row["label"] for row in rows)
    judged = [row for row in rows if row["label"] != UNJUDGED]
    by_track: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        by_track[row["track"]][row["label"]] += 1

    truth_rows = []
    for record_id, reference in sorted(truth.items()):
        row = by_id.get(record_id)
        cluster_judgement = judgements.get(row["cluster"]) if row and row["cluster"] else None
        truth_rows.append({
            "id": record_id,
            "reference": reference,
            "label": row["label"] if row else "missing",
            "citations": [c for c in (cluster_judgement or {}).get("citations", []) if c["verified"]],
        })
    cited_rows = []
    for row in rows:
        if row["cited_ids"]:
            judgement = judgements.get(row["cluster"]) or {}
            judged_ids = {c.get("arxiv_id") for c in judgement.get("citations", []) if c["verified"]}
            cited_rows.append({
                "id": row["id"],
                "cited_ids": row["cited_ids"],
                "retrieved": sorted(set(row["cited_ids"]) & set(retrieved)),
                "cited_by_judge": sorted(set(row["cited_ids"]) & judged_ids),
                "label": row["label"],
            })

    cluster_rows = []
    for cluster in clusters:
        judgement = judgements.get(cluster.cluster_id, {})
        cluster_rows.append({
            "cluster": cluster.cluster_id,
            "size": len(cluster.members),
            "terms": cluster.terms,
            "label": judgement.get("label", UNJUDGED),
            "barrier": judgement.get("barrier", ""),
            "confidence": judgement.get("confidence"),
            "citations": judgement.get("citations", []),
            "downgraded_from": judgement.get("downgraded_from"),
            "queries": judgement.get("queries", []),
            "tracks": dict(Counter(by_id[m]["track"] for m in cluster.members if m in by_id).most_common(3)),
        })
    result = {
        "generated_by": "tools/audit/rediscovery.py",
        "generated_on": dt.date.today().isoformat(),
        "total": len(rows),
        "labels": LABELS,
        "counts": dict(counts),
        "judged": len(judged),
        "basis": dict(Counter(row["basis"] for row in rows)),
        "by_track": {track: dict(counter) for track, counter in sorted(by_track.items())},
        "ground_truth": {
            "n": len(truth_rows),
            "published": sum(r["label"] == "published" for r in truth_rows),
            "rows": truth_rows,
        },
        "cited_records": cited_rows,
        "clusters": cluster_rows,
        "records": rows,
    }
    if spot_check:
        agree = sum(1 for v in spot_check.values() if v.get("agree"))
        result["spot_check"] = {"n": len(spot_check), "agree": agree, "rows": spot_check}
    return result


def _pct(part: float, whole: float) -> str:
    return f"{100 * part / whole:.0f}%" if whole else "-"


def render(analysis: dict) -> str:
    counts, judged = analysis["counts"], analysis["judged"]
    lines = [
        "# Rediscovery Audit",
        "",
        f"Generated {analysis['generated_on']} by `tools/audit/rediscovery.py`; do not edit by hand.",
        f"Scope: the {analysis['total']} records in `research/registry/negative_results.json`, grouped into",
        f"{len(analysis['clusters'])} clusters by shared reasoning. A judge searched arXiv for each cluster's barrier",
        "and labelled it; labels propagate from the members it read to the rest of the cluster.",
        "\"Published\" requires a citation whose abstract contains the judge's quote verbatim.",
        "",
        "## Headline",
        "",
        "| Label | Records | Share of judged | Meaning |",
        "|---|---|---|---|",
    ]
    for label, meaning in LABELS.items():
        lines.append(f"| {label} | {counts.get(label, 0)} | {_pct(counts.get(label, 0), judged)} | {meaning} |")
    if counts.get(UNJUDGED):
        lines.append(f"| {UNJUDGED} | {counts[UNJUDGED]} | - | Not in a judged cluster (for example, added after the export). |")
    basis = analysis["basis"]
    lines += [
        "",
        f"Basis: {basis.get('shown', 0)} records were read by a judge; {basis.get('propagated', 0)} inherited their cluster's label.",
        "",
        "## By track",
        "",
        "| Track | Records | Published | Adjacent | Not found | Unclear |",
        "|---|---|---|---|---|---|",
    ]
    tracks = sorted(analysis["by_track"].items(), key=lambda item: -sum(item[1].values()))
    for track, labels in tracks:
        n = sum(labels.values())
        lines.append(
            f"| {fm.TRACK_TITLES.get(track, track)} | {n} | "
            + " | ".join(_pct(labels.get(name, 0), n) for name in ("published", "adjacent", "not-found", "unclear"))
            + " |"
        )
    gt = analysis["ground_truth"]
    lines += [
        "",
        "## Ground truth",
        "",
        f"{gt['n']} records restate textbook barriers and were chosen before judging. {gt['published']} of them came back published.",
        "",
        "| Record | Known reference | Label | Verified citation |",
        "|---|---|---|---|",
    ]
    for row in gt["rows"]:
        cite = row["citations"][0] if row["citations"] else None
        cite_text = f"{cite.get('arxiv_id') or cite.get('doc_id')} {cite.get('title', '')[:70]}" if cite else ""
        lines.append(f"| `{row['id']}` | {row['reference']} | {row['label']} | {cite_text} |")
    if analysis["cited_records"]:
        lines += ["", "Records that cite an arXiv id themselves (ids were hidden from the judge):", ""]
        for row in analysis["cited_records"]:
            lines.append(
                f"- `{row['id']}` cites {', '.join(row['cited_ids'])}: retrieved by search "
                f"{'yes' if row['retrieved'] else 'no'}, cited by the judge {'yes' if row['cited_by_judge'] else 'no'}, label {row['label']}."
            )
    spot = analysis.get("spot_check")
    if spot:
        lines += [
            "",
            f"Spot check: a fresh reviewer re-read {spot['n']} randomly chosen judged records with their label and citations "
            f"and agreed with {spot['agree']} ({_pct(spot['agree'], spot['n'])}).",
        ]
    queue = [c for c in analysis["clusters"] if c["label"] in ("published", "adjacent", "unclear")]
    queue.sort(key=lambda c: (c["confidence"] if c["confidence"] is not None else 0, -c["size"]))
    lines += [
        "",
        "## Review queue",
        "",
        "Clusters a human should check first: published, adjacent or unclear labels, lowest judge confidence first.",
        "",
        "| Cluster | Records | Label | Confidence | Barrier | Citation |",
        "|---|---|---|---|---|---|",
    ]
    for c in queue[:20]:
        cite = next((x for x in c["citations"] if x["verified"]), None)
        cite_text = f"{cite.get('arxiv_id') or cite.get('doc_id')}" if cite else ""
        confidence = "-" if c["confidence"] is None else f"{c['confidence']:.2f}"
        lines.append(f"| {c['cluster']} | {c['size']} | {c['label']} | {confidence} | {c['barrier'].replace('|', '/')[:220]} | {cite_text} |")
    lines += ["", "## Clusters", "", "| Cluster | Records | Main tracks | Label | Top terms |", "|---|---|---|---|---|"]
    for c in analysis["clusters"]:
        tracks_text = ", ".join(fm.TRACK_TITLES.get(t, t) for t in c["tracks"])
        lines.append(f"| {c['cluster']} | {c['size']} | {tracks_text} | {c['label']} | {', '.join(c['terms'][:6])} |")
    return "\n".join(lines).rstrip() + "\n"


def _save_clusters(root: Path, clusters: list[Cluster], shown: set[str], n_records: int) -> None:
    path = root / CLUSTERS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"exported_on": dt.date.today().isoformat(), "records": n_records, "shown": sorted(shown), "clusters": [asdict(c) for c in clusters]}
    path.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _load_clusters(root: Path) -> tuple[list[Cluster], set[str]] | None:
    path = root / CLUSTERS_FILE
    if not path.exists():
        return None
    data = read_json(path)
    return [Cluster(**c) for c in data["clusters"]], set(data.get("shown", []))


def _load_judgements(root: Path) -> dict:
    path = root / JUDGEMENTS_FILE
    return read_json(path) if path.exists() else {"clusters": {}, "spot_check": {}}


def _save_judgements(root: Path, data: dict) -> None:
    path = root / JUDGEMENTS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _local_texts(root: Path, paths: list[Path]) -> dict[str, str]:
    wanted = {c.get("doc_id") for p in paths for row in _rows(p) for c in row.get("citations") or [] if c.get("doc_id")}
    if not wanted:
        return {}
    from tools.corpus.api import Corpus

    corpus = Corpus(root)
    texts = {}
    for doc_id in wanted:
        doc = corpus.get(doc_id)
        if doc is not None:
            texts[doc_id] = doc.text
    return texts


def _client(root: Path) -> Client:
    cache = root / CACHE_DIR
    return Client(opener=PacedOpener(cache), delay=0.0, cache_dir=cache)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export", help="Cluster negatives and write judge batches.")
    export.add_argument("--out", type=Path, required=True)
    export.add_argument("--clusters", type=int, default=60)
    export.add_argument("--batches", type=int, default=6)
    export.add_argument("--max-members", type=int, default=6)
    find = sub.add_parser("search", help="Search arXiv (paced, cached, logged).")
    find.add_argument("query")
    find.add_argument("--max", type=int, default=15)
    find.add_argument("--who", default="")
    imp = sub.add_parser("import", help="Import judge outputs (JSONL).")
    imp.add_argument("files", nargs="+", type=Path)
    imp.add_argument("--spot-check", action="store_true", help="Files hold reviewer verdicts {id, agree, note}.")
    spot = sub.add_parser("spot-export", help="Sample judged records for an independent reviewer.")
    spot.add_argument("--out", type=Path, required=True)
    spot.add_argument("--n", type=int, default=30)
    spot.add_argument("--seed", type=int, default=0)
    sub.add_parser("report", help="Write rediscovery_audit.json and REDISCOVERY_AUDIT.md.")
    args = parser.parse_args(argv)
    root = args.root
    records = fm.load_records(root)

    if args.command == "export":
        from tools.corpus.api import Corpus

        corpus = Corpus(root)
        corpus.refresh()
        clusters = cluster_negatives(records, n_clusters=args.clusters)
        must = set(GROUND_TRUTH) | {r["id"] for r in records if cited_ids(r)}
        packets = build_packets(clusters, records, corpus, max_members=args.max_members, must_include=must)
        export_batches(packets, args.out, args.batches)
        _save_clusters(root, clusters, {m["id"] for p in packets for m in p["members"]}, len(records))
        print(f"{len(clusters)} clusters in {args.batches} batches; instructions in {args.out / 'INSTRUCTIONS.md'}")
        return 0

    if args.command == "search":
        rows = search(_client(root), args.query, max_results=args.max, log=root / QUERY_LOG, who=args.who)
        for row in rows:
            print(f"[{row['arxiv_id']}] {row['published']} {row['title']}\n    {', '.join(row['authors'])}\n    {row['abstract'][:900]}\n")
        if not rows:
            print("no results")
        return 0

    data = _load_judgements(root)
    if args.command == "import":
        if args.spot_check:
            for path in args.files:
                for row in _rows(path):
                    data.setdefault("spot_check", {})[row["id"]] = {"agree": bool(row.get("agree")), "note": str(row.get("note", ""))[:400]}
        else:
            papers = known_papers(root / CACHE_DIR)
            judged = import_judgements(args.files, papers, _local_texts(root, args.files))
            data.setdefault("clusters", {}).update(judged)
            dropped = sum(1 for j in judged.values() for c in j["citations"] if not c["verified"])
            downgraded = sum(1 for j in judged.values() if j.get("downgraded_from"))
            print(f"imported {len(judged)} clusters; {dropped} unverified citations dropped; {downgraded} published labels downgraded")
        _save_judgements(root, data)
        return 0

    loaded = _load_clusters(root)
    clusters, shown = loaded if loaded else (cluster_negatives(records), set())
    papers = known_papers(root / CACHE_DIR)
    analysis = analyse(records, clusters, data.get("clusters", {}), GROUND_TRUTH, shown, set(papers), data.get("spot_check"))

    if args.command == "spot-export":
        by_id = {r["id"]: r for r in records}
        judged_rows = [row for row in analysis["records"] if row["label"] != UNJUDGED]
        sample = random.Random(args.seed).sample(judged_rows, min(args.n, len(judged_rows)))
        clusters_by_id = {c["cluster"]: c for c in analysis["clusters"]}
        items = []
        for row in sample:
            cluster = clusters_by_id[row["cluster"]]
            citations = []
            for c in cluster["citations"]:
                if c["verified"]:
                    paper = papers.get(c["arxiv_id"] or "")
                    citations.append({**c, "abstract": paper.abstract if paper else ""})
            items.append({**_member(by_id[row["id"]], row["similarity"] or 0.0), "assigned_label": row["label"],
                          "cluster_barrier": cluster["barrier"], "citations": citations, "basis": row["basis"]})
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"labels": LABELS, "items": items}, indent=1), encoding="utf-8")
        print(f"wrote {len(items)} spot-check items")
        return 0

    audits = root / AUDITS
    audits.mkdir(parents=True, exist_ok=True)
    (audits / "rediscovery_audit.json").write_text(json.dumps(analysis, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (audits / "REDISCOVERY_AUDIT.md").write_text(render(analysis), encoding="utf-8")
    print(json.dumps({"total": analysis["total"], "counts": analysis["counts"], "ground_truth": {
        k: analysis["ground_truth"][k] for k in ("n", "published")}}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

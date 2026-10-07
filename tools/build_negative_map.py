"""Lay out the negative results as a 2D map for the website.

Records with similar wording land near each other: TF-IDF over id, claim, and
reason, reduced with truncated SVD, then placed with t-SNE. K-means groups the
layout into regions, each named by its most distinctive two-word phrase.

Needs scikit-learn, so it runs locally and its output is committed:
    python tools/build_negative_map.py
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TOKEN = r"(?u)\b[a-zA-Z][a-zA-Z0-9]{2,}\b"
# Phrases made of these words describe the claim's grammar, not its topic.
FILLER = {
    "algorithm", "efficient", "evidence", "exp", "gives", "hard", "polynomial", "provide", "provides",
    "quantum", "row", "rows", "self", "supplies", "supply", "time", "yields",
}


def _is_topic(phrase: str) -> bool:
    return not any(word in FILLER for word in phrase.split())


def _document(record: dict[str, Any]) -> str:
    words = re.sub(r"[-_]+", " ", record["id"]).lower()
    return " ".join([words, record.get("claim", ""), record.get("reason", "")])


def _region_label(claims_matrix: Any, members: Any, terms: Any, used: set[str]) -> str:
    import numpy as np

    mean = np.asarray(claims_matrix[members].mean(axis=0)).ravel()
    for index in np.argsort(-mean):
        term = terms[index]
        if mean[index] <= 0:
            break
        if _is_topic(term) and term not in used:
            return term
    return ""


def build_map(records: list[dict[str, Any]], seed: int = 7, regions: int = 9) -> dict[str, Any]:
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.manifold import TSNE

    n = len(records)
    vectorizer = TfidfVectorizer(
        stop_words="english", min_df=min(3, n), max_df=0.5 if n >= 50 else 1.0, token_pattern=TOKEN
    )
    features = vectorizer.fit_transform([_document(r) for r in records])
    components = max(2, min(40, features.shape[1] - 1))
    reduced = TruncatedSVD(n_components=components, random_state=seed).fit_transform(features)
    reduced = reduced / (np.linalg.norm(reduced, axis=1, keepdims=True) + 1e-9)
    perplexity = min(30, max(5, (n - 1) // 3))
    layout = TSNE(
        n_components=2, perplexity=perplexity, init="pca", metric="cosine", random_state=seed
    ).fit_transform(reduced)
    layout = (layout - layout.min(axis=0)) / (layout.max(axis=0) - layout.min(axis=0))

    clusters = KMeans(n_clusters=min(regions, n), n_init=10, random_state=seed).fit(layout)
    phrases = TfidfVectorizer(
        stop_words="english", ngram_range=(2, 2), min_df=min(2, n), token_pattern=TOKEN
    )
    claims = phrases.fit_transform([r.get("claim", "") for r in records])
    terms = phrases.get_feature_names_out()

    labels = clusters.labels_
    order = sorted(set(labels), key=lambda c: -int(np.sum(labels == c)))
    used: set[str] = set()
    region_list = []
    for cluster in order:
        members = np.where(labels == cluster)[0]
        label = _region_label(claims, members, terms, used)
        used.add(label)
        cx, cy = layout[members].mean(axis=0)
        region_list.append(
            {"x": round(float(cx), 4), "y": round(float(cy), 4), "label": label, "count": int(len(members))}
        )

    points = [
        {"id": r["id"], "x": round(float(x), 4), "y": round(float(y), 4)} for r, (x, y) in zip(records, layout)
    ]
    return {"points": points, "regions": region_list}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--regions", type=int, default=9, help="Number of labelled regions.")
    args = parser.parse_args(argv)
    data_dir = args.root / "site" / "data"
    records = json.loads((data_dir / "negatives.json").read_text(encoding="utf-8"))["records"]
    payload = build_map(records, regions=args.regions)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    (data_dir / "negative_map.json").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

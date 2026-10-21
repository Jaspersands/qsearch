"""MCP server (stdio) exposing the Q-Search corpus to research agents.

    python tools/corpus/mcp_server.py [--root PATH] [--dense auto|on|off]

Tools: been_tried(idea, k), search_corpus(query, kinds, tags, k), get_doc(doc_id),
classical_baselines(idea, k), check_duplicate_negative(claim, threshold),
screen_dqi_candidate(params) (the DQI soundness screen of tools/dqi_screen; no index needed).
The index refreshes incrementally before a query when it is older than --refresh-seconds.
--dense auto uses embeddings only while every document has one (after `build --dense`);
--dense on also embeds new documents at each refresh. Results carry `index_incomplete` and
`index_issues` so an agent can tell an unreadable registry from an empty match.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import asdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from tools.corpus.api import Corpus, CorpusRootError, checkout_root  # noqa: E402
from tools.corpus.baselines import recommend  # noqa: E402
from tools.corpus.cli import _hit_json, _issues_json, _recommendation_json  # noqa: E402
from tools.corpus.duplicates import NO_NEGATIVES, allow_patterns, claim_report, valid_threshold  # noqa: E402
from tools.corpus.ranking import Embedder, query_terms  # noqa: E402
from tools.dqi_screen.screen import candidate_from_dict, screen  # noqa: E402


def create_server(
    root: Path | None = None, dense: str = "auto", refresh_seconds: float = 30.0, embedder: Embedder | None = None
) -> FastMCP:
    corpus = Corpus(checkout_root(Path(root) if root else None), embedder=embedder)  # CorpusRootError if not a checkout
    last_refresh = [0.0]

    def ready(force: bool = False) -> bool:
        if force or time.time() - last_refresh[0] >= refresh_seconds:
            corpus.refresh(dense=dense == "on")
            last_refresh[0] = time.time()
        # auto: a ranker that cannot see the newest documents would push them down, so wait for full coverage
        return dense == "on" or (dense == "auto" and corpus.has_dense())

    server = FastMCP("qsearch-corpus")

    @server.tool()
    def been_tried(idea: str, k: int = 5) -> dict:
        """Before proposing a research direction, find the closest retained negative results,
        dequantization checks, research notes, handoff passes, theorem modules and literature.
        Returns groups of ranked hits with file:line locations. A close match is a lead to read,
        not a verdict. If index_incomplete is true, a registry could not be read and an empty
        group does not mean the idea is new."""
        use_dense = ready()
        groups = corpus.been_tried(idea, k=k, dense=use_dense)
        groups_json = {name: [_hit_json(h) for h in hits] for name, hits in groups.items()}
        return {"query": idea, "groups": groups_json, **_issues_json(corpus)}

    @server.tool()
    def search_corpus(query: str, kinds: list[str] | None = None, tags: list[str] | None = None, k: int = 10) -> dict:
        """Ranked search over the Q-Search corpus. kinds filters by document kind: negative,
        dequant, note, handoff, theorem, hypothesis, literature, experiment, result, proof,
        candidate. tags filters registry records by applies_to tag."""
        use_dense = ready()
        hits = corpus.search(query, kinds=tuple(kinds or ()), tags=tuple(tags or ()), k=k, dense=use_dense)
        return {"query": query, "hits": [_hit_json(h) for h in hits], **_issues_json(corpus)}

    @server.tool()
    def get_doc(doc_id: str) -> dict:
        """Full text and metadata of one document, by the doc_id a search returned."""
        ready()
        doc = corpus.get(doc_id)
        if doc is None:
            return {"error": f"unknown doc_id {doc_id}"}
        return asdict(doc)

    @server.tool()
    def screen_dqi_candidate(params: dict) -> dict:
        """Screen a DQI candidate against the Mazumder-Niroula soundness rules (arXiv:2610.06753).
        params: name, objective ("count" or "cosine"), q, m, n, rho, and optionally radius,
        min_distance, decoder_known, encoder_known, p, b, c, classical_witness, finite_dqi_mean
        (see tools/dqi_screen/examples). Returns the quantities, each rule's check and a verdict:
        "not viable", "unknown" or "viable". This is a soundness screen, not a proof: the rules
        are asymptotic and assume worst-case Hamming decoding."""
        try:
            return asdict(screen(candidate_from_dict(params)))
        except (TypeError, ValueError) as exc:
            return {"error": str(exc)}

    @server.tool()
    def classical_baselines(idea: str, k: int = 5) -> dict:
        """Before claiming a quantum advantage for an idea, list the classical algorithms it must
        beat: entries of the curated catalog ranked by keyword overlap with the idea plus the
        nearby notes and negatives that already name them, each with a summary, references and,
        when one exists, a command to run it. A recommendation is a competitor to run, not a
        verdict; an empty list does not mean no classical baseline applies."""
        ready()
        recs = recommend(corpus, idea, k=k)
        return {"idea": idea, "recommendations": [_recommendation_json(r) for r in recs], **_issues_json(corpus)}

    @server.tool()
    def check_duplicate_negative(claim: str, threshold: float = 0.6, allow: list[str] | None = None) -> dict:
        """Before filing a new negative result, check whether a retained negative already says
        it. Returns the retained (and quarantined) negatives whose TF-IDF cosine with the claim
        is at least threshold, highest first (the closest five; total counts them all);
        duplicate is true when there is any. Pass the claim and its reason. A match is a record
        to read and extend, not proof of identity: most matches of generated records are sweep
        siblings, one template filled in for another instance. After reading such a sibling,
        pass its id in allow (or an id prefix ending in * for its family): it is then listed
        under allowed and does not count. If index_incomplete is true, no match does not mean
        the claim is new. threshold must be in (0, 1]. A claim with no words to compare (empty
        or only stop words), a threshold outside (0, 1], a bare * in allow or an index with no
        negative records returns an error."""
        if not query_terms(claim):
            return {"error": "the claim has no words to compare (it is empty or only stop words)"}
        try:
            threshold = valid_threshold(threshold)
            patterns = allow_patterns(allow)
        except ValueError as exc:
            return {"error": str(exc)}
        # Always refresh (a no-op costs well under a second): a negative another agent filed
        # inside the refresh window is exactly the duplicate this gate exists to catch.
        ready(force=True)
        report = claim_report(corpus, claim, threshold=threshold, allow=patterns)
        if report.documents == 0:
            return {"error": NO_NEGATIVES, **_issues_json(corpus)}
        return {
            "claim": claim,
            "threshold": threshold,
            "matches": [_hit_json(h) for h in report.matches],
            "total": report.total,
            "allowed": [{"doc_id": h.doc_id, "score": h.score} for h in report.allowed],
            "duplicate": bool(report.matches),
            **_issues_json(corpus),
        }

    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", help="Q-Search checkout to index (default: QSEARCH_ROOT or this repo).")
    parser.add_argument("--dense", choices=("auto", "on", "off"), default="auto")
    parser.add_argument("--refresh-seconds", type=float, default=30.0)
    args = parser.parse_args(argv)
    try:
        server = create_server(Path(args.root) if args.root else None, args.dense, args.refresh_seconds)
    except CorpusRootError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""MCP server (stdio) exposing the Q-Search corpus to research agents.

    python tools/corpus/mcp_server.py [--root PATH] [--dense auto|on|off]

Tools: been_tried(idea, k), search_corpus(query, kinds, tags, k), get_doc(doc_id).
The index refreshes incrementally before a query when it is older than --refresh-seconds.
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

from tools.corpus.api import Corpus  # noqa: E402
from tools.corpus.cli import _hit_json  # noqa: E402


def create_server(root: Path | None = None, dense: str = "auto", refresh_seconds: float = 30.0) -> FastMCP:
    corpus = Corpus(Path(root) if root else None)
    last_refresh = [0.0]

    def ready() -> bool:
        if time.time() - last_refresh[0] >= refresh_seconds:
            corpus.refresh()
            last_refresh[0] = time.time()
        return dense == "on" or (dense == "auto" and corpus.has_dense())

    server = FastMCP("qsearch-corpus")

    @server.tool()
    def been_tried(idea: str, k: int = 5) -> dict:
        """Before proposing a research direction, find the closest retained negative results,
        dequantization checks, research notes, handoff passes, theorem modules and literature.
        Returns groups of ranked hits with file:line locations. A close match is a lead to read,
        not a verdict."""
        use_dense = ready()
        groups = corpus.been_tried(idea, k=k, dense=use_dense)
        return {"query": idea, "groups": {name: [_hit_json(h) for h in hits] for name, hits in groups.items()}}

    @server.tool()
    def search_corpus(query: str, kinds: list[str] | None = None, tags: list[str] | None = None, k: int = 10) -> dict:
        """Ranked search over the Q-Search corpus. kinds filters by document kind: negative,
        dequant, note, handoff, theorem, hypothesis, literature, experiment, result, proof,
        candidate. tags filters registry records by applies_to tag."""
        use_dense = ready()
        hits = corpus.search(query, kinds=tuple(kinds or ()), tags=tuple(tags or ()), k=k, dense=use_dense)
        return {"query": query, "hits": [_hit_json(h) for h in hits]}

    @server.tool()
    def get_doc(doc_id: str) -> dict:
        """Full text and metadata of one document, by the doc_id a search returned."""
        ready()
        doc = corpus.get(doc_id)
        if doc is None:
            return {"error": f"unknown doc_id {doc_id}"}
        return asdict(doc)

    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", help="Q-Search checkout to index (default: QSEARCH_ROOT or this repo).")
    parser.add_argument("--dense", choices=("auto", "on", "off"), default="auto")
    parser.add_argument("--refresh-seconds", type=float, default=30.0)
    args = parser.parse_args(argv)
    create_server(Path(args.root) if args.root else None, args.dense, args.refresh_seconds).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

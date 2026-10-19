"""Search the Q-Search corpus: has this idea been tried, and where is it written up?

    python tools/corpus/cli.py been-tried "use a quadratic extension norm to solve mixed-coset OPI"
    python tools/corpus/cli.py search "Helstrom product readout" --kinds negative,note
    python tools/corpus/cli.py similar negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY
    python tools/corpus/cli.py build [--full] [--dense]

Every query first refreshes the index incrementally (well under a second when nothing changed).
A file or registry record that could not be parsed is reported on stderr; when it is a registry
file, `been-tried` says INDEX INCOMPLETE and exits 2, because missing negatives are not novelty.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.corpus.api import Corpus, Hit  # noqa: E402


def _status(hit: Hit) -> str:
    return str(hit.meta.get("status") or "")


def _hit_json(hit: Hit) -> dict:
    return {
        "doc_id": hit.doc_id,
        "kind": hit.kind,
        "location": hit.location,
        "title": hit.title,
        "snippet": hit.snippet,
        "status": _status(hit),
        "tags": hit.meta.get("tags", []),
        "reason": hit.meta.get("reason"),
        "score": hit.score,
    }


def _print_hit(index: int, hit: Hit) -> None:
    label = hit.doc_id.split(":", 1)[1] if hit.kind in {"negative", "dequant"} else hit.title
    tags = ", ".join(str(t) for t in hit.meta.get("tags", [])[:4])
    extra = " · ".join(part for part in (_status(hit), tags) if part)
    print(f"  {index}. {hit.kind:<10} {label[:110]}" + (f"  [{extra}]" if extra else ""))
    print(f"     {hit.location}")
    if hit.kind in {"negative", "dequant"}:
        print(f"     Claim: {hit.title[:220]}")
        if hit.meta.get("reason"):
            print(f"     Why not: {str(hit.meta['reason'])[:300]}")
    elif hit.snippet:
        print(f"     {hit.snippet}")


def _warn_issues(corpus: Corpus) -> None:
    issues = corpus.issues()
    for issue in issues[:10]:
        print(f"warning: {issue['path']}: {issue['message']}", file=sys.stderr)
    if len(issues) > 10:
        print(f"warning: ... and {len(issues) - 10} more parse problems", file=sys.stderr)
    if corpus.incomplete():
        print("warning: INDEX INCOMPLETE: a registry file or record could not be read; "
              "results may be missing retained negatives.", file=sys.stderr)


def _issues_json(corpus: Corpus) -> dict:
    return {"index_incomplete": corpus.incomplete(), "index_issues": corpus.issues()}


def _corpus(args: argparse.Namespace) -> Corpus:
    corpus = Corpus(Path(args.root) if args.root else None)
    if args.command == "build" or not getattr(args, "no_refresh", False):
        stats = corpus.refresh(full=getattr(args, "full", False), dense=args.command == "build" and args.dense)
        if args.command == "build":
            print(
                f"files scanned {stats.files_scanned}, files changed {stats.files_changed}, "
                f"docs +{stats.docs_added} -{stats.docs_removed}, docs total {stats.docs_total}, "
                f"refit {stats.refit}, vectors +{stats.vectors_added}, {stats.seconds}s"
            )
    _warn_issues(corpus)
    if getattr(args, "dense", False) and args.command != "build" and not corpus.has_dense():
        print("note: dense vectors do not cover every document; run `build --dense` to update them.", file=sys.stderr)
    return corpus


def cmd_build(args: argparse.Namespace) -> int:
    _corpus(args)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    kinds = tuple(k for k in (args.kinds or "").split(",") if k)
    tags = tuple(t for t in (args.tags or "").split(",") if t)
    hits = corpus.search(args.query, kinds=kinds, tags=tags, k=args.k, dense=args.dense)
    if args.json:
        print(json.dumps({"query": args.query, "hits": [_hit_json(h) for h in hits], **_issues_json(corpus)}, indent=2))
        return 0
    for index, hit in enumerate(hits, start=1):
        _print_hit(index, hit)
    return 0


def cmd_been_tried(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    groups = corpus.been_tried(args.idea, k=args.k, dense=args.dense)
    incomplete = corpus.incomplete()
    if args.json:
        payload = {
            "query": args.idea,
            "groups": {name: [_hit_json(h) for h in hits] for name, hits in groups.items()},
            **_issues_json(corpus),
        }
        print(json.dumps(payload, indent=2))
        return 2 if incomplete else 0
    if incomplete:
        print("INDEX INCOMPLETE: a registry file or record could not be read (see the warnings on stderr).")
        print("An empty group below does not mean the idea is new.\n")
    print(f"Been tried? {args.idea[:120]}\n")
    for name, hits in groups.items():
        print(name)
        if not hits:
            print("  (nothing close; the index is incomplete)" if incomplete else "  (nothing close)")
        for index, hit in enumerate(hits, start=1):
            _print_hit(index, hit)
        print()
    print("Ranked by text similarity. A close match is a lead to read, not a verdict on the idea.")
    return 2 if incomplete else 0


def cmd_similar(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    try:
        hits = corpus.similar(args.doc_id, k=args.k, dense=args.dense)
    except KeyError:
        print(f"unknown doc_id {args.doc_id}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"doc_id": args.doc_id, "hits": [_hit_json(h) for h in hits]}, indent=2))
        return 0
    for index, hit in enumerate(hits, start=1):
        _print_hit(index, hit)
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    doc = corpus.get(args.doc_id)
    if doc is None:
        print(f"unknown doc_id {args.doc_id}", file=sys.stderr)
        return 1
    print(json.dumps(asdict(doc), indent=2, default=str))
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    """Held-out check: each case {"id", "query"} should retrieve its record within the top k."""
    corpus = _corpus(args)
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    found = 0
    for case in cases:
        target = case["id"] if ":" in case["id"] else f"negative:{case['id']}"
        hits = corpus.search(case["query"], k=args.k, dense=args.dense, kinds=tuple(case.get("kinds", ())))
        ids = [hit.doc_id for hit in hits]
        rank = ids.index(target) + 1 if target in ids else None
        found += rank is not None
        print(f"{'hit ' + str(rank) if rank else 'MISS ':<6} {target}")
    print(f"\n{found}/{len(cases)} retrieved in the top {args.k}")
    return 0 if found >= args.min else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", help="Q-Search checkout to index (default: QSEARCH_ROOT or this repo).")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser, k: int) -> None:
        p.add_argument("-k", type=int, default=k, help="Results to show (per group for been-tried).")
        p.add_argument("--dense", action="store_true", help="Also rank with local sentence embeddings.")
        p.add_argument("--json", action="store_true")
        p.add_argument("--no-refresh", action="store_true", help="Skip the incremental index refresh.")

    build = sub.add_parser("build", help="Build or update the index.")
    build.add_argument("--full", action="store_true", help="Re-parse every file and refit TF-IDF.")
    build.add_argument("--dense", action="store_true", help="Also compute local sentence embeddings.")
    build.set_defaults(func=cmd_build)

    search = sub.add_parser("search", help="Ranked search over every document kind.")
    search.add_argument("query")
    search.add_argument("--kinds", help="Comma list: negative,dequant,note,handoff,theorem,hypothesis,literature,...")
    search.add_argument("--tags", help="Comma list of registry applies_to tags.")
    common(search, 10)
    search.set_defaults(func=cmd_search)

    tried = sub.add_parser("been-tried", help="Closest negatives, notes, code and literature for an idea.")
    tried.add_argument("idea")
    common(tried, 5)
    tried.set_defaults(func=cmd_been_tried)

    similar = sub.add_parser("similar", help="Documents most like a given doc_id.")
    similar.add_argument("doc_id")
    common(similar, 10)
    similar.set_defaults(func=cmd_similar)

    get = sub.add_parser("get", help="Print one document as JSON.")
    get.add_argument("doc_id")
    get.add_argument("--no-refresh", action="store_true")
    get.set_defaults(func=cmd_get)

    evaluate = sub.add_parser("heldout", help="Held-out retrieval check from a JSON list of {id, query}.")
    evaluate.add_argument("cases")
    evaluate.add_argument("--min", type=int, default=0, help="Exit 1 when fewer cases are retrieved.")
    common(evaluate, 5)
    evaluate.set_defaults(func=cmd_eval)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

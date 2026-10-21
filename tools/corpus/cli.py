"""Search the Q-Search corpus: has this idea been tried, and where is it written up?

    python tools/corpus/cli.py been-tried "use a quadratic extension norm to solve mixed-coset OPI"
    python tools/corpus/cli.py search "Helstrom product readout" --kinds negative,note
    python tools/corpus/cli.py similar negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY
    python tools/corpus/cli.py near-duplicates --out research/audits/registry_duplicates.json --per-family 3
    python tools/corpus/cli.py check-new --text "a draft negative claim"      # exit 2 on a likely duplicate
    python tools/corpus/cli.py build [--full] [--dense]

Every query first refreshes the index incrementally (well under a second when nothing changed).
A file or registry record that could not be parsed is reported on stderr; when it is a registry
file, `been-tried` says INDEX INCOMPLETE and exits 2, because missing negatives are not novelty.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import asdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.corpus.api import Corpus, Hit  # noqa: E402
from tools.corpus.duplicates import REPORT_THRESHOLD, check_claim, near_duplicates  # noqa: E402


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


def _record_label(doc_id: str) -> str:
    prefix, _, rest = doc_id.partition(":")
    return f"{rest} (quarantined)" if prefix == "quarantined" else rest or doc_id


def _cell(text: str, width: int = 160) -> str:
    text = " ".join(str(text).split()).replace("|", "\\|")
    return text if len(text) <= width else text[: width - 1].rstrip() + "…"


def _duplicates_markdown(payload: dict, per_family: int | None, limit: int) -> str:
    pairs = payload["pairs"]
    cap = f", at most {per_family} pairs per sweep family" if per_family is not None else ""
    lines = [
        "# Near-duplicate negatives",
        "",
        f"Generated on {payload['generated_on']} by `python tools/corpus/cli.py near-duplicates`: "
        f"`{payload['kind']}` documents (retained and quarantined negatives) whose TF-IDF cosine is at "
        f"least {payload['threshold']}{cap}, highest first, {len(pairs)} pairs"
        + (f" (the first {limit})." if len(pairs) >= limit else "."),
        "",
        "A cosine of 1.000 means the same words in the same proportions. A name that occurs in a single "
        "record is not in the vocabulary, so two records generated from one template for different "
        "instances (a size, trial, code family or proposal) can score 1.000. Most pairs are such sweep "
        "siblings, not restatements; the per-family cap only groups ids that differ in their last "
        "`-<number>`. A pair is a lead to read, not a verdict; see the hand check in "
        "`tools/corpus/README.md`, \"Duplicates\".",
        "",
        "| cosine | a | b | claim a | claim b |",
        "|---|---|---|---|---|",
    ]
    for pair in pairs:
        lines.append(
            f"| {pair['score']:.3f} | {_record_label(pair['a'])} | {_record_label(pair['b'])} | "
            f"{_cell(pair['title_a'])} | {_cell(pair['title_b'])} |"
        )
    return "\n".join(lines) + "\n"


def cmd_near_duplicates(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    pairs = near_duplicates(
        corpus, kind=args.kind, threshold=args.threshold, limit=args.limit, per_family=args.per_family
    )
    payload = {
        "kind": args.kind,
        "threshold": args.threshold,
        "pairs": [asdict(pair) for pair in pairs],
        "generated_on": dt.date.today().isoformat(),
    }
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        markdown = out.with_name(out.stem.upper() + ".md")
        markdown.write_text(_duplicates_markdown(payload, args.per_family, args.limit), encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2))
    elif args.out:
        print(f"{len(pairs)} pairs at cosine >= {args.threshold}; wrote {out} and {markdown}")
    else:
        for index, pair in enumerate(pairs, start=1):
            print(f"  {index}. {pair.score:.3f}  {_record_label(pair.a)}  ~  {_record_label(pair.b)}")
            print(f"     {pair.title_a[:160]}")
            print(f"     {pair.title_b[:160]}")
        print(f"\n{len(pairs)} pairs at TF-IDF cosine >= {args.threshold}. A pair is a lead to read, not a verdict.")
    return 0


def _claim_text(args: argparse.Namespace) -> str:
    """The claim to check: --text, or a file; a JSON registry record contributes claim + reason_invalid."""
    if args.text is not None:
        return args.text
    raw = Path(args.file).read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(data, dict) and data.get("claim"):
        return f"{data['claim']} {data.get('reason_invalid') or ''}".strip()
    return raw


def cmd_check_new(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    matches = check_claim(corpus, _claim_text(args), threshold=args.threshold)
    if args.json:
        payload = {"matches": [_hit_json(h) for h in matches], "duplicate": bool(matches), **_issues_json(corpus)}
        print(json.dumps(payload, indent=2))
        return 2 if matches else 0
    if not matches:
        print(f"No retained negative has TF-IDF cosine >= {args.threshold} with this claim.")
        if corpus.incomplete():
            print("INDEX INCOMPLETE: a registry could not be read, so no match does not mean the claim is new.")
        return 0
    print(f"POSSIBLE DUPLICATE: {len(matches)} retained negative(s) at TF-IDF cosine >= {args.threshold}.\n")
    for index, hit in enumerate(matches, start=1):
        _print_hit(index, hit)
        print(f"     Cosine: {hit.score:.3f}")
    print("\nRead the record first: extend it, or say how the new claim differs.")
    return 2


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

    dups = sub.add_parser("near-duplicates", help="Pairs of negatives with a high TF-IDF cosine.")
    dups.add_argument("--kind", default="negative", help="Document kind to compare (default: negative).")
    dups.add_argument("--threshold", type=float, default=REPORT_THRESHOLD, help="Minimum cosine (default 0.9).")
    dups.add_argument("--limit", type=int, default=200, help="Pairs to keep, highest first.")
    dups.add_argument("--per-family", type=int, help="At most this many pairs of ids differing only in a trailing number.")
    dups.add_argument("--out", help="Write FILE.json and FILE.md (stem upper-cased) next to it.")
    dups.add_argument("--json", action="store_true")
    dups.add_argument("--no-refresh", action="store_true", help="Skip the incremental index refresh.")
    dups.set_defaults(func=cmd_near_duplicates)

    check = sub.add_parser("check-new", help="Exit 2 when a draft claim is close to a retained negative.")
    source = check.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="The draft claim.")
    source.add_argument("--file", help="A text file, or a JSON record whose claim and reason_invalid are checked.")
    check.add_argument("--threshold", type=float, default=0.6, help="Minimum TF-IDF cosine for a match.")
    check.add_argument("--json", action="store_true")
    check.add_argument("--no-refresh", action="store_true", help="Skip the incremental index refresh.")
    check.set_defaults(func=cmd_check_new)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

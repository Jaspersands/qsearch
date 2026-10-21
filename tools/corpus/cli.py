"""Search the Q-Search corpus: has this idea been tried, and where is it written up?

    python tools/corpus/cli.py been-tried "use a quadratic extension norm to solve mixed-coset OPI"
    python tools/corpus/cli.py search "Helstrom product readout" --kinds negative,note
    python tools/corpus/cli.py similar negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY
    python tools/corpus/cli.py near-duplicates --out research/audits/registry_duplicates.json --per-family 3
    python tools/corpus/cli.py check-new --text "a draft negative claim"      # exit 2 on a likely duplicate
    python tools/corpus/cli.py baselines "sampling the Gibbs law of a signed parity-check code"
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
import textwrap
from dataclasses import asdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.corpus.api import Corpus, CorpusRootError, Hit, checkout_root  # noqa: E402
from tools.corpus.baselines import CatalogError, Recommendation, recommend  # noqa: E402
from tools.corpus.duplicates import (  # noqa: E402
    NO_NEGATIVES,
    REPORT_THRESHOLD,
    ClaimReport,
    DraftError,
    allow_patterns,
    claim_report,
    draft_claims,
    own_ids,
    pair_report,
    valid_threshold,
)
from tools.corpus.ranking import query_terms  # noqa: E402


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


def _recommendation_json(rec: Recommendation) -> dict:
    return {
        "baseline": rec.baseline,
        "score": rec.score,
        "matched": rec.matched,
        "evidence": [_hit_json(h) for h in rec.evidence],
    }


def _record_label(doc_id: str) -> str:
    prefix, _, rest = doc_id.partition(":")
    return f"{rest} (quarantined)" if prefix == "quarantined" else rest or doc_id


def _print_hit(index: int, hit: Hit) -> None:
    label = _record_label(hit.doc_id) if hit.kind in {"negative", "dequant"} else hit.title
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
    corpus = Corpus(checkout_root(Path(args.root) if args.root else None))
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


def _cell(text: str, width: int = 160) -> str:
    text = " ".join(str(text).split()).replace("|", "\\|")
    return text if len(text) <= width else text[: width - 1].rstrip() + "…"


def _pair_count(shown: int, total: int) -> str:
    """'7 pairs', or '5 of 136 pairs' when --limit cut the list."""
    return f"{shown} of {total} pairs" if total > shown else f"{shown} pairs"


def _duplicates_markdown(payload: dict) -> str:
    pairs, kind, total, per_family = payload["pairs"], payload["kind"], payload["total"], payload["per_family"]
    cap = f", at most {per_family} pairs per sweep family" if per_family is not None else ""
    described = f"`{kind}` documents" + (" (retained and quarantined negatives)" if kind == "negative" else "")
    count = (
        f"the first {len(pairs)} of {total} pairs (`--limit {payload['limit']}`)." if total > len(pairs)
        else f"{len(pairs)} pairs."
    )
    lines = [
        "# Near-duplicate negatives" if kind == "negative" else f"# Near-duplicate `{kind}` documents",
        "",
        f"Generated on {payload['generated_on']} by `python tools/corpus/cli.py near-duplicates`: "
        f"{described} whose TF-IDF cosine is at least {payload['threshold']}{cap}, highest first: {count} "
        f"{payload['documents']} documents were compared, on a TF-IDF fit of the current documents.",
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
    out = Path(args.out) if args.out else None
    if out is not None and out.suffix != ".json":
        print(f"error: --out must name a .json file (FILE.md is written next to it), got {out}", file=sys.stderr)
        return 1
    corpus = _corpus(args)
    incomplete = corpus.incomplete()
    if out is not None and incomplete:
        print(
            f"error: INDEX INCOMPLETE: a registry file or record could not be read; not writing {out}. "
            "Repair the registry and run again.",
            file=sys.stderr,
        )
        return 2
    if out is not None:
        corpus.refit()  # scores then depend on the current documents only, so the report reproduces
    report = pair_report(
        corpus, kind=args.kind, threshold=args.threshold, limit=args.limit, per_family=args.per_family
    )
    if report.documents == 0:
        print(f"error: the index has no `{args.kind}` documents; check --kind.", file=sys.stderr)
        return 1
    pairs = report.pairs
    payload = {
        "kind": args.kind,
        "threshold": args.threshold,
        "per_family": args.per_family,
        "limit": args.limit,
        "total": report.total,
        "documents": report.documents,
        "pairs": [asdict(pair) for pair in pairs],
        "generated_on": dt.date.today().isoformat(),
        "changed_since_fit": corpus.changed_since_fit(),
        **_issues_json(corpus),
    }
    count = _pair_count(len(pairs), report.total)
    status = 2 if incomplete else 0
    if out is not None:
        markdown = out.with_name(out.stem.upper() + ".md")
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            markdown.write_text(_duplicates_markdown(payload), encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot write {out} and {markdown}: {exc}", file=sys.stderr)
            return 1
    if args.json:
        print(json.dumps(payload, indent=2))
        return status
    if out is not None:
        print(f"{count} at cosine >= {args.threshold}; wrote {out} and {markdown}")
        return status
    if incomplete:
        print("INDEX INCOMPLETE: a registry file or record could not be read (see the warnings on stderr).")
        print("Pairs of the records that could not be read are missing below.\n")
    for index, pair in enumerate(pairs, start=1):
        print(f"  {index}. {pair.score:.3f}  {_record_label(pair.a)}  ~  {_record_label(pair.b)}")
        print(f"     {pair.title_a[:160]}")
        print(f"     {pair.title_b[:160]}")
    cut = " (raise --limit to see the rest)" if report.total > len(pairs) else ""
    print(f"\n{count} at TF-IDF cosine >= {args.threshold}{cut}. A pair is a lead to read, not a verdict.")
    return status


def _claim_header(report: ClaimReport, threshold: float) -> str:
    if not report.matches:
        return f"no negative record (retained or quarantined) has TF-IDF cosine >= {threshold}"
    of_them = f", {report.quarantined} of them quarantined," if report.quarantined else ""
    shown = f"; the closest {len(report.matches)} are shown" if report.total > len(report.matches) else ""
    return f"POSSIBLE DUPLICATE: {report.total} negative record(s){of_them} at TF-IDF cosine >= {threshold}{shown}"


def cmd_check_new(args: argparse.Namespace) -> int:
    # Read the draft before touching the index, so an unreadable file fails fast with exit 1, never 0.
    if args.text is not None:
        drafts = [(args.text, None)]
    else:
        try:
            raw = Path(args.file).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"error: cannot read {args.file}: {exc}", file=sys.stderr)
            return 1
        try:
            drafts = draft_claims(raw)
        except DraftError as exc:
            print(f"error: {args.file}: {exc}", file=sys.stderr)
            return 1
    if not all(query_terms(text) for text, _ in drafts):
        print("error: the draft claim has no words to compare (it is empty or only stop words).", file=sys.stderr)
        return 1
    corpus = _corpus(args)
    # Each draft leaves out every draft's own record, so a batch gets the same answer once filed.
    exclude = tuple(doc_id for _, record_id in drafts for doc_id in own_ids(record_id))
    allow = tuple(args.allow or ())
    reports = [
        (record_id, claim_report(corpus, text, threshold=args.threshold, exclude=exclude, allow=allow))
        for text, record_id in drafts
    ]
    if reports[0][1].documents == 0:
        print(f"error: {NO_NEGATIVES}; check --root and research/registry/.", file=sys.stderr)
        return 1
    duplicate = any(report.matches for _, report in reports)
    if args.json:
        payload = {
            "matches": [dict(_hit_json(h), draft_id=record_id) for record_id, report in reports for h in report.matches],
            "total": sum(report.total for _, report in reports),
            "allowed": [
                {"doc_id": h.doc_id, "score": h.score, "draft_id": record_id}
                for record_id, report in reports
                for h in report.allowed
            ],
            "drafts": len(reports),
            "duplicate": duplicate,
            **_issues_json(corpus),
        }
        print(json.dumps(payload, indent=2))
        return 2 if duplicate else 0
    for number, (record_id, report) in enumerate(reports, start=1):
        header = _claim_header(report, args.threshold)
        if len(reports) == 1:
            print(header[0].upper() + header[1:] + ("" if report.matches else " with this claim") + ".")
        else:
            print(("" if number == 1 else "\n") + f"{record_id or f'record {number}'}: {header}.")
        if report.allowed:
            names = [_record_label(hit.doc_id) for hit in report.allowed]
            more = f", and {len(names) - 10} more" if len(names) > 10 else ""
            print(f"Not counted: {len(names)} matching record(s) allowed by --allow: {', '.join(names[:10])}{more}.")
        if report.matches:
            print()
        for index, hit in enumerate(report.matches, start=1):
            _print_hit(index, hit)
            print(f"     Cosine: {hit.score:.3f}")
    if not duplicate:
        if corpus.incomplete():
            print("INDEX INCOMPLETE: a registry could not be read, so no match does not mean the claim is new.")
        return 0
    print(
        "\nRead the record first: extend it, or say how the new claim differs. A sweep sibling you have "
        "read and that should stay a separate record can be accepted with --allow ID."
    )
    return 2


def _reference_label(ref: dict) -> str:
    return f"arXiv:{ref['arxiv']}" if "arxiv" in ref else f"research/{ref['note']}.md"


def cmd_baselines(args: argparse.Namespace) -> int:
    corpus = _corpus(args)
    recs = recommend(corpus, args.idea, k=args.k)
    if args.json:
        payload = {"idea": args.idea, "recommendations": [_recommendation_json(r) for r in recs], **_issues_json(corpus)}
        print(json.dumps(payload, indent=2))
        return 0
    if not recs:
        print("No catalog baseline matches this idea by keyword or is named by a nearby note or negative.")
        print("That does not mean no classical baseline applies; the catalog is tools/corpus/baselines.json.")
        return 0
    print(f"Classical baselines for: {args.idea[:120]}\n")
    for index, rec in enumerate(recs, start=1):
        baseline = rec.baseline
        matched = f"matched {', '.join(rec.matched)}" if rec.matched else "no keyword matched"
        cited = (
            f"cited by {', '.join(hit.location for hit in rec.evidence)}" if rec.evidence else "no nearby note names it"
        )
        print(f"  {index}. {baseline['name']}  [{baseline['id']}]  score {rec.score}")
        print(f"     why: {matched}; {cited}")
        print(textwrap.fill(baseline["summary"], width=100, initial_indent=" " * 5, subsequent_indent=" " * 5))
        if baseline["references"]:
            print(f"     references: {', '.join(_reference_label(ref) for ref in baseline['references'])}")
        runnable = baseline.get("runnable") or {}
        if runnable.get("command"):
            entry = f"  (entry {runnable['entry']})" if runnable.get("entry") else ""
            print(f"     run: {runnable['command']}{entry}")
        elif runnable.get("entry"):
            print(f"     call: {runnable['entry']} (a library function; it needs an instance)")
        print()
    print(
        textwrap.fill(
            "Score: the share of a baseline's keywords found in the idea, plus 0.1 for each note or "
            "negative among the ten nearest documents that names it (a note once, however many of its "
            "sections are near). Run the baseline before claiming an advantage; a high score is a lead, "
            "not a verdict.",
            width=100,
        )
    )
    return 0


def _threshold(value: str) -> float:
    try:
        return valid_threshold(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from None


def _allow(value: str) -> str:
    try:
        return allow_patterns([value])[0]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from None


def _count(value: str) -> int:
    number = int(value)
    if number < 1:  # -k 0 would show nothing and then say that no baseline matches
        raise argparse.ArgumentTypeError("-k must be at least 1")
    return number


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
    dups.add_argument("--threshold", type=_threshold, default=REPORT_THRESHOLD, help="Minimum cosine (default 0.9).")
    dups.add_argument("--limit", type=int, default=200, help="Pairs to keep, highest first; the total is still reported.")
    dups.add_argument("--per-family", type=int, help="At most this many pairs of ids differing only in a trailing number.")
    dups.add_argument("--out", help="Write FILE.json and FILE.md (stem upper-cased) next to it.")
    dups.add_argument("--json", action="store_true")
    dups.add_argument("--no-refresh", action="store_true", help="Skip the incremental index refresh.")
    dups.set_defaults(func=cmd_near_duplicates)

    check = sub.add_parser(
        "check-new",
        help="Exit 2 when a draft claim is close to a negative record, 1 when the draft cannot be read or has no words.",
    )
    source = check.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="The draft claim.")
    source.add_argument(
        "--file",
        help="A text file, or a JSON record (or list of records) whose claim and reason_invalid are checked; "
        "a record is never matched with its own id.",
    )
    check.add_argument(
        "--threshold", type=_threshold, default=0.6, help="Minimum TF-IDF cosine for a match, in (0, 1] (default 0.6)."
    )
    check.add_argument(
        "--allow",
        action="append",
        type=_allow,
        metavar="ID",
        help="A record the draft is known to differ from (say a sweep sibling you have read), or an id prefix "
        "ending in * for a family; its matches are listed but do not count. Repeatable.",
    )
    check.add_argument("--json", action="store_true")
    check.add_argument("--no-refresh", action="store_true", help="Skip the incremental index refresh.")
    check.set_defaults(func=cmd_check_new)

    baselines = sub.add_parser("baselines", help="Classical baselines an idea should be compared against.")
    baselines.add_argument("idea")
    baselines.add_argument("-k", type=_count, default=5, help="Baselines to show.")
    baselines.add_argument("--json", action="store_true")
    baselines.add_argument("--no-refresh", action="store_true", help="Skip the incremental index refresh.")
    baselines.set_defaults(func=cmd_baselines)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (CorpusRootError, CatalogError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

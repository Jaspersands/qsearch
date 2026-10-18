"""Where do proposals die? A failure-mode meta-analysis of the negative-results registry.

    python tools/audit/failure_modes.py                         # rules + stored judgements -> report
    python tools/audit/failure_modes.py --export-batches DIR --batches 8
    python tools/audit/failure_modes.py --import out/*.jsonl --judge opus-subagents
    python tools/audit/failure_modes.py --import second/*.jsonl --judge second --second-opinion

Each retained negative gets one primary failure mode: the step at which the proposal
died. A keyword rule pass labels every record. A judge pass (in-session subagents, one
label per group of records that share their reasoning) overrides the rule label where it
exists and measures how far the rules can be trusted for new records.

Outputs: research/audits/failure_modes.json and FAILURE_MODE_META_ANALYSIS.md.
Judgements live in research/audits/failure_mode_judgements.json so the report rebuilds
without re-judging.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.corpus.docs import flatten, read_json  # noqa: E402

REGISTRY = "research/registry/negative_results.json"
JUDGEMENTS = "research/audits/failure_mode_judgements.json"
TEMPLATED_REASON = "Falsified or refined by exact theorem evaluation."


@dataclass(frozen=True)
class Mode:
    title: str
    definition: str
    prefilter: str
    patterns: tuple[tuple[str, float], ...]


MODES: dict[str, Mode] = {
    "classical_competitor": Mode(
        "Classical competitor",
        "A classical algorithm, invariant or canonicalization solves the instance, separates the pair, "
        "or matches the quantum route.",
        "Run the track's standard classical attacks (canonicalization, refinement or WL, support splitting, "
        "LLL, dynamic programming, norm constructions) on the exact instance before building a quantum observable.",
        (
            (r"classical(ly)?[- ]([\w-]+ ){0,2}(algorithm|solver|attack|baseline|reconstruct|recover|simulat|canonicali[sz]|invariant|decod|procedure|dynamic program|filtration|signature|sampler|learn)", 3),
            (r"(matched|matching|equivalent) classical", 3),
            (r"classical(ly)? (recovered|solved|matched|shadowed|separated|computable|efficient)", 3),
            (r"\bdequanti[sz]", 3),
            (r"canonicali[sz]", 2),
            (r"separate[sd]? (the |this |that |each |every )?(code |graph |candidate )?(pair|row|instance|codes|graphs)", 2),
            (r"(colou?r) refinement|weisfeiler|\bWL\b|individuali[sz]ation", 2),
            (r"support[- ]splitting|information[- ]set|hull[- ]dimension|t-closure|conductor|schur[- ](filtration|product)|low-weight|matroid|weight[- ]enumerator|tuple-profile|profile[- ]partition|incidence", 2),
            (r"equivalent[- ]controls?", 2),
            (r"polynomial[- ]time (classical )?(signature|invariant|algorithm|attack|solver|filtration|reconstruction)", 2),
            (r"\b(LLL|nearest[- ]plane|gaussian elimination|RREF)\b", 1),
            (r"(match(es|ing)?|beats|outperforms) the ([\w-]+ )?quantum|no (quantum )?advantage over", 2),
            (r"norm construction|evaluator recover", 2),
        ),
    ),
    "no_signal": Mode(
        "No signal",
        "The quantum state or observable carries no usable information: labels stay uniform, bias or "
        "correlation is zero or negligible, the channel is the identity or the state maximally mixed.",
        "Compute the one-copy and few-copy bias or mutual information of the proposed observable on a "
        "small instance; a zero or exponentially small value ends the proposal.",
        (
            (r"\b(remains?|stays?|is|are|exactly|perfectly) uniform\b|uniform(ly)? (distributed|random|labels?)", 3),
            (r"zero (bias|correlation|advantage|signal|information|mutual|holevo)", 3),
            (r"(pairwise|mutually|conditionally) independen", 2),
            (r"maximally mixed|exactly (the )?identity|identity (channel|echo)|\bI/2\b", 3),
            (r"no (usable |extractable |useful )?(signal|bias|information|correlation)\b", 3),
            (r"vanish(es|ing)?\b|negligible (bias|advantage|signal|correlation|information)", 2),
            (r"\bholevo", 1),
            (r"indistinguishab", 2),
            (r"(tracks|matches) (the )?([a-z-]+ )?random controls?", 2),
            (r"exponent is unchanged|unchanged (exponent|density)", 2),
            (r"no (nonzero|nontrivial) (bias|character|invariant|multiplicit)", 2),
            (r"has no [a-z_ -]{0,20}invariants", 1),
        ),
    ),
    "readout": Mode(
        "Readout",
        "Information is present but extracting it costs too much: the needed measurement (Helstrom, PGM, "
        "collective) is not efficiently implementable or needs exponentially many copies.",
        "Name the measurement with its gate and copy count before claiming a success probability; compare "
        "it against product and local Helstrom readout.",
        (
            (r"\bread[- ]?out\b", 2),
            (r"\bmeasurements?\b", 1),
            (r"helstrom|pretty[- ]good measurement|\bPGM\b|\bPOVM", 2),
            (r"collective (measurement|readout|operation)", 2),
            (r"(exponentially|super-?polynomially) many (copies|samples|measurements|repetitions)", 3),
            (r"(?<!in)distinguishability", 1),
            (r"success (probability|rate|threshold)", 1),
            (r"sample complexity|\bcopies\b|multi-copy", 1),
        ),
    ),
    "state_prep": Mode(
        "State preparation and access",
        "The input state, source superposition or access model cannot be prepared or accessed efficiently, "
        "or covers negligible source mass.",
        "Write down the state-preparation circuit and the fraction of natural source mass it covers before "
        "analysing the readout.",
        (
            (r"state[- ]prep|prepar(e|es|ing|ation) (of )?(the |a |an |its )?([a-z-]+ )?(state|source|superposition|register)", 3),
            (r"start[- ]state", 2),
            (r"source (mass|coverage|access|model|state|superposition|unfolding)", 2),
            (r"\bQRAM\b|data loading|amplitude encoding", 3),
            (r"(coherent|physical|natural) access", 2),
            (r"input (model|access)", 1),
            (r"coset[- ]state (generation|preparation|source)", 2),
        ),
    ),
    "resource_blowup": Mode(
        "Resource blow-up",
        "The proposed route itself needs exponential time, memory, enumeration, precision or bit length.",
        "Count the route's own time, memory and precision as a function of n, including classical pre- and "
        "post-processing.",
        (
            (r"exponential(ly)? (time|cost|memory|size|depth|gates?|runtime|blow-?up|overhead|work)", 2),
            (r"exponential time exponent|super-?polynomial (time|cost|runtime)", 2),
            (r"2\^\{?\(?[a-z]|\(n!\)|\bn!|factorial", 2),
            (r"\bprecision\b|bit[- ]length|bit[- ]complexity", 2),
            (r"did not converge|out of memory|\bGB\b|resident|timed out", 2),
            (r"enumerat(es|ion|e|ing) (all|every|the full)", 1),
            (r"exponentially small (gap|amplitude|probability|overlap)", 2),
        ),
    ),
    "finite_size": Mode(
        "Finite-size evidence",
        "Evidence comes only from small or finite instances, with no scaling law or uniform statement.",
        "Fix the growing family and the asymptotic statement before running finite scans; treat finite "
        "scans as falsifiers, not evidence.",
        (
            (r"\bfinite\b", 1),
            (r"small (n|instances?|cases?|sizes?|samples?|blocks?)\b", 2),
            (r"\bn\s*(=|<=|≤)\s*\d+|\bup to n\b|ends at n", 2),
            (r"no (all-n|asymptotic|scaling|growing)", 2),
            (r"(does not|cannot|fails to) (transfer|extrapolat|scale)", 2),
            (r"extrapolat", 1),
            (r"finite (data|evidence|scans?|audits?|census|instances|eigenspectra|controls?|probes?|blocks?)", 2),
        ),
    ),
    "proof_gap": Mode(
        "Proof gap",
        "A required theorem, reduction, bound or certificate is missing or does not follow from what was shown.",
        "List the lemmas the claim needs and mark which are proved; promote nothing with an open lemma on the "
        "critical path.",
        (
            (r"\b(no|without|lacks?|lacking|missing|absent|supplies no|gives no|provides no)\b [a-z,\- ]{0,40}(theorem|proof|lemma|reduction|certificate|bound|derivation)", 3),
            (r"(is|are|was|were) not (yet )?prove[dn]|unprove[dn]|not been proved|no [a-z ]{0,30} is proved", 2),
            (r"conjectur", 1),
            (r"does not (follow|imply)|cannot be inferred", 2),
            (r"(proof|theorem|lemma)[- ](debt|gap|obligation)", 2),
            (r"remains? (unspecified|undetermined|unknown|open)", 1),
            (r"\bheuristic", 1),
        ),
    ),
    "hidden_advice": Mode(
        "Hidden advice or oracle",
        "The speedup relies on an uncharged oracle, planted secret, toy promise or artificial family rather "
        "than a natural input.",
        "State the access model and charge every oracle call; reject families whose hardness comes from a "
        "planted secret or masking.",
        (
            (r"oracle_secret_finding|toy[- ]oracle|secret-finding framing", 4),
            (r"uncharged (oracle|advice|quer)", 3),
            (r"knows? the (secret|answer|hidden)", 3),
            (r"\badvice\b|\bplanted\b", 2),
            (r"artificial (phase|family|promise)|pseudo-hard|masked", 2),
            (r"\boracles?\b", 1),
            (r"simulation cap", 1),
        ),
    ),
    "overbroad": Mode(
        "Overbroad claim",
        "The claim says more than the evidence covers: one case generalized to a family, a scoped barrier "
        "stated as universal, or a mismatched model.",
        "Write the claim's exact scope (family, model, parameters) next to the evidence's scope and cut the "
        "claim to the intersection.",
        (
            (r"over-?broad|over-?generali[sz]|over-?claim|over-?stat", 4),
            (r"universal(ly)? (no-go|claim|barrier|statement)", 3),
            (r"without a scoped|\bscoped\b", 1),
            (r"rather than the (full|general|whole|entire)", 2),
            (r"does not cover|covers only|covers exactly one", 2),
            (r"solves no (structured )?(computational )?(decision )?problem|no (structured|natural) (problem|family)", 2),
            (r"outside the [a-z\- ]{0,40}model|model mismatch", 2),
            (r"special case|single (instance|case|family|register)", 1),
        ),
    ),
}
UNCLEAR = "unclear"
UNCLEAR_DEFINITION = "The record does not say enough to tell where the proposal died."
ALL_MODES = (*MODES, UNCLEAR)
# Tie-break: specific mechanisms before generic "finite" or "missing proof".
PRIORITY = (
    "classical_competitor", "no_signal", "hidden_advice", "state_prep", "readout",
    "resource_blowup", "overbroad", "proof_gap", "finite_size",
)
FIELD_WEIGHTS = (("reason_invalid", 2.0), ("lesson", 1.0), ("claim", 0.5))

TRACKS: tuple[tuple[str, str], ...] = (
    ("toy_oracle", r"^LEGACY|oracle_secret_finding|toy[- ]oracle|NO-TOY-ORACLE"),
    ("dqi_opi", r"\bOPI\b|\bDQI\b|PRIME[- ]CHARACTER|JACOBI|MORSE|optimal polynomial intersection"),
    ("bpqm_gibbs", r"BPQM|POLAR[- ]CODE|POLAR[- ]SOURCE|GIBBS|belief propagation|successive cancellation"),
    (
        "applied_barriers",
        r"BARREN|BOSON-SAMPLING|QUANTUM-SUPREMACY|RANDOM-CIRCUIT|QUANTUM-MACHINE-LEARNING|ERROR-MITIGATION|QAOA"
        r"|CONTINUOUS-VARIABLE|SCRAMBLING|QUANTUM-CHAOS|CONTINUOUS-SPECTRUM",
    ),
    ("lattice", r"LATTICE|\bLWE\b|\bLLL\b|TERNARY|\bSIS\b|nearest-plane"),
    ("dcp", r"\bDCP\b|\bEDCP\b|\bDHS\b|DIHEDRAL|SUBSET[- ]SUM|KUPERBERG|REGEV|HIDDEN[- ]SHIFT|^HS-"),
    (
        "code_equivalence",
        r"^CODE|NEG-CODE|SELF-DUAL|GOPPA|\bBCH\b|\bREED\b|^QC-|SCHUR|CLOSURE|\bHULL\b|CANONICALI[SZ]|MATROID"
        r"|code[- ]equivalence|AFFINE-GEOMETRY-CODE|TRACE-FUNCTION|CYCLIC-CODE",
    ),
    (
        "coset_observables",
        r"COSET|^CFI|WREATH|HYPEROCTAHEDRAL|COMMUTANT|SYMMETRIC|GRAPH|WEISFEILER|\bWL\b|NONABELIAN|CARRIER|LIE-TYPE"
        r"|\bS_?\d{1,2}\b|^REP-|FOURIER|IRREP|\bPGM\b|DERANGEMENT|MULTIPLICITY|RACAH|RECOUPLING",
    ),
    ("query_lower_bound", r"QUERY|LOWER-BOUND"),
)
GENERIC_TAGS = re.compile(r"^(CODE-COSET-COLLECTIVE|PO-[A-Z-]+)$")
TRACK_TITLES = {
    "code_equivalence": "Code equivalence",
    "coset_observables": "Coset observables / nonabelian HSP",
    "dcp": "Dihedral coset / hidden shift",
    "dqi_opi": "DQI / OPI / prime characters",
    "bpqm_gibbs": "BPQM / Gibbs",
    "lattice": "Lattices",
    "applied_barriers": "Applied-QC barriers from the literature",
    "toy_oracle": "Legacy toy oracles",
    "query_lower_bound": "Query lower bounds",
    "other": "Other",
}


@dataclass
class RuleResult:
    primary: str
    scores: dict[str, float] = field(default_factory=dict)
    cues: list[str] = field(default_factory=list)


def is_templated(record: dict) -> bool:
    return record.get("reason_invalid", "").strip() == TEMPLATED_REASON


def _evidence_words(record: dict) -> str:
    evidence = record.get("evidence") or {}
    if isinstance(evidence, dict):
        keys = " ".join(str(key).replace("_", " ") for key in evidence)
        return f"{keys}. {flatten(evidence)[:600]}"
    return str(evidence)[:600]


def _fields(record: dict) -> dict[str, str]:
    if is_templated(record):
        return {"reason_invalid": _evidence_words(record), "lesson": "", "claim": ""}
    return {name: str(record.get(name, "")) for name, _ in FIELD_WEIGHTS}


def record_text(record: dict) -> str:
    fields = _fields(record)
    return " ".join(fields[name] for name, _ in FIELD_WEIGHTS if fields[name])


def rule_label(record: dict) -> RuleResult:
    fields = _fields(record)
    scores: dict[str, float] = {}
    cues: list[str] = []
    for name, mode in MODES.items():
        total = 0.0
        for pattern, weight in mode.patterns:
            for field_name, field_weight in FIELD_WEIGHTS:
                match = re.search(pattern, fields[field_name], re.I)
                if match:
                    total += weight * field_weight
                    cues.append(f"{name}:{match.group(0)}")
        if total:
            scores[name] = total
    if not scores:
        return RuleResult(UNCLEAR, {}, [])
    best = max(scores.values())
    primary = next(name for name in PRIORITY if scores.get(name) == best)
    return RuleResult(primary, scores, sorted(set(cues)))


def track_for(record: dict) -> str:
    candidates = [record.get("id", "")]
    candidates += [tag for tag in record.get("applies_to", []) if not GENERIC_TAGS.match(tag)]
    candidates.append(record.get("claim", ""))
    for text in candidates:
        for name, pattern in TRACKS:
            if re.search(pattern, text, re.I if text is candidates[-1] else 0):
                return name
    return "other"


def _group_key(record: dict) -> str:
    if is_templated(record):
        evidence = record.get("evidence") or {}
        basis = "T|" + ",".join(sorted(evidence)) if isinstance(evidence, dict) else "T|" + str(evidence)
    else:
        basis = record.get("reason_invalid", "") + "||" + record.get("lesson", "")
    normalized = re.sub(r"\d+(\.\d+)?", "#", basis).strip().lower()
    return hashlib.sha1(normalized.encode()).hexdigest()[:12]


def judge_groups(records: list[dict]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        groups[_group_key(record)].append(record["id"])
    return dict(groups)


def _judge_item(key: str, ids: list[str], record: dict) -> dict:
    evidence = record.get("evidence")
    return {
        "key": key,
        "ids": ids,
        "claim": str(record.get("claim", ""))[:600],
        "reason_invalid": str(record.get("reason_invalid", ""))[:1200],
        "lesson": str(record.get("lesson", ""))[:600],
        "evidence": json.dumps(evidence, sort_keys=True, default=str)[:700] if evidence else "",
        "templated": is_templated(record),
    }


def export_batches(
    records: list[dict], out_dir: Path, n_batches: int, sample: int | None = None, seed: int = 0
) -> list[Path]:
    """Write judge input files: one item per group of records that share their reasoning."""
    by_id = {record["id"]: record for record in records}
    groups = sorted(judge_groups(records).items())
    rng = random.Random(seed)
    rng.shuffle(groups)
    if sample is not None:
        groups = groups[:sample]
    out_dir.mkdir(parents=True, exist_ok=True)
    definitions = {name: mode.definition for name, mode in MODES.items()} | {UNCLEAR: UNCLEAR_DEFINITION}
    paths = []
    for index in range(n_batches):
        items = [_judge_item(key, ids, by_id[ids[0]]) for key, ids in groups[index::n_batches]]
        path = out_dir / f"batch_{index + 1:02d}.json"
        path.write_text(json.dumps({"batch": index + 1, "modes": definitions, "items": items}, indent=1), encoding="utf-8")
        paths.append(path)
    return paths


def _read_judge_lines(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("["):
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def import_judgements(records: list[dict], paths: list[Path], judge: str) -> dict[str, dict]:
    """Expand judge outputs (one line per group key) to per-record labels."""
    groups = judge_groups(records)
    labels: dict[str, dict] = {}
    for path in paths:
        for row in _read_judge_lines(path):
            key, primary = row.get("key"), row.get("primary")
            if key not in groups:
                raise ValueError(f"{path}: unknown group key {key!r}")
            if primary not in ALL_MODES:
                raise ValueError(f"{path}: unknown mode {primary!r} for {key}")
            secondary = [mode for mode in row.get("secondary", []) if mode in MODES and mode != primary]
            for record_id in groups[key]:
                labels[record_id] = {
                    "primary": primary,
                    "secondary": secondary,
                    "quote": str(row.get("quote", ""))[:300],
                    "judge": judge,
                }
    return labels


def agreement(rule: dict[str, str], judge: dict[str, dict]) -> dict:
    ids = sorted(set(rule) & set(judge))
    n = len(ids)
    if not n:
        return {"n": 0}
    strict = sum(rule[i] == judge[i]["primary"] for i in ids)
    lenient = sum(rule[i] in {judge[i]["primary"], *judge[i].get("secondary", [])} for i in ids)
    predicted = Counter(rule[i] for i in ids)
    actual = Counter(judge[i]["primary"] for i in ids)
    per_mode = {}
    for mode in ALL_MODES:
        if not predicted[mode] and not actual[mode]:
            continue
        hits = sum(rule[i] == mode == judge[i]["primary"] for i in ids)
        per_mode[mode] = {
            "precision": round(hits / predicted[mode], 4) if predicted[mode] else None,
            "recall": round(hits / actual[mode], 4) if actual[mode] else None,
            "support": actual[mode],
        }
    expected = sum(predicted[m] * actual[m] for m in ALL_MODES) / (n * n)
    observed = strict / n
    kappa = (observed - expected) / (1 - expected) if expected < 1 else 1.0
    confusion: dict[str, dict[str, int]] = defaultdict(dict)
    for i in ids:
        row = confusion[judge[i]["primary"]]
        row[rule[i]] = row.get(rule[i], 0) + 1
    return {
        "n": n,
        "strict": round(observed, 4),
        "lenient": round(lenient / n, 4),
        "kappa": round(kappa, 4),
        "per_mode": per_mode,
        "confusion": dict(confusion),
    }


def first_seen(root: Path, rel: str = REGISTRY) -> dict[str, str]:
    """Date each record id first appeared in the committed registry, from git history."""
    try:
        log = subprocess.run(
            ["git", "-C", str(root), "log", "--reverse", "--format=%H %cs", "--", rel],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    seen: dict[str, str] = {}
    for line in log.splitlines():
        sha, day = line.split()
        blob = subprocess.run(["git", "-C", str(root), "show", f"{sha}:{rel}"], capture_output=True, text=True)
        if blob.returncode:
            continue
        try:
            data = json.loads(blob.stdout)
        except ValueError:
            continue
        for record in data if isinstance(data, list) else []:
            if isinstance(record, dict) and record.get("id"):
                seen.setdefault(record["id"], day)
    return seen


def _count(rows: list[dict], key: str) -> dict[str, dict[str, int]]:
    table: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        table[row[key]][row["mode"]] += 1
    return {name: dict(counter) for name, counter in sorted(table.items())}


def analyse(records: list[dict], judgements: dict, seen: dict[str, str]) -> dict:
    labels = judgements.get("labels", {})
    rows = []
    for record in records:
        rule = rule_label(record)
        judged = labels.get(record["id"])
        day = seen.get(record["id"])
        rows.append({
            "id": record["id"],
            "track": track_for(record),
            "mode": judged["primary"] if judged else rule.primary,
            "secondary": judged.get("secondary", []) if judged else [],
            "label_source": "judge" if judged else "rule",
            "rule_mode": rule.primary,
            "rule_cues": rule.cues[:6],
            "quote": judged.get("quote", "") if judged else "",
            "templated": is_templated(record),
            "first_seen": day,
            "period": day[:7] if day else "uncommitted",
        })
    counts = Counter(row["mode"] for row in rows)
    rule_map = {row["id"]: row["rule_mode"] for row in rows}
    result = {
        "generated_by": "tools/audit/failure_modes.py",
        "generated_on": dt.date.today().isoformat(),
        "total": len(rows),
        "modes": {name: MODES[name].definition for name in MODES} | {UNCLEAR: UNCLEAR_DEFINITION},
        "label_sources": dict(Counter(row["label_source"] for row in rows)),
        "counts": {mode: counts[mode] for mode in ALL_MODES if counts[mode]},
        "by_track": _count(rows, "track"),
        "trend": _count(rows, "period"),
        "rule_agreement": agreement(rule_map, labels),
        "judge_meta": judgements.get("meta", {}),
        "records": rows,
    }
    second = judgements.get("second_opinion")
    if second:
        result["second_opinion"] = agreement({i: label["primary"] for i, label in second.items()}, labels)
    return result


def _pct(part: float, whole: float) -> str:
    return f"{100 * part / whole:.0f}%" if whole else "-"


def _title(mode: str) -> str:
    return MODES[mode].title if mode in MODES else "Unclear"


def render(analysis: dict) -> str:
    total = analysis["total"]
    counts = analysis["counts"]
    ordered = sorted(counts, key=lambda m: -counts[m])
    sources = analysis["label_sources"]
    lines = [
        "# Failure-Mode Meta-Analysis",
        "",
        f"Generated {analysis['generated_on']} by `tools/audit/failure_modes.py`; do not edit by hand.",
        f"Scope: the {total} records in `{REGISTRY}`. Each record gets one primary failure mode, the step at which",
        "the proposal died. Judge labels come from in-session subagents reading claim, reason and lesson;",
        "records without a judge label fall back to the keyword rules.",
        "",
        f"Labels by source: {sources.get('judge', 0)} judge, {sources.get('rule', 0)} rule.",
        "",
        "## Where proposals die",
        "",
        "| Failure mode | Records | Share | Definition |",
        "|---|---|---|---|",
    ]
    for mode in ordered:
        definition = MODES[mode].definition if mode in MODES else UNCLEAR_DEFINITION
        lines.append(f"| {_title(mode)} | {counts[mode]} | {_pct(counts[mode], total)} | {definition} |")

    lines += ["", "## By track", "", "| Track | Records | Top mode | Second | Third |", "|---|---|---|---|---|"]
    tracks = sorted(analysis["by_track"].items(), key=lambda item: -sum(item[1].values()))
    for track, modes in tracks:
        n = sum(modes.values())
        top = sorted(modes.items(), key=lambda item: -item[1])[:3]
        cells = [f"{_title(m)} {_pct(c, n)}" for m, c in top] + [""] * (3 - len(top))
        lines.append(f"| {TRACK_TITLES.get(track, track)} | {n} | " + " | ".join(cells) + " |")

    top_modes = ordered[:6]
    lines += [
        "",
        "## Over time",
        "",
        "Period is the month a record first appeared in the committed registry (from git history). The earliest",
        "period also holds every record that was already present when the registry was first committed.",
        "",
        "| Period | Records | " + " | ".join(_title(m) for m in top_modes) + " |",
        "|---|---|" + "---|" * len(top_modes),
    ]
    for period, modes in sorted(analysis["trend"].items()):
        n = sum(modes.values())
        lines.append(f"| {period} | {n} | " + " | ".join(_pct(modes.get(m, 0), n) for m in top_modes) + " |")

    lines += ["", "## How far to trust the labels", ""]
    rule = analysis["rule_agreement"]
    if rule.get("n"):
        lines += [
            f"Keyword rules against judge labels on {rule['n']} records: primary mode agrees on "
            f"{_pct(rule['strict'], 1)}, and the rule's mode is among the judge's primary or secondary modes on "
            f"{_pct(rule['lenient'], 1)} (Cohen's kappa {rule['kappa']:.2f}).",
            "",
            "| Mode | Rule precision | Rule recall | Judge support |",
            "|---|---|---|---|",
        ]
        for mode, score in sorted(rule["per_mode"].items(), key=lambda item: -item[1]["support"]):
            fmt = lambda v: "-" if v is None else f"{100 * v:.0f}%"  # noqa: E731
            lines.append(f"| {_title(mode)} | {fmt(score['precision'])} | {fmt(score['recall'])} | {score['support']} |")
        lines.append("")
        lines.append(
            "Use the rules for triage of new records only where precision is high; the judge labels are the "
            "ones the distribution above rests on."
        )
    else:
        lines.append("No judge labels yet; every label above comes from keyword rules of unmeasured accuracy.")
    second = analysis.get("second_opinion")
    if second and second.get("n"):
        lines += [
            "",
            f"A second, independent judge relabeled {second['n']} records: its primary mode matches the first "
            f"judge's on {_pct(second['strict'], 1)} and falls within the first judge's primary or secondary modes "
            f"on {_pct(second['lenient'], 1)} (kappa {second['kappa']:.2f}). That is the ceiling for any automatic labeler.",
        ]

    lines += [
        "",
        "## Pre-filters",
        "",
        "One check per failure mode, most frequent first. Running the check before a proposal is built would have",
        "stopped the records counted here at the cheapest point.",
        "",
    ]
    rows = analysis["records"]
    for mode in ordered:
        if mode not in MODES:
            continue
        examples = [row for row in rows if row["mode"] == mode and row["quote"]][:2]
        lines.append(f"**{MODES[mode].title}** ({counts[mode]} records). {MODES[mode].prefilter}")
        for row in examples:
            lines.append(f"- `{row['id']}`: \"{row['quote']}\"")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def load_records(root: Path) -> list[dict]:
    return [record for record in read_json(root / REGISTRY) if isinstance(record, dict) and record.get("id")]


def _load_judgements(root: Path) -> dict:
    path = root / JUDGEMENTS
    return read_json(path) if path.exists() else {}


def _write(root: Path, analysis: dict) -> None:
    audits = root / "research" / "audits"
    audits.mkdir(parents=True, exist_ok=True)
    (audits / "failure_modes.json").write_text(json.dumps(analysis, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (audits / "FAILURE_MODE_META_ANALYSIS.md").write_text(render(analysis), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--export-batches", type=Path, metavar="DIR", help="Write judge input batches and stop.")
    parser.add_argument("--batches", type=int, default=8)
    parser.add_argument("--sample", type=int, help="Export only this many randomly chosen groups.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--import", dest="imports", nargs="+", type=Path, help="Judge output files (JSONL).")
    parser.add_argument("--judge", default="judge", help="Name recorded with imported labels.")
    parser.add_argument("--second-opinion", action="store_true", help="Store imported labels as the second judge.")
    args = parser.parse_args(argv)

    records = load_records(args.root)
    if args.export_batches:
        paths = export_batches(records, args.export_batches, args.batches, sample=args.sample, seed=args.seed)
        print(f"wrote {len(paths)} batches covering {sum(len(json.loads(p.read_text())['items']) for p in paths)} groups")
        return 0
    judgements = _load_judgements(args.root)
    if args.imports:
        labels = import_judgements(records, args.imports, args.judge)
        slot = "second_opinion" if args.second_opinion else "labels"
        judgements.setdefault(slot, {}).update(labels)
        meta = judgements.setdefault("meta", {})
        meta[slot] = {"judge": args.judge, "records": len(judgements[slot]), "imported": dt.date.today().isoformat()}
        path = args.root / JUDGEMENTS
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(judgements, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"imported {len(labels)} record labels into {slot}")
    analysis = analyse(records, judgements, first_seen(args.root))
    _write(args.root, analysis)
    print(json.dumps({"total": analysis["total"], "counts": analysis["counts"], "rule_agreement": {
        k: v for k, v in analysis["rule_agreement"].items() if k in ("n", "strict", "lenient", "kappa")}}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

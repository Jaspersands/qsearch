"""The Tools workflow runs on any change that can turn a tests/tools test red.

Besides the tests and the tool packages they import, some tests read the real checkout: the
seeded arXiv verdicts, the referee's
committed reviews with the queue and brief pages they decide, the notes the baseline catalog
cites, the CLI with every theorem and core module, the classical package's upstream modules
and committed reports, and the paper's numbers with the reports behind them.
A change to one of those files alone must trigger .github/workflows/tools.yml; otherwise the
red appears later, on an unrelated tools change or in the nightly full run. The lists below
come from the same constants the reading tests use, so a new reference fails here until
tools.yml names it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from tests.tools import test_arxiv_watch, test_classical_package, test_paper_numbers, test_referee
from tools.arxiv_watch.verdicts import VERDICTS_FILE
from tools.brief.build_brief import OUTPUT_MD
from tools.corpus.baselines import load_catalog
from tools.preflight.preflight import MANIFEST
from tools.referee.referee import QUEUE, REVIEWS

REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "tools.yml"
CLI_AND_MODULES = "test_preflight line scan, imports and manifest; test_split_cli real CLI"


def _filters(text: str) -> dict[str, list[str]]:
    """Each event under `on:` -> its `paths` patterns (the workflow's own simple layout)."""
    events: dict[str, list[str]] = {}
    event, in_paths = None, False
    for line in text.split("\non:\n", 1)[1].splitlines():
        if line.strip().startswith("#") or not line.strip():
            continue
        if not line.startswith(" "):
            break
        if match := re.fullmatch(r"  (\w+):.*", line):
            event, in_paths = match.group(1), False
        elif re.fullmatch(r"    paths:\s*", line):
            in_paths = True
            events[event] = []
        elif in_paths and (match := re.fullmatch(r'      - "([^"]+)"\s*', line)):
            events[event].append(match.group(1))
        else:
            in_paths = False
    return events


def _regex(pattern: str) -> re.Pattern[str]:
    """A GitHub path-filter glob: `**` crosses directories, `*` and `?` do not."""
    parts = re.split(r"(\*\*|\*|\?)", pattern)
    wild = {"**": ".*", "*": "[^/]*", "?": "[^/]"}
    return re.compile("".join(wild.get(part, re.escape(part)) for part in parts))


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO).as_posix()


def _classical_reports() -> list[str]:
    """The committed reports test_package_reproduces_the_committed_report compares with, and
    the reports those modules read (prime_character_finite_readout reads the OPI report)."""
    test = test_classical_package.test_package_reproduces_the_committed_report
    [modules] = [mark.args[1] for mark in test.pytestmark if mark.name == "parametrize"]
    vendored = test_classical_package.PACKAGE / "src" / "qsearch_classical"
    pending, seen, reports = list(modules), set(), []
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        source = (vendored / f"{name}.py").read_text(encoding="utf-8")
        reports += re.findall(r'^REPORT = ROOT ?/ ?"([^"]+)"', source, re.M)
        pending += re.findall(r"^from qsearch_classical\.(\w+) import REPORT\b", source, re.M)
    return sorted(set(reports))


def _files(directory: Path) -> list[str]:
    return sorted(_rel(path) for path in directory.rglob("*") if path.is_file() and "__pycache__" not in path.parts)


def _imported_tool_packages() -> list[str]:
    """tools/<name> for every tool package a tests/tools module imports."""
    names = set()
    for test in (REPO / "tests" / "tools").glob("*.py"):
        names |= set(re.findall(r"^\s*(?:from|import) tools\.(\w+)", test.read_text(encoding="utf-8"), re.M))
    return sorted(f"tools/{name}" for name in names)


def real_checkout_reads() -> dict[str, list[str]]:
    """Each test, or group of tests, that reads the real checkout -> the files that decide it."""
    paper = test_paper_numbers.PAPER
    numbers_map = paper / "numbers_map.json"
    numbers = json.loads(numbers_map.read_text(encoding="utf-8"))["numbers"] if numbers_map.exists() else []
    sync = test_classical_package._sync()
    modules = sorted(_rel(path) for top in ("theorems", "core", "qsearch_cli") for path in (REPO / top).rglob("*.py"))
    return {
        "the Tools job (its dependencies and this workflow, which test_spend also reads)": [
            "requirements-tools.txt",
            _rel(WORKFLOW),
        ],
        "tests/tools itself": _files(REPO / "tests" / "tools"),
        "the tool packages tests/tools imports": [
            path for package in _imported_tool_packages() for path in _files(REPO / package)
        ],
        "pytest (the root conftest and the tests package)": ["conftest.py", "tests/__init__.py"],
        "test_arxiv_watch seed checks": [VERDICTS_FILE, _rel(test_arxiv_watch.REVIEW)],
        "test_referee committed reviews, the pages they decide and the note it quotes": [
            *_files(test_referee.REVIEWS_DIR),
            _rel(test_referee.STORED),
            *test_referee.PAGES,
            _rel(test_referee.POLAR_NOTE),
        ],
        CLI_AND_MODULES: ["qsearch.py", MANIFEST, *modules],
        "test_corpus_baselines note references": sorted(
            {f"research/{ref['note']}.md" for entry in load_catalog() for ref in entry["references"] if "note" in ref}
        ),
        "test_classical_package package, upstream modules and reports": [
            *_files(test_classical_package.PACKAGE),
            *(f"theorems/{name}.py" for name in (*sync.MODULES, sync.VALIDATOR_SOURCE)),
            *_classical_reports(),
        ],
        "test_paper_numbers": [
            *(_rel(paper / name) for name in ("make_numbers.py", "numbers_map.json", "numbers.tex", "main.tex")),
            *sorted({entry["source"] for entry in numbers}),
        ],
    }


def test_push_and_pull_request_filter_on_the_same_paths() -> None:
    filters = _filters(WORKFLOW.read_text(encoding="utf-8"))
    assert set(filters) == {"push", "pull_request"}
    assert filters["push"] == filters["pull_request"]
    assert len(filters["push"]) == len(set(filters["push"]))
    assert not [pattern for pattern in filters["push"] if pattern.startswith("!")]  # _regex has no negation


def test_tools_workflow_runs_on_every_file_a_test_reads_from_the_checkout() -> None:
    patterns = [_regex(pattern) for pattern in _filters(WORKFLOW.read_text(encoding="utf-8"))["pull_request"]]
    reads = real_checkout_reads()
    assert all(reads.values()) and len(reads[CLI_AND_MODULES]) > 1000
    assert len(_classical_reports()) == 6 and len(reads["test_corpus_baselines note references"]) >= 10
    assert {"tools/corpus", "tools/split_cli", "tools/brief"} <= set(_imported_tool_packages())
    missed = {}
    for reader, paths in reads.items():
        unmatched = [path for path in paths if not any(pattern.fullmatch(path) for pattern in patterns)]
        if unmatched:
            missed[reader] = unmatched[:5] + ([f"... and {len(unmatched) - 5} more"] if len(unmatched) > 5 else [])
    assert missed == {}


def test_tools_workflow_runs_when_the_referee_or_the_brief_rewrites_its_pages() -> None:
    """A routine `referee.py import` then `render`, or a brief rebuild, changes only those tools'
    outputs, which test_referee reads; a first review of a note adds a page that is not there yet."""
    patterns = [_regex(pattern) for pattern in _filters(WORKFLOW.read_text(encoding="utf-8"))["pull_request"]]
    reviews = Path(REVIEWS).parent.as_posix()
    outputs = [REVIEWS, QUEUE, OUTPUT_MD, f"{reviews}/NOTE_NOT_YET_REVIEWED.md", f"{reviews}/pass2/out/batch_01.jsonl"]
    assert set(test_referee.PAGES) <= set(outputs)
    assert [path for path in outputs if not any(pattern.fullmatch(path) for pattern in patterns)] == []


def test_heldout_step_runs_when_its_corpus_changes() -> None:
    patterns = [_regex(pattern) for pattern in _filters(WORKFLOW.read_text(encoding="utf-8"))["pull_request"]]
    # The lexical ranker fits the complete source corpus: a newly added note or a
    # quarantine move can change retrieval even without changing a held-out query.
    sources = ["research/registry/negative_results.json", "research/registry/quarantined_campaign_negatives.json",
               "research/A_NEW_NOTE.md", "research/literature/a_new_paper.json"]
    assert [path for path in sources if not any(pattern.fullmatch(path) for pattern in patterns)] == []


def test_filter_globs_follow_github_semantics() -> None:
    assert _regex("tools/corpus/**").fullmatch("tools/corpus/sources/arxiv.py")
    assert _regex("theorems/**").fullmatch("theorems/sub/module.py")
    assert _regex("theorems/polar_*.py").fullmatch("theorems/polar_source_design.py")
    assert not _regex("theorems/polar_*.py").fullmatch("theorems/sub/polar_x.py")
    assert not _regex("research/audits/**").fullmatch("research/PRIME_CHARACTER_OPI.md")
    assert not _regex("research/audits/cli_manifest.json").fullmatch("research/audits/cli_manifestXjson")
    assert _regex("qsearch.py").fullmatch("qsearch.py") and not _regex("qsearch.py").fullmatch("tools/qsearch.py")


def test_filters_are_read_from_this_workflows_layout() -> None:
    text = 'name: T\n\non:\n  push:\n    branches: [main]\n    paths:\n      - "a/**"\n      # why b\n      - "b.py"\n'
    text += '  pull_request:\n    paths:\n      - "a/**"\n\npermissions:\n  contents: read\n'
    assert _filters(text) == {"push": ["a/**", "b.py"], "pull_request": ["a/**"]}

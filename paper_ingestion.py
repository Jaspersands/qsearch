"""Local paper/LaTeX ingestion for mechanism extraction."""

from __future__ import annotations

import json
import re
import tarfile
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


PAPER_INGESTION_PATH = Path("research/paper_ingestion.json")
NO_GO_INDEX_PATH = Path("research/literature_no_go_index.json")
ARXIV_CACHE_DIR = Path("research/literature_cache")


@dataclass(frozen=True)
class TheoremLikeStatement:
    kind: str
    label: str
    statement: str
    source_locator: str = ""
    extraction_confidence: str = "low"
    raw_latex: str = ""


@dataclass(frozen=True)
class NoGoIndexEntry:
    paper_id: str
    title: str
    barrier_type: str
    evidence: str
    affected_mechanisms: list[str]
    required_action: str


@dataclass(frozen=True)
class IngestedPaperRecord:
    id: str
    source_path: str
    title: str
    mechanism: str
    problem_family: str
    reduction: str
    no_go_barrier: str
    proof_technique: str
    open_question: str
    reusable_abstraction: str
    extracted_terms: list[str]
    theorem_like_statements: list[TheoremLikeStatement]
    citation_keys: list[str]
    source_format: str = "unknown"


KEYWORD_MAP = {
    "sparse fourier transform": ("hash-based sparse Fourier localization", "sparse Fourier recovery"),
    "hashtobins": ("filtered hash-to-bins Fourier measurements", "structured-query sparse Fourier recovery"),
    "correlated fashion": ("correlated sample-pair localization", "structured-query sparse Fourier recovery"),
    "significant fourier": ("significant Fourier coefficient learning", "random-access noisy Fourier learning"),
    "hidden number": ("hidden-number Fourier/lattice decoding", "hidden number problems"),
    "random access model": ("random-sample Fourier access separation", "random-access noisy Fourier learning"),
    "learning parity with noise": ("random-example noisy character learning", "LPN/LWE-style learning problems"),
    "hidden subgroup": ("nonabelian Fourier/coset-state sampling", "hidden subgroup problems"),
    "hidden shift": ("phase-state Fourier sampling", "hidden shift problems"),
    "dihedral": ("dihedral phase-state sieving", "dihedral HSP"),
    "lattice": ("lattice reduction interface", "lattice problems"),
    "gowers": ("higher-order Fourier/Gowers structure", "higher-order harmonic analysis"),
    "code equivalence": ("hidden-permutation coset states", "code equivalence"),
    "graph isomorphism": ("hidden-permutation coset states", "graph isomorphism"),
    "qsvt": ("singular-value transformation", "block-encoded linear algebra"),
    "block encoding": ("block-encoded matrix access", "linear algebra input models"),
    "quantum walk": ("quantum walk spectral search", "walk-based algorithms"),
    "span program": ("adversary/span-program synthesis", "query complexity"),
}


def _read_tex_with_inputs(path: Path, root: Path | None = None, visited: set[Path] | None = None) -> str:
    """Expand local TeX input/include commands without escaping the paper tree."""
    resolved = path.resolve()
    source_root = (root or path.parent).resolve()
    seen = visited if visited is not None else set()
    if resolved in seen or len(seen) >= 128:
        return ""
    if resolved != source_root and source_root not in resolved.parents:
        return ""
    if not resolved.exists() or not resolved.is_file():
        return ""
    seen.add(resolved)
    raw = resolved.read_text(errors="ignore")

    def expand(match: re.Match[str]) -> str:
        name = match.group(1).strip()
        candidate = (resolved.parent / name).resolve()
        if candidate.suffix == "":
            candidate = candidate.with_suffix(".tex")
        if candidate != source_root and source_root not in candidate.parents:
            return ""
        return _read_tex_with_inputs(candidate, root=source_root, visited=seen)

    return re.sub(r"\\(?:input|include)\s*\{([^{}]+)\}", expand, raw)


def _read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".tex":
        return _read_tex_with_inputs(path)
    if suffix in {".txt", ".md"}:
        return path.read_text(errors="ignore")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception:
            return ""
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return ""


def arxiv_pdf_url(arxiv_id: str) -> str:
    normalized = arxiv_id.strip().removeprefix("arXiv:").split("v", 1)[0]
    return f"https://arxiv.org/pdf/{normalized}.pdf"


def download_arxiv_pdfs(
    arxiv_ids: Iterable[str],
    cache_dir: Path = ARXIV_CACHE_DIR,
    timeout: int = 30,
) -> list[Path]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for arxiv_id in arxiv_ids:
        normalized = arxiv_id.strip().removeprefix("arXiv:")
        if not normalized:
            continue
        output_path = cache_dir / f"{normalized.replace('/', '_')}.pdf"
        if not output_path.exists():
            with urllib.request.urlopen(arxiv_pdf_url(normalized), timeout=timeout) as response:
                output_path.write_bytes(response.read())
        downloaded.append(output_path)
    return downloaded


def arxiv_source_url(arxiv_id: str) -> str:
    normalized = arxiv_id.strip().removeprefix("arXiv:").split("v", 1)[0]
    return f"https://export.arxiv.org/e-print/{normalized}"


def download_arxiv_sources(
    arxiv_ids: Iterable[str],
    cache_dir: Path = ARXIV_CACHE_DIR,
    timeout: int = 30,
) -> list[Path]:
    """Download source archives and return one likely main TeX file per paper."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    main_files: list[Path] = []
    for arxiv_id in arxiv_ids:
        normalized = arxiv_id.strip().removeprefix("arXiv:")
        if not normalized:
            continue
        safe_id = normalized.replace("/", "_")
        source_dir = cache_dir / f"{safe_id}_source"
        source_dir.mkdir(parents=True, exist_ok=True)
        tex_files = sorted(source_dir.rglob("*.tex"))
        if not tex_files:
            archive = cache_dir / f"{safe_id}.source"
            with urllib.request.urlopen(arxiv_source_url(normalized), timeout=timeout) as response:
                archive.write_bytes(response.read())
            try:
                with tarfile.open(archive, mode="r:*") as bundle:
                    root = source_dir.resolve()
                    for member in bundle.getmembers():
                        destination = (source_dir / member.name).resolve()
                        if root not in destination.parents and destination != root:
                            raise ValueError("unsafe path in arXiv source archive")
                    bundle.extractall(source_dir)
            except tarfile.TarError:
                archive.unlink(missing_ok=True)
                continue
            tex_files = sorted(source_dir.rglob("*.tex"))
        if tex_files:
            main_files.append(max(tex_files, key=lambda path: ("\\documentclass" in path.read_text(errors="ignore"), path.stat().st_size)))
    return main_files


def _clean_latex(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", r" \1 ", text)
    text = re.sub(r"[{}$^_]", " ", text)
    return " ".join(text.split())


def _title_from_text(path: Path, raw: str, cleaned: str) -> str:
    title_match = re.search(r"\\title\{([^{}]+)\}", raw, flags=re.IGNORECASE | re.DOTALL)
    if title_match:
        return " ".join(title_match.group(1).split())
    for line in raw.splitlines():
        stripped = line.strip("# \t")
        if stripped and len(stripped) > 8:
            return stripped[:180]
    return path.stem.replace("_", " ")


def _sentence_with(text: str, keywords: Iterable[str], fallback: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for keyword in keywords:
        for sentence in sentences:
            normalized = " ".join(sentence.split())
            noisy_tex = "filecontents" in normalized.lower() or "\\tikz" in normalized.lower()
            digit_fraction = sum(character.isdigit() for character in normalized) / max(1, len(normalized))
            if keyword in normalized.lower() and len(normalized) <= 1600 and not noisy_tex and digit_fraction < 0.18:
                return normalized[:500]
    return fallback


def extract_citation_keys(raw: str) -> list[str]:
    keys: set[str] = set()
    for cite_body in re.findall(r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])*\{([^{}]+)\}", raw):
        for key in cite_body.split(","):
            cleaned = key.strip()
            if cleaned:
                keys.add(cleaned)
    for arxiv_id in re.findall(r"arXiv:\s*([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", raw, flags=re.IGNORECASE):
        keys.add(f"arxiv:{arxiv_id}")
    for legacy_id in re.findall(r"(?:quant-ph|cs|math|cond-mat)/[0-9]{7}", raw, flags=re.IGNORECASE):
        keys.add(f"arxiv:{legacy_id}")
    return sorted(keys)


def extract_theorem_like_statements(raw: str, cleaned: str) -> list[TheoremLikeStatement]:
    statements: list[TheoremLikeStatement] = []
    environment_pattern = re.compile(
        r"\\begin\{(theorem|lemma|proposition|corollary|conjecture|definition|problem)\}"
        r"(.*?)\\end\{\1\}",
        flags=re.IGNORECASE | re.DOTALL,
    )
    for index, match in enumerate(environment_pattern.finditer(raw), start=1):
        kind = match.group(1).lower()
        raw_body = match.group(2).strip()
        label_match = re.search(r"\\label\{([^{}]+)\}", raw_body)
        body = re.sub(r"\\label\{[^{}]+\}", "", raw_body)
        body = " ".join(body.split())
        if body:
            label = label_match.group(1) if label_match else f"{kind}-{index}"
            line = raw.count("\n", 0, match.start()) + 1
            statements.append(
                TheoremLikeStatement(
                    kind=kind,
                    label=label,
                    statement=body[:2000],
                    source_locator=f"line {line}; \\begin{{{kind}}}",
                    extraction_confidence="high",
                    raw_latex=raw_body[:3000],
                )
            )

    sentence_pattern = re.compile(
        r"(?P<kind>Theorem|Lemma|Proposition|Corollary|Conjecture|Open problem|Lower bound|No-go result)"
        r"(?P<label>\s+[0-9A-Za-z_.-]+)?[:.]\s+(?P<body>[^.!?]*(?:[.!?]))",
        flags=re.IGNORECASE,
    )
    for match in sentence_pattern.finditer(cleaned):
        body = match.group("body").strip()
        if body:
            statements.append(
                TheoremLikeStatement(
                    kind=match.group("kind").lower().replace(" ", "-"),
                    label=(match.group("label") or "").strip() or f"statement-{len(statements) + 1}",
                    statement=body[:800],
                    source_locator="flattened-text sentence match",
                    extraction_confidence="low",
                )
            )
    seen = set()
    unique = []
    for statement in statements:
        key = (statement.kind, statement.statement)
        if key in seen:
            continue
        seen.add(key)
        unique.append(statement)
    return unique[:20]


def extract_paper_record(path: Path) -> IngestedPaperRecord | None:
    raw = _read_text(path)
    if not raw.strip():
        return None
    cleaned = _clean_latex(raw)
    lower = cleaned.lower()
    terms = [keyword for keyword in KEYWORD_MAP if keyword in lower]
    if terms:
        mechanisms = sorted({KEYWORD_MAP[term][0] for term in terms})
        families = sorted({KEYWORD_MAP[term][1] for term in terms})
    else:
        mechanisms = ["manual review required"]
        families = ["unclassified quantum algorithms"]

    barrier_keywords = [
        "do not expect",
        "cannot",
        "impossible",
        "hardness",
        "no-go",
        "barrier",
        "lower bound",
        "limitations",
        "dequant",
        "random access model",
    ]
    proof_keywords = ["proof", "lemma", "theorem", "reduction", "adversary", "representation", "hashing", "fourier"]
    open_keywords = ["still open", "open problem", "conjecture", "future work", "question", "we leave"]
    abstraction_keywords = [
        "significant fourier",
        "hashtobins",
        "correlated fashion",
        "random access model",
        "framework",
        "primitive",
        "oracle",
        "coset state",
        "block encoding",
        "phase state",
        "span program",
    ]
    theorem_like = extract_theorem_like_statements(raw, cleaned)
    citation_keys = extract_citation_keys(raw)

    return IngestedPaperRecord(
        id=f"LOCAL-{path.stem.upper().replace('-', '_')}",
        source_path=str(path),
        title=_title_from_text(path, raw, cleaned),
        mechanism="; ".join(mechanisms),
        problem_family="; ".join(families),
        reduction=_sentence_with(cleaned, ["reduction", "reduces", "reduce"], "No explicit reduction sentence extracted."),
        no_go_barrier=_sentence_with(cleaned, barrier_keywords, "No no-go or lower-bound barrier sentence extracted."),
        proof_technique=_sentence_with(cleaned, proof_keywords, "No proof-technique sentence extracted."),
        open_question=_sentence_with(cleaned, open_keywords, "No open-question sentence extracted."),
        reusable_abstraction=_sentence_with(cleaned, abstraction_keywords, "No reusable abstraction sentence extracted."),
        extracted_terms=terms,
        theorem_like_statements=theorem_like,
        citation_keys=citation_keys,
        source_format=path.suffix.lower().removeprefix("."),
    )


def ingest_papers(paths: Iterable[Path]) -> list[IngestedPaperRecord]:
    records: list[IngestedPaperRecord] = []
    for input_path in paths:
        path = input_path.expanduser()
        candidates = sorted(p for p in path.rglob("*") if p.suffix.lower() in {".tex", ".txt", ".md", ".pdf"}) if path.is_dir() else [path]
        for candidate in candidates:
            record = extract_paper_record(candidate)
            if record:
                records.append(record)
    records.sort(key=lambda item: item.id)
    return records


def build_no_go_index(records: list[IngestedPaperRecord]) -> list[NoGoIndexEntry]:
    entries: list[NoGoIndexEntry] = []
    for record in records:
        evidence_items = [record.no_go_barrier]
        evidence_items.extend(
            statement.statement
            for statement in record.theorem_like_statements
            if statement.kind in {"lower-bound", "no-go-result"} or any(
                token in statement.statement.lower() for token in ["no-go", "lower bound", "impossible", "cannot", "barrier"]
            )
        )
        for index, evidence in enumerate(evidence_items):
            lower = evidence.lower()
            if not any(
                token in lower
                for token in [
                    "no-go",
                    "barrier",
                    "lower bound",
                    "impossible",
                    "hardness",
                    "dequant",
                    "cannot",
                    "do not expect",
                    "limitation",
                ]
            ):
                continue
            if "fourier" in lower and ("symmetric" in lower or "nonabelian" in lower):
                barrier_type = "nonabelian-fourier-sampling"
                affected = ["coset-state", "nonabelian-hsp", "graph-isomorphism", "code-equivalence"]
            elif "random access" in lower and ("fourier" in lower or "lpn" in lower or "lwe" in lower):
                barrier_type = "random-access-fourier-separation"
                affected = ["random-label-dcp", "significant-fourier-learning", "hidden-number", "query-model"]
            elif "full-table" in lower or "dequant" in lower or "classical" in lower:
                barrier_type = "classical-dequantization"
                affected = ["hidden-shift", "phase-state", "query-model"]
            elif "lower bound" in lower:
                barrier_type = "query-or-complexity-lower-bound"
                affected = record.extracted_terms or ["unclassified"]
            else:
                barrier_type = "general-no-go-or-hardness"
                affected = record.extracted_terms or ["unclassified"]
            entries.append(
                NoGoIndexEntry(
                    paper_id=record.id,
                    title=record.title,
                    barrier_type=barrier_type,
                    evidence=evidence[:800],
                    affected_mechanisms=affected,
                    required_action="Map any candidate using this mechanism to the barrier and state how it bypasses or respects it.",
                )
            )
    unique: dict[tuple[str, str, str], NoGoIndexEntry] = {}
    for entry in entries:
        unique[(entry.paper_id, entry.barrier_type, entry.evidence)] = entry
    return sorted(unique.values(), key=lambda item: (item.barrier_type, item.paper_id, item.evidence))


def write_paper_ingestion(
    paths: Iterable[Path],
    output_path: Path = PAPER_INGESTION_PATH,
    no_go_index_path: Path = NO_GO_INDEX_PATH,
) -> list[dict]:
    paper_records = ingest_papers(paths)
    records = [asdict(record) for record in paper_records]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, indent=2, sort_keys=True))
    no_go_index = [asdict(entry) for entry in build_no_go_index(paper_records)]
    no_go_index_path.parent.mkdir(parents=True, exist_ok=True)
    no_go_index_path.write_text(json.dumps(no_go_index, indent=2, sort_keys=True))
    return records


def write_paper_ingestion_with_arxiv(
    paths: Iterable[Path],
    arxiv_ids: Iterable[str],
    output_path: Path = PAPER_INGESTION_PATH,
    no_go_index_path: Path = NO_GO_INDEX_PATH,
) -> list[dict]:
    arxiv_ids = list(arxiv_ids)
    sources = download_arxiv_sources(arxiv_ids)
    source_ids = {path.parent.name.removesuffix("_source") for path in sources}
    pdf_fallbacks = [
        path
        for path in download_arxiv_pdfs(arxiv_ids)
        if path.stem not in source_ids
    ]
    return write_paper_ingestion([*paths, *sources, *pdf_fallbacks], output_path=output_path, no_go_index_path=no_go_index_path)

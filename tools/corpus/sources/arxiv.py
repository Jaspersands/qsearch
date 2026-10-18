"""Minimal arXiv API client: Atom parsing, polite pacing and an optional response cache."""

from __future__ import annotations

import hashlib
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
USER_AGENT = "qsearch-tools/0.1 (research tooling; https://github.com/Jaspersands/qsearch)"


@dataclass(frozen=True)
class Paper:
    arxiv_id: str
    version: str
    title: str
    abstract: str
    authors: list[str]
    published: str  # YYYY-MM-DD
    updated: str
    categories: list[str]
    url: str


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def split_id(raw: str) -> tuple[str, str]:
    """'http://arxiv.org/abs/2609.01234v2' -> ('2609.01234', 'v2'); old-style ids keep their archive."""
    tail = raw.split("/abs/", 1)[-1]
    match = re.match(r"(.+?)(v\d+)?$", tail)
    assert match is not None
    return match.group(1), match.group(2) or ""


def parse_atom(body: bytes) -> list[Paper]:
    root = ET.fromstring(body)
    papers = []
    for entry in root.findall(f"{ATOM}entry"):
        raw_id = entry.findtext(f"{ATOM}id", default="")
        if "/abs/" not in raw_id:
            continue  # arXiv returns an error entry for malformed queries
        arxiv_id, version = split_id(raw_id)
        categories = [c.get("term", "") for c in entry.findall(f"{ATOM}category")]
        primary = entry.find(f"{ARXIV}primary_category")
        if primary is not None and primary.get("term") in categories:
            categories.remove(primary.get("term"))
            categories.insert(0, primary.get("term", ""))
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                version=version,
                title=_clean(entry.findtext(f"{ATOM}title")),
                abstract=_clean(entry.findtext(f"{ATOM}summary")),
                authors=[_clean(a.findtext(f"{ATOM}name")) for a in entry.findall(f"{ATOM}author")],
                published=(entry.findtext(f"{ATOM}published") or "")[:10],
                updated=(entry.findtext(f"{ATOM}updated") or "")[:10],
                categories=categories,
                url=f"https://arxiv.org/abs/{arxiv_id}",
            )
        )
    return papers


def query_url(search_query: str, max_results: int = 50, start: int = 0) -> str:
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{API}?{urllib.parse.urlencode(params)}"


class Client:
    """arXiv asks for at most one request every three seconds; `delay` enforces that."""

    def __init__(
        self,
        opener: Callable | None = urllib.request.urlopen,
        sleep: Callable[[float], None] = time.sleep,
        delay: float = 3.0,
        cache_dir: Path | None = None,
        timeout: int = 30,
    ) -> None:
        self.opener = opener
        self.sleep = sleep
        self.delay = delay
        self.cache_dir = cache_dir
        self.timeout = timeout
        self._called = False

    def _fetch(self, url: str) -> bytes:
        cached = None
        if self.cache_dir is not None:
            cached = self.cache_dir / f"{hashlib.sha1(url.encode()).hexdigest()}.xml"
            if cached.exists():
                return cached.read_bytes()
        if self.opener is None:
            raise RuntimeError(f"no network opener and no cached response for {url}")
        if self._called:
            self.sleep(self.delay)
        self._called = True
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with self.opener(request, timeout=self.timeout) as response:
            body = response.read()
        if cached is not None:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(body)
        return body

    def search(self, search_query: str, max_results: int = 50, start: int = 0) -> list[Paper]:
        return parse_atom(self._fetch(query_url(search_query, max_results, start)))

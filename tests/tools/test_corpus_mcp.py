from __future__ import annotations

import json
from pathlib import Path

import anyio

from tools.corpus.mcp_server import create_server


def _call(server, name: str, arguments: dict) -> dict:
    async def go():
        return await server.call_tool(name, arguments)

    result = anyio.run(go)
    # FastMCP returns (content blocks, structured result) for dict-returning tools.
    if isinstance(result, tuple):
        return result[1].get("result", result[1])
    return json.loads(result[0].text)


def test_server_lists_its_tools(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")

    async def names():
        return sorted(tool.name for tool in await server.list_tools())

    assert anyio.run(names) == [
        "been_tried",
        "check_duplicate_negative",
        "classical_baselines",
        "get_doc",
        "screen_dqi_candidate",
        "search_corpus",
    ]


def test_been_tried_tool_returns_grouped_hits(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "been_tried", {"idea": "quadratic extension norm for mixed coset OPI", "k": 2})
    killed = payload["groups"]["Killed before"]
    assert killed[0]["doc_id"] == "negative:NEG-OPI-MIXED-COSET-HARDNESS"
    assert killed[0]["location"].startswith("research/registry/negative_results.json:")


def test_search_and_get_tools(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")
    hits = _call(server, "search_corpus", {"query": "exterior characters", "kinds": ["note"], "k": 3})["hits"]
    assert hits and {hit["kind"] for hit in hits} == {"note"}
    doc = _call(server, "get_doc", {"doc_id": hits[0]["doc_id"]})
    assert doc["doc_id"] == hits[0]["doc_id"] and doc["text"]
    missing = _call(server, "get_doc", {"doc_id": "negative:NOPE"})
    assert missing["error"].startswith("unknown doc_id")


def test_screen_dqi_candidate_tool(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off")
    examples = Path(__file__).resolve().parents[2] / "tools" / "dqi_screen" / "examples"
    params = json.loads((examples / "mpi_signed_cosine.json").read_text())
    payload = _call(server, "screen_dqi_candidate", {"params": params})
    assert payload["verdict"] == "viable"
    assert {check["rule"] for check in payload["checks"]} >= {"R1", "reach", "R2"}
    payload = _call(server, "screen_dqi_candidate", {"params": {"objective": "count"}})
    assert payload["error"]


def test_server_sees_files_added_after_start(fake_repo: Path) -> None:
    server = create_server(fake_repo, dense="off", refresh_seconds=0)
    _call(server, "search_corpus", {"query": "warmup"})
    (fake_repo / "theorems" / "wombat_sieve.py").write_text('"""Wombat sieve for hidden shifts."""\n')
    hits = _call(server, "search_corpus", {"query": "wombat sieve hidden shift", "k": 1})["hits"]
    assert hits[0]["doc_id"] == "theorem:wombat_sieve"


def test_stdio_round_trip_like_an_agent_client(fake_repo: Path) -> None:
    import sys

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    script = Path(__file__).resolve().parents[2] / "tools" / "corpus" / "mcp_server.py"
    params = StdioServerParameters(command=sys.executable, args=[str(script), "--root", str(fake_repo), "--dense", "off"])

    async def go():
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("been_tried", {"idea": "Helstrom product readout", "k": 1})
                assert not result.isError
                if result.structuredContent:
                    return result.structuredContent.get("result", result.structuredContent)
                return json.loads(result.content[0].text)

    payload = anyio.run(go)
    assert payload["groups"]["Killed before"][0]["doc_id"] == "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"


def test_malformed_record_neither_breaks_the_server_nor_locks_out_other_agents(fake_repo: Path) -> None:
    from tests.tools.conftest import NEGATIVES, QUARANTINED
    from tools.corpus.api import Corpus

    server = create_server(fake_repo, dense="off", refresh_seconds=0)
    _call(server, "search_corpus", {"query": "warmup"})
    registry = fake_repo / "research" / "registry"
    kangaroo = {"id": "NEG-NEW-ONE", "claim": "Kangaroo sieve", "reason_invalid": "x", "lesson": "y", "applies_to": ["DCP"]}
    (registry / "negative_results.json").write_text(json.dumps(NEGATIVES + [kangaroo], indent=2))
    bad = QUARANTINED + [{"id": "NEG-Q2", "original_record": "see NEG-NEW-ONE", "status": "QUARANTINED"}]
    (registry / "quarantined_campaign_negatives.json").write_text(json.dumps(bad, indent=2))
    hits = _call(server, "search_corpus", {"query": "kangaroo sieve", "kinds": ["negative"]})["hits"]
    assert hits[0]["doc_id"] == "negative:NEG-NEW-ONE"
    other = Corpus(fake_repo)
    other.store.conn.execute("PRAGMA busy_timeout = 500")
    (fake_repo / "theorems" / "numbat.py").write_text('"""Numbat sieve."""\n')
    other.refresh()  # another agent can still write the index
    assert other.search("numbat sieve")[0].doc_id == "theorem:numbat"


def test_auto_dense_waits_for_full_vector_coverage(fake_repo: Path) -> None:
    import numpy as np

    from tools.corpus.api import Corpus

    calls: list[int] = []

    def embed(texts):
        calls.append(len(texts))
        return np.ones((len(texts), 3), dtype=np.float32) / np.sqrt(3)

    Corpus(fake_repo, embedder=embed).refresh(dense=True)  # someone ran `build --dense` once
    del calls[:]
    server = create_server(fake_repo, dense="auto", refresh_seconds=0, embedder=embed)
    _call(server, "search_corpus", {"query": "Helstrom"})
    assert calls == [1]  # coverage is complete, so the query was embedded
    (fake_repo / "theorems" / "wombat_sieve.py").write_text('"""Wombat sieve for hidden shifts."""\n')
    hits = _call(server, "search_corpus", {"query": "wombat sieve hidden shift", "k": 1})["hits"]
    assert hits[0]["doc_id"] == "theorem:wombat_sieve"
    assert calls == [1]  # the new doc has no vector, so auto mode stayed lexical
    on = create_server(fake_repo, dense="on", refresh_seconds=0, embedder=embed)
    _call(on, "search_corpus", {"query": "wombat"})
    assert calls == [1, 1, 1]  # "on" embeds the one missing doc, then the query

from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

from tools.referee import extract as X


FIXTURE_NOTE = textwrap.dedent(
    """\
    # Fixture Radial Bound

    2026-10-18. LOCAL APPLICATION REVIEW PENDING. No speedup is claimed. Not a new algorithm.
    Producer: `python theorems/fixture_radial.py --write --seed 3`.
    Output: `research/classical_baselines/fixture_radial.json`.

    ## Question And Result

    Does the radial bound hold for every saved input? It holds for all twelve
    saved inputs, with margin at least 0.031.

    ## 1. Lemma: Radial Bound

    For every radius r at least 1 the weight enumerator is bounded by the
    radial sum, by the triangle inequality applied term by term.

    ## Decisive Controls

    The Prange completion baseline reaches 0.654 on the same inputs.

    ## Try To Kill It

    We searched 10000 random inputs for a counterexample to the radial bound
    and found none.

    ## Decision And Next

    Keep the bound; next test the 32-radius inputs.
    """
)


def _write(root: Path, stem: str, text: str | bytes) -> Path:
    path = root / "research" / f"{stem}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")
    return path


def test_parse_note_reads_every_field(tmp_path: Path) -> None:
    path = _write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE)
    packet = X.parse_note(path)
    assert (packet.stem, packet.status, packet.date) == ("FIXTURE_NOTE", "review-pending", "2026-10-18")
    assert packet.path == "research/FIXTURE_NOTE.md"
    assert packet.title == "Fixture Radial Bound"
    assert packet.producer == {
        "command": "python theorems/fixture_radial.py --write --seed 3",
        "script": "theorems/fixture_radial.py",
        "flags": "--write --seed 3",
        "artifact": "research/classical_baselines/fixture_radial.json",
    }
    assert "No speedup is claimed." in packet.not_claimed
    assert "Not a new algorithm." in packet.not_claimed
    assert "##" not in packet.result and "twelve" in packet.result
    assert [d["heading"] for d in packet.derivations] == ["1. Lemma: Radial Bound"]
    assert "triangle inequality" in packet.derivations[0]["text"]
    assert [c["heading"] for c in packet.controls] == ["Decisive Controls"]
    assert packet.self_check is not None and "counterexample" in packet.self_check
    assert packet.decision is not None and "32-radius" in packet.decision
    assert packet.content_sha == hashlib.sha256(path.read_bytes()).hexdigest()
    assert isinstance(packet.flags, list)
    assert X.to_dict(packet)["stem"] == "FIXTURE_NOTE"


def test_parse_note_falls_back_to_the_first_section_for_result(tmp_path: Path) -> None:
    text = textwrap.dedent(
        """\
        # Fallback

        2026-10-12. Review pending.

        ## Setup And Inputs

        The saved inputs are the N127 instances.

        ## Discussion

        Later text.
        """
    )
    packet = X.parse_note(_write(tmp_path, "FALLBACK", text))
    assert "N127 instances" in packet.result
    assert "Later text" not in packet.result
    assert packet.derivations == [] and packet.controls == []
    assert packet.self_check is None and packet.decision is None
    assert packet.producer is None


def test_parse_note_reads_producer_from_the_reproduce_block_at_the_end(tmp_path: Path) -> None:
    (tmp_path / "theorems").mkdir()
    (tmp_path / "theorems" / "end_block.py").write_text(
        'ROOT = None\nREPORT = ROOT / "research/classical_baselines/end_block.json"\n', encoding="utf-8"
    )
    text = textwrap.dedent(
        """\
        # End Block

        2026-10-14. REVIEW PENDING.

        ## Claim

        A claim with no artifact path in the text.

        ## Reproduce

        ```text
        python theorems/end_block.py --write
        ```
        """
    )
    packet = X.parse_note(_write(tmp_path, "END_BLOCK", text))
    assert packet.producer == {
        "command": "python theorems/end_block.py --write",
        "script": "theorems/end_block.py",
        "flags": "--write",
        "artifact": "research/classical_baselines/end_block.json",
    }


def test_parse_note_keeps_fenced_headings_inside_their_section(tmp_path: Path) -> None:
    text = textwrap.dedent(
        """\
        # Fenced

        2026-10-15. Review pending.

        ## 2. Derivation

        The exact table is

        ```text
        ## not a heading
        k = 3
        ```

        and the bound follows.

        ## Decision

        Stop here.
        """
    )
    packet = X.parse_note(_write(tmp_path, "FENCED", text))
    assert [d["heading"] for d in packet.derivations] == ["2. Derivation"]
    body = packet.derivations[0]["text"]
    assert "## not a heading" in body and "the bound follows" in body
    assert packet.decision == "Stop here."


def test_parse_note_reads_replacement_bytes_and_long_producer_flags(tmp_path: Path) -> None:
    raw = (
        b"# Bytes \xff Note\n\n2026-10-16. REVIEW PENDING. No hardness claim.\n\n"
        b"## Result\n\nThe sampler matches the target law \xfe within 0.01.\n\n## Execute\n\n"
        b"```\npython theorems/polar_source_design.py --length 32768 --grid 256 --power 3 --write\n```\n"
    )
    path = _write(tmp_path, "BYTES_NOTE", raw)
    packet = X.parse_note(path)
    assert packet.content_sha == hashlib.sha256(raw).hexdigest()
    assert "�" in packet.title
    assert packet.producer is not None
    assert packet.producer["flags"] == "--length 32768 --grid 256 --power 3 --write"
    assert packet.producer["artifact"] is None
    assert "within 0.01" in packet.result


def _with_artifact(root: Path, artifact: str, payload: str) -> X.NotePacket:
    path = root / artifact
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    text = FIXTURE_NOTE.replace("research/classical_baselines/fixture_radial.json", artifact.removeprefix("research/"))
    return X.parse_note(_write(root, "FIXTURE_NOTE", text))


def test_artifact_excerpt_lists_keys_and_numeric_leaves(tmp_path: Path) -> None:
    data = {"status": "ok", "mean": 0.9028, "flag": True, "tail": {"k110": 0.3145, "runs": [1, 2, 3, 4, 5, 6, 7]}}
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", json.dumps(data))
    assert packet.producer["artifact"] == "classical_baselines/fixture_radial.json"
    excerpt = X.artifact_excerpt(tmp_path, packet)
    assert excerpt is not None
    assert excerpt.startswith("keys: flag, mean, status, tail")
    assert "mean = 0.9028" in excerpt and "tail.k110 = 0.3145" in excerpt
    assert not any(line.startswith("flag") for line in excerpt.splitlines()[1:])  # booleans are not leaves
    assert "tail.runs[4] = 5" in excerpt and "tail.runs[5]" not in excerpt and "(+2)" in excerpt
    assert len(excerpt) <= 4000
    big = {f"key{i:04d}": i / 7 for i in range(2000)}
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", json.dumps(big))
    short = X.artifact_excerpt(tmp_path, packet, max_chars=500)
    assert short is not None and len(short) <= 500 and short.endswith("[truncated]")


def test_artifact_excerpt_is_none_when_missing_or_invalid(tmp_path: Path) -> None:
    packet = X.parse_note(_write(tmp_path, "FIXTURE_NOTE", FIXTURE_NOTE))
    assert X.artifact_excerpt(tmp_path, packet) is None
    packet = _with_artifact(tmp_path, "research/classical_baselines/fixture_radial.json", "{not json")
    assert X.artifact_excerpt(tmp_path, packet) is None
    fallback = X.parse_note(_write(tmp_path, "FALLBACK", "# F\n\n2026-10-01. Review pending.\n\n## Result\n\nNo producer.\n"))
    assert fallback.producer is None and X.artifact_excerpt(tmp_path, fallback) is None
    assert X._resolve_artifact(tmp_path, "classical_baselines/fixture_radial.json") == (
        tmp_path / "research/classical_baselines/fixture_radial.json"
    )
    assert X._resolve_artifact(tmp_path, "classical_baselines/absent.json") is None

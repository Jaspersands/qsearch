"""Offline tests: no credentials or Anthropic services are accessed."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from tools import claude_research_agent as runner


@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.setattr(runner, "REPO_ROOT", root)

    def forbidden():
        pytest.fail("Unexpected live client or credential access")

    monkeypatch.setattr(runner, "make_client", forbidden)
    monkeypatch.setattr(runner, "load_codex_env", forbidden)
    return root


def read_result(bundle):
    return json.loads((bundle / "result.json").read_text())


class FakeStream:
    def __init__(self, text="A checked deduction.\n", stop="end_turn", failure=None):
        self.text = text
        self.failure = failure
        self.message = NS(
            content=[NS(type="text", text=text)], stop_reason=stop,
            usage=NS(input_tokens=900, output_tokens=200, cache_creation_input_tokens=0,
                     cache_read_input_tokens=0),
        )
        self.current_message_snapshot = self.message

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    @property
    def text_stream(self):
        yield self.text
        if self.failure:
            raise self.failure

    def get_final_message(self):
        return self.message


class FakeClient:
    def __init__(self, count=1000, stream=None, count_failure=None):
        self.messages = self
        self.count = count
        self.response = stream or FakeStream()
        self.count_failure = count_failure
        self.count_calls = []
        self.stream_calls = []
        self.closed = False

    def count_tokens(self, **kwargs):
        self.count_calls.append(kwargs)
        if self.count_failure:
            raise self.count_failure
        return NS(input_tokens=self.count)

    def stream(self, **kwargs):
        self.stream_calls.append(kwargs)
        return self.response

    def create(self, **kwargs):
        pytest.fail("Generation must use streaming")

    def close(self):
        self.closed = True


def test_dry_run_is_offline_with_snapshots_and_hashes(repo):
    (repo / "prompt.md").write_text("Review the proof.")
    evidence = b"A stated hypothesis.\n"
    (repo / "note.md").write_bytes(evidence)
    (repo / "second.txt").write_text("Another source.")
    args = ["--prompt-file", "prompt.md", "--context", "note.md", "--context", "second.txt",
            "--effort", "max", "--role", "constructive", "--dry-run"]
    assert runner.main(args) == 0
    assert runner.main(args) == 0
    bundles = list((repo / "research/audits/claude_runs").iterdir())
    assert len(bundles) == 2
    for bundle in bundles:
        result = read_result(bundle)
        request = json.loads((bundle / "request.json").read_text())
        assert result["status"] == "dry_run"
        assert result["billing_status"] == "not_started"
        assert result["budget_check"] == "not_performed"
        assert result["context"][0]["sha256"] == hashlib.sha256(evidence).hexdigest()
        assert (bundle / result["context"][0]["snapshot"]).read_bytes() == evidence
        assert len(result["context"]) == 2
        assert request["model"] == "claude-opus-5-5"
        assert request["max_tokens"] == 32768
        assert request["thinking"] == {"type": "adaptive"}
        assert request["output_config"] == {"effort": "max"}
        assert "tools" not in request
        assert (bundle / "response.md").read_text() == ""


@pytest.mark.parametrize("count,allowance", [(1000, 1256), (20001, 20402)])
def test_budget_refusal_never_starts_generation(repo, monkeypatch, count, allowance):
    client = FakeClient(count=count)
    monkeypatch.setattr(runner, "make_client", lambda: client)
    bundle = repo / "refused"
    assert runner.main(["Question", "--max-budget-usd", "0.001", "--output-dir", str(bundle)]) == 2
    result = read_result(bundle)
    assert result["status"] == "budget_refused"
    assert result["input_token_allowance"] == allowance
    assert result["preflight_cost_estimate_usd"] == pytest.approx((4 * allowance + 20 * 32768) / 1_000_000)
    assert len(client.count_calls) == 1
    assert not client.stream_calls
    assert client.closed
    assert result["billing_status"] == "not_started"


def test_success_uses_count_then_stream_and_records_actual_usage(repo, monkeypatch, capsys):
    client = FakeClient()
    monkeypatch.setattr(runner, "make_client", lambda: client)
    bundle = repo / "success"
    assert runner.main(["UNPRINTED PROMPT", "--effort", "high", "--output-dir", str(bundle)]) == 0
    result = read_result(bundle)
    assert result["status"] == "completed"
    assert result["usage"]["output_tokens"] == 200
    assert result["usage_cost_estimate_usd"] == pytest.approx(0.0076)
    assert (bundle / "response.md").read_text() == client.response.text
    assert len(client.stream_calls) == len(client.count_calls) == 1
    assert "max_tokens" not in client.count_calls[0]
    assert client.stream_calls[0]["max_tokens"] == 32768
    assert client.count_calls[0]["thinking"] == {"type": "adaptive"}
    assert "UNPRINTED PROMPT" not in capsys.readouterr().out


@pytest.mark.parametrize("stop,text,status", [
    ("max_tokens", "Partial deduction", "truncated"),
    ("max_tokens", "", "truncated"),
    ("end_turn", "", "empty_response"),
    ("pause_turn", "Unfinished", "incomplete"),
])
def test_incomplete_responses_are_not_success(repo, monkeypatch, stop, text, status):
    client = FakeClient(stream=FakeStream(text=text, stop=stop))
    monkeypatch.setattr(runner, "make_client", lambda: client)
    bundle = repo / "incomplete"
    assert runner.main(["Question", "--output-dir", str(bundle)]) == 1
    result = read_result(bundle)
    assert result["status"] == status
    assert result["stop_reason"] == stop
    assert result["usage"]["output_tokens"] == 200
    assert (bundle / "response.md").read_text() == text


@pytest.mark.parametrize("failure,code,status", [
    (RuntimeError("PRIVATE SERVER BODY"), 1, "failed"),
    (KeyboardInterrupt(), 130, "interrupted"),
])
def test_partial_stream_failure_is_saved_without_retry(repo, monkeypatch, capsys, failure, code, status):
    client = FakeClient(stream=FakeStream(text="Partial evidence", failure=failure))
    monkeypatch.setattr(runner, "make_client", lambda: client)
    bundle = repo / "failed"
    assert runner.main(["Question", "--output-dir", str(bundle)]) == code
    result = read_result(bundle)
    assert result["status"] == status
    assert result["billing_status"] == "unknown"
    assert result["usage_is_partial"] is True
    assert (bundle / "response.md").read_text() == "Partial evidence"
    assert len(client.stream_calls) == 1
    assert "PRIVATE SERVER BODY" not in (bundle / "result.json").read_text()
    captured = capsys.readouterr()
    assert "PRIVATE SERVER BODY" not in captured.err + captured.out


def test_count_error_has_no_paid_generation_and_sanitized_status(repo, monkeypatch):
    error = RuntimeError("PRIVATE SERVER BODY")
    error.status_code = 429
    client = FakeClient(count_failure=error)
    monkeypatch.setattr(runner, "make_client", lambda: client)
    bundle = repo / "count_error"
    assert runner.main(["Question", "--output-dir", str(bundle)]) == 1
    result = read_result(bundle)
    assert result["failure_stage"] == "count_tokens"
    assert result["http_status"] == 429
    assert result["billing_status"] == "not_started"
    assert not client.stream_calls


@pytest.mark.parametrize("kind", ["outside", "secret", "symlink", "symlink_directory", "binary"])
def test_context_rejects_unsafe_paths_before_client_or_bundle(repo, kind):
    outside = repo.parent / "outside.md"
    outside.write_text("External text")
    if kind == "outside":
        path = outside
    elif kind == "secret":
        path = repo / ".env"
        # No secret is created or read, including in this test.
    elif kind == "symlink":
        path = repo / "linked.md"
        path.symlink_to(outside)
    elif kind == "symlink_directory":
        (repo / "linked").symlink_to(repo.parent, target_is_directory=True)
        path = repo / "linked/outside.md"
    else:
        path = repo / "binary.dat"
        path.write_bytes(b"not text\x00")
    bundle = repo / "rejected"
    assert runner.main(["Question", "--context", str(path), "--output-dir", str(bundle)]) == 2
    assert not bundle.exists()


@pytest.mark.parametrize("args", [
    ["Question", "--prompt-file", "note.md"],
    ["Question", "--model", "unknown-model"],
    ["Question", "--model", "claude-sonnet-4-5", "--effort", "max"],
    ["Question", "--max-budget-usd", "NaN"],
    ["Question", "--max-budget-usd", "201"],
    ["Question", "--max-tokens", "64001"],
])
def test_cli_rejects_invalid_configuration(repo, args):
    with pytest.raises(SystemExit) as failure:
        runner.main(args)
    assert failure.value.code == 2


def test_explicit_bundle_is_never_overwritten(repo):
    bundle = repo / "existing"
    bundle.mkdir()
    (bundle / "response.md").write_text("Keep this result")
    assert runner.main(["Question", "--dry-run", "--output-dir", str(bundle)]) == 2
    assert (bundle / "response.md").read_text() == "Keep this result"

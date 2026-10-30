"""The exact holdout audit must not admit candidates or modify input data."""

import hashlib
import json

import pytest
import qsearch


def parse(*options):
    return qsearch.build_parser().parse_args(["holdout-jets", *options])


def test_default_is_read_only(monkeypatch, capsys, tmp_path):
    import theorems.holdout_jet_audit as source

    monkeypatch.setattr(source, "report", lambda: {"speedup_claim_allowed": False})
    monkeypatch.setattr(qsearch, "initialize_seed_registry", lambda **kw: pytest.fail("unrelated registry write"))
    args = parse()
    args.root = tmp_path
    assert args.func(args) == 0
    assert not json.loads(capsys.readouterr().out)["speedup_claim_allowed"]
    assert not list(tmp_path.iterdir())


def test_public_input_provenance_and_explicit_output(tmp_path, capsys):
    specification = {"generator": [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]],
                     "degree": 3, "multiplicity": 2, "holdout": 3}
    path, destination = tmp_path / "input.json", tmp_path / "output.json"
    payload = json.dumps(specification).encode()
    path.write_bytes(payload)
    args = parse("--input", str(path), "--write", "--output", str(destination))
    assert args.func(args) == 0
    data = json.loads(destination.read_text())
    assert data == json.loads(capsys.readouterr().out)
    assert data["input_file_sha256"] == hashlib.sha256(payload).hexdigest()
    assert path.read_bytes() == payload
    assert sorted(p.name for p in tmp_path.iterdir()) == ["input.json", "output.json"]


@pytest.mark.parametrize("options", [("--output", "unused.json"), ("--rational",), ("--reduced",),
                                     ("--input", "unused.json", "--write")])
def test_invalid_write_and_mode_requests_fail_before_read(options):
    args = parse(*options)
    with pytest.raises(ValueError):
        args.func(args)


def test_output_cannot_overwrite_input(tmp_path):
    path = tmp_path / "input.json"
    payload = json.dumps({"generator": [[1, 0, 1], [0, 1, 1]],
                          "degree": 2, "multiplicity": 1, "holdout": 2}).encode()
    path.write_bytes(payload)
    args = parse("--input", str(path), "--write", "--output", str(path))
    with pytest.raises(ValueError, match="overwrite"):
        args.func(args)
    assert path.read_bytes() == payload


@pytest.mark.parametrize("payload", [[], {"generator": []},
    {"generator": [], "degree": 3, "multiplicity": 2, "holdout": 0, "secret": [1, 2]}])
def test_input_schema_is_exact(tmp_path, payload):
    path = tmp_path / "input.json"
    path.write_text(json.dumps(payload))
    args = parse("--input", str(path))
    with pytest.raises(ValueError, match="exactly"):
        args.func(args)

"""The CLI must construct before any scientific workflow can run."""

from pathlib import Path

import qsearch


def test_cli_source_compiles_with_legal_future_import_order():
    path = Path(qsearch.__file__)
    compile(path.read_bytes(), str(path), "exec")


def test_wreath_cli_uses_scoped_writer_without_initializing_seeds(monkeypatch, capsys):
    import theorems.wreath_coset_permutation_holevo_collapse as source

    writes = []
    monkeypatch.setattr(source, "write_report", lambda **kw: writes.append(kw["write_registry"]))
    monkeypatch.setattr(qsearch, "validate_registry", lambda: {"valid": True})
    monkeypatch.setattr(qsearch, "initialize_seed_registry", lambda **kw: (_ for _ in ()).throw(AssertionError("unrelated seed initialization")))
    for options in ([], ["--no-registry"]):
        args = qsearch.build_parser().parse_args(["wreath-coset-permutation-holevo-collapse", *options])
        assert args.func(args) == 0
        assert "not general code equivalence" in capsys.readouterr().out
    assert writes == [True, False]


def test_cfi_cli_applies_retraction_not_old_registration(tmp_path, monkeypatch, capsys):
    import json
    import theorems.cfi_graph_coset_luks_subsumption_barrier as cfi
    import theorems.nonabelian_barrier_scope_audit as audit

    calls = []
    report = {"status": "CFI_BOUNDED_VALENCE_BASELINE_SCOPED", "speedup_claim_allowed": False}
    output = tmp_path / "cfi.json"
    monkeypatch.setattr(cfi, "REPORT", output)
    monkeypatch.setattr(cfi, "build_report", lambda: report)
    monkeypatch.setattr(audit, "quarantine_reviewed_negatives", lambda: calls.append("quarantine"))
    monkeypatch.setattr(qsearch, "validate_registry", lambda: {"valid": True})
    monkeypatch.setattr(qsearch, "initialize_seed_registry", lambda **kw: (_ for _ in ()).throw(AssertionError("must not initialize unrelated seeds")))
    for options, expected_calls in (([], ["quarantine"]), (["--no-registry"], [])):
        calls.clear()
        args = qsearch.build_parser().parse_args(["cfi-graph-coset-luks-subsumption-barrier", *options])
        assert args.func(args) == 0
        assert calls == expected_calls
        assert json.loads(output.read_text()) == report
        assert "no general quantum lower bound" in capsys.readouterr().out
    assert not hasattr(cfi, "register_negative_result")
    assert sorted(p.name for p in tmp_path.iterdir()) == ["cfi.json"]


def test_cfi_cli_refuses_publication_after_changed_registry_evidence(tmp_path, monkeypatch):
    import pytest
    import theorems.cfi_graph_coset_luks_subsumption_barrier as cfi
    import theorems.nonabelian_barrier_scope_audit as audit

    def changed_evidence():
        raise ValueError("reviewed negative changed")

    monkeypatch.setattr(cfi, "REPORT", tmp_path / "cfi.json")
    monkeypatch.setattr(cfi, "build_report", lambda: {"status": "CFI_BOUNDED_VALENCE_BASELINE_SCOPED"})
    monkeypatch.setattr(audit, "quarantine_reviewed_negatives", changed_evidence)
    args = qsearch.build_parser().parse_args(["cfi-graph-coset-luks-subsumption-barrier"])
    with pytest.raises(ValueError, match="reviewed negative changed"):
        args.func(args)
    assert list(tmp_path.iterdir()) == []


def test_coherent_gram_cli_writes_arithmetic_not_quantum_execution(tmp_path, capsys):
    from fractions import Fraction
    import hashlib
    import json
    import pytest

    args = qsearch.build_parser().parse_args(["power-sde", "--coherent-gram", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    path = tmp_path / "research/reductions/invariant_gram_selector.json"
    saved = json.loads(path.read_text())
    assert saved == json.loads(capsys.readouterr().out)
    assert saved["public_controller_implemented"] is True
    assert saved["gram_outcomes_are_classical_reference_inputs"] is True
    for flag in ("quantum_receiver_implemented", "quantum_execution_performed",
                 "general_rank_improvement_established", "novelty_established",
                 "uniform_source_improvement_established",
                 "sequential_comparator_implemented_end_to_end",
                 "sequential_comparator_is_optimal",
                 "high_rank_direction_promoted",
                 "speedup_claim_allowed", "candidate_promoted",
                 "compiled_quantum_precision_budget_available"):
        assert saved[flag] is False
    assert len(saved["cases"]) == 6
    for row in saved["cases"]:
        assert row["moments"] == [0, 0, 0]
        assert row["gram_covariance_checked"] is True
        p = row["prime"]
        assert len(row["measurement_rows"]) == 6
        assert row["lifted_source_count"] == (14 if p % 3 == 2 else 16)
        assert row["matched_sequential_sufficient_count"] == (12 if p % 3 == 2 else 18)
        assert row["sequential_quadratic_arity"] == 6
        assert row["sequential_scalar_cubic_arity"] == (2 if p % 3 == 2 else 3)
        assert row["fewer_sources_than_this_comparator"] is (p % 3 == 1)
        assert Fraction(**row["arithmetic_abort_bound"]) <= Fraction(1, 2**row["failure_bits"])
        assert row["root_calls"] <= row["root_call_cap"] == 11
        assert row["conic_calls"] <= row["conic_call_cap"] == 4
        assert row["uniform_calls"] <= row["uniform_call_cap"]
        assert row["random_bits"] <= row["random_bit_cap"]
        assert any(row["scales"])
        for labels, degree in ((row["central_ell"], 3), (row["central_beta"], 2),
                               (row["reference_alpha"], 2)):
            assert sum(a*s**degree for a, s in zip(labels, row["scales"])) % p == 0
    root = Path(qsearch.__file__).resolve().parent
    for source, digest in saved["source_sha256"].items():
        assert hashlib.sha256((root/source).read_bytes()).hexdigest() == digest
    assert sorted(p.name for p in path.parent.iterdir()) == [path.name]
    assert not (tmp_path / "research/registry/candidates.json").exists()
    for conflicting in ("--random-column", "--rees-budget", "--bounded-randomness",
                        "--uniform-instrument", "--codimension-budget"):
        with pytest.raises(SystemExit):
            qsearch.build_parser().parse_args(["power-sde", "--coherent-gram", conflicting])


def test_coherent_gram_cli_is_read_only_without_write(tmp_path, capsys, monkeypatch):
    import json
    import theorems.invariant_gram_selector as gram

    monkeypatch.setattr(gram, "report", lambda: {"quantum_receiver_implemented": False})
    args = qsearch.build_parser().parse_args(["power-sde", "--coherent-gram"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert json.loads(capsys.readouterr().out) == {"quantum_receiver_implemented": False}
    assert list(tmp_path.iterdir()) == []


def test_random_column_cli_records_arithmetic_not_hsp_execution(tmp_path, capsys):
    import json
    import pytest
    from fractions import Fraction

    args = qsearch.build_parser().parse_args(["power-sde", "--random-column", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    path = tmp_path / "research/reductions/random_column_rees.json"
    saved = json.loads(path.read_text())
    assert saved == json.loads(capsys.readouterr().out)
    assert saved["quantum_receiver_implemented"] is False
    assert saved["speedup_claim_allowed"] is False
    assert saved["adversarial_bank_control"]["reason"] == "ATTEMPT_CAP"
    for row in saved["cases"]:
        assert Fraction(**row["tree_abort_bound"]) <= Fraction(1, 16)
        assert Fraction(**row["total_error_bound"]) <= Fraction(1, 3)
        assert row["all_failed_trees_charged"] is True
        assert row["labels_resampled_inside_kernel_trials"] is False
    assert not (tmp_path / "research/registry/candidates.json").exists()
    for conflicting in ("--rees-budget", "--codimension-budget", "--bounded-randomness", "--uniform-instrument"):
        with pytest.raises(SystemExit):
            qsearch.build_parser().parse_args(["power-sde", "--random-column", conflicting])


def test_random_column_cli_read_only_without_write(tmp_path, capsys, monkeypatch):
    import json
    import theorems.random_column_rees_budget as budget
    monkeypatch.setattr(budget, "report", lambda: {"quantum_receiver_implemented": False})
    args = qsearch.build_parser().parse_args(["power-sde", "--random-column"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert json.loads(capsys.readouterr().out) == {"quantum_receiver_implemented": False}
    assert list(tmp_path.iterdir()) == []


def test_uniform_instrument_cli_writes_separate_nonexecution_certificate(tmp_path, capsys):
    import json
    import pytest
    from fractions import Fraction

    args = qsearch.build_parser().parse_args(["power-sde", "--uniform-instrument", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    path = tmp_path / "research/reductions/rees_uniform_instrument.json"
    saved = json.loads(path.read_text())
    assert saved == json.loads(capsys.readouterr().out)
    assert saved["circuit_generator_implemented"] is False
    assert saved["quantum_receiver_implemented"] is False
    assert saved["speedup_claim_allowed"] is False
    for row in saved["cases"]:
        assert Fraction(**row["qft_error_bound"]) <= Fraction(1, 9)
        assert Fraction(**row["complete_output_error_bound"]) <= Fraction(1, 3)
    assert sorted(p.name for p in path.parent.iterdir()) == [path.name]
    assert not (tmp_path / "research/registry/candidates.json").exists()
    for conflicting in ("--rees-budget", "--codimension-budget", "--bounded-randomness"):
        with pytest.raises(SystemExit):
            qsearch.build_parser().parse_args(["power-sde", "--uniform-instrument", conflicting])


def test_uniform_instrument_cli_is_read_only_without_write(tmp_path, capsys, monkeypatch):
    import json
    import theorems.rees_uniform_instrument as instrument
    monkeypatch.setattr(instrument, "report", lambda: {"quantum_receiver_implemented": False})
    args = qsearch.build_parser().parse_args(["power-sde", "--uniform-instrument"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert json.loads(capsys.readouterr().out) == {"quantum_receiver_implemented": False}
    assert list(tmp_path.iterdir()) == []


def test_codimension_budget_cli_is_isolated_and_explicit(tmp_path, capsys):
    import json
    import pytest
    from fractions import Fraction

    previous = tmp_path / "research/reductions/rees_full_grade_budget.json"
    previous.parent.mkdir(parents=True)
    previous.write_text("previous whole-grade certificate")
    args = qsearch.build_parser().parse_args([
        "power-sde", "--codimension-budget", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((previous.parent / "codimension_hybrid_budget.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert previous.read_text() == "previous whole-grade certificate"
    assert saved["quantum_receiver_implemented"] is False
    assert saved["speedup_claim_allowed"] is False
    for row in saved["cases"]:
        assert Fraction(**row["total_error_bound"]) <= Fraction(**row["error_target"])
    assert not (tmp_path / "research/registry/candidates.json").exists()
    for conflicting in ("--rees-budget", "--bounded-randomness"):
        with pytest.raises(SystemExit):
            qsearch.build_parser().parse_args([
                "power-sde", "--codimension-budget", conflicting])


def test_codimension_budget_cli_is_read_only_without_write(tmp_path, capsys, monkeypatch):
    import json
    import theorems.codimension_hybrid_budget as budget

    monkeypatch.setattr(budget, "report", lambda: {"quantum_receiver_implemented": False})
    args = qsearch.build_parser().parse_args(["power-sde", "--codimension-budget"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert json.loads(capsys.readouterr().out) == {"quantum_receiver_implemented": False}
    assert list(tmp_path.iterdir()) == []


def test_subspace_source_cli_records_hypothetical_complete_budgets(tmp_path, capsys):
    from fractions import Fraction
    import hashlib
    import json

    args = qsearch.build_parser().parse_args(["subspace-source", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path/"research/reductions/rees_subspace_source.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert saved["status"] == "CONDITIONAL_SOURCE_REDUCTION_RESOURCE_PLAN_ONLY"
    assert saved["public_group_profile"]["rees_dimension"] == 97
    assert saved["public_group_profile"]["class"] == 9
    assert not any(saved["public_group_profile"]["design_moments"])
    assert [r["rank"] for r in saved["profiles"]] == [1, 2, 8, 32]
    for row in saved["profiles"]:
        b = row["budget"]
        raw, growth, outputs = b["raw_copy_cap"], b["growth_attempt_cap"], b["ideal_target_copies"]
        assert raw == outputs+growth
        assert b["tensor_factor_controlled_action_call_cap"] == row["rank"]*outputs
        assert Fraction(**b["total_error_bound"]) <= Fraction(1, 3)
        assert not b["preparer_quantum_backend_implemented"]
        assert not b["speedup_claim_allowed"]
    for key in ("quantum_execution_performed", "quantum_receiver_implemented",
                "natural_hard_state_family_established", "novelty_established",
                "nonflat_conjugation_symmetry_covered", "speedup_claim_allowed"):
        assert saved[key] is False
    assert saved["hypothetical_source_promises"]["state_constructed"] is False
    root = Path(qsearch.__file__).resolve().parent
    for source, digest in saved["source_sha256"].items():
        assert hashlib.sha256((root/source).read_bytes()).hexdigest() == digest
    assert not (tmp_path/"research/registry/candidates.json").exists()


def test_subspace_source_cli_is_read_only_without_write(tmp_path, capsys, monkeypatch):
    import json
    import theorems.rees_subspace_source as source
    monkeypatch.setattr(source, "report", lambda: {"quantum_execution_performed": False})
    args = qsearch.build_parser().parse_args(["subspace-source"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert json.loads(capsys.readouterr().out) == {"quantum_execution_performed": False}
    assert not list(tmp_path.iterdir())


def test_mixed_spectrum_cli_retains_control_scope_and_preserves_flat_report(tmp_path, capsys):
    from fractions import Fraction
    import hashlib
    import json

    flat = tmp_path/"research/reductions/rees_subspace_source.json"
    flat.parent.mkdir(parents=True)
    flat.write_text("prior flat source report")
    args = qsearch.build_parser().parse_args(["subspace-source", "--mixed-spectrum", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((flat.parent/"mixed_spectral_source.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert flat.read_text() == "prior flat source report"
    assert saved["exact_spectra_supplied_only_to_reference"]
    assert saved["status"] == "CONDITIONAL_REDUCTION_FINITE_CONTROLS_ONLY"
    for row in saved["cases"]:
        assert row["profile"]["known_spectrum_reference_only"]
        assert row["flag_stabilizer_from_known_diagonal_reference"] == [0]
        assert row["whole_support_wedge_stabilizer"] == [0, 1, 2]
        assert Fraction(**row["actual_nonidentity_trace_gap"]) >= Fraction(**row["supplied_trace_gap"])
        assert row["profile"]["good_offset"]
        assert not row["single_product_preparation_caps"]["dme_program_copies_included"]
    for key in ("quantum_rank_acquisition_implemented", "quantum_spectral_filter_implemented",
                "total_raw_copy_budget_implemented", "end_to_end_quantum_execution",
                "novelty_established", "natural_hard_family_established", "speedup_claim_allowed"):
        assert saved[key] is False
    root = Path(qsearch.__file__).resolve().parent
    for source, digest in saved["source_sha256"].items():
        assert hashlib.sha256((root/source).read_bytes()).hexdigest() == digest


def test_iterated_stabilizer_cli_records_distinct_upper_and_full_groups(tmp_path, capsys):
    import json
    args = qsearch.build_parser().parse_args(["iterated-stabilizer", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path / "research/classical_baselines/iterated_quadratic_jet.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert saved["schema_version"] == "1.1"
    assert len(saved["cases"]) == 4
    unknown, resolved = saved["cases"][2:]
    assert unknown["input"] == resolved["input"]
    assert unknown["full_stabilizer_generators"] is None
    assert unknown["status"] == "UNKNOWN_FULL_STABILIZER"
    assert resolved["full_stabilizer_order"] == {"base": 7, "exponent": 3}
    assert resolved["full_stabilizer_certified"]
    assert not saved["quantum_advantage_claimed"] and not saved["hardness_claimed"]
    assert not (tmp_path / "history.json").exists()


def test_iterated_stabilizer_cli_consumes_public_input_and_fixed_anchor(tmp_path, capsys):
    import hashlib
    import json
    source, output = tmp_path / "problem.json", tmp_path / "result.json"
    specification = {"p": 7, "block_size": 2, "T": 0, "c": [1, 1],
                     "A": [[0, 0], [0, 0]], "B": [[[0, 0], [0, 0]]] * 2, "ell": [0, 1]}
    consumed = json.dumps({"input": specification, "anchors": [[3, 0]]}).encode()
    source.write_bytes(consumed)
    args = qsearch.build_parser().parse_args([
        "iterated-stabilizer", "--input", str(source), "--write", "--output", str(output)])
    args.root = tmp_path
    assert args.func(args) == 0
    result = json.loads(capsys.readouterr().out)
    assert json.loads(output.read_text()) == result
    assert result["input_file_sha256"] == hashlib.sha256(consumed).hexdigest()
    assert result["schema_version"] == "1.1"
    assert result["input"] == specification and result["anchors"] == [[3, 0]]
    assert result["full_stabilizer_certified"] and result["full_stabilizer_order"] == {"base": 7, "exponent": 1}
    assert not result["all_upper_generators_propagate"]
    assert not (tmp_path / "research/classical_baselines/iterated_quadratic_jet.json").exists()


def test_iterated_stabilizer_cli_does_not_clobber_calibration_with_input(tmp_path):
    import pytest
    args = qsearch.build_parser().parse_args([
        "iterated-stabilizer", "--input", str(tmp_path / "problem.json"), "--write"])
    with pytest.raises(ValueError, match="requires --output"):
        args.func(args)
    args = qsearch.build_parser().parse_args([
        "iterated-stabilizer", "--output", str(tmp_path / "unused.json")])
    with pytest.raises(ValueError, match="requires --write"):
        args.func(args)


def test_native_sampling_cli_writes_scoped_exact_controls(tmp_path, capsys):
    import json
    args = qsearch.build_parser().parse_args(["inverse-trace-sampling", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    row = json.loads((tmp_path / "research/classical_baselines/inverse_trace_menu_refresh.json").read_text())
    assert json.loads(capsys.readouterr().out) == row
    assert not row["general_classical_hardness"] and not row["speedup_established"]
    assert row["finite_controls"][1]["conditional_tv"] == {"numerator": 39, "denominator": 4240}
    assert [r["free_field_variables"] for r in row["conditional_residual_forecasts"]] == [4, 6, 12]
    assert not any(r["residual_sampler_implemented"] for r in row["conditional_residual_forecasts"])


def test_native_hash_cli_runs_complete_cells_on_exact_input(tmp_path, capsys):
    import json
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--hash-cells", "--bits", "5", "--cells", "2",
        "--prange-trials", "16", "--timeout-ms", "5000", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path / "research/classical_baselines/inverse_trace_hash_cells.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert saved["residual"]["source"] == "FIXED_ACCEPTED_PREFIX"
    assert saved["residual"]["binary_coordinates"] == 4
    assert all(c["enumeration"]["complete"] for c in saved["cells"])
    assert all(c["independent_reference"]["reported_complete_set_matches"] for c in saved["cells"])
    assert not saved["uniform_sampler"] and not saved["speedup_established"]
    assert not (tmp_path / "research/classical_baselines/inverse_trace_menu_refresh.json").exists()


def test_native_hash_cli_rejects_unscoped_known_anchor():
    import pytest
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--hash-cells", "--supply-anchor"])
    with pytest.raises(ValueError, match="requires --anchor-report"):
        args.func(args)


def test_native_hash_cli_fingerprints_consumed_anchor_bytes(tmp_path, capsys, monkeypatch):
    import hashlib
    import json
    from theorems.explicit_quadratic_opi import field
    import theorems.inverse_trace_hash_probe as probe
    instance = {"bits": 2, "points": [0, 1, 2, 3], "checks": 1,
                "targets": [0]*4,
                "field_modulus_coefficients": list(map(int, field(2).modulus().coeffs()))}
    input_path, anchor_path = tmp_path/"input.json", tmp_path/"anchor.json"
    input_path.write_text(json.dumps(instance))
    consumed = json.dumps({"instance": instance, "witness": [0]*4}).encode()
    anchor_path.write_bytes(consumed)
    original = probe.run_probe

    def replace_anchor_after_loading(*args, **kwargs):
        result = original(*args, **kwargs)
        anchor_path.write_text("replacement unrelated to the consumed witness")
        return result

    monkeypatch.setattr(probe, "run_probe", replace_anchor_after_loading)
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--hash-cells", "--input", str(input_path),
        "--anchor-report", str(anchor_path), "--supply-anchor", "--cells", "1",
        "--surplus", "1", "--prange-trials", "0"])
    assert args.func(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["anchor_report_sha256"] == hashlib.sha256(consumed).hexdigest()
    assert report["anchor_report_sha256"] != hashlib.sha256(anchor_path.read_bytes()).hexdigest()


def test_quadratic_cli_preserves_saved_native_cells(tmp_path, capsys):
    import hashlib
    import json
    from theorems.inverse_trace_hash_probe import run_probe
    from theorems.inverse_trace_smt import native_instance
    prior = run_probe(native_instance(5), cells=2, prange_trials=0)
    source = tmp_path/"cells.json"
    consumed = json.dumps(prior).encode()
    source.write_bytes(consumed)
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--quadratic-cells", "--input", str(source), "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["instance"] == prior["instance"]
    assert report["residual"] == prior["residual"]
    assert report["input_report_sha256"] == hashlib.sha256(consumed).hexdigest()
    assert not report["new_hashes_generated"] and not report["full_algebraic_solver"]
    assert not report["uniform_sampler"] and not report["speedup_established"]
    assert not report["all_local_quadratic_relations_covered"]  # n5 has additional relations.
    assert not report["higher_degree_closure_covered"]
    assert report["local_quadratic_span_certificates"][0]["certificate"]["bits"] == 5
    for original, result in zip(prior["cells"], report["cells"], strict=True):
        assert result["hash_rows"] == original["hash_rows"]
        assert result["hash_rhs"] == original["hash_rhs"]
        assert original["enumeration"]["model_count"] > 0
        assert not result["analysis"]["native_cell_empty_certified"]
    path = tmp_path/"research/classical_baselines/inverse_trace_hash_quadratic.json"
    assert json.loads(path.read_text()) == report


def test_quadratic_cli_rejects_a_changed_saved_residual(tmp_path):
    import json
    import pytest
    from theorems.inverse_trace_hash_probe import run_probe
    from theorems.inverse_trace_smt import native_instance
    prior = run_probe(native_instance(5), cells=1, prange_trials=0)
    prior["residual"]["residual_syndrome"][0] ^= 1
    source = tmp_path/"changed.json"
    source.write_text(json.dumps(prior))
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--quadratic-cells", "--input", str(source)])
    with pytest.raises(ValueError, match="exact reconstruction"):
        args.func(args)


def test_quadratic_cli_rejects_unverified_local_completeness(tmp_path, monkeypatch):
    import json
    import pytest
    from theorems.inverse_trace_hash_probe import run_probe
    from theorems.inverse_trace_smt import native_instance
    import theorems.inverse_trace_local_quadratic_span as local_span
    prior = run_probe(native_instance(5), cells=1, prange_trials=0)
    source = tmp_path/"cells.json"
    source.write_text(json.dumps(prior))
    original = local_span.span_certificate

    def tampered(*args, **kwargs):
        certificate = original(*args, **kwargs)
        certificate["complete_local_quadratic_span"] = True
        return certificate

    monkeypatch.setattr(local_span, "span_certificate", tampered)
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--quadratic-cells", "--input", str(source)])
    with pytest.raises(ArithmeticError, match="completeness certificate failed"):
        args.func(args)


def test_quadratic_cli_refuses_a_false_contradiction_for_known_anchor(tmp_path, monkeypatch):
    import json
    import pytest
    from theorems.explicit_quadratic_opi import field
    from theorems.inverse_trace_hash_probe import run_probe
    import theorems.inverse_trace_hash_quadratic as quadratic
    instance = {"bits": 3, "points": [0, 1, 2, 3], "checks": 1,
                "targets": [0]*4,
                "field_modulus_coefficients": list(map(int, field(3).modulus().coeffs()))}
    prior = run_probe(instance, surplus=1, cells=1, anchor_word=[0]*4, prange_trials=0)
    source = tmp_path/"anchored.json"
    source.write_text(json.dumps(prior))
    monkeypatch.setattr(quadratic, "analyze_cell", lambda *args, **kwargs: {"native_cell_empty_certified": True})
    args = qsearch.build_parser().parse_args([
        "inverse-trace-sampling", "--quadratic-cells", "--input", str(source)])
    with pytest.raises(ArithmeticError, match="native anchor"):
        args.func(args)


def test_parser_builds_and_preserves_the_integrated_swap_command():
    # argparse raises on duplicate registration during build_parser itself.
    parser=qsearch.build_parser()
    validation=parser.parse_args(["validate"])
    assert validation.func is qsearch.command_validate
    swap=parser.parse_args(["native-higher-call-two-copy-swap-purity-bridge","--no-write"])
    assert swap.no_write is True
    assert swap.func is qsearch.command_native_higher_call_two_copy_swap_purity_bridge


def test_norm_comparison_options_are_wired(tmp_path, capsys):
    import json
    parser = qsearch.build_parser()
    output = tmp_path / "norm-control.json"
    args = parser.parse_args(["inverse-trace-norm", "--bits", "5", "--max-trials", "0",
                              "--compare-flat-dimension", "1", "--flat-seed", "1030",
                              "--write", "--output", str(output)])
    assert args.func(args) == 0
    saved = json.loads(output.read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert saved["same_instance_flat_comparison"]["norm_family_membership"]["certificate_verified"]


def test_prime_power_sde_workflow_writes_exact_replayable_artifact(tmp_path, capsys):
    import json
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path / "research/reductions/prime_power_regular_sde.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert not saved["quantum_receiver_executed"] and not saved["speedup_established"]
    assert not saved["pilot_subgroup_coordinates_implemented"]
    for case in saved["cases"]:
        p, degree, scales = case["prime"], case["degree"], case["lift"]["scales"]
        assert case["lift"]["original_module_verified"] and any(scales)
        assert all(s == 0 or s % p for s in scales)
        assert all(sum(col[j] * pow(s, degree, p**e)
                       for col, s in zip(case["columns"], scales)) % p**e == 0
                   for j, e in enumerate(case["exponents"]))
        assert case["whole_grade_budget"]["pilot_samples"] == len(case["exponents"])+2
        certificate = case["regular_block_certificate"]
        assert certificate["rank"] == len(case["exponents"])
        assert len(certificate["indices"]) == len(case["exponents"])+1
        assert all(case["field_witness"][i] for i in certificate["indices"])


def test_random_kernel_cli_selects_separate_artifact(tmp_path,capsys,monkeypatch):
    import json
    import theorems.random_regular_sde as module
    payload = {"status":"TEST_DISPATCH_ONLY","quantum_receiver_executed":False}
    monkeypatch.setattr(module,"report",lambda:payload)
    args = qsearch.build_parser().parse_args(["prime-power-sde","--random-kernel","--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert json.loads(capsys.readouterr().out) == payload
    assert json.loads((tmp_path/"research/reductions/random_regular_sde.json").read_text()) == payload
    assert not (tmp_path/"research/reductions/prime_power_regular_sde.json").exists()


def test_span_block_cli_uses_separate_artifact_and_rejects_combined_modes(tmp_path,capsys,monkeypatch):
    import json
    import pytest
    import theorems.span_regular_sde as module
    payload = {"status":"TEST_DISPATCH_ONLY","quantum_receiver_executed":False}
    monkeypatch.setattr(module,"report",lambda:payload)
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde","--span-blocks","--write"])
    args.root = tmp_path
    assert args.func(args)==0
    assert json.loads(capsys.readouterr().out)==payload
    assert json.loads((tmp_path/"research/reductions/span_regular_sde.json").read_text())==payload
    with pytest.raises(SystemExit):
        parser.parse_args(["prime-power-sde","--span-blocks","--random-kernel"])


def test_pilot_cli_writes_separate_scoped_artifact(tmp_path,capsys):
    import json
    import pytest
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde","--pilots","--write"])
    args.root = tmp_path
    assert args.func(args)==0
    saved = json.loads((tmp_path/"research/reductions/pilot_module_descent.json").read_text())
    assert json.loads(capsys.readouterr().out)==saved
    assert saved["public_label_pilot_coordinates_implemented"]
    assert not saved["quantum_receiver_executed"] and not saved["speedup_established"]
    for mode in ("--span-blocks","--random-kernel"):
        with pytest.raises(SystemExit):
            parser.parse_args(["prime-power-sde","--pilots",mode])


def test_receiver_policy_cli_is_explicitly_not_quantum_execution(tmp_path,capsys):
    import json
    import pytest
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde","--receiver-policy","--write"])
    args.root = tmp_path
    assert args.func(args)==0
    saved = json.loads((tmp_path/"research/reductions/pilot_receiver_policy.json").read_text())
    assert json.loads(capsys.readouterr().out)==saved
    assert not saved["quantum_receiver_executed"] and not saved["speedup_established"]
    assert saved["postselection_falsifier"]["conditional_distance"]=={"numerator":1,"denominator":10}
    for mode in ("--pilots","--span-blocks","--random-kernel"):
        with pytest.raises(SystemExit):
            parser.parse_args(["prime-power-sde","--receiver-policy",mode])


def test_unit_kernel_cli_artifact_and_exclusive_modes(tmp_path, capsys):
    import json
    import pytest
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde", "--unit-kernel", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path/"research/reductions/unit_power_module.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert not saved["quantum_receiver_implemented"] and not saved["all_prime_ring_hsp_bound"]
    assert all(row["result"]["original_ambient_verified"] for row in saved["cases"])
    for mode in ("--pilots", "--span-blocks", "--random-kernel", "--receiver-policy"):
        with pytest.raises(SystemExit):
            parser.parse_args(["prime-power-sde", "--unit-kernel", mode])


def test_unit_kernel_cli_read_only_by_default(tmp_path, capsys):
    args = qsearch.build_parser().parse_args(["prime-power-sde", "--unit-kernel"])
    args.root = tmp_path
    assert args.func(args) == 0
    capsys.readouterr()
    assert not (tmp_path/"research").exists()


def test_subset_kernel_cli_artifact_and_exclusive_modes(tmp_path, capsys):
    import json
    import pytest
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde", "--subset-kernel", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path/"research/reductions/small_prime_module.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert not saved["quantum_receiver_implemented"] and not saved["all_prime_ring_hsp_bound"]
    assert all(row["result"]["original_ambient_verified"] for row in saved["cases"])
    assert {tree["regime"] for tree in saved["source_trees"]} == {
        "SMALL_PRIME_REGULAR_SUBSET", "LARGE_PRIME_UNIT_KERNEL"}
    for mode in ("--pilots", "--span-blocks", "--random-kernel", "--receiver-policy", "--unit-kernel"):
        with pytest.raises(SystemExit):
            parser.parse_args(["prime-power-sde", "--subset-kernel", mode])


def test_subset_kernel_cli_read_only_by_default(tmp_path, capsys):
    args = qsearch.build_parser().parse_args(["prime-power-sde", "--subset-kernel"])
    args.root = tmp_path
    assert args.func(args) == 0
    capsys.readouterr()
    assert not (tmp_path/"research").exists()


def test_rank_reduction_cli_preserves_public_arithmetic_scope(tmp_path, capsys):
    import json
    import pytest
    parser = qsearch.build_parser()
    args = parser.parse_args(["prime-power-sde", "--rank-reduction", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path/"research/reductions/ring_to_field_rank_reduction.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert saved["status"] == "PUBLIC_RING_TO_FIELD_CONTROLS_NOT_HSP_EXECUTION"
    assert saved["torsion_controls"] and saved["readout_controls"]
    assert not saved["full_outer_reduction_implemented"]
    assert not saved["field_core_newly_proved"] and not saved["speedup_claim_allowed"]
    assert not saved["candidate_promotion"] and not saved["proof_promotion"]
    assert all(row["result"]["certificate_verified"] for row in saved["readout_controls"])
    assert all(not row["result"]["hidden_subgroup_recovery_certified"]
               for row in saved["readout_controls"])
    for mode in ("--pilots", "--span-blocks", "--random-kernel", "--receiver-policy",
                 "--unit-kernel", "--subset-kernel"):
        with pytest.raises(SystemExit):
            parser.parse_args(["prime-power-sde", "--rank-reduction", mode])


def test_rank_reduction_cli_is_read_only_without_write(tmp_path, capsys):
    args = qsearch.build_parser().parse_args(["prime-power-sde", "--rank-reduction"])
    args.root = tmp_path
    assert args.func(args) == 0
    capsys.readouterr()
    assert not (tmp_path/"research").exists()

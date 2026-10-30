"""General and smaller-track subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.

Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.
A command imports what it needs from ``qsearch`` when it runs, so loading this module stays
cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def add_holdout_jets(subparsers):
    parser = subparsers.add_parser("holdout-jets", help="Verify exact binary Hasse-jet holdout certificates; not a quantum attack")
    parser.add_argument("--input", type=Path, help="JSON public generator, degree, multiplicity and holdout")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--rational", action="store_true", help="Compare the same matrix over the rationals, within a small exact cap")
    mode.add_argument("--reduced", action="store_true", help="Remove characteristic-two redundant derivative orders")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.set_defaults(func=command_holdout_jets)


def command_holdout_jets(args):
    import hashlib
    from theorems.holdout_jet_audit import analyze, report

    if args.output and not args.write:
        raise ValueError("--output requires --write")
    if args.input and args.write and not args.output:
        raise ValueError("writing a supplied input requires --output")
    if not args.input and (args.rational or args.reduced):
        raise ValueError("--rational and --reduced require --input")
    if args.input:
        consumed = args.input.read_bytes()
        specification = json.loads(consumed)
        required = {"generator", "degree", "multiplicity", "holdout"}
        if not isinstance(specification, dict) or set(specification) != required:
            raise ValueError("input must contain exactly generator, degree, multiplicity and holdout")
        data = analyze(**specification, rational=args.rational, reduced=args.reduced)
        data["input_file_sha256"] = hashlib.sha256(consumed).hexdigest()
    else:
        data = report()
    data["proof_note"] = "research/GOPPA_HOLDOUT_QUANTUM_ACCESS.md"
    payload = json.dumps(data, indent=2) + "\n"
    if args.write:
        destination = args.output or args.root / "research/code_equivalence/holdout_jet_audit.json"
        if args.input and destination.resolve() == args.input.resolve():
            raise ValueError("output must not overwrite the supplied input")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0


def add_iterated_stabilizer(subparsers):
    parser = subparsers.add_parser("iterated-stabilizer", help="Test exact low-jet classical certificates for iterated polynomial symmetries")
    parser.add_argument("--input", type=Path, help="Public quadratic-map specification, optionally wrapped with input and fixed anchors")
    parser.add_argument("--output", type=Path, help="Output path with --write; required when writing an --input result")
    parser.add_argument("--write", action="store_true")
    parser.set_defaults(func=command_iterated_stabilizer)


def command_iterated_stabilizer(args):
    import hashlib
    from theorems.iterated_quadratic_jet import QuadraticIteration, analyze, report
    if args.output and not args.write:
        raise ValueError("--output requires --write")
    if args.input and args.write and not args.output:
        raise ValueError("writing an --input result requires --output to preserve the calibration report")
    if args.input:
        consumed = args.input.read_bytes()
        supplied = json.loads(consumed)
        if not isinstance(supplied, dict):
            raise ValueError("--input must contain a public specification object")
        if "input" in supplied:
            specification, anchors = supplied["input"], supplied.get("anchors")
        else:
            specification, anchors = supplied, None
        if not isinstance(specification, dict):
            raise ValueError("public quadratic-map specification must be an object")
        data = analyze(QuadraticIteration(**specification), anchors=anchors)
        data["input_file_sha256"] = hashlib.sha256(consumed).hexdigest()
        data["proof_note"] = "research/ITERATED_QUADRATIC_JET_FILTER.md"
    else:
        data = report()
    payload = json.dumps(data, indent=2)+"\n"
    if args.write:
        destination = args.output or args.root/"research/classical_baselines/iterated_quadratic_jet.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0


def add_inverse_trace_sampling(subparsers):
    parser = subparsers.add_parser("inverse-trace-sampling", help="Audit native sampling laws or probe complete binary-hash cells")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--hash-cells", action="store_true")
    mode.add_argument("--quadratic-cells", action="store_true", help="Check quadratic contradictions on the exact cells of a saved hash-cell report")
    parser.add_argument("--max-monomials", type=int, default=300000)
    parser.add_argument("--input", type=Path, help="Original instance or saved report containing its instance")
    parser.add_argument("--anchor-report", type=Path, help="Separate witness-conditioned diagnostic, NOT unplanted initialization")
    parser.add_argument("--supply-anchor", action="store_true", help="Verify and preblock the supplied anchor before enumerating the rest of its cell")
    parser.add_argument("--bits", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1028)
    parser.add_argument("--target-mode", choices=("ones", "random"), default="ones")
    parser.add_argument("--prefix-seed", type=int, default=1029)
    parser.add_argument("--hash-seed", type=int, default=1030)
    parser.add_argument("--cells", type=int, default=3)
    parser.add_argument("--surplus", type=int)
    parser.add_argument("--timeout-ms", type=int, default=10000)
    parser.add_argument("--resource-limit", type=int, default=50000000)
    parser.add_argument("--max-models", type=int, default=16)
    parser.add_argument("--prange-trials", type=int, default=256)
    parser.add_argument("--reference-bits", type=int, default=16)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.set_defaults(func=command_inverse_trace_sampling)


def command_inverse_trace_sampling(args):
    from theorems.inverse_trace_menu_refresh import json_value, report
    if args.quadratic_cells:
        data = _quadratic_saved_cells(args)
        default = "research/classical_baselines/inverse_trace_hash_quadratic.json"
    elif args.hash_cells:
        import hashlib
        from theorems.inverse_trace_hash_probe import run_probe
        from theorems.inverse_trace_smt import native_instance
        if args.supply_anchor and not args.anchor_report:
            raise ValueError("--supply-anchor requires --anchor-report")
        supplied = json.loads(args.input.read_text()) if args.input else None
        instance = (supplied.get("instance", supplied) if supplied is not None else
                    native_instance(args.bits, args.seed, args.target_mode))
        anchor = None
        anchor_bytes = None
        if args.anchor_report:
            anchor_bytes = args.anchor_report.read_bytes()
            anchor = json.loads(anchor_bytes)
            if anchor.get("instance") != instance or not anchor.get("witness"):
                raise ValueError("anchor report must contain a witness for the exact supplied original instance")
        data = run_probe(instance, prefix_seed=args.prefix_seed, hash_seed=args.hash_seed,
                         cells=args.cells, surplus=args.surplus, timeout_ms=args.timeout_ms,
                         resource_limit=args.resource_limit, max_models=args.max_models,
                         prange_trials=args.prange_trials, reference_bits=args.reference_bits,
                         anchor_word=None if anchor is None else anchor["witness"],
                         supply_anchor=args.supply_anchor)
        if args.anchor_report:
            data["anchor_report_sha256"] = hashlib.sha256(anchor_bytes).hexdigest()
        default = "research/classical_baselines/inverse_trace_hash_cells.json"
    else:
        if args.input or args.anchor_report or args.supply_anchor:
            raise ValueError("instance/anchor inputs require --hash-cells")
        data = report()
        default = "research/classical_baselines/inverse_trace_menu_refresh.json"
    payload = json.dumps(data, default=json_value, indent=2)+"\n"
    if args.write:
        path = args.output or Path(default)
        if not path.is_absolute():
            path = args.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload)
    print(payload, end="")
    return 0


def _quadratic_saved_cells(args):
    import hashlib
    from time import perf_counter
    import theorems.inverse_trace_algebraic_audit as algebraic
    import theorems.inverse_trace_hash_probe as probe
    import theorems.inverse_trace_hash_quadratic as quadratic
    import theorems.inverse_trace_local_quadratic_span as local_span

    start = perf_counter()
    if not args.input or args.anchor_report or args.supply_anchor:
        raise ValueError("--quadratic-cells requires --input of a saved hash-cell report; anchors come from that report")
    consumed = args.input.read_bytes()
    prior = json.loads(consumed)
    instance, saved = prior["instance"], prior["residual"]
    digest = hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest()
    if digest != prior["instance_sha256"]:
        raise ValueError("saved original instance digest disagrees")
    sources = (Path(__file__), Path(quadratic.__file__), Path(probe.__file__),
               Path(algebraic.__file__), Path(local_span.__file__))
    root = Path(__file__).resolve().parents[2]
    before = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    descriptor, decode, valid = probe.prepare_probe(
        instance, prefix_seed=saved["prefix_seed"], surplus=saved["free_field_variables"],
        anchor_word=saved["supplied_anchor_full_word"])
    for key in ("residual_indices", "accepted_prefix", "residual_syndrome", "anchor_u",
                "trace_kernel_basis", "binary_coordinates", "hash_rows_count", "source"):
        if descriptor[key] != saved[key]:
            raise ValueError(f"saved residual disagrees with its exact reconstruction: {key}")
    cells = prior["cells"]
    if not isinstance(cells, list) or not 1 <= len(cells) <= 32:
        raise ValueError("saved report must contain 1..32 declared cells")
    local_certificates = []
    for target in sorted({instance["targets"][i] for i in descriptor["residual_indices"]}):
        certificate = local_span.span_certificate(instance["bits"], target)
        verified = local_span.verify_span_certificate(certificate)
        if certificate["complete_local_quadratic_span"] and not verified:
            raise ArithmeticError("local quadratic completeness certificate failed replay")
        local_certificates.append({"certificate": certificate, "verified": verified})
    preparation_seconds = perf_counter()-start
    results = []
    for cell in cells:
        rows, rhs = cell["hash_rows"], cell["hash_rhs"]
        if len(rows) != descriptor["hash_rows_count"]:
            raise ValueError("saved cell has a different hash width")
        anchor = descriptor["anchor_u"]
        if anchor is not None:
            if not valid(decode(anchor)) or any(
                    ((row & anchor).bit_count() & 1) != ((rhs >> j) & 1)
                    for j, row in enumerate(rows)):
                raise ValueError("saved anchor does not belong to this native hash cell")
        result = quadratic.analyze_cell(
            instance, descriptor["residual_indices"], descriptor["residual_syndrome"],
            rows, rhs, timeout_ms=args.timeout_ms, max_monomials=args.max_monomials)
        if anchor is not None and result["native_cell_empty_certified"]:
            raise ArithmeticError("quadratic contradiction rejected an independently verified native anchor")
        results.append({"cell_index": cell["cell_index"], "hash_rows": rows, "hash_rhs": rhs,
                        "known_anchor_verified": anchor is not None, "analysis": result})
    after = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    if after != before:
        raise RuntimeError("source files changed during quadratic campaign")
    if hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest() != digest:
        raise ArithmeticError("quadratic campaign mutated the original instance")
    return {"status": "BOUNDED_NATIVE_QUADRATIC_SPAN_PROBE", "instance": instance,
            "instance_sha256": digest, "residual": saved, "cells": results,
            "input_report_sha256": hashlib.sha256(consumed).hexdigest(),
            "input_report_path": str(args.input), "source_hashes": before,
            "local_quadratic_span_certificates": local_certificates,
            "all_local_quadratic_relations_covered": all(c["verified"] for c in local_certificates),
            "higher_degree_closure_covered": False,
            "preparation_seconds": preparation_seconds, "total_seconds": perf_counter()-start,
            "whole_workflow_wall_clock_cap_enforced": False,
            "source_fingerprint_scope": "selected_disk_sources_before_and_after_not_bytecode_attestation",
            "new_hashes_generated": False, "uniform_sampler": False,
            "full_algebraic_solver": False, "hardness_evidence": False,
            "speedup_established": False}


def add_inverse_trace_norm(subparsers):
    parser = subparsers.add_parser("inverse-trace-norm", help="Test a polynomial-norm attack on the original inverse-trace relation")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--bits", type=int, default=17)
    parser.add_argument("--seed", type=int, default=1028)
    parser.add_argument("--polynomial-seed", type=int, default=1029)
    parser.add_argument("--target-mode", choices=("ones", "random"), default="ones")
    parser.add_argument("--max-trials", type=int, default=64)
    parser.add_argument("--compare-flat-dimension", type=int,
                        help="Run the existing flat attack on the same all-one input and test whole norm-family membership")
    parser.add_argument("--flat-seed", type=int, default=1030)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("research/classical_baselines/inverse_trace_norm.json"))
    parser.set_defaults(func=command_inverse_trace_norm)


def command_inverse_trace_norm(args):
    from theorems.inverse_trace_norm import run_experiment
    from theorems.inverse_trace_smt import native_instance
    instance = json.loads(args.input.read_text()) if args.input else native_instance(args.bits, args.seed, args.target_mode)
    result = run_experiment(instance, seed=args.polynomial_seed, max_trials=args.max_trials,
                            compare_flat_dimension=args.compare_flat_dimension, flat_seed=args.flat_seed)
    payload = json.dumps(result, indent=2)+"\n"
    if args.write:
        path = args.output if args.output.is_absolute() else args.root/args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload)
    print(payload, end="")
    return 0


def add_inverse_trace_smt(subparsers):
    parser = subparsers.add_parser("inverse-trace-smt", help="Attack the original inverse-trace relation with capped exact SAT")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--bits", type=int, default=17)
    parser.add_argument("--seed", type=int, default=1028)
    parser.add_argument("--target-mode", choices=("ones", "random"), default="ones")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--pipeline", choices=("direct", "qfbv"), default="direct")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--resource-limit", type=int, default=50_000_000)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("research/classical_baselines/inverse_trace_smt.json"))
    parser.set_defaults(func=command_inverse_trace_smt)


def command_inverse_trace_smt(args):
    from theorems.inverse_trace_smt import native_instance, run_experiment
    instance = json.loads(args.input.read_text()) if args.input else native_instance(args.bits, args.seed, args.target_mode)
    result = run_experiment(instance, prefix_seed=args.seed ^ 0x9e3779b9, full=args.full,
                            timeout_ms=args.timeout_ms, resource_limit=args.resource_limit,
                            pipeline=args.pipeline)
    payload = json.dumps(result, indent=2)+"\n"
    if args.write:
        path = args.output if args.output.is_absolute() else args.root/args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        print(payload, end="")
    return 0


def add_inverse_trace_genus_zero(subparsers):
    parser = subparsers.add_parser("inverse-trace-genus-zero", help="Expected-polynomial genus-zero norm search for trace-affine targets")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--bits", type=int, default=17)
    parser.add_argument("--bit", type=int, default=8)
    parser.add_argument("--c", type=int, help="Nonzero trace slope")
    parser.add_argument("--d0", type=int, default=0, help="Trace offset")
    parser.add_argument("--seed", type=int, default=1030)
    parser.add_argument("--allocation-seed", type=int, default=1031)
    parser.add_argument("--max-trials", type=int, default=32)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("research/classical_baselines/inverse_trace_genus_zero.json"))
    parser.set_defaults(func=command_inverse_trace_genus_zero)


def command_inverse_trace_genus_zero(args):
    from theorems.inverse_trace_genus_zero import run_experiment, trace_bit_instance
    if args.input:
        instance = json.loads(args.input.read_text())
        if args.c is None:
            raise ValueError("--c (nonzero trace slope) required when supplying custom --input")
        c = args.c
        d0 = args.d0
    else:
        instance, default_c, default_d0 = trace_bit_instance(args.bits, args.bit)
        c = args.c if args.c is not None else default_c
        d0 = args.d0 if args.d0 != 0 else default_d0
    result = run_experiment(instance, c=c, d0=d0, seed=args.seed,
                            allocation_seed=args.allocation_seed, max_trials=args.max_trials)
    payload = json.dumps(result, indent=2) + "\n"
    if args.write:
        path = args.output if args.output.is_absolute() else args.root / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload)
    print(payload, end="")
    return 0



def add_audit(subparsers) -> None:
    audit = subparsers.add_parser("audit", help="Regenerate research artifacts and validate the registry.")
    audit.add_argument("--output-dir", type=Path, default=Path("research"))
    audit.add_argument("--refresh-arxiv", action="store_true")
    audit.add_argument("--overwrite-registry", action="store_true")
    audit.set_defaults(func=command_audit)


def command_audit(args: argparse.Namespace) -> int:
    from qsearch import (
        CANDIDATES_PATH,
        EXPERIMENTS_PATH,
        NEGATIVE_RESULTS_PATH,
        build_agenda,
        import_legacy_negative_results,
        initialize_seed_registry,
        validate_registry,
        write_literature_index,
        write_outputs,
        write_problem_ontology,
        write_research_audit,
    )
    root = args.root.resolve()
    output_dir = args.output_dir
    agenda = build_agenda(root)
    write_outputs(agenda, output_dir)
    write_research_audit(agenda, root, output_dir)
    write_literature_index(output_dir / "literature_index.json", refresh_arxiv=args.refresh_arxiv)
    write_problem_ontology(output_dir / "problem_ontology.json")
    initialize_seed_registry(overwrite=args.overwrite_registry)
    imported = import_legacy_negative_results(root)
    validation = validate_registry()

    print("Q-Search audit complete")
    print(f"Agenda: {output_dir / 'agenda.json'}")
    print(f"Registry candidates: {CANDIDATES_PATH}")
    print(f"Registry experiments: {EXPERIMENTS_PATH}")
    print(f"Negative results: {NEGATIVE_RESULTS_PATH}")
    print(f"Imported legacy negative results: {imported}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_propose(subparsers) -> None:
    propose = subparsers.add_parser("propose", help="Register proof-gated seed candidates or a candidate JSON file.")
    propose.add_argument("--file", type=Path)
    propose.set_defaults(func=command_propose)


def command_propose(args: argparse.Namespace) -> int:
    from qsearch import (
        CandidateRecord,
        initialize_seed_registry,
        registry_summary,
        upsert_candidate,
    )
    initialize_seed_registry(overwrite=False)
    if args.file:
        payload = json.loads(args.file.read_text())
        candidate = CandidateRecord(**payload)
        upsert_candidate(candidate)
        print(f"Accepted candidate: {candidate.id}")
    else:
        print("Seed proof-gated candidates are registered.")
    print(registry_summary())
    return 0


def add_literature(subparsers) -> None:
    literature = subparsers.add_parser("literature", help="Extract structured mechanism records from seed and optional arXiv literature.")
    literature.add_argument("--output-dir", type=Path, default=Path("research"))
    literature.add_argument("--refresh-arxiv", action="store_true")
    literature.add_argument("--max-arxiv-results", type=int, default=20)
    literature.add_argument("--verbose", action="store_true")
    literature.set_defaults(func=command_literature)


def command_literature(args: argparse.Namespace) -> int:
    from qsearch import write_literature_index, write_literature_records
    write_literature_index(args.output_dir / "literature_index.json", refresh_arxiv=args.refresh_arxiv)
    records = write_literature_records(
        args.output_dir / "literature_records.json",
        refresh_arxiv=args.refresh_arxiv,
        max_arxiv_results=args.max_arxiv_results,
    )
    print(f"Structured literature records: {len(records)}")
    print(f"Literature records: {args.output_dir / 'literature_records.json'}")
    if args.verbose:
        for record in records:
            print(f"- {record['id']} | {record['mechanism']}")
    return 0


def add_hypothesize(subparsers) -> None:
    hypothesize = subparsers.add_parser("hypothesize", help="Generate proof-gated hypotheses from literature and ontology records.")
    hypothesize.add_argument("--refresh-arxiv", action="store_true")
    hypothesize.add_argument("--max-arxiv-results", type=int, default=20)
    hypothesize.set_defaults(func=command_hypothesize)


def command_hypothesize(args: argparse.Namespace) -> int:
    from qsearch import (
        CANDIDATES_PATH,
        REJECTED_CANDIDATES_PATH,
        hypothesize_from_literature,
        initialize_seed_registry,
        validate_registry,
        write_literature_records,
    )
    initialize_seed_registry(overwrite=False)
    write_literature_records(
        Path("research/literature_records.json"),
        refresh_arxiv=args.refresh_arxiv,
        max_arxiv_results=args.max_arxiv_results,
    )
    result = hypothesize_from_literature(refresh_arxiv=args.refresh_arxiv, max_arxiv_results=args.max_arxiv_results)
    validation = validate_registry()
    print("Literature hypothesis generation complete")
    print(f"Accepted candidates: {', '.join(result.accepted) if result.accepted else 'none'}")
    print(f"Rejected candidates: {', '.join(result.rejected) if result.rejected else 'none'}")
    print(f"Generated experiments: {', '.join(result.experiments) if result.experiments else 'none'}")
    print(f"Candidate registry: {CANDIDATES_PATH}")
    print(f"Rejected registry: {REJECTED_CANDIDATES_PATH}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_hidden_shift(subparsers) -> None:
    hidden_shift = subparsers.add_parser("hidden-shift", help="Run hidden-shift/DHSP phase-family audits and sieve baselines.")
    hidden_shift.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,kloosterman_trace,legendre_symbol,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2,noisy_cubic_chirp",
    )
    hidden_shift.add_argument("--min-bits", type=int, default=5)
    hidden_shift.add_argument("--max-bits", type=int, default=8)
    hidden_shift.add_argument("--shift", type=int, default=7)
    hidden_shift.add_argument("--sieve-samples", type=int, default=2048)
    hidden_shift.add_argument("--sample-count", type=int)
    hidden_shift.add_argument("--seed", type=int, default=0)
    hidden_shift.add_argument("--no-registry", action="store_true")
    hidden_shift.set_defaults(func=command_hidden_shift)


def command_hidden_shift(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_dcp_sample_workbench,
        write_hidden_shift_workbench,
        write_recursive_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_workbench(
        families=families,
        min_bits=args.min_bits,
        max_bits=args.max_bits,
        shift=args.shift,
        sieve_samples=args.sieve_samples,
        seed=args.seed,
        sample_count=args.sample_count,
        write_registry=not args.no_registry,
    )
    dcp_payload = write_dcp_sample_workbench(
        sample_count=args.sieve_samples,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    decoder_payload = write_recursive_decoder_report(
        n_values=(max(4, args.max_bits),),
        trials_per_size=3,
        samples_per_stage=args.sieve_samples,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Hidden-shift/DHSP workbench complete")
    print("Artifact: research/phase_workbench/hidden_shift_audit.json")
    print(f"Family audits: {len(payload['family_audits'])}")
    print(f"Table-free exact value-query controls: {len(payload['value_query_controls'])}; no phase-state access is assumed")
    print(f"Summary: {payload['summary']}")
    print(
        "Legacy idealized phase-label trace: "
        f"v2={payload['sieve_baseline']['best_two_adic_valuation']}/"
        f"{payload['sieve_baseline']['target_two_adic_valuation']} "
        f"from {payload['sieve_baseline']['initial_states']} labels"
    )
    print(
        "DCP state-sample baseline: "
        f"trials={dcp_payload['headline_metrics']['trial_count']} "
        f"evaluator_queries={dcp_payload['headline_metrics']['evaluator_query_count']} "
        f"postselection_gap={dcp_payload['headline_metrics']['postselection_optimism_gap']} "
        f"full_decodes={dcp_payload['headline_metrics']['full_hidden_reflection_decode_count']}"
    )
    print("DCP artifact: research/phase_workbench/dcp_sample_native_sieve.json")
    print(
        "Recursive DCP decoder: "
        f"full_recoveries={decoder_payload['headline_metrics']['empirical_full_recovery_count']}/"
        f"{decoder_payload['headline_metrics']['recursive_trial_count']} "
        f"proved_failure_bounds={decoder_payload['headline_metrics']['proved_full_failure_bound_count']}"
    )
    print("Decoder artifact: research/phase_workbench/dcp_recursive_decoder.json")
    print(
        "Phase-state trace: "
        f"strategy={payload['phase_state_trace']['strategy']} "
        f"v2={payload['phase_state_trace']['best_two_adic_valuation']}/"
        f"{payload['phase_state_trace']['target_two_adic_valuation']} "
        f"survivors={payload['phase_state_trace']['final_state_count']}"
    )
    print(f"Falsifiers triggered: {len(payload['falsifiers_triggered'])}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_collective_observables(subparsers) -> None:
    collective_observables = subparsers.add_parser(
        "collective-observables",
        help="Run adversarial collective-observable search on coset/nonabelian graph-pair frontiers.",
    )
    collective_observables.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cycle-vs-chorded-cycle")
    collective_observables.add_argument("--tuple-cap", type=int, default=120_000)
    collective_observables.add_argument("--no-registry", action="store_true")
    collective_observables.add_argument("--verbose", action="store_true")
    collective_observables.set_defaults(func=command_collective_observables)


def command_collective_observables(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_collective_observable_search,
    )
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_collective_observable_search(
        pair_ids=pair_ids,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Collective-observable search complete")
    print("Artifact: research/coset_workbench/collective_observable_search.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Observables: {payload['headline_metrics']['observable_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['boundary_status']}")
            for record in audit["observable_records"]:
                print(
                    f"  {record['observable_name']} | {record['status']} | "
                    f"registers={record['register_count']} shadow={record['classical_shadow']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_tensor_observables(subparsers) -> None:
    tensor_observables = subparsers.add_parser(
        "tensor-observables",
        help="Audit graphlet/homomorphism tensor observables against classical small-pattern-count shadows.",
    )
    tensor_observables.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cfi-k6-parity-twist,cycle-vs-chorded-cycle")
    tensor_observables.add_argument("--tuple-cap", type=int, default=1_000_000)
    tensor_observables.add_argument("--no-registry", action="store_true")
    tensor_observables.add_argument("--verbose", action="store_true")
    tensor_observables.set_defaults(func=command_tensor_observables)


def command_tensor_observables(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_graphlet_tensor_observables,
    )
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_graphlet_tensor_observables(
        pair_ids=pair_ids,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Graphlet tensor observable audit complete")
    print("Artifact: research/coset_workbench/graphlet_tensor_observables.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Observables: {payload['headline_metrics']['observable_count']}")
    print(f"Classical-shadow collapses: {payload['headline_metrics']['classical_shadow_collapse_count']}")
    print(f"Boundary pairs: {payload['headline_metrics']['boundary_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['status']}")
            for record in audit["records"]:
                print(
                    f"  {record['observable_name']} | {record['status']} | "
                    f"bond={record['bond_dimension']} shadow={record['classical_shadow']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_gm_switching(subparsers) -> None:
    gm_switching = subparsers.add_parser(
        "gm-switching",
        aliases=["godsil-mckay"],
        help="Search Godsil-McKay switched cospectral graph rows and attack them with classical baselines.",
    )
    gm_switching.add_argument("--no-registry", action="store_true")
    gm_switching.add_argument("--verbose", action="store_true")
    gm_switching.set_defaults(func=command_gm_switching)


def command_gm_switching(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_godsil_mckay_search
    initialize_seed_registry(overwrite=False)
    payload = write_godsil_mckay_search(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Godsil-McKay switching search complete")
    print("Artifact: research/coset_workbench/godsil_mckay_switching_search.json")
    print(f"Families: {payload['headline_metrics']['family_count']}")
    print(f"Rows: {payload['headline_metrics']['row_count']}")
    print(f"Non-isomorphic cospectral rows: {payload['headline_metrics']['nonisomorphic_cospectral_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_row_count']}")
    print(f"Survivor rows: {payload['headline_metrics']['survivor_row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for family in payload["family_records"]:
            print(f"- {family['spec']['id']} | {family['status']} | checked={family['subsets_checked']}")
            for record in family["records"]:
                distinguishing = [item["name"] for item in record["baselines"] if item["distinguishes"]]
                print(f"  {record['id']} | {record['status']} | distinguishes={','.join(distinguishing) or 'none'}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_cfi_scaling(subparsers) -> None:
    cfi_scaling = subparsers.add_parser(
        "cfi-scaling",
        help="Probe CFI parity scaling boundaries for coset-state collective-measurement experiments.",
    )
    cfi_scaling.add_argument("--base-sizes", default="4,5,6,7")
    cfi_scaling.add_argument("--wl2-pair-cap", type=int, default=10_000)
    cfi_scaling.add_argument("--wl-tuple-cap", type=int, default=100_000)
    cfi_scaling.add_argument("--graphlet-tuple-cap", type=int, default=1_000_000)
    cfi_scaling.add_argument("--no-registry", action="store_true")
    cfi_scaling.add_argument("--verbose", action="store_true")
    cfi_scaling.set_defaults(func=command_cfi_scaling)


def command_cfi_scaling(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_cfi_scaling_probe,
    )
    initialize_seed_registry(overwrite=False)
    base_sizes = parse_int_csv(args.base_sizes)
    payload = write_cfi_scaling_probe(
        base_sizes=base_sizes,
        wl2_pair_cap=args.wl2_pair_cap,
        wl_tuple_cap=args.wl_tuple_cap,
        graphlet_tuple_cap=args.graphlet_tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI scaling probe complete")
    print("Artifact: research/coset_workbench/cfi_scaling_probe.json")
    print(f"Base sizes: {payload['base_sizes']}")
    print(f"Boundary rows: {payload['headline_metrics']['boundary_record_count']}")
    print(f"3-WL skips: {payload['headline_metrics']['wl3_skipped_count']}")
    print(f"Graphlet skips: {payload['headline_metrics']['graphlet4_skipped_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- K{record['base_size']} n={record['vertex_count']} | {record['status']} | "
                f"wl3={'eval' if record['wl3_evaluated'] else 'skip'} "
                f"graphlet4={'eval' if record['graphlet4_evaluated'] else 'skip'}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_cfi_base_search(subparsers) -> None:
    cfi_base_search = subparsers.add_parser(
        "cfi-base-search",
        help="Search non-complete CFI base families and attack them with individualized-WL baselines.",
    )
    cfi_base_search.add_argument("--base-ids", default="complete-k5,triangular-prism,cube-q3,mobius-ladder-8,petersen,heawood-like-14")
    cfi_base_search.add_argument("--max-individualization", type=int, default=3)
    cfi_base_search.add_argument("--tuple-cap", type=int, default=40_000)
    cfi_base_search.add_argument("--exact-vertex-cap", type=int, default=50)
    cfi_base_search.add_argument("--no-registry", action="store_true")
    cfi_base_search.add_argument("--verbose", action="store_true")
    cfi_base_search.set_defaults(func=command_cfi_base_search)


def command_cfi_base_search(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_cfi_base_family_search
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_cfi_base_family_search(
        base_ids=base_ids,
        max_individualization=args.max_individualization,
        tuple_cap=args.tuple_cap,
        exact_vertex_cap=args.exact_vertex_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI base-family search complete")
    print("Artifact: research/coset_workbench/cfi_base_family_search.json")
    print(f"Bases: {payload['headline_metrics']['base_count']}")
    print(f"Individualized-WL dequantized: {payload['headline_metrics']['individualized_wl_dequantized_count']}")
    print(f"Proof-debt survivors: {payload['headline_metrics']['proof_debt_survivor_count']}")
    print(f"Finite survivors: {payload['headline_metrics']['finite_survivor_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base']['id']} cfi_n={record['cfi_vertex_count']} | {record['status']} | "
                f"first_indiv={record['first_individualized_separator']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_cfi_parity_solver(subparsers) -> None:
    cfi_parity_solver = subparsers.add_parser(
        "cfi-parity-solver",
        help="Run the promised complete-CFI gadget parity decoder as a structural dequantization baseline.",
    )
    cfi_parity_solver.add_argument("--base-sizes", default="4,5,6,7,8")
    cfi_parity_solver.add_argument("--seed", type=int, default=2718)
    cfi_parity_solver.add_argument("--no-shuffle", action="store_true")
    cfi_parity_solver.add_argument("--no-registry", action="store_true")
    cfi_parity_solver.add_argument("--verbose", action="store_true")
    cfi_parity_solver.set_defaults(func=command_cfi_parity_solver)


def command_cfi_parity_solver(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_cfi_parity_solver_report,
    )
    initialize_seed_registry(overwrite=False)
    base_sizes = parse_int_csv(args.base_sizes)
    payload = write_cfi_parity_solver_report(
        base_sizes=base_sizes,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI parity solver complete")
    print("Artifact: research/coset_workbench/cfi_parity_solver.json")
    print(f"Base sizes: {payload['base_sizes']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Ambiguous controls: {payload['headline_metrics']['ambiguous_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- K{record['base_size']} n={record['vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_cfi_structural_decoder(subparsers) -> None:
    cfi_structural_decoder = subparsers.add_parser(
        "cfi-structural-decoder",
        help="Run the promised regular-CFI gadget parity decoder across non-complete base families.",
    )
    cfi_structural_decoder.add_argument("--base-ids", default="complete-k5,triangular-prism,cube-q3,mobius-ladder-8,petersen,heawood-like-14")
    cfi_structural_decoder.add_argument("--seed", type=int, default=9041)
    cfi_structural_decoder.add_argument("--no-shuffle", action="store_true")
    cfi_structural_decoder.add_argument("--no-registry", action="store_true")
    cfi_structural_decoder.add_argument("--verbose", action="store_true")
    cfi_structural_decoder.set_defaults(func=command_cfi_structural_decoder)


def command_cfi_structural_decoder(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_cfi_structural_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_cfi_structural_decoder_report(
        base_ids=base_ids,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI structural decoder complete")
    print("Artifact: research/coset_workbench/cfi_structural_decoder.json")
    print(f"Bases: {payload['base_ids']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Ambiguous rows: {payload['headline_metrics']['ambiguous_count']}")
    print(f"Failed rows: {payload['headline_metrics']['failed_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base_id']} n={record['cfi_vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_cfi_irregular_decoder(subparsers) -> None:
    cfi_irregular_decoder = subparsers.add_parser(
        "cfi-irregular-decoder",
        help="Run the degree-separated irregular-CFI structural parity decoder.",
    )
    cfi_irregular_decoder.add_argument("--base-ids", default="complete-bipartite-3-5,complete-bipartite-4-5,complete-tripartite-2-3-4")
    cfi_irregular_decoder.add_argument("--seed", type=int, default=13001)
    cfi_irregular_decoder.add_argument("--no-shuffle", action="store_true")
    cfi_irregular_decoder.add_argument("--no-registry", action="store_true")
    cfi_irregular_decoder.add_argument("--verbose", action="store_true")
    cfi_irregular_decoder.set_defaults(func=command_cfi_irregular_decoder)


def command_cfi_irregular_decoder(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_irregular_cfi_structural_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_irregular_cfi_structural_decoder_report(
        base_ids=base_ids,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Irregular CFI structural decoder complete")
    print("Artifact: research/coset_workbench/cfi_irregular_structural_decoder.json")
    print(f"Bases: {payload['base_ids']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Proof debt rows: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Degree-separated rows: {payload['headline_metrics']['degree_separated_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base']['id']} n={record['cfi_vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_cfi_bipartite_decoder(subparsers) -> None:
    cfi_bipartite_decoder = subparsers.add_parser(
        "cfi-bipartite-decoder",
        help="Run the bipartition-based CFI structural decoder, including non-degree-separated stress rows.",
    )
    cfi_bipartite_decoder.add_argument("--base-ids", default="complete-k4,mobius-ladder-8,complete-bipartite-3-5,prism-degree4-hub")
    cfi_bipartite_decoder.add_argument("--seed", type=int, default=17011)
    cfi_bipartite_decoder.add_argument("--no-shuffle", action="store_true")
    cfi_bipartite_decoder.add_argument("--no-registry", action="store_true")
    cfi_bipartite_decoder.add_argument("--verbose", action="store_true")
    cfi_bipartite_decoder.set_defaults(func=command_cfi_bipartite_decoder)


def command_cfi_bipartite_decoder(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_bipartite_cfi_structural_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_bipartite_cfi_structural_decoder_report(
        base_ids=base_ids,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Bipartite CFI structural decoder complete")
    print("Artifact: research/coset_workbench/cfi_bipartite_structural_decoder.json")
    print(f"Bases: {payload['base_ids']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Proof debt rows: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Non-degree-separated rows: {payload['headline_metrics']['non_degree_separated_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base']['id']} n={record['cfi_vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_individualized_wl(subparsers) -> None:
    individualized_wl = subparsers.add_parser(
        "individualized-wl",
        help="Run individualization-refinement WL baselines for graph/coset rows.",
    )
    individualized_wl.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cycle-vs-chorded-cycle")
    individualized_wl.add_argument("--max-individualization", type=int, default=3)
    individualized_wl.add_argument("--tuple-cap", type=int, default=40_000)
    individualized_wl.add_argument("--no-registry", action="store_true")
    individualized_wl.add_argument("--verbose", action="store_true")
    individualized_wl.set_defaults(func=command_individualized_wl)


def command_individualized_wl(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_individualized_wl_baseline,
    )
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_individualized_wl_baseline(
        pair_ids=pair_ids,
        max_individualization=args.max_individualization,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Individualized-WL baseline complete")
    print("Artifact: research/coset_workbench/individualized_wl_baseline.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Dequantized pairs: {payload['headline_metrics']['dequantized_pair_count']}")
    print(f"Survivor pairs: {payload['headline_metrics']['survivor_pair_count']}")
    print(f"Proof-debt pairs: {payload['headline_metrics']['proof_debt_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['status']}")
            for record in audit["records"]:
                print(
                    f"  t={record['individualization_size']} | {record['status']} | "
                    f"count={record['tuple_count']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_individualized_tensors(subparsers) -> None:
    individualized_tensors = subparsers.add_parser(
        "individualized-tensors",
        help="Run individualized rooted tensor/graphlet baselines for graph/coset rows.",
    )
    individualized_tensors.add_argument(
        "--pairs",
        default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cfi-k6-parity-twist,cycle-vs-chorded-cycle",
    )
    individualized_tensors.add_argument("--max-root-size", type=int, default=2)
    individualized_tensors.add_argument("--tuple-cap", type=int, default=3_000_000)
    individualized_tensors.add_argument("--no-registry", action="store_true")
    individualized_tensors.add_argument("--verbose", action="store_true")
    individualized_tensors.set_defaults(func=command_individualized_tensors)


def command_individualized_tensors(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_individualized_tensor_observables,
    )
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_individualized_tensor_observables(
        pair_ids=pair_ids,
        max_root_size=args.max_root_size,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Individualized rooted tensor baseline complete")
    print("Artifact: research/coset_workbench/individualized_tensor_observables.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Dequantized pairs: {payload['headline_metrics']['dequantized_pair_count']}")
    print(f"Survivor pairs: {payload['headline_metrics']['survivor_pair_count']}")
    print(f"Proof-debt pairs: {payload['headline_metrics']['proof_debt_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['status']}")
            for record in audit["records"]:
                print(
                    f"  roots={record['root_size']} | {record['status']} | "
                    f"extensions={record['extension_tuple_count']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_representation_obstructions(subparsers) -> None:
    representation_obstructions = subparsers.add_parser(
        "representation-obstructions",
        help="Audit symmetric-group irrep growth and strong-Fourier no-go pressure.",
    )
    representation_obstructions.add_argument("--n-values", default="4,5,6,8,10,12,14,16")
    representation_obstructions.add_argument("--no-registry", action="store_true")
    representation_obstructions.add_argument("--verbose", action="store_true")
    representation_obstructions.set_defaults(func=command_representation_obstructions)


def command_representation_obstructions(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_representation_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_representation_obstruction_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Representation obstruction report complete")
    print("Artifact: research/representation/symmetric_group_obstructions.json")
    print(f"n values: {payload['n_values']}")
    print(f"No-go pressure rows: {payload['headline_metrics']['no_go_pressure_count']}")
    print(f"Min low-dimensional mass: {payload['headline_metrics']['min_low_dimension_mass']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} partitions={record['partition_count']} | {record['status']} | "
                f"low-dim-mass={record['low_dimension_mass']:.4g} balanced={record['balanced_shape_mass']:.4g}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_weak_fourier(subparsers) -> None:
    weak_fourier = subparsers.add_parser(
        "weak-fourier",
        help="Audit weak Fourier irrep-label signal for symmetric-group involution hidden subgroups.",
    )
    weak_fourier.add_argument("--n-values", default="6,8,10,12,14,16")
    weak_fourier.add_argument("--no-registry", action="store_true")
    weak_fourier.add_argument("--verbose", action="store_true")
    weak_fourier.set_defaults(func=command_weak_fourier)


def command_weak_fourier(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_weak_fourier_signal_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_weak_fourier_signal_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Weak Fourier signal audit complete")
    print("Artifact: research/representation/weak_fourier_involution_signal.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Nearly Plancherel: {payload['headline_metrics']['near_plancherel_count']}")
    print(f"Small signal: {payload['headline_metrics']['small_signal_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} {record['involution_type']} r={record['transposition_count']} | "
                f"{record['status']} | tv={record['total_variation_from_plancherel']:.4g} "
                f"low-frac={record['low_dimension_signal_fraction']:.4g}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_diagram_hidden_subalgebra_coset_no_go(subparsers) -> None:
    diagram_hidden_subalgebra_coset_no_go = subparsers.add_parser(
        "diagram-hidden-subalgebra-coset-no-go",
        help="Exp Diagram Hidden Subalgebra Coset No Go",
    )
    diagram_hidden_subalgebra_coset_no_go.set_defaults(func=command_diagram_hidden_subalgebra_coset_no_go)


def command_diagram_hidden_subalgebra_coset_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_diagram_hidden_subalgebra_coset_no_go
    report = write_diagram_hidden_subalgebra_coset_no_go()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_diagram_multiplicity_source_mass_gate(subparsers) -> None:
    diagram_multiplicity_source_mass_gate = subparsers.add_parser(
        "diagram-multiplicity-source-mass-gate",
        help="Exp Diagram Multiplicity Source Mass Gate",
    )
    diagram_multiplicity_source_mass_gate.set_defaults(func=command_diagram_multiplicity_source_mass_gate)


def command_diagram_multiplicity_source_mass_gate(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_diagram_multiplicity_source_mass_gate
    report = write_diagram_multiplicity_source_mass_gate()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_all_codimension_baba_no_go(subparsers) -> None:
    all_codimension_baba_no_go = subparsers.add_parser(
        "all-codimension-baba-no-go",
        help="Exp Code Self Dual Wreath All Codimension Baba No Go",
    )
    all_codimension_baba_no_go.set_defaults(func=command_all_codimension_baba_no_go)


def command_all_codimension_baba_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_all_codimension_baba_no_go_report
    report = write_all_codimension_baba_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_class_uniform_commutator_moment(subparsers) -> None:
    class_uniform_commutator_moment = subparsers.add_parser(
        "class-uniform-commutator-moment",
        help="Exp Code Self Dual Wreath Class Uniform Commutator Moment",
    )
    class_uniform_commutator_moment.set_defaults(func=command_class_uniform_commutator_moment)


def command_class_uniform_commutator_moment(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_class_uniform_commutator_moment_report
    report = write_class_uniform_commutator_moment_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_codimension_one_commuting_compression_no_go(subparsers) -> None:
    codimension_one_commuting_compression_no_go = subparsers.add_parser(
        "codimension-one-commuting-compression-no-go",
        help="Exp Code Self Dual Wreath Codimension One Commuting Compression No Go",
    )
    codimension_one_commuting_compression_no_go.set_defaults(func=command_codimension_one_commuting_compression_no_go)


def command_codimension_one_commuting_compression_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_codimension_one_commuting_compression_no_go_report
    report = write_codimension_one_commuting_compression_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_codimension_two_universal_no_go(subparsers) -> None:
    codimension_two_universal_no_go = subparsers.add_parser(
        "codimension-two-universal-no-go",
        help="Exp Code Self Dual Wreath Codimension Two Universal No Go",
    )
    codimension_two_universal_no_go.set_defaults(func=command_codimension_two_universal_no_go)


def command_codimension_two_universal_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_codimension_two_universal_no_go_report
    report = write_codimension_two_universal_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_commutator_sector_filter_no_go(subparsers) -> None:
    commutator_sector_filter_no_go = subparsers.add_parser(
        "commutator-sector-filter-no-go",
        help="Exp Code Self Dual Wreath Commutator Sector Filter No Go",
    )
    commutator_sector_filter_no_go.set_defaults(func=command_commutator_sector_filter_no_go)


def command_commutator_sector_filter_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_commutator_sector_filter_no_go_report
    report = write_commutator_sector_filter_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_component_block_coherence_boundary(subparsers) -> None:
    component_block_coherence_boundary = subparsers.add_parser(
        "component-block-coherence-boundary",
        help="Exp Code Self Dual Wreath Component Block Coherence Boundary",
    )
    component_block_coherence_boundary.set_defaults(func=command_component_block_coherence_boundary)


def command_component_block_coherence_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_block_coherence_boundary_report
    report = write_component_block_coherence_boundary_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_component_coefficient_projection_normal_form(subparsers) -> None:
    component_coefficient_projection_normal_form = subparsers.add_parser(
        "component-coefficient-projection-normal-form",
        help="Exp Code Self Dual Wreath Component Coefficient Projection Normal Form",
    )
    component_coefficient_projection_normal_form.set_defaults(func=command_component_coefficient_projection_normal_form)


def command_component_coefficient_projection_normal_form(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_coefficient_projection_normal_form_report
    report = write_component_coefficient_projection_normal_form_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_component_noncrossing_lower_bound(subparsers) -> None:
    component_noncrossing_lower_bound = subparsers.add_parser(
        "component-noncrossing-lower-bound",
        help="Exp Code Self Dual Wreath Component Noncrossing Lower Bound",
    )
    component_noncrossing_lower_bound.set_defaults(func=command_component_noncrossing_lower_bound)


def command_component_noncrossing_lower_bound(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_noncrossing_lower_bound_report
    report = write_component_noncrossing_lower_bound_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_full_support_pair_budget_no_go(subparsers) -> None:
    full_support_pair_budget_no_go = subparsers.add_parser(
        "full-support-pair-budget-no-go",
        help="Exp Code Self Dual Wreath Full Support Pair Budget No Go",
    )
    full_support_pair_budget_no_go.set_defaults(func=command_full_support_pair_budget_no_go)


def command_full_support_pair_budget_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_full_support_pair_budget_no_go_report
    report = write_full_support_pair_budget_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_information_set_universal_no_go(subparsers) -> None:
    information_set_universal_no_go = subparsers.add_parser(
        "information-set-universal-no-go",
        help="Exp Code Self Dual Wreath Information Set Universal No Go",
    )
    information_set_universal_no_go.set_defaults(func=command_information_set_universal_no_go)


def command_information_set_universal_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_information_set_universal_no_go_report
    report = write_information_set_universal_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_interleaved_even_parity_no_go(subparsers) -> None:
    interleaved_even_parity_no_go = subparsers.add_parser(
        "interleaved-even-parity-no-go",
        help="Exp Code Self Dual Wreath Interleaved Even Parity No Go",
    )
    interleaved_even_parity_no_go.set_defaults(func=command_interleaved_even_parity_no_go)


def command_interleaved_even_parity_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_interleaved_even_parity_no_go_report
    report = write_interleaved_even_parity_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_interleaved_leaf_pressure_no_go(subparsers) -> None:
    interleaved_leaf_pressure_no_go = subparsers.add_parser(
        "interleaved-leaf-pressure-no-go",
        help="Exp Code Self Dual Wreath Interleaved Leaf Pressure No Go",
    )
    interleaved_leaf_pressure_no_go.set_defaults(func=command_interleaved_leaf_pressure_no_go)


def command_interleaved_leaf_pressure_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_interleaved_leaf_pressure_no_go_report
    report = write_interleaved_leaf_pressure_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_interleaved_product_lift_no_go(subparsers) -> None:
    interleaved_product_lift_no_go = subparsers.add_parser(
        "interleaved-product-lift-no-go",
        help="Exp Code Self Dual Wreath Interleaved Product Lift No Go",
    )
    interleaved_product_lift_no_go.set_defaults(func=command_interleaved_product_lift_no_go)


def command_interleaved_product_lift_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_interleaved_product_lift_no_go_report
    report = write_interleaved_product_lift_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_nonsystematic_incidence_lattice_bound(subparsers) -> None:
    nonsystematic_incidence_lattice_bound = subparsers.add_parser(
        "nonsystematic-incidence-lattice-bound",
        help="Exp Code Self Dual Wreath Nonsystematic Incidence Lattice Bound",
    )
    nonsystematic_incidence_lattice_bound.set_defaults(func=command_nonsystematic_incidence_lattice_bound)


def command_nonsystematic_incidence_lattice_bound(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_nonsystematic_incidence_lattice_bound_report
    report = write_nonsystematic_incidence_lattice_bound_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_nonsystematic_mod_four_no_go(subparsers) -> None:
    nonsystematic_mod_four_no_go = subparsers.add_parser(
        "nonsystematic-mod-four-no-go",
        help="Exp Code Self Dual Wreath Nonsystematic Mod Four No Go",
    )
    nonsystematic_mod_four_no_go.set_defaults(func=command_nonsystematic_mod_four_no_go)


def command_nonsystematic_mod_four_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_nonsystematic_mod_four_no_go_report
    report = write_nonsystematic_mod_four_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_nonsystematic_pair_witness_collapse(subparsers) -> None:
    nonsystematic_pair_witness_collapse = subparsers.add_parser(
        "nonsystematic-pair-witness-collapse",
        help="Exp Code Self Dual Wreath Nonsystematic Pair Witness Collapse",
    )
    nonsystematic_pair_witness_collapse.set_defaults(func=command_nonsystematic_pair_witness_collapse)


def command_nonsystematic_pair_witness_collapse(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_nonsystematic_pair_witness_collapse_report
    report = write_nonsystematic_pair_witness_collapse_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_nonsystematic_twisted_star_no_go(subparsers) -> None:
    nonsystematic_twisted_star_no_go = subparsers.add_parser(
        "nonsystematic-twisted-star-no-go",
        help="Exp Code Self Dual Wreath Nonsystematic Twisted Star No Go",
    )
    nonsystematic_twisted_star_no_go.set_defaults(func=command_nonsystematic_twisted_star_no_go)


def command_nonsystematic_twisted_star_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_nonsystematic_twisted_star_no_go_report
    report = write_nonsystematic_twisted_star_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_plancherel_target_word_collapse(subparsers) -> None:
    plancherel_target_word_collapse = subparsers.add_parser(
        "plancherel-target-word-collapse",
        help="Exp Code Self Dual Wreath Plancherel Target Word Collapse",
    )
    plancherel_target_word_collapse.set_defaults(func=command_plancherel_target_word_collapse)


def command_plancherel_target_word_collapse(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_plancherel_target_word_collapse_report
    report = write_plancherel_target_word_collapse_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_poisson_ridge_word_mixture(subparsers) -> None:
    poisson_ridge_word_mixture = subparsers.add_parser(
        "poisson-ridge-word-mixture",
        help="Exp Code Self Dual Wreath Poisson Ridge Word Mixture",
    )
    poisson_ridge_word_mixture.set_defaults(func=command_poisson_ridge_word_mixture)


def command_poisson_ridge_word_mixture(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_poisson_ridge_word_mixture_report
    report = write_poisson_ridge_word_mixture_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_same_support_triangle_target_no_go(subparsers) -> None:
    same_support_triangle_target_no_go = subparsers.add_parser(
        "same-support-triangle-target-no-go",
        help="Exp Code Self Dual Wreath Same Support Triangle Target No Go",
    )
    same_support_triangle_target_no_go.set_defaults(func=command_same_support_triangle_target_no_go)


def command_same_support_triangle_target_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_same_support_triangle_target_no_go_report
    report = write_same_support_triangle_target_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_separator_defect_frontier(subparsers) -> None:
    separator_defect_frontier = subparsers.add_parser(
        "separator-defect-frontier",
        help="Exp Code Self Dual Wreath Separator Defect Frontier",
    )
    separator_defect_frontier.set_defaults(func=command_separator_defect_frontier)


def command_separator_defect_frontier(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_separator_defect_frontier_report
    report = write_separator_defect_frontier_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_systematic_stopping_core_no_go(subparsers) -> None:
    systematic_stopping_core_no_go = subparsers.add_parser(
        "systematic-stopping-core-no-go",
        help="Exp Code Self Dual Wreath Systematic Stopping Core No Go",
    )
    systematic_stopping_core_no_go.set_defaults(func=command_systematic_stopping_core_no_go)


def command_systematic_stopping_core_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_systematic_stopping_core_no_go_report
    report = write_systematic_stopping_core_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_translated_parity_commutator_no_go(subparsers) -> None:
    translated_parity_commutator_no_go = subparsers.add_parser(
        "translated-parity-commutator-no-go",
        help="Exp Code Self Dual Wreath Translated Parity Commutator No Go",
    )
    translated_parity_commutator_no_go.set_defaults(func=command_translated_parity_commutator_no_go)


def command_translated_parity_commutator_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_translated_parity_commutator_no_go_report
    report = write_translated_parity_commutator_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_semidirect_hms_transfer_boundary(subparsers) -> None:
    semidirect_hms_transfer_boundary = subparsers.add_parser(
        "semidirect-hms-transfer-boundary",
        help="Exp Semidirect Hms Transfer Boundary",
    )
    semidirect_hms_transfer_boundary.set_defaults(func=command_semidirect_hms_transfer_boundary)


def command_semidirect_hms_transfer_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_semidirect_hms_transfer_boundary
    report = write_semidirect_hms_transfer_boundary()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_cfi_code_reduction(subparsers) -> None:
    cfi_code_reduction = subparsers.add_parser(
        "cfi-code-reduction",
        help="Certify the faithful CFI graph-to-code reduction and run legal graph-side dequantization attacks.",
    )
    cfi_code_reduction.add_argument(
        "--bases",
        default="complete-k5,triangular-prism,cube-q3,mobius-ladder-8,petersen,heawood-like-14",
    )
    cfi_code_reduction.add_argument("--seed", type=int, default=14_071)
    cfi_code_reduction.add_argument("--no-registry", action="store_true")
    cfi_code_reduction.add_argument("--verbose", action="store_true")
    cfi_code_reduction.set_defaults(func=command_cfi_code_reduction)


def command_cfi_code_reduction(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_cfi_graph_code_reduction
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.bases.split(",") if item.strip()]
    payload = write_cfi_graph_code_reduction(
        base_ids=base_ids or None,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Faithful CFI graph-to-code reduction audit complete")
    print("Artifact: research/code_equivalence/cfi_code_reduction.json")
    print(f"Theorem directions certified: {metrics['theorem_direction_count']}")
    print(f"Graph recoveries verified: {metrics['recovery_verified_count']}")
    print(f"Equivalent controls verified: {metrics['equivalent_control_verified_count']}")
    print(f"Promised-family dequantizations: {metrics['promised_decoder_dequantized_count']}")
    print(f"Transferred GI proof debt: {metrics['transferred_gi_proof_debt_count']}")
    print(f"Positive quantum evidence: {metrics['positive_quantum_evidence_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base_id']} | [{record['code_dimension']},{record['code_length']}] | "
                f"{record['status']} | decoder={record['promised_decoder_recovers_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dequantize(subparsers) -> None:
    dequantize = subparsers.add_parser("dequantize", help="Scan candidates/results for classical dequantization risks.")
    dequantize.add_argument("--verbose", action="store_true")
    dequantize.set_defaults(func=command_dequantize)


def command_dequantize(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_dequantization_report
    initialize_seed_registry(overwrite=False)
    report = write_dequantization_report()
    validation = validate_registry()
    print("Dequantization report complete")
    print("Report: research/dequantization_report.json")
    print("Attack matrix: research/dequantization_attack_matrix.json")
    print("Registry: research/registry/dequantization_checks.json")
    print(f"Findings: {report['finding_count']}")
    print(f"Blocking findings: {report['blocking_finding_count']}")
    matrix_summary = report.get("attack_legality_matrix", {}).get("summary", {})
    if matrix_summary:
        print(
            "Attack matrix: "
            f"{matrix_summary.get('attack_row_count', 0)} attack rows, "
            f"{matrix_summary.get('query_model_row_count', 0)} query-model rows, "
            f"{matrix_summary.get('random_sample_undersampled_gap_count', 0)} undersampled sampled-access gaps"
        )
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for finding in report["findings"]:
            print(f"- {finding['severity']} | {finding['target_id']} | {finding['evidence']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_baselines(subparsers) -> None:
    baselines = subparsers.add_parser("baselines", help="Run classical baseline sweeps across hidden-shift query/sample budgets.")
    baselines.add_argument("--families", default="bent_quadratic_f2,masked_quadratic_f2,quartic_character,kloosterman_trace,noisy_cubic_chirp,fp2_quadratic_form,mm_majority_bent_f2")
    baselines.add_argument("--n-values", default="5,6,7,8")
    baselines.add_argument("--sample-counts", default="4,8,16,32,64,128")
    baselines.add_argument("--shift", type=int, default=7)
    baselines.add_argument("--seed", type=int, default=0)
    baselines.add_argument("--no-registry", action="store_true")
    baselines.add_argument("--verbose", action="store_true")
    baselines.set_defaults(func=command_baselines)


def command_baselines(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_hidden_shift_baselines,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_baselines(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Classical baseline sweep complete")
    print("Artifact: research/classical_baselines/hidden_shift_baselines.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"random={summary['random_sample_recovery_count']} "
                f"evaluator={summary['low_complexity_evaluator_recovery_count']} "
                f"collision_survival={summary['collision_scale_survival_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_query_lower_bounds(subparsers) -> None:
    query_lower_bounds = subparsers.add_parser(
        "query-lower-bounds",
        aliases=["hidden-shift-lower-bounds"],
        help="Probe hidden-shift query/time lower-bound gaps with exhaustive candidate fingerprints.",
    )
    query_lower_bounds.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,kloosterman_trace,legendre_symbol,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2,noisy_cubic_chirp",
    )
    query_lower_bounds.add_argument("--n-values", default="5,6,7,8")
    query_lower_bounds.add_argument("--sample-counts", default="2,4,8,16,32,64")
    query_lower_bounds.add_argument("--shift", type=int, default=7)
    query_lower_bounds.add_argument("--seed", type=int, default=0)
    query_lower_bounds.add_argument("--trials", type=int, default=5)
    query_lower_bounds.add_argument("--no-registry", action="store_true")
    query_lower_bounds.add_argument("--verbose", action="store_true")
    query_lower_bounds.set_defaults(func=command_query_lower_bounds)


def command_query_lower_bounds(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_hidden_shift_query_lower_bounds,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_query_lower_bounds(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        trials=args.trials,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Hidden-shift query lower-bound probe complete")
    print("Artifact: research/classical_baselines/hidden_shift_query_lower_bounds.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"poly-fingerprints={summary['poly_sample_unique_count']} "
                f"chosen-poly={summary.get('chosen_query_poly_unique_count', 0)} "
                f"agreement-ceilings={summary.get('agreement_query_ceiling_count', 0)} "
                f"overlap-collisions={summary['overlap_scale_collision_count']} "
                f"undersampled={summary['undersampled_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_learnability(subparsers) -> None:
    learnability = subparsers.add_parser("learnability", help="Run low-degree and sparse-structure learnability baselines.")
    learnability.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,noisy_cubic_chirp,kloosterman_trace,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2",
    )
    learnability.add_argument("--n-values", default="5,6,7,8")
    learnability.add_argument("--samples", type=int, default=128)
    learnability.add_argument("--seed", type=int, default=0)
    learnability.add_argument("--no-registry", action="store_true")
    learnability.add_argument("--verbose", action="store_true")
    learnability.set_defaults(func=command_learnability)


def command_learnability(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_learnability_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_learnability_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        samples=args.samples,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Learnability baseline report complete")
    print("Artifact: research/classical_baselines/learnability_baselines.json")
    print(f"Records: {payload['record_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"dequantized={summary['dequantized_low_degree_count']} "
                f"unresolved={summary['high_degree_or_unresolved_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_fourier_learnability(subparsers) -> None:
    fourier_learnability = subparsers.add_parser(
        "fourier-learnability",
        aliases=["compressibility"],
        help="Run sparse Fourier and derivative-spectrum compressibility baselines.",
    )
    fourier_learnability.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,noisy_cubic_chirp,kloosterman_trace,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2",
    )
    fourier_learnability.add_argument("--n-values", default="5,6,7,8")
    fourier_learnability.add_argument("--sample-counts", default="4,8,16,32,64,128")
    fourier_learnability.add_argument("--no-registry", action="store_true")
    fourier_learnability.add_argument("--verbose", action="store_true")
    fourier_learnability.set_defaults(func=command_fourier_learnability)


def command_fourier_learnability(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_fourier_compressibility_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_fourier_compressibility_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Fourier compressibility baseline report complete")
    print("Artifact: research/classical_baselines/fourier_compressibility_baselines.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"evaluator={summary['explicit_evaluator_sparse_recovery_count']} "
                f"sample={summary['random_sample_sparse_recovery_count']} "
                f"derivative={summary['derivative_sparse_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_character_shift(subparsers) -> None:
    character_shift = subparsers.add_parser(
        "character-shift",
        help="Run multiplicative-character hidden-shift sample/elimination baselines.",
    )
    character_shift.add_argument("--families", default="legendre_symbol,quartic_character")
    character_shift.add_argument("--n-values", default="5,6,7,8")
    character_shift.add_argument("--sample-counts", default="2,4,8,16,32")
    character_shift.add_argument("--shift", type=int, default=7)
    character_shift.add_argument("--seed", type=int, default=0)
    character_shift.add_argument("--no-registry", action="store_true")
    character_shift.add_argument("--verbose", action="store_true")
    character_shift.set_defaults(func=command_character_shift)


def command_character_shift(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_character_shift_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_shift_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character shift baseline report complete")
    print("Artifact: research/classical_baselines/character_shift_baselines.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"poly-sample={summary['unique_by_poly_samples_count']} "
                f"exhaustive={summary['exhaustive_time_only_count']} "
                f"insufficient={summary['insufficient_sample_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_character_decoders(subparsers) -> None:
    character_decoders = subparsers.add_parser(
        "character-decoders",
        help="Search non-exhaustive decoders for multiplicative-character hidden shifts.",
    )
    character_decoders.add_argument("--families", default="legendre_symbol,quartic_character")
    character_decoders.add_argument("--n-values", default="5,6,7,8")
    character_decoders.add_argument("--sample-counts", default="4,8,16,32")
    character_decoders.add_argument("--shift", type=int, default=7)
    character_decoders.add_argument("--seed", type=int, default=0)
    character_decoders.add_argument("--no-registry", action="store_true")
    character_decoders.add_argument("--verbose", action="store_true")
    character_decoders.set_defaults(func=command_character_decoders)


def command_character_decoders(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_character_decoder_search_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_decoder_search_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character decoder search complete")
    print("Artifact: research/classical_baselines/character_decoder_search.json")
    print(f"Attempts: {payload['attempt_count']}")
    print(f"Probes: {payload['probe_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"poly-style={summary['non_exhaustive_success_count']} "
                f"pair-ratio={summary.get('pair_ratio_filter_success_count', 0)} "
                f"algebraic-degree={summary.get('algebraic_degree_exponential_success_count', 0)} "
                f"exhaustive={summary['exhaustive_success_count']} "
                f"invariant={summary['shift_invariant_probe_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_character_lower_bound(subparsers) -> None:
    character_lower_bound = subparsers.add_parser(
        "character-lower-bound",
        aliases=["character-decoding-lower-bound"],
        help="Build the multiplicative-character sample/decode lower-bound ledger.",
    )
    character_lower_bound.add_argument("--families", default="legendre_symbol,quartic_character")
    character_lower_bound.add_argument("--n-values", default="5,6,7,8")
    character_lower_bound.add_argument("--sample-counts", default="4,8,16,32")
    character_lower_bound.add_argument("--shift", type=int, default=7)
    character_lower_bound.add_argument("--seed", type=int, default=0)
    character_lower_bound.add_argument("--trials", type=int, default=5)
    character_lower_bound.add_argument("--no-registry", action="store_true")
    character_lower_bound.add_argument("--verbose", action="store_true")
    character_lower_bound.set_defaults(func=command_character_lower_bound)


def command_character_lower_bound(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_character_shift_lower_bound_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_shift_lower_bound_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        trials=args.trials,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character lower-bound ledger complete")
    print("Artifact: research/classical_baselines/character_shift_lower_bound.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"sample={summary['sample_fingerprint_count']} "
                f"chosen={summary['chosen_query_fingerprint_count']} "
                f"pair-ratio={summary.get('pair_ratio_filter_success_count', 0)} "
                f"max-pair-exp={summary.get('max_pair_ratio_operation_exponent_per_bit', 0.0):.2f} "
                f"gcd={summary['full_degree_gcd_success_count']} "
                f"max-gcd-exp={summary['max_gcd_operation_exponent_per_bit']:.2f}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_character_moments(subparsers) -> None:
    character_moments = subparsers.add_parser(
        "character-moments",
        aliases=["character-moment-obstruction"],
        help="Check exact low-degree moment obstructions for multiplicative-character shifts.",
    )
    character_moments.add_argument("--families", default="legendre_symbol,quartic_character")
    character_moments.add_argument("--n-values", default="5,6,7,8")
    character_moments.add_argument("--no-registry", action="store_true")
    character_moments.add_argument("--verbose", action="store_true")
    character_moments.set_defaults(func=command_character_moments)


def command_character_moments(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_character_moment_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_moment_obstruction_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character moment obstruction complete")
    print("Artifact: research/classical_baselines/character_moment_obstruction.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"min-first-nonzero={summary['minimum_first_nonzero_degree']} "
                f"blocked={summary['all_rows_block_low_degree_moments']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_character_query_info(subparsers) -> None:
    character_query_info = subparsers.add_parser(
        "character-query-info",
        aliases=["character-query-information"],
        help="Audit information-theoretic query ceilings for multiplicative-character shifts.",
    )
    character_query_info.add_argument("--families", default="legendre_symbol,quartic_character")
    character_query_info.add_argument("--n-values", default="5,6,7,8")
    character_query_info.add_argument("--failure-probability", type=float, default=0.01)
    character_query_info.add_argument("--no-registry", action="store_true")
    character_query_info.add_argument("--verbose", action="store_true")
    character_query_info.set_defaults(func=command_character_query_info)


def command_character_query_info(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_character_query_information_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_query_information_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        failure_probability=args.failure_probability,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character query information ceiling complete")
    print("Artifact: research/classical_baselines/character_query_information.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"max-union-bound-q={summary['max_union_bound_queries']} "
                f"max-q/logp={summary['max_query_ceiling_over_log2_prime']:.2f} "
                f"killed={summary['query_lower_bound_killed_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_character_complexity(subparsers) -> None:
    character_complexity = subparsers.add_parser(
        "character-complexity",
        help="Audit shifted-character classical upper bounds, preprocessing, advice, and reduction debt.",
    )
    character_complexity.add_argument("--families", default="legendre_symbol,quartic_character")
    character_complexity.add_argument("--n-values", default="5,6,7,8,9,10")
    character_complexity.add_argument("--shift", type=int, default=7)
    character_complexity.add_argument("--max-prefix-factor", type=int, default=8)
    character_complexity.add_argument("--no-registry", action="store_true")
    character_complexity.add_argument("--verbose", action="store_true")
    character_complexity.set_defaults(func=command_character_complexity)


def command_character_complexity(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_character_shift_complexity_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_shift_complexity_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        shift=args.shift,
        max_prefix_factor=args.max_prefix_factor,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Multiplicative-character complexity/preprocessing audit complete")
    print("Artifact: research/classical_baselines/character_shift_complexity.json")
    print(f"Rows: {metrics['preprocessing_row_count']}")
    print(f"Fixed-prefix online decodes: {metrics['fixed_prefix_decode_success_count']}")
    print(f"Uniform polylog decoders: {metrics['uniform_polylog_classical_decoder_count']}")
    print(f"Natural reductions: {metrics['natural_problem_reduction_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for row in payload["preprocessing_records"]:
            print(
                f"- {row['family_id']} n={row['n_bits']} p={row['prime']} | {row['status']} | "
                f"prefix={row['first_globally_unique_prefix']} | prefix/n={row['prefix_over_n_bits']} | "
                f"preprocess={row['preprocessing_operations']} | online={row['online_lookup_operations']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_family_triage(subparsers) -> None:
    family_triage = subparsers.add_parser("family-triage", help="Triage hidden-shift phase families across baseline artifacts.")
    family_triage.add_argument("--no-registry", action="store_true")
    family_triage.add_argument("--verbose", action="store_true")
    family_triage.set_defaults(func=command_family_triage)


def command_family_triage(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_phase_family_triage
    payload = write_phase_family_triage(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Phase-family triage complete")
    print("Artifact: research/phase_workbench/phase_family_triage.json")
    print(f"Families: {payload['family_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"blocker={record['primary_blocker']} | action={record['next_action']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_phase_naturalness(subparsers) -> None:
    phase_naturalness = subparsers.add_parser(
        "phase-naturalness",
        help="Audit hidden-shift phase families for artificial masks and unsupported descriptions.",
    )
    phase_naturalness.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,noisy_cubic_chirp,kloosterman_trace,quartic_character,legendre_symbol,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2",
    )
    phase_naturalness.add_argument("--n-values", default="5,6,7,8")
    phase_naturalness.add_argument("--no-registry", action="store_true")
    phase_naturalness.add_argument("--verbose", action="store_true")
    phase_naturalness.set_defaults(func=command_phase_naturalness)


def command_phase_naturalness(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_phase_family_naturalness_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_phase_family_naturalness_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Phase-family naturalness audit complete")
    print("Artifact: research/phase_workbench/phase_family_naturalness.json")
    print(f"Records: {payload['record_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"artificial={summary['artificial_record_count']} natural={summary['natural_record_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_trace_functions(subparsers) -> None:
    trace_functions = subparsers.add_parser(
        "trace-functions",
        help="Search natural finite-field rational trace-function hidden-shift families.",
    )
    trace_functions.add_argument(
        "--families",
        default="trace_kloosterman_x_plus_inv,trace_quadratic_plus_inv,trace_cubic_plus_inv,trace_two_pole,trace_cubic_two_pole",
    )
    trace_functions.add_argument("--n-values", default="5,6,7,8")
    trace_functions.add_argument("--sample-counts", default="8,16,32,64")
    trace_functions.add_argument("--shift", type=int, default=7)
    trace_functions.add_argument("--seed", type=int, default=0)
    trace_functions.add_argument("--no-registry", action="store_true")
    trace_functions.add_argument("--verbose", action="store_true")
    trace_functions.set_defaults(func=command_trace_functions)


def command_trace_functions(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_trace_function_search_report,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_trace_function_search_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Trace-function hidden-shift search complete")
    print("Artifact: research/phase_workbench/trace_function_search.json")
    print(f"Records: {payload['record_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"algebraic={summary.get('algebraic_decoder_count', 0)} "
                f"sample={summary['sample_dequantized_count']} sparse={summary['sparse_spectrum_count']} "
                f"low_degree={summary['low_degree_count']} unresolved={summary['unresolved_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_run(subparsers) -> None:
    run = subparsers.add_parser("run", help="Run a registry experiment by id.")
    run.add_argument("experiment_id", nargs="?")
    run.add_argument("--all-supported", action="store_true")
    run.add_argument("--list-supported", action="store_true")
    run.add_argument("--verbose", action="store_true")
    run.set_defaults(func=command_run)


def command_run(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        run_experiment,
        run_supported_experiments,
        supported_experiment_ids,
        validate_registry,
    )
    initialize_seed_registry(overwrite=False)
    if args.list_supported:
        print("Supported experiment IDs")
        print("========================")
        for experiment_id in supported_experiment_ids():
            print(experiment_id)
        return 0
    if args.all_supported:
        results = run_supported_experiments()
    else:
        if not args.experiment_id:
            raise SystemExit("run requires EXPERIMENT_ID unless --all-supported is set")
        results = [run_experiment(args.experiment_id)]
    validation = validate_registry()
    print("Experiment runner complete")
    for result in results:
        print(f"{result.experiment_id} -> {result.result_id} [{result.status}]")
        if args.verbose:
            print(f"  {result.summary}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_run_next(subparsers) -> None:
    run_next = subparsers.add_parser("run-next", help="Select and run the next highest-priority registry experiment.")
    run_next.add_argument("--dry-run", action="store_true")
    run_next.set_defaults(func=command_run_next)


def command_run_next(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        run_next_experiment,
        select_next_experiment,
        validate_registry,
    )
    initialize_seed_registry(overwrite=False)
    if args.dry_run:
        selection = select_next_experiment()
        print("Next experiment selection")
        print("=========================")
        print(f"Experiment: {selection.experiment_id}")
        print(f"Score: {selection.score}")
        print(f"Supported: {selection.supported}")
        print(f"Reason: {selection.reason}")
        return 0
    selection, result = run_next_experiment()
    validation = validate_registry()
    print("Next experiment run complete")
    print(f"Selected: {selection.experiment_id} (score={selection.score})")
    print(f"Reason: {selection.reason}")
    print(f"Result: {result.result_id} [{result.status}]")
    print("Run history: research/experiment_run_history.json")
    print("Trends: research/experiment_trends.json")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_trends(subparsers) -> None:
    trends = subparsers.add_parser("trends", help="Build append-only experiment trend summaries.")
    trends.add_argument("--verbose", action="store_true")
    trends.set_defaults(func=command_trends)


def command_trends(args: argparse.Namespace) -> int:
    from qsearch import write_experiment_trends
    report = write_experiment_trends()
    print("Experiment trends complete")
    print("Artifact: research/experiment_trends.json")
    print(f"History records: {report['history_count']}")
    print(f"Trend records: {report['trend_count']}")
    if args.verbose:
        for trend in report["trends"]:
            print(
                f"- {trend['experiment_id']} runs={trend['run_count']} "
                f"latest={trend['latest_status']} blockers={trend['blocking_run_count']}"
            )
    return 0


def add_proof_routes(subparsers) -> None:
    proof_routes = subparsers.add_parser("proof-routes", help="Audit scoped proof dependencies and pinned evidence; not mathematical proof checking.")
    proof_routes.add_argument("--initialize", action="store_true", help="Create the curated initial manifest once; never overwrite existing evidence pins.")
    proof_routes.set_defaults(func=command_proof_routes)


def command_proof_routes(args: argparse.Namespace) -> int:
    from qsearch import initialize_proof_routes, write_proof_route_audit
    if args.initialize:
        initialize_proof_routes()
    report = write_proof_route_audit()
    print(f"Proof-route contracts: {report['claim_count']}")
    print(f"Unsupported assertions: {report['unsupported_assertion_count']}")
    print(f"Unresolved claims: {report['unresolved_claim_count']}")
    print("Contract audit only; mathematical truth and speedup claims are not certified.")
    return int(report["unsupported_assertion_count"] > 0)


def add_proofs(subparsers) -> None:
    proofs = subparsers.add_parser("proofs", help="Build per-candidate proof-obligation status records.")
    proofs.add_argument("--verbose", action="store_true")
    proofs.set_defaults(func=command_proofs)


def command_proofs(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_proof_status_report
    initialize_seed_registry(overwrite=False)
    report = write_proof_status_report()
    validation = validate_registry()
    print("Proof status report complete")
    print("Report: research/proof_status_report.json")
    print("Proof debt: research/proof_debt_report.json")
    print("Registry: research/registry/proof_status.json")
    print(f"Proof statuses: {report['proof_status_count']}")
    print(f"Blocking statuses: {report['blocking_status_count']}")
    print(f"Needs evidence: {report['needs_evidence_count']}")
    print(
        "Proof debt: "
        f"{report.get('proof_debt_count', 0)} debts, "
        f"{report.get('lemma_count', 0)} lemmas, "
        f"{report.get('reduction_edge_count', 0)} reduction edges, "
        f"{report.get('counterexample_search_count', 0)} counterexample searches"
    )
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in report["records"]:
            if record["status"] != "text-present":
                print(f"- {record['candidate_id']} {record['obligation_id']} {record['status']}: {record['evidence']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_reductions(subparsers) -> None:
    reductions = subparsers.add_parser(
        "reductions",
        help="Build typed reduction edges and reject routes with unproved model, complexity, or family coverage.",
    )
    reductions.add_argument("--max-verbose-issues", type=int, default=4)
    reductions.add_argument("--verbose", action="store_true")
    reductions.set_defaults(func=command_reductions)


def command_reductions(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_reduction_contract_audit,
        write_reduction_ledger,
    )
    initialize_seed_registry(overwrite=False)
    report = write_reduction_ledger()
    contract_audit = write_reduction_contract_audit()
    validation = validate_registry()
    print("Certificate-gated reduction ledger complete")
    print("Artifact: research/reductions/reduction_ledger.json")
    print("Registry: research/registry/reductions.json")
    print(f"Edges: {report['edge_count']} ({report['accepted_edge_count']} accepted, {report['blocked_edge_count']} blocked)")
    print(f"Routes: {report['route_count']} ({report['complete_route_count']} complete, {report['blocked_route_count']} blocked)")
    print(f"Blocked candidates: {report['blocked_candidate_count']}")
    print(
        f"Exact interface audits: {contract_audit['route_audit_count']} "
        f"({contract_audit['blocked_interface_count']} blocked)"
    )
    print(f"Status: {report['status']}")
    print(f"Summary: {report['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for route in report["routes"]:
            print(
                f"- {route['candidate_id']} | {route['id']} | {route['status']} | "
                f"blocking={len(route['blocking_edge_ids'])}"
            )
        for edge in report["edges"]:
            if edge["accepted"]:
                continue
            certificate = edge["certificate"]
            print(f"  {certificate['id']} | issues={len(edge['issues'])}")
            for issue in edge["issues"][: args.max_verbose_issues]:
                print(f"    {issue['field']}: {issue['message']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_reduction_contracts(subparsers) -> None:
    reduction_contracts = subparsers.add_parser(
        "reduction-contracts",
        help="Audit candidate interfaces against exact primary-source reduction theorem contracts.",
    )
    reduction_contracts.add_argument("--max-verbose-checks", type=int, default=5)
    reduction_contracts.add_argument("--verbose", action="store_true")
    reduction_contracts.set_defaults(func=command_reduction_contracts)


def command_reduction_contracts(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        write_reduction_contract_audit,
        write_theorem_catalog,
    )
    initialize_seed_registry(overwrite=False)
    catalog = write_theorem_catalog()
    report = write_reduction_contract_audit()
    print("Exact reduction theorem-contract audit complete")
    print("Catalog: research/reductions/theorem_contracts.json")
    print("Audit: research/reductions/interface_audit.json")
    print(f"Theorem contracts: {catalog['contract_count']}")
    print(f"Route interfaces: {report['route_audit_count']}")
    print(f"Blocked interfaces: {report['blocked_interface_count']}")
    print(f"Access mismatches: {report['access_mismatch_count']}")
    print(f"Family-coverage mismatches: {report['family_coverage_mismatch_count']}")
    print(f"Status: {report['status']}")
    print(f"Summary: {report['summary']}")
    if args.verbose:
        for audit in report["audits"]:
            failed = [check for check in audit["checks"] if not check["passed"]]
            print(
                f"- {audit['candidate_id']} | {audit['route_id']} | {audit['status']} | "
                f"failed={len(failed)} debt={audit['proof_debt_score']}"
            )
            for check in failed[: args.max_verbose_checks]:
                print(f"  {check['axis']}: {check['burden']}")
    return 0


def add_proof_queue(subparsers) -> None:
    proof_queue = subparsers.add_parser("proof-queue", help="Build a prioritized proof-debt work queue with commands and kill criteria.")
    proof_queue.add_argument("--max-items", type=int, default=30)
    proof_queue.add_argument("--verbose", action="store_true")
    proof_queue.set_defaults(func=command_proof_queue)


def command_proof_queue(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, write_proof_status_report, write_proof_work_queue
    initialize_seed_registry(overwrite=False)
    write_proof_status_report()
    report = write_proof_work_queue(max_items=args.max_items)
    print("Proof work queue complete")
    print("Artifact: research/proof_work_queue.json")
    print(f"Items: {report['work_item_count']}")
    print(f"Action clusters: {report['action_cluster_count']}")
    print(f"Ready to run: {report['ready_to_run_count']}")
    print(f"Theory/mixed: {report['theory_or_mixed_count']}")
    print(f"Status: {report['status']}")
    top = report.get("top_action_cluster") or report.get("top_work_item")
    if top:
        top_id = top.get("id", "cluster")
        print(f"Top: {top_id} | {top['work_type']} | score={top['priority_score']}")
        print(f"Command: {top['recommended_command']}")
    if args.verbose:
        for cluster in report["action_clusters"]:
            print(
                f"* cluster {cluster['work_type']} | score={cluster['priority_score']} | "
                f"candidates={cluster['affected_candidate_count']}"
            )
            print(f"  command: {cluster['recommended_command']}")
        for item in report["items"]:
            print(f"- {item['id']} | {item['work_type']} | score={item['priority_score']} | {item['status']}")
            print(f"  action: {item['recommended_action']}")
            print(f"  command: {item['recommended_command']}")
    return 0


def add_sweep(subparsers) -> None:
    sweep = subparsers.add_parser("sweep", help="Run parameter sweeps for executable workbenches.")
    sweep.add_argument("--kind", choices=["hidden-shift"], default="hidden-shift")
    sweep.add_argument("--n-values", default="5,6,7,8")
    sweep.add_argument("--sample-counts", default="256,512,1024,2048")
    sweep.add_argument("--families", default="bent_quadratic_f2,masked_quadratic_f2,quartic_character,kloosterman_trace,noisy_cubic_chirp")
    sweep.add_argument("--shift", type=int, default=7)
    sweep.add_argument("--seed", type=int, default=0)
    sweep.add_argument("--no-registry", action="store_true")
    sweep.set_defaults(func=command_sweep)


def command_sweep(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_hidden_shift_sweep,
    )
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_sweep(
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        families=families,
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Scaling sweep complete")
    print("Artifact: research/scaling/hidden_shift_sweep.json")
    print(f"Rows: {len(payload['rows'])}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_conjectures(subparsers) -> None:
    conjectures = subparsers.add_parser("conjectures", help="Build candidate conjecture, assumption, reduction, and blocker records.")
    conjectures.add_argument("--verbose", action="store_true")
    conjectures.set_defaults(func=command_conjectures)


def command_conjectures(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_conjecture_report
    initialize_seed_registry(overwrite=False)
    report = write_conjecture_report()
    validation = validate_registry()
    print("Conjecture report complete")
    print("Report: research/conjecture_report.json")
    print("Registry: research/registry/conjectures.json")
    print(f"Conjectures: {report['conjecture_count']}")
    print(f"Blocked: {report['blocked_count']}")
    print(f"Needs evidence: {report['needs_evidence_count']}")
    print(f"Active: {report['active_count']}")
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for conjecture in report["conjectures"]:
            print(f"- {conjecture['id']} | {conjecture['status']} | blockers={len(conjecture['blocking_evidence'])}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_mutate(subparsers) -> None:
    mutate = subparsers.add_parser("mutate", help="Generate blocker-driven mutation proposals without accepting them as candidates.")
    mutate.add_argument("--verbose", action="store_true")
    mutate.set_defaults(func=command_mutate)


def command_mutate(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_mutation_report
    initialize_seed_registry(overwrite=False)
    report = write_mutation_report()
    validation = validate_registry()
    print("Mutation report complete")
    print("Report: research/mutation_report.json")
    print("Registry: research/registry/mutation_proposals.json")
    print(f"Proposals: {report['proposal_count']}")
    print(f"Reduction-interface repairs: {report.get('interface_repair_proposal_count', 0)}")
    print(f"Proposal-only (not proof-gate eligible): {report.get('proposal_only_count', 0)}")
    print(
        "Proof-gate preflights: "
        f"{report.get('accepted_preflight_count', 0)} accepted, "
        f"{report.get('rejected_preflight_count', 0)} rejected, "
        f"{report.get('not_generated_preflight_count', 0)} proposal-only"
    )
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for proposal in report["proposals"]:
            print(f"- {proposal['id']} | {proposal['mutation_type']} | {proposal['rationale']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_quarantine_invalid(subparsers) -> None:
    quarantine_invalid = subparsers.add_parser(
        "quarantine-invalid",
        help="Move mutation candidates with failed exact access contracts out of the accepted registry.",
    )
    quarantine_invalid.add_argument("--verbose", action="store_true")
    quarantine_invalid.set_defaults(func=command_quarantine_invalid)


def command_quarantine_invalid(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        quarantine_exact_access_invalid_mutations,
        validate_registry,
        write_reduction_contract_audit,
        write_reduction_ledger,
    )
    initialize_seed_registry(overwrite=False)
    report = quarantine_exact_access_invalid_mutations()
    write_reduction_ledger()
    write_reduction_contract_audit()
    validation = validate_registry()
    print("Exact-interface quarantine complete")
    print("Report: research/quarantine_report.json")
    print(f"Quarantined candidates: {report['quarantined_candidate_count']}")
    print(f"Removed experiments: {report['removed_experiment_count']}")
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for candidate_id in report["quarantined_candidate_ids"]:
            print(f"- {candidate_id}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_blockers(subparsers) -> None:
    blockers = subparsers.add_parser("blockers", help="Cluster dequantization, proof-debt, and negative-result blockers.")
    blockers.add_argument("--verbose", action="store_true")
    blockers.set_defaults(func=command_blockers)


def command_blockers(args: argparse.Namespace) -> int:
    from qsearch import write_blocker_taxonomy
    report = write_blocker_taxonomy()
    print("Blocker taxonomy complete")
    print("Artifact: research/blocker_taxonomy.json")
    print(f"Evidence rows: {report['evidence_count']}")
    print(f"Blocker classes: {report['blocker_class_count']}")
    print(f"Top blocker: {report['top_blocker_class']}")
    print(f"Top actionable blocker: {report['top_actionable_blocker_class']}")
    print(f"Status: {report['status']}")
    if args.verbose:
        for item in report["classes"]:
            print(
                f"- {item['blocker_class']} score={item['priority_score']} "
                f"evidence={item['evidence_count']} action={item['required_action']}"
            )
    return 0


def add_frontiers(subparsers) -> None:
    frontiers = subparsers.add_parser("frontiers", help="Rank research frontiers from current blockers and artifacts.")
    frontiers.add_argument("--verbose", action="store_true")
    frontiers.set_defaults(func=command_frontiers)


def command_frontiers(args: argparse.Namespace) -> int:
    from qsearch import write_frontier_map
    report = write_frontier_map()
    print("Research frontier map complete")
    print("Artifact: research/frontier_map.json")
    print(f"Frontiers: {report['frontier_count']}")
    print(f"Top frontier: {report['top_frontier']}")
    print(f"Status: {report['status']}")
    if args.verbose:
        for frontier in report["frontiers"]:
            print(
                f"- {frontier['frontier_id']} score={frontier['priority_score']} "
                f"status={frontier['status']} next={frontier['next_experiment']}"
            )
    return 0


def add_query_models(subparsers) -> None:
    query_models = subparsers.add_parser("query-models", help="Build candidate-level query-model and lower-bound obligation records.")
    query_models.add_argument("--verbose", action="store_true")
    query_models.set_defaults(func=command_query_models)


def command_query_models(args: argparse.Namespace) -> int:
    from qsearch import write_query_model_ledger
    report = write_query_model_ledger()
    print("Query-model ledger complete")
    print("Artifact: research/query_model_ledger.json")
    print(f"Candidates: {report['candidate_count']}")
    print(f"Blocking records: {report['blocking_record_count']}")
    print(f"Status: {report['status']}")
    if args.verbose:
        for record in report["records"]:
            print(
                f"- {record['candidate_id']} | {record['candidate_kind']} | {record['status']} | "
                f"attacks={len(record['attacks_that_must_be_excluded'])} obligations={len(record['lower_bound_obligations'])}"
            )
    return 0


def add_ingest_papers(subparsers) -> None:
    ingest_papers = subparsers.add_parser("ingest-papers", help="Extract mechanism records from local .tex/.txt/.md/.pdf papers.")
    ingest_papers.add_argument("paths", nargs="*", type=Path)
    ingest_papers.add_argument("--arxiv-id", action="append", default=[])
    ingest_papers.add_argument("--verbose", action="store_true")
    ingest_papers.set_defaults(func=command_ingest_papers)


def command_ingest_papers(args: argparse.Namespace) -> int:
    from qsearch import write_paper_ingestion, write_paper_ingestion_with_arxiv
    records = (
        write_paper_ingestion_with_arxiv(args.paths, args.arxiv_id)
        if args.arxiv_id
        else write_paper_ingestion(args.paths)
    )
    print("Paper ingestion complete")
    print("Artifact: research/paper_ingestion.json")
    print("No-go index: research/literature_no_go_index.json")
    print(f"Records: {len(records)}")
    if args.verbose:
        for record in records:
            print(f"- {record['id']} | {record['mechanism']} | {record['problem_family']}")
    return 0


def add_planted_qary_cube_basis_coordinate_bridge(subparsers) -> None:
    planted_qary_cube_basis_coordinate_bridge = subparsers.add_parser(
        "planted-qary-cube-basis-coordinate-bridge",
        help="Audit planted q-ary centered-RREF basis coordinate bounds, q-independent cube shifts, and deterministic prime/residue selection.",
    )
    planted_qary_cube_basis_coordinate_bridge.add_argument("--no-write", action="store_true")
    planted_qary_cube_basis_coordinate_bridge.set_defaults(func=command_planted_qary_cube_basis_coordinate_bridge)


def command_planted_qary_cube_basis_coordinate_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_cube_basis_coordinate_bridge import (
        build_planted_qary_cube_basis_coordinate_bridge_report,
        write_planted_qary_cube_basis_coordinate_bridge_report,
    )

    payload = (
        build_planted_qary_cube_basis_coordinate_bridge_report()
        if args.no_write
        else write_planted_qary_cube_basis_coordinate_bridge_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_lattice_qft_cutoff_phase_fidelity_bridge(subparsers) -> None:
    lattice_qft_cutoff_phase_fidelity_bridge = subparsers.add_parser(
        "lattice-qft-cutoff-phase-fidelity-bridge",
        help="Audit exact banded dyadic QFT cutoff kernels, universal label uniformity, and joint-channel quadrature visibility bounds.",
    )
    lattice_qft_cutoff_phase_fidelity_bridge.add_argument("--no-write", action="store_true")
    lattice_qft_cutoff_phase_fidelity_bridge.set_defaults(func=command_lattice_qft_cutoff_phase_fidelity_bridge)


def command_lattice_qft_cutoff_phase_fidelity_bridge(args: argparse.Namespace) -> int:
    from theorems.lattice_qft_cutoff_phase_fidelity_bridge import (
        build_lattice_qft_cutoff_phase_fidelity_bridge_report,
        write_lattice_qft_cutoff_phase_fidelity_bridge_report,
    )

    payload = (
        build_lattice_qft_cutoff_phase_fidelity_bridge_report()
        if args.no_write
        else write_lattice_qft_cutoff_phase_fidelity_bridge_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_cdkm_adder_sparsity_bridge(subparsers) -> None:
    planted_qary_cdkm_adder_sparsity_bridge = subparsers.add_parser(
        "planted-qary-cdkm-adder-sparsity-bridge",
        help="Audit planted q-ary centered-RREF CDKM adder sparsity, modulus-independent free-column cell widths, and gate compression.",
    )
    planted_qary_cdkm_adder_sparsity_bridge.add_argument("--no-write", action="store_true")
    planted_qary_cdkm_adder_sparsity_bridge.set_defaults(func=command_planted_qary_cdkm_adder_sparsity_bridge)


def command_planted_qary_cdkm_adder_sparsity_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_cdkm_adder_sparsity_bridge import (
        build_planted_qary_cdkm_adder_sparsity_bridge_report,
        write_planted_qary_cdkm_adder_sparsity_bridge_report,
    )

    payload = (
        build_planted_qary_cdkm_adder_sparsity_bridge_report()
        if args.no_write
        else write_planted_qary_cdkm_adder_sparsity_bridge_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_offset_pair_mass_frontier_audit(subparsers) -> None:
    planted_qary_offset_pair_mass_frontier_audit = subparsers.add_parser(
        "planted-qary-offset-pair-mass-frontier-audit",
        help="Audit planted q-ary offset-average pair-mass product bounds and q-independent dyadic (M_box, W) schedules for the 1/ell budget.",
    )
    planted_qary_offset_pair_mass_frontier_audit.add_argument("--no-write", action="store_true")
    planted_qary_offset_pair_mass_frontier_audit.set_defaults(func=command_planted_qary_offset_pair_mass_frontier_audit)


def command_planted_qary_offset_pair_mass_frontier_audit(args: argparse.Namespace) -> int:
    from theorems.planted_qary_offset_pair_mass_frontier_audit import (
        build_planted_qary_offset_pair_mass_frontier_audit_report,
        write_planted_qary_offset_pair_mass_frontier_audit_report,
    )

    payload = (
        build_planted_qary_offset_pair_mass_frontier_audit_report()
        if args.no_write
        else write_planted_qary_offset_pair_mass_frontier_audit_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_classical_attack_threshold_bridge(subparsers) -> None:
    planted_qary_classical_attack_threshold_bridge = subparsers.add_parser(
        "planted-qary-classical-attack-threshold-bridge",
        help="Replay public classical attacks, exact LLL reducedness, polynomial-space RREF and determinant-gap counterexamples.",
    )
    planted_qary_classical_attack_threshold_bridge.add_argument("--no-write", action="store_true")
    planted_qary_classical_attack_threshold_bridge.set_defaults(func=command_planted_qary_classical_attack_threshold_bridge)


def command_planted_qary_classical_attack_threshold_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_classical_attack_threshold_bridge import (
        build_planted_qary_classical_attack_threshold_bridge_report,
        write_planted_qary_classical_attack_threshold_bridge_report,
    )

    payload = (
        build_planted_qary_classical_attack_threshold_bridge_report()
        if args.no_write
        else write_planted_qary_classical_attack_threshold_bridge_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_multiprobe_gl_rank_saturation_bridge(subparsers) -> None:
    planted_qary_multiprobe_gl_rank_saturation_bridge = subparsers.add_parser(
        "planted-qary-multiprobe-gl-rank-saturation-bridge",
        help="Audit planted q-ary multiprobe GL_d(F_q) rank-saturation laws, first-moment indistinguishability, and q-Gaussian rank stratification.",
    )
    planted_qary_multiprobe_gl_rank_saturation_bridge.add_argument("--no-write", action="store_true")
    planted_qary_multiprobe_gl_rank_saturation_bridge.set_defaults(func=command_planted_qary_multiprobe_gl_rank_saturation_bridge)


def command_planted_qary_multiprobe_gl_rank_saturation_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_multiprobe_gl_rank_saturation_bridge import (
        build_planted_qary_multiprobe_gl_rank_saturation_bridge,
        write_planted_qary_multiprobe_gl_rank_saturation_bridge,
    )

    payload = (
        build_planted_qary_multiprobe_gl_rank_saturation_bridge()
        if args.no_write
        else write_planted_qary_multiprobe_gl_rank_saturation_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_coset_shift_fourier_bias_bridge(subparsers) -> None:
    planted_qary_coset_shift_fourier_bias_bridge = subparsers.add_parser(
        "planted-qary-coset-shift-fourier-bias-bridge",
        help="Audit planted q-ary coset-shift QFT phase erasure, off-dual shift invariance, and first-moment equalization on B + a.",
    )
    planted_qary_coset_shift_fourier_bias_bridge.add_argument("--no-write", action="store_true")
    planted_qary_coset_shift_fourier_bias_bridge.set_defaults(func=command_planted_qary_coset_shift_fourier_bias_bridge)


def command_planted_qary_coset_shift_fourier_bias_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_coset_shift_fourier_bias_bridge import (
        build_planted_qary_coset_shift_fourier_bias_bridge,
        write_planted_qary_coset_shift_fourier_bias_bridge,
    )

    payload = (
        build_planted_qary_coset_shift_fourier_bias_bridge()
        if args.no_write
        else write_planted_qary_coset_shift_fourier_bias_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_second_moment_probe_variance_bridge(subparsers) -> None:
    planted_qary_second_moment_probe_variance_bridge = subparsers.add_parser(
        "planted-qary-second-moment-probe-variance-bridge",
        help="Audit planted q-ary second-moment probe variance law, projective-ray covariance localization, and dual-spike concentration.",
    )
    planted_qary_second_moment_probe_variance_bridge.add_argument("--no-write", action="store_true")
    planted_qary_second_moment_probe_variance_bridge.set_defaults(func=command_planted_qary_second_moment_probe_variance_bridge)


def command_planted_qary_second_moment_probe_variance_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_second_moment_probe_variance_bridge import (
        build_planted_qary_second_moment_probe_variance_bridge,
        write_planted_qary_second_moment_probe_variance_bridge,
    )

    payload = (
        build_planted_qary_second_moment_probe_variance_bridge()
        if args.no_write
        else write_planted_qary_second_moment_probe_variance_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_noisy_parity_check_likelihood_bridge(subparsers) -> None:
    planted_qary_noisy_parity_check_likelihood_bridge = subparsers.add_parser(
        "planted-qary-noisy-parity-check-likelihood-bridge",
        help="Audit planted q-ary noisy parity-check weight-power Fourier damping, off-dual noise invariance, and dual minimum-distance scaling.",
    )
    planted_qary_noisy_parity_check_likelihood_bridge.add_argument("--no-write", action="store_true")
    planted_qary_noisy_parity_check_likelihood_bridge.set_defaults(func=command_planted_qary_noisy_parity_check_likelihood_bridge)


def command_planted_qary_noisy_parity_check_likelihood_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_noisy_parity_check_likelihood_bridge import (
        build_planted_qary_noisy_parity_check_likelihood_bridge,
        write_planted_qary_noisy_parity_check_likelihood_bridge,
    )

    payload = (
        build_planted_qary_noisy_parity_check_likelihood_bridge()
        if args.no_write
        else write_planted_qary_noisy_parity_check_likelihood_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_dual_intersection_cascade_bridge(subparsers) -> None:
    planted_qary_dual_intersection_cascade_bridge = subparsers.add_parser(
        "planted-qary-dual-intersection-cascade-bridge",
        help="Audit planted q-ary dual-intersection cascade candidate subspace size law, spurious survivor decay, and oversampling recovery probability.",
    )
    planted_qary_dual_intersection_cascade_bridge.add_argument("--no-write", action="store_true")
    planted_qary_dual_intersection_cascade_bridge.set_defaults(func=command_planted_qary_dual_intersection_cascade_bridge)


def command_planted_qary_dual_intersection_cascade_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_dual_intersection_cascade_bridge import (
        build_planted_qary_dual_intersection_cascade_bridge,
        write_planted_qary_dual_intersection_cascade_bridge,
    )

    payload = (
        build_planted_qary_dual_intersection_cascade_bridge()
        if args.no_write
        else write_planted_qary_dual_intersection_cascade_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_noisy_dual_intersection_false_negative_bridge(subparsers) -> None:
    planted_qary_noisy_dual_intersection_false_negative_bridge = subparsers.add_parser(
        "planted-qary-noisy-dual-intersection-false-negative-bridge",
        help="Audit noisy QFT dual-intersection weight-stratified true-codeword survival, spurious noise-invariance, and primal distance scaling.",
    )
    planted_qary_noisy_dual_intersection_false_negative_bridge.add_argument("--no-write", action="store_true")
    planted_qary_noisy_dual_intersection_false_negative_bridge.set_defaults(func=command_planted_qary_noisy_dual_intersection_false_negative_bridge)


def command_planted_qary_noisy_dual_intersection_false_negative_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_noisy_dual_intersection_false_negative_bridge import (
        build_planted_qary_noisy_dual_intersection_false_negative_bridge,
        write_planted_qary_noisy_dual_intersection_false_negative_bridge,
    )

    payload = (
        build_planted_qary_noisy_dual_intersection_false_negative_bridge()
        if args.no_write
        else write_planted_qary_noisy_dual_intersection_false_negative_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_multiproduct_k_copy_dual_tensor_bridge(subparsers) -> None:
    planted_qary_multiproduct_k_copy_dual_tensor_bridge = subparsers.add_parser(
        "planted-qary-multiproduct-k-copy-dual-tensor-bridge",
        help="Audit planted q-ary K-copy primal-difference shift cancellation, constant-sum dual fiber spectral decomposition, and K-invariant coset purity.",
    )
    planted_qary_multiproduct_k_copy_dual_tensor_bridge.add_argument("--no-write", action="store_true")
    planted_qary_multiproduct_k_copy_dual_tensor_bridge.set_defaults(func=command_planted_qary_multiproduct_k_copy_dual_tensor_bridge)


def command_planted_qary_multiproduct_k_copy_dual_tensor_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_multiproduct_k_copy_dual_tensor_bridge import (
        build_planted_qary_multiproduct_k_copy_dual_tensor_bridge,
        write_planted_qary_multiproduct_k_copy_dual_tensor_bridge,
    )

    payload = (
        build_planted_qary_multiproduct_k_copy_dual_tensor_bridge()
        if args.no_write
        else write_planted_qary_multiproduct_k_copy_dual_tensor_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_planted_qary_punctured_coordinate_projection_bridge(subparsers) -> None:
    planted_qary_punctured_coordinate_projection_bridge = subparsers.add_parser(
        "planted-qary-punctured-coordinate-projection-bridge",
        help="Audit planted q-ary coordinate puncturing bipartite Schmidt spectrum, puncturing-shortening QFT duality, and d_min rank-locking.",
    )
    planted_qary_punctured_coordinate_projection_bridge.add_argument("--no-write", action="store_true")
    planted_qary_punctured_coordinate_projection_bridge.set_defaults(func=command_planted_qary_punctured_coordinate_projection_bridge)


def command_planted_qary_punctured_coordinate_projection_bridge(args: argparse.Namespace) -> int:
    from theorems.planted_qary_punctured_coordinate_projection_bridge import (
        build_planted_qary_punctured_coordinate_projection_bridge,
        write_planted_qary_punctured_coordinate_projection_bridge,
    )

    payload = (
        build_planted_qary_punctured_coordinate_projection_bridge()
        if args.no_write
        else write_planted_qary_punctured_coordinate_projection_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_ternary_cubic_syndrome_twirl_reflection_collapse(subparsers) -> None:
    ternary_cubic_syndrome_twirl_reflection_collapse = subparsers.add_parser(
        "ternary-cubic-syndrome-twirl-reflection-collapse",
        help="Run the ternary cubic/mixed syndrome correction block-convolution and twirl-pinching audit.",
    )
    ternary_cubic_syndrome_twirl_reflection_collapse.add_argument("--no-write", action="store_true")
    ternary_cubic_syndrome_twirl_reflection_collapse.set_defaults(func=command_ternary_cubic_syndrome_twirl_reflection_collapse)


def command_ternary_cubic_syndrome_twirl_reflection_collapse(args: argparse.Namespace) -> int:
    from theorems.ternary_cubic_syndrome_twirl_reflection_collapse import (
        build_ternary_cubic_syndrome_twirl_reflection_collapse_report,
        write_ternary_cubic_syndrome_twirl_reflection_collapse_report,
    )

    payload = (
        build_ternary_cubic_syndrome_twirl_reflection_collapse_report()
        if getattr(args, "no_write", False)
        else write_ternary_cubic_syndrome_twirl_reflection_collapse_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_prime_character_capacity_source(subparsers) -> None:
    prime_character_capacity_source = subparsers.add_parser(
        "prime-character-capacity-source",
        help="Run the prime character capacity source ambiguity accounting and native Fourier filter audit.",
    )
    prime_character_capacity_source.add_argument("--no-write", action="store_true")
    prime_character_capacity_source.add_argument("--json", action="store_true")
    prime_character_capacity_source.set_defaults(func=command_prime_character_capacity_source)


def command_prime_character_capacity_source(args: argparse.Namespace) -> int:
    from theorems.prime_character_capacity_source import run_controls, REPORT
    report = run_controls()
    if not getattr(args, "no_write", False):
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    if getattr(args, "json", False):
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps({"controls": len(report["bounded_physical_controls"]),
                          "large_profiles": len(report["analytic_large_profiles"])}, indent=2))
    return 0


def add_prime_character_finite_readout(subparsers) -> None:
    prime_character_finite_readout = subparsers.add_parser(
        "prime-character-finite-readout",
        help="Run the prime character finite readout radial near-isometry means and tails audit.",
    )
    prime_character_finite_readout.add_argument("--no-write", action="store_true")
    prime_character_finite_readout.add_argument("--json", action="store_true")
    prime_character_finite_readout.set_defaults(func=command_prime_character_finite_readout)


def command_prime_character_finite_readout(args: argparse.Namespace) -> int:
    from theorems.prime_character_finite_readout import run_controls, REPORT
    report = run_controls()
    if not getattr(args, "no_write", False):
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    if getattr(args, "json", False):
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps({"profiles": len(report["fixed_input_profiles"]),
                          "unlicensed_degree_controls": len(report["unlicensed_degree_controls"])}, indent=2))
    return 0


def add_validate(subparsers) -> None:
    validate = subparsers.add_parser("validate", help="Validate candidates and experiments against proof obligations.")
    validate.set_defaults(func=command_validate)


def command_validate(args: argparse.Namespace) -> int:
    from qsearch import validate_registry
    validation = validate_registry()
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["valid"] else 1


def add_list(subparsers) -> None:
    list_cmd = subparsers.add_parser("list", help="List registry records.")
    list_cmd.add_argument(
        "--kind",
        choices=[
            "all",
            "candidates",
            "experiments",
            "results",
            "dequantization",
            "proofs",
            "reductions",
            "reduction-contracts",
            "scaling",
            "conjectures",
            "mutations",
            "negative",
            "rejected",
        ],
        default="all",
    )
    list_cmd.add_argument("--limit", type=int, default=20)
    list_cmd.add_argument("--verbose", action="store_true")
    list_cmd.set_defaults(func=command_list)


def command_list(args: argparse.Namespace) -> int:
    from qsearch import (
        CONTRACT_AUDIT_PATH,
        initialize_seed_registry,
        load_candidates,
        load_conjectures,
        load_dequantization_checks,
        load_experiment_results,
        load_experiments,
        load_mutation_proposals,
        load_negative_results,
        load_proof_status,
        load_reduction_ledger,
        load_rejected_candidates,
        load_scaling_runs,
    )
    initialize_seed_registry(overwrite=False)
    if args.kind in {"all", "candidates"}:
        print("Candidates")
        print("==========")
        for candidate in load_candidates():
            print(f"{candidate['id']} | {candidate['status']} | {candidate['title']}")
            if args.verbose:
                print(f"  mechanism: {candidate['quantum_mechanism']}")
                print(f"  literature: {', '.join(candidate['literature_ids'])}")
    if args.kind in {"all", "experiments"}:
        print("\nExperiments")
        print("===========")
        for experiment in load_experiments():
            print(f"{experiment['id']} | {experiment['candidate_id']} | {experiment['status']} | {experiment['title']}")
            if args.verbose:
                print(f"  falsifiers: {'; '.join(experiment['falsifiers'])}")
    if args.kind in {"all", "results"}:
        print("\nExperiment Results")
        print("==================")
        for result in load_experiment_results()[: args.limit]:
            print(f"{result['id']} | {result['experiment_id']} | {result['status']} | {result['summary']}")
            if args.verbose:
                print(f"  metrics: {json.dumps(result.get('metrics', {}), sort_keys=True)}")
                print(f"  falsifiers: {'; '.join(result.get('falsifiers_triggered', []))}")
    if args.kind in {"all", "dequantization"}:
        print("\nDequantization Checks")
        print("=====================")
        for finding in load_dequantization_checks()[: args.limit]:
            print(f"{finding['id']} | {finding['severity']} | {finding['target_id']} | {finding['claim_under_test']}")
            if args.verbose:
                print(f"  evidence: {finding['evidence']}")
                print(f"  action: {finding['required_action']}")
    if args.kind in {"all", "proofs"}:
        print("\nProof Status")
        print("============")
        for record in load_proof_status()[: args.limit]:
            print(f"{record['candidate_id']} | {record['obligation_id']} | {record['status']}")
            if args.verbose:
                print(f"  evidence: {record['evidence']}")
                print(f"  next: {record['next_action']}")
    if args.kind in {"all", "reductions"}:
        print("\nReduction Routes")
        print("================")
        ledger = load_reduction_ledger()
        for route in ledger.get("routes", [])[: args.limit]:
            print(f"{route['id']} | {route['candidate_id']} | {route['status']}")
            if args.verbose:
                print(f"  source: {route['natural_source_problem']}")
                print(f"  target: {route['candidate_target']}")
                print(f"  blocking edges: {', '.join(route['blocking_edge_ids'])}")
    if args.kind in {"all", "reduction-contracts"}:
        print("\nReduction Contract Interfaces")
        print("=============================")
        contract_audit = json.loads(CONTRACT_AUDIT_PATH.read_text()) if CONTRACT_AUDIT_PATH.exists() else {}
        for audit in contract_audit.get("audits", [])[: args.limit]:
            print(f"{audit['route_id']} | {audit['candidate_id']} | {audit['status']}")
            if args.verbose:
                failed = [check for check in audit.get("checks", []) if not check.get("passed")]
                print(f"  theorem: {audit.get('theorem_contract_id', '')}")
                print(f"  failed axes: {', '.join(check['axis'] for check in failed)}")
    if args.kind in {"all", "scaling"}:
        print("\nScaling Runs")
        print("============")
        for run in load_scaling_runs()[: args.limit]:
            print(f"{run['id']} | {run['status']} | {run['summary']}")
            if args.verbose:
                print(f"  metrics: {json.dumps(run.get('headline_metrics', {}), sort_keys=True)}")
    if args.kind in {"all", "conjectures"}:
        print("\nConjectures")
        print("===========")
        for conjecture in load_conjectures()[: args.limit]:
            print(f"{conjecture['id']} | {conjecture['status']} | {conjecture['statement']}")
            if args.verbose:
                print(f"  reductions: {'; '.join(conjecture.get('reduction_links', []))}")
                print(f"  blockers: {len(conjecture.get('blocking_evidence', []))}")
    if args.kind in {"all", "mutations"}:
        print("\nMutation Proposals")
        print("==================")
        for proposal in load_mutation_proposals()[: args.limit]:
            print(f"{proposal['id']} | {proposal['mutation_type']} | {proposal['status']}")
            if args.verbose:
                print(f"  rationale: {proposal['rationale']}")
                print(f"  required: {'; '.join(proposal.get('required_modules', []))}")
    if args.kind in {"all", "negative"}:
        print("\nNegative Results")
        print("================")
        for item in load_negative_results()[: args.limit]:
            print(f"{item['id']} | {item['claim']}")
            if args.verbose:
                print(f"  invalid: {item['reason_invalid']}")
                print(f"  lesson: {item['lesson']}")
    if args.kind in {"all", "rejected"}:
        print("\nRejected Candidates")
        print("===================")
        for item in load_rejected_candidates()[: args.limit]:
            print(f"{item['id']} | {item['title']} | issues={len(item.get('issues', []))}")
            if args.verbose:
                for issue in item.get("issues", []):
                    print(f"  {issue['obligation_id']}:{issue['field']}: {issue['message']}")
    return 0


def add_ternary_pair_lattice(subparsers) -> None:
    ternary_pair_lattice = subparsers.add_parser(
        "ternary-pair-lattice",
        help="Run exact A2 ternary congruence geometry and ordinary pair-finder falsifiers.",
    )
    ternary_pair_lattice.add_argument("--no-registry", action="store_true")
    ternary_pair_lattice.set_defaults(func=command_ternary_pair_lattice)


def command_ternary_pair_lattice(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_pair_lattice import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    validation = validate_registry()
    print("ternary_pair_lattice complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_pair_collimation(subparsers) -> None:
    ternary_pair_collimation = subparsers.add_parser(
        "ternary-pair-collimation",
        help="Run exact native least-trit pair receiver and arithmetic target audit.",
    )
    ternary_pair_collimation.add_argument("--no-registry", action="store_true")
    ternary_pair_collimation.set_defaults(func=command_ternary_pair_collimation)


def command_ternary_pair_collimation(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_pair_collimation import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    validation = validate_registry()
    print("ternary_pair_collimation complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_pair_cell_coverage(subparsers) -> None:
    ternary_pair_cell_coverage = subparsers.add_parser(
        "ternary-pair-cell-coverage",
        help="Run exact native-word recovery predicates for public Babai repair lists.",
    )
    ternary_pair_cell_coverage.add_argument("--no-registry", action="store_true")
    ternary_pair_cell_coverage.set_defaults(func=command_ternary_pair_cell_coverage)


def command_ternary_pair_cell_coverage(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_pair_cell_coverage import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    validation = validate_registry()
    print("ternary_pair_cell_coverage complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_curvature_frontier(subparsers) -> None:
    ternary_curvature_frontier = subparsers.add_parser(
        "ternary-curvature-frontier",
        help="Run sharp scalar curvature geometry and exact joint full-root source replay.",
    )
    ternary_curvature_frontier.add_argument("--no-registry", action="store_true")
    ternary_curvature_frontier.set_defaults(func=command_ternary_curvature_frontier)


def command_ternary_curvature_frontier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_curvature_frontier import REPORT, write_ternary_curvature_frontier_report
    write_ternary_curvature_frontier_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print("ternary_curvature_frontier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_cyclic_extractor(subparsers) -> None:
    ternary_cyclic_extractor = subparsers.add_parser(
        "ternary-cyclic-extractor",
        help="Run exact native curvature cycle extractor and partition audit.",
    )
    ternary_cyclic_extractor.add_argument("--no-registry", action="store_true")
    ternary_cyclic_extractor.set_defaults(func=command_ternary_cyclic_extractor)


def command_ternary_cyclic_extractor(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_cyclic_extractor import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    validation = validate_registry()
    print("ternary_cyclic_extractor complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_posterior_dual(subparsers) -> None:
    ternary_posterior_dual = subparsers.add_parser(
        "ternary-posterior-dual",
        help="Run exact joint paired posterior and final-effect support frontier audit.",
    )
    ternary_posterior_dual.add_argument("--no-registry", action="store_true")
    ternary_posterior_dual.set_defaults(func=command_ternary_posterior_dual)


def command_ternary_posterior_dual(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_posterior_dual import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    validation = validate_registry()
    print("ternary_posterior_dual complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_least_trit_bootstrap(subparsers) -> None:
    ternary_least_trit_bootstrap = subparsers.add_parser(
        "ternary-least-trit-bootstrap",
        help="Run native weak least-trit bootstrap and full-label copy gate audit.",
    )
    ternary_least_trit_bootstrap.add_argument("--no-registry", action="store_true")
    ternary_least_trit_bootstrap.set_defaults(func=command_ternary_least_trit_bootstrap)


def command_ternary_least_trit_bootstrap(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_least_trit_bootstrap import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    validation = validate_registry()
    print("ternary_least_trit_bootstrap complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_ternary_covariant_noise(subparsers) -> None:
    ternary_covariant_noise = subparsers.add_parser(
        "ternary-covariant-noise",
        help="Run native covariant receiver and exact classical signal ledger audit.",
    )
    ternary_covariant_noise.add_argument("--no-registry", action="store_true")
    ternary_covariant_noise.set_defaults(func=command_ternary_covariant_noise)


def command_ternary_covariant_noise(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.ternary_covariant_noise import REPORT, build_report
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    validation = validate_registry()
    print("ternary_covariant_noise complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_parity_block_usd_prange(subparsers) -> None:
    parity_block_usd_prange = subparsers.add_parser(
        "parity-block-usd-prange",
        help="Run constructive parity block USD and matched classical block-Prange sampler audit.",
    )
    parity_block_usd_prange.add_argument("--no-registry", action="store_true")
    parity_block_usd_prange.set_defaults(func=command_parity_block_usd_prange)


def command_parity_block_usd_prange(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.parity_block_usd_prange import REPORT, write_report
    write_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print("parity_block_usd_prange complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_linear_erasure_prange_duality(subparsers) -> None:
    linear_erasure_prange_duality = subparsers.add_parser(
        "linear-erasure-prange-duality",
        help="Run positive affine-subspace instrument duality and matched affine Gibbs sampler audit.",
    )
    linear_erasure_prange_duality.add_argument("--no-registry", action="store_true")
    linear_erasure_prange_duality.set_defaults(func=command_linear_erasure_prange_duality)


def command_linear_erasure_prange_duality(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.linear_erasure_prange_duality import REPORT, write_report
    write_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print("linear_erasure_prange_duality complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_parity_block_med_lpn_barrier(subparsers) -> None:
    parity_block_med_lpn_barrier = subparsers.add_parser(
        "parity-block-med-lpn-barrier",
        help="Run parity block minimum-error discrimination, Helstrom optimality, and LPN reduction audit.",
    )
    parity_block_med_lpn_barrier.add_argument("--no-registry", action="store_true")
    parity_block_med_lpn_barrier.set_defaults(func=command_parity_block_med_lpn_barrier)


def command_parity_block_med_lpn_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.parity_block_med_lpn_barrier import REPORT, write_report
    write_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print("parity_block_med_lpn_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_nil3_state_hsp_descent_receiver(subparsers) -> None:
    nil3_state_hsp_descent_receiver = subparsers.add_parser(
        "nil3-state-hsp-descent-receiver",
        help="Audit the conditional native level3 phase lift; complete quotient recovery remains open.",
    )
    nil3_state_hsp_descent_receiver.add_argument("--no-registry", action="store_true")
    nil3_state_hsp_descent_receiver.set_defaults(func=command_nil3_state_hsp_descent_receiver)


def command_nil3_state_hsp_descent_receiver(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.nil3_state_hsp_descent_receiver import REPORT, write_report
    report = write_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_wreath_orientation_gram_norm(subparsers) -> None:
    wreath_orientation_gram_norm = subparsers.add_parser(
        "wreath-orientation-gram-norm",
        help="Run wreath orientation projector Gram norm, complementary pairing duality, and sub-POVM audit.",
    )
    wreath_orientation_gram_norm.add_argument("--no-registry", action="store_true")
    wreath_orientation_gram_norm.set_defaults(func=command_wreath_orientation_gram_norm)


def command_wreath_orientation_gram_norm(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.self_dual_wreath_orientation_gram_norm import REPORT_PATH, write_report
    write_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print("wreath_orientation_gram_norm complete")
    print(f"Artifact: {REPORT_PATH}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_wreath_coset_permutation_holevo_collapse(subparsers) -> None:
    wreath_coset_permutation_holevo_collapse = subparsers.add_parser(
        "wreath-coset-permutation-holevo-collapse",
        help="Check a valid wreath coset source, normalized information, and matched classical permutation recovery.",
    )
    wreath_coset_permutation_holevo_collapse.add_argument("--no-registry", action="store_true")
    wreath_coset_permutation_holevo_collapse.set_defaults(func=command_wreath_coset_permutation_holevo_collapse)


def command_wreath_coset_permutation_holevo_collapse(args: argparse.Namespace) -> int:
    from qsearch import validate_registry
    from theorems.wreath_coset_permutation_holevo_collapse import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("Wreath source corrected; repaired family recovered classically, not general code equivalence.")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_character_shift_decoding_lower_bound_barrier(subparsers) -> None:
    character_shift_decoding_lower_bound_barrier = subparsers.add_parser(
        "character-shift-decoding-lower-bound-barrier",
        help="Run uniform character shift decoding lower bound, Weil agreement identity, and cyclotomic degree obstruction audit.",
    )
    character_shift_decoding_lower_bound_barrier.add_argument("--no-registry", action="store_true")
    character_shift_decoding_lower_bound_barrier.set_defaults(func=command_character_shift_decoding_lower_bound_barrier)


def command_character_shift_decoding_lower_bound_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.character_shift_decoding_lower_bound_barrier import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("character_shift_decoding_lower_bound_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dihedral_coset_chirp_aliasing_spectral_flatness_barrier(subparsers) -> None:
    dihedral_coset_chirp_aliasing_spectral_flatness_barrier = subparsers.add_parser(
        "dihedral-coset-chirp-aliasing-spectral-flatness-barrier",
        help="Run dihedral coset quadratic chirp aliasing barrier, Gauss sum spectral flatness, and Bombieri-Weil anti-concentration audit.",
    )
    dihedral_coset_chirp_aliasing_spectral_flatness_barrier.add_argument("--no-registry", action="store_true")
    dihedral_coset_chirp_aliasing_spectral_flatness_barrier.set_defaults(func=command_dihedral_coset_chirp_aliasing_spectral_flatness_barrier)


def command_dihedral_coset_chirp_aliasing_spectral_flatness_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    import json
    from theorems.dihedral_coset_chirp_aliasing_spectral_flatness_barrier import REPORT, build_report, register_negative_result
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    if not getattr(args, "no_registry", False):
        register_negative_result()
    validation = validate_registry()
    print("dihedral_coset_chirp_aliasing_spectral_flatness_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_cfi_graph_coset_luks_subsumption_barrier(subparsers) -> None:
    cfi_graph_coset_luks_subsumption_barrier = subparsers.add_parser(
        "cfi-graph-coset-luks-subsumption-barrier",
        help="Check CFI graph structure and its fixed-valence classical baseline; retract unsupported quantum no-go claims.",
    )
    cfi_graph_coset_luks_subsumption_barrier.add_argument("--no-registry", action="store_true")
    cfi_graph_coset_luks_subsumption_barrier.set_defaults(func=command_cfi_graph_coset_luks_subsumption_barrier)


def command_cfi_graph_coset_luks_subsumption_barrier(args: argparse.Namespace) -> int:
    from qsearch import validate_registry
    from core.research_registry import _write_json
    from theorems.cfi_graph_coset_luks_subsumption_barrier import REPORT, build_report
    from theorems.nonabelian_barrier_scope_audit import quarantine_reviewed_negatives
    report = build_report()
    if not getattr(args, "no_registry", False):
        quarantine_reviewed_negatives()
    _write_json(REPORT, report)
    validation = validate_registry()
    print("CFI fixed-valence classical baseline checked; no general quantum lower bound claimed.")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_godsil_mckay_cospectral_tensor_invariance_barrier(subparsers) -> None:
    godsil_mckay_cospectral_tensor_invariance_barrier = subparsers.add_parser(
        "godsil-mckay-cospectral-tensor-invariance-barrier",
        help="Run Godsil-McKay switching cospectrality, CTQW amplitude invariance, and neighborhood topology barrier audit.",
    )
    godsil_mckay_cospectral_tensor_invariance_barrier.add_argument("--no-registry", action="store_true")
    godsil_mckay_cospectral_tensor_invariance_barrier.set_defaults(func=command_godsil_mckay_cospectral_tensor_invariance_barrier)


def command_godsil_mckay_cospectral_tensor_invariance_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    import json
    from theorems.godsil_mckay_cospectral_tensor_invariance_barrier import REPORT, build_report, register_negative_result
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    if not getattr(args, "no_registry", False):
        register_negative_result()
    validation = validate_registry()
    print("godsil_mckay_cospectral_tensor_invariance_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_rowspace_rref_gauge_elimination_fourier_extinction_barrier(subparsers) -> None:
    rowspace_rref_gauge_elimination_fourier_extinction_barrier = subparsers.add_parser(
        "rowspace-rref-gauge-elimination-fourier-extinction-barrier",
        help="Run rowspace RREF gauge elimination and self-dual code equivalence Fourier extinction barrier audit.",
    )
    rowspace_rref_gauge_elimination_fourier_extinction_barrier.add_argument("--no-registry", action="store_true")
    rowspace_rref_gauge_elimination_fourier_extinction_barrier.set_defaults(func=command_rowspace_rref_gauge_elimination_fourier_extinction_barrier)


def command_rowspace_rref_gauge_elimination_fourier_extinction_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    import json
    from theorems.rowspace_rref_gauge_elimination_fourier_extinction_barrier import REPORT, build_report, register_negative_result
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    if not getattr(args, "no_registry", False):
        register_negative_result()
    validation = validate_registry()
    print("rowspace_rref_gauge_elimination_fourier_extinction_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_planted_qary_source(subparsers) -> None:
    planted_qary_source = subparsers.add_parser(
        "planted-qary-source",
        help="Generate public q-ary kernel lattices with certified field/rank promises and classical attacks.",
    )
    planted_qary_source.add_argument("--no-write", action="store_true")
    planted_qary_source.set_defaults(func=command_planted_qary_source)


def command_planted_qary_source(args: argparse.Namespace) -> int:
    from theorems.planted_qary_usvp_source import REPORT, build_report, exact_json
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    recovered = sum(c["matched_attack_calibration"]["tested_instance_classically_recovers_planted_direction"]
                    for c in report["source_controls"])
    print(report["status"])
    print(f"Public classical recovery: {recovered}/{len(report['source_controls'])} controls")
    print(f"Artifact: {REPORT}")
    print("Statistical uniqueness is not computational hardness. No quantum advantage admitted.")
    return 0


def add_lattice_localization_gap_frontier(subparsers) -> None:
    localization_frontier = subparsers.add_parser("lattice-localization-gap-frontier",
        help="Challenge public lower-gap cube/sine localization schedules with classical attacks.")
    localization_frontier.add_argument("--no-write", action="store_true")
    localization_frontier.set_defaults(func=command_lattice_localization_gap_frontier)


def command_lattice_localization_gap_frontier(args: argparse.Namespace) -> int:
    from theorems.lattice_localization_gap_frontier import REPORT, build_report, exact_json
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print(f"Public classical recovery: {report['classically_recovered_controls']}/{report['controls_tested']} controls")
    print(f"Artifact: {REPORT}")
    print("Conditional source schedule, not certified hardness or an efficient receiver.")
    return 0


def add_lattice_sine_window_source(subparsers) -> None:
    sine_source=subparsers.add_parser("lattice-sine-window-source",
        help="Compile public coherent sine localization and audit actual unknown phase registers.")
    sine_source.add_argument("--no-write",action="store_true")
    sine_source.set_defaults(func=command_lattice_sine_window_source)


def command_lattice_sine_window_source(args: argparse.Namespace) -> int:
    from theorems.lattice_sine_window_source import REPORT,build_report,exact_json
    report=build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report),indent=2)+"\n")
    print(report["status"])
    print(f"Charged source preparations: {report['charged_source_preparations']}")
    print(f"Artifact: {REPORT}")
    print("Public source only. Hardness and efficient noisy decoding remain unproved.")
    return 0


def add_lattice_cube_coset_source(subparsers) -> None:
    lattice_cube_source = subparsers.add_parser(
        "lattice-cube-coset-source",
        help="Census actual public lattice cube fibres, Born weights, contamination and LLL controls.",
    )
    lattice_cube_source.add_argument("--no-write", action="store_true")
    lattice_cube_source.set_defaults(func=command_lattice_cube_coset_source)


def command_lattice_cube_coset_source(args: argparse.Namespace) -> int:
    from theorems.lattice_cube_coset_source import REPORT, build_report
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("Public LLL solves the calibration. Source circuits have separate workflows; the noisy decoder remains open.")
    return 0


def add_lattice_cube_source_circuit(subparsers) -> None:
    lattice_cube_circuit = subparsers.add_parser(
        "lattice-cube-source-circuit",
        help="Compile clean public lattice cube arithmetic and uniform-parent logical circuits.",
    )
    lattice_cube_circuit.add_argument("--no-write", action="store_true")
    lattice_cube_circuit.set_defaults(func=command_lattice_cube_source_circuit)


def command_lattice_cube_source_circuit(args: argparse.Namespace) -> int:
    from theorems.lattice_cube_source_circuit import REPORT, build_report
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("Clean logical evaluator compiled. Full phase readout has a separate workflow; the receiver remains open.")
    return 0


def add_lattice_cube_dcp_readout(subparsers) -> None:
    lattice_phase_source = subparsers.add_parser(
        "lattice-cube-dcp-readout",
        help="Compile and audit actual lattice-to-DCP phase readout with opaque noisy registers.",
    )
    lattice_phase_source.add_argument("--no-write", action="store_true")
    lattice_phase_source.set_defaults(func=command_lattice_cube_dcp_readout)


def command_lattice_cube_dcp_readout(args: argparse.Namespace) -> int:
    from theorems.lattice_cube_dcp_readout import REPORT, build_report
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("Actual lattice phase registers emitted. Finite diagnostics do not prove a growing-family speedup.")
    return 0


def add_lattice_qft_precision(subparsers) -> None:
    lattice_qft_precision = subparsers.add_parser(
        "lattice-qft-precision", help="Compile budgeted QFT cutoffs and audit encoded angles, inverse calls and rare-event debt.",
    )
    lattice_qft_precision.add_argument("--no-write", action="store_true")
    lattice_qft_precision.set_defaults(func=command_lattice_qft_precision)


def command_lattice_qft_precision(args: argparse.Namespace) -> int:
    from theorems.lattice_qft_precision import REPORT, build_report, exact_json
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("Joint QFT precision is budgeted. Rare conditional accuracy and full source/hardware correctness remain separate.")
    return 0

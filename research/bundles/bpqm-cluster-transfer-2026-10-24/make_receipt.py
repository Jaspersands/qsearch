"""Produce a source-bound mathematical certificate and bounded diagnostics."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import sqrt
from pathlib import Path
import platform
import random

import cluster_transfer as t

HERE = Path(__file__).resolve().parent


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True)+"\n").encode("ascii")


def source_hashes():
    names = ("CLUSTER_TRANSFER.md", "HANDOFF.md", "cluster_transfer.py",
             "test_cluster_transfer.py", "make_receipt.py")
    paths = [HERE/name for name in names]
    paths += [HERE.parent/"central-rank-2026-10-23/central_rank.py"]
    return {str(path.relative_to(HERE.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def finite_controls():
    out = []
    for rows, n in (((1, 2, 3), 2), ((1, 1, 0), 2), ((3,), 2)):
        laws = t.finite_laws(rows, n, F(13, 20))
        p = laws["coset_probabilities"]
        success = sum(sqrt(float(a)/len(p)) for a in p)**2
        bern = t.bernoulli_kernel_law(rows, n, F(13, 20))
        jump = sum(mass*d.bit_count() for d, mass in bern.items())
        out.append({"rows": list(rows), "n": n, "eta_exact": str(laws["eta"]),
                    "joint_tv_exact": str(laws["joint_tv"]),
                    "coset_probabilities_exact": list(map(str, p)),
                    "optimal_decoding_success_floating_diagnostic": success,
                    "annealed_mean_jump_exact": str(jump),
                    "finite_enumeration_is_exponential": True,
                    "decoder_error_certificate_inferred": False})
    return out


def native_diagnostics():
    out = []
    for n in (128, 512, 2048):
        cases = []
        for trial in range(16):
            seed = 261024000+n*100+trial
            rng = random.Random(seed)
            rows = t.socket_rows(n, rng)
            selected = tuple(row for row in rows if t.coin(F(13, 20), rng))
            geometry = t.kernel_geometry(selected, n)
            delta = t.draw_kernel(geometry["basis"], rng)
            if any((row & delta).bit_count() % 2 for row in selected):
                raise ArithmeticError("invalid sampled kernel word")
            cases.append({"seed": seed,
                          "matrix_sha256": hashlib.sha256(encoded(list(rows))).hexdigest(),
                          "parallel_pairs_cancelled": (6*n-sum(row.bit_count() for row in rows))//2,
                          "selected_rows": len(selected), "rank": geometry["rank"],
                          "nullity": geometry["nullity"],
                          "active_coordinates": geometry["active_coordinates"],
                          "conditional_mean_jump_exact": str(geometry["mean_jump"]),
                          "sampled_jump": delta.bit_count(),
                          "sampled_jump_at_least_n_over_50": 50*delta.bit_count() >= n})
        out.append({"n": n, "m": 2*n, "draws": len(cases), "cases": cases,
                    "source": "uniform_regular_socket_matching_then_independent_Ber_13_over_20_rows",
                    "rejection_conditioning": False, "uniform_disorder_transfer": "UNKNOWN",
                    "confidence_claim": False, "quantum_circuit_run": False,
                    "statevector_or_Gibbs_enumeration": False})
    return out


def report(certificate):
    if not t.verify_certificate(certificate):
        raise ArithmeticError("unverified certificate")
    bounds = []
    for n in (128, 512, 1024, 2048, 4096, 8192):
        bound = t.mobility_bound(n, certificate)
        rounded = t.upward_dyadic(bound)
        bounds.append({"n": n, "annealed_tail_upper_dyadic": str(rounded),
                       "annealed_tail_float_for_display": float(rounded),
                       "uniform_disorder_tail_upper": None,
                       "required_decoder_block_error_upper": None,
                       "unknown_reason": "no applicable finite-block quantum error certificate"})
    return {"status": "local_unreviewed_structural_bound_not_mixing_or_speedup",
            "python": platform.python_version(), "source_sha256": source_hashes(),
            "entropy_certificate_sha256": hashlib.sha256(encoded(certificate)).hexdigest(),
            "exact_endpoint_comparisons": 2*len(certificate["intervals"]),
            "certificate_c": certificate["c"], "certificate_cutoff": certificate["cutoff"],
            "certificate_decay": certificate["decay"], "bounds": bounds,
            "finite_controls": finite_controls(), "native_diagnostics": native_diagnostics(),
            "established_locally": ["rational_uniform_entropy_certificate",
                                    "annealed_native_long_kernel_word_bound",
                                    "decoder_conditioned_whole_history_disorder_transfer"],
            "not_established": ["native_regular_ensemble_Gibbs_bottleneck",
                                "finite_block_BPQM_error_rate", "worst_start_mixing_lower_bound",
                                "all_classical_lower_bound", "new_quantum_algorithm"],
            "prior_art": ["https://arxiv.org/html/2510.08446v1",
                          "https://arxiv.org/html/2103.09225v1",
                          "https://arxiv.org/pdf/2610.03566"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-certificate", type=Path)
    args = parser.parse_args()
    if args.verify_certificate:
        t.verify_certificate(json.loads(args.verify_certificate.read_text()))
        print("Exact rational entropy certificate: PASS")
    else:
        certificate = t.make_certificate()
        result = report(certificate)
        if args.write:
            (HERE/"entropy_certificate.json").write_bytes(encoded(certificate))
            (HERE/"receipt.json").write_bytes(encoded(result))
        if args.output:
            args.output.write_bytes(encoded(result))
        print(json.dumps({"status": result["status"], "endpoint_checks": result["exact_endpoint_comparisons"],
                          "native_matrix_draws": sum(x["draws"] for x in result["native_diagnostics"]),
                          "finite_block_error": "UNKNOWN"}, sort_keys=True))

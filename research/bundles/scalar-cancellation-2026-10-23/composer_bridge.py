"""Exercise the existing isolated rank composer with a real scalar backend."""

import importlib.util
from pathlib import Path
import sys

from scalar_cancellation import ScalarBackend, reduced_degree, scalar_call_cap


COMPOSER_PATH = (Path(__file__).resolve().parents[1]
                 / "central-rank-2026-10-23" / "central_rank.py")
SPEC = importlib.util.spec_from_file_location("qsearch_rank_composer", COMPOSER_PATH)
composer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = composer
SPEC.loader.exec_module(composer)


def solve_matrix(matrix, prime, degree, rank_cap, *, security_bits=64, rng=None):
    reduced = reduced_degree(prime, degree)
    calls = scalar_call_cap(reduced, rank_cap)
    backend = ScalarBackend(prime, reduced, max_scalar_calls=max(1, calls),
                            security_bits=security_bits, rng=rng)
    witness = composer.compressed_witness(matrix, prime, degree, rank_cap, backend)
    report = backend.report()
    report.update({
        "requested_degree": degree,
        "public_rank_cap": rank_cap,
        "observed_rank": witness.observed_rank,
        "acquired_columns": witness.acquired_columns,
        "used_prefix_columns": witness.used_prefix_columns,
        "scalar_call_count_matches_composer": witness.scalar_calls == backend.stats.scalar_calls,
        "original_matrix_moment_verified": composer.valid_witness(matrix, witness.weights, prime, degree),
        "quantum_receiver_executed": False,
        "general_polynomial_in_rank_sde_backend": False,
        "speedup_claim_allowed": False,
    })
    if not report["scalar_call_count_matches_composer"]:
        raise ArithmeticError("composer/backend scalar count mismatch")
    return witness, report

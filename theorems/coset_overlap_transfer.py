"""Exact spatial transfer for ONE round of the retained-data path echo.

Boundary variables are a pair of group elements. Conjugation orbits reduce
the matrix, and modular sparse arithmetic avoids signed-weight cancellation.
This is a factorial-in-degree evaluator, not an unknown-input classical solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from sympy import prevprime

from coherent_overlap_programs import OverlapEchoProgram
from coset_hidden_involution_binary_decision_reduction import involution_conjugacy_class
from coset_overlap_echo import _group_data, reflection_coefficients
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


REPORT_PATH = Path("research/representation/coset_overlap_transfer.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-OVERLAP-SPATIAL-TRANSFER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrbitTransfer:
    degree: int
    transpositions: int
    hidden: tuple[int, ...] | None
    order: int
    representatives: tuple[tuple[int, int], ...]
    orbit_sizes: np.ndarray
    weights: np.ndarray
    endpoint: np.ndarray
    a_to_b: csr_matrix
    b_to_a: csr_matrix
    coefficient_l1_numerator: int
    acting_group_order: int
    fingerprint: str

    def contract(self) -> dict:
        return {
            "degree": self.degree, "transpositions": self.transpositions,
            "hypothesis": "null" if self.hidden is None else "fixed-hidden",
            "hidden_member": None if self.hidden is None else list(self.hidden),
            "group_order": self.order, "unquotiented_boundary_size": self.order**2,
            "nonzero_weight_boundary_size": int(self.orbit_sizes.sum()),
            "orbit_boundary_size": len(self.representatives),
            "acting_group_order": self.acting_group_order,
            "acting_group": "full simultaneous conjugation" if self.hidden is None else "centralizer of this ONE hidden member",
            "a_to_b_nonzero_entries": int(self.a_to_b.nnz),
            "b_to_a_nonzero_entries": int(self.b_to_a.nnz),
            "kernel_sha256": self.fingerprint,
            "rounds_supported": 1, "polynomial_in_degree": False,
            "classical_solver_for_unknown_input": False,
            "orbit_sizes_required_in_terminal_sum": True,
        }


@lru_cache(maxsize=4, typed=True)
def build_orbit_transfer(n: int, transpositions: int, hidden: tuple[int, ...] | None = None) -> OrbitTransfer:
    OverlapEchoProgram(n, transpositions, 3)
    if n > 6:
        raise ValueError("factorial transfer construction budget exceeded")
    if hidden is not None and hidden not in involution_conjugacy_class(n, transpositions):
        raise ValueError("hidden member does not belong to the declared involution class")
    coefficients, _ = reflection_coefficients(n, transpositions)
    group, index, multiply, inverse, _ = _group_data(n)
    order = len(group)
    identity = index[tuple(range(n))]
    h = None if hidden is None else index[hidden]
    choices = (identity,) if h is None else (identity, h)
    acting = np.arange(order) if h is None else np.flatnonzero(multiply[:, h] == multiply[h, :])
    conjugations = np.array([multiply[multiply[g, :], inverse[g]] for g in acting])
    support = np.flatnonzero(coefficients)
    lookup = np.full((order, order), -1, dtype=np.int32)
    representatives, sizes, weights, endpoint = [], [], [], []
    for a in support:
        for c in support:
            if lookup[a, c] >= 0:
                continue
            images = np.unique(conjugations[:, a] * order + conjugations[:, c])
            if np.any(lookup.ravel()[images] >= 0):
                raise ValueError("conjugation orbit partition overlaps")
            lookup.ravel()[images] = len(representatives)
            representatives.append((int(a), int(c)))
            sizes.append(len(images))
            weight = int(coefficients[a]) * int(coefficients[c])
            end = int(multiply[c, a] in choices)
            if (np.any(coefficients[images // order] * coefficients[images % order] != weight)
                    or np.any(np.isin(multiply[images % order, images // order], choices) != bool(end))):
                raise ValueError("weights or boundary predicate are not invariant on the proposed orbit")
            weights.append(weight)
            endpoint.append(end)
    if sum(sizes) != len(support)**2:
        raise ValueError("zero-weight elimination or orbit partition lost boundary mass")

    def count_matrix(a_to_b: bool) -> csr_matrix:
        offsets, columns, values = [0], [], []
        for first, second in representatives:
            incoming = []
            for t in choices:
                if a_to_b:
                    # Output (b,d); d c b a=t fixes c=d^-1 t a^-1 b^-1.
                    other = multiply[multiply[multiply[inverse[second], t], inverse[support]], inverse[first]]
                else:
                    # Output (a,c); d c b a=t fixes d=t a^-1 b^-1 c^-1.
                    other = multiply[multiply[multiply[t, inverse[first]], inverse[support]], inverse[second]]
                incoming.extend(lookup[support, other].tolist())
            ids, counts = np.unique([i for i in incoming if i >= 0], return_counts=True)
            columns.extend(ids.tolist())
            values.extend(counts.tolist())
            offsets.append(len(columns))
        result = csr_matrix((np.array(values, dtype=np.float64), np.array(columns, dtype=np.int32),
                             np.array(offsets, dtype=np.int32)), shape=(len(representatives),)*2)
        if result.nnz and (result.data.min() < 1 or np.any(result.data != np.floor(result.data))):
            raise ValueError("transfer counts must be positive exact integers")
        return result

    forward, backward = count_matrix(True), count_matrix(False)
    sizes, weights, endpoint = (np.array(items, dtype=np.int64) for items in (sizes, weights, endpoint))
    digest = hashlib.sha256()
    for matrix in (forward, backward):
        for array in (matrix.indptr, matrix.indices, matrix.data):
            digest.update(array.tobytes())
            array.setflags(write=False)
    for array in (sizes, weights, endpoint):
        digest.update(array.tobytes())
        array.setflags(write=False)
    return OrbitTransfer(n, transpositions, hidden, order, tuple(representatives), sizes, weights, endpoint,
                         forward, backward, sum(abs(int(c)) for c in coefficients), len(acting), digest.hexdigest())


def _safe_prime_ceiling(kernel: OrbitTransfer) -> int:
    row_sum = max(1, *(int(np.asarray(matrix.sum(axis=1)).max()) for matrix in (kernel.a_to_b, kernel.b_to_a)))
    max_weight = max(1, int(np.max(np.abs(kernel.weights))))
    # Only the nonnegative COUNT-matrix dot uses float64. Every product and
    # every partial sum is an exactly representable integer below 2^52.
    # Weight multiplication and the terminal sum then use bounded int64.
    return min(1 << 30, ((1 << 52)-1) // row_sum,
               ((1 << 62)-1) // (row_sum * max_weight),
               ((1 << 62)-1) // max(1, int(kernel.orbit_sizes.sum())))


def modular_moments(kernel: OrbitTransfer, copies: tuple[int, ...], prime: int) -> dict[int, int]:
    if (not copies or any(type(k) is not int or not 3 <= k <= 128 for k in copies)
            or type(prime) is not int or not 2 <= prime < _safe_prime_ceiling(kernel)):
        raise ValueError("invalid copy sweep or modulus outside the exact arithmetic budget")
    state = (kernel.weights * kernel.endpoint) % prime
    terminal = kernel.orbit_sizes * kernel.endpoint
    result = {}
    for edge in range(1, max(copies)-1):
        matrix = kernel.a_to_b if edge % 2 else kernel.b_to_a
        raw = matrix @ state
        if not np.isfinite(raw).all() or np.any(raw != np.floor(raw)):
            raise ValueError("integer-exact sparse count contraction failed")
        state = (raw.astype(np.int64) * kernel.weights) % prime
        k = edge + 2
        if k in copies:
            result[k] = int(np.dot(terminal, state)) % prime
    return result


def exact_path_moments(program: OverlapEchoProgram, copies: tuple[int, ...], *, hidden: tuple[int, ...] | None = None) -> dict:
    if program.rounds != 1:
        raise ValueError("this spatial transfer supports ONE echo round, not repeated temporal layers")
    if (not copies or len(set(copies)) != len(copies) or any(type(k) is not int or not 3 <= k <= 128 for k in copies)
            or max(copies) != program.copies):
        raise ValueError("distinct copy counts in [3,128] with maximum equal to the program budget required")
    kernel = build_orbit_transfer(program.degree, program.transpositions, hidden)
    copies = tuple(sorted(copies))
    # Bound the sum of absolute path weights, independently of unitary norm.
    bounds = {k: kernel.coefficient_l1_numerator**(2*(k-1)) for k in copies}
    residues = dict.fromkeys(copies, 0)
    modulus, primes = 1, []
    ceiling = _safe_prime_ceiling(kernel)
    prime = int(prevprime(ceiling))
    while modulus <= 2 * max(bounds.values()):
        observed = modular_moments(kernel, copies, prime)
        inverse = pow(modulus, -1, prime)
        for k in copies:
            residues[k] += modulus * (((observed[k] - residues[k]) * inverse) % prime)
        modulus *= prime
        primes.append(prime)
        prime = int(prevprime(prime))
    numerators = {k: value if value <= modulus//2 else value-modulus for k, value in residues.items()}
    held_out = modular_moments(kernel, copies, prime)
    rows = []
    for k in copies:
        numerator = numerators[k]
        if abs(numerator) > bounds[k] or numerator % prime != held_out[k]:
            raise ValueError("CRT reconstruction failed the absolute bound or held-out modulus")
        moment = Fraction(numerator, kernel.order**(2*(k-1)))
        if abs(moment) > 1:
            raise ValueError("reconstructed echo moment violates physical unitarity")
        rows.append({"copies": k, "moment_numerator_hex": hex(moment.numerator),
                     "moment_denominator_hex": hex(moment.denominator), "moment": float(moment),
                     "minus_probability": float((1-moment)/2)})
    return {"kernel": kernel.contract(), "rows": rows,
        "arithmetic_certificate": {"primes": primes, "crt_modulus_hex": hex(modulus),
            "absolute_numerator_bound_hex": hex(max(bounds.values())), "held_out_prime": prime,
            "held_out_residues": {str(k): held_out[k] for k in copies},
            "modulus_exceeds_twice_absolute_bound": modulus > 2 * max(bounds.values()),
            "count_dot_integer_exact_below_2_to_52": True,
            "weighted_and_terminal_int64_operations_below_2_to_62": True,
            "floating_cancellation_used_for_result": False},
        "verified": True, "rounds": 1, "growing_degree_advantage_proved": False}


def _fraction(row: dict) -> Fraction:
    return Fraction(int(row["moment_numerator_hex"], 16), int(row["moment_denominator_hex"], 16))


def _hex_fraction(value: Fraction) -> dict:
    return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}


def _integer_count_product(matrix: csr_matrix, values: list[int]) -> list[int]:
    """Exact nonnegative integer dot by bounded radix digits, not float fitting."""
    if len(values) != matrix.shape[1] or any(type(v) is not int or v < 0 for v in values):
        raise ValueError("nonnegative integer vector required")
    radix_bits = 24
    if int(np.asarray(matrix.sum(axis=1)).max()) * ((1 << radix_bits)-1) >= 1 << 52:
        raise ValueError("radix count product exceeds the exact float64 integer range")
    result = [0] * matrix.shape[0]
    for shift in range(0, max(values, default=0).bit_length(), radix_bits):
        digits = np.array([(value >> shift) & ((1 << radix_bits)-1) for value in values], dtype=np.int64)
        partial = matrix @ digits
        if not np.isfinite(partial).all() or np.any(partial != np.floor(partial)):
            raise ValueError("radix count product lost integrality")
        for i, value in enumerate(partial):
            result[i] += int(value) << shift
    return result


def verify_decay_witness(kernel: OrbitTransfer, witness: list[int], ratio: Fraction) -> dict:
    """Certify P u <= ratio*u with exact integers for the absolute two-step map."""
    if (type(ratio) is not Fraction or not 0 < ratio < 1 or len(witness) != len(kernel.weights)
            or any(type(v) is not int or v < 1 for v in witness)):
        raise ValueError("positive integer witness and exact ratio in (0,1) required")
    weights = [abs(int(w)) for w in kernel.weights]
    first = [w*v for w, v in zip(weights, _integer_count_product(kernel.a_to_b, witness))]
    second = [w*v for w, v in zip(weights, _integer_count_product(kernel.b_to_a, first))]
    valid = all(ratio.denominator * value <= ratio.numerator * kernel.order**4 * u
                for value, u in zip(second, witness))
    if not valid:
        return {"certified": False, "reason": "exact positive-vector inequality failed"}
    initial_multiplier = max(Fraction(w*int(end), kernel.order**2*u)
                             for w, end, u in zip(weights, kernel.endpoint, witness))
    terminal = [int(size)*int(end) for size, end in zip(kernel.orbit_sizes, kernel.endpoint)]
    even = initial_multiplier * sum(t*u for t, u in zip(terminal, witness))
    odd = initial_multiplier * Fraction(sum(t*v for t, v in zip(terminal, first)), kernel.order**2)
    return {"certified": True, "kernel_sha256": kernel.fingerprint, "ratio": _hex_fraction(ratio),
        "scope": {"degree": kernel.degree, "transpositions": kernel.transpositions, "rounds": 1,
                  "hidden_member": None if kernel.hidden is None else list(kernel.hidden),
                  "program": "negative-character odd/even path echo with fixed X readout"},
        "positive_witness_hex": [hex(v) for v in witness],
        "even_copies_prefactor": _hex_fraction(even), "odd_copies_prefactor": _hex_fraction(odd),
        "exact_integer_inequalities_checked": len(witness),
        "moment_bound": "min(1, C_parity * ratio^floor((K-2)/2)) for EVERY integer K>=3, ONE round and this fixed group/class",
        "review_status": "derived-finite-degree-all-copy-bound-review-pending",
        "growing_degree_or_temporal_depth_bound": False}


def find_decay_witness(kernel: OrbitTransfer, *, ratio: Fraction = Fraction(3, 4)) -> dict:
    """Numerics propose a witness; exact integer inequalities alone accept it."""
    if type(ratio) is not Fraction or not 0 < ratio < 1:
        raise ValueError("exact rational rate in (0,1) required")
    weight = np.abs(kernel.weights) / kernel.order**2
    proposed = np.ones(len(weight))
    for _ in range(128):
        proposed = 1 + weight * (kernel.b_to_a @ (weight * (kernel.a_to_b @ proposed))) / float(ratio)
        if not np.isfinite(proposed).all() or np.max(proposed) > 1e100:
            return {"certified": False, "reason": "proposal iteration diverged; no conclusion"}
    proposed /= np.max(proposed)
    witness = [max(1, round(float(value)*(1 << 40))) for value in proposed]
    return verify_decay_witness(kernel, witness, ratio)


def certified_moment_cap(certificate: dict, program: OverlapEchoProgram) -> Fraction:
    scope = certificate.get("scope", {})
    if (certificate.get("certified") is not True or not isinstance(program, OverlapEchoProgram)
            or (program.degree, program.transpositions, program.rounds) !=
               (scope.get("degree"), scope.get("transpositions"), scope.get("rounds"))):
        raise ValueError("decay certificate does not cover this degree, class or temporal depth")
    copies = program.copies
    def value(record):
        return Fraction(int(record["numerator_hex"], 16), int(record["denominator_hex"], 16))
    prefactor = value(certificate["odd_copies_prefactor" if copies % 2 else "even_copies_prefactor"])
    return min(Fraction(1), prefactor * value(certificate["ratio"])**((copies-2)//2))


def replay_decay_certificate(kernel: OrbitTransfer, record: dict) -> bool:
    try:
        ratio = Fraction(int(record["ratio"]["numerator_hex"], 16), int(record["ratio"]["denominator_hex"], 16))
        rebuilt = verify_decay_witness(kernel, [int(v, 16) for v in record["positive_witness_hex"]], ratio)
        return (record.get("certified") is True and rebuilt.get("certified") is True
                and all(record.get(key) == rebuilt.get(key) for key in
                        ("kernel_sha256", "scope", "even_copies_prefactor", "odd_copies_prefactor")))
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def pair_event_baseline(n: int, transpositions: int, copies: int) -> dict:
    """Finite degree calibration of a pair-event count; front end is quantum."""
    from coset_binary_carrier_instruments import _independent_label_factor_laws
    if type(copies) is not int or not 3 <= copies <= 128:
        raise ValueError("finite pair-event copy budget exceeded")
    _, law = _independent_label_factor_laws(n, transpositions)
    p0 = sum((p for ratio, p in law.items() if ratio > 1), Fraction())
    p1 = sum((ratio*p for ratio, p in law.items() if ratio > 1), Fraction())
    pairs = copies // 2
    null = [math.comb(pairs, count)*p0**count*(1-p0)**(pairs-count) for count in range(pairs+1)]
    alt = [math.comb(pairs, count)*p1**count*(1-p1)**(pairs-count) for count in range(pairs+1)]
    if sum(null) != 1 or sum(alt) != 1:
        raise ValueError("pair-event law lost probability mass")
    tv = sum(abs(a-b) for a, b in zip(null, alt))/2
    return {"copies": copies, "pairs_measured": pairs,
        "positive_event_null_probability": str(p0), "positive_event_hidden_probability": str(p1),
        "exact_total_variation": str(tv), "total_variation": float(tv),
        "quantum_frontend": True, "classical_unknown_input_solver": False,
        "group_qft_or_inverse_calls": 6 * pairs,
        "lower_bound_on_full_pair_likelihood_readout": True,
        "uniform_fixed_point_free_full_label_score": "involution_character_arithmetic.independent_pair_label_likelihood" if 2*transpositions == n else None,
        "finite_binomial_calibration_not_uniform_degree_algorithm": True,
        "unused_odd_copy_charged_but_ignored": copies % 2 == 1}


def prefix_tail_envelope(record: dict, *, tail_start: int = 32) -> dict:
    """Complete an all-copy bound from a finite exact prefix and monotone tails."""
    certificates = record.get("decay_certificates", [])
    if (type(tail_start) is not int or tail_start < 4 or len(certificates) != 2
            or record.get("decay_certificates_replayed") != [True, True]):
        return {"certified": False, "reason": "both replayed decay certificates required"}
    null = {r["copies"]: _fraction(r) for r in record["null"]["rows"]}
    alternative = {r["copies"]: _fraction(r) for r in record["alternative"]["rows"]}
    if any(k not in null or k not in alternative for k in range(3, tail_start)):
        return {"certified": False, "reason": "exact finite prefix has missing copy counts"}
    values = {k: abs(null[k]-alternative[k])/2 for k in range(3, tail_start)}
    peak = max(values.values())
    tails = [sum(certified_moment_cap(c, OverlapEchoProgram(record["degree"], record["transpositions"], k))
                 for c in certificates)/2 for k in (tail_start, tail_start+1)]
    if any(value >= peak for value in tails):
        return {"certified": False, "reason": "parity-tail bounds do not lie below the exact prefix maximum"}
    pair = Fraction(pair_event_baseline(record["degree"], record["transpositions"], 3)["exact_total_variation"])
    return {"certified": True, "prefix_first_copy_count": 3, "prefix_last_copy_count": tail_start-1,
        "prefix_count": len(values), "tail_first_copy_count": tail_start,
        "tail_parity_caps": [_hex_fraction(value) for value in tails],
        "all_copy_tv_cap": _hex_fraction(peak), "exact_maximizing_copy_counts": [k for k, value in values.items() if value == peak],
        "one_pair_tv": str(pair), "one_pair_dominates_every_copy_count": pair > peak,
        "scope": "this fixed degree/class, ONE round and the specified X readout; not an asymptotic degree bound"}


def build_transfer_audit(*, degrees: tuple[int, ...] = (3, 4, 6), copies: tuple[int, ...] = (3, 4, 6, 8, 12, 18, 24, 36, 48, 64)) -> dict:
    from coset_overlap_echo import exact_three_copy_echo, source_block_control
    if any(type(n) is not int or n not in (3, 4, 6) for n in degrees):
        raise ValueError("audit baselines support S3, S4 and S6 controls")
    if 3 not in copies:
        raise ValueError("an audit must include the independent three-copy anchor")
    records, comparisons, bound_checks = [], [], []
    for n in degrees:
        t = n // 2
        evaluation_copies = tuple(sorted(set(copies) | (set(range(3, 32)) if n == 6 else set())))
        program = OverlapEchoProgram(n, t, max(evaluation_copies), 1)
        hidden = involution_conjugacy_class(n, t)[0]
        null = exact_path_moments(program, evaluation_copies, hidden=None)
        alternative = exact_path_moments(program, evaluation_copies, hidden=hidden)
        laws = []
        for null_row, alt_row in zip(null["rows"], alternative["rows"]):
            m0, mh = _fraction(null_row), _fraction(alt_row)
            k = null_row["copies"]
            tv = abs(mh-m0)/2
            baseline = pair_event_baseline(n, t, k)
            laws.append({"copies": k, "exact_output_total_variation": str(tv),
                         "output_total_variation": float(tv),
                         "fixed_minus_means_null_success": str(Fraction(1, 2)+(mh-m0)/4),
                         "pair_event_baseline": baseline,
                         "echo_beats_pair_event": tv > Fraction(baseline["exact_total_variation"])})
            if k == 3:
                prior = exact_three_copy_echo(n, t)
                comparisons.append(m0 == Fraction(prior["null_word_moment"]) and all(mh == Fraction(v) for v in prior["per_hidden_moments"]))
            if n == 3 and k == 4:
                physical = source_block_control(OverlapEchoProgram(n, t, k, 1))
                comparisons.append(physical["verified"] and abs(float(tv)-physical["output_total_variation"]) < 1e-9)
        certificates = [find_decay_witness(build_orbit_transfer(n, t, h)) for h in (None, hidden)]
        replayed = [replay_decay_certificate(build_orbit_transfer(n, t, h), certificate)
                    if certificate.get("certified") else False for h, certificate in zip((None, hidden), certificates)]
        caps = []
        if all(replayed):
            for k in sorted(set(evaluation_copies) | {128, 256, 1024}):
                cap = sum(certified_moment_cap(certificate, OverlapEchoProgram(n, t, k)) for certificate in certificates) / 2
                caps.append({"copies": k, "exact_output_tv_upper_bound": _hex_fraction(cap), "output_tv_upper_bound": float(cap)})
            for row, m0, mh in zip(laws, null["rows"], alternative["rows"]):
                p = OverlapEchoProgram(n, t, row["copies"])
                bound_checks.extend(abs(_fraction(value)) <= certified_moment_cap(certificate, p)
                                   for value, certificate in zip((m0, mh), certificates))
        record = {"degree": n, "transpositions": t, "null": null,
                        "alternative": alternative, "output_laws": laws,
                        "decay_certificates": certificates, "decay_certificates_replayed": replayed,
                        "all_copy_bound_rows": caps, "requested_copy_counts": list(copies)}
        record["prefix_tail_envelope"] = prefix_tail_envelope(record)
        records.append(record)
    checked = bool(records and comparisons and all(comparisons) and all(bound_checks))
    return {"records": records, "independent_comparisons": comparisons,
            "exact_moments_below_certified_bounds": bound_checks, "verified": checked,
            "rounds_supported": 1, "class_covariance_justifies_representative": True,
            "all_hidden_members_recomputed_at_large_copy_counts": False,
            "fixed_degree_copy_sweep_is_growing_degree_evidence": False,
            "temporal_rounds_equal_degree_evaluated": False,
            "novelty_established": False, "speedup_claim_allowed": False}


def build_transfer_report(**kwargs) -> dict:
    audit = build_transfer_audit(**kwargs)
    s6 = next((r for r in audit["records"] if r["degree"] == 6), None)
    decay = bool(audit["verified"] and s6 and all(s6["decay_certificates_replayed"]))
    simple = decay and all(Fraction(int(c["ratio"]["numerator_hex"], 16), int(c["ratio"]["denominator_hex"], 16)) == Fraction(3, 4)
                           and all(Fraction(int(c[key]["numerator_hex"], 16), int(c[key]["denominator_hex"], 16)) <= 3
                                   for key in ("even_copies_prefactor", "odd_copies_prefactor")) for c in s6["decay_certificates"])
    return {"created_at": utc_now(), "derivation_document": "research/COHERENT_OVERLAP_TRANSFER.md",
        "transfer_audit": audit,
        "claim_gate": {"exact_transfer_controls_verified": audit["verified"],
            "s6_one_round_all_copy_decay_certified": decay,
            "s6_simple_tv_bound_three_times_three_quarters_power": bool(simple),
            "s6_all_copy_one_pair_dominance_certified": bool(decay and s6["prefix_tail_envelope"].get("certified") is True and s6["prefix_tail_envelope"].get("one_pair_dominates_every_copy_count") is True),
            "growing_degree_bound_proved": False, "repeated_temporal_round_bound_proved": False,
            "classical_dequantization_proved": False, "independently_reviewed": False,
            "novelty_established": False, "speedup_claim_allowed": False},
        "headline_metrics": {"degree_control_count": len(audit["records"]),
            "exact_output_law_count": sum(len(r["output_laws"]) for r in audit["records"]),
            "finite_control_failure_count": sum(not value for value in audit["independent_comparisons"] + audit["exact_moments_below_certified_bounds"]),
            "s6_all_copy_decay_certificate_count": sum(s6["decay_certificates_replayed"]) if s6 else 0,
            "finite_echo_wins_over_pair_event": sum(row["echo_beats_pair_event"] for r in audit["records"] for row in r["output_laws"]),
            "growing_degree_speedup_count": 0},
        "status": "derived-s6-one-round-all-copy-decay-review-pending" if decay else "exact-transfer-controls-only" if audit["verified"] else "control-failure",
        "summary": "An exact conjugation-orbit transfer evaluates long one-round echoes without full quantum-state matrices. Integer certificates bound the S6 one-round output TV by 3*(3/4)^floor((K-2)/2), capped at one; growing degree and repeated temporal rounds remain unresolved." if simple else "Exact spatial echo transfer evaluated; a complete S6 all-copy decay certificate is not available.",
        "falsifiers_triggered": ["At fixed S6, increasing copies in the one-round negative-character echo drives both readout laws to a fair coin exponentially; it cannot amplify this signal."] if decay else [],
        "next_experiments": ["Derive a degree-uniform transfer estimate or a costed temporal-history contraction; do not extend the one-round S6 certificate by changing labels.",
                             "Investigate a local-return/light-cone bound for repeated words without assuming random-gate mixing; otherwise pivot rather than tuning more finite echo variants."],
    }


def write_transfer_report(output_path: Path = REPORT_PATH, *, write_registry: bool = True,
                          registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
                          registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
                          registry_result_id: str | None = None, **kwargs) -> dict:
    payload = build_transfer_report(**kwargs)
    payload["artifacts"] = {"report": str(output_path)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}-COSET",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id,
            created_at=payload["created_at"], status=payload["status"], summary=payload["summary"],
            metrics=payload["headline_metrics"], falsifiers_triggered=payload["falsifiers_triggered"], artifacts=payload["artifacts"]))
        if payload["claim_gate"]["s6_simple_tv_bound_three_times_three_quarters_power"]:
            upsert_negative_result(NegativeResultRecord(
                id="S6-ONE-ROUND-OVERLAP-ECHO-ALL-COPY-DECAY", source=str(output_path),
                claim="More copies amplify the fixed-S6 one-round negative-character echo into a useful asymptotic detector.",
                reason_invalid=("Exact positive transfer inequalities give output TV<=min(1,3*(3/4)^floor((K-2)/2)) for every K>=3. An exact K=3..31 prefix and both parity tails prove the global maximum is 16843/303750 at K=3, below one pair's TV=1271/7200."
                                if payload["claim_gate"]["s6_all_copy_one_pair_dominance_certified"] else
                                "Exact positive transfer inequalities give output TV<=min(1,3*(3/4)^floor((K-2)/2)) for every K>=3; long-copy rational controls also lose to a pair-event quantum measurement."),
                lesson="This is a fixed-degree, one-round, specified-readout obstruction. It is not a general HSP, growing-degree or multiple-round lower bound, not a classical unknown-input solver, and not a novelty certificate.",
                applies_to=[registry_candidate_id], evidence={"artifact": str(output_path), "review_status": "derived-review-pending"}))
    return payload


def replay_transfer_report(path: Path = REPORT_PATH) -> dict:
    """Rebuild kernels and replay the exact claimed S6 bound from saved vectors."""
    issues, count, prefix_rows = [], 0, 0
    try:
        payload = json.loads(path.read_text())
        records = [r for r in payload["transfer_audit"]["records"] if r["degree"] == 6]
        if len(records) != 1 or records[0]["transpositions"] != 3:
            raise ValueError("exactly one S6 fixed-point-free record required")
        certificates = records[0]["decay_certificates"]
        if len(certificates) != 2:
            raise ValueError("both null and hidden certificates required")
        expected = (None, involution_conjugacy_class(6, 3)[0])
        for hidden, certificate in zip(expected, certificates):
            kernel = build_orbit_transfer(6, 3, hidden)
            if not replay_decay_certificate(kernel, certificate):
                raise ValueError("saved witness, scope, fingerprint or prefactor failed exact replay")
            ratio = certificate["ratio"]
            if Fraction(int(ratio["numerator_hex"], 16), int(ratio["denominator_hex"], 16)) != Fraction(3, 4):
                raise ValueError("saved contraction rate does not prove the stated 3/4 bound")
            if any(Fraction(int(certificate[key]["numerator_hex"], 16), int(certificate[key]["denominator_hex"], 16)) > 3
                   for key in ("even_copies_prefactor", "odd_copies_prefactor")):
                raise ValueError("saved prefactor does not prove the stated factor three")
            count += 1
        for hidden, key in zip(expected, ("null", "alternative")):
            stored = {r["copies"]: _fraction(r) for r in records[0][key]["rows"]}
            if len(stored) != len(records[0][key]["rows"]):
                raise ValueError("duplicate copy counts in saved sweep")
            rebuilt = exact_path_moments(OverlapEchoProgram(6, 3, 31), tuple(range(3, 32)), hidden=hidden)
            for row in rebuilt["rows"]:
                if stored.get(row["copies"]) != _fraction(row):
                    raise ValueError("saved finite-prefix moment failed exact CRT replay")
                prefix_rows += 1
        envelope = prefix_tail_envelope(records[0])
        if (envelope.get("certified") is not True or envelope.get("one_pair_dominates_every_copy_count") is not True
                or envelope != records[0]["prefix_tail_envelope"]):
            raise ValueError("saved all-copy maximum failed prefix-and-tail replay")
    except (OSError, KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        issues.append(str(error))
    return {"valid": not issues and count == 2 and prefix_rows == 58, "replayed_certificate_count": count,
            "exact_prefix_moments_replayed": prefix_rows,
            "full_requested_sweep_replayed": False,
            "replayed_claims": ["exponential all-copy decay", "global maximum at K=3 and domination by one pair"],
            "issues": issues, "scope": "S6, fixed-point-free class, one round, specified X readout, all K>=3",
            "formal_proof_or_novelty_certification": False, "speedup_claim_allowed": False}

"""Counterchecks for two overbroad nonabelian no-go records, not new algorithms.

Execute legal public candidate tests on regular coset states, distinguish spin-one
from spin-half commutants, and measure an invariant with a constant-size circuit
despite an exponentially large commutant. None supplies a GI receiver.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, permutations
import json
from math import comb, factorial, log, log1p
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ACTIVE = ROOT / "research/registry/negative_results.json"
ARCHIVE = ROOT / "research/registry/quarantined_campaign_negatives.json"
REPORT = ROOT / "research/representation/nonabelian_barrier_scope_audit.json"
NOTE = "research/NONABELIAN_BARRIER_SCOPE_AUDIT.md"
REVIEWED = {
    "NEG-SYMMETRIC-GROUP-KRONECKER-RACAH-BARRIER": {
        "sha256": "0e9f13606c9c368f56b8f47f8362c46e06439aa42e6d7103208e095e3759bac6",
        "reasons": [
            "MRS studies the long-involution GI ensemble, not all transposition subgroups.",
            "A public candidate Hadamard test has Theta(1/n^2) information for a uniform hidden transposition.",
            "Commutant dimension is not a quantum gate lower bound; worst-case coefficient hardness does not supply that reduction.",
            "EHK is a query upper bound, not the cited copy lower bound or a polynomial-time receiver.",
        ],
    },
    "NEG-SU2-COMPACT-LIE-HSP-COMMUTANT-INFLATION": {
        "sha256": "6baeff6e7033b74b8353c70f82010cc64b3b01da74b84365725695645119580c",
        "reasons": [
            "Catalan dimensions apply to tensor powers of spin half, not spin one: spin-one counts at M=2,3 are 3,15.",
            "Exponential commutant dimension does not imply exponentially costly measurements or recoupling circuits.",
            "The torus zero-weight state is not an extremal spin-coherent state.",
            "No specified continuous-input precision model or valid reduction proves exclusion from BQP.",
        ],
    },
}


def positive_integer(value, name, low=1, high=10**6):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")


def record_hash(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def right_swap(g, pair):
    """Right multiply an array-encoded permutation by a PUBLIC transposition."""
    i, j = pair
    result = list(g)
    result[i], result[j] = result[j], result[i]
    return tuple(result)


def transposition_coset_control(n):
    """Exact sparse Hadamard branches for EVERY g and hidden transposition h.

    n! enumeration is a bounded verifier only, not an algorithmic subroutine.
    The tested public element is fixed to (0,1), independently of h.
    """
    positive_integer(n, "bounded regular-state verification size", 3, 6)
    group = tuple(permutations(range(n)))
    public = (0, 1)
    rows = []
    for hidden in combinations(range(n), 2):
        probabilities = set()
        for g in group:
            support = (g, right_swap(g, hidden))
            # After H, controlled R_public, H: amplitudes are integers/(2 sqrt(2)).
            plus, minus = Counter(support), Counter(support)
            for x in support:
                y = right_swap(x, public)
                plus[y] += 1
                minus[y] -= 1
            p_plus = Fraction(sum(c*c for c in plus.values()), 8)
            p_minus = Fraction(sum(c*c for c in minus.values()), 8)
            expected = Fraction(1) if hidden == public else Fraction(1, 2)
            if p_plus != expected or p_plus + p_minus != 1:
                raise ArithmeticError("actual coset-state branches contradict the trace identity")
            probabilities.add(str(p_plus))
        rows.append({"hidden_transposition": list(hidden), "P_plus": sorted(probabilities)})
    return {"n": n, "group_order": factorial(n), "coset_states_checked": len(rows)*len(group),
            "public_test_transposition": list(public), "test_uses_hidden_element": False,
            "actual_sparse_H_controlled_R_H_branches": True, "rows": rows}


def candidate_test_information(n):
    """Analytic scaling only; no n! state or candidate table is allocated."""
    positive_integer(n, "permutation degree", 3, 10**6)
    size = comb(n, 2)
    x = 1/size
    # 1 - h2((1+x)/2), evaluated without subtracting nearly equal entropies.
    if x < 0.01:
        deficit = sum(x**(2*k)/((2*k)*(2*k-1)) for k in range(1, 6))/log(2)
    else:
        deficit = ((1+x)*log1p(x)+(1-x)*log1p(-x))/(2*log(2))
    return {"n": n, "ensemble_size": size, "mode": "ANALYTIC_NOT_STATE_SIMULATION",
            "mutual_information_bits_numeric": x-deficit,
            "mutual_information_lower_exact": str(Fraction(1, size)-Fraction(2, size*size)),
            "controlled_public_word_swaps_Fredkin": (n-1).bit_length(),
            "ancilla_H_gates": 2, "coset_states_used": 1,
            "classical_candidate_enumeration_queries_upper": size+1,
            "classical_test": "Query f(e) once and f(t) for each public transposition; equality identifies h.",
            "new_quantum_speedup": False, "hard_GI_ensemble_solved": False}


def su2_multiplicities(twice_spin, copies):
    """Exact Clebsch-Gordan recurrence, with integer doubled-spin labels."""
    positive_integer(twice_spin, "twice the spin", 1, 8)
    positive_integer(copies, "tensor copies", 0, 64)
    multiplicities = {0: 1}
    for _ in range(copies):
        updated = Counter()
        for spin, multiplicity in multiplicities.items():
            for total in range(abs(spin-twice_spin), spin+twice_spin+1, 2):
                updated[total] += multiplicity
        multiplicities = dict(sorted(updated.items()))
    if sum(m*(j+1) for j, m in multiplicities.items()) != (twice_spin+1)**copies:
        raise ArithmeticError("Clebsch-Gordan dimension mismatch")
    return multiplicities


def commutant_dimension(twice_spin, copies):
    return sum(m*m for m in su2_multiplicities(twice_spin, copies).values())


def collective_generators(twice_spin, copies):
    """Bound dense matrices BEFORE allocation; only tiny independent controls."""
    positive_integer(twice_spin, "dense twice spin", 1, 2)
    positive_integer(copies, "dense copies", 1, 6)
    dimension = (twice_spin+1)**copies
    if dimension > 64:
        raise ValueError("dense Hilbert dimension exceeds 64; use the analytic recurrence")
    spin = twice_spin/2
    m = np.arange(spin, -spin-1, -1)
    raising = np.zeros((twice_spin+1, twice_spin+1), complex)
    for column in range(1, len(m)):
        raising[column-1, column] = np.sqrt(spin*(spin+1)-m[column]*(m[column]+1))
    local = ((raising+raising.T)/2, (raising-raising.T)/(2j), np.diag(m))
    totals = []
    for operator in local:
        total = np.zeros((dimension, dimension), complex)
        for position in range(copies):
            term = np.ones((1, 1), complex)
            for i in range(copies):
                term = np.kron(term, operator if i == position else np.eye(twice_spin+1))
            total += term
        totals.append(total)
    return totals


def dense_commutant_nullity(twice_spin, copies):
    positive_integer(twice_spin, "nullspace twice spin", 1, 2)
    positive_integer(copies, "nullspace copies", 1, 3)
    if (twice_spin+1)**copies > 9:
        raise ValueError("commutator superoperator control capped at Hilbert dimension 9")
    generators = collective_generators(twice_spin, copies)
    dimension = len(generators[0])
    equations = np.vstack([np.kron(np.eye(dimension), J)-np.kron(J.T, np.eye(dimension))
                           for J in generators])
    singular_values = np.linalg.svd(equations, compute_uv=False)
    rank = int(np.count_nonzero(singular_values > 1e-10))
    return {"twice_spin": twice_spin, "copies": copies, "Hilbert_dimension": dimension,
            "commutator_linear_system_shape": list(equations.shape),
            "numerical_nullity": dimension**2-rank, "rank_threshold": 1e-10,
            "smallest_nonzero_singular_value": float(min(singular_values[singular_values > 1e-10])),
            "exact_recurrence_dimension": commutant_dimension(twice_spin, copies)}


def invariant_swap_control(copies):
    """Actual two-gate Bell readout of SWAP, identity on all other qubits."""
    positive_integer(copies, "dense qubit copies", 2, 6)
    H = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    swap2 = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    bell = CX @ np.kron(H, np.eye(2))
    spectators = np.eye(2**(copies-2))
    U, swap = np.kron(bell, spectators), np.kron(swap2, spectators)
    expected = np.kron(np.diag([1, 1, 1, -1]), spectators)
    residual = float(np.max(np.abs(U.conj().T @ swap @ U-expected)))
    commutator = max(float(np.max(np.abs(swap @ J-J @ swap)))
                     for J in collective_generators(1, copies))
    if residual > 1e-12 or commutator > 1e-12:
        raise ArithmeticError("invariant Bell measurement failed")
    return {"qubits": copies, "commutant_dimension": commutant_dimension(1, copies),
            "readout_gates_in_order": ["CNOT(0,1)", "H(0)"], "Z_readouts": [0, 1],
            "antisymmetric_outcome": "11", "gate_count": 2,
            "diagonalization_max_residual": residual, "SU2_generator_commutator_max": commutator,
            "arbitrary_optimal_HSP_measurement_compiled": False}


def reviewed_originals():
    active, archive = json.loads(ACTIVE.read_text()), json.loads(ARCHIVE.read_text())
    originals = {}
    for key, review in REVIEWED.items():
        live = [r for r in active if r["id"] == key]
        saved = [r for r in archive if r["id"] == key]
        if len(live) > 1 or len(saved) > 1 or not (live or saved):
            raise ValueError("duplicate or missing reviewed negative")
        original = live[0] if live else saved[0]["original_record"]
        if record_hash(original) != review["sha256"]:
            raise ValueError("reviewed negative changed; independent review required")
        if saved and (saved[0]["original_record"] != original
                      or saved[0]["status"] != "QUARANTINED_OVERBROAD_NO_GO"):
            raise ValueError("archive differs from reviewed evidence")
        originals[key] = original
    return originals


def quarantine_reviewed_negatives():
    """Preserve exact reviewed originals, refuse changed evidence and stale writes."""
    from core.research_registry import _write_json
    before_active, before_archive = ACTIVE.read_bytes(), ARCHIVE.read_bytes()
    active, archive = json.loads(before_active), json.loads(before_archive)
    originals = reviewed_originals()
    existing = {r["id"] for r in archive}
    for key, review in REVIEWED.items():
        if key not in existing:
            archive.append({"id": key, "status": "QUARANTINED_OVERBROAD_NO_GO",
                            "reviewed_on": "2026-10-19", "review": NOTE,
                            "retraction_reasons": review["reasons"],
                            "original_record": originals[key], "original_sha256": review["sha256"],
                            "original_checks_are_general_proofs": False,
                            "reinstatement_requires_scoped_mathematical_review": True})
    if ACTIVE.read_bytes() != before_active or ARCHIVE.read_bytes() != before_archive:
        raise ValueError("registry changed during review; reread before retry")
    if any(key not in existing for key in REVIEWED):
        _write_json(ARCHIVE, archive)
    if ACTIVE.read_bytes() != before_active:
        raise ValueError("active registry changed after archival; retry")
    if any(r["id"] in REVIEWED for r in active):
        _write_json(ACTIVE, [r for r in active if r["id"] not in REVIEWED])


def build_report():
    originals = reviewed_originals()
    multiplicities = []
    for copies in range(1, 21):
        multiplicities.append({"copies": copies,
                               "spin_half_commutant": commutant_dimension(1, copies),
                               "spin_one_commutant": commutant_dimension(2, copies),
                               "Catalan": comb(2*copies, copies)//(copies+1),
                               "mode": "EXACT_RECURRENCE_NOT_STATE_SIMULATION"})
    return {
        "schema_version": 1, "status": "TWO_OVERBROAD_NEGATIVE_RECORDS_COUNTERCHECKED",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reviewed_original_hashes": {key: record_hash(r) for key, r in originals.items()},
        "regular_coset_state_controls": [transposition_coset_control(n) for n in (3, 4, 5, 6)],
        "candidate_test_scaling": [candidate_test_information(n) for n in (8, 16, 64, 1024, 10**6)],
        "SU2_tensor_multiplicity_controls": multiplicities,
        "independent_dense_commutant_controls": [dense_commutant_nullity(2, 2), dense_commutant_nullity(1, 3)],
        "invariant_measurement_controls": [invariant_swap_control(m) for m in (2, 3, 4, 6)],
        "large_commutant_small_measurement": {"qubits": 20, "Catalan_dimension": commutant_dimension(1, 20),
                                             "measurement_gates": 2, "mode": "ANALYTIC_NO_20_QUBIT_MATRIX"},
        "retained_scoped_barriers": [
            "Weak irrep labels cannot identify conjugate subgroup orientations.",
            "MRS: single-coset POVMs fail on the specified long-involution GI ensemble.",
            "HRS: useful GI coset measurements require Omega(n log n) jointly measured states.",
            "EHK supplies polynomial queries, not a polynomial-time receiver.",
            "Efficient Schur transforms do not compile an arbitrary GI optimal measurement.",
        ],
        "primary_sources": ["https://arxiv.org/abs/quant-ph/0501056", "https://arxiv.org/abs/quant-ph/0511148",
                            "https://arxiv.org/abs/quant-ph/0401083", "https://arxiv.org/abs/quant-ph/0407082"],
        "retraction_reasons": {key: r["reasons"] for key, r in REVIEWED.items()},
        "new_quantum_algorithm": False, "general_nonabelian_HSP_solved": False,
        "continuous_HSP_input_model_specified": False, "general_circuit_lower_bound_proved": False,
        "speedup_claim_allowed": False, "accepted_speedup_candidate": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="Write the bounded countercheck report.")
    parser.add_argument("--quarantine", action="store_true", help="Archive ONLY the two hash-bound reviewed negatives.")
    args = parser.parse_args()
    report = build_report()
    if args.quarantine:
        quarantine_reviewed_negatives()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "reviewed_ids": list(REVIEWED),
                      "report_written": args.write, "quarantined": args.quarantine,
                      "coset_branches_checked": sum(r["coset_states_checked"] for r in report["regular_coset_state_controls"]),
                      "speedup_claim_allowed": False}, indent=2))


if __name__ == "__main__":
    main()

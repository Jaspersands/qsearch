"""Scoped coset identities and constructive access; broad trilemma retracted.

Invariant POVM effects cannot distinguish a conjugacy orbit. Noncommuting
pair sums cannot share an eigenbasis. Neither statement nor an exponential
commutant dimension proves an exponential circuit lower bound. Finite
physical controls here are not an HSP receiver or a new speedup.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from itertools import combinations, product
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/COSET_MULTIPLICITY_CARRIER_TRILEMMA.md"
REPORT = ROOT / "research/representation/coset_multiplicity_carrier_trilemma.json"
NEGATIVE_RESULT_ID = "NEG-COSET-MULTIPLICITY-CARRIER-DECOUPLING-TRILEMMA"


def _integer(value: int, name: str, low: int, high: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")


def standard_rep_matrix(perm: Tuple[int, ...], n: int) -> np.ndarray:
    """Exact NONORTHONORMAL coordinates; not physical computational amplitudes."""
    _integer(n, "permutation degree", 2, 256)
    if sorted(perm) != list(range(n)):
        raise ValueError("invalid permutation")
    dim = n - 1
    matrix = np.zeros((dim, dim), dtype=np.int64)
    for col in range(dim):
        p_col = perm[col]
        p_last = perm[n - 1]
        if p_col < dim:
            matrix[p_col, col] += 1
        if p_last < dim:
            matrix[p_last, col] -= 1
    return matrix


def verify_three_copy_commutator(n: int) -> Dict[str, Any]:
    """Verify exact closed-form commutator entry [K_12, K_23]_{(0,0,0),(0,0,1)} = n."""
    _integer(n, "bounded commutator control", 3, 12)
    dim = n - 1
    dim2 = dim * dim

    # Compute two-copy class sum K = sum_{tau} V(tau) (x) V(tau)
    K = np.zeros((dim2, dim2), dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            p = list(range(n))
            p[i], p[j] = p[j], p[i]
            V = standard_rep_matrix(tuple(p), n)
            K += np.kron(V, V)

    # Compute [K_12, K_23] entry at row (0,0,0) [index 0], col (0,0,1) [index 1]
    # K_12 = K (x) I_dim, K_23 = I_dim (x) K
    val = 0
    dim3 = dim * dim * dim
    for mid in range(dim3):
        m1 = mid // (dim * dim)
        rem = mid % (dim * dim)
        m2 = rem // dim
        m3 = rem % dim

        k12_0_mid = K[0, m1 * dim + m2] if m3 == 0 else 0
        k23_mid_1 = K[m2 * dim + m3, 1] if m1 == 0 else 0

        k23_0_mid = K[0, m2 * dim + m3] if m1 == 0 else 0
        k12_mid_1 = K[m1 * dim + m2, 0] if m3 == 1 else 0

        val += int(k12_0_mid * k23_mid_1 - k23_0_mid * k12_mid_1)

    return {
        "n": n,
        "standard_dimension": dim,
        "three_copy_dimension": dim3,
        "observed_witness_entry": val,
        "theoretical_witness_entry": n,
        "entry_matches_closed_form": val == n,
        "is_strictly_noncommuting": val != 0,
        "basis": "NONORTHONORMAL_DIFFERENCE_COORDINATES",
        "mode": "EXACT_BOUNDED_MATRIX_CONTROL",
        "general_circuit_lower_bound": False,
    }


def orthonormal_standard_matrix(perm: Tuple[int, ...], n: int) -> np.ndarray:
    """Bounded physical standard representation in the Helmert basis."""
    _integer(n, "bounded physical representation", 3, 8)
    if sorted(perm) != list(range(n)):
        raise ValueError("invalid permutation")
    basis = np.zeros((n, n-1))
    for j in range(n-1):
        denominator = math.sqrt((j+1)*(j+2))
        basis[:j+1, j] = 1/denominator
        basis[j+1, j] = -(j+1)/denominator
    permutation = np.zeros((n, n))
    permutation[list(perm), np.arange(n)] = 1
    return basis.T @ permutation @ basis


def verify_commutant_zero_information(n: int) -> Dict[str, Any]:
    """Actual two-copy conditional coset states and a binary invariant POVM.

    rho_h=(I+V(h))/(2(n-2)) is the normalized standard-irrep column state
    for a transposition subgroup. Conditioning on this irrep is explicit;
    the experiment does not assume it has significant natural source mass.
    """
    _integer(n, "bounded Born-probability control", 3, 8)
    dim = n - 1
    omega = np.eye(dim).reshape(-1)/math.sqrt(dim)
    projector = np.outer(omega, omega)
    probabilities, minimum_eigenvalues, traces, commutators = [], [], [], []
    for i, j in combinations(range(n), 2):
        perm = list(range(n))
        perm[i], perm[j] = perm[j], perm[i]
        v = orthonormal_standard_matrix(tuple(perm), n)
        rho = (np.eye(dim)+v)/(2*(n-2))
        state = np.kron(rho, rho)
        traces.append(float(np.trace(state)))
        minimum_eigenvalues.append(float(np.linalg.eigvalsh(state)[0]))
        joint_action = np.kron(v, v)
        commutators.append(float(np.max(np.abs(projector@joint_action-joint_action@projector))))
        probability = float(np.trace(projector@state))
        probabilities.append([probability, 1-probability])
    probabilities = np.asarray(probabilities)
    mean = probabilities.mean(axis=0)
    information = float(np.sum(probabilities*np.log2(probabilities/mean))/len(probabilities))
    variation = float(np.ptp(probabilities, axis=0).max())
    physical = min(minimum_eigenvalues) >= -1e-12 and max(abs(t-1) for t in traces) < 1e-12
    physical = physical and float(probabilities.min()) >= 0 and float(probabilities.max()) <= 1
    constant = variation < 1e-12
    return {
        "n": n,
        "transposition_count": len(probabilities),
        "conditional_standard_irrep": True,
        "single_copy_irrep_probability_exact": str(Fraction(2*(n-1)*(n-2), math.factorial(n))),
        "expected_invariant_probability_exact": str(Fraction(1, (n-1)*(n-2))),
        "conditional_born_probabilities": probabilities.tolist(),
        "probability_variation": variation,
        "minimum_state_eigenvalue_numeric": min(minimum_eigenvalues),
        "maximum_trace_one_residual": max(abs(t-1) for t in traces),
        "effect_commutator_max": max(commutators),
        "physical_states_and_probabilities_verified": physical,
        "is_constant_across_class": constant,
        "mutual_information_bits_numeric": max(0.0, information),
        "zero_information_verified": physical and constant and max(commutators) < 1e-12,
        "mode": "BOUNDED_PHYSICAL_BORN_CONTROL_NOT_A_GENERAL_THEOREM_TEST",
    }


def compute_commutant_dimension(n: int, k: int) -> int:
    """Compute dim(Commutant(V^k)) = (1/n!) sum_{g in S_n} (fix(g) - 1)^{2k}."""
    _integer(n, "permutation degree", 2, 256)
    _integer(k, "tensor copies", 0, 128)
    # Rencontres numbers count permutations with f fixed points, without n! enumeration.
    derangements = [1, 0]
    for j in range(2, n+1):
        derangements.append((j-1)*(derangements[-1]+derangements[-2]))
    n_fact = math.factorial(n)
    total = sum(math.comb(n, f)*derangements[n-f]*(f-1)**(2*k) for f in range(n+1))
    assert total % n_fact == 0
    return total // n_fact


def build_scaling_profiles(
    n_values: Sequence[int] = (3, 4, 5, 6, 7, 8, 10, 12, 16)
) -> List[Dict[str, Any]]:
    """Exact character dimensions; never convert dimensions into gate bounds."""
    profiles: List[Dict[str, Any]] = []

    for n in n_values:
        _integer(n, "profile degree", 3, 128)
        if n <= 6:
            comm_audit = verify_three_copy_commutator(n)
            info_audit = verify_commutant_zero_information(n)
            witness = comm_audit["observed_witness_entry"]
            info_bits = info_audit["mutual_information_bits_numeric"]
        else:
            witness = n
            info_bits = 0.0

        dim_k3 = compute_commutant_dimension(n, 3)
        lower = Fraction((n-1)**(2*n), math.factorial(n))
        dimension = compute_commutant_dimension(n, n)

        profiles.append({
            "n": n,
            "standard_dimension": n - 1,
            "commutator_witness_entry": witness,
            "commutator_matches_n": witness == n,
            "commutant_mutual_information_bits": info_bits,
            "commutant_dimension_k3": dim_k3,
            "commutant_dimension_k_n": dimension,
            "identity_term_dimension_lower_bound_exact": str(lower),
            "dimension_lower_bound_log2_numeric": math.log2(lower.numerator)-math.log2(lower.denominator),
            "dimension_lower_bound_verified": lower <= dimension,
            "commutator_evidence": "BOUNDED_MATRIX_CONTROL" if n <= 6 else "ANALYTICAL_IDENTITY",
            "information_evidence": "PHYSICAL_BORN_CONTROL" if n <= 6 else "COVARIANCE_THEOREM_NOT_EXECUTED",
            "general_circuit_lower_bound_proved": False,
            "status": "PASS",
        })

    return profiles


def pair_class_sum_access_control(n: int = 3, copies: int = 3) -> Dict[str, Any]:
    """Explicit finite PREPARE/SELECT compression for natural permutation carriers.

    The analytic access construction acts on word registers, not an n**copies
    table. This bounded dense control verifies it and its standard-subspace
    restriction. It is not a Racah transform or an informative HSP decoder.
    """
    _integer(n, "bounded SELECT degree", 3, 4)
    _integer(copies, "bounded SELECT copies", 3, 3)
    words = tuple(product(range(n), repeat=copies))
    index = {word: i for i, word in enumerate(words)}
    pairs = tuple(combinations(range(n), 2))
    dimension, terms = len(words), len(pairs)
    prepare = np.vstack([np.eye(dimension)/math.sqrt(terms)]*terms)
    averages, block_errors, unitary_errors = [], [], []
    for registers in ((0, 1), (1, 2)):
        select = np.zeros((terms*dimension, terms*dimension))
        average = np.zeros((dimension, dimension))
        for label, (a, b) in enumerate(pairs):
            for column, word in enumerate(words):
                output = list(word)
                for register in registers:
                    value = output[register]
                    output[register] = b if value == a else a if value == b else value
                row = index[tuple(output)]
                select[label*dimension+row, label*dimension+column] = 1
                average[row, column] += 1/terms
        unitary_errors.append(float(np.max(np.abs(select.T@select-np.eye(terms*dimension)))))
        block_errors.append(float(np.max(np.abs(prepare.T@select@prepare-average))))
        averages.append(average)
    commutator = averages[0]@averages[1]-averages[1]@averages[0]
    standard = np.eye(n)-np.ones((n, n))/n
    subspace = np.kron(np.kron(standard, standard), standard)
    return {
        "n": n, "copies": copies, "representation": "NATURAL_PERMUTATION_WITH_STANDARD_SUBSPACE",
        "controlled_transposition_terms": terms,
        "dense_control_dimension": dimension,
        "unnormalized_class_sum_block_encoding_normalization": terms,
        "normalized_class_sum_block_encoding_normalization": 1,
        "unitarity_max_residual": max(unitary_errors),
        "prepared_block_max_residual": max(block_errors),
        "overlapping_normalized_sum_commutator_max": float(np.max(np.abs(commutator))),
        "standard_subspace_commutator_max": float(np.max(np.abs(subspace@commutator@subspace))),
        "analytic_access_plan_uses_dense_tables": False,
        "verifier_uses_dense_tables": True,
        "uniform_gate_compiler_implemented": False,
        "arbitrary_Racah_transform_compiled": False,
        "hard_coset_decoder_compiled": False,
        "speedup_claim_allowed": False,
    }


def build_report() -> Dict[str, Any]:
    """Retain valid identities and explicitly retract the unsupported exclusions."""
    small_audits = [verify_three_copy_commutator(n) for n in (3, 4, 5, 6)]
    info_audits = [verify_commutant_zero_information(n) for n in (3, 4, 5, 6)]
    scaling = build_scaling_profiles()

    all_witness_verified = all(a["entry_matches_closed_form"] for a in small_audits)
    all_zero_info_verified = all(a["zero_information_verified"] for a in info_audits)
    access = pair_class_sum_access_control()
    access_verified = (access["unitarity_max_residual"] < 1e-12
                       and access["prepared_block_max_residual"] < 1e-12
                       and access["standard_subspace_commutator_max"] > 1e-12)
    dimensions_verified = all(row["dimension_lower_bound_verified"] for row in scaling)

    report: Dict[str, Any] = {
        "report_id": "COSET-MULTIPLICITY-CARRIER-TRILEMMA-REPORT",
        "negative_result_id": NEGATIVE_RESULT_ID,
        "negative_result_status": "QUARANTINED_OVERBROAD_NO_GO",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_path": str(DERIVATION.relative_to(ROOT)),
        "summary": (
            "Invariant POVMs cannot distinguish members of one conjugacy orbit. "
            "Overlapping pair class sums are noncommuting but have structured efficient access. "
            "Exact commutant dimensions establish no circuit lower bound. The exhaustive "
            "trilemma and universal factorial-copy claim are retracted."
        ),
        "retained_scoped_statements": {
            "commutant_zero_information": (
                "For a covariant state ensemble and invariant POVM effects, Born probabilities "
                "are constant WITHIN a conjugacy orbit. A later carrier-sensitive measurement "
                "is not covered unless its total effects are invariant."
            ),
            "pair_non_commutation": (
                "[K_12, K_23]_{(0,0,0),(0,0,1)} = n for all n >= 3. Overlapping pair class sums "
                "cannot share an eigenbasis; this does not exclude sequential coherent operations."
            ),
            "dimension": (
                "dim End_Sn(V^k)=(1/n!) sum_g (fix(g)-1)^(2k). Its identity summand gives "
                "a dimension lower bound, not a lower bound for a specified quantum circuit."
            ),
        },
        "retracted_claims": [
            "Factorial multiplicity dimension forces exponential Racah circuit complexity.",
            "All separable nonabelian coset measurements need Omega(n!) copies.",
            "Every receiver falls under an exhaustive computational trilemma.",
            "A trace spread of V(h) tensor I constitutes a physical mutual-information check.",
        ],
        "headline_metrics": {
            "all_commutator_witnesses_verified": all_witness_verified,
            "all_commutant_zero_information_verified": all_zero_info_verified,
            "bounded_pair_access_verified": access_verified,
            "dimension_lower_bounds_verified": dimensions_verified,
            "tail_n": scaling[-1]["n"],
            "tail_commutator_witness": scaling[-1]["commutator_witness_entry"],
            "tail_dimension_lower_bound_log2_numeric": scaling[-1]["dimension_lower_bound_log2_numeric"],
            "exhaustive_trilemma_proved": False,
            "general_circuit_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "accepted_speedup_candidate": False,
        },
        "small_commutator_audits": small_audits,
        "small_zero_information_audits": info_audits,
        "scaling_profiles": scaling,
        "constructive_pair_class_sum_access": access,
        "counterexample_reference": "research/NONABELIAN_BARRIER_SCOPE_AUDIT.md",
        "source_mass_and_useful_joint_decoder": "UNRESOLVED_FOR_HARD_ENSEMBLES",
        "status": "PASS" if (all_witness_verified and all_zero_info_verified
                               and access_verified and dimensions_verified) else "FAIL",
    }

    return report


def write_report(write_registry: bool = True) -> Path:
    """Generate corrected evidence; never reinstate the retracted negative."""
    from core.research_registry import _write_json
    from theorems.nonabelian_barrier_scope_audit import quarantine_reviewed_negatives

    report = build_report()
    if write_registry:
        quarantine_reviewed_negatives()
    _write_json(REPORT, report)
    return REPORT


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check scoped coset identities and retract the unsupported general trilemma."
    )
    parser.add_argument("--write", action="store_true", help="Write corrected report and quarantine reviewed negative")
    parser.add_argument("--no-registry", action="store_true", help="Do not update negative results registry")
    args = parser.parse_args()

    if args.write:
        path = write_report(write_registry=not args.no_registry)
        print(f"Wrote report to {path}")
    else:
        rep = build_report()
        print("=" * 70)
        print("COSET MULTIPLICITY SCOPE: BROAD TRILEMMA RETRACTED")
        print("=" * 70)
        print(f"Status: {rep['status']}")
        print(f"Commutator Witnesses Verified: {rep['headline_metrics']['all_commutator_witnesses_verified']}")
        print(f"Commutant Zero Information Verified: {rep['headline_metrics']['all_commutant_zero_information_verified']}")
        print(f"Tail Commutator Witness (n=16): {rep['headline_metrics']['tail_commutator_witness']}")
        print(f"Tail Dimension Lower Bound log2: {rep['headline_metrics']['tail_dimension_lower_bound_log2_numeric']:.2f}")
        print("General circuit lower bound: NOT ESTABLISHED")
        print("=" * 70)


if __name__ == "__main__":
    main()

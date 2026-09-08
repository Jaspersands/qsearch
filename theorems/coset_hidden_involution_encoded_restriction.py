"""Normalized subgroup restriction with an implicit multiplicity register.

E = (QFT_K tensor I_coset) FACTOR QFT_G^dagger APPEND_COLUMN.
The finite matrices below check conventions, isometry and covariance. They
are NOT the proposed implementation of the QFT primitives at growing rank.
See research/ENCODED_RESTRICTION.md for the conditional circuit reduction.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import compose_permutations, inverse_permutation
from coset_hidden_involution_bounded_support_commutant_generation import hyperoctahedral_group, _K_generators
from coset_hidden_involution_commutant_support_growth_boundary import _matrix_for_permutation
from coset_hidden_involution_paired_tower_missing_label_boundary import bipartitions, hyperoctahedral_branching_coefficient
from coset_hidden_involution_multiplicity_twirl_projection import hermitian_bounded_support_orbit_representatives
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now

REPORT_PATH = Path("research/representation/coset_hidden_involution_encoded_restriction.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIDDEN-INVOLUTION-ENCODED-RESTRICTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


def factor_left_hyperoctahedral_coset(permutation: Permutation) -> tuple[Permutation, Matching, Permutation]:
    """Return k,Q,t with g=k*t, k in K_m, Q=g^-1(P0), canonical t(Q)=P0.

This works by sorting m pairs, without enumerating K or the matching space.
Both directions are deterministic polynomial-time maps and can be made
reversible by compute/copy/uncompute. No label is measured or postselected.
"""
    degree = len(permutation)
    if degree < 2 or degree % 2 or sorted(permutation) != list(range(degree)):
        raise ValueError("expected a permutation of positive even degree")
    inverse = inverse_permutation(permutation)
    matching = tuple(sorted(tuple(sorted((inverse[2*i], inverse[2*i+1]))) for i in range(degree // 2)))
    representative = [0] * degree
    for i, (a, b) in enumerate(matching):
        representative[a], representative[b] = 2*i, 2*i+1
    t = tuple(representative)
    k = compose_permutations(permutation, inverse_permutation(t))
    return k, matching, t


@lru_cache(maxsize=4096)
def _symmetric_matrix(partition: Partition, permutation: Permutation) -> np.ndarray:
    if sum(partition) <= 1:
        return np.ones((1, 1))
    return _matrix_for_permutation(partition, permutation)


def _wreath_matrix(alpha: Partition, beta: Partition, element: Permutation) -> np.ndarray:
    """Finite induced-model irrep in signed-subset and two Young-tableau bases."""
    m, b = len(element) // 2, sum(beta)
    if sum(alpha) + b != m:
        raise ValueError("bipartition has wrong rank")
    pair_permutation = tuple(element[2*i] // 2 for i in range(m))
    flips = tuple(element[2*i] % 2 for i in range(m))
    if any(element[2*i+1] != (element[2*i] ^ 1) for i in range(m)):
        raise ValueError("element does not preserve the standard matching")
    negative_sets = tuple(combinations(range(m), b))
    positions = {subset: index for index, subset in enumerate(negative_sets)}
    width = hook_length_dimension(alpha) * hook_length_dimension(beta)
    matrix = np.zeros((len(negative_sets) * width,) * 2)
    for source, negative in enumerate(negative_sets):
        positive = tuple(i for i in range(m) if i not in negative)
        image_negative = tuple(sorted(pair_permutation[i] for i in negative))
        image_positive = tuple(sorted(pair_permutation[i] for i in positive))
        target = positions[image_negative]
        internal_alpha = tuple(image_positive.index(pair_permutation[i]) for i in positive)
        internal_beta = tuple(image_negative.index(pair_permutation[i]) for i in negative)
        sign = (-1)**sum(flips[i] for i in negative)
        matrix[target*width:(target+1)*width, source*width:(source+1)*width] = sign * np.kron(
            _symmetric_matrix(alpha, internal_alpha), _symmetric_matrix(beta, internal_beta))
    return matrix


def _logical_action_controls(compact: np.ndarray, actions: list[tuple[Permutation, np.ndarray]]) -> dict[str, Any]:
    d, copies, dimension = compact.shape
    matrix = compact.reshape(d * copies, dimension)
    logical = []
    residual = 0.0
    for _, action in actions:
        image = matrix @ action @ matrix.conj().T
        tensor = image.reshape(d, copies, d, copies)
        copy_action = sum(tensor[i, :, i, :] for i in range(d)) / d
        residual = max(residual, float(np.linalg.norm(image - np.kron(np.eye(d), copy_action))))
        logical.append(copy_action)
    return {
        "orbit_average_count": len(actions),
        "carrier_identity_tensor_logical_action_residual": residual,
        "maximum_logical_operator_norm": max((float(np.linalg.norm(a, 2)) for a in logical), default=0.0) if copies else 0.0,
        "maximum_logical_commutator_norm": max((float(np.linalg.norm(a @ b - b @ a))
                                                for a in logical for b in logical), default=0.0),
        "normalization_factor": 1,
    }


def finite_encoded_restriction(partition: Partition, *, fixed_column: int = 0) -> dict[str, Any]:
    n = sum(partition)
    if n not in (4, 6, 8) or any(part <= 0 for part in partition) or tuple(sorted(partition, reverse=True)) != partition:
        raise ValueError("dense Fourier controls are restricted to S_4, S_6 and S_8")
    m, dimension = n // 2, hook_length_dimension(partition)
    if not 0 <= fixed_column < dimension:
        raise ValueError("fixed_column is outside the irrep")
    group = tuple(permutations(range(n)))
    subgroup = hyperoctahedral_group(m)
    factorizations = [factor_left_hyperoctahedral_coset(g) for g in group]
    matchings = sorted({matching for _, matching, _ in factorizations})
    transversal = {matching: t for _, matching, t in factorizations}
    columns = np.stack([_symmetric_matrix(partition, transversal[matching])[:, fixed_column]
                        for matching in matchings], axis=1)
    subgroup_action = np.stack([_symmetric_matrix(partition, k) for k in subgroup])
    factored = math.sqrt(dimension / len(group)) * np.einsum("kab,bt->kta", subgroup_action, columns).conj()
    embedding = factored.reshape(len(group), dimension)
    actions = []
    for representative in hermitian_bounded_support_orbit_representatives(m, 4):
        rho = _symmetric_matrix(partition, representative)
        hermitian = (rho + rho.conj().T) / 2
        average = sum(k @ hermitian @ k.conj().T for k in subgroup_action) / len(subgroup)
        actions.append((representative, average))

    blocks = []
    qft_rows = []
    for alpha, beta in bipartitions(m):
        irreps = [_wreath_matrix(alpha, beta, k) for k in subgroup]
        d = irreps[0].shape[0]
        qft = math.sqrt(d / len(subgroup)) * np.stack([rho.reshape(-1) for rho in irreps], axis=1)
        qft_rows.append(qft)
        block = (qft @ factored.reshape(len(subgroup), -1)).reshape(d, d * len(matchings), dimension)
        expected_copies = hyperoctahedral_branching_coefficient(partition, alpha, beta)
        isotypic = block.reshape(-1, dimension)
        intertwining = 0.0
        for k in _K_generators(m):
            transformed = np.einsum("ab,bci->aci", _wreath_matrix(alpha, beta, k), block)
            intertwining = max(intertwining, float(np.linalg.norm(transformed - block @ _symmetric_matrix(partition, k))))
        # Compress only the finite verification, without assuming the predicted
        # copy rank. This avoids a factorial-sized dense image projector.
        candidates = block.transpose(1, 0, 2).reshape(d * len(matchings), d * dimension)
        vectors, values, _ = np.linalg.svd(candidates, full_matrices=False)
        copy_rank = int(np.count_nonzero(values > 1e-9))
        basis = vectors[:, :copy_rank]
        compact = np.einsum("qa,cqi->cai", basis.conj(), block)
        outside = float(np.linalg.norm(block - np.einsum("qa,cai->cqi", basis, compact)))
        compact_matrix = compact.reshape(d * copy_rank, dimension)
        image = compact_matrix @ compact_matrix.conj().T
        code_projector = sum(row @ row.conj().T for row in compact) / d
        product_residual = float(np.linalg.norm(image - np.kron(np.eye(d), code_projector))) + 2 * outside
        blocks.append({
            "alpha": list(alpha), "beta": list(beta), "carrier_dimension": d,
            "expected_copy_dimension": expected_copies,
            "encoded_multiplicity_ambient_dimension": d * len(matchings),
            "isotypic_rank": int(np.linalg.matrix_rank(isotypic, tol=1e-9)),
            "code_rank": copy_rank,
            "code_projector_residual": float(np.linalg.norm(code_projector @ code_projector - code_projector)),
            "carrier_identity_tensor_code_residual": product_residual,
            "intertwining_residual": intertwining,
            "logical_action": _logical_action_controls(compact, actions),
        })
    qft = np.vstack(qft_rows)
    qft_residual = float(np.linalg.norm(qft.conj().T @ qft - np.eye(len(subgroup))))
    isometry_residual = float(np.linalg.norm(embedding.conj().T @ embedding - np.eye(dimension)))
    verified = bool(qft_residual < 1e-9 and isometry_residual < 1e-9 and all(
        row["isotypic_rank"] == row["carrier_dimension"] * row["expected_copy_dimension"]
        and row["code_rank"] == row["expected_copy_dimension"]
        and max(row["code_projector_residual"], row["carrier_identity_tensor_code_residual"], row["intertwining_residual"]) < 1e-9
        and row["logical_action"]["carrier_identity_tensor_logical_action_residual"] < 1e-9
        and row["logical_action"]["maximum_logical_operator_norm"] <= 1 + 1e-9
        for row in blocks))
    return {"partition": list(partition), "fixed_column": fixed_column,
            "input_dimension": dimension, "group_order": len(group), "subgroup_order": len(subgroup),
            "matching_count": len(matchings), "embedding_isometry_residual": isometry_residual,
            "subgroup_qft_unitarity_residual": qft_residual, "blocks": blocks,
            "finite_normalization_and_covariance_verified": verified}


def matching_orbit_type(matching: Matching) -> Partition:
    """Half-component sizes in the union with the standard reference matching."""
    n = 2 * len(matching)
    if n == 0 or sorted(point for pair in matching for point in pair) != list(range(n)) or any(len(pair) != 2 for pair in matching):
        raise ValueError("expected a perfect matching on range(2*m)")
    partner = {}
    for a, b in matching:
        partner[a], partner[b] = b, a
    unseen, sizes = set(range(n)), []
    while unseen:
        queue, component = [min(unseen)], set()
        while queue:
            vertex = queue.pop()
            if vertex in component:
                continue
            component.add(vertex)
            queue.extend((vertex ^ 1, partner[vertex]))
        unseen.difference_update(component)
        sizes.append(len(component) // 2)
    return tuple(sorted(sizes, reverse=True))


def reference_invariant_identification_bound(half_degree: int, reference_rounds: int = 1) -> Fraction:
    """Orbit-label decision-tree bound, not a general measurement/query bound.

    One round allows any number of copies in a single globally K-invariant
    measurement. More rounds mean a CLASSICAL adaptive oracle revealing at
    most one partition-valued orbit label per query, with no retained quantum
    side information. This is not a bound on general multi-reference circuits.
    """
    if not isinstance(half_degree, int) or half_degree < 1 or not isinstance(reference_rounds, int) or reference_rounds < 0:
        raise ValueError("positive integer half degree and nonnegative integer rounds required")
    from coset_hidden_involution_paired_tower_missing_label_boundary import partition_number
    hypotheses = math.factorial(2 * half_degree) // (2**half_degree * math.factorial(half_degree))
    return min(Fraction(1), Fraction(partition_number(half_degree)**reference_rounds, hypotheses))


def finite_reference_orbit_control(half_degree: int) -> dict[str, Any]:
    if half_degree not in (2, 3, 4):
        raise ValueError("exhaustive reference-orbit controls are restricted to ranks 2, 3, 4")
    subgroup = hyperoctahedral_group(half_degree)
    matchings = {factor_left_hyperoctahedral_coset(g)[1] for g in permutations(range(2 * half_degree))}
    classes = {}
    for matching in matchings:
        classes.setdefault(matching_orbit_type(matching), set()).add(matching)
    verified = True
    rows = []
    for partition, members in sorted(classes.items()):
        representative = min(members)
        orbit = {tuple(sorted(tuple(sorted((k[a], k[b]))) for a, b in representative)) for k in subgroup}
        centralizer = math.prod(part**count * math.factorial(count) for part, count in Counter(partition).items())
        predicted = 2**(half_degree - len(partition)) * math.factorial(half_degree) // centralizer
        verified &= orbit == members and len(members) == predicted
        rows.append({"orbit_type": list(partition), "size": len(members), "formula_size": predicted})
    return {"half_degree": half_degree, "hypotheses": len(matchings), "orbit_count": len(classes),
            "orbits": rows, "partition_classification_verified": bool(verified),
            "identification_upper_bound": str(reference_invariant_identification_bound(half_degree)),
            "binary_decision_ruled_out": False}


def finite_physical_fourier_control() -> dict[str, Any]:
    """Independent full S4 QFT check of the physical coset column convention."""
    group = tuple(permutations(range(4)))
    positions = {g: i for i, g in enumerate(group)}
    partitions = tuple(integer_partitions(4))
    fourier = np.vstack([math.sqrt(hook_length_dimension(lam) / len(group)) *
                         np.stack([_symmetric_matrix(tuple(lam), g).reshape(-1) for g in group], axis=1)
                         for lam in partitions])
    reference = (1, 0, 3, 2)
    alternatives = (reference, (2, 3, 0, 1), (3, 2, 1, 0))
    residual, parity_masses = 0.0, []
    for hidden in alternatives:
        right = np.zeros((len(group), len(group)))
        for g, column in positions.items():
            right[positions[compose_permutations(g, hidden)], column] = 1
        transformed = fourier @ ((np.eye(len(group)) + right) / len(group)) @ fourier.conj().T
        predicted, offset, odd_mass = np.zeros_like(transformed), 0, 0.0
        for lam in partitions:
            lam = tuple(lam)
            d = hook_length_dimension(lam)
            column_density = (np.eye(d) + _symmetric_matrix(lam, hidden)) / len(group)
            predicted[offset:offset+d*d, offset:offset+d*d] = np.kron(np.eye(d), column_density)
            odd = (np.eye(d) - _symmetric_matrix(lam, reference)) / 2
            odd_mass += d * float(np.trace(odd @ column_density))
            offset += d*d
        residual = max(residual, float(np.linalg.norm(transformed - predicted)))
        parity_masses.append({"hidden_involution": list(hidden), "aligned": hidden == reference,
                              "reference_odd_mass": odd_mass,
                              "predicted_reference_odd_mass": 0.0 if hidden == reference else 0.5})
    return {"group": "S_4", "coset_column_convention_residual": residual,
            "qft_unitarity_residual": float(np.linalg.norm(fourier.conj().T @ fourier - np.eye(len(group)))),
            "reference_parity_controls": parity_masses,
            "physical_convention_and_alignment_distinction_verified": bool(residual < 1e-10 and all(
                abs(row["reference_odd_mass"] - row["predicted_reference_odd_mass"]) < 1e-10 for row in parity_masses))}


def build_encoded_restriction_report() -> dict[str, Any]:
    controls = [finite_encoded_restriction((3, 1)), finite_encoded_restriction((2, 2)),
                finite_encoded_restriction((3, 2, 1)), finite_encoded_restriction((3, 2, 1), fixed_column=5),
                finite_encoded_restriction((4, 2, 2))]
    physical = finite_physical_fourier_control()
    orbit_controls = [finite_reference_orbit_control(m) for m in (2, 3, 4)]
    generator = np.random.default_rng(20260908)
    scalable_controls = []
    for m in (4, 8, 16, 32, 64, 128):
        passed = 0
        for _ in range(16):
            g = tuple(int(x) for x in generator.permutation(2*m))
            k, matching, t = factor_left_hyperoctahedral_coset(g)
            passed += int(compose_permutations(k, t) == g and len(matching) == m
                          and all(k[2*i+1] == (k[2*i] ^ 1) for i in range(m)))
        scalable_controls.append({"half_degree": m, "passed": passed, "trials": 16})
    return {
        "created_at": utc_now(), "status": "normalized-encoded-restriction-validated-logical-decoder-open",
        "summary": "Inverse G-QFT, reversible K-coset factorization and K-QFT give a normalized carrier-extraction reduction with an implicit copy code. An explicit copy index or target measurement is not supplied.",
        "derivation_document": "research/ENCODED_RESTRICTION.md", "finite_controls": controls,
        "physical_fourier_control": physical, "reference_orbit_controls": orbit_controls,
        "reference_identification_scaling": [{"half_degree": m,
            "fixed_reference_identification_upper_bound": str(reference_invariant_identification_bound(m)),
            "log2_upper_bound": math.log2(reference_invariant_identification_bound(m).numerator) - math.log2(reference_invariant_identification_bound(m).denominator)}
            for m in (4, 8, 16, 32, 64, 128)],
        "scalable_factorization_controls": scalable_controls,
        "access_contract": {
            "input": "A V_lambda state with known K left action, standard row encoding and a computable fixed column.",
            "quantum_primitives": ["QFT over S_(2m)", "QFT over C2 wr S_m", "reversible permutation/matching arithmetic"],
            "postselection_steps": 0, "normalization_loss": 1,
            "resource_bound": "QFT_G cost + QFT_K cost + poly(m); O(m log m) register space up to primitive workspaces.",
            "dense_control_cost_is_not_quantum_cost": True,
            "output": "mu, carrier row, and an encoded multiplicity subspace inside (K-column, K-left-coset) registers.",
        },
        "headline_metrics": {"finite_isometry_controls_passed": sum(row["finite_normalization_and_covariance_verified"] for row in controls),
                             "repeated_copy_blocks_verified": sum(row["expected_copy_dimension"] > 1 for control in controls for row in control["blocks"]),
                             "noncommuting_encoded_copy_blocks": sum(row["logical_action"]["maximum_logical_commutator_norm"] > 1e-9 for control in controls for row in control["blocks"]),
                             "physical_fourier_controls_passed": int(physical["physical_convention_and_alignment_distinction_verified"]),
                             "reference_orbit_controls_passed": sum(row["partition_classification_verified"] for row in orbit_controls),
                             "scalable_factorization_trials_passed": sum(row["passed"] for row in scalable_controls),
                             "maximum_half_degree": 128, "postselection_steps": 0,
                             "explicit_copy_index_compiler_count": 0, "hidden_involution_decoder_count": 0},
        "claim_gate": {"finite_encoded_isometry_verified": all(row["finite_normalization_and_covariance_verified"] for row in controls),
                       "polynomial_reduction_given_qft_primitives_derived": True,
                       "normalized_logical_orbit_average_reduction_derived": True,
                       "physical_real_symmetric_column_convention_verified": physical["physical_convention_and_alignment_distinction_verified"],
                       "fixed_reference_invariant_identification_obstruction_derived": True,
                       "binary_decision_ruled_out_by_reference_bound": False,
                       "qft_gate_circuits_implemented_in_this_module": False,
                       "explicit_copy_basis_compiled": False, "target_pgm_effect_compiled": False,
                       "unknown_hidden_centralizer_access_granted": False, "speedup_claim_allowed": False},
        "falsifiers_triggered": ["An exponentially large implicit multiplicity code does not itself require exponentially many qubits or postselection.",
                                  "Carrier extraction is not an explicit multiplicity-index transform or a hidden-involution measurement."],
        "next_experiments": ["Derive a source-aware logical target effect from normalized orbit averages without a complete spectral label requirement.",
                             "Specify a binary decision effect or a symmetry-breaking/multiple-reference identification protocol with its full information and resource budget.",
                             "Use the physical Fourier convention without importing the aligned h-even law into an unknown reference frame."],
    }


def write_encoded_restriction_report(path: Path = REPORT_PATH, *, write_registry: bool = True,
                                    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
                                    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
                                    registry_result_id: str = "") -> dict[str, Any]:
    payload = build_encoded_restriction_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (ExperimentRecord, ExperimentResultRecord, NegativeResultRecord,
                                       upsert_experiment, upsert_experiment_result, upsert_negative_result)
        upsert_experiment(ExperimentRecord(
            id=registry_experiment_id, candidate_id=registry_candidate_id, title="Normalized encoded subgroup restriction",
            status=payload["status"], hypothesis="Subgroup carrier extraction need not solve explicit multiplicity labeling.",
            protocol="Factor G into left K cosets; verify the two-QFT embedding, block covariance and copy-code projector.",
            positive_signal="Normalized logical access to task-relevant multiplicity effects without a fine spectral separator.",
            falsifiers=["isometry or intertwining identity fails", "postselection is hidden in register conversion", "the hidden centralizer is assumed known"],
            metrics=list(payload["headline_metrics"]), dependencies=["efficient group QFT primitives", "canonical matching transversal"],
            next_actions=payload["next_experiments"],
        ))
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}", experiment_id=registry_experiment_id,
            candidate_id=registry_candidate_id, created_at=payload["created_at"], status=payload["status"],
            summary=payload["summary"], metrics=payload["headline_metrics"],
            falsifiers_triggered=payload["falsifiers_triggered"], artifacts={"encoded_restriction": str(path)},
        ))
        upsert_negative_result(NegativeResultRecord(
            id="ENCODED-CARRIER-EXTRACTION-NOT-EXPLICIT-COPY-INDEX-OR-DECODER", source=registry_experiment_id,
            claim="The normalized two-QFT restriction map supplies an explicit multiplicity index and the target hidden-involution measurement.",
            reason_invalid="It produces an implicit copy code. The logical target effect, physical access transfer and decoder remain unspecified.",
            lesson="Use encoded logical access where possible, but charge target-effect construction and unknown-centralizer dependence separately.",
            applies_to=[registry_candidate_id, "encoded subgroup restriction"], evidence={"artifact": str(path)},
        ))
        upsert_negative_result(NegativeResultRecord(
            id="FIXED-REFERENCE-INVARIANT-IDENTIFICATION-ORBIT-BOUND", source=registry_experiment_id,
            claim="Measurements invariant under one fixed reference K can identify a uniformly random fixed-point-free hidden involution with constant success.",
            reason_invalid="All likelihoods coincide within each reference-matching orbit. There are p(m) orbits among (2m-1)!! hypotheses, so success is at most p(m)/(2m-1)!! even with arbitrarily many jointly invariant copies.",
            lesson="This does not obstruct binary class detection, carrier-sensitive or other symmetry-breaking effects, or protocols with different references. Aligned h-even source mass is not a fixed-reference input law.",
            applies_to=[registry_candidate_id, "fixed-reference invariant identification"], evidence={"artifact": str(path)},
        ))
    return payload

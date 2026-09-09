"""Information lost by independent reference twirls of physical coset blocks.

These are conditional channel bounds, not a lower bound on arbitrary coherent
algorithms. The universal derivation is review-pending; dense finite controls
independently check physical normalization and distinguishability.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product
from pathlib import Path

import numpy as np

from coset_hidden_involution_binary_decision_reduction import compose_permutations
from coset_hidden_involution_encoded_restriction import _symmetric_matrix, matching_orbit_type
from coset_hidden_involution_pair_matching_charge_hierarchy import _perfect_matchings
from coset_hidden_involution_paired_tower_missing_label_boundary import partition_number
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now

REPORT_PATH = Path("research/representation/coset_hidden_involution_reference_twirl_information.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIDDEN-INVOLUTION-REFERENCE-TWIRL-INFORMATION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_ID = "INDEPENDENT-REFERENCE-CARRIER-DISCARD-ERASES-BINARY-INFORMATION"


def _positive_integer(value: int, name: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def matching_count(half_degree: int) -> int:
    _positive_integer(half_degree, "half_degree")
    return math.factorial(2 * half_degree) // (2**half_degree * math.factorial(half_degree))


def reference_orbit_size(partition: tuple[int, ...]) -> int:
    if not partition or any(type(x) is not int or x < 1 for x in partition) or tuple(sorted(partition, reverse=True)) != partition:
        raise ValueError("expected a nonempty integer partition")
    m = sum(partition)
    z = math.prod(part**count * math.factorial(count) for part, count in Counter(partition).items())
    return 2**(m - len(partition)) * math.factorial(m) // z


def orbit_block_chi_squared(orbit_size: int, block_size: int) -> Fraction:
    """D^b Tr(sigma_O,b^2)-1 = (2^b-1)/|O|, D=|G|."""
    _positive_integer(orbit_size, "orbit_size")
    _positive_integer(block_size, "block_size")
    return Fraction(2**block_size - 1, orbit_size)


def block_twirl_distance_squared_bound(half_degree: int, block_sizes: tuple[int, ...]) -> Fraction:
    """Upper bound on squared HALF trace norm, under the uniform hidden prior.

    Each disjoint block is diagonally twirled by a known conjugate of K.
    The references and block partition must be chosen independently of h and
    measurement outcomes. All outputs may subsequently be measured jointly.
    Empty blocks describe zero input copies and return zero.
    """
    count = matching_count(half_degree)
    for size in block_sizes:
        _positive_integer(size, "block_size")
    cost = sum(2**size - 1 for size in block_sizes)
    return min(Fraction(1), Fraction(partition_number(half_degree) * cost, 2 * count))


def adaptive_block_twirl_distance_squared_bound(half_degree: int, maximum_block_sizes: tuple[int, ...]) -> Fraction:
    """Null-prefix hybrid bound for CLASSICAL outcome-adaptive references.

    Fresh block j must be twirled before interacting with retained memory.
    At most len(maximum_block_sizes) rounds; round j uses at most its listed
    size. Arbitrary quantum memory and later joint processing are allowed.
    Cauchy-Schwarz gives T^2 <= t * p(m)/(2M) * sum_j(2^b_j-1).
    Quantum-coherently controlled references or twirls after memory coupling
    are not covered. No posterior-uniformity assumption is made.
    """
    return min(Fraction(1), len(maximum_block_sizes) *
               block_twirl_distance_squared_bound(half_degree, maximum_block_sizes))


def necessary_equal_block_size(half_degree: int, blocks: int, distance: Fraction = Fraction(1, 3), *, adaptive: bool = False) -> int:
    """Necessary, not sufficient, b for trace distance >= distance in t blocks."""
    _positive_integer(blocks, "blocks")
    if not isinstance(distance, Fraction) or not 0 < distance <= 1:
        raise ValueError("distance must be an exact Fraction in (0,1]")
    if type(adaptive) is not bool:
        raise ValueError("adaptive must be a boolean")
    threshold = 1 + 2 * distance**2 * matching_count(half_degree) / (blocks**(2 if adaptive else 1) * partition_number(half_degree))
    needed = (threshold.numerator + threshold.denominator - 1) // threshold.denominator
    return max(1, (needed - 1).bit_length())


def fixed_reference_mixture_chi_squared(half_degree: int, block_sizes: tuple[int, ...]) -> Fraction:
    """Exact second moment; not a trace-distance lower bound.

    Rare tiny orbits can make this enormous while trace distance stays small.
    Unlike the Pinsker bound, this formula assumes the SAME reference in all
    blocks. Computing it enumerates p(m) partitions, not a scalable decoder.
    """
    count = matching_count(half_degree)
    for size in block_sizes:
        _positive_integer(size, "block_size")
    return sum((Fraction(reference_orbit_size(nu), count)**2 *
                (math.prod(1 + orbit_block_chi_squared(reference_orbit_size(nu), b)
                           for b in block_sizes) - 1)
                for nu in integer_partitions(half_degree)), Fraction())


@lru_cache(maxsize=3)
def _matching_data(half_degree: int) -> tuple:
    if half_degree not in (1, 2, 3, 4):
        raise ValueError("enumerated matching controls are restricted to ranks 1..4")
    matchings = tuple(_perfect_matchings(tuple(range(2 * half_degree))))
    involutions, classes = [], {}
    for index, matching in enumerate(matchings):
        h = [0] * (2 * half_degree)
        for a, b in matching:
            h[a], h[b] = b, a
        involutions.append(tuple(h))
        classes.setdefault(matching_orbit_type(matching), []).append(index)
    return tuple(involutions), tuple((nu, tuple(indices)) for nu, indices in sorted(classes.items()))


def _tensor(matrices) -> np.ndarray:
    result = np.ones((1, 1))
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def _mixture_for_blocks(single: list[list[np.ndarray]], classes: tuple, block_sizes: tuple[int, ...]) -> np.ndarray:
    """Scaled block state: average h ONCE, independently conjugate each block."""
    dimension = math.prod(single[i][0].shape[0] for i in range(len(single)))
    mixture = np.zeros((dimension, dimension))
    for _, indices in classes:
        start, blocks = 0, []
        for size in block_sizes:
            block = sum(_tensor(single[i][h] for i in range(start, start + size)) for h in indices) / len(indices)
            blocks.append(block)
            start += size
        mixture += len(indices) / len(single[0]) * _tensor(blocks)
    return mixture


@lru_cache(maxsize=16)
def finite_binary_control(half_degree: int, block_sizes: tuple[int, ...]) -> dict:
    """Physical Fourier blocks, with row degeneracy and the global prior kept."""
    if half_degree not in (2, 3) or not block_sizes or any(type(b) is not int or b < 1 for b in block_sizes):
        raise ValueError("finite controls require rank 2 or 3 and positive block sizes")
    copies = sum(block_sizes)
    if copies > (4 if half_degree == 2 else 2):
        raise ValueError("dense controls capped at four S4 or two S6 copies")
    involutions, classes = _matching_data(half_degree)
    order = math.factorial(2 * half_degree)
    partitions = integer_partitions(2 * half_degree)
    matrices = {lam: [np.eye(hook_length_dimension(lam)) + _symmetric_matrix(lam, h)
                      for h in involutions] for lam in partitions}
    raw_distance, twirled_distance, chi2 = 0.0, 0.0, 0.0
    raw_trace, twirled_trace, min_eigenvalue, global_residual = 0.0, 0.0, 0.0, 0.0
    for labels in product(partitions, repeat=copies):
        single = [matrices[lam] for lam in labels]
        dimension = math.prod(hook_length_dimension(lam) for lam in labels)
        raw = sum(_tensor(single[i][h] for i in range(copies)) for h in range(len(involutions))) / len(involutions)
        twirled = _mixture_for_blocks(single, classes, block_sizes)
        raw_delta, twirled_delta = raw - np.eye(dimension), twirled - np.eye(dimension)
        # Fourier row registers are maximally mixed: each column block occurs
        # prod(d_lambda) times, not once and not with uniform partition weight.
        weight = dimension / order**copies
        raw_eigenvalues = np.linalg.eigvalsh(raw_delta)
        twirled_eigenvalues = np.linalg.eigvalsh(twirled_delta)
        raw_distance += weight * float(np.abs(raw_eigenvalues).sum()) / 2
        twirled_distance += weight * float(np.abs(twirled_eigenvalues).sum()) / 2
        chi2 += weight * float(np.square(twirled_eigenvalues).sum())
        raw_trace += weight * float(np.trace(raw))
        twirled_trace += weight * float(np.trace(twirled))
        min_eigenvalue = min(min_eigenvalue, float(twirled_eigenvalues.min()) + 1)
        if len(block_sizes) == 1:
            global_residual = max(global_residual, float(np.linalg.norm(raw - twirled)))
    exact_chi2 = fixed_reference_mixture_chi_squared(half_degree, block_sizes)
    bound = block_twirl_distance_squared_bound(half_degree, block_sizes)
    verified = (abs(raw_trace - 1) < 1e-10 and abs(twirled_trace - 1) < 1e-10
                and min_eigenvalue > -1e-9 and twirled_distance <= raw_distance + 1e-10
                and twirled_distance**2 <= float(bound) + 1e-10
                and abs(chi2 - float(exact_chi2)) < 1e-9 and global_residual < 1e-9)
    return {"half_degree": half_degree, "block_sizes": list(block_sizes), "copies": copies,
            "raw_binary_trace_distance": raw_distance, "twirled_binary_trace_distance": twirled_distance,
            "trace_distance_squared_upper_bound": str(bound), "raw_trace": raw_trace,
            "twirled_trace": twirled_trace, "scaled_minimum_eigenvalue": min_eigenvalue,
            "chi_squared": chi2, "exact_chi_squared": str(exact_chi2),
            "single_global_block_invariance_residual": global_residual if len(block_sizes) == 1 else None,
            "physical_finite_controls_verified": bool(verified)}


def finite_regular_basis_control() -> dict:
    """Independent S4 group-basis check, including a two-copy 576x576 state."""
    group = tuple(permutations(range(4)))
    positions = {g: i for i, g in enumerate(group)}
    involutions, classes = _matching_data(2)
    states = []
    for h in involutions:
        right = np.zeros((24, 24))
        for column, g in enumerate(group):
            right[positions[compose_permutations(g, h)], column] = 1
        states.append((np.eye(24) + right) / 24)
    orbit_controls = []
    for nu, indices in classes:
        for b in (1, 2):
            state = sum(_tensor([states[h]] * b) for h in indices) / len(indices)
            purity = 24**b * float(np.vdot(state, state).real) - 1
            expected = orbit_block_chi_squared(len(indices), b)
            eig = np.linalg.eigvalsh(state)
            positive = eig[eig > 1e-14]
            relative_entropy = float(np.sum(positive * np.log(24**b * positive)))
            distance = float(np.abs(eig - 24.0**(-b)).sum()) / 2
            orbit_controls.append({"orbit_type": list(nu), "orbit_size": len(indices), "block_size": b,
                "chi_squared": purity, "exact_chi_squared": str(expected),
                "relative_entropy_nats": relative_entropy, "trace_distance": distance,
                "verified": bool(abs(purity - float(expected)) < 1e-10
                    and 2 * distance**2 <= relative_entropy + 1e-10
                    and relative_entropy <= math.log1p(float(expected)) + 1e-10)})
    regular = _mixture_for_blocks([states, states], classes, (1, 1))
    distance = float(np.abs(np.linalg.eigvalsh(regular) - 1 / 24**2).sum()) / 2
    fourier = finite_binary_control(2, (1, 1))["twirled_binary_trace_distance"]
    return {"orbit_controls": orbit_controls, "regular_binary_trace_distance": distance,
            "fourier_binary_trace_distance": fourier,
            "independent_regular_controls_verified": bool(all(row["verified"] for row in orbit_controls)
                                                          and abs(distance - fourier) < 1e-10)}


def finite_adaptive_reference_control(half_degree: int) -> dict:
    """Exact two-round physical projector probe, not a useful decoder.

    P_r=(I+R_r)/2 gives Pr(+|h)=(1+[r=h])/2, invariant under C_G(r).
    After outcome + choose r=0 again; after - choose r=1. The complete
    transcript uses the same hidden h. This tests accounting and posterior
    nonuniformity, not the general quantum-memory hybrid proof by itself.
    """
    if half_degree not in (2, 3, 4):
        raise ValueError("adaptive transcript controls restricted to ranks 2..4")
    count = matching_count(half_degree)
    paths = []
    for first, second in product((False, True), repeat=2):
        reference = 0 if first else 1
        probability = Fraction()
        for hidden in range(count):
            positive1 = Fraction(1 + (hidden == 0), 2)
            positive2 = Fraction(1 + (hidden == reference), 2)
            probability += (positive1 if first else 1 - positive1) * (positive2 if second else 1 - positive2) / count
        paths.append({"outcomes": [first, second], "second_reference_index": reference,
                      "hidden_probability": str(probability), "null_probability": "1/4"})
    distance = sum((abs(Fraction(row["hidden_probability"]) - Fraction(1, 4)) for row in paths), Fraction()) / 2
    bound = adaptive_block_twirl_distance_squared_bound(half_degree, (1, 1))
    return {"half_degree": half_degree, "paths": paths, "transcript_trace_distance": str(distance),
            "adaptive_trace_distance_squared_upper_bound": str(bound),
            "prior_reciprocal_orbit_mean": str(Fraction(partition_number(half_degree), count)),
            "posterior_reciprocal_orbit_mean_after_positive": str(Fraction(partition_number(half_degree) + 1, count + 1)),
            "exact_transcript_control_verified": bool(sum(Fraction(row["hidden_probability"]) for row in paths) == 1
                                                      and distance**2 <= bound)}


def finite_coherent_reference_erasure_control(partition: tuple[int, ...]) -> dict:
    """A constructive countercontrol OUTSIDE the preinteraction-twirl model.

    V|i> = |G|^-1/2 sum_g |g> tensor rho_lambda(g)^dagger|i>.
    QFT on the reference turns this into |lambda> |i> tensor a Bell pair.
    The input can therefore be recovered after arbitrary carrier erasure.
    This transports the original quantum problem; it does not decode h.
    """
    if partition not in integer_partitions(4):
        raise ValueError("coherent reference matrix controls restricted to S4 irreps")
    group = tuple(permutations(range(4)))
    d = hook_length_dimension(partition)
    representations = [_symmetric_matrix(partition, g) for g in group]
    encoding = np.stack([rho.conj().T for rho in representations]) / math.sqrt(len(group))
    fourier = np.vstack([math.sqrt(hook_length_dimension(lam) / len(group)) *
                         np.stack([_symmetric_matrix(lam, g).reshape(-1) for g in group], axis=1)
                         for lam in integer_partitions(4)])
    transformed = (fourier @ encoding.reshape(len(group), d * d)).reshape(len(group), d, d)
    offset = sum(hook_length_dimension(lam)**2 for lam in integer_partitions(4)[:integer_partitions(4).index(partition)])
    expected = np.zeros_like(transformed)
    for i in range(d):
        for j in range(d):
            expected[offset + i * d + j, j, i] = 1 / math.sqrt(d)
    isometry = encoding.reshape(len(group) * d, d)
    isometry_residual = float(np.linalg.norm(isometry.conj().T @ isometry - np.eye(d)))
    bell_residual = float(np.linalg.norm(transformed - expected))
    recovery_residual, erasure_residual = 0.0, 0.0
    for i, j in product(range(d), repeat=2):
        # Matrix units check channel identity, including coherences, rather
        # than checking only basis-state recovery probabilities.
        reference = encoding[:, :, i] @ encoding[:, :, j].conj().T
        decoded = fourier @ reference @ fourier.conj().T
        block = decoded[offset:offset + d*d, offset:offset + d*d].reshape(d, d, d, d)
        recovered = np.trace(block, axis1=1, axis2=3)
        unit = np.zeros((d, d))
        unit[i, j] = 1
        recovery_residual = max(recovery_residual, float(np.linalg.norm(recovered - unit)))
        lost = sum(np.outer(encoding[g, :, i], encoding[g, :, j].conj()) for g in range(len(group)))
        erasure_residual = max(erasure_residual, float(np.linalg.norm(lost - (i == j) * np.eye(d) / d)))
    verified = bool(max(isometry_residual, bell_residual, recovery_residual, erasure_residual) < 1e-10)
    return {"partition": list(partition), "input_dimension": d, "reference_dimension": len(group),
            "isometry_residual": isometry_residual, "fourier_bell_factorization_residual": bell_residual,
            "all_matrix_unit_recovery_residual": recovery_residual,
            "erased_carrier_input_independence_residual": erasure_residual,
            "matrix_units_checked": d*d, "finite_identity_channel_recovery_verified": verified,
            "preinteraction_twirl_assumption_satisfied": False,
            "input_hidden_information_already_transferred_to_reference": True,
            "hidden_involution_decoder_supplied": False}


def build_reference_twirl_information_report() -> dict:
    controls = [finite_binary_control(2, blocks) for blocks in ((1,), (1, 1), (2,), (1, 1, 1), (2, 1), (3,), (2, 2))]
    controls += [finite_binary_control(3, blocks) for blocks in ((1,), (1, 1), (2,))]
    regular = finite_regular_basis_control()
    adaptive_controls = [finite_adaptive_reference_control(m) for m in (2, 3, 4)]
    coherent_controls = [finite_coherent_reference_erasure_control(lam) for lam in integer_partitions(4)]
    scaling = []
    for m in (4, 8, 16, 32, 64, 128, 256):
        blocks = m**2
        bound = block_twirl_distance_squared_bound(m, (1,) * blocks)
        adaptive_bound = adaptive_block_twirl_distance_squared_bound(m, (1,) * blocks)
        scaling.append({"half_degree": m, "independent_single_copy_blocks": blocks,
                        "trace_distance_squared_upper_bound": str(bound),
                        "log2_trace_distance_upper_bound": (math.log2(bound.numerator) - math.log2(bound.denominator)) / 2,
                        "necessary_equal_block_size_for_distance_one_third": necessary_equal_block_size(m, blocks),
                        "adaptive_trace_distance_squared_upper_bound": str(adaptive_bound),
                        "log2_adaptive_trace_distance_upper_bound": (math.log2(adaptive_bound.numerator) - math.log2(adaptive_bound.denominator)) / 2,
                        "adaptive_necessary_equal_block_size_for_distance_one_third": necessary_equal_block_size(m, blocks, adaptive=True)})
    orbit_checks = [{"half_degree": m, "enumerated_orbits": len(_matching_data(m)[1]),
                    "orbit_formula_verified": all(len(indices) == reference_orbit_size(nu) for nu, indices in _matching_data(m)[1])}
                   for m in (1, 2, 3, 4)]
    # A rare aligned orbit makes the second moment large. It does not imply
    # appreciable total variation; report this as a misuse countercontrol.
    rare_m, rare_blocks = 8, (1,) * 64
    rare = {"half_degree": rare_m, "single_copy_blocks": len(rare_blocks),
            "exact_mixture_chi_squared": str(fixed_reference_mixture_chi_squared(rare_m, rare_blocks)),
            "trace_distance_squared_upper_bound": str(block_twirl_distance_squared_bound(rare_m, rare_blocks)),
            "large_chi_squared_is_not_a_detection_lower_bound": True}
    finite = bool(all(row["physical_finite_controls_verified"] for row in controls)
                  and regular["independent_regular_controls_verified"] and all(row["orbit_formula_verified"] for row in orbit_checks)
                  and all(row["exact_transcript_control_verified"] for row in adaptive_controls)
                  and all(row["finite_identity_channel_recovery_verified"] for row in coherent_controls))
    return {"created_at": utc_now(), "status": "derived-blockwise-reference-information-loss-review-pending",
        "summary": "Independent reference-carrier discard suppresses binary detection: T^2 <= p(m)/(2(2m-1)!!) sum_j(2^b_j-1) for predetermined references. Classical adaptation with quantum memory obeys a weaker bound multiplied by the round count, provided fresh blocks are twirled before memory interaction. A single global twirl and coherent carrier retention remain open.",
        "derivation_document": "research/REFERENCE_TWIRL_INFORMATION.md",
        "literature": ["https://cs.uwaterloo.ca/~watrous/TQI/TQI.5.pdf", "https://arxiv.org/abs/2102.04576",
                       "https://arxiv.org/abs/quant-ph/0511148", "https://arxiv.org/abs/quant-ph/0511149"],
        "scope": {"prior": "uniform fixed-point-free involution; the same h in every sample",
            "null": "trivial-subgroup state I/|S_(2m)| in each input",
            "channel": "independent diagonal K_j twirl per disjoint block; K_j known conjugates of C2 wr S_m",
            "reference_schedule": "fixed in advance or randomized independently of input and outcomes",
            "adaptive_extension": "classical outcome-adaptive references, bounded rounds/block sizes, arbitrary quantum memory; fresh blocks twirled BEFORE memory interaction",
            "postprocessing": "arbitrary joint quantum channel/POVM after the twirls",
            "equivalent_single_copy_discard": "dephase reference irrep type AND discard its carrier, retaining multiplicity state",
            "not_equivalent": "carrier tracing alone with padded registers and retained intertype coherence",
            "trace_distance_convention": "half trace norm; equal-prior success = 1/2 + T/2"},
        "finite_controls": controls, "regular_basis_control": regular, "orbit_controls": orbit_checks,
        "adaptive_reference_controls": adaptive_controls,
        "coherent_reference_erasure_countercontrols": coherent_controls,
        "scaling": scaling, "rare_orbit_countercontrol": rare,
        "headline_metrics": {"finite_binary_controls_passed": sum(row["physical_finite_controls_verified"] for row in controls),
            "regular_basis_controls_passed": int(regular["independent_regular_controls_verified"]),
            "scaling_records": len(scaling), "maximum_half_degree": 256,
            "m128_log2_single_copy_distance_upper_bound": scaling[-2]["log2_trace_distance_upper_bound"],
            "m128_necessary_block_size": scaling[-2]["necessary_equal_block_size_for_distance_one_third"],
            "m128_adaptive_log2_distance_upper_bound": scaling[-2]["log2_adaptive_trace_distance_upper_bound"],
            "m128_adaptive_necessary_block_size": scaling[-2]["adaptive_necessary_equal_block_size_for_distance_one_third"],
            "coherent_reference_identity_channels_verified": sum(row["finite_identity_channel_recovery_verified"] for row in coherent_controls),
            "strict_finite_information_loss_controls": sum(row["twirled_binary_trace_distance"] < row["raw_binary_trace_distance"] - 1e-9 for row in controls)},
        "claim_gate": {"finite_controls_verified": finite, "scoped_blockwise_information_bound_derived": finite,
            "independent_single_copy_discard_obstructed": finite, "general_binary_detection_ruled_out": False,
            "single_global_twirl_ruled_out": False, "coherent_encoded_access_ruled_out": False,
            "classically_adaptive_preinteraction_twirl_bound_derived": finite,
            "coherent_preinteraction_encoding_escape_finite_verified": all(row["finite_identity_channel_recovery_verified"] for row in coherent_controls),
            "coherent_transport_supplies_detector": False,
            "quantum_controlled_reference_bound_derived": False, "new_general_entanglement_lower_bound_claimed": False,
            "machine_checked_proof": False, "speedup_claim_allowed": False},
        "falsifiers_triggered": ["Noncommuting multiplicity operators do not restore carrier correlations erased independently per input.",
                                 "A large chi-squared moment from rare reference-aligned orbits is not a detection lower bound."],
        "next_experiments": ["Compile a source-weighted collective effect retaining correlations across at least the necessary block scale.",
            "Analyze quantum-controlled references or memory coupling before the destructive twirl; ordinary classical adaptation alone does not escape.",
            "Audit data processing whenever a candidate drops carriers, intertype coherence, or a block environment."],
    }


def write_reference_twirl_information_report(path: Path = REPORT_PATH, *, write_registry: bool = True,
        registry_experiment_id: str = DEFAULT_EXPERIMENT_ID, registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
        registry_result_id: str = "") -> dict:
    from research_registry import (ExperimentRecord, ExperimentResultRecord, NegativeResultRecord,
                                   upsert_experiment, upsert_experiment_result, upsert_negative_result)
    payload = build_reference_twirl_information_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if write_registry:
        upsert_experiment(ExperimentRecord(id=registry_experiment_id, candidate_id=registry_candidate_id,
            title="Reference-carrier discard and binary information", status=payload["status"],
            hypothesis="Independent multiplicity-only registers retain enough information for polynomial-copy binary detection.",
            protocol="Derive exact orbit purity and entropy bounds; independently verify Fourier and regular-basis states.",
            positive_signal="A precisely specified carrier-retaining or sufficiently collective effect escapes the scoped channel bound.",
            falsifiers=["natural-prior distance vanishes", "type dephasing and carrier discard were treated as coherent access", "rare-orbit moments were promoted to success"],
            metrics=list(payload["headline_metrics"]), dependencies=payload["literature"], next_actions=payload["next_experiments"]))
        upsert_experiment_result(ExperimentResultRecord(id=registry_result_id or f"RESULT-{registry_experiment_id}",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id, created_at=payload["created_at"],
            status=payload["status"], summary=payload["summary"], metrics=payload["headline_metrics"],
            falsifiers_triggered=payload["falsifiers_triggered"], artifacts={"reference_twirl_information": str(path)}))
        if payload["claim_gate"]["scoped_blockwise_information_bound_derived"]:
            upsert_negative_result(NegativeResultRecord(id=NEGATIVE_ID, source=registry_experiment_id,
                claim="After independent reference-type dephasing and carrier discard, polynomially many single-copy multiplicity registers permit constant-advantage binary detection.",
                reason_invalid=payload["summary"],
                lesson="Retain charged cross-input carrier correlations. Predetermined references and classical adaptation with fresh-block twirling before memory coupling obey separate bounds. Quantum-controlled references and pre-twirl memory interaction remain outside scope. This is not a general HSP lower bound or classical dequantization.",
                applies_to=[registry_candidate_id, "independent reference-carrier discard"], evidence={"artifact": str(path), "scope": payload["scope"]}))
    return payload

"""Source-weighted binary evaluation of existing collective carrier instruments.

This evaluates physical outcome laws, not commutator size. It deliberately
does not search tiny circuits or promote a fixed-copy detection algorithm.
The finite schedules calibrate the evaluator; all fixed-copy candidates must
still pass the asymptotic copy budget, classifier, and classical baseline gates.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

from isotypic_instruments import finite_isotypic_instrument, isotypic_label_resource_contract
from involution_character_arithmetic import label_arithmetic_scaling_controls

from coset_three_copy_recoupling_obstruction import involutions
from coset_hidden_involution_reference_twirl_information import matching_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_carrier_noncentral_readout_boundary import _natural_informative_block
from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
from self_dual_wreath_plancherel_carrier_contextuality import _triple_isotypic_projectors
from weak_fourier_signal import character_on_involution

REPORT_PATH = Path("research/representation/coset_binary_carrier_instruments.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-BINARY-CARRIER-INSTRUMENTS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SCHEDULES = ("", "L", "R", "LL", "LR", "RL", "LRL", "RLR", "T", "LT", "RT", "TL")


def binary_outcome_statistics(null: np.ndarray, alternative: np.ndarray) -> dict:
    """No silent clipping, normalization, postselection or omitted outcomes."""
    if any(np.iscomplexobj(values) and np.any(np.abs(np.asarray(values).imag) > 1e-12) for values in (null, alternative)):
        raise ValueError("probabilities must be real")
    null, alternative = np.asarray(null, dtype=float), np.asarray(alternative, dtype=float)
    if null.ndim != 1 or null.shape != alternative.shape or not null.size:
        raise ValueError("binary laws must be equal-length nonempty vectors")
    if not np.isfinite(null).all() or not np.isfinite(alternative).all():
        raise ValueError("binary laws contain nonfinite probabilities")
    if min(float(null.min()), float(alternative.min())) < -1e-10:
        raise ValueError("binary laws contain negative probabilities")
    residual = max(abs(float(null.sum()) - 1), abs(float(alternative.sum()) - 1))
    if residual > 1e-8:
        raise ValueError(f"binary law mass lost or renormalized before evaluation: residual={residual}")
    distance = float(np.abs(alternative - null).sum()) / 2
    return {"total_variation": distance, "equal_prior_bayes_success": (1 + distance) / 2,
            "normalization_residual": residual, "output_count": len(null),
            "optimal_likelihood_table_is_a_compiled_classifier": False}


def one_pair_likelihood_ratio(sources: tuple, target: tuple[int, ...], transposition_count: int, side: str) -> Fraction:
    """Exact ratio for source labels plus ONE pair label, on positive null mass.

    Pair-label quantum access and character evaluation are separate resource
    contracts. Repeated overlapping measurements do not inherit this formula.
    """
    if len(sources) != 3 or side not in ("L", "R"):
        raise ValueError("one left/right pair on three sources required")
    degree = sum(sources[0])
    if (any(source not in integer_partitions(degree) for source in sources)
            or target not in integer_partitions(degree) or type(transposition_count) is not int
            or not 1 <= transposition_count <= degree // 2):
        raise ValueError("incompatible source, target or involution class")
    ratios = [Fraction(character_on_involution(source, transposition_count), hook_length_dimension(source)) for source in sources]
    target_ratio = Fraction(character_on_involution(target, transposition_count), hook_length_dimension(target))
    left, right, unused = (0, 1, 2) if side == "L" else (1, 2, 0)
    return (1 + ratios[unused]) * (1 + ratios[left] + ratios[right] + target_ratio)


def invariant_block_transcript_distance_squared_bound(half_degree: int, block_size: int, blocks: int) -> Fraction:
    """Only fresh-block invariant measurements with CLASSICAL retained history.

    Each complete block POVM commutes with diagonal G. No quantum state is
    retained between blocks. Outcome-adaptive instrument choices are allowed.
    Since every transcript is independent of which h in the class was chosen,
    the conditional hidden prior remains uniform. Relative-entropy chain rule
    and Pinsker yield T^2 <= t(2^b-1)/(2M).
    """
    if type(block_size) is not int or block_size < 1 or type(blocks) is not int or blocks < 0:
        raise ValueError("positive block size and nonnegative block count required")
    return min(Fraction(1), Fraction(blocks * (2**block_size - 1), 2 * matching_count(half_degree)))


def _half_trace_norm(matrix: np.ndarray) -> float:
    return float(np.abs(np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)).sum()) / 2


def _total_projectors(sources: tuple, representations: dict) -> tuple[np.ndarray, ...]:
    n = sum(sources[0])
    dimension = math.prod(hook_length_dimension(lam) for lam in sources)
    result = []
    for target in integer_partitions(n):
        projector = np.zeros((dimension, dimension), dtype=complex)
        for g, rho in representations[target].items():
            projector += np.trace(rho).conjugate() * np.kron(np.kron(
                representations[sources[0]][g], representations[sources[1]][g]), representations[sources[2]][g])
        projector *= hook_length_dimension(target) / math.factorial(n)
        result.append((projector + projector.conj().T) / 2)
    return tuple(result)


@lru_cache(maxsize=34)
def _pair_gpe_instrument(left: tuple[int, ...], right: tuple[int, ...]):
    n = sum(left)
    if n not in (3, 4) or sum(right) != n:
        raise ValueError("dense GPE controls are restricted to compatible S3/S4 pairs")
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in integer_partitions(n)}
    group = tuple(representations[left])
    return finite_isotypic_instrument(
        [np.kron(representations[left][g], representations[right][g]) for g in group],
        {lam: [table[g] for g in group] for lam, table in representations.items()},
    )


@lru_cache(maxsize=2)
def evaluate_pair_gpe_cleanup(n: int, transposition_count: int) -> dict:
    """All physical source triples, comparing clean labels to discarded GPE rows.

    Pair-local group twirling destroys the shared-h correlation across that
    partition. This is not the global diagonal twirl, which preserves the
    binary class mixture. No favorable source block is postselected.
    """
    if (n, transposition_count) not in ((3, 1), (4, 2)):
        raise ValueError("cleanup controls use the physical S3/S4 classes")
    partitions, hidden = integer_partitions(n), involutions(n, transposition_count)
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    p0, p1, follow0, follow1 = [], [], [], []
    clean_distance = discarded_distance = 0.0
    residuals = dict.fromkeys(("clean_workspace", "legacy_projector", "first_label_probability",
                              "conditional_binary_proportionality", "discard_equals_pair_twirl",
                              "global_conjugation_preserves_binary_state"), 0.0)
    for sources in itertools.product(partitions, repeat=3):
        dimensions = [hook_length_dimension(lam) for lam in sources]
        dimension = math.prod(dimensions)
        null = dimension / math.factorial(n)**3 * np.eye(dimension)
        alternative = sum(_natural_informative_block(sources, h, representations) for h in hidden) / len(hidden)
        instrument = _pair_gpe_instrument(*sources[:2])
        residuals["clean_workspace"] = max(residuals["clean_workspace"], max(instrument.residuals.values()))
        left = _triple_isotypic_projectors(sources, "left")
        right = _triple_isotypic_projectors(sources, "right")
        spectator = np.eye(dimensions[2])
        discarded_alternative = np.zeros_like(alternative, dtype=complex)
        for index, label in enumerate(instrument.labels):
            projector = np.kron(instrument.projectors[label], spectator)
            residuals["legacy_projector"] = max(residuals["legacy_projector"], float(np.linalg.norm(projector - left[index])))
            clean0, clean1 = projector @ null @ projector, projector @ alternative @ projector
            zero, one = np.zeros_like(null, dtype=complex), np.zeros_like(alternative, dtype=complex)
            for kraus in instrument.fourier_kraus[label]:
                lifted = np.kron(kraus, spectator)
                zero += lifted @ null @ lifted.conj().T
                one += lifted @ alternative @ lifted.conj().T
            discarded_alternative += one
            clean_distance += _half_trace_norm(clean1 - clean0)
            discarded_distance += _half_trace_norm(one - zero)
            p0.append(float(np.trace(zero).real))
            p1.append(float(np.trace(one).real))
            residuals["first_label_probability"] = max(residuals["first_label_probability"],
                abs(p0[-1] - float(np.trace(clean0).real)), abs(p1[-1] - float(np.trace(clean1).real)))
            ratio = float(one_pair_likelihood_ratio(sources, label, transposition_count, "L"))
            residuals["conditional_binary_proportionality"] = max(residuals["conditional_binary_proportionality"],
                float(np.linalg.norm(one - ratio * zero)))
            for following in right:
                follow0.append(float(np.trace(following @ zero).real))
                follow1.append(float(np.trace(following @ one).real))
        twirled = np.zeros_like(alternative, dtype=complex)
        for g in representations[sources[0]]:
            pair = np.kron(representations[sources[0]][g], representations[sources[1]][g])
            local = np.kron(pair, spectator)
            twirled += local @ alternative @ local.conj().T / math.factorial(n)
            global_action = np.kron(pair, representations[sources[2]][g])
            residuals["global_conjugation_preserves_binary_state"] = max(
                residuals["global_conjugation_preserves_binary_state"],
                float(np.linalg.norm(global_action @ alternative @ global_action.conj().T - alternative)))
        residuals["discard_equals_pair_twirl"] = max(residuals["discard_equals_pair_twirl"],
            float(np.linalg.norm(discarded_alternative - twirled)))
    first, follow = binary_outcome_statistics(p0, p1), binary_outcome_statistics(follow0, follow1)
    verified = (max(residuals.values()) < 1e-8
                and abs(discarded_distance - first["total_variation"]) < 1e-8
                and abs(follow["total_variation"] - first["total_variation"]) < 1e-8
                and discarded_distance <= clean_distance + 1e-8)
    return {"n": n, "source_blocks_evaluated": len(partitions)**3, "residuals": residuals,
            "clean_first_pair_retained_trace_distance": clean_distance,
            "discarded_reference_retained_trace_distance": discarded_distance,
            "extra_loss_from_discarded_reference": clean_distance - discarded_distance,
            "first_pair_transcript": first, "discard_then_clean_right_transcript": follow,
            "finite_complete_source_cleanup_verified": bool(verified),
            "hypothesis_independent_state_after_first_label": residuals["conditional_binary_proportionality"] < 1e-8,
            "global_twirl_is_the_same_channel_as_pair_twirl": False}


def _rank_one_carrier_hmm(sources: tuple, projectors: dict, null: np.ndarray,
                          alternative: np.ndarray, schedules: tuple) -> dict:
    """Exact latent-total-irrep model, ONLY when both pair couplings have rank one.

    Joint projectors have physical rank d_nu, not rank one. 'Rank one' means
    rank in the multiplicity space. No general efficient Racah evaluator is
    assumed by this dense finite classical replay.
    """
    targets = integer_partitions(sum(sources[0]))
    dimensions = np.array([hook_length_dimension(nu) for nu in targets])
    joint = {side: [[total @ p for p in projectors[side]] for total in projectors["T"]] for side in "LR"}
    ranks = [float(np.trace(j).real) / dimensions[t] for side in "LR"
             for t, row in enumerate(joint[side]) for j in row]
    rank_residual = max(abs(value - round(value)) for value in ranks)
    maximum = max(round(value) for value in ranks)
    if rank_residual > 1e-8 or maximum > 1 or min(ranks) < -1e-8:
        return {"applicable": False, "maximum_multiplicity": maximum, "channels": {}}
    transitions = {}
    for previous, current in itertools.product("LR", repeat=2):
        transitions[previous + current] = np.array([
            [[float(np.trace(new @ old).real) / dimensions[t] for new in joint[current][t]]
             for old in joint[previous][t]] for t in range(len(targets))])
    channels = {}
    for schedule in schedules:
        if not schedule or any(side not in "LR" for side in schedule):
            continue
        side = schedule[0]
        branches = [(a, np.array([float(np.trace(joint[side][t][a] @ null).real) for t in range(len(targets))]),
                     np.array([float(np.trace(joint[side][t][a] @ alternative).real) for t in range(len(targets))]))
                    for a in range(len(targets))]
        for previous, current in zip(schedule, schedule[1:]):
            branches = [(b, p0 * transitions[previous + current][:, a, b], p1 * transitions[previous + current][:, a, b])
                        for a, p0, p1 in branches for b in range(len(targets))]
        output = {key: [] for key in ("null_transcript", "alt_transcript", "null_row", "alt_row")}
        for a, p0, p1 in branches:
            output["null_transcript"].append(float(p0.sum()))
            output["alt_transcript"].append(float(p1.sum()))
            emissions = np.stack([np.diag(joint[schedule[-1]][t][a]).real / dimensions[t] for t in range(len(targets))])
            output["null_row"].extend((p0 @ emissions).tolist())
            output["alt_row"].extend((p1 @ emissions).tolist())
        channels[schedule] = output
    return {"applicable": True, "maximum_multiplicity": maximum, "channels": channels}


@lru_cache(maxsize=4)
def evaluate_binary_carrier_instruments(n: int = 4, transposition_count: int = 2,
                                        schedules: tuple[str, ...] = SCHEDULES) -> dict:
    if n not in (3, 4) or type(transposition_count) is not int or not 1 <= transposition_count <= n // 2:
        raise ValueError("finite instruments restricted to nontrivial S3/S4 involution classes")
    if (not schedules or len(set(schedules)) != len(schedules)
            or any(type(s) is not str or len(s) > 3 or any(c not in "LRT" for c in s) for s in schedules)):
        raise ValueError("distinct L/R/T schedules of depth at most three required")
    partitions = integer_partitions(n)
    hidden = involutions(n, transposition_count)
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    accumulators = {s: {key: [] for key in ("null_transcript", "alt_transcript", "null_row", "alt_row", "null_dephased", "alt_dephased")}
                    for s in schedules}
    retained = dict.fromkeys(schedules, 0.0)
    rule_distance, rule_residual = dict.fromkeys(schedules, 0.0), dict.fromkeys(schedules, 0.0)
    hmm_residual, hmm_blocks, maximum_joint_multiplicity = 0.0, 0, 0
    raw_distance, source_blocks, maximum_projector_residual = 0.0, 0, 0.0
    for sources in itertools.product(partitions, repeat=3):
        dimensions = [hook_length_dimension(lam) for lam in sources]
        dimension = math.prod(dimensions)
        null = dimension / math.factorial(n)**3 * np.eye(dimension)
        alternative = sum(_natural_informative_block(sources, h, representations) for h in hidden) / len(hidden)
        raw_distance += _half_trace_norm(alternative - null)
        source_blocks += 1
        projectors = {side: _triple_isotypic_projectors(sources, "left" if side == "L" else "right") for side in "LR"}
        projectors["T"] = _total_projectors(sources, representations)
        hmm = _rank_one_carrier_hmm(sources, projectors, null, alternative, schedules)
        hmm_blocks += int(hmm["applicable"])
        maximum_joint_multiplicity = max(maximum_joint_multiplicity, hmm["maximum_multiplicity"])
        for side in "LRT":
            maximum_projector_residual = max(maximum_projector_residual,
                float(np.linalg.norm(sum(projectors[side]) - np.eye(dimension))),
                max(float(np.linalg.norm(p @ p - p)) for p in projectors[side]))
        branches = {"": [((), null, alternative, np.diag(null).real, np.diag(alternative).real)]}
        prefixes = sorted({s[:length] for s in schedules for length in range(1, len(s) + 1)}, key=lambda s: (len(s), s))
        for prefix in prefixes:
            branches[prefix] = []
            for labels, zero, one, classical_zero, classical_one in branches[prefix[:-1]]:
                for label, projector in enumerate(projectors[prefix[-1]]):
                    # Keep zero-probability outcomes. Their labels matter for
                    # comparing complete channels, and no branch is normalized.
                    transition = np.abs(projector)**2
                    branches[prefix].append((labels + (label,), projector @ zero @ projector,
                        projector @ one @ projector, transition @ classical_zero, transition @ classical_one))
        for schedule in schedules:
            output = accumulators[schedule]
            start = {key: len(output[key]) for key in ("null_transcript", "alt_transcript", "null_row", "alt_row")}
            for labels, zero, one, classical_zero, classical_one in branches[schedule]:
                p0, p1 = float(np.trace(zero).real), float(np.trace(one).real)
                output["null_transcript"].append(p0)
                output["alt_transcript"].append(p1)
                output["null_row"].extend(np.diag(zero).real.tolist())
                output["alt_row"].extend(np.diag(one).real.tolist())
                output["null_dephased"].extend(classical_zero.tolist())
                output["alt_dephased"].extend(classical_one.tolist())
                retained[schedule] += _half_trace_norm(one - zero)
                if schedule in ("L", "R"):
                    ratio = one_pair_likelihood_ratio(sources, partitions[labels[0]], transposition_count, schedule)
                    rule_residual[schedule] = max(rule_residual[schedule], abs(p1 - float(ratio) * p0))
                    if ratio > 1:
                        rule_distance[schedule] += p1 - p0
            if schedule in hmm["channels"]:
                for key, values in hmm["channels"][schedule].items():
                    hmm_residual = max(hmm_residual, float(np.max(np.abs(np.asarray(output[key][start[key]:]) - values))))
    rows = []
    for schedule in schedules:
        output = accumulators[schedule]
        transcript = binary_outcome_statistics(output["null_transcript"], output["alt_transcript"])
        row = binary_outcome_statistics(output["null_row"], output["alt_row"])
        classical = binary_outcome_statistics(output["null_dephased"], output["alt_dephased"])
        rows.append({"schedule": schedule or "NONE", "measurement_depth": len(schedule),
            "transcript": transcript, "young_row_readout": row,
            "product_dephased_markov_ablation": classical,
            "retained_quantum_trace_distance": retained[schedule],
            "irrecoverable_trace_distance_loss": max(0.0, raw_distance - retained[schedule]),
            "uncompiled_residual_measurement_gap": max(0.0, retained[schedule] - row["total_variation"]),
            "one_pair_character_classifier_distance": rule_distance[schedule] if schedule in ("L", "R") else None,
            "one_pair_character_likelihood_residual": rule_residual[schedule] if schedule in ("L", "R") else None,
            "latent_total_irrep_hmm_replay_verified": bool(schedule and all(side in "LR" for side in schedule)
                                                          and hmm_blocks == source_blocks and hmm_residual < 1e-8),
            "retained_helstrom_distance_is_implemented_readout": False,
            "dephased_ablation_is_a_general_classical_lower_bound": False})
    verified = bool(maximum_projector_residual < 1e-8 and hmm_residual < 1e-8 and all(
        item["transcript"]["total_variation"] <= item["young_row_readout"]["total_variation"] + 1e-8
        and item["young_row_readout"]["total_variation"] <= item["retained_quantum_trace_distance"] + 1e-8
        and item["retained_quantum_trace_distance"] <= raw_distance + 1e-8
        and item["product_dephased_markov_ablation"]["total_variation"] <= raw_distance + 1e-8
        and (item["one_pair_character_likelihood_residual"] is None
             or (item["one_pair_character_likelihood_residual"] < 1e-8 and abs(
                 item["one_pair_character_classifier_distance"] - item["transcript"]["total_variation"]) < 1e-8))
        for item in rows))
    return {"n": n, "transposition_count": transposition_count, "copy_count": 3,
            "hidden_class_size": len(hidden), "source_blocks_evaluated": source_blocks,
            "source_blocks_expected": len(partitions)**3, "postselected_source_mass": False,
            "physical_raw_trace_distance": raw_distance, "maximum_projector_residual": maximum_projector_residual,
            "latent_total_irrep_hmm_source_blocks": hmm_blocks, "maximum_joint_multiplicity": maximum_joint_multiplicity,
            "full_outcome_law_hmm_replay_residual": hmm_residual,
            "schedules": rows, "finite_full_source_instrument_checks_verified": verified}


def build_binary_carrier_instrument_report() -> dict:
    from symmetric_character import kronecker_coefficient
    controls = [evaluate_binary_carrier_instruments(3, 1), evaluate_binary_carrier_instruments(4, 2)]
    cleanup = [evaluate_pair_gpe_cleanup(3, 1), evaluate_pair_gpe_cleanup(4, 2)]
    arithmetic = label_arithmetic_scaling_controls()
    scaling = [{"half_degree": m, "block_size": 3, "classical_history_blocks": m**2,
                "trace_distance_squared_upper_bound": str(invariant_block_transcript_distance_squared_bound(m, 3, m**2))}
               for m in (4, 8, 16, 32, 64, 128)]
    verified = (all(row["finite_full_source_instrument_checks_verified"] for row in controls)
                and all(row["finite_complete_source_cleanup_verified"] for row in cleanup))
    witness_shape = (4, 2)
    coefficient = kronecker_coefficient(witness_shape, witness_shape, witness_shape)
    d = hook_length_dimension(witness_shape)
    source_mass = Fraction(d * (d + character_on_involution(witness_shape, 3)), math.factorial(6))**3
    return {"created_at": utc_now(), "status": ("binary-instrument-calibration-fixed-copy-route-obstructed" if verified else "blocked-instrument-control-failure"),
        "summary": "Complete natural-source binary channels distinguish clean isotypic labels from discarded GPE reference rows. Clean compute-copy-uncompute has a uniform primitive reduction; discarding rows loses shared-hidden information. Fixed-copy repetition and the growing-copy classifier remain blocked.",
        "derivation_document": "research/BINARY_CARRIER_INSTRUMENTS.md", "controls": controls, "scaling": scaling,
        "gpe_cleanup_controls": cleanup,
        "fixed_point_free_label_arithmetic_controls": arithmetic,
        "clean_isotypic_label_access": isotypic_label_resource_contract(128, 128**2, 128, 1e-6),
        "classical_model_nonextension_witness": {"n": 6, "source_partitions": [list(witness_shape)] * 3,
            "pair_partition": list(witness_shape), "total_partition": list(witness_shape),
            "pair_kronecker_coefficient": coefficient, "joint_multiplicity": coefficient**2,
            "exact_natural_source_triple_mass": str(source_mass),
            "actual_joint_target_branch_mass_computed": False, "quantum_advantage_implied": False},
        "headline_metrics": {"finite_full_source_controls_passed": sum(row["finite_full_source_instrument_checks_verified"] for row in controls),
            "schedules_evaluated": sum(len(row["schedules"]) for row in controls),
            "explicit_one_pair_classifiers_checked": sum(item["one_pair_character_likelihood_residual"] is not None for row in controls for item in row["schedules"]),
            "source_blocks_evaluated": sum(row["source_blocks_evaluated"] for row in controls),
            "source_blocks_with_exact_latent_irrep_model": sum(row["latent_total_irrep_hmm_source_blocks"] for row in controls),
            "source_blocks_with_clean_gpe_contract": sum(row["source_blocks_evaluated"] for row in cleanup),
            "clean_gpe_cleanup_controls_passed": sum(row["finite_complete_source_cleanup_verified"] for row in cleanup),
            "polynomial_label_arithmetic_controls": len(arithmetic),
            "growing_copy_measurement_compilers": 0},
        "claim_gate": {"finite_complete_channel_evaluation_verified": verified,
            "invariant_transcript_implies_zero_binary_signal": False,
            "ideal_likelihood_tables_are_scalable_classifiers": False,
            "residual_helstrom_measurement_compiled": False, "general_classical_separation_proved": False,
            "legal_classical_sampler_for_initial_latent_distribution_supplied": False,
            "latent_model_replaces_quantum_frontend": False,
            "clean_isotypic_label_uniform_primitive_reduction_available": True,
            "exact_fixed_point_free_two_copy_score_available": True,
            "finite_clean_gpe_controls_verified": all(row["finite_complete_source_cleanup_verified"] for row in cleanup),
            "discarded_gpe_reference_implements_luders_in_general": False,
            "gate_level_sn_qft_backend_supplied": False,
            "finite_alternation_explained_by_latent_irrep_model": all(row["latent_total_irrep_hmm_source_blocks"] == row["source_blocks_evaluated"]
                                                                   and row["full_outcome_law_hmm_replay_residual"] < 1e-8 for row in controls),
            "fixed_copy_calibrations_are_candidate_algorithms": False, "speedup_claim_allowed": False},
        "falsifiers_triggered": ["Conjugation invariance removes hidden-member information, not necessarily class-versus-trivial information.",
            "Measuring another carrier label can irreversibly lose information; a large commutator does not certify an improved detector.",
            "All tested L/R binary outcome laws are reproduced by classical latent-irrep dynamics after the joint quantum label front end; no legal classical replacement of that front end is supplied.",
            "Discarding the GPE reference rows has the same first-label probabilities but is a pair-local twirl, not the assumed Luders instrument; it erases all remaining three-input binary information conditional on that label.",
            "Fixed-copy invariant instruments repeated polynomially many times remain below the required asymptotic information budget."],
        "next_experiments": ["Supply a growing-copy collective program AND an efficiently evaluable outcome decision rule.",
            "Compare its full source-weighted channel against stronger product-basis and tensor-contraction baselines.",
            "Use the current schedules only as regression controls, not as evidence of a new scalable algorithm."],
    }


def write_binary_carrier_instrument_report(path: Path = REPORT_PATH, *, write_registry: bool = True,
        registry_experiment_id: str = DEFAULT_EXPERIMENT_ID, registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
        registry_result_id: str = "") -> dict:
    from research_registry import (ExperimentRecord, ExperimentResultRecord, NegativeResultRecord,
                                   upsert_experiment, upsert_experiment_result, upsert_negative_result)
    report = build_binary_carrier_instrument_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if write_registry:
        upsert_experiment(ExperimentRecord(id=registry_experiment_id, candidate_id=registry_candidate_id,
            title="Source-weighted binary carrier instruments", status=report["status"],
            hypothesis="Known carrier instruments expose useful binary information without assuming an ideal residual measurement.",
            protocol="Evaluate physical null/shared-hidden laws, actual readouts, retained states, latent-irrep replay, clean GPE compute-copy-uncompute and adversarial reference discard. Charge QFT/action calls separately from classifier cost.",
            positive_signal="A growing-copy program with a compiled outcome classifier, not finite Bayes-table performance.",
            falsifiers=["outcome mass is missing", "disturbance destroys the needed signal", "GPE workspace is discarded instead of uncomputed", "classifier cost is omitted", "fixed-copy repetition fails the information bound"],
            metrics=list(report["headline_metrics"]), dependencies=["physical three-copy Fourier blocks", "existing pair-carrier projectors"],
            next_actions=report["next_experiments"]))
        upsert_experiment_result(ExperimentResultRecord(id=registry_result_id or f"RESULT-{registry_experiment_id}",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id, created_at=report["created_at"],
            status=report["status"], summary=report["summary"], metrics=report["headline_metrics"],
            falsifiers_triggered=report["falsifiers_triggered"], artifacts={"binary_carrier_instruments": str(path)}))
        if report["claim_gate"]["finite_complete_channel_evaluation_verified"]:
            upsert_negative_result(NegativeResultRecord(id="CARRIER-INVARIANCE-NOT-A-BINARY-NO-GO", source=registry_experiment_id,
                claim="An invariant carrier transcript with no information about which class member is hidden cannot detect the class against the trivial subgroup.",
                reason_invalid="The two tasks have different priors and alternatives. Complete S3/S4 physical channels have nonzero binary signal; the one-pair character likelihood is checked independently.",
                lesson="Evaluate the actual null/alternative distributions, retain all source weights, and separately account for copy scaling and classifier implementation.",
                applies_to=[registry_candidate_id, "carrier transcript task transfer"], evidence={"artifact": str(path)}))
        if report["claim_gate"]["finite_alternation_explained_by_latent_irrep_model"]:
            upsert_negative_result(NegativeResultRecord(id="FINITE-BINARY-CARRIER-ALTERNATION-LATENT-IRREP", source=registry_experiment_id,
                claim="For the tested S3/S4 binary inputs, alternating carrier outcome laws cannot be reproduced by classical postprocessing of a joint pair/total quantum label outcome.",
                reason_invalid="Every L/R transcript and final Young-row probability is reproduced by latent-irrep Markov dynamics after the joint pair/total quantum label measurement. Measuring that total label after one pair resolves the retained finite binary information.",
                lesson="A dephased product-basis ablation was too weak. No legal classical sampler for the hypothesis-dependent initial latent distribution is supplied, so this does not replace the quantum front end. The rank-one condition already fails in S6, and transition-computation cost must be charged.",
                applies_to=[registry_candidate_id, "finite alternating-carrier binary signals"], evidence={"artifact": str(path)}))
        if report["claim_gate"]["finite_clean_gpe_controls_verified"]:
            upsert_negative_result(NegativeResultRecord(id="DISCARDED-GPE-REFERENCE-NOT-LUDERS-INSTRUMENT", source=registry_experiment_id,
                claim="Copying an isotypic label and discarding the GPE reference rows implements the clean projective instrument used by subsequent carrier measurements.",
                reason_invalid="Fourier Kraus sums give a group twirl within each label, not P rho P. All physical S3/S4 source triples retain only first-pair transcript information after pair-reference discard; in S4 this loses an additional 37/192 trace distance relative to clean L.",
                lesson="Copy only the irrep label, then invert the entire GPE computation to clean its workspace. Charge supplied QFT and controlled-action access. A global diagonal twirl preserves the binary mixture; this pair-local failure is neither an arbitrary compiler no-go nor classical dequantization.",
                applies_to=[registry_candidate_id, "isotypic instrument implementation"], evidence={"artifact": str(path), "derivation": report["derivation_document"]}))
    return report

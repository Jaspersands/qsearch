"""Native full-root covariant readout, paired noise and costed attack gates.

LOCAL DERIVATIONS / REVIEW PENDING. A receiver and held-out verifier exist;
the polynomial radix decoder REQUIRES CHOSEN LABELS, not the native source.
No efficient random-label secret search or quantum advantage is supplied.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random

import numpy as np
from flint import nmod_mat

from cyclotomic_fiber_receiver import native_source

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_covariant_noise.json"
ROOT_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))


def _integer(x, name, minimum=1):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def root_digits(q):
    _integer(q, "native modulus", 3)
    r, value = 0, q
    while value % 3 == 0:
        r, value = r+1, value//3
    if value != 1:
        raise ValueError("native modulus must be a power of3")
    return r


def _word(values, q, name, length=None):
    values = tuple(values)
    if not values or (length is not None and len(values) != length) or any(
            type(x) is not int or not 0 <= x < q for x in values):
        raise ValueError(f"canonical nonempty {name} required")
    return values


def phase(x, q):
    return complex(np.exp(2j*np.pi*float(Fraction(x % q, q))))


def noise_probability(q, first, second):
    """Exact formula, numerically evaluated; no Gaussian-error substitution."""
    root_digits(q)
    _word((first, second), q, "paired noise", 2)
    return abs(1+phase(first, q)+phase(second, q))**2/(3*q*q)


def noise_character(q, frequency):
    """E exp(2*pi*i*frequency.e/q), by exact character orthogonality."""
    root_digits(q)
    frequency = _word(frequency, q, "paired frequency", 2)
    if frequency == (0, 0):
        return Fraction(1)
    roots = {(a % q, b % q) for a, b in ROOT_DIRECTIONS}
    return Fraction(1, 3) if frequency in roots else Fraction(0)


def qutrit_qft_recipe(digits, offset=0):
    """Inverse QFT over Z_(3**digits), using only one/two-qutrit gates."""
    _integer(digits, "register digits")
    _integer(offset, "register offset", 0)
    tape = []
    for j in range(digits):
        tape.append({"gate": "inverse_F3", "wire": offset+j})
        for k in range(j+1, digits):
            tape.append({"gate": "controlled_phase", "wires": (offset+j, offset+k),
                         "phase_denominator": 3**(k-j+1), "phase_sign": -1})
    for j in range(digits//2):
        tape.append({"gate": "swap", "wires": (offset+j, offset+digits-1-j)})
    return tuple(tape)


def receiver_recipe(digits):
    """Explicit native embedding: the fixed two-qutrit swap20<->01."""
    _integer(digits, "root digits")
    tape = ({"gate": "swap_basis20_01", "wires": (digits-1, 2*digits-1)},)
    return {"qutrit_registers": 2*digits, "input_qutrit_wire": digits-1,
            "clean_qutrit_ancillas": 2*digits-1,
            "gates": tape+qutrit_qft_recipe(digits)+qutrit_qft_recipe(digits, digits),
            "all_registers_measured_in_computational_basis": True,
            "unknown_state_preparation_or_inverse_required": False,
            "approximate_phase_gate_error_must_be_charged": True,
            "one_and_two_qutrit_gates_are_explicit_not_a_Q_square_table": True,
            "hardware_qubit_native_gate_compilation_supplied": False}


def apply_qutrit_tape(state, width, tape):
    """Bounded gate replay, deliberately separate from the scalable recipe."""
    _integer(width, "gate replay width")
    if width > 6:
        raise ValueError("dense gate replay capped at six qutrits")
    state = np.asarray(state, dtype=complex)
    if state.shape != (3**width,):
        raise ValueError("one state amplitude per native qutrit word required")
    state = state.reshape((3,)*width)
    F3 = np.array([[phase(-j*k, 3)/math.sqrt(3) for k in range(3)] for j in range(3)])
    for gate in tape:
        if gate["gate"] == "inverse_F3":
            wire = gate["wire"]
            state = np.moveaxis(np.tensordot(F3, state, axes=(1, wire)), 0, wire)
            continue
        first, second = gate["wires"]
        if gate["gate"] == "controlled_phase":
            a, b = [1]*width, [1]*width
            a[first] = b[second] = 3
            products = np.arange(3).reshape(a)*np.arange(3).reshape(b)
            state = state*np.exp(2j*np.pi*gate["phase_sign"]*products/gate["phase_denominator"])
        elif gate["gate"] == "swap":
            state = np.swapaxes(state, first, second)
        elif gate["gate"] == "swap_basis20_01":
            swapped = state.copy()
            source, target = [slice(None)]*width, [slice(None)]*width
            source[first], source[second], target[first], target[second] = 2, 0, 0, 1
            swapped[tuple(source)], swapped[tuple(target)] = state[tuple(target)], state[tuple(source)]
            state = swapped
        else:
            raise ValueError("unknown native gate")
    return state.reshape(-1)


@dataclass(frozen=True)
class CovariantRecord:
    first: tuple
    second: tuple
    outcome: tuple
    modulus: int

    def __post_init__(self):
        root_digits(self.modulus)
        object.__setattr__(self, "first", _word(self.first, self.modulus, "first frequency"))
        object.__setattr__(self, "second", _word(self.second, self.modulus, "second frequency", len(self.first)))
        object.__setattr__(self, "outcome", _word(self.outcome, self.modulus, "two-register outcome", 2))

    def residual(self, trial):
        trial = _word(trial, self.modulus, "secret trial", len(self.first))
        return tuple((b-sum(a*s for a, s in zip(row, trial))) % self.modulus
                     for row, b in zip((self.first, self.second), self.outcome))

    def probability(self, trial):
        return noise_probability(self.modulus, *self.residual(trial))

    def public(self):
        return {"first": self.first, "second": self.second, "outcome": self.outcome, "modulus": self.modulus}


def physical_readout_control(source, secret):
    """One original native qutrit: bounded actual embedding and two QFTs."""
    if source.inputs != 1 or source.level % 2 or source.modulus > 27:
        raise ValueError("native one-qutrit dense control capped at modulus27")
    q = source.modulus
    secret = _word(secret, q, "calibration secret", source.dimension)
    first, second = source.frequencies[0]
    a, c = (sum(x*s for x, s in zip(row, secret)) % q for row in (first, second))
    embedded = np.zeros((q, q), dtype=complex)
    embedded[0, 0], embedded[1, 0], embedded[0, 1] = 1/math.sqrt(3), phase(a, q)/math.sqrt(3), phase(c, q)/math.sqrt(3)
    reference = np.fft.fftn(embedded, norm="ortho")
    input_state = np.zeros((q, q), dtype=complex)
    input_state[0, 0], input_state[1, 0], input_state[2, 0] = embedded[0, 0], embedded[1, 0], embedded[0, 1]
    recipe = receiver_recipe(root_digits(q))
    output = apply_qutrit_tape(input_state.reshape(-1), recipe["qutrit_registers"], recipe["gates"]).reshape(q, q)
    probabilities = abs(output)**2
    predicted = np.array([[noise_probability(q, (b-a) % q, (d-c) % q) for d in range(q)] for b in range(q)])
    error = float(np.max(abs(probabilities-predicted)))
    circuit_error = float(np.max(abs(output-reference)))
    if error > 1e-11 or circuit_error > 1e-11 or abs(float(probabilities.sum())-1) > 1e-11:
        raise ArithmeticError("full native quantum readout/source law mismatch")
    return {"native_level": source.level, "modulus": q, "native_labels": source.labels,
            "calibration_secret": secret, "outcome_probability_error": error,
            "gate_recipe": recipe, "gate_replay_amplitude_error": circuit_error,
            "normalization_error": abs(float(probabilities.sum())-1),
            "embedding_support": [[0, 0], [1, 0], [0, 1]],
            "all_outcomes_kept": True, "source_substituted_by_field_shadow": False,
            "dense_QFT_is_calibration_only": True}


def sample_noise(q, rng):
    """Offline floating sampler of the EXACT physical error formula.

    Uniform proposals, density<=3 and mean acceptance1/3. This simulates
    classical outcomes for tests; it does NOT supply an unknown phase state.
    """
    root_digits(q)
    proposals = 0
    while True:
        e = (rng.randrange(q), rng.randrange(q))
        proposals += 1
        if rng.random() < abs(1+phase(e[0], q)+phase(e[1], q))**2/9:
            return e, proposals


def simulated_record(first, second, secret, q, rng):
    """Native-law calibration; the latent secret never enters the decoder."""
    first = _word(first, q, "first frequency")
    second = _word(second, q, "second frequency", len(first))
    secret = _word(secret, q, "calibration secret", len(first))
    e, proposals = sample_noise(q, rng)
    outcomes = tuple((sum(x*s for x, s in zip(row, secret))+error) % q
                     for row, error in zip((first, second), e))
    return CovariantRecord(first, second, outcomes, q), proposals


def projected_noise_character(q, pair_weights, frequency):
    """Scalar compression of INDEPENDENT original qutrit errors.

    Weights must be fixed independently of outcomes. Shared original records
    must first be combined to their NET weights, not treated as fresh copies.
    """
    root_digits(q)
    _word((frequency,), q, "scalar dual frequency", 1)
    weights = tuple(_word(pair, q, "paired linear weight", 2) for pair in pair_weights)
    if not weights:
        raise ValueError("at least one original qutrit weight required")
    return math.prod(noise_character(q, tuple(frequency*x % q for x in pair)) for pair in weights)


def scalar_projection_gate(q, pair_weights):
    """Complete compact classification, including nonunit subgroup noise."""
    root_digits(q)
    weights = tuple(_word(pair, q, "paired linear weight", 2) for pair in pair_weights)
    if not weights:
        raise ValueError("nonempty paired weight list required")
    nonzero = tuple(pair for pair in weights if any(pair))
    if not nonzero:
        return {"classification": "zero_statistic", "noise_image_step": q,
                "secret_information_in_this_scalar": False}
    unit = next((x for pair in nonzero for x in pair if x % 3), None)
    if unit is None:
        step = math.gcd(q, *(x for pair in nonzero for x in pair))
        return {"classification": "uniform_on_noise_image_subgroup", "noise_image_step": step,
                "secret_information_in_this_scalar": False,
                "unknown_linear_mean_belongs_to_same_subgroup": True}
    inverse = pow(unit, -1, q)
    normalized = [tuple(inverse*x % q for x in pair) for pair in nonzero]
    if any(noise_character(q, pair) == 0 for pair in normalized):
        return {"classification": "exactly_uniform_full_modulus", "noise_image_step": 1,
                "secret_information_in_this_scalar": False}
    bias = Fraction(1, 3)**len(nonzero)
    return {"classification": "common_unit_scaled_root_directions", "noise_image_step": 1,
            "surviving_dual_frequencies": sorted((inverse, -inverse % q)),
            "fourier_bias": str(bias), "active_original_qutrits": len(nonzero),
            "nonuniform_noise_allows_potential_signal": True,
            "secret_information_proved_without_the_combined_public_label": False,
            "inverse_squared_bias_sampling_scale": str(1/(bias*bias))}


def compression_character(q, rows, frequency):
    """Exact pushed-forward Fourier law; NO scalar-marginal independence."""
    root_digits(q)
    rows = tuple(tuple(row) for row in rows)
    frequency = _word(frequency, q, "compression dual frequency", len(rows))
    if not rows or not rows[0] or len(rows[0]) % 2 or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("rectangular compression on paired original errors required")
    for row in rows:
        _word(row, q, "compression row", len(rows[0]))
    original_dual = tuple(sum(u*row[j] for u, row in zip(frequency, rows)) % q for j in range(len(rows[0])))
    return math.prod(noise_character(q, original_dual[j:j+2]) for j in range(0, len(original_dual), 2))


@dataclass(frozen=True)
class TaggedEquation:
    """One marginal with an EXACT known complex first-character bias.

    Origins include all supplied ancestors, even those with coefficient zero:
    the IID fresh-batch source argument must not silently reuse their labels.
    """
    first: tuple
    outcome: int
    modulus: int
    bias: Fraction
    noise_phase_turns: Fraction
    origins: frozenset

    def __post_init__(self):
        root_digits(self.modulus)
        object.__setattr__(self, "first", _word(self.first, self.modulus, "tagged first frequency"))
        _word((self.outcome,), self.modulus, "tagged outcome", 1)
        if not isinstance(self.bias, Fraction) or not 0 < self.bias <= Fraction(1, 3):
            raise ValueError("exact positive physical marginal bias<=1/3 required")
        if not isinstance(self.noise_phase_turns, Fraction):
            raise ValueError("exact known phase tag required")
        object.__setattr__(self, "noise_phase_turns", self.noise_phase_turns % 1)
        origins = frozenset(self.origins)
        if not origins or any(type(i) is not int or i < 0 for i in origins):
            raise ValueError("nonempty canonical original record IDs required")
        object.__setattr__(self, "origins", origins)

    @classmethod
    def from_covariant(cls, record, origin):
        return cls(record.first, record.outcome[0], record.modulus, Fraction(1, 3), Fraction(0), frozenset((origin,)))

    def probability(self, trial):
        trial = _word(trial, self.modulus, "tagged trial", len(self.first))
        residual = (self.outcome-sum(a*s for a, s in zip(self.first, trial))) % self.modulus
        angle = (Fraction(residual, self.modulus)-self.noise_phase_turns) % 1
        return (1+2*float(self.bias)*phase(angle.numerator, angle.denominator).real)/self.modulus

    def public(self):
        return {"first": self.first, "outcome": self.outcome, "modulus": self.modulus,
                "bias": str(self.bias), "noise_phase_turns": str(self.noise_phase_turns),
                "original_record_ids": sorted(self.origins)}


def low_signed_relation(first_vectors):
    """Canonical GF3 kernel word, represented by INTEGER signs0,+1,-1."""
    vectors = tuple(tuple(v) for v in first_vectors)
    if not vectors or not vectors[0] or any(len(v) != len(vectors[0]) for v in vectors) or any(
            type(x) is not int or x < 0 for v in vectors for x in v):
        raise ValueError("rectangular public nonnegative frequency vectors required")
    n, m = len(vectors[0]), len(vectors)
    if m < n+1:
        raise ValueError("n+1 supplied equations required for guaranteed relation")
    reduced, rank = nmod_mat([[v[l] % 3 for v in vectors] for l in range(n)], 3).rref()
    pivots = tuple(next(j for j in range(m) if reduced[i, j]) for i in range(rank))
    free = next(j for j in range(m) if j not in pivots)
    coefficients = [0]*m; coefficients[free] = 1
    for i, pivot in enumerate(pivots):
        coefficients[pivot] = -int(reduced[i, free]) % 3
    return tuple(-1 if x == 2 else x for x in coefficients)


def collimate_tagged(records):
    """Actual classical modulus reduction, ALL outcome residues retained.

    A low-only Gaussian relation forces the linear mean divisible by3.
    Dividing the outcome keeps its residue as an exact noise-phase tag.
    Signal amplitude MULTIPLIES; this is not coherent phase-state sieving.
    """
    records = tuple(records)
    if not records or any(not isinstance(record, TaggedEquation) for record in records):
        raise ValueError("tagged independent equations required")
    q, n = records[0].modulus, len(records[0].first)
    if q <= 3 or any(record.modulus != q or len(record.first) != n for record in records):
        raise ValueError("equal-dimensional equations at a native root above3 required")
    seen = set()
    for record in records:
        if seen.intersection(record.origins):
            raise ValueError("shared original ancestors invalidate independent-noise multiplication")
        seen.update(record.origins)
    weights = low_signed_relation(tuple(record.first for record in records))
    combined = tuple(sum(w*record.first[j] for w, record in zip(weights, records)) % q for j in range(n))
    if any(a % 3 for a in combined):
        raise ArithmeticError("low Gaussian relation failed native integer divisibility")
    observed = sum(w*record.outcome for w, record in zip(weights, records)) % q
    residue = observed % 3
    bias = math.prod(record.bias for w, record in zip(weights, records) if w)
    turns = (sum((w*record.noise_phase_turns for w, record in zip(weights, records)), Fraction(0))
             -Fraction(residue, q)) % 1
    output = TaggedEquation(tuple(a//3 for a in combined), observed//3, q//3, bias, turns, frozenset(seen))
    return output, {"parent_modulus": q, "output_modulus": q//3, "signed_weights": weights,
                    "observed_residue": residue, "all_three_residues_kept": True,
                    "supplied_equations_charged": len(records), "original_qutrits_charged": len(seen),
                    "surviving_bias": str(bias), "noise_phase_turns": str(turns),
                    "zero_output_frequency_is_no_secret_signal": not any(output.first),
                    "inverse_squared_bias_sampling_scale": str(1/(bias*bias)),
                    "unit_visibility_preserved_like_a_quantum_phase_state": False,
                    "unused_parent_transcripts_or_joint_multiple_outputs_bounded": False}


def bkw_collision_ledger(n, digits, samples, eliminated_coordinates=1, leaves=2):
    _integer(n, "dimension")
    _integer(digits, "root digits")
    _integer(samples, "supplied native records")
    _integer(eliminated_coordinates, "exact collision coordinates")
    _integer(leaves, "independent signed-sum leaves")
    if eliminated_coordinates > n:
        raise ValueError("cannot eliminate more coordinates than available")
    q = 3**digits
    bound = min(Fraction(1), Fraction(math.comb(samples, 2), q**eliminated_coordinates))
    return {"dimension": n, "modulus": str(q), "supplied_original_qutrits": samples,
            "eliminated_coordinates": eliminated_coordinates,
            "exact_coordinate_collisions_probability_upper": str(bound),
            "signed_sum_active_original_records": leaves, "surviving_character_bias": str(Fraction(1, 3)**leaves),
            "inverse_squared_bias_sampling_scale": str(9**leaves),
            "labels_only_bucket_selection_and_independent_disjoint_leaves_required": True,
            "low_modulus_bucket_match_is_full_modulus_elimination": False,
            "shared_combined_records_are_independent": False,
            "all_classical_preprocessing_or_joint_decoding_ruled_out": False}


def chosen_radix_plan(n, digits):
    _integer(n, "dimension")
    _integer(digits, "root digits")
    q = 3**digits
    return tuple((coordinate, digit, tuple(3**(digits-1-digit) if j == coordinate else 0 for j in range(n)))
                 for coordinate in range(n) for digit in range(digits))


def decode_chosen_radix(batches, n, digits):
    """Actual polynomial estimator, but checks its stronger access premise.

    Each scheduled frequency needs fresh copies. Native IID labels do not
    supply this schedule efficiently. No all-secret search or planted-secret
    argument is passed to the estimator.
    """
    plan = chosen_radix_plan(n, digits)
    batches = tuple(tuple(batch) for batch in batches)
    if len(batches) != len(plan):
        raise ValueError("one fresh batch per scheduled chosen frequency required")
    q, recovered = 3**digits, [0]*n
    decisions = []
    for (coordinate, digit, first), batch in zip(plan, batches):
        if not batch or any(not isinstance(record, CovariantRecord) or record.modulus != q
                            or record.first != first for record in batch):
            raise ValueError("decoder rejects random labels substituted for chosen frequencies")
        correction = sum(a*s for a, s in zip(first, recovered)) % q
        mean = sum(phase(record.outcome[0]-correction, q) for record in batch)/len(batch)
        scores = [float((mean*phase(-d, 3)).real) for d in range(3)]
        value = max(range(3), key=lambda d: scores[d])
        recovered[coordinate] += value*3**digit
        decisions.append({"coordinate": coordinate, "digit": digit, "chosen_first_frequency": first,
                          "samples": len(batch), "scores": scores, "decoded_digit": value})
    return {"secret": tuple(recovered), "decisions": decisions,
            "access_model": "CHOSEN_NATIVE_PHASE_FREQUENCIES_REQUIRED",
            "random_native_source_decoder_supplied": False}


def radix_access_ledger(n, digits, confidence_bits=16):
    plan = chosen_radix_plan(n, digits)
    _integer(confidence_bits, "confidence bits")
    repeats = 24*((2*len(plan)-1).bit_length()+confidence_bits)
    samples = repeats*len(plan)
    q = 3**digits
    return {"dimension": n, "root_digits": digits, "modulus": str(q),
            "chosen_frequency_samples_per_digit": repeats, "chosen_qutrits_required": samples,
            "conditional_chosen_access_failure_bound": f"2^-{confidence_bits}",
            "native_exact_first_frequency_probability": str(Fraction(1, q**n)),
            "expected_native_qutrits_for_rejection_compiling_this_exact_schedule": str(samples*q**n),
            "random_native_label_access_is_chosen_query_access": False,
            "native_polynomial_decoder_or_speedup_claim": False}


def heldout_score(records, trial):
    """Three correlated character features per qutrit, not three samples."""
    records = tuple(records)
    if not records or any(record.modulus != records[0].modulus or len(record.first) != len(records[0].first)
                          for record in records):
        raise ValueError("fresh equal-dimension/equal-modulus held-out records required")
    return sum((phase(e[0], record.modulus)+phase(e[1], record.modulus)
                +phase(e[0]-e[1], record.modulus)).real
               for record in records for e in (record.residual(trial),))/len(records)


def heldout_gate(samples, tested_candidates=1):
    _integer(samples, "held-out samples")
    _integer(tested_candidates, "held-out-independent candidate count")
    return {"fresh_native_qutrit_records": samples, "tested_candidates": tested_candidates,
            "score_threshold": .5, "true_secret_mean_score": 1, "fixed_wrong_secret_native_mean_score": 0,
            "false_acceptance_union_bound": "min(1,T*exp(-2*M/81))",
            "true_rejection_upper": "exp(-2*M/81)",
            "false_acceptance_union_bound_approximation": min(1., tested_candidates*math.exp(-2*samples/81)),
            "candidates_independent_of_this_holdout_required": True,
            "adaptive_reuse_or_label_selected_holdout_certified": False,
            "efficient_candidate_generation_supplied": False}


def native_identifiability_ledger(n, digits, confidence_bits=16):
    """Polynomial samples uniquely separate secrets; SEARCH still missing."""
    _integer(n, "dimension")
    _integer(digits, "root digits")
    _integer(confidence_bits, "confidence bits")
    # ln(3)<2, ln(2)<1 and 2*41/81>1 make this integer choice conservative.
    samples = 41*(2*n*digits+confidence_bits)
    return {"dimension": n, "root_digits": digits, "native_qutrit_samples": samples,
            "secret_count": str(3**(n*digits)),
            "unique_score_threshold_separator_failure_upper": f"2^-{confidence_bits}",
            "proof": "Union over true rejection and every fixed wrong trial: q^n*exp(-2*M/81)",
            "all_secret_search_required_by_reference_decoder": True,
            "efficient_random_label_candidate_search_supplied": False,
            "information_sufficiency_is_a_quantum_speedup": False}


def _native_controls():
    rows = []
    for n, level, labels, secret in ((1, 4, [[(2, 5)]], (7,)),
                                     (2, 4, [[(2, 5), (8, 4)]], (7, 3)),
                                     (1, 6, [[(17, 11)]], (23,))):
        rows.append(physical_readout_control(native_source(labels, level), secret))
    return rows


def _heldout_controls():
    controls = []
    for n, digits, seed in ((2, 8, 81201), (4, 16, 81202), (8, 32, 81203)):
        rng, q = random.Random(seed), 3**digits
        secret = tuple(rng.randrange(q) for _ in range(n))
        records, proposals = [], 0
        for _ in range(1024):
            first, second = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
            record, count = simulated_record(first, second, secret, q, rng)
            records.append(record); proposals += count
        wrong = ((secret[0]+q//3) % q, *secret[1:])
        controls.append({"dimension": n, "root_digits": digits, "modulus": str(q), "seed": seed,
                         "heldout_records": len(records), "offline_noise_proposals": proposals,
                         "true_secret_score": heldout_score(records, secret),
                         "fixed_nonprimitive_difference_wrong_secret_score": heldout_score(records, wrong),
                         "first_three_public_records": [record.public() for record in records[:3]],
                         "gate": heldout_gate(len(records)),
                         "truth_used_only_to_simulate_and_evaluate_not_to_search": True,
                         "native_secret_recovery_algorithm": False})
    return controls


def build_report():
    q, n, digits, repeats = 3**12, 2, 12, 192
    rng, secret = random.Random(81103), (127493, 381742)
    batches, proposals = [], 0
    for _, _, first in chosen_radix_plan(n, digits):
        batch = []
        for _ in range(repeats):
            record, count = simulated_record(first, tuple(rng.randrange(q) for _ in range(n)), secret, q, rng)
            batch.append(record); proposals += count
        batches.append(batch)
    radix = decode_chosen_radix(batches, n, digits)
    if radix["secret"] != secret:
        raise ArithmeticError("chosen-access calibration failed; not evidence of native-source recovery")
    rng, q_tree, n_tree = random.Random(81303), 81, 2
    tree_secret = (37, 59)
    tree = []
    for origin in range(27):
        first, second = (tuple(rng.randrange(q_tree) for _ in range(n_tree)) for _ in range(2))
        record, _ = simulated_record(first, second, tree_secret, q_tree, rng)
        tree.append(TaggedEquation.from_covariant(record, origin))
    original_tree = [record.public() for record in tree]
    tree_steps = []
    while tree[0].modulus > 3:
        next_layer = []
        for start in range(0, len(tree), n_tree+1):
            output, ledger = collimate_tagged(tree[start:start+n_tree+1])
            next_layer.append(output); tree_steps.append({"ledger": ledger, "output": output.public()})
        tree = next_layer
    return {"schema_version": 1, "status": "LOCAL_NATIVE_RECEIVER_AND_CLASSICAL_ACCESS_AUDIT_REVIEW_PENDING",
            "noise_law": "|1+exp(2pi*i*e1/q)+exp(2pi*i*e2/q)|^2/(3*q^2)",
            "exact_noise_fourier_support": [[list(v), "1/3"] for v in ROOT_DIRECTIONS]+[[[0, 0], "1"]],
            "exact_paired_collision_multiplier": "5/3",
            "paired_errors_independent_within_a_qutrit": False,
            "different_fresh_qutrit_error_pairs_independent": True,
            "native_physical_readout_controls": _native_controls(),
            "scalable_receiver_gate_ledgers": [{"root_digits": r, "qutrits": 2*r,
                                                 "one_two_qutrit_gate_count": 1+2*(r+r*(r-1)//2+r//2)}
                                                for r in (4, 16, 32, 128)],
            "scalar_attack_gates": [{"modulus": 81, "weights": weights, "gate": scalar_projection_gate(81, weights)}
                                    for weights in (((1, 0), (80, 0)), ((1, 0), (2, 0)), ((1, 2),), ((3, 0),), ((1, 0), (0, 1), (1, 80)))],
            "chosen_access_countercontrol": {"modulus": str(q), "dimension": n, "root_digits": digits,
                                              "physical_qutrits_consumed": n*digits*repeats,
                                              "offline_noise_proposals": proposals, "decoded_secret": radix["secret"],
                                              "planted_calibration_secret": secret, "decisions": radix["decisions"],
                                              "first_register_outcomes": [[record.outcome[0] for record in batch] for batch in batches],
                                              "access_premise_is_NOT_native_random_labels": True,
                                              "speedup_claim_allowed": False},
            "chosen_access_ledgers": [radix_access_ledger(n, r) for n, r in ((1, 12), (4, 16), (8, 32))],
            "exact_BKW_collision_ledgers": [bkw_collision_ledger(4, r, 4096, leaves=leaves)
                                            for r, leaves in ((8, 2), (16, 4), (32, 8))],
            "classical_Gaussian_collimation": {"dimension": n_tree, "original_modulus": q_tree,
                                              "original_marginal_records": original_tree, "steps": tree_steps,
                                              "final_record": tree[0].public(), "original_secret_mod3": tuple(x % 3 for x in tree_secret),
                                              "original_phase_states_classically_simulated": False,
                                              "compressed_scalar_signal_not_full_transcript_information": True},
            "growing_root_heldout_controls": _heldout_controls(),
            "native_polynomial_sample_identifiability": [native_identifiability_ledger(n, r)
                                                         for n, r in ((2, 8), (4, 16), (8, 32), (32, 128))],
            "proof_obligations": ["independent review of exact paired channel and compression classification",
                                  "full QFT gate precision and reversible embedding, not dense tables",
                                  "polynomial native random-label candidate search or source-valid chosen-label compiler",
                                  "classical attacks retain joint error correlations and charge label collisions",
                                  "held-out independence; training reuse does not certify a proposed secret"],
            "accepted_quantum_algorithm": False, "random_label_polynomial_secret_decoder": False,
            "classical_simulator_of_original_unknown_phase_states": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
        print(json.dumps({"report": str(REPORT), "accepted_quantum_algorithm": False,
                          "chosen_access_qutrits": report["chosen_access_countercontrol"]["physical_qutrits_consumed"]}))
    else:
        print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

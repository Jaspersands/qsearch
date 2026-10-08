"""Heterogeneous zero-sum block receiver for vector-centre F3 StateHSP.

LOCAL DERIVATION / REVIEW PENDING. Ordinary nil-2 HSP is already tractable.
Calibrations are deliberately classically easy and cannot establish advantage.
The specified quantum algorithm uses unknown copies and known controlled R,
not the hidden parameters or probability tables used by the reference driver.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from flint import nmod_mat
import numpy as np

from cyclic_centre_state_hsp_receiver import (
    ceil, character_matrix, density, dot, integer, kernel, qutrit_sector_actions,
    word, words, probabilities_from_moments,
)
from ternary_cyclic_extractor import zero_sum_support

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/VECTOR_CENTRE_STATE_HSP_TARGET.md"
REPORT = ROOT / "research/reductions/vector_centre_state_hsp_receiver.json"


def rank(rows, width):
    rows = tuple(word(row, width, 3) for row in rows)
    return int(nmod_mat(rows, 3).rank()) if rows and width else 0


def span_contains(frame, v):
    v = word(v, len(v), 3)
    return rank(tuple(frame)+(v,), len(v)) == rank(frame, len(v))


def nullspace(rows, width):
    integer(width, "field dimension")
    if width == 0:
        for row in rows:
            word(row, 0, 3)
        return ()
    return kernel(rows, width, 3)


def combine(frame, c, width):
    c = word(c, len(frame), 3)
    return tuple(sum(a*v[i] for a, v in zip(c, frame)) % 3 for i in range(width))


def complement(frame, width):
    frame = tuple(word(v, width, 3) for v in frame)
    if rank(frame, width) != len(frame):
        raise ValueError("independent field frame required")
    full, extra = list(frame), []
    for j in range(width):
        e = tuple(int(i == j) for i in range(width))
        if not span_contains(full, e):
            full.append(e)
            extra.append(e)
    return tuple(extra)


class SpanAccumulator:
    def __init__(self, width):
        integer(width, "span dimension")
        self.width, self.rows = width, []

    def add(self, row):
        row = word(row, self.width, 3)
        if len(self.rows) < self.width and rank(tuple(self.rows)+(row,), self.width) > len(self.rows):
            self.rows.append(row)

    def kernel(self):
        return nullspace(self.rows, self.width)


@dataclass(frozen=True)
class VectorExtension:
    B: tuple[tuple[tuple[int, ...], ...], ...]

    def __post_init__(self):
        if not isinstance(self.B, (tuple, list)) or not self.B or not self.B[0]:
            raise ValueError("nonempty vector bilinear form required")
        d = len(self.B[0])
        matrices = []
        for matrix in self.B:
            if len(matrix) != d:
                raise ValueError("all central components need the same square field matrix")
            matrices.append(tuple(word(row, d, 3) for row in matrix))
        object.__setattr__(self, "B", tuple(matrices))

    @property
    def d(self):
        return len(self.B[0])

    @property
    def k(self):
        return len(self.B)

    def bilinear(self, x, y):
        x, y = word(x, self.d, 3), word(y, self.d, 3)
        return tuple(sum(x[i]*dot(row, y) for i, row in enumerate(A)) % 3 for A in self.B)

    def element(self, g):
        if not isinstance(g, (tuple, list)) or len(g) != 2:
            raise ValueError("group element (quotient vector, centre vector) required")
        return word(g[0], self.d, 3), word(g[1], self.k, 3)

    def multiply(self, g, h):
        x, z = self.element(g)
        y, w = self.element(h)
        return (tuple((a+b) % 3 for a, b in zip(x, y)),
                tuple((a+b+c) % 3 for a, b, c in zip(z, w, self.bilinear(x, y))))

    def commutator(self, x, y):
        return tuple((a-b) % 3 for a, b in zip(self.bilinear(x, y), self.bilinear(y, x)))

    def quotient_chart(self, quotient_frame, central_fixed_frame):
        V = tuple(word(v, self.d, 3) for v in quotient_frame)
        Z = tuple(word(v, self.k, 3) for v in central_fixed_frame)
        if rank(V, self.d) != len(V) or rank(Z, self.k) != len(Z):
            raise ValueError("independent quotient and central frames required")
        for x in V:
            for y in V:
                if not span_contains(Z, self.commutator(x, y)):
                    raise ValueError("commutator escapes learned fixed centre: return FAILURE")
        return QuotientChart(self, V, Z, complement(Z, self.k))


@dataclass(frozen=True)
class QuotientChart:
    extension: VectorExtension
    quotient_frame: tuple
    central_fixed_frame: tuple
    central_complement: tuple

    @property
    def dimension(self):
        return len(self.quotient_frame)+len(self.central_complement)

    def section(self, coordinates):
        t = word(coordinates, self.dimension, 3)
        split = len(self.quotient_frame)
        x = combine(self.quotient_frame, t[:split], self.extension.d)
        z = combine(self.central_complement, t[split:], self.extension.k)
        return x, tuple((a+2*b) % 3 for a, b in zip(z, self.extension.bilinear(x, x)))

    def record(self):
        whole_abelian = not any(any(self.extension.commutator(x, y)) for x in self.quotient_frame for y in self.quotient_frame)
        return {"quotient_frame": self.quotient_frame, "central_fixed_frame": self.central_fixed_frame,
                "central_complement": self.central_complement, "dimension": self.dimension,
                "full_preimage_group_is_abelian": whole_abelian,
                "section_homomorphism_only_mod_fixed_centre": not whole_abelian,
                "quotient_action_requires_original_fixed_centre_support": True,
                "general_section_linear_on_full_workspace_claimed": False}


def resource_ledger(d, k, epsilon, failure_bits):
    integer(d, "quotient dimension", 1)
    integer(k, "centre dimension", 1)
    integer(failure_bits, "failure bits", 1)
    if isinstance(epsilon, bool) or not isinstance(epsilon, (int, Fraction, str)):
        raise ValueError("exact rational original gap required")
    epsilon = Fraction(epsilon)
    if not 0 < epsilon <= 1:
        raise ValueError("original gap must lie in (0,1]")
    W, delta = (k+1)**2, Fraction(1, 16)
    H = 32*W*(4*d+failure_bits+2)
    N = ceil(2*Fraction(2*(W+H)+8*(2*k+failure_bits+2), 1)/epsilon)
    M = ceil(2*Fraction(2*(d+k)+failure_bits+2, 1)/epsilon)
    eta = Fraction(1, 2**(failure_bits+2))
    return {"quotient_dimension": d, "centre_dimension": k,
            "original_gap_lower": str(epsilon), "failure_bits": failure_bits,
            "zero_sum_window": W, "conditional_modulus_defect_threshold": str(delta),
            "purified_commutator_squared_upper": str(32*delta),
            "nontrivial_ternary_root_squared_distance_exact": "3",
            "required_included_witnesses_per_unfixed_central_element": H,
            "original_central_measurement_count": N, "fresh_original_final_copy_count": M,
            "total_original_copy_cap": N+M, "known_controlled_R_call_cap": 2*N+M,
            "conditional_quantum_register_buffer_cap": W,
            "leftover_registers_strictly_less_than": W,
            "central_count_failure_upper": str(eta), "all_pair_overgroup_failure_upper": str(eta),
            "final_decoder_failure_upper": str(eta), "total_ideal_failure_upper": str(3*eta),
            "same_central_sector_collision_required": False,
            "minimum_conditional_gap_assumed": False,
            "all_central_characters_enumerated_by_algorithm": False,
            "unknown_state_inverse_or_cloning_used": False,
            "original_IID_same_state_source_required": True,
            "approximate_input_or_action_error_certified": False}


class ZeroSumBuffer:
    """Each original index enters once; only a bounded live window is recycled."""

    def __init__(self, k, on_block=None, retain_blocks=False):
        integer(k, "centre dimension", 1)
        if type(retain_blocks) is not bool or (on_block is not None and not callable(on_block)):
            raise ValueError("Boolean retention flag and optional block callback required")
        self.k, self.W = k, (k+1)**2
        self.on_block, self.retain = on_block, retain_blocks
        self.buffer, self.blocks = [], []
        self.inputs = self.used = self.count = self.max_buffer = self.kernel_calls = 0
        self.digest = hashlib.sha256()

    def push(self, label):
        label = word(label, self.k, 3)
        self.buffer.append((self.inputs, label))
        self.inputs += 1
        self.max_buffer = max(self.max_buffer, len(self.buffer))
        if len(self.buffer) < self.W:
            return
        certificate = zero_sum_support([v for _, v in self.buffer])
        positions = certificate["support"]
        if (not positions or len(set(positions)) != len(positions)
                or any(type(j) is not int or not 0 <= j < self.W for j in positions)):
            raise ArithmeticError("zero-sum primitive returned an empty or reused support")
        selected = tuple(self.buffer[j] for j in positions)
        total = tuple(sum(v[j] for _, v in selected) % 3 for j in range(self.k))
        if any(total) or not 1 <= len(selected) <= self.W:
            raise ArithmeticError("invalid vector-zero-sum block")
        record = {"original_indices": tuple(i for i, _ in selected),
                  "central_characters": tuple(v for _, v in selected), "exact_sum": total,
                  "copies_consumed": len(selected), "same_sector_copies_assumed": False}
        self.digest.update((json.dumps(record, separators=(",", ":"))+"\n").encode())
        self.used += len(selected)
        self.count += 1
        self.kernel_calls += certificate["Gaussian_kernel_calls"]
        if self.retain:
            self.blocks.append(record)
        if self.on_block is not None:
            self.on_block(record)
        taken = set(positions)
        self.buffer = [v for j, v in enumerate(self.buffer) if j not in taken]

    def finish(self):
        if not len(self.buffer) < self.W or self.used+len(self.buffer) != self.inputs:
            raise ArithmeticError("coverage or bounded-memory invariant failed")
        return {"centre_dimension": self.k, "zero_sum_window": self.W,
                "original_inputs": self.inputs, "included_original_inputs": self.used,
                "block_count": self.count, "maximum_live_conditional_registers": self.max_buffer,
                "Gaussian_kernel_calls": self.kernel_calls,
                "leftover_original_indices": tuple(i for i, _ in self.buffer),
                "leftover_characters": tuple(v for _, v in self.buffer),
                "complete_blocks_retained": self.retain, "blocks": self.blocks if self.retain else None,
                "complete_selected_block_stream_sha256": self.digest.hexdigest(),
                "support_selection_reads_internal_measurement_outcomes": False,
                "retained_characters_claimed_IID": False,
                "distinct_indices_certify_physical_IID_copies": False}


def mixed_sector_instrument(labels, states, literal=True):
    """Actual differently conditioned single-qutrit Weyl states, all branches."""
    labels = tuple(word(v, 1, 3) for v in labels)
    if not labels or len(labels) != len(states) or any(sum(v[j] for v in labels) % 3 for j in range(1)):
        raise ValueError("nonempty paid VECTOR-zero-sum block required")
    if type(literal) is not bool:
        raise ValueError("Boolean literal flag required")
    states = tuple(density(s) for s in states)
    if any(s.shape != (3, 3) for s in states):
        raise ValueError("bounded Weyl control uses a single qutrit per conditional state")
    phi = np.ones(9, complex)
    for lam, rho in zip(labels, states):
        phi *= np.array([np.trace(U @ rho) for U in qutrit_sector_actions(lam[0])])
    law = probabilities_from_moments(phi, words(2, 3), 3)
    actual = None
    if literal:
        if len(labels) > 4:
            raise ValueError("complete dense mixed-instrument replay capped at four supplied copies")
        tensor = np.ones((1, 1), complex)
        for rho in states:
            tensor = np.kron(tensor, rho)
        actions = []
        for i in range(9):
            U = np.ones((1, 1), complex)
            for lam in labels:
                U = np.kron(U, qutrit_sector_actions(lam[0])[i])
            actions.append(U)
        K = np.einsum("yx,xij->yij", character_matrix(words(2, 3), 3)/9, np.stack(actions))
        actual = np.array([np.trace(U @ tensor @ U.conj().T).real for U in K])
        if max(abs(actual-law)) > 2e-11:
            raise ArithmeticError("literal heterogeneous instrument disagrees with its linearised law")
    return {"central_characters": labels, "actual_conditional_copies_consumed": len(labels),
            "input_density_real_imag": [[[[float(a.real), float(a.imag)] for a in row] for row in rho] for rho in states],
            "full_character_words": words(2, 3), "character_law_probabilities": law.tolist(),
            "literal_Kraus_probabilities": None if actual is None else actual.tolist(),
            "heterogeneous_sector_states_used": len(set(labels)) > 1,
            "identical_conditional_state_promise_used": False,
            "known_controlled_R_calls": len(labels), "all_outcomes_retained": True,
            "full_unprepared_workspace_action_claimed_linear": False}


def rank_one_extension(k):
    integer(k, "centre dimension", 1)
    return VectorExtension((((0, 0), (1, 0)),)+(((0, 0), (0, 0)),)*(k-1))


def conditional_action(label, g):
    """Known two-qutrit linear representation in a measured central sector."""
    label = word(label, len(label), 3)
    if not label:
        raise ValueError("nonempty vector character required")
    x, z = rank_one_extension(len(label)).element(g)
    a, b = x
    clock = np.diag(np.exp(2j*np.pi*b*np.arange(3)/3))
    return np.exp(2j*np.pi*(dot(label, z) % 3)/3)*np.kron(qutrit_sector_actions(label[0])[3*a+b], clock)


def vector_sector_instrument(labels, amplitudes):
    """Whole two-qutrit instruments, including nonstabilizer pure controls."""
    labels = tuple(word(v, len(labels[0]), 3) for v in labels) if labels else ()
    if not labels or len(labels) != len(amplitudes) or len(labels) > 3:
        raise ValueError("one to three supplied pure conditional copies required")
    if any(sum(v[j] for v in labels) % 3 for j in range(len(labels[0]))):
        raise ValueError("full VECTOR sum must vanish, not just the cocycle image")
    inputs = []
    norms = []
    for v in amplitudes:
        a = np.asarray(v, complex)
        if a.shape != (9,) or not np.isfinite(a).all() or np.vdot(a, a).real <= 0:
            raise ValueError("nonzero finite nine-component conditional amplitude required")
        norms.append(float(np.vdot(a, a).real))
        inputs.append(a/np.sqrt(norms[-1]))
    points = words(2, 3)
    phi = np.ones(9, complex)
    tensor_outputs = []
    for x in points:
        v = np.ones(1, complex)
        for label, state in zip(labels, inputs):
            out = conditional_action(label, (x, (0,)*len(label))) @ state
            v = np.kron(v, out)
        tensor_outputs.append(v)
    for label, state in zip(labels, inputs):
        phi *= np.array([np.vdot(state, conditional_action(label, (x, (0,)*len(label))) @ state) for x in points])
    law = probabilities_from_moments(phi, points, 3)
    branch_vectors = character_matrix(points, 3) @ np.stack(tensor_outputs)/9
    actual = np.sum(abs(branch_vectors)**2, axis=1)
    if max(abs(actual-law)) > 2e-11:
        raise ArithmeticError("two-qutrit full Kraus law disagrees with its moments")
    return {"central_characters": labels, "input_amplitudes_real_imag": [[[float(a.real), float(a.imag)] for a in v] for v in amplitudes],
            "input_amplitude_squared_norms": norms, "full_character_words": points,
            "character_law_probabilities": law.tolist(), "literal_Kraus_probabilities": actual.tolist(),
            "actual_conditional_copies_consumed": len(labels), "known_controlled_R_calls": len(labels),
            "physical_qutrits": 2*len(labels), "all_outcomes_retained": True,
            "identical_conditional_state_promise_used": False,
            "full_unprepared_workspace_action_claimed_linear": False}


def exact_vector_control(labels, coefficients, phase_exponents=None):
    if phase_exponents is None:
        phase_exponents = [(0,)*9 for _ in labels]
    if len(coefficients) != len(labels) or len(phase_exponents) != len(labels):
        raise ValueError("one exact conditional amplitude record per label required")
    phases = tuple(word(row, 9, 3) for row in phase_exponents)
    if any(len(row) != 9 or any(type(a) is not int for a in row) for row in coefficients):
        raise ValueError("nine exact integer coefficients per input required")
    vectors = [np.array(row)*np.exp(2j*np.pi*np.array(t)/3) for row, t in zip(coefficients, phases)]
    r = vector_sector_instrument(labels, vectors)
    r.update({"input_integer_amplitudes": coefficients, "input_root_phase_exponents": phases})
    return r


def calibration_amplitude(label, tau_a, tau_b, kind):
    j = -dot(label, tau_b) % 3
    coefficients, phases = [0]*9, [0]*9
    for t in range(3):
        if kind == "nonabelian-preimage" or t == 0:
            coefficients[3*t+j] = 1
            phases[3*t+j] = dot(label, tau_a)*t % 3
    return tuple(coefficients), tuple(phases)


def label_stream(seed, count, k, fixed_axes=(), skew=Fraction(1)):
    integer(seed, "random seed")
    integer(count, "source copy count")
    integer(k, "centre dimension", 1)
    if (not isinstance(skew, Fraction) or not 0 < skew <= 1
            or any(type(j) is not int or not 0 <= j < k for j in fixed_axes)
            or len(set(fixed_axes)) != len(fixed_axes)):
        raise ValueError("valid fixed coordinates and exact positive spectrum mixture required")
    rng = np.random.default_rng(seed)
    zero = (0,)*k
    for start in range(0, count, 4096):
        size = min(4096, count-start)
        batch = rng.integers(0, 3, size=(size, k), dtype=np.int8)
        for j in fixed_axes:
            batch[:, j] = 0
        active = rng.random(size) < float(skew)
        for v, a in zip(batch.tolist(), active):
            yield tuple(v) if a else zero


def receive(G, epsilon, failure_bits, backend):
    """Control flow uses measurement outcomes only, never hidden source parameters.

    The backend must implement fresh centre sampling, a single Fourier
    experiment on the ACTUAL selected registers, and fresh original-state
    quotient sampling. A simulator is not a scalable hardware implementation.
    """
    ledger = resource_ledger(G.d, G.k, epsilon, failure_bits)
    N = ledger["original_central_measurement_count"]
    centre, block_span = SpanAccumulator(G.k), SpanAccumulator(G.d)
    hist = Counter()
    def consume(block):
        y = word(backend.measure_block(block), G.d, 3)
        hist[y] += 1
        block_span.add(y)
    selector = ZeroSumBuffer(G.k, consume)
    first_labels = []
    for index in range(N):
        lam = word(backend.measure_centre(index), G.k, 3)
        if len(first_labels) < 128:
            first_labels.append(lam)
        centre.add(lam)
        selector.push(lam)
    coverage = selector.finish()
    central_basis, T = centre.kernel(), block_span.kernel()
    chart = G.quotient_chart(T, central_basis)
    final, final_hist = SpanAccumulator(chart.dimension), Counter()
    M = ledger["fresh_original_final_copy_count"]
    for index in range(N, N+M):
        y = word(backend.measure_original(chart, index), chart.dimension, 3)
        final.add(y)
        final_hist[y] += 1
    final_kernel = final.kernel()
    lifted = [chart.section(v) for v in final_kernel]+[((0,)*G.d, z) for z in central_basis]
    return {"ledger": ledger, "coverage": coverage,
            "central_character_span_basis": centre.rows, "learned_fixed_centre_basis": central_basis,
            "block_character_span_basis": block_span.rows, "block_character_histogram": [{"character": y, "count": hist[y]} for y in sorted(hist)],
            "quotient_chart": chart.record(), "final_character_span_basis": final.rows,
            "final_character_histogram": [{"character": y, "count": final_hist[y]} for y in sorted(final_hist)],
            "final_kernel_basis": final_kernel, "lifted_subgroup_generators": lifted,
            "actual_known_controlled_R_calls": N+coverage["included_original_inputs"]+M,
            "actual_original_copies_consumed": N+M,
            "first_128_observed_labels": first_labels,
            "status": "MEASUREMENT_RECORD_DECODED_NOT_INDEPENDENTLY_CERTIFIED",
            "uniform_control_flow_uses_hidden_source_parameters": False,
            "measurement_backend_is_scalable_hardware_execution": False,
            "source_IID_and_known_R_contract_verified_from_outcomes_alone": False}


def calibration_character_frames(chart, tau_a, tau_b, fixed_axes, source_kind):
    active, inactive = SpanAccumulator(chart.dimension), SpanAccumulator(chart.dimension)
    basis_elements = [chart.section(tuple(int(i == j) for i in range(chart.dimension))) for j in range(chart.dimension)]
    for j in range(chart.extension.k):
        if j not in fixed_axes:
            active.add(tuple((z[j]-tau_a[j]*x[0]-tau_b[j]*x[1]) % 3 for x, z in basis_elements))
    if source_kind == "nonnormal-line":
        arow = tuple(x[0] for x, _ in basis_elements)
        active.add(arow)
        inactive.add(arow)
    return tuple(active.rows), tuple(inactive.rows)


class CalibrationBackend:
    """Closed laws of specified X/Z/clock measurements, NOT an oracle input."""
    def __init__(self, k, source_kind, seed, fixed_axes, skew, count):
        self.k, self.kind, self.fixed, self.skew = k, source_kind, fixed_axes, skew
        self.tau_b = tuple((j+1) % 3 for j in range(k))
        self.tau_a = tuple((2*j+1) % 3 for j in range(k)) if source_kind == "nonabelian-preimage" else (0,)*k
        self.stream = iter(label_stream(seed, count, k, fixed_axes, skew))
        self.rng = np.random.default_rng(seed+1)
        self.centre_calls, self.original_calls = 0, 0
        self.live, self.frames = {}, None

    def measure_centre(self, index):
        if index != self.centre_calls:
            raise ValueError("fresh consecutive original centre input required")
        lam = next(self.stream)
        self.centre_calls += 1
        self.live[index] = lam
        return lam

    def measure_block(self, block):
        for index, lam in zip(block["original_indices"], block["central_characters"]):
            if self.live.pop(index, None) != lam:
                raise ValueError("conditional register reused, missing or mislabeled")
        return (int(self.rng.integers(0, 3)), 0) if self.kind == "nonnormal-line" else (0, 0)

    def measure_original(self, chart, index):
        if index != self.centre_calls+self.original_calls:
            raise ValueError("final sample must use a fresh original input")
        self.original_calls += 1
        if self.frames is None:
            self.frames = calibration_character_frames(chart, self.tau_a, self.tau_b, self.fixed, self.kind)
        # The skewed source is a mixture, not a uniform annihilator law.
        frame = self.frames[0 if self.rng.random() < float(self.skew) else 1]
        c = tuple(int(a) for a in self.rng.integers(0, 3, size=len(frame)))
        return combine(frame, c, chart.dimension)


def affine_solution(rows, rhs, width):
    if len(rows) != len(rhs):
        raise ValueError("one field right-hand side per equation required")
    augmented = tuple(word(row, width, 3)+(word((b,), 1, 3)[0],) for row, b in zip(rows, rhs))
    if not augmented:
        return (0,)*width
    reduced, r = nmod_mat(augmented, 3).rref()
    out = [0]*width
    for i in range(r):
        row = tuple(int(reduced[i, j]) for j in range(width+1))
        pivot = next(j for j, a in enumerate(row) if a)
        if pivot == width:
            raise ValueError("inconsistent basis readout equations")
        out[pivot] = row[-1]
    return tuple(out)


def basis_readout_baseline(k, kind, seed, fixed_axes, skew, count, tau_a, tau_b):
    """Alternative measurements on fresh counterfactual copies, not reused ones."""
    labels = list(label_stream(seed, count, k, fixed_axes, skew))
    clock = tuple(-dot(lam, tau_b) % 3 for lam in labels)
    fourier = tuple(dot(lam, tau_a) % 3 for lam in labels) if kind == "nonabelian-preimage" else None
    recovered_b = affine_solution(labels, tuple(-j % 3 for j in clock), k)
    recovered_a = affine_solution(labels, fourier, k) if fourier is not None else (0,)*k
    Z = nullspace(labels, k)
    difference_b = tuple((a-b) % 3 for a, b in zip(recovered_b, tau_b))
    difference_a = tuple((a-b) % 3 for a, b in zip(recovered_a, tau_a))
    actual_Z = tuple(tuple(int(i == j) for i in range(k)) for j in fixed_axes)
    exact = len(Z) == len(actual_Z) and all(span_contains(actual_Z, z) for z in Z)
    exact = exact and span_contains(Z, difference_b) and span_contains(Z, difference_a)
    return {"status": "SOURCE_SPECIFIC_BASIS_READOUT_RECOVERED" if exact else "SOURCE_SPECIFIC_BASELINE_FAILED",
            "alternative_fresh_copy_count": count, "central_label_rows": labels,
            "clock_computational_basis_outcomes": clock, "first_qutrit_Fourier_basis_indices": fourier,
            "recovered_tau_a_mod_fixed_centre": recovered_a, "recovered_tau_b_mod_fixed_centre": recovered_b,
            "learned_fixed_centre_basis": Z,
            "classical_postprocessing": "affine F3 linear solve, no collective receiver",
            "uses_known_single_register_basis_measurements": True,
            "classical_sample_access_to_unknown_quantum_state_assumed_free": False,
            "copies_shared_with_collective_receiver": False,
            "baseline_establishes_general_StateHSP_classical_algorithm": False}


def calibration_receiver(k, source_kind="nonnormal-line", seed=33151, fixed_axes=(), skew=Fraction(1), failure_bits=4):
    """Full capped protocol on transparent, classically easy StateHSP controls."""
    G = rank_one_extension(k)
    if source_kind not in ("nonnormal-line", "nonabelian-preimage"):
        raise ValueError("declared calibration source required")
    if source_kind == "nonabelian-preimage" and 0 not in fixed_axes:
        raise ValueError("this source fixes the cocycle-image central coordinate")
    if not isinstance(skew, Fraction) or not 0 < skew <= 1:
        raise ValueError("exact positive spectrum mixture weight required")
    if any(type(j) is not int or not 0 <= j < k for j in fixed_axes) or len(set(fixed_axes)) != len(fixed_axes):
        raise ValueError("canonical distinct fixed central axes required")
    ledger = resource_ledger(2, k, skew, failure_bits)
    backend = CalibrationBackend(k, source_kind, seed, fixed_axes, skew, ledger["original_central_measurement_count"])
    record = receive(G, skew, failure_bits, backend)
    chart_data = record["quotient_chart"]
    chart = G.quotient_chart(chart_data["quotient_frame"], chart_data["central_fixed_frame"])
    actual_Z = tuple(tuple(int(i == j) for i in range(k)) for j in fixed_axes)
    if len(chart.central_fixed_frame) != len(actual_Z) or any(not span_contains(actual_Z, z) for z in chart.central_fixed_frame):
        raise ArithmeticError("learned centre does not equal true calibration fixed centre")
    expected_kernel = nullspace(backend.frames[0], chart.dimension)
    final_kernel = record["final_kernel_basis"]
    if len(final_kernel) != len(expected_kernel) or any(not span_contains(expected_kernel, v) for v in final_kernel):
        raise ArithmeticError("capped original-state measurement failed on the declared mixture")
    expected_dimension = len(actual_Z)+(1 if source_kind == "nonnormal-line" else 2)
    if len(record["lifted_subgroup_generators"]) != expected_dimension:
        raise ArithmeticError("fixed central generators were lost in the lift")
    baseline = basis_readout_baseline(k, source_kind, seed+71, fixed_axes, skew,
                                     ledger["fresh_original_final_copy_count"], backend.tau_a, backend.tau_b)
    record.update({"source_kind": source_kind, "seed": seed,
            "calibration_tau_a": backend.tau_a, "calibration_tau_b": backend.tau_b, "fixed_central_axes": fixed_axes,
            "spectrum_uniform_mixture_weight": str(skew),
            "final_law_active_uniform_character_frame": backend.frames[0],
            "final_law_inactive_uniform_character_frame": backend.frames[1],
            "basis_readout_baseline": baseline,
            "status": "FULL_BUDGET_REFERENCE_RECOVERED",
            "native_DHSP_source_bridge_supplied": False,
            "calibration_has_polynomial_basis_readout_baseline": True,
            "quantum_advantage_inferred_from_calibration": False,
            "hidden_parameters_or_density_tables_are_quantum_algorithm_inputs": False})
    return record


def original_final_control(record):
    """Literal ALL-branch final experiment on fresh ORIGINAL mixed copies."""
    k, kind = record["ledger"]["centre_dimension"], record["source_kind"]
    G = rank_one_extension(k)
    c = record["quotient_chart"]
    chart = G.quotient_chart(c["quotient_frame"], c["central_fixed_frame"])
    if k > 3 or chart.dimension > 4:
        raise ValueError("literal final-law calibration is bounded, not scalable input preparation")
    skew = Fraction(record["spectrum_uniform_mixture_weight"])
    labels = [v for v in words(k, 3) if all(v[j] == 0 for j in record["fixed_central_axes"])]
    points = words(chart.dimension, 3)
    original_moments, literal = np.zeros(len(points), complex), np.zeros(len(points))
    F = character_matrix(points, 3)/len(points)
    for label in labels:
        weight = float(skew)/len(labels)+(float(1-skew) if not any(label) else 0)
        coeff, phase = calibration_amplitude(label, record["calibration_tau_a"], record["calibration_tau_b"], kind)
        v = np.array(coeff)*np.exp(2j*np.pi*np.array(phase)/3)
        v /= np.linalg.norm(v)
        outputs = np.stack([conditional_action(label, chart.section(t)) @ v for t in points])
        original_moments += weight*np.array([np.vdot(v, out) for out in outputs])
        literal += weight*np.sum(abs(F @ outputs)**2, axis=1)
    law = probabilities_from_moments(original_moments, points, 3)
    active, inactive = record["final_law_active_uniform_character_frame"], record["final_law_inactive_uniform_character_frame"]
    exact_law = [skew/Fraction(3**len(active)) if span_contains(active, y) else Fraction(0) for y in points]
    exact_law = [p+((1-skew)/Fraction(3**len(inactive)) if span_contains(inactive, y) else 0) for p, y in zip(exact_law, points)]
    if max(abs(literal-law)) > 2e-11 or max(abs(law-np.array([float(p) for p in exact_law]))) > 2e-11:
        raise ArithmeticError("original mixed-source Kraus law disagrees with the recorded mixture")
    return {"source_kind": kind, "full_character_words": points,
            "literal_Kraus_probabilities": literal.tolist(), "original_moment_Fourier_probabilities": law.tolist(),
            "exact_mixture_probabilities": [str(p) for p in exact_law],
            "uses_fresh_original_copies_not_selected_conditional_states": True,
            "all_outcomes_retained": True, "large_density_table_is_algorithm_input": False}


def run_controls():
    diag = lambda t: np.diag(t)
    instruments = [mixed_sector_instrument(((1,), (2,)), (diag([1., 0., 0.]), diag([0., 1., 0.]))),
                   mixed_sector_instrument(((0,), (1,), (2,)), (np.eye(3)/3, diag([.5, .25, .25]), diag([.25, .5, .25]))),
                   mixed_sector_instrument(((1,), (2,)), (diag([1-2/3/2**40, 1/3/2**40, 1/3/2**40]), np.eye(3)/3))]
    rng = np.random.default_rng(90551)
    for _ in range(2):
        states = []
        for _ in range(2):
            a = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
            rho = a @ a.conj().T
            states.append(rho/np.trace(rho))
        instruments.append(mixed_sector_instrument(((1,), (2,)), states))
    source_specs = [(2, "nonnormal-line", (), Fraction(1)),
                    (2, "nonnormal-line", (1,), Fraction(1)),
                    (2, "nonabelian-preimage", (0,), Fraction(1)),
                    (3, "nonabelian-preimage", (0, 2), Fraction(1)),
                    (2, "nonnormal-line", (), Fraction(1, 4))]
    runs = [calibration_receiver(k, kind, 33151+i, fixed, skew) for i, (k, kind, fixed, skew) in enumerate(source_specs)]
    for r in runs:
        r["literal_final_original_instrument"] = original_final_control(r)
    vector_controls = []
    for labels in (((1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1))):
        data = [calibration_amplitude(lam, (0, 0), (1, 2), "nonnormal-line") for lam in labels]
        vector_controls.append(exact_vector_control(labels, [c for c, _ in data], [t for _, t in data]))
    labels = ((0, 1, 1), (0, 2, 2))
    data = [calibration_amplitude(lam, (2, 1, 0), (1, 2, 0), "nonabelian-preimage") for lam in labels]
    vector_controls.append(exact_vector_control(labels, [c for c, _ in data], [t for _, t in data]))
    for labels in (((1, 2), (2, 1)), ((0, 1), (1, 1), (2, 1))):
        vector_controls.append(exact_vector_control(labels, rng.integers(-2, 3, size=(len(labels), 9)).tolist()))
    large = ZeroSumBuffer(12, retain_blocks=True)
    labels = list(label_stream(90437, 1024, 12))
    for lam in labels:
        large.push(lam)
    pool = large.finish()
    pool.update({"seed": 90437, "complete_original_characters": labels,
                 "distinct_label_count": len(set(labels)),
                 "largest_identical_sector_bucket": max(Counter(labels).values()),
                 "full_confidence_copy_ledger_met_by_this_pool": False,
                 "large_pool_is_a_coverage_control_not_an_algorithm_scaling_claim": True})
    return {"status": "VECTOR_CENTRE_HETEROGENEOUS_STATE_HSP_RECEIVER_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "literal_heterogeneous_instruments": instruments, "full_budget_reference_receivers": runs,
            "exact_two_qutrit_heterogeneous_instruments": vector_controls,
            "large_distinct_sector_coverage_control": pool,
            "growing_integer_resource_ledgers": [resource_ledger(d, k, Fraction(1, 4), 32) for d, k in ((8, 8), (32, 32), (128, 128), (512, 512))],
            "uniform_quantum_recipe_specified": True,
            "all_central_extensions_or_higher_nilpotency_solved": False,
            "new_classical_HSP_speedup_claimed": False, "candidate_record_accepted": False,
            "novelty_claimed": False, "Shor_level_result_claimed": False,
            "native_DHSP_or_CCP_receiver_compiled": False,
            "routine_CLI_registry_UI_and_Git_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "full_budget_receivers": len(report["full_budget_reference_receivers"]),
                      "total_original_copies_in_reference_runs": sum(r["actual_original_copies_consumed"] for r in report["full_budget_reference_receivers"])}, indent=2))


if __name__ == "__main__":
    main()

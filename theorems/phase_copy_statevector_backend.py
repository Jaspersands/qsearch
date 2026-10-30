"""Finite state-vector simulation backend for polynomial-phase copy learning.

Test and demonstration backend ONLY. The physical controller receives only
opaque handles and public outcomes. Hidden parameters exist ONLY in this file.
"""
from __future__ import annotations

import math
import random
from typing import Sequence

import numpy as np

from theorems.affine_phase_erasure import PhasePacket, merge_branch, monomials
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _canonical


def _poly_val(indices, coeffs, point, p):
    total = 0
    for alpha, c in zip(indices, coeffs):
        if not c:
            continue
        term = c
        for x, a in zip(point, alpha):
            if a:
                term = (term * pow(x, a, p)) % p
        total = (total + term) % p
    return total


class StateVectorPhaseSource:
    """Simulates an opaque physical source of unknown polynomial-phase states.

    Maintains states in memory keyed by opaque integer handle IDs.
    Hidden coefficients are kept private to this backend.
    """

    def __init__(
        self,
        p: int,
        width: int,
        degree: int,
        hidden_coefficients: Sequence[int],
        *,
        rng: random.Random | None = None,
        cap: int | None = None,
        fourier_convention: int = 1,
        physical_qft_sign: int | None = None,
    ):
        ring(p)
        if type(width) is not int or width < 1:
            raise ValueError("positive width required")
        if type(degree) is not int or not 1 <= degree < p:
            raise ValueError("degree in [1, p-1] required")
        if fourier_convention not in (1, -1):
            raise ValueError("fourier_convention must be +1 or -1")
        if physical_qft_sign is None:
            physical_qft_sign = fourier_convention
        if physical_qft_sign not in (1, -1):
            raise ValueError("physical_qft_sign must be +1 or -1")

        self.p = p
        self.width = width
        self.degree = degree
        self.indices = tuple(a for a in monomials(width, degree) if any(a))
        _canonical(hidden_coefficients, len(self.indices), p)
        self._hidden = tuple(hidden_coefficients)
        self.rng = rng if rng is not None else random.Random()
        self.cap = cap
        self._fourier_convention = fourier_convention
        self._physical_qft_sign = physical_qft_sign

        self.draw_count = 0
        self._next_handle_id = 1
        # handle_id -> dict[tuple[int, ...], complex] (sparse state representation)
        self._states: dict[int, dict[tuple[int, ...], complex]] = {}
        self._handle_axis: dict[int, int | None] = {}
        self._consumed: set[int] = set()

    @property
    def fourier_convention(self) -> int:
        return self._fourier_convention

    def _fresh_handle(self, state: dict[tuple[int, ...], complex] | None, axis: int | None = None) -> int:
        hid = self._next_handle_id
        self._next_handle_id += 1
        self._states[hid] = state
        self._handle_axis[hid] = axis
        return hid

    def _consume_handle_with_axis(
        self, handle_id: int
    ) -> tuple[dict[tuple[int, ...], complex] | None, int | None]:
        if handle_id in self._consumed:
            raise ValueError(f"handle {handle_id} has already been consumed (state reuse violation)")
        if handle_id not in self._states:
            raise ValueError(f"handle {handle_id} is unknown or invalid")
        state = self._states.pop(handle_id)
        axis = self._handle_axis.pop(handle_id, None)
        self._consumed.add(handle_id)
        return state, axis

    def _consume_handle(self, handle_id: int) -> dict[tuple[int, ...], complex] | None:
        state, _ = self._consume_handle_with_axis(handle_id)
        return state

    def draw(self) -> int:
        """Draw one fresh original copy from the source. Consumes 1 against cap."""
        from theorems.polynomial_phase_copy_learning import SourceCapExhausted
        if self.cap is not None and self.draw_count >= self.cap:
            raise SourceCapExhausted(f"source draw cap of {self.cap} exhausted")
        self.draw_count += 1
        # We record handle with marker None indicating fresh full-domain copy
        hid = self._next_handle_id
        self._next_handle_id += 1
        self._states[hid] = None  # Full-domain fresh copy
        self._handle_axis[hid] = None
        return hid

    def measure_all_but(self, handle_id: int, axis: int) -> tuple[tuple[int, ...], int]:
        """Measure all coordinates except axis.

        Consumes handle_id.
        Returns (observed_coordinates, new_handle_id).
        """
        if type(axis) is not int or not 0 <= axis < self.width:
            raise ValueError(f"invalid axis {axis}")
        state, prev_axis = self._consume_handle_with_axis(handle_id)
        if state is not None or prev_axis is not None:
            raise ValueError("measure_all_but requires a fresh unmeasured full-domain copy")

        # The full-domain state has uniform amplitudes, so the marginal distribution
        # of measuring all coordinates except axis is strictly uniform over F_p^(width-1).
        observed = tuple(self.rng.randrange(self.p) for _ in range(self.width - 1))

        # Build post-measurement state on coordinate axis:
        # |t> has phase exp(2pi i * F(point) / p) / sqrt(p).
        slice_state = {}
        sqrt_p = math.sqrt(self.p)
        for t in range(self.p):
            point = observed[:axis] + (t,) + observed[axis:]
            val = _poly_val(self.indices, self._hidden, point, self.p)
            slice_state[(t,)] = np.exp(2j * np.pi * val / self.p) / sqrt_p

        new_hid = self._fresh_handle(slice_state, axis=axis)
        return observed, new_hid

    def apply_known_phase(self, handle_id: int, correction: tuple[int, ...]) -> int:
        r"""Apply diagonal public phase correction: \omega^{-\sum_{r=0}^d c_r t^r}.

        Consumes handle_id and returns new_handle_id.
        """
        state, axis = self._consume_handle_with_axis(handle_id)
        if not state:
            raise ValueError("cannot apply phase to empty state")
        new_state = {}
        for (t,), amp in state.items():
            corr_val = sum(c * pow(t, r, self.p) for r, c in enumerate(correction)) % self.p
            phase = np.exp(-2j * np.pi * corr_val / self.p)
            new_state[(t,)] = amp * phase
        return self._fresh_handle(new_state, axis=axis)

    def shear_merge(
        self,
        handle_ids: Sequence[int],
        scales: Sequence[int],
    ) -> tuple[tuple[tuple[int], ...], int]:
        """Perform public shear merge with given scales.

        Consumes ALL handle_ids.
        Zero-scale handles are discarded (consumed).
        Returns (outcomes, new_handle_id).
        """
        if len(handle_ids) != len(scales):
            raise ValueError("handle_ids and scales must have matching length")
        _canonical(scales, len(scales), self.p)
        if not any(scales):
            raise ValueError("at least one scale must be nonzero")

        consumed = [self._consume_handle_with_axis(hid) for hid in handle_ids]
        states = [c[0] for c in consumed]
        axes = [c[1] for c in consumed]
        if any(a is None for a in axes) or len(set(axes)) != 1:
            raise ValueError("cannot merge handles from different coordinate axes")
        merged_axis = axes[0]

        fresh = (self.rng.randrange(self.p),)
        outcomes = []
        for state, c in zip(states, scales):
            if not c:
                outcomes.append((0,))
                continue
            q = self.rng.choice(tuple(state))
            outcomes.append(((q[0] - c * fresh[0]) % self.p,))

        merged_state, prob = merge_branch(self.p, states, scales, outcomes)
        new_hid = self._fresh_handle(merged_state, axis=merged_axis)
        return tuple(outcomes), new_hid

    def fourier_measure(self, handle_id: int) -> int:
        """Measure univariate state in the Fourier basis. Consumes handle_id."""
        state, axis = self._consume_handle_with_axis(handle_id)
        if not state:
            raise ValueError("cannot measure empty state")
        vec = np.zeros(self.p, dtype=complex)
        for (t,), amp in state.items():
            vec[t] = amp
        # Standard QFT: \hat{a}_k = 1/sqrt(p) \sum_t a_t exp(-2pi i k t / p)
        transformed = np.fft.fft(vec) / math.sqrt(self.p)
        probs = np.abs(transformed) ** 2
        total_p = np.sum(probs)
        if total_p < 1e-12:
            raise ValueError("state has vanishing norm in Fourier basis")
        probs = probs / total_p
        k = int(self.rng.choices(range(self.p), weights=probs)[0])
        return (k * self._physical_qft_sign) % self.p

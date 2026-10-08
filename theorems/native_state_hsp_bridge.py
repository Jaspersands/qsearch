"""Exact native sample-to-StateHSP bridge and fixed-class transfer ceiling.

Known cyclotomic coset inputs only, not an invented oracle problem. This
does not compile a growing-class receiver or certify a new speedup.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from flint import fmpz_poly
import numpy as np
from sympy import Poly, cyclotomic_poly, symbols

from cyclotomic_rescaling_gate import ideal_chart, multiply, pairing, plus, reduce_element
from cyclic_centre_state_hsp_receiver import integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/reductions/native_state_hsp_bridge.json"


@dataclass(frozen=True)
class NativeGroup:
    level: int
    dimension: int = 1

    def __post_init__(self):
        integer(self.level, "native level", 1)
        integer(self.dimension, "native vector dimension", 1)
        if self.level > 512:
            raise ValueError("existing exact ring API is capped at level512")

    def vector(self, v):
        if not isinstance(v, (tuple, list)) or len(v) != self.dimension:
            raise ValueError("declared native vector dimension required")
        return tuple(reduce_element(tuple(a), self.level) for a in v)

    def rotate(self, v, t):
        root = ((1, 0), (0, 1), (-1, -1))[t % 3]
        return tuple(multiply(a, root, self.level) for a in self.vector(v))

    def element(self, g):
        v, t = g
        if type(t) is not int or t not in (0, 1, 2):
            raise ValueError("canonical cyclotomic rotation digit required")
        return self.vector(v), t

    def compose(self, g, h):
        x, t = self.element(g)
        y, u = self.element(h)
        y = self.rotate(y, t)
        return tuple(plus(a, b, self.level) for a, b in zip(x, y)), (t+u) % 3

    def hidden_elements(self, secret):
        secret = self.vector(secret)
        lambdas = ((0, 0), (1, 0), (1, 1))
        return tuple((tuple(multiply((-a[0], -a[1]), lam, self.level) for a in secret), t) for t, lam in enumerate(lambdas))

    def induced_action(self, label, g):
        label = self.vector(label)
        b, t = self.element(g)
        R = np.zeros((3, 3), complex)
        for j in range(3):
            out = (j-t) % 3
            phase = sum((pairing(a, v, self.level) for a, v in zip(label, self.rotate(b, out))), Fraction()) % 1
            R[out, j] = np.exp(2j*np.pi*float(phase))
        return R

    def supplied_phase_state(self, label, secret):
        label, secret = self.vector(label), self.vector(secret)
        values = []
        for lam in ((0, 0), (1, 0), (1, 1)):
            phase = sum((pairing(a, multiply(s, lam, self.level), self.level) for a, s in zip(label, secret)), Fraction()) % 1
            values.append(np.exp(2j*np.pi*float(phase))/np.sqrt(3))
        return np.array(values)

    def class_two_coordinates(self, g):
        if self.level != 2:
            raise ValueError("exponent-three bilinear chart only at native level2")
        v, t = self.element(g)
        return tuple((a+b) % 3 for a, b in v)+(t,), tuple(b % 3 for _, b in v)


def ring_words(level):
    if level > 4:
        raise ValueError("full ring enumeration is finite calibration only")
    h0, _, h1 = ideal_chart(level)[0]
    return tuple(product(range(h0), range(h1)))


def class_ceiling(level, dimension, target_class):
    integer(level, "native level", 1)
    integer(dimension, "native vector dimension", 1)
    integer(target_class, "target nilpotency class", 1)
    c = min(level, target_class)
    digits = (level+1)//2
    kept = min(digits, (c+1)//2)
    return {"native_level": level, "native_dimension": dimension,
            "target_class_bound": target_class, "native_nilpotency_class": level,
            "lower_central_kernel_contains": f"pi^{target_class} A",
            "all_group_homomorphisms_into_class_bounded_targets_share_this_kernel": True,
            "full_ring_secret_fibre_count": {"base": 3, "exponent": dimension*(level-c)},
            "integer_embedded_secret_fibre_count": {"base": 3, "exponent": dimension*(digits-kept)},
            "integer_secret_trits_per_coordinate": digits,
            "maximum_integer_secret_trits_retained_per_coordinate": kept,
            "secret_guesses_needed_from_uniform_prior_if_ONLY_quotient_outputs_used": {"base": 3, "exponent": dimension*(digits-kept)},
            "bound_applies_to_arbitrary_quantum_state_conversions": False,
            "bound_applies_to_adaptive_nonhomomorphic_receivers": False,
            "higher_class_receiver_supplied": False}


def exact_original_overlap_control(level, secret):
    """Integer cyclotomic reduction of EVERY original mixed-state expectation."""
    G = NativeGroup(level)
    secret = G.vector((secret,))
    labels = ring_words(level)
    q = 3**((level+1)//2)
    x = symbols("x")
    Phi = fmpz_poly([int(a) for a in reversed(Poly(cyclotomic_poly(q, x), x).all_coeffs())])
    denominator = 3*len(labels)
    hidden = set(G.hidden_elements(secret))
    exact_nonzero = []
    maximum_matrix_error = 0.
    for b, t in product(labels, range(3)):
        lam = ((0, 0), (1, 0), (1, 1))[t]
        residual = plus(b, multiply(secret[0], lam, level), level)
        counts = [0]*q
        matrix_total = 0j
        for a in labels:
            for j in range(3):
                v = G.rotate((residual,), j)[0]
                f = pairing(a, v, level)*q
                if f.denominator != 1:
                    raise ArithmeticError("exact native character root exceeds declared modulus")
                counts[int(f) % q] += 1
            psi = G.supplied_phase_state((a,), secret)
            matrix_total += np.vdot(psi, G.induced_action((a,), ((b,), t)) @ psi)/len(labels)
        expected = int(((b,), t) in hidden)
        reduced = fmpz_poly(counts) % Phi
        if reduced != fmpz_poly([denominator*expected]):
            raise ArithmeticError("original native source lacks the asserted StateHSP gap")
        maximum_matrix_error = max(maximum_matrix_error, abs(matrix_total-expected))
        if expected:
            exact_nonzero.append(((b,), t))
    if maximum_matrix_error > 2e-11:
        raise ArithmeticError("literal induced representation disagrees with exact overlap")
    return {"level": level, "native_secret": secret, "native_label_count": len(labels),
            "every_group_element_checked": 3*len(labels), "character_root_modulus": q,
            "exact_original_Bose_subgroup": exact_nonzero,
            "original_absolute_overlap_gap": "1", "maximum_literal_matrix_error": maximum_matrix_error,
            "original_density_is_uniform_classical_labels_and_actual_supplied_qutrits": True,
            "known_representation_depends_on_hidden_secret": False,
            "full_coherent_graph_state_or_unknown_inverse_used": False,
            "bounded_matrix_replay_is_scalable_receiver": False}


def central_descent_control(level, secret=(2, 1)):
    """Actual native conditional overlaps; no conditional-gap oracle premise."""
    if not 2 <= level <= 4:
        raise ValueError("conditional full-table replay is bounded to native levels2-4")
    G = NativeGroup(level)
    labels, q = ring_words(level), 3**((level+1)//2)
    central = (1, 0)
    for _ in range(level-1):
        central = multiply(central, (-1, 1), level)
    buckets = {i: [] for i in range(3)}
    for a in labels:
        f = pairing(a, central, level)*3
        if f.denominator != 1:
            raise ArithmeticError("designated centre does not have order three")
        buckets[int(f) % 3].append(a)
    if set(map(len, buckets.values())) != {len(labels)//3}:
        raise ArithmeticError("uniform original source does not give uniform central characters")
    zvalues = {multiply(central, (u, 0), level): u for u in range(3)}
    supports = ((0,), (1, 2), (1, 1, 1), (2, 2, 2), (0, 1, 2))
    x = symbols("x")
    Phi = fmpz_poly([int(a) for a in reversed(Poly(cyclotomic_poly(q, x), x).all_coeffs())])
    maximum_error, survivors = 0., 0
    for b, t in product(labels, range(3)):
        residual = plus(b, multiply(secret, ((0, 0), (1, 0), (1, 1))[t], level), level)
        u = zvalues.get(residual)
        mu = []
        for lam in range(3):
            counts, actual = [0]*q, 0j
            for a in buckets[lam]:
                for j in range(3):
                    exponent = pairing(a, G.rotate((residual,), j)[0], level)*q
                    counts[int(exponent) % q] += 1
                psi = G.supplied_phase_state((a,), (secret,))
                actual += np.vdot(psi, G.induced_action((a,), ((b,), t)) @ psi)/len(buckets[lam])
            expected = 0j if u is None else np.exp(2j*np.pi*(lam*u % 3)/3)
            target = [0]*q
            if u is not None:
                target[(lam*u % 3)*(q//3)] = 3*len(buckets[lam])
            if fmpz_poly(counts) % Phi != fmpz_poly(target) % Phi:
                raise ArithmeticError("native conditional overlap does not equal the central coset phase")
            maximum_error = max(maximum_error, abs(actual-expected))
            mu.append(actual)
        for block in supports:
            if abs(np.prod([mu[lam] for lam in block])-int(u is not None)) > 2e-11:
                raise ArithmeticError("heterogeneous central zero sum loses the exact quotient gap")
        survivors += int(u is not None)
    return {"level": level, "native_secret": secret, "central_generator": central,
            "central_character_bucket_sizes": [len(buckets[i]) for i in range(3)],
            "tested_nonempty_zero_sum_blocks": supports, "every_group_element_checked": 3*len(labels),
            "group_elements_in_hidden_subgroup_times_designated_centre": survivors,
            "maximum_literal_conditional_error": maximum_error,
            "exact_quotient_Bose_gap_after_fresh_window_zero_sum": "1",
            "fresh_independent_windows_give_IID_output_sources": True,
            "adaptive_recycled_outputs_claimed_IID": False,
            "quotient_group_is_abelian": level == 2,
            "polynomial_growing_depth_copy_recurrence_proved": False}


def run_controls():
    controls = [exact_original_overlap_control(r, s) for r in range(1, 5) for s in ((1, 0), (0, 1), (2, 1))]
    G = NativeGroup(4)
    label = ((1, 0),)
    left, right = ((0, 0),), ((3, 0),)
    fidelity = float(abs(np.vdot(G.supplied_phase_state(label, left), G.supplied_phase_state(label, right)))**2)
    # These inputs have the SAME class-two image but distinguishable phase states.
    if reduce_element((3, 0), 2) != (0, 0) or fidelity >= 1-1e-12:
        raise ArithmeticError("fixed-class projection countercontrol failed")
    return {"status": "NATIVE_COPY_ONLY_STATE_HSP_SOURCE_BRIDGE_AND_FIXED_CLASS_CEILING_REVIEW_PENDING",
            "exact_original_source_controls": controls,
            "exact_central_descent_controls": [central_descent_control(r) for r in range(2, 5)],
            "growing_class_transfer_ledgers": [class_ceiling(r, n, 2) for r, n in ((2, 1), (4, 1), (8, 8), (32, 32), (128, 128))],
            "homomorphic_projection_loss_countercontrol": {"level": 4, "target_class": 2,
                "integer_secrets": [0, 3], "same_projected_secret": True, "label": label,
                "conditional_phase_state_fidelity": fidelity,
                "quantum_sample_information_destroyed_by_ALL_transformations": False},
            "existing_vector_centre_receiver_applies_at_level2": True,
            "growing_native_nilpotency_class_handled": False,
            "new_native_receiver_or_classical_speedup_supplied": False,
            "novelty_claimed": False, "Shor_level_result_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(r, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": r["status"], "source_controls": len(r["exact_original_source_controls"]),
                      "full_depth_receiver_supplied": False}))


if __name__ == "__main__":
    main()

"""Costed native-copy orbit source and relative-inverse amplification audit.

LOCAL DERIVATION / REVIEW PENDING. Known relative preparation is reversible,
but does not provide a fixed-purification creation/reflection oracle. No new
full-depth receiver, exact nilpotent algorithm or speedup is asserted.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

import numpy as np

from cyclotomic_rescaling_gate import reduce_element
from cyclic_centre_state_hsp_receiver import integer
from native_state_hsp_bridge import NativeGroup, ring_words

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/reductions/native_orbit_source_access.json"


def inverse(G, g):
    b, t = G.element(g)
    return tuple(reduce_element((-a[0], -a[1]), G.level) for a in G.rotate(b, -t)), (-t) % 3


def relative_orbit_reflection(V, state):
    return 2*V @ (V.conj().T @ state)-state


def label_filter(P, state, group_size, seed_dimension):
    v = state.reshape(group_size, seed_dimension, -1)
    return np.einsum("hg,gie->hie", P, v).reshape(group_size*seed_dimension, -1)


def norm_squared(state):
    return float(np.vdot(state, state).real)


def native_fourier_filters(G, elements):
    """Complete known irreplabel controls at levels1-2, not a general QFT."""
    if G.level not in (1, 2) or G.dimension != 1:
        raise ValueError("complete Fourier partition is calibrated only at n1 levels1-2")
    N = len(elements)
    filters = []
    for u, v in product(range(3), repeat=2):
        characters = np.array([np.exp(2j*np.pi*((u*(b[0][0]+b[0][1])+v*t) % 3)/3) for b, t in elements])
        filters.append(({"kind": "one_dimensional", "parameters": (u, v), "irrep_dimension": 1}, np.outer(characters, characters.conj())/N))
    if G.level == 2:
        indices = {g: i for i, g in enumerate(elements)}
        for lam in (1, 2):
            P = np.zeros((N, N), complex)
            for z in range(3):
                centre = (((-z, z),), 0)
                for i, g in enumerate(elements):
                    h = G.compose(g, inverse(G, centre))
                    P[indices[h], i] += np.exp(-2j*np.pi*(lam*z % 3)/3)/3
            filters.append(({"kind": "three_dimensional_central", "parameters": (lam,), "irrep_dimension": 3}, P))
    if np.linalg.norm(sum(P for _, P in filters)-np.eye(N)) > 2e-11:
        raise ArithmeticError("complete native Fourier-label projectors do not partition the group register")
    return filters


def source_recipe(level, dimension):
    integer(level, "native level", 1)
    integer(dimension, "secret dimension", 1)
    return {"native_level": level, "native_dimension": dimension,
            "group_order": {"base": 3, "exponent": level*dimension+1},
            "one_original_IID_native_copy_consumed_per_output": True,
            "group_coordinate_trits": level*dimension+1,
            "known_controlled_R_calls_per_orbit_source": 1,
            "relative_inverse_known_controlled_R_calls": 1,
            "recipe": ["Prepare uniform PUBLIC native group coordinates.",
                       "Apply the known induced R(g), controlled by the group register and observed source label.",
                       "Discard the original input registers to obtain an ordinary coset mixed state."],
            "controlled_R_phase_arithmetic_depends_on_secret": False,
            "forward_and_inverse_relative_preparation_are_known": True,
            "relative_inverse_returns_unknown_input_not_a_known_blank": True,
            "fixed_purification_preparation_oracle_supplied": False,
            "unknown_input_or_purification_reflection_supplied": False,
            "original_exact_subgroup_indicator_required_for_uniform_coset_state": True,
            "fresh_outputs_are_IID_before_conditioning_on_hidden_or_full_label_transcripts": True,
            "source_noise_and_gate_precision_certificate_supplied": False,
            "growing_class_solver_supplied": False}


@dataclass(frozen=True)
class OrbitControl:
    level: int
    secret: tuple

    def __post_init__(self):
        integer(self.level, "native level", 1)
        NativeGroup(self.level).vector((self.secret,))

    def matrices(self):
        if self.level not in (1, 2):
            raise ValueError("complete native orbit matrices are calibrated only at levels1-2")
        G = NativeGroup(self.level)
        secret = G.vector((self.secret,))
        labels = ring_words(self.level)
        elements = tuple(((b,), t) for b, t in product(labels, range(3)))
        N, D, E = len(elements), 3*len(labels), len(labels)
        omega = np.zeros((D, E), complex)
        for i, a in enumerate(labels):
            omega[3*i:3*i+3, i] = G.supplied_phase_state((a,), secret)/np.sqrt(E)
        V = np.zeros((N*D, D), complex)
        for ig, g in enumerate(elements):
            for i, a in enumerate(labels):
                V[ig*D+3*i:ig*D+3*i+3, 3*i:3*i+3] = G.induced_action((a,), g)/np.sqrt(N)
        if np.max(abs(V.conj().T @ V-np.eye(D))) > 2e-11:
            raise ArithmeticError("relative orbit preparation is not an isometry")
        prepared = V @ omega
        group_density = np.einsum("gie,hie->gh", prepared.reshape(N, D, E), prepared.reshape(N, D, E).conj())
        H = set(G.hidden_elements(secret))
        target = np.array([[int(G.compose(inverse(G, h), g) in H)/N for h in elements] for g in elements], complex)
        if np.max(abs(group_density-target)) > 2e-11:
            raise ArithmeticError("actual copy-to-coset orbit source does not have the promised density")
        return G, labels, elements, V, omega, prepared, group_density

    def run(self):
        G, labels, elements, V, omega, prepared, density = self.matrices()
        N, D = len(elements), omega.shape[0]
        # The trivial-irrep label is a genuine all-group Fourier filter.
        P = np.ones((N, N), complex)/N
        compressed = V.conj().T @ label_filter(P, V, N, D)
        if np.max(abs(compressed @ compressed-compressed)) > 2e-11:
            raise ArithmeticError("Fourier-label compression is not the seed isotypic projector")
        commutation_error = np.linalg.norm(label_filter(P, V, N, D)-V @ compressed)
        born = norm_squared(label_filter(P, prepared, N, D))
        expected = Fraction(1, 3**self.level)
        if abs(born-float(expected)) > 2e-11:
            raise ArithmeticError("coset-source trivial-label mass is incorrect")
        state = prepared.copy()
        histories = []
        for iteration in range(9):
            p = norm_squared(label_filter(P, state, N, D))
            histories.append({"iterations": iteration, "actual_trivial_label_probability": p})
            state = relative_orbit_reflection(V, state-2*label_filter(P, state, N, D))
        if max(abs(h["actual_trivial_label_probability"]-born) for h in histories) > 2e-11:
            raise ArithmeticError("relative orbit reflection unexpectedly amplifies a central Fourier label")
        # Counterfactual FULL purification reflection. Not a supplied operation.
        good_reflected = prepared-2*label_filter(P, prepared, N, D)
        overlap = np.vdot(prepared, good_reflected)
        true_reflected = 2*prepared*overlap-good_reflected
        true_probability = norm_squared(label_filter(P, true_reflected, N, D))
        exact_true = expected*(3-4*expected)**2
        if abs(true_probability-float(exact_true)) > 2e-11:
            raise ArithmeticError("fixed-purification Grover contrast is incorrect")
        complete_filters = []
        for schema, F in native_fourier_filters(G, elements):
            FV = label_filter(F, V, N, D)
            C = V.conj().T @ FV
            identity_error = np.linalg.norm(FV-V @ C)
            projector_error = np.linalg.norm(C @ C-C)
            if max(identity_error, projector_error) > 2e-11:
                raise ArithmeticError("a whole irreplabel filter violates relative-preparation commutation")
            before = norm_squared(label_filter(F, prepared, N, D))
            after = relative_orbit_reflection(V, prepared-2*label_filter(F, prepared, N, D))
            after_probability = norm_squared(label_filter(F, after, N, D))
            if abs(before-after_probability) > 2e-11:
                raise ArithmeticError("a whole Fourier-label probability changed under relative reflection")
            complete_filters.append({**schema, "regular_group_projector_rank": int(round(np.trace(F).real)),
                                     "seed_compressed_projector_rank": int(round(np.trace(C).real)),
                                     "compressed_projector_idempotence_error": float(projector_error),
                                     "orbit_projector_commutation_error": float(identity_error),
                                     "actual_initial_label_probability": before,
                                     "actual_probability_after_relative_Grover_iteration": after_probability})
        # A noncentral coordinate filter genuinely amplifies, but returns R(g)rho R(g)^dagger.
        coordinate_filter = np.zeros((N, N), complex)
        coordinate_filter[0, 0] = 1
        PV = label_filter(coordinate_filter, V, N, D)
        C = V.conj().T @ PV
        filtered = label_filter(coordinate_filter, prepared, N, D)
        moved = relative_orbit_reflection(V, prepared-2*filtered)
        coordinate_after = norm_squared(label_filter(coordinate_filter, moved, N, D))
        coordinate_p = Fraction(1, N)
        coordinate_exact_after = coordinate_p*(3-4*coordinate_p)**2
        corrected_seed = label_filter(coordinate_filter, moved, N, D).reshape(N, D, -1)[0]
        scalar = (3-4*float(coordinate_p))/np.sqrt(N)
        if np.linalg.norm(corrected_seed-scalar*omega) > 2e-11:
            raise ArithmeticError("amplified public identity-coordinate event does not merely restore the input")
        if abs(coordinate_after-float(coordinate_exact_after)) > 2e-11:
            raise ArithmeticError("noncentral coordinate amplification has incorrect Born accounting")
        coordinate_control = {
            "known_group_coordinate_index": 0,
            "exact_initial_probability": str(coordinate_p),
            "exact_probability_after_one_relative_iteration": str(coordinate_exact_after),
            "actual_probability_after_one_relative_iteration": coordinate_after,
            "compressed_filter_is_scalar_identity": True,
            "compressed_filter_scalar": str(coordinate_p),
            "compressed_projector_idempotence_error": float(np.linalg.norm(C@C-C)),
            "orbit_projector_commutation_error": float(np.linalg.norm(PV-V@C)),
            "normalized_conditioned_seed_return_error": float(np.linalg.norm(corrected_seed/scalar-omega)),
            "group_event_probability_depends_on_secret": False,
            "output_seed_equals_original_unknown_seed": True,
            "secret_decoded": False,
        }
        return {"native_level": self.level, "native_secret": self.secret,
                "all_public_group_elements": elements, "seed_native_label_count": len(labels),
                "group_dimension": N, "input_seed_dimension": D,
                "inaccessible_environment_dimension_in_mathematical_purification": omega.shape[1],
                "relative_orbit_isometry_rank": D, "desired_fixed_purification_reflection_rank": 1,
                "full_group_coset_density_real_imag": [[[float(a.real), float(a.imag)] for a in row] for row in density],
                "relative_preparation_inverse_return_error": float(np.linalg.norm(V.conj().T @ prepared-omega)),
                "trivial_label_compressed_projector_idempotence_error": float(np.linalg.norm(compressed @ compressed-compressed)),
                "Fourier_label_orbit_projector_commutation_error": float(commutation_error),
                "exact_trivial_label_probability": str(expected),
                "relative_reflection_iteration_history": histories,
                "complete_known_Fourier_label_partition": complete_filters,
                "noncentral_coordinate_amplification_countercontrol": coordinate_control,
                "counterfactual_true_purification_one_iteration_probability": true_probability,
                "exact_counterfactual_true_probability": str(exact_true),
                "one_native_source_copy_used_for_each_orbit_state": True,
                "known_relative_preparation_and_inverse_executed": True,
                "counterfactual_fixed_purification_reflection_is_supplied": False,
                "simulation_density_or_secret_are_quantum_algorithm_inputs": False,
                "source_creation_inverse_oracle_of_exact_nilpotent_theorem_supplied": False,
                "growing_class_algorithm_supplied": False}


def run_controls():
    return {"status": "NATIVE_COPY_TO_COSET_SOURCE_AND_RELATIVE_ORACLE_REFLECTION_AUDIT_REVIEW_PENDING",
            "complete_native_orbit_controls": [OrbitControl(r, s).run() for r in (1, 2) for s in ((1, 0), (2, 1))],
            "growing_source_recipes": [source_recipe(r, n) for r, n in ((2, 1), (8, 8), (32, 32), (128, 128))],
            "primary_exact_theorem_requires_fixed_purification_creation_and_inverse": True,
            "primary_nonexact_Proposition3_does_not_require_creation_inverse": True,
            "bounded_class_hypothesis_remains_required_by_primary_results": True,
            "relative_reflection_amplifies_central_Fourier_label_filters": False,
            "all_catalytic_or_noncommuting_receiver_strategies_ruled_out": False,
            "native_full_depth_receiver_supplied": False,
            "novelty_claimed": False, "Shor_level_result_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(r, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": r["status"], "complete_orbit_controls": len(r["complete_native_orbit_controls"])}))


if __name__ == "__main__":
    main()

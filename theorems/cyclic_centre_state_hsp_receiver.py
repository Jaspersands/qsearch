"""Costed odd-prime cyclic-centre StateHSP receiver and finite controls.

LOCAL DERIVATION / REVIEW PENDING. The uniform quantum recipe uses copies
and a known controlled action, not the density tables used in calibration.
No new classical HSP speedup, DHSP solver, novelty or hardness claim.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import nmod_mat
import numpy as np
from scipy.linalg import block_diag
from sympy import isprime

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/CYCLIC_CENTRE_STATE_HSP_RECEIVER.md"
REPORT = ROOT / "research/reductions/cyclic_centre_state_hsp_receiver.json"


def integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def prime(p):
    integer(p, "odd prime", 3)
    if not isprime(p) or p % 2 == 0:
        raise ValueError("odd PRIME required, not an arbitrary cyclic modulus")
    return p


def word(x, width, p):
    if not isinstance(x, (tuple, list)) or len(x) != width:
        raise ValueError("field word with the declared dimension required")
    if any(type(a) is not int or not 0 <= a < p for a in x):
        raise ValueError("canonical integer field coefficients required")
    return tuple(x)


def words(width, p):
    return tuple(product(range(p), repeat=width))


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def ceil(x):
    return -(-x.numerator // x.denominator)


def kernel(rows, width, p):
    integer(width, "kernel width", 1)
    prime(p)
    rows = tuple(word(row, width, p) for row in rows)
    if not rows:
        return tuple(tuple(int(i == j) for i in range(width)) for j in range(width))
    reduced, rank = nmod_mat(rows, p).rref()
    pivots = tuple(next(j for j in range(width) if reduced[i, j]) for i in range(rank))
    out = []
    for j in range(width):
        if j in pivots:
            continue
        v = [0]*width
        v[j] = 1
        for i, pivot in enumerate(pivots):
            v[pivot] = -int(reduced[i, j]) % p
        out.append(tuple(v))
    return tuple(out)


@dataclass(frozen=True)
class BilinearExtension:
    p: int
    B: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        prime(self.p)
        if not isinstance(self.B, (tuple, list)) or not self.B:
            raise ValueError("nonempty bilinear form required")
        object.__setattr__(self, "B", tuple(word(row, len(self.B), self.p) for row in self.B))

    @property
    def d(self):
        return len(self.B)

    def bilinear(self, x, y):
        x, y = word(x, self.d, self.p), word(y, self.d, self.p)
        return sum(x[i]*dot(row, y) for i, row in enumerate(self.B)) % self.p

    def element(self, g):
        if not isinstance(g, (tuple, list)) or len(g) != 2:
            raise ValueError("group element (field word, central scalar) required")
        x, z = g
        word((z,), 1, self.p)
        return word(x, self.d, self.p), z

    def multiply(self, g, h):
        x, z = self.element(g)
        y, w = self.element(h)
        return tuple((a+b) % self.p for a, b in zip(x, y)), (z+w+self.bilinear(x, y)) % self.p

    def commutator(self, x, y):
        return (self.bilinear(x, y)-self.bilinear(y, x)) % self.p

    def isotropic_frame(self, frame):
        frame = tuple(word(row, self.d, self.p) for row in frame)
        if frame and nmod_mat(frame, self.p).rank() != len(frame):
            raise ValueError("independent overgroup frame required")
        if any(self.commutator(x, y) for x in frame for y in frame):
            raise ValueError("recovered overgroup does not commute: return FAILURE")
        return frame

    def chart(self, frame, coordinates):
        frame = self.isotropic_frame(frame)
        c = word(coordinates, len(frame)+1, self.p)
        x = tuple(sum(a*v[i] for a, v in zip(c[:-1], frame)) % self.p for i in range(self.d))
        return x, (c[-1]+pow(2, -1, self.p)*self.bilinear(x, x)) % self.p


def resource_ledger(p, d, epsilon, failure_bits):
    prime(p)
    integer(d, "quotient dimension", 1)
    integer(failure_bits, "failure bits", 1)
    if isinstance(epsilon, bool) or not isinstance(epsilon, (int, Fraction, str)):
        raise ValueError("exact rational original gap required")
    epsilon = Fraction(epsilon)
    if not 0 < epsilon <= 1:
        raise ValueError("original gap must be in (0,1]")
    h, selection_bits = (p-1).bit_length(), (p-2).bit_length()
    delta = Fraction(1, 16*p*p)
    sector_bits = failure_bits+2+selection_bits
    m = 32*p*p*(d*h+sector_bits)
    C = p*m
    weight = epsilon/(2*(p-1))
    N = ceil(Fraction(2*C+8*(failure_bits+2), 1)/weight)
    M = ceil(2*Fraction((d+1)*h+failure_bits+2, 1)/epsilon)
    return {
        "p": p, "quotient_dimension": d, "original_gap_lower": str(epsilon),
        "failure_bits": failure_bits, "ceil_log2_p": h,
        "data_selected_sector_union_bits": selection_bits,
        "conditional_modulus_defect_threshold": str(delta),
        "commutator_norm_squared_upper": str(32*delta),
        "nontrivial_root_distance_squared_lower": str(Fraction(16, p*p)),
        "tensor_copies_per_Fourier_experiment": p,
        "sector_Fourier_experiments": m, "selected_sector_copy_quota": C,
        "one_nonzero_sector_weight_lower_if_centre_not_fixed": str(weight),
        "original_centre_acquisition_cap": N,
        "fresh_original_final_copy_cap": M, "total_original_copy_cap": N+M,
        "known_controlled_R_call_cap": N+C+M,
        "conditional_bucket_memory_cap": (p-1)*C,
        "quota_failure_upper": str(Fraction(1, 2**(failure_bits+2))),
        "all_selected_sector_overgroup_failure_upper": str(Fraction(1, 2**(failure_bits+2))),
        "final_decoder_failure_upper": str(Fraction(1, 2**(failure_bits+2))),
        "total_ideal_failure_upper": str(Fraction(3, 2**(failure_bits+2))),
        "minimum_conditional_gap_required": False,
        "iid_copies_of_one_original_state_required": True,
        "polynomial_in_parameters": ["d", "p", "1/epsilon", "failure_bits", "controlled_R_cost"],
        "polylog_group_order_at_arbitrary_binary_encoded_prime": False,
        "approximate_source_or_gate_error_certified": False,
    }


def density(rho):
    rho = np.asarray(rho, dtype=complex)
    if rho.ndim != 2 or not rho.shape[0] or rho.shape[0] != rho.shape[1]:
        raise ValueError("finite calibration density matrix required")
    if not np.all(np.isfinite(rho)) or np.max(abs(rho-rho.conj().T)) > 1e-12:
        raise ValueError("finite Hermitian matrix required")
    if abs(np.trace(rho)-1) > 1e-12 or np.linalg.eigvalsh(rho).min() < -1e-12:
        raise ValueError("normalized positive density required")
    return rho


def character_matrix(points, p):
    return np.exp(-2j*np.pi*np.array([[dot(y, x) % p for x in points] for y in points])/p)


def probabilities_from_moments(moments, points, p):
    raw = character_matrix(points, p) @ moments/len(points)
    if not np.all(np.isfinite(raw)) or max(abs(raw.imag)) > 2e-11 or min(raw.real) < -2e-11:
        raise ValueError("invalid Fourier probability law: sector/linearisation premise failed")
    if abs(sum(raw)-1) > 2e-11:
        raise ValueError("Fourier probability law is not normalized")
    out = np.maximum(raw.real, 0)
    return out/sum(out)


def qutrit_sector_actions(lam):
    word((lam,), 1, 3)
    omega = np.exp(2j*np.pi/3)
    actions = []
    for a, b in words(2, 3):
        U = np.zeros((3, 3), complex)
        for x in range(3):
            U[(x+a) % 3, x] = omega**((lam*b*x) % 3)
        actions.append(U)
    return tuple(actions)


def sector_fourier_control(rho, lam, literal=True):
    """Three actual conditional copies, known action, ALL nine outcomes."""
    if type(literal) is not bool:
        raise ValueError("Boolean literal-control flag required")
    if lam not in (1, 2) or type(lam) is not int:
        raise ValueError("faithful NONZERO central sector required")
    rho = density(rho)
    if rho.shape != (3, 3):
        raise ValueError("literal control uses one qutrit per conditional copy")
    points = words(2, 3)
    actions = qutrit_sector_actions(lam)
    phi = np.array([np.trace(U @ rho) for U in actions])
    expected = probabilities_from_moments(phi**3, points, 3)
    error = None
    physical = None
    if literal:
        tensor = np.kron(np.kron(rho, rho), rho)
        known = np.stack([np.kron(np.kron(U, U), U) for U in actions])
        K = np.einsum("yx,xij->yij", character_matrix(points, 3)/9, known)
        physical = np.array([np.trace(U @ tensor @ U.conj().T).real for U in K])
        error = float(max(abs(physical-expected)))
        if error > 2e-11 or abs(sum(physical)-1) > 2e-11:
            raise ArithmeticError("actual complete tensor instrument disagrees with character law")
    return {
        "central_character": lam, "input_qutrit_copies_consumed": 3,
        "known_controlled_R_calls": 3, "full_character_words": points,
        "conditional_action_moments_real_imag": [[float(z.real), float(z.imag)] for z in phi],
        "tensor_moment_Fourier_probabilities": expected.tolist(),
        "literal_Kraus_probabilities": None if physical is None else physical.tolist(),
        "maximum_literal_probability_error": error,
        "every_outcome_retained": True, "selected_sector_supplied_for_free": False,
        "nonabelian_QFT_or_unknown_inverse_used": False,
        "full_unconditioned_tensor_action_claimed_linear": False,
    }


def two_qudit_purified_control(lam, magic_coefficients):
    """Literal 81-character instrument on three NON-stabilizer 2-qudit copies."""
    if type(lam) is not int or lam not in (1, 2):
        raise ValueError("faithful nonzero sector required")
    if (not isinstance(magic_coefficients, (list, tuple)) or len(magic_coefficients) != 3
            or any(type(a) is not int for a in magic_coefficients) or not any(magic_coefficients)):
        raise ValueError("three nonzero-together integer calibration amplitudes required")
    norm = sum(a*a for a in magic_coefficients)
    v = np.kron(np.array([1., 0., 0.]), np.array(magic_coefficients)/np.sqrt(norm))
    basis, points = words(2, 3), words(4, 3)
    index = {x: i for i, x in enumerate(basis)}
    joint, phi = [], []
    for a1, a2, b1, b2 in points:
        shifted = np.zeros(9, complex)
        for i, t in enumerate(basis):
            shifted[index[((t[0]+a1) % 3, (t[1]+a2) % 3)]] = v[i]*np.exp(2j*np.pi*(lam*(b1*t[0]+b2*t[1]) % 3)/3)
        phi.append(np.vdot(v, shifted))
        joint.append(np.kron(np.kron(shifted, shifted), shifted))
    actual = np.sum(abs(character_matrix(points, 3) @ np.array(joint)/81)**2, axis=1)
    expected = probabilities_from_moments(np.array(phi)**3, points, 3)
    if max(abs(actual-expected)) > 2e-11:
        raise ArithmeticError("literal two-qudit tensor-control instrument failed")
    one = sector_fourier_control(np.outer(np.array(magic_coefficients), np.array(magic_coefficients))/norm, lam)
    nontrivial = [abs(complex(*z)) for z in one["conditional_action_moments_real_imag"][1:]]
    if max(nontrivial) >= 1-1e-10:
        raise ValueError("this control requires an actually nonstabilizer calibration vector")
    return {"central_character": lam, "nonstabilizer_integer_amplitudes": list(magic_coefficients),
            "integer_amplitude_squared_norm": norm, "full_character_words": points,
            "complete_literal_probabilities": actual.tolist(),
            "tensor_moment_Fourier_probabilities": expected.tolist(),
            "maximum_literal_probability_error": float(max(abs(actual-expected))),
            "actual_conditional_input_copies": 3, "physical_qutrits_in_three_copies": 6,
            "conditional_full_quotient_dimension": 4,
            "maximum_nonidentity_one_component_overlap": max(nontrivial),
            "one_component_instrument": one,
            "density_table_is_an_algorithm_input": False,
            "source_is_a_new_toy_oracle_problem": False}


def calibration_source(kind, central_lift=0, eta=Fraction(1, 8)):
    """Established Heisenberg StateHSP controls, not proposed oracle problems."""
    word((central_lift,), 1, 3)
    if kind not in ("coset-mixed", "coset-coherent", "tiny-conditional-gap", "centre-fixed", "rare-central-sector"):
        raise ValueError("declared StateHSP calibration family required")
    if not isinstance(eta, Fraction) or not 0 < eta <= 1:
        raise ValueError("exact positive contamination required")
    points = words(2, 3)
    chars = character_matrix(points, 3).conj().T
    actions0 = tuple(np.diag(row) for row in chars)
    basis = np.zeros(3, complex)
    basis[-central_lift % 3] = 1
    v0 = np.array([int(b == 0) for a, b in points], complex)/np.sqrt(3)
    sigma0 = np.diag(abs(v0)**2)
    sigma1 = sigma2 = np.outer(basis, basis.conj())
    weights = np.array([1/3, 1/3, 1/3])
    if kind == "coset-coherent":
        sigma0 = np.outer(v0, v0.conj())
        state = np.concatenate((v0, basis, basis))/np.sqrt(3)
        original = np.outer(state, state.conj())
    elif kind == "tiny-conditional-gap":
        sigma0 = np.eye(9)/9
        sigma1 = np.diag([1-2*float(eta)/3, float(eta)/3, float(eta)/3])
        sigma2 = np.eye(3)/3
        original = block_diag(sigma0, sigma1, sigma2)/3
    elif kind == "centre-fixed":
        weights = np.array([1., 0., 0.])
        original = block_diag(sigma0, np.zeros((3, 3)), np.zeros((3, 3)))
    elif kind == "rare-central-sector":
        weights = np.array([1-2*float(eta)/3, float(eta)/3, float(eta)/3])
        original = block_diag(*(w*s for w, s in zip(weights, (sigma0, sigma1, sigma2))))
    else:
        original = block_diag(sigma0, sigma1, sigma2)/3
    density(original)
    ext = BilinearExtension(3, ((0, 0), (1, 0)))
    actions = (actions0, qutrit_sector_actions(1), qutrit_sector_actions(2))

    def action(g):
        x, z = ext.element(g)
        i = points.index(x)
        return block_diag(*(np.exp(2j*np.pi*(lam*z % 3)/3)*actions[lam][i] for lam in range(3)))

    if kind == "tiny-conditional-gap":
        subgroup = (((0, 0), 0),)
        gap = Fraction(2, 3)
    elif kind == "centre-fixed":
        subgroup = tuple(((0, b), z) for b in range(3) for z in range(3))
        gap = Fraction(1)
    else:
        subgroup = tuple(((0, b), central_lift*b % 3) for b in range(3))
        gap = eta if kind == "rare-central-sector" else Fraction(1)
    overlaps = [np.trace(action((x, z)) @ original) for x in points for z in range(3)]
    actual = tuple((x, z) for x in points for z in range(3)
                   if abs(np.trace(action((x, z)) @ original)-1) < 2e-11)
    if actual != subgroup:
        raise ArithmeticError("calibration source has the wrong actual Bose subgroup")
    maximum_outside = max((abs(a) for a, g in zip(overlaps, ((x, z) for x in points for z in range(3)))
                           if g not in subgroup), default=0)
    if maximum_outside > 1-float(gap)+2e-11:
        raise ArithmeticError("global Bose-gap control failed")
    return {"kind": kind, "central_lift": central_lift, "eta": eta, "extension": ext,
            "points": points, "weights": weights, "conditional_states": (sigma0, sigma1, sigma2),
            "original": original, "action": action, "subgroup": subgroup, "gap": gap,
            "maximum_outside_overlap": float(maximum_outside)}


def final_fourier_control(source, frame, centre_fixed=False):
    if type(centre_fixed) is not bool:
        raise ValueError("Boolean successful-centre-branch control required")
    ext = source["extension"]
    frame = ext.isotropic_frame(frame) if not centre_fixed else ()
    if centre_fixed and source["kind"] != "centre-fixed":
        raise ValueError("cannot grant a centre-fixed quotient action on a nontrivial sector source")
    dimension = ext.d if centre_fixed else len(frame)+1
    points = words(dimension, ext.p)
    group_elements = tuple((x, 0) if centre_fixed else ext.chart(frame, x) for x in points)
    actions = np.stack([source["action"](g) for g in group_elements])
    moments = np.array([np.trace(U @ source["original"]) for U in actions])
    expected = probabilities_from_moments(moments, points, ext.p)
    K = np.einsum("yx,xij->yij", character_matrix(points, ext.p)/len(points), actions)
    physical = np.array([np.trace(U @ source["original"] @ U.conj().T).real for U in K])
    if max(abs(physical-expected)) > 2e-11:
        raise ArithmeticError("final full original-state instrument disagrees with its claimed law")
    return {"dimension": dimension, "character_words": points,
            "group_chart_elements": group_elements, "probabilities": expected.tolist(),
            "literal_Kraus_probabilities": physical.tolist(),
            "maximum_literal_probability_error": float(max(abs(physical-expected))),
            "uses_fresh_original_state_not_the_selected_sector_state": True}


def reference_receiver(source, seed=78631, failure_bits=4):
    """Execute the capped classical control flow using finite calibration laws.

    Density-dependent probabilities simulate quantum instruments; they are
    not inputs to the specified uniform quantum algorithm.
    """
    ext = source["extension"]
    ledger = resource_ledger(ext.p, ext.d, source["gap"], failure_bits)
    rng = np.random.default_rng(seed)
    N, C, m = (ledger[k] for k in ("original_centre_acquisition_cap", "selected_sector_copy_quota", "sector_Fourier_experiments"))
    stream = rng.choice(ext.p, size=N, p=source["weights"])
    hits = []
    for lam in range(1, ext.p):
        indices = np.flatnonzero(stream == lam)
        if len(indices) >= C:
            hits.append((int(indices[C-1])+1, lam))
    if hits:
        draws, selected = min(hits)
        control = sector_fourier_control(source["conditional_states"][selected], selected, literal=False)
        sampled = rng.choice(len(source["points"]), size=m, p=control["tensor_moment_Fourier_probabilities"])
        histogram = np.bincount(sampled, minlength=len(source["points"]))
        observed = [point for point, count in zip(source["points"], histogram) if count]
        frame = kernel(observed, ext.d, ext.p)
        try:
            ext.isotropic_frame(frame)
        except ValueError:
            return {"status": "FAILURE_NONCOMMUTING_OVERGROUP", "seed": seed, "ledger": ledger}
        final = final_fourier_control(source, frame)
        centre_fixed = False
    else:
        draws, selected, frame, observed, histogram = N, None, (), [], np.array([], dtype=int)
        if source["kind"] != "centre-fixed":
            return {"status": "FAILURE_CENTRE_QUOTA", "seed": seed, "ledger": ledger}
        final = final_fourier_control(source, frame, centre_fixed=True)
        centre_fixed = True
    M = ledger["fresh_original_final_copy_cap"]
    sampled = rng.choice(len(final["character_words"]), size=M, p=final["probabilities"])
    final_histogram = np.bincount(sampled, minlength=len(final["character_words"]))
    rows = [point for point, count in zip(final["character_words"], final_histogram) if count]
    recovered = kernel(rows, final["dimension"], ext.p)
    recovered_elements = []
    for t in words(len(recovered), ext.p):
        u = tuple(sum(a*row[j] for a, row in zip(t, recovered)) % ext.p for j in range(final["dimension"]))
        if centre_fixed:
            recovered_elements.extend((u, z) for z in range(ext.p))
        else:
            recovered_elements.append(ext.chart(frame, u))
    recovered_elements = tuple(sorted(recovered_elements))
    return {
        "status": "RECOVERED" if recovered_elements == source["subgroup"] else "FAILURE_FINAL_KERNEL",
        "source_kind": source["kind"], "calibration_central_lift": source["central_lift"],
        "contamination_eta": str(source["eta"]), "seed": seed, "ledger": ledger,
        "actual_original_centre_draws": draws, "centre_bucket_counts": np.bincount(stream[:draws], minlength=3).tolist(),
        "selected_nonzero_sector": selected, "successful_centre_fixed_branch": centre_fixed,
        "tensor_sample_histogram": histogram.tolist(), "tensor_observed_character_words": observed,
        "recovered_quotient_overgroup_frame": frame,
        "quotient_overgroup_commutator_zero": None if centre_fixed else True,
        "actual_abelian_overgroup_used": not centre_fixed,
        "centre_fixed_quotient_action_linear_on_support": centre_fixed,
        "centre_fixed_section_claimed_linear_on_full_workspace": False,
        "final_instrument": final, "final_sample_histogram": final_histogram.tolist(),
        "recovered_final_kernel_basis": recovered, "recovered_Bose_subgroup_elements": recovered_elements,
        "actual_Bose_subgroup_elements": source["subgroup"],
        "actual_total_original_copies": draws+M,
        "actual_known_controlled_R_calls": draws+(C if selected is not None else 0)+M,
        "one_original_source_state_copied_or_reused": False,
        "density_tables_required_by_uniform_quantum_recipe": False,
        "finite_reference_simulation_is_scalable_quantum_hardware_execution": False,
    }


def run_controls():
    cases = [calibration_source(kind, c) for kind in ("coset-mixed", "coset-coherent") for c in range(3)]
    cases.extend([calibration_source("tiny-conditional-gap", eta=Fraction(1, 8)),
                  calibration_source("tiny-conditional-gap", eta=Fraction(1, 2**40)),
                  calibration_source("centre-fixed"),
                  calibration_source("rare-central-sector", eta=Fraction(1, 8))])
    instruments = []
    runs = []
    for i, source in enumerate(cases):
        if source["kind"] != "centre-fixed":
            for lam in (1, 2):
                control = sector_fourier_control(source["conditional_states"][lam], lam)
                control.update({"source_kind": source["kind"], "calibration_central_lift": source["central_lift"],
                                "contamination_eta": str(source["eta"])})
                instruments.append(control)
        # Pinned calibration seeds exercise the genuinely tiny-gap sector.
        seed = 78632 if source["kind"] == "tiny-conditional-gap" else 78631+i
        runs.append(reference_receiver(source, seed))
    if any(r["status"] != "RECOVERED" for r in runs):
        raise ArithmeticError("a capped complete reference receiver failed its calibration")
    eta = Fraction(1, 2**40)
    a = (1-eta)**3
    tiny = {
        "original_Bose_gap_lower": "2/3", "selected_sector": 1,
        "conditional_exact_gap_of_Z_direction": str(eta),
        "conditional_nontrivial_exact_anyonic_symmetry": False,
        "approximate_commuting_overgroup_may_retain_Z_direction": True,
        "exact_tensor_probability_if_second_character_zero": str((1+2*a)/9),
        "exact_tensor_probability_if_second_character_nonzero": str((1-a)/9),
        "final_original_probability_yb0_yz1": str((3-2*eta)/9),
        "final_original_probability_yb_nonzero_yz1": str(eta/9),
        "final_original_probability_yz_not_one": "1/9",
        "original_central_sector_weights": ["1/3"]*3,
    }
    return {
        "status": "CONSTRUCTIVE_ODD_PRIME_CYCLIC_CENTRE_STATE_HSP_REVIEW_PENDING",
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "bilinear_extension_form": {"p": 3, "B": [[0, 0], [1, 0]]},
        "complete_literal_sector_instruments": instruments,
        "nonstabilizer_two_qudit_instruments": [two_qudit_purified_control(lam, amplitudes)
                                               for lam in (1, 2) for amplitudes in ((1, 2, 3), (2, 1, 1))],
        "capped_complete_reference_receivers": runs,
        "tiny_conditional_gap_countercontrol": tiny,
        "growing_integer_resource_ledgers": [resource_ledger(p, d, Fraction(1, 4), 32)
                                            for p in (3, 5, 7, 17) for d in (8, 32, 128, 512)],
        "uniform_quantum_recipe_specified": True,
        "arbitrary_mixed_state_conditional_gap_assumed": False,
        "all_central_extensions_solved": False, "native_DHSP_source_reduction_supplied": False,
        "new_classical_HSP_speedup_claimed": False, "candidate_record_accepted": False,
        "novelty_claimed": False, "Shor_level_result_claimed": False,
        "routine_CLI_registry_UI_and_Git_owner": "Gemini or Antigravity",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "literal_sector_instruments": len(report["complete_literal_sector_instruments"]),
                      "capped_receivers": len(report["capped_complete_reference_receivers"])}, indent=2))


if __name__ == "__main__":
    main()

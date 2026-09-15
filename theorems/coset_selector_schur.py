"""Source-stabilizer Schur blocks, with multiplicities and full-source cost charged.

This is a specialization of standard qubit Schur-Weyl duality, not an
internal Specht recoupling circuit or a growing-degree measurement compiler.
"""

from fractions import Fraction
from functools import lru_cache
import itertools
import math

import numpy as np

from coset_mask_symmetry import _probabilities, physical_selector_schur_channel, radial_probabilities
from coset_mask_tail_fidelity import regular_selector_query_control
from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_global_collision_free_mass import elementary_symmetric_fraction, plancherel_weights
from weak_fourier_signal import character_on_involution


def symmetric_power(matrices, degree):
    """Normalized Dicke-basis matrix of Sym^degree(B), including singular B."""
    b = np.asarray(matrices, dtype=complex)
    if type(degree) is not int or degree < 0 or b.shape[-2:] != (2, 2) or not np.isfinite(b).all():
        raise ValueError("finite 2x2 matrices and nonnegative integer degree required")
    result = np.zeros((*b.shape[:-2], degree+1, degree+1), dtype=complex)
    for p in range(degree+1):
        for q in range(degree+1):
            for overlap in range(max(0, p+q-degree), min(p, q)+1):
                result[..., p, q] += (math.comb(q, overlap)*math.comb(degree-q, p-overlap)
                    * b[..., 0, 0]**(degree-p-q+overlap) * b[..., 0, 1]**(q-overlap)
                    * b[..., 1, 0]**(p-overlap) * b[..., 1, 1]**overlap)
            result[..., p, q] *= math.sqrt(math.comb(degree, q)/math.comb(degree, p))
    return result


def selector_spin_sectors(count):
    if type(count) is not int or count < 0:
        raise ValueError("nonnegative integer source count required")
    return tuple((ell, count-2*ell+1,
        math.comb(count, ell)-(math.comb(count, ell-1) if ell else 0))
        for ell in range(count//2+1))


def source_stabilizer_cost(counts):
    counts = tuple(counts)
    if not counts or any(type(c) is not int or c < 0 for c in counts) or sum(counts) < 1:
        raise ValueError("nonempty nonnegative integer source counts with positive total required")
    k = sum(counts)
    return {"copy_count": k, "source_counts": list(counts),
        "source_orbit_size": math.factorial(k)//math.prod(math.factorial(c) for c in counts),
        "stabilizer_order": math.prod(math.factorial(c) for c in counts),
        "spin_block_count": math.prod(c//2+1 for c in counts),
        "largest_spin_block_dimension": math.prod(c+1 for c in counts),
        "spin_matrix_entries": math.prod(math.comb(c+3, 3) for c in counts),
        "multiplicity_weighted_dimension": 2**k,
        "all_sources_distinct": max(counts) == 1,
        "dimension_is_a_circuit_lower_bound": False}


def selector_schur_storage(copy_count, source_category_count):
    k, r = copy_count, source_category_count
    if type(k) is not int or type(r) is not int or k < 1 or r < 1:
        raise ValueError("positive integer copy and source-category counts required")
    return {"copy_count": k, "source_category_count": r,
        "source_histogram_count": math.comb(k+r-1, r-1),
        "entries_per_hypothesis_all_histograms": math.comb(k+4*r-1, 4*r-1),
        "ordered_source_dense_entries": (4*r)**k,
        "fixed_category_count_polynomial_in_copies": True,
        "growing_category_count_polynomial_proved": False,
        "group_pair_contraction_and_precision_costs_excluded": True}


def _compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in _compositions(total-first, parts-1):
                yield (first, *rest)


def _batch_kron(left, right):
    shape = (*left.shape[:-2], left.shape[-2]*right.shape[-2], left.shape[-1]*right.shape[-1])
    return np.einsum("...ab,...cd->...acbd", left, right).reshape(shape)


def _source_kernels(values, inverse, products):
    size = len(inverse)
    b = np.empty((len(values), size, size, 2, 2), dtype=complex)
    b[..., 0, 0] = values[:, 0, None, None]
    b[..., 0, 1] = values[:, inverse, None]
    b[..., 1, 0] = values[:, None, :]
    b[..., 1, 1] = values[:, products]
    return b.reshape(len(values), size*size, 2, 2)


@lru_cache(maxsize=5, typed=True)
def source_resolved_schur_model(degree, copies, *, erase_source_labels=False):
    """Finite calibration evaluator, without D^K physical or 2^K selector matrices."""
    if type(copies) is not int or copies < 1 or type(erase_source_labels) is not bool:
        raise ValueError("positive integer copies and explicit source-erasure boolean required")
    data, _, _, a, residual = regular_selector_query_control(degree)
    p = data[3][:, None]*data[2]/len(a)
    if erase_source_labels:
        p = p.sum(axis=0, keepdims=True)
    r = len(p)
    cost = selector_schur_storage(copies, r)
    if cost["entries_per_hypothesis_all_histograms"]*(len(data[8])+1) > 2_000_000:
        raise ValueError("finite calibration block budget exceeded; use the symbolic cost audit")
    kernels = np.array([_source_kernels(p if h is None else p+p[:, h], data[6], data[7])
        for h in (None, *data[8])])
    coefficients = np.outer(a.conjugate(), a).reshape(-1)
    local = {}
    for j in range(r):
        b = kernels[:, j]
        determinant = b[..., 0, 0]*b[..., 1, 1]-b[..., 0, 1]*b[..., 1, 0]
        for c in range(copies+1):
            for ell, _, _ in selector_spin_sectors(c):
                local[j, c, ell] = determinant[..., None, None]**ell*symmetric_power(b, c-2*ell)
    blocks = []
    for counts in _compositions(copies, r):
        orbit = source_stabilizer_cost(counts)["source_orbit_size"]
        for sectors in itertools.product(*(selector_spin_sectors(c) for c in counts)):
            ell, dimensions, multiplicities = zip(*sectors)
            tensor = np.ones((len(data[8])+1, len(a)**2, 1, 1), dtype=complex)
            for j, c in enumerate(counts):
                tensor = _batch_kron(tensor, local[j, c, ell[j]])
            matrices = np.einsum("g,hgab->hab", coefficients, tensor)
            weights = np.array([sum(ell)+sum(index) for index in itertools.product(*(range(d) for d in dimensions))])
            matrices.setflags(write=False)
            weights.setflags(write=False)
            blocks.append({"source_counts": counts, "spin_defects": ell,
                "source_orbit_size": orbit, "spin_multiplicity": math.prod(multiplicities),
                "weights": weights, "hypothesis_blocks": matrices})
    return {"degree": degree, "copy_count": copies, "source_category_count": r,
        "hidden_members_evaluated": len(data[8]), "blocks": blocks, "cost": cost,
        "source_labels_erased": erase_source_labels, "query_unitarity_residual": residual,
        "group_pair_terms_per_hidden_member": len(a)**2,
        "growing_degree_measurement_compiled": False, "speedup_claim_allowed": False}


def radial_schur_statistics(model, weight_probabilities):
    w = _probabilities(weight_probabilities)
    k = model["copy_count"]
    if len(w) != k+1:
        raise ValueError("one probability per Hamming weight required")
    amplitudes = np.sqrt(w/np.array([math.comb(k, m) for m in range(k+1)]))
    distances = np.zeros(model["hidden_members_evaluated"])
    masses = np.zeros(len(distances)+1)
    decision = pinched = wrong_multiplicity = top_spin = 0.0
    hermiticity = negativity = 0.0
    for block in model["blocks"]:
        x = amplitudes[block["weights"]]
        physical = block["hypothesis_blocks"]*np.outer(x, x)
        multiplicity = block["source_orbit_size"]*block["spin_multiplicity"]
        hermiticity = max(hermiticity, float(np.max(np.abs(physical-physical.conj().swapaxes(-1, -2)))))
        negativity = max(negativity, -float(np.linalg.eigvalsh(physical).min()))
        masses += multiplicity*np.trace(physical, axis1=-2, axis2=-1).real
        delta = physical[1:].mean(axis=0)-physical[0]
        norm = float(np.abs(np.linalg.eigvalsh(delta)).sum()/2)
        decision += multiplicity*norm
        wrong_multiplicity += block["source_orbit_size"]*norm
        if not any(block["spin_defects"]):
            top_spin += multiplicity*norm
        same_weight = block["weights"][:, None] == block["weights"][None, :]
        pinched += multiplicity*float(np.abs(np.linalg.eigvalsh(delta*same_weight)).sum()/2)
        distances += multiplicity*np.abs(np.linalg.eigvalsh(physical[1:]-physical[0])).sum(axis=-1)/2
    residual = max(hermiticity, negativity, float(np.max(np.abs(masses-1))))
    if residual > 1e-8 or decision > distances.mean()+1e-8 or pinched > decision+1e-8:
        raise ArithmeticError("Schur blocks lost mass, positivity, coherence or shared-hidden averaging")
    return {"weight_probabilities": w.tolist(), "decision_distance": decision,
        "individual_hidden_distances": distances.tolist(), "weight_pinched_distance": pinched,
        "incorrect_unit_multiplicity_distance": wrong_multiplicity,
        "incorrect_top_spin_only_distance": top_spin, "normalization_residual": residual,
        "source_only_baseline_requires_quantum_frontend": True,
        "efficient_measurement_supplied": False, "speedup_claim_allowed": False}


def full_source_collision_audit(degree, copies, *, exact_distinct=False):
    if type(degree) is not int or degree < 2 or degree % 2 or type(copies) is not int or copies < 1:
        raise ValueError("even degree >=2 and positive integer copies required")
    if type(exact_distinct) is not bool:
        raise ValueError("exact_distinct must be boolean")
    p = plancherel_weights(degree)
    q = tuple(Fraction(hook_length_dimension(lam)*(hook_length_dimension(lam)
        +character_on_involution(lam, degree//2)), math.factorial(degree)) for lam in integer_partitions(degree))
    if sum(q) != 1 or any(not 0 <= y <= 2*x for x, y in zip(p, q)):
        raise ArithmeticError("alternative weak-Fourier source law failed Plancherel domination")
    collision = [sum(x*x for x in law) for law in (p, q)]
    distinct = [math.factorial(copies)*elementary_symmetric_fraction(law, copies)
        for law in (p, q)] if exact_distinct else [None, None]
    union = [min(Fraction(1), math.comb(copies, 2)*c) for c in collision]
    if exact_distinct and any(1-d > b for d, b in zip(distinct, union)):
        raise ArithmeticError("exact collision law exceeded birthday bound")
    return {"degree": degree, "copy_count": copies, "partition_count": len(p),
        "null_pair_collision": str(collision[0]), "alternative_pair_collision": str(collision[1]),
        "null_collision_upper_bound": str(union[0]), "alternative_collision_upper_bound": str(union[1]),
        "null_distinct_probability": None if distinct[0] is None else str(distinct[0]),
        "alternative_distinct_probability": None if distinct[1] is None else str(distinct[1]),
        "alternative_pair_collision_at_most_four_times_null": collision[1] <= 4*collision[0],
        "maximum_plancherel_atom": str(max(p)), "source_law_independent_of_hidden_conjugate": True,
        "source_law_independent_of_fixed_mask": True, "finite_asymptotic_crossover_certified": False,
        "asymptotic": "At polynomial K, both collision probabilities are O(K^2 exp(-c sqrt(n))); existing maximal-dimension bounds imply o(1).",
        "interpretation": "With asymptotically full natural mass, every source occurs once and the source-stabilizer Schur block remains 2^K dimensional. Not a circuit lower bound."}


@lru_cache(maxsize=1)
def audit_source_resolved_selector_schur():
    controls = []
    for n, k in ((3, 2), (3, 3), (4, 2)):
        physical = physical_selector_schur_channel(k, n)
        model = source_resolved_schur_model(n, k)
        coarse = source_resolved_schur_model(n, k, erase_source_labels=True)
        probes = []
        weights = [np.array([math.comb(k, m)/2**k for m in range(k+1)]),
            np.ones(k+1)/(k+1), *np.eye(k+1)]
        spectral_residual = 0.0
        for w in weights:
            row = radial_schur_statistics(model, w)
            erased = radial_schur_statistics(coarse, w)
            p = radial_probabilities(w)
            dense = physical["blocks"]*np.sqrt(p[:, None]*p[None, :])
            decision = float(np.abs(np.linalg.eigvalsh(dense[1:].mean(axis=0)-dense[0])).sum()/2)
            individual = np.abs(np.linalg.eigvalsh(dense[1:]-dense[0])).sum(axis=(-1, -2))/2
            if abs(decision-row["decision_distance"]) > 1e-8 or not np.allclose(individual, row["individual_hidden_distances"], atol=1e-8):
                raise ArithmeticError("source Schur decision disagrees with independent physical channel")
            for counts in _compositions(k, model["source_category_count"]):
                source = tuple(j for j, c in enumerate(counts) for _ in range(c))
                index = physical["sources"].index(source)
                spectra = []
                for block in model["blocks"]:
                    if block["source_counts"] == counts:
                        amp = np.sqrt(w[block["weights"]]/np.array([math.comb(k, m) for m in block["weights"]]))
                        spectrum = np.linalg.eigvalsh(block["hypothesis_blocks"]*np.outer(amp, amp))
                        spectra.append(np.repeat(spectrum, block["spin_multiplicity"], axis=-1))
                reconstructed = np.sort(np.concatenate(spectra, axis=-1), axis=-1)
                spectral_residual = max(spectral_residual, float(np.max(np.abs(reconstructed-np.linalg.eigvalsh(dense[:, index])))))
            if erased["decision_distance"] > decision+1e-8:
                raise ArithmeticError("source erasure increased information")
            probes.append(dict(row, erased_source_distance=erased["decision_distance"]))
        if spectral_residual > 1e-8:
            raise ArithmeticError("multiplicity-expanded source spectra do not match the physical outputs")
        controls.append({"degree": n, "copy_count": k, "source_histogram_count": model["cost"]["source_histogram_count"],
            "hidden_members_checked": model["hidden_members_evaluated"], "full_spectral_residual": spectral_residual,
            "probes": probes, "verified": True})
    return {"controls": controls, "verified": True,
        "extended_copy_controls": [dict(radial_schur_statistics(source_resolved_schur_model(3, k),
            np.ones(k+1)/(k+1)), degree=3, copy_count=k, cost=selector_schur_storage(k, 3)) for k in (4, 6)],
        "cost_controls": [source_stabilizer_cost(c) for c in ((64,), (32, 32), (8,)*8, (1,)*64)],
        "storage_controls": [selector_schur_storage(64, r) for r in (1, 2, 8, 64)],
        "source_collision_controls": [full_source_collision_audit(n, k, exact_distinct=k <= 4)
            for n in (4, 8, 16, 24) for k in (2, 4, n*n)],
        "source_stabilizer_reduction_derived": True,
        "full_source_collision_free_asymptotic_derived": True,
        "classical_simulator_for_growing_degree": False,
        "intermediate_band_obstructed": False, "efficient_measurement_compiled": False,
        "formal_proof_verification": False, "independent_review": False, "novelty_established": False,
        "literature": [{"id": "bacon-chuang-harrow-schur-2004", "url": "https://arxiv.org/abs/quant-ph/0407082"},
            {"id": "moroder-et-al-permutation-invariant-2012", "url": "https://arxiv.org/abs/1205.4941"},
            {"id": "aggarwal-elboim-maximal-dimension-2026", "url": "https://arxiv.org/abs/2605.25995"}],
        "research_update": "Radial masks admit exact source-stabilizer spin blocks with all multiplicities and cross-weight coherence retained. Cost is polynomial in copies ONLY at fixed source-category count and excludes group-pair contraction. Full irrep labels are asymptotically collision-free at polynomial copies under both hypotheses, leaving a 2^K block. This defeats this symmetry-only route to small matrices, not all efficient measurements. Coarsening labels loses information in physical controls; no middle-band no-go or speedup follows."}

"""Radial pure-mask reduction and finite, non-certifying mask optimization."""

from functools import lru_cache
import itertools
import math

import numpy as np

from coset_mask_tail_fidelity import _regular_selector_model


def _probabilities(values):
    values = np.asarray(values, dtype=float)
    if (values.ndim != 1 or len(values) < 1 or not np.isfinite(values).all()
            or np.any(values < 0) or abs(values.sum()-1) > 1e-10):
        raise ValueError("finite nonnegative probability vector summing to one required")
    return values


def radialize_mask_probabilities(probabilities):
    p = _probabilities(probabilities)
    if len(p) < 2 or len(p) & (len(p)-1):
        raise ValueError("mask probability count must be a power of two >=2")
    k = len(p).bit_length()-1
    weights = np.bincount([s.bit_count() for s in range(len(p))], weights=p, minlength=k+1)
    return weights, np.array([weights[s.bit_count()]/math.comb(k, s.bit_count()) for s in range(len(p))])


def radial_probabilities(weight_probabilities):
    weights = _probabilities(weight_probabilities)
    if len(weights) < 2:
        raise ValueError("at least two weight probabilities required")
    k = len(weights)-1
    return np.array([weights[s.bit_count()]/math.comb(k, s.bit_count()) for s in range(2**k)])


def diagonal_mixture_instrument(mixture_weights, distributions):
    weights = _probabilities(mixture_weights)
    rows = np.array([_probabilities(row) for row in distributions])
    if rows.ndim != 2 or len(rows) != len(weights):
        raise ValueError("one equal-length distribution per mixture weight required")
    p = weights @ rows
    filters = np.zeros_like(rows)
    live = p > 0
    filters[:, live] = np.sqrt(weights[:, None]*rows[:, live]/p[live])
    # Complete the instrument on unused coordinates; all actual outputs vanish there.
    filters[0, ~live] = 1
    return p, filters


def schur_mask_distance(difference_blocks, probabilities):
    p = _probabilities(probabilities)
    delta = np.asarray(difference_blocks, dtype=complex)
    if (delta.ndim != 3 or delta.shape[1:] != (len(p), len(p)) or not np.isfinite(delta).all()
            or not np.allclose(delta, delta.conj().swapaxes(-1, -2), atol=1e-10, rtol=0)):
        raise ValueError("finite Hermitian source blocks matching the selector dimension required")
    return float(np.linalg.svd(delta*np.sqrt(p[:, None]*p[None, :]), compute_uv=False).sum()/2)


@lru_cache(maxsize=3, typed=True)
def physical_selector_schur_channel(copies, degree=3):
    """Actual regular-basis effects with every source and shared hidden member."""
    data, actions, projectors, _, effects, residuals = _regular_selector_model(copies, degree)
    d = len(actions)
    hidden = tuple(indices[0] for indices in data[8])
    sources = tuple(itertools.product(range(len(projectors)), repeat=copies))
    blocks = []
    for h in (None, *hidden):
        rho = np.eye(d)/d if h is None else (np.eye(d)+actions[h])/d
        conditional = []
        for source in sources:
            sigma = np.ones((1, 1))
            for j in source:
                sigma = np.kron(projectors[j] @ rho, sigma)
            conditional.append(np.einsum("stab,ba->st", effects, sigma))
        blocks.append(conditional)
    blocks = np.array(blocks)
    errors = dict(residuals,
        hermiticity=float(np.max(np.abs(blocks-blocks.conj().swapaxes(-1, -2)))),
        positivity=max(0.0, -float(np.linalg.eigvalsh(blocks).min())),
        trace_preservation=float(np.max(np.abs(np.diagonal(blocks, axis1=-2, axis2=-1).sum(axis=1)-1))))
    if max(errors.values()) > 1e-8:
        raise ArithmeticError("regular-basis source-labelled Schur channel is invalid")
    blocks.setflags(write=False)
    delta = blocks[1:].mean(axis=0)-blocks[0]
    delta.setflags(write=False)
    return {"blocks": blocks, "difference_blocks": delta, "sources": sources, "residuals": errors}


def _permuted_masks(copies, permutation):
    return np.array([sum(((s >> permutation[i]) & 1) << i for i in range(copies)) for s in range(2**copies)])


@lru_cache(maxsize=1)
def audit_selector_mask_symmetry():
    rng = np.random.default_rng(161803)
    controls = []
    for k in (2, 3):
        model = physical_selector_schur_channel(k)
        blocks, delta, sources = model["blocks"], model["difference_blocks"], model["sources"]
        index = {source: i for i, source in enumerate(sources)}
        size = 2**k
        permutations = list(itertools.permutations(range(k)))
        covariance = 0.0
        for permutation in permutations:
            masks = _permuted_masks(k, permutation)
            source_indices = [index[tuple(source[i] for i in permutation)] for source in sources]
            permuted = blocks[:, source_indices][:, :, masks][:, :, :, masks]
            covariance = max(covariance, float(np.max(np.abs(permuted-blocks))))
        probes = []
        inputs = [np.eye(size)[1]]+[rng.dirichlet(np.ones(size)) for _ in range(12)]
        for p in inputs:
            w, radial = radialize_mask_probabilities(p)
            distance = schur_mask_distance(delta, p)
            radial_distance = schur_mask_distance(delta, radial)
            alpha = np.sqrt(p)*np.exp(1j*rng.normal(size=size))
            phased_distance = float(np.linalg.svd(delta*np.outer(alpha, alpha.conjugate()), compute_uv=False).sum()/2)
            q = rng.dirichlet(np.ones(size))
            q[[0, -1]] = 0
            q /= q.sum()
            average, filters = diagonal_mixture_instrument([.37, .63], [p, q])
            instrument_error = float(np.max(np.abs((filters**2).sum(axis=0)-1)))
            average_output = blocks*np.sqrt(average[:, None]*average[None, :])
            for weight, child, f in zip((.37, .63), (p, q), filters):
                target = weight*blocks*np.sqrt(child[:, None]*child[None, :])
                instrument_error = max(instrument_error, float(np.max(np.abs(average_output*np.outer(f, f)-target))))
            child_distance = .37*distance+.63*schur_mask_distance(delta, q)
            concavity_gap = schur_mask_distance(delta, average)-child_distance
            if (covariance > 1e-8 or instrument_error > 1e-8 or abs(phased_distance-distance) > 1e-8
                    or radial_distance < distance-1e-8 or concavity_gap < -1e-8):
                raise ArithmeticError("mask phase, instrument, covariance or radial-domination check failed")
            probes.append({"input_distance": distance, "radial_distance": radial_distance,
                "radial_gain": radial_distance-distance, "weight_probabilities": w.tolist(),
                "phase_distance_residual": abs(phased_distance-distance),
                "concavity_gap": concavity_gap, "instrument_residual": instrument_error})
        controls.append({"copy_count": k, "source_tuple_count": len(sources),
            "hidden_members_checked": 3, "permutations_checked": len(permutations),
            "joint_permutation_covariance_residual": covariance, "probes": probes, "verified": True})
    return {"controls": controls, "verified": True, "source_adaptive_masks_covered": False,
        "uniform_mask_is_asserted_optimal": False, "cross_weight_coherence_discarded": False,
        "formal_proof_verification": False, "novelty_established": False}


def search_finite_radial_masks(copies):
    """Feasible finite witnesses only; SLSQP is not a global optimality certificate."""
    from scipy.optimize import minimize
    delta = physical_selector_schur_channel(copies)["difference_blocks"]
    uniform_weights = np.array([math.comb(copies, m)/2**copies for m in range(copies+1)])
    score = lambda w: schur_mask_distance(delta, radial_probabilities(w))
    starts = [uniform_weights, *np.eye(copies+1)]
    witnesses = [(score(w), w.copy()) for w in starts]
    converged = 0
    for start in starts:
        def objective(w):
            p = np.maximum(w, 0)
            return -score(p/p.sum()) if p.sum() else 0.0
        result = minimize(objective, start, method="SLSQP", bounds=[(0, 1)]*(copies+1),
            constraints=[{"type": "eq", "fun": lambda w: w.sum()-1}],
            options={"ftol": 1e-11, "maxiter": 120})
        converged += bool(result.success)
        if np.isfinite(result.x).all() and np.maximum(result.x, 0).sum() > 0:
            w = np.maximum(result.x, 0)
            w /= w.sum()
            witnesses.append((score(w), w))
    best, weights = max(witnesses, key=lambda item: item[0])
    return {"degree": 3, "copy_count": copies, "source_only_distance": score(np.eye(copies+1)[0]),
        "source_only_baseline_requires_quantum_frontend": True,
        "uniform_mask_distance": score(uniform_weights),
        "best_single_weight_distance": max(score(w) for w in np.eye(copies+1)),
        "best_observed_radial_distance": best, "best_observed_weight_probabilities": weights.tolist(),
        "optimizer_starts": len(starts), "optimizer_reports_converged": converged,
        "global_optimality_certified": False, "growing_degree_advantage_established": False,
        "efficient_final_measurement_supplied": False, "speedup_claim_allowed": False}


@lru_cache(maxsize=1)
def audit_low_occupation_support():
    """All physical entries, followed by rank-charged full-mask trace norms."""
    rng = np.random.default_rng(141421)
    controls = []
    for n, k in ((3, 2), (3, 3), (4, 2)):
        model = physical_selector_schur_channel(k, n)
        delta, blocks = model["difference_blocks"], model["blocks"]
        hidden_count = len(blocks)-1
        q0 = blocks[0, :, 0, 0].real
        qh = blocks[1, :, 0, 0].real
        joint_source_chi = float(np.sum((qh-q0)**2/q0))
        source_factor = 1+1/hidden_count
        if abs(joint_source_chi-(source_factor**k-1)) > 1e-9:
            raise ArithmeticError("unexpected physical source chi-square")
        size = 2**k
        squares = (np.abs(delta)**2/q0[:, None, None]).sum(axis=0)
        unions = np.array([[(s|t).bit_count() for t in range(size)] for s in range(size)])
        bounds = (1+(2.0**unions-1)/hidden_count)*source_factor**(k-unions)-1
        excess = float(np.max(squares-bounds))
        if excess > 1e-9:
            raise ArithmeticError("physical selector entry exceeded its active-union bound")
        probes = []
        for t in range(k+1):
            support = np.array([s for s in range(size) if s.bit_count() <= t])
            for weights in (np.full(len(support), 1/len(support)), rng.dirichlet(np.ones(len(support)))):
                p = np.zeros(size)
                p[support] = weights
                frobenius_square = float(p @ squares @ p)
                rank_bound = math.sqrt(len(support)*frobenius_square)/2
                distance = schur_mask_distance(delta, p)
                entry_bound = float(bounds[np.ix_(support, support)].max())
                if distance > rank_bound+1e-9 or frobenius_square > entry_bound+1e-9:
                    raise ArithmeticError("rank-charged low-weight mask bound failed")
                probes.append({"maximum_mask_weight": t, "support_size": len(support),
                    "total_distance": distance, "source_weighted_frobenius_squared": frobenius_square,
                    "rank_charged_trace_distance_upper_bound": rank_bound,
                    "largest_active_union_chi_square_bound": entry_bound})
        controls.append({"degree": n, "copy_count": k, "source_tuple_count": len(model["sources"]),
            "hidden_members_checked": hidden_count, "matrix_entries_checked": size*size,
            "largest_entry_bound_excess": excess, "probes": probes, "verified": True})
    return {"controls": controls, "verified": True, "formal_proof_verification": False,
        "independent_review": False, "novelty_established": False,
        "low_high_intersector_coherence_obstructed": False}


def low_occupation_scaling_controls():
    from isotypic_instruments import source_selector_low_occupation_contract
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
        source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
        physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True,
        declared_mask_weight_and_support_bounds_hold=True)
    return [source_selector_low_occupation_contract(n, n*n, n//4, **flags) for n in (128, 1024, 4096)]

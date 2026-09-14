"""Adversarial controls for a source-weighted environmental fidelity bound."""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import itertools
import math

import numpy as np

from coset_source_selector_quantum import _half_trace_norm, _prepend_tensor
from isotypic_instruments import source_selector_mask_tail_information_contract


def _positive_square_root(matrix):
    values, vectors = np.linalg.eigh((matrix+matrix.conj().T)/2)
    if values.min() < -1e-9:
        raise ArithmeticError("environment state is not positive")
    return (vectors*np.sqrt(np.maximum(values, 0))) @ vectors.conj().T


def _root_fidelity(first, second):
    return 2*_half_trace_norm(_positive_square_root(first) @ _positive_square_root(second))


def _span_failure(reference, other, target):
    vectors, singular, _ = np.linalg.svd(np.column_stack((reference, other)), full_matrices=False)
    basis = vectors[:, singular > 1e-12]
    return float(np.linalg.norm(basis.conj().T @ target)**2)


def _mask(copies, rule):
    indices = np.arange(2**copies)
    alpha = (1+indices/7)*np.exp(1j*(.31*indices+.13*indices**2))
    if rule == "high_asymmetric":
        alpha[[s for s in indices if int(s).bit_count() < copies-1]] = 0
    elif rule == "low_high_superposition":
        alpha[:] = 0
        alpha[0], alpha[-1] = math.sqrt(.3), 1j*math.sqrt(.7)
    elif rule != "complex_full":
        raise ValueError("unknown mask rule")
    return alpha/np.linalg.norm(alpha)


@lru_cache(maxsize=1)
def audit_environment_fidelity():
    """Use actual three-vector environments, including singular Gram matrices."""
    rng = np.random.default_rng(271828)
    controls = []
    for family in ("orthogonal", "complex", "nearly_collinear", "coincident"):
        local = []
        for j in range(2):
            vectors = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
            if family == "orthogonal":
                vectors = np.eye(3, dtype=complex)
            elif family in ("nearly_collinear", "coincident"):
                vectors[2] = vectors[0]+(1e-5 if family == "nearly_collinear" else 0)*vectors[2]
            vectors /= np.linalg.norm(vectors, axis=1)[:, None]
            local.append(vectors)
        q = np.array([Fraction(1, 1000), Fraction(999, 1000)], dtype=float)
        failures = np.array([_span_failure(e, v, u) for e, u, v in local])
        overlaps = np.array([abs(np.vdot(e, u))+abs(np.vdot(e, v))+abs(np.vdot(v, u)) for e, u, v in local])
        if np.any(failures > np.minimum(1, 2*overlaps)+1e-9):
            raise ArithmeticError("three-vector projection bound failed")
        a = min(1.0, float(q @ failures))
        endpoint_a = float(q @ np.array([abs(np.vdot(e, v))**2 for e, _, v in local]))
        k = 3
        for rule in ("high_asymmetric", "low_high_superposition", "complex_full"):
            alpha = _mask(k, rule)
            weights = np.abs(alpha)**2
            residual, bulk, endpoint = 0.0, np.zeros(k+1), np.zeros(k+1)
            for sources in itertools.product(range(2), repeat=k):
                mass = math.prod(q[j] for j in sources)
                branches = []
                for g in (0, 1, 2):
                    rows = []
                    for s in range(2**k):
                        vector = np.ones(1, dtype=complex)
                        for i, j in enumerate(sources):
                            vector = np.kron(local[j][g if s & (1 << i) else 0], vector)
                        rows.append(alpha[s]*vector)
                    branches.append(np.array(rows))
                u, v = branches[1:]
                cross_norm = 2*_half_trace_norm(u @ v.conj().T)
                fidelity = _root_fidelity(u.T @ u.conj(), v.T @ v.conj())
                residual = max(residual, abs(cross_norm-fidelity))
                for t in range(k+1):
                    keep = [s for s in range(2**k) if s.bit_count() >= t]
                    bulk[t] += mass*2*_half_trace_norm((u @ v.conj().T)[np.ix_(keep, keep)])
                    endpoint[t] += mass*2*_half_trace_norm((branches[0] @ v.conj().T)[np.ix_(keep, keep)])
            tails = []
            for t in range(k+1):
                retained = [s for s in range(2**k) if s.bit_count() >= t]
                m = float(weights[retained].sum())
                bulk_bound = math.sqrt(m*sum(weights[s]*a**s.bit_count() for s in retained))
                endpoint_bound = math.sqrt(m*sum(weights[s]*endpoint_a**s.bit_count() for s in retained))
                if bulk[t] > bulk_bound+1e-8 or endpoint[t] > endpoint_bound+1e-8:
                    raise ArithmeticError("source-averaged mask-tail fidelity bound failed")
                tails.append({"minimum_weight": t, "lower_tail_mass": max(0.0, 1-m),
                    "bulk_cross_norm": float(bulk[t]), "bulk_fidelity_upper_bound": bulk_bound,
                    "endpoint_cross_norm": float(endpoint[t]), "endpoint_fidelity_upper_bound": endpoint_bound})
            if residual > 1e-7:
                raise ArithmeticError("partial-trace norm differs from environmental root fidelity")
            controls.append({"family": family, "mask": rule, "copy_count": k,
                "source_probabilities": q.tolist(), "root_fidelity_identity_residual": residual,
                "source_averaged_failure": a, "endpoint_source_averaged_failure": endpoint_a,
                "tails": tails, "verified": True})
    return {"controls": controls, "verified": True, "formal_proof_verification": False,
        "is_quantum_algorithm_experiment": False}


@lru_cache(maxsize=3, typed=True)
def _regular_selector_model(copies, degree=3):
    """Shared regular-basis effects, not a reduced character-kernel calculation."""
    from coset_binary_carrier_instruments import _source_parity_group_data
    if type(copies) is not int or type(degree) is not int or (degree, copies) not in ((3, 2), (3, 3), (4, 2)):
        raise ValueError("physical mask controls require S3 with two/three copies or S4 with two copies")
    data = _source_parity_group_data(degree, 1 if degree == 3 else 2)
    d, product = len(data[0]), data[7]
    actions = np.eye(d)[product]
    p = data[3][:, None]*data[2]/d
    projectors = p[:, product]
    rng = np.random.default_rng(314159)
    hamiltonian = np.einsum("g,gab->ab", rng.normal(size=d)+1j*rng.normal(size=d), actions)
    spectrum, vectors = np.linalg.eigh((hamiltonian+hamiltonian.conj().T)/2)
    unitary = (vectors*np.exp(.73j*spectrum)) @ vectors.conj().T
    coefficients = unitary[:, 0]
    size = 2**copies
    queries = []
    for s in range(size):
        query = np.zeros((d**copies, d**copies), dtype=complex)
        for g in range(d):
            term = np.ones((1, 1))
            for i in range(copies):
                term = np.kron(actions[g] if s & (1 << i) else np.eye(d), term)
            query += coefficients[g]*term
        queries.append(query)
    effects = np.array([[other.conj().T @ query for other in queries] for query in queries])
    residuals = {"regular_unitary": float(np.linalg.norm(unitary.conj().T @ unitary-np.eye(d))),
        "every_mask_unitary": max(float(np.linalg.norm(q.conj().T @ q-np.eye(d**copies))) for q in queries)}
    return data, actions, projectors, coefficients, effects, residuals


@lru_cache(maxsize=6)
def arbitrary_mask_physical_control(copies, rule):
    """Independent S3 regular-basis channel; enumerate ORDERED source tuples."""
    data, actions, projectors, coefficients, effects, model_residuals = _regular_selector_model(copies)
    alpha = _mask(copies, rule)
    d, product, size = len(actions), data[7], 2**copies
    outer = np.outer(coefficients.conjugate(), coefficients).reshape(-1)
    walsh = np.array([[(-1)**((s & z).bit_count()) for z in range(size)] for s in range(size)])/math.sqrt(size)
    preparations = np.array([alpha*np.array([(-1)**((s & z).bit_count()) for s in range(size)]) for z in range(size)])
    residuals = {**model_residuals,
        "physical_channel": 0.0, "comparison_preparation_channel": 0.0, "natural_mass": 0.0,
        "positivity": 0.0}
    mixture_distances = np.zeros(3)
    walsh_distances = np.zeros(3)
    actual_distances = np.zeros(3)
    decision = wrong_multiset_decision = 0.0
    hidden = tuple(indices[0] for indices in data[8])
    for sources in itertools.product(range(len(projectors)), repeat=copies):
        actual, mixtures, laws = [], [], []
        for h in (None, *hidden):
            rho = np.eye(d)/d if h is None else (np.eye(d)+actions[h])/d
            sigma = np.ones((1, 1))
            tensor = np.ones((d*d, 1, 1), dtype=complex)
            positive = np.ones((d, 1, 1), dtype=complex)
            for j in sources:
                local_state = projectors[j] @ rho
                sigma = np.kron(local_state, sigma)
                values = np.einsum("ab,gba->g", local_state, actions)
                kernel = np.zeros((d, d, 2, 2), dtype=complex)
                kernel[:, :, 0, 0] = values[0]
                kernel[:, :, 0, 1] = values[data[6], None]
                kernel[:, :, 1, 0] = values[None, :]
                kernel[:, :, 1, 1] = values[product]
                tensor = _prepend_tensor(tensor, kernel.reshape(d*d, 2, 2))
                f = np.zeros((d, 2, 2), dtype=complex)
                f[:, 0, 0] = f[:, 1, 1] = values[0]/2
                f[:, 0, 1] = f[:, 1, 0] = values/2
                positive = _prepend_tensor(positive, f)
            physical = np.einsum("stab,ba->st", effects, sigma)*np.outer(alpha, alpha.conjugate())
            predicted = np.einsum("g,gab->ab", outer, tensor)*np.outer(alpha, alpha.conjugate())
            right = None if h is None else product[data[6], h]
            w = np.abs(coefficients if h is None else coefficients+coefficients[right])**2/(1 if h is None else 2)
            uniform_q = np.einsum("g,gab->ab", w, positive)
            law = np.diag(walsh @ uniform_q @ walsh.T).real
            prepared = np.einsum("z,za,zb->ab", law, preparations, preparations.conjugate())
            q_alpha = size*uniform_q*np.outer(alpha, alpha.conjugate())
            residuals["physical_channel"] = max(residuals["physical_channel"], float(np.linalg.norm(physical-predicted)))
            residuals["comparison_preparation_channel"] = max(residuals["comparison_preparation_channel"], float(np.linalg.norm(prepared-q_alpha)))
            residuals["natural_mass"] = max(residuals["natural_mass"], float(abs(np.trace(physical)-np.trace(sigma))))
            residuals["positivity"] = max(residuals["positivity"], -float(np.linalg.eigvalsh(physical).min()), -float(law.min()))
            actual.append(physical)
            mixtures.append(q_alpha)
            laws.append(law)
        block_decision = _half_trace_norm(np.mean(actual[1:], axis=0)-actual[0])
        decision += block_decision
        if sources == tuple(sorted(sources)):
            multiplicity = math.factorial(copies)//math.prod(math.factorial(c) for c in Counter(sources).values())
            wrong_multiset_decision += multiplicity*block_decision
        for b in range(3):
            mixture_distances[b] += _half_trace_norm(mixtures[b+1]-mixtures[0])
            walsh_distances[b] += float(np.abs(laws[b+1]-laws[0]).sum()/2)
            actual_distances[b] += _half_trace_norm(actual[b+1]-actual[0])
    if max(residuals.values()) > 1e-8 or np.any(mixture_distances > walsh_distances+1e-9):
        raise ArithmeticError("arbitrary-mask physical channel or comparison contraction failed")
    return {"degree": 3, "copy_count": copies, "mask": rule,
        "ordered_source_tuples_evaluated": len(projectors)**copies, "hidden_members_evaluated": len(hidden),
        "physical_decision_trace_distance": decision, "individual_trace_distances": actual_distances.tolist(),
        "unjustified_unpermuted_source_multiset_estimate": wrong_multiset_decision,
        "positive_comparison_trace_distances": mixture_distances.tolist(),
        "walsh_comparison_trace_distances": walsh_distances.tolist(),
        "uniform_overlap": float(1/(size*np.max(np.abs(alpha)**2))),
        "source_multiset_compression_used": False, "residuals": residuals, "verified": True,
        "speedup_claim_allowed": False, "novelty_established": False}


def mask_tail_scaling_controls():
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
        only_source_records_and_selector_qubits_retained=True, physical_inputs_discarded=True,
        mask_fixed_before_inputs_and_source_records=True)
    return [source_selector_mask_tail_information_contract(n, n*n, None, weight*n,
        mask_lower_tail_probability_upper_bound=pi, **flags)
        for n in (1024, 4096) for weight, pi in ((3, Fraction(0)), (3, Fraction(1, 2**n)), (0, Fraction(0)))]

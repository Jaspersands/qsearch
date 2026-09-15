"""Physical low/high cross-block controls, with high-side coefficient orientation."""

from fractions import Fraction
from functools import lru_cache
import math

import numpy as np

from coset_mask_symmetry import physical_selector_schur_channel, schur_mask_distance
from coset_mask_tail_fidelity import _regular_selector_model
from isotypic_instruments import source_selector_occupation_band_contract


def _double_character_column(values, sources, first, second, coefficients, inverse, products):
    """Rows are high-side g', columns low-side g; no endpoint subtraction."""
    order = len(coefficients)
    factors = np.ones((len(sources), order, order))
    for i in range(sources.shape[1]):
        local = values[sources[:, i]]
        in_first, in_second = bool(first & (1 << i)), bool(second & (1 << i))
        if in_first and in_second:
            factors *= local[:, products]
        elif in_first:
            factors *= local[:, None, :]
        elif in_second:
            factors *= local[:, inverse, None]
        else:
            factors *= local[:, 0, None, None]
    return factors * np.outer(coefficients.conjugate(), coefficients)[None, :, :]


@lru_cache(maxsize=1)
def audit_overlap_decay_counterexample():
    """Exact S6 moments: a shared active site may be identity, not decaying."""
    from coset_binary_carrier_instruments import _source_parity_group_data
    data = _source_parity_group_data(6, 3)
    order, hidden = len(data[0]), [int(h[0]) for h in data[8]]
    p = [[Fraction(int(d)*int(chi), order) for chi in row] for d, row in zip(data[3], data[2])]
    q0 = [row[0] for row in p]
    v = hidden[0]
    controls = []
    for h, translated in zip(hidden, data[8]):
        if h == v:
            continue
        qh = [row[0]+row[h] for row in p]
        moment = [row[v]+row[int(translated[v])] for row in p]
        source_square = sum(q*q/q0j for q, q0j in zip(qh, q0))
        exclusive_square = sum(x*x/q0j for x, q0j in zip(moment, q0))
        # S={0}, T={0,1}, g'=g=v: the shared factor R(v)^dagger R(v) is I.
        actual = source_square*exclusive_square
        invalid = exclusive_square**2
        if not 0 < invalid < actual or exclusive_square > Fraction(4, 15):
            raise ArithmeticError("declared overlap-decay counterexample did not separate")
        controls.append({"hidden_index": h, "shared_group_element": v,
            "exclusive_factor_squared_norm": str(exclusive_square),
            "actual_two_site_squared_norm": str(actual),
            "incorrect_shared_site_decay_prediction": str(invalid)})
    return {"degree": 6, "controls": controls, "verified": True,
        "shared_sites_may_be_counted_as_high_only_decay": False,
        "interpretation": "A nonzero coefficient of the valid unitary (I+i R(v))/sqrt(2); not a separate oracle candidate."}


@lru_cache(maxsize=1)
def audit_cross_sector_coherence():
    rng = np.random.default_rng(173205)
    controls = []
    for n, k in ((3, 2), (3, 3), (4, 2)):
        model = physical_selector_schur_channel(k, n)
        data, actions, projectors, a, _, _ = _regular_selector_model(k, n)
        blocks, delta = model["blocks"], model["difference_blocks"]
        sources = np.array(model["sources"])
        d, hidden = len(a), [h[0] for h in data[8]]
        m_class = len(hidden)
        q0 = blocks[0, :, 0, 0].real
        p = np.einsum("jab,gba->jg", projectors, actions).real/d
        empty_conjugate = a.sum().conjugate()
        envelope = (1+1/m_class)**k
        minimum_class = min(d//int(np.sum(data[2][:, g]**2)) for g in range(1, d))
        rows = []
        reconstruction = endpoint_error = 0.0
        for s in range(2**k):
            for t in range(2**k):
                if t.bit_count() <= s.bit_count():
                    continue
                rebuilt, off = [], []
                for eta, translated in enumerate((None, *data[8])):
                    values = p if translated is None else p+p[:, translated]
                    terms = _double_character_column(values, sources, s, t, a, data[6], data[7])
                    rebuilt.append(terms.sum(axis=(1, 2)))
                    low_column = blocks[eta, :, s, 0]/empty_conjugate
                    endpoint_error = max(endpoint_error,
                        float(np.max(np.abs(terms[:, 0, :].sum(axis=1)-a[0].conjugate()*low_column))))
                    keep = np.ones(d, dtype=bool)
                    keep[0] = False
                    if translated is not None:
                        h = translated[0]
                        endpoint_error = max(endpoint_error,
                            float(np.max(np.abs(terms[:, h, :].sum(axis=1)-a[h].conjugate()*low_column))))
                        keep[h] = False
                    off.append(terms[:, keep, :].sum(axis=(1, 2)))
                rebuilt, off = np.array(rebuilt), np.array(off)
                reconstruction = max(reconstruction, float(np.max(np.abs(rebuilt-blocks[:, :, s, t]))))
                low = blocks[:, :, s, 0]/empty_conjugate
                terms = {"low_column": a[0].conjugate()*(low[1:].mean(axis=0)-low[0]),
                    "hidden_endpoint": (a[hidden].conjugate()[:, None]*low[1:]).mean(axis=0),
                    "alternative_off_endpoint": off[1:].mean(axis=0), "null_off_endpoint": -off[0]}
                reconstruction = max(reconstruction, float(np.max(np.abs(sum(terms.values())-delta[:, s, t]))))
                weight, high_only = s.bit_count(), (t & ~s).bit_count()
                bounds = {"low_column": math.sqrt((1+(2**weight-1)/m_class)*(1+1/m_class)**(k-weight)-1),
                    "hidden_endpoint": math.sqrt(envelope/m_class),
                    "alternative_off_endpoint": d*math.sqrt(envelope)*min(1, 4/minimum_class)**(high_only/2),
                    "null_off_endpoint": d*min(1, 1/minimum_class)**(high_only/2)}
                norms = {name: float(np.sqrt(np.sum(np.abs(term)**2/q0))) for name, term in terms.items()}
                if any(norms[name] > bound+1e-8 for name, bound in bounds.items()):
                    raise ArithmeticError("cross-sector coefficient norm bound failed")
                rows.append({"low_subset": s, "high_subset": t, "shared_sites": (s&t).bit_count(),
                    "high_only_sites": high_only, "component_norms": norms, "component_upper_bounds": bounds})
        probes = []
        for low_weight in range(k):
            for high_weight in range(low_weight+1, k+1):
                left = np.array([s for s in range(2**k) if s.bit_count() <= low_weight])
                right = np.array([s for s in range(2**k) if s.bit_count() >= high_weight])
                pl, ph = rng.dirichlet(np.ones(len(left))), rng.dirichlet(np.ones(len(right)))
                p_left, p_right = np.zeros(2**k), np.zeros(2**k)
                p_left[left], p_right[right] = pl, ph
                dl, dh = schur_mask_distance(delta, p_left), schur_mask_distance(delta, p_right)
                for weight in (0.0, .3, .5, 1.0):
                    probability = weight*p_left+(1-weight)*p_right
                    distance = schur_mask_distance(delta, probability)
                    pinched = weight*dl+(1-weight)*dh
                    cross = delta[:, left][:, :, right]*np.sqrt(weight*(1-weight)*pl[:, None]*ph[None, :])
                    cross_norm = float(np.linalg.svd(cross, compute_uv=False).sum())
                    frobenius_square = float(np.sum(np.abs(cross)**2/q0[:, None, None]))
                    rank_bound = math.sqrt(len(left)*frobenius_square)
                    if distance < pinched-1e-8 or distance-pinched > cross_norm+1e-8 or cross_norm > rank_bound+1e-8:
                        raise ArithmeticError("cross-block pinching, rank or source Cauchy check failed")
                    probes.append({"low_weight": low_weight, "high_weight": high_weight,
                        "low_probability": weight, "low_support_size": len(left),
                        "full_distance": distance, "pinched_distance": pinched,
                        "intersector_gain": distance-pinched, "cross_block_trace_norm": cross_norm,
                        "rank_charged_cross_upper_bound": rank_bound})
        if max(reconstruction, endpoint_error) > 1e-8:
            raise ArithmeticError("independent double-character expansion or endpoint identity failed")
        controls.append({"degree": n, "copy_count": k, "source_tuple_count": len(sources),
            "hidden_members_checked": m_class, "double_character_reconstruction_residual": reconstruction,
            "high_side_endpoint_identity_residual": endpoint_error, "rows": rows, "probes": probes, "verified": True})
    return {"controls": controls, "overlap_counterexample": audit_overlap_decay_counterexample(),
        "verified": True, "formal_proof_verification": False, "independent_review": False,
        "novelty_established": False, "all_arbitrary_masks_obstructed": False}


def occupation_band_scaling_controls():
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
        source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
        physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True)
    return [source_selector_occupation_band_contract(n, n*n, n//4, 3*n,
        middle_mass_upper_bound=pi, **flags) for n, pi in ((128, 0), (1024, 0), (4096, 0),
            (4096, Fraction(1, 2**4096)), (4096, Fraction(1, 4)))]

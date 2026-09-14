"""Empty-subset coherence controls for the fixed common-query architecture."""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import math

import numpy as np

from coset_mask_symmetry import physical_selector_schur_channel, schur_mask_distance
from coset_mask_tail_fidelity import _regular_selector_model
from isotypic_instruments import source_selector_vacuum_coherence_contract


@lru_cache(maxsize=1)
def audit_source_character_squares():
    """Exact full-label equality and coarse-label inequality, not sampled rows."""
    from coset_binary_carrier_instruments import _source_parity_group_data
    from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type
    controls = []
    for n, transpositions in ((3, 1), (4, 2), (6, 3)):
        data = _source_parity_group_data(n, transpositions)
        group, partitions, characters, dimensions = data[:4]
        order = len(group)
        class_sizes = Counter(permutation_cycle_type(g) for g in group)
        hidden_index = int(data[8][0][0])
        for rule in ("full_irreps", "character_sign_coarsening", "all_irreps_merged"):
            if rule == "full_irreps":
                categories = [[i] for i in range(len(partitions))]
            elif rule == "all_irreps_merged":
                categories = [list(range(len(partitions)))]
            else:
                categories = [[i for i in range(len(partitions)) if (data[4][i] < 0) == sign]
                              for sign in (False, True)]
                categories = [category for category in categories if category]
            q0 = [Fraction(sum(int(dimensions[i])**2 for i in category), order) for category in categories]
            weighted = []
            for g in range(order):
                p = [Fraction(sum(int(dimensions[i])*int(characters[i, g]) for i in category), order)
                     for category in categories]
                value = sum(x*x/q for x, q in zip(p, q0))
                bound = Fraction(1, class_sizes[permutation_cycle_type(group[g])])
                if value > bound or (rule == "full_irreps" and value != bound):
                    raise ArithmeticError("source-weighted character column bound failed")
                weighted.append(value)
            controls.append({"degree": n, "partition_rule": rule, "categories": len(categories),
                "group_elements_checked": order, "class_size": len(data[8]),
                "source_chi_square": str(weighted[hidden_index]),
                "source_chi_square_upper_bound": str(Fraction(1, len(data[8]))),
                "category_count_penalty_required": False, "verified": True})
    return {"controls": controls, "verified": True, "exact_arithmetic": True}


@lru_cache(maxsize=1)
def audit_vacuum_coherence():
    """Compare character expansion with actual U_t^dagger U_s physical effects."""
    rng = np.random.default_rng(577215)
    controls = []
    for k in (2, 3):
        model = physical_selector_schur_channel(k)
        data, actions, projectors, coefficients, _, _ = _regular_selector_model(k)
        blocks, delta, sources = model["blocks"], model["difference_blocks"], model["sources"]
        d, size, hidden_count = len(actions), 2**k, len(data[8])
        p = np.einsum("jab,gba->jg", projectors, actions).real/d
        q0 = p[:, 0]
        qh = q0+p[:, data[8][0][0]]
        q0_joint = np.prod(q0[np.array(sources)], axis=1)
        qh_joint = np.prod(qh[np.array(sources)], axis=1)
        v = float(np.sum((qh-q0)**2/q0))
        source_distance = float(np.abs(qh_joint-q0_joint).sum()/2)
        reconstruction_error = mass_error = 0.0
        empty_phase = coefficients.sum()
        off_terms = np.zeros((hidden_count+1, len(sources), size), dtype=complex)
        minimum_class = min(d//int(np.sum(data[2][:, g]**2)) for g in range(1, d))
        # The column (S,0), not row (0,S), uses a_g and conjugate(empty_phase).
        for eta, translated in enumerate((None, *data[8])):
            values = p if translated is None else p+p[:, translated]
            probabilities = values[:, 0]
            joint = np.prod(probabilities[np.array(sources)], axis=1)
            expected_mass = q0_joint if translated is None else qh_joint
            mass_error = max(mass_error, float(np.max(np.abs(joint-expected_mass))))
            for s in range(size):
                factors = np.ones((len(sources), d))
                for i in range(k):
                    labels = np.array(sources)[:, i]
                    factors *= values[labels] if s & (1 << i) else probabilities[labels, None]
                column = empty_phase.conjugate()*(factors @ coefficients)
                reconstruction_error = max(reconstruction_error,
                    float(np.max(np.abs(column-blocks[eta, :, s, 0]))))
                keep = np.ones(d, dtype=bool)
                keep[0] = False
                if translated is not None:
                    keep[translated[0]] = False
                off_terms[eta, :, s] = factors[:, keep] @ coefficients[keep]
        rows = []
        for s in range(1, size):
            m = s.bit_count()
            value = float(np.sum(np.abs(delta[:, s, 0])**2/q0_joint))
            compressed_chi_square = (1+(2**m-1)/hidden_count)*(1+v)**(k-m)-1
            if value > compressed_chi_square+1e-9:
                raise ArithmeticError("vacuum row exceeded compressed-input chi-square bound")
            terms = {"source_mass": coefficients[0]*(qh_joint-q0_joint),
                "hidden_endpoint": np.mean(coefficients[[h[0] for h in data[8]]])*qh_joint,
                "alternative_off_subgroup": off_terms[1:, :, s].mean(axis=0),
                "null_off_identity": -off_terms[0, :, s]}
            reconstruction_error = max(reconstruction_error, float(np.max(np.abs(
                empty_phase.conjugate()*sum(terms.values())-delta[:, s, 0]))))
            norms = {name: float(np.sqrt(np.sum(np.abs(term)**2/q0_joint))) for name, term in terms.items()}
            envelope = (1+v)**k
            bounds = {"source_mass": math.sqrt(envelope-1), "hidden_endpoint": math.sqrt(envelope/hidden_count),
                "alternative_off_subgroup": math.sqrt(d*(1+v)**(k-m))*(4/minimum_class)**(m/2),
                "null_off_identity": math.sqrt(d)*(1/minimum_class)**(m/2)}
            if any(norms[name] > bound+1e-9 for name, bound in bounds.items()):
                raise ArithmeticError("vacuum coefficient decomposition exceeded a weighted-source bound")
            rows.append({"subset": s, "subset_weight": m, "weighted_row_squared_norm": value,
                "compressed_input_chi_square_upper_bound": compressed_chi_square,
                "coefficient_component_norms": norms, "coefficient_component_upper_bounds": bounds})
        probes = []
        row_squares = np.array([row["weighted_row_squared_norm"] for row in rows])
        for w0 in (0.0, .1, .5, .9, 1.0):
            for nonempty in (np.eye(size-1)[-1], rng.dirichlet(np.ones(size-1))):
                probabilities = np.r_[w0, (1-w0)*nonempty]
                beta_distance = schur_mask_distance(delta, np.r_[0, nonempty])
                distance = schur_mask_distance(delta, probabilities)
                dephased = w0*source_distance+(1-w0)*beta_distance
                cross_norm = math.sqrt(w0*(1-w0))*float(
                    np.sqrt((np.abs(delta[:, 1:, 0])**2) @ nonempty).sum())
                jensen = math.sqrt(w0*(1-w0)*float(nonempty @ row_squares))
                gain = distance-dephased
                if gain < -1e-9 or gain > cross_norm+1e-9 or cross_norm > jensen+1e-9:
                    raise ArithmeticError("vacuum pinching or weighted-source Jensen bound failed")
                probes.append({"vacuum_probability": w0, "total_distance": distance,
                    "vacuum_dephased_distance": dephased, "nonempty_distance": beta_distance,
                    "vacuum_coherence_gain": gain, "cross_block_half_trace_norm": cross_norm,
                    "source_weighted_jensen_upper_bound": jensen})
        if max(reconstruction_error, mass_error) > 1e-8:
            raise ArithmeticError("physical empty-subset column or natural source masses disagree")
        controls.append({"degree": 3, "copy_count": k, "source_tuple_count": len(sources),
            "hidden_members_checked": hidden_count, "character_reconstruction_residual": reconstruction_error,
            "class_invariant_source_mass_residual": mass_error, "source_chi_square": v,
            "source_only_distance": source_distance, "rows": rows, "probes": probes, "verified": True})
    return {"controls": controls, "verified": True, "formal_proof_verification": False,
        "independent_review": False, "novelty_established": False,
        "nonempty_mask_information_obstructed": False, "speedup_claim_allowed": False}


def vacuum_coherence_scaling_controls():
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
        source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
        physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True)
    return [source_selector_vacuum_coherence_contract(n, n*n, **flags) for n in (16, 128, 1024, 4096)]

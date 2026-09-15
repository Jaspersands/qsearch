"""All-mask cross-channel hybrid bound for low coefficient-mass common queries."""

from fractions import Fraction
from functools import lru_cache
import itertools
import math

import numpy as np

from coset_mask_symmetry import physical_selector_schur_channel
from coset_mask_tail_fidelity import regular_selector_query_control
from coset_selector_schur import _batch_kron, _source_kernels
from isotypic_instruments import source_selector_coefficient_mass_contract


def exact_shifted_character_square_audit():
    from coset_binary_carrier_instruments import _source_parity_group_data
    rows = []
    for n, t in ((3, 1), (4, 2), (6, 3)):
        data = _source_parity_group_data(n, t)
        d, r, m = len(data[0]), len(data[1]), len(data[8])
        centralizers = np.sum(data[2]**2, axis=0)
        if sum(int(c) for c in centralizers) != r*d:
            raise ArithmeticError("full-group inverse-class-size sum is not the number of classes")
        averages = [Fraction(sum(int(centralizers[h[x]]) for h in data[8]), m*d) for x in range(d)]
        cap = Fraction(r, m)
        if max(averages) > cap:
            raise ArithmeticError("shifted hidden-class character-square average exceeded the full-group cap")
        rows.append({"degree": n, "shifts_checked": d, "hidden_members_checked": m,
            "class_count": r, "exact_maximum_shifted_square_average": str(max(averages)),
            "exact_full_group_cap": str(cap), "verified": True})
    return rows


def involution_rotation_word(data, word):
    """Exact Gaussian-integer numerator for product (I+i R(v))/sqrt(2)."""
    d, inverse, products = len(data[0]), data[6], data[7]
    word = tuple(word)
    if any(type(v) is not int or not 0 < v < d or inverse[v] != v for v in word):
        raise ValueError("word requires declared nonidentity involution indices")
    coefficients = [(0, 0)]*d
    coefficients[0] = (1, 0)
    for v in word:
        updated = coefficients.copy()
        for g, (real, imag) in enumerate(coefficients):
            target = products[inverse[v], g]
            before = updated[target]
            updated[target] = (before[0]-imag, before[1]+real)
        coefficients = updated
    scale_squared = 1 << len(word)
    if sum(a*a+b*b for a, b in coefficients) != scale_squared:
        raise ArithmeticError("rotation word lost exact canonical coefficient l2 normalization")
    return {"gaussian_integer_coefficients": coefficients, "normalization_squared": scale_squared,
        "word_length": len(word), "support_size": sum(bool(a or b) for a, b in coefficients),
        "coefficient_l1_squared_upper_bound": scale_squared,
        "arbitrary_gate_count_lower_bound": False}


def _cross_map_apply(kernel, operator):
    reference = operator.shape[0]//2
    return (kernel[:, :, None, :, None]*operator.reshape(2, reference, 2, reference)[None]).reshape(len(kernel), 2*reference, 2*reference)


def exact_single_irrep_reflection_controls():
    from coset_binary_carrier_instruments import _source_parity_group_data
    controls = []
    for n, t in ((3, 1), (4, 2), (6, 3)):
        data = _source_parity_group_data(n, t)
        order, characters, dimensions = len(data[0]), data[2], data[3]
        for target, lam in enumerate(data[1]):
            dimension = int(dimensions[target])
            numerator = [-2*dimension*int(x) for x in characters[target]]
            numerator[0] += order
            spectrum = [Fraction(sum(a*int(chi) for a, chi in zip(numerator, row)), order*int(d))
                for row, d in zip(characters, dimensions)]
            mass = Fraction(sum(abs(a) for a in numerator), order)
            if spectrum != [Fraction(-1 if j == target else 1) for j in range(len(dimensions))]:
                raise ArithmeticError("canonical coefficients do not implement the specified irrep reflection")
            if sum(a*a for a in numerator) != order*order or mass > 1+2*dimension:
                raise ArithmeticError("irrep reflection exceeded its Parseval or coefficient-l1 bound")
            sign = lam == (1,)*n
            if sign and mass != 3-Fraction(4, order):
                raise ArithmeticError("sign-reflection coefficient mass is not 3-4/|G|")
            controls.append({"degree": n, "target_partition": list(lam), "target_dimension": dimension,
                "exact_coefficient_l1": str(mass), "exact_squared_coefficient_l1": str(mass*mass),
                "coefficient_l1_upper_bound": 1+2*dimension, "is_sign_irrep": sign,
                "is_missing_harmonic_for_this_hidden_class": int(characters[target, data[8][0][0]]) == -dimension,
                "verified": True})
    return controls


@lru_cache(maxsize=1)
def audit_coefficient_mass_channel_bound():
    rng = np.random.default_rng(223607)
    cross_controls = []
    for n in (3, 4):
        data, actions, projectors, _, _ = regular_selector_query_control(n)
        d, hidden = len(actions), [h[0] for h in data[8]]
        p = data[3][:, None]*data[2]/d
        kernels, errors = [], {"cross_isometry": 0.0, "physical_kernel": 0.0, "ancilla_contractivity": 0.0,
            "entrywise_difference_bound": 0.0}
        for h in (None, *hidden):
            root = np.eye(d)/math.sqrt(d) if h is None else (np.eye(d)+actions[h])/math.sqrt(2*d)
            carrier = np.empty((d, len(p), 2, d, d), dtype=complex)
            for g in range(d):
                carrier[g, :, 0] = projectors @ root
                carrier[g, :, 1] = actions[g] @ carrier[g, :, 0]
            errors["cross_isometry"] = max(errors["cross_isometry"], float(np.max(np.abs(np.sum(np.abs(carrier)**2, axis=(1, 3, 4))-1))))
            physical = np.einsum("gjsab,ujtab->ugjst", carrier, carrier.conjugate())
            values = p if h is None else p+p[:, data[8][hidden.index(h)]]
            expected = _source_kernels(values, data[6], data[7]).transpose(1, 0, 2, 3).reshape(d, d, len(p), 2, 2)
            errors["physical_kernel"] = max(errors["physical_kernel"], float(np.max(np.abs(physical-expected))))
            kernels.append(expected)
        for _ in range(24):
            gp, g = rng.integers(0, d, size=2)
            x = rng.normal(size=(6, 6))+1j*rng.normal(size=(6, 6))
            x /= np.linalg.svd(x, compute_uv=False).sum()
            for eta, kernel in enumerate(kernels):
                result = _cross_map_apply(kernel[gp, g], x)
                norm = float(np.linalg.svd(result, compute_uv=False).sum())
                errors["ancilla_contractivity"] = max(errors["ancilla_contractivity"], norm-1)
                if eta:
                    delta = kernel[gp, g]-kernels[0][gp, g]
                    measured = float(np.linalg.svd(_cross_map_apply(delta, x), compute_uv=False).sum())
                    upper = float(np.abs(delta).sum())
                    errors["entrywise_difference_bound"] = max(errors["entrywise_difference_bound"], measured-upper)
        if max(errors.values()) > 1e-8:
            raise ArithmeticError("cross-isometry, kernel, reference-ancilla or local hybrid check failed")
        cross_controls.append({"degree": n, "group_pairs_checked": d*d, "hidden_members_checked": len(hidden),
            "ancilla_operator_probes": 24*(len(hidden)+1), "errors": errors, "verified": True})

    tensor_controls = []
    for n, k in ((3, 2), (3, 3), (4, 2)):
        data, _, _, a, _ = regular_selector_query_control(n)
        model = physical_selector_schur_channel(k, n)
        p = data[3][:, None]*data[2]/len(a)
        kernels = [_source_kernels(p if h is None else p+p[:, h], data[6], data[7]) for h in (None, *data[8])]
        coefficients = np.outer(a.conjugate(), a).reshape(-1)
        residual = telescoping = 0.0
        for index, source in enumerate(model["sources"]):
            products = []
            for kernel in kernels:
                tensor = np.ones((len(a)**2, 1, 1), dtype=complex)
                for j in source:
                    tensor = _batch_kron(kernel[j], tensor)
                products.append(tensor)
            reconstructed = np.array([np.einsum("g,gab->ab", coefficients, row) for row in products])
            residual = max(residual, float(np.max(np.abs(reconstructed-model["blocks"][:, index]))))
            for eta in range(1, len(kernels)):
                summed = np.zeros_like(products[0])
                for pivot in range(k):
                    tensor = np.ones((len(a)**2, 1, 1), dtype=complex)
                    for i, j in enumerate(source):
                        local = kernels[eta][j]-kernels[0][j] if i == pivot else kernels[eta if i < pivot else 0][j]
                        tensor = _batch_kron(local, tensor)
                    summed += tensor
                telescoping = max(telescoping, float(np.max(np.abs(summed-(products[eta]-products[0])))))
        if max(residual, telescoping) > 1e-8:
            raise ArithmeticError("fixed-shared-hidden tensor expansion or telescoping identity failed")
        tensor_controls.append({"degree": n, "copy_count": k, "source_tuples_checked": len(model["sources"]),
            "physical_reconstruction_residual": residual, "tensor_telescoping_residual": telescoping, "verified": True})
    words = []
    for n in (3, 4):
        data, actions, _, _, _ = regular_selector_query_control(n)
        generators = [int(x[0]) for x in data[8]]
        for length in (0, 1, 2, 5, 8):
            word = [generators[i % len(generators)] for i in range(length)]
            row = involution_rotation_word(data, word)
            a = np.array([complex(x, y) for x, y in row["gaussian_integer_coefficients"]])/math.sqrt(row["normalization_squared"])
            unitary = np.einsum("g,gab->ab", a, actions)
            direct = np.eye(len(a), dtype=complex)
            for v in word:
                direct = (np.eye(len(a))+1j*actions[v]) @ direct/math.sqrt(2)
            residual = float(np.max(np.abs(unitary-direct)))
            mass = float(np.abs(a).sum()**2)
            if residual > 1e-8 or mass > min(row["support_size"], row["coefficient_l1_squared_upper_bound"])+1e-8:
                raise ArithmeticError("typed query word exceeded its canonical coefficient-mass certificate")
            words.append({"degree": n, "word_length": length, "exact_support": row["support_size"],
                "actual_coefficient_l1_squared": mass, "word_coefficient_l1_squared_upper_bound": row["coefficient_l1_squared_upper_bound"],
                "physical_word_residual": residual, "verified": True})
    return {"cross_channel_controls": cross_controls, "tensor_controls": tensor_controls,
        "shifted_character_square_controls": exact_shifted_character_square_audit(), "word_controls": words,
        "single_irrep_reflection_controls": exact_single_irrep_reflection_controls(),
        "scaling_controls": coefficient_mass_scaling_controls(), "verified": True,
        "all_fixed_mask_coefficient_mass_bound_derived": True,
        "all_common_queries_nontrivially_obstructed": False, "classical_sampler_supplied": False,
        "formal_proof_verification": False, "independent_review": False, "novelty_established": False,
        "research_update": "A cross-channel diamond-norm hybrid bound gives E_h T<=2 K (sum_g |a_g|)^2 sqrt(p(n)/M) for every fixed selector state in the common-query physical-discard model. Polynomial-support queries and single polynomial-dimensional irrep reflections are obstructed across ALL weight bands; the sign reflection has coefficient-l1 norm 3-4/|G| despite being dense. Products of q involutory group rotations have squared mass <=2^q, giving an obstruction for q<=(1/4-epsilon)n log2 n at polynomial copies. Larger-mass dense queries and source adaptation remain open; coefficient mass is not a general circuit lower bound. Derived/review-pending, not a speedup or classical sampler."}


def coefficient_mass_scaling_controls():
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
        source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
        physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True,
        declared_coefficient_mass_bound_holds=True)
    return [dict(source_selector_coefficient_mass_contract(n, n*n, bound, **flags), query_family=family)
        for n in (128, 512, 1024) for family, bound in (("support_at_most_n_squared", n*n),
            ("n_involutory_rotations", 1 << n), ("one_eighth_n_log_n_rotations", 1 << (n*(n.bit_length()-1)//8)),
            ("generic_dense_unitary_bound", math.factorial(n)), ("single_sign_irrep_reflection", 9))]

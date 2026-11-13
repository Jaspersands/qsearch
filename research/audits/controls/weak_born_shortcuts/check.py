#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Three exact, scoped shortcut falsifiers; no sampling simulation or sweep."""

import hashlib
import json
import sys
import time
from pathlib import Path

from sage.all import (AA, QQ, SR, PolynomialRing, QuadraticField,
                      diagonal_matrix, identity_matrix, matrix, vector)
from sage.version import version as SAGE_VERSION


def matrix_strings(value):
    return [[str(x) for x in row] for row in value.rows()]


def projected_partition_control():
    lam = QQ(1) / 10
    identity = identity_matrix(QQ, 2)
    z = diagonal_matrix(QQ, [1, -1])
    x = matrix(QQ, [[0, 1], [1, 0]])
    h = -z.tensor_product(identity) - identity.tensor_product(z) + lam * x.tensor_product(x)
    field = QuadraticField(401, "sqrt401", embedding=AA(401).sqrt())
    root = field.gen()
    r = root / 10
    ground = vector(field, [r + 2, 0, 0, -lam])
    norm2 = ground.dot_product(ground)
    assert h.change_ring(field) * ground == -r * ground
    actual_probability = ground[3] ** 2 / norm2
    expected_probability = (1 - 2 / r) / 2
    assert actual_probability == expected_probability
    assert AA(actual_probability) > 0
    assert AA(r) > lam > 0
    ring = PolynomialRing(QQ, "t")
    t = ring.gen()
    expected_charpoly = (t * t - QQ(401) / 100) * (t * t - lam * lam)
    assert ring(h.charpoly()) == expected_charpoly
    compressed = h.matrix_from_rows_and_columns([2, 3], [2, 3])
    assert compressed == diagonal_matrix(QQ, [0, 2])
    assert compressed.charpoly().roots(QQ) == [(QQ(2), 1), (QQ(0), 1)] or set(compressed.eigenvalues()) == {QQ(0), QQ(2)}
    return {
        "status": "PASS", "basis_order": ["00", "01", "10", "11"],
        "lambda": str(lam), "hamiltonian": matrix_strings(h),
        "characteristic_polynomial": str(expected_charpoly),
        "ground_energy": "-sqrt(401)/10",
        "ground_vector_before_normalization": [str(v) for v in ground],
        "ground_squared_norm": str(norm2),
        "first_bit_one_probability_exact": str(actual_probability),
        "first_bit_one_probability_formula": "(1 - 20/sqrt(401))/2",
        "first_bit_one_probability_strictly_positive": True,
        "compressed_first_bit_one_hamiltonian": matrix_strings(compressed),
        "compressed_lowest_energy": "0",
        "projected_partition_ratio": "(1+exp(-2*beta))/(2*cosh(sqrt(401)*beta/10)+2*cosh(beta/10))",
        "ratio_upper_bound_for_beta_nonnegative": "2*exp(-sqrt(401)*beta/10)",
        "ratio_limit_beta_to_infinity": "0",
        "limit_justification": "The numerator is at most 2 and the denominator includes exp(sqrt(401)*beta/10).",
        "scope": "Replacing the true projected Gibbs mass by the compressed-Hamiltonian partition ratio fails.",
    }


def negative_norm_polymer_control():
    a = QQ(1) / 32
    psi = vector(QQ, [1, -a, -a, 0])
    s = 1 + 2 * a * a
    h0 = diagonal_matrix(QQ, [-2, 0, 0, 2])
    energy = -2 / s
    w = (h0 - energy * identity_matrix(QQ, 4)) * psi
    assert psi.dot_product(psi) == s
    assert psi.dot_product(w) == 0
    perturbation = -(w.column() * psi.row() + psi.column() * w.row()) / s
    lam = 4 * a
    native_term = perturbation / lam
    h = h0 + perturbation
    assert perturbation == perturbation.transpose()
    assert native_term.base_ring() is QQ
    assert h * psi == energy * psi
    operator_norm_squared = 8 * a * a / (s * s)
    ring = PolynomialRing(QQ, "t")
    t = ring.gen()
    assert ring(perturbation.charpoly()) == t * t * (t * t - operator_norm_squared)
    assert perturbation.rank() == 2
    native_norm_squared = operator_norm_squared / (lam * lam)
    assert native_norm_squared == 1 / (2 * s * s) < 1
    operator_norm = AA(operator_norm_squared).sqrt()
    # Weyl: the second eigenvalue is at least 0-||V||.  The displayed
    # eigenvalue is strictly below it, so it is the unique ground energy.
    assert AA(energy) < -operator_norm
    weyl_gap_lower_bound = -operator_norm - AA(energy)
    assert weyl_gap_lower_bound > 0
    roots = h.charpoly().roots(QQ)
    eigenvalues = sorted([value for value, multiplicity in roots for _ in range(multiplicity)])
    assert len(eigenvalues) == 4
    assert eigenvalues == sorted([energy, -4 * a * a / s, QQ(0), QQ(2)])
    assert eigenvalues[0] == energy < eigenvalues[1]

    creation = matrix(QQ, [[0, 0], [1, 0]])
    identity = identity_matrix(QQ, 2)
    create1 = creation.tensor_product(identity)
    create2 = identity.tensor_product(creation)
    c = a * create1 + a * create2 + a * a * create1 * create2
    assert c ** 3 == 0
    vacuum = vector(QQ, [1, 0, 0, 0])
    exponential_state = (identity_matrix(QQ, 4) - c + (c * c) / 2) * vacuum
    assert exponential_state == psi
    normalized_projector = psi.column() * psi.row() / s
    assert normalized_projector.trace() == 1
    assert normalized_projector ** 2 == normalized_projector
    assert h * normalized_projector == energy * normalized_projector

    # The four paired partitions of {1,2}; the single/single cover is
    # disconnected.  No positivity assumption is inserted.
    partitions = [("one_block", -a * a), ("two_singletons", a * a)]
    paired_covers = []
    connected_weight = QQ(0)
    all_weight = QQ(0)
    for ket_name, ket_amplitude in partitions:
        for bra_name, bra_amplitude in partitions:
            contribution = ket_amplitude * bra_amplitude
            connected = ket_name == "one_block" or bra_name == "one_block"
            all_weight += contribution
            if connected:
                connected_weight += contribution
            paired_covers.append({"ket_partition": ket_name, "bra_partition": bra_name,
                                  "connected": connected, "weight": str(contribution)})
    assert connected_weight == -a ** 4 < 0
    assert all_weight == 0 == psi[3] ** 2
    reconstructed_norm = 1 + a * a + a * a + a ** 4 + connected_weight
    assert reconstructed_norm == s
    return {
        "status": "PASS", "a": str(a), "lambda": str(lam),
        "unnormalized_psi": [str(v) for v in psi], "squared_norm_s": str(s),
        "normalized_state_convention": "psi/sqrt(s); the creation ansatz itself has vacuum amplitude 1.",
        "normalized_density_matrix": matrix_strings(normalized_projector),
        "ground_energy": str(energy), "w": [str(v) for v in w],
        "perturbation_V": matrix_strings(perturbation),
        "native_rational_h_equals_V_over_lambda": matrix_strings(native_term),
        "V_operator_norm_squared": str(operator_norm_squared),
        "h_operator_norm_squared": str(native_norm_squared), "h_operator_norm_strictly_below_one": True,
        "H_times_psi_equals_E_times_psi": True,
        "Weyl_unique_ground_certificate": "E < -||V|| <= second_eigenvalue(H)",
        "Weyl_gap_lower_bound_exact": "(1024-32*sqrt(2))/513",
        "exact_spectrum": [str(v) for v in eigenvalues],
        "exact_spectral_gap": str(eigenvalues[1] - eigenvalues[0]),
        "creation_coefficients": {"C1": str(a), "C2": str(a), "C12": str(a * a)},
        "exp_minus_C_vacuum_exactly_equals_psi": True,
        "paired_covers_on_12": paired_covers,
        "connected_paired_cover_weight": str(connected_weight),
        "complete_12_weight": str(all_weight),
        "norm_reconstructed_from_connected_weights": str(reconstructed_norm),
        "scope": "The direct connected paired-cover norm expansion need not have nonnegative polymer weights, even for this bounded rational perturbation.",
    }


def amplitude_damping_control():
    eta, theta = SR.var("eta theta")
    root = eta.sqrt()
    complement_root = (1 - eta).sqrt()
    # Input-major/output-minor Choi order: 00,01,10,11.  These are the
    # vectorized Kraus operators diag(1,sqrt(eta)) and sqrt(1-eta)|0><1|.
    v0 = vector(SR, [1, 0, 0, root])
    v1 = vector(SR, [0, 0, complement_root, 0])
    choi = v0.column() * v0.row() + v1.column() * v1.row()
    expected_choi = matrix(SR, [[1, 0, 0, root], [0, 0, 0, 0],
                                [0, 0, 1 - eta, 0], [root, 0, 0, eta]])
    assert choi == expected_choi
    reset_choi = diagonal_matrix(SR, [1, 0, 1, 0])
    partial_trace = matrix(SR, 2, 2, lambda i, j: sum(choi[2 * i + a, 2 * j + a] for a in range(2)))
    assert partial_trace == identity_matrix(SR, 2)
    residual = choi - theta * reset_choi
    minor = residual.matrix_from_rows_and_columns([0, 3], [0, 3])
    expected_minor = matrix(SR, [[1 - theta, root], [root, eta]])
    assert minor == expected_minor
    determinant = minor.det().expand()
    assert determinant == -theta * eta
    return {
        "status": "PASS", "parameter_domain": "0 < eta <= 1, theta > 0",
        "choi_convention": "Unnormalized Choi matrix, input-major/output-minor order 00,01,10,11; partial trace over output is I.",
        "amplitude_damping_choi": matrix_strings(choi),
        "reset_to_zero_choi": matrix_strings(reset_choi),
        "residual_choi": matrix_strings(residual),
        "principal_indices": [0, 3], "principal_minor": matrix_strings(minor),
        "principal_minor_determinant": str(determinant),
        "strictly_negative_on_parameter_domain": True,
        "scope": "No positive reset-to-|0> fraction can be subtracted while retaining complete positivity; not a no-go for other decompositions or samplers.",
    }


def main():
    start = time.monotonic()
    result = {"status": "PASS", "scope": "Three prescribed exact shortcut controls only; no all-input sampler conclusion.",
              "projected_partition": projected_partition_control(),
              "negative_norm_polymer": negative_norm_polymer_control(),
              "amplitude_damping_reset": amplitude_damping_control()}
    script = Path(__file__).resolve()
    source = script.parents[2] / "sources" / "dissipative_selection" / "weak_ground.txt"
    result.update({"python_executable": sys.executable, "sage_version": SAGE_VERSION,
                   "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                   "creation_ansatz_source": str(source), "creation_ansatz_source_lines": [260, 324],
                   "creation_ansatz_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                   "elapsed_seconds": round(time.monotonic() - start, 6)})
    destination = script.with_name("result.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)
    print("FULL_RESULT_PATH " + str(destination), flush=True)


if __name__ == "__main__":
    main()

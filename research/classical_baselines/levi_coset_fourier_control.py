#!/opt/anaconda3/bin/python
"""One exact p=3, n=3 Levi-coset Fourier/membership diagnostic.

Enumerates H only for analysis. It performs neither quantum execution nor
native recovery of H, and p=3 is below the proposed p>=128*n threshold.
"""

import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"


def run_control():
    from sage.all import GF, QQ, CyclotomicField, VectorSpace, identity_matrix, matrix, zero_matrix, vector

    started = time.perf_counter()
    p, n, r, s = 3, 3, 2, 1
    F = GF(p)
    I = identity_matrix(F, n)
    S = matrix(F, [[1, 1, 0], [0, 1, 1], [1, 0, 0]])
    Sinv = S.inverse()
    mixing = matrix(F, [[1, 0, 1], [0, 1, 0], [1, 0, 2]])
    g = S * mixing * Sinv
    ginv = g.inverse()
    V = VectorSpace(F, n)
    U = V.subspace([S.column(0), S.column(1)])
    W = V.subspace([S.column(2)])
    Wperp = matrix(F, [S.column(2)]).right_kernel()
    assert U.dimension() == 2 and W.dimension() == 1 and (U + W).dimension() == 3

    def encode(M):
        return [[int(value) for value in row] for row in M.rows()]

    def encode_basis(space):
        return [[int(value) for value in row] for row in space.basis()]

    def key(M):
        return tuple(int(value) for value in M.list())

    def elementary(i, j):
        E = zero_matrix(F, n)
        E[i, j] = 1
        return E

    canonical_H = []
    for entries in itertools.product(range(p), repeat=4):
        A = matrix(F, 2, 2, entries)
        if not A.is_invertible():
            continue
        for scalar in (1, 2):
            h = zero_matrix(F, n)
            for i in range(2):
                for j in range(2):
                    h[i, j] = A[i, j]
            h[2, 2] = scalar
            canonical_H.append(h)
    H = [S * h * Sinv for h in canonical_H]
    Hkeys = {key(h) for h in H}
    assert len(H) == len(Hkeys) == 96
    conjugate_keys = {key(g * h * ginv) for h in H}
    assert conjugate_keys != Hkeys
    normalizer_counterexample = next(h for h in H if key(g * h * ginv) not in Hkeys)
    right_coset = [h * ginv for h in H]
    uninverted_coset = [g * h for h in H]

    block_positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)]
    off_positions = [(0, 2), (1, 2), (2, 0), (2, 1)]
    algebra_basis = [S * elementary(i, j) * Sinv for i, j in block_positions]
    off_basis = [S * elementary(i, j) * Sinv for i, j in off_positions]
    matrix_space = VectorSpace(F, n * n)
    algebra = matrix_space.subspace([vector(F, A.list()) for A in algebra_basis])
    right_annihilator = matrix_space.subspace([vector(F, (g * B).list()) for B in off_basis])
    uninverted_annihilator = matrix_space.subspace([vector(F, (B * ginv).list()) for B in off_basis])
    assert algebra.dimension() == 5
    assert right_annihilator.dimension() == uninverted_annihilator.dimension() == 4
    assert all((B * A).trace() == 0 for B in off_basis for A in algebra_basis)
    # Four basis checks certify every frequency in each entire 4D
    # annihilator by trace linearity; this is not a full 3^9-point FFT.
    assert all(((g * B) * x).trace() == 0 for B in off_basis for x in right_coset)
    assert all(((B * ginv) * x).trace() == 0 for B in off_basis for x in uninverted_coset)

    roots = CyclotomicField(3)
    zeta = roots.gen()

    def exact_amplitude(B, coset):
        counts = [0, 0, 0]
        for x in coset:
            counts[int((B * x).trace())] += 1
        phase_sum = sum((count * zeta**j for j, count in enumerate(counts)), roots(0))
        square = QQ(phase_sum * phase_sum.conjugate()) / (len(H) * p ** (n * n))
        return {
            "trace_pairing": "tr(B*x), without a transpose",
            "trace_residue_counts_0_1_2": counts,
            "exact_phase_sum": str(phase_sum),
            "normalized_amplitude": str(phase_sum) + "/sqrt(96*3^9)",
            "normalized_squared_amplitude": str(square),
            "all_96_phases_equal_one": counts == [96, 0, 0],
        }

    fixed_CD = [([1, 0], [1, 0]), ([0, 1], [0, 1]), ([1, 1], [1, 2])]
    frequency_controls = []
    wrong_orientation_witness = None
    for C, D in fixed_CD:
        off = zero_matrix(F, n)
        off[0, 2], off[1, 2] = C
        off[2, 0], off[2, 1] = D
        assert matrix(F, 2, 1, C).rank() == matrix(F, 1, 2, D).rank() == 1
        original = S * off * Sinv
        B_right = g * original
        B_uninverted = original * ginv
        kernel_right = B_right.right_kernel()
        kernel_uninverted_transpose = B_uninverted.transpose().right_kernel()
        assert kernel_right.dimension() == kernel_uninverted_transpose.dimension() == 1
        correct_right = all(v in U for v in kernel_right.basis())
        correct_uninverted = all(v in Wperp for v in kernel_uninverted_transpose.basis())
        assert correct_right and correct_uninverted
        amp_right = exact_amplitude(B_right, right_coset)
        amp_uninverted = exact_amplitude(B_uninverted, uninverted_coset)
        assert amp_right["all_96_phases_equal_one"] and amp_uninverted["all_96_phases_equal_one"]
        wrong_kernel = B_uninverted.right_kernel()
        wrong_dual_kernel = B_right.transpose().right_kernel()
        wrong_kernel_contained = all(v in U for v in wrong_kernel.basis())
        wrong_dual_contained = all(v in Wperp for v in wrong_dual_kernel.basis())
        row = {
            "C": C, "D": D, "right_coset_frequency": encode(B_right),
            "uninverted_coset_frequency": encode(B_uninverted),
            "right_frequency_kernel_basis": encode_basis(kernel_right),
            "right_kernel_contained_in_U": bool(correct_right),
            "uninverted_frequency_transpose_kernel_basis": encode_basis(kernel_uninverted_transpose),
            "uninverted_transpose_kernel_contained_in_Wperp": bool(correct_uninverted),
            "right_coset_amplitude": amp_right, "uninverted_coset_amplitude": amp_uninverted,
            "wrong_uninverted_plain_kernel_basis": encode_basis(wrong_kernel),
            "wrong_uninverted_plain_kernel_contained_in_U": bool(wrong_kernel_contained),
            "wrong_right_transpose_kernel_basis": encode_basis(wrong_dual_kernel),
            "wrong_right_transpose_kernel_contained_in_Wperp": bool(wrong_dual_contained),
        }
        frequency_controls.append(row)
        if wrong_orientation_witness is None and not wrong_kernel_contained:
            wrong_orientation_witness = {
                "C": C, "D": D,
                "uninverted_plain_kernel_basis": encode_basis(wrong_kernel),
                "not_contained_in_U": True,
                "right_transpose_kernel_basis": encode_basis(wrong_dual_kernel),
                "not_contained_in_Wperp": not wrong_dual_contained,
            }
    assert wrong_orientation_witness is not None
    single_probability = QQ(len(H)) / p ** (n * n)
    annihilator_size = p**4
    beta = annihilator_size * single_probability
    full_rank_count = (p**2 - 1) ** 2
    conditional_full_rank = QQ(full_rank_count) / annihilator_size
    good_full_rank_mass = beta * conditional_full_rank
    assert beta == QQ(32) / 81 and conditional_full_rank == QQ(64) / 81
    assert good_full_rank_mass == QQ(2048) / 6561
    outside_B = g * S * elementary(0, 0) * Sinv
    assert vector(F, outside_B.list()) not in right_annihilator
    outside_frequency_control = exact_amplitude(outside_B, right_coset)
    assert outside_frequency_control["normalized_squared_amplitude"] != "0"

    def algebra_member(X):
        return vector(F, X.list()) in algebra

    def H_member(Y):
        # Analysis-only implementation of testing f(Y)=f(I) on GL_3.
        assert Y.is_invertible()
        return key(Y) in Hkeys

    fixed_rank_one = [
        ([1, 0, 0], [1, 0, 0]), ([0, 1, 0], [0, 1, 0]),
        ([1, 0, 0], [0, 1, 0]), ([0, 1, 0], [1, 0, 0]),
        # Two explicit positive controls: a rank-one map within U, and
        # a rank-one map onto W whose covector annihilates U.
        ([1, 1, 0], [1, 0, 0]), ([0, 1, 0], [1, 2, 2]),
    ]
    membership_controls = []
    for u_values, phi_values in fixed_rank_one:
        u = vector(F, u_values)
        phi = vector(F, phi_values)
        X = u.column() * phi.row()
        assert X.rank() == 1
        admissible = [t for t in (1, 2) if (I + t * X).is_invertible()]
        checks = []
        for t in admissible:
            observed = H_member(I + t * X)
            expected = algebra_member(X)
            assert observed == expected
            checks.append({"t": t, "I_plus_tX_in_H": observed, "X_in_A": bool(expected)})
        assert admissible  # p=3 permits a nonzero t for every rank-one X.
        membership_controls.append({"u": u_values, "phi": phi_values,
                                    "admissible_nonzero_t": admissible, "checks": checks})
    assert any(row["checks"][0]["X_in_A"] for row in membership_controls)
    assert any(not row["checks"][0]["X_in_A"] for row in membership_controls)

    def transvection_certificate(candidate_basis):
        candidate_inverse = candidate_basis.inverse()
        tests = []
        for i, j in ((0, 1), (1, 0)):
            transvection = I + candidate_basis * elementary(i, j) * candidate_inverse
            assert transvection.is_invertible()
            tests.append({"i": i, "j": j, "membership": H_member(transvection)})
        return {"tests": tests, "accept": all(test["membership"] for test in tests)}

    true_certificate = transvection_certificate(S)
    wrong_basis = S * (I + elementary(2, 0))
    wrong_U = V.subspace([wrong_basis.column(0), wrong_basis.column(1)])
    wrong_W = V.subspace([wrong_basis.column(2)])
    assert (wrong_U + wrong_W).dimension() == 3 and wrong_U != U
    wrong_certificate = transvection_certificate(wrong_basis)
    assert true_certificate["accept"] and not wrong_certificate["accept"]

    output = {
        "scope": "Finite exact algebra/classical membership diagnosis only. H enumeration is ANALYSIS ONLY; no quantum execution or native H-recovery, and p=3 fails p>=128*n.",
        "p": p, "n": n, "r": r, "s": s, "proposed_prime_threshold": 128 * n,
        "S": encode(S), "g": encode(g), "H_order": len(H),
        "g_normalizes_H": False, "normalizer_counterexample_h": encode(normalizer_counterexample),
        "U_basis": encode_basis(U), "W_basis": encode_basis(W), "Wperp_basis": encode_basis(Wperp),
        "algebra_dimension": int(algebra.dimension()), "algebra_density_in_all_matrices": str(QQ(1) / p**4),
        "right_annihilator_dimension": int(right_annihilator.dimension()),
        "uninverted_annihilator_dimension": int(uninverted_annihilator.dimension()),
        "annihilator_flatness_basis_trace_checks": 2 * 4 * len(H),
        "annihilator_number_frequencies": annihilator_size,
        "exact_squared_amplitude_per_annihilator_frequency": str(single_probability),
        "exact_annihilator_mass_beta": str(beta),
        "full_rank_C_D_frequency_count_inside_annihilator": full_rank_count,
        "conditional_full_rank_C_D_probability": str(conditional_full_rank),
        "joint_annihilator_and_full_rank_mass": str(good_full_rank_mass),
        "residual_mass_outside_annihilator": str(1 - beta),
        "full_Fourier_support_is_claimed_4_dimensional": False,
        "outside_nonzero_frequency_control": outside_frequency_control,
        "fixed_frequency_controls": frequency_controls,
        "wrong_orientation_witness": wrong_orientation_witness,
        "fixed_rank_one_membership_controls": membership_controls,
        "true_pair_transvection_certificate": true_certificate,
        "fixed_wrong_complementary_pair_basis": encode(wrong_basis),
        "wrong_pair_transvection_certificate": wrong_certificate,
        "worker_seconds": time.perf_counter() - started,
    }
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"artifact": str(artifact), "H_order": len(H), "annihilator_mass": str(beta),
                      "conditional_full_rank": str(conditional_full_rank), "joint_good_mass": str(good_full_rank_mass),
                      "wrong_orientation_found": True, "rank_one_controls": len(membership_controls),
                      "true_certificate": true_certificate["accept"], "wrong_certificate": wrong_certificate["accept"],
                      "worker_seconds": output["worker_seconds"]}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run([SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"], check=True, timeout=30)
    else:
        raise SystemExit("Usage: levi_coset_fourier_control.py")

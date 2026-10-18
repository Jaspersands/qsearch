"""DCP multi-copy Schur-Weyl symmetric-subspace projection and classical r-sample majority bridge.

Extends Subsystem 59 from 2-copy Bell measurements to r-copy symmetric subspace
projections Pi_{Sym^r} on single-qubit DCP phase states rho(theta, gamma)^{tensor r}
with theta = 2*pi * <a, s> / q and visibility gamma in [0, 1], and compares
collective Schur-Weyl measurements against classical r-sample majority/likelihood decoding:

1. Exact Secret-Independent Symmetric Projection Weight:
   In the r-qubit computational basis, the (r + 1)-dimensional symmetric subspace
   Sym^r(C^2) is spanned by the normalized Dicke states
       |D_w^{(r)}> = C(r, w)^{-1/2} sum_{x in {0,1}^r : wt(x) == w} |x>,   w in {0, ..., r}.
   Because the diagonal phase unitary U(theta)^{tensor r} commutes with all qubit
   permutations pi in S_r, the symmetric projection probability is strictly independent
   of the secret phase theta (and s) for every r >= 1 and gamma in [0, 1]:
       P(Sym^r | theta, gamma) = Tr(Pi_{Sym^r} rho(theta, gamma)^{tensor r})
                               = sum_{k=0}^r ((1 + gamma)/2)^{r - k} ((1 - gamma)/2)^k.
   At r = 2, P(Sym^2 | theta, gamma) = (3 + gamma^2) / 4 = 1 - P(Psi^-), recovering
   Subsystem 59's singlet purity estimator.

2. Half-Period Commuting Regime (theta in {0, pi}) — Classical r-Sample Majority Optimality:
   For any half-period DCP distinguishability task (theta = 0 vs theta = pi),
   rho(0, gamma) and rho(pi, gamma) commute and are simultaneously diagonal in the
   single-copy X basis {|+>, |->}. Consequently:
     - The exact 2^r x 2^r collective quantum Helstrom trace distance equals the
       classical r-sample Binomial majority/likelihood total-variation distance:
           D_tr(rho(0, gamma)^{tensor r}, rho(pi, gamma)^{tensor r})
               = D_TV(Binomial(r, (1 + gamma)/2), Binomial(r, (1 - gamma)/2)).
     - Unentangled single-copy X measurements followed by classical r-sample majority
       voting are 100% quantum-optimal across all collective POVMs.
     - Postselecting onto Sym^r(C^2) when r >= 3 and 0 < gamma < 1 strictly discards
       non-zero trace-distance signal carried by the mixed-symmetry Schur-Weyl sectors.

3. Non-Commuting Quadrature Regime (theta = pi/2) & Dicke Harmonic Readout vs. Header Collision Cost:
   - Inside Sym^r(C^2), the extreme Dicke coherence observable
         O_{GHZ}^{(r)} = |D_0^{(r)}><D_r^{(r)}| + |D_r^{(r)}><D_0^{(r)}|
     has expectation Tr(O_{GHZ}^{(r)} rho(theta, gamma)^{tensor r}) = 2^{-(r-1)} gamma^r cos(r * theta)
     (compared to gamma^r cos^r(theta) for X^{tensor r}), which is matched without entangling
     gates by the signed mean of random even-Y-weight separable Pauli strings.
   - For non-commuting hypotheses theta = 0 vs theta = pi/2 on r >= 2 identical headers,
     collective Schur-Weyl Helstrom measurement strictly exceeds any fixed single-copy
     measurement basis followed by classical r-sample likelihood decoding (e.g. at r = 2,
     gamma = 0.8: collective trace distance 0.649934 vs optimal fixed-basis 2-sample TV
     distance gamma / sqrt(2) = 0.565685), but requires r copies sharing the exact same
     public header a_1 = ... = a_r in Z_q^n (birthday pool cost Omega(Q^{(r-1)/r})).
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_multicopy_schur_weyl_symmetric_projection_bridge"
SCHEMA_VERSION = "dcp-multicopy-schur-weyl-symmetric-projection-bridge-v1"

ComplexMatrix = List[List[complex]]


def _validate_r_and_gamma(r_copies: int, gamma: float) -> None:
    if type(r_copies) is not int or not 1 <= r_copies <= 6:
        raise ValueError("r_copies must be an integer in [1, 6]")
    if not math.isfinite(gamma) or not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must be a finite number in [0, 1]")


def single_copy_density_matrix(theta: float, gamma: float) -> ComplexMatrix:
    """Return the 2x2 density matrix rho(theta, gamma) in the computational basis."""
    if not math.isfinite(theta):
        raise ValueError("theta must be finite")
    if not math.isfinite(gamma) or not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must be in [0, 1]")
    off = 0.5 * gamma * cmath.exp(-1j * theta)
    return [[0.5 + 0j, off], [off.conjugate(), 0.5 + 0j]]


def _kron(a_mat: ComplexMatrix, b_mat: ComplexMatrix) -> ComplexMatrix:
    ra, ca = len(a_mat), len(a_mat[0])
    rb, cb = len(b_mat), len(b_mat[0])
    out: ComplexMatrix = [[0j] * (ca * cb) for _ in range(ra * rb)]
    for i1 in range(ra):
        for j1 in range(ca):
            aij = a_mat[i1][j1]
            for i2 in range(rb):
                row = i1 * rb + i2
                for j2 in range(cb):
                    out[row][j1 * cb + j2] = aij * b_mat[i2][j2]
    return out


def _matmul(a_mat: ComplexMatrix, b_mat: ComplexMatrix) -> ComplexMatrix:
    n = len(a_mat)
    m = len(b_mat[0])
    k_len = len(b_mat)
    out: ComplexMatrix = [[0j] * m for _ in range(n)]
    for i in range(n):
        for k in range(k_len):
            aik = a_mat[i][k]
            if aik == 0j:
                continue
            for j in range(m):
                out[i][j] += aik * b_mat[k][j]
    return out


def _trace_prod(a_mat: ComplexMatrix, b_mat: ComplexMatrix) -> complex:
    n = len(a_mat)
    acc = 0j
    for i in range(n):
        for k in range(n):
            acc += a_mat[i][k] * b_mat[k][i]
    return acc


def _frobenius_norm_commutator(a_mat: ComplexMatrix, b_mat: ComplexMatrix) -> float:
    ab = _matmul(a_mat, b_mat)
    ba = _matmul(b_mat, a_mat)
    n = len(a_mat)
    acc = 0.0
    for i in range(n):
        for j in range(n):
            diff = ab[i][j] - ba[i][j]
            acc += (diff.real ** 2) + (diff.imag ** 2)
    return math.sqrt(acc)


def r_copy_tensor_density_matrix(theta: float, gamma: float, r_copies: int) -> ComplexMatrix:
    """Construct the explicit 2^r x 2^r density matrix rho(theta, gamma)^{tensor r}."""
    _validate_r_and_gamma(r_copies, gamma)
    rho_1 = single_copy_density_matrix(theta, gamma)
    rho_r = rho_1
    for _ in range(r_copies - 1):
        rho_r = _kron(rho_r, rho_1)
    return rho_r


def dicke_basis_vectors(r_copies: int) -> List[List[complex]]:
    """Return the r + 1 normalized Dicke states |D_w^{(r)}> (w = 0, ..., r) in C^{2^r}."""
    if type(r_copies) is not int or not 1 <= r_copies <= 8:
        raise ValueError("r_copies must be an integer in [1, 8]")
    dim = 1 << r_copies
    basis: List[List[complex]] = []
    for w in range(r_copies + 1):
        vec = [0j] * dim
        norm = math.sqrt(float(math.comb(r_copies, w)))
        for x in range(dim):
            if bin(x).count("1") == w:
                vec[x] = complex(1.0 / norm, 0.0)
        basis.append(vec)
    return basis


def symmetric_subspace_projector(r_copies: int) -> ComplexMatrix:
    """Construct the explicit 2^r x 2^r orthogonal projector Pi_{Sym^r} onto Sym^r(C^2)."""
    vecs = dicke_basis_vectors(r_copies)
    dim = 1 << r_copies
    proj: ComplexMatrix = [[0j] * dim for _ in range(dim)]
    for v in vecs:
        for i in range(dim):
            vi = v[i]
            if vi == 0j:
                continue
            for j in range(dim):
                proj[i][j] += vi * v[j].conjugate()
    return proj


def symmetric_projection_probability_closed_form(r_copies: int, gamma: float) -> float:
    """Closed-form symmetric projection weight sum_{k=0}^r ((1+gamma)/2)^{r-k} ((1-gamma)/2)^k."""
    _validate_r_and_gamma(r_copies, gamma)
    p_plus = 0.5 * (1.0 + gamma)
    p_minus = 0.5 * (1.0 - gamma)
    return sum((p_plus ** (r_copies - k)) * (p_minus ** k) for k in range(r_copies + 1))


def verify_symmetric_projection_secret_independence(
    r_copies: int,
    gamma: float,
    test_thetas: Sequence[float],
) -> Dict[str, Any]:
    """Verify that Tr(Pi_{Sym^r} rho(theta, gamma)^{tensor r}) matches the closed form and is independent of theta."""
    _validate_r_and_gamma(r_copies, gamma)
    if not test_thetas:
        raise ValueError("test_thetas must be non-empty")
    proj = symmetric_subspace_projector(r_copies)
    cf_prob = symmetric_projection_probability_closed_form(r_copies, gamma)

    explicit_probs: List[float] = []
    for th in test_thetas:
        rho_r = r_copy_tensor_density_matrix(float(th), gamma, r_copies)
        prob = _trace_prod(proj, rho_r).real
        explicit_probs.append(prob)

    max_formula_err = max(abs(p - cf_prob) for p in explicit_probs)
    max_theta_spread = max(explicit_probs) - min(explicit_probs)

    return {
        "r_copies": r_copies,
        "gamma": gamma,
        "symmetric_subspace_dimension": r_copies + 1,
        "full_hilbert_dimension": 1 << r_copies,
        "closed_form_probability": cf_prob,
        "explicit_probabilities": explicit_probs,
        "max_formula_error": max_formula_err,
        "max_theta_spread": max_theta_spread,
        "secret_independent_projection_verified": (
            max_formula_err < 1e-12 and max_theta_spread < 1e-12
        ),
    }


def _real_symmetric_eigenvalues_jacobi(mat_real: List[List[float]]) -> List[float]:
    """Compute all eigenvalues of a real symmetric matrix via exact cyclic Jacobi rotations."""
    n = len(mat_real)
    a = [[float(mat_real[i][j]) for j in range(n)] for i in range(n)]
    for _ in range(60):
        max_off = 0.0
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) > max_off:
                    max_off = abs(a[p][q])
        if max_off < 1e-15:
            break
        for p in range(n):
            for q in range(p + 1, n):
                apq = a[p][q]
                if abs(apq) < 1e-15:
                    continue
                app = a[p][p]
                aqq = a[q][q]
                tau = (aqq - app) / (2.0 * apq)
                t = math.copysign(1.0 / (abs(tau) + math.sqrt(1.0 + tau * tau)), tau) if tau != 0.0 else 1.0
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = t * c
                a[p][p] = app - t * apq
                a[q][q] = aqq + t * apq
                a[p][q] = 0.0
                a[q][p] = 0.0
                for k in range(n):
                    if k != p and k != q:
                        akp = a[k][p]
                        akq = a[k][q]
                        a[k][p] = c * akp - s * akq
                        a[p][k] = a[k][p]
                        a[k][q] = s * akp + c * akq
                        a[q][k] = a[k][q]
    return [a[i][i] for i in range(n)]


def _hermitian_trace_distance(rho_a: ComplexMatrix, rho_b: ComplexMatrix) -> float:
    """Compute (1/2) ||rho_a - rho_b||_1 by embedding the n x n Hermitian difference into a 2n x 2n real symmetric matrix."""
    n = len(rho_a)
    real_2n = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            diff = 0.5 * ((rho_a[i][j] - rho_b[i][j]) + (rho_a[j][i] - rho_b[j][i]).conjugate())
            re_val = diff.real
            im_val = diff.imag
            real_2n[i][j] = re_val
            real_2n[i + n][j + n] = re_val
            real_2n[i][j + n] = -im_val
            real_2n[i + n][j] = im_val
    eigvals_2n = _real_symmetric_eigenvalues_jacobi(real_2n)
    # Each eigenvalue of the Hermitian n x n matrix appears with multiplicity 2 in the 2n x 2n real embedding
    return 0.25 * sum(abs(ev) for ev in eigvals_2n)


def classical_binomial_majority_tv_distance(r_copies: int, p_plus: float, q_plus: float) -> float:
    """Compute exact total variation distance between Binomial(r, p_plus) and Binomial(r, q_plus)."""
    _validate_r_and_gamma(r_copies, 1.0)
    tv = 0.0
    for k in range(r_copies + 1):
        comb = float(math.comb(r_copies, k))
        pk = comb * (p_plus ** k) * ((1.0 - p_plus) ** (r_copies - k))
        qk = comb * (q_plus ** k) * ((1.0 - q_plus) ** (r_copies - k))
        tv += 0.5 * abs(pk - qk)
    return tv


def verify_half_period_commuting_majority_optimality(
    r_copies: int,
    gamma: float,
) -> Dict[str, Any]:
    """Verify that for theta=0 vs theta=pi, classical r-sample X majority vote achieves the exact collective Helstrom distance."""
    _validate_r_and_gamma(r_copies, gamma)
    rho_0 = r_copy_tensor_density_matrix(0.0, gamma, r_copies)
    rho_pi = r_copy_tensor_density_matrix(math.pi, gamma, r_copies)
    proj_sym = symmetric_subspace_projector(r_copies)

    collective_helstrom_tv = _hermitian_trace_distance(rho_0, rho_pi)
    sym_0 = _matmul(_matmul(proj_sym, rho_0), proj_sym)
    sym_pi = _matmul(_matmul(proj_sym, rho_pi), proj_sym)
    sym_projected_tv = _hermitian_trace_distance(sym_0, sym_pi)
    non_sym_sector_tv_contribution = collective_helstrom_tv - sym_projected_tv

    p_plus_0 = 0.5 * (1.0 + gamma)
    p_plus_pi = 0.5 * (1.0 - gamma)
    classical_majority_tv = classical_binomial_majority_tv_distance(r_copies, p_plus_0, p_plus_pi)

    commutator_norm = _frobenius_norm_commutator(rho_0, rho_pi)

    return {
        "r_copies": r_copies,
        "gamma": gamma,
        "commutator_frobenius_norm": commutator_norm,
        "collective_helstrom_trace_distance": collective_helstrom_tv,
        "classical_r_sample_majority_tv_distance": classical_majority_tv,
        "symmetric_subspace_restricted_trace_distance": sym_projected_tv,
        "non_symmetric_sector_trace_distance_loss": non_sym_sector_tv_contribution,
        "classical_majority_matches_collective_helstrom": (
            abs(collective_helstrom_tv - classical_majority_tv) < 1e-12
            and commutator_norm < 1e-12
        ),
    }


def verify_dicke_harmonic_and_noncommuting_quadrature_separation(
    r_copies: int,
    gamma: float,
    theta_quad: float = math.pi / 2.0,
) -> Dict[str, Any]:
    """Verify Dicke extreme-coherence harmonic cos(r*theta) and collective vs fixed-basis separable separation at theta=pi/2."""
    _validate_r_and_gamma(r_copies, gamma)
    rho_0 = r_copy_tensor_density_matrix(0.0, gamma, r_copies)
    rho_theta = r_copy_tensor_density_matrix(theta_quad, gamma, r_copies)
    proj_sym = symmetric_subspace_projector(r_copies)

    # 1. Extreme Dicke coherence observable O_{GHZ}^{(r)} = |0^r><1^r| + |1^r><0^r| inside Sym^r(C^2)
    dim = 1 << r_copies
    ghz_exp_explicit = (rho_theta[0][dim - 1] + rho_theta[dim - 1][0]).real
    ghz_exp_closed_form = (gamma ** r_copies) * math.cos(r_copies * theta_quad) / float(1 << (r_copies - 1))

    # Separable even-Y Pauli average matches O_{GHZ}^{(r)} without entangling gates
    even_y_sum = 0.0
    even_masks = [mask for mask in range(dim) if bin(mask).count("1") % 2 == 0]
    for mask in even_masks:
        y_wt = bin(mask).count("1")
        sign = (-1) ** (y_wt // 2)
        x_wt = r_copies - y_wt
        pauli_prod = (gamma ** r_copies) * (math.cos(theta_quad) ** x_wt) * (math.sin(theta_quad) ** y_wt)
        even_y_sum += sign * pauli_prod
    separable_even_y_mean = even_y_sum / float(len(even_masks))

    # 2. Collective Helstrom trace distance vs optimal fixed single-copy projection basis for 0 vs theta_quad
    collective_tv = _hermitian_trace_distance(rho_0, rho_theta)
    sym_0 = _matmul(_matmul(proj_sym, rho_0), proj_sym)
    sym_th = _matmul(_matmul(proj_sym, rho_theta), proj_sym)
    sym_only_tv = _hermitian_trace_distance(sym_0, sym_th)

    delta_1 = gamma * abs(math.sin(0.5 * theta_quad))
    fixed_basis_majority_tv = classical_binomial_majority_tv_distance(
        r_copies, 0.5 * (1.0 + delta_1), 0.5 * (1.0 - delta_1)
    )
    naive_x_basis_tv = classical_binomial_majority_tv_distance(
        r_copies, 0.5 * (1.0 + gamma), 0.5 * (1.0 + gamma * math.cos(theta_quad))
    )

    return {
        "r_copies": r_copies,
        "gamma": gamma,
        "theta_quad": theta_quad,
        "dicke_ghz_expectation_explicit": ghz_exp_explicit,
        "dicke_ghz_expectation_closed_form": ghz_exp_closed_form,
        "separable_even_y_pauli_mean": separable_even_y_mean,
        "harmonic_identity_error": max(
            abs(ghz_exp_explicit - ghz_exp_closed_form),
            abs(separable_even_y_mean - ghz_exp_closed_form),
        ),
        "collective_helstrom_tv": collective_tv,
        "symmetric_subspace_helstrom_tv": sym_only_tv,
        "optimal_fixed_single_copy_basis_r_sample_tv": fixed_basis_majority_tv,
        "naive_x_basis_r_sample_tv": naive_x_basis_tv,
        "collective_minus_fixed_basis_tv_gain": collective_tv - fixed_basis_majority_tv,
        "requires_r_identical_headers_birthday_scale_Q_to_r_minus_1_over_r": True,
    }


def generate_dcp_multicopy_schur_weyl_symmetric_projection_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the multi-copy Schur-Weyl symmetric projection bridge."""
    theta_grid = [0.0, 0.35, math.pi / 4.0, math.pi / 2.0, 2.1, math.pi]

    projection_audits = [
        verify_symmetric_projection_secret_independence(r_copies=2, gamma=0.8, test_thetas=theta_grid),
        verify_symmetric_projection_secret_independence(r_copies=3, gamma=0.75, test_thetas=theta_grid),
        verify_symmetric_projection_secret_independence(r_copies=4, gamma=0.6, test_thetas=theta_grid),
        verify_symmetric_projection_secret_independence(r_copies=3, gamma=1.0, test_thetas=theta_grid),
        verify_symmetric_projection_secret_independence(r_copies=3, gamma=0.0, test_thetas=theta_grid),
    ]

    half_period_majority_audits = [
        verify_half_period_commuting_majority_optimality(r_copies=2, gamma=0.8),
        verify_half_period_commuting_majority_optimality(r_copies=3, gamma=0.8),
        verify_half_period_commuting_majority_optimality(r_copies=4, gamma=0.7),
    ]

    quadrature_audits = [
        verify_dicke_harmonic_and_noncommuting_quadrature_separation(r_copies=2, gamma=0.8, theta_quad=math.pi / 2.0),
        verify_dicke_harmonic_and_noncommuting_quadrature_separation(r_copies=3, gamma=0.8, theta_quad=math.pi / 3.0),
        verify_dicke_harmonic_and_noncommuting_quadrature_separation(r_copies=2, gamma=1.0, theta_quad=math.pi / 2.0),
    ]

    r2_sym_prob = projection_audits[0]["closed_form_probability"]
    r2_expected = (3.0 + 0.8 * 0.8) / 4.0

    all_passed = (
        all(a["secret_independent_projection_verified"] for a in projection_audits)
        and abs(r2_sym_prob - r2_expected) < 1e-12
        and all(a["classical_majority_matches_collective_helstrom"] for a in half_period_majority_audits)
        and half_period_majority_audits[1]["non_symmetric_sector_trace_distance_loss"] > 0.01
        and all(a["harmonic_identity_error"] < 1e-12 for a in quadrature_audits)
        and quadrature_audits[0]["collective_minus_fixed_basis_tv_gain"] > 0.08
        and abs(quadrature_audits[0]["collective_helstrom_tv"] - quadrature_audits[0]["symmetric_subspace_helstrom_tv"]) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "r-copy symmetric subspace projections Pi_{Sym^r} and Schur-Weyl measurements on matched-header DCP phase states rho(a, s, gamma)^{tensor r}",
            "does_not_claim": "Collective advantage for commuting half-period targets (theta in {0, pi}) or collision-free multi-copy acquisition under IID uniform random headers",
            "controls_included": "Includes exact theta-independent symmetric projection weight across r=2,3,4, exact equality between collective Helstrom trace distance and classical r-sample Binomial majority voting at theta in {0, pi}, non-symmetric sector loss under pure Sym^r postselection at r>=3, and scoped non-commuting quadrature gain at theta=pi/2 on matched headers.",
        },
        "symmetric_projection_audits": projection_audits,
        "half_period_commuting_majority_audits": half_period_majority_audits,
        "noncommuting_quadrature_and_harmonic_audits": quadrature_audits,
        "all_checks_passed": all_passed,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    payload["certificate_sha256_16"] = digest
    return payload

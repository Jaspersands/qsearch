"""Test local orbit-span repair against an EXACT matched classical Gibbs walk.

Sign-normalized compressed physical bits give the PGM if its orbit reflection
is available. Local deformed-check projectors have this span as their joint
kernel, but each sector is exactly the symmetric heat-bath generator. A
polynomial sector gap would ALSO give a classical sampler.
Known stochastic-Hamiltonian mechanism; local application REVIEW PENDING.
No universal BPQM, stoquastic, sampling or quantum-speedup no-go is asserted.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import sqrt
from pathlib import Path
import random
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer, rational
from theorems.coherent_local_gibbs import CodeProblem
from theorems.parity_block_usd_prange import affine_system, uniform_affine_solution

REPORT = ROOT / "research/phase_workbench/gibbs_orbit_parent.json"
DEPENDENCIES = ("coherent_local_gibbs.py", "bpqm_gibbs_frontier.py",
                "parity_block_usd_prange.py", "affine_cluster_native_probe.py")


def overlap(value):
    c = rational(value)
    if not 0 <= c < 1:
        raise ValueError("finite-temperature overlap 0<=c<1 required; c=1 collapses the orbit rank")
    return c


def weight(word, width, c):
    """Positive INTEGER product weight, with its common denominator omitted."""
    integer(width, "weight width", 0, 512)
    integer(word, "canonical weight word", 0, (1 << width)-1)
    c = overlap(c)
    ones = word.bit_count()
    return (c.denominator+c.numerator)**(width-ones)*(c.denominator-c.numerator)**ones


def row_orbit(problem, representative):
    """Small-control enumeration only; production steps NEVER call this."""
    if problem.length > 8:
        raise ValueError("UNKNOWN: dense orbit verifier capped at eight clauses")
    integer(representative, "sector representative", 0, (1 << problem.length)-1)
    orbit = {representative}
    for h in problem.checks:
        orbit |= {y ^ h for y in tuple(orbit)}
    return tuple(sorted(orbit))


def local_projector(width, c):
    """Actual CNOT relabeling and controlled real Ry readout of one check.

    LSB is the pivot. CNOTs pivot->other wires relabel complement pairs;
    on each pair Ry(-theta) maps the positive product-weight vector to |0>.
    The projector is U^dagger |1><1|_pivot U. Explicit tables are bounded
    calibration gates, not an efficient compiler at growing check degree.
    """
    integer(width, "bounded local support", 0, 8)
    c = overlap(c)
    dimension = 1 << width
    if not width:
        return np.zeros((1, 1)), np.eye(1)
    complement = dimension-1
    relabel, rotate = np.zeros((dimension, dimension)), np.zeros((dimension, dimension))
    for y in range(dimension):
        z = y ^ (complement ^ 1) if y & 1 else y
        relabel[z, y] = 1
    for z in range(0, dimension, 2):
        a, b = weight(z, width, c), weight(z ^ complement, width, c)
        cosine, sine = sqrt(float(Fraction(a, a+b))), sqrt(float(Fraction(b, a+b)))
        rotate[z:z+2, z:z+2] = ((cosine, sine), (-sine, cosine))
    U = rotate @ relabel
    return U.T @ np.diag([y & 1 for y in range(dimension)]) @ U, U


def parent_matrix(problem, c):
    if problem.length > 8:
        raise ValueError("UNKNOWN: dense parent verifier capped at eight clauses")
    c = overlap(c)
    dimension = 1 << problem.length
    result = np.zeros((dimension, dimension))
    for h in problem.checks:
        support = [j for j in range(problem.length) if (h >> j) & 1]
        term, _ = local_projector(len(support), c)
        for y in range(dimension):
            local_y = sum(((y >> j) & 1) << i for i, j in enumerate(support))
            for z_local in range(1 << len(support)):
                z = (y & ~h) | sum(((z_local >> i) & 1) << j for i, j in enumerate(support))
                result[y, z] += term[local_y, z_local]/len(problem.checks)
    return result


def exact_sector_kernel(problem, c, representative):
    """Independent exact rational heat bath on J+rowspan(H)."""
    c = overlap(c)
    states = row_orbit(problem, representative)
    index = {y: i for i, y in enumerate(states)}
    weights = [weight(y, problem.length, c) for y in states]
    partition = sum(weights)
    pi = tuple(Fraction(w, partition) for w in weights)
    kernel = [[Fraction(0) for _ in states] for _ in states]
    for i, y in enumerate(states):
        for h in problem.checks:
            j = index[y ^ h]
            if not h:
                kernel[i][i] += Fraction(1, len(problem.checks))
                continue
            flip = Fraction(weights[j], len(problem.checks)*(weights[i]+weights[j]))
            kernel[i][j] += flip
            kernel[i][i] += Fraction(1, len(problem.checks))-flip
    if any(sum(row) != 1 for row in kernel):
        raise ArithmeticError("nonstochastic heat-bath row")
    if any(pi[i]*kernel[i][j] != pi[j]*kernel[j][i]
           for i in range(len(states)) for j in range(len(states))):
        raise ArithmeticError("exact heat-bath detailed balance failed")
    return states, pi, kernel


def local_deformed_code_control(width, c):
    """Independently build actual channel states for even-parity codewords."""
    integer(width, "deformed-check calibration support", 1, 6)
    c = overlap(c)
    phi = np.sqrt([float(Fraction(weight(y, width, c), (2*c.denominator)**width))
                   for y in range(1 << width)])
    words = [d for d in range(1 << width) if not d.bit_count() % 2]
    states = np.array([[phi[y]*(-1)**((d & y).bit_count() % 2) for d in words]
                       for y in range(1 << width)])
    basis, _ = np.linalg.qr(states)
    complement = np.eye(1 << width)-basis @ basis.T
    term, U = local_projector(width, c)
    residual = float(np.max(np.abs(term-complement)))
    if residual > 1e-10:
        raise ArithmeticError("local gate projector differs from the actual deformed-code complement")
    return {"support": width, "c_exact": str(c), "deformed_code_complement_residual": residual,
            "local_gate_unitarity_residual": float(np.max(np.abs(U.T @ U-np.eye(1 << width)))),
            "projector_idempotence_residual": float(np.max(np.abs(term @ term-term))),
            "CNOT_relabel_gates": width-1, "bounded_controlled_rotation_blocks": 1 << (width-1),
            "growing_degree_rotation_table_is_NOT_a_polynomial_compiler": True}


def sector_control(problem, c):
    """Every syndrome, actual local gates, and independent full orbit source."""
    c = overlap(c)
    parent = parent_matrix(problem, c)
    dimension = len(parent)
    visited, sectors, projector = set(), [], np.zeros_like(parent)
    for representative in range(dimension):
        if representative in visited:
            continue
        states, pi, kernel = exact_sector_kernel(problem, c, representative)
        visited.update(states)
        roots = np.sqrt(list(map(float, pi)))
        S = np.array(kernel, dtype=float)*roots[:, None]/roots[None, :]
        restriction = parent[np.ix_(states, states)]
        expected = np.eye(len(states))-S
        residual = float(np.max(np.abs(restriction-expected)))
        eigenvalues = np.linalg.eigvalsh(restriction)
        gap = float(eigenvalues[1]) if len(states) > 1 else None
        ground = np.zeros(dimension)
        ground[list(states)] = roots
        projector += np.outer(ground, ground)
        sectors.append({"representative_hex": hex(representative), "size": len(states),
                        "similarity_max_residual": residual,
                        "stationary_ground_residual": float(np.max(np.abs(restriction @ roots))),
                        "gap_NUMERICAL_NOT_A_LOWER_BOUND_CERTIFICATE": gap,
                        "exact_detailed_balance": True})
    basis, _ = problem.structure
    codewords = [problem.encode(u) for u in range(1 << len(basis))]
    phi = np.sqrt([float(Fraction(weight(y, problem.length, c), (2*c.denominator)**problem.length))
                   for y in range(dimension)])
    source = np.array([[phi[y]*(-1)**((d & y).bit_count() % 2) for d in codewords]
                       for y in range(dimension)])
    Q, _ = np.linalg.qr(source)
    orbit_projector = Q @ Q.T
    ground_residual = float(np.max(np.abs(parent @ orbit_projector)))
    span_residual = float(np.max(np.abs(orbit_projector-projector)))
    eigenvalues = np.linalg.eigvalsh(parent)
    nullity = int(np.count_nonzero(abs(eigenvalues) < 1e-10))
    if max(ground_residual, span_residual, *(r["similarity_max_residual"] for r in sectors)) > 1e-10:
        raise ArithmeticError("local parent / actual source / classical walk mismatch")
    if nullity != 1 << len(basis) or min(eigenvalues) < -1e-10 or max(eigenvalues) > 1+1e-10:
        raise ArithmeticError("parent has the wrong kernel or normalized spectrum")
    return {"length": problem.length, "checks_hex": list(map(hex, problem.checks)), "c_exact": str(c),
            "code_dimension": len(basis), "parent_ground_dimension_exact": 1 << len(basis),
            "parent_ground_dimension_numerical": nullity,
            "sectors": sectors, "actual_source_orbit_span_residual": span_residual,
            "parent_annihilates_actual_source_residual": ground_residual,
            "finite_matrices_are_NOT_asymptotic_gap_evidence": True}


def spectral_readout_reference(problem, c):
    """BOUNDED dense sign(P X_i P), not a supplied efficient span reflection.

    Build P from the local parent's ground space, independently of conditional
    Gibbs masses. The nonzero compressed-bit spectrum is uniformly separated
    from zero by sqrt(1-c^2). Matrix diagonalization is exponential in length.
    """
    if problem.length > 6:
        raise ValueError("UNKNOWN: dense spectral-repair reference capped at six clauses")
    c = overlap(c)
    parent = parent_matrix(problem, c)
    eigenvalues, eigenvectors = np.linalg.eigh(parent)
    basis = eigenvectors[:, abs(eigenvalues) < 1e-10]
    P = basis @ basis.T
    code_basis, information_coordinates = problem.structure
    if len(code_basis) > 4 or len(basis.T) != 1 << len(code_basis):
        raise ValueError("UNKNOWN: dense decoder cap or unresolved numerical parent kernel")
    theoretical_gap = sqrt(float(1-c*c))
    roots, compressed, metrics = [], [], []
    for coordinate in information_coordinates:
        X = np.zeros_like(parent)
        for y in range(len(parent)):
            X[y ^ (1 << coordinate), y] = 1
        C = P @ X @ P
        values, vectors = np.linalg.eigh(C)
        nonzero = abs(values) > theoretical_gap/2
        if np.count_nonzero(nonzero) != len(basis.T) or min(abs(values[nonzero])) < theoretical_gap-1e-10:
            raise ArithmeticError("compressed physical bit violates its uniform gap bound")
        sign = (vectors[:, nonzero]*np.sign(values[nonzero])) @ vectors[:, nonzero].T
        reflection = sign+np.eye(len(parent))-P
        residual = float(np.max(np.abs(reflection @ reflection-np.eye(len(parent)))))
        if residual > 1e-10:
            raise ArithmeticError("spectral repair is not a clean bounded reflection")
        roots.append(reflection)
        compressed.append(C)
        metrics.append({"information_coordinate": coordinate,
                        "nonzero_gap_numeric": float(min(abs(values[nonzero]))),
                        "reflection_unitarity_max_residual": residual})
    before = max((float(np.linalg.norm(A @ B-B @ A, ord=2)) for A in compressed for B in compressed), default=0.)
    after = max((float(np.linalg.norm(A @ B-B @ A, ord=2)) for A in roots for B in roots), default=0.)
    if after > 1e-10:
        raise ArithmeticError("repaired information-root projectors do not commute")
    return P, roots, {"theoretical_compressed_gap_lower_squared_exact": str(1-c*c),
                      "roots": metrics, "raw_compressed_commutator_norm_max_numeric": before,
                      "repaired_reflection_commutator_norm_max_numeric": after,
                      "span_from_local_parent_dense_eigendecomposition": True,
                      "span_reflection_efficiently_compiled": False,
                      "dense_spectral_reference_NOT_a_scalable_quantum_execution": True}


def compressed_block_encoding_reference(problem, c, information_index=0):
    """Actual two-ancilla unitary with top block P X_i P, normalization ONE."""
    P, _, _ = spectral_readout_reference(problem, c)
    integer(information_index, "information index", 0, len(problem.structure[1])-1)
    coordinate = problem.structure[1][information_index]
    dimension = len(P)
    X, bitflip = np.zeros_like(P), np.array([[0., 1.], [1., 0.]])
    for y in range(dimension):
        X[y ^ (1 << coordinate), y] = 1
    complement = np.eye(dimension)-P
    common = np.kron(np.eye(4), P)
    first = common+np.kron(np.kron(bitflip, np.eye(2)), complement)
    second = common+np.kron(np.kron(np.eye(2), bitflip), complement)
    return first @ np.kron(np.eye(4), X) @ second, P @ X @ P


def spectral_gibbs_control(problem, c):
    """Execute A, label XOR, A^dagger, and final readout, keeping ALL work.

    Data is stored in the Fourier basis throughout, so the final physical
    Z^J then H is simply y->y XOR J. Never postselect cleared source labels.
    """
    c = overlap(c)
    _, roots, recipe = spectral_readout_reference(problem, c)
    dimension, k = 1 << problem.length, len(roots)
    if len(problem.checks) > 6 or problem.length+2*k > 14:
        raise ValueError("UNKNOWN: complete-sign spectral readout statevector cap")
    identity = np.eye(dimension)
    plus = [(identity+R)/2 for R in roots]
    minus = [(identity-R)/2 for R in roots]
    phi = np.sqrt([float(Fraction(weight(y, problem.length, c), (2*c.denominator)**problem.length))
                   for y in range(dimension)])
    codewords = [problem.encode(u) for u in range(1 << k)]

    def apply_decoder(state, reverse=False):
        for i in (reversed(range(k)) if reverse else range(k)):
            out = np.zeros_like(state)
            for r in range(1 << k):
                out[r] += state[r] @ plus[i].T
                out[r ^ (1 << i)] += state[r] @ minus[i].T
            state = out
        return state

    word_success = []
    for u, word in enumerate(codewords):
        state = phi*np.array([(-1)**((word & y).bit_count() % 2) for y in range(dimension)])
        for i in range(k):
            state = (minus[i] if (u >> i) & 1 else plus[i]) @ state
        word_success.append(float(np.vdot(state, state).real))
    rows = []
    for signs in range(dimension):
        state = np.zeros((1 << k, 1 << k, dimension))
        for u, word in enumerate(codewords):
            phase = (-1)**((signs & word).bit_count() % 2)
            state[0, u] = phase*phi*np.array([(-1)**((word & y).bit_count() % 2)
                                            for y in range(dimension)])/sqrt(1 << k)
        state = apply_decoder(state)
        after_xor = np.zeros_like(state)
        for r in range(1 << k):
            for u in range(1 << k):
                after_xor[r, u ^ r] = state[r, u]
        state = apply_decoder(after_xor, reverse=True)
        state = state[:, :, np.arange(dimension) ^ signs]
        probabilities = (abs(state)**2).sum(axis=(0, 1))
        norm = float(sum(probabilities))
        spin_words, fibers = [], {}
        for x in range(1 << len(problem.checks)):
            y = 0
            for i, h in enumerate(problem.checks):
                if (x >> i) & 1:
                    y ^= h
            spin_words.append(y)
            fibers[y] = fibers.get(y, 0)+1
        actual = np.array([probabilities[y]/fibers[y] for y in spin_words])
        exact_weights = [weight(y ^ signs, problem.length, c) for y in spin_words]
        partition = sum(exact_weights)
        target = np.array([float(Fraction(w, partition)) for w in exact_weights])
        abort = float(sum(probabilities[y] for y in range(dimension) if y not in fibers))
        TV = float(np.abs(actual-target).sum()+abort)/2
        flattened = state.reshape(-1, dimension)
        density = flattened.T @ flattened
        purity = float(np.trace(density @ density))
        if abs(norm-1) > 1e-10 or TV > 1e-10 or abs(purity-1) > 1e-10:
            raise ArithmeticError("full flagged spectral-repair sampler differs from exact Gibbs")
        rows.append({"signs_hex": hex(signs), "unconditional_TV_numeric": TV,
                     "abort_mass_numeric": abort, "data_purity_numeric": purity,
                     "source_label_zero_probability_numeric": float((abs(state[:, 0])**2).sum()),
                     "record_zero_probability_numeric": float((abs(state[0])**2).sum()),
                     "postselection_used": False})
    return {"length": problem.length, "checks_hex": list(map(hex, problem.checks)), "c_exact": str(c),
            "spectral_repair_recipe": recipe, "all_sign_rows": rows,
            "word_error_numeric": 1-float(np.mean(word_success)),
            "all_sign_mean_unconditional_TV_numeric": float(np.mean([r["unconditional_TV_numeric"] for r in rows])),
            "retained_qubits": problem.length+2*k,
            "dense_reference_matrix_entries_at_least": dimension**2,
            "scalable_gate_count_or_speedup_established": False}


def universal_gap_budget(problem, c, *, failure_bits=10):
    """A rigorous but usually exponential comparison floor, NOT a gap estimate.

    At c=0 the nonconstant Fourier characters have energy >=1/R. Compare
    stationary max/min and local flip rates at c>0 to obtain rho^(M+w)/R.
    Finite spectra never enter this certificate. The proof remains local-review
    pending; a huge sufficient budget does not prove slow mixing.
    """
    c = overlap(c)
    integer(failure_bits, "TV accuracy exponent", 1, 64)
    k = len(problem.structure[0])
    rank = problem.length-k
    if not rank:
        return {"status": "TRIVIAL_SINGLETON_SECTOR", "steps_sufficient": 0,
                "gap_lower_exact": None, "parent_positive_gap_claimed": False}
    rho = (1-c)/(1+c)
    width = max(h.bit_count() for h in problem.checks)
    lower = rho**(problem.length+width)/len(problem.checks)
    odds = 1/rho
    log_odds_upper = 0
    while (1 << log_odds_upper)*odds.denominator < odds.numerator:
        log_odds_upper += 1
    numerator = rank+problem.length*log_odds_upper+2*failure_bits
    budget = (numerator*lower.denominator+2*lower.numerator-1)//(2*lower.numerator)
    return {"status": "UNIFORM_COMPARISON_BOUND_LOCAL_REVIEW_PENDING", "c_exact": str(c),
            "row_rank": rank, "generators": len(problem.checks), "max_check_support": width,
            "gap_lower_exact": str(lower), "stationary_minimum_lower_exact": str(rho**problem.length/(1 << rank)),
            "ceil_log2_odds_upper": log_odds_upper, "steps_sufficient": budget,
            "TV_at_most_after_THIS_budget_under_uniform_coins": f"2^-{failure_bits}",
            "large_sufficient_budget_proves_slow_mixing": False,
            "numerical_eigenvalues_used_as_certificates": False}


def quotient_step(problem, c, y, rng):
    """One exact local update; no partition function, matrix or orbit table."""
    c = overlap(c)
    integer(y, "current clause word", 0, (1 << problem.length)-1)
    index = rng.randrange(len(problem.checks))
    h = problem.checks[index]
    width, ones = h.bit_count(), (y & h).bit_count()
    a, b = c.denominator+c.numerator, c.denominator-c.numerator
    old, new = a**(width-ones)*b**ones, a**ones*b**(width-ones)
    if rng.randrange(old+new) < new:
        y ^= h
    return y, index, width


def quotient_trajectory(problem, c, signs, *, seed, steps=256):
    """Polynomial-work actual classical updates; no stationary initialization."""
    c = overlap(c)
    integer(signs, "original signs", 0, (1 << problem.length)-1)
    integer(seed, "seeded replay", 0, (1 << 64)-1)
    integer(steps, "paid updates", 1, 10**6)
    rng = random.Random(seed)
    y, tested_bits, transcript = signs, 0, hashlib.sha256()
    for _ in range(steps):
        y, index, width = quotient_step(problem, c, y, rng)
        tested_bits += width
        transcript.update(f"{index}:{y};".encode())
    equations = tuple((sum(((h >> j) & 1) << i for i, h in enumerate(problem.checks)),
                       ((y ^ signs) >> j) & 1) for j in range(problem.length))
    system = affine_system(equations, len(problem.checks))
    if not system["consistent"]:
        raise ArithmeticError("classical quotient walk escaped its original sign sector")
    x = uniform_affine_solution(system, len(problem.checks), rng)
    replay = signs
    for j, h in enumerate(problem.checks):
        if (x >> j) & 1:
            replay ^= h
    if replay != y:
        raise ArithmeticError("uniform gauge lift failed original parity equations")
    return {"length": problem.length, "checks_hex": list(map(hex, problem.checks)),
            "original_signs_hex": hex(signs), "final_quotient_hex": hex(y), "lifted_spins_hex": hex(x),
            "c_exact": str(c), "seed": seed, "updates_charged": steps,
            "local_factor_bits_tested": tested_bits, "uniform_draw_calls_before_gauge_lift": 2*steps,
            "gauge_dimension": len(problem.checks)-system["rank"], "native_lift_verified": True,
            "transcript_sha256": transcript.hexdigest(), "full_domain_materialized": False,
            "output_is_certified_Gibbs_sample": False, "TV_error_claim": None,
            "randomness": "SEEDED_REPLAY_NOT_IID_CONFIDENCE", "quantum_circuit_executed": False}


def gram_access_certificate(length, dimension, c):
    """All-code normalization bound; scalar arithmetic, NOT a Gram table.

    Gamma_uv=c^wt(G(u+v)). Its largest eigenvalue is its positive row sum.
    Systematic information coordinates imply wt(Gu)>=wt(u), hence the row
    sum is <=(1+c)^k. Charge BOTH implementable Gram normalizations.
    """
    integer(length, "analytic clause length", 1, 4096)
    integer(dimension, "analytic code dimension", 0, length)
    c = overlap(c)
    row_sum_upper = (1+c)**dimension
    divisors = {"product_channel_LCU": (1+c)**length,
                "source_purification_swap": Fraction(1 << dimension)}
    records = {name: {"Gram_divisor_exact": str(divisor),
                       "encoded_Gram_norm_upper_exact": str(row_sum_upper/divisor),
                       "inverse_adjoint_on_ANY_normalized_solution_lower_exact": str(divisor/row_sum_upper)}
               for name, divisor in divisors.items()}
    best = min(divisors, key=divisors.get)
    return {"length": length, "code_dimension": dimension, "c_exact": str(c),
            "mode": "ALL_CODE_SCALAR_BOUND_NO_STATE_OR_GRAM_ENUMERATION",
            "unscaled_Gram_row_sum_upper_exact": str(row_sum_upper), "encodings": records,
            "better_of_these_two_encodings": best,
            "best_inverse_adjoint_quantity_lower_exact": records[best]["inverse_adjoint_on_ANY_normalized_solution_lower_exact"],
            "QLS_cost_expression_floor_is_NOT_a_general_query_or_circuit_lower_bound": True,
            "all_span_reflection_constructions_excluded": False,
            "new_preconditioner_or_affine_dilation_supplied": False}


def gram_preparation_control(problem, c):
    """Execute public source-prep / SWAP / unprep, not a supplied Gram oracle."""
    if problem.length > 6 or len(problem.structure[0]) > 3:
        raise ValueError("UNKNOWN: physical Gram block verifier capped at six clauses/three information bits")
    c = overlap(c)
    k, D = len(problem.structure[0]), 1 << problem.length
    N = 1 << k
    gamma = (1-sqrt(float(1-c*c)))/2
    a, b = sqrt(1-gamma), sqrt(gamma)
    rotation = np.array([[a, -b], [b, a]])
    product_rotation = np.ones((1, 1))
    for _ in range(problem.length):
        product_rotation = np.kron(rotation, product_rotation)
    words = [problem.encode(u) for u in range(N)]
    preparations = np.array([product_rotation[np.arange(D) ^ d] for d in words])
    H = np.array([[(-1)**((u & v).bit_count() % 2) for v in range(N)] for u in range(N)])/sqrt(N)
    block = np.zeros((N, N))
    for v in range(N):
        state = np.zeros((N, D, N))
        state[0, 0, v] = 1
        state = np.einsum("ab,bdc->adc", H, state)
        state = np.einsum("uij,ujv->uiv", preparations, state)
        state = state.transpose(2, 1, 0)
        state = np.einsum("uji,ujv->uiv", preparations, state)
        state = np.einsum("ab,bdc->adc", H, state)
        if abs(float(np.sum(state**2))-1) > 1e-10:
            raise ArithmeticError("source/SWAP/unprepare circuit lost probability")
        block[:, v] = state[0, 0]
    exact = [[c**(u ^ v).bit_count() for v in words] for u in words]
    Gram = np.array(exact, dtype=float)
    residual = float(np.max(np.abs(block-Gram/N)))
    row_sum = sum(exact[0])
    if any(sum(row) != row_sum for row in exact) or row_sum > (1+c)**k or residual > 1e-10:
        raise ArithmeticError("actual Gram encoding or systematic row-sum bound failed")
    # Independently check each single-wire LCU and its product on code columns.
    prepare = np.array([[sqrt(a/(a+b)), -sqrt(b/(a+b))],
                        [sqrt(b/(a+b)), sqrt(a/(a+b))]])
    select = np.block([[np.eye(2), np.zeros((2, 2))],
                       [np.zeros((2, 2)), np.array([[0., 1.], [1., 0.]])]])
    U = np.kron(prepare.T, np.eye(2)) @ select @ np.kron(prepare, np.eye(2))
    T = np.array([[a, b], [b, a]])
    local_residual = float(np.max(np.abs(U[:2, :2]-T/(a+b))))
    channel = np.ones((1, 1))
    for _ in range(problem.length):
        channel = np.kron(U[:2, :2], channel)
    columns = channel[:, words]
    product_residual = float(np.max(np.abs(columns.T @ columns-Gram/float((1+c)**problem.length))))
    if max(local_residual, product_residual) > 1e-10:
        raise ArithmeticError("product-channel LCU normalization mismatch")
    return {"length": problem.length, "checks_hex": list(map(hex, problem.checks)), "c_exact": str(c),
            "exact_Gram_row_sum": str(row_sum), "systematic_row_sum_bound": str((1+c)**k),
            "physical_source_swap_unprepare_block_residual": residual,
            "single_wire_LCU_top_block_residual": local_residual,
            "product_channel_Gram_residual": product_residual,
            "purification_ancilla_postselection_IS_charged_in_the_block_normalization": True,
            "actual_logical_Gram_entries_checked": N*N,
            "Gram_access_certificate": gram_access_certificate(problem.length, k, c)}


def pair_native_reflection_control(pairs, c):
    """Countercontrol: a bad generic Gram encoding is NOT intrinsic hardness."""
    integer(pairs, "bounded disjoint pair count", 1, 3)
    c = overlap(c)
    problem = CodeProblem(2*pairs, tuple(3 << (2*i) for i in range(pairs)))
    local_term, local_U = local_projector(2, c)
    U, P = np.ones((1, 1)), np.ones((1, 1))
    for _ in range(pairs):
        U, P = np.kron(local_U, U), np.kron(np.eye(4)-local_term, P)
    flags = sum(1 << (2*i) for i in range(pairs))
    phase = np.diag([1 if not y & flags else -1 for y in range(1 << (2*pairs))])
    native = U.T @ phase @ U
    residual = float(np.max(np.abs(native-(2*P-np.eye(len(P))))))
    if residual > 1e-10:
        raise ArithmeticError("direct local-gate/AND span reflection failed")
    a, b = c.denominator+c.numerator, c.denominator-c.numerator
    probabilities = []
    for signs in range(4):
        w0, w1 = 1, 1
        for j in range(2):
            w0 *= b if (signs >> j) & 1 else a
            w1 *= a if (signs >> j) & 1 else b
        probabilities.append({"pair_signs": signs, "classical_spin_one_probability_exact": str(Fraction(w1, w0+w1))})
    return {"pairs": pairs, "length": 2*pairs, "c_exact": str(c),
            "native_reflection_vs_exact_span_residual": residual,
            "local_two_wire_unitaries_forward_and_inverse": 2*pairs,
            "global_flag_phase": "phase +1 on all-zero pivot flags, -1 otherwise; reversible AND costs O(pairs)",
            "all_pair_sign_classical_exact_sampler": probabilities,
            "parent_gap_or_generic_Gram_inversion_used": False,
            "growing_pair_family_HAS_a_direct_polynomial_reflection_and_classical_sampler": True,
            "new_quantum_speedup": False}


def run_controls():
    hashes = {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
              for name in DEPENDENCIES}
    producer = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    cases = [CodeProblem(5, (25, 26, 12)), CodeProblem(5, (25, 26, 12, 25, 0)),
             CodeProblem(4, (7, 14, 9)), CodeProblem(3, (0, 0))]
    controls = [sector_control(problem, c) for problem in cases for c in ("0", "1/5", "13/20")]
    from theorems.affine_cluster_native_probe import socket_instance
    model, source = socket_instance(64, random.Random(29))
    checks = tuple(sum(((mask >> i) & 1) << j for j, (mask, _) in enumerate(model.clauses))
                   for i in range(model.spins))
    signs = sum(sign << j for j, (_, sign) in enumerate(model.clauses))
    native = CodeProblem(len(model.clauses), checks)
    trajectory = quotient_trajectory(native, "13/20", signs, seed=4831)
    budget = universal_gap_budget(native, "13/20")
    repaired_controls = [spectral_gibbs_control(p, c) for p in cases[:2] for c in ("1/5", "13/20")]
    local_controls = [local_deformed_code_control(w, c) for w in (1, 2, 3, 6) for c in ("0", "13/20")]
    gram_controls = [gram_preparation_control(p, c) for p in cases[:3] for c in ("0", "1/5", "13/20")]
    pair_controls = [pair_native_reflection_control(pairs, "13/20") for pairs in (1, 2, 3)]
    gram_scaling = [gram_access_certificate(2*k, k, "13/20") for k in (16, 64, 256, 1024)]
    if producer != hashlib.sha256(Path(__file__).read_bytes()).hexdigest() or any(
            digest != hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name, digest in hashes.items()):
        raise RuntimeError("producer or dependency changed during the run")
    return {"schema_version": 2, "status": "SPECTRAL_REPAIR_PARENT_AND_GRAM_ACCESS_COSTED_REVIEW_PENDING",
            "producer_sha256": producer, "dependency_sha256": hashes, "finite_all_sector_controls": controls,
            "spectrally_repaired_full_Gibbs_controls": repaired_controls,
            "independent_local_deformation_controls": local_controls,
            "actual_public_Gram_encoding_controls": gram_controls,
            "native_Gram_access_bound_NO_Gram_table": gram_access_certificate(native.length, len(native.structure[0]), "13/20"),
            "half_rate_Gram_access_scaling_ANALYTIC_ONLY": gram_scaling,
            "direct_pair_reflection_countercontrols": pair_controls,
            "native_source": source, "native_actual_classical_trajectory": trajectory,
            "native_uniform_comparison_budget_NOT_executed": budget,
            "general_quantum_BPQM_dequantized": False, "polynomial_gap_proved": False,
            "classical_hardness_or_slow_mixing_proved": False, "new_quantum_algorithm": False,
            "speedup_claim_allowed": False, "accepted_speedup_candidate": False,
            "independent_review_or_formal_verification_completed": False, "no_central_registry_promotion": True,
            "literature": ["https://arxiv.org/abs/0712.1008", "https://arxiv.org/abs/0806.1746",
                           "https://arxiv.org/abs/1806.01838", "https://arxiv.org/abs/2006.16924",
                           "https://arxiv.org/abs/2607.07691v2"],
            "mechanism_is_known_stochastic_Hamiltonian_correspondence_not_claimed_novel": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "finite_controls": len(report["finite_all_sector_controls"]),
                      "native_updates": report["native_actual_classical_trajectory"]["updates_charged"],
                      "polynomial_gap_proved": False, "speedup_claim_allowed": False}, indent=2))


if __name__ == "__main__":
    main()

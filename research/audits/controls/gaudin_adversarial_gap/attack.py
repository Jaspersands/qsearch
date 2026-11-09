"""One bounded CLASSICAL native joint-gap falsification experiment.

Run with /opt/anaconda3/bin/python. No old control is imported or rerun.
Only N=6, M=3; a finite failure to falsify is never a lower-bound proof.
"""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import differential_evolution, minimize


N, M = 6, 3
MIN_SPACING = 1 / 64
THRESHOLD = 1 / N
ROBUST_MARGIN = 1e-6
MAX_EVALUATIONS = 4096
SEED = 20261107
WEIGHTS = [np.array(w, dtype=float) for w in (
    [3**i for i in range(N)], [1, 7, 23, 61, 127, 251],
    [2, 11, 37, 83, 173, 359])]
STATES = list(combinations(range(N), M))
DIM = len(STATES)
LOCATIONS = {state: k for k, state in enumerate(STATES)}
NUMBER = np.zeros((N, DIM, DIM))
SWAP_MINUS_I = np.zeros((N, N, DIM, DIM))
for column, state in enumerate(STATES):
    occupied = set(state)
    for i in range(N):
        NUMBER[i, column, column] = int(i in occupied)
        for j in range(N):
            if i == j or ((i in occupied) == (j in occupied)):
                continue
            target = tuple(sorted(occupied.symmetric_difference({i, j})))
            SWAP_MINUS_I[i, j, LOCATIONS[target], column] = 1
            SWAP_MINUS_I[i, j, column, column] = -1


def decode(x):
    """Surjective stick-breaking coordinates for all five allowed spacings."""
    remaining = 1.0
    simplex = []
    for fraction in x[:4]:
        piece = remaining * fraction
        simplex.append(piece)
        remaining -= piece
    simplex.append(remaining)
    spacings = MIN_SPACING + (5 - 5 * MIN_SPACING) * np.array(simplex)
    sites = np.concatenate(([0.0], np.cumsum(spacings)))
    sites[-1] = 5.0
    return sites, float(x[4])


def encode(spacings, coupling):
    simplex = (np.array(spacings) - MIN_SPACING) / (5 - 5 * MIN_SPACING)
    remaining, result = 1.0, []
    for piece in simplex[:4]:
        fraction = float(piece / remaining) if remaining > 1e-14 else 0.0
        result.append(np.clip(fraction, 0, 1))
        remaining -= piece
    return result + [coupling]


def spectrum(sites, coupling):
    differences = sites[:, None] - sites[None, :]
    np.fill_diagonal(differences, 1)
    coefficients = coupling / (2 * differences)
    np.fill_diagonal(coefficients, 0)
    charges = NUMBER + np.einsum('ij,ijab->iab', coefficients, SWAP_MINUS_I)
    # Three fixed combinations from the frozen old control. A scalar
    # degeneracy is not a joint degeneracy: reject a mixed joint basis.
    attempts = []
    for weights in WEIGHTS:
        combination = np.einsum('i,iab->ab', weights, charges)
        eigenvalues, vectors = np.linalg.eigh(combination)
        tuples = np.array([np.diag(vectors.T @ q @ vectors) for q in charges]).T
        residual = max(float(np.max(np.linalg.norm(
            q @ vectors - vectors * tuples[:, i], axis=0)))
            for i, q in enumerate(charges))
        relative_residual = residual / max(1.0, float(np.max(np.abs(charges))))
        attempts.append({'weights': weights.tolist(), 'residual': residual,
                         'relative_residual': relative_residual})
        if residual < 1e-8 and relative_residual < 1e-11:
            break
    else:
        # Do not insert a penalty that could hide an unresolved spectrum.
        raise RuntimeError(f'No verified simultaneous basis: {attempts}')
    pairwise = tuples[:, None, :] - tuples[None, :, :]
    squared_gaps = np.einsum('ijk,ijk->ij', pairwise, pairwise)
    np.fill_diagonal(squared_gaps, np.inf)
    row, column = map(int, np.unravel_index(np.argmin(squared_gaps), squared_gaps.shape))
    return {
        'minimum_squared_joint_gap': float(squared_gaps[row, column]),
        'sites': sites.tolist(), 'g': coupling,
        'minimum_adjacent_spacing': float(np.min(np.diff(sites))),
        'closest_pair_indices_in_combination_basis': [row, column],
        'closest_pair_charge_vectors': [tuples[row].tolist(), tuples[column].tolist()],
        'max_joint_eigenvector_residual': residual,
        'relative_joint_residual': relative_residual,
        'combination_weights': weights.tolist(),
        'minimum_combination_eigenvalue_spacing': float(np.min(np.diff(eigenvalues))),
        'combination_attempts': attempts,
        'sum_charge_identity_max_error': float(np.max(np.abs(charges.sum(axis=0)-M*np.eye(DIM)))),
        'max_commutator_entry': max(float(np.max(np.abs(q @ r-r @ q)))
                                    for q in charges for r in charges),
    }


class CandidateFound(Exception):
    pass


def main():
    evaluations, best, improvements = 0, None, []
    worst_residual, multiple_combination_count = 0.0, 0

    def objective(x, stop=True):
        nonlocal evaluations, best, worst_residual, multiple_combination_count
        if evaluations >= MAX_EVALUATIONS:
            raise RuntimeError('Hard evaluation cap reached')
        evaluations += 1
        sites, coupling = decode(x)
        detail = spectrum(sites, coupling)
        worst_residual = max(worst_residual, detail['max_joint_eigenvector_residual'])
        multiple_combination_count += int(len(detail['combination_attempts']) > 1)
        value = detail['minimum_squared_joint_gap']
        if best is None or value < best['minimum_squared_joint_gap']:
            best = dict(detail, optimization_coordinates=np.asarray(x).tolist(),
                        evaluation=evaluations)
            improvements.append({'evaluation': evaluations, 'value': value})
        if stop and value < THRESHOLD - ROBUST_MARGIN:
            raise CandidateFound
        return value

    rng = np.random.default_rng(SEED)
    initial_population = rng.uniform(0, 1, size=(60, 5))
    initial_population[:, 4] *= 16
    equal = [1.0] * 5
    cluster_left = [MIN_SPACING] * 4 + [5-4*MIN_SPACING]
    cluster_right = list(reversed(cluster_left))
    symmetric_cluster = [MIN_SPACING, MIN_SPACING, 5-4*MIN_SPACING,
                         MIN_SPACING, MIN_SPACING]
    starts = [(name, spacings, g) for name, spacings in (
        ('equally_spaced', equal), ('left_cluster', cluster_left),
        ('right_cluster', cluster_right), ('split_cluster', symmetric_cluster))
        for g in (0.0, 0.1, 1.0, 16.0)]
    for i, (_, spacings, coupling) in enumerate(starts):
        initial_population[i] = encode(spacings, coupling)
    de_summary, local_summary, candidate = None, None, False
    try:
        de = differential_evolution(
            objective, [(0, 1)] * 4 + [(0, 16)], seed=SEED,
            init=initial_population, maxiter=59, popsize=12, polish=False,
            tol=0, atol=0, workers=1, updating='immediate')
        de_summary = {'nfev': int(de.nfev), 'nit': int(de.nit),
                      'success': bool(de.success), 'message': str(de.message),
                      'fun': float(de.fun)}
        local = minimize(objective, np.array(best['optimization_coordinates']),
                         method='Powell', bounds=[(0, 1)] * 4 + [(0, 16)],
                         options={'maxfev': 480, 'xtol': 1e-10, 'ftol': 1e-12})
        local_summary = {'nfev': int(local.nfev), 'nit': int(local.nit),
                         'success': bool(local.success), 'message': str(local.message),
                         'fun': float(local.fun)}
    except CandidateFound:
        candidate = True

    # One counted independent recomputation of the selected best coordinates.
    objective(np.array(best['optimization_coordinates']), stop=False)
    rational = {
        'sites': [str(Fraction(s).limit_denominator(65536)) for s in best['sites']],
        'g': str(Fraction(best['g']).limit_denominator(65536)),
        'exact_certificate_required': True,
    }
    result = {
        'status': 'NUMERICAL_CANDIDATE_REQUIRES_EXACT_CERTIFICATION' if candidate
                  else 'FINITE_NONFALSIFICATION_ONLY',
        'scope': 'One deterministic bounded N6 M3 optimization; native physical joint charge vectors.',
        'N': N, 'M': M, 'dimension': DIM,
        'native_charge_convention': 'Q_i=n_i+(g/2)*sum_j(SWAP_ij-I)/(eps_i-eps_j)',
        'constraints': {'eps_0': 0, 'eps_5': 5, 'minimum_spacing': '1/64', 'g_interval': [0, 16]},
        'seed': SEED, 'evaluation_cap': MAX_EVALUATIONS,
        'evaluation_count': evaluations, 'threshold_1_over_N': THRESHOLD,
        'robust_violation_margin': ROBUST_MARGIN,
        'differential_evolution': de_summary, 'powell_polish': local_summary,
        'initial_named_starts': [{'name': name, 'spacings': spacings, 'g': g}
                                 for name, spacings, g in starts],
        'best': best, 'improvement_history': improvements,
        'worst_accepted_joint_residual': worst_residual,
        'multiple_combination_evaluation_count': multiple_combination_count,
        'rationalized_best_for_parent_only': rational,
        'versions': {'numpy': np.__version__, 'scipy': scipy.__version__},
        'claim_gates': {'all_parameter_lower_bound': False, 'all_N_gap': False,
                        'exact_counterexample': False, 'efficient_algorithm': False,
                        'hardness': False, 'quantum_execution': False},
    }
    Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in (
        'status', 'evaluation_count', 'best', 'worst_accepted_joint_residual',
        'multiple_combination_evaluation_count')}, indent=2))


if __name__ == '__main__':
    main()

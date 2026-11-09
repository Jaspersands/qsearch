"""One predeclared continuation: q512,k128,seed3101; no sweep or tuning."""
from pathlib import Path
from types import SimpleNamespace
from fractions import Fraction
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research.classical_baselines.scalar_opi_fft_probe import tables, arithmetic, prange
from research.classical_baselines.scalar_opi_fourier_elimination import eliminate
from theorems.explicit_quadratic_opi import field, filter_bound


def main():
    started = time.monotonic()
    t, q, k, seed = 9, 512, 128, 3101
    A = tables(t, seed)
    row = {'t': t, 'q': q, 'm': q-1, 'k': k, 'seed': seed,
           'field_modulus': list(map(int, field(t).modulus().coeffs())),
           'tables': [[i for i, value in enumerate(a) if value] for a in A[1:]]}
    report = {'status': 'PREDECLARED_INPUT_SAVED_BEFORE_TEST', 'row': row,
              'contract': 'SCALAR_OPI_FOURIER_ELIMINATION.md: Predeclared next-size test',
              'new_seeds_or_parameter_tuning': False,
              'asymptotic_or_matched_runtime_claimed': False}
    path = Path(__file__).with_suffix('.json')
    if path.exists():
        previous = json.loads(path.read_text())['row']
        assert all(previous[key] == row[key] for key in row), 'Input must not change on replay'
    path.write_text(json.dumps(report, indent=2)+'\n')
    print('Saved original q512 k128 seed3101 tables and modulus before test.', flush=True)
    quantum = filter_bound(SimpleNamespace(dimension=k, length=q-1))
    row['dqi_rational_filter'] = quantum
    row['dqi_mean_lower'] = quantum['expected_score_lower']
    row['dqi_mean_lower_decimal'] = quantum['expected_score_lower_decimal']
    arithmetic(t)
    row['prange'] = prange(t, k, A, seed+10_000, 32)
    print('Prange32', row['prange']['best']['hits'],
          'DQI mean enclosure', [float(Fraction(quantum[key])*(q-1))
                                for key in ('expected_score_lower', 'expected_score_upper')], flush=True)
    row['algorithm_h_greedy'] = eliminate(t, k, A)
    report['status'] = 'NATIVE_WITNESS_SAVED_BEFORE_COMPARISON'
    path.write_text(json.dumps(report, indent=2)+'\n')
    score = row['algorithm_h_greedy']['hits']
    row['meets_rational_filter_mean_lower_bound'] = Fraction(score, q-1) >= Fraction(row['dqi_mean_lower'])
    report['status'] = 'ONE_PREDECLARED_NEXT_SIZE_CASE_COMPLETE_NOT_ASYMPTOTIC_EVIDENCE'
    report['wall_seconds_including_preprocessing'] = time.monotonic()-started
    path.write_text(json.dumps(report, indent=2)+'\n')
    print('AlgorithmH', score, 'meets DQI lower', row['meets_rational_filter_mean_lower_bound'],
          'seconds', report['wall_seconds_including_preprocessing'], flush=True)


if __name__ == '__main__':
    main()

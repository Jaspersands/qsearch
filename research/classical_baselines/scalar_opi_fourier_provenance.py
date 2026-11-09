"""Replay saved parities to diagnose row mixing, without selecting new ones.

Uses the probe's initial Fourier lift; independent algebra/field verification
is separately in scalar_opi_fourier_sage_check.py. This is provenance and
gain accounting on the same six cases, not independent correctness evidence.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research.classical_baselines.scalar_opi_fourier_elimination import score_spectrum


def main():
    source_path = ROOT / 'research/classical_baselines/scalar_opi_fft_probe.json'
    run_path = ROOT / 'research/classical_baselines/scalar_opi_fourier_elimination.json'
    source = json.loads(source_path.read_text())
    run = json.loads(run_path.read_text())
    results = []
    for native, saved in zip(source['rows'], run['rows']):
        q, k, t = native['q'], native['k'], native['t']
        assert (q, native['seed']) == (saved['q'], saved['seed'])
        accepted = [[0]*q for _ in range(q)]
        for point, targets in enumerate(native['tables'], 1):
            for target in targets:
                accepted[point][target] = 1
        _, terms = score_spectrum(t, k, accepted)
        rows = [dict(row) | {0: q//2} for row in terms]
        touched, selected_mixed, single_gain, mixed_gain = set(), 0, 0, 0
        first_alias = first_mixed = None
        checkpoints = []
        last_mean = (q-1)*q//2
        n = k*t
        for step in saved['algorithm_h_greedy']['trajectory']:
            index = step['step']
            a, bit = int(step['selected_mask_hex'], 16), step['fixed_parity']
            pivot = a & -a
            owners = [(i, row[a]) for i, row in enumerate(rows) if row.get(a)]
            assert sum(w for _, w in owners) == step['selected_signed_weight']
            if len(owners) > 1:
                selected_mixed += 1
                mixed_gain += abs(step['selected_signed_weight'])
                if first_mixed is None:
                    first_mixed = {'step': index, 'owner_count': len(owners),
                                   'mean_before_numerator': last_mean}
            else:
                assert len(owners) == 1
                single_gain += abs(step['selected_signed_weight'])
                touched.add(owners[0][0])
            for i, row in enumerate(rows):
                child = {}
                for mask, weight in row.items():
                    if mask & pivot:
                        mask ^= a
                        if bit:
                            weight = -weight
                    child[mask] = child.get(mask, 0) + weight
                rows[i] = {mask: weight for mask, weight in child.items() if weight}
            mean = sum(row.get(0, 0) for row in rows)
            assert mean == step['mean_numerator']
            if first_alias is None:
                seen = set()
                for row in rows:
                    masks = set(row) - {0}
                    intersection = seen & masks
                    if intersection:
                        first_alias = {
                            'after_step': index,
                            'remaining_free_bits': n-index,
                            'rows_selected_before_first_alias': len(touched),
                            'mean_numerator': mean,
                        }
                        break
                    seen.update(masks)
            if index in {n//4, n//2, 3*n//4, n-t, len(saved['algorithm_h_greedy']['trajectory'])}:
                constants = [row.get(0, 0) for row in rows]
                checkpoints.append({
                    'after_step': index, 'mean_numerator': mean,
                    'rows_with_constant_score_one': sum(c == q for c in constants),
                    'row_mean_numerator_histogram': {
                        str(c): constants.count(c) for c in sorted(set(constants))},
                })
            last_mean = mean
        result = {
            'q': q, 'k': k, 'seed': native['seed'], 'denominator': q,
            'first_nonzero_cross_row_support_alias': first_alias,
            'first_selected_mixed_row_frequency': first_mixed,
            'selected_mixed_row_steps': selected_mixed,
            'gain_on_selected_single_row_frequencies_numerator': single_gain,
            'gain_on_selected_mixed_row_frequencies_numerator': mixed_gain,
            'checkpoints': checkpoints,
        }
        assert single_gain + mixed_gain == saved['algorithm_h_greedy']['total_gain_numerator']
        results.append(result)
        print(q, native['seed'], 'first_alias', first_alias, 'mixed_gain', mixed_gain/q, flush=True)
    output = {
        'status': 'SAME_SIX_CASES_PROVENANCE_NOT_ASYMPTOTIC_EVIDENCE',
        'input_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (source_path, run_path)},
        'scope': 'Nonzero row Fourier support collisions, not full row-space intersections; single-row selections after aliases need not satisfy the early direct-sum invariant.',
        'rows': results,
    }
    (Path(__file__).with_suffix('.json')).write_text(json.dumps(output, indent=2)+'\n')


if __name__ == '__main__':
    main()

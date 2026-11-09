"""One native-table Algorithm H probe; exact signed Walsh restriction.

Known weighted-parity elimination: Crowston et al., arXiv:1104.1135,
Section 2, Reduction Rule 1 and Algorithm H.  The choice here is the
largest absolute current coefficient.  No approximation guarantee is
asserted for this greedy choice on scalar OPI.
"""
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research.classical_baselines.scalar_opi_fft_probe import arithmetic
from theorems.explicit_quadratic_opi import encoded, field


def walsh(values):
    """Unnormalized integer Walsh transform in the supplied binary basis."""
    out = list(map(int, values))
    half = 1
    while half < len(out):
        for start in range(0, len(out), 2 * half):
            for j in range(start, start + half):
                a, b = out[j], out[j + half]
                out[j], out[j + half] = a + b, a - b
        half *= 2
    return out


def lift_basis(t, k, point, mul):
    """Transpose of monomial evaluation, with coefficient bits j*t+l."""
    lifts = [0] * t
    power = 1
    for j in range(k):
        for bit in range(t):
            value = int(mul[power, 1 << bit])
            for output_bit in range(t):
                if (value >> output_bit) & 1:
                    lifts[output_bit] |= 1 << (j * t + bit)
        power = int(mul[power, point])
    return lifts


def score_spectrum(t, k, accepted):
    """F(z)=sum_mask weights[mask] (-1)^<mask,z> / q, exactly."""
    q, _, _, mul, *_ = arithmetic(t)
    weights = {}
    row_nonzero_terms = []
    for point in range(1, q):
        lifts = lift_basis(t, k, point, mul)
        masks = [0] * q
        for a in range(1, q):
            low = a & -a
            masks[a] = masks[a ^ low] ^ lifts[low.bit_length() - 1]
        row_terms = []
        for mask, coefficient in zip(masks, walsh(accepted[point])):
            if coefficient:
                weights[mask] = weights.get(mask, 0) + coefficient
                if mask:
                    row_terms.append((mask, coefficient))
        row_nonzero_terms.append(row_terms)
    weights = {a: w for a, w in weights.items() if w}
    assert weights.get(0, 0) == (q - 1) * q // 2
    return weights, row_nonzero_terms


def restrict(weights, parity, bit):
    """Substitute one free bit, retaining original positions for the rest."""
    assert parity and bit in (0, 1)
    pivot = parity & -parity
    result = {}
    counts = {}
    for mask, coefficient in weights.items():
        if mask & pivot:
            mask ^= parity
            if bit:
                coefficient = -coefficient
        result[mask] = result.get(mask, 0) + coefficient
        counts[mask] = counts.get(mask, 0) + 1
    assert all(not (mask & pivot) for mask in result)
    merged = sum(count > 1 for mask, count in counts.items() if mask)
    cancelled = sum(value == 0 for mask, value in result.items() if mask)
    return {a: w for a, w in result.items() if w}, pivot, merged, cancelled


def recover_assignment(constraints):
    value = 0  # Unfixed free coordinates may be chosen arbitrarily.
    for parity, bit, pivot in reversed(constraints):
        if ((value & parity).bit_count() & 1) != bit:
            value ^= pivot
    assert all(((value & a).bit_count() & 1) == b for a, b, _ in constraints)
    return value


def native_word(t, k, assignment):
    q, R, elements, *_ = arithmetic(t)
    coefficients = [(assignment >> (j * t)) & (q - 1) for j in range(k)]
    polynomial = R.zero()
    power = R.one()
    for coefficient in coefficients:
        polynomial += power * elements[coefficient]
        power *= R.gen()
    assert polynomial.is_zero() or polynomial.degree() < k
    return coefficients, [encoded(polynomial(a)) for a in elements[1:]]


def eliminate(t, k, accepted):
    started = time.monotonic()
    q = 1 << t
    weights, _ = score_spectrum(t, k, accepted)
    initial_support = len(weights) - 1
    constraints, trajectory = [], []
    visits = 0
    free = (1 << (k * t)) - 1
    gain = 0
    while any(weights.keys()):
        # Deterministic ties use the smallest frequency, not hidden data.
        parity = min((a for a in weights if a), key=lambda a: (-abs(weights[a]), a))
        coefficient = weights[parity]
        bit = int(coefficient < 0)
        before = weights.get(0, 0)
        support_before = len(weights) - 1
        visits += len(weights)
        assert parity & ~free == 0
        weights, pivot, merged, cancelled = restrict(weights, parity, bit)
        free ^= pivot
        constraints.append((parity, bit, pivot))
        gain += abs(coefficient)
        assert weights.get(0, 0) == before + abs(coefficient)
        assert len(constraints) <= k * t
        trajectory.append({
            'step': len(constraints), 'selected_mask_hex': hex(parity),
            'selected_signed_weight': coefficient, 'fixed_parity': bit,
            'pivot_bit': pivot.bit_length() - 1,
            'support_before': support_before, 'support_after': len(weights) - 1,
            'merged_nonconstant_buckets': merged,
            'cancelled_nonconstant_buckets': cancelled,
            'mean_numerator': weights.get(0, 0), 'mean_denominator': q,
        })
    assignment = recover_assignment(constraints)
    coefficients, word = native_word(t, k, assignment)
    hits = int(sum(accepted[i][value] for i, value in enumerate(word, 1)))
    assert weights.get(0, 0) == hits * q
    assert gain == hits * q - (q - 1) * q // 2
    return {
        'hits': hits, 'monomial_coefficients': coefficients, 'word': word,
        'binary_assignment_hex': hex(assignment),
        'initial_nonconstant_support': initial_support,
        'steps': len(constraints), 'unfixed_bits': free.bit_count(),
        'total_gain_numerator': gain, 'common_denominator': q,
        'trajectory': trajectory,
        'work': {'restriction_dictionary_entries_visited': visits,
                 'max_selection_entries_visited': visits,
                 'initial_walsh_integer_additions': (q - 1) * q * t,
                 'native_horner_evaluations': q - 1},
        'wall_seconds': time.monotonic() - started,
    }


def exact_controls():
    # All 307 affine subsets of the four coefficient bits of degree<2/F4.
    t, k, q = 2, 2, 4
    accepted = [[0] * q for _ in range(q)]
    for point, targets in ((1, (0, 1)), (2, (0, 1)), (3, (1, 2))):
        for value in targets:
            accepted[point][value] = 1
    initial, row_terms = score_spectrum(t, k, accepted)
    scores = {}
    for assignment in range(1 << (t * k)):
        _, word = native_word(t, k, assignment)
        scores[assignment] = sum(accepted[i][v] for i, v in enumerate(word, 1))
        value = sum(w * (-1 if (a & assignment).bit_count() & 1 else 1)
                    for a, w in initial.items())
        assert value == q * scores[assignment]
    queue = [(initial, (1 << (t * k)) - 1, tuple(scores))]
    seen = set()
    transitions = 0
    negative_restrictions = 0
    while queue:
        weights, free, points = queue.pop()
        if points in seen:
            continue
        seen.add(points)
        assert len(points) * weights.get(0, 0) == q * sum(scores[x] for x in points)
        for x in points:
            value = sum(w * (-1 if (a & x).bit_count() & 1 else 1)
                        for a, w in weights.items())
            assert value == q * scores[x]
        parity = free
        while parity:
            for bit in (0, 1):
                child, pivot, _, _ = restrict(weights, parity, bit)
                remaining = tuple(x for x in points if ((x & parity).bit_count() & 1) == bit)
                assert len(remaining) * 2 == len(points)
                assert child.get(0, 0) == weights.get(0, 0) + (-1 if bit else 1) * weights.get(parity, 0)
                transitions += 1
                negative_restrictions += int(weights.get(parity, 0) < 0)
                queue.append((child, free ^ pivot, remaining))
            parity = (parity - 1) & free
    assert len(seen) == 307 and negative_restrictions > 0
    # Frequencies from two DISTINCT native evaluation rows must alias with
    # the right sign, rather than being treated as independent messages.
    a, wa = row_terms[0][0]
    b, wb = row_terms[1][0]
    assert a != b and wa == wb == 2
    plus, _, _, _ = restrict({a: wa, b: wb}, a ^ b, 0)
    minus, _, _, _ = restrict({a: wa, b: wb}, a ^ b, 1)
    assert list(plus.values()) == [4] and minus == {}
    result = eliminate(t, k, accepted)
    assert result['hits'] == scores[int(result['binary_assignment_hex'], 16)]
    return {'native_field_mapping_assignments': len(scores),
            'all_affine_sections': len(seen),
            'exact_signed_restriction_transitions': transitions,
            'negative_weight_cases': negative_restrictions,
            'distinct_row_alias_sum_and_cancellation': True,
            'backsubstitution_native_score': True}


def main():
    started = time.monotonic()
    controls = exact_controls()
    source_path = ROOT / 'research/classical_baselines/scalar_opi_fft_probe.json'
    source = json.loads(source_path.read_text())
    assert [(r['q'], r['seed']) for r in source['rows']] == [
        (q, seed) for q in (16, 64, 256) for seed in (3101, 3102)]
    rows = []
    for old in source['rows']:
        t, q, k = old['t'], old['q'], old['k']
        assert list(map(int, field(t).modulus().coeffs())) == old['field_modulus']
        accepted = [[0] * q for _ in range(q)]
        for point, targets in enumerate(old['tables'], 1):
            assert len(targets) == len(set(targets)) == q // 2
            for value in targets:
                accepted[point][value] = 1
        result = eliminate(t, k, accepted)
        row = {key: old[key] for key in ('t', 'q', 'm', 'k', 'seed', 'field_modulus',
                                        'dqi_mean_lower', 'dqi_mean_lower_decimal')}
        row.update({'algorithm_h_greedy': result,
                    'prange32_best': old['prange']['best']['hits'],
                    'previous_freeze_aware_sc': old['freeze_aware_sc']['hits']})
        rows.append(row)
        print(f'q={q} k={k} seed={old["seed"]}: AlgorithmH={result["hits"]}, '
              f'Prange32={row["prange32_best"]}, steps={result["steps"]}, '
              f'seconds={result["wall_seconds"]:.3f}', flush=True)
    report = {
        'status': 'BOUNDED_NATIVE_CLASSICAL_PROBE_NOT_ASYMPTOTIC_EVIDENCE',
        'method': 'Known Algorithm H; greedy maximum absolute current Walsh weight',
        'primary_source': 'Crowston et al., arXiv:1104.1135, Section 2, Reduction Rule 1 and Algorithm H',
        'input_tables': 'research/classical_baselines/scalar_opi_fft_probe.json',
        'source': 'Same six retained IID half-table cases, original nonzero field points, monomial degree<k; no reroll',
        'normalization': 'Unnormalized integer table Walsh coefficients; common denominator q throughout',
        'controls': controls, 'rows': rows,
        'wall_seconds': time.monotonic() - started,
        'quantum_circuit_executed': False,
        'matched_runtime_comparison_claimed': False,
        'novel_algorithm_claimed': False,
        'hardness_or_asymptotic_advantage_claimed': False,
    }
    path = ROOT / 'research/classical_baselines/scalar_opi_fourier_elimination.json'
    path.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()

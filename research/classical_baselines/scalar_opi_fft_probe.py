"""One bounded native-table experiment; no exact-posterior or speedup claim."""
from pathlib import Path
from types import SimpleNamespace
from functools import lru_cache
import json
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from flint import fq_default_poly_ctx
from theorems.explicit_quadratic_opi import field, element, encoded, filter_bound


@lru_cache(None)
def arithmetic(t):
    q = 1 << t
    F, R = field(t), fq_default_poly_ctx(field(t))
    els = [element(t, a) for a in range(q)]
    mul = np.array([[encoded(a*b) for b in els] for a in els], dtype=np.int32)
    x, W, scales = R.gen(), R.gen(), []
    basis = [R.one()]
    for r in range(t):
        scale = W(els[1 << r])
        S = W / scale
        scales.append(np.array([encoded(S(a)) for a in els], dtype=np.int32))
        basis += [p*S for p in basis]
        W = W*W + W*scale
    assert all(p.degree() == j for j, p in enumerate(basis))
    return q, R, els, mul, scales, basis


def tables(t, seed):
    q = 1 << t
    rng = random.Random(seed)
    a = np.zeros((q, q), dtype=np.int32)
    for i in range(1, q):
        a[i, rng.sample(range(q), q//2)] = 1
    return a  # Row0 is NEUTRAL, not a sampled half-set.


def sc(t, k, accepted, aware):
    q, R, els, mul, scales, basis = arithmetic(t)
    work = {'pair_candidates': 0, 'high_candidates': 0, 'decisions': 0}
    symbols = np.arange(q, dtype=np.int32)

    def messages(n, beta, cutoff):
        if n == 1:
            yield 0, accepted[beta].copy()
            return
        half = n//2
        r = half.bit_length()-1
        s = int(scales[r][beta])
        child_cut = min(cutoff, half) if cutoff <= half else half
        left = messages(half, beta, child_cut)
        right = messages(half, beta ^ half, child_cut)
        jl, L = next(left)
        jr, RR = next(right)
        for step in range(half):
            assert jl == jr
            high_frozen = jl+half >= cutoff
            if aware and high_frozen:
                low = L + RR
                work['pair_candidates'] += q
            elif s == 0:
                low = L.copy()  # The other maximum is a common constant.
            elif s == 1:
                low = RR.copy()
            else:
                aa = symbols[:, None] ^ mul[s][None, :]
                bb = symbols[:, None] ^ mul[s ^ 1][None, :]
                low = (L[aa]+RR[bb]).max(axis=1)
                work['pair_candidates'] += q*q
            c = yield jl, low-low.max()
            high = L[c ^ mul[s]]+RR[c ^ mul[s ^ 1]]
            work['high_candidates'] += q
            v = yield jl+half, high-high.max()
            av, bv = c ^ int(mul[s, v]), c ^ int(mul[s ^ 1, v])
            if step+1 < half:
                jl, L = left.send(av)
                jr, RR = right.send(bv)
            else:
                for child, value in ((left, av), (right, bv)):
                    try:
                        child.send(value)
                    except StopIteration:
                        pass
                    else:
                        raise AssertionError('child did not terminate')

    coeff = [0]*q
    gen = messages(q, 0, k)
    j, likelihood = next(gen)
    for step in range(q):
        c = int(likelihood.argmax()) if j < k else 0
        coeff[j] = c
        work['decisions'] += 1
        if step+1 < q:
            j, likelihood = gen.send(c)
        else:
            try:
                gen.send(c)
            except StopIteration:
                pass
            else:
                raise AssertionError('root did not terminate')
    P = R.zero()
    for c, b in zip(coeff[:k], basis[:k]):
        P += b*els[c]
    assert P.is_zero() or P.degree() < k
    values = [encoded(P(a)) for a in els]  # Independent native Horner.
    hits = int(accepted[np.arange(q), values].sum())
    return {'hits': hits, 'message_subspace_basis': coeff[:k],
            'monomial_coefficients': [encoded(c) for c in P.coeffs()],
            'word': values[1:], 'work': work}


def prange(t, k, accepted, seed, restarts):
    q, R, els, *_ = arithmetic(t)
    rng = random.Random(seed)
    scores, best = [], None
    for _ in range(restarts):
        I = rng.sample(range(1, q), k)  # Independent of the accepted tables.
        ys = [els[rng.choice(np.flatnonzero(accepted[i]).tolist())] for i in I]
        Q = R.one()
        for i in I:
            Q *= R.gen()-els[i]
        derivative = Q.derivative()
        P = R.zero()
        for i, y in zip(I, ys):
            quotient, remainder = divmod(Q, R.gen()-els[i])
            assert remainder.is_zero()
            P += quotient*(y/derivative(els[i]))
        assert P.is_zero() or P.degree() < k
        assert all(P(els[i]) == y for i, y in zip(I, ys))
        word = [encoded(P(a)) for a in els]
        hits = int(accepted[np.arange(q), word].sum())
        scores.append(hits)
        if best is None or hits > best['hits']:
            best = {'hits': hits, 'monomial_coefficients': [encoded(c) for c in P.coeffs()],
                    'word': word[1:]}
    return {'scores': scores, 'best': best, 'restarts': restarts,
            'native_polynomial_evaluations': restarts*(q-1+k)}


def main():
    start = time.monotonic()
    controls = []
    for t in (2, 3):
        q, R, els, *_ = arithmetic(t)
        A = tables(t, 700+t)
        for aware in (False, True):
            assert sc(t, q, A, aware)['hits'] == q-1
        const = sc(t, 1, A, True)
        assert const['hits'] == int(A.sum(axis=0).max())
        controls.append({'t': t, 'unrestricted_exact': True, 'constant_exact': True})
    A = tables(4, 704)
    original = sc(4, 4, A, False)
    for seed in range(10):
        B = tables(4, 800+seed)
        B[:4] = A[:4]
        assert sc(4, 4, B, False)['message_subspace_basis'] == original['message_subspace_basis']
    rows = []
    for t in (4, 6, 8):
        q, *_ = arithmetic(t)
        k = q//4
        quantum = filter_bound(SimpleNamespace(dimension=k, length=q-1))
        for seed in (3101, 3102):
            A = tables(t, seed)
            ordinary = sc(t, k, A, False)
            aware = sc(t, k, A, True)
            baseline = prange(t, k, A, seed+10_000, 32)
            row = {'t': t, 'q': q, 'm': q-1, 'k': k, 'seed': seed,
                   'tables': [np.flatnonzero(a).tolist() for a in A[1:]],
                   'field_modulus': list(map(int, field(t).modulus().coeffs())),
                   'ordinary_sc': ordinary, 'freeze_aware_sc': aware, 'prange': baseline,
                   'dqi_mean_lower': quantum['expected_score_lower'],
                   'dqi_mean_lower_decimal': quantum['expected_score_lower_decimal']}
            rows.append(row)
            print(f'q={q} k={k} seed={seed}: ordinary={ordinary["hits"]} aware={aware["hits"]} '
                  f'Prange32={baseline["best"]["hits"]} DQI_mean>={quantum["expected_score_lower_decimal"]*(q-1):.3f}/{q-1}', flush=True)
    report = {'status': 'FINITE_CLASSICAL_FALSIFIER_NOT_ASYMPTOTIC_EVIDENCE',
              'heuristic': 'max-sum SC; condition current high freezes; future correlations not exact',
              'original_source': 'IID explicit half tables, nonzero F2^t points, degree<k; neutral point0',
              'controls': controls, 'ordinary_suffix_invariance_controls': 10,
              'wall_seconds': time.monotonic()-start, 'rows': rows,
              'quantum_circuit_executed': False, 'matched_runtime_comparison_claimed': False}
    path = ROOT/'research/classical_baselines/scalar_opi_fft_probe.json'
    path.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()

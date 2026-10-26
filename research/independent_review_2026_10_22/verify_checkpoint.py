"""Independent bounded checks; no repository imports or shared writes.

Run with python3 -B. Reads resident witness receipts, verifies their native
equations with polynomial arithmetic, and writes only beside this script.
Finite controls falsify formula mistakes, not asymptotic complexity claims.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations
from math import comb, isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent


def rem(a, modulus):
    while a and a.bit_length() >= modulus.bit_length():
        a ^= modulus << (a.bit_length() - modulus.bit_length())
    return a


def mul(a, b, modulus):
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        b >>= 1
    return rem(p, modulus)


def gcd(a, b):
    while b:
        a, b = b, rem(a, b)
    return a


def inverse(a, modulus):
    if not a:
        return 0
    u, v, s, t = a, modulus, 1, 0
    while u != 1:
        assert u, "nonunit under supplied modulus"
        shift = u.bit_length() - v.bit_length()
        if shift < 0:
            u, v, s, t = v, u, t, s
            shift = -shift
        u ^= v << shift
        s ^= t << shift
    return rem(s, modulus)


def trace(a, n, modulus):
    answer = 0
    for _ in range(n):
        answer ^= a
        a = mul(a, a, modulus)
    assert answer in (0, 1)
    return answer


def irreducible(n, modulus):
    assert modulus.bit_length() == n + 1
    x = 2
    for j in range(1, n + 1):
        x = mul(x, x, modulus)
        if j <= n // 2 and gcd(x ^ 2, modulus) != 1:
            return False
    return x == 2


def log2_up(x):
    if not x:
        return None
    k = x.numerator.bit_length() - x.denominator.bit_length()
    p = F(1 << k) if k >= 0 else F(1, 1 << -k)
    return k if x <= p else k + 1


def ratio(x):
    return [x.numerator, x.denominator]


def verify_witnesses():
    source = RESEARCH / 'classical_baselines/reciprocal_trace_flats.json'
    raw = source.read_bytes()
    report = json.loads(raw)
    result = []
    for case in report['cases']:
        data, word = case['input'], case['witness']
        n, points, k, targets, modulus = (
            data['bits'], data['points'], data['checks'],
            data['targets'], data['field_modulus'])
        assert len(points) == n*n == len(word) == len(targets)
        assert len(set(points)) == len(points) and k == n*n//8
        assert irreducible(n, modulus)
        assert all(0 <= x < 1 << n for x in points + word)
        syndromes = [0]*k
        wrong_bits = []
        for i, (alpha, x, b) in enumerate(zip(points, word, targets)):
            z = inverse(x, modulus)
            assert (x == 0 and z == 0) or mul(x, z, modulus) == 1
            if trace(z, n, modulus) != b:
                wrong_bits.append(i)
            v = x
            for j in range(k):
                syndromes[j] ^= v
                v = mul(v, alpha, modulus)
        assert not any(syndromes) and not wrong_bits
        result.append({'n': n, 'N': len(points), 'K': k,
                       'modulus': modulus, 'irreducible': True,
                       'native_valid': True, 'bad_trace_positions': wrong_bits,
                       'nonzero_syndromes': sum(bool(s) for s in syndromes),
                       'input_and_witness_sha256': sha256(json.dumps(
                           [data, word], sort_keys=True).encode()).hexdigest()})
    return {'artifact_sha256': sha256(raw).hexdigest(), 'cases': result,
            'scope': 'Verification of existing witnesses, not rerunning construction'}


def quantum_budget(n):
    q, N = 1 << n, n*n
    K, w = N//8, 3*N//5
    a, t = N-w, N-w-K+1
    gap = a*a-N*(K-1)
    L = N*(a-K+1)//gap
    s = N*(K-1)//gap+1
    degree = s*a-1
    ell = degree//(K-1)
    monomials = sum(degree-(K-1)*j+1 for j in range(ell+1))
    constraints = N*s*(s+1)//2
    assert monomials > constraints
    root = isqrt(q)+int(isqrt(q)**2 < q)
    beta = min(F(1), F(1+2*root, q))
    delta = F(sum(comb(N, j) for j in range(w+1, N+1)), 1 << N)
    ambiguity = min(F(1), (q**K-1)*comb(N, t)*min(F(1, 2), F(4, q))**t)
    eta = (q**K-1)*beta**(N-K+1)
    failure = 3*delta+(2*L+1)*ambiguity+2*eta
    return {'n': n, 'N': N, 'K': K, 'w': w, 's': s, 'L': L,
            'monomials': monomials, 'constraints': constraints,
            'tail_log2_upper': log2_up(delta),
            'ambiguity_log2_upper': log2_up(ambiguity),
            'coherent_excess_log2_upper': log2_up(eta),
            'failure_log2_upper': log2_up(failure),
            'scope': 'Exact rational mathematical bound, not a quantum run'}


def tiny_mixture():
    # F8, H=(1,1,1,1), with actual field inverse-trace constraints.
    n, modulus, N, K, M = 3, 0b1011, 4, 1, 3
    assert irreducible(n, modulus)
    pred = [trace(inverse(x, modulus), n, modulus) for x in range(8)]
    words = [w+(w[0]^w[1]^w[2],) for w in product(range(8), repeat=3)]
    patterns = [tuple(pred[x] for x in w) for w in words]
    rows = []
    for b in product(range(2), repeat=N):
        counts = [sum(p[i] == b[i] for i in range(N)) for p in patterns]
        full = sum(c == N for c in counts)
        # Check exact MDS conditional masses, including all information sets.
        for size in range(N-K+1):
            for S in combinations(range(N), size):
                count = sum(all(p[i] == b[i] for i in S) for p in patterns)
                assert count == len(words)//(1 << size)
        weights = [M**c for c in counts]
        truncated = [sum(comb(c, s)*(M-1)**s for s in range(min(c,N-K)+1))
                     for c in counts]
        Z, Z0 = sum(weights), sum(truncated)
        tv = sum(abs(F(a,Z)-F(t,Z0)) for a,t in zip(weights,truncated))/2
        removed = F(Z-Z0,Z)
        assert tv <= removed
        systematic_success = F(full, (8//2)**(N-K))
        error = F(full, F(len(words), 1 << N))-1
        assert systematic_success == (1+error)*F(1, 1 << K)
        nu_success = F(sum(t for t,c in zip(truncated,counts) if c == N),Z0)
        assert nu_success <= systematic_success
        rows.append({'target': list(b), 'solution_count': full,
                     'systematic_success': ratio(systematic_success),
                     'truncated_mixture_success': ratio(nu_success),
                     'pi_success': ratio(F(full*M**N,Z)),
                     'tv': ratio(tv), 'discarded_joint_mass': ratio(removed)})
    return {'n': n, 'N': N, 'K': K, 'M': M, 'enumerated_codewords': len(words),
            'targets_checked': len(rows), 'rows': rows,
            'scope': 'Exact finite formula falsifier only'}


if __name__ == '__main__':
    result = {'witnesses': verify_witnesses(),
              'quantum_budgets': [quantum_budget(n) for n in (17,31,61)],
              'tiny_mixture': tiny_mixture()}
    result['checker_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    path = HERE / 'checkpoint_verification.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'witnesses': result['witnesses'],
                      'quantum_budgets': result['quantum_budgets'],
                      'tiny_mixture_targets_checked': result['tiny_mixture']['targets_checked']},
                     indent=2))
